# 🏛️ Estrutura Canônica do Projeto (AGENTS.md v8)

> **Projeto:** `template-agent`  
> **Especificação:** `AGENTS.md v8`  
> **Status:** Ativo & Imutável  

---

## 🌳 Árvore Estrutural Canônica

```text
meu_projeto_agy/
├── README.md                 # Visão geral, instruções e onboarding do projeto
├── MAPA_DO_PROJETO.md        # [MOC] Índice principal e mapa de navegação
├── agy.yaml                  # Manifesto global do projeto e governança (v8)
├── AGENTS.md                 # Orquestrador enxuto (roteador global e orçamentador de tokens)
├── pyproject.toml            # Dependências gerenciadas via uv/pip
├── .env.example              # Exemplo de variáveis de ambiente
├── .vault/                   # 🔒 COFRE CRIPTOGRAFADO (AES-256-GCM, gitignored, permissão 0600)
│   └── credentials.vault     # Segredos isolados (NUNCA no RAG/memoria.db)
│
├── agents/                   # [PERSONAS E REGRAS DE ATUAÇÃO (3-Tier Boundaries)]
│   ├── zelador_agent.md      # Higiene, linters, poda de tokens e integridade
│   ├── bibliotecario_agent.md # Especialista em RAG e Memória de Longo Prazo
│   ├── guardiao_agent.md     # Especialista no acesso seguro ao cofre criptografado
│   ├── arquiteto_agent.md    # Decisão autônoma de novos agentes e auto-emancipação
│   └── workers/              # Subagentes operários assíncronos
│
├── tools/                    # [FERRAMENTAS DETERMINÍSTICAS (CONSUMO ZERO LLM)]
│   ├── __init__.py
│   ├── autopilot.py          # Motor unificado de auto-governança, saúde e emancipação
│   ├── rag.py                # Motor executável SQLite FTS5 da memória
│   ├── vault.py              # Acesso seguro ao cofre estritamente em RAM
│   ├── token_counter.py      # Auditoria e medição de consumo de tokens
│   ├── scope_monitor.py      # Monitor autônomo de densidade e limite de emancipação
│   └── dispatch_intern.py    # Despachante assíncrono de subagentes operários
│
└── context/                  # [BASE DE CONHECIMENTO E MEMÓRIA PERSISTENTE]
    ├── README.md             # Índice central da base de conhecimento
    ├── memory/               # 🧠 MEMÓRIA PERSISTENTE
    │   ├── notas/            # Notas atômicas em Markdown com cabeçalho YAML
    │   └── propostas/        # RFCs de governança e propostas de arquitetura
    ├── sops/                 # Procedimentos Operacionais Padrão (SOPs)
    │   ├── padrao_manutencao.md # Manutenção contínua e silenciosa
    │   ├── gestao_cofre.md   # Gestão do cofre e ciclo de vida de segredos
    │   └── auto_emancipacao.md # Regras de separação de subprojetos
    ├── runbooks/             # Guias operacionais e resolução de incidentes
    └── architecture/         # Decisões de arquitetura
        ├── fluxo_seguranca.md# Especificação do Escudo Zero Leaks
        └── economia_tokens.md# Diretrizes de otimização de tokens
```

---

## 🔒 Diretiva de Manutenção Contínua
* Este arquivo é a **Fonte Única de Verdade (SSOT)** da topologia física de diretórios e arquivos do ecossistema.
* O `zelador_agent.md` verifica se a estrutura física diverge deste contrato a cada ciclo de manutenção.
