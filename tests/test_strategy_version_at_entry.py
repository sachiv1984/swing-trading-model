"""
strategy_version_at_entry regression tests (ST-01, EPIC-01, v8.0, BLG-SPEC-78).

Forward-only field on trade_plans and positions, stamped at row-creation time
from strategy_version_registry.get_current_strategy_version(). No backfill of
existing rows — see database.ensure_strategy_version_at_entry_columns()
docstring and docs/specs/data_model.md DS-11.

No live database calls — database.create_trade_plan / create_position are
exercised against a mocked get_db() connection, following the same pattern
as test_trade_plan_tags.py.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# conftest.py registers a MagicMock stub at sys.modules["database"] (BLG-QA-20).
# Evict it so Python loads the real backend/database.py for the functions under test.
# Private copy of the real backend/database.py; conftest's sys.modules["database"]
# stub stays in place for every other test file (ST-14, BLG-QA-190).
from tests._real_database import load_real_database  # noqa: E402

database = load_real_database("database_real_for_test_strategy_version_at_entry")

from strategy_version_registry import (  # noqa: E402
    get_current_strategy_version,
    STRATEGY_VERSION_REGISTRY,
)


# ---------------------------------------------------------------------------
# get_current_strategy_version — pure function
# ---------------------------------------------------------------------------

def test_returns_latest_registry_entry():
    assert get_current_strategy_version() == STRATEGY_VERSION_REGISTRY[-1]["version"]


def test_returns_a_string_matching_current_strategy_rules_version():
    # The current behavioural version is the newest strategy_rules.md Change
    # Log row that is not documentation-only (2026-10-06 coverage rule). Read
    # from the file rather than a literal, so it does not go stale (it pinned
    # "1.4" until ST-16, v9.11, registered 1.15).
    import re
    from pathlib import Path
    from strategy_version_registry import DOCUMENTATION_ONLY_VERSIONS

    rules = (Path(__file__).parent.parent / "claude" / "strategy" / "strategy_rules.md").read_text()
    logged = re.findall(r"^\| (\d+\.\d+) \|", rules, re.MULTILINE)
    behavioural = [v for v in logged if v not in DOCUMENTATION_ONLY_VERSIONS]
    newest = max(behavioural, key=lambda v: tuple(int(x) for x in v.split(".")))
    assert get_current_strategy_version() == newest


# ---------------------------------------------------------------------------
# database.create_trade_plan / create_position — column wiring
# ---------------------------------------------------------------------------

def _mock_conn(returned_row):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = returned_row
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cursor


def _column_index(sql, column):
    """Locate `column`'s positional index in an `INSERT INTO t (a, b, c) VALUES (...)`
    statement, so tests assert against the actual param bound to that column rather
    than an assumed fixed position (e.g. "last") -- a fragile assumption once later
    stories legitimately append further columns after this one (ST-12, EPIC-03, v8.4:
    thesis_model_version/thesis_prompt_version added after strategy_version_at_entry
    on trade_plans, which broke a prior `params[-1]`-based version of this test)."""
    columns_block = sql.split("(", 1)[1].split(")", 1)[0]
    columns = [c.strip() for c in columns_block.split(",")]
    return columns.index(column)


def test_create_trade_plan_passes_strategy_version_at_entry_to_insert():
    mock_conn, mock_cursor = _mock_conn({"id": "plan-1", "strategy_version_at_entry": "1.4"})
    data = {
        "ticker": "AAPL",
        "market": "US",
        "strategy_version_at_entry": "1.4",
    }
    with patch.object(database, "get_db", return_value=mock_conn):
        database.create_trade_plan("portfolio-1", data)

    args, _ = mock_cursor.execute.call_args
    sql, params = args
    assert "strategy_version_at_entry" in sql
    assert params[_column_index(sql, "strategy_version_at_entry")] == "1.4"


def test_create_trade_plan_defaults_to_none_when_absent():
    mock_conn, mock_cursor = _mock_conn({"id": "plan-1", "strategy_version_at_entry": None})
    data = {"ticker": "AAPL", "market": "US"}
    with patch.object(database, "get_db", return_value=mock_conn):
        database.create_trade_plan("portfolio-1", data)

    args, _ = mock_cursor.execute.call_args
    sql, params = args
    assert params[_column_index(sql, "strategy_version_at_entry")] is None


def test_create_position_passes_strategy_version_at_entry_to_insert():
    mock_conn, mock_cursor = _mock_conn({"id": "pos-1", "strategy_version_at_entry": "1.4"})
    position_data = {
        "ticker": "AAPL",
        "market": "US",
        "strategy_version_at_entry": "1.4",
    }
    with patch.object(database, "get_db", return_value=mock_conn):
        database.create_position("portfolio-1", position_data)

    args, _ = mock_cursor.execute.call_args
    sql, params = args
    assert "strategy_version_at_entry" in sql
    # Look the value up by column position rather than assuming it is last
    # (ST-02, v9.10, appended atr_source after it).
    columns = [c.strip() for c in sql.split("INSERT INTO positions (")[1].split(")")[0].split(",")]
    assert params[columns.index("strategy_version_at_entry")] == "1.4"
    assert params[columns.index("atr_source")] is None


def test_ensure_strategy_version_at_entry_columns_is_idempotent_ddl():
    mock_conn, mock_cursor = _mock_conn(None)
    with patch.object(database, "get_db", return_value=mock_conn):
        database.ensure_strategy_version_at_entry_columns()

    executed_sql = [call.args[0] for call in mock_cursor.execute.call_args_list]
    assert any("ADD COLUMN IF NOT EXISTS strategy_version_at_entry" in s and "trade_plans" in s for s in executed_sql)
    assert any("ADD COLUMN IF NOT EXISTS strategy_version_at_entry" in s and "positions" in s for s in executed_sql)
