"""
Submódulo de matching entre datasets.
Identifica correspondências entre registros criminais.
"""

from .engine import MatchingEngine, match_datasets
from .similarity import calculate_similarity, calculate_name_similarity

__all__ = [
    "MatchingEngine",
    "match_datasets",
    "calculate_similarity",
    "calculate_name_similarity",
]
