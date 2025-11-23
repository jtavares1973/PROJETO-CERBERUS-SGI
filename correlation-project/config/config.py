"""Configurações centralizadas do projeto"""
from pathlib import Path

# Diretórios
BASE_DIR = Path(__file__).parent.parent
RAW_CSV_DIR = BASE_DIR / "raw_csv"
OUTPUT_DIR = BASE_DIR / "output"

# Mapeamento de campos (sem caracteres especiais, sem pontos, snake_case)
FIELD_MAPPING = {
    # Campos de identificação
    'ï»¿Sequencial': 'sequencial',
    'Sequencial': 'sequencial',
    'Cd.Envolvido': 'codigo_envolvido',
    'Cd.Unidade Registro': 'codigo_unidade_registro',
    'Cd.Unidade Apuração': 'codigo_unidade_apuracao',
    'Cd.Unidade ApuraÃ§Ã£o': 'codigo_unidade_apuracao',
    'Cd.Natureza': 'codigo_natureza',
    'Cd.Ocorrência': 'codigo_ocorrencia',
    'Cd.OcorrÃªncia': 'codigo_ocorrencia',
    'COD_OCORRÊNCIA_IML_PESSOA': 'codigo_iml_pessoa',
    'COD_OCORRÃNCIA_IML_PESSOA': 'codigo_iml_pessoa',
    'Número': 'numero_ocorrencia',
    'NÃºmero': 'numero_ocorrencia',
    'Aditamento': 'numero_aditamento',
    
    # Campos de pessoa
    'Nome envolvido': 'nome',
    'Mãe do envolvido': 'nome_mae',
    'MÃ£e do envolvido': 'nome_mae',
    'Pai do envolvido': 'nome_pai',
    'Sexo': 'sexo_original',
    'Sexo Padronizado': 'sexo',
    'Nascimento': 'data_nascimento',
    'Idade ocorrência': 'idade_ocorrencia',
    'Idade ocorrÃªncia': 'idade_ocorrencia',
    
    # Campos de natureza
    'Natureza': 'natureza',
    'Natureza Padronizada': 'natureza_padronizada',
    'Natureza do Envolvido': 'natureza_envolvido',
    'Envolvimento': 'envolvimento',
    'Envolvimento Padronizado': 'envolvimento_padronizado',
    'Crime Tentado (S/N)?': 'crime_tentado',
    'Flagrante (S/N)?': 'flagrante',
    
    # Campos de data
    'Data do Registro': 'data_registro',
    'Data Início do Fato': 'data_fato',
    'Data InÃ­cio do Fato': 'data_fato',
    'Ano do Fato': 'ano_fato',
    'Ano de Registro': 'ano_registro',
    
    # Campos de local
    'Cidade com RA': 'cidade_ra',
    'Unidade Policial de Registro': 'unidade_registro',
    'Unidade Policial de Apuração': 'unidade_apuracao',
    'Unidade Policial de ApuraÃ§Ã£o': 'unidade_apuracao',
    
    # Campos narrativos
    'Histórico': 'historico',
    'HistÃ³rico': 'historico',
    
    # Campos IML
    'Possui laudo IML': 'possui_laudo_iml',
    'Encaminhado ao IML': 'encaminhado_iml',
    'Pessoa Raça IML': 'raca_iml',
    'Pessoa RaÃ§a IML': 'raca_iml',
    'Pessoa Raça Padronizada': 'raca_padronizada',
    'Pessoa RaÃ§a Padronizada': 'raca_padronizada',
    'Estado Civil (Laudo IML)': 'estado_civil_iml',
    'Estado Civil (Millenium)': 'estado_civil_sistema',
    
    # Campos de contato
    'Pessoa localizada': 'pessoa_localizada',
    'Telefone Residencial': 'telefone_residencial',
    'Telefone Celular': 'telefone_celular',
    'Morador de Rua': 'morador_rua',
    
    # Campos de documentação
    'Identidade': 'numero_identidade',
    'Órgão Expedidor Identidade': 'orgao_expedidor_identidade',
    'ÃrgÃ£o Expedidor Identidade': 'orgao_expedidor_identidade',
    'UF Identidade': 'uf_identidade',
    'Nacionalidade': 'nacionalidade',
    'Grau de Instrução': 'grau_instrucao',
    'Grau de InstruÃ§Ã£o': 'grau_instrucao',
    
    # Campos de gênero e identidade
    'Orientação de Gênero': 'orientacao_genero',
    'OrientaÃ§Ã£o de GÃªnero': 'orientacao_genero',
    'Identidade de Gênero': 'identidade_genero',
    'Identidade de GÃªnero': 'identidade_genero',
    'Nome Social': 'nome_social',
    
    # Campos de faixa etária
    'Faixa etária padronizada': 'faixa_etaria_padronizada',
    'Faixa etÃ¡ria padronizada': 'faixa_etaria_padronizada',
    'Faixa etária Millenium': 'faixa_etaria_sistema',
    'Faixa etÃ¡ria Millenium': 'faixa_etaria_sistema',
    
    # Campos de vínculo
    'Pessoa vinculada': 'pessoa_vinculada',
    'Tipo vínculo envolvido': 'tipo_vinculo',
    'Tipo vÃ­nculo envolvido': 'tipo_vinculo',
}

