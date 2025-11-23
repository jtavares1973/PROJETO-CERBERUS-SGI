# CERBERUS - Guia de Desenvolvimento

## Arquitetura do Sistema

### Visão Geral
O CERBERUS é um sistema modular de análise criminal composto por:

1. **Config**: Gerenciamento de configurações
2. **Utils**: Funções utilitárias reutilizáveis
3. **Models**: Modelos de dados validados com Pydantic
4. **ETL**: Pipeline de processamento de dados
   - Padronização: Normalização de dados
   - Matching: Identificação de correspondências
   - Pipeline: Orquestração do fluxo

### Fluxo de Dados

```
┌─────────────┐
│ Dados Raw   │ (CSV, Excel, etc.)
└─────┬───────┘
      │
      ▼
┌─────────────────┐
│ Padronização    │ Normaliza nomes, documentos, datas
└─────┬───────────┘
      │
      ▼
┌─────────────────┐
│ Geração Chaves  │ Cria chaves de matching
└─────┬───────────┘
      │
      ▼
┌─────────────────┐
│ Matching        │ Encontra correspondências
└─────┬───────────┘
      │
      ▼
┌─────────────────┐
│ Resultados      │ Exporta matches encontrados
└─────────────────┘
```

## Módulos Principais

### 1. Config (`config/`)

**Propósito**: Centraliza configurações do sistema

**Arquivos**:
- `settings.py`: Define classe `Settings` com parâmetros configuráveis

**Uso**:
```python
from config import get_settings

settings = get_settings()
print(settings.similarity_threshold)  # 0.85
```

### 2. Utils (`utils/`)

**Propósito**: Funções utilitárias para todo o sistema

**Arquivos**:
- `normalization.py`: Normalização de texto e dados
- `key_generation.py`: Geração de chaves para matching
- `validation.py`: Validação de dados (CPF, datas, etc.)

**Principais funções**:

```python
from utils import (
    normalize_name,           # Normaliza nomes de pessoa
    normalize_document,       # Normaliza CPF, RG
    generate_composite_key,   # Gera chave composta
    generate_phonetic_key,    # Gera chave fonética
    validate_cpf,            # Valida CPF
)
```

### 3. Models (`models/`)

**Propósito**: Modelos de dados com validação Pydantic

**Arquivos**:
- `base.py`: Modelo base
- `pessoa.py`: Modelos de pessoa e eventos criminais
- `matching.py`: Modelos de resultados de matching

**Modelos principais**:

```python
from models import (
    Pessoa,           # Dados básicos de pessoa
    Desaparecimento,  # Registro de desaparecimento
    Homicidio,        # Registro de homicídio
    Cadaver,          # Registro de cadáver
    MatchKey,         # Chave de matching
    MatchResult,      # Resultado de match
)
```

### 4. ETL (`etl/`)

**Propósito**: Pipeline de processamento de dados

#### 4.1 Padronização (`etl/padronizacao/`)

Normaliza datasets para processamento uniforme.

```python
from etl.padronizacao import padronizar_dataset

df_normalizado = padronizar_dataset(df_raw, "desaparecimento")
```

**Transformações aplicadas**:
- Normalização de nomes (remove prefixos, sufixos)
- Normalização de documentos (remove formatação)
- Validação de CPFs
- Conversão de datas
- Padronização de campos de texto

#### 4.2 Matching (`etl/matching/`)

Identifica correspondências entre registros.

```python
from etl.matching import match_datasets, MatchingEngine

# Uso simples
matches = match_datasets(df1, df2, "dataset1", "dataset2")

# Uso avançado
engine = MatchingEngine(similarity_threshold=0.85)
keys1 = engine.generate_keys(df1, "dataset1")
keys2 = engine.generate_keys(df2, "dataset2")
matches = engine.match_records(keys1, keys2)
```

**Tipos de matching**:
- **Exact**: Match exato em chave composta ou CPF
- **Phonetic**: Match por similaridade fonética
- **Fuzzy**: Match por similaridade textual (Levenshtein)

