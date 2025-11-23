"""
Exemplo de Uso do AGENTE-CORRELACAO

Este script demonstra como usar o agente programaticamente
para correlacionar dados de desaparecidos com mortes.
"""

import sys
from pathlib import Path

# Adicionar projeto ao path
sys.path.insert(0, str(Path(__file__).parent))

from agente_correlacao import AgenteCorrelacao


def exemplo_basico():
    """Exemplo mais simples possível"""
    print("\n" + "="*80)
    print("EXEMPLO 1: Uso Básico")
    print("="*80 + "\n")
    
    agente = AgenteCorrelacao(verbose=True)
    
    # Executar pipeline completo
    df_resultado = agente.executar_pipeline_completo(
        caminho_csv=r"d:\___MeusScripts\LangChain\Dados-homi-desaperecido.csv",
        output_path="output/exemplo_basico.csv"
    )
    
    print("\n✅ Processamento concluído!")
    print(f"📊 Total de registros: {len(df_resultado) if df_resultado is not None else 0}")


def exemplo_etapa_por_etapa():
    """Exemplo com controle fino de cada etapa"""
    print("\n" + "="*80)
    print("EXEMPLO 2: Etapa por Etapa")
    print("="*80 + "\n")
    
    agente = AgenteCorrelacao(verbose=True)
    
    # Executar passo a passo
    agente.executar_etapa_por_etapa(
        caminho_csv=r"d:\___MeusScripts\LangChain\Dados-homi-desaperecido.csv"
    )
    
    # Salvar resultado
    agente.salvar_resultado("output/exemplo_etapas.csv")
    
    # Gerar relatório
    relatorio = agente.gerar_relatorio()
    print("\n📋 Relatório JSON:")
    import json
    print(json.dumps(relatorio, indent=2, ensure_ascii=False))


def exemplo_analise_transtornos():
    """Exemplo focado em análise de transtornos psiquiátricos"""
    print("\n" + "="*80)
    print("EXEMPLO 3: Análise de Transtornos Psiquiátricos")
    print("="*80 + "\n")
    
    agente = AgenteCorrelacao(verbose=False)  # Modo silencioso
    
    # Executar pipeline
    agente.executar_etapa_por_etapa(
        caminho_csv=r"d:\___MeusScripts\LangChain\Dados-homi-desaperecido.csv"
    )
    
    # Filtrar casos com transtornos
    if agente.df_final is not None:
        casos_com_transtorno = agente.df_final[
            agente.df_final['tem_transtorno_psiquiatrico'] == True
        ]
        
        print(f"\n🧠 Casos com transtornos detectados: {len(casos_com_transtorno)}")
        
        if len(casos_com_transtorno) > 0:
            print("\n📋 Primeiros 5 casos:")
            print(casos_com_transtorno[[
                'nome', 
                'tipo_transtorno', 
                'confianca_transtorno',
                'classificacao_final'
            ]].head())
            
            # Salvar apenas casos com transtornos
            casos_com_transtorno.to_csv(
                "output/casos_com_transtornos.csv",
                index=False,
                sep=';',
                encoding='utf-8-sig'
            )
            print("\n✅ Casos salvos em: output/casos_com_transtornos.csv")


def exemplo_analise_matches():
    """Exemplo focado em análise de matches"""
    print("\n" + "="*80)
    print("EXEMPLO 4: Análise de Matches")
    print("="*80 + "\n")
    
    agente = AgenteCorrelacao(verbose=False)
    
    agente.executar_etapa_por_etapa(
        caminho_csv=r"d:\___MeusScripts\LangChain\Dados-homi-desaperecido.csv"
    )
    
    if agente.df_final is not None:
        # Filtrar apenas registros com match
        tem_match_cad = agente.df_final.get('match_forte_cad', False) | \
                       agente.df_final.get('match_moderado_cad', False) | \
                       agente.df_final.get('match_fraco_cad', False)
        
        tem_match_hom = agente.df_final.get('match_forte_hom', False) | \
                       agente.df_final.get('match_moderado_hom', False) | \
                       agente.df_final.get('match_fraco_hom', False)
        
        casos_com_match = agente.df_final[tem_match_cad | tem_match_hom]
        
        print(f"\n🔗 Casos correlacionados: {len(casos_com_match)}")
        
        if len(casos_com_match) > 0:
            print("\n📋 Distribuição por tipo de match:")
            print(casos_com_match['fonte_match'].value_counts())
            
            # Salvar
            casos_com_match.to_csv(
                "output/casos_correlacionados.csv",
                index=False,
                sep=';',
                encoding='utf-8-sig'
            )
            print("\n✅ Casos salvos em: output/casos_correlacionados.csv")


def menu():
    """Menu interativo"""
    print("\n" + "="*80)
    print("EXEMPLOS DE USO DO AGENTE-CORRELACAO")
    print("="*80)
    print("\n1. Uso Básico (pipeline completo)")
    print("2. Etapa por Etapa (controle fino)")
    print("3. Análise de Transtornos Psiquiátricos")
    print("4. Análise de Matches e Correlações")
    print("5. Executar TODOS os exemplos")
    print("0. Sair")
    
    escolha = input("\nEscolha uma opção: ")
    
    return escolha


if __name__ == "__main__":
    # Criar diretório de output
    Path("output").mkdir(exist_ok=True)
    
    # Menu interativo
    while True:
        escolha = menu()
        
        if escolha == "1":
            exemplo_basico()
        elif escolha == "2":
            exemplo_etapa_por_etapa()
        elif escolha == "3":
            exemplo_analise_transtornos()
        elif escolha == "4":
            exemplo_analise_matches()
        elif escolha == "5":
            exemplo_basico()
            exemplo_etapa_por_etapa()
            exemplo_analise_transtornos()
            exemplo_analise_matches()
        elif escolha == "0":
            print("\n👋 Até logo!")
            break
        else:
            print("\n❌ Opção inválida!")
        
        input("\n\nPressione ENTER para continuar...")
