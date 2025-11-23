# 🚀 Setup em Outro PC - Guia Completo

## Pré-requisitos

- **Git**: https://git-scm.com/download/win
- **Python 3.11+**: https://www.python.org/downloads/
- **Ollama**: https://ollama.ai/download

---

## Passo 1: Clonar o Repositório

```bash
# Abrir terminal (Git Bash ou PowerShell)
cd D:/___MeusScripts/

# Clonar repositório
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git

# Entrar na pasta
cd SEU_REPOSITORIO
```

---

## Passo 2: Instalar Dependências Python

```bash
# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# Windows PowerShell:
venv\Scripts\Activate.ps1

# Windows CMD:
venv\Scripts\activate.bat

# Git Bash:
source venv/Scripts/activate

# Instalar dependências
pip install -r requirements.txt
```

---

## Passo 3: Configurar Ollama

```bash
# Verificar instalação
ollama --version

# Baixar modelo português (7B - rápido)
ollama pull qwen2.5-ptbr:7b

# OU modelo menor (1.5B - mais rápido, menos preciso)
ollama pull qwen2:1.5b

# OU modelo maior (14B - mais lento, mais preciso)
ollama pull qwen2.5:14b

# Verificar modelos instalados
ollama list
```

**Modelos disponíveis:**
- `qwen2.5-ptbr:7b` (4.7GB) - **RECOMENDADO** - Português, rápido, 84% confiança
- `qwen2:1.5b` (934MB) - Muito rápido, menor precisão
- `qwen2.5:14b` (9.3GB) - Mais preciso, mais lento

---

## Passo 4: Copiar Dados (NÃO ESTÃO NO GIT)

⚠️ **IMPORTANTE**: Dados CSV/Excel não sobem para GitHub (são sensíveis)

Você precisa copiar manualmente do PC original:

```
Copiar do PC original:
├── Dados-homi-desaperecido.csv  (arquivo original)
└── output/
    ├── correlacoes_unicas_deduplicadas.xlsx
    └── validacao_progresso.xlsx (se quiser continuar validação)
```

Formas de transferir:
- Pen drive / HD externo
- OneDrive / Google Drive
- Email (se arquivo for pequeno)
- Rede local (compartilhamento Windows)

---

## Passo 5: Configurar Validação

```bash
# Configurar modelo, temperatura, prompt
python scripts/configurar_validacao.py

# Escolher opções:
# 1 - Modelo (qwen2.5-ptbr:7b recomendado)
# 2 - Temperatura (0.1 para determinismo)
# 3 - Timeout (60s padrão)
# 4-7 - Detalhes do prompt
# 9 - Salvar configuração
```

---

## Passo 6: Executar Projeto

### Opção A: Script Automático (Windows)

```bash
# Duplo clique em:
iniciar.bat

# Ou via terminal:
./iniciar.bat
```

### Opção B: Manual

```bash
# Terminal 1 - Validação
python archive/old_scripts/EXECUTAR_VALIDACAO.py

# Terminal 2 - Monitor (opcional)
python scripts/monitor_progresso.py
```

---

## Estrutura Esperada Após Setup

```
SEU_REPOSITORIO/
├── .gitignore                    ✅ Excluir dados sensíveis
├── requirements.txt              ✅ Dependências Python
├── README.md                     ✅ Documentação principal
├── LEIA-ME-PRIMEIRO.txt         ✅ Guia inicial
├── INICIAR_AQUI.md              ✅ Quick start
├── iniciar.bat / iniciar.sh     ✅ Launchers
├── config_validacao.json        ⚠️  Criar com configurar_validacao.py
├── Dados-homi-desaperecido.csv  ❌ COPIAR MANUALMENTE
├── scripts/
│   ├── configurar_validacao.py  ✅ No Git
│   ├── monitor_progresso.py     ✅ No Git
│   └── organizar_projeto.py     ✅ No Git
├── archive/
│   └── old_scripts/
│       └── EXECUTAR_VALIDACAO.py ✅ Script principal (funcional)
├── docs/
│   ├── COMO_USAR.md             ✅ No Git
│   ├── ARQUITETURA.md           ✅ No Git
│   └── ESTRUTURA_FINAL.md       ✅ No Git
├── output/                       📁 Pasta vazia no Git
│   ├── .gitkeep                 ✅ Mantém estrutura
│   └── *.xlsx                   ❌ COPIAR MANUALMENTE (se necessário)
└── utils/
    ├── chaves.py                ✅ No Git
    └── __init__.py              ✅ No Git
```

