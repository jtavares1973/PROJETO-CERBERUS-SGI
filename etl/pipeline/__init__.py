"""
Submódulo de pipeline ETL.
Orquestra o fluxo completo de processamento de dados.
"""

from .etl_pipeline import ETLPipeline, run_pipeline

__all__ = [
    "ETLPipeline",
    "run_pipeline",
]
