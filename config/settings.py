"""
Configurações do sistema CERBERUS.
Define parâmetros para ETL, matching e processamento de dados criminais.
"""

from pathlib import Path
from typing import Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """Configurações principais do CERBERUS."""
    
    # Diretórios
    project_root: Path = Path(__file__).parent.parent
    output_dir: Path = project_root / "output"
    
    # Configurações de normalização
    remove_accents: bool = True
    lowercase: bool = True
    remove_special_chars: bool = True
    
    # Configurações de matching
    similarity_threshold: float = 0.85
    phonetic_matching: bool = True
    fuzzy_matching: bool = True
    
    # Configurações de chave de matching
    key_fields: list[str] = [
        "nome",
        "data_nascimento",
        "cpf",
        "rg",
        "nome_mae"
    ]
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    class Config:
        env_prefix = "CERBERUS_"
        case_sensitive = False


# Singleton para configurações
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Retorna instância única das configurações."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
