# 📋 SOP: Padrão de Manutenção Silenciosa e Higiene

> **Código:** `SOP-MNT-001`  
> **Responsável:** `zelador_agent.md` | **Decisor:** `<Autor / Decisor do Projeto>`  

---

## 1. Objetivo
Garantir a integridade, sintaxe, formatação e orçamentos do repositório sem requerer esforço cognitivo ou testes manuais por parte do usuário.

## 2. Frequência e Gatilhos
* Executado ao término de cada tarefa de desenvolvimento ou modificação estrutural.
* Disparado antes de congelamento de versões ou commits.

## 3. Checklist Obrigatório de Execução
1. **Verificação de Linters:**
   ```bash
   uv run ruff check tools/
   ```
2. **Execução de Testes Determinísticos:**
   ```bash
   uv run pytest -q
   ```
3. **Auditoria de Orçamento de Contexto:**
   ```bash
   uv run python3 tools/token_counter.py --strict
   ```
4. **Verificação de Links e MOC:**
   * Garantir que não existam referências a `[[Wikilinks]]`.
   * Verificar se novos artefatos foram devidamente indexados no [MAPA_DO_PROJETO.md](../../MAPA_DO_PROJETO.md).
