# 🗺️ Mapa do Projeto (MOC - Map of Content)

> **Versão:** 8.0.0  
> **Status:** Ativo  

Este mapa fornece a navegação direta e o índice unificado de todos os artefatos do ecossistema.

---

## 🏛️ Núcleo e Orquestração

* [AGENTS.md](AGENTS.md) - Roteador principal e orquestrador global (Nível 1)
* [ESTRUTURA_DO_PROJETO.md](ESTRUTURA_DO_PROJETO.md) - Desenho da topologia física canônica
* [agy.yaml](agy.yaml) - Manifesto global de governança e limiares do sistema

---

## 🤖 Agentes Especialistas (Nível 2)

* [agents/zelador_agent.md](agents/zelador_agent.md) - Auditoria silenciosa, poda de tokens, linters e links
* [agents/bibliotecario_agent.md](agents/bibliotecario_agent.md) - Especialista em memória de longo prazo e busca FTS5
* [agents/guardiao_agent.md](agents/guardiao_agent.md) - Gestão do cofre AES-256-GCM e injeção em RAM
* [agents/arquiteto_agent.md](agents/arquiteto_agent.md) - Avaliador da 3ª ocorrência, monitor de escopo e auto-emancipação
* [agents/workers/](agents/workers) - Subagentes operários assíncronos

---

## 🛠️ Ferramentas Determinísticas (`tools/`)

* [tools/autopilot.py](tools/autopilot.py) - Motor unificado de auto-governança, saúde, segurança e emancipação
* [tools/vault.py](tools/vault.py) - Manipulação e injeção do cofre seguro
* [tools/rag.py](tools/rag.py) - Motor SQLite FTS5 da memória
* [tools/token_counter.py](tools/token_counter.py) - Auditor de densidade de tokens
* [tools/scope_monitor.py](tools/scope_monitor.py) - Detecção de densidade e gatilho de emancipação
* [tools/dispatch_intern.py](tools/dispatch_intern.py) - Despachante assíncrono para operários

---

## 📚 Base de Conhecimento e Memória (`context/` - Nível 3)

* [context/README.md](context/README.md) - Visão geral da base de conhecimento
* **Memória Persistente (`context/memory/`):**
  * [context/memory/notas/](context/memory/notas) - Notas atômicas com frontmatter YAML
  * [context/memory/propostas/](context/memory/propostas) - RFCs de arquitetura e propostas
* **Procedimentos Operacionais Padrão (`context/sops/`):**
  * [context/sops/padrao_manutencao.md](context/sops/padrao_manutencao.md) - Padrão de manutenção silenciosa
  * [context/sops/gestao_cofre.md](context/sops/gestao_cofre.md) - Gestão e ciclo de vida de credenciais
  * [context/sops/auto_emancipacao.md](context/sops/auto_emancipacao.md) - Processo de emancipação de submódulos
* **Arquitetura e Runbooks:**
  * [context/architecture/fluxo_seguranca.md](context/architecture/fluxo_seguranca.md)
  * [context/architecture/economia_tokens.md](context/architecture/economia_tokens.md)
  * [context/runbooks/](context/runbooks)
