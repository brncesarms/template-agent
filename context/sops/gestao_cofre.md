# 📋 SOP: Gestão do Cofre Criptografado e Política Zero Leaks

> **Código:** `SOP-SEC-001`  
> **Responsável:** `guardiao_agent.md` | **Decisor:** `<Autor / Decisor do Projeto>`  

---

## 1. Objetivo
Estabelecer o procedimento de manipulação, armazenamento e rotação de credenciais, impedindo qualquer vazamento para repositórios git, logs ou memória de inferência LLM.

## 2. Princípios de Segurança
* **Permissões de Sistema de Arquivos:** O diretório `.vault/` deve possuir permissão estrita `0700` e arquivos internos `0600`.
* **Criptografia Autônoma:** Algoritmo AES-256-GCM.
* **Isolamento de RAG:** O arquivo `credentials.vault` é expressamente ignorado pelo indexador RAG (`tools/rag.py`).

## 3. Fluxo Operacional
1. **Adicionar Credencial:**
   ```bash
   uv run python3 tools/vault.py set --key "IDENTIFICADOR" --value "VALOR_SECRETO"
   ```
2. **Consultar Existência (Sem expor o valor):**
   ```bash
   uv run python3 tools/vault.py list
   ```
3. **Injeção Efêmera:**
   Subprocessos que demandam credenciais devem ler a chave diretamente da memória via `tools/vault.py get` sem salvar saída em disco.
