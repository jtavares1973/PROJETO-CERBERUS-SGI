"""
Modelos de dados para pessoas e eventos criminais.
"""

from datetime import date, datetime
from typing import Optional
from pydantic import Field, field_validator
from .base import BaseModel


class Pessoa(BaseModel):
    """Modelo base para dados de pessoa."""
    
    nome: str = Field(..., min_length=1, description="Nome completo")
    nome_mae: Optional[str] = Field(None, description="Nome da mãe")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento")
    cpf: Optional[str] = Field(None, description="CPF")
    rg: Optional[str] = Field(None, description="RG")
    sexo: Optional[str] = Field(None, description="Sexo (M/F)")
    
    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, v: Optional[str]) -> Optional[str]:
        """Remove formatação do CPF."""
        if v:
            return ''.join(filter(str.isdigit, v))
        return v
    
    @field_validator("sexo")
    @classmethod
    def validate_sexo(cls, v: Optional[str]) -> Optional[str]:
        """Normaliza sexo para M/F."""
        if v:
            v = v.upper().strip()
            if v in ["M", "MASCULINO", "MASC"]:
                return "M"
            elif v in ["F", "FEMININO", "FEM"]:
                return "F"
        return v


class Desaparecimento(Pessoa):
    """Modelo para registro de desaparecimento."""
    
    data_desaparecimento: datetime = Field(..., description="Data do desaparecimento")
    local_desaparecimento: Optional[str] = Field(None, description="Local do desaparecimento")
    circunstancias: Optional[str] = Field(None, description="Circunstâncias do desaparecimento")
    boletim_ocorrencia: Optional[str] = Field(None, description="Número do BO")
    status: str = Field(default="ativo", description="Status do caso")


class Homicidio(Pessoa):
    """Modelo para registro de homicídio."""
    
    data_homicidio: datetime = Field(..., description="Data do homicídio")
    local_homicidio: Optional[str] = Field(None, description="Local do homicídio")
    causa_morte: Optional[str] = Field(None, description="Causa da morte")
    arma_utilizada: Optional[str] = Field(None, description="Arma utilizada")
    boletim_ocorrencia: Optional[str] = Field(None, description="Número do BO")
    status: str = Field(default="em_investigacao", description="Status do caso")


class Cadaver(BaseModel):
    """Modelo para registro de cadáver localizado."""
    
    data_localizacao: datetime = Field(..., description="Data da localização")
    local_localizacao: str = Field(..., description="Local onde foi encontrado")
    sexo: Optional[str] = Field(None, description="Sexo presumido")
    idade_estimada: Optional[int] = Field(None, description="Idade estimada")
    caracteristicas: Optional[str] = Field(None, description="Características físicas")
    causa_morte_estimada: Optional[str] = Field(None, description="Causa da morte estimada")
    estado_conservacao: Optional[str] = Field(None, description="Estado de conservação")
    identificado: bool = Field(default=False, description="Se foi identificado")
    nome_identificado: Optional[str] = Field(None, description="Nome se identificado")
    boletim_ocorrencia: Optional[str] = Field(None, description="Número do BO")
    
    @field_validator("sexo")
    @classmethod
    def validate_sexo(cls, v: Optional[str]) -> Optional[str]:
        """Normaliza sexo para M/F."""
        if v:
            v = v.upper().strip()
            if v in ["M", "MASCULINO", "MASC"]:
                return "M"
            elif v in ["F", "FEMININO", "FEM"]:
                return "F"
        return v
