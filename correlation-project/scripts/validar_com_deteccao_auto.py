"""
Script de validação com DETECÇÃO AUTOMÁTICA DE HARDWARE.

Detecta se está no PC CASA ou TRABALHO e ajusta automaticamente:
- Modelo Ollama
- Timeout
- Tamanho de histórico
- Batch size (casos simultâneos)
"""

import sys
from pathlib import Path

# Adicionar pasta utils ao path
sys.path.insert(0, str(Path(__file__).parent.parent / 'utils'))

try:
    from detector_hardware import detectar_e_configurar, salvar_config_auto
    DETECTOR_DISPONIVEL = True
except ImportError:
    print("⚠️  Detector de hardware não disponível, usando config padrão")
    DETECTOR_DISPONIVEL = False

import pandas as pd
import ollama
import json
from datetime import datetime


def carregar_ou_criar_config():
    """
    Carrega config_validacao.json ou cria automaticamente baseado no hardware.
    """
    config_file = Path('config_validacao.json')
    
    if config_file.exists():
        # Carregar config existente
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"[OK] Configuracao carregada: {config_file}")
        return config
    
    # Se não existe e detector disponível, criar automaticamente
    if DETECTOR_DISPONIVEL:
        print("\n[AUTO] Config nao encontrada. Criando automaticamente...")
        hardware, config_profile = detectar_e_configurar(verbose=True)
        
        config = config_profile.to_dict()
        salvar_config_auto(config_profile)
        
        return config
    
    # Fallback: config padrão
    print("[WARN] Usando configuracao padrao")
    return {
        'modelo': 'qwen2.5-ptbr:7b',
        'temperatura': 0.1,
        'timeout_segundos': 60,
        'tamanho_historico': 800,
        'batch_size': 1,
        'prompt_detalhes': {
            'incluir_transtorno': True,
            'incluir_rg': True,
            'incluir_pais': True,
            'formato_visual': True
        }
    }


def validar_caso_com_ia(caso, config):
    """
    Valida se dois BOs (desaparecimento e morte) referem-se à mesma pessoa.
    
    Args:
        caso: Série pandas com dados da correlação
        config: Dict com configurações (modelo, temperatura, etc)
        
    Returns:
        Dict com: validado, mesma_pessoa, confianca, justificativa, erro
    """
    
    # Extrair configurações
    modelo = config.get('modelo', 'qwen2.5-ptbr:7b')
    temperatura = config.get('temperatura', 0.1)
    timeout = config.get('timeout_segundos', 60)
    tam_hist = config.get('tamanho_historico', 800)
    prompt_det = config.get('prompt_detalhes', {})
    
    # Preparar dados
    transtorno = 'Sim' if caso.get('tem_transtorno_psiquiatrico') else 'Não'
    tipo_transtorno = caso.get('tipo_transtorno', 'Não informado')
    
    # Montar prompt com opções configuráveis
    prompt_base = f"""TAREFA: Analisar se os dois boletins de ocorrência abaixo são DA MESMA PESSOA.

═══════════════════════════════════════════════════════════════════
DESAPARECIMENTO
═══════════════════════════════════════════════════════════════════
BO: {caso['bo_desaparecimento']}
Data: {caso['data_desaparecimento']}
Local: {caso['cidade_desaparecimento']} - {caso['unidade_desaparecimento']}

RELATO DO DESAPARECIMENTO:
{caso['historico_desaparecimento'][:tam_hist]}

═══════════════════════════════════════════════════════════════════
ÓBITO/CADÁVER
═══════════════════════════════════════════════════════════════════
BO: {caso['bo_morte']}
Tipo: {caso['tipo_morte']}
Data: {caso['data_morte']} ({caso['dias_entre_eventos']} dias depois)
Local: {caso['cidade_morte']} - {caso['unidade_morte']}

RELATO DO ÓBITO:
{caso['historico_morte'][:tam_hist]}

═══════════════════════════════════════════════════════════════════
DADOS DA PESSOA PARA VALIDAÇÃO
═══════════════════════════════════════════════════════════════════
Nome: {caso['nome']}
Data Nascimento: {caso['data_nascimento']}
Mãe: {caso['nome_mae']}"""
    
    # Adicionar campos opcionais baseado na config
    if prompt_det.get('incluir_pais', True):
        prompt_base += f"\nPai: {caso['nome_pai']}"
    
    if prompt_det.get('incluir_rg', True):
        rg_completo = f"{caso['numero_rg']}" if pd.notna(caso.get('numero_rg')) else 'Não informado'
        prompt_base += f"\nRG: {rg_completo}"
    
    prompt_base += f"\nSexo: {caso['sexo']}"
    
    if prompt_det.get('incluir_transtorno', True):
        prompt_base += f"\nTranstorno Psiquiátrico: {transtorno} ({tipo_transtorno})"
    
    prompt_base += f"""

═══════════════════════════════════════════════════════════════════
ANÁLISE REQUERIDA
═══════════════════════════════════════════════════════════════════

Compare os dados de identificação nos dois BOs.
Avalie se o intervalo de {caso['dias_entre_eventos']} dias é coerente.

Responda APENAS com o JSON abaixo (sem texto adicional):
{{
    "mesma_pessoa": true,
    "confianca": 95,
    "justificativa": "Breve explicação"
}}"""
    
    try:
        response = ollama.chat(
            model=modelo,
            messages=[{'role': 'user', 'content': prompt_base}],
            options={
                'temperature': temperatura,
                'num_predict': 300
            },
            timeout=timeout
        )
        
        resposta_texto = response['message']['content'].strip()
        
        # Limpar resposta
        if '```json' in resposta_texto:
            resposta_texto = resposta_texto.split('```json')[1].split('```')[0].strip()
        elif '```' in resposta_texto:
            resposta_texto = resposta_texto.split('```')[1].split('```')[0].strip()
        
        resultado = json.loads(resposta_texto)
        
        return {
            'validado': True,
            'mesma_pessoa': resultado.get('mesma_pessoa', False),
            'confianca': int(resultado.get('confianca', 0)),
            'justificativa': resultado.get('justificativa', ''),
            'erro': None
        }
        
    except json.JSONDecodeError:
        return {
            'validado': False,
            'mesma_pessoa': None,
            'confianca': 0,
            'justificativa': '',
            'erro': f'Erro ao parsear JSON: {resposta_texto[:200]}'
        }
    except Exception as e:
        return {
            'validado': False,
            'mesma_pessoa': None,
            'confianca': 0,
            'justificativa': '',
            'erro': str(e)
        }


