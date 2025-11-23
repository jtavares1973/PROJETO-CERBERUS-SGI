"""
Classes base para padronização de datasets.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
import pandas as pd
from utils.normalization import normalize_name, normalize_document
from utils.validation import validate_cpf


class PadronizadorBase(ABC):
    """Classe base para padronizadores de datasets."""
    
    def __init__(self):
        self.errors: List[Dict[str, Any]] = []
    
    @abstractmethod
    def padronizar(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Padroniza um DataFrame.
        
        Args:
            df: DataFrame a ser padronizado
            
        Returns:
            DataFrame padronizado
        """
        pass
    
    def _normalizar_nomes(self, df: pd.DataFrame, campos: List[str]) -> pd.DataFrame:
        """Normaliza campos de nome."""
        for campo in campos:
            if campo in df.columns:
                df[f"{campo}_normalizado"] = df[campo].apply(
                    lambda x: normalize_name(x) if pd.notna(x) else ""
                )
        return df
    
    def _normalizar_documentos(self, df: pd.DataFrame, campos: List[str]) -> pd.DataFrame:
        """Normaliza campos de documento."""
        for campo in campos:
            if campo in df.columns:
                df[f"{campo}_normalizado"] = df[campo].apply(
                    lambda x: normalize_document(x) if pd.notna(x) else ""
                )
        return df
    
    def _validar_cpfs(self, df: pd.DataFrame, campo: str = "cpf") -> pd.DataFrame:
        """Valida CPFs e marca inválidos."""
        if campo in df.columns:
            df[f"{campo}_valido"] = df[campo].apply(
                lambda x: validate_cpf(x) if pd.notna(x) else False
            )
        return df
    
    def get_errors(self) -> List[Dict[str, Any]]:
        """Retorna erros encontrados durante padronização."""
        return self.errors


def padronizar_dataset(df: pd.DataFrame, tipo_dataset: str) -> pd.DataFrame:
    """
    Padroniza dataset de acordo com o tipo.
    
    Args:
        df: DataFrame a padronizar
        tipo_dataset: Tipo do dataset (desaparecimento, homicidio, cadaver)
        
    Returns:
        DataFrame padronizado
    """
    from .transformers import (
        normalize_desaparecimento_data,
        normalize_homicidio_data,
        normalize_cadaver_data,
    )
    
    if tipo_dataset == "desaparecimento":
        return normalize_desaparecimento_data(df)
    elif tipo_dataset == "homicidio":
        return normalize_homicidio_data(df)
    elif tipo_dataset == "cadaver":
        return normalize_cadaver_data(df)
    else:
        raise ValueError(f"Tipo de dataset desconhecido: {tipo_dataset}")
