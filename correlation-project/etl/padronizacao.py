"""Módulo para padronizar campos dos CSVs"""
import pandas as pd
import re
from typing import Dict, Optional
from config.config import FIELD_MAPPING
from utils.normalization import (
    normalizar_nome, normalizar_sexo, parse_data, 
    calcular_idade, extrair_ano, limpar_texto,
    gerar_chave_forte, gerar_chave_moderada, gerar_chave_fraca
)


def limpar_nome_coluna(nome: str) -> str:
    """
    Limpa nome de coluna removendo caracteres especiais e convertendo para snake_case.
    
    Args:
        nome: Nome original da coluna
        
    Returns:
        Nome limpo em snake_case
    """
    # Remove BOM se existir
    nome = nome.replace('\ufeff', '').replace('ï»¿', '')
    
    # Remove acentos e caracteres especiais
    from utils.normalization import remover_acentos
    nome = remover_acentos(nome)
    
    # Remove pontos, parênteses, barra e outros caracteres especiais
    nome = re.sub(r'[.\(\)\[\]\{\}\/\\?!@#$%^&*+=|~`]', '', nome)
    
    # Substitui espaços e hífens por underscore
    nome = re.sub(r'[\s\-]+', '_', nome)
    
    # Remove underscores múltiplos
    nome = re.sub(r'_+', '_', nome)
    
    # Remove underscores no início e fim
    nome = nome.strip('_')
    
    # Converte para minúsculo
    nome = nome.lower()
    
    return nome


