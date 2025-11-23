"""
Script de validação com retomada automática
Salva progresso após cada caso validado
"""

import pandas as pd
import ollama
import json
from pathlib import Path
from datetime import datetime

def validar_caso(caso):
    """Valida um caso com qwen3:14b"""
    
    # Monta prompt detalhado
    prompt = f"""
# VALIDAÇÃO DE IDENTIDADE - BOLETINS DE OCORRÊNCIA

## DADOS DO DESAPARECIMENTO
BO: {caso['bo_desaparecimento']}
Data: {caso['data_desaparecimento']}
Histórico: {caso['historico_desaparecimento'][:500]}...

## DADOS DO ÓBITO
BO: {caso['bo_morte']}
Data: {caso['data_morte']}
Histórico: {caso['historico_morte'][:500]}...

## IDENTIFICAÇÃO DA PESSOA
Nome: {caso['nome']}
Data Nascimento: {caso['data_nascimento']}
Nome da Mãe: {caso['nome_mae']}
Nome do Pai: {caso['nome_pai']}
RG: {caso['numero_rg']}
Transtorno Psiquiátrico: {caso.get('tem_transtorno_psiquiatrico', 'N/A')}
Tipo: {caso.get('tipo_transtorno', 'N/A')}

## INTERVALO TEMPORAL
Dias entre desaparecimento e morte: {caso['dias_entre_eventos']} dias

## MISSÃO
Analisar se estes BOs referem-se à MESMA PESSOA. Compare:
1. Dados de identificação (nome mãe, pai, RG, data nascimento)
2. Menções explícitas nos históricos
3. Relatos familiares
4. Coerência temporal

Responda APENAS com JSON:
{{
    "mesma_pessoa": true/false,
    "confianca": 0-100,
    "justificativa": "explicação detalhada"
}}
"""
    
    try:
        response = ollama.chat(
            model='qwen3:14b',
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.1}
        )
        
        texto = response['message']['content']
        
        # Tenta extrair JSON
        if '{' in texto and '}' in texto:
            inicio = texto.index('{')
            fim = texto.rindex('}') + 1
            json_str = texto[inicio:fim]
            resultado = json.loads(json_str)
            
            return {
                'validado': True,
                'mesma_pessoa': resultado.get('mesma_pessoa', False),
                'confianca': resultado.get('confianca', 0),
                'justificativa': resultado.get('justificativa', ''),
                'erro': None
            }
        else:
            return {
                'validado': False,
                'mesma_pessoa': False,
                'confianca': 0,
                'justificativa': texto[:200],
                'erro': 'JSON não encontrado'
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
    print("=" * 80)
    print("VALIDAÇÃO COM RETOMADA AUTOMÁTICA")
    print("=" * 80)
    
    # Carrega correlações
    arquivo_entrada = Path('output/correlacoes_unicas_deduplicadas.xlsx')
    arquivo_saida = Path('output/validacao_unica_progresso.xlsx')
    
    print(f"\n📂 Carregando: {arquivo_entrada}")
    df = pd.read_excel(arquivo_entrada, sheet_name='FORTES - Únicas')
    print(f"   ✓ {len(df)} casos FORTES únicos carregados")
    
    # Verifica se há progresso anterior
    if arquivo_saida.exists():
        print(f"\n📥 Encontrado arquivo de progresso anterior")
        df_anterior = pd.read_excel(arquivo_saida)
        
        # Conta validados
        validados = df_anterior['ia_validado'].notna().sum()
        print(f"   ✓ {validados} casos já validados")
        
        # Atualiza df com resultados anteriores
        if validados > 0:
            df = df_anterior
            print(f"   ✓ Retomando do caso {validados + 1}")
    else:
        print(f"\n🆕 Primeira execução - criando arquivo de progresso")
        df['ia_validado'] = None
        df['ia_mesma_pessoa'] = None
        df['ia_confianca'] = None
        df['ia_justificativa'] = None
        df['ia_erro'] = None
    
    # Verifica modelo
    print("\n🔍 Verificando qwen3:14b...")
    try:
        modelos = ollama.list()
        if 'qwen3:14b' not in [m.get('model', m.get('name', '')) for m in modelos.get('models', [])]:
            print("   ❌ qwen3:14b não encontrado!")
            return
        print("   ✅ qwen3:14b disponível")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return
    
    # Processa cada caso
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
        
        # Valida
        resultado = validar_caso(caso)
        
        # Atualiza DataFrame
        df.at[idx, 'ia_validado'] = True
        df.at[idx, 'ia_mesma_pessoa'] = resultado['mesma_pessoa']
        df.at[idx, 'ia_confianca'] = resultado['confianca']
        df.at[idx, 'ia_justificativa'] = resultado['justificativa']
        df.at[idx, 'ia_erro'] = resultado['erro']
        
        # Status
        if resultado['erro']:
            print(f"   ⚠️ Erro: {resultado['erro']}")
        elif resultado['mesma_pessoa']:
            print(f"   ✅ CONFIRMADA (confiança: {resultado['confianca']}%)")
        else:
            print(f"   ❌ REJEITADA (confiança: {resultado['confianca']}%)")
        
        # Salva progresso
        df.to_excel(arquivo_saida, index=False)
        
        # Estatísticas
        validados = df['ia_validado'].notna().sum()
        confirmados = (df['ia_mesma_pessoa'] == True).sum()
        rejeitados = (df['ia_mesma_pessoa'] == False).sum()
        
        # Tempo estimado
        decorrido = (datetime.now() - inicio).total_seconds() / 60
        tempo_por_caso = decorrido / validados if validados > 0 else 0
        restantes = total - validados
        tempo_restante = restantes * tempo_por_caso
        
        if validados % 10 == 0:
            print(f"\n   📊 Progresso: {validados}/{total} ({confirmados} ✅ | {rejeitados} ❌)")
            print(f"   ⏱️ Tempo restante: ~{tempo_restante:.1f} min")
            print(f"   💾 Progresso salvo em: {arquivo_saida}")
    
    # Relatório final
    print("\n" + "=" * 80)
    print("✅ VALIDAÇÃO CONCLUÍDA!")
    print("=" * 80)
    
    confirmados = (df['ia_mesma_pessoa'] == True).sum()
    rejeitados = (df['ia_mesma_pessoa'] == False).sum()
    erros = df['ia_erro'].notna().sum()
    
    print(f"\n📊 RESULTADOS:")
    print(f"   Total validado: {total}")
    print(f"   ✅ Confirmados: {confirmados} ({confirmados/total*100:.1f}%)")
    print(f"   ❌ Rejeitados: {rejeitados} ({rejeitados/total*100:.1f}%)")
    print(f"   ⚠️ Erros: {erros}")
    print(f"\n💾 Arquivo salvo: {arquivo_saida}")
    
    # Cria relatório final
    print(f"\n📋 Gerando relatório final...")
    df_confirmados = df[df['ia_mesma_pessoa'] == True].copy()
    df_confirmados = df_confirmados.sort_values('dias_entre_eventos')
    
    with pd.ExcelWriter('output/RELATORIO_VALIDACAO_FINAL.xlsx', engine='openpyxl') as writer:
        df_confirmados.to_excel(writer, sheet_name='Casos Confirmados', index=False)
        df.to_excel(writer, sheet_name='Todos os Casos', index=False)
        
        # Estatísticas
        stats = pd.DataFrame({
            'Métrica': ['Total Analisado', 'Confirmados', 'Rejeitados', 'Taxa Confirmação', 'Confiança Média'],
            'Valor': [
                total,
                confirmados,
                rejeitados,
                f"{confirmados/total*100:.1f}%",
                f"{df[df['ia_mesma_pessoa']==True]['ia_confianca'].mean():.1f}%"
            ]
        })
        stats.to_excel(writer, sheet_name='Estatísticas', index=False)
    
    print(f"   ✅ RELATORIO_VALIDACAO_FINAL.xlsx criado!")
    print(f"\n🎯 Casos confirmados prontos para análise pericial!")

if __name__ == "__main__":
    main()
