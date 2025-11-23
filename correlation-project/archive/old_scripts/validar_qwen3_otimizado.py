"""
Validação de Correlações com Qwen3:14b OTIMIZADO
Versão RÁPIDA e PRECISA - 1 modelo apenas
"""

import pandas as pd
import ollama
from datetime import datetime
import json
from pathlib import Path


def criar_prompt_otimizado(caso):
    """Prompt otimizado para qwen3:14b focado em validação de identidade"""
    
    # Monta dados de identificação
    dados_id = f"""DADOS DE IDENTIFICAÇÃO:
- Nome: {caso['nome']}
- Data Nascimento: {caso['data_nascimento']}
- Mãe: {caso['nome_mae']}
- Pai: {caso['nome_pai']}
- RG: {caso['numero_rg']} ({caso['orgao_rg']}/{caso['uf_rg']})
- Sexo: {caso['sexo']}
- Transtorno Psiquiátrico: {caso.get('tem_transtorno_psiquiatrico', 'Não informado')}
- Tipo Transtorno: {caso.get('tipo_transtorno', 'N/A')}"""

    prompt = f"""Você é um perito criminal especializado em análise de correlação de casos.

TAREFA: Validar se o desaparecimento e a morte se referem à MESMA PESSOA.

{dados_id}

DESAPARECIMENTO:
BO: {caso['bo_desaparecimento']}
Data: {caso['data_desaparecimento']}
Local: {caso['cidade_desaparecimento']} ({caso['unidade_desaparecimento']})
Histórico: {caso['historico_desaparecimento'][:500]}

MORTE ({caso['tipo_morte']}):
BO: {caso['bo_morte']}
Data: {caso['data_morte']}
Local: {caso['cidade_morte']} ({caso['unidade_morte']})
Histórico: {caso['historico_morte'][:500]}

INTERVALO: {caso['dias_entre_eventos']} dias

ANÁLISE:
1. IDENTIDADE: Os dados (nome, data nasc, mãe, pai, RG) confirmam ser a MESMA pessoa? 
2. CONEXÃO: Os históricos mencionam relação entre os eventos?
3. EVIDÊNCIAS: Há citações de busca, investigação ou continuidade?
4. COMPATIBILIDADE: O intervalo de {caso['dias_entre_eventos']} dias é coerente?

RESPONDA APENAS EM JSON (sem markdown):
{{
  "mesma_pessoa": true/false,
  "dados_conferem": {{"data_nasc": true/false, "mae": true/false, "pai": true/false, "rg": true/false}},
  "correlacao_valida": true/false,
  "confianca": 0-100,
  "evidencias": ["lista"],
  "justificativa": "texto breve"
}}"""

    return prompt


def validar_caso(caso):
    """Valida um caso usando qwen3:14b otimizado"""
    
    try:
        prompt = criar_prompt_otimizado(caso)
        
        # Chama Ollama com parâmetros otimizados
        response = ollama.chat(
            model='qwen3:14b',
            messages=[{
                'role': 'user',
                'content': prompt
            }],
            options={
                'temperature': 0.1,  # Muito baixa para precisão máxima
                'top_p': 0.9,
                'num_predict': 800,  # Limite razoável
                'num_ctx': 4096      # Contexto suficiente
            }
        )
        
        content = response['message']['content']
        
        # Extrai JSON
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        
        if start_idx >= 0 and end_idx > start_idx:
            json_str = content[start_idx:end_idx]
            resultado = json.loads(json_str)
            resultado['resposta_completa'] = content
            return resultado
        else:
            return {'erro': 'JSON não encontrado', 'resposta_texto': content}
            
    except Exception as e:
        return {'erro': str(e)}


