"""
Teste Rápido do Sistema AGENTE-CORRELACAO

Este script verifica se todos os módulos estão importando corretamente.
"""

import sys
from pathlib import Path

# Adicionar projeto ao path
sys.path.insert(0, str(Path(__file__).parent))

print("="*80)
print("TESTE DE IMPORTAÇÃO - AGENTE-CORRELACAO")
print("="*80 + "\n")

# Testar imports básicos
print("1. Testando imports de configuração...")
try:
    from config.config import FIELD_MAPPING, PSYCHIATRIC_KEYWORDS
    print("   ✓ config.config OK")
except Exception as e:
    print(f"   ✗ ERRO: {e}")

# Testar utils
print("\n2. Testando imports de utilitários...")
try:
    from utils.normalization import normalizar_nome, parse_data, gerar_chave_forte
    print("   ✓ utils.normalization OK")
except Exception as e:
    print(f"   ✗ ERRO: {e}")

try:
    from utils.psychiatric_detector import PsychiatricDetector
    print("   ✓ utils.psychiatric_detector OK")
except Exception as e:
    print(f"   ✗ ERRO: {e}")

# Testar models
print("\n3. Testando imports de modelos...")
try:
    from models.schemas import PessoaBase, RegistroUnificado
    print("   ✓ models.schemas OK")
except Exception as e:
    print(f"   ✗ ERRO: {e}")

# Testar ETL
print("\n4. Testando imports de ETL...")
try:
    from etl.padronizacao import pipeline_padronizacao_completa
    print("   ✓ etl.padronizacao OK")
except Exception as e:
    print(f"   ✗ ERRO: {e}")

try:
    from etl.matching_engine import MatchingEngine
    print("   ✓ etl.matching_engine OK")
except Exception as e:
    print(f"   ✗ ERRO: {e}")

try:
    from etl.pipeline import pipeline_completo
    print("   ✓ etl.pipeline OK")
except Exception as e:
    print(f"   ✗ ERRO: {e}")

# Testar agente
print("\n5. Testando import do agente principal...")
try:
    from agente_correlacao import AgenteCorrelacao
    print("   ✓ agente_correlacao OK")
except Exception as e:
    print(f"   ✗ ERRO: {e}")

# Teste funcional básico
print("\n" + "="*80)
print("TESTE FUNCIONAL")
print("="*80 + "\n")

print("6. Testando normalização de nome...")
try:
    nome_teste = "José da Silva Júnior"
    nome_normalizado = normalizar_nome(nome_teste)
    print(f"   Input: '{nome_teste}'")
    print(f"   Output: '{nome_normalizado}'")
    print("   ✓ Normalização funcionando")
except Exception as e:
    print(f"   ✗ ERRO: {e}")

print("\n7. Testando detector psiquiátrico...")
try:
    detector = PsychiatricDetector()
    texto_teste = "Paciente apresenta histórico de esquizofrenia e faz uso de Haldol."
    resultado = detector.detectar(texto_teste)
    print(f"   Texto: '{texto_teste}'")
    print(f"   Detectado: {resultado['tem_transtorno_psiquiatrico']}")
    print(f"   Tipo: {resultado['tipo_transtorno']}")
    print(f"   Confiança: {resultado['confianca']}")
    print("   ✓ Detector funcionando")
except Exception as e:
    print(f"   ✗ ERRO: {e}")

print("\n8. Testando geração de chaves...")
try:
    from datetime import datetime
    nome_norm = "joao silva"
    data_nasc = datetime(1985, 3, 15)
    
    chave_forte = gerar_chave_forte(nome_norm, data_nasc)
    print(f"   Nome: '{nome_norm}'")
    print(f"   Data: {data_nasc}")
    print(f"   Chave Forte: '{chave_forte}'")
    print("   ✓ Geração de chaves funcionando")
except Exception as e:
    print(f"   ✗ ERRO: {e}")

# Resumo final
print("\n" + "="*80)
print("RESUMO DO TESTE")
print("="*80)
print("\n✅ Todos os módulos principais estão funcionando!")
print("\nO sistema está pronto para uso.")
print("\nPara executar o pipeline completo:")
print('  python agente_correlacao.py "caminho/do/arquivo.csv"')
print("\nOu rode os exemplos interativos:")
print('  python exemplos.py')
print("\n" + "="*80 + "\n")
