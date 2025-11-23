"""Pipeline principal de ETL"""
import pandas as pd
import sys
from pathlib import Path

# Adicionar diretórios ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import (
    NATUREZA_DESAPARECIMENTO, NATUREZA_LOCALIZACAO_CADAVER, NATUREZA_HOMICIDIO,
    CLASSIFICACAO_DESAPARECIDO_SIMPLES, CLASSIFICACAO_DESAPARECIDO_MORTO,
    CLASSIFICACAO_DESAPARECIDO_VITIMA_HOMICIDIO, OUTPUT_DIR
)
from etl.padronizacao import pipeline_padronizacao_completa
from etl.matching_engine import MatchingEngine, MatchResult
from utils.psychiatric_detector import PsychiatricDetector
from utils.chaves import enriquecer_com_chaves, filtrar_grupo_alvo


def carregar_csv(caminho: str, sep: str = ';', encoding: str = 'latin-1') -> pd.DataFrame:
    """Carrega um CSV com tratamento de erros"""
    print(f"[Carregamento] Lendo arquivo: {caminho}")
    
    try:
        df = pd.read_csv(caminho, sep=sep, encoding=encoding, on_bad_lines='skip')
        print(f"[Carregamento] {len(df)} registros carregados")
        return df
    except Exception as e:
        print(f"[ERRO] Falha ao carregar arquivo: {e}")
        return None


def separar_por_natureza(df: pd.DataFrame) -> dict:
    """
    Separa o DataFrame por tipo de natureza.
    
    Returns:
        Dict com chaves: 'desaparecidos', 'cadaveres', 'homicidios'
    """
    print("\n[Separação] Separando registros por natureza...")
    
    resultado = {
        'desaparecidos': pd.DataFrame(),
        'cadaveres': pd.DataFrame(),
        'homicidios': pd.DataFrame(),
        'outros': pd.DataFrame()
    }
    
    if 'natureza_padronizada' not in df.columns and 'natureza' not in df.columns:
        print("[AVISO] Coluna de natureza não encontrada")
        return resultado
    
    col_natureza = 'natureza_padronizada' if 'natureza_padronizada' in df.columns else 'natureza'
    
    # Desaparecidos
    mask_desap = df[col_natureza].isin(NATUREZA_DESAPARECIMENTO)
    resultado['desaparecidos'] = df[mask_desap].copy()
    print(f"  - Desaparecidos: {len(resultado['desaparecidos'])} registros")
    
    # Cadáveres
    mask_cadaver = df[col_natureza].isin(NATUREZA_LOCALIZACAO_CADAVER)
    resultado['cadaveres'] = df[mask_cadaver].copy()
    print(f"  - Cadáveres: {len(resultado['cadaveres'])} registros")
    
    # Homicídios
    mask_homicidio = df[col_natureza].isin(NATUREZA_HOMICIDIO)
    resultado['homicidios'] = df[mask_homicidio].copy()
    print(f"  - Homicídios: {len(resultado['homicidios'])} registros")
    
    # Outros
    mask_outros = ~(mask_desap | mask_cadaver | mask_homicidio)
    resultado['outros'] = df[mask_outros].copy()
    print(f"  - Outros: {len(resultado['outros'])} registros")
    
    return resultado


