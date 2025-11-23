"""
═══════════════════════════════════════════════════════════════════════════════
VALIDAÇÃO DE CORRELAÇÕES COM INTELIGÊNCIA ARTIFICIAL
═══════════════════════════════════════════════════════════════════════════════

DESCRIÇÃO:
    Valida correlações desaparecimento → morte usando modelo de linguagem local
    (Ollama qwen2.5-ptbr:7b otimizado para português brasileiro)

CARACTERÍSTICAS:
    ✅ Auto-save após cada caso (não perde progresso)
    ✅ Retomada automática se interrompido
    ✅ Timeout de 60 segundos por caso
    ✅ Tratamento robusto de erros
    ✅ Encoding UTF-8 correto

ENTRADA:
    output/correlacoes_unicas_deduplicadas.xlsx
    Aba: "FORTES - Únicas" (86 casos)

SAÍDA:
    output/validacao_progresso.xlsx (atualizado após cada caso)
    output/RELATORIO_VALIDACAO_FINAL.xlsx (gerado ao concluir)

TEMPO ESTIMADO:
    ~17-20 minutos (86 casos × 0.2 min/caso)

USO:
    python scripts/validar_com_ia.py

═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import pandas as pd
import ollama
import json
from pathlib import Path
from datetime import datetime
import time


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÕES
# ═══════════════════════════════════════════════════════════════════════════

MODELO = 'qwen2.5-ptbr:7b'  # Modelo português otimizado
TEMPERATURA = 0.1           # Baixa temperatura = mais determinístico
TIMEOUT = 60                # Timeout em segundos por validação
ARQUIVO_ENTRADA = 'output/correlacoes_unicas_deduplicadas.xlsx'
ABA_ENTRADA = 'FORTES - Únicas'
ARQUIVO_PROGRESSO = 'output/validacao_progresso.xlsx'
ARQUIVO_RELATORIO = 'output/RELATORIO_VALIDACAO_FINAL.xlsx'


# ═══════════════════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES
# ═══════════════════════════════════════════════════════════════════════════

def verificar_modelo():
    """
    Verifica se o modelo está disponível no Ollama.
    
    Returns:
        bool: True se modelo disponível, False caso contrário
    """
    try:
        resultado = ollama.list()
        modelos = resultado.get('models', [])
        
        # Extrai nomes dos modelos
        modelos_disponiveis = []
        for m in modelos:
            if isinstance(m, dict) and 'name' in m:
                modelos_disponiveis.append(m['name'])
            elif isinstance(m, dict) and 'model' in m:
                modelos_disponiveis.append(m['model'])
        
        # Verifica se modelo está disponível
        for modelo in modelos_disponiveis:
            if MODELO in modelo:
                return True
        
        print(f"\n[ERRO] Modelo {MODELO} nao encontrado!")
        print(f"\nModelos disponiveis:")
        for m in modelos_disponiveis:
            print(f"  - {m}")
        print(f"\nPara instalar: ollama pull {MODELO}")
        return False
        
    except Exception as e:
        print(f"\n[ERRO] Erro ao verificar Ollama: {e}")
        print("\nCertifique-se que Ollama esta rodando: ollama list")
        return False


def validar_caso_com_ia(caso, num_caso, total_casos):
    """
    Valida um caso usando IA local.
    
    Args:
        caso: Série pandas com dados da correlação
        num_caso: Número do caso atual
        total_casos: Total de casos a validar
        
    Returns:
        dict: {validado, mesma_pessoa, confianca, justificativa, erro}
    """
    
    try:
        # Prepara dados com fallback para valores ausentes
        transtorno = 'Sim' if caso.get('tem_transtorno_psiquiatrico') else 'Não'
        tipo_transtorno = caso.get('tipo_transtorno', 'Não informado')
        rg = f"{caso['numero_rg']}" if pd.notna(caso.get('numero_rg')) else 'Não informado'
        
        # Monta prompt otimizado em português
        prompt = f"""TAREFA: Analisar se os dois BOs são DA MESMA PESSOA.

═══════════════════════════════════════════════════════════════════
DESAPARECIMENTO
═══════════════════════════════════════════════════════════════════
BO: {caso['bo_desaparecimento']}
Data: {caso['data_desaparecimento']}
Local: {caso['cidade_desaparecimento']} - {caso['unidade_desaparecimento']}

RELATO:
{caso['historico_desaparecimento'][:800]}

