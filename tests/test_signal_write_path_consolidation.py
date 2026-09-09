"""
Signal write-path consolidation regression tests (ST-02, EPIC-01, v9.3, BLG-BE-44).

database.create_signal() and database.create_rebalance_exit_signal() were
previously two independently-implemented INSERT ... ON CONFLICT ... DO UPDATE
statements against the `signals` table. Both now route through a single
shared helper, database._signal_upsert(), parameterised by which columns
each caller updates on conflict.

These tests confirm the consolidation introduced no behavioural change:
- create_signal() must NOT reset `status` on conflict (would clobber a
  signal already marked `entered`/`dismissed`/etc).
- create_rebalance_exit_signal() must NOT overwrite real sizing fields with
  its 0/None sentinels on conflict — only `status`/`reason` change.
- The positional SQL parameter order for both INSERT statements is
  unchanged (portfolio_id, ticker, market, signal_date, rank,
  momentum_percent, current_price, price_gbp, atr_value, volatility,
  initial_stop, suggested_shares, allocation_gbp, total_cost, status,
  reason) — covered independently in test_signal_write_sanitization.py,
  re-asserted here for the consolidated code path.

No live database calls — exercised against a mocked get_db() connection.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# conftest.py registers a MagicMock stub at sys.modules["database"] (BLG-QA-20)
# that lacks the real implementations under test here. Evict it so Python
# loads the real backend/database.py, following test_signal_write_sanitization.py.
sys.modules.pop("database", None)
import database


def _mock_conn():
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {"id": "sig-1"}
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cursor


_SIGNAL_DATA = {
    "ticker": "AAPL",
    "market": "US",
    "signal_date": "2026-09-01",
    "rank": 1,
    "momentum_percent": 10.0,
    "current_price": 100.0,
    "price_gbp": 80.0,
    "atr_value": 2.0,
    "volatility": 0.1,
    "initial_stop": 90.0,
    "suggested_shares": 5,
    "allocation_gbp": 400.0,
    "total_cost": 400.0,
}


def test_create_signal_both_paths_share_the_same_upsert_helper():
    # Both wrappers must delegate to the same consolidated helper.
    import inspect
    src_create = inspect.getsource(database.create_signal)
    src_rebalance = inspect.getsource(database.create_rebalance_exit_signal)
    assert "_signal_upsert(" in src_create
    assert "_signal_upsert(" in src_rebalance


def test_create_signal_does_not_reset_status_on_conflict():
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn):
        database.create_signal("p-001", _SIGNAL_DATA)

    query = mock_cursor.execute.call_args[0][0]
    assert "status = EXCLUDED.status" not in query
    assert "rank = EXCLUDED.rank" in query
    assert "reason = EXCLUDED.reason" in query


def test_create_rebalance_exit_signal_does_not_overwrite_sizing_fields_on_conflict():
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn):
        database.create_rebalance_exit_signal(
            portfolio_id="p-001", ticker="NVDA", market="US",
            current_price=100.0, price_gbp=80.0,
            signal_date="2026-09-01", reason="not in top-5",
        )

    query = mock_cursor.execute.call_args[0][0]
    assert "status = EXCLUDED.status" in query
    assert "reason = EXCLUDED.reason" in query
    for sizing_col in ("rank", "momentum_percent", "atr_value", "volatility",
                       "initial_stop", "suggested_shares", "allocation_gbp",
                       "total_cost"):
        assert f"{sizing_col} = EXCLUDED.{sizing_col}" not in query


def test_create_signal_insert_parameter_order_unchanged():
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn):
        database.create_signal("p-001", _SIGNAL_DATA)

    args = mock_cursor.execute.call_args[0][1]
    assert args[0] == "p-001"
    assert args[1] == "AAPL"
    assert args[2] == "US"
    assert args[3] == "2026-09-01"
    assert args[14] == "new"  # status
    assert args[15] is None  # reason (not supplied)


def test_create_rebalance_exit_signal_insert_parameter_order_unchanged():
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn):
        database.create_rebalance_exit_signal(
            portfolio_id="p-001", ticker="NVDA", market="US",
            current_price=100.0, price_gbp=80.0,
            signal_date="2026-09-01", reason="not in top-5",
        )

    args = mock_cursor.execute.call_args[0][1]
    assert args[0] == "p-001"
    assert args[1] == "NVDA"
    assert args[2] == "US"
    assert args[3] == "2026-09-01"
    assert args[4] == 0  # rank sentinel
    assert args[14] == "exit_rebalance"
    assert args[15] == "not in top-5"
