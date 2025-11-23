"""
Módulo para geração de chaves de correlação e filtros de grupo-alvo.

Este módulo fornece funções para:
- Gerar chaves únicas de ocorrência (ano + unidade + número)
- Gerar chaves únicas de pessoa (nome normalizado + data nascimento)
- Identificar naturezas-alvo (desaparecimento, homicídio, cadáver)
- Identificar papéis de pessoa (vítima, autor, testemunha, etc.)
- Filtrar dataset para grupo-alvo de análise
"""

import pandas as pd
import re
from typing import Optional


def gerar_chave_ocorrencia(row: pd.Series) -> Optional[str]:
    """
    Gera chave única de ocorrência no formato: ano_unidade_numero
    
    Exemplo: "2023_16DP_12345"
    
    Args:
        row: Linha do DataFrame com campos ano_registro, unidade_registro, numero_ocorrencia
        
    Returns:
        String com chave única ou None se dados insuficientes
    """
    try:
        ano = str(row.get('ano_registro', '')).strip()
        unidade = str(row.get('unidade_registro', '')).strip()
        numero = str(row.get('numero_ocorrencia', '')).strip()
        
        if not ano or not unidade or not numero:
            return None
            
        # Remove caracteres especiais da unidade
        unidade = re.sub(r'[^A-Za-z0-9]', '', unidade)
        
        return f"{ano}_{unidade}_{numero}"
    except:
        return None


def gerar_chave_pessoa(row: pd.Series) -> Optional[str]:
    """
    Gera chave única de pessoa no formato: nome_normalizado|data_nascimento
    
    Exemplo: "joao_silva|1985-03-15"
    
    Args:
        row: Linha do DataFrame com campos nome ou nome_normalizado, data_nascimento
        
    Returns:
        String com chave única ou None se dados insuficientes
    """
    try:
        # Tenta usar nome_normalizado primeiro, depois nome
        nome = ''
        if 'nome_normalizado' in row.index:
            nome = str(row.get('nome_normalizado', '')).strip().lower()
        if not nome or nome == 'nan':
            nome = str(row.get('nome', '')).strip().lower()
        
        # Tenta diferentes nomes de coluna para data nascimento
        data_nasc = ''
        for col in ['data_nascimento', 'data_nascimento_dt', 'dt_nascimento']:
            if col in row.index:
                data_nasc = str(row.get(col, '')).strip()
                if data_nasc and data_nasc != 'nan':
                    break
        
        if not nome or not data_nasc or nome == 'nan' or data_nasc == 'nan':
            return None
        
        # Normaliza nome: remove acentos, caracteres especiais, espaços múltiplos
        nome = re.sub(r'[^a-z0-9\s]', '', nome)
        nome = re.sub(r'\s+', '_', nome)
        
        return f"{nome}|{data_nasc}"
    except:
        return None


def identificar_natureza_alvo(natureza: str) -> Optional[str]:
    """
    Identifica se a natureza pertence ao grupo-alvo de análise.
    
    Grupo-alvo:
    - DESAPARECIMENTO DE PESSOA
    - HOMICIDIO
    - LOCALIZACAO OU REMOCAO CADAVER
    
    Args:
        natureza: String com descrição da natureza
        
    Returns:
        String padronizada da natureza-alvo ou None
    """
    if pd.isna(natureza):
        return None
        
    natureza_upper = str(natureza).upper().strip()
    
    if 'DESAPARECIMENTO' in natureza_upper:
        return 'DESAPARECIMENTO'
    elif 'HOMICIDIO' in natureza_upper or 'HOMICÍDIO' in natureza_upper:
        return 'HOMICIDIO'
    elif 'CADAVER' in natureza_upper or 'CADÁVER' in natureza_upper:
        return 'CADAVER'
    
    return None


def identificar_papel_pessoa(papel: str) -> Optional[str]:
    """
    Identifica e padroniza o papel da pessoa na ocorrência.
    
    Papéis reconhecidos:
    - VITIMA
    - AUTOR
    - TESTEMUNHA
    - COMUNICANTE
    - REPRESENTANTE
    
    Args:
        papel: String com descrição do papel
        
    Returns:
        String padronizada do papel ou None
    """
    if pd.isna(papel):
        return None
        
    papel_upper = str(papel).upper().strip()
    
    if 'VITIMA' in papel_upper or 'VÍTIMA' in papel_upper:
        return 'VITIMA'
    elif 'AUTOR' in papel_upper:
        return 'AUTOR'
    elif 'TESTEMUNHA' in papel_upper:
        return 'TESTEMUNHA'
    elif 'COMUNICANTE' in papel_upper:
        return 'COMUNICANTE'
    elif 'REPRESENTANTE' in papel_upper:
        return 'REPRESENTANTE'
    
    return None


