"""
Detector automático de hardware para otimização de configuração.

Este módulo detecta as especificações do PC (CPU, GPU, RAM) e retorna
perfil de configuração otimizado para validação com IA.

Suporta:
- PC CASA: Ryzen 9 7950X + RTX 5070 Ti 16GB + 64GB DDR5
- PC TRABALHO: i9-12900HK + RTX 5070 12GB + 32GB DDR4
"""

import platform
import subprocess
import psutil
import json
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class HardwareProfile:
    """Perfil de hardware detectado"""
    nome: str
    cpu: str
    ram_gb: int
    gpu: Optional[str]
    vram_gb: Optional[int]
    tipo: str  # 'CASA' ou 'TRABALHO'
    
    def __str__(self):
        gpu_info = f"{self.gpu} ({self.vram_gb}GB)" if self.gpu else "CPU apenas"
        return f"{self.nome}: {self.cpu} | {self.ram_gb}GB RAM | {gpu_info}"


@dataclass
class ConfigProfile:
    """Perfil de configuração para validação IA"""
    modelo: str
    temperatura: float
    timeout_segundos: int
    tamanho_historico: int
    batch_size: int  # Quantos casos processar em paralelo
    comentario: str
    
    def to_dict(self):
        return {
            'modelo': self.modelo,
            'temperatura': self.temperatura,
            'timeout_segundos': self.timeout_segundos,
            'tamanho_historico': self.tamanho_historico,
            'batch_size': self.batch_size,
            'prompt_detalhes': {
                'incluir_transtorno': True,
                'incluir_rg': True,
                'incluir_pais': True,
                'formato_visual': True
            }
        }


def detectar_cpu() -> str:
    """Detecta modelo da CPU"""
    try:
        if platform.system() == 'Windows':
            # Tenta múltiplos métodos no Windows
            try:
                # Método 1: PowerShell
                output = subprocess.check_output(
                    'powershell "Get-WmiObject -Class Win32_Processor | Select-Object -ExpandProperty Name"',
                    shell=True,
                    text=True,
                    stderr=subprocess.DEVNULL
                )
                cpu = output.strip()
                if cpu and 'AMD' in cpu or 'Intel' in cpu:
                    return cpu
            except:
                pass
            
            # Método 2: wmic (fallback)
            try:
                output = subprocess.check_output(
                    'wmic cpu get name',
                    shell=True,
                    text=True,
                    stderr=subprocess.DEVNULL
                )
                cpu = output.split('\n')[1].strip()
                if cpu:
                    return cpu
            except:
                pass
        else:
            output = subprocess.check_output(
                'lscpu | grep "Model name"',
                shell=True,
                text=True
            )
            cpu = output.split(':')[1].strip()
            return cpu
        
    except:
        pass
    
    # Fallback para detecção genérica
    return platform.processor()


def detectar_ram_gb() -> int:
    """Detecta quantidade de RAM em GB"""
    try:
        return round(psutil.virtual_memory().total / (1024**3))
    except:
        return 0


def detectar_gpu() -> tuple[Optional[str], Optional[int]]:
    """Detecta GPU NVIDIA e VRAM"""
    try:
        if platform.system() == 'Windows':
            # Tenta nvidia-smi
            output = subprocess.check_output(
                'nvidia-smi --query-gpu=name,memory.total --format=csv,noheader',
                shell=True,
                text=True,
                stderr=subprocess.DEVNULL
            )
            
            linha = output.strip().split(',')
            gpu_nome = linha[0].strip()
            vram_mb = int(linha[1].strip().split()[0])
            vram_gb = round(vram_mb / 1024)
            
            return gpu_nome, vram_gb
        else:
            # Linux
            output = subprocess.check_output(
                'nvidia-smi --query-gpu=name,memory.total --format=csv,noheader',
                shell=True,
                text=True,
                stderr=subprocess.DEVNULL
            )
            
            linha = output.strip().split(',')
            gpu_nome = linha[0].strip()
            vram_mb = int(linha[1].strip().split()[0])
            vram_gb = round(vram_mb / 1024)
            
            return gpu_nome, vram_gb
    except:
        return None, None


def identificar_pc() -> HardwareProfile:
    """Identifica perfil de hardware do PC atual"""
    cpu = detectar_cpu()
    ram_gb = detectar_ram_gb()
    gpu, vram_gb = detectar_gpu()
    
    # Identificar tipo de PC baseado nas specs
    if '7950X' in cpu or ram_gb >= 60:
        # PC CASA: Ryzen 9 7950X + 64GB DDR5
        tipo = 'CASA'
        nome = 'PC Casa (High-End)'
    elif 'i9' in cpu or '12900' in cpu:
        # PC TRABALHO: i9-12900HK + 32GB DDR4
        tipo = 'TRABALHO'
        nome = 'PC Trabalho (Mid-High)'
    else:
        # PC desconhecido - usar perfil conservador
        tipo = 'GENERICO'
        nome = 'PC Genérico'
    
    return HardwareProfile(
        nome=nome,
        cpu=cpu,
        ram_gb=ram_gb,
        gpu=gpu,
        vram_gb=vram_gb,
        tipo=tipo
    )


