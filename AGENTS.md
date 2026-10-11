# 🧭 Orquestrador Global & Roteador de Agentes

> **Projeto:** `template-agent` | **Autoridade:** `<Autor / Decisor do Projeto>`  
> **Filosofia:** Cloud-First Puro | Zero Inferência Local | Token Economy | Escudo Zero Leaks

---

## 1. Diretrizes Mestras de Operação

1. **Zero Inferência Local:** Preservar hardware, manter silêncio acústico e estabilidade térmica. Inferência delegada integralmente a modelos em nuvem.
2. **Progressive Disclosure (3 Níveis):**
   * **Nível 1 (Aqui):** Roteamento global de alta velocidade (< 150 linhas).
   * **Nível 2 (agents/):** Carregamento exclusivo do especialista requisitado.
   * **Nível 3 (context/):** Consulta cirúrgica via RAG SQLite FTS5 (`tools/rag.py`).
3. **Escudo Zero Leaks:** Segredos isolados em `.vault/credentials.vault` (AES-256-GCM). Injeção estritamente em RAM via `tools/vault.py`.
4. **Governança Silenciosa:** Testes automatizados (`uv run pytest`, `uv run ruff check`) executados via agentes; sem testes manuais pelo usuário.
5. **Piloto Automático & Zero Overhead:** O motor de auto-governança assume proativamente a saúde, integridade, segurança (`.vault` 0700/0600), documentação, síntese de novos agentes e emancipação de subprojetos.

---

## 2. Roteamento de Agentes Especialistas

| Domínio / Necessidade | Agente Especialista | Responsabilidade Primária |
| :--- | :--- | :--- |
| **Zeladoria, Higiene & Tokens** | [zelador_agent.md](agents/zelador_agent.md) | Limpeza, ruff/pytest, poda de tokens e integridade de links |
| **Memória & Busca Atômica** | [bibliotecario_agent.md](agents/bibliotecario_agent.md) | Consulta/inserção em SQLite FTS5 e notas atômicas |
| **Cofre & Credenciais** | [guardiao_agent.md](agents/guardiao_agent.md) | Gerenciamento seguro AES-256-GCM e injeção em RAM |
| **Arquitetura, Governança & RFCs** | [arquiteto_agent.md](agents/arquiteto_agent.md) | Regra da 3ª ocorrência, monitor de escopo e auto-emancipação |
| **Tarefas Operárias Assíncronas** | [workers/](agents/workers) | Subagentes delegados para execução de rotinas repetitivas |

---

## 3. Ferramentas Determinísticas Locais (Zero Token Cost)

* **Piloto Automático & Meta-Governança:** `uv run python3 tools/autopilot.py`
* **Cofre & Segredos:** `uv run python3 tools/vault.py --help`
* **Busca na Memória RAG:** `uv run python3 tools/rag.py search "<termo>"`
* **Auditoria de Tokens:** `uv run python3 tools/token_counter.py`
* **Monitor de Escopo & Emancipação:** `uv run python3 tools/scope_monitor.py`
* **Despachante Operário:** `uv run python3 tools/dispatch_intern.py`

---

## 4. Mapa de Navegação e Documentação

* **MOC (Map of Content):** [MAPA_DO_PROJETO.md](MAPA_DO_PROJETO.md)
* **Topologia Canônica:** [ESTRUTURA_DO_PROJETO.md](ESTRUTURA_DO_PROJETO.md)
* **Manifesto Global:** [agy.yaml](agy.yaml)
* **Procedimentos Operacionais:** [context/sops/](context/sops)
* **Memória Persistente & RFCs:** [context/memory/](context/memory)
* **Decisões de Arquitetura:** [context/architecture/](context/architecture)
