## ROADMAP (CLEANUP) — tornar o projeto mais “clean” sem reescrever

### Objetivo
Reduzir **redundância** (muitos scripts com a mesma função), deixar **1 caminho oficial** de execução e tornar a documentação **consistente com o código ativo**, sem “detonar” o histórico.

---

### Estado atual (o que é oficial hoje)
O que está **ativo e suportado** no dia a dia está principalmente em:
- `etl/` (ETL/padronização/enriquecimento/detecção)
- `utils/` (chaves, normalização, detector psiquiátrico, export Excel)
- `scripts/` (validação com IA, monitor, config)

**Fluxo oficial atual (mínimo e operacional):**
1. (Pré-requisito) Ter a planilha de entrada: `output/correlacoes_unicas_deduplicadas.xlsx` (aba `FORTES - Únicas`)
2. Validar com IA:
   - `python scripts/validar_com_ia.py`
   - ou `python scripts/validar_com_deteccao_auto.py` (autoajuste por hardware)
3. (Opcional) Monitorar:
   - `python scripts/monitor_progresso.py`
4. Saídas:
   - `output/validacao_progresso.xlsx`
   - `output/RELATORIO_VALIDACAO_FINAL.xlsx`

**Importante:** as etapas de “gerar correlações” e “deduplicar” existem como histórico em `archive/old_scripts/` e devem ser tratadas como **legado** até serem promovidas/reestruturadas.

---

### Fluxo alvo (ponta-a-ponta, em um único caminho)
Objetivo de médio prazo: ter um fluxo oficial completo:
1. ETL (`dataset_unificado.xlsx`)
2. Geração de correlações (temporal por `chave_pessoa`)
3. Deduplicação
4. Validação com IA
5. Relatório final

---

### Política de organização (para acabar com redundância)
- **`scripts/`**: somente *entrypoints* oficiais (o que o usuário executa).
- **`etl/`, `utils/`**: somente lógica reutilizável (sem “main” gigante, sem duplicação).
- **`archive/`**: somente histórico (não referenciar como “principal” na documentação).
- **Documentação**: `docs/` é a fonte canônica; arquivos duplicados na raiz devem virar ponteiro/link.

---

### Próximos passos recomendados (ordem segura)
1. **(agora)** Unificar docs e declarar fluxo oficial (este arquivo + ajustes em `docs/`).
2. Consolidar entrypoints: 1 comando por etapa (ou 1 CLI com subcomandos).
3. Promover scripts necessários do legado para o caminho oficial (correlação/dedup), ou reimplementar mínimo no lugar certo.
4. Criar “contratos” de dados (colunas obrigatórias/invariantes) e validar antes de salvar artefatos.