def aplicar_detector_psiquiatrico(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica o detector de transtornos psiquiátricos"""
    print("\n[Transtornos] Detectando menções a transtornos psiquiátricos...")
    
    detector = PsychiatricDetector()
    
    if 'historico_limpo' in df.columns:
        df = detector.processar_dataframe(df, coluna_texto='historico_limpo')
    elif 'historico' in df.columns:
        df = detector.processar_dataframe(df, coluna_texto='historico')
    else:
        print("[AVISO] Coluna de histórico não encontrada")
        df['tem_transtorno_psiquiatrico'] = False
        df['tipo_transtorno'] = ''
        df['evidencia_transtorno'] = ''
        df['confianca_transtorno'] = 'inconclusivo'
    
    qtd_detectados = df['tem_transtorno_psiquiatrico'].sum()
    print(f"[Transtornos] Detectados em {qtd_detectados} registros")
    
    return df


def unificar_registros(
    df_desaparecidos: pd.DataFrame,
    df_cadaveres: pd.DataFrame,
    df_homicidios: pd.DataFrame,
    matches_desap_cad: list,
    matches_desap_hom: list
) -> pd.DataFrame:
    """
    Unifica os registros criando a base final.
    
    Returns:
        DataFrame unificado
    """
    print("\n[Unificação] Criando base unificada...")
    
    registros_unificados = []
    ids_processados = set()
    
    # Criar dicionários de lookup
    dict_cadaveres = df_cadaveres.set_index('id_unico').to_dict('index')
    dict_homicidios = df_homicidios.set_index('id_unico').to_dict('index')
    
    # Mapear desaparecidos para cadáveres/homicídios
    mapa_desap_cad = {m.id_origem: m for m in matches_desap_cad}
    mapa_desap_hom = {m.id_origem: m for m in matches_desap_hom}
    
    # Processar desaparecidos
    for _, desap in df_desaparecidos.iterrows():
        id_desap = desap['id_unico']
        
        registro = {
            # Dados básicos
            'id_unico': id_desap,
            'nome': desap.get('nome', ''),
            'nome_normalizado': desap.get('nome_normalizado', ''),
            'data_nascimento': desap.get('data_nascimento_dt'),
            'sexo': desap.get('sexo', 'IGN'),
            'idade_estimativa': desap.get('idade_estimativa'),
            'nome_mae': desap.get('nome_mae', ''),
            'local_de_referencia': desap.get('cidade_ra', ''),
            
            # Chaves de correlação (NOVO)
            'chave_ocorrencia': desap.get('chave_ocorrencia', ''),
            'chave_pessoa': desap.get('chave_pessoa', ''),
            'natureza_alvo': desap.get('natureza_alvo', ''),
            'papel_pessoa': desap.get('papel_pessoa', ''),
            
            # Desaparecimento
            'data_desaparecimento': desap.get('data_fato_dt'),
            'boletim_desaparecimento': desap.get('cd_ocorrencia', ''),
            'historico_desaparecimento': desap.get('historico_limpo', ''),
            'unidade_registro_desap': desap.get('unidade_registro', ''),
            'pessoa_localizada': desap.get('pessoa_localizada', ''),
            
            # Chaves
            'chave_forte': desap.get('chave_forte', ''),
            'chave_moderada': desap.get('chave_moderada', ''),
            'chave_fraca': desap.get('chave_fraca', ''),
            
            # Transtorno
            'tem_transtorno_psiquiatrico': desap.get('tem_transtorno_psiquiatrico', False),
            'tipo_transtorno': desap.get('tipo_transtorno', ''),
            'evidencia_transtorno': desap.get('evidencia_transtorno', ''),
            'confianca_transtorno': desap.get('confianca_transtorno', 'inconclusivo'),
        }
        
        # Verificar match com cadáver
        if id_desap in mapa_desap_cad:
            match_cad = mapa_desap_cad[id_desap]
            id_cad = match_cad.id_destino
            
            if id_cad in dict_cadaveres:
                cadaver = dict_cadaveres[id_cad]
                registro.update({
                    'data_localizacao_cadaver': cadaver.get('data_fato_dt'),
                    'boletim_localizacao': cadaver.get('cd_ocorrencia', ''),
                    'local_cadaver': cadaver.get('cidade_ra', ''),
                    'cod_iml_pessoa': cadaver.get('cod_iml_pessoa', ''),
                    'possui_laudo_iml': cadaver.get('possui_laudo_iml', ''),
                    'match_forte_cad': match_cad.tipo_match == 'forte',
                    'match_moderado_cad': match_cad.tipo_match == 'moderado',
                    'match_fraco_cad': match_cad.tipo_match == 'fraco',
                    'fonte_match': 'desaparecido->cadaver',
                    'classificacao_final': CLASSIFICACAO_DESAPARECIDO_MORTO
                })
                ids_processados.add(id_cad)
        
        # Verificar match com homicídio
        if id_desap in mapa_desap_hom:
            match_hom = mapa_desap_hom[id_desap]
            id_hom = match_hom.id_destino
            
            if id_hom in dict_homicidios:
                homicidio = dict_homicidios[id_hom]
                registro.update({
                    'data_homicidio': homicidio.get('data_fato_dt'),
                    'boletim_homicidio': homicidio.get('cd_ocorrencia', ''),
                    'local_homicidio': homicidio.get('cidade_ra', ''),
                    'circunstancias_homicidio': homicidio.get('historico_limpo', ''),
                    'match_forte_hom': match_hom.tipo_match == 'forte',
                    'match_moderado_hom': match_hom.tipo_match == 'moderado',
                    'match_fraco_hom': match_hom.tipo_match == 'fraco',
                    'fonte_match': 'desaparecido->homicidio',
                    'classificacao_final': CLASSIFICACAO_DESAPARECIDO_VITIMA_HOMICIDIO
                })
                ids_processados.add(id_hom)
        
        # Classificação se não teve match
        if 'classificacao_final' not in registro:
            if registro.get('pessoa_localizada') and 'SIM' in str(registro['pessoa_localizada']).upper():
                registro['classificacao_final'] = "Desaparecido localizado vivo"
            else:
                registro['classificacao_final'] = CLASSIFICACAO_DESAPARECIDO_SIMPLES
        
        registros_unificados.append(registro)
    
    # TODO: Adicionar cadáveres e homicídios sem match
    # (registros órfãos que não foram correlacionados)
    
    df_unificado = pd.DataFrame(registros_unificados)
    print(f"[Unificação] {len(df_unificado)} registros unificados")
    
    return df_unificado


def pipeline_completo(caminho_csv: str, output_path: str = None) -> pd.DataFrame:
    """
    Executa o pipeline completo de ETL.
    
    Args:
        caminho_csv: Caminho para o CSV de entrada
        output_path: Caminho para salvar o resultado (opcional)
    
    Returns:
        DataFrame unificado final
    """
    print("\n" + "="*80)
    print("INICIANDO PIPELINE COMPLETO DE CORRELAÇÃO")
    print("="*80 + "\n")
    
    # 1. Carregar dados
    df_raw = carregar_csv(caminho_csv)
    if df_raw is None:
        return None
    
    # 2. Padronizar
    df_padronizado = pipeline_padronizacao_completa(df_raw, prefixo_id='REG')
    
    # 3. Enriquecer com chaves de correlação
    print("\n[Enriquecimento] Gerando chaves de correlação...")
    df_padronizado = enriquecer_com_chaves(df_padronizado)
    
    # 4. Aplicar detector psiquiátrico em TODOS os registros
    print("\n[Transtornos] Detectando transtornos psiquiátricos em todos os registros...")
    df_padronizado = aplicar_detector_psiquiatrico(df_padronizado)
    
    # 5. Separar por natureza (para estatísticas)
    bases = separar_por_natureza(df_padronizado)
    
    # 6. Usar TODO o dataset enriquecido como resultado final
    df_final = df_padronizado.copy()
    
    print(f"\n[Dataset Final] Total de registros processados: {len(df_final):,}")
    print(f"  - Desaparecimentos: {len(bases['desaparecidos']):,}")
    print(f"  - Cadáveres: {len(bases['cadaveres']):,}")
    print(f"  - Homicídios: {len(bases['homicidios']):,}")
    print(f"  - Outros: {len(bases['outros']):,}")
    
    # 7. Salvar resultado
    if output_path:
        print(f"\n[Salvamento] Salvando resultado em: {output_path}")
        
        # Determinar formato pelo caminho
        if output_path.endswith('.xlsx'):
            from utils.excel_export import criar_relatorio_completo
            criar_relatorio_completo(df_final, output_path, incluir_estatisticas=True)
        else:
            df_final.to_csv(output_path, index=False, sep=';', encoding='utf-8-sig')
        
        print("[Salvamento] Concluído!")
    
    print("\n" + "="*80)
    print("PIPELINE CONCLUÍDO COM SUCESSO")
    print("="*80 + "\n")
    
    return df_final


if __name__ == "__main__":
    # Executar pipeline
    caminho_entrada = r"d:\___MeusScripts\LangChain\Dados-homi-desaperecido.csv"
    caminho_saida = OUTPUT_DIR / "dataset_unificado.xlsx"  # Mudado para XLSX
    
    df_resultado = pipeline_completo(caminho_entrada, str(caminho_saida))
    
    if df_resultado is not None:
        print("\n[ESTATÍSTICAS FINAIS]")
        print(f"Total de registros: {len(df_resultado)}")
        
        if 'natureza_alvo' in df_resultado.columns:
            print(f"\nDistribuição por natureza da ocorrência:")
            print(df_resultado['natureza_alvo'].value_counts())
        
        if 'contexto_pessoa' in df_resultado.columns:
            print(f"\nDistribuição por contexto da pessoa:")
            print(df_resultado['contexto_pessoa'].value_counts())
        
        print(f"\nRegistros com transtorno detectado: {df_resultado['tem_transtorno_psiquiatrico'].sum()}")
