import pandas as pd

df = pd.read_excel('output/RELATORIO_ANALISE_CORRELACOES.xlsx', sheet_name='CASOS PARA ANÁLISE')

print("=" * 80)
print("RELATÓRIO COM CAMPO DE TRANSTORNO PSIQUIÁTRICO - EXEMPLO")
print("=" * 80)

for i in range(min(3, len(df))):
    caso = df.iloc[i]
    print(f"\n{'='*80}")
    print(f"CASO {i+1}: {caso['Nome Completo']}")
    print(f"{'='*80}")
    print(f"📋 Data Nascimento: {caso['Data Nascimento']}")
    print(f"👨‍👩‍👦 Nome Mãe: {caso['Nome da Mãe']}")
    print(f"👨‍👩‍👦 Nome Pai: {caso['Nome do Pai']}")
    print(f"🆔 RG: {caso['RG']}")
    print(f"\n🧠 TRANSTORNO PSIQUIÁTRICO: {caso['🧠 Transtorno Psiquiátrico']}")
    print(f"📋 TIPO TRANSTORNO: {caso['📋 Tipo Transtorno']}")
    print(f"\n📋 BO Desaparecimento: {caso['📋 BO Desaparecimento']}")
    print(f"⚰️ BO Morte: {caso['⚰️ BO Morte/Cadáver']}")
    print(f"⏱️ Dias Entre Eventos: {caso['⏱️ Dias Entre Eventos']} dias")
    print(f"💪 Força: {caso['Força Correlação']}")
    print(f"\n🤖 VALIDAÇÃO IA:")
    print(f"   Confiança: {caso['🤖 Confiança IA (%)']}%")
    print(f"   Justificativa: {caso['📝 Análise da IA']}")
    print(f"\n👮 CAMPOS PARA ANÁLISE HUMANA:")
    print(f"   [ ] Análise do Perito: {caso['👮 Análise do Perito']}")
    print(f"   [ ] Data Análise: {caso['📅 Data Análise']}")
    print(f"   [ ] Nome Analista: {caso['✍️ Nome do Analista']}")
    print(f"   [ ] Observações: {caso['💭 Observações']}")

print("\n" + "=" * 80)
print(f"TOTAL: {len(df)} casos prontos para análise")
print("=" * 80)
