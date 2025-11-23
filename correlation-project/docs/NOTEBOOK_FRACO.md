# ⚠️ Rodando em Notebook Fraco (Sem GPU)

## O que acontece?

Quando você abre o projeto em um **notebook sem GPU** ou com **hardware limitado**, o sistema detecta automaticamente e faz os seguintes ajustes:

---

## Detecção Automática

```bash
$ python utils/detector_hardware.py

======================================================================
DETECCAO AUTOMATICA DE HARDWARE
======================================================================

[INFO] Hardware Detectado:
   Tipo: GENERICO
   CPU: Intel Core i5-8250U
   RAM: 8 GB
   GPU: Nao detectada (CPU apenas)

[CONFIG] Configuracao Otimizada:
   Modelo: qwen2:1.5b          # ← MODELO LEVE (934MB)
   Temperatura: 0.1
   Timeout: 90s                 # ← TIMEOUT LONGO
   Historico: 500 chars         # ← MENOS CONTEXTO
   Batch size: 1 caso(s)        # ← UM POR VEZ
   => PC Genérico - Modo conservador

[ATENCAO] Hardware limitado detectado!
   - Usando modelo LEVE: qwen2:1.5b
   - Processamento mais LENTO esperado
   - Tempo estimado: ~86 minutos para 86 casos
   - Sistema funcionara, mas pode demorar

[INFO] GPU nao detectada - Usando CPU
   - Ollama rodara em CPU (mais lento)
   - Considere usar modelo ainda menor se travar:
     ollama pull qwen2:0.5b
======================================================================
```

---

## Ajustes Aplicados

### 1. Modelo Ultra-Leve

| PC | Modelo | Tamanho | Velocidade |
|----|--------|---------|------------|
| **Casa** (RTX 5070 Ti) | qwen2.5-ptbr:7b | 4.7GB | ⚡⚡⚡⚡⚡ |
| **Trabalho** (RTX 5070) | qwen2.5-ptbr:7b | 4.7GB | ⚡⚡⚡⚡ |
| **Notebook** (CPU) | qwen2:1.5b | 934MB | ⚡⚡ |

### 2. Timeout Aumentado

- **PC Casa**: 45s (resposta rápida)
- **PC Trabalho**: 60s (segurança)
- **Notebook**: 90s (muito mais tempo para CPU)

### 3. Menos Contexto

- **PC Casa**: 1000 chars (histórico completo)
- **PC Trabalho**: 800 chars (padrão)
- **Notebook**: 500 chars (essencial apenas)

### 4. Sem Paralelismo

- **PC Casa**: 3 casos simultâneos
- **PC Trabalho**: 2 casos simultâneos
- **Notebook**: 1 caso por vez (não sobrecarrega)

---

## Comparação de Performance

### Validação de 86 Casos

| Hardware | Tempo | Confiança | Status |
|----------|-------|-----------|--------|
| **PC Casa** (Ryzen 9 + RTX 5070 Ti 16GB) | ~17 min | 84% | ⚡ RÁPIDO |
| **PC Trabalho** (i9 + RTX 5070 12GB) | ~25 min | 84% | ✅ BOM |
| **Notebook** (i5 + 8GB + CPU) | ~86 min | 75% | 🐌 LENTO MAS FUNCIONA |

---

## Exemplo Real - Notebook Fraco

```bash
# No notebook sem GPU
$ python scripts/validar_com_deteccao_auto.py

================================================================================
VALIDACAO COM IA - DETECCAO AUTOMATICA DE HARDWARE
================================================================================

======================================================================
DETECCAO AUTOMATICA DE HARDWARE
======================================================================

[INFO] Hardware Detectado:
   Tipo: GENERICO
   CPU: Intel Core i5-8250U
   RAM: 8 GB
   GPU: Nao detectada (CPU apenas)

[CONFIG] Configuracao Otimizada:
   Modelo: qwen2:1.5b
   Temperatura: 0.1
   Timeout: 90s
   Historico: 500 chars
   Batch size: 1 caso(s)
   => PC Genérico - Modo conservador

[ATENCAO] Hardware limitado detectado!
   - Usando modelo LEVE: qwen2:1.5b
   - Processamento mais LENTO esperado
   - Tempo estimado: ~86 minutos para 86 casos
   - Sistema funcionara, mas pode demorar

[INFO] GPU nao detectada - Usando CPU
   - Ollama rodara em CPU (mais lento)
======================================================================

[OK] Configuracao carregada: config_validacao.json

[CONFIG] Configuracao Ativa:
   Modelo: qwen2:1.5b           # ← LEVE
   Temperatura: 0.1
   Timeout: 90s                 # ← MAIOR
   Historico: 500 chars         # ← MENOR
   Batch size: 1                # ← SEM PARALELISMO

[OK] 86 casos carregados

[EXEC] Processando 86 casos pendentes...

[1/86] ADAO FERREIRA... [+] CONFIRMADA (85%)    # Demora ~60s
[2/86] ALAILSON CORREA... [+] CONFIRMADA (80%)  # Demora ~60s
[3/86] ALEX SANDRO... [+] CONFIRMADA (82%)      # Demora ~60s
...

# LENTO, MAS FUNCIONA!
```

