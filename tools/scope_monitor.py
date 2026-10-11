#!/usr/bin/env python3
"""Autonomous Scope & Density Monitor for Archimedes.

Monitors repository density to enforce the Auto-Emancipation principle.
When a module or directory exceeds density thresholds, triggers RFC generation.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

DEFAULT_WARNING_THRESHOLD = 30
DEFAULT_CRITICAL_THRESHOLD = 40
PROPOSALS_DIR = Path("context/memory/propostas")


def check_directory_density(
    base_dir: Path = Path("."),
    warning_threshold: int = DEFAULT_WARNING_THRESHOLD,
    critical_threshold: int = DEFAULT_CRITICAL_THRESHOLD,
) -> list[dict]:
    """Scan subdirectories and check file count thresholds."""
    results = []

    # Excluded directories (infrastructure and central knowledge base)
    ignored = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", ".vault", "context"}

    for item in base_dir.iterdir():
        if not item.is_dir() or item.name in ignored:
            continue

        # Count all regular files recursively
        files = [f for f in item.rglob("*") if f.is_file() and not any(p in ignored for p in f.parts)]
        count = len(files)

        status = "normal"
        if count >= critical_threshold:
            status = "critical"
        elif count >= warning_threshold:
            status = "warning"

        results.append(
            {
                "module": item.name,
                "path": str(item),
                "file_count": count,
                "status": status,
            }
        )

    return sorted(results, key=lambda x: x["file_count"], reverse=True)


def trigger_emancipation_rfc(module_name: str, file_count: int) -> Path:
    """Generate an RFC proposal for module auto-emancipation."""
    PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    rfc_id = f"RFC-EMANCIPATE-{module_name.upper()}"
    target_file = PROPOSALS_DIR / f"{rfc_id.lower()}.md"

    rfc_content = f"""# 📜 Proposta de Auto-Emancipação: {module_name}

> **ID:** `{rfc_id}`  
> **Data:** {today}  
> **Status:** `proposta`  
> **Gatilho:** `scope_monitor.py` (Densidade Crítica: {file_count} arquivos)  

---

## 1. Justificativa
O submódulo `{module_name}` atingiu {file_count} arquivos, superando o limiar crítico de densidade ({DEFAULT_CRITICAL_THRESHOLD} arquivos). Para preservar a simplicidade e a economia de tokens do orquestrador Archimedes, recomenda-se sua segregação em repositório autônomo com seu próprio `AGENTS.md`.

## 2. Plano de Transição
1. Inicializar repositório dedicado para `{module_name}`.
2. Migrar arquivos correspondentes e dependências.
3. Configurar ponte MCP ou subprocesso determinístico em `archimedes`.
4. Arquivar referências no `MAPA_DO_PROJETO.md`.
"""
    target_file.write_text(rfc_content, encoding="utf-8")
    return target_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Archimedes Scope & Auto-Emancipation Monitor")
    parser.add_argument("--auto-rfc", action="store_true", help="Generate RFC for critical modules")
    args = parser.parse_args()

    results = check_directory_density()

    print(f"{'Módulo':<25} | {'Arquivos':<10} | {'Status'}")
    print("-" * 50)

    critical_found = []
    for r in results:
        status_label = r["status"].upper()
        print(f"{r['module']:<25} | {r['file_count']:<10} | {status_label}")
        if r["status"] == "critical":
            critical_found.append(r)

    print("-" * 50)

    if critical_found:
        print(f"⚠️ Atenção: {len(critical_found)} módulo(s) atingiram densidade crítica!")
        if args.auto_rfc:
            for c in critical_found:
                rfc_path = trigger_emancipation_rfc(c["module"], c["file_count"])
                print(f"RFC gerada em: {rfc_path}")
        else:
            print("Execute com --auto-rfc para gerar propostas de auto-emancipação.")
        sys.exit(2)
    else:
        print("✅ Todos os módulos operando dentro dos limiares de densidade.")


if __name__ == "__main__":
    main()
