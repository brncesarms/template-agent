# ⚡ Decisão de Arquitetura: Token Economy & Divulgação Progressiva

> **Status:** Aprovado  
> **Data:** 2026-10-11  

---

## 1. Contexto
Janelas de contexto saturadas com instruções redundantes provocam degradação de atenção do modelo, latência elevada e custos desnecessários de tokens.

## 2. Padrão de 3 Níveis (*Progressive Disclosure*)
* **Nível 1 (Raiz):** `AGENTS.md` com menos de 150 linhas; funciona puramente como mapa tático de roteamento.
* **Nível 2 (Especialistas):** Arquivos `agents/*.md` carregados apenas quando a conversa direciona o fluxo para seu domínio específico.
* **Nível 3 (Conhecimento Cirúrgico):** Fragmentos da memória persistente recuperados através de busca FTS5 pontual (`tools/rag.py`), sem despejar a documentação inteira no prompt.

## 3. Ferramentas Determinísticas
Tarefas puramente computacionais (contagem de linhas, checagem de integridade, criptografia, indexação de texto) são resolvidas por scripts Python locais sem invocar modelos de linguagem.
