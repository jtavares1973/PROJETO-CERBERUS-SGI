"""Funções utilitárias para normalização de dados"""
import re
import unicodedata
from datetime import datetime
from typing import Optional, Tuple
import pandas as pd


def limpar_texto_sujo(texto: str) -> str:
    """
    Remove caracteres de controle, lixo e corrige encoding incorreto.
    Aplica antes de qualquer processamento.
    """
    if not isinstance(texto, str) or pd.isna(texto):
        return ""
    
    # 1. Corrigir UTF-8 mal-interpretado como Latin-1
    try:
        if any(char in texto for char in ['Ã', 'Â', 'Ê', 'Ç', 'É']):
            try:
                texto = texto.encode('latin-1').decode('utf-8', errors='ignore')
            except (UnicodeDecodeError, UnicodeEncodeError):
                pass
    except:
        pass
    
    # 2. Substituições de UTF-8 mal-codificado
    substituicoes = {
        'Ã£': 'ã', 'Ã¡': 'á', 'Ã¢': 'â', 'Ã ': 'à', 'Ãµ': 'õ', 'Ã³': 'ó', 'Ã´': 'ô',
        'Ã©': 'é', 'Ãª': 'ê', 'Ã­': 'í', 'Ãº': 'ú', 'Ã§': 'ç',
        'Ã': 'Ã', 'Ã‰': 'É', 'ÃŠ': 'Ê', 'Ã"': 'Ó', 'Ã‡': 'Ç',
        'Â': '', 
    }
    
    for errado, correto in substituicoes.items():
        texto = texto.replace(errado, correto)
    
    # 3. Remove caracteres de controle (exceto tab, newline, carriage return)
    texto = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', texto)
    
    # 4. Remove BOM e zero-width characters
    texto = re.sub(r'[\uFEFF\u200B-\u200D\uFFFE\uFFFF]', '', texto)
    
    # 5. Remove APENAS caracteres de controle, preserva acentos e caracteres Unicode válidos
    # Não usar isprintable() pois remove acentos
    caracteres_proibidos = set(range(0x00, 0x09)) | set(range(0x0E, 0x20)) | {0x7F}
    texto = ''.join(c for c in texto if ord(c) not in caracteres_proibidos)
    
    # 6. Normaliza espaços
    texto = re.sub(r'\s+', ' ', texto)
    
    return texto.strip()


def remover_acentos(texto: str) -> str:
    """Remove acentos de uma string"""
    if not isinstance(texto, str):
        return ""
    
    # Limpa antes de processar
    texto = limpar_texto_sujo(texto)
    
    nfkd = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])


def normalizar_nome(nome: str, remover_preposicoes: bool = False) -> str:
    """
    Normaliza um nome para facilitar matching.
    
    Args:
        nome: Nome a ser normalizado
        remover_preposicoes: Se True, remove preposições como 'da', 'de', 'dos'
    
    Returns:
        Nome normalizado
    """
    if not isinstance(nome, str) or pd.isna(nome):
        return ""
    
    # Limpar caracteres inválidos primeiro
    nome = limpar_texto_sujo(nome)
    
    # Converter para minúsculas
    nome = nome.lower().strip()
    
    # Remover acentos
    nome = remover_acentos(nome)
    
    # Remover pontuação
    nome = re.sub(r'[^\w\s]', '', nome)
    
    # Remover múltiplos espaços
    nome = re.sub(r'\s+', ' ', nome)
    
    # Opcional: remover preposições
    if remover_preposicoes:
        preposicoes = ['da', 'de', 'do', 'dos', 'das']
        palavras = nome.split()
        palavras = [p for p in palavras if p not in preposicoes]
        nome = ' '.join(palavras)
    
    return nome.strip()


def normalizar_sexo(sexo: str) -> str:
    """
    Normaliza o campo sexo.
    
    Returns:
        'M', 'F' ou 'IGN'
    """
    if not isinstance(sexo, str) or pd.isna(sexo):
        return 'IGN'
    
    sexo = sexo.upper().strip()
    
    if sexo in ['M', 'MASCULINO', 'MASC', 'H', 'HOMEM']:
        return 'M'
    elif sexo in ['F', 'FEMININO', 'FEM', 'MULHER']:
        return 'F'
    else:
        return 'IGN'


