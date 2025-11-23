# PROJETO-CERBERUS-SGI

CERBERUS é um sistema de análise criminal que cruza desaparecimentos, localização de cadáver e homicídios. Realiza ETL completo, gera chaves de matching, detecta padrões e valida identidade usando IA local, focando precisão e rastreabilidade.

## Estrutura do Projeto

```
PROJETO-CERBERUS-SGI/
├── config/                    # Configurações do sistema
│   ├── __init__.py
│   └── settings.py           # Configurações principais
├── utils/                    # Funções utilitárias
│   ├── __init__.py
│   ├── normalization.py      # Normalização de texto e dados
│   ├── key_generation.py     # Geração de chaves de matching
│   └── validation.py         # Validação de dados
├── models/                   # Modelos de dados Pydantic
│   ├── __init__.py
│   ├── base.py              # Modelo base
│   ├── pessoa.py            # Modelos de pessoa e eventos
│   └── matching.py          # Modelos de matching
├── etl/                     # Pipeline ETL
│   ├── __init__.py
│   ├── padronizacao/        # Padronização de dados
│   │   ├── __init__.py
│   │   ├── padronizador.py
│   │   └── transformers.py
│   ├── matching/            # Matching entre datasets
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   └── similarity.py
│   └── pipeline/            # Orquestração do pipeline
│       ├── __init__.py
│       └── etl_pipeline.py
├── scripts/                 # Scripts executáveis
│   ├── __init__.py
│   ├── run_pipeline.py      # Executa pipeline completo
│   ├── test_normalization.py # Testa normalização
│   └── test_matching.py     # Testa matching
├── output/                  # Resultados do processamento
├── requirements.txt         # Dependências Python
└── README.md               # Documentação
```

## Funcionalidades Principais

### 1. Normalização de Dados
- Remoção de acentos e caracteres especiais
- Padronização de nomes (remoção de prefixos/sufixos)
- Normalização de documentos (CPF, RG)
- Validação de CPF

### 2. Geração de Chaves de Matching
- Chaves compostas baseadas em múltiplos campos
- Chaves fonéticas para matching aproximado
- Chaves de bloqueio para otimização

### 3. Matching entre Datasets
- Matching exato por CPF ou chave composta
- Matching fonético por similaridade de nomes
- Matching fuzzy usando distância de Levenshtein
- Scores de confiança (high, medium, low)

### 4. Pipeline ETL Completo
- Carregamento de dados (CSV, Excel)
- Padronização automática
- Matching entre múltiplos datasets
- Exportação de resultados

## Instalação

```bash
# Clone o repositório
git clone https://github.com/jtavares1973/PROJETO-CERBERUS-SGI.git
cd PROJETO-CERBERUS-SGI

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

## Uso

### Teste de Normalização
```bash
python scripts/test_normalization.py
```

### Teste de Matching
```bash
python scripts/test_matching.py
```

### Pipeline Completo
```bash
python scripts/run_pipeline.py
```

### Uso Programático

```python
from etl.pipeline import ETLPipeline
from pathlib import Path

# Inicializa pipeline
pipeline = ETLPipeline()

# Carrega e padroniza datasets
pipeline.load_dataset(Path("data/desaparecimentos.csv"), "desaparecimentos", "desaparecimento")
pipeline.padronizar("desaparecimentos", "desaparecimento")

# Realiza matching
matches = pipeline.realizar_matching("desaparecimentos", "cadaveres")

# Exporta resultados
pipeline.export_matches("resultados_matching.csv")
```

## Configuração

O sistema pode ser configurado através de variáveis de ambiente com o prefixo `CERBERUS_`:

```bash
export CERBERUS_SIMILARITY_THRESHOLD=0.85
export CERBERUS_LOG_LEVEL=INFO
```

Ou editando diretamente o arquivo `config/settings.py`.

## Modelos de Dados

### Pessoa
Modelo base com dados pessoais:
- Nome, CPF, RG, data de nascimento
- Nome da mãe, sexo

### Desaparecimento
Extends Pessoa com:
- Data e local do desaparecimento
- Circunstâncias, número de BO

### Homicídio
Extends Pessoa com:
- Data e local do homicídio
- Causa da morte, arma utilizada

### Cadáver
Modelo independente com:
- Data e local da localização
- Características físicas, idade estimada
- Estado de conservação

## Contribuindo

Este é um projeto em desenvolvimento. Contribuições são bem-vindas!

## Licença

[Definir licença]