---

## O Sistema NÃO Trava! ✅

### Proteções Implementadas

1. **Timeout Alto (90s)**
   - CPU tem tempo suficiente para processar
   - Não gera timeout error

2. **Modelo Pequeno (1.5B)**
   - Cabe na RAM (apenas 1GB)
   - Resposta rápida mesmo em CPU

3. **Um Caso por Vez**
   - Não sobrecarrega memória
   - Processamento estável

4. **Contexto Reduzido**
   - Menos tokens para processar
   - Resposta mais rápida

---

## Se Ainda Assim Estiver Lento

### Opção 1: Modelo Ainda Menor

```bash
# Instalar modelo ultra-leve (0.5B)
ollama pull qwen2:0.5b

# Editar config_validacao.json manualmente
{
    "modelo": "qwen2:0.5b",      # ← MENOR
    "temperatura": 0.1,
    "timeout_segundos": 120,      # ← MAIS TEMPO
    "tamanho_historico": 300,     # ← MENOS CONTEXTO
    "batch_size": 1
}
```

### Opção 2: Processar Menos Casos

```python
# Editar script para processar apenas alguns casos
pendentes = pendentes[:10]  # Processar apenas 10 casos para teste
```

### Opção 3: Usar GPU Externa (Google Colab)

```bash
# No Google Colab (GPU grátis)
!git clone https://github.com/jtavares1973/PROJETO-CERBERUS-SGI.git
%cd PROJETO-CERBERUS-SGI

# Instalar Ollama
!curl -fsSL https://ollama.com/install.sh | sh

# Rodar normalmente
!python scripts/validar_com_deteccao_auto.py
# Detecta GPU do Colab automaticamente!
```

---

## Resumo: O Que Esperar

### ✅ FUNCIONA

- ✅ Sistema detecta automaticamente
- ✅ Aplica config conservadora
- ✅ Roda sem travar
- ✅ Gera resultados válidos

### ⚠️ LIMITAÇÕES

- 🐌 **MUITO mais lento** (~86 min vs ~17 min)
- 📉 **Confiança menor** (75% vs 84%)
- 💻 **CPU 100%** durante processamento
- 🔋 **Bateria drena rápido** (se notebook)

### 💡 RECOMENDAÇÃO

Se você tem:
- **PC Casa/Trabalho com GPU**: Use lá (muito mais rápido)
- **Notebook fraco**: Funciona, mas deixe processando e vá fazer café ☕
- **Pressa**: Use Google Colab (GPU grátis)

---

## Mensagens de Erro Comuns

### "Out of memory"

**Causa**: RAM insuficiente para modelo.

**Solução**:
```bash
# Usar modelo menor
ollama pull qwen2:0.5b
# Editar config_validacao.json
```

### "Timeout exceeded"

**Causa**: CPU muito lenta, não processa em 90s.

**Solução**:
```json
{
    "timeout_segundos": 180  // Aumentar para 3 minutos
}
```

### "Connection refused"

**Causa**: Ollama não está rodando.

**Solução**:
```bash
# Iniciar Ollama
ollama serve
```

---

## Conclusão

**SIM, funciona em notebook fraco!**

- ✅ Sistema se adapta automaticamente
- ✅ Usa modelo leve (1.5B)
- ✅ Timeout longo (90s)
- ✅ Processamento conservador
- ⚠️ MAS: É **5x mais lento**

**Melhor estratégia:**
1. Testar com 5-10 casos primeiro
2. Se funcionar bem, processar todos
3. Deixar rodando de noite/fim de semana

**Não precisa se preocupar - o sistema cuida de tudo automaticamente!** 🚀
