"""
AGENTE-CORRELACAO

Agente MCP especializado em ETL, entity matching e análise de correlação 
entre datasets de desaparecidos, localização de cadáveres e homicídios.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, Any, Optional
import pandas as pd

from etl.pipeline import (
    carregar_csv, 
    separar_por_natureza, 
    aplicar_detector_psiquiatrico,
    unificar_registros,
    pipeline_completo
)
from etl.padronizacao import pipeline_padronizacao_completa
from etl.matching_engine import MatchingEngine
from config.config import OUTPUT_DIR


class AgenteCorrelacao:
    """
    Agente inteligente para correlacionar dados de desaparecimentos e mortes.
    
    Missão:
    1. Normalizar datasets
    2. Gerar chaves de matching
    3. Realizar matching cross-dataset
    4. Extrair indicadores psiquiátricos
    5. Criar dataset unificado
    """
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.df_raw = None
        self.df_padronizado = None
        self.bases_separadas = None
        self.matching_engine = MatchingEngine()
        self.df_final = None
    
    def log(self, mensagem: str):
        """Log condicional"""
        if self.verbose:
            print(mensagem)
    
    def executar_pipeline_completo(
        self, 
        caminho_csv: str, 
        output_path: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Executa todo o pipeline de ponta a ponta.
        
        Args:
            caminho_csv: Caminho do CSV de entrada
            output_path: Caminho para salvar resultado (opcional)
        
        Returns:
            DataFrame unificado
        """
        self.log("\n" + "="*80)
        self.log("AGENTE-CORRELACAO - Iniciando")
        self.log("="*80 + "\n")
        
        return pipeline_completo(caminho_csv, output_path)
    
    def executar_etapa_por_etapa(self, caminho_csv: str):
        """
        Executa o pipeline passo a passo (para debugging e controle fino).
        
        Args:
            caminho_csv: Caminho do CSV de entrada
        """
        self.log("\n[ETAPA 1/6] Carregando dados...")
        self.df_raw = carregar_csv(caminho_csv)
        
        if self.df_raw is None:
            self.log("[ERRO] Falha ao carregar dados. Abortando.")
            return
        
        self.log(f"✓ {len(self.df_raw)} registros carregados\n")
        
        self.log("[ETAPA 2/6] Padronizando campos...")
        self.df_padronizado = pipeline_padronizacao_completa(self.df_raw, prefixo_id='REG')
        self.log("✓ Padronização concluída\n")
        
        self.log("[ETAPA 3/6] Separando por natureza...")
        self.bases_separadas = separar_por_natureza(self.df_padronizado)
        self.log("✓ Separação concluída\n")
        
        self.log("[ETAPA 4/6] Detectando transtornos psiquiátricos...")
        if len(self.bases_separadas['desaparecidos']) > 0:
            self.bases_separadas['desaparecidos'] = aplicar_detector_psiquiatrico(
                self.bases_separadas['desaparecidos']
            )
        self.log("✓ Detecção concluída\n")
        
        self.log("[ETAPA 5/6] Fazendo matching entre bases...")
        self._executar_matching()
        self.log("✓ Matching concluído\n")
        
        self.log("[ETAPA 6/6] Unificando registros...")
        self._executar_unificacao()
        self.log("✓ Unificação concluída\n")
        
        self.log("="*80)
        self.log("AGENTE-CORRELACAO - Concluído com Sucesso")
        self.log("="*80 + "\n")
    
    def _executar_matching(self):
        """Executa o matching entre as bases"""
        df_desap = self.bases_separadas['desaparecidos']
        df_cad = self.bases_separadas['cadaveres']
        df_hom = self.bases_separadas['homicidios']
        
        self.matches_desap_cad = []
        self.matches_desap_hom = []
        
        if len(df_desap) > 0 and len(df_cad) > 0:
            resultado = self.matching_engine.executar_matching_completo(
                df_desap, df_cad,
                nome_origem="Desaparecidos",
                nome_destino="Cadáveres"
            )
            self.matches_desap_cad = (
                resultado['fortes'] + 
                resultado['moderados'] + 
                resultado['fracos']
            )
        
        if len(df_desap) > 0 and len(df_hom) > 0:
            resultado = self.matching_engine.executar_matching_completo(
                df_desap, df_hom,
                nome_origem="Desaparecidos",
                nome_destino="Homicídios"
            )
            self.matches_desap_hom = (
                resultado['fortes'] + 
                resultado['moderados'] + 
                resultado['fracos']
            )
    
    def _executar_unificacao(self):
        """Executa a unificação dos registros"""
        self.df_final = unificar_registros(
            self.bases_separadas['desaparecidos'],
            self.bases_separadas['cadaveres'],
            self.bases_separadas['homicidios'],
            self.matches_desap_cad,
            self.matches_desap_hom
        )
    
    def salvar_resultado(self, output_path: str):
        """Salva o resultado final"""
        if self.df_final is None:
            self.log("[ERRO] Nenhum resultado para salvar. Execute o pipeline primeiro.")
            return
        
        self.log(f"\n[Salvamento] Salvando em: {output_path}")
        self.df_final.to_csv(output_path, index=False, sep=';', encoding='utf-8-sig')
        self.log("[Salvamento] ✓ Concluído!\n")
    
    def gerar_relatorio(self) -> Dict[str, Any]:
        """
        Gera um relatório estatístico do processamento.
        
        Returns:
            Dict com estatísticas
        """
        if self.df_final is None:
            return {"erro": "Nenhum dado processado"}
        
        relatorio = {
            "total_registros": len(self.df_final),
            "classificacoes": self.df_final['classificacao_final'].value_counts().to_dict(),
            "transtornos_detectados": int(self.df_final['tem_transtorno_psiquiatrico'].sum()),
            "matches_fortes": int(
                self.df_final.get('match_forte_cad', pd.Series([False])).sum() +
                self.df_final.get('match_forte_hom', pd.Series([False])).sum()
            ),
            "matches_moderados": int(
                self.df_final.get('match_moderado_cad', pd.Series([False])).sum() +
                self.df_final.get('match_moderado_hom', pd.Series([False])).sum()
            ),
            "matches_fracos": int(
                self.df_final.get('match_fraco_cad', pd.Series([False])).sum() +
                self.df_final.get('match_fraco_hom', pd.Series([False])).sum()
            ),
        }
        
        return relatorio
    
    def exibir_relatorio(self):
        """Exibe o relatório no console"""
        relatorio = self.gerar_relatorio()
        
        if "erro" in relatorio:
            self.log(f"[ERRO] {relatorio['erro']}")
            return
        
        self.log("\n" + "="*80)
        self.log("RELATÓRIO ESTATÍSTICO")
        self.log("="*80)
        self.log(f"\nTotal de registros processados: {relatorio['total_registros']}")
        
        self.log("\n📊 Distribuição por Classificação:")
        for classificacao, count in relatorio['classificacoes'].items():
            self.log(f"  • {classificacao}: {count}")
        
        self.log(f"\n🧠 Transtornos Psiquiátricos:")
        self.log(f"  • Detectados: {relatorio['transtornos_detectados']}")
        
        self.log(f"\n🔗 Matching:")
        self.log(f"  • Matches Fortes: {relatorio['matches_fortes']}")
        self.log(f"  • Matches Moderados: {relatorio['matches_moderados']}")
        self.log(f"  • Matches Fracos: {relatorio['matches_fracos']}")
        self.log("="*80 + "\n")


def main():
    """Função principal para execução direta"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AGENTE-CORRELACAO - ETL e Matching de Desaparecidos"
    )
    parser.add_argument(
        'input', 
        type=str, 
        help='Caminho do CSV de entrada'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Caminho do CSV de saída (padrão: output/dataset_unificado.csv)'
    )
    parser.add_argument(
        '--etapa-por-etapa',
        action='store_true',
        help='Executar passo a passo (útil para debug)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Modo silencioso (menos logs)'
    )
    
    args = parser.parse_args()
    
    # Determinar output
    if args.output is None:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        args.output = str(OUTPUT_DIR / "dataset_unificado.csv")
    
    # Criar agente
    agente = AgenteCorrelacao(verbose=not args.quiet)
    
    # Executar
    if args.etapa_por_etapa:
        agente.executar_etapa_por_etapa(args.input)
        agente.salvar_resultado(args.output)
    else:
        agente.executar_pipeline_completo(args.input, args.output)
    
    # Exibir relatório
    if hasattr(agente, 'df_final') and agente.df_final is not None:
        agente.exibir_relatorio()


if __name__ == "__main__":
    main()