def obter_config_otimizada(hardware: HardwareProfile) -> ConfigProfile:
    """Retorna configuração otimizada baseada no hardware"""
    
    if hardware.tipo == 'CASA':
        # PC CASA: Ryzen 9 7950X + RTX 5070 Ti 16GB + 64GB RAM
        # Configuração AGRESSIVA - máxima performance
        return ConfigProfile(
            modelo='qwen2.5-ptbr:7b',  # Modelo completo, rápido
            temperatura=0.1,            # Determinístico
            timeout_segundos=45,        # Timeout curto (é rápido)
            tamanho_historico=1000,     # Mais contexto
            batch_size=3,               # Pode processar múltiplos casos
            comentario='PC Casa - Performance máxima (Ryzen 9 7950X + RTX 5070 Ti 16GB)'
        )
    
    elif hardware.tipo == 'TRABALHO':
        # PC TRABALHO: i9-12900HK + RTX 5070 12GB + 32GB RAM
        # Configuração BALANCEADA - boa performance, mais conservador
        return ConfigProfile(
            modelo='qwen2.5-ptbr:7b',  # Mesmo modelo, funciona bem
            temperatura=0.1,            # Determinístico
            timeout_segundos=60,        # Timeout padrão
            tamanho_historico=800,      # Contexto padrão
            batch_size=2,               # Mais conservador
            comentario='PC Trabalho - Performance balanceada (i9-12900HK + RTX 5070 12GB)'
        )
    
    else:
        # PC GENÉRICO - configuração CONSERVADORA
        return ConfigProfile(
            modelo='qwen2:1.5b',        # Modelo menor, mais rápido
            temperatura=0.1,
            timeout_segundos=90,        # Timeout longo por segurança
            tamanho_historico=500,      # Menos contexto
            batch_size=1,               # Um caso por vez
            comentario='PC Genérico - Modo conservador'
        )


def salvar_config_auto(config: ConfigProfile, arquivo: str = 'config_validacao.json'):
    """Salva configuração automática em arquivo JSON"""
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(config.to_dict(), f, indent=4, ensure_ascii=False)


def detectar_e_configurar(verbose: bool = True) -> tuple[HardwareProfile, ConfigProfile]:
    """
    Detecta hardware e retorna configuração otimizada.
    
    Args:
        verbose: Se True, imprime informações na tela
        
    Returns:
        Tupla (hardware_profile, config_profile)
    """
    # Detectar hardware
    hardware = identificar_pc()
    
    # Obter configuração otimizada
    config = obter_config_otimizada(hardware)
    
    if verbose:
        print("\n" + "="*70)
        print("DETECCAO AUTOMATICA DE HARDWARE")
        print("="*70)
        print(f"\n[INFO] Hardware Detectado:")
        print(f"   Tipo: {hardware.tipo}")
        print(f"   CPU: {hardware.cpu}")
        print(f"   RAM: {hardware.ram_gb} GB")
        if hardware.gpu:
            print(f"   GPU: {hardware.gpu} ({hardware.vram_gb} GB)")
        else:
            print(f"   GPU: Nao detectada (CPU apenas)")
        
        print(f"\n[CONFIG] Configuracao Otimizada:")
        print(f"   Modelo: {config.modelo}")
        print(f"   Temperatura: {config.temperatura}")
        print(f"   Timeout: {config.timeout_segundos}s")
        print(f"   Historico: {config.tamanho_historico} chars")
        print(f"   Batch size: {config.batch_size} caso(s)")
        print(f"   => {config.comentario}")
        
        # Avisos baseados no hardware
        if hardware.tipo == 'GENERICO':
            print(f"\n[ATENCAO] Hardware limitado detectado!")
            print(f"   - Usando modelo LEVE: {config.modelo}")
            print(f"   - Processamento mais LENTO esperado")
            print(f"   - Tempo estimado: ~86 minutos para 86 casos")
            print(f"   - Sistema funcionara, mas pode demorar")
            
            if not hardware.gpu:
                print(f"\n[INFO] GPU nao detectada - Usando CPU")
                print(f"   - Ollama rodara em CPU (mais lento)")
                print(f"   - Considere usar modelo ainda menor se travar:")
                print(f"     ollama pull qwen2:0.5b")
        
        elif hardware.tipo == 'TRABALHO':
            print(f"\n[OK] Hardware adequado - Performance balanceada")
            print(f"   - Tempo estimado: ~25 minutos para 86 casos")
        
        elif hardware.tipo == 'CASA':
            print(f"\n[EXCELENTE] Hardware de alta performance!")
            print(f"   - Tempo estimado: ~17 minutos para 86 casos")
            print(f"   - Processamento paralelo ativado (batch {config.batch_size})")
        
        print("="*70 + "\n")
    
    return hardware, config


def criar_config_automatica():
    """Cria config_validacao.json automaticamente baseado no hardware"""
    hardware, config = detectar_e_configurar(verbose=True)
    
    # Salvar configuração
    salvar_config_auto(config)
    
    print("✅ Configuração salva em: config_validacao.json")
    print(f"   Perfil: {hardware.tipo}")
    print(f"   Modelo: {config.modelo}")
    print()


if __name__ == '__main__':
    # Teste do detector
    criar_config_automatica()