def main():
    print("=" * 80)
    print("VALIDAÇÃO OTIMIZADA COM QWEN3:14B")
    print("Modelo único de alta performance + dados de identificação completos")
    print("=" * 80)
    
    # Carrega correlações deduplicadas
    arquivo = Path('output/correlacoes_unicas_deduplicadas.xlsx')
    
    if not arquivo.exists():
        print(f"❌ Arquivo não encontrado: {arquivo}")
        print("   Execute: python remover_duplicatas.py")
        return
    
    print(f"\n📂 Carregando: {arquivo}")
    df = pd.read_excel(arquivo, sheet_name='Correlações Únicas')
    print(f"   ✓ {len(df)} correlações únicas carregadas")
    
    # Verifica modelo
    print("\n🔍 Verificando qwen3:14b...")
    try:
        modelos = ollama.list()
        nomes = [m.get('model', m.get('name', '')) for m in modelos.get('models', [])]
        
        if 'qwen3:14b' not in nomes:
            print("   ❌ qwen3:14b não encontrado!")
            print("   Execute: ollama pull qwen3:14b")
            return
            
        print("   ✅ qwen3:14b disponível")
        
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return
    
    # Menu de opções
    print("\n" + "=" * 80)
    print("OPÇÕES DE VALIDAÇÃO:")
    print("=" * 80)
    
    df_fortes = df[df['forca_correlacao'] == 'FORTE']
    df_criticos = df[df['dias_entre_eventos'] <= 7]
    
    print(f"1. TODOS os casos ({len(df)}) - Tempo: ~90-120 min")
    print(f"2. Amostra de 10 casos - Tempo: ~3 min")
    print(f"3. Casos FORTES ({len(df_fortes)}) - Tempo: ~30-40 min ⭐ RECOMENDADO")
    print(f"4. Amostra de 10 FORTES - Tempo: ~3 min")
    print(f"5. Casos CRÍTICOS 0-7 dias ({len(df_criticos)}) - Tempo: ~15-20 min")
    
    opcao = input("\nEscolha (1-5): ").strip()
    
    # Seleciona dataset
    if opcao == '1':
        df_validar = df.copy()
        desc = f"TODOS ({len(df)} casos)"
    elif opcao == '2':
        df_validar = df.head(10)
        desc = "Amostra de 10"
    elif opcao == '3':
        df_validar = df_fortes.copy()
        desc = f"FORTES ({len(df_fortes)} casos)"
    elif opcao == '4':
        df_validar = df_fortes.head(10)
        desc = "Amostra de 10 FORTES"
    elif opcao == '5':
        df_validar = df_criticos.copy()
        desc = f"CRÍTICOS ({len(df_criticos)} casos)"
    else:
        print("❌ Opção inválida!")
        return
    
    print(f"\n✓ Validando: {desc}")
    print(f"   Tempo estimado: ~{len(df_validar) * 0.2:.0f} minutos")
    
    # Validação
    print("\n" + "=" * 80)
    print("INICIANDO VALIDAÇÕES...")
    print("=" * 80)
    
    resultados = []
    inicio = datetime.now()
    
    for i, (idx, caso) in enumerate(df_validar.iterrows()):
        print(f"\n[{i + 1}/{len(df_validar)}] {caso['nome']}")
        print(f"   BO Desap: {caso['bo_desaparecimento']} | BO Morte: {caso['bo_morte']}")
        print(f"   Intervalo: {caso['dias_entre_eventos']} dias | Força: {caso['forca_correlacao']}")
        
        resultado = validar_caso(caso)
        
        # Adiciona dados do caso
        resultado_completo = {
            'chave_pessoa': caso['chave_pessoa'],
            'nome': caso['nome'],
            'data_nascimento': caso['data_nascimento'],
            'nome_mae': caso['nome_mae'],
            'nome_pai': caso['nome_pai'],
            'numero_rg': caso['numero_rg'],
            'tem_transtorno_psiquiatrico': caso.get('tem_transtorno_psiquiatrico', 'Não informado'),
            'tipo_transtorno': caso.get('tipo_transtorno', 'N/A'),
            'bo_desaparecimento': caso['bo_desaparecimento'],
            'bo_morte': caso['bo_morte'],
            'dias_entre': caso['dias_entre_eventos'],
            'tipo_morte': caso['tipo_morte'],
            'forca_correlacao': caso['forca_correlacao'],
            'validacao': resultado,
            'timestamp': datetime.now().isoformat()
        }
        
        resultados.append(resultado_completo)
        
        # Mostra resultado
        if 'erro' in resultado:
            print(f"   ⚠️ Erro: {resultado['erro']}")
        elif 'correlacao_valida' in resultado:
            valida = resultado['correlacao_valida']
            conf = resultado.get('confianca', 0)
            status = "✅ CONFIRMADA" if valida else "❌ REJEITADA"
            print(f"   {status} (confiança: {conf}%)")
        
        # Salva progresso a cada 10
        if len(resultados) % 10 == 0:
            salvar_parcial(resultados)
            tempo_decorrido = (datetime.now() - inicio).total_seconds() / 60
            tempo_por_caso = tempo_decorrido / len(resultados)
            tempo_restante = tempo_por_caso * (len(df_validar) - len(resultados))
            print(f"\n   💾 Progresso salvo | Tempo restante: ~{tempo_restante:.0f} min")
    
    # Salva final
    print("\n" + "=" * 80)
    print("SALVANDO RESULTADOS FINAIS...")
    print("=" * 80)
    
    salvar_final(resultados, df_validar, desc)
    
    tempo_total = (datetime.now() - inicio).total_seconds() / 60
    print(f"\n✅ CONCLUÍDO em {tempo_total:.1f} minutos!")
    print(f"   Velocidade: {tempo_total/len(resultados):.1f} min/caso")


