# ARQUITETURA DO SISTEMA DE CORRELAÇÕES

## 📋 VISÃO GERAL

Sistema para correlacionar registros de **desaparecimento** com registros de **morte** (cadáver/homicídio), identificando casos onde a mesma pessoa desapareceu e posteriormente foi encontrada morta.

---

## 🏗️ FLUXO DE DADOS

```
CSV Bruto (21,455 registros)
    ↓
[1. ETL/PIPELINE] - Padronização + Enriquecimento + Detecção Psiquiátrica
    ↓
dataset_unificado.xlsx (21,455 registros processados)
    ↓
[2. GERAÇÃO DE CORRELAÇÕES] - Análise temporal por chave_pessoa
    ↓
correlacoes_completas_com_identificacao.xlsx (450 correlações)
    ↓
[3. DEDUPLICAÇÃO] - Remove duplicatas, mantém melhor correlação
    ↓
correlacoes_unicas_deduplicadas.xlsx (161 pessoas únicas)
    ↓
[4. VALIDAÇÃO IA] - Valida identidade com Ollama qwen3:14b
    ↓
validacao_unica_progresso.xlsx (86 casos FORTES validados)
    ↓
[5. RELATÓRIO FINAL] - Excel formatado para analistas
    ↓
RELATORIO_VALIDACAO_FINAL.xlsx
```

---

## 📊 ESTRUTURA DE DADOS

### COLUNAS PRINCIPAIS (dataset_unificado.xlsx)

#### Identificação da Pessoa
- `chave_pessoa` - Chave única: `nome_normalizado|DD/MM/YYYY`
- `nome` - Nome completo original
- `nome_normalizado` - Nome sem acentos, maiúsculas
- `data_nascimento` - Data de nascimento (datetime)
- `ano_nascimento` - Ano de nascimento (int)
- `nome_mae` - Nome da mãe
- `nome_mae_normalizado` - Nome da mãe normalizado
- `nome_pai` - Nome do pai
- **`numero_identidade`** - Número do RG ⚠️ CORRETO
- `orgao_expedidor_identidade` - Órgão emissor do RG
- `uf_identidade` - UF do RG
- `sexo` - M/F/IGN
- `raca_padronizada` - Raça padronizada

#### Identificação do Evento
- `chave_ocorrencia` - Chave única: `YYYY_UNIDADE_NUMERO`
- `natureza_alvo` - DESAPARECIMENTO | CADAVER | HOMICIDIO
- `papel_pessoa` - VITIMA (sempre)
- `data_fato_dt` - Data do fato (datetime)
- `historico_limpo` - Histórico do BO limpo
- `cidade_ra` - Cidade/RA do evento
- `unidade_registro` - Delegacia/Unidade

#### Transtorno Psiquiátrico
- `tem_transtorno_psiquiatrico` - Boolean
- `tipo_transtorno` - Tipo específico detectado
- `evidencia_transtorno` - Trecho do texto que evidencia
- `confianca_transtorno` - alta/média/baixa/inconclusivo

---

## 🔑 LÓGICA DE CORRELAÇÃO

### Regra de Negócio
1. **Mesma pessoa** (`chave_pessoa` idêntica)
2. **Sequência temporal**: DESAPARECIMENTO → CADAVER/HOMICIDIO
3. **Sem eventos intermediários** (ideal, mas não obrigatório)

### Classificação por Intervalo
- **FORTE**: 0-30 dias entre desaparecimento e morte
- **MÉDIA**: 31-90 dias
- **FRACA**: > 90 dias

### Campos de Correlação
- `dias_entre_eventos` - Intervalo em dias
- `tem_evento_intermediario` - Boolean
- `forca_correlacao` - FORTE/MÉDIA/FRACA
- `explicacao` - Texto explicativo

---

## 🎯 MAPEAMENTO DE COLUNAS CORRETO

### ❌ PROBLEMA IDENTIFICADO
O script `gerar_correlacoes_completas.py` estava usando:
```python
'numero_rg': desap['numero_identidade'],  # ✅ CORRETO
```

Mas a validação esperava:
```python
caso['numero_rg']  # ✅ Nome correto na correlação
```

### ✅ COLUNAS CORRETAS

| Campo Lógico | Coluna no dataset_unificado.xlsx | Coluna na correlação |
|--------------|----------------------------------|---------------------|
| RG | `numero_identidade` | `numero_rg` |
| Órgão RG | `orgao_expedidor_identidade` | `orgao_rg` |
| UF RG | `uf_identidade` | `uf_rg` |
| Nome Mãe | `nome_mae` | `nome_mae` |
| Nome Pai | `nome_pai` | `nome_pai` |
| Data Nasc | `data_nascimento` | `data_nascimento` |

---

## 🚨 PONTOS DE ATENÇÃO

### 1. Duplicatas
**Causa**: Mesmo par (BO desaparecimento + BO morte) aparece múltiplas vezes no dataset.

**Exemplo**: NILDERSON DA SILVA apareceu 6x com o mesmo par de BOs.

**Solução**: Script `remover_duplicatas.py` que:
- Agrupa por `chave_pessoa`
- Ordena por `dias_entre_eventos` (ASC)
- Mantém primeiro registro (menor intervalo)

