# 🛡️ Decisão de Arquitetura: Fluxo de Segurança e Política Zero Leaks

> **Status:** Aprovado  

---

## 1. Contexto
O ecossistema opera sob a filosofia Cloud-First, orquestrado por modelos de IA na nuvem e executando ferramentas em ambiente local. A exposição inadvertida de senhas, chaves de API e credenciais em arquivos versionados ou no contexto de prompts constitui risco inaceitável.

## 2. Princípios de Blindagem
1. **Zero Leaks Vault:** Criptografia simétrica com chave AES-256 no padrão GCM (autenticada) isolada em `.vault/credentials.vault`.
2. **Injeção em Memória:** As credenciais descriptografadas só existem na memória RAM de execução imediata do subprocesso.
3. **Imunidade de RAG:** A pasta `.vault` é explicitamente excluída da indexação de memória e do versionamento git.
