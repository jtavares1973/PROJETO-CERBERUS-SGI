"""
Monitor de progresso SIMPLES e LIMPO
"""
import pandas as pd
import time
import os
from pathlib import Path
from datetime import datetime


def mostrar():
    arquivo = Path('output/validacao_progresso.xlsx')
    
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            if not arquivo.exists():
                print("⏳ Aguardando validação iniciar...")
                time.sleep(5)
                continue
            
            df = pd.read_excel(arquivo)
            
            # Stats
            total = len(df)
            confirmados = len(df[df['ia_mesma_pessoa'] == True])
            rejeitados = len(df[df['ia_mesma_pessoa'] == False])
            erros = len(df[df['ia_validado'] == False])
            
            # Barra
            pct = (total / 86) * 100
            barras = int(pct / 2)
            barra = '█' * barras + '░' * (50 - barras)
            
            print("=" * 60)
            print("VALIDAÇÃO IA - PROGRESSO")
            print("=" * 60)
            print(f"\n{total}/86 casos ({pct:.1f}%)")
            print(f"[{barra}]\n")
            
            print(f"✓ Confirmados: {confirmados}")
            print(f"✗ Rejeitados:  {rejeitados}")
            if erros > 0:
                print(f"⚠ Erros:       {erros}")
            
            # Confiança
            casos_conf = df[(df['ia_validado'] == True) & (df['ia_mesma_pessoa'] == True)]
            if len(casos_conf) > 0 and casos_conf['ia_confianca'].mean() > 0:
                conf_media = casos_conf['ia_confianca'].mean()
                print(f"📊 Confiança:  {conf_media:.0f}%")
            
            # Tempo
            restantes = 86 - total
            tempo_restante = restantes * 0.2
            print(f"⏱ Restam:      ~{tempo_restante:.1f} min")
            
            # Último caso
            if len(df) > 0:
                ultimo = df.iloc[-1]
                status = "✓" if ultimo['ia_mesma_pessoa'] else "✗"
                nome_curto = ultimo['nome'][:40]
                print(f"\nÚltimo: {status} {nome_curto}")
            
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Ctrl+C para sair")
            print("=" * 60)
            
            if total >= 86:
                print("\n🎉 VALIDAÇÃO CONCLUÍDA!")
                break
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\n✓ Monitor encerrado (validação continua rodando)")


if __name__ == "__main__":
    mostrar()
