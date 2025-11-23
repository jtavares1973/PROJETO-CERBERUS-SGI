"""
VISUALIZADOR DE PROGRESSO DA VALIDACAO
Mostra em tempo real o status da validacao enquanto ela roda
"""

import pandas as pd
import time
from pathlib import Path
from datetime import datetime
import os


def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_progresso():
    """Mostra progresso da validacao em tempo real"""
    
    arquivo = Path('output/validacao_progresso.xlsx')
    
    print("=" * 80)
    print("MONITOR DE PROGRESSO DA VALIDACAO")
    print("=" * 80)
    print("\nPressione Ctrl+C para sair")
    print("\nAtualizando a cada 5 segundos...\n")
    
    ultima_atualizacao = None
    
    try:
        while True:
            if not arquivo.exists():
                print("\n[AGUARDANDO] Arquivo de progresso ainda nao existe...")
                print("             A validacao ainda nao iniciou ou esta nos primeiros casos")
                time.sleep(5)
                continue
            
            # Le arquivo
            try:
                df = pd.read_excel(arquivo)
            except Exception as e:
                print(f"\n[ERRO] Nao foi possivel ler arquivo: {e}")
                time.sleep(5)
                continue
            
            # Calcula estatisticas
            total = len(df)
            validados = df['ia_validado'].notna().sum()
            confirmados = (df['ia_mesma_pessoa'] == True).sum()
            rejeitados = (df['ia_mesma_pessoa'] == False).sum()
            erros = df['ia_erro'].notna().sum()
            
            # Limpa tela e mostra info atualizada
            limpar_tela()
            
            print("=" * 80)
            print("MONITOR DE PROGRESSO DA VALIDACAO IA")
            print("=" * 80)
            
            # Barra de progresso
            progresso_pct = (validados / total * 100) if total > 0 else 0
            barra_tamanho = 50
            barra_completa = int(barra_tamanho * validados / total) if total > 0 else 0
            barra = "█" * barra_completa + "░" * (barra_tamanho - barra_completa)
            
            print(f"\n[PROGRESSO] {validados}/{total} casos validados ({progresso_pct:.1f}%)")
            print(f"[{barra}]")
            
            # Estatisticas
            print(f"\n[RESULTADOS]")
            print(f"  Confirmados: {confirmados} ({confirmados/validados*100:.1f}% dos validados)" if validados > 0 else "  Confirmados: 0")
            print(f"  Rejeitados:  {rejeitados} ({rejeitados/validados*100:.1f}% dos validados)" if validados > 0 else "  Rejeitados: 0")
            print(f"  Erros:       {erros}")
            
            # Ultimo caso processado
            if validados > 0:
                ultimos = df[df['ia_validado'].notna()].tail(3)
                print(f"\n[ULTIMOS CASOS PROCESSADOS]")
                for idx, caso in ultimos.iterrows():
                    status = "OK - CONFIRMADA" if caso['ia_mesma_pessoa'] else "REJEITADA"
                    if pd.notna(caso['ia_erro']):
                        status = f"ERRO: {caso['ia_erro'][:40]}"
                    
                    print(f"  • {caso['nome'][:40]}")
                    print(f"    {caso['bo_desaparecimento']} → {caso['bo_morte']} ({caso['dias_entre_eventos']} dias)")
                    print(f"    Status: {status}")
                    if pd.notna(caso.get('ia_confianca')):
                        print(f"    Confianca: {caso['ia_confianca']:.0f}%")
                    print()
            
            # Confianca media
            if confirmados > 0:
                conf_media = df[df['ia_mesma_pessoa'] == True]['ia_confianca'].mean()
                print(f"[CONFIANCA MEDIA] {conf_media:.1f}% (casos confirmados)")
            
            # Tempo estimado
            if validados > 0 and validados < total:
                # Estima baseado em 0.2 min/caso
                restantes = total - validados
                tempo_estimado = restantes * 0.2
                print(f"\n[TEMPO ESTIMADO] ~{tempo_estimado:.1f} minutos restantes")
            
            # Status
            print(f"\n[STATUS] ", end="")
            if validados == total:
                print("VALIDACAO CONCLUIDA!")
                print("\nExecute: python EXECUTAR_VALIDACAO.py para ver relatorio final")
                break
            else:
                print("Validacao em andamento...")
            
            # Info de atualizacao
            agora = datetime.now().strftime("%H:%M:%S")
            print(f"\n[ATUALIZADO] {agora}")
            print("\nPressione Ctrl+C para sair (a validacao continuara rodando)")
            print("=" * 80)
            
            # Aguarda 5 segundos
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\n[SAINDO] Monitor encerrado")
        print("         A validacao continua rodando em background")


if __name__ == "__main__":
    mostrar_progresso()
