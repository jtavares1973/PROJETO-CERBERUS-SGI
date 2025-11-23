"""
Remove duplicatas das correlações mantendo apenas a melhor por pessoa
"""

import pandas as pd
from pathlib import Path


def remover_duplicatas():
    print("=" * 80)
    print("REMOVENDO DUPLICATAS - MANTENDO MELHOR CORRELAÇÃO POR PESSOA")
    print("=" * 80)
    
    # Carrega correlações
    arquivo = Path('output/correlacoes_completas_com_identificacao.xlsx')
    print(f"\n📂 Carregando: {arquivo}")
    df = pd.read_excel(arquivo, sheet_name='Todas Correlações')
    print(f"   Total original: {len(df)} correlações")
    
    # Conta duplicatas
    duplicatas = df.groupby('chave_pessoa').size()
    pessoas_duplicadas = duplicatas[duplicatas > 1]
    
    print(f"\n🔍 Análise de duplicatas:")
    print(f"   Pessoas únicas: {df['chave_pessoa'].nunique()}")
    print(f"   Pessoas com múltiplas correlações: {len(pessoas_duplicadas)}")
    print(f"   Total de registros duplicados: {duplicatas.sum() - len(duplicatas)}")
    
    # Mostra exemplos de duplicatas
    print(f"\n📋 Exemplos de pessoas com múltiplas correlações:")
    for i, (chave, qtd) in enumerate(pessoas_duplicadas.head(5).items()):
        pessoa_casos = df[df['chave_pessoa'] == chave]
        nome = pessoa_casos.iloc[0]['nome']
        print(f"   {i+1}. {nome}: {qtd} correlações")
        for idx, caso in pessoa_casos.iterrows():
            print(f"      - BO Desap: {caso['bo_desaparecimento']} → BO Morte: {caso['bo_morte']} ({caso['dias_entre_eventos']} dias)")
    
    # Remove duplicatas mantendo a correlação mais forte
    print(f"\n🔧 Aplicando regra de deduplicação:")
    print(f"   1. Prioridade: menor intervalo de dias")
    print(f"   2. Se empate: mantém o primeiro registro")
    
    # Ordena por pessoa e dias (menor primeiro)
    df_sorted = df.sort_values(['chave_pessoa', 'dias_entre_eventos', 'bo_desaparecimento'])
    
    # Remove duplicatas mantendo o primeiro (menor intervalo)
    df_dedup = df_sorted.drop_duplicates(subset=['chave_pessoa'], keep='first')
    
    print(f"\n✅ Resultado:")
    print(f"   Antes: {len(df)} correlações")
    print(f"   Depois: {len(df_dedup)} correlações únicas")
    print(f"   Removidos: {len(df) - len(df_dedup)} duplicatas")
    
    # Estatísticas após deduplicação
    print(f"\n📊 Estatísticas (após deduplicação):")
    fortes = len(df_dedup[df_dedup['forca_correlacao'] == 'FORTE'])
    medias = len(df_dedup[df_dedup['forca_correlacao'] == 'MÉDIA'])
    fracas = len(df_dedup[df_dedup['forca_correlacao'] == 'FRACA'])
    
    print(f"   FORTES (0-30 dias): {fortes}")
    print(f"   MÉDIAS (31-90 dias): {medias}")
    print(f"   FRACAS (>90 dias): {fracas}")
    
    # Salva arquivo deduplicado
    arquivo_saida = Path('output/correlacoes_unicas_deduplicadas.xlsx')
    print(f"\n💾 Salvando arquivo deduplicado: {arquivo_saida}")
    
    with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
        # Todas as correlações únicas
        df_dedup.to_excel(writer, sheet_name='Correlações Únicas', index=False)
        
        # Por força
        df_fortes = df_dedup[df_dedup['forca_correlacao'] == 'FORTE'].copy()
        df_medias = df_dedup[df_dedup['forca_correlacao'] == 'MÉDIA'].copy()
        df_fracas = df_dedup[df_dedup['forca_correlacao'] == 'FRACA'].copy()
        
        df_fortes.to_excel(writer, sheet_name='FORTES - Únicas', index=False)
        df_medias.to_excel(writer, sheet_name='MÉDIAS - Únicas', index=False)
        df_fracas.to_excel(writer, sheet_name='FRACAS - Únicas', index=False)
        
        # Estatísticas
        stats = {
            'Métrica': [
                'Total Original',
                'Duplicatas Removidas',
                'Total Único',
                '',
                'FORTES (0-30 dias)',
                'MÉDIAS (31-90 dias)',
                'FRACAS (>90 dias)',
                '',
                'Pessoas com múltiplas correlações',
                'Critério deduplicação'
            ],
            'Valor': [
                len(df),
                len(df) - len(df_dedup),
                len(df_dedup),
                '',
                fortes,
                medias,
                fracas,
                '',
                len(pessoas_duplicadas),
                'Menor intervalo de dias'
            ]
        }
        
        pd.DataFrame(stats).to_excel(writer, sheet_name='Estatísticas', index=False)
        
        # Lista de casos removidos (duplicatas)
        df_removidos = df[~df.index.isin(df_dedup.index)].copy()
        df_removidos = df_removidos.sort_values(['nome', 'dias_entre_eventos'])
        df_removidos.to_excel(writer, sheet_name='Duplicatas Removidas', index=False)
    
    print(f"   ✓ {len(df_dedup)} correlações únicas")
    print(f"   ✓ 5 abas: Únicas, FORTES, MÉDIAS, FRACAS, Estatísticas, Duplicatas")
    
    print("\n" + "=" * 80)
    print("✅ DEDUPLICAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print(f"\nArquivo: {arquivo_saida}")
    print(f"\nAgora use este arquivo para validação com IA!")
    print(f"Comando: Substitua 'correlacoes_completas_com_identificacao.xlsx'")
    print(f"         por 'correlacoes_unicas_deduplicadas.xlsx'")
    
    return df_dedup


if __name__ == "__main__":
    remover_duplicatas()
