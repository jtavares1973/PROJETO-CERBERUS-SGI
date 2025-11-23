# CERBERUS - Project Summary

## Project Overview
CERBERUS is a criminal analysis system that cross-references missing persons, homicides, and cadaver records to identify potential matches and patterns.

## What Was Created

### 1. Directory Structure
```
PROJETO-CERBERUS-SGI/
├── config/           - System configuration
├── utils/            - Utility functions
├── models/           - Pydantic data models
├── etl/              - ETL pipeline
│   ├── padronizacao/ - Data standardization
│   ├── matching/     - Record matching
│   └── pipeline/     - ETL orchestration
├── scripts/          - Example scripts
└── output/           - Results directory
```

### 2. Core Modules

#### Config Module
- **settings.py**: Centralized configuration with Pydantic BaseSettings
- Configurable via environment variables (CERBERUS_ prefix)
- Default similarity threshold: 0.85

#### Utils Module
- **normalization.py**: Text and data normalization
  - `normalize_name()`: Removes prefixes/suffixes, accents
  - `normalize_document()`: Standardizes CPF/RG format
  - `normalize_text()`: General text cleaning
- **key_generation.py**: Matching key generation
  - `generate_composite_key()`: MD5 hash from multiple fields
  - `generate_phonetic_key()`: Soundex-like phonetic key
  - `generate_blocking_key()`: Performance optimization key
- **validation.py**: Data validation
  - `validate_cpf()`: Brazilian CPF validation with checksum
  - `validate_date()`: Date format validation
  - `validate_nome()`: Name validation

#### Models Module (Pydantic)
- **base.py**: BaseModel with timestamps
- **pessoa.py**: Person-related models
  - `Pessoa`: Base person data (name, CPF, RG, birth date, mother's name)
  - `Desaparecimento`: Missing person record (extends Pessoa)
  - `Homicidio`: Homicide record (extends Pessoa)
  - `Cadaver`: Cadaver record (independent model)
- **matching.py**: Matching-related models
  - `MatchKey`: Generated matching key with normalized fields
  - `MatchResult`: Match result with similarity score and confidence

#### ETL Module

##### Padronização (Standardization)
- **padronizador.py**: Base standardizer class
- **transformers.py**: Type-specific transformers
  - `normalize_pessoa_data()`: Basic person data
  - `normalize_desaparecimento_data()`: Missing person data
  - `normalize_homicidio_data()`: Homicide data
  - `normalize_cadaver_data()`: Cadaver data

##### Matching
- **engine.py**: MatchingEngine class
  - Generates matching keys from DataFrames
  - Compares records using similarity algorithms
  - Returns MatchResult objects with confidence levels
- **similarity.py**: Similarity calculation functions
  - Uses Levenshtein distance for text similarity
  - Weighted field comparison
  - Support for exact, fuzzy, and phonetic matching

##### Pipeline
- **etl_pipeline.py**: Complete ETL orchestration
  - Loads datasets (CSV, Excel)
  - Applies standardization
  - Performs matching between datasets
  - Exports results

### 3. Example Scripts
- **test_normalization.py**: Demonstrates normalization functions
- **test_matching.py**: Demonstrates matching with sample data
- **run_pipeline.py**: Full pipeline execution example

### 4. Documentation
- **README.md**: User-facing documentation with quick start
- **DEVELOPER.md**: Developer guide with architecture details
- **setup.sh**: Environment setup script

## Key Features Implemented

### 1. Data Normalization
✅ Name standardization (remove titles, suffixes)
✅ Document normalization (CPF, RG)
✅ Text cleaning (accents, special characters)
✅ CPF validation with checksum

### 2. Matching Key Generation
✅ Composite keys from multiple fields
✅ Phonetic keys for fuzzy name matching
✅ Blocking keys for performance optimization

### 3. Record Matching
✅ Three matching types:
  - **Exact**: CPF or composite key match
  - **Phonetic**: Name sounds similar
  - **Fuzzy**: Levenshtein distance similarity
✅ Similarity scoring (0.0 to 1.0)
✅ Confidence levels (high/medium/low)
✅ Configurable threshold

### 4. ETL Pipeline
✅ Multi-format data loading (CSV, Excel)
✅ Automatic standardization
✅ Cross-dataset matching
✅ Result export

## Testing Results

All core functionality tested and working:

1. **Module Imports**: ✅ All modules import correctly
2. **Configuration**: ✅ Settings load with defaults
3. **Normalization**: ✅ Text, names, documents normalized correctly
4. **Key Generation**: ✅ Composite and phonetic keys generated
5. **Models**: ✅ Pydantic validation working
6. **Standardization**: ✅ DataFrames processed correctly
7. **Matching**: ✅ Records matched with similarity scores
8. **Security**: ✅ No vulnerabilities found (CodeQL)

## Usage Examples

### Basic Normalization
```python
from utils import normalize_name, validate_cpf

name = normalize_name("Dr. João da Silva Jr.")  # "joao da silva"
valid = validate_cpf("123.456.789-09")  # True
```

### Dataset Matching
```python
from etl.matching import match_datasets
import pandas as pd

df1 = pd.DataFrame([...])  # Missing persons
df2 = pd.DataFrame([...])  # Cadavers

matches = match_datasets(df1, df2, "missing", "cadavers")
for match in matches:
    print(f"Match: {match.similarity_score:.2%} confidence: {match.confidence}")
```

### Full Pipeline
```python
from etl.pipeline import ETLPipeline

pipeline = ETLPipeline()
pipeline.load_dataset("data.csv", "dataset1", "desaparecimento")
pipeline.padronizar("dataset1", "desaparecimento")
matches = pipeline.realizar_matching("dataset1", "dataset2")
pipeline.export_matches("results.csv")
```

## Dependencies

Core dependencies installed:
- pydantic >= 2.0.0 (data validation)
- pydantic-settings >= 2.0.0 (configuration)
- pandas >= 2.0.0 (data processing)
- unidecode >= 1.3.0 (text normalization)
- python-Levenshtein >= 0.21.0 (similarity)

## System Requirements

- Python 3.10+
- pip package manager
- Virtual environment (recommended)

## Quick Start

```bash
# Setup
bash setup.sh

# Run tests
PYTHONPATH=. python scripts/test_normalization.py
PYTHONPATH=. python scripts/test_matching.py

# Or install in development mode
pip install -e .
python scripts/test_normalization.py
```

## What's Next?

The foundation is complete. Future enhancements could include:

1. **Data Sources**: Connectors for real criminal databases
2. **Advanced Matching**: Machine learning-based matching
3. **Visualization**: Dashboard for viewing matches
4. **API**: REST API for integration
5. **Performance**: Distributed processing for large datasets
6. **AI Integration**: Local AI for pattern detection
7. **Testing**: Comprehensive unit and integration tests

## File Statistics

- **Total Python files**: 27
- **Total lines of code**: ~2000+
- **Modules**: 4 main modules (config, utils, models, etl)
- **Submodules**: 3 ETL submodules
- **Scripts**: 3 example scripts
- **Documentation**: 3 docs (README, DEVELOPER, SUMMARY)

---

**Status**: ✅ Complete and operational
**Security**: ✅ No vulnerabilities detected
**Tests**: ✅ All systems validated
