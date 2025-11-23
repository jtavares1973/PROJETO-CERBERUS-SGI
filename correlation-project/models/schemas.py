"""Modelos Pydantic para validação de dados"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class PessoaBase(BaseModel):
    """Modelo base para dados de uma pessoa"""
    
    # Identificação
    id_unico: str = Field(..., description="ID único gerado")
    nome: str = Field(..., description="Nome completo")
    nome_normalizado: str = Field(..., description="Nome normalizado para matching")
    
    # Dados pessoais
    data_nascimento: Optional[datetime] = Field(None, description="Data de nascimento")
    sexo: str = Field(..., description="Sexo: M, F ou IGN")
    idade_estimativa: Optional[int] = Field(None, description="Idade estimada")
    nome_mae: Optional[str] = Field(None, description="Nome da mãe")
    nome_pai: Optional[str] = Field(None, description="Nome do pai")
    local_de_referencia: Optional[str] = Field(None, description="Local de referência")
    
    # Chaves para matching
    chave_forte: Optional[str] = Field(None, description="Nome + data nascimento completa")
    chave_moderada: Optional[str] = Field(None, description="Nome + ano nascimento")
    chave_fraca: Optional[str] = Field(None, description="Apenas nome normalizado")
    
    @validator('sexo')
    def validar_sexo(cls, v):
        """Valida o campo sexo"""
        if v not in ['M', 'F', 'IGN']:
            return 'IGN'
        return v
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S') if v else None
        }


class RegistroDesaparecimento(BaseModel):
    """Dados específicos de desaparecimento"""
    
    data_desaparecimento: Optional[datetime] = None
    boletim_desaparecimento: Optional[str] = None
    historico_desaparecimento: Optional[str] = None
    unidade_registro: Optional[str] = None
    pessoa_localizada: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S') if v else None
        }


class RegistroLocalizacaoCadaver(BaseModel):
    """Dados específicos de localização de cadáver"""
    
    data_localizacao_cadaver: Optional[datetime] = None
    boletim_localizacao: Optional[str] = None
    local_cadaver: Optional[str] = None
    causa_morte_presumida: Optional[str] = None
    possui_laudo_iml: Optional[str] = None
    cod_iml_pessoa: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S') if v else None
        }


class RegistroHomicidio(BaseModel):
    """Dados específicos de homicídio"""
    
    data_homicidio: Optional[datetime] = None
    boletim_homicidio: Optional[str] = None
    arma_usada: Optional[str] = None
    tipo_homicidio: Optional[str] = None
    circunstancias_homicidio: Optional[str] = None
    local_homicidio: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S') if v else None
        }


class TranstornoPsiquiatrico(BaseModel):
    """Dados sobre transtornos psiquiátricos detectados"""
    
    tem_transtorno_psiquiatrico: bool = False
    tipo_transtorno: Optional[str] = None
    evidencia_transtorno: Optional[str] = None
    confianca_transtorno: str = 'inconclusivo'
    
    @validator('confianca_transtorno')
    def validar_confianca(cls, v):
        """Valida o nível de confiança"""
        if v not in ['alta', 'media', 'baixa', 'inconclusivo']:
            return 'inconclusivo'
        return v


class MatchInfo(BaseModel):
    """Informações sobre o matching realizado"""
    
    match_forte: bool = False
    match_moderado: bool = False
    match_fraco: bool = False
    fonte_match: Optional[str] = Field(None, description="De onde veio o match")
    ids_relacionados: Optional[str] = Field(None, description="IDs dos registros relacionados")


class RegistroUnificado(BaseModel):
    """Modelo unificado completo"""
    
    # Dados da pessoa (obrigatórios)
    pessoa: PessoaBase
    
    # Dados de desaparecimento (opcional)
    desaparecimento: Optional[RegistroDesaparecimento] = None
    
    # Dados de localização de cadáver (opcional)
    cadaver: Optional[RegistroLocalizacaoCadaver] = None
    
    # Dados de homicídio (opcional)
    homicidio: Optional[RegistroHomicidio] = None
    
    # Transtorno psiquiátrico
    transtorno: Optional[TranstornoPsiquiatrico] = None
    
    # Informações de matching
    matching: MatchInfo
    
    # Classificação final
    classificacao_final: str = Field(
        ..., 
        description="Classificação do caso"
    )
    
    @validator('classificacao_final')
    def validar_classificacao(cls, v):
        """Valida a classificação final"""
        classificacoes_validas = [
            "Desaparecido sem desfecho",
            "Desaparecido localizado vivo",
            "Desaparecido encontrado morto",
            "Desaparecido vítima de homicídio",
            "Cadáver sem registro de desaparecimento",
            "Homicídio sem registro de desaparecimento",
        ]
        
        if v not in classificacoes_validas:
            return "Desaparecido sem desfecho"
        return v
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S') if v else None
        }
    
    def to_flat_dict(self) -> dict:
        """Converte para um dicionário flat (uma linha de CSV)"""
        flat = {}
        
        # Dados da pessoa
        for key, value in self.pessoa.dict().items():
            flat[f'pessoa_{key}'] = value
        
        # Desaparecimento
        if self.desaparecimento:
            for key, value in self.desaparecimento.dict().items():
                flat[f'desap_{key}'] = value
        
        # Cadáver
        if self.cadaver:
            for key, value in self.cadaver.dict().items():
                flat[f'cadaver_{key}'] = value
        
        # Homicídio
        if self.homicidio:
            for key, value in self.homicidio.dict().items():
                flat[f'homic_{key}'] = value
        
        # Transtorno
        if self.transtorno:
            for key, value in self.transtorno.dict().items():
                flat[f'transt_{key}'] = value
        
        # Matching
        for key, value in self.matching.dict().items():
            flat[f'match_{key}'] = value
        
        # Classificação
        flat['classificacao_final'] = self.classificacao_final
        
        return flat
