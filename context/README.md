# 📚 Base de Conhecimento e Memória Persistente

Este diretório constitui o **Nível 3 (Conhecimento)** do ecossistema (*Progressive Disclosure*).

---

## 🗂️ Estrutura

* **memory/:** Memória persistente e SSOT (Single Source of Truth).
  * `memoria.db`: Banco relacional SQLite FTS5 (gerado dinamicamente via `tools/rag.py sync`).
  * `notas/`: Notas atômicas em Markdown com cabeçalho YAML obrigatório.
  * `propostas/`: RFCs de evolução, novas personas e propostas de auto-emancipação.
* **sops/:** Procedimentos Operacionais Padrão (SOPs).
* **architecture/:** Decisões de Arquitetura de Software e Infraestrutura (ADRs e guias).
* **runbooks/:** Procedimentos de operação e recuperação de incidentes.
