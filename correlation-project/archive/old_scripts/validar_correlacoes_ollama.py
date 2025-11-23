"""
Validação de Correlações Temporais usando Ollama (Local)
Usa DOIS modelos para máxima precisão:
1. qwen2.5-ptbr:7b - Especializado em português brasileiro
2. qwen3:14b - Máxima capacidade de raciocínio
"""

import pandas as pd
import ollama
from datetime import datetime
import json
from pathlib import Path


def criar_prompt_validacao(caso):
    """Cria prompt detalhado para validação de correlação"""
    
    prompt = f"""Você é um analista forense especializado em investigação criminal.

CASO DE CORRELAÇÃO TEMPORAL:

DESAPARECIMENTO:
- BO: {caso['bo_desaparecimento']}
- Nome: {caso['nome']}
- Data Nascimento: {caso['data_nascimento']}
- Nome da Mãe: {caso['nome_mae']}
- Nome do Pai: {caso['nome_pai']}
- RG: {caso['numero_rg']} - {caso['orgao_rg']}/{caso['uf_rg']}
- Sexo: {caso['sexo']}
- Data Desaparecimento: {caso['data_desaparecimento']}
- Local: {caso['cidade_desaparecimento']}
- Unidade: {caso['unidade_desaparecimento']}
- Histórico: {caso['historico_desaparecimento']}

MORTE/CADÁVER:
- BO: {caso['bo_morte']}
- Tipo: {caso['tipo_morte']}
- Data Morte: {caso['data_morte']}
- Local: {caso['cidade_morte']}
- Unidade: {caso['unidade_morte']}
- Histórico: {caso['historico_morte']}

INTERVALO: {caso['dias_entre_eventos']} dias

ANÁLISE NECESSÁRIA:
1. CONFIRME A IDENTIDADE: Compare data nascimento, nome mãe, nome pai e RG - são a MESMA PESSOA?
2. Os históricos indicam CONEXÃO entre desaparecimento e morte?
3. Há evidências EXPLÍCITAS ou IMPLÍCITAS nos textos?
4. O intervalo temporal ({caso['dias_entre_eventos']} dias) é compatível?
5. Há menção de buscas, investigação ou continuidade entre os casos?

RESPONDA EM JSON:
{{
  "mesma_pessoa": true/false,
  "confianca_identidade": "ALTA/MÉDIA/BAIXA",
  "dados_conferem": {{
    "data_nascimento": true/false,
    "nome_mae": true/false,
    "nome_pai": true/false,
    "rg": true/false
  }},
  "evidencias_conexao": ["lista de evidências encontradas"],
  "trechos_relevantes": ["citações EXATAS dos históricos"],
  "correlacao_valida": true/false,
  "confianca_correlacao": 0-100,
  "justificativa": "explicação detalhada",
  "alerta_investigacao": "pontos críticos"
}}

IMPORTANTE: Use os dados de identificação (data nascimento, mãe, pai, RG) para CONFIRMAR a identidade primeiro."""

    return prompt


def validar_com_modelo(caso, modelo_nome):
    """Valida um caso usando um modelo específico do Ollama"""
    
    print(f"   🤖 Validando com {modelo_nome}...")
    
    try:
        prompt = criar_prompt_validacao(caso)
        
        # Chama o modelo Ollama
        response = ollama.chat(
            model=modelo_nome,
            messages=[{
                'role': 'user',
                'content': prompt
            }],
            options={
                'temperature': 0.3,  # Baixa temperatura para respostas mais consistentes
                'num_predict': 1000  # Limite de tokens
            }
        )
        
        # Extrai o conteúdo da resposta
        content = response['message']['content']
        
        # Tenta extrair JSON da resposta
        try:
            # Procura por blocos JSON
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                resultado = json.loads(json_str)
                resultado['modelo_usado'] = modelo_nome
                resultado['resposta_completa'] = content
                return resultado
            else:
                print(f"      ⚠️ Resposta não contém JSON válido")
                return None
                
        except json.JSONDecodeError as e:
            print(f"      ⚠️ Erro ao parsear JSON: {e}")
            # Retorna resposta em formato texto se não conseguir parsear
            return {
                'modelo_usado': modelo_nome,
                'erro_parsing': True,
                'resposta_texto': content
            }
            
    except Exception as e:
        print(f"      ❌ Erro ao validar com {modelo_nome}: {e}")
        return None


