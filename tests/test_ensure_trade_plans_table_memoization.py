"""
ST-08 regression test (BLG-BE-98, EPIC-03, v8.9).

GET /trade-plans/tags ~10s p50 root cause: ensure_trade_plans_table() was
called at the top of every trade_plans router endpoint (11 call sites) and
re-ran a CREATE TABLE + 4 CREATE INDEX statements plus 5 further
ensure_*_column() sub-calls (each opening its own DB connection) on every
single request, not just the first — GET /positions/tags has no equivalent
call and is ~4x faster. Fixed with a process-level memoization flag: the
real DDL work runs exactly once per process, every subsequent call is a
cheap no-op.

CI-safe: no live DB — get_db() and the 5 ensure_*_column sub-functions are
all mocked. No live DB or network connections.

Import note: each test imports `database` fresh via importlib inside the
test body (not at module level) and evicts conftest.py's session-scoped
stub first. A module-level import here would bind whatever object happened
to be in sys.modules["database"] at *collection* time, which depends on
what other test files' own module-level code has done to that slot by
then (several files, e.g. test_api_contracts.py, deliberately evict/
reinstall it) — resolving fresh inside each test body is what makes this
file's outcome independent of collection order across the suite.
"""
import importlib
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))


def _real_database_module():
    """Evict any stub/prior binding and (re)import the real database.py."""
    sys.modules.pop("database", None)
    return importlib.import_module("database")


def _mock_conn():
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db = MagicMock()
    mock_get_db.return_value.__enter__.return_value = mock_conn
    return mock_get_db, mock_conn


def test_first_call_performs_the_real_ddl_and_sub_calls():
    database = _real_database_module()
    database._trade_plans_table_ensured = False
    mock_get_db, mock_conn = _mock_conn()

    with (
        patch.object(database, "get_db", mock_get_db),
        patch.object(database, "ensure_regime_context_text_column") as m1,
        patch.object(database, "ensure_trade_plan_tags_column") as m2,
        patch.object(database, "ensure_thesis_provenance_columns") as m3,
        patch.object(database, "ensure_invalidation_condition_column") as m4,
        patch.object(database, "ensure_is_ai_draft_column") as m5,
    ):
        database.ensure_trade_plans_table()

    mock_conn.cursor.assert_called()  # the CREATE TABLE/INDEX cursor was opened
    for m in (m1, m2, m3, m4, m5):
        m.assert_called_once()
    assert database._trade_plans_table_ensured is True

    database._trade_plans_table_ensured = False  # don't leak state to other tests


def test_subsequent_calls_are_a_no_op():
    """Root-cause fix: after the first real call, ensure_trade_plans_table()
    must not re-open a connection or re-run any sub-call — this is what
    turns 11 endpoints' worth of DDL-per-request into DDL-once-per-process."""
    database = _real_database_module()
    database._trade_plans_table_ensured = True  # simulate "already ensured this process"
    mock_get_db, mock_conn = _mock_conn()

    with (
        patch.object(database, "get_db", mock_get_db),
        patch.object(database, "ensure_regime_context_text_column") as m1,
        patch.object(database, "ensure_trade_plan_tags_column") as m2,
        patch.object(database, "ensure_thesis_provenance_columns") as m3,
        patch.object(database, "ensure_invalidation_condition_column") as m4,
        patch.object(database, "ensure_is_ai_draft_column") as m5,
    ):
        database.ensure_trade_plans_table()

    mock_get_db.assert_not_called()
    for m in (m1, m2, m3, m4, m5):
        m.assert_not_called()

    database._trade_plans_table_ensured = False  # don't leak state to other tests
