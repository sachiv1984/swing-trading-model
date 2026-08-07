#!/usr/bin/env python3
"""
generate_data_dictionary.py — ST-14 (BLG-BE-78, EPIC-03, v8.4)

Generates a data dictionary directly from the live database schema
(information_schema.tables / information_schema.columns), as a
mechanically-derived cross-check against docs/specs/data_model.md's
hand-maintained canonical schema. Confirms columns actually documented
match what the live schema actually has — the class of drift found by
db_index_audit_arc4_2026-08-06.md (undocumented tables) and
BLG-SPEC-116 (a structural defect a hand-maintained doc could not
self-detect).

Not a replacement for data_model.md: this generates a structural
snapshot only (table/column/type/nullable/default) with no narrative
purpose/populating-function context — data_model.md remains canonical
and hand-maintained; this script's output is a triage input for keeping
it accurate.

Usage:
    python3 scripts/generate_data_dictionary.py [--output PATH]

If DATABASE_URL / DB credentials are unavailable in this checkout, exits
gracefully with a clear message rather than failing -- matching this
repo's existing "no credentials in this checkout" convention (see
scripts/backtest_data_integrity_smoke_test.py, roadmap_prompt.md v9.6
STEP 2.3).
"""
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "docs" / "ops" / "generated_data_dictionary.md"

_COLUMNS_QUERY = """
    SELECT
        c.table_name,
        c.column_name,
        c.data_type,
        c.udt_name,
        c.is_nullable,
        c.column_default,
        c.character_maximum_length
    FROM information_schema.columns c
    JOIN information_schema.tables t
        ON t.table_name = c.table_name AND t.table_schema = c.table_schema
    WHERE c.table_schema = 'public'
        AND t.table_type = 'BASE TABLE'
    ORDER BY c.table_name, c.ordinal_position
"""


def _connect():
    """Returns a live DB connection, or None if unreachable in this checkout."""
    sys.path.insert(0, str(REPO_ROOT / "backend"))
    try:
        from database import get_db  # noqa: PLC0415
    except Exception as exc:
        print(f"[generate_data_dictionary] Cannot import backend.database: {exc}")
        return None

    try:
        conn = get_db()
        return conn
    except Exception as exc:
        print(f"[generate_data_dictionary] No live database reachable in this checkout: {exc}")
        return None


def _fetch_columns(conn):
    with conn:
        with conn.cursor() as cur:
            cur.execute(_COLUMNS_QUERY)
            return [dict(r) for r in cur.fetchall()]


def _format_type(row: dict) -> str:
    t = row["data_type"]
    if t == "character varying" and row.get("character_maximum_length"):
        return f"VARCHAR({row['character_maximum_length']})"
    if t == "USER-DEFINED":
        return row["udt_name"].upper()
    return t.upper()


def render_markdown(rows: list, generated_at: str) -> str:
    tables = {}
    for row in rows:
        tables.setdefault(row["table_name"], []).append(row)

    lines = [
        "# Generated Data Dictionary (Live Schema Snapshot)",
        "",
        "**Owner:** Data Model & Domain Schema Owner",
        "**Class:** Generated Artefact (not hand-maintained — regenerate via `scripts/generate_data_dictionary.py`)",
        "**Status:** Active",
        f"**Generated:** {generated_at}",
        "",
        "> **Not canonical.** `docs/specs/data_model.md` remains the canonical, hand-maintained schema of record "
        "(purpose, populating function, migration history). This file is a mechanically-derived structural "
        "snapshot for cross-checking drift only (ST-14, BLG-BE-78, EPIC-03, v8.4).",
        "",
        f"**Tables found:** {len(tables)}",
        "",
    ]

    for table_name in sorted(tables):
        cols = tables[table_name]
        lines.append(f"## {table_name}")
        lines.append("")
        lines.append("| Column | Type | Nullable | Default |")
        lines.append("|--------|------|----------|---------|")
        for c in cols:
            default = c["column_default"] or ""
            if default and len(default) > 40:
                default = default[:37] + "..."
            lines.append(
                f"| {c['column_name']} | {_format_type(c)} | "
                f"{'YES' if c['is_nullable'] == 'YES' else 'NO'} | {default or '—'} |"
            )
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output markdown file path")
    args = parser.parse_args()

    conn = _connect()
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if conn is None:
        print(
            "[generate_data_dictionary] No live database reachable in this checkout — "
            "skipping generation. Run this script in an environment with DATABASE_URL "
            "configured (e.g. CI with the Postgres service, or a local dev DB) to "
            "produce a real snapshot."
        )
        return 0

    try:
        rows = _fetch_columns(conn)
    except Exception as exc:
        print(f"[generate_data_dictionary] Query failed: {exc}")
        return 1

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown(rows, generated_at))
    print(f"[generate_data_dictionary] Wrote {len(rows)} column(s) across "
          f"{len({r['table_name'] for r in rows})} table(s) to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
