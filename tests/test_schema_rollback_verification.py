"""
ST-09 (BLG-BE-49, EPIC-02, v9.0): down-migration rollback verification for
the 5 most recent schema migrations.

**Adaptation note (implementation note, not a spec deviation — see
execution_state.json ST-09):** `database_migration_governance.md` describes
a `backend/migrations/<YYYYMMDD>_<NNN>_<desc>.sql` file convention with a
paired `rollback_<file>.sql`, but no such directory or files actually exist
anywhere in this repo — schema changes are applied via inline, idempotent
`ensure_*_table()`/`ensure_*_column()`/`ensure_*_index()` functions in
`backend/database.py` instead (confirmed via repo-wide search). This test
file satisfies the story's intent — verified rollback safety for the 5
most recent schema changes — against the mechanism this codebase actually
uses, rather than the file convention the governance doc describes but was
never adopted in practice.

**"5 most recent" identification (git pickaxe, reverse-chronological by
commit date, `backend/database.py`):**
1. `ensure_claude_audit_log_compliance_check_column` — 53286f6c, 2026-08-20 (ST-06, EPIC-02, v8.9)
2. `ensure_trade_debriefs_table`                     — 53286f6c, 2026-08-20 (ST-06, EPIC-02, v8.9)
3. `ensure_backtest_rule_run_tables`                 — 967e77f4, 2026-08-18 (ST-07, EPIC-02, v8.9)
4. `ensure_triggered_by_price_alert_id_column`       — 7bba5c6e, 2026-08-14 (ST-09, EPIC-02, v8.8)
5. `ensure_signals_ticker_upper_index`                — 7bba5c6e, 2026-08-14 (ST-12, EPIC-02, v8.8)

**Pattern (documented here for future migrations, per this story's own
second AC):** for each new schema-changing `ensure_*` function added to
`backend/database.py`, add a corresponding test below (or a new one
following this file's pattern) that: (1) ensures any prerequisite
table(s) exist with a minimal stub if the real `ensure_*_table()` isn't
itself in scope, (2) runs the forward migration and asserts the new
table/column/index is present, (3) runs a DOWN statement (`DROP COLUMN
IF EXISTS` / `DROP TABLE IF EXISTS` / `DROP INDEX IF EXISTS` — all
idempotent, safe to re-run) and asserts it's gone, (4) re-runs the
forward migration and asserts it's back — proving the forward migration
is safe to re-apply after a rollback, not just safe to apply once. Phase
B CI (`.github/workflows/ci-tests.yml` `pytest-phase-b` job, real
`postgres:15` service) is required — these tests are skipped in Phase A
(stub `DATABASE_URL`), same as `tests/test_schema.py`'s existing
pattern, which this file follows.
"""
import os
import sys
import pytest
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

_DATABASE_URL = os.getenv("DATABASE_URL", "")
_SKIP_PHASE_A = "stub" in _DATABASE_URL.lower()
_SKIP_REASON = "Phase A — DATABASE_URL is a stub; rollback verification requires real Postgres (Phase B)"


def _get_conn():
    return psycopg2.connect(_DATABASE_URL, cursor_factory=RealDictCursor)


def _column_exists(conn, table, column) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT 1 FROM information_schema.columns WHERE table_name = %s AND column_name = %s",
            (table, column),
        )
        return cur.fetchone() is not None


def _table_exists(conn, table) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_name = %s",
            (table,),
        )
        return cur.fetchone() is not None


def _index_exists(conn, index_name) -> bool:
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_indexes WHERE indexname = %s", (index_name,))
        return cur.fetchone() is not None


def _real_database_module():
    sys.modules.pop("database", None)
    import database
    return database


@pytest.mark.skipif(_SKIP_PHASE_A, reason=_SKIP_REASON)
class TestClaudeAuditLogComplianceCheckColumnRollback:
    """1. ensure_claude_audit_log_compliance_check_column (53286f6c, ST-06, v8.9)."""

    def test_rollback_then_reapply(self):
        database = _real_database_module()
        conn = _get_conn()
        try:
            database.ensure_claude_audit_log_table()
            database.ensure_claude_audit_log_compliance_check_column()
            assert _column_exists(conn, "claude_audit_log", "compliance_check_result")

            # DOWN
            with conn.cursor() as cur:
                cur.execute("ALTER TABLE claude_audit_log DROP COLUMN IF EXISTS compliance_check_result")
            conn.commit()
            assert not _column_exists(conn, "claude_audit_log", "compliance_check_result")

            # Re-apply (forward again, post-rollback)
            database.ensure_claude_audit_log_compliance_check_column()
            assert _column_exists(conn, "claude_audit_log", "compliance_check_result")
        finally:
            conn.close()


