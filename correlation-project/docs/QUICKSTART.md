# 🚀 Guia de Início Rápido

## 5 Minutos para Começar

### Passo 1: Instalar Dependências

```bash
pip install pandas pydantic python-dateutil
```

### Passo 2: Preparar seus Dados

Coloque seu CSV no local apropriado. Exemplo:
```
d:\___MeusScripts\LangChain\Dados-homi-desaperecido.csv
```

### Passo 3: Executar o Agente

#### Opção A: Via Linha de Comando (Recomendado para Iniciantes)

```bash
cd correlation-project
python agente_correlacao.py "d:\___MeusScripts\LangChain\Dados-homi-desaperecido.csv"
```

O resultado será salvo automaticamente em `output/dataset_unificado.csv`

#### Opção B: Via Script Python

Crie um arquivo `meu_script.py`:

```python
from agente_correlacao import AgenteCorrelacao

agente = AgenteCorrelacao(verbose=True)

df = agente.executar_pipeline_completo(
    caminho_csv="d:\\___MeusScripts\\LangChain\\Dados-homi-desaperecido.csv",
    output_path="output/meu_resultado.csv"
)

agente.exibir_relatorio()
```

Execute:
```bash
python meu_script.py
```

#### Opção C: Exemplos Interativos

```bash
python exemplos.py
```

Escolha um dos exemplos prontos do menu!

---

## 📊 O que Você Verá

### Durante a Execução:

```
================================================================================
AGENTE-CORRELACAO - Iniciando
================================================================================

[Carregamento] Lendo arquivo: Dados-homi-desaperecido.csv
[Carregamento] 15234 registros carregados

[Pipeline] Iniciando padronização...
[Pipeline] Passo 1/4: Padronizando nomes de colunas...
[Pipeline] Passo 2/4: Processando campos de pessoa...
[Pipeline] Passo 3/4: Criando chaves de matching...
[Pipeline] Passo 4/4: Gerando IDs únicos...
[Pipeline] Padronização concluída!

[Separação] Separando registros por natureza...
  - Desaparecidos: 9876 registros
  - Cadáveres: 3421 registros
  - Homicídios: 1937 registros

[Transtornos] Detectando menções a transtornos psiquiátricos...
[Transtornos] Detectados em 1234 registros

================================================================================
MATCHING: Desaparecidos <-> Cadáveres
================================================================================

[Match Forte] Encontrados 234 matches
[Match Moderado] Encontrados 187 matches
[Match Fraco] Encontrados 92 matches

[Unificação] Criando base unificada...
[Unificação] 9876 registros unificados

================================================================================
AGENTE-CORRELACAO - Concluído com Sucesso
================================================================================
```

### Relatório Final:

```
================================================================================
RELATÓRIO ESTATÍSTICO
================================================================================

Total de registros processados: 9876

📊 Distribuição por Classificação:
  • Desaparecido sem desfecho: 7321
  • Desaparecido encontrado morto: 1234
  • Desaparecido vítima de homicídio: 876
  • Desaparecido localizado vivo: 445

🧠 Transtornos Psiquiátricos:
  • Detectados: 1234

🔗 Matching:
  • Matches Fortes: 234
  • Matches Moderados: 187
  • Matches Fracos: 92
================================================================================
```

---

## 📁 Onde Encontrar os Resultados

Após a execução, verifique:

```
correlation-project/
└── output/
    ├── dataset_unificado.csv      ← Resultado principal
    ├── casos_com_transtornos.csv  ← Se executou o exemplo 3
    └── casos_correlacionados.csv  ← Se executou o exemplo 4
```

---

## 🔍 Como Interpretar o CSV de Saída

### Colunas Principais:

| Coluna | Descrição |
|--------|-----------|
| `id_unico` | ID único do registro |
| `nome` | Nome da pessoa |
| `classificacao_final` | Status final (desaparecido, morto, etc.) |
| `data_desaparecimento` | Quando desapareceu |
| `data_localizacao_cadaver` | Quando foi encontrado (se aplicável) |
| `tem_transtorno_psiquiatrico` | `True` se detectado transtorno |
| `tipo_transtorno` | Tipos detectados |
| `match_forte` | Se houve match de alta confiança |
| `fonte_match` | De onde veio a correlação |

### Filtrar no Excel/LibreOffice:

1. Abra o CSV
2. Selecione a primeira linha
3. Ative "AutoFiltro"
4. Filtre por:
   - `classificacao_final = "Desaparecido encontrado morto"`
   - `tem_transtorno_psiquiatrico = TRUE`
   - `match_forte = TRUE`

---

## ❓ Problemas Comuns

### 1. "ModuleNotFoundError: No module named 'pandas'"

**Solução:**
```bash
pip install pandas pydantic python-dateutil
```

### 2. "FileNotFoundError: arquivo.csv não encontrado"

**Solução:**
- Verifique o caminho do arquivo
- Use caminho absoluto: `d:\\pasta\\arquivo.csv` (Windows)
- Ou caminho relativo: `./dados/arquivo.csv`

### 3. "Encoding error"

**Solução:**
O agente tenta automaticamente `latin-1`, mas você pode editar `etl/pipeline.py`:

```python
df = pd.read_csv(caminho, sep=';', encoding='utf-8', on_bad_lines='skip')
```

### 4. "Nenhum match encontrado"

**Possíveis causas:**
- Campos de nome ou data ausentes
- Dados muito inconsistentes
- Naturezas não reconhecidas

**Solução:**
- Use `--etapa-por-etapa` para debug
- Verifique `config/config.py` → `FIELD_MAPPING`

---

## 🎯 Próximos Passos

1. ✅ Execute o pipeline básico
2. 📊 Analise o relatório estatístico
3. 🔍 Abra o CSV de saída no Excel
4. 🧠 Explore casos com transtornos psiquiátricos
5. 🔗 Analise os matches encontrados
6. ⚙️ Personalize `config/config.py` se necessário

---

## 📞 Precisa de Ajuda?

Veja o `README.md` completo ou execute:

```bash
python agente_correlacao.py --help
```

---

**Boa sorte! 🚀**
