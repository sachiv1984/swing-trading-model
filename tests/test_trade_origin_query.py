"""
trade_history.trade_origin derivation regression test (ST-31, BLG-FEAT-78,
EPIC-01, v8.4).

`get_trade_history_by_tax_year()` now joins `trade_plans` (via the documented
two-hop `trade_history.position_id = positions.id = trade_plans.position_id`
relationship, data_model.md) and returns a computed `trade_origin` column:
"Signal" when the linked trade plan (if any) has a non-null `signal_id`
(momentum screener signal), else "Manual".

Scope note (ESC-EXEC-20260807-01, resolved): this is NOT a price-alert
indicator. `price_alerts` (BLG-FE-116) has no schema linkage to any trade --
there is no data anywhere that could distinguish an alert-triggered trade
from a manually-initiated one. `signal_id` is the only trigger-shaped field
that actually exists, so the AC was reinterpreted (Product Owner approved)
to use it, correctly labeled.

No live database required -- verifies the exact SQL `get_trade_history_by_
tax_year()` issues via a mocked `get_db()` connection, following the same
pattern used by `test_trade_plans_ticker_index.py` (ST-10, EPIC-03, v8.4).
"""
from datetime import date
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# conftest.py registers a MagicMock stub at sys.modules["database"] (BLG-QA-20).
# Evict it so Python loads the real backend/database.py for the function under test.
sys.modules.pop("database", None)
import database  # noqa: E402


def _mock_conn(fetchall_rows=None):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = fetchall_rows or []
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cursor


def test_query_joins_trade_plans_on_position_id():
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn):
        database.get_trade_history_by_tax_year("portfolio-1", date(2025, 4, 6), date(2026, 4, 5))

    sql = mock_cursor.execute.call_args.args[0]
    assert "LEFT JOIN trade_plans" in sql
    assert "tp.position_id = th.position_id" in sql


def test_query_computes_trade_origin_via_signal_id_case():
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn):
        database.get_trade_history_by_tax_year("portfolio-1", date(2025, 4, 6), date(2026, 4, 5))

    sql = mock_cursor.execute.call_args.args[0]
    assert "tp.signal_id IS NOT NULL THEN 'Signal'" in sql
    assert "ELSE 'Manual'" in sql
    assert "AS trade_origin" in sql


def test_query_does_not_reference_price_alerts():
    """Scope guard (ESC-EXEC-20260807-01): confirms this story did not
    fabricate a price_alerts linkage that doesn't exist in the schema."""
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn):
        database.get_trade_history_by_tax_year("portfolio-1", date(2025, 4, 6), date(2026, 4, 5))

    sql = mock_cursor.execute.call_args.args[0]
    assert "price_alerts" not in sql.lower()


def test_query_preserves_original_portfolio_and_date_filter():
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn):
        database.get_trade_history_by_tax_year("portfolio-1", date(2025, 4, 6), date(2026, 4, 5))

    sql, params = mock_cursor.execute.call_args.args
    assert "th.portfolio_id = %s" in sql
    assert "th.exit_date BETWEEN %s AND %s" in sql
    assert params == ("portfolio-1", date(2025, 4, 6), date(2026, 4, 5))


def test_returns_fetchall_result_unmodified():
    """Confirms the function still returns exactly what the cursor fetches --
    no post-processing added that could drop or reshape rows."""
    fake_rows = [{"id": "trade-1", "trade_origin": "Signal"}, {"id": "trade-2", "trade_origin": "Manual"}]
    mock_conn, mock_cursor = _mock_conn(fetchall_rows=fake_rows)
    with patch.object(database, "get_db", return_value=mock_conn):
        result = database.get_trade_history_by_tax_year("portfolio-1", date(2025, 4, 6), date(2026, 4, 5))

    assert result == fake_rows
