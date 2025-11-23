# 🚀 PASSO A PASSO: Criar Repositório no GitHub

## ✅ Você Acabou de Fazer (Neste PC)

```bash
✅ git init                  # Repositório local criado
✅ git add .                 # 68 arquivos adicionados
✅ git commit -m "..."       # Commit inicial feito
```

---

## 📋 Próximos Passos

### **1️⃣ CRIAR CONTA NO GITHUB** (se não tiver)

1. Abrir navegador: <https://github.com>
2. Clicar em **"Sign up"** (Cadastrar)
3. Preencher:
   - Email
   - Password (senha forte)
   - Username (seu nome de usuário)
4. Verificar email
5. ✅ Conta criada!

---

### **2️⃣ CRIAR REPOSITÓRIO NO GITHUB**

#### Via Interface Web (RECOMENDADO para iniciantes):

1. **Fazer login** no GitHub: <https://github.com/login>

2. **Clicar no "+" no canto superior direito** → **"New repository"**

3. **Preencher:**
   ```
   Repository name: correlacao-desaparecimento-ia
   Description: Sistema de validação IA para correlação desaparecimento/cadáver
   
   Visibilidade:
   ⚪ Public (qualquer um vê) 
   🔘 Private (só você vê)  ← RECOMENDADO (dados sensíveis)
   
   ❌ NÃO marcar "Add README" (já temos)
   ❌ NÃO marcar ".gitignore" (já temos)
   ❌ NÃO marcar "license" (opcional)
   ```

4. **Clicar em "Create repository"** (botão verde)

5. **COPIAR o URL** que aparecer (exemplo):
   ```
   https://github.com/SEU_USUARIO/correlacao-desaparecimento-ia.git
   ```

---

### **3️⃣ CONECTAR LOCAL COM GITHUB**

Voltar para o **terminal** neste PC:

```bash
# 1. Conectar repositório local com GitHub
cd /d/___MeusScripts/LangChain

git remote add origin https://github.com/SEU_USUARIO/correlacao-desaparecimento-ia.git

# 2. Verificar conexão
git remote -v
# Deve mostrar:
# origin  https://github.com/SEU_USUARIO/... (fetch)
# origin  https://github.com/SEU_USUARIO/... (push)

# 3. Enviar código para GitHub
git push -u origin main
```

**Se pedir autenticação:**
- Username: seu nome de usuário GitHub
- Password: usar **Personal Access Token** (não senha normal)

---

### **4️⃣ CRIAR PERSONAL ACCESS TOKEN** (se necessário)

GitHub não aceita senha normal no terminal. Precisa de token:

1. **GitHub.com** → **Settings** (ícone do perfil, canto superior direito)

2. **Developer settings** (menu esquerda, final da página)

3. **Personal access tokens** → **Tokens (classic)** → **Generate new token**

4. **Preencher:**
   ```
   Note: Token para validacao-ia
   Expiration: 90 days (ou mais)
   
   Marcar permissões:
   ✅ repo (todas as subopções)
   ```

5. **Generate token** (botão verde no final)

6. **COPIAR o token** (tipo: `ghp_xxxxxxxxxxxxxxxxxxxx`)
   
   ⚠️ **IMPORTANTE**: Salvar em lugar seguro! Não aparece de novo!

7. **Usar no terminal:**
   ```bash
   # Quando pedir Password, colar o token (não a senha!)
   Username: seu_usuario
   Password: ghp_xxxxxxxxxxxxxxxxxxxx  ← colar token aqui
   ```

---

### **5️⃣ VERIFICAR NO GITHUB**

Depois do `git push`:

1. Abrir navegador: `https://github.com/SEU_USUARIO/correlacao-desaparecimento-ia`

2. **Deve aparecer:**
   - ✅ 68 arquivos
   - ✅ README.md (descrição do projeto)
   - ✅ Pastas: scripts/, docs/, archive/, utils/, etc.
   - ❌ **NÃO deve ter**: *.csv, *.xlsx (dados sensíveis)

---

## 🖥️ NO OUTRO PC - CLONAR PROJETO

### **Via HTTPS (mais simples):**

```bash
# 1. Abrir terminal (Git Bash, PowerShell, CMD)
cd D:/___MeusScripts/

# 2. Clonar repositório
git clone https://github.com/SEU_USUARIO/correlacao-desaparecimento-ia.git

# 3. Entrar na pasta
cd correlacao-desaparecimento-ia

# 4. Verificar arquivos
ls -la
# Deve mostrar: scripts/, docs/, README.md, etc.

# 5. Instalar dependências
pip install -r requirements.txt

# 6. Baixar modelo Ollama
ollama pull qwen2.5-ptbr:7b

# 7. ⚠️ COPIAR MANUALMENTE (não estão no Git):
#    - Dados-homi-desaperecido.csv
#    - output/correlacoes_unicas_deduplicadas.xlsx
#    (Via pen drive, OneDrive, email, etc.)

# 8. Configurar validação
python scripts/configurar_validacao.py

# 9. Executar
./iniciar.bat  # Windows
./iniciar.sh   # Linux/Mac
```

---

### **Via SSH (mais avançado, sem senha):**

Se quiser evitar digitar token toda vez:

```bash
# 1. Gerar chave SSH (se não tiver)
ssh-keygen -t ed25519 -C "seu.email@exemplo.com"
# Apertar Enter 3x (aceitar padrões)

# 2. Copiar chave pública
cat ~/.ssh/id_ed25519.pub
# Copiar TODA a saída (começa com "ssh-ed25519 ...")

# 3. Adicionar no GitHub:
#    GitHub.com → Settings → SSH and GPG keys → New SSH key
#    - Title: "PC Casa" ou "PC Trabalho"
#    - Key: colar chave copiada
#    - Add SSH key

# 4. Clonar via SSH (em vez de HTTPS)
git clone git@github.com:SEU_USUARIO/correlacao-desaparecimento-ia.git

# Vantagem: Não pede senha/token nunca mais!
```

---

## 🔄 SINCRONIZAR MUDANÇAS ENTRE PCS

### **PC 1 (fez mudanças) → GitHub:**

```bash
# 1. Ver o que mudou
git status

# 2. Adicionar mudanças
git add .

# 3. Commitar com mensagem clara
git commit -m "Validação: processados casos 87-100, ajustado prompt"

# 4. Enviar para GitHub
git push
```

### **PC 2 (receber mudanças) → Atualizar:**

```bash
# 1. Baixar mudanças
git pull

# 2. Copiar dados atualizados (se necessário)
#    - output/validacao_progresso.xlsx
#    (Via pen drive, OneDrive, etc.)
```

---

## ⚠️ CUIDADOS IMPORTANTES

### ✅ **O QUE VAI PARA O GITHUB:**

- ✅ Scripts Python (*.py)
- ✅ Documentação (*.md, *.txt)
- ✅ Configurações de projeto (requirements.txt, .gitignore)
- ✅ Estrutura de pastas (scripts/, docs/, utils/)

### ❌ **O QUE NÃO VAI PARA O GITHUB (já está no .gitignore):**

- ❌ Dados CSV (Dados-homi-desaperecido.csv)
- ❌ Arquivos Excel (*.xlsx, *.xls)
- ❌ Configuração local (config_validacao.json)
- ❌ Cache Python (__pycache__/)
- ❌ Arquivos temporários (*.tmp, *.log)

### 🔒 **SEGURANÇA:**

- **Repositório PRIVATE**: Ninguém vê (dados sensíveis)
- **Não commitar CSV/Excel**: Dados pessoais protegidos
- **Token seguro**: Não compartilhar Personal Access Token
- **SSH recomendado**: Mais seguro que HTTPS

---

## 🆘 PROBLEMAS COMUNS

### **1. "fatal: remote origin already exists"**

```bash
git remote remove origin
git remote add origin https://github.com/SEU_USUARIO/...
```

### **2. "Authentication failed" / "Username/Password incorretos"**

- ❌ **NÃO usar senha normal do GitHub**
- ✅ **Usar Personal Access Token** (passo 4️⃣ acima)

### **3. "failed to push... remote contains work that you do not have locally"**

```bash
# Opção 1 (recomendado):
git pull origin main --rebase
git push

# Opção 2 (se não houver conflitos):
git pull origin main --allow-unrelated-histories
git push
```

### **4. Arquivos .csv aparecem no git status (não deveriam)**

```bash
# Verificar .gitignore
cat .gitignore | grep csv
# Deve mostrar: *.csv

# Se ainda aparece, limpar cache:
git rm --cached *.csv
git commit -m "Remove arquivos CSV do repositório"
git push
```

### **5. "git command not found"**

- Instalar Git: <https://git-scm.com/download/win>
- Reiniciar terminal

---

## 📚 COMANDOS GIT ÚTEIS

```bash
# Ver status (o que mudou)
git status

# Ver histórico de commits
git log --oneline --graph

# Ver diferenças antes de commitar
git diff

# Descartar mudanças locais (CUIDADO!)
git checkout -- arquivo.py

# Ver remotes configurados
git remote -v

# Mudar URL do remote (HTTPS → SSH ou vice-versa)
git remote set-url origin git@github.com:USER/REPO.git

# Ver branches
git branch -a

# Criar branch para testes
git checkout -b feature/novo-modelo
git checkout main  # voltar para main

# Ver tamanho do repositório
git count-objects -vH
```

---

## ✅ CHECKLIST FINAL

- [ ] Conta GitHub criada
- [ ] Repositório criado (private)
- [ ] `git remote add origin ...` executado
- [ ] `git push -u origin main` executado com sucesso
- [ ] Repositório visível no navegador
- [ ] Arquivos .csv **NÃO** aparecem no GitHub
- [ ] SETUP_OUTRO_PC.md revisado
- [ ] Token salvo em lugar seguro (se usar HTTPS)
- [ ] Ou SSH configurado (se preferir SSH)

---

## 🎯 PRÓXIMAS AÇÕES

1. ✅ **Testar clone em outro PC** (ou em outra pasta):
   ```bash
   git clone https://github.com/SEU_USUARIO/correlacao-desaparecimento-ia.git
   ```

2. ✅ **Copiar dados** (CSV/Excel) para o novo PC

3. ✅ **Instalar Ollama + modelo**:
   ```bash
   ollama pull qwen2.5-ptbr:7b
   ```

4. ✅ **Executar validação**:
   ```bash
   python scripts/configurar_validacao.py
   ./iniciar.bat
   ```

---

## 📞 PRECISA DE AJUDA?

- **Documentação Git**: <https://git-scm.com/doc>
- **GitHub Docs**: <https://docs.github.com>
- **Projeto local**: `SETUP_OUTRO_PC.md`
- **Como usar**: `correlation-project/docs/COMO_USAR.md`

---

**Status:** ✅ Repositório local pronto! Próximo: criar no GitHub web interface
