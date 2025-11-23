"""
Análise dos Modelos Instalados vs Recomendação
"""

print("=" * 80)
print("SEUS MODELOS INSTALADOS - ANÁLISE PARA CORRELAÇÃO CRIMINAL")
print("=" * 80)

modelos_analise = {
    "🥇 TOP 1 - MELHOR PARA SEU CASO": {
        "modelo": "qwen2.5-ptbr:7b",
        "tamanho": "15 GB (otimizado para português)",
        "porque": [
            "✅ ESPECIALIZADO EM PORTUGUÊS BRASILEIRO",
            "✅ Qwen 2.5 é um dos melhores modelos atuais",
            "✅ 7B params com fine-tuning para PT-BR",
            "✅ Excelente raciocínio lógico",
            "✅ Perfeito para textos jurídicos/policiais"
        ],
        "nota": "10/10 - IDEAL PARA VOCÊ"
    },
    
    "🥈 TOP 2 - ALTERNATIVA PODEROSA": {
        "modelo": "qwen3:14b",
        "tamanho": "9.3 GB",
        "porque": [
            "✅ Modelo MAIOR e mais capaz (14B params)",
            "✅ Qwen 3 - versão mais recente",
            "✅ Melhor raciocínio complexo",
            "✅ Bom português (não especializado mas funciona bem)",
            "✅ Vai usar mais a sua GPU"
        ],
        "nota": "9.5/10 - Mais poder bruto"
    },
    
    "🥉 TOP 3 - EQUILIBRADO": {
        "modelo": "mistral-nemo:12b",
        "tamanho": "7.1 GB",
        "porque": [
            "✅ Modelo intermediário (12B params)",
            "✅ Mistral tem ótimo raciocínio",
            "✅ Rápido e eficiente",
            "✅ Bom equilíbrio velocidade/qualidade"
        ],
        "nota": "9/10 - Muito bom"
    },
    
    "⭐ BÔNUS - ESPECIALIZADO": {
        "modelo": "analise-criminal-pcdf:latest",
        "tamanho": "4.9 GB",
        "porque": [
            "✅ PARECE SER UM MODELO CUSTOMIZADO PARA PCDF!",
            "✅ Pode já estar treinado para casos policiais",
            "✅ Provavelmente baseado em llama3.1",
            "✅ Se funciona bem, pode ser o melhor de todos!"
        ],
        "nota": "?/10 - TESTAR! Pode ser uma joia escondida"
    }
}

for titulo, info in modelos_analise.items():
    print(f"\n{titulo}")
    print(f"Modelo: {info['modelo']}")
    print(f"Tamanho: {info['tamanho']}")
    print(f"Nota: {info['nota']}")
    print("\nPor que usar:")
    for motivo in info['porque']:
        print(f"   {motivo}")

print("\n" + "=" * 80)
print("🎯 MINHA RECOMENDAÇÃO FINAL PARA VOCÊ")
print("=" * 80)

print("""
Com seu hardware monstruoso (Ryzen 9 + RTX 5070 Ti + 64GB RAM):

🥇 MELHOR ESCOLHA: qwen2.5-ptbr:7b
   → Especializado em português brasileiro
   → Vai entender perfeitamente os BOs da PCDF
   → Tamanho não é problema para você
   → Comando: Use este!

🥈 SE QUISER MAIS PODER: qwen3:14b
   → Modelo maior, mais inteligente
   → Melhor raciocínio complexo
   → Comando: Também excelente!

⭐ TESTE PRIMEIRO: analise-criminal-pcdf:latest
   → Esse nome sugere que foi customizado para PCDF!
   → Pode já estar otimizado para o seu caso exato
   → VALE A PENA TESTAR PRIMEIRO!

📊 ESTRATÉGIA SUGERIDA:
1. Teste com analise-criminal-pcdf:latest (parece específico!)
2. Se não for bom, use qwen2.5-ptbr:7b (português perfeito)
3. Se quiser ainda mais poder, use qwen3:14b

Seu PC aguenta qualquer um rodando RÁPIDO!
""")

print("\n" + "=" * 80)
print("🚀 PRÓXIMO PASSO")
print("=" * 80)

print("""
Vou criar 3 scripts para você testar:

1. teste_modelo_analise_criminal.py
   → Testa o modelo analise-criminal-pcdf com 1 caso real

2. validar_com_qwen_ptbr.py
   → Usa qwen2.5-ptbr:7b para validar correlações

3. validar_com_qwen3_14b.py
   → Usa qwen3:14b para máxima precisão

Qual você quer que eu crie primeiro?
   a) Testar o analise-criminal-pcdf (curiosidade!)
   b) Ir direto com qwen2.5-ptbr (português garantido)
   c) Usar qwen3:14b (máximo poder)
   d) Criar os 3 para você comparar
""")
