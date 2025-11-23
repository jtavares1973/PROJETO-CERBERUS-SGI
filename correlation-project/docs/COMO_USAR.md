# Como Usar o Sistema de Validação

## 📋 Visão Geral

Este sistema valida correlações entre boletins de **desaparecimento** e **morte/cadáver** usando inteligência artificial local (Ollama).

**Objetivo**: Confirmar se os dois BOs referem-se à **mesma pessoa**.

---

## 🎯 Fluxo de Trabalho

```
1. Preparação
   ↓
2. Execução da Validação (17-20 min)
   ↓
3. Monitoramento (opcional)
   ↓
4. Análise de Resultados
```

---

## 🚀 Passo a Passo

### **1. Preparação**

#### 1.1 Instalar Ollama

Windows/Mac:
```bash
# Baixar de: https://ollama.ai
```

Linux:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### 1.2 Baixar Modelo

```bash
# Modelo português otimizado (recomendado)
ollama pull qwen2.5-ptbr:7b

# Verificar instalação
ollama list
```

Você deve ver algo como:
```
NAME                    ID              SIZE
qwen2.5-ptbr:7b        abc123def456    4.7GB
```

#### 1.3 Verificar Dados de Entrada

Certifique-se que existe:
```
output/correlacoes_unicas_deduplicadas.xlsx
```

Com a aba: **"FORTES - Únicas"** (86 casos)

---

### **2. Executar Validação**

#### Opção A: Uma Janela (simples)

```bash
cd correlation-project
python scripts/validar_com_ia.py
```

**Saída esperada**:
```
====================================================================
VALIDAÇÃO DE CORRELAÇÕES COM IA
Modelo: qwen2.5-ptbr:7b | Temperatura: 0.1
====================================================================

[1/4] Verificando modelo qwen2.5-ptbr:7b... ✓
[2/4] Carregando output/correlacoes_unicas_deduplicadas.xlsx... ✓ (86 casos)
[3/4] Verificando progresso anterior... ✓ (iniciando do zero)
[4/4] Iniciando validações...
====================================================================

[1/86] ADAO FERREIRA DE SOUSA
   BO: 2024_08DP_5392 → 2024_01DP_3877
   Intervalo: 1 dias
   Validando com IA... ✓ CONFIRMADA (90%) [2.3s]

[2/86] AELCIO DA SILVA SANTOS
   BO: 2024_06DP_2154 → 2024_16DP_4621
   Intervalo: 1 dias
   Validando com IA... ✗ REJEITADA (85%) [1.8s]

...
```

#### Opção B: Duas Janelas (com monitoramento)

**Terminal 1** (validação):
```bash
cd correlation-project
python scripts/validar_com_ia.py
```

**Terminal 2** (monitor):
```bash
cd correlation-project
python scripts/monitor_progresso.py
```

**Monitor mostra**:
```
============================================================
VALIDAÇÃO IA - PROGRESSO
============================================================

12/86 casos (14.0%)
[███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]

✓ Confirmados: 10
✗ Rejeitados:  2
📊 Confiança:  92%
⏱ Restam:      ~14.8 min

Último: ✓ ALEX SANDRO DA SILVA

[11:25:33] Ctrl+C para sair
============================================================
```

---

### **3. Acompanhar Progresso**

#### Progresso Salvo Automaticamente

O script salva após **cada caso validado**. Se travar ou você interromper:

```bash
# Apenas execute novamente
python scripts/validar_com_ia.py
```

Ele **retoma de onde parou** automaticamente! ✅

#### Ver Status Rápido

```bash
python -c "import pandas as pd; df = pd.read_excel('output/validacao_progresso.xlsx'); print(f'{df[\"ia_validado\"].sum()}/86 validados')"
```

---

### **4. Ver Resultados**

Quando concluir, abra:

```
output/RELATORIO_VALIDACAO_FINAL.xlsx
```

**3 Abas**:

1. **Casos Confirmados**: Apenas os confirmados pela IA
2. **Todos os Casos**: Todos (confirmados + rejeitados)
3. **Estatísticas**: Resumo geral

**Colunas importantes**:
- `ia_mesma_pessoa`: True/False
- `ia_confianca`: 0-100%
- `ia_justificativa`: Explicação da IA
- `dias_entre_eventos`: Tempo entre desaparecimento e morte

