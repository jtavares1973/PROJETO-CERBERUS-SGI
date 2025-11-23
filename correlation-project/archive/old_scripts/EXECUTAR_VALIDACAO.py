"""
═══════════════════════════════════════════════════════════════════════════════
SCRIPT PRINCIPAL DE VALIDAÇÃO COM IA
═══════════════════════════════════════════════════════════════════════════════

📋 PROPÓSITO:
   Valida correlações pessoa desaparecida → encontrada morta usando IA local
   (Ollama qwen3:14b)

🎯 CARACTERÍSTICAS:
   ✅ Salva progresso após CADA caso validado
   ✅ Retoma automaticamente se interrompido
   ✅ Estatísticas em tempo real
   ✅ Relatório final formatado

📊 INPUT:
   - output/correlacoes_unicas_deduplicadas.xlsx (aba: FORTES - Únicas)
   - 86 casos FORTES (0-30 dias entre desaparecimento e morte)

📈 OUTPUT:
   - output/validacao_progresso.xlsx (atualizado continuamente)
   - output/RELATORIO_VALIDACAO_FINAL.xlsx (ao concluir)

⏱️ TEMPO ESTIMADO:
   - 86 casos × ~0.2 min/caso = ~17-20 minutos

═══════════════════════════════════════════════════════════════════════════════
"""

import pandas as pd
import ollama
import json
from pathlib import Path
from datetime import datetime


def validar_caso_com_ia(caso):
    """
    Valida se dois BOs (desaparecimento e morte) referem-se à mesma pessoa.
    
    Utiliza qwen2.5-ptbr:7b otimizado para português.
    
    Args:
        caso: Série pandas com dados da correlação
        
    Returns:
        Dict com: validado, mesma_pessoa, confianca, justificativa, erro
    """
    
    # Prepara dados com fallback para valores ausentes
    transtorno = 'Sim' if caso.get('tem_transtorno_psiquiatrico') else 'Não'
    tipo_transtorno = caso.get('tipo_transtorno', 'Não informado')
    rg_completo = f"{caso['numero_rg']}" if pd.notna(caso.get('numero_rg')) else 'Não informado'
    
    # Monta prompt OTIMIZADO em português claro
    prompt = f"""TAREFA: Analisar se os dois boletins de ocorrência abaixo são DA MESMA PESSOA.

═══════════════════════════════════════════════════════════════════
DESAPARECIMENTO
═══════════════════════════════════════════════════════════════════
BO: {caso['bo_desaparecimento']}
Data: {caso['data_desaparecimento']}
Local: {caso['cidade_desaparecimento']} - {caso['unidade_desaparecimento']}

RELATO DO DESAPARECIMENTO:
{caso['historico_desaparecimento'][:800]}

═══════════════════════════════════════════════════════════════════
ÓBITO/CADÁVER
═══════════════════════════════════════════════════════════════════
BO: {caso['bo_morte']}
Tipo: {caso['tipo_morte']}
Data: {caso['data_morte']} ({caso['dias_entre_eventos']} dias depois)
Local: {caso['cidade_morte']} - {caso['unidade_morte']}

RELATO DO ÓBITO:
{caso['historico_morte'][:800]}

═══════════════════════════════════════════════════════════════════
DADOS DA PESSOA PARA VALIDAÇÃO
═══════════════════════════════════════════════════════════════════
Nome: {caso['nome']}
Data Nascimento: {caso['data_nascimento']}
Mãe: {caso['nome_mae']}
Pai: {caso['nome_pai']}
RG: {rg_completo}
Sexo: {caso['sexo']}
Transtorno Psiquiátrico: {transtorno} ({tipo_transtorno})

═══════════════════════════════════════════════════════════════════
ANÁLISE REQUERIDA
═══════════════════════════════════════════════════════════════════

Compare os dados de identificação (nome, data nascimento, mãe, pai, RG) nos dois BOs.
Verifique se os relatos mencionam os mesmos familiares ou detalhes que conectam os eventos.
Avalie se o intervalo de {caso['dias_entre_eventos']} dias é coerente.

Responda APENAS com o JSON abaixo (sem texto adicional):
{{
    "mesma_pessoa": true,
    "confianca": 95,
    "justificativa": "Sua análise aqui"
}}"""
    
    try:
        response = ollama.chat(
            model='qwen2.5-ptbr:7b',
            messages=[{'role': 'user', 'content': prompt}],
            options={
                'temperature': 0.1, 
                'num_predict': 500,
                'num_ctx': 4096
            },
            stream=False
        )
        
        texto = response['message']['content']
        
        # Extrai JSON da resposta
        if '{' in texto and '}' in texto:
            inicio = texto.index('{')
            fim = texto.rindex('}') + 1
            json_str = texto[inicio:fim]
            resultado = json.loads(json_str)
            
            # Normaliza campo confiança (pode vir com ou sem acento)
            confianca = resultado.get('confianca', resultado.get('confiança', 0))
            
            return {
                'validado': True,
                'mesma_pessoa': resultado.get('mesma_pessoa', False),
                'confianca': confianca,
                'justificativa': resultado.get('justificativa', ''),
                'erro': None
            }
        else:
            return {
                'validado': False,
                'mesma_pessoa': False,
                'confianca': 0,
                'justificativa': texto[:300],
                'erro': 'JSON não encontrado na resposta'
            }
            
    except json.JSONDecodeError as e:
        return {
            'validado': False,
            'mesma_pessoa': False,
            'confianca': 0,
            'justificativa': '',
            'erro': f'Erro ao parsear JSON: {str(e)[:100]}'
        }
    except Exception as e:
        return {
            'validado': False,
            'mesma_pessoa': False,
            'confianca': 0,
            'justificativa': '',
            'erro': str(e)[:200]
        }


