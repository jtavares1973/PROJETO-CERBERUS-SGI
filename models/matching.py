"""
Modelos para resultados de matching entre datasets.
"""

from typing import Optional, Dict, Any
from pydantic import Field
from .base import BaseModel


class MatchKey(BaseModel):
    """Chave de matching gerada para um registro."""
    
    record_id: str = Field(..., description="ID do registro original")
    source_dataset: str = Field(..., description="Dataset de origem")
    nome_normalizado: str = Field(..., description="Nome normalizado")
    nome_fonetico: Optional[str] = Field(None, description="Representação fonética do nome")
    cpf_normalizado: Optional[str] = Field(None, description="CPF normalizado")
    rg_normalizado: Optional[str] = Field(None, description="RG normalizado")
    data_nascimento: Optional[str] = Field(None, description="Data de nascimento")
    nome_mae_normalizado: Optional[str] = Field(None, description="Nome da mãe normalizado")
    composite_key: str = Field(..., description="Chave composta para matching")
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return self.model_dump()


class MatchResult(BaseModel):
    """Resultado de matching entre dois registros."""
    
    source_id: str = Field(..., description="ID do registro fonte")
    target_id: str = Field(..., description="ID do registro alvo")
    source_dataset: str = Field(..., description="Dataset fonte")
    target_dataset: str = Field(..., description="Dataset alvo")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Score de similaridade")
    match_type: str = Field(..., description="Tipo de match (exact, fuzzy, phonetic)")
    matched_fields: list[str] = Field(default_factory=list, description="Campos que deram match")
    confidence: str = Field(..., description="Nível de confiança (high, medium, low)")
    
    def is_high_confidence(self) -> bool:
        """Verifica se é um match de alta confiança."""
        return self.confidence == "high" and self.similarity_score >= 0.85
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return self.model_dump()
