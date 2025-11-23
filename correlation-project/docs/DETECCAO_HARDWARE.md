# 🖥️ Detecção Automática de Hardware

## O que é?

Sistema que detecta automaticamente as especificações do seu PC e ajusta a configuração da validação IA para máxima performance.

**Não precisa mais editar configs manualmente quando trocar de PC!**

---

## Hardware Suportado

### PC CASA (High-End)
- **CPU**: AMD Ryzen 9 7950X (16-Core)
- **RAM**: 64GB DDR5
- **GPU**: NVIDIA RTX 5070 Ti (16GB VRAM)
- **SSD**: NVMe 2TB

**Configuração Automática:**
- Modelo: `qwen2.5-ptbr:7b` (4.7GB)
- Timeout: 45 segundos (processamento rápido)
- Histórico: 1000 caracteres (mais contexto)
- Batch size: 3 casos simultâneos
- Tempo estimado: ~17 minutos para 86 casos

### PC TRABALHO (Mid-High)
- **CPU**: Intel i9-12900HK (20 threads)
- **RAM**: 32GB DDR4
- **GPU**: NVIDIA RTX 5070 (12GB VRAM)
- **SSD**: NVMe 1TB (7000MB/s)

**Configuração Automática:**
- Modelo: `qwen2.5-ptbr:7b` (4.7GB)
- Timeout: 60 segundos (segurança extra)
- Histórico: 800 caracteres (padrão)
- Batch size: 2 casos simultâneos
- Tempo estimado: ~25 minutos para 86 casos

### PC GENÉRICO (Fallback)
Qualquer outro PC não identificado.

**Configuração Automática:**
- Modelo: `qwen2:1.5b` (934MB - mais leve)
- Timeout: 90 segundos
- Histórico: 500 caracteres
- Batch size: 1 caso por vez
- Modo conservador para compatibilidade

---

## Como Usar

### Opção 1: Automático (Recomendado)

```bash
# Executar script com detecção automática
python scripts/validar_com_deteccao_auto.py
```

**O que acontece:**
1. Detecta CPU, GPU, RAM automaticamente
2. Identifica se é PC CASA, TRABALHO ou GENÉRICO
3. Aplica configuração otimizada
4. Inicia validação

### Opção 2: Criar Config Manualmente

```bash
# Criar config_validacao.json baseado no hardware
cd utils
python detector_hardware.py
```

**Output:**
```
======================================================================
🔍 DETECÇÃO AUTOMÁTICA DE HARDWARE
======================================================================

📊 Hardware Detectado:
   Tipo: CASA
   CPU: AMD Ryzen 9 7950X 16-Core Processor
   RAM: 63 GB
   GPU: NVIDIA GeForce RTX 5070 Ti (16 GB)

⚙️  Configuração Otimizada:
   Modelo: qwen2.5-ptbr:7b
   Temperatura: 0.1
   Timeout: 45s
   Histórico: 1000 chars
   Batch size: 3 casos
   💬 PC Casa - Performance máxima (Ryzen 9 7950X + RTX 5070 Ti 16GB)
======================================================================

✅ Configuração salva em: config_validacao.json
```

### Opção 3: Config Manual (se preferir)

```bash
# Usar interface de configuração manual
python scripts/configurar_validacao.py
```

---

## Comparação de Performance

| PC | Modelo | Tempo/caso | 86 casos | Confiança |
|----|--------|------------|----------|-----------|
| **CASA (Ryzen 9 7950X + RTX 5070 Ti 16GB)** | qwen2.5-ptbr:7b | 0.2 min | **~17 min** | 84% |
| **TRABALHO (i9-12900HK + RTX 5070 12GB)** | qwen2.5-ptbr:7b | 0.3 min | **~25 min** | 84% |
| GENÉRICO (CPU apenas) | qwen2:1.5b | 1.0 min | ~86 min | 75% |

---

## Detalhes Técnicos

### Detecção de Hardware

O sistema detecta:

1. **CPU**: Via PowerShell (Windows) ou lscpu (Linux)
2. **RAM**: Total de memória física
3. **GPU**: Via nvidia-smi (NVIDIA GPUs)
4. **VRAM**: Memória da GPU