def validar_com_dois_modelos(caso):
    """Valida usando ambos os modelos e compara resultados"""
    
    print(f"\n🔍 Validando caso: {caso['nome']}")
    print(f"   BO Desaparecimento: {caso['bo_desaparecimento']}")
    print(f"   BO Morte: {caso['bo_morte']}")
    print(f"   Intervalo: {caso['dias_entre_eventos']} dias")
    
    # Valida com ambos os modelos
    resultado_ptbr = validar_com_modelo(caso, 'qwen2.5-ptbr:7b')
    resultado_qwen3 = validar_com_modelo(caso, 'qwen3:14b')
    
    # Combina resultados
    resultado_final = {
        'chave_pessoa': caso['chave_pessoa'],
        'nome': caso['nome'],
        'bo_desaparecimento': caso['bo_desaparecimento'],
        'bo_morte': caso['bo_morte'],
        'dias_entre': caso['dias_entre_eventos'],
        'tipo_morte': caso['tipo_morte'],
        'cidade_desaparecimento': caso['cidade_desaparecimento'],
        'cidade_morte': caso['cidade_morte'],
        'validacao_ptbr': resultado_ptbr,
        'validacao_qwen3': resultado_qwen3,
        'timestamp_validacao': datetime.now().isoformat()
    }
    
    # Análise de consenso
    if resultado_ptbr and resultado_qwen3:
        consenso_correlacao = (
            resultado_ptbr.get('correlacao_valida') and 
            resultado_qwen3.get('correlacao_valida')
        )
        
        confianca_media = (
            resultado_ptbr.get('confianca_correlacao', 0) +
            resultado_qwen3.get('confianca_correlacao', 0)
        ) / 2
        
        resultado_final['consenso'] = {
            'ambos_confirmam': consenso_correlacao,
            'confianca_media': confianca_media,
            'acordo': 'SIM' if consenso_correlacao else 'NÃO'
        }
        
        print(f"   ✅ Consenso: {resultado_final['consenso']['acordo']} ({confianca_media:.1f}% confiança)")
    
    return resultado_final


