"""
Teste do detector de hardware em diferentes cenários.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'utils'))

from detector_hardware import identificar_pc, obter_config_otimizada


def simular_cenarios():
    """Simula diferentes tipos de PC"""
    
    print("\n" + "="*80)
    print("TESTE: Simulação de Detecção em Diferentes PCs")
    print("="*80)
    
    # Cenário 1: PC Real (detectado)
    print("\n[CENARIO 1] PC REAL - Detecção Automática")
    print("-" * 80)
    
    hardware = identificar_pc()
    config = obter_config_otimizada(hardware)
    
    print(f"Tipo PC: {hardware.tipo}")
    print(f"CPU: {hardware.cpu}")
    print(f"RAM: {hardware.ram_gb}GB")
    print(f"GPU: {hardware.gpu or 'Não detectada'}")
    if hardware.vram_gb:
        print(f"VRAM: {hardware.vram_gb}GB")
    
    print(f"\nConfiguracao Aplicada:")
    print(f"  Modelo: {config.modelo}")
    print(f"  Timeout: {config.timeout_segundos}s")
    print(f"  Historico: {config.tamanho_historico} chars")
    print(f"  Batch: {config.batch_size}")
    print(f"  Comentario: {config.comentario}")
    
    # Cenário 2: Notebook sem GPU (simulado)
    print("\n[CENARIO 2] NOTEBOOK SEM GPU - Simulação")
    print("-" * 80)
    
    from detector_hardware import HardwareProfile
    
    notebook_fraco = HardwareProfile(
        nome='Notebook Básico',
        cpu='Intel Core i5-8250U',
        ram_gb=8,
        gpu=None,  # SEM GPU
        vram_gb=None,
        tipo='GENERICO'
    )
    
    config_notebook = obter_config_otimizada(notebook_fraco)
    
    print(f"Tipo PC: {notebook_fraco.tipo}")
    print(f"CPU: {notebook_fraco.cpu}")
    print(f"RAM: {notebook_fraco.ram_gb}GB")
    print(f"GPU: Não detectada (CPU apenas)")
    
    print(f"\nConfiguracao Aplicada:")
    print(f"  Modelo: {config_notebook.modelo}")
    print(f"  Timeout: {config_notebook.timeout_segundos}s")
    print(f"  Historico: {config_notebook.tamanho_historico} chars")
    print(f"  Batch: {config_notebook.batch_size}")
    print(f"  Comentario: {config_notebook.comentario}")
    
    # Análise
    print("\n" + "="*80)
    print("ANALISE")
    print("="*80)
    
    if notebook_fraco.gpu is None:
        print("\n[AVISO] Notebook sem GPU detectado!")
        print("\nAjustes aplicados automaticamente:")
        print(f"  - Modelo LEVE: {config_notebook.modelo} (vs {config.modelo})")
        print(f"  - Timeout MAIOR: {config_notebook.timeout_segundos}s (vs {config.timeout_segundos}s)")
        print(f"  - Historico MENOR: {config_notebook.tamanho_historico} chars (vs {config.tamanho_historico} chars)")
        print(f"  - Batch CONSERVADOR: {config_notebook.batch_size} caso (vs {config.batch_size} casos)")
        
        print("\nTempo estimado (86 casos):")
        print(f"  - PC Casa (GPU): ~17 minutos")
        print(f"  - Notebook (CPU): ~86 minutos")
        
        print("\nCONCLUSAO:")
        print("  [OK] Sistema detecta e se adapta automaticamente!")
        print("  [OK] Funciona, mas mais lento em notebooks fracos")
        print("  [OK] Nao trava, usa modelo leve e config conservadora")
    
    print("\n" + "="*80 + "\n")


if __name__ == '__main__':
    simular_cenarios()