@pytest.mark.skipif(_SKIP_PHASE_A, reason=_SKIP_REASON)
class TestTradeDebriefsTableRollback:
    """2. ensure_trade_debriefs_table (53286f6c, ST-06, v8.9).

    trade_debriefs.trade_history_id has a FK to trade_history(id) — a
    minimal stub trade_history table is created first (same pattern as
    tests/test_schema.py's _ensure_positions_table)."""

    def test_rollback_then_reapply(self):
        database = _real_database_module()
        conn = _get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS trade_history (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid()
                    )
                """)
            conn.commit()

            database.ensure_trade_debriefs_table()
            assert _table_exists(conn, "trade_debriefs")

            # DOWN
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS trade_debriefs")
            conn.commit()
            assert not _table_exists(conn, "trade_debriefs")

            # Re-apply
            database.ensure_trade_debriefs_table()
            assert _table_exists(conn, "trade_debriefs")
        finally:
            conn.close()


@pytest.mark.skipif(_SKIP_PHASE_A, reason=_SKIP_REASON)
class TestBacktestRuleRunTablesRollback:
    """3. ensure_backtest_rule_run_tables (967e77f4, ST-07, v8.9)."""

    def test_rollback_then_reapply(self):
        database = _real_database_module()
        conn = _get_conn()
        try:
            database.ensure_backtest_rule_run_tables()
            assert _table_exists(conn, "backtest_rule_runs")

            # DOWN
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS backtest_rule_runs")
            conn.commit()
            assert not _table_exists(conn, "backtest_rule_runs")

            # Re-apply
            database.ensure_backtest_rule_run_tables()
            assert _table_exists(conn, "backtest_rule_runs")
        finally:
            conn.close()


@pytest.mark.skipif(_SKIP_PHASE_A, reason=_SKIP_REASON)
class TestTriggeredByPriceAlertIdColumnRollback:
    """4. ensure_triggered_by_price_alert_id_column (7bba5c6e, ST-09, v8.8)."""

    def test_rollback_then_reapply(self):
        database = _real_database_module()
        conn = _get_conn()
        try:
            database.ensure_trade_plans_table()
            database.ensure_triggered_by_price_alert_id_column()
            assert _column_exists(conn, "trade_plans", "triggered_by_price_alert_id")

            # DOWN
            with conn.cursor() as cur:
                cur.execute("ALTER TABLE trade_plans DROP COLUMN IF EXISTS triggered_by_price_alert_id")
            conn.commit()
            assert not _column_exists(conn, "trade_plans", "triggered_by_price_alert_id")

            # Re-apply
            database.ensure_triggered_by_price_alert_id_column()
            assert _column_exists(conn, "trade_plans", "triggered_by_price_alert_id")
        finally:
            conn.close()


@pytest.mark.skipif(_SKIP_PHASE_A, reason=_SKIP_REASON)
class TestSignalsTickerUpperIndexRollback:
    """5. ensure_signals_ticker_upper_index (7bba5c6e, ST-12, v8.8).

    Minimal stub signals table created first — the real signals table's
    full schema is out of scope for this index-rollback check."""

    def test_rollback_then_reapply(self):
        database = _real_database_module()
        conn = _get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS signals (
                        id SERIAL PRIMARY KEY,
                        ticker VARCHAR(20)
                    )
                """)
            conn.commit()

            database.ensure_signals_ticker_upper_index()
            assert _index_exists(conn, "idx_signals_ticker_upper")

            # DOWN
            with conn.cursor() as cur:
                cur.execute("DROP INDEX IF EXISTS idx_signals_ticker_upper")
            conn.commit()
            assert not _index_exists(conn, "idx_signals_ticker_upper")

            # Re-apply
            database.ensure_signals_ticker_upper_index()
            assert _index_exists(conn, "idx_signals_ticker_upper")
        finally:
            conn.close()
