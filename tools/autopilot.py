#!/usr/bin/env python3
"""Autonomous Meta-Governance & Auto-Pilot Engine for Agent Ecosystem.

Consolidates all health checks, security enforcement, CRLF sanitization,
memory RAG syncing, agent synthesis (Rule of 3rd Occurrence), and
project auto-emancipation into a single, zero-cognitive-overhead system.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))


def enforce_vault_security(root: Path = WORKSPACE_ROOT) -> list[str]:
    """Enforce strict 0700 on .vault and 0600 on secret files."""
    actions = []
    vault_dir = root / ".vault"
    if vault_dir.exists():
        os.chmod(vault_dir, stat.S_IRWXU)
        actions.append("chmod 0700 .vault/")

    for filename in ["credentials.vault", "master.key"]:
        target = vault_dir / filename
        if target.exists():
            os.chmod(target, stat.S_IRUSR | stat.S_IWUSR)
            actions.append(f"chmod 0600 .vault/{filename}")

    return actions


def sanitize_line_endings(root: Path = WORKSPACE_ROOT) -> list[str]:
    """Convert CRLF to LF across scripts, python, markdown, and config files."""
    sanitized = []
    ignored = {".venv", ".git", "__pycache__", ".pytest_cache", ".ruff_cache"}
    extensions = (".py", ".sh", ".json", ".md", ".toml", ".yaml")

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ignored]
        for f in filenames:
            if f.endswith(extensions):
                filepath = Path(dirpath) / f
                try:
                    data = filepath.read_bytes()
                    if b"\r\n" in data:
                        filepath.write_bytes(data.replace(b"\r\n", b"\n"))
                        sanitized.append(str(filepath.relative_to(root)))
                except Exception:
                    continue
    return sanitized


def run_linters_and_tests(root: Path = WORKSPACE_ROOT, auto_fix: bool = False) -> dict:
    """Run ruff and pytest deterministically."""
    results = {"ruff": "passed", "pytest": "passed", "details": []}

    # Ruff check
    ruff_cmd = ["uv", "run", "ruff", "check", "tools/"]
    if auto_fix:
        ruff_cmd.append("--fix")

    ruff_res = subprocess.run(ruff_cmd, cwd=root, capture_output=True, text=True, check=False)
    if ruff_res.returncode != 0:
        results["ruff"] = "failed"
        results["details"].append(f"Ruff errors: {ruff_res.stdout or ruff_res.stderr}")

    # Pytest (skip recursive call if already running inside pytest)
    if "PYTEST_CURRENT_TEST" not in os.environ:
        pytest_res = subprocess.run(
            ["uv", "run", "pytest", "-q"], cwd=root, capture_output=True, text=True, check=False
        )
        if pytest_res.returncode != 0:
            results["pytest"] = "failed"
            results["details"].append(f"Pytest failures: {pytest_res.stdout or pytest_res.stderr}")

    return results


def sync_memory_db(root: Path = WORKSPACE_ROOT) -> int:
    """Synchronize all atomic notes into SQLite FTS5 database."""
    try:
        from tools.rag import sync_notes

        return sync_notes(notes_dir=root / "context/memory/notas", db_path=root / "context/memory/memoria.db")
    except Exception as e:
        print(f"Warning syncing memory: {e}", file=sys.stderr)
        return 0


def audit_scope_and_tokens(root: Path = WORKSPACE_ROOT) -> dict:
    """Audit AGENTS.md line limit and check module density for emancipation."""
    from tools.scope_monitor import check_directory_density
    from tools.token_counter import audit_files

    token_reports = audit_files(base_dir=root)
    agents_rep = next((r for r in token_reports if r["path"] == "AGENTS.md" or r["path"].endswith("/AGENTS.md")), None)
    agents_lines = agents_rep["lines"] if agents_rep else 0

    density_reports = check_directory_density(base_dir=root)
    critical_modules = [m for m in density_reports if m["status"] == "critical"]
    warning_modules = [m for m in density_reports if m["status"] == "warning"]

    return {
        "agents_md_lines": agents_lines,
        "agents_md_budget_ok": agents_lines <= 150,
        "critical_modules": critical_modules,
        "warning_modules": warning_modules,
    }


def create_specialized_agent(
    domain: str,
    mission: str,
    commands: list[str] | None = None,
    root: Path = WORKSPACE_ROOT,
) -> Path:
    """Autonomously scaffold a new specialized agent, register in AGENTS.md and memory."""
    clean_domain = re.sub(r"[^a-zA-Z0-9_]", "_", domain.lower()).strip("_")
    agent_filename = f"{clean_domain}_agent.md"
    agent_path = root / "agents" / agent_filename

    cmd_list = (
        commands
        if commands
        else [f"# Comandos determinísticos de {clean_domain}", f"uv run python3 tools/{clean_domain}.py --help"]
    )
    cmds_block = "\n".join(cmd_list)

    content = f"""# 🤖 Agente Especialista: {domain.title()} (`{agent_filename}`)

