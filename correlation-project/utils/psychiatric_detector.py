"""Detector de transtornos psiquiátricos em textos narrativos"""
import re
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
from config.config import PSYCHIATRIC_KEYWORDS
from utils.normalization import remover_acentos, limpar_texto


class PsychiatricDetector:
    """Detecta menções a transtornos psiquiátricos em textos"""
    
    def __init__(self, keywords: Optional[List[str]] = None):
        """
        Inicializa o detector.
        
        Args:
            keywords: Lista de palavras-chave (default: usa config.PSYCHIATRIC_KEYWORDS)
        """
        self.keywords = keywords or PSYCHIATRIC_KEYWORDS
        self._prepare_patterns()
    
    def _prepare_patterns(self):
        """Prepara os padrões regex para busca"""
        # Criar padrões com e sem acentos
        self.patterns = []
        for keyword in self.keywords:
            # Versão original
            pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
            self.patterns.append((keyword, pattern))
            
            # Versão sem acentos
            keyword_sem_acento = remover_acentos(keyword)
            if keyword_sem_acento != keyword:
                pattern_sem_acento = re.compile(
                    r'\b' + re.escape(keyword_sem_acento) + r'\b', 
                    re.IGNORECASE
                )
                self.patterns.append((keyword, pattern_sem_acento))
    
    def detectar(self, texto: str) -> Dict[str, Any]:
        """
        Detecta transtornos psiquiátricos em um texto.
        
        Args:
            texto: Texto a analisar
        
        Returns:
            Dict com:
                - tem_transtorno_psiquiatrico: bool
                - tipo_transtorno: str (lista dos tipos encontrados)
                - evidencia_transtorno: str (trechos relevantes)
                - confianca: str ('alta', 'media', 'baixa')
        """
        if not isinstance(texto, str) or pd.isna(texto):
            return {
                'tem_transtorno_psiquiatrico': False,
                'tipo_transtorno': '',
                'evidencia_transtorno': '',
                'confianca': 'inconclusivo'
            }
        
        # Limpar o texto de caracteres inválidos (limpar_texto já chama limpar_texto_sujo)
        texto_limpo = limpar_texto(texto)
        texto_normalizado = remover_acentos(texto_limpo.lower())
        
        # Buscar matches
        matches = []
        evidencias = set()
        
        for keyword, pattern in self.patterns:
            for match in pattern.finditer(texto_limpo):
                matches.append(keyword)
                # Extrair contexto ao redor (50 caracteres antes e depois)
                start = max(0, match.start() - 50)
                end = min(len(texto_limpo), match.end() + 50)
                evidencia = texto_limpo[start:end].strip()
                evidencias.add(evidencia)
        
        # Se não encontrou nada
        if not matches:
            return {
                'tem_transtorno_psiquiatrico': False,
                'tipo_transtorno': '',
                'evidencia_transtorno': '',
                'confianca': 'inconclusivo'
            }
        
        # Classificar confiança
        confianca = self._calcular_confianca(matches, texto_normalizado)
        
        # Extrair tipos de transtorno
        tipos = self._extrair_tipos(matches)
        
        return {
            'tem_transtorno_psiquiatrico': True,
            'tipo_transtorno': '; '.join(tipos),
            'evidencia_transtorno': ' | '.join(list(evidencias)[:3]),  # Máximo 3 evidências
            'confianca': confianca
        }
    
    def _calcular_confianca(self, matches: List[str], texto_normalizado: str) -> str:
        """
        Calcula o nível de confiança baseado nos matches.
        
        Args:
            matches: Lista de keywords encontradas
            texto_normalizado: Texto normalizado
        
        Returns:
            'alta', 'media' ou 'baixa'
        """
        # Confiança alta: múltiplas menções ou termos específicos
        termos_alta_confianca = [
            'esquizofrenia', 'bipolar', 'psicose', 'internacao psiquiatrica',
            'hospital psiquiatrico', 'transtorno mental', 'tratamento psiquiatrico'
        ]
        
        matches_unicos = set(remover_acentos(m.lower()) for m in matches)
        
        # Alta: menção a diagnóstico específico
        for termo in termos_alta_confianca:
            if termo in texto_normalizado:
                return 'alta'
        
        # Alta: múltiplas menções (3+)
        if len(matches_unicos) >= 3:
            return 'alta'
        
        # Média: 2 menções ou menção a medicamento específico
        medicamentos = ['rivotril', 'haldol', 'olanzapina', 'risperidona', 
                       'quetiapina', 'clozapina', 'fluoxetina', 'sertralina']
        
        tem_medicamento = any(med in texto_normalizado for med in medicamentos)
        
        if len(matches_unicos) >= 2 or tem_medicamento:
            return 'media'
        
        # Baixa: apenas 1 menção genérica
        return 'baixa'
    
    def _extrair_tipos(self, matches: List[str]) -> List[str]:
        """
        Extrai os tipos de transtornos encontrados.
        
        Args:
            matches: Lista de keywords encontradas
        
        Returns:
            Lista de tipos de transtorno (únicos e categorizados)
        """
        tipos = set()
        
        # Mapear keywords para categorias
        categorias = {
            'esquizofrenia': ['esquizofrenia'],
            'transtorno bipolar': ['bipolar', 'transtorno bipolar'],
            'depressão': ['depressao', 'depressivo'],
            'ansiedade': ['ansiedade', 'transtorno de ansiedade', 'ansiolitico'],
            'psicose': ['psicose', 'psicotico', 'surto psicotico', 'crise psicotica'],
            'comportamento suicida': ['tentativa de suicidio', 'ideacao suicida'],
            'transtorno mental geral': ['transtorno mental', 'doenca mental', 
                                       'problema psiquiatrico', 'disturbio mental'],
        }
        
        matches_norm = [remover_acentos(m.lower()) for m in matches]
        
        for categoria, keywords in categorias.items():
            for keyword in keywords:
                if any(keyword in match for match in matches_norm):
                    tipos.add(categoria)
                    break
        
        # Se não categorizou nada específico, usar "transtorno mental"
        if not tipos:
            tipos.add('transtorno mental')
        
        return sorted(list(tipos))
    
    def processar_dataframe(self, df: pd.DataFrame, coluna_texto: str = 'historico') -> pd.DataFrame:
        """
        Processa um DataFrame inteiro, detectando transtornos.
        
        Args:
            df: DataFrame com os dados
            coluna_texto: Nome da coluna com o texto narrativo
        
        Returns:
            DataFrame com novas colunas adicionadas
        """
        resultados = df[coluna_texto].apply(self.detectar)
        
        df['tem_transtorno_psiquiatrico'] = resultados.apply(lambda x: x['tem_transtorno_psiquiatrico'])
        df['tipo_transtorno'] = resultados.apply(lambda x: x['tipo_transtorno'])
        df['evidencia_transtorno'] = resultados.apply(lambda x: x['evidencia_transtorno'])
        df['confianca_transtorno'] = resultados.apply(lambda x: x['confianca'])
        
        return df


# Função standalone para uso direto
def detectar_transtorno(texto: str) -> Dict[str, Any]:
    """
    Função standalone para detectar transtornos psiquiátricos.
    
    Args:
        texto: Texto a analisar
    
    Returns:
        Dict com resultados da detecção
    """
    detector = PsychiatricDetector()
    return detector.detectar(texto)
