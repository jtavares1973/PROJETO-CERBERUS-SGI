"""
═══════════════════════════════════════════════════════════════════════════════
CONFIGURADOR INTERATIVO DE VALIDAÇÃO
═══════════════════════════════════════════════════════════════════════════════

Interface simples para ajustar:
- Modelo de IA (qwen2.5-ptbr:7b, qwen2:1.5b, etc)
- Temperatura (0.0 - 1.0)
- Timeout por caso
- Tamanho do histórico no prompt

Salva em: config_validacao.json
Usado por: EXECUTAR_VALIDACAO.py

═══════════════════════════════════════════════════════════════════════════════
"""

import json
import os
from pathlib import Path


ARQUIVO_CONFIG = 'config_validacao.json'

CONFIG_PADRAO = {
    'modelo': 'qwen2.5-ptbr:7b',
    'temperatura': 0.1,
    'timeout_segundos': 60,
    'tamanho_historico': 800,
    'prompt_detalhes': {
        'incluir_transtorno': True,
        'incluir_rg': True,
        'incluir_pais': True,
        'formato_visual': True
    }
}


def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def carregar_config():
    """Carrega configuração existente ou cria padrão"""
    if Path(ARQUIVO_CONFIG).exists():
        with open(ARQUIVO_CONFIG, 'r', encoding='utf-8') as f:
            return json.load(f)
    return CONFIG_PADRAO.copy()


