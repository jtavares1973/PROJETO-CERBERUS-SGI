"""
Script de exemplo para executar pipeline ETL completo.
"""

from pathlib import Path
from etl.pipeline import run_pipeline
from config import get_settings


def main():
    """Executa pipeline de exemplo."""
    settings = get_settings()
    
    # Configuração dos datasets
    # Ajuste os caminhos conforme seus arquivos reais
    datasets = {
        "desaparecimentos": {
            "filepath": Path("data/desaparecimentos.csv"),
            "type": "desaparecimento",
        },
        "homicidios": {
            "filepath": Path("data/homicidios.csv"),
            "type": "homicidio",
        },
        "cadaveres": {
            "filepath": Path("data/cadaveres.csv"),
            "type": "cadaver",
        },
    }
    
    # Pares de matching
    matching_pairs = [
        ("desaparecimentos", "cadaveres"),
        ("desaparecimentos", "homicidios"),
        ("homicidios", "cadaveres"),
    ]
    
    # Executa pipeline
    print("Iniciando pipeline ETL CERBERUS...")
    results = run_pipeline(datasets, matching_pairs, settings.output_dir)
    
    # Exibe resultados
    print("\n=== Resultados do Pipeline ===")
    print(f"Datasets padronizados: {len(results['padronizados'])}")
    for dataset in results['padronizados']:
        print(f"  - {dataset}")
    
    print(f"\nMatching realizados: {len(results['matches'])}")
    for match in results['matches']:
        print(f"  - {match['source']} x {match['target']}: {match['count']} matches")
    
    if results['errors']:
        print(f"\nErros encontrados: {len(results['errors'])}")
        for error in results['errors']:
            print(f"  - {error}")
    
    print(f"\nDuração total: {results['duration']:.2f} segundos")
    print(f"Outputs salvos em: {settings.output_dir}")


if __name__ == "__main__":
    main()
