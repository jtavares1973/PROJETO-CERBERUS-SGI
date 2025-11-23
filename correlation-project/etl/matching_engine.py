"""Engine de matching entre bases de dados"""
import pandas as pd
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass


@dataclass
class MatchResult:
    """Resultado de um match"""
    id_origem: str
    id_destino: str
    tipo_match: str  # 'forte', 'moderado', 'fraco'
    chave_usada: str
    confianca: float  # 0.0 a 1.0


class MatchingEngine:
    """Engine para fazer matching entre datasets"""
    
    def __init__(self):
        self.matches_fortes: List[MatchResult] = []
        self.matches_moderados: List[MatchResult] = []
        self.matches_fracos: List[MatchResult] = []
    
    def fazer_match_forte(
        self, 
        df_origem: pd.DataFrame, 
        df_destino: pd.DataFrame,
        col_chave: str = 'chave_forte',
        col_id_origem: str = 'id_unico',
        col_id_destino: str = 'id_unico'
    ) -> List[MatchResult]:
        """
        Faz match forte (nome + data nascimento completa).
        
        Args:
            df_origem: DataFrame de origem
            df_destino: DataFrame de destino
            col_chave: Nome da coluna com a chave
            col_id_origem: Nome da coluna com ID na origem
            col_id_destino: Nome da coluna com ID no destino
        
        Returns:
            Lista de MatchResult
        """
        matches = []
        
        # Filtrar registros com chave forte
        df_origem_com_chave = df_origem[df_origem[col_chave].notna()].copy()
        df_destino_com_chave = df_destino[df_destino[col_chave].notna()].copy()
        
        print(f"[Match Forte] Origem: {len(df_origem_com_chave)} registros com chave")
        print(f"[Match Forte] Destino: {len(df_destino_com_chave)} registros com chave")
        
        # Fazer merge
        merged = pd.merge(
            df_origem_com_chave[[col_id_origem, col_chave]],
            df_destino_com_chave[[col_id_destino, col_chave]],
            on=col_chave,
            how='inner'
        )
        
        print(f"[Match Forte] Encontrados {len(merged)} matches")
        
        # Converter para MatchResult
        for _, row in merged.iterrows():
            match = MatchResult(
                id_origem=row[col_id_origem],
                id_destino=row[col_id_destino],
                tipo_match='forte',
                chave_usada=row[col_chave],
                confianca=0.95
            )
            matches.append(match)
            self.matches_fortes.append(match)
        
        return matches
    
    def fazer_match_moderado(
        self,
        df_origem: pd.DataFrame,
        df_destino: pd.DataFrame,
        col_chave: str = 'chave_moderada',
        col_id_origem: str = 'id_unico',
        col_id_destino: str = 'id_unico',
        excluir_ids_origem: set = None,
        excluir_ids_destino: set = None
    ) -> List[MatchResult]:
        """
        Faz match moderado (nome + ano nascimento).
        Exclui registros que já tiveram match forte.
        """
        matches = []
        
        # Filtrar registros já matchados
        if excluir_ids_origem is None:
            excluir_ids_origem = set()
        if excluir_ids_destino is None:
            excluir_ids_destino = set()
        
        df_origem_filtrado = df_origem[
            (df_origem[col_chave].notna()) &
            (~df_origem[col_id_origem].isin(excluir_ids_origem))
        ].copy()
        
        df_destino_filtrado = df_destino[
            (df_destino[col_chave].notna()) &
            (~df_destino[col_id_destino].isin(excluir_ids_destino))
        ].copy()
        
        print(f"[Match Moderado] Origem: {len(df_origem_filtrado)} registros disponíveis")
        print(f"[Match Moderado] Destino: {len(df_destino_filtrado)} registros disponíveis")
        
        # Fazer merge
        merged = pd.merge(
            df_origem_filtrado[[col_id_origem, col_chave, 'sexo']],
            df_destino_filtrado[[col_id_destino, col_chave, 'sexo']],
            on=col_chave,
            how='inner',
            suffixes=('_origem', '_destino')
        )
        
        # Validar que o sexo é compatível
        merged = merged[
            (merged['sexo_origem'] == merged['sexo_destino']) |
            (merged['sexo_origem'] == 'IGN') |
            (merged['sexo_destino'] == 'IGN')
        ]
        
        print(f"[Match Moderado] Encontrados {len(merged)} matches")
        
        for _, row in merged.iterrows():
            match = MatchResult(
                id_origem=row[col_id_origem],
                id_destino=row[col_id_destino],
                tipo_match='moderado',
                chave_usada=row[col_chave],
                confianca=0.75
            )
            matches.append(match)
            self.matches_moderados.append(match)
        
        return matches
    
    def fazer_match_fraco(
        self,
        df_origem: pd.DataFrame,
        df_destino: pd.DataFrame,
        col_chave: str = 'chave_fraca',
        col_id_origem: str = 'id_unico',
        col_id_destino: str = 'id_unico',
        excluir_ids_origem: Optional[Set] = None,
        excluir_ids_destino: Optional[Set] = None,
        validar_idade: bool = True
    ) -> List[MatchResult]:
        """
        Faz match fraco (apenas nome).
        Exclui registros já matchados e valida idade se possível.
        """
        matches = []
        
        if excluir_ids_origem is None:
            excluir_ids_origem = set()
        if excluir_ids_destino is None:
            excluir_ids_destino = set()
        
        df_origem_filtrado = df_origem[
            (df_origem[col_chave].notna()) &
            (~df_origem[col_id_origem].isin(excluir_ids_origem))
        ].copy()
        
        df_destino_filtrado = df_destino[
            (df_destino[col_chave].notna()) &
            (~df_destino[col_id_destino].isin(excluir_ids_destino))
        ].copy()
        
        print(f"[Match Fraco] Origem: {len(df_origem_filtrado)} registros disponíveis")
        print(f"[Match Fraco] Destino: {len(df_destino_filtrado)} registros disponíveis")
        
        # Preparar colunas para merge
        cols_origem = [col_id_origem, col_chave, 'sexo']
        cols_destino = [col_id_destino, col_chave, 'sexo']
        
        if validar_idade and 'idade_estimativa' in df_origem.columns:
            cols_origem.append('idade_estimativa')
        if validar_idade and 'idade_estimativa' in df_destino.columns:
            cols_destino.append('idade_estimativa')
        
        merged = pd.merge(
            df_origem_filtrado[cols_origem],
            df_destino_filtrado[cols_destino],
            on=col_chave,
            how='inner',
            suffixes=('_origem', '_destino')
        )
        
        # Validar sexo
        merged = merged[
            (merged['sexo_origem'] == merged['sexo_destino']) |
            (merged['sexo_origem'] == 'IGN') |
            (merged['sexo_destino'] == 'IGN')
        ]
        
        # Validar idade (diferença máxima de 3 anos)
        if validar_idade and 'idade_estimativa_origem' in merged.columns:
            merged = merged[
                (merged['idade_estimativa_origem'].isna()) |
                (merged['idade_estimativa_destino'].isna()) |
                (abs(merged['idade_estimativa_origem'] - merged['idade_estimativa_destino']) <= 3)
            ]
        
        print(f"[Match Fraco] Encontrados {len(merged)} matches após validações")
        
        for _, row in merged.iterrows():
            match = MatchResult(
                id_origem=row[col_id_origem],
                id_destino=row[col_id_destino],
                tipo_match='fraco',
                chave_usada=row[col_chave],
                confianca=0.50
            )
            matches.append(match)
            self.matches_fracos.append(match)
        
        return matches
    
    def executar_matching_completo(
        self,
        df_origem: pd.DataFrame,
        df_destino: pd.DataFrame,
        nome_origem: str = "Origem",
        nome_destino: str = "Destino"
    ) -> Dict[str, List[MatchResult]]:
        """
        Executa o processo completo de matching (forte -> moderado -> fraco).
        
        Returns:
            Dict com listas de matches por tipo
        """
        print(f"\n{'='*80}")
        print(f"MATCHING: {nome_origem} <-> {nome_destino}")
        print(f"{'='*80}\n")
        
        # Match forte
        matches_fortes = self.fazer_match_forte(df_origem, df_destino)
        
        # IDs já matchados
        ids_origem_matchados = {m.id_origem for m in matches_fortes}
        ids_destino_matchados = {m.id_destino for m in matches_fortes}
        
        # Match moderado (excluindo já matchados)
        matches_moderados = self.fazer_match_moderado(
            df_origem, df_destino,
            excluir_ids_origem=ids_origem_matchados,
            excluir_ids_destino=ids_destino_matchados
        )
        
        # Atualizar matchados
        ids_origem_matchados.update({m.id_origem for m in matches_moderados})
        ids_destino_matchados.update({m.id_destino for m in matches_moderados})
        
        # Match fraco
        matches_fracos = self.fazer_match_fraco(
            df_origem, df_destino,
            excluir_ids_origem=ids_origem_matchados,
            excluir_ids_destino=ids_destino_matchados
        )
        
        print(f"\n{'='*80}")
        print(f"RESUMO DO MATCHING")
        print(f"{'='*80}")
        print(f"Matches fortes: {len(matches_fortes)}")
        print(f"Matches moderados: {len(matches_moderados)}")
        print(f"Matches fracos: {len(matches_fracos)}")
        print(f"Total: {len(matches_fortes) + len(matches_moderados) + len(matches_fracos)}")
        print(f"{'='*80}\n")
        
        return {
            'fortes': matches_fortes,
            'moderados': matches_moderados,
            'fracos': matches_fracos
        }
    
    def obter_todos_matches(self) -> List[MatchResult]:
        """Retorna todos os matches realizados"""
        return self.matches_fortes + self.matches_moderados + self.matches_fracos
    
    def criar_mapeamento_ids(self) -> Dict[str, List[str]]:
        """
        Cria um mapeamento de ID origem -> lista de IDs destino.
        
        Returns:
            Dict[id_origem, List[id_destino]]
        """
        mapeamento = {}
        
        for match in self.obter_todos_matches():
            if match.id_origem not in mapeamento:
                mapeamento[match.id_origem] = []
            mapeamento[match.id_origem].append(match.id_destino)
        
        return mapeamento
