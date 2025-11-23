#!/bin/bash
# Script de setup do ambiente CERBERUS

echo "🔧 Configurando ambiente CERBERUS..."

# Verifica se Python 3.10+ está instalado
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Cria ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativa ambiente virtual
echo "🔌 Ativando ambiente virtual..."
source venv/bin/activate

# Instala dependências
echo "📥 Instalando dependências..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "✅ Setup completo!"
echo ""
echo "Para ativar o ambiente, execute:"
echo "  source venv/bin/activate"
echo ""
echo "Para testar o sistema, execute:"
echo "  PYTHONPATH=. python scripts/test_normalization.py"
echo "  PYTHONPATH=. python scripts/test_matching.py"
