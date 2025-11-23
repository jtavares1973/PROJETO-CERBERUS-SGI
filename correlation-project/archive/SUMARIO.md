# 📦 SUMÁRIO DO PROJETO - AGENTE-CORRELACAO

## ✅ Projeto Completo e Funcional

Este documento resume todos os componentes do sistema.

---

## 📁 Estrutura Completa

```
correlation-project/
│
├── 📝 README.md                          # Documentação principal
├── 📋 requirements.txt                   # Dependências Python
├── 🤖 agente_correlacao.py              # AGENTE PRINCIPAL (CLI + API)
├── 📚 exemplos.py                        # Exemplos interativos
│
├── config/                               # Configurações
│   ├── __init__.py
│   └── config.py                        # Mapeamentos e constantes
│
├── models/                               # Modelos de dados
│   ├── __init__.py
│   └── schemas.py                       # Schemas Pydantic
│
├── utils/                                # Utilitários
│   ├── __init__.py
│   ├── normalization.py                 # Normalização de dados
│   └── psychiatric_detector.py          # Detector de transtornos
│
├── etl/                                  # Pipeline ETL
│   ├── __init__.py
│   ├── padronizacao.py                  # Padronização de campos
│   ├── matching_engine.py               # Engine de matching
│   └── pipeline.py                      # Orquestrador principal
│
├── raw_csv/                              # [VAZIO] Coloque CSVs aqui
│
├── output/                               # Resultados gerados
│   └── dataset_unificado.csv            # (gerado após execução)
│
└── docs/                                 # Documentação adicional
    └── QUICKSTART.md                    # Guia de início rápido
```

---

## 🧩 Componentes Principais

### 1. **agente_correlacao.py** 🤖
- **Função:** Agente principal com CLI e API Python
- **Uso CLI:** `python agente_correlacao.py arquivo.csv`
- **Uso API:** `from agente_correlacao import AgenteCorrelacao`

### 2. **config/config.py** ⚙️
- Mapeamento de campos do CSV
- Palavras-chave para detecção de transtornos
- Classificações e naturezas reconhecidas

### 3. **utils/normalization.py** 🧹
- `normalizar_nome()` - Remove acentos, padroniza
- `normalizar_sexo()` - M, F ou IGN
- `parse_data()` - Converte strings para datetime
- `gerar_chave_forte/moderada/fraca()` - Cria chaves de matching

### 4. **utils/psychiatric_detector.py** 🧠
- Classe `PsychiatricDetector`
- Detecta menções a transtornos mentais
- Retorna: tipo, evidência, confiança

### 5. **etl/padronizacao.py** 📊
- `padronizar_colunas()` - Renomeia campos
- `processar_campos_pessoa()` - Enriquece dados
- `criar_chaves_matching()` - Gera chaves
- `pipeline_padronizacao_completa()` - Executa tudo

### 6. **etl/matching_engine.py** 🔗
- Classe `MatchingEngine`
- `fazer_match_forte()` - Nome + data completa
- `fazer_match_moderado()` - Nome + ano
- `fazer_match_fraco()` - Apenas nome (com validações)

### 7. **etl/pipeline.py** 🚀
- `pipeline_completo()` - Orquestrador principal
- Carrega → Padroniza → Separa → Detecta → Matcha → Unifica

### 8. **models/schemas.py** 📐
- Modelos Pydantic para validação
- `PessoaBase`, `RegistroDesaparecimento`, etc.
- `RegistroUnificado` - Modelo completo final

---

## 🎯 Fluxo de Execução

```
1. CARREGAMENTO
   └─> Lê CSV (encoding latin-1, sep=;)

2. PADRONIZAÇÃO
   ├─> Renomeia colunas (FIELD_MAPPING)
   ├─> Normaliza nomes (sem acentos, minúsculo)
   ├─> Processa datas (parse_data)
   ├─> Normaliza sexo (M/F/IGN)
   ├─> Calcula idade
   └─> Cria chaves (forte/moderada/fraca)

3. SEPARAÇÃO
   ├─> Desaparecidos (NATUREZA_DESAPARECIMENTO)
   ├─> Cadáveres (NATUREZA_LOCALIZACAO_CADAVER)
   └─> Homicídios (NATUREZA_HOMICIDIO)

4. DETECÇÃO DE TRANSTORNOS
   └─> Analisa campo "histórico" com keywords

5. MATCHING
   ├─> Desaparecidos <-> Cadáveres
   │   ├─> Match forte (95% confiança)
   │   ├─> Match moderado (75% confiança)
   │   └─> Match fraco (50% confiança)
   │
   └─> Desaparecidos <-> Homicídios
       └─> (mesmo processo)

6. UNIFICAÇÃO
   └─> Cria dataset final com todos os campos

7. SALVAMENTO
   └─> CSV unificado em output/
```

---

## 📊 Campos do Dataset Final

### Pessoa
- `id_unico`, `nome`, `nome_normalizado`
- `data_nascimento`, `sexo`, `idade_estimativa`
- `nome_mae`, `local_de_referencia`

### Desaparecimento
- `data_desaparecimento`, `boletim_desaparecimento`
- `historico_desaparecimento`, `pessoa_localizada`

### Cadáver (se houver match)
- `data_localizacao_cadaver`, `boletim_localizacao`
- `local_cadaver`, `cod_iml_pessoa`, `possui_laudo_iml`

