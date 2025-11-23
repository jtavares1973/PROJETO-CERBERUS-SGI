"""
═══════════════════════════════════════════════════════════════════════════════
MONITOR DE PROGRESSO DA VALIDAÇÃO
═══════════════════════════════════════════════════════════════════════════════

DESCRIÇÃO:
    Monitor visual LIMPO e SIMPLES do progresso da validação com IA.
    Atualiza a cada 5 segundos automaticamente.

USO:
    python scripts/monitor_progresso.py
    
    (Pressione Ctrl+C para sair - a validação continua rodando)

═══════════════════════════════════════════════════════════════════════════════
"""

import pandas as pd
import time
import os
from pathlib import Path
from datetime import datetime


ARQUIVO_PROGRESSO = 'output/validacao_progresso.xlsx'
TOTAL_CASOS = 86
INTERVALO_ATUALIZACAO = 5  # segundos


def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_progresso():
    """Exibe progresso em tempo real"""
    
    arquivo = Path(ARQUIVO_PROGRESSO)
    
    try:
        while True:
            limpar_tela()
            
            # Verifica se arquivo existe
            if not arquivo.exists():
                print("=" * 60)
                print("AGUARDANDO VALIDAÇÃO INICIAR...")
                print("=" * 60)
                print("\n⏳ Arquivo de progresso ainda não existe")
                print("   Execute: python scripts/validar_com_ia.py")
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}]")
                time.sleep(INTERVALO_ATUALIZACAO)
                continue
            
            # Lê progresso
            try:
                df = pd.read_excel(arquivo)
            except Exception as e:
                print(f"⚠ Erro ao ler arquivo: {e}")
                time.sleep(INTERVALO_ATUALIZACAO)
                continue
            
            # Calcula estatísticas
            validados = int(df['ia_validado'].sum())
            confirmados = int((df['ia_mesma_pessoa'] == True).sum())
            rejeitados = int((df['ia_mesma_pessoa'] == False).sum())
            erros = int(df['ia_erro'].notna().sum())
            
            # Progresso percentual
            pct = (validados / TOTAL_CASOS) * 100
            barras = int(pct / 2)  # 50 caracteres = 100%
            barra = '█' * barras + '░' * (50 - barras)
            
            # Exibe
            print("=" * 60)
            print("VALIDAÇÃO IA - PROGRESSO")
            print("=" * 60)
            print(f"\n{validados}/{TOTAL_CASOS} casos ({pct:.1f}%)")
            print(f"[{barra}]\n")
            
            print(f"✓ Confirmados: {confirmados}")
            print(f"✗ Rejeitados:  {rejeitados}")
            if erros > 0:
                print(f"⚠ Erros:       {erros}")
            
            # Confiança média
            casos_conf = df[(df['ia_validado'] == True) & (df['ia_mesma_pessoa'] == True)]
            if len(casos_conf) > 0:
                conf_media = casos_conf['ia_confianca'].mean()
                if conf_media > 0:
                    print(f"📊 Confiança:  {conf_media:.0f}%")
            
            # Tempo estimado
            restantes = TOTAL_CASOS - validados
            tempo_estimado = restantes * 0.2  # 0.2 min/caso
            if restantes > 0:
                print(f"⏱ Restam:      ~{tempo_estimado:.1f} min")
            
            # Último caso processado
            if validados > 0:
                ultimos_validados = df[df['ia_validado'] == True]
                if len(ultimos_validados) > 0:
                    ultimo = ultimos_validados.iloc[-1]
                    status = "✓" if ultimo['ia_mesma_pessoa'] else "✗"
                    nome_curto = str(ultimo['nome'])[:40]
                    print(f"\nÚltimo: {status} {nome_curto}")
            
            # Rodapé
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Ctrl+C para sair")
            print("=" * 60)
            
            # Verifica se concluído
            if validados >= TOTAL_CASOS:
                print("\n🎉 VALIDAÇÃO CONCLUÍDA!")
                print("\n📊 Ver relatório: output/RELATORIO_VALIDACAO_FINAL.xlsx\n")
                break
            
            # Aguarda próxima atualização
            time.sleep(INTERVALO_ATUALIZACAO)
            
    except KeyboardInterrupt:
        print("\n\n✓ Monitor encerrado")
        print("  (A validação continua rodando em background)\n")


if __name__ == "__main__":
    mostrar_progresso()
