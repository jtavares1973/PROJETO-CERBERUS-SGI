import pandas as pd

df = pd.read_excel('output/correlacoes_unicas_deduplicadas.xlsx', sheet_name='FORTES - Únicas')
print(f'Total linhas: {len(df)}')
print(f'Pessoas únicas: {df["chave_pessoa"].nunique()}')
print(f'DUPLICADOS: {len(df) - df["chave_pessoa"].nunique()}')

dupes = df[df.duplicated(subset=['chave_pessoa'], keep=False)].sort_values('chave_pessoa')
if len(dupes) > 0:
    print(f'\nExemplos de duplicados:')
    for pessoa in dupes['chave_pessoa'].unique()[:3]:
        casos = dupes[dupes['chave_pessoa'] == pessoa][['nome', 'dias_entre_eventos', 'chave_desaparecimento', 'chave_obito']]
        print(f'\n{pessoa}:')
        print(casos.to_string(index=False))
