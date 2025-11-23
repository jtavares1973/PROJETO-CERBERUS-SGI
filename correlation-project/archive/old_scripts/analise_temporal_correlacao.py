"""
Análise de Correlação Temporal - Lógica Elucidadora

REGRA DE NEGÓCIO:
Se uma pessoa:
1. DESAPARECEU em Data1
2. Foi encontrada MORTA (homicídio ou cadáver) em Data2
3. E Data2 é IMEDIATAMENTE após Data1 (sem outra ocorrência no meio)
   → ENTÃO: É provável que o desaparecimento tenha terminado em morte

Se houver OUTRA ocorrência entre Data1 e Data2:
   → A pessoa pode ter sido localizada viva e depois teve outro problema
"""

import pandas as pd
from datetime import datetime, timedelta
import numpy as np

print("=" * 80)
print("ANÁLISE DE CORRELAÇÃO TEMPORAL - DESAPARECIMENTO → MORTE")
print("=" * 80)

# Carregar dados
arquivo = "output/dataset_filtrado_grupo_alvo.xlsx"
print(f"\n[1/5] Carregando dados: {arquivo}")
df = pd.read_excel(arquivo, sheet_name='Dados Filtrados')
print(f"Total de registros: {len(df):,}")

# Converter data_fato para datetime
print(f"\n[2/5] Preparando dados temporais...")
if 'data_fato' in df.columns:
    df['data_fato_dt'] = pd.to_datetime(df['data_fato'], errors='coerce')
elif 'data_fato_dt' in df.columns:
    df['data_fato_dt'] = pd.to_datetime(df['data_fato_dt'], errors='coerce')
else:
    print("ERRO: Coluna de data não encontrada!")
    exit(1)

# Remover registros sem data
df = df[df['data_fato_dt'].notna()].copy()
print(f"Registros com data válida: {len(df):,}")

# Ordenar por pessoa e data
df = df.sort_values(['chave_pessoa', 'data_fato_dt'])

print(f"\n[3/5] Identificando sequências temporais...")

# Agrupar por pessoa
correlacoes_encontradas = []

for chave_pessoa, grupo in df.groupby('chave_pessoa'):
    if len(grupo) < 2:
        continue  # Precisa de pelo menos 2 ocorrências
    
    # Ordenar por data
    grupo = grupo.sort_values('data_fato_dt')
    ocorrencias = grupo.to_dict('records')
    
    # Analisar sequências
    for i in range(len(ocorrencias) - 1):
        atual = ocorrencias[i]
        proxima = ocorrencias[i + 1]
        
        # Verificar se é sequência DESAPARECIMENTO → MORTE
        if atual['natureza_alvo'] == 'DESAPARECIMENTO':
            if proxima['natureza_alvo'] in ['HOMICIDIO', 'CADAVER']:
                # Calcular dias entre eventos
                dias_diferenca = (proxima['data_fato_dt'] - atual['data_fato_dt']).days
                
                # Verificar se há outras ocorrências no meio
                tem_ocorrencia_no_meio = False
                if i + 2 < len(ocorrencias):
                    # Há pelo menos mais uma ocorrência depois
                    # Mas só conta se estiver ENTRE as duas datas
                    for j in range(i + 2, len(ocorrencias)):
                        data_meio = ocorrencias[j]['data_fato_dt']
                        if atual['data_fato_dt'] < data_meio < proxima['data_fato_dt']:
                            tem_ocorrencia_no_meio = True
                            break
                
                # Classificar o tipo de correlação
                if dias_diferenca <= 30 and not tem_ocorrencia_no_meio:
                    forca = 'FORTE'
                    explicacao = 'Morte ocorreu até 30 dias após desaparecimento, sem ocorrências intermediárias'
                elif dias_diferenca <= 90 and not tem_ocorrencia_no_meio:
                    forca = 'MÉDIA'
                    explicacao = 'Morte ocorreu até 90 dias após desaparecimento, sem ocorrências intermediárias'
                elif not tem_ocorrencia_no_meio:
                    forca = 'FRACA'
                    explicacao = f'Morte ocorreu {dias_diferenca} dias após desaparecimento, sem ocorrências intermediárias'
                else:
                    forca = 'INCONCLUSIVA'
                    explicacao = 'Há outras ocorrências entre o desaparecimento e a morte - pessoa pode ter sido localizada viva'
                
                correlacoes_encontradas.append({
                    'chave_pessoa': chave_pessoa,
                    'nome': atual.get('nome', ''),
                    'data_desaparecimento': atual['data_fato_dt'],
                    'bo_desaparecimento': atual.get('chave_ocorrencia', ''),
                    'cidade_desaparecimento': atual.get('cidade_ra', 'N/A'),
                    'unidade_desaparecimento': atual.get('unidade_registro', ''),
                    'data_morte': proxima['data_fato_dt'],
                    'tipo_morte': proxima['natureza_alvo'],
                    'bo_morte': proxima.get('chave_ocorrencia', ''),
                    'cidade_morte': proxima.get('cidade_ra', 'N/A'),
                    'unidade_morte': proxima.get('unidade_registro', ''),
                    'dias_entre_eventos': dias_diferenca,
                    'tem_evento_intermediario': tem_ocorrencia_no_meio,
                    'forca_correlacao': forca,
                    'explicacao': explicacao
                })