**Níveis de confiança**:
- **High**: Similaridade ≥ 95% e CPF ou 3+ campos
- **Medium**: Similaridade ≥ 85%
- **Low**: Similaridade < 85%

#### 4.3 Pipeline (`etl/pipeline/`)

Orquestra o fluxo completo de ETL.

```python
from etl.pipeline import ETLPipeline

pipeline = ETLPipeline()

# Carrega datasets
pipeline.load_dataset(path1, "desaparecimentos", "desaparecimento")
pipeline.load_dataset(path2, "cadaveres", "cadaver")

# Padroniza
pipeline.padronizar("desaparecimentos", "desaparecimento")
pipeline.padronizar("cadaveres", "cadaver")

# Realiza matching
matches = pipeline.realizar_matching("desaparecimentos", "cadaveres")

# Exporta resultados
pipeline.export_matches("matches.csv")
```

## Scripts de Exemplo

### `test_normalization.py`
Demonstra funções de normalização e validação.

```bash
PYTHONPATH=. python scripts/test_normalization.py
```

### `test_matching.py`
Demonstra matching entre datasets de teste.

```bash
PYTHONPATH=. python scripts/test_matching.py
```

### `run_pipeline.py`
Executa pipeline completo (requer arquivos de dados).

```bash
PYTHONPATH=. python scripts/run_pipeline.py
```

## Extensão do Sistema

### Adicionando Novos Tipos de Dados

1. **Criar modelo em `models/pessoa.py`**:
```python
class NovoTipo(Pessoa):
    campo_especifico: str
    # ...
```

2. **Adicionar transformador em `etl/padronizacao/transformers.py`**:
```python
def normalize_novo_tipo_data(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_pessoa_data(df)
    # Transformações específicas
    return df
```

3. **Atualizar `padronizar_dataset`** para incluir novo tipo.

### Adicionando Novos Algoritmos de Matching

1. **Criar função em `etl/matching/similarity.py`**:
```python
def calculate_novo_algoritmo(rec1, rec2) -> float:
    # Implementação
    return score
```

2. **Integrar em `MatchingEngine.match_records()`**.

### Personalizando Configurações

Edite `config/settings.py` ou use variáveis de ambiente:

```bash
export CERBERUS_SIMILARITY_THRESHOLD=0.90
export CERBERUS_LOG_LEVEL=DEBUG
```

## Boas Práticas

### 1. Normalização
- Sempre normalize dados antes de matching
- Use `normalize_name()` para nomes de pessoas
- Use `normalize_document()` para documentos
- Valide CPFs com `validate_cpf()`

### 2. Matching
- Ajuste `similarity_threshold` baseado na qualidade dos dados
- Use `phonetic_matching` para dados com erros ortográficos
- Filtre matches por `confidence` para reduzir falsos positivos

### 3. Performance
- Use blocking keys para datasets grandes
- Processe em lotes se necessário
- Cache chaves de matching quando possível

### 4. Qualidade de Dados
- Valide dados de entrada
- Trate valores faltantes apropriadamente
- Mantenha log de erros de padronização

## Testing

Execute os scripts de teste para verificar funcionalidade:

```bash
# Setup do ambiente
bash setup.sh

# Testes de normalização
PYTHONPATH=. python scripts/test_normalization.py

# Testes de matching
PYTHONPATH=. python scripts/test_matching.py
```

## Troubleshooting

### ImportError: No module named 'X'
Solução: Defina PYTHONPATH ou instale em modo desenvolvimento:
```bash
export PYTHONPATH=.
# ou
pip install -e .
```

### Matches com baixa qualidade
- Verifique threshold de similaridade
- Confirme que dados foram normalizados
- Valide qualidade dos dados de entrada

### Performance lenta
- Use blocking keys para reduzir comparações
- Processe datasets em paralelo
- Considere indexação para datasets grandes
