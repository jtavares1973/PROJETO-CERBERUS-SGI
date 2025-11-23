import pandas as pd

df = pd.read_excel('output/validacao_progresso.xlsx')
validados = df[df['ia_validado'] == True]

print(f'Validados: {len(validados)}/86')
print(f'Confirmados: {len(validados[validados["ia_mesma_pessoa"]==True])}')
print(f'Rejeitados: {len(validados[validados["ia_mesma_pessoa"]==False])}')

if len(validados) > 0:
    print(f'\nÚltimo validado:')
    print(f'  {validados.iloc[-1]["nome"]}')
    print(f'  Status: {"✓ CONFIRMADA" if validados.iloc[-1]["ia_mesma_pessoa"] else "✗ REJEITADA"}')