print(f"\n[4/5] Processando resultados...")
df_correlacoes = pd.DataFrame(correlacoes_encontradas)

if len(df_correlacoes) == 0:
    print("\nNenhuma correlação temporal encontrada!")
    exit(0)

# Estatísticas
print(f"\n{'='*80}")
print(f"CORRELAÇÕES ENCONTRADAS: {len(df_correlacoes):,}")
print(f"{'='*80}")

print(f"\n📊 DISTRIBUIÇÃO POR FORÇA DE CORRELAÇÃO:")
print(df_correlacoes['forca_correlacao'].value_counts())

print(f"\n📊 DISTRIBUIÇÃO POR TIPO DE MORTE:")
print(df_correlacoes['tipo_morte'].value_counts())

print(f"\n📊 TEMPO MÉDIO ENTRE DESAPARECIMENTO E MORTE:")
print(f"   - Correlações FORTES: {df_correlacoes[df_correlacoes['forca_correlacao']=='FORTE']['dias_entre_eventos'].mean():.0f} dias")
print(f"   - Correlações MÉDIAS: {df_correlacoes[df_correlacoes['forca_correlacao']=='MÉDIA']['dias_entre_eventos'].mean():.0f} dias")
print(f"   - Correlações FRACAS: {df_correlacoes[df_correlacoes['forca_correlacao']=='FRACA']['dias_entre_eventos'].mean():.0f} dias")

print(f"\n🔍 TOP 10 CORRELAÇÕES MAIS FORTES (menor tempo):")
top10 = df_correlacoes[df_correlacoes['forca_correlacao'].isin(['FORTE', 'MÉDIA'])].nsmallest(10, 'dias_entre_eventos')
for idx, row in top10.iterrows():
    print(f"\n   {row['nome']}")
    print(f"   • Desapareceu: {row['data_desaparecimento'].strftime('%d/%m/%Y')} em {row['cidade_desaparecimento']}")
    print(f"     BO: {row['bo_desaparecimento']}")
    print(f"   • Encontrado morto: {row['data_morte'].strftime('%d/%m/%Y')} em {row['cidade_morte']}")
    print(f"     BO: {row['bo_morte']}")
    print(f"   • Tipo: {row['tipo_morte']} | Intervalo: {row['dias_entre_eventos']} dias")
    print(f"   • Força: {row['forca_correlacao']}")

print(f"\n[5/5] Salvando resultados...")
arquivo_saida = "output/correlacoes_temporais.xlsx"

# Criar diferentes planilhas por força de correlação
with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
    df_correlacoes.to_excel(writer, sheet_name='Todas Correlações', index=False)
    
    df_fortes = df_correlacoes[df_correlacoes['forca_correlacao'] == 'FORTE']
    if len(df_fortes) > 0:
        df_fortes.to_excel(writer, sheet_name='Correlações FORTES', index=False)
    
    df_medias = df_correlacoes[df_correlacoes['forca_correlacao'] == 'MÉDIA']
    if len(df_medias) > 0:
        df_medias.to_excel(writer, sheet_name='Correlações MÉDIAS', index=False)
    
    df_fracas = df_correlacoes[df_correlacoes['forca_correlacao'] == 'FRACA']
    if len(df_fracas) > 0:
        df_fracas.to_excel(writer, sheet_name='Correlações FRACAS', index=False)
    
    df_inconclusivas = df_correlacoes[df_correlacoes['forca_correlacao'] == 'INCONCLUSIVA']
    if len(df_inconclusivas) > 0:
        df_inconclusivas.to_excel(writer, sheet_name='INCONCLUSIVAS', index=False)

print(f"\n✅ Arquivo gerado: {arquivo_saida}")
print(f"\n📋 Planilhas criadas:")
print(f"   1. Todas Correlações - {len(df_correlacoes):,} casos")
print(f"   2. Correlações FORTES - {len(df_fortes):,} casos (até 30 dias)")
print(f"   3. Correlações MÉDIAS - {len(df_medias):,} casos (31-90 dias)")
print(f"   4. Correlações FRACAS - {len(df_fracas):,} casos (>90 dias)")
print(f"   5. INCONCLUSIVAS - {len(df_inconclusivas):,} casos (eventos intermediários)")

print(f"\n{'='*80}")
print("ANÁLISE CONCLUÍDA!")
print(f"{'='*80}")