> **Nível de Divulgação:** 2 (Especialista)  
> **Missão:** {mission}  

---

## 1. Responsabilidades

* Execução autônoma de rotinas especializadas do domínio `{clean_domain}`.
* Preservação da economia de tokens e isolamento de contexto.
* Reporte transparente de status sem intervenção manual pelo usuário.

---

## 2. Comandos Operacionais

```bash
{cmds_block}
```

---

## 3. Protocolo de Governança
Este agente opera sob as Diretrizes Mestras do [AGENTS.md](file://{root}/AGENTS.md).
"""
    agent_path.write_text(content, encoding="utf-8")

    # Update AGENTS.md routing table if not already present
    agents_md = root / "AGENTS.md"
    agents_text = agents_md.read_text(encoding="utf-8")
    if agent_filename not in agents_text:
        table_entry = f"| **{domain.title()}** | [{agent_filename}](file://{root}/agents/{agent_filename}) | {mission[:60]}... |\n"
        # Insert before the closing markdown table or section 3
        if "## 3. Ferramentas Determinísticas" in agents_text:
            agents_text = agents_text.replace(
                "## 3. Ferramentas Determinísticas",
                f"{table_entry}\n---\n\n## 3. Ferramentas Determinísticas",
            )
            agents_md.write_text(agents_text, encoding="utf-8")

    # Register in RAG atomic note
    try:
        from tools.rag import add_note

        add_note(
            title=f"Criação Autônoma do Agente {domain.title()}",
            content=f"Agente especialista `{agent_filename}` criado automaticamente pela governança autônoma.\n\nMissão: {mission}",
            tags=["agente", "auto_governanca", clean_domain],
            impact="medio",
            notes_dir=root / "context/memory/notas",
            db_path=root / "context/memory/memoria.db",
        )
    except Exception as e:
        print(f"Warning creating note for agent: {e}", file=sys.stderr)

    return agent_path


def emancipate_module(
    module_name: str,
    target_dir: Path | None = None,
    root: Path = WORKSPACE_ROOT,
) -> Path:
    """Autonomously emancipate an oversized module into a standalone project."""
    source_module = root / module_name
    if not source_module.exists() or not source_module.is_dir():
        raise FileNotFoundError(f"Module '{module_name}' does not exist in {root}")

    if target_dir is None:
        target_dir = root.parent / f"agent-{module_name}"

    target_dir.mkdir(parents=True, exist_ok=True)

    # Copy files
    for item in source_module.iterdir():
        dest = target_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)

    # Create standalone AGENTS.md
    standalone_agents_md = target_dir / "AGENTS.md"
    standalone_agents_md.write_text(
        f"""# 🚀 Projeto Emancipado: {module_name.title()}

> **Origem:** Auto-Emancipação | **Autoridade:** Decisor Técnico  
> **Filosofia:** Cloud-First Puro | Módulo Especialista Autônomo  

---

## 1. Missão do Projeto
Projeto segregado autonomamente a partir do ecossistema de agentes para preservar a economia de tokens e foco arquitetural.

## 2. Comandos do Módulo
Consulte os scripts locais e execute via `uv run`.
""",
        encoding="utf-8",
    )

    # Create basic pyproject.toml if missing
    standalone_pyproject = target_dir / "pyproject.toml"
    if not standalone_pyproject.exists():
        standalone_pyproject.write_text(
            f"""[project]
name = "{module_name}"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = []
""",
            encoding="utf-8",
        )

    # Document emancipation in Agent Ecosystem
    try:
        from tools.rag import add_note

        add_note(
            title=f"Auto-Emancipação do Módulo {module_name}",
            content=f"O módulo `{module_name}` foi segregado para projeto autônomo em `{target_dir}` para manter a densidade controlada.",
            tags=["emancipacao", "arquitetura", module_name],
            impact="alto",
            notes_dir=root / "context/memory/notas",
            db_path=root / "context/memory/memoria.db",
        )
    except Exception as e:
        print(f"Warning logging emancipation: {e}", file=sys.stderr)

    return target_dir


def run_full_cycle(root: Path = WORKSPACE_ROOT, auto_fix: bool = True) -> dict:
    """Run full self-governance cycle: security, sanitation, lint, tests, RAG sync, and audit."""
    report = {}

    # 1. Vault permissions
    report["vault_actions"] = enforce_vault_security(root)

    # 2. Line endings
    report["sanitized_files"] = sanitize_line_endings(root) if auto_fix else []

    # 3. Linter & tests
    report["code_hygiene"] = run_linters_and_tests(root, auto_fix=auto_fix)

    # 4. Sync memory
    report["synced_notes"] = sync_memory_db(root)

    # 5. Tokens & scope
    report["scope_and_tokens"] = audit_scope_and_tokens(root)

    report["status"] = (
        "HEALTHY"
        if report["code_hygiene"]["ruff"] == "passed"
        and report["code_hygiene"]["pytest"] == "passed"
        and report["scope_and_tokens"]["agents_md_budget_ok"]
        else "ATTENTION_REQUIRED"
    )

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Agent Ecosystem Autonomous Meta-Governance & Auto-Pilot Engine")
    subparsers = parser.add_subparsers(dest="command")

    # default cycle
    parser.add_argument("--check", action="store_true", help="Run checks in read-only mode")
    parser.add_argument("--fix", action="store_true", default=True, help="Auto-repair and sync all components")

    # create-agent
    agent_parser = subparsers.add_parser("create-agent", help="Autonomously generate and wire a specialized agent")
    agent_parser.add_argument("--name", required=True, help="Domain or agent name (e.g. devops, finanças)")
    agent_parser.add_argument("--mission", required=True, help="Primary mission of the agent")
    agent_parser.add_argument("--commands", nargs="*", help="Optional command examples")

    # emancipate
    emancipate_parser = subparsers.add_parser("emancipate", help="Auto-emancipate a module into a standalone project")
    emancipate_parser.add_argument("--module", required=True, help="Directory name of the module to emancipate")
    emancipate_parser.add_argument("--target", help="Destination path for the new standalone project")

    args = parser.parse_args()

    if args.command == "create-agent":
        created = create_specialized_agent(domain=args.name, mission=args.mission, commands=args.commands)
        print(f"✅ Agente especialista criado e roteado com sucesso: {created}")
        # Run sync after creation
        run_full_cycle(auto_fix=True)
        return

    if args.command == "emancipate":
        target = Path(args.target) if args.target else None
        dest = emancipate_module(module_name=args.module, target_dir=target)
        print(f"🚀 Módulo '{args.module}' emancipado com sucesso para: {dest}")
        run_full_cycle(auto_fix=True)
        return

    # Default run
    auto_fix = not args.check
    result = run_full_cycle(auto_fix=auto_fix)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "HEALTHY":
        sys.exit(1)


if __name__ == "__main__":
    main()
