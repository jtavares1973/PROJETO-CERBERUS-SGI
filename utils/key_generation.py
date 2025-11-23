"""
Funções para geração de chaves de matching.
Cria identificadores únicos para comparação entre datasets.
"""

import hashlib
from typing import Optional, Dict, Any


def generate_phonetic_key(name: str) -> str:
    """
    Gera chave fonética simplificada para um nome.
    Usa algoritmo similar ao Soundex adaptado para português.
    
    Args:
        name: Nome para gerar chave fonética
        
    Returns:
        Chave fonética
    """
    if not name:
        return ""
    
    # Normaliza o nome
    name = name.upper().strip()
    
    # Mapeia letras para códigos fonéticos
    phonetic_map = {
        'B': '1', 'P': '1',
        'C': '2', 'K': '2', 'Q': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6',
        'F': '7', 'V': '7',
        'G': '8', 'J': '8',
        'S': '9', 'Z': '9', 'X': '9',
    }
    
    # Remove vogais exceto a primeira letra
    first_char = name[0] if name else ''
    result = first_char
    
    for i, char in enumerate(name[1:], 1):
        if char in phonetic_map:
            code = phonetic_map[char]
            # Evita códigos duplicados consecutivos
            if not result or result[-1] != code:
                result += code
    
    return result[:6].ljust(6, '0')


def generate_composite_key(data: Dict[str, Any], fields: list[str] = None) -> str:
    """
    Gera chave composta a partir de múltiplos campos.
    Usa hash para criar identificador único.
    
    Args:
        data: Dicionário com dados do registro
        fields: Lista de campos a usar na chave (usa campos padrão se None)
        
    Returns:
        Chave composta (hash MD5)
    """
    if fields is None:
        fields = ["nome", "data_nascimento", "cpf", "nome_mae"]
    
    # Concatena valores dos campos disponíveis
    key_parts = []
    for field in fields:
        value = data.get(field)
        if value:
            # Converte para string e normaliza
            str_value = str(value).strip().lower()
            key_parts.append(f"{field}:{str_value}")
    
    # Gera hash da concatenação
    composite = "|".join(key_parts)
    hash_obj = hashlib.md5(composite.encode('utf-8'))
    
    return hash_obj.hexdigest()


def generate_blocking_key(name: str, birth_year: Optional[str] = None) -> str:
    """
    Gera chave de bloqueio para reduzir comparações.
    Usa primeiras letras do nome e ano de nascimento.
    
    Args:
        name: Nome da pessoa
        birth_year: Ano de nascimento (opcional)
        
    Returns:
        Chave de bloqueio
    """
    if not name:
        return ""
    
    # Pega primeiras 3 letras do primeiro e último nome
    parts = name.strip().split()
    first_name = parts[0][:3] if parts else ""
    last_name = parts[-1][:3] if len(parts) > 1 else ""
    
    blocking_key = f"{first_name}{last_name}".upper()
    
    if birth_year:
        blocking_key += f"_{birth_year}"
    
    return blocking_key