def eh_vitima_grupo_alvo(row: pd.Series) -> bool:
    """
    Verifica se o registro é de uma vítima do grupo-alvo.
    
    Args:
        row: Linha do DataFrame com campos natureza_alvo e papel_pessoa
        
    Returns:
        True se for vítima de natureza-alvo, False caso contrário
    """
    return (pd.notna(row.get('natureza_alvo')) and 
            row.get('papel_pessoa') == 'VITIMA')


def enriquecer_com_chaves(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriquece DataFrame com chaves de correlação e classificações.
    
    Adiciona as colunas:
    - chave_ocorrencia: Identificador único da ocorrência
    - chave_pessoa: Identificador único da pessoa
    - natureza_alvo: Classificação da natureza da OCORRÊNCIA (DESAPARECIMENTO/HOMICIDIO/CADAVER)
    - contexto_pessoa: Classificação do contexto da PESSOA (DESAPARECIMENTO/HOMICIDIO/CADAVER)
    - papel_pessoa: Classificação do papel (VITIMA/AUTOR/TESTEMUNHA/etc)
    
    Args:
        df: DataFrame com dados das ocorrências
        
    Returns:
        DataFrame enriquecido com novas colunas
    """
    print("Gerando chaves de correlação...")
    
    # Gera chaves
    df['chave_ocorrencia'] = df.apply(gerar_chave_ocorrencia, axis=1)
    df['chave_pessoa'] = df.apply(gerar_chave_pessoa, axis=1)
    
    # Classifica natureza da OCORRÊNCIA (usa 'natureza' ou 'natureza_padronizada')
    col_natureza = 'natureza_padronizada' if 'natureza_padronizada' in df.columns else 'natureza'
    if col_natureza in df.columns:
        df['natureza_alvo'] = df[col_natureza].apply(identificar_natureza_alvo)
    else:
        df['natureza_alvo'] = None
    
    # Classifica contexto da PESSOA (usa 'natureza_envolvido')
    if 'natureza_envolvido' in df.columns:
        df['contexto_pessoa'] = df['natureza_envolvido'].apply(identificar_natureza_alvo)
    else:
        df['contexto_pessoa'] = None
    
    # Classifica papel (usa 'tipo_vinculo')
    if 'tipo_vinculo' in df.columns:
        df['papel_pessoa'] = df['tipo_vinculo'].apply(identificar_papel_pessoa)
    else:
        df['papel_pessoa'] = None
    
    # Estatísticas
    total_com_chave_ocorrencia = df['chave_ocorrencia'].notna().sum()
    total_com_chave_pessoa = df['chave_pessoa'].notna().sum()
    total_natureza_alvo = df['natureza_alvo'].notna().sum()
    total_contexto_pessoa = df['contexto_pessoa'].notna().sum() if 'contexto_pessoa' in df.columns else 0
    
    print(f"- Chaves de ocorrência geradas: {total_com_chave_ocorrencia:,}")
    print(f"- Chaves de pessoa geradas: {total_com_chave_pessoa:,}")
    print(f"- Natureza da ocorrência classificada: {total_natureza_alvo:,}")
    print(f"- Contexto da pessoa classificado: {total_contexto_pessoa:,}")
    
    # Distribuição dos contextos
    if 'contexto_pessoa' in df.columns and df['contexto_pessoa'].notna().sum() > 0:
        print(f"\nDistribuição por contexto da pessoa:")
        print(df['contexto_pessoa'].value_counts())
    
    return df


def filtrar_grupo_alvo(df: pd.DataFrame, apenas_vitimas: bool = True) -> pd.DataFrame:
    """
    Filtra DataFrame para manter apenas registros do grupo-alvo.
    
    Args:
        df: DataFrame com dados enriquecidos
        apenas_vitimas: Se True, filtra apenas vítimas; se False, mantém todos os papéis
        
    Returns:
        DataFrame filtrado
    """
    if apenas_vitimas:
        df_filtrado = df[df.apply(eh_vitima_grupo_alvo, axis=1)].copy()
        print(f"Filtrado para vítimas do grupo-alvo: {len(df_filtrado):,} registros")
    else:
        df_filtrado = df[df['natureza_alvo'].notna()].copy()
        print(f"Filtrado para grupo-alvo (todos os papéis): {len(df_filtrado):,} registros")
    
    return df_filtrado
