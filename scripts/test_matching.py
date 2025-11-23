"""
Script de exemplo para testar matching entre registros.
"""

import pandas as pd
from etl.matching import match_datasets
from etl.padronizacao import padronizar_dataset


def create_sample_data():
    """Cria dados de exemplo para teste."""
    # Dataset de desaparecimentos
    desaparecimentos = pd.DataFrame([
        {
            "nome": "João da Silva",
            "data_nascimento": "1990-01-01",
            "cpf": "123.456.789-09",
            "nome_mae": "Maria da Silva",
            "data_desaparecimento": "2023-01-15",
            "sexo": "M",
        },
        {
            "nome": "José Carlos Santos",
            "data_nascimento": "1985-05-20",
            "cpf": "987.654.321-00",
            "nome_mae": "Ana Santos",
            "data_desaparecimento": "2023-02-10",
            "sexo": "M",
        },
    ])
    
    # Dataset de cadáveres (com identificação)
    cadaveres = pd.DataFrame([
        {
            "nome_identificado": "Joao Silva",  # Nome similar ao primeiro
            "sexo": "M",
            "idade_estimada": 33,
            "data_localizacao": "2023-01-20",
            "local_localizacao": "Parque Municipal",
            "identificado": True,
        },
        {
            "nome_identificado": "Jose Carlos Santos",  # Similar ao segundo
            "sexo": "M",
            "idade_estimada": 38,
            "data_localizacao": "2023-03-05",
            "local_localizacao": "Rodovia BR-101",
            "identificado": True,
        },
    ])
    
    return desaparecimentos, cadaveres


def main():
    """Executa teste de matching."""
    print("=== Teste de Matching entre Datasets ===\n")
    
    # Cria dados de exemplo
    df_desap, df_cadav = create_sample_data()
    
    print("Datasets criados:")
    print(f"  Desaparecimentos: {len(df_desap)} registros")
    print(f"  Cadáveres: {len(df_cadav)} registros")
    
    # Padroniza datasets
    print("\nPadronizando datasets...")
    df_desap_pad = padronizar_dataset(df_desap, "desaparecimento")
    df_cadav_pad = padronizar_dataset(df_cadav, "cadaver")
    
    # Realiza matching
    print("\nRealizando matching...")
    matches = match_datasets(
        df_desap_pad,
        df_cadav_pad,
        "desaparecimentos",
        "cadaveres",
        similarity_threshold=0.70,  # Threshold mais baixo para exemplo
    )
    
    # Exibe resultados
    print(f"\nMatches encontrados: {len(matches)}")
    for i, match in enumerate(matches, 1):
        print(f"\nMatch {i}:")
        print(f"  Desaparecimento ID: {match.source_id}")
        print(f"  Cadáver ID: {match.target_id}")
        print(f"  Similaridade: {match.similarity_score:.2%}")
        print(f"  Tipo: {match.match_type}")
        print(f"  Confiança: {match.confidence}")
        print(f"  Campos correspondentes: {', '.join(match.matched_fields)}")


if __name__ == "__main__":
    main()
