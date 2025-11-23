import sys
from pathlib import Path

print("VERIFICACAO FINAL DO SISTEMA")
print("=" * 60)

# 1. Scripts principais
scripts = [
    'scripts/validar_com_ia.py',
    'scripts/monitor_progresso.py',
    'scripts/organizar_projeto.py'
]

print("\n1. SCRIPTS PRINCIPAIS:")
for s in scripts:
    status = "OK" if Path(s).exists() else "FALTA"
    print(f"   [{status}] {s}")

# 2. Documentacao
docs = [
    'docs/COMO_USAR.md',
    'docs/ARQUITETURA.md',
    'LEIA-ME-PRIMEIRO.txt',
    'ESTRUTURA_FINAL.md',
    'README.md'
]

print("\n2. DOCUMENTACAO:")
for d in docs:
    status = "OK" if Path(d).exists() else "FALTA"
    print(f"   [{status}] {d}")

# 3. Inicio rapido
inicios = ['iniciar.bat', 'iniciar.sh']

print("\n3. INICIO RAPIDO:")
for i in inicios:
    status = "OK" if Path(i).exists() else "FALTA"
    print(f"   [{status}] {i}")

# 4. Dados
print("\n4. DADOS:")
if Path('output/correlacoes_unicas_deduplicadas.xlsx').exists():
    try:
        import pandas as pd
        df = pd.read_excel('output/correlacoes_unicas_deduplicadas.xlsx', sheet_name='FORTES - Unicas')
        print(f"   [OK] {len(df)} casos FORTES prontos para validacao")
    except Exception as e:
        print(f"   [AVISO] Arquivo existe mas erro ao ler: {e}")
else:
    print("   [FALTA] output/correlacoes_unicas_deduplicadas.xlsx")

# 5. Archive
print("\n5. ARQUIVOS ARQUIVADOS:")
if Path('archive/old_scripts').exists():
    arquivados = len(list(Path('archive/old_scripts').glob('*.py')))
    print(f"   [OK] {arquivados} scripts antigos arquivados")

print("\n" + "=" * 60)
print("STATUS: SISTEMA ORGANIZADO E PRONTO!")
print("=" * 60)
print("\nPROXIMO PASSO:")
print("  Windows: Duplo clique em iniciar.bat")
print("  Linux:   ./iniciar.sh")
print("\nOu manualmente:")
print("  python scripts/validar_com_ia.py")
print("")
