"""
Módulo de modelos de dados com Pydantic.
Define estruturas de dados para desaparecimentos, homicídios e cadáveres.
"""

from .base import BaseModel
from .pessoa import Pessoa, Desaparecimento, Homicidio, Cadaver
from .matching import MatchResult, MatchKey

__all__ = [
    "BaseModel",
    "Pessoa",
    "Desaparecimento",
    "Homicidio",
    "Cadaver",
    "MatchResult",
    "MatchKey",
]