**Legenda:**
- ✅ Está no Git (será clonado automaticamente)
- ❌ NÃO está no Git (copiar manualmente)
- ⚠️ Precisa criar/configurar
- 📁 Pasta vazia (estrutura mantida)

---

## Verificação Final

```bash
# 1. Verificar Python
python --version
# Esperado: Python 3.11 ou superior

# 2. Verificar dependências
pip list | grep -E "pandas|openpyxl|ollama"
# Esperado: pandas 2.2.0, openpyxl 3.1.2, ollama 0.4.4

# 3. Verificar Ollama
ollama list
# Esperado: qwen2.5-ptbr:7b ou outro modelo

# 4. Verificar dados
ls Dados-*.csv
# Esperado: Dados-homi-desaperecido.csv

# 5. Verificar configuração
cat config_validacao.json
# Esperado: JSON com modelo, temperatura, etc.
```

---

## Problemas Comuns

### 1. "comando não encontrado: git"
**Solução**: Instalar Git - https://git-scm.com/download/win

### 2. "comando não encontrado: python"
**Solução**: Instalar Python - https://www.python.org/downloads/
- ✅ Marcar "Add Python to PATH" durante instalação

### 3. "comando não encontrado: ollama"
**Solução**: Instalar Ollama - https://ollama.ai/download
- Reiniciar terminal após instalação

### 4. "FileNotFoundError: Dados-homi-desaperecido.csv"
**Solução**: Copiar arquivo CSV do PC original

### 5. "ModuleNotFoundError: pandas"
**Solução**: `pip install -r requirements.txt`

### 6. "ollama.ResponseError: model not found"
**Solução**: `ollama pull qwen2.5-ptbr:7b`

### 7. Timeout na validação (máquina mais lenta)
**Solução**: 
```bash
python scripts/configurar_validacao.py
# Opção 3 - Aumentar timeout para 120s
```

---

## Sincronização Entre PCs

### No PC Original (após fazer mudanças):

```bash
# 1. Ver o que mudou
git status

# 2. Adicionar mudanças
git add .

# 3. Commitar com mensagem descritiva
git commit -m "Validação: processados mais 20 casos"

# 4. Enviar para GitHub
git push origin main
```

### No PC Novo (para receber mudanças):

```bash
# 1. Baixar mudanças
git pull origin main

# 2. Copiar dados atualizados (se necessário)
# Copiar output/validacao_progresso.xlsx do PC original
```

---

## Comandos Git Úteis

```bash
# Ver histórico de commits
git log --oneline

# Ver mudanças não commitadas
git diff

# Descartar mudanças locais
git checkout -- arquivo.py

# Atualizar do GitHub
git pull

# Enviar para GitHub
git push

# Ver branch atual
git branch

# Criar novo branch (para testes)
git checkout -b testes

# Voltar para branch main
git checkout main
```

---

## Performance - Tempo Estimado por PC

| Hardware | Modelo | Tempo/caso | 86 casos |
|----------|--------|------------|----------|
| **Ryzen 9 7950X + RTX 5070 Ti** | qwen2.5-ptbr:7b | 0.2 min | ~17 min |
| Ryzen 5 5600 + RTX 3060 | qwen2.5-ptbr:7b | 0.4 min | ~34 min |
| Ryzen 5 5600 + RTX 3060 | qwen2:1.5b | 0.2 min | ~17 min |
| Intel i5 + Sem GPU | qwen2:1.5b | 1.0 min | ~86 min |

**Recomendações:**
- GPU NVIDIA: Usar qwen2.5-ptbr:7b (melhor qualidade)
- CPU apenas: Usar qwen2:1.5b (mais rápido)
- Máquina lenta: Aumentar timeout para 120s

---

## Próximos Passos

1. ✅ Clonar repositório
2. ✅ Instalar Python + dependências
3. ✅ Instalar Ollama + modelo
4. ✅ Copiar dados (CSV/Excel)
5. ✅ Configurar validação
6. ✅ Executar `iniciar.bat`
7. 📊 Analisar resultados em `output/RELATORIO_VALIDACAO_FINAL.xlsx`

---

## Contato / Dúvidas

- 📁 Documentação: `docs/COMO_USAR.md`
- 🏗️ Arquitetura: `docs/ARQUITETURA.md`
- 📋 Quick start: `INICIAR_AQUI.md`

**Status Atual do Projeto:**
- ✅ 86/86 casos validados
- ✅ 69 confirmados (80.2%)
- ✅ 17 rejeitados (19.8%)
- ✅ 84% confiança média
- ✅ 0 erros