# Palavras-chave para detecção de transtornos psiquiátricos
PSYCHIATRIC_KEYWORDS = [
    # Termos gerais
    'transtorno mental',
    'problema psiquiátrico',
    'doença mental',
    'distúrbio mental',
    'tratamento psiquiátrico',
    'acompanhamento psiquiátrico',
    'internação psiquiátrica',
    'hospital psiquiátrico',
    
    # Diagnósticos específicos
    'esquizofrenia',
    'bipolar',
    'transtorno bipolar',
    'depressão',
    'depressivo',
    'ansiedade',
    'transtorno de ansiedade',
    'psicose',
    'psicótico',
    'surto psicótico',
    'crise psicótica',
    'paranoia',
    'paranoide',
    'alucinação',
    'delírio',
    
    # Comportamentos
    'tentativa de suicídio',
    'ideação suicida',
    'automutilação',
    'alteração de comportamento',
    'comportamento agressivo',
    'surto',
    'crise',
    
    # Medicamentos
    'medicação controlada',
    'medicamento psiquiátrico',
    'antipsicótico',
    'antidepressivo',
    'estabilizador de humor',
    'ansiolítico',
    'rivotril',
    'haldol',
    'olanzapina',
    'risperidona',
    'quetiapina',
    'clozapina',
    'fluoxetina',
    'sertralina',
    'paroxetina',
    'lítio',
    
    # CID
    'cid f',
    'cid-10 f',
    'f20',  # esquizofrenia
    'f31',  # bipolar
    'f32',  # depressão
    'f33',  # depressão recorrente
    'f41',  # ansiedade
    'f60',  # personalidade
]

# Classificações finais possíveis
CLASSIFICACAO_DESAPARECIDO_SIMPLES = "Desaparecido sem desfecho"
CLASSIFICACAO_DESAPARECIDO_LOCALIZADO = "Desaparecido localizado vivo"
CLASSIFICACAO_DESAPARECIDO_MORTO = "Desaparecido encontrado morto"
CLASSIFICACAO_DESAPARECIDO_VITIMA_HOMICIDIO = "Desaparecido vítima de homicídio"
CLASSIFICACAO_CADAVER_SEM_DESAPARECIMENTO = "Cadáver sem registro de desaparecimento"
CLASSIFICACAO_HOMICIDIO_SEM_DESAPARECIMENTO = "Homicídio sem registro de desaparecimento"

# Tipos de natureza
NATUREZA_DESAPARECIMENTO = ['DESAPARECIMENTO DE PESSOA', '73_DESAPARECIMENTO DE PESSOA']
NATUREZA_LOCALIZACAO_CADAVER = ['LOCALIZAÇÃO DE CADÁVER', 'LOCALIZACAO DE CADAVER']
NATUREZA_HOMICIDIO = ['HOMICÍDIO', 'HOMICIDIO', 'LATROCÍNIO', 'LATROCINIO']