def main():
    """Executa o processo completo de validação"""
    
    print("=" * 80)
    print("VALIDACAO DE CORRELACOES COM IA")
    print("Modelo: Ollama qwen2.5-ptbr:7b (PORTUGUES) | Temperatura: 0.1")
    print("=" * 80)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 1. CARREGAR DADOS
    # ═══════════════════════════════════════════════════════════════════════════
    arquivo_entrada = Path('output/correlacoes_unicas_deduplicadas.xlsx')
    arquivo_saida = Path('output/validacao_progresso.xlsx')
    
    print(f"\n[Carregamento] Arquivo: {arquivo_entrada}")
    df = pd.read_excel(arquivo_entrada, sheet_name='FORTES - Únicas')
    print(f"   OK - {len(df)} casos FORTES unicos carregados")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 2. VERIFICAR PROGRESSO ANTERIOR
    # ═══════════════════════════════════════════════════════════════════════════
    if arquivo_saida.exists():
        print(f"\n[Progresso] Arquivo encontrado")
        df_anterior = pd.read_excel(arquivo_saida)
        validados = df_anterior['ia_validado'].notna().sum()
        print(f"   OK - {validados} casos ja validados")
        
        if validados > 0:
            df = df_anterior
            print(f"   OK - Retomando do caso {validados + 1}")
    else:
        print(f"\n[Progresso] Primeira execucao")
        # Adiciona colunas de resultado
        df['ia_validado'] = None
        df['ia_mesma_pessoa'] = None
        df['ia_confianca'] = None
        df['ia_justificativa'] = None
        df['ia_erro'] = None
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 3. VERIFICAR MODELO OLLAMA
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n[Ollama] Verificando qwen2.5-ptbr:7b...")
    try:
        modelos = ollama.list()
        nomes_modelos = [m.get('model', m.get('name', '')) for m in modelos.get('models', [])]
        
        if 'qwen2.5-ptbr:7b' not in nomes_modelos:
            print("   ERRO - qwen2.5-ptbr:7b nao encontrado!")
            print("   Dica: Execute: ollama pull qwen2.5-ptbr:7b")
            return
            
        print("   OK - qwen2.5-ptbr:7b disponivel (modelo em PORTUGUES)")
        
    except Exception as e:
        print(f"   ERRO - Ao conectar com Ollama: {e}")
        print("   Dica: Verifique se Ollama esta rodando: ollama serve")
        return
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 4. PROCESSAR CADA CASO
    # ═══════════════════════════════════════════════════════════════════════════
    print(f"\n" + "=" * 80)
    print("INICIANDO VALIDAÇÕES...")
    print("=" * 80)
    
    total = len(df)
    inicio = datetime.now()
    
    for idx, caso in df.iterrows():
        # Pula se já validado
        if pd.notna(caso.get('ia_validado')):
            continue
        
        # Número do caso
        num_caso = idx + 1
        
        print(f"\n[{num_caso}/{total}] {caso['nome']}")
        print(f"   BO Desap: {caso['bo_desaparecimento']} | BO Morte: {caso['bo_morte']}")
        print(f"   Intervalo: {caso['dias_entre_eventos']} dias | Força: {caso['forca_correlacao']}")
        print(f"   Validando com IA...", end=' ', flush=True)
        
        # Valida com IA
        resultado = validar_caso_com_ia(caso)
        
        # Atualiza DataFrame
        df.at[idx, 'ia_validado'] = True
        df.at[idx, 'ia_mesma_pessoa'] = resultado['mesma_pessoa']
        df.at[idx, 'ia_confianca'] = resultado['confianca']
        df.at[idx, 'ia_justificativa'] = resultado['justificativa']
        df.at[idx, 'ia_erro'] = resultado['erro']
        
        # Mostra resultado
        if resultado['erro']:
            print(f"AVISO - ERRO: {resultado['erro']}")
        elif resultado['mesma_pessoa']:
            print(f"OK - CONFIRMADA ({resultado['confianca']}%)")
        else:
            print(f"REJEITADA ({resultado['confianca']}%)")
        
        # Salva progresso
        df.to_excel(arquivo_saida, index=False)
        
        # Estatísticas
        validados = df['ia_validado'].notna().sum()
        confirmados = (df['ia_mesma_pessoa'] == True).sum()
        rejeitados = (df['ia_mesma_pessoa'] == False).sum()
        
        # Tempo estimado
        decorrido_min = (datetime.now() - inicio).total_seconds() / 60
        tempo_por_caso = decorrido_min / validados if validados > 0 else 0
        restantes = total - validados
        tempo_restante_min = restantes * tempo_por_caso
        
        # Mostra estatísticas a cada 10 casos
        if validados % 10 == 0:
            print(f"\n   [Progresso] {validados}/{total} | Confirmados: {confirmados} | Rejeitados: {rejeitados}")
            print(f"   [Tempo] Restante: ~{tempo_restante_min:.1f} min")
            print(f"   [Salvo] {arquivo_saida}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 5. RELATÓRIO FINAL
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("VALIDACAO CONCLUIDA!")
    print("=" * 80)
    
    confirmados = (df['ia_mesma_pessoa'] == True).sum()
    rejeitados = (df['ia_mesma_pessoa'] == False).sum()
    erros = df['ia_erro'].notna().sum()
    confianca_media = df[df['ia_mesma_pessoa'] == True]['ia_confianca'].mean()
    
    print(f"\n[RESULTADOS FINAIS]")
    print(f"   Total validado: {total}")
    print(f"   Confirmados: {confirmados} ({confirmados/total*100:.1f}%)")
    print(f"   Rejeitados: {rejeitados} ({rejeitados/total*100:.1f}%)")
    print(f"   Erros: {erros}")
    print(f"   Confianca media (confirmados): {confianca_media:.1f}%")
    
    tempo_total = (datetime.now() - inicio).total_seconds() / 60
    print(f"\n   Tempo total: {tempo_total:.1f} minutos")
    
    # Gera relatório final
    print(f"\n[Relatorio] Gerando relatorio final...")
    arquivo_final = Path('output/RELATORIO_VALIDACAO_FINAL.xlsx')
    
    df_confirmados = df[df['ia_mesma_pessoa'] == True].copy()
    df_confirmados = df_confirmados.sort_values('dias_entre_eventos')
    
    with pd.ExcelWriter(arquivo_final, engine='openpyxl') as writer:
        # Aba 1: Casos confirmados
        df_confirmados.to_excel(writer, sheet_name='Casos Confirmados', index=False)
        
        # Aba 2: Todos os casos
        df.to_excel(writer, sheet_name='Todos os Casos', index=False)
        
        # Aba 3: Estatísticas
        stats = pd.DataFrame({
            'Metrica': [
                'Total Analisado',
                'Casos Confirmados',
                'Casos Rejeitados',
                'Taxa de Confirmacao',
                'Confianca Media (confirmados)',
                'Casos com Erro',
                'Tempo Total (min)'
            ],
            'Valor': [
                total,
                confirmados,
                rejeitados,
                f"{confirmados/total*100:.1f}%",
                f"{confianca_media:.1f}%",
                erros,
                f"{tempo_total:.1f}"
            ]
        })
        stats.to_excel(writer, sheet_name='Estatisticas', index=False)
    
    print(f"   OK - {arquivo_final}")
    print(f"\n[SUCESSO] {confirmados} casos confirmados prontos para analise pericial!")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[AVISO] Validacao interrompida pelo usuario")
        print("[DICA] Execute novamente para retomar do ultimo caso salvo")
    except Exception as e:
        print(f"\n\n[ERRO CRITICO] {e}")
        import traceback
        traceback.print_exc()
