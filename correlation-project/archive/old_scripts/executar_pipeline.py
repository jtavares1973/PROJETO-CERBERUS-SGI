"""Executar pipeline com dados reais"""
import sys
sys.path.insert(0, '.')
from etl.pipeline import pipeline_completo

# Executar com dados reais
print('\n' + '='*80)
print('EXECUTANDO PIPELINE COM DADOS REAIS')
print('='*80 + '\n')

df = pipeline_completo(
    caminho_csv=r'd:\___MeusScripts\LangChain\Dados-homi-desaperecido.csv',
    output_path='output/dataset_unificado.xlsx'  # XLSX formatado
)

if df is not None:
    print('\n' + '='*80)
    print('PIPELINE CONCLUIDO COM SUCESSO!')
    print('='*80 + '\n')
    
    print(f'Total de registros: {len(df)}')
    
    print('\nClassificacoes:')
    print(df['classificacao_final'].value_counts())
    
    if 'tem_transtorno_psiquiatrico' in df.columns:
        qtd_transtornos = df['tem_transtorno_psiquiatrico'].sum()
        print(f'\nTranstornos detectados: {qtd_transtornos}')
    
    print(f'\nArquivo salvo em: output/dataset_unificado.xlsx')
    print('Planilhas incluidas:')
    print('  - Dados Completos')
    print('  - Estatisticas')
    print('  - Transtornos Detectados')
    print('  - Correlacoes')
    print('\n' + '='*80 + '\n')
else:
    print('\nERRO ao executar pipeline!')
