#!/usr/bin/env python3
"""Deterministic Token & Context Auditor for Archimedes.

Measures line counts and estimated tokens across agents and router files
to enforce the Token Economy principles (< 150 lines in AGENTS.md).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

MAX_AGENTS_MD_LINES = 150


def estimate_tokens(text: str) -> int:
    """Approximate token count using ~4 chars per token heuristic."""
    return max(1, len(text) // 4)


def audit_files(base_dir: Path = Path(".")) -> list[dict]:
    """Inspect core router and agent markdown files."""
    targets = [
        base_dir / "AGENTS.md",
        base_dir / "ESTRUTURA_DO_PROJETO.md",
        base_dir / "MAPA_DO_PROJETO.md",
        base_dir / "agy.yaml",
        *sorted(base_dir.glob("agents/*.md")),
    ]

    report = []
    for file_path in targets:
        if not file_path.exists():
            continue
        text = file_path.read_text(encoding="utf-8")
        lines = len(text.splitlines())
        tokens = estimate_tokens(text)
        report.append(
            {
                "path": str(file_path),
                "lines": lines,
                "est_tokens": tokens,
                "bytes": len(text.encode("utf-8")),
            }
        )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Archimedes Token & Context Auditor")
    parser.add_argument("--strict", action="store_true", help="Exit with error if budget exceeded")
    args = parser.parse_args()

    files = audit_files()
    has_violation = False

    print(f"{'Arquivo':<35} | {'Linhas':<8} | {'Est. Tokens':<12} | {'Status'}")
    print("-" * 70)

    for item in files:
        status = "OK"
        if item["path"] == "AGENTS.md" and item["lines"] > MAX_AGENTS_MD_LINES:
            status = f"ALERTA (> {MAX_AGENTS_MD_LINES} linhas)"
            has_violation = True

        print(f"{item['path']:<35} | {item['lines']:<8} | {item['est_tokens']:<12} | {status}")

    print("-" * 70)
    total_tokens = sum(i["est_tokens"] for i in files)
    print(f"Total Estimado de Instruções Carregáveis: ~{total_tokens} tokens")

    if args.strict and has_violation:
        sys.exit(1)


if __name__ == "__main__":
    main()