### Homicídio (se houver match)
- `data_homicidio`, `boletim_homicidio`
- `circunstancias_homicidio`, `local_homicidio`

### Transtorno Psiquiátrico
- `tem_transtorno_psiquiatrico` (bool)
- `tipo_transtorno` (texto)
- `evidencia_transtorno` (trechos do histórico)
- `confianca_transtorno` (alta/media/baixa/inconclusivo)

### Matching
- `chave_forte`, `chave_moderada`, `chave_fraca`
- `match_forte_cad`, `match_moderado_cad`, `match_fraco_cad`
- `match_forte_hom`, `match_moderado_hom`, `match_fraco_hom`
- `fonte_match`, `classificacao_final`

---

## 🚀 Como Executar

### Opção 1: CLI Direto
```bash
python agente_correlacao.py "Dados-homi-desaperecido.csv"
```

### Opção 2: Com Output Customizado
```bash
python agente_correlacao.py "dados.csv" -o "saida/resultado.csv"
```

### Opção 3: Modo Debug (Etapa por Etapa)
```bash
python agente_correlacao.py "dados.csv" --etapa-por-etapa
```

### Opção 4: Exemplos Interativos
```bash
python exemplos.py
```

### Opção 5: Programaticamente
```python
from agente_correlacao import AgenteCorrelacao

agente = AgenteCorrelacao()
df = agente.executar_pipeline_completo("dados.csv", "output/resultado.csv")
agente.exibir_relatorio()
```

---

## 📈 Métricas e Estatísticas

O sistema gera automaticamente:

- **Total de registros** processados
- **Distribuição por classificação:**
  - Desaparecido sem desfecho
  - Desaparecido localizado vivo
  - Desaparecido encontrado morto
  - Desaparecido vítima de homicídio
- **Transtornos detectados** (quantidade e tipos)
- **Matches realizados:**
  - Fortes (alta confiança)
  - Moderados (média confiança)
  - Fracos (baixa confiança)

---

## 🧠 Detecção de Transtornos - Keywords

O sistema detecta ~60 palavras-chave, incluindo:

**Diagnósticos:**
- esquizofrenia, bipolar, depressão, ansiedade, psicose

**Comportamentos:**
- tentativa de suicídio, surto, crise, automutilação

**Medicamentos:**
- rivotril, haldol, olanzapina, fluoxetina, sertralina

**CIDs:**
- F20, F31, F32, F33, F41...

**Termos Gerais:**
- transtorno mental, problema psiquiátrico, acompanhamento

---

## ✅ Checklist de Validação

- [x] Normalização de nomes (sem acentos, minúsculo)
- [x] Normalização de datas (múltiplos formatos)
- [x] Normalização de sexo (M/F/IGN)
- [x] Cálculo de idade (a partir de data nascimento)
- [x] Chaves de matching (forte, moderada, fraca)
- [x] Matching desaparecidos <-> cadáveres
- [x] Matching desaparecidos <-> homicídios
- [x] Detecção de transtornos psiquiátricos
- [x] Unificação de registros
- [x] Validação com Pydantic
- [x] Relatórios estatísticos
- [x] CLI funcional
- [x] API Python
- [x] Exemplos de uso
- [x] Documentação completa

---

## 🎓 Princípios Éticos

O sistema segue rigorosamente:

1. **Nunca inventar dados**
2. **Nunca inferir raça, etnia ou orientação sem fonte**
3. **Sempre citar evidências textuais** (transtornos)
4. **Não alterar nomes originais**
5. **Usar null/IGN quando faltam dados**
6. **Ser auditável e reprodutível**

---

## 🔧 Customização

### Adicionar novos campos:
1. Edite `config/config.py` → `FIELD_MAPPING`

### Adicionar keywords de transtornos:
1. Edite `config/config.py` → `PSYCHIATRIC_KEYWORDS`

### Modificar classificações:
1. Edite `config/config.py` → Constantes `CLASSIFICACAO_*`

### Ajustar validações de matching:
1. Edite `etl/matching_engine.py` → Métodos de matching

---

## 📦 Dependências

```
pandas >= 1.5.0
pydantic >= 2.0.0
python-dateutil >= 2.8.0
```

Instale com:
```bash
pip install -r requirements.txt
```

---

## 🏆 Funcionalidades Avançadas

### 1. Matching Cascata
Sistema tenta match forte primeiro, depois moderado, depois fraco.
Evita duplicatas e conflitos.

### 2. Validação Cruzada
Valida sexo, idade e datas entre registros matchados.

### 3. Confiança Graduada
Cada match tem score de confiança (0.95, 0.75, 0.50).

### 4. Detecção Contextual
Extrai trechos do texto onde transtornos são mencionados.

### 5. Pipeline Modular
Cada etapa pode ser executada independentemente.

---

## 📞 Suporte

- Veja `README.md` para documentação completa
- Veja `docs/QUICKSTART.md` para início rápido
- Execute `python agente_correlacao.py --help` para ajuda CLI

---

## 🎉 Pronto para Uso!

O sistema está **100% funcional** e pronto para processar seus dados.

Execute agora:
```bash
cd correlation-project
python agente_correlacao.py "caminho/para/seu/arquivo.csv"
```

---

**Desenvolvido com IA: GitHub Copilot + Claude Sonnet 4.5**  
**Data:** 23 de novembro de 2025