### 2. Nomenclatura de Colunas
**Padronização**:
- Dataset ETL: `numero_identidade` (nome técnico do sistema)
- Correlação: `numero_rg` (nome orientado ao negócio)
- Esta conversão acontece em `gerar_correlacoes_completas.py`

### 3. Validação IA
**Campos obrigatórios no prompt**:
- Nome completo
- Data de nascimento
- Nome da mãe
- Nome do pai
- Número RG
- Históricos completos dos BOs
- Transtorno psiquiátrico (se houver)

---

## 📁 ARQUIVOS PRINCIPAIS

### Scripts de Processamento
1. **`etl/pipeline.py`** - Pipeline principal de ETL
   - Carrega CSV bruto
   - Padroniza dados
   - Enriquece com chaves de correlação
   - Detecta transtornos psiquiátricos
   - Gera `dataset_unificado.xlsx`

2. **`gerar_correlacoes_completas.py`** - Gera correlações temporais
   - Lê `dataset_unificado.xlsx`
   - Agrupa por `chave_pessoa`
   - Identifica sequências DESAPARECIMENTO → MORTE
   - Calcula intervalos e força da correlação
   - Gera `correlacoes_completas_com_identificacao.xlsx` (450 registros)

3. **`remover_duplicatas.py`** - Remove registros duplicados
   - Lê correlações completas
   - Remove duplicatas por `chave_pessoa`
   - Mantém correlação com menor intervalo
   - Gera `correlacoes_unicas_deduplicadas.xlsx` (161 registros únicos)

4. **`validar_com_retomada.py`** - Valida com IA (Ollama)
   - Lê correlações deduplicadas
   - Valida identidade caso a caso com qwen3:14b
   - Salva progresso após cada caso
   - Permite retomada se interrompido
   - Gera `validacao_unica_progresso.xlsx`

### Utilitários
- **`utils/chaves.py`** - Geração de chaves de correlação
- **`utils/psychiatric_detector.py`** - Detecção de transtornos
- **`config/config.py`** - Configurações centralizadas

### Visualização
- **`ver_relatorio_completo.py`** - Exibe casos no terminal
- **`mostrar_validacao.py`** - Mostra resultados da validação

---

## 🔄 PROCESSO COMPLETO

### Passo 1: ETL Inicial
```bash
cd correlation-project
python etl/pipeline.py
```
**Output**: `output/dataset_unificado.xlsx` (21,455 registros)

### Passo 2: Gerar Correlações
```bash
python gerar_correlacoes_completas.py
```
**Output**: `output/correlacoes_completas_com_identificacao.xlsx` (450 correlações)

### Passo 3: Remover Duplicatas
```bash
python remover_duplicatas.py
```
**Output**: `output/correlacoes_unicas_deduplicadas.xlsx` (161 únicas)

### Passo 4: Validar com IA
```bash
python validar_com_retomada.py
```
**Output**: 
- `output/validacao_unica_progresso.xlsx` (progresso contínuo)
- `output/RELATORIO_VALIDACAO_FINAL.xlsx` (relatório final)

---

## 📈 ESTATÍSTICAS ESPERADAS

### Dataset Unificado (21,455)
- Desaparecimentos: ~10,000
- Cadáveres: ~8,000
- Homicídios: ~3,000

### Correlações (161 únicas)
- FORTES (0-30 dias): 86 casos ⭐
- MÉDIAS (31-90 dias): 12 casos
- FRACAS (>90 dias): 63 casos

### Validação IA (esperado)
- Taxa de confirmação: ~80%
- Confiança média: ~95%
- Casos com transtorno: ~5-10%

---

## ⚙️ CONFIGURAÇÃO DO AMBIENTE

### Modelo IA
- **Modelo**: Ollama qwen3:14b (9.3GB)
- **Temperatura**: 0.1 (determinístico)
- **Formato**: JSON estruturado
- **Hardware**: GPU 16GB VRAM (RTX 5070 Ti)
- **Tempo**: ~0.2 min/caso

### Bibliotecas Python
- pandas, openpyxl - Manipulação de dados
- ollama - Interface com LLM local
- re, unicodedata - Processamento de texto

---

## 🎯 PRÓXIMOS PASSOS

1. ✅ Corrigir referências de colunas (numero_identidade vs numero_rg)
2. ⏳ Executar validação completa dos 86 casos FORTES
3. ⏳ Gerar relatório final formatado para analistas
4. ⏳ Documentar casos confirmados para perícia

---

## 📝 NOTAS TÉCNICAS

### Por que Duplicatas?
O dataset pode ter:
- Mesma pessoa em múltiplos BOs (desaparecimentos repetidos)
- Registros duplicados por erro de sistema
- Múltiplas vítimas no mesmo BO
- Correções/atualizações de BOs

### Por que Validação IA?
Mesmo com `chave_pessoa` idêntica:
- Pode haver homônimos com mesma data de nascimento
- Dados podem estar incompletos
- Nome da mãe/pai confirmam identidade
- IA analisa narrativa dos históricos para conexões explícitas

### Por que Transtorno Psiquiátrico?
- Fator de risco relevante
- Contexto para análise pericial
- Pode explicar desaparecimento
- Importante para políticas públicas

---

**Última atualização**: 2025-11-23
**Versão**: 2.0
**Status**: Em produção
