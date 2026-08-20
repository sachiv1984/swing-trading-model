"""
trade_plans functional ticker index regression test (ST-10, BLG-BE-82, EPIC-03, v8.4).

`ensure_trade_plans_table()`'s idempotent create-path never actually created
the plain `idx_trade_plans_ticker ON trade_plans(ticker)` that
`docs/specs/data_model.md`'s DS-04 schema block previously (incorrectly)
documented -- and even if it had, `get_trade_plans()`'s actual predicate is
`WHERE UPPER(ticker)=%s`, which a plain index cannot serve. Found by
`docs/ops/db_index_audit_arc4_2026-08-06.md` Finding 1.

No live database required -- verifies the exact SQL statements
`ensure_trade_plans_table()` issues via a mocked `get_db()` connection,
following the same pattern already used by `test_trade_plan_tags.py`.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# conftest.py registers a MagicMock stub at sys.modules["database"] (BLG-QA-20).
# Evict it so Python loads the real backend/database.py for the function under test.
sys.modules.pop("database", None)
import database  # noqa: E402


def _mock_conn():
    mock_cursor = MagicMock()
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cursor


def _executed_sql(mock_cursor) -> list:
    """Flatten every cur.execute(...) call's first positional arg into one list of SQL strings."""
    return [call.args[0] for call in mock_cursor.execute.call_args_list if call.args]


def test_ensure_trade_plans_table_creates_functional_ticker_index():
    # ST-08 (BLG-BE-98, EPIC-03, v8.9): ensure_trade_plans_table() is now
    # memoized process-wide (a prior test in this file, or in another file
    # sharing this process, may have already set the flag) -- reset it so
    # this test actually exercises the real DDL path it's asserting on,
    # rather than silently no-op'ing and passing vacuously.
    database._trade_plans_table_ensured = False
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn), \
         patch.object(database, "ensure_regime_context_text_column"), \
         patch.object(database, "ensure_trade_plan_tags_column"):
        database.ensure_trade_plans_table()

    sql_statements = _executed_sql(mock_cursor)
    ticker_index_statements = [s for s in sql_statements if "idx_trade_plans_ticker" in s.lower() or "idx_trade_plans_ticker".lower() in s.lower()]

    assert any("UPPER(ticker)" in s for s in sql_statements), (
        "ensure_trade_plans_table() must create a functional index on UPPER(ticker) "
        "to match get_trade_plans()'s actual WHERE UPPER(ticker)=%s predicate"
    )


def test_ensure_trade_plans_table_does_not_create_plain_ticker_index():
    database._trade_plans_table_ensured = False  # see comment in the test above
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn), \
         patch.object(database, "ensure_regime_context_text_column"), \
         patch.object(database, "ensure_trade_plan_tags_column"):
        database.ensure_trade_plans_table()

    sql_statements = _executed_sql(mock_cursor)
    # The old plain (non-functional) index name must not be (re-)created --
    # it was never used by the live UPPER(ticker) predicate.
    #
    # ST-08 re-review (retry 1, EPIC-03, v8.9): the search literal itself
    # contains spaces, so comparing it against a space-stripped haystack
    # (s.lower().replace(" ", "")) could never match -- the assertion was
    # vacuously true regardless of what SQL actually ran. Strip spaces from
    # the search literal too so the comparison is apples-to-apples.
    target = "idx_trade_plans_ticker on trade_plans(ticker)".replace(" ", "")
    assert not any(
        target in s.lower().replace(" ", "")
        for s in sql_statements
    ), "must not create the plain, non-functional idx_trade_plans_ticker index"


def test_get_trade_plans_ticker_filter_uses_upper():
    """Confirms the predicate this index must serve -- get_trade_plans(ticker=...)
    filters on UPPER(ticker), which is exactly what idx_trade_plans_ticker_upper indexes."""
    mock_conn, mock_cursor = _mock_conn()
    mock_cursor.fetchall.return_value = []
    with patch.object(database, "get_db", return_value=mock_conn):
        database.get_trade_plans("portfolio-1", ticker="nvda")

    sql_statements = _executed_sql(mock_cursor)
    assert any("UPPER(ticker)" in s for s in sql_statements)