### Identificação do PC

```python
# Lógica de identificação
if '7950X' in cpu or ram_gb >= 60:
    tipo = 'CASA'  # Ryzen 9 7950X + 64GB
elif 'i9' in cpu or '12900' in cpu:
    tipo = 'TRABALHO'  # i9-12900HK
else:
    tipo = 'GENERICO'  # Outros PCs
```

### Arquivos Criados

- `config_validacao.json`: Configuração ativa
- `utils/detector_hardware.py`: Módulo de detecção
- `scripts/validar_com_deteccao_auto.py`: Script principal

---

## Vantagens

### ✅ Automático
- Detecta PC automaticamente
- Zero configuração manual
- Funciona em qualquer PC

### ✅ Otimizado
- Usa recursos máximos de cada PC
- Ajusta timeout baseado em performance
- Batch processing quando possível

### ✅ Portável
- Mesmo código funciona em todos os PCs
- Commit único no Git
- Clone e execute

### ✅ Inteligente
- Modelo leve em PCs fracos
- Modelo completo em PCs fortes
- Fallback seguro se detecção falhar

---

## Troubleshooting

### "Detector de hardware não disponível"

**Causa**: Módulo `detector_hardware.py` não encontrado.

**Solução**:
```bash
# Verificar estrutura
ls utils/detector_hardware.py  # Deve existir

# Se não existir, copiar do GitHub
git pull origin main
```

### "nvidia-smi não encontrado"

**Causa**: GPU NVIDIA não instalada ou drivers ausentes.

**Solução**: Sistema usa modo CPU (funcional, mais lento).

### Detecção errada do PC

**Solução Manual**:
```bash
# Editar config_validacao.json manualmente
{
    "modelo": "qwen2.5-ptbr:7b",
    "temperatura": 0.1,
    "timeout_segundos": 60,
    "tamanho_historico": 800,
    "batch_size": 1
}
```

---

## Integração com GitHub

### Commit das mudanças

```bash
git add utils/detector_hardware.py
git add scripts/validar_com_deteccao_auto.py
git add docs/DETECCAO_HARDWARE.md
git commit -m "feat: Detecção automática de hardware para otimização por PC"
git push
```

### No outro PC

```bash
git pull
python scripts/validar_com_deteccao_auto.py
# Detecta novo PC automaticamente!
```

---

## Exemplo de Uso

```bash
$ python scripts/validar_com_deteccao_auto.py

================================================================================
VALIDACAO COM IA - DETECCAO AUTOMATICA DE HARDWARE
================================================================================

======================================================================
🔍 DETECÇÃO AUTOMÁTICA DE HARDWARE
======================================================================

📊 Hardware Detectado:
   Tipo: TRABALHO
   CPU: Intel Core i9-12900HK
   RAM: 32 GB
   GPU: NVIDIA GeForce RTX 5070 (12 GB)

⚙️  Configuração Otimizada:
   Modelo: qwen2.5-ptbr:7b
   Temperatura: 0.1
   Timeout: 60s
   Histórico: 800 chars
   Batch size: 2 casos
   💬 PC Trabalho - Performance balanceada (i9-12900HK + RTX 5070 12GB)
======================================================================

[OK] Configuracao carregada: config_validacao.json

[CONFIG] Configuracao Ativa:
   Modelo: qwen2.5-ptbr:7b
   Temperatura: 0.1
   Timeout: 60s
   Historico: 800 chars
   Batch size: 2

[OK] 86 casos carregados

[EXEC] Processando 86 casos pendentes...

[1/86] ADAO FERREIRA... [+] CONFIRMADA (90%)
[2/86] ALAILSON CORREA... [+] CONFIRMADA (85%)
[3/86] ALEX SANDRO... [+] CONFIRMADA (88%)
...
```

---

## Resumo

✅ **Detecta automaticamente** qual PC você está usando  
✅ **Aplica configuração otimizada** para cada máquina  
✅ **Performance máxima** em cada ambiente  
✅ **Zero configuração manual** necessária  
✅ **Funciona em qualquer PC** (com fallback inteligente)

**Troque de PC sem preocupação - o sistema se adapta automaticamente!** 🚀
