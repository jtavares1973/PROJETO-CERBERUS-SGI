"""Script para analisar a estrutura do CSV"""
import pandas as pd

# Ler CSV com encoding correto
df = pd.read_csv('Dados-homi-desaperecido.csv', sep=';', nrows=100, encoding='latin-1', on_bad_lines='skip')

print(f"Shape do dataset: {df.shape}")
print(f"\n{'='*80}")
print("COLUNAS DO DATASET:")
print(f"{'='*80}\n")

for i, col in enumerate(df.columns.tolist(), 1):
    print(f"{i:2d}. {col}")

print(f"\n{'='*80}")
print("VALORES ÚNICOS DAS COLUNAS-CHAVE:")
print(f"{'='*80}\n")

# Identificar tipos de natureza
if 'Natureza' in df.columns:
    print(f"\nNaturezas encontradas (primeiras 10):")
    print(df['Natureza'].value_counts().head(10))

if 'Natureza Padronizada' in df.columns:
    print(f"\n\nNaturezas Padronizadas:")
    print(df['Natureza Padronizada'].value_counts())

if 'Natureza do Envolvido' in df.columns:
    print(f"\n\nNatureza do Envolvido:")
    print(df['Natureza do Envolvido'].value_counts())

# Amostra de dados
print(f"\n{'='*80}")
print("AMOSTRA DE DADOS (primeira linha não-nula):")
print(f"{'='*80}\n")

for col in df.columns[:15]:
    valor = df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else "N/A"
    print(f"{col}: {valor}")
