"""Unit tests for get_monthly_claude_cost (ST-07, EPIC-07, v7.6, BLG-FEAT-77).

Reframed per ESC-EXEC-20260720-01: sources claude_audit_log (the immutable
Claude API audit trail), aggregated by calendar month.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# See tests/test_signal_write_sanitization.py for the rationale — conftest.py's
# database stub lacks the real implementation under test here.
sys.modules.pop("database", None)
import database  # noqa: E402


def _mock_conn(row):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = row
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cursor


def test_returns_total_and_count():
    mock_conn, mock_cursor = _mock_conn({"total_cost": 7.42, "request_count": 12})
    with patch.object(database, "get_db", return_value=mock_conn):
        with patch.object(database, "ensure_claude_audit_log_table"):
            result = database.get_monthly_claude_cost()
    assert result == {"total_cost_usd": 7.42, "request_count": 12}


def test_zero_spend_month_returns_zero_not_none():
    mock_conn, mock_cursor = _mock_conn({"total_cost": 0.0, "request_count": 0})
    with patch.object(database, "get_db", return_value=mock_conn):
        with patch.object(database, "ensure_claude_audit_log_table"):
            result = database.get_monthly_claude_cost()
    assert result["total_cost_usd"] == 0.0
    assert result["request_count"] == 0


def test_query_filters_on_current_calendar_month():
    mock_conn, mock_cursor = _mock_conn({"total_cost": 1.0, "request_count": 1})
    with patch.object(database, "get_db", return_value=mock_conn):
        with patch.object(database, "ensure_claude_audit_log_table"):
            database.get_monthly_claude_cost()

    executed_sql = mock_cursor.execute.call_args[0][0]
    assert "claude_audit_log" in executed_sql
    assert "date_trunc('month', NOW())" in executed_sql


def test_db_failure_returns_zero_defaults_not_exception():
    """Fail-safe convention (matches get_daily_ai_cost) — a DB error must not
    propagate to the endpoint as a 500; it degrades to a zero-cost reading."""
    with patch.object(database, "get_db", side_effect=Exception("connection refused")):
        result = database.get_monthly_claude_cost()
    assert result == {"total_cost_usd": 0.0, "request_count": 0}
