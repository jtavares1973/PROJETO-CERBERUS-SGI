#!/bin/bash
#
# INICIO RÁPIDO - Validação com IA
#
# Este script facilita a execução da validação abrindo 2 terminais:
#   Terminal 1: Validação com IA
#   Terminal 2: Monitor de progresso
#

echo "════════════════════════════════════════════════════════════════"
echo "VALIDAÇÃO COM IA - INÍCIO RÁPIDO"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Abrindo 2 terminais:"
echo "  Terminal 1: Validação com IA"
echo "  Terminal 2: Monitor de progresso"
echo ""

# Verifica se está no diretório correto
if [ ! -f "scripts/validar_com_ia.py" ]; then
    echo "❌ ERRO: Execute este script da pasta correlation-project/"
    exit 1
fi

# Verifica Python
if ! command -v python &> /dev/null; then
    echo "❌ ERRO: Python não encontrado"
    exit 1
fi

# Verifica Ollama
if ! command -v ollama &> /dev/null; then
    echo "❌ ERRO: Ollama não instalado"
    echo "   Instale em: https://ollama.ai"
    exit 1
fi

# Verifica modelo
if ! ollama list | grep -q "qwen2.5-ptbr:7b"; then
    echo "⚠️  Modelo qwen2.5-ptbr:7b não encontrado"
    echo ""
    read -p "Deseja instalar agora? (s/n): " resposta
    if [ "$resposta" = "s" ]; then
        echo "Instalando modelo (4.7GB)..."
        ollama pull qwen2.5-ptbr:7b
    else
        echo "❌ Modelo necessário para continuar"
        exit 1
    fi
fi

echo ""
echo "✅ Pré-requisitos OK!"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "INICIANDO..."
echo "════════════════════════════════════════════════════════════════"
echo ""

# Terminal 1: Validação (background)
echo "Terminal 1: Validação com IA"
python scripts/validar_com_ia.py &
PID_VALIDACAO=$!

# Aguarda 2 segundos
sleep 2

# Terminal 2: Monitor
echo "Terminal 2: Monitor de progresso"
echo ""
echo "(Pressione Ctrl+C para sair do monitor)"
echo ""
python scripts/monitor_progresso.py

# Quando monitor fechar, validação continua
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "Monitor encerrado. Validação continua rodando (PID: $PID_VALIDACAO)"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Para ver status:"
echo "  python scripts/monitor_progresso.py"
echo ""
echo "Para parar validação:"
echo "  kill $PID_VALIDACAO"
echo ""
