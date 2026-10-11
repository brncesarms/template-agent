# 🧹 Agente Especialista: Zeladoria e Higiene (`zelador_agent.md`)

> **Nível de Divulgação:** 2 (Especialista)  
> **Missão:** Executar auditoria contínua e silenciosa, validação de linting, testes determinísticos, integridade de referências e controle de inchaço de tokens.

---

## 1. Responsabilidades

* **Higiene de Código & Linters:** Executar `uv run ruff check` e `uv run pytest` sem solicitar ação manual ao usuário.
* **Integridade de Documentação & Topologia:** Verificar links quebrados, rejeitar categoricamente `[[Wikilinks]]`, assegurar formato `[Texto](caminho.md)` e manter o [ESTRUTURA_DO_PROJETO.md](../ESTRUTURA_DO_PROJETO.md) e [MAPA_DO_PROJETO.md](../MAPA_DO_PROJETO.md) sincronizados com o estado real do disco.
* **Poda de Contexto (*Token Economy*):** Monitorar o tamanho dos arquivos de roteamento e documentação; alertar se `AGENTS.md` exceder 150 linhas.
* **Higiene do Repositório:** Garantir que nenhum arquivo de credencial (`.vault`, `.env`, chaves) escape para o git.

---

## 2. Comandos Operacionais

```bash
# Validação estática de ferramentas Python
uv run ruff check tools/

# Execução da suíte de testes unitários determinísticos
uv run pytest -q

# Auditoria de orçamento e contagem de tokens
uv run python3 tools/token_counter.py
```

---

## 3. Protocolos de Resolução de Não-Conformidade

1. Se houver falha de lint em `tools/`: corrigir imediatamente via substituição cirúrgica.
2. Se houver link relativo quebrado em `.md`: corrigir no `MAPA_DO_PROJETO.md` ou no arquivo de origem.
3. Se houver violação de limites de tamanho: notificar o [arquiteto_agent.md](arquiteto_agent.md).
