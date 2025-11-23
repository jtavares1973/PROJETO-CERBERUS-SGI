"""
Funções de normalização de texto e dados.
Prepara dados para matching e análise.
"""

import re
from typing import Optional
from unidecode import unidecode


def normalize_text(text: Optional[str], remove_accents: bool = True, 
                   lowercase: bool = True, remove_special: bool = True) -> str:
    """
    Normaliza texto removendo acentos, convertendo para minúsculas e 
    removendo caracteres especiais.
    
    Args:
        text: Texto a ser normalizado
        remove_accents: Se deve remover acentuação
        lowercase: Se deve converter para minúsculas
        remove_special: Se deve remover caracteres especiais
        
    Returns:
        Texto normalizado
    """
    if not text:
        return ""
    
    # Remove espaços extras
    text = " ".join(text.split())
    
    # Remove acentos
    if remove_accents:
        text = unidecode(text)
    
    # Converte para minúsculas
    if lowercase:
        text = text.lower()
    
    # Remove caracteres especiais (mantém letras, números e espaços)
    if remove_special:
        text = re.sub(r'[^a-z0-9\s]', '', text)
    
    # Remove espaços múltiplos
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def normalize_name(name: Optional[str]) -> str:
    """
    Normaliza nome de pessoa para matching.
    Remove prefixos, sufixos e padroniza formato.
    
    Args:
        name: Nome a ser normalizado
        
    Returns:
        Nome normalizado
    """
    if not name:
        return ""
    
    # Normaliza texto básico
    normalized = normalize_text(name)
    
    # Remove prefixos comuns (dr, sr, sra, etc)
    prefixes = ['dr', 'dra', 'sr', 'sra', 'srta', 'prof', 'profa']
    words = normalized.split()
    words = [w for w in words if w not in prefixes]
    
    # Remove sufixos comuns (jr, filho, neto, etc)
    suffixes = ['jr', 'junior', 'filho', 'filha', 'neto', 'neta', 'sobrinho', 'sobrinha']
    words = [w for w in words if w not in suffixes]
    
    return " ".join(words)


def normalize_document(document: Optional[str]) -> str:
    """
    Normaliza números de documento (CPF, RG, etc).
    Remove pontuação e formatação.
    
    Args:
        document: Número do documento
        
    Returns:
        Documento normalizado (apenas números)
    """
    if not document:
        return ""
    
    # Remove tudo que não é número
    return re.sub(r'\D', '', document)