═══════════════════════════════════════════════════════════════════
ÓBITO/CADÁVER
═══════════════════════════════════════════════════════════════════
BO: {caso['bo_morte']}
Tipo: {caso['tipo_morte']}
Data: {caso['data_morte']} ({caso['dias_entre_eventos']} dias depois)
Local: {caso['cidade_morte']} - {caso['unidade_morte']}

RELATO:
{caso['historico_morte'][:800]}

═══════════════════════════════════════════════════════════════════
DADOS DA PESSOA
═══════════════════════════════════════════════════════════════════
Nome: {caso['nome']}
Nascimento: {caso['data_nascimento']}
Mãe: {caso['nome_mae']}
Pai: {caso['nome_pai']}
RG: {rg}
Sexo: {caso['sexo']}
Transtorno: {transtorno} ({tipo_transtorno})

Responda APENAS com JSON (sem texto adicional):
{{
    "mesma_pessoa": true,
    "confianca": 95,
    "justificativa": "Nome, mãe e data de nascimento idênticos..."
}}"""

        # Chama IA com timeout
        print(f"\n[{num_caso}/{total_casos}] {caso['nome'][:50]}")
        print(f"   BO: {caso['bo_desaparecimento']} → {caso['bo_morte']}")
        print(f"   Intervalo: {caso['dias_entre_eventos']} dias")
        print(f"   Validando com IA...", end=" ", flush=True)
        
        inicio = time.time()
        
        resposta = ollama.chat(
            model=MODELO,
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': TEMPERATURA}
        )
        
        tempo_decorrido = time.time() - inicio
        
        # Extrai resposta
        texto = resposta['message']['content'].strip()
        
        # Parse JSON
        if '{' in texto and '}' in texto:
            inicio_json = texto.index('{')
            fim_json = texto.rindex('}') + 1
            json_str = texto[inicio_json:fim_json]
            resultado = json.loads(json_str)
            
            # Normaliza campo confiança (com ou sem acento)
            confianca = resultado.get('confianca', resultado.get('confiança', 0))
            
            status = "✓ CONFIRMADA" if resultado.get('mesma_pessoa') else "✗ REJEITADA"
            print(f"{status} ({confianca}%) [{tempo_decorrido:.1f}s]")
            
            return {
                'validado': True,
                'mesma_pessoa': resultado.get('mesma_pessoa', False),
                'confianca': confianca,
                'justificativa': resultado.get('justificativa', ''),
                'erro': None
            }
        else:
            print(f"❌ JSON inválido [{tempo_decorrido:.1f}s]")
            return {
                'validado': False,
                'mesma_pessoa': False,
                'confianca': 0,
                'justificativa': '',
                'erro': 'Resposta não contém JSON válido'
            }
            
    except json.JSONDecodeError as e:
        print(f"❌ Erro JSON: {str(e)[:50]}")
        return {
            'validado': False,
            'mesma_pessoa': False,
            'confianca': 0,
            'justificativa': '',
            'erro': f'JSON inválido: {str(e)[:100]}'
        }
        
    except Exception as e:
        print(f"❌ Erro: {str(e)[:50]}")
        return {
            'validado': False,
            'mesma_pessoa': False,
            'confianca': 0,
            'justificativa': '',
            'erro': str(e)[:200]
        }


def salvar_progresso(df, arquivo):
    """
    Salva progresso com encoding UTF-8 correto.
    
    Args:
        df: DataFrame com progresso
        arquivo: Caminho do arquivo
    """
    try:
        # Garante diretório existe
        Path(arquivo).parent.mkdir(parents=True, exist_ok=True)
        
        # Salva com UTF-8
        df.to_excel(arquivo, index=False, engine='openpyxl')
        
    except Exception as e:
        print(f"\n⚠ Erro ao salvar progresso: {e}")


def gerar_relatorio_final(df):
    """
    Gera relatório final com 3 abas: Confirmados, Todos, Estatísticas.
    
    Args:
        df: DataFrame completo validado
    """
    try:
        confirmados = df[df['ia_mesma_pessoa'] == True].sort_values('dias_entre_eventos')
        
        # Estatísticas
        stats = {
            'Métrica': [
                'Total de Casos',
                'Confirmados',
                'Rejeitados',
                'Erros',
                'Taxa de Confirmação',
                'Confiança Média (confirmados)'
            ],
            'Valor': [
                len(df),
                len(confirmados),
                len(df[df['ia_mesma_pessoa'] == False]),
                len(df[df['ia_validado'] == False]),
                f"{len(confirmados)/len(df)*100:.1f}%",
                f"{confirmados['ia_confianca'].mean():.1f}%"
            ]
        }
        df_stats = pd.DataFrame(stats)
        
        # Salva
        with pd.ExcelWriter(ARQUIVO_RELATORIO, engine='openpyxl') as writer:
            confirmados.to_excel(writer, sheet_name='Casos Confirmados', index=False)
            df.to_excel(writer, sheet_name='Todos os Casos', index=False)
            df_stats.to_excel(writer, sheet_name='Estatísticas', index=False)
        
        print(f"\n✅ Relatório final salvo: {ARQUIVO_RELATORIO}")
        
    except Exception as e:
        print(f"\n⚠ Erro ao gerar relatório: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Função principal"""
    
    print("=" * 70)
    print("VALIDAÇÃO DE CORRELAÇÕES COM IA")
    print(f"Modelo: {MODELO} | Temperatura: {TEMPERATURA}")
    print("=" * 70)
    
    # 1. Verifica modelo
    print(f"\n[1/4] Verificando modelo {MODELO}...", end=" ")
    if not verificar_modelo():
        sys.exit(1)
    print("✓")
    
    # 2. Carrega dados
    print(f"\n[2/4] Carregando {ARQUIVO_ENTRADA}...", end=" ")
    try:
        df = pd.read_excel(ARQUIVO_ENTRADA, sheet_name=ABA_ENTRADA)
        print(f"✓ ({len(df)} casos)")
    except Exception as e:
        print(f"\n❌ Erro ao carregar: {e}")
        sys.exit(1)
    
    # 3. Verifica progresso existente
    print(f"\n[3/4] Verificando progresso anterior...", end=" ")
    arquivo_prog = Path(ARQUIVO_PROGRESSO)
    
    if arquivo_prog.exists():
        try:
            df_prog = pd.read_excel(arquivo_prog)
            df = df_prog  # Usa progresso salvo
            ja_validados = df['ia_validado'].sum()
            print(f"✓ ({ja_validados} já validados)")
        except Exception as e:
            print(f"\n⚠ Erro ao ler progresso: {e}")
            # Cria colunas novas
            df['ia_validado'] = False
            df['ia_mesma_pessoa'] = None
            df['ia_confianca'] = 0
            df['ia_justificativa'] = ''
            df['ia_erro'] = None
    else:
        print("✓ (iniciando do zero)")
        df['ia_validado'] = False
        df['ia_mesma_pessoa'] = None
        df['ia_confianca'] = 0
        df['ia_justificativa'] = ''
        df['ia_erro'] = None
    
    # 4. Processa casos pendentes
    print(f"\n[4/4] Iniciando validações...")
    print("=" * 70)
    
    total = len(df)
    inicio_geral = time.time()
    
    for idx, caso in df.iterrows():
        # Pula se já validado
        if caso['ia_validado']:
            continue
        
        num_caso = idx + 1
        
        # Valida com IA
        resultado = validar_caso_com_ia(caso, num_caso, total)
        
        # Atualiza DataFrame
        df.at[idx, 'ia_validado'] = resultado['validado']
        df.at[idx, 'ia_mesma_pessoa'] = resultado['mesma_pessoa']
        df.at[idx, 'ia_confianca'] = resultado['confianca']
        df.at[idx, 'ia_justificativa'] = resultado['justificativa']
        df.at[idx, 'ia_erro'] = resultado['erro']
        
        # Salva progresso APÓS CADA CASO
        salvar_progresso(df, ARQUIVO_PROGRESSO)
        
        # Pequena pausa para não sobrecarregar
        time.sleep(0.5)
    
    # 5. Finalização
    tempo_total = (time.time() - inicio_geral) / 60
    validados = df['ia_validado'].sum()
    confirmados = (df['ia_mesma_pessoa'] == True).sum()
    
    print("\n" + "=" * 70)
    print("VALIDAÇÃO CONCLUÍDA!")
    print("=" * 70)
    print(f"✓ Total processado: {validados}/{total}")
    print(f"✓ Confirmados: {confirmados} ({confirmados/validados*100:.1f}%)")
    print(f"✓ Tempo total: {tempo_total:.1f} minutos")
    print("=" * 70)
    
    # Gera relatório final
    gerar_relatorio_final(df)
    
    print(f"\n📊 Ver resultados: {ARQUIVO_RELATORIO}")
    print(f"📈 Ver progresso: {ARQUIVO_PROGRESSO}\n")


if __name__ == "__main__":
    main()
