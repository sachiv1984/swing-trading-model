"""
Regression tests for scripts/generate_data_dictionary.py (ST-14, BLG-BE-78,
EPIC-03, v8.4).

Covers the script's pure formatting logic (_format_type, render_markdown) --
no live database required. The script's DB-connection path degrades
gracefully with no DATABASE_URL configured, matching this repo's existing
"no credentials in this checkout" convention (see
scripts/backtest_data_integrity_smoke_test.py) -- covered separately by
running the script directly (see docs/ops/data_dictionary_diff_triage_2026-08-07.md).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import generate_data_dictionary as gdd  # noqa: E402


def test_format_type_varchar_with_length():
    row = {"data_type": "character varying", "udt_name": "varchar", "character_maximum_length": 50}
    assert gdd._format_type(row) == "VARCHAR(50)"


def test_format_type_user_defined_uses_udt_name():
    row = {"data_type": "USER-DEFINED", "udt_name": "jsonb", "character_maximum_length": None}
    assert gdd._format_type(row) == "JSONB"


def test_format_type_plain_type_uppercased():
    row = {"data_type": "uuid", "udt_name": "uuid", "character_maximum_length": None}
    assert gdd._format_type(row) == "UUID"


def test_render_markdown_groups_by_table_and_sorts():
    rows = [
        {"table_name": "positions", "column_name": "id", "data_type": "uuid", "udt_name": "uuid",
         "is_nullable": "NO", "column_default": None, "character_maximum_length": None},
        {"table_name": "cash_transactions", "column_name": "id", "data_type": "uuid", "udt_name": "uuid",
         "is_nullable": "NO", "column_default": None, "character_maximum_length": None},
    ]
    md = gdd.render_markdown(rows, "2026-08-07T00:00:00Z")
    # sorted alphabetically -- cash_transactions before positions
    assert md.index("## cash_transactions") < md.index("## positions")
    assert "**Tables found:** 2" in md
    assert "Not canonical." in md


def test_render_markdown_nullable_and_default_rendering():
    rows = [
        {"table_name": "trade_plans", "column_name": "status", "data_type": "character varying",
         "udt_name": "varchar", "is_nullable": "NO", "column_default": "'draft'::character varying",
         "character_maximum_length": 20},
        {"table_name": "trade_plans", "column_name": "position_id", "data_type": "uuid",
         "udt_name": "uuid", "is_nullable": "YES", "column_default": None,
         "character_maximum_length": None},
    ]
    md = gdd.render_markdown(rows, "2026-08-07T00:00:00Z")
    assert "| status | VARCHAR(20) | NO |" in md
    assert "| position_id | UUID | YES | — |" in md


def test_render_markdown_truncates_long_defaults():
    rows = [
        {"table_name": "t", "column_name": "c", "data_type": "text", "udt_name": "text",
         "is_nullable": "YES", "column_default": "x" * 100, "character_maximum_length": None},
    ]
    md = gdd.render_markdown(rows, "2026-08-07T00:00:00Z")
    assert "..." in md
    # truncated default shorter than the original 100-char value
    default_line = [l for l in md.splitlines() if l.startswith("| c |")][0]
    assert len(default_line) < 150
