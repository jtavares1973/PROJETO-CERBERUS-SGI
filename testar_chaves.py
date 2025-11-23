"""
Script de teste para validar a geração de chaves de correlação.
"""

import pandas as pd
from utils.chaves import (
    gerar_chave_ocorrencia,
    gerar_chave_pessoa,
    identificar_natureza_alvo,
    identificar_papel_pessoa,
    enriquecer_com_chaves,
    filtrar_grupo_alvo
)


def testar_chaves():
    print("=" * 60)
    print("TESTE DE GERAÇÃO DE CHAVES DE CORRELAÇÃO")
    print("=" * 60)
    
    # Dados de teste
    dados_teste = {
        'ano_registro': ['2023', '2023', '2024'],
        'unidade_registro': ['16º DP', '5º DP', '12º DP'],
        'numero_ocorrencia': ['12345', '67890', '11111'],
        'nome_envolvido': ['João da Silva', 'Maria Oliveira', 'José Santos'],
        'data_nascimento': ['1985-03-15', '1990-07-22', '1978-11-30'],
        'natureza': ['DESAPARECIMENTO DE PESSOA', 'HOMICIDIO', 'LOCALIZACAO OU REMOCAO CADAVER'],
        'papel_envolvido': ['VITIMA', 'VITIMA', 'VITIMA']
    }
    
    df_teste = pd.DataFrame(dados_teste)
    
    print("\n1. TESTANDO CHAVE DE OCORRÊNCIA:")
    print("-" * 60)
    for idx, row in df_teste.iterrows():
        chave = gerar_chave_ocorrencia(row)
        print(f"   {row['ano_registro']} + {row['unidade_registro']} + {row['numero_ocorrencia']}")
        print(f"   → {chave}")
        print()
    
    print("\n2. TESTANDO CHAVE DE PESSOA:")
    print("-" * 60)
    for idx, row in df_teste.iterrows():
        chave = gerar_chave_pessoa(row)
        print(f"   {row['nome_envolvido']} ({row['data_nascimento']})")
        print(f"   → {chave}")
        print()
    
    print("\n3. TESTANDO CLASSIFICAÇÃO DE NATUREZA:")
    print("-" * 60)
    for natureza in df_teste['natureza']:
        classificacao = identificar_natureza_alvo(natureza)
        print(f"   {natureza}")
        print(f"   → {classificacao}")
        print()
    
    print("\n4. TESTANDO CLASSIFICAÇÃO DE PAPEL:")
    print("-" * 60)
    for papel in df_teste['papel_envolvido']:
        classificacao = identificar_papel_pessoa(papel)
        print(f"   {papel}")
        print(f"   → {classificacao}")
        print()
    
    print("\n5. TESTANDO ENRIQUECIMENTO COMPLETO:")
    print("-" * 60)
    df_enriquecido = enriquecer_com_chaves(df_teste)
    print(f"\nColunas adicionadas: {list(df_enriquecido.columns[-4:])}")
    print("\nAmostra do resultado:")
    print(df_enriquecido[['chave_ocorrencia', 'chave_pessoa', 'natureza_alvo', 'papel_pessoa']])
    
    print("\n6. TESTANDO FILTRO DE GRUPO-ALVO:")
    print("-" * 60)
    df_filtrado = filtrar_grupo_alvo(df_enriquecido, apenas_vitimas=True)
    print(f"\nRegistros após filtro: {len(df_filtrado)}")
    
    print("\n" + "=" * 60)
    print("TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 60)


if __name__ == "__main__":
    testar_chaves()