def main():
    print("=" * 80)
    print("VALIDAÇÃO DE CORRELAÇÕES COM IA LOCAL (OLLAMA)")
    print("Modelos: qwen2.5-ptbr:7b (português) + qwen3:14b (raciocínio)")
    print("=" * 80)
    
    # Carrega correlações COM IDENTIFICAÇÃO COMPLETA
    arquivo_correlacoes = Path('output/correlacoes_completas_com_identificacao.xlsx')
    
    if not arquivo_correlacoes.exists():
        print(f"❌ Arquivo não encontrado: {arquivo_correlacoes}")
        print("   Execute: python gerar_correlacoes_completas.py")
        return
    
    print(f"\n📂 Carregando correlações de: {arquivo_correlacoes}")
    df_correlacoes = pd.read_excel(arquivo_correlacoes, sheet_name='Todas Correlações')
    print(f"   ✓ {len(df_correlacoes)} correlações carregadas")
    print(f"   ✅ COM DADOS DE IDENTIFICAÇÃO: Nome Mãe, Nome Pai, RG, Data Nascimento")
    
    # Verifica se modelos estão disponíveis
    print("\n🔍 Verificando modelos Ollama...")
    try:
        modelos_disponiveis = ollama.list()
        modelos_nomes = [m.get('model', m.get('name', '')) for m in modelos_disponiveis.get('models', [])]
        
        if 'qwen2.5-ptbr:7b' not in modelos_nomes:
            print("   ⚠️ Modelo qwen2.5-ptbr:7b não encontrado!")
            print("   Execute: ollama pull qwen2.5-ptbr:7b")
            return
            
        if 'qwen3:14b' not in modelos_nomes:
            print("   ⚠️ Modelo qwen3:14b não encontrado!")
            print("   Execute: ollama pull qwen3:14b")
            return
            
        print("   ✅ qwen2.5-ptbr:7b disponível")
        print("   ✅ qwen3:14b disponível")
        
    except Exception as e:
        print(f"   ❌ Erro ao verificar modelos: {e}")
        print("   Certifique-se de que o Ollama está rodando!")
        return
    
    # Pergunta quantos casos validar
    print("\n" + "=" * 80)
    print("OPÇÕES DE VALIDAÇÃO:")
    print("=" * 80)
    print(f"1. Validar TODOS ({len(df_correlacoes)} casos) - Tempo estimado: ~3-4 horas")
    print(f"2. Validar amostra de 10 casos (teste rápido) - Tempo: ~5 min")
    print(f"3. Validar apenas casos FORTES (0-30 dias) - {len(df_correlacoes[df_correlacoes['forca_correlacao'] == 'FORTE'])} casos - Tempo: ~60-75 min")
    print(f"4. Validar amostra de 10 casos FORTES (teste) - Tempo: ~5 min")
    print(f"5. Validar apenas casos CRÍTICOS (0-7 dias) - Tempo: variável")
    
    opcao = input("\nEscolha uma opção (1-5): ").strip()
    
    if opcao == '1':
        df_validar = df_correlacoes.copy()
        print(f"\n✓ Validando TODOS os {len(df_validar)} casos")
    elif opcao == '2':
        df_validar = df_correlacoes.head(10)
        print(f"\n✓ Validando amostra de {len(df_validar)} casos")
    elif opcao == '3':
        df_validar = df_correlacoes[df_correlacoes['forca_correlacao'] == 'FORTE']
        print(f"\n✓ Validando {len(df_validar)} casos FORTES")
    elif opcao == '4':
        df_validar = df_correlacoes[df_correlacoes['dias_entre'] <= 7]
        print(f"\n✓ Validando {len(df_validar)} casos CRÍTICOS (0-7 dias)")
    else:
        print("❌ Opção inválida!")
        return
    
    # Valida cada caso
    print("\n" + "=" * 80)
    print("INICIANDO VALIDAÇÕES...")
    print("=" * 80)
    
    resultados = []
    
    for i, (idx, caso) in enumerate(df_validar.iterrows()):
        print(f"\n[{i + 1}/{len(df_validar)}]")
        
        resultado = validar_com_dois_modelos(caso)
        resultados.append(resultado)
        
        # Salva progresso a cada 5 casos
        if len(resultados) % 5 == 0:
            print(f"\n💾 Salvando progresso ({len(resultados)} casos validados)...")
            salvar_resultados_parciais(resultados)
    
    # Salva resultados finais
    print("\n" + "=" * 80)
    print("SALVANDO RESULTADOS FINAIS...")
    print("=" * 80)
    
    salvar_resultados_finais(resultados, df_validar)
    
    print("\n✅ VALIDAÇÃO CONCLUÍDA!")
    print(f"   Total de casos validados: {len(resultados)}")
    print(f"   Arquivo gerado: output/validacao_ia_ollama_completa.xlsx")


def salvar_resultados_parciais(resultados):
    """Salva progresso parcial"""
    arquivo_parcial = Path('output/validacao_ia_parcial.json')
    arquivo_parcial.parent.mkdir(exist_ok=True)
    
    with open(arquivo_parcial, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)


