"""
Validação de Correlações usando IA (GPT/LLM)
Analisa históricos para encontrar evidências que confirmem a correlação
"""

import pandas as pd
import json
import os
from datetime import datetime

# Verificar se há API key disponível
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    USE_AI = True
except:
    USE_AI = False
    print("⚠️ OpenAI não configurada. Use: export OPENAI_API_KEY='sua-chave'")

print("=" * 80)
print("VALIDAÇÃO DE CORRELAÇÕES COM IA")
print("=" * 80)

# Carregar dados
df_correlacoes = pd.read_excel('output/correlacoes_temporais.xlsx', sheet_name='Correlações FORTES')
df_completo = pd.read_excel('output/dataset_filtrado_grupo_alvo.xlsx', sheet_name='Dados Filtrados')

print(f"\n📊 Carregados: {len(df_correlacoes)} correlações fortes para validar")

def buscar_evidencias_com_ia(historico_desap, historico_morte, nome_pessoa, dias_intervalo):
    """
    Usa IA para analisar os históricos e buscar evidências de correlação
    """
    
    prompt = f"""Você é um analista criminal especializado em correlação de casos.

CASO: {nome_pessoa}

HISTÓRICO DO DESAPARECIMENTO:
{historico_desap[:800]}

HISTÓRICO DA MORTE/LOCALIZAÇÃO DO CORPO:
{historico_morte[:800]}

INTERVALO: {dias_intervalo} dia(s) entre os eventos

TAREFA: Analise se há evidências que conectam esses dois eventos. Procure por:
1. Menções ao nome da pessoa em ambos os históricos
2. Descrições físicas compatíveis
3. Locais mencionados que se relacionam
4. Circunstâncias que indicam continuidade entre os eventos
5. Menções a "desaparecido", "pessoa que estava desaparecida", "localizado"
6. Referências cruzadas entre os BOs

Responda em JSON com esta estrutura:
{{
    "evidencias_encontradas": true/false,
    "confianca": "ALTA/MÉDIA/BAIXA",
    "evidencias": ["lista de evidências específicas encontradas"],
    "trechos_relevantes": ["trechos exatos que conectam os casos"],
    "conclusao": "explicação breve da correlação"
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um analista criminal especializado em correlação de casos. Responda sempre em JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        resultado_texto = response.choices[0].message.content
        
        # Extrair JSON do resultado
        if "```json" in resultado_texto:
            resultado_texto = resultado_texto.split("```json")[1].split("```")[0]
        elif "```" in resultado_texto:
            resultado_texto = resultado_texto.split("```")[1].split("```")[0]
        
        return json.loads(resultado_texto.strip())
    
    except Exception as e:
        print(f"   ⚠️ Erro na análise com IA: {e}")
        return {
            "evidencias_encontradas": False,
            "confianca": "ERRO",
            "evidencias": [],
            "trechos_relevantes": [],
            "conclusao": f"Erro na análise: {str(e)}"
        }

def validar_correlacao_sem_ia(historico_desap, historico_morte, nome_pessoa):
    """
    Validação básica sem IA (usando regex e keywords)
    """
    nome_limpo = nome_pessoa.lower()
    hist_desap_lower = str(historico_desap).lower()
    hist_morte_lower = str(historico_morte).lower()
    
    evidencias = []
    
    # Verificar se nome aparece em ambos
    if nome_limpo in hist_desap_lower and nome_limpo in hist_morte_lower:
        evidencias.append("Nome da pessoa aparece em ambos os históricos")
    
    # Palavras-chave de conexão
    keywords_conexao = [
        "desaparecido", "pessoa que estava desaparecida", 
        "localizado", "encontrado", "cadáver localizado",
        "em relação ao desaparecimento", "referente ao bo"
    ]
    
    for keyword in keywords_conexao:
        if keyword in hist_morte_lower:
            evidencias.append(f"Menção a '{keyword}' no histórico da morte")
    
    confianca = "ALTA" if len(evidencias) >= 2 else "MÉDIA" if len(evidencias) == 1 else "BAIXA"
    
    return {
        "evidencias_encontradas": len(evidencias) > 0,
        "confianca": confianca,
        "evidencias": evidencias,
        "trechos_relevantes": [],
        "conclusao": f"Validação automática encontrou {len(evidencias)} evidência(s)"
    }

# Processar amostra
print(f"\n{'='*80}")
print("VALIDANDO CORRELAÇÕES (amostra de 10 casos)")
print("="*80)

resultados_validacao = []

# Pegar 10 primeiros casos
for idx, caso in df_correlacoes.head(10).iterrows():
    print(f"\n📋 Caso {idx+1}: {caso['nome']}")
    print(f"   Intervalo: {caso['dias_entre_eventos']} dia(s)")
    
    # Buscar históricos completos
    reg_desap = df_completo[df_completo['chave_ocorrencia'] == caso['bo_desaparecimento']]
    reg_morte = df_completo[df_completo['chave_ocorrencia'] == caso['bo_morte']]
    
    historico_desap = ""
    historico_morte = ""
    
    if len(reg_desap) > 0 and 'historico' in reg_desap.columns:
        historico_desap = str(reg_desap.iloc[0]['historico'])
    
    if len(reg_morte) > 0 and 'historico' in reg_morte.columns:
        historico_morte = str(reg_morte.iloc[0]['historico'])
    
    if not historico_desap or not historico_morte or historico_desap == 'nan' or historico_morte == 'nan':
        print("   ⚠️ Históricos não disponíveis")
        continue
    
    # Validar com IA ou sem IA
    if USE_AI:
        print("   🤖 Analisando com IA...")
        validacao = buscar_evidencias_com_ia(
            historico_desap, 
            historico_morte, 
            caso['nome'],
            caso['dias_entre_eventos']
        )
    else:
        print("   🔍 Analisando com regex...")
        validacao = validar_correlacao_sem_ia(
            historico_desap,
            historico_morte,
            caso['nome']
        )
    
    print(f"   ✅ Confiança: {validacao['confianca']}")
    print(f"   📌 Evidências encontradas: {len(validacao['evidencias'])}")
    for ev in validacao['evidencias'][:3]:  # Mostrar até 3
        print(f"      • {ev}")
    
    if validacao['trechos_relevantes']:
        print(f"   📝 Trechos relevantes:")
        for trecho in validacao['trechos_relevantes'][:2]:
            print(f"      '{trecho[:100]}...'")
    
    print(f"   💡 Conclusão: {validacao['conclusao'][:150]}...")
    
    # Salvar resultado
    resultados_validacao.append({
        'nome': caso['nome'],
        'bo_desaparecimento': caso['bo_desaparecimento'],
        'bo_morte': caso['bo_morte'],
        'dias_entre_eventos': caso['dias_entre_eventos'],
        'confianca_correlacao': validacao['confianca'],
        'qtd_evidencias': len(validacao['evidencias']),
        'evidencias': ' | '.join(validacao['evidencias']),
        'conclusao_ia': validacao['conclusao']
    })

# Salvar resultados
if resultados_validacao:
    df_validacao = pd.DataFrame(resultados_validacao)
    arquivo_saida = "output/validacao_ia_correlacoes.xlsx"
    df_validacao.to_excel(arquivo_saida, index=False)
    
    print(f"\n{'='*80}")
    print("RESUMO DA VALIDAÇÃO")
    print("="*80)
    
    print(f"\n📊 DISTRIBUIÇÃO DE CONFIANÇA:")
    for conf in ['ALTA', 'MÉDIA', 'BAIXA']:
        qtd = (df_validacao['confianca_correlacao'] == conf).sum()
        if qtd > 0:
            print(f"   {conf}: {qtd} casos")
    
    print(f"\n✅ Arquivo salvo: {arquivo_saida}")
    print(f"\n💡 PRÓXIMOS PASSOS:")
    print(f"   1. Revisar casos com confiança ALTA - correlação muito provável")
    print(f"   2. Investigar casos com confiança BAIXA - podem precisar revisão")
    print(f"   3. Usar IA para analisar os 162 casos completos")

print(f"\n{'='*80}")
print("VALIDAÇÃO CONCLUÍDA!")
print("="*80)

if not USE_AI:
    print(f"\n⚠️ ATENÇÃO: Validação feita com regex (sem IA)")
    print(f"   Para usar IA completa, configure:")
    print(f"   export OPENAI_API_KEY='sua-chave-aqui'")
    print(f"   pip install openai")