def salvar_parcial(resultados):
    """Salva progresso"""
    arquivo = Path('output/validacao_parcial.json')
    arquivo.parent.mkdir(exist_ok=True)
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)


def salvar_final(resultados, df_original, descricao):
    """Salva resultados finais em Excel"""
    
    arquivo = Path('output/validacao_qwen3_otimizada.xlsx')
    arquivo.parent.mkdir(exist_ok=True)
    
    # Prepara dados
    dados = []
    
    for r in resultados:
        val = r['validacao']
        
        linha = {
            'nome': r['nome'],
            'data_nascimento': r['data_nascimento'],
            'nome_mae': r['nome_mae'],
            'nome_pai': r['nome_pai'],
            'rg': r['numero_rg'],
            'tem_transtorno_psiquiatrico': r.get('tem_transtorno_psiquiatrico', 'Não informado'),
            'tipo_transtorno': r.get('tipo_transtorno', 'N/A'),
            'bo_desaparecimento': r['bo_desaparecimento'],
            'bo_morte': r['bo_morte'],
            'dias_entre': r['dias_entre'],
            'tipo_morte': r['tipo_morte'],
            'forca_correlacao': r['forca_correlacao']
        }
        
        if 'erro' not in val:
            linha['mesma_pessoa'] = val.get('mesma_pessoa')
            linha['correlacao_valida'] = val.get('correlacao_valida')
            linha['confianca'] = val.get('confianca')
            linha['justificativa'] = val.get('justificativa', '')
            
            # Dados conferem
            dados_conf = val.get('dados_conferem', {})
            linha['data_nasc_ok'] = dados_conf.get('data_nasc')
            linha['mae_ok'] = dados_conf.get('mae')
            linha['pai_ok'] = dados_conf.get('pai')
            linha['rg_ok'] = dados_conf.get('rg')
        else:
            linha['erro'] = val.get('erro')
        
        dados.append(linha)
    
    df_result = pd.DataFrame(dados)
    
    # Filtra
    df_confirmadas = df_result[df_result['correlacao_valida'] == True].copy()
    df_rejeitadas = df_result[df_result['correlacao_valida'] == False].copy()
    
    # Ordena
    df_confirmadas = df_confirmadas.sort_values('confianca', ascending=False)
    df_rejeitadas = df_rejeitadas.sort_values('confianca', ascending=True)
    
    # Salva Excel
    with pd.ExcelWriter(arquivo, engine='openpyxl') as writer:
        df_result.to_excel(writer, sheet_name='Todas Validações', index=False)
        df_confirmadas.to_excel(writer, sheet_name='CONFIRMADAS', index=False)
        df_rejeitadas.to_excel(writer, sheet_name='REJEITADAS', index=False)
        
        # Stats
        stats = {
            'Métrica': [
                'Total Validados',
                'Correlações CONFIRMADAS',
                'Correlações REJEITADAS',
                'Taxa Confirmação (%)',
                'Confiança Média (confirmadas)',
                'Confiança Média (rejeitadas)',
                'Mesma Pessoa (todos)',
                'Descrição'
            ],
            'Valor': [
                len(resultados),
                len(df_confirmadas),
                len(df_rejeitadas),
                len(df_confirmadas) / len(resultados) * 100 if resultados else 0,
                df_confirmadas['confianca'].mean() if len(df_confirmadas) > 0 else 0,
                df_rejeitadas['confianca'].mean() if len(df_rejeitadas) > 0 else 0,
                df_result['mesma_pessoa'].sum() if 'mesma_pessoa' in df_result else 0,
                descricao
            ]
        }
        
        pd.DataFrame(stats).to_excel(writer, sheet_name='Estatísticas', index=False)
    
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Total validados: {len(resultados)}")
    print(f"   CONFIRMADAS: {len(df_confirmadas)} ({len(df_confirmadas)/len(resultados)*100:.1f}%)")
    print(f"   REJEITADAS: {len(df_rejeitadas)}")
    print(f"   Confiança média (confirmadas): {df_confirmadas['confianca'].mean():.1f}%" if len(df_confirmadas) > 0 else "")
    print(f"\n   Arquivo: {arquivo}")


if __name__ == "__main__":
    main()
