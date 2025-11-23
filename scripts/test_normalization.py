"""
Script de exemplo para testar funções de normalização.
"""

from utils.normalization import normalize_name, normalize_text, normalize_document
from utils.key_generation import generate_composite_key, generate_phonetic_key
from utils.validation import validate_cpf


def test_normalization():
    """Testa funções de normalização."""
    print("=== Teste de Normalização ===\n")
    
    # Testa normalização de nomes
    nomes = [
        "Dr. João da Silva Jr.",
        "Maria José dos Santos",
        "José Carlos de Souza Filho",
    ]
    
    print("Normalização de Nomes:")
    for nome in nomes:
        normalizado = normalize_name(nome)
        print(f"  '{nome}' -> '{normalizado}'")
    
    # Testa normalização de documentos
    print("\nNormalização de Documentos:")
    documentos = [
        "123.456.789-00",
        "12.345.678-9",
        "MG-12.345.678",
    ]
    
    for doc in documentos:
        normalizado = normalize_document(doc)
        print(f"  '{doc}' -> '{normalizado}'")
    
    # Testa validação de CPF
    print("\nValidação de CPF:")
    cpfs = [
        "123.456.789-09",
        "111.111.111-11",  # Inválido
        "12345678909",
    ]
    
    for cpf in cpfs:
        valido = validate_cpf(cpf)
        print(f"  {cpf}: {'Válido' if valido else 'Inválido'}")


def test_key_generation():
    """Testa geração de chaves."""
    print("\n=== Teste de Geração de Chaves ===\n")
    
    # Dados de exemplo
    pessoa1 = {
        "nome": "João da Silva",
        "data_nascimento": "1990-01-01",
        "cpf": "12345678909",
        "nome_mae": "Maria da Silva",
    }
    
    pessoa2 = {
        "nome": "Joao da Silva",  # Nome similar
        "data_nascimento": "1990-01-01",
        "cpf": "12345678909",
        "nome_mae": "Maria da Silva",
    }
    
    # Gera chaves compostas
    key1 = generate_composite_key(pessoa1)
    key2 = generate_composite_key(pessoa2)
    
    print("Chaves Compostas:")
    print(f"  Pessoa 1: {key1}")
    print(f"  Pessoa 2: {key2}")
    print(f"  São iguais: {key1 == key2}")
    
    # Gera chaves fonéticas
    print("\nChaves Fonéticas:")
    nomes = ["João da Silva", "Joao da Silva", "Jose Carlos"]
    for nome in nomes:
        key = generate_phonetic_key(nome)
        print(f"  '{nome}' -> {key}")


def main():
    """Executa testes."""
    test_normalization()
    test_key_generation()


if __name__ == "__main__":
    main()
