"""
Módulo ETL (Extract, Transform, Load) do CERBERUS.
Processa e integra dados de desaparecimentos, homicídios e cadáveres.
"""

from .padronizacao import padronizar_dataset, PadronizadorBase
from .matching import match_datasets, MatchingEngine
from .pipeline import ETLPipeline, run_pipeline

__all__ = [
    "padronizar_dataset",
    "PadronizadorBase",
    "match_datasets",
    "MatchingEngine",
    "ETLPipeline",
    "run_pipeline",
]
