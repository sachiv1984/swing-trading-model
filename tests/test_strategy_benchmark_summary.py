"""
Tests for database.get_backtest_summary()'s last_imported_at formatting.

ST-03 (BLG-OPS-143, EPIC-01, v8.8): imported_at is a TIMESTAMPTZ column, so
psycopg2 returns a timezone-aware datetime whose .isoformat() already ends in
"+00:00". The pre-fix code appended a literal "Z" on top regardless, producing
a malformed double-suffixed timestamp ("...+00:00Z") that is not valid
ISO-8601 and that `new Date(...)` on the frontend parses as Invalid Date —
this was the root cause of the Strategy Benchmark page's "Benchmark data as
of ..." line never rendering a date (it silently fell back to "—").
"""
import sys
import importlib
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))


def _real_database_module():
    """Re-resolve the real backend/database.py fresh, regardless of what other
    test files' collection-time `sys.modules["database"]` swaps left behind —
    other files alphabetically before/after this one (test_api_contracts.py,
    test_strategy_version_at_entry.py, etc.) also evict/replace
    sys.modules["database"] at their own module scope, and pytest completes
    collection for the whole session before running any test, so a
    module-level import here can silently end up bound to a different
    `database` object than whatever `patch("database.get_db")` resolves at
    test-run time. Doing both the reload and the patch inside the same test
    call keeps them pointed at the identical object.
    """
    sys.modules.pop("database", None)
    return importlib.import_module("database")


def _mock_cursor_for_summary(last_imported_value):
    """Build a cursor mock matching get_backtest_summary()'s query sequence:
    1. Panel 1 aggregate stats -> fetchone()
    2. Panel 2 yearly breakdown -> fetchall()
    3. MAX(imported_at) -> fetchone()
    4. Distinct available years -> fetchall()
    """
    cur = MagicMock()
    cur.fetchone.side_effect = [
        {"total_trades": 583, "win_rate_pct": 52.3, "avg_pnl_gbp": 922.16,
         "total_pnl_gbp": 537619.91, "avg_hold_days": 18.7},
        {"last_imported": last_imported_value},
    ]
    cur.fetchall.side_effect = [
        [],  # yearly_breakdown
        [{"entry_year": 2026}],  # available_years
    ]
    return cur


def _mock_get_db(cur):
    conn = MagicMock()
    conn.cursor.return_value.__enter__.return_value = cur
    ctx = MagicMock()
    ctx.__enter__.return_value = conn
    return ctx


class TestLastImportedAtFormat:
    def test_timezone_aware_timestamp_produces_single_z_suffix(self):
        """A TIMESTAMPTZ value (tz-aware datetime, as psycopg2 actually returns)
        must not produce a double-suffixed '+00:00Z' string."""
        db = _real_database_module()
        aware_ts = datetime(2026, 8, 14, 3, 28, 0, 319748, tzinfo=timezone.utc)
        cur = _mock_cursor_for_summary(aware_ts)
        with patch.object(db, "get_db", return_value=_mock_get_db(cur)):
            result = db.get_backtest_summary()

        last_imported_at = result["last_imported_at"]
        assert last_imported_at is not None
        assert not last_imported_at.endswith("+00:00Z"), (
            f"malformed double-suffixed timestamp: {last_imported_at}"
        )
        assert last_imported_at.endswith("Z")
        assert last_imported_at.count("+") == 0

    def test_result_is_valid_iso8601_parseable(self):
        """The frontend does `new Date(val)` — the value must round-trip
        through Python's own ISO-8601 parser after stripping the Z suffix."""
        db = _real_database_module()
        aware_ts = datetime(2026, 8, 14, 3, 28, 0, 319748, tzinfo=timezone.utc)
        cur = _mock_cursor_for_summary(aware_ts)
        with patch.object(db, "get_db", return_value=_mock_get_db(cur)):
            result = db.get_backtest_summary()

        last_imported_at = result["last_imported_at"]
        # Strip trailing Z and confirm the remainder parses as a naive ISO-8601 datetime.
        parsed = datetime.fromisoformat(last_imported_at[:-1])
        assert parsed.year == 2026
        assert parsed.month == 8
        assert parsed.day == 14

    def test_none_when_no_trades_imported(self):
        db = _real_database_module()
        cur = _mock_cursor_for_summary(None)
        with patch.object(db, "get_db", return_value=_mock_get_db(cur)):
            result = db.get_backtest_summary()
        assert result["last_imported_at"] is None
