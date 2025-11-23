"""
Gera arquivo Excel filtrado apenas com registros do grupo-alvo:
- DESAPARECIMENTO DE PESSOA
- HOMICIDIO
- LOCALIZACAO OU REMOCAO CADAVER
"""

import pandas as pd
from pathlib import Path

# Carregar arquivo completo
arquivo_entrada = "output/dataset_unificado.xlsx"
arquivo_saida = "output/dataset_filtrado_grupo_alvo.xlsx"

print("=" * 80)
print("GERANDO ARQUIVO FILTRADO - GRUPO ALVO")
print("=" * 80)

print(f"\n[1/4] Carregando arquivo: {arquivo_entrada}")
df = pd.read_excel(arquivo_entrada, sheet_name='Dados Completos')
print(f"Total de registros no arquivo original: {len(df):,}")

print(f"\n[2/4] Aplicando filtros do grupo-alvo...")
# Filtrar por natureza_alvo (natureza da ocorrência)
df_filtrado = df[df['natureza_alvo'].isin(['DESAPARECIMENTO', 'HOMICIDIO', 'CADAVER'])].copy()

print(f"Registros após filtro: {len(df_filtrado):,}")
print(f"\nDistribuição por natureza da ocorrência:")
print(df_filtrado['natureza_alvo'].value_counts())

print(f"\nDistribuição por contexto da pessoa:")
print(df_filtrado['contexto_pessoa'].value_counts())

print(f"\n[3/4] Gerando estatísticas adicionais...")

# Contar pessoas únicas
pessoas_unicas = df_filtrado['chave_pessoa'].nunique()
ocorrencias_unicas = df_filtrado['chave_ocorrencia'].nunique()

print(f"Pessoas únicas (chave_pessoa): {pessoas_unicas:,}")
print(f"Ocorrências únicas (chave_ocorrencia): {ocorrencias_unicas:,}")

# Identificar possíveis duplicatas (mesma pessoa em múltiplas ocorrências)
duplicatas = df_filtrado[df_filtrado.duplicated(subset=['chave_pessoa'], keep=False)]
pessoas_com_multiplas_ocorrencias = duplicatas['chave_pessoa'].nunique()

print(f"Pessoas com múltiplas ocorrências: {pessoas_com_multiplas_ocorrencias:,}")

# Detectar transtornos
if 'tem_transtorno_psiquiatrico' in df_filtrado.columns:
    transtornos = df_filtrado['tem_transtorno_psiquiatrico'].sum()
    print(f"Registros com transtorno psiquiátrico: {transtornos:,}")

print(f"\n[4/4] Salvando arquivo filtrado: {arquivo_saida}")

# Criar planilha de estatísticas
stats_data = {
    'Métrica': [
        'Total de Registros',
        'Pessoas Únicas',
        'Ocorrências Únicas',
        'Pessoas com Múltiplas Ocorrências',
        'Desaparecimentos',
        'Localizações de Cadáver',
        'Homicídios',
        'Transtornos Detectados'
    ],
    'Valor': [
        len(df_filtrado),
        pessoas_unicas,
        ocorrencias_unicas,
        pessoas_com_multiplas_ocorrencias,
        (df_filtrado['natureza_alvo'] == 'DESAPARECIMENTO').sum(),
        (df_filtrado['natureza_alvo'] == 'CADAVER').sum(),
        (df_filtrado['natureza_alvo'] == 'HOMICIDIO').sum(),
        df_filtrado['tem_transtorno_psiquiatrico'].sum() if 'tem_transtorno_psiquiatrico' in df_filtrado.columns else 0
    ]
}
df_stats = pd.DataFrame(stats_data)

# Criar planilha de pessoas com múltiplas ocorrências
if pessoas_com_multiplas_ocorrencias > 0:
    colunas_importantes = ['nome', 'chave_pessoa', 'chave_ocorrencia', 'natureza_alvo', 
                          'contexto_pessoa', 'data_fato', 'unidade_registro']
    colunas_disponiveis = [col for col in colunas_importantes if col in df_filtrado.columns]
    
    df_duplicatas = duplicatas[colunas_disponiveis].sort_values('chave_pessoa')
else:
    df_duplicatas = pd.DataFrame()

# Salvar Excel com múltiplas abas
with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
    df_filtrado.to_excel(writer, sheet_name='Dados Filtrados', index=False)
    df_stats.to_excel(writer, sheet_name='Estatísticas', index=False)
    if len(df_duplicatas) > 0:
        df_duplicatas.to_excel(writer, sheet_name='Múltiplas Ocorrências', index=False)

print(f"\n✅ Arquivo gerado com sucesso!")
print(f"📂 Local: {Path(arquivo_saida).absolute()}")
print(f"\n📊 Planilhas criadas:")
print(f"   1. Dados Filtrados - {len(df_filtrado):,} registros")
print(f"   2. Estatísticas - Resumo dos dados")
if len(df_duplicatas) > 0:
    print(f"   3. Múltiplas Ocorrências - {len(df_duplicatas):,} registros")

print("\n" + "=" * 80)
print("PROCESSAMENTO CONCLUÍDO!")
print("=" * 80)
