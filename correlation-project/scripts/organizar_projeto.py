"""
═══════════════════════════════════════════════════════════════════════════════
ORGANIZAÇÃO DE ARQUIVOS DO PROJETO
═══════════════════════════════════════════════════════════════════════════════

DESCRIÇÃO:
    Move arquivos temporários/antigos para pasta archive/
    Mantém apenas scripts essenciais e documentação

ESTRUTURA APÓS ORGANIZAÇÃO:
    
    correlation-project/
    ├── scripts/           # Scripts principais organizados
    │   ├── validar_com_ia.py
    │   ├── monitor_progresso.py
    │   └── ...
    ├── output/            # Resultados finais
    │   ├── correlacoes_unicas_deduplicadas.xlsx
    │   ├── validacao_progresso.xlsx
    │   └── RELATORIO_VALIDACAO_FINAL.xlsx
    ├── docs/              # Documentação
    │   ├── ARQUITETURA.md
    │   └── COMO_USAR.md
    └── archive/           # Arquivos temporários/antigos
        ├── old_scripts/
        └── temp_files/

═══════════════════════════════════════════════════════════════════════════════
"""

import shutil
from pathlib import Path


# Arquivos temporários para mover
ARQUIVOS_TEMPORARIOS = [
    'EXECUTAR_VALIDACAO.py',
    'VER_PROGRESSO.py',
    'VER_PROGRESSO_SIMPLES.py',
    'COMO_EXECUTAR.md',
    'check_status.py',
    'verificar_duplicados.py',
    'validar_qwen3_otimizado.py',
    'testar_modelo.py',
    'ver_relatorio_completo.py',
    'remover_duplicatas.py',
    'gerar_correlacoes_completas.py'
]


def criar_estrutura():
    """Cria estrutura de pastas organizada"""
    
    print("\n📁 Criando estrutura de pastas...")
    
    pastas = [
        'scripts',
        'output',
        'docs',
        'archive/old_scripts',
        'archive/temp_files'
    ]
    
    for pasta in pastas:
        Path(pasta).mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {pasta}/")


def mover_arquivos_temporarios():
    """Move arquivos temporários para archive/"""
    
    print("\n🗂️  Movendo arquivos temporários...")
    
    movidos = 0
    for arquivo in ARQUIVOS_TEMPORARIOS:
        origem = Path(arquivo)
        if origem.exists():
            destino = Path('archive/old_scripts') / arquivo
            try:
                shutil.move(str(origem), str(destino))
                print(f"   ✓ {arquivo} → archive/old_scripts/")
                movidos += 1
            except Exception as e:
                print(f"   ⚠ Erro ao mover {arquivo}: {e}")
    
    print(f"\n   Total movido: {movidos} arquivos")


def mover_documentacao():
    """Move documentação para docs/"""
    
    print("\n📄 Organizando documentação...")
    
    docs = ['ARQUITETURA.md', 'README.md']
    
    for doc in docs:
        origem = Path(doc)
        if origem.exists():
            destino = Path('docs') / doc
            try:
                if not destino.exists():
                    shutil.copy(str(origem), str(destino))
                    print(f"   ✓ {doc} → docs/")
            except Exception as e:
                print(f"   ⚠ Erro: {e}")


def listar_arquivos_raiz():
    """Lista arquivos que sobraram na raiz"""
    
    print("\n📋 Arquivos restantes na raiz:")
    
    raiz = Path('.')
    arquivos = [f for f in raiz.iterdir() if f.is_file() and not f.name.startswith('.')]
    
    if arquivos:
        for arq in sorted(arquivos):
            print(f"   • {arq.name}")
    else:
        print("   ✓ Raiz limpa!")


def criar_readme_principal():
    """Cria README.md principal atualizado"""
    
    conteudo = """# Projeto de Correlação Desaparecimento → Morte

## 🎯 Objetivo

Validar correlações entre boletins de desaparecimento e morte usando inteligência artificial local (Ollama).

## 📁 Estrutura do Projeto

```
correlation-project/
├── scripts/              # Scripts principais
│   ├── validar_com_ia.py      # Validação com IA
│   └── monitor_progresso.py   # Monitor em tempo real
├── output/               # Resultados
│   ├── correlacoes_unicas_deduplicadas.xlsx
│   ├── validacao_progresso.xlsx
│   └── RELATORIO_VALIDACAO_FINAL.xlsx
├── docs/                 # Documentação
│   ├── ARQUITETURA.md         # Arquitetura completa do sistema
│   └── COMO_USAR.md           # Guia de uso detalhado
└── archive/              # Arquivos antigos
```

## 🚀 Como Usar

### 1. Pré-requisitos

```bash
# Instalar Ollama
https://ollama.ai

# Baixar modelo português
ollama pull qwen2.5-ptbr:7b

# Verificar instalação
ollama list
```

### 2. Executar Validação

```bash
# Terminal 1: Rodar validação
python scripts/validar_com_ia.py

# Terminal 2: Monitorar progresso (opcional)
python scripts/monitor_progresso.py
```

### 3. Ver Resultados

Após conclusão, abrir: `output/RELATORIO_VALIDACAO_FINAL.xlsx`

## ⚙️ Configurações

Edite `scripts/validar_com_ia.py`:

- `MODELO`: Modelo a usar (padrão: qwen2.5-ptbr:7b)
- `TEMPERATURA`: 0.1 (mais determinístico) a 1.0 (mais criativo)
- `TIMEOUT`: Tempo máximo por caso (padrão: 60s)

## 📊 Dados

- **Entrada**: 86 casos FORTES (0-30 dias entre eventos)
- **Saída**: ~68-70 confirmações esperadas (80% taxa)
- **Tempo**: ~17-20 minutos total

## 📖 Documentação Completa

Ver: `docs/ARQUITETURA.md` e `docs/COMO_USAR.md`

## ⚠️ Troubleshooting

**Problema**: Validação trava

**Solução**: Script salva progresso automaticamente. Apenas execute novamente:
```bash
python scripts/validar_com_ia.py
```

**Problema**: Modelo muito lento

**Solução**: Use modelo menor (7B em vez de 14B)

## 🔧 Manutenção

Para reorganizar arquivos temporários:
```bash
python scripts/organizar_projeto.py
```
"""
    
    Path('README.md').write_text(conteudo, encoding='utf-8')
    print("\n✅ README.md principal criado!")


def main():
    """Executa organização"""
    
    print("=" * 70)
    print("ORGANIZAÇÃO DO PROJETO")
    print("=" * 70)
    
    criar_estrutura()
    mover_arquivos_temporarios()
    mover_documentacao()
    criar_readme_principal()
    listar_arquivos_raiz()
    
    print("\n" + "=" * 70)
    print("✅ ORGANIZAÇÃO CONCLUÍDA!")
    print("=" * 70)
    print("\n📁 Estrutura:")
    print("   scripts/    → Scripts principais")
    print("   output/     → Resultados")
    print("   docs/       → Documentação")
    print("   archive/    → Arquivos antigos\n")


if __name__ == "__main__":
    main()
