#!/usr/bin/env python3
"""Deterministic RAG & Long-Term Memory Tool for Archimedes (SQLite FTS5).

Manages context/memory/memoria.db, indexes atomic notes, and runs surgical full-text search.
"""

from __future__ import annotations

import argparse
import re
import sqlite3
from datetime import date
from pathlib import Path

import yaml

DEFAULT_DB_PATH = Path("context/memory/memoria.db")
DEFAULT_NOTES_DIR = Path("context/memory/notas")


def get_db_connection(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Create or connect to SQLite database and ensure FTS5 schema exists."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                date TEXT,
                author TEXT,
                tags TEXT,
                impact TEXT,
                status TEXT,
                filepath TEXT,
                content TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
                id UNINDEXED,
                title,
                tags,
                content,
                content='notes',
                content_rowid='rowid'
            )
            """
        )
        # Triggers to keep FTS5 in sync
        conn.execute(
            """
            CREATE TRIGGER IF NOT EXISTS notes_ai AFTER INSERT ON notes BEGIN
                INSERT INTO notes_fts(rowid, id, title, tags, content)
                VALUES (new.rowid, new.id, new.title, new.tags, new.content);
            END;
            """
        )
        conn.execute(
            """
            CREATE TRIGGER IF NOT EXISTS notes_ad AFTER DELETE ON notes BEGIN
                INSERT INTO notes_fts(notes_fts, rowid, id, title, tags, content)
                VALUES('delete', old.rowid, old.id, old.title, old.tags, old.content);
            END;
            """
        )
        conn.execute(
            """
            CREATE TRIGGER IF NOT EXISTS notes_au AFTER UPDATE ON notes BEGIN
                INSERT INTO notes_fts(notes_fts, rowid, id, title, tags, content)
                VALUES('delete', old.rowid, old.id, old.title, old.tags, old.content);
                INSERT INTO notes_fts(rowid, id, title, tags, content)
                VALUES (new.rowid, new.id, new.title, new.tags, new.content);
            END;
            """
        )

    return conn


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from Markdown text."""
    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
    match = re.match(pattern, content, re.DOTALL)
    if match:
        raw_meta = match.group(1)
        body = match.group(2)
        try:
            meta = yaml.safe_load(raw_meta) or {}
            return meta, body
        except (yaml.YAMLError, ValueError, TypeError):
            return {}, content
    return {}, content


def sync_notes(notes_dir: Path = DEFAULT_NOTES_DIR, db_path: Path = DEFAULT_DB_PATH) -> int:
    """Index all Markdown notes from directory into SQLite FTS5."""
    if not notes_dir.exists():
        notes_dir.mkdir(parents=True, exist_ok=True)
        return 0

    conn = get_db_connection(db_path)
    count = 0

    with conn:
        for md_file in notes_dir.glob("*.md"):
            text = md_file.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(text)

            note_id = str(meta.get("id") or md_file.stem)
            title = str(meta.get("titulo") or meta.get("title") or md_file.stem)
            note_date = str(meta.get("data") or meta.get("date") or "")
            author = str(meta.get("autor") or meta.get("author") or "Decisor Técnico")
            raw_tags = meta.get("tags") or []
            tags = ", ".join(raw_tags) if isinstance(raw_tags, list) else str(raw_tags)
            impact = str(meta.get("impacto") or meta.get("impact") or "medio")
            status = str(meta.get("status") or "ativo")

            conn.execute(
                """
                INSERT INTO notes (id, title, date, author, tags, impact, status, filepath, content)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    title=excluded.title,
                    date=excluded.date,
                    author=excluded.author,
                    tags=excluded.tags,
                    impact=excluded.impact,
                    status=excluded.status,
                    filepath=excluded.filepath,
                    content=excluded.content
                """,
                (
                    note_id,
                    title,
                    note_date,
                    author,
                    tags,
                    impact,
                    status,
                    str(md_file),
                    body.strip(),
                ),
            )
            count += 1

    return count


def search_notes(query: str, db_path: Path = DEFAULT_DB_PATH, limit: int = 5) -> list[dict]:
    """Search notes using SQLite FTS5 match."""
    conn = get_db_connection(db_path)
    # Sanitize FTS5 query terms
    clean_query = " ".join(re.findall(r"\w+", query))
    if not clean_query:
        return []

    # Execute FTS match
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT n.id, n.title, n.tags, n.filepath, snippet(notes_fts, 3, '[', ']', '...', 15) as snippet
            FROM notes_fts
            JOIN notes n ON notes_fts.id = n.id
            WHERE notes_fts MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (f"{clean_query}*", limit),
        )
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.OperationalError:
        # Fallback to LIKE if syntax fails
        cursor.execute(
            """
            SELECT id, title, tags, filepath, substr(content, 1, 100) as snippet
            FROM notes
            WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
            LIMIT ?
            """,
            (f"%{query}%", f"%{query}%", f"%{query}%", limit),
        )
        return [dict(row) for row in cursor.fetchall()]


def add_note(
    title: str,
    content: str,
    tags: list[str],
    impact: str = "medio",
    notes_dir: Path = DEFAULT_NOTES_DIR,
    db_path: Path = DEFAULT_DB_PATH,
) -> Path:
    """Create a new atomic note file conforming to v8 frontmatter and index it."""
    notes_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    note_num = len(list(notes_dir.glob("*.md"))) + 1
    note_id = f"NOTA-{note_num:04d}"

    filename = f"{note_id.lower()}_{re.sub(r'[^a-zA-Z0-9_]', '_', title.lower())}.md"
    file_path = notes_dir / filename

    yaml_header = {
        "id": note_id,
        "titulo": title,
        "data": today,
        "autor": "Decisor Técnico",
        "tags": tags,
        "impacto": impact,
        "status": "ativo",
        "referencias": [],
    }

    doc = "---\n" + yaml.dump(yaml_header, sort_keys=False, allow_unicode=True) + "---\n\n" + content
    file_path.write_text(doc, encoding="utf-8")

    sync_notes(notes_dir, db_path)
    return file_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Archimedes RAG & Long-Term Memory Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # sync
    subparsers.add_parser("sync", help="Synchronize Markdown notes into SQLite FTS5")

    # search
    search_parser = subparsers.add_parser("search", help="Search memory via FTS5")
    search_parser.add_argument("query", help="Search query string")
    search_parser.add_argument("--limit", type=int, default=5, help="Result limit")

    # add-note
    add_parser = subparsers.add_parser("add-note", help="Create a standardized atomic note")
    add_parser.add_argument("--title", required=True, help="Note title")
    add_parser.add_argument("--content", required=True, help="Note body text")
    add_parser.add_argument("--tags", default="archimedes", help="Comma-separated tags")
    add_parser.add_argument(
        "--impact", choices=["alto", "medio", "baixo"], default="medio", help="Impact level"
    )

    args = parser.parse_args()

    if args.command == "sync":
        total = sync_notes()
        print(f"Indexed {total} atomic notes into {DEFAULT_DB_PATH}")

    elif args.command == "search":
        results = search_notes(args.query, limit=args.limit)
        if not results:
            print(f"No results found for query: '{args.query}'")
        else:
            print(f"Found {len(results)} match(es):")
            for r in results:
                print(f"\n[{r['id']}] {r['title']} ({r.get('filepath')})")
                print(f"Tags: {r.get('tags')}")
                print(f"Snippet: {r.get('snippet')}")

    elif args.command == "add-note":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        created = add_note(title=args.title, content=args.content, tags=tags, impact=args.impact)
        print(f"Created atomic note at: {created}")


if __name__ == "__main__":
    main()
