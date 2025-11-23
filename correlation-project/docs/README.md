# 🔍 AGENTE-CORRELACAO
## Sistema de ETL e Matching para Correlação de Desaparecidos e Mortes

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Latest-green.svg)](https://pandas.pydata.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Latest-red.svg)](https://pydantic-docs.helpmanual.io/)

---

## 📖 Visão Geral

O **AGENTE-CORRELACAO** é um sistema especializado de ETL (Extract, Transform, Load) e correlação de dados projetado para identificar conexões entre três bases de dados críticas:

1. **Desaparecidos** 👤
2. **Localização de Cadáveres** 🏥
3. **Vítimas de Homicídio** ⚠️

### 🎯 Objetivo Principal

Descobrir automaticamente se pessoas que **desapareceram**:
- Foram **encontradas mortas** (localização de cadáver)
- Foram **vítimas de homicídio**
- Permanecem **desaparecidas sem desfecho**

### 🧠 Funcionalidades Especiais

- **Matching Inteligente** com três níveis de confiança (forte, moderado, fraco)
- **Detecção Automática de Transtornos Psiquiátricos** no histórico narrativo
- **Normalização Profissional** de nomes, datas e campos
- **Pipeline Auditável e Reprodutível**
- **Validação com Pydantic** para garantir qualidade dos dados

---

## 🏗️ Arquitetura do Projeto

```
correlation-project/
│
├── raw_csv/                    # CSVs originais (colocar aqui)
│
├── config/
│   └── config.py              # Configurações centralizadas
│
├── models/
│   └── schemas.py             # Modelos Pydantic para validação
│
├── utils/
│   ├── normalization.py       # Funções de normalização
│   └── psychiatric_detector.py # Detector de transtornos
│
├── etl/
│   ├── padronizacao.py        # Padronização de campos
│   ├── matching_engine.py     # Engine de matching
│   └── pipeline.py            # Pipeline completo
│
├── output/                    # Resultados gerados
│   └── dataset_unificado.csv
│
├── docs/                      # Documentação
│
├── agente_correlacao.py       # 🤖 AGENTE PRINCIPAL
│
└── README.md                  # Este arquivo
```

---

## 🚀 Como Usar

### 1️⃣ Instalação de Dependências

```bash
pip install pandas pydantic python-dateutil
```

### 2️⃣ Preparar os Dados

Coloque seu CSV de entrada no diretório raiz ou especifique o caminho completo.

Exemplo:
```
d:\___MeusScripts\LangChain\Dados-homi-desaperecido.csv
```

### 3️⃣ Executar o Agente

#### Modo Simples (Automático):

```bash
python agente_correlacao.py "caminho/para/seu/arquivo.csv"
```

#### Modo com Output Personalizado:

```bash
python agente_correlacao.py "caminho/para/arquivo.csv" -o "saida/resultado.csv"
```

#### Modo Etapa por Etapa (Para Debug):

```bash
python agente_correlacao.py "caminho/para/arquivo.csv" --etapa-por-etapa
```

#### Modo Silencioso:

```bash
python agente_correlacao.py "caminho/para/arquivo.csv" --quiet
```

### 4️⃣ Uso Programático

```python
from agente_correlacao import AgenteCorrelacao

# Criar o agente
agente = AgenteCorrelacao(verbose=True)

# Executar pipeline completo
df_resultado = agente.executar_pipeline_completo(
    caminho_csv="Dados-homi-desaperecido.csv",
    output_path="output/dataset_unificado.csv"
)

# Exibir relatório estatístico
agente.exibir_relatorio()
```

---

## 🔍 Como Funciona o Matching

### Chaves de Matching

O sistema cria três tipos de chaves para correlacionar registros:

#### 1. **Chave Forte** (Confiança: 95%)
```
nome_normalizado + data_nascimento_completa
```
Exemplo: `"joao silva|1985-03-15"`

#### 2. **Chave Moderada** (Confiança: 75%)
```
nome_normalizado + ano_nascimento
```
Exemplo: `"joao silva|1985"`

#### 3. **Chave Fraca** (Confiança: 50%)
```
nome_normalizado
```
Exemplo: `"joao silva"`

### Validações Adicionais

- **Sexo**: Deve ser compatível (ou desconhecido)
- **Idade**: Diferença máxima de 3 anos (no match fraco)
- **Data**: Desaparecimento deve ocorrer antes da localização

---

## 🧠 Detecção de Transtornos Psiquiátricos

O agente analisa o campo **"Histórico"** para identificar menções a:

### Termos Detectados:

- Transtorno mental, problema psiquiátrico
- Esquizofrenia, bipolar, depressão, ansiedade
- Psicose, surto psicótico, crise
- Tentativa de suicídio, ideação suicida
- Medicamentos: Rivotril, Haldol, Olanzapina, etc.
- CIDs: F20, F31, F32, F33, F41...

### Níveis de Confiança:

- **Alta**: Diagnóstico específico ou múltiplas menções
- **Média**: 2+ menções ou medicamento psiquiátrico
- **Baixa**: 1 menção genérica
- **Inconclusivo**: Nenhuma menção

### Princípios Éticos:

✅ **NUNCA inferir sem evidência textual**  
✅ **NUNCA inventar fatos**  
✅ **Sempre citar a fonte (trecho do histórico)**

---

## 📊 Dataset Final Unificado

### Campos do CSV de Saída:

```csv
id_unico, nome, nome_normalizado, data_nascimento, sexo, idade_estimativa,
nome_mae, local_de_referencia, data_desaparecimento, historico_desaparecimento,
data_localizacao_cadaver, local_cadaver, causa_morte_presumida,
data_homicidio, circunstancias_homicidio, local_homicidio,
tem_transtorno_psiquiatrico, tipo_transtorno, evidencia_transtorno,
classificacao_final, match_forte, match_moderado, match_fraco, fonte_match
```

### Classificações Possíveis:

- ✅ **Desaparecido localizado vivo**
- ⚰️ **Desaparecido encontrado morto**
- 🔫 **Desaparecido vítima de homicídio**
- ❓ **Desaparecido sem desfecho**
- 🏥 **Cadáver sem registro de desaparecimento**
- ⚠️ **Homicídio sem registro de desaparecimento**

---

## 📈 Exemplo de Relatório

Ao final da execução, o agente exibe:

```
================================================================================
RELATÓRIO ESTATÍSTICO
================================================================================

Total de registros processados: 1523

📊 Distribuição por Classificação:
  • Desaparecido sem desfecho: 987
  • Desaparecido encontrado morto: 234
  • Desaparecido vítima de homicídio: 189
  • Desaparecido localizado vivo: 113

🧠 Transtornos Psiquiátricos:
  • Detectados: 342

🔗 Matching:
  • Matches Fortes: 187
  • Matches Moderados: 145
  • Matches Fracos: 91
================================================================================
```

---

## ⚙️ Configurações Avançadas

Edite `config/config.py` para personalizar:

- Mapeamento de campos
- Palavras-chave de transtornos
- Classificações finais
- Tipos de natureza reconhecidos

---

## 🎭 Prompt para MCP (Model Context Protocol)

Use este prompt para integrar com sistemas MCP:

```
You are AGENTE-CORRELACAO, an MCP agent specialized in ETL, entity matching,
and correlation analysis between three datasets: desaparecidos, localização 
de cadáver, and vítimas de homicídio.

Your mission is:

1. Normalize the datasets:
   - Padronizar nomes de campos
   - Normalizar nomes de pessoas (sem acentos, minúsculo, limpo)
   - Padronizar datas, sexo, idade estimada

2. Generate matching keys:
   - chave_forte = nome_normalizado + data_nascimento
   - chave_moderada = nome_normalizado + ano_nascimento
   - chave_fraca = nome_normalizado

3. Perform cross-dataset matching:
   - Desaparecido → localizado morto
   - Desaparecido → vítima de homicídio
   - Reconciliar conflitos e identificar desfechos

4. Extract psychiatric indicators from "historico":
   - Localizar termos como "transtorno", "psicótico", "suicídio", "bipolar"
   - NUNCA inferir sem texto
   - Preencher: tem_transtorno_psiquiatrico, tipo_transtorno, evidencia_transtorno

5. Create a unified dataset with validated fields using Pydantic models

6. Your behavior:
   - Nunca inventar dados
   - Nunca inferir raça, cor ou etnia
   - Não alterar nomes
   - Em campos ausentes, usar null
   - Ser extremamente preciso e ético
   - Sempre devolver JSON válido
```

---

## 🤝 Contribuindo

Este é um sistema profissional de análise de dados criminais. 

**Princípios:**
- Ética acima de tudo
- Precisão e auditabilidade
- Nunca inventar ou inferir dados sensíveis
- Sempre citar fontes

---

## 📝 Licença

Este projeto foi desenvolvido para fins de análise criminal e pesquisa.

---

## 👨‍💻 Autor

Desenvolvido por **GitHub Copilot** usando Claude Sonnet 4.5

---

## 🆘 Suporte

Para questões ou problemas:
1. Verifique os logs de execução
2. Use `--etapa-por-etapa` para debug detalhado
3. Verifique se os campos do CSV estão mapeados em `config/config.py`

---

**Última atualização:** 23 de novembro de 2025
