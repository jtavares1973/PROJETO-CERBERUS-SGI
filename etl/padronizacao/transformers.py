"""
Transformadores específicos para cada tipo de dataset.
"""

import pandas as pd
from utils.normalization import normalize_name, normalize_document


def normalize_pessoa_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza dados básicos de pessoa.
    
    Args:
        df: DataFrame com dados de pessoa
        
    Returns:
        DataFrame normalizado
    """
    df = df.copy()
    
    # Normaliza nomes
    if "nome" in df.columns:
        df["nome_normalizado"] = df["nome"].apply(
            lambda x: normalize_name(x) if pd.notna(x) else ""
        )
    
    if "nome_mae" in df.columns:
        df["nome_mae_normalizado"] = df["nome_mae"].apply(
            lambda x: normalize_name(x) if pd.notna(x) else ""
        )
    
    # Normaliza documentos
    if "cpf" in df.columns:
        df["cpf_normalizado"] = df["cpf"].apply(
            lambda x: normalize_document(x) if pd.notna(x) else ""
        )
    
    if "rg" in df.columns:
        df["rg_normalizado"] = df["rg"].apply(
            lambda x: normalize_document(x) if pd.notna(x) else ""
        )
    
    # Normaliza sexo
    if "sexo" in df.columns:
        df["sexo"] = df["sexo"].apply(
            lambda x: x.upper().strip()[0] if pd.notna(x) and x else None
        )
    
    return df


def normalize_desaparecimento_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza dados de desaparecimento.
    
    Args:
        df: DataFrame com dados de desaparecimento
        
    Returns:
        DataFrame normalizado
    """
    df = normalize_pessoa_data(df)
    
    # Converte datas
    if "data_desaparecimento" in df.columns:
        df["data_desaparecimento"] = pd.to_datetime(
            df["data_desaparecimento"], errors="coerce"
        )
    
    # Normaliza local
    if "local_desaparecimento" in df.columns:
        df["local_desaparecimento"] = df["local_desaparecimento"].str.strip()
    
    return df


def normalize_homicidio_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza dados de homicídio.
    
    Args:
        df: DataFrame com dados de homicídio
        
    Returns:
        DataFrame normalizado
    """
    df = normalize_pessoa_data(df)
    
    # Converte datas
    if "data_homicidio" in df.columns:
        df["data_homicidio"] = pd.to_datetime(
            df["data_homicidio"], errors="coerce"
        )
    
    # Normaliza campos específicos
    if "local_homicidio" in df.columns:
        df["local_homicidio"] = df["local_homicidio"].str.strip()
    
    if "causa_morte" in df.columns:
        df["causa_morte"] = df["causa_morte"].str.strip()
    
    return df


def normalize_cadaver_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza dados de cadáver.
    
    Args:
        df: DataFrame com dados de cadáver
        
    Returns:
        DataFrame normalizado
    """
    df = df.copy()
    
    # Converte datas
    if "data_localizacao" in df.columns:
        df["data_localizacao"] = pd.to_datetime(
            df["data_localizacao"], errors="coerce"
        )
    
    # Normaliza local
    if "local_localizacao" in df.columns:
        df["local_localizacao"] = df["local_localizacao"].str.strip()
    
    # Normaliza sexo estimado
    if "sexo" in df.columns:
        df["sexo"] = df["sexo"].apply(
            lambda x: x.upper().strip()[0] if pd.notna(x) and x else None
        )
    
    # Se identificado, normaliza nome e cria campo "nome_normalizado" para matching
    if "nome_identificado" in df.columns:
        df["nome_normalizado"] = df["nome_identificado"].apply(
            lambda x: normalize_name(x) if pd.notna(x) else ""
        )
    
    return df
