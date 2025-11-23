"""
Pipeline ETL completo para processamento de dados criminais.
"""

from typing import Dict, List, Optional, Any
import pandas as pd
from pathlib import Path
from datetime import datetime

from config import get_settings
from etl.padronizacao import padronizar_dataset
from etl.matching import match_datasets
from models.matching import MatchResult


class ETLPipeline:
    """Pipeline completo de ETL para dados criminais."""
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Inicializa pipeline.
        
        Args:
            output_dir: Diretório para outputs (usa configuração se None)
        """
        self.settings = get_settings()
        self.output_dir = output_dir or self.settings.output_dir
        self.output_dir.mkdir(exist_ok=True)
        
        self.datasets: Dict[str, pd.DataFrame] = {}
        self.padronizados: Dict[str, pd.DataFrame] = {}
        self.matches: List[MatchResult] = []
        
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
    
    def load_dataset(
        self, 
        filepath: Path, 
        dataset_name: str,
        dataset_type: str,
    ) -> pd.DataFrame:
        """
        Carrega dataset de arquivo.
        
        Args:
            filepath: Caminho do arquivo
            dataset_name: Nome identificador do dataset
            dataset_type: Tipo (desaparecimento, homicidio, cadaver)
            
        Returns:
            DataFrame carregado
        """
        # Detecta formato e carrega
        if filepath.suffix == '.csv':
            df = pd.read_csv(filepath)
        elif filepath.suffix in ['.xlsx', '.xls']:
            df = pd.read_excel(filepath)
        else:
            raise ValueError(f"Formato não suportado: {filepath.suffix}")
        
        self.datasets[dataset_name] = df
        return df
    
    def padronizar(self, dataset_name: str, dataset_type: str) -> pd.DataFrame:
        """
        Padroniza um dataset carregado.
        
        Args:
            dataset_name: Nome do dataset
            dataset_type: Tipo do dataset
            
        Returns:
            DataFrame padronizado
        """
        if dataset_name not in self.datasets:
            raise ValueError(f"Dataset não encontrado: {dataset_name}")
        
        df = self.datasets[dataset_name]
        df_padronizado = padronizar_dataset(df, dataset_type)
        
        self.padronizados[dataset_name] = df_padronizado
        return df_padronizado
    
    def realizar_matching(
        self,
        source_name: str,
        target_name: str,
        similarity_threshold: Optional[float] = None,
    ) -> List[MatchResult]:
        """
        Realiza matching entre dois datasets.
        
        Args:
            source_name: Nome do dataset fonte
            target_name: Nome do dataset alvo
            similarity_threshold: Threshold de similaridade (usa config se None)
            
        Returns:
            Lista de matches encontrados
        """
        if source_name not in self.padronizados:
            raise ValueError(f"Dataset não padronizado: {source_name}")
        if target_name not in self.padronizados:
            raise ValueError(f"Dataset não padronizado: {target_name}")
        
        threshold = similarity_threshold or self.settings.similarity_threshold
        
        matches = match_datasets(
            self.padronizados[source_name],
            self.padronizados[target_name],
            source_name,
            target_name,
            threshold,
        )
        
        self.matches.extend(matches)
        return matches
    
    def export_matches(self, filename: str = "matches.csv") -> Path:
        """
        Exporta matches para arquivo.
        
        Args:
            filename: Nome do arquivo de saída
            
        Returns:
            Path do arquivo criado
        """
        if not self.matches:
            raise ValueError("Nenhum match para exportar")
        
        # Converte matches para DataFrame
        matches_data = [match.to_dict() for match in self.matches]
        df_matches = pd.DataFrame(matches_data)
        
        # Salva arquivo
        output_path = self.output_dir / filename
        df_matches.to_csv(output_path, index=False)
        
        return output_path
    
    def export_padronizado(self, dataset_name: str, filename: str) -> Path:
        """
        Exporta dataset padronizado.
        
        Args:
            dataset_name: Nome do dataset
            filename: Nome do arquivo de saída
            
        Returns:
            Path do arquivo criado
        """
        if dataset_name not in self.padronizados:
            raise ValueError(f"Dataset não padronizado: {dataset_name}")
        
        output_path = self.output_dir / filename
        self.padronizados[dataset_name].to_csv(output_path, index=False)
        
        return output_path
    
    def run(
        self,
        datasets: Dict[str, Dict[str, Any]],
        matching_pairs: List[tuple[str, str]],
    ) -> Dict[str, Any]:
        """
        Executa pipeline completo.
        
        Args:
            datasets: Dicionário com configs dos datasets
                     {name: {filepath: Path, type: str}}
            matching_pairs: Lista de pares para matching
                           [(source_name, target_name), ...]
            
        Returns:
            Dicionário com resultados do pipeline
        """
        self.start_time = datetime.now()
        
        results = {
            "loaded": [],
            "padronizados": [],
            "matches": [],
            "errors": [],
        }
        
        # Carrega e padroniza datasets
        for name, config in datasets.items():
            try:
                self.load_dataset(config["filepath"], name, config["type"])
                self.padronizar(name, config["type"])
                results["padronizados"].append(name)
            except Exception as e:
                results["errors"].append({
                    "dataset": name,
                    "error": str(e),
                })
        
        # Realiza matching
        for source, target in matching_pairs:
            try:
                matches = self.realizar_matching(source, target)
                results["matches"].append({
                    "source": source,
                    "target": target,
                    "count": len(matches),
                })
            except Exception as e:
                results["errors"].append({
                    "matching": f"{source} x {target}",
                    "error": str(e),
                })
        
        self.end_time = datetime.now()
        results["duration"] = (self.end_time - self.start_time).total_seconds()
        
        return results


def run_pipeline(
    datasets: Dict[str, Dict[str, Any]],
    matching_pairs: List[tuple[str, str]],
    output_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Função helper para executar pipeline.
    
    Args:
        datasets: Configurações dos datasets
        matching_pairs: Pares para matching
        output_dir: Diretório de saída
        
    Returns:
        Resultados do pipeline
    """
    pipeline = ETLPipeline(output_dir)
    return pipeline.run(datasets, matching_pairs)
