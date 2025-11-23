# COMO EXECUTAR A VALIDAÇÃO

## 🚀 EXECUÇÃO RÁPIDA

### 1. Inicie a validação (em background):
```bash
cd /d/___MeusScripts/LangChain/correlation-project
python EXECUTAR_VALIDACAO.py &
```

### 2. Veja o progresso em tempo real (em outra janela):
```bash
cd /d/___MeusScripts/LangChain/correlation-project
python VER_PROGRESSO.py
```

---

## 📊 O QUE VOCÊ VERÁ

O monitor mostra:
- **Barra de progresso visual** (█████░░░░░)
- **Estatísticas em tempo real**: confirmados, rejeitados, erros
- **Últimos 3 casos processados**
- **Confiança média**
- **Tempo estimado restante**

Atualiza **a cada 5 segundos** automaticamente.

---

## ⏱️ TEMPO ESPERADO

- **86 casos FORTES** × 0.2 min/caso = **~17-20 minutos**

---

## 📁 ARQUIVOS GERADOS

Durante execução:
- `output/validacao_progresso.xlsx` - Salvo após cada caso

Ao finalizar:
- `output/RELATORIO_VALIDACAO_FINAL.xlsx` - Relatório completo

---

## ❓ PROBLEMAS?

### Validação não inicia:
```bash
# Verifica se Ollama está rodando
ollama list

# Se não estiver, inicie:
ollama serve
```

### Quer recomeçar do zero:
```bash
# Remove arquivo de progresso
rm output/validacao_progresso.xlsx

# Executa novamente
python EXECUTAR_VALIDACAO.py
```

### Quer retomar validação interrompida:
```bash
# Apenas execute novamente - ele retoma automaticamente
python EXECUTAR_VALIDACAO.py
```

---

## 🎯 RESULTADO FINAL

Ao concluir, você terá:

1. **RELATORIO_VALIDACAO_FINAL.xlsx** com 3 abas:
   - **Casos Confirmados** (ordenados por intervalo)
   - **Todos os Casos** (completo)
   - **Estatísticas** (resumo)

2. Estatísticas esperadas:
   - ~70-75 confirmados (~80-85%)
   - ~10-15 rejeitados
   - Confiança média: ~90-95%

---

## 📖 DOCUMENTAÇÃO COMPLETA

Veja `ARQUITETURA.md` para entender toda a estrutura do sistema.
