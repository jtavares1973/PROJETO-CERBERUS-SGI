# Projeto de Correlação Desaparecimento → Morte

## 🎯 Objetivo

Validar correlações entre boletins de desaparecimento e morte usando inteligência artificial local (Ollama).

## 📁 Estrutura do Projeto

```
correlation-project/
├── scripts/              # Scripts principais
│   ├── validar_com_ia.py      # Validação com IA
│   └── monitor_progresso.py   # Monitor em tempo real
├── output/               # Resultados
│   ├── correlacoes_unicas_deduplicadas.xlsx
│   ├── validacao_progresso.xlsx
│   └── RELATORIO_VALIDACAO_FINAL.xlsx
├── docs/                 # Documentação
│   ├── ARQUITETURA.md         # Arquitetura completa do sistema
│   └── COMO_USAR.md           # Guia de uso detalhado
└── archive/              # Arquivos antigos
```

## 🚀 Como Usar

### 1. Pré-requisitos

```bash
# Instalar Ollama
https://ollama.ai

# Baixar modelo português
ollama pull qwen2.5-ptbr:7b

# Verificar instalação
ollama list
```

### 2. Executar Validação

```bash
# Terminal 1: Rodar validação
python3 scripts/validar_com_ia.py

# Terminal 2: Monitorar progresso (opcional)
python3 scripts/monitor_progresso.py
```

### 3. Ver Resultados

Após conclusão, abrir: `output/RELATORIO_VALIDACAO_FINAL.xlsx`

## ⚙️ Configurações

Edite `scripts/validar_com_ia.py`:

- `MODELO`: Modelo a usar (padrão: qwen2.5-ptbr:7b)
- `TEMPERATURA`: 0.1 (mais determinístico) a 1.0 (mais criativo)
- `TIMEOUT`: Tempo máximo por caso (padrão: 60s)

## 📊 Dados

- **Entrada**: 86 casos FORTES (0-30 dias entre eventos)
- **Saída**: ~68-70 confirmações esperadas (80% taxa)
- **Tempo**: ~17-20 minutos total

## 📖 Documentação Completa

Ver: `docs/ARQUITETURA.md` e `docs/COMO_USAR.md`

## ⚠️ Troubleshooting

**Problema**: Validação trava

**Solução**: Script salva progresso automaticamente. Apenas execute novamente:
```bash
python3 scripts/validar_com_ia.py
```

**Problema**: Modelo muito lento

**Solução**: Use modelo menor (7B em vez de 14B)

## 🔧 Manutenção

Para reorganizar arquivos temporários:
```bash
python3 scripts/organizar_projeto.py
```