def padronizar_colunas(df: pd.DataFrame, mapping: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    """
    Padroniza os nomes das colunas do DataFrame.
    Remove pontos, parênteses e caracteres especiais, converte para snake_case.
    
    Args:
        df: DataFrame original
        mapping: Dicionário de mapeamento (default: usa FIELD_MAPPING)
    
    Returns:
        DataFrame com colunas padronizadas
    """
    if mapping is None:
        mapping = FIELD_MAPPING
    
    # Criar mapeamento para colunas não mapeadas
    novo_mapping = {}
    for col in df.columns:
        if col in mapping:
            novo_mapping[col] = mapping[col]
        else:
            # Limpar automaticamente colunas não mapeadas
            novo_mapping[col] = limpar_nome_coluna(col)
    
    # Renomear colunas
    df_renamed = df.rename(columns=novo_mapping)
    
    return df_renamed


def processar_campos_pessoa(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processa e enriquece os campos relacionados à pessoa.
    
    Args:
        df: DataFrame com campos padronizados
    
    Returns:
        DataFrame com campos processados
    """
    df = df.copy()
    
    # Normalizar nome
    if 'nome' in df.columns:
        df['nome_normalizado'] = df['nome'].apply(normalizar_nome)
    else:
        df['nome_normalizado'] = ''
    
    # Normalizar nome da mãe
    if 'nome_mae' in df.columns:
        df['nome_mae_normalizado'] = df['nome_mae'].apply(normalizar_nome)
    else:
        df['nome_mae_normalizado'] = ''
    
    # Normalizar sexo
    if 'sexo' in df.columns:
        df['sexo'] = df['sexo'].apply(normalizar_sexo)
    else:
        df['sexo'] = 'IGN'
    
    # Processar data de nascimento
    if 'data_nascimento' in df.columns:
        df['data_nascimento_dt'] = df['data_nascimento'].apply(parse_data)
        df['ano_nascimento'] = df['data_nascimento_dt'].apply(extrair_ano)
    else:
        df['data_nascimento_dt'] = None
        df['ano_nascimento'] = None
    
    # Processar data do fato
    if 'data_fato' in df.columns:
        df['data_fato_dt'] = df['data_fato'].apply(parse_data)
    else:
        df['data_fato_dt'] = None
    
    # Calcular idade
    def calc_idade_row(row):
        if pd.notna(row.get('data_nascimento_dt')) and pd.notna(row.get('data_fato_dt')):
            return calcular_idade(row['data_nascimento_dt'], row['data_fato_dt'])
        elif pd.notna(row.get('data_nascimento_dt')):
            return calcular_idade(row['data_nascimento_dt'])
        return None
    
    df['idade_calculada'] = df.apply(calc_idade_row, axis=1)
    
    # Usar idade da ocorrência se não temos calculada
    if 'idade_ocorrencia' in df.columns:
        df['idade_estimativa'] = df.apply(
            lambda row: row['idade_calculada'] if pd.notna(row.get('idade_calculada')) 
                        else row.get('idade_ocorrencia'),
            axis=1
        )
    else:
        df['idade_estimativa'] = df['idade_calculada']
    
    # Limpar histórico
    if 'historico' in df.columns:
        df['historico_limpo'] = df['historico'].apply(limpar_texto)
    else:
        df['historico_limpo'] = ''
    
    return df


def criar_chaves_matching(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria as chaves para matching entre bases.
    
    Args:
        df: DataFrame com campos processados
    
    Returns:
        DataFrame com chaves de matching
    """
    df = df.copy()
    
    # Chave forte: nome + data nascimento completa
    df['chave_forte'] = df.apply(
        lambda row: gerar_chave_forte(
            row.get('nome_normalizado', ''),
            row.get('data_nascimento_dt')
        ),
        axis=1
    )
    
    # Chave moderada: nome + ano nascimento
    df['chave_moderada'] = df.apply(
        lambda row: gerar_chave_moderada(
            row.get('nome_normalizado', ''),
            row.get('ano_nascimento')
        ),
        axis=1
    )
    
    # Chave fraca: apenas nome
    df['chave_fraca'] = df['nome_normalizado'].apply(gerar_chave_fraca)
    
    return df


def criar_id_unico(df: pd.DataFrame, prefixo: str = 'REG') -> pd.DataFrame:
    """
    Cria IDs únicos para cada registro.
    
    Args:
        df: DataFrame
        prefixo: Prefixo para o ID (ex: 'DESAP', 'CAD', 'HOM')
    
    Returns:
        DataFrame com coluna id_unico
    """
    df = df.copy()
    
    # Usar índice + hash do nome para garantir unicidade
    def gerar_id(row):
        base = f"{prefixo}"
        
        # Tentar usar IDs existentes primeiro
        try:
            if pd.notna(row.get('cd_envolvido')):
                return f"{base}_{int(float(row['cd_envolvido']))}"
        except (ValueError, TypeError):
            pass
        
        try:
            if pd.notna(row.get('sequencial')):
                val = row['sequencial']
                if isinstance(val, (int, float)):
                    return f"{base}_{int(val)}"
        except (ValueError, TypeError):
            pass
        
        # Fallback: usar hash do nome + index
        nome_hash = abs(hash(row.get('nome_normalizado', ''))) % 1000000
        return f"{base}_{row.name}_{nome_hash}"
    
    df['id_unico'] = df.apply(gerar_id, axis=1)
    
    return df


def pipeline_padronizacao_completa(
    df: pd.DataFrame, 
    prefixo_id: str = 'REG',
    mapping: Optional[Dict[str, str]] = None
) -> pd.DataFrame:
    """
    Pipeline completo de padronização.
    
    Args:
        df: DataFrame original
        prefixo_id: Prefixo para IDs únicos
        mapping: Mapeamento de colunas (opcional)
    
    Returns:
        DataFrame totalmente processado
    """
    print(f"[Pipeline] Iniciando padronização...")
    print(f"[Pipeline] Registros originais: {len(df)}")
    
    # 1. Padronizar colunas
    print("[Pipeline] Passo 1/4: Padronizando nomes de colunas...")
    df = padronizar_colunas(df, mapping)
    
    # 2. Processar campos de pessoa
    print("[Pipeline] Passo 2/4: Processando campos de pessoa...")
    df = processar_campos_pessoa(df)
    
    # 3. Criar chaves de matching
    print("[Pipeline] Passo 3/4: Criando chaves de matching...")
    df = criar_chaves_matching(df)
    
    # 4. Criar IDs únicos
    print("[Pipeline] Passo 4/4: Gerando IDs únicos...")
    df = criar_id_unico(df, prefixo_id)
    
    print(f"[Pipeline] Padronização concluída!")
    print(f"[Pipeline] Registros com chave forte: {df['chave_forte'].notna().sum()}")
    print(f"[Pipeline] Registros com chave moderada: {df['chave_moderada'].notna().sum()}")
    print(f"[Pipeline] Registros com chave fraca: {df['chave_fraca'].notna().sum()}")
    
    return df
