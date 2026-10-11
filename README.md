# 🧭 Template Agent

> **Template Canônico de Ecossistema de Agentes com Meta-Governança Autônoma**  
> **Filosofia:** Cloud-First Puro | Zero Inferência Local | Token Economy | Escudo Zero Leaks

---

## 📌 Sobre Este Template

O **`template-agent`** é o esqueleto canônico para construção de ecossistemas autônomos de agentes de inteligência artificial. Ele implementa uma arquitetura robusta baseada em:

1. **Cloud-First & Zero Inferência Local:** Delegar o raciocínio a modelos na nuvem, mantendo o hardware local leve e silencioso.
2. **Progressive Disclosure (3 Níveis):**
   * **Nível 1 ([AGENTS.md](AGENTS.md)):** Roteamento global de alta velocidade com consumo mínimo de tokens (< 150 linhas).
   * **Nível 2 ([agents/](agents/)):** Carregamento exclusivo do especialista necessário.
   * **Nível 3 ([context/](context/)):** Base profunda consultada cirurgicamente via RAG SQLite FTS5.
3. **Escudo Zero Leaks:** Credenciais armazenadas com AES-256-GCM em `.vault/credentials.vault`, permissões `0700`/`0600` e injeção restrita à RAM.
4. **Governança Silenciosa:** O motor determinístico ([tools/autopilot.py](tools/autopilot.py)) audita linters, testes, sanitização e criação de agentes sem fricção manual.

---

## 🚀 Como Usar Este Template

### 1. Criar um novo repositório a partir do template
Clique em **"Use this template"** no GitHub ou clone diretamente:

```bash
git clone https://github.com/brncesarms/template-agent.git meu-novo-agente
cd meu-novo-agente
```

### 2. Configurar o ambiente
```bash
# Instalar dependências com uv
uv sync
```

### 3. Personalizar o manifesto
Edite o arquivo [agy.yaml](agy.yaml) com o nome do seu projeto, autor e limiares desejados.

### 4. Validar o Piloto Automático
```bash
# Executa validação de saúde, permissões e testes
uv run python3 tools/autopilot.py
```

---

## 📂 Estrutura de Diretórios

```text
meu-novo-agente/
├── README.md                 # Este documento
├── MAPA_DO_PROJETO.md        # [MOC] Índice e navegação do ecossistema
├── ESTRUTURA_DO_PROJETO.md   # Topologia canônica imutável da árvore de arquivos
├── AGENTS.md                 # Roteador mestre e orquestrador global (Nível 1)
├── agy.yaml                  # Manifesto global do projeto e governança
├── pyproject.toml            # Dependências gerenciadas via uv/pip
├── .env.example              # Modelo de variáveis de ambiente
│
├── .vault/                   # 🔒 Cofre criptografado AES-256-GCM (gitignored)
│   └── credentials.vault
│
├── agents/                   # Personas especializadas (Nível 2)
│   ├── zelador_agent.md      # Limpeza, linters, testes e poda de tokens
│   ├── bibliotecario_agent.md # Memória de longo prazo e RAG SQLite FTS5
│   ├── guardiao_agent.md     # Gestão segura do cofre AES-256-GCM
│   ├── arquiteto_agent.md    # Monitor de escopo e auto-emancipação
│   └── workers/              # Subagentes operários assíncronos
│
├── tools/                    # Ferramentas determinísticas em Python (Custo zero LLM)
│   ├── autopilot.py          # Motor de auto-governança e saúde
│   ├── vault.py              # Acesso ao cofre estritamente em RAM
│   ├── rag.py                # Motor SQLite FTS5
│   ├── token_counter.py      # Medição e orçamento de tokens
│   ├── scope_monitor.py      # Monitoramento de densidade de arquivos
│   └── dispatch_intern.py    # Despachante de operários
│
└── context/                  # Base de conhecimento e memória (Nível 3)
    ├── README.md
    ├── memory/               # Notas atômicas e propostas (vazio inicialmente)
    ├── sops/                 # Procedimentos Operacionais Padrão (SOPs)
    ├── architecture/         # Decisões de arquitetura
    └── runbooks/             # Guias de operação e incidentes
```

---

## 🛠️ Ferramentas Determinísticas

* **Piloto Automático:** `uv run python3 tools/autopilot.py`
* **Cofre Seguro:** `uv run python3 tools/vault.py --help`
* **Memória RAG:** `uv run python3 tools/rag.py search "<termo>"`
* **Auditor de Tokens:** `uv run python3 tools/token_counter.py`
* **Monitor de Escopo:** `uv run python3 tools/scope_monitor.py`
