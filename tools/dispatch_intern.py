#!/usr/bin/env python3
"""Asynchronous Task & Worker Dispatcher for Agent Ecosystem.

Dispatches routine tasks, generates 3rd occurrence RFCs, and handles delegation.
"""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

PROPOSALS_DIR = Path("context/memory/propostas")


def create_third_occurrence_rfc(domain: str, occurrences: list[str] | None = None) -> Path:
    """Create an RFC when a domain or task pattern is detected 3 times."""
    PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    clean_domain = re.sub(r"[^a-zA-Z0-9_]", "_", domain.lower()).strip("_")
    rfc_file = PROPOSALS_DIR / f"rfc_agente_{clean_domain}.md"

    occ_bullets = (
        "\n".join(f"* {item}" for item in occurrences)
        if occurrences
        else "* Ocorrência 1: Tarefa pontual executada\n* Ocorrência 2: Tarefa repetida manualmente\n* Ocorrência 3: Padrão consolidado detectado"
    )

    content = f"""# 📜 Proposta de Novo Agente: `{clean_domain}` (Regra da 3ª Ocorrência)

> **Domínio:** `{clean_domain}`  
> **Data:** {today}  
> **Status:** `proposta`  
> **Autor:** Governança Autônoma Agent Ecosystem  

---

## 1. Evidências de Ocorrência
{occ_bullets}

## 2. Escopo Proposto para o Agente Especialista
* **Arquivo Alvo:** `agents/{clean_domain}_agent.md`
* **Nível:** 2 (Especialista)
* **Objetivo:** Automatizar e encapsular procedimentos de `{clean_domain}` com consumo mínimo de tokens.

## 3. Próximos Passos
1. Validação com o decisor técnico Decisor Técnico.
2. Criação do arquivo de persona em `agents/`.
3. Inclusão no roteamento do `AGENTS.md` e atualização do `MAPA_DO_PROJETO.md`.
"""
    rfc_file.write_text(content, encoding="utf-8")
    return rfc_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Agent Ecosystem Worker & Task Dispatcher")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # create-proposal
    prop_parser = subparsers.add_parser("create-proposal", help="Create RFC for 3rd occurrence rule")
    prop_parser.add_argument("--domain", required=True, help="Domain or task name")
    prop_parser.add_argument(
        "--notes", nargs="*", help="Optional description of the 3 occurrences"
    )

    args = parser.parse_args()

    if args.command == "create-proposal":
        path = create_third_occurrence_rfc(args.domain, args.notes)
        print(f"RFC de 3ª ocorrência gerada em: {path}")


if __name__ == "__main__":
    main()
