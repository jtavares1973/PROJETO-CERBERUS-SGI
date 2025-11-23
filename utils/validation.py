"""
Funções de validação de dados.
Valida documentos e formatos de dados.
"""

import re
from datetime import datetime
from typing import Optional


def validate_cpf(cpf: Optional[str]) -> bool:
    """
    Valida número de CPF brasileiro.
    
    Args:
        cpf: Número do CPF (com ou sem formatação)
        
    Returns:
        True se CPF é válido, False caso contrário
    """
    if not cpf:
        return False
    
    # Remove formatação
    cpf = re.sub(r'\D', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Valida primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[9]) != digito1:
        return False
    
    # Valida segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    return int(cpf[10]) == digito2


def validate_date(date_str: Optional[str], date_format: str = "%Y-%m-%d") -> bool:
    """
    Valida formato de data.
    
    Args:
        date_str: String com a data
        date_format: Formato esperado da data
        
    Returns:
        True se data é válida, False caso contrário
    """
    if not date_str:
        return False
    
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def validate_nome(nome: Optional[str], min_length: int = 3) -> bool:
    """
    Valida nome de pessoa.
    
    Args:
        nome: Nome a validar
        min_length: Comprimento mínimo do nome
        
    Returns:
        True se nome é válido, False caso contrário
    """
    if not nome or len(nome.strip()) < min_length:
        return False
    
    # Verifica se tem pelo menos uma letra
    if not re.search(r'[a-zA-Z]', nome):
        return False
    
    return True
