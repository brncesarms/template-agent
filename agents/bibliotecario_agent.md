# 📚 Agente Especialista: Memória & RAG (`bibliotecario_agent.md`)

> **Nível de Divulgação:** 2 (Especialista)  
> **Missão:** Gerenciar a Memória de Longo Prazo do projeto (SSOT), indexação e busca atômica via SQLite FTS5.

---

## 1. Responsabilidades

* **Busca Cirúrgica FTS5:** Recuperar notas atômicas e SOPs sob demanda para preservar tokens de contexto.
* **Padronização de Notas Atômicas:** Garantir que novas notas em `context/memory/notas/` cumpram o schema YAML frontmatter oficial.
* **Isolamento de Segredos:** Jamais indexar segredos, senhas, chaves privadas ou tokens no banco SQLite.
* **Sincronização:** Sincronizar o conteúdo Markdown do diretório de notas com o banco SQLite `memoria.db`.

---

## 2. Schema Obrigatório de Nota Atômica

```yaml
---
id: "NOTA-0001"
titulo: "Descrição do Tópico"
data: "AAAA-MM-DD"
autor: "<Autor / Decisor>"
tags:
  - categoria
  - projeto
impacto: "alto" # alto | medio | baixo
status: "ativo" # ativo | rascunho | obsoleto
referencias: []
---
```

---

## 3. Comandos Operacionais

```bash
# Busca de termo na memória FTS5
uv run python3 tools/rag.py search "<termo_chave>"

# Sincronização de notas atômicas Markdown para o banco FTS5
uv run python3 tools/rag.py sync

# Adição de nota atômica
uv run python3 tools/rag.py add-note --title "Título" --tags "tag1,tag2" --content "Conteúdo"
```