---

## ⚙️ Configurações Avançadas

Edite `scripts/validar_com_ia.py`:

```python
# Linha 35-40

MODELO = 'qwen2.5-ptbr:7b'    # Modelo a usar
TEMPERATURA = 0.1             # 0.1 = determinístico, 1.0 = criativo
TIMEOUT = 60                  # Segundos por caso
```

### Modelos Alternativos

```bash
# Menor e mais rápido (menos preciso)
ollama pull qwen2:1.5b
MODELO = 'qwen2:1.5b'

# Maior e mais preciso (mais lento)
ollama pull qwen2.5:14b
MODELO = 'qwen2.5:14b'
```

---

## 📊 Resultados Esperados

| Métrica | Valor Esperado |
|---------|----------------|
| Total de casos | 86 |
| Taxa de confirmação | ~75-85% |
| Confiança média | ~88-95% |
| Tempo total | 17-20 min |
| Erros esperados | 0-2 casos |

---

## ⚠️ Troubleshooting

### Problema: "Modelo não encontrado"

**Solução**:
```bash
ollama list  # Ver modelos instalados
ollama pull qwen2.5-ptbr:7b  # Instalar
```

### Problema: Validação trava

**Causas comuns**:
- GPU sem VRAM suficiente
- Ollama travou
- Timeout muito curto

**Solução**:
```bash
# 1. Reinicie Ollama
ollama serve

# 2. Use modelo menor
ollama pull qwen2:1.5b

# 3. Aumente timeout em validar_com_ia.py
TIMEOUT = 120  # 2 minutos
```

### Problema: Caracteres estranhos no terminal

**Causa**: Encoding UTF-8

**Solução**: Script novo já corrige isso! Use:
```bash
python scripts/validar_com_ia.py
```

### Problema: Script muito lento

**Solução**:
```python
# Em validar_com_ia.py, reduza histórico:

# Linha ~135 e ~150
{caso['historico_desaparecimento'][:500]}  # Era 800
{caso['historico_morte'][:500]}  # Era 800
```

---

## 📈 Análise dos Resultados

### Taxa de Confirmação

- **80-90%**: Excelente! Correlações de alta qualidade
- **60-80%**: Bom, mas revisar rejeições manualmente
- **<60%**: Problema nos dados ou modelo inadequado

### Confiança Média

- **>90%**: IA muito confiante (bom sinal)
- **70-90%**: Normal, revisar casos de baixa confiança
- **<70%**: Modelo pode estar inadequado

### Casos para Revisar Manualmente

Filtrar no Excel:
1. `ia_mesma_pessoa = False` E `ia_confianca < 80%`
2. `ia_mesma_pessoa = True` E `ia_confianca < 70%`

---

## 🔄 Reprocessar Casos

Se quiser validar novamente do zero:

```bash
# Apagar progresso anterior
rm output/validacao_progresso.xlsx

# Executar novamente
python scripts/validar_com_ia.py
```

---

## 📚 Mais Informações

- **Arquitetura do Sistema**: Ver `docs/ARQUITETURA.md`
- **Código Fonte**: Ver `scripts/validar_com_ia.py`
- **Dados**: Ver `output/correlacoes_unicas_deduplicadas.xlsx`

---

## 💡 Dicas Profissionais

1. **Use duas janelas**: Uma para validação, outra para monitor
2. **Não interrompa manualmente**: Deixe concluir (salva progresso de qualquer forma)
3. **Revise manualmente**: Casos com confiança <75%
4. **Documente mudanças**: Se alterar prompt ou modelo
5. **Backup dos resultados**: Copie `RELATORIO_VALIDACAO_FINAL.xlsx` antes de reprocessar

---

## 🆘 Suporte

Problemas não resolvidos? Verifique:

1. ✅ Ollama rodando: `ollama list`
2. ✅ Modelo instalado: `ollama pull qwen2.5-ptbr:7b`
3. ✅ Arquivo entrada existe: `output/correlacoes_unicas_deduplicadas.xlsx`
4. ✅ Python 3.8+: `python --version`
5. ✅ Dependências: `pip install pandas openpyxl ollama`

---

**Última atualização**: 2025-01-23
