"""
Guia: Melhores Modelos Locais (Ollama) para Análise de Correlação Criminal

MODELOS RECOMENDADOS (em ordem de prioridade):
"""

# ============================================================================
# 🥇 TOP 3 MODELOS PARA ANÁLISE CRIMINAL EM PORTUGUÊS
# ============================================================================

MODELOS_RECOMENDADOS = {
    "1_MELHOR_GERAL": {
        "nome": "llama3.1:8b",
        "tamanho": "4.7 GB",
        "precisao": "⭐⭐⭐⭐⭐ (Excelente)",
        "velocidade": "⭐⭐⭐⭐ (Rápido)",
        "portugues": "⭐⭐⭐⭐ (Muito bom)",
        "raciocinio": "⭐⭐⭐⭐⭐ (Excelente lógica)",
        "comando": "ollama pull llama3.1:8b",
        "porque": "Melhor custo-benefício. Ótimo raciocínio lógico para conectar eventos temporais."
    },
    
    "2_MELHOR_PORTUGUES": {
        "nome": "gemma2:9b",
        "tamanho": "5.4 GB", 
        "precisao": "⭐⭐⭐⭐⭐ (Excelente)",
        "velocidade": "⭐⭐⭐⭐ (Rápido)",
        "portugues": "⭐⭐⭐⭐⭐ (Perfeito)",
        "raciocinio": "⭐⭐⭐⭐ (Muito bom)",
        "comando": "ollama pull gemma2:9b",
        "porque": "Google Gemma 2 tem excelente compreensão de português e contexto."
    },
    
    "3_MAIS_RAPIDO": {
        "nome": "phi3:mini",
        "tamanho": "2.3 GB",
        "precisao": "⭐⭐⭐⭐ (Muito bom)",
        "velocidade": "⭐⭐⭐⭐⭐ (Muito rápido)",
        "portugues": "⭐⭐⭐ (Bom)",
        "raciocinio": "⭐⭐⭐⭐ (Muito bom)",
        "comando": "ollama pull phi3:mini",
        "porque": "Microsoft Phi-3 é pequeno mas poderoso. Ideal se tiver pouca RAM."
    },
    
    "4_ALTERNATIVA_POTENTE": {
        "nome": "qwen2.5:7b",
        "tamanho": "4.7 GB",
        "precisao": "⭐⭐⭐⭐⭐ (Excelente)",
        "velocidade": "⭐⭐⭐⭐ (Rápido)",
        "portugues": "⭐⭐⭐⭐ (Muito bom)",
        "raciocinio": "⭐⭐⭐⭐⭐ (Excelente)",
        "comando": "ollama pull qwen2.5:7b",
        "porque": "Alibaba Qwen2.5 é novo e muito bom em raciocínio complexo."
    }
}

# ============================================================================
# 📊 COMPARAÇÃO PARA SEU CASO DE USO
# ============================================================================

print("=" * 80)
print("RECOMENDAÇÃO DE MODELO PARA ANÁLISE CRIMINAL")
print("=" * 80)

print("\n🎯 PARA SEU CASO (Correlação Criminal + Português):\n")

print("🥇 RECOMENDAÇÃO PRINCIPAL: llama3.1:8b")
print("   Motivos:")
print("   ✅ Excelente raciocínio lógico para conectar eventos")
print("   ✅ Bom entendimento de português")
print("   ✅ Consegue analisar sequências temporais")
print("   ✅ Identifica padrões em texto jurídico")
print("   ✅ 4.7 GB - roda bem em máquinas comuns")
print("   📥 Instalar: ollama pull llama3.1:8b\n")

print("🥈 ALTERNATIVA SE QUISER MAIS PORTUGUÊS: gemma2:9b")
print("   ✅ Melhor compreensão de português brasileiro")
print("   ✅ Muito bom em análise de texto")
print("   ⚠️ Um pouco maior (5.4 GB)")
print("   📥 Instalar: ollama pull gemma2:9b\n")

print("🥉 SE TIVER POUCA RAM (<8GB): phi3:mini")
print("   ✅ Apenas 2.3 GB - muito leve")
print("   ✅ Surpreendentemente capaz")
print("   ⚠️ Português não é perfeito mas funciona")
print("   📥 Instalar: ollama pull phi3:mini\n")

# ============================================================================
# 🔧 PASSO A PASSO PARA INSTALAR E TESTAR
# ============================================================================

print("\n" + "=" * 80)
print("COMO INSTALAR E TESTAR")
print("=" * 80)

print("""
PASSO 1: Instalar Ollama (se ainda não tem)
   Windows: https://ollama.com/download
   
PASSO 2: Baixar o modelo recomendado
   Abra o terminal e execute:
   
   ollama pull llama3.1:8b
   
   (vai baixar ~4.7 GB)

PASSO 3: Testar o modelo
   
   ollama run llama3.1:8b
   
   Digite: "Analise este texto em português: José desapareceu dia 10/01. 
           No dia 11/01 foi encontrado morto. Há correlação?"
   
   Se responder bem, está pronto!

PASSO 4: Integrar no seu script Python
   
   pip install ollama
   
   Eu já vou criar o script integrado para você!
""")

print("\n" + "=" * 80)
print("REQUISITOS DO SISTEMA")
print("=" * 80)

print("""
Para llama3.1:8b (recomendado):
   • RAM: 8 GB mínimo (16 GB ideal)
   • Espaço: 5 GB livre
   • CPU: Qualquer processador moderno
   • GPU: Não obrigatória (mas acelera)

Para gemma2:9b (alternativa):
   • RAM: 10 GB mínimo (16 GB ideal)
   • Espaço: 6 GB livre

Para phi3:mini (leve):
   • RAM: 4 GB mínimo (8 GB ideal)
   • Espaço: 3 GB livre
""")

print("\n" + "=" * 80)
print("📋 RESUMO DA ESCOLHA")
print("=" * 80)

print("""
🎯 MINHA RECOMENDAÇÃO FINAL: llama3.1:8b

Por quê?
✅ Melhor equilíbrio entre qualidade e velocidade
✅ Excelente em raciocínio lógico (essencial para correlações)
✅ Bom português (suficiente para seu caso)
✅ Tamanho razoável (4.7 GB)
✅ Roda bem em hardware comum
✅ Modelo mais testado e confiável

Se você tem uma máquina boa (16GB+ RAM):
   → Use gemma2:9b para melhor português

Se sua máquina é mais fraca (<8GB RAM):
   → Use phi3:mini para economizar recursos
""")

print("\n🚀 Pronto para criar o script integrado com Ollama?")
print("   Digite: 'sim' e eu crio o código completo!")