def salvar_resultados_finais(resultados, df_original):
    """Salva resultados em Excel com múltiplas abas"""
    
    arquivo_saida = Path('output/validacao_ia_ollama_completa.xlsx')
    arquivo_saida.parent.mkdir(exist_ok=True)
    
    # Prepara DataFrame principal
    dados_principais = []
    
    for r in resultados:
        linha = {
            'chave_pessoa': r['chave_pessoa'],
            'nome': r['nome'],
            'bo_desaparecimento': r['bo_desaparecimento'],
            'bo_morte': r['bo_morte'],
            'dias_entre': r['dias_entre'],
            'tipo_morte': r['tipo_morte'],
            'cidade_desaparecimento': r['cidade_desaparecimento'],
            'cidade_morte': r['cidade_morte']
        }
        
        # Adiciona resultados do modelo PT-BR
        if r['validacao_ptbr']:
            linha['ptbr_correlacao_valida'] = r['validacao_ptbr'].get('correlacao_valida')
            linha['ptbr_confianca'] = r['validacao_ptbr'].get('confianca_correlacao')
            linha['ptbr_mesma_pessoa'] = r['validacao_ptbr'].get('mesma_pessoa')
            linha['ptbr_justificativa'] = r['validacao_ptbr'].get('justificativa', '')
        
        # Adiciona resultados do Qwen3
        if r['validacao_qwen3']:
            linha['qwen3_correlacao_valida'] = r['validacao_qwen3'].get('correlacao_valida')
            linha['qwen3_confianca'] = r['validacao_qwen3'].get('confianca_correlacao')
            linha['qwen3_mesma_pessoa'] = r['validacao_qwen3'].get('mesma_pessoa')
            linha['qwen3_justificativa'] = r['validacao_qwen3'].get('justificativa', '')
        
        # Adiciona consenso
        if 'consenso' in r:
            linha['consenso'] = r['consenso']['acordo']
            linha['confianca_media'] = r['consenso']['confianca_media']
        
        dados_principais.append(linha)
    
    df_resultado = pd.DataFrame(dados_principais)
    
    # Filtra resultados por consenso
    df_confirmados = df_resultado[df_resultado['consenso'] == 'SIM'].copy()
    df_rejeitados = df_resultado[df_resultado['consenso'] == 'NÃO'].copy()
    
    # Ordena por confiança
    df_confirmados = df_confirmados.sort_values('confianca_media', ascending=False)
    df_rejeitados = df_rejeitados.sort_values('confianca_media', ascending=True)
    
    # Salva em Excel
    with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
        df_resultado.to_excel(writer, sheet_name='Todas_Validacoes', index=False)
        df_confirmados.to_excel(writer, sheet_name='Correlacoes_Confirmadas', index=False)
        df_rejeitados.to_excel(writer, sheet_name='Correlacoes_Rejeitadas', index=False)
        
        # Estatísticas
        stats = {
            'total_validados': len(resultados),
            'confirmados_consenso': len(df_confirmados),
            'rejeitados_consenso': len(df_rejeitados),
            'taxa_confirmacao': len(df_confirmados) / len(resultados) * 100 if resultados else 0,
            'confianca_media_confirmados': df_confirmados['confianca_media'].mean() if len(df_confirmados) > 0 else 0,
            'confianca_media_rejeitados': df_rejeitados['confianca_media'].mean() if len(df_rejeitados) > 0 else 0
        }
        
        df_stats = pd.DataFrame([stats])
        df_stats.to_excel(writer, sheet_name='Estatisticas', index=False)
    
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Total validados: {stats['total_validados']}")
    print(f"   Confirmados (consenso): {stats['confirmados_consenso']} ({stats['taxa_confirmacao']:.1f}%)")
    print(f"   Rejeitados (consenso): {stats['rejeitados_consenso']}")
    print(f"   Confiança média (confirmados): {stats['confianca_media_confirmados']:.1f}%")


if __name__ == "__main__":
    main()