def salvar_config(config):
    """Salva configuração em JSON"""
    with open(ARQUIVO_CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    print(f"\n✓ Configuracao salva em: {ARQUIVO_CONFIG}")


def mostrar_config_atual(config):
    """Mostra configuração atual"""
    print("\n" + "=" * 70)
    print("CONFIGURACAO ATUAL")
    print("=" * 70)
    print(f"\n1. Modelo: {config['modelo']}")
    print(f"2. Temperatura: {config['temperatura']}")
    print(f"3. Timeout: {config['timeout_segundos']}s")
    print(f"4. Tamanho historico: {config['tamanho_historico']} caracteres")
    print("\nDetalhes do Prompt:")
    print(f"   - Incluir transtorno: {config['prompt_detalhes']['incluir_transtorno']}")
    print(f"   - Incluir RG: {config['prompt_detalhes']['incluir_rg']}")
    print(f"   - Incluir pais (mae/pai): {config['prompt_detalhes']['incluir_pais']}")
    print(f"   - Formato visual: {config['prompt_detalhes']['formato_visual']}")


def menu_modelo():
    """Menu para escolher modelo"""
    print("\n" + "=" * 70)
    print("ESCOLHER MODELO")
    print("=" * 70)
    print("\n1. qwen2.5-ptbr:7b  (Recomendado - Portugues, 4.7GB)")
    print("2. qwen2:1.5b       (Rapido - Pequeno, 1.5GB)")
    print("3. qwen2.5:14b      (Preciso - Grande, 9GB)")
    print("4. Outro (digitar nome)")
    print("0. Voltar")
    
    opcao = input("\nEscolha: ").strip()
    
    if opcao == '1':
        return 'qwen2.5-ptbr:7b'
    elif opcao == '2':
        return 'qwen2:1.5b'
    elif opcao == '3':
        return 'qwen2.5:14b'
    elif opcao == '4':
        modelo = input("\nDigite o nome do modelo: ").strip()
        return modelo if modelo else None
    return None


def menu_temperatura():
    """Menu para ajustar temperatura"""
    print("\n" + "=" * 70)
    print("AJUSTAR TEMPERATURA")
    print("=" * 70)
    print("\nTemperatura controla criatividade vs determinismo:")
    print("  0.0 - Muito deterministico (sempre mesma resposta)")
    print("  0.1 - Recomendado para validacao (preciso)")
    print("  0.5 - Balanceado")
    print("  1.0 - Muito criativo (variacoes)")
    
    try:
        temp = float(input("\nDigite temperatura (0.0 - 1.0): ").strip())
        if 0.0 <= temp <= 1.0:
            return temp
        print("Valor invalido! Usando 0.1")
        return 0.1
    except:
        print("Valor invalido! Usando 0.1")
        return 0.1


def menu_timeout():
    """Menu para ajustar timeout"""
    print("\n" + "=" * 70)
    print("AJUSTAR TIMEOUT")
    print("=" * 70)
    print("\nTempo maximo por caso (segundos):")
    print("  30  - Rapido (pode falhar em casos complexos)")
    print("  60  - Recomendado (balanceado)")
    print("  120 - Conservador (para modelos lentos)")
    
    try:
        timeout = int(input("\nDigite timeout (segundos): ").strip())
        if timeout > 0:
            return timeout
        print("Valor invalido! Usando 60")
        return 60
    except:
        print("Valor invalido! Usando 60")
        return 60


def menu_historico():
    """Menu para ajustar tamanho do histórico"""
    print("\n" + "=" * 70)
    print("AJUSTAR TAMANHO DO HISTORICO")
    print("=" * 70)
    print("\nQuantos caracteres incluir de cada historico:")
    print("  500  - Rapido (menos contexto)")
    print("  800  - Recomendado (balanceado)")
    print("  1000 - Completo (mais lento)")
    
    try:
        tamanho = int(input("\nDigite tamanho: ").strip())
        if tamanho > 0:
            return tamanho
        print("Valor invalido! Usando 800")
        return 800
    except:
        print("Valor invalido! Usando 800")
        return 800


def menu_prompt_detalhes(config):
    """Menu para ajustar detalhes do prompt"""
    while True:
        print("\n" + "=" * 70)
        print("DETALHES DO PROMPT")
        print("=" * 70)
        print("\n1. Incluir transtorno psiquiatrico:", config['prompt_detalhes']['incluir_transtorno'])
        print("2. Incluir RG:", config['prompt_detalhes']['incluir_rg'])
        print("3. Incluir nomes dos pais:", config['prompt_detalhes']['incluir_pais'])
        print("4. Usar formato visual (separadores):", config['prompt_detalhes']['formato_visual'])
        print("\n0. Voltar")
        
        opcao = input("\nAlterar item (1-4) ou 0 para voltar: ").strip()
        
        if opcao == '0':
            break
        elif opcao == '1':
            config['prompt_detalhes']['incluir_transtorno'] = not config['prompt_detalhes']['incluir_transtorno']
        elif opcao == '2':
            config['prompt_detalhes']['incluir_rg'] = not config['prompt_detalhes']['incluir_rg']
        elif opcao == '3':
            config['prompt_detalhes']['incluir_pais'] = not config['prompt_detalhes']['incluir_pais']
        elif opcao == '4':
            config['prompt_detalhes']['formato_visual'] = not config['prompt_detalhes']['formato_visual']


def menu_principal():
    """Menu principal"""
    config = carregar_config()
    
    while True:
        limpar_tela()
        print("=" * 70)
        print("CONFIGURADOR DE VALIDACAO COM IA")
        print("=" * 70)
        
        mostrar_config_atual(config)
        
        print("\n" + "=" * 70)
        print("OPCOES")
        print("=" * 70)
        print("\n1. Alterar modelo")
        print("2. Ajustar temperatura")
        print("3. Ajustar timeout")
        print("4. Ajustar tamanho historico")
        print("5. Configurar detalhes do prompt")
        print("\n8. Restaurar configuracao padrao")
        print("9. Salvar e sair")
        print("0. Sair sem salvar")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == '0':
            print("\nSaindo sem salvar...")
            break
        
        elif opcao == '1':
            novo_modelo = menu_modelo()
            if novo_modelo:
                config['modelo'] = novo_modelo
                print(f"\n✓ Modelo alterado para: {novo_modelo}")
                input("\nPressione Enter para continuar...")
        
        elif opcao == '2':
            nova_temp = menu_temperatura()
            config['temperatura'] = nova_temp
            print(f"\n✓ Temperatura ajustada para: {nova_temp}")
            input("\nPressione Enter para continuar...")
        
        elif opcao == '3':
            novo_timeout = menu_timeout()
            config['timeout_segundos'] = novo_timeout
            print(f"\n✓ Timeout ajustado para: {novo_timeout}s")
            input("\nPressione Enter para continuar...")
        
        elif opcao == '4':
            novo_tamanho = menu_historico()
            config['tamanho_historico'] = novo_tamanho
            print(f"\n✓ Tamanho historico ajustado para: {novo_tamanho}")
            input("\nPressione Enter para continuar...")
        
        elif opcao == '5':
            menu_prompt_detalhes(config)
        
        elif opcao == '8':
            config = CONFIG_PADRAO.copy()
            print("\n✓ Configuracao restaurada para o padrao")
            input("\nPressione Enter para continuar...")
        
        elif opcao == '9':
            salvar_config(config)
            print("\n✓ Configuracao salva com sucesso!")
            print("\nPara usar: python archive/old_scripts/EXECUTAR_VALIDACAO.py")
            input("\nPressione Enter para sair...")
            break


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nOperacao cancelada pelo usuario.")
