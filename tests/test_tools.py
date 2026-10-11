"""Deterministic unit tests for Archimedes core tools."""

import tempfile
from pathlib import Path

from tools.rag import add_note, search_notes, sync_notes
from tools.scope_monitor import check_directory_density
from tools.token_counter import audit_files, estimate_tokens
from tools.vault import get_or_create_key, load_vault, save_vault


def test_estimate_tokens():
    text = "hello world"
    assert estimate_tokens(text) == len(text) // 4


def test_vault_roundtrip():
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_dir = Path(tmpdir) / ".vault"
        vault_file = vault_dir / "credentials.vault"

        key = get_or_create_key(vault_dir)
        assert len(key) == 32

        # Initial should be empty
        assert load_vault(vault_file, key) == {}

        # Save secret
        save_vault({"MY_TOKEN": "secret_abc123"}, vault_file, key)

        # Decrypt secret
        loaded = load_vault(vault_file, key)
        assert loaded.get("MY_TOKEN") == "secret_abc123"


def test_rag_fts5_indexing_and_search():
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        db_path = base / "memoria.db"
        notes_dir = base / "notas"

        # Add note
        note_path = add_note(
            title="Teste Arquitetura FTS5",
            content="Esta é uma nota de validação da memória SQLite FTS5.",
            tags=["teste", "fts5"],
            notes_dir=notes_dir,
            db_path=db_path,
        )
        assert note_path.exists()

        # Sync
        total = sync_notes(notes_dir, db_path)
        assert total >= 1

        # Search match
        matches = search_notes("FTS5", db_path=db_path)
        assert len(matches) > 0
        assert "Teste Arquitetura FTS5" in matches[0]["title"]


def test_token_counter_audit():
    report = audit_files()
    assert len(report) > 0
    agents_md = next((r for r in report if r["path"] == "AGENTS.md"), None)
    assert agents_md is not None
    assert agents_md["lines"] <= 150


def test_scope_monitor():
    density = check_directory_density()
    assert isinstance(density, list)
    for entry in density:
        assert entry["status"] in {"normal", "warning", "critical"}


def test_autopilot_full_cycle():
    from tools.autopilot import run_full_cycle

    res = run_full_cycle(auto_fix=True)
    assert res["status"] == "HEALTHY"
    assert res["code_hygiene"]["ruff"] == "passed"
    assert res["code_hygiene"]["pytest"] == "passed"
    assert res["scope_and_tokens"]["agents_md_budget_ok"] is True