def parse_data(data_str: str, formatos: Optional[list] = None) -> Optional[datetime]:
    """
    Tenta parsear uma data em diversos formatos.
    
    Args:
        data_str: String com a data
        formatos: Lista de formatos a tentar (opcional)
    
    Returns:
        datetime ou None se falhar
    """
    if not isinstance(data_str, str) or pd.isna(data_str):
        return None
    
    if formatos is None:
        formatos = [
            '%d/%m/%Y',
            '%d/%m/%Y %H:%M',
            '%d/%m/%Y %H:%M:%S',
            '%Y-%m-%d',
            '%Y-%m-%d %H:%M:%S',
            '%d-%m-%Y',
        ]
    
    for formato in formatos:
        try:
            return datetime.strptime(data_str, formato)
        except (ValueError, TypeError):
            continue
    
    return None


def calcular_idade(data_nascimento: datetime, data_referencia: Optional[datetime] = None) -> Optional[int]:
    """
    Calcula a idade com base na data de nascimento.
    
    Args:
        data_nascimento: Data de nascimento
        data_referencia: Data de referência (default: hoje)
    
    Returns:
        Idade em anos ou None
    """
    if not data_nascimento:
        return None
    
    if not data_referencia:
        data_referencia = datetime.now()
    
    idade = data_referencia.year - data_nascimento.year
    
    # Ajustar se ainda não fez aniversário no ano
    if (data_referencia.month, data_referencia.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1
    
    return idade if idade >= 0 else None


def extrair_ano(data: datetime) -> Optional[int]:
    """Extrai o ano de uma data"""
    return data.year if data else None


def gerar_chave_forte(nome_normalizado: str, data_nascimento: Optional[datetime]) -> Optional[str]:
    """
    Gera chave forte para matching: nome + data completa de nascimento
    
    Returns:
        Chave ou None se faltarem dados
    """
    if not nome_normalizado or data_nascimento is None or pd.isna(data_nascimento):
        return None
    
    try:
        return f"{nome_normalizado}|{data_nascimento.strftime('%Y-%m-%d')}"
    except (AttributeError, ValueError):
        return None


def gerar_chave_moderada(nome_normalizado: str, ano_nascimento: Optional[int]) -> Optional[str]:
    """
    Gera chave moderada para matching: nome + ano de nascimento
    
    Returns:
        Chave ou None se faltarem dados
    """
    if not nome_normalizado or ano_nascimento is None or pd.isna(ano_nascimento):
        return None
    
    try:
        return f"{nome_normalizado}|{int(ano_nascimento)}"
    except (ValueError, TypeError):
        return None


def gerar_chave_fraca(nome_normalizado: str) -> Optional[str]:
    """
    Gera chave fraca para matching: apenas nome
    
    Returns:
        Chave ou None se faltar nome
    """
    if not nome_normalizado:
        return None
    
    return nome_normalizado


def limpar_texto(texto: str) -> str:
    """
    Limpa um texto removendo caracteres especiais e normalizando espaços.
    Aplica limpeza profunda de caracteres inválidos.
    """
    if not isinstance(texto, str) or pd.isna(texto):
        return ""
    
    # Limpar caracteres inválidos PRIMEIRO
    texto = limpar_texto_sujo(texto)
    
    # Remover quebras de linha excessivas
    texto = re.sub(r'\n+', ' ', texto)
    
    # Remover múltiplos espaços
    texto = re.sub(r'\s+', ' ', texto)
    
    return texto.strip()


def validar_data_nascimento(data_nascimento: datetime, data_fato: Optional[datetime] = None) -> bool:
    """
    Valida se a data de nascimento é plausível.
    
    Args:
        data_nascimento: Data a validar
        data_fato: Data do fato (opcional)
    
    Returns:
        True se válida
    """
    if not data_nascimento:
        return False
    
    # Não pode ser no futuro
    if data_nascimento > datetime.now():
        return False
    
    # Não pode ser muito antiga (> 120 anos)
    idade = calcular_idade(data_nascimento)
    if idade and idade > 120:
        return False
    
    # Se temos data do fato, validar contra ela
    if data_fato:
        idade_no_fato = calcular_idade(data_nascimento, data_fato)
        if idade_no_fato and (idade_no_fato < 0 or idade_no_fato > 120):
            return False
    
    return True
