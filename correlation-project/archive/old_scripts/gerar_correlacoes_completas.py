"""
Gera correlações temporais COM DADOS DE IDENTIFICAÇÃO COMPLETOS
Inclui: Data Nascimento, Nome Mãe, Nome Pai, RG
"""

import pandas as pd
from pathlib import Path
from datetime import datetime


def gerar_correlacoes_com_identificacao():
    print("=" * 80)
    print("GERANDO CORRELAÇÕES COM DADOS DE IDENTIFICAÇÃO COMPLETOS")
    print("=" * 80)
    
    # Carrega dataset
    arquivo_dataset = Path('output/dataset_unificado.xlsx')
    print(f"\n📂 Carregando dataset: {arquivo_dataset}")
    df = pd.read_excel(arquivo_dataset)
    print(f"   ✓ {len(df)} registros carregados")
    
    # Filtra apenas grupo-alvo (desaparecimento, cadaver, homicidio)
    df_alvo = df[df['natureza_alvo'].isin(['DESAPARECIMENTO', 'CADAVER', 'HOMICIDIO'])].copy()
    print(f"   ✓ {len(df_alvo)} registros do grupo-alvo")
    
    # Converte datas (usa data_fato_dt que já está convertida)
    df_alvo['data_fato_dt'] = pd.to_datetime(df_alvo['data_fato_dt'], errors='coerce')
    
    print("\n🔍 Buscando correlações temporais...")
    print("   Critério: Desaparecimento seguido de Cadáver/Homicídio")
    
    correlacoes = []
    
    # Agrupa por pessoa
    pessoas = df_alvo['chave_pessoa'].unique()
    print(f"   Total de pessoas únicas: {len(pessoas)}")
    
    for idx, chave_pessoa in enumerate(pessoas):
        if (idx + 1) % 1000 == 0:
            print(f"   Processando... {idx + 1}/{len(pessoas)}")
        
        # Registros da pessoa
        registros_pessoa = df_alvo[df_alvo['chave_pessoa'] == chave_pessoa].sort_values('data_fato_dt')
        
        # Busca desaparecimentos
        desaparecimentos = registros_pessoa[registros_pessoa['natureza_alvo'] == 'DESAPARECIMENTO']
        
        # Busca mortes (cadaver ou homicidio)
        mortes = registros_pessoa[registros_pessoa['natureza_alvo'].isin(['CADAVER', 'HOMICIDIO'])]
        
        # Para cada desaparecimento, busca mortes posteriores
        for _, desap in desaparecimentos.iterrows():
            mortes_posteriores = mortes[mortes['data_fato_dt'] > desap['data_fato_dt']]
            
            for _, morte in mortes_posteriores.iterrows():
                # Calcula intervalo
                dias_entre = (morte['data_fato_dt'] - desap['data_fato_dt']).days
                
                # Verifica se há eventos intermediários
                eventos_intermediarios = registros_pessoa[
                    (registros_pessoa['data_fato_dt'] > desap['data_fato_dt']) &
                    (registros_pessoa['data_fato_dt'] < morte['data_fato_dt'])
                ]
                tem_intermediario = len(eventos_intermediarios) > 0
                
                # Classifica força da correlação
                if dias_entre <= 30:
                    forca = 'FORTE'
                elif dias_entre <= 90:
                    forca = 'MÉDIA'
                else:
                    forca = 'FRACA'
                
                # DADOS COMPLETOS DE IDENTIFICAÇÃO
                correlacao = {
                    # Identificação da Pessoa
                    'chave_pessoa': chave_pessoa,
                    'nome': desap['nome'],
                    'data_nascimento': desap['data_nascimento'],
                    'ano_nascimento': desap['ano_nascimento'],
                    'nome_mae': desap['nome_mae'],
                    'nome_mae_normalizado': desap['nome_mae_normalizado'],
                    'nome_pai': desap['nome_pai'],
                    'numero_rg': desap['numero_identidade'],
                    'orgao_rg': desap['orgao_expedidor_identidade'],
                    'uf_rg': desap['uf_identidade'],
                    'sexo': desap['sexo'],
                    'raca': desap['raca_padronizada'],
                    
                    # Transtorno Psiquiátrico
                    'tem_transtorno_psiquiatrico': desap['tem_transtorno_psiquiatrico'],
                    'tipo_transtorno': desap['tipo_transtorno'],
                    'evidencia_transtorno': desap['evidencia_transtorno'],
                    
                    # Desaparecimento
                    'data_desaparecimento': desap['data_fato_dt'].strftime('%Y-%m-%d'),
                    'bo_desaparecimento': desap['chave_ocorrencia'],
                    'cidade_desaparecimento': desap['cidade_ra'],
                    'unidade_desaparecimento': desap['unidade_registro'],
                    'historico_desaparecimento': desap['historico_limpo'],
                    
                    # Morte
                    'data_morte': morte['data_fato_dt'].strftime('%Y-%m-%d'),
                    'tipo_morte': morte['natureza_alvo'],
                    'bo_morte': morte['chave_ocorrencia'],
                    'cidade_morte': morte['cidade_ra'],
                    'unidade_morte': morte['unidade_registro'],
                    'historico_morte': morte['historico_limpo'],
                    
                    # Análise Temporal
                    'dias_entre_eventos': dias_entre,
                    'tem_evento_intermediario': tem_intermediario,
                    'forca_correlacao': forca,
                    'explicacao': f"Pessoa desapareceu em {desap['data_fato_dt'].strftime('%d/%m/%Y')} "
                                 f"e {morte['natureza_alvo'].lower()} encontrado em "
                                 f"{morte['data_fato_dt'].strftime('%d/%m/%Y')} ({dias_entre} dias depois)"
                }
                
                correlacoes.append(correlacao)
    
    print(f"\n✅ Total de correlações encontradas: {len(correlacoes)}")
    
    # Converte para DataFrame
    df_correlacoes = pd.DataFrame(correlacoes)
    
    # Estatísticas
    print("\n📊 ESTATÍSTICAS:")
    print(f"   FORTES (0-30 dias): {len(df_correlacoes[df_correlacoes['forca_correlacao'] == 'FORTE'])}")
    print(f"   MÉDIAS (31-90 dias): {len(df_correlacoes[df_correlacoes['forca_correlacao'] == 'MÉDIA'])}")
    print(f"   FRACAS (>90 dias): {len(df_correlacoes[df_correlacoes['forca_correlacao'] == 'FRACA'])}")
    
    # Ordena por data
    df_correlacoes = df_correlacoes.sort_values('data_desaparecimento', ascending=False)
    
    # Separa por força
    df_fortes = df_correlacoes[df_correlacoes['forca_correlacao'] == 'FORTE'].copy()
    df_medias = df_correlacoes[df_correlacoes['forca_correlacao'] == 'MÉDIA'].copy()
    df_fracas = df_correlacoes[df_correlacoes['forca_correlacao'] == 'FRACA'].copy()
    
    # Salva arquivo Excel
    arquivo_saida = Path('output/correlacoes_completas_com_identificacao.xlsx')
    arquivo_saida.parent.mkdir(exist_ok=True)
    
    print(f"\n💾 Salvando arquivo: {arquivo_saida}")
    
    with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
        # Todas as correlações
        df_correlacoes.to_excel(writer, sheet_name='Todas Correlações', index=False)
        
        # Por força
        df_fortes.to_excel(writer, sheet_name='Correlações FORTES', index=False)
        df_medias.to_excel(writer, sheet_name='Correlações MÉDIAS', index=False)
        df_fracas.to_excel(writer, sheet_name='Correlações FRACAS', index=False)
        
        # Estatísticas detalhadas
        stats = {
            'Métrica': [
                'Total de Correlações',
                'Correlações FORTES (0-30 dias)',
                'Correlações MÉDIAS (31-90 dias)',
                'Correlações FRACAS (>90 dias)',
                'Média de dias entre eventos',
                'Menor intervalo (dias)',
                'Maior intervalo (dias)',
                'Com dados completos de identificação'
            ],
            'Valor': [
                len(df_correlacoes),
                len(df_fortes),
                len(df_medias),
                len(df_fracas),
                df_correlacoes['dias_entre_eventos'].mean(),
                df_correlacoes['dias_entre_eventos'].min(),
                df_correlacoes['dias_entre_eventos'].max(),
                len(df_correlacoes[df_correlacoes['numero_rg'].notna()])
            ]
        }
        
        df_stats = pd.DataFrame(stats)
        df_stats.to_excel(writer, sheet_name='Estatísticas', index=False)
    
    print(f"   ✓ Arquivo salvo com {len(df_correlacoes)} correlações")
    print(f"   ✓ {len(df_correlacoes.columns)} colunas incluindo TODOS os dados de identificação")
    
    # Mostra amostra dos dados de identificação
    print("\n👥 AMOSTRA DE DADOS DE IDENTIFICAÇÃO (primeiros 3 casos):")
    print("=" * 80)
    
    for idx, caso in df_correlacoes.head(3).iterrows():
        print(f"\nCASO {idx + 1}:")
        print(f"   Nome: {caso['nome']}")
        print(f"   Data Nascimento: {caso['data_nascimento']}")
        print(f"   Nome Mãe: {caso['nome_mae']}")
        print(f"   Nome Pai: {caso['nome_pai']}")
        print(f"   RG: {caso['numero_rg']} - {caso['orgao_rg']}/{caso['uf_rg']}")
        print(f"   Intervalo: {caso['dias_entre_eventos']} dias")
        print(f"   Força: {caso['forca_correlacao']}")
    
    print("\n" + "=" * 80)
    print("✅ PROCESSO CONCLUÍDO!")
    print("=" * 80)
    print(f"Arquivo gerado: {arquivo_saida}")
    print("\nAgora a IA terá TODOS os dados para validar a identidade:")
    print("  ✅ Data de Nascimento")
    print("  ✅ Nome da Mãe")
    print("  ✅ Nome do Pai")
    print("  ✅ RG + Órgão Expedidor + UF")
    print("  ✅ Sexo e Cor da Pele")
    print("  ✅ Históricos completos de ambos os BOs")


if __name__ == "__main__":
    gerar_correlacoes_com_identificacao()
