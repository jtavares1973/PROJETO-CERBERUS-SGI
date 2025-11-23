"""
Engine de matching entre datasets.
"""

from typing import List, Dict, Any, Optional
import pandas as pd
from models.matching import MatchResult, MatchKey
from utils.key_generation import generate_composite_key, generate_phonetic_key
from .similarity import calculate_similarity


class MatchingEngine:
    """Engine para realizar matching entre datasets."""
    
    def __init__(self, similarity_threshold: float = 0.85):
        """
        Inicializa engine de matching.
        
        Args:
            similarity_threshold: Threshold mínimo de similaridade para match
        """
        self.similarity_threshold = similarity_threshold
        self.matches: List[MatchResult] = []
    
    def generate_keys(self, df: pd.DataFrame, source_dataset: str) -> List[MatchKey]:
        """
        Gera chaves de matching para um dataset.
        
        Args:
            df: DataFrame com dados
            source_dataset: Nome do dataset de origem
            
        Returns:
            Lista de MatchKey geradas
        """
        keys = []
        
        for idx, row in df.iterrows():
            # Prepara dados para geração de chave
            data = {
                "nome": row.get("nome_normalizado", ""),
                "cpf": row.get("cpf_normalizado", ""),
                "rg": row.get("rg_normalizado", ""),
                "data_nascimento": str(row.get("data_nascimento", "")),
                "nome_mae": row.get("nome_mae_normalizado", ""),
            }
            
            # Gera chaves
            composite_key = generate_composite_key(data)
            phonetic_key = generate_phonetic_key(data.get("nome", ""))
            
            match_key = MatchKey(
                record_id=str(idx),
                source_dataset=source_dataset,
                nome_normalizado=data["nome"],
                nome_fonetico=phonetic_key,
                cpf_normalizado=data["cpf"],
                rg_normalizado=data["rg"],
                data_nascimento=data["data_nascimento"],
                nome_mae_normalizado=data["nome_mae"],
                composite_key=composite_key,
            )
            
            keys.append(match_key)
        
        return keys
    
    def match_records(
        self,
        source_keys: List[MatchKey],
        target_keys: List[MatchKey],
    ) -> List[MatchResult]:
        """
        Realiza matching entre dois conjuntos de chaves.
        
        Args:
            source_keys: Chaves do dataset fonte
            target_keys: Chaves do dataset alvo
            
        Returns:
            Lista de matches encontrados
        """
        matches = []
        
        for source_key in source_keys:
            for target_key in target_keys:
                # Calcula similaridade
                similarity = calculate_similarity(
                    source_key.to_dict(),
                    target_key.to_dict(),
                )
                
                if similarity >= self.similarity_threshold:
                    # Determina tipo de match e campos correspondentes
                    match_type, matched_fields = self._analyze_match(
                        source_key, target_key
                    )
                    
                    # Determina confiança
                    confidence = self._calculate_confidence(similarity, matched_fields)
                    
                    match_result = MatchResult(
                        source_id=source_key.record_id,
                        target_id=target_key.record_id,
                        source_dataset=source_key.source_dataset,
                        target_dataset=target_key.source_dataset,
                        similarity_score=similarity,
                        match_type=match_type,
                        matched_fields=matched_fields,
                        confidence=confidence,
                    )
                    
                    matches.append(match_result)
        
        self.matches.extend(matches)
        return matches
    
    def _analyze_match(
        self, source: MatchKey, target: MatchKey
    ) -> tuple[str, List[str]]:
        """Analisa tipo de match e campos correspondentes."""
        matched_fields = []
        
        # Verifica matches exatos
        if source.composite_key == target.composite_key:
            return "exact", ["composite_key"]
        
        # Verifica campos individuais
        if source.cpf_normalizado and source.cpf_normalizado == target.cpf_normalizado:
            matched_fields.append("cpf")
        
        if source.nome_normalizado and source.nome_normalizado == target.nome_normalizado:
            matched_fields.append("nome")
        
        if source.nome_fonetico and source.nome_fonetico == target.nome_fonetico:
            matched_fields.append("nome_fonetico")
        
        if source.data_nascimento and source.data_nascimento == target.data_nascimento:
            matched_fields.append("data_nascimento")
        
        # Determina tipo baseado em campos correspondentes
        if "cpf" in matched_fields or len(matched_fields) >= 3:
            return "exact", matched_fields
        elif "nome_fonetico" in matched_fields:
            return "phonetic", matched_fields
        else:
            return "fuzzy", matched_fields
    
    def _calculate_confidence(
        self, similarity: float, matched_fields: List[str]
    ) -> str:
        """Calcula nível de confiança do match."""
        if similarity >= 0.95 and ("cpf" in matched_fields or len(matched_fields) >= 3):
            return "high"
        elif similarity >= 0.85:
            return "medium"
        else:
            return "low"
    
    def get_matches(self) -> List[MatchResult]:
        """Retorna todos os matches encontrados."""
        return self.matches


def match_datasets(
    df_source: pd.DataFrame,
    df_target: pd.DataFrame,
    source_name: str,
    target_name: str,
    similarity_threshold: float = 0.85,
) -> List[MatchResult]:
    """
    Realiza matching entre dois datasets.
    
    Args:
        df_source: DataFrame fonte
        df_target: DataFrame alvo
        source_name: Nome do dataset fonte
        target_name: Nome do dataset alvo
        similarity_threshold: Threshold de similaridade
        
    Returns:
        Lista de matches encontrados
    """
    engine = MatchingEngine(similarity_threshold)
    
    # Gera chaves
    source_keys = engine.generate_keys(df_source, source_name)
    target_keys = engine.generate_keys(df_target, target_name)
    
    # Realiza matching
    matches = engine.match_records(source_keys, target_keys)
    
    return matches