def main():
    """Executa validação com detecção automática de hardware"""
    
    print("\n" + "="*80)
    print("VALIDACAO COM IA - DETECCAO AUTOMATICA DE HARDWARE")
    print("="*80 + "\n")
    
    # Carregar ou criar configuração automaticamente
    config = carregar_ou_criar_config()
    
    print(f"\n[CONFIG] Configuracao Ativa:")
    print(f"   Modelo: {config['modelo']}")
    print(f"   Temperatura: {config['temperatura']}")
    print(f"   Timeout: {config['timeout_segundos']}s")
    print(f"   Histórico: {config['tamanho_historico']} chars")
    print(f"   Batch size: {config.get('batch_size', 1)}")
    print()
    
    # Carregar dados
    input_file = Path('output/correlacoes_unicas_deduplicadas.xlsx')
    output_file = Path('output/validacao_progresso.xlsx')
    
    if not input_file.exists():
        print(f"[ERRO] Arquivo nao encontrado: {input_file}")
        return
    
    df = pd.read_excel(input_file, sheet_name='FORTES - Únicas')
    print(f"[OK] {len(df)} casos carregados\n")
    
    # Carregar progresso existente
    if output_file.exists():
        df_prog = pd.read_excel(output_file)
        ja_validados = df_prog[df_prog['ia_validado'] == True].index.tolist()
        print(f"[INFO] Progresso anterior: {len(ja_validados)} casos ja validados")
    else:
        # Criar DataFrame de progresso
        df['ia_validado'] = False
        df['ia_mesma_pessoa'] = None
        df['ia_confianca'] = 0
        df['ia_justificativa'] = ''
        df['ia_erro'] = ''
        ja_validados = []
    
    # Processar casos não validados
    pendentes = [i for i in range(len(df)) if i not in ja_validados]
    
    if not pendentes:
        print("\n[OK] Todos os casos ja foram validados!")
        return
    
    print(f"[EXEC] Processando {len(pendentes)} casos pendentes...\n")
    
    confirmados = rejeitados = erros = 0
    conf_total = 0
    
    for idx in pendentes:
        caso = df.iloc[idx]
        
        print(f"[{idx+1}/{len(df)}] {caso['nome'][:30]}... ", end='', flush=True)
        
        resultado = validar_caso_com_ia(caso, config)
        
        if resultado['validado']:
            df.at[idx, 'ia_validado'] = True
            df.at[idx, 'ia_mesma_pessoa'] = resultado['mesma_pessoa']
            df.at[idx, 'ia_confianca'] = resultado['confianca']
            df.at[idx, 'ia_justificativa'] = resultado['justificativa']
            
            if resultado['mesma_pessoa']:
                confirmados += 1
                conf_total += resultado['confianca']
                print(f"[+] CONFIRMADA ({resultado['confianca']}%)")
            else:
                rejeitados += 1
                print(f"[-] REJEITADA ({resultado['confianca']}%)")
        else:
            erros += 1
            df.at[idx, 'ia_validado'] = False
            df.at[idx, 'ia_erro'] = resultado['erro']
            print(f"[!] ERRO: {resultado['erro'][:50]}")
        
        # Salvar progresso
        df.to_excel(output_file, index=False)
    
    # Estatísticas finais
    print("\n" + "="*80)
    print("[RESULTADO] VALIDACAO CONCLUIDA")
    print("="*80)
    print(f"[+] Confirmadas: {confirmados} ({confirmados/len(df)*100:.1f}%)")
    print(f"[-] Rejeitadas: {rejeitados} ({rejeitados/len(df)*100:.1f}%)")
    print(f"[!] Erros: {erros}")
    
    if confirmados > 0:
        print(f"[STAT] Confianca media (confirmadas): {conf_total/confirmados:.1f}%")
    
    print(f"\n[SAVE] Progresso salvo em: {output_file}")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
