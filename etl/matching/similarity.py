"""
Funções de cálculo de similaridade entre registros.
"""

from typing import Dict, Any, Optional
from Levenshtein import ratio as levenshtein_ratio


def calculate_name_similarity(name1: str, name2: str) -> float:
    """
    Calcula similaridade entre dois nomes.
    Usa distância de Levenshtein.
    
    Args:
        name1: Primeiro nome
        name2: Segundo nome
        
    Returns:
        Score de similaridade (0.0 a 1.0)
    """
    if not name1 or not name2:
        return 0.0
    
    # Normaliza
    name1 = name1.lower().strip()
    name2 = name2.lower().strip()
    
    # Calcula similaridade
    return levenshtein_ratio(name1, name2)


def calculate_field_similarity(value1: Any, value2: Any) -> float:
    """
    Calcula similaridade entre dois valores de campo.
    
    Args:
        value1: Primeiro valor
        value2: Segundo valor
        
    Returns:
        Score de similaridade (0.0 a 1.0)
    """
    # Se ambos estão vazios
    if not value1 and not value2:
        return 0.0
    
    # Se apenas um está vazio
    if not value1 or not value2:
        return 0.0
    
    # Converte para string
    str1 = str(value1).strip().lower()
    str2 = str(value2).strip().lower()
    
    # Match exato
    if str1 == str2:
        return 1.0
    
    # Similaridade de string
    return levenshtein_ratio(str1, str2)


def calculate_similarity(record1: Dict[str, Any], record2: Dict[str, Any]) -> float:
    """
    Calcula similaridade geral entre dois registros.
    Usa ponderação de campos.
    
    Args:
        record1: Primeiro registro
        record2: Segundo registro
        
    Returns:
        Score de similaridade ponderado (0.0 a 1.0)
    """
    # Pesos dos campos (devem somar 1.0)
    weights = {
        "nome_normalizado": 0.30,
        "cpf_normalizado": 0.25,
        "data_nascimento": 0.15,
        "nome_mae_normalizado": 0.15,
        "rg_normalizado": 0.10,
        "nome_fonetico": 0.05,
    }
    
    total_score = 0.0
    total_weight = 0.0
    
    for field, weight in weights.items():
        value1 = record1.get(field)
        value2 = record2.get(field)
        
        # Se ambos os valores existem, calcula similaridade
        if value1 and value2:
            if field in ["nome_normalizado", "nome_mae_normalizado"]:
                field_score = calculate_name_similarity(value1, value2)
            else:
                field_score = calculate_field_similarity(value1, value2)
            
            total_score += field_score * weight
            total_weight += weight
    
    # Se nenhum campo foi comparado, retorna 0
    if total_weight == 0:
        return 0.0
    
    # Normaliza score pelo peso total usado
    return total_score / total_weight
