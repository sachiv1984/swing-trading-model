"""
Momentum signal run completion marker (DS-39).

ST-30 / ST-32 (EPIC-05, v9.15, BLG-OPS-190 / BLG-OPS-192). generate_momentum_signals
writes one marker per completed run, after its signals are saved, with the
tickers it ranked. A run in which no ticker qualifies still writes a marker
(an empty ranking); a run that fails before finishing writes none. The
month-end rebalance job reads the marker (tests/test_nightly_computations.py
RX-06, RX-08, RX-11, RX-12).

No live database: the module-level `database` names in services.signal_service
are patched per test, and the real DS-39 functions run against a mocked get_db().
"""

import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from tests._real_database import load_real_database  # noqa: E402

database = load_real_database("database_real_for_test_momentum_signal_run_marker")
import services.signal_service as signal_service  # noqa: E402

RUN_DAY = datetime(2026, 6, 30, 16, 0)


def _frame(start, step, n=600):
    """Daily closes rising (step > 0) or falling (step < 0) in a straight line."""
    idx = pd.bdate_range(end="2026-06-30", periods=n)
    close = pd.Series(start + step * np.arange(n), index=idx, dtype=float)
    return pd.DataFrame({"close": close, "high": close * 1.01, "low": close * 0.99, "volume": 1_000_000})


def _run(prices_by_ticker, index_frame):
    """Run generate_momentum_signals with every external read patched. Returns
    (result, record mock, create_signal mock)."""
    def download(ticker, start, end):
        if ticker in ("SPY", "^FTSE"):
            return index_frame
        return prices_by_ticker.get(ticker)

    record = MagicMock()
    create = MagicMock()
    with patch.object(signal_service, "get_portfolio", return_value={"id": "portfolio-001", "cash": 10000}), \
         patch.object(signal_service, "get_positions", return_value=[]), \
         patch.object(signal_service, "get_settings", return_value=[]), \
         patch.object(signal_service, "get_all_tickers",
                      return_value=[{"ticker": t} for t in prices_by_ticker]), \
         patch.object(signal_service, "download_ticker_data", side_effect=download), \
         patch.object(signal_service, "get_live_fx_rate", return_value=1.27), \
         patch.object(signal_service, "compute_atr_simple",
                      side_effect=lambda close, period: close.diff().abs().rolling(period).mean()), \
         patch.object(signal_service, "create_signal", create), \
         patch.object(signal_service, "record_momentum_signal_run", record), \
         patch("services.signal_service.datetime") as mock_dt:
        mock_dt.now.return_value = RUN_DAY
        result = signal_service.generate_momentum_signals()
    return result, record, create


def test_zero_qualifier_run_records_an_empty_marker():
    """Every ticker is below its 200-day MA, so none qualifies: the run still
    completes and records a marker with no tickers (BLG-OPS-192)."""
    falling = {"AAA": _frame(500, -0.5), "BBB": _frame(400, -0.4)}
    result, record, create = _run(falling, index_frame=_frame(100, 0.1))
    assert result["signals_generated"] == 0
    create.assert_not_called()
    record.assert_called_once_with("portfolio-001", "2026-06-30", [])


def test_qualifying_run_records_the_ranked_tickers_after_saving_them():
    """Rising tickers in a risk-on market qualify: the marker lists exactly the
    tickers whose signals were saved."""
    rising = {"AAA": _frame(100, 0.5), "BBB": _frame(100, 0.3)}
    result, record, create = _run(rising, index_frame=_frame(100, 0.1))
    saved = sorted(c.args[1]["ticker"] for c in create.call_args_list)
    assert saved == ["AAA", "BBB"]
    assert result["signals_generated"] == 2
    record.assert_called_once()
    portfolio_id, run_date, tickers = record.call_args.args
    assert (portfolio_id, run_date, sorted(tickers)) == ("portfolio-001", "2026-06-30", ["AAA", "BBB"])


def test_failed_run_records_no_marker():
    """No price data at all: the run raises before finishing and leaves no
    marker, so the month-end job reports the run as missing (BLG-OPS-190)."""
    with pytest.raises(ValueError):
        _run({"AAA": None}, index_frame=_frame(100, 0.1))
    # _run raises before returning its mocks; check via a fresh patch instead.
    record = MagicMock()
    with patch.object(signal_service, "get_portfolio", return_value={"id": "portfolio-001", "cash": 10000}), \
         patch.object(signal_service, "get_positions", return_value=[]), \
         patch.object(signal_service, "get_settings", return_value=[]), \
         patch.object(signal_service, "get_all_tickers", return_value=[{"ticker": "AAA"}]), \
         patch.object(signal_service, "download_ticker_data", return_value=None), \
         patch.object(signal_service, "record_momentum_signal_run", record), \
         pytest.raises(ValueError):
        signal_service.generate_momentum_signals()
    record.assert_not_called()


def test_marker_write_failure_is_logged_not_raised(capsys):
    """If the marker cannot be written, the run (whose signals are already saved)
    still returns; the month-end job will then report the run as missing."""
    with patch.object(signal_service, "record_momentum_signal_run", side_effect=RuntimeError("db down")):
        signal_service._record_run_completed("portfolio-001", "2026-06-30", ["AAA"])
    assert "Could not record momentum run completion for 2026-06-30" in capsys.readouterr().out


def _mock_conn(fetchone=None):
    cur = MagicMock()
    cur.fetchone.return_value = fetchone
    cur.__enter__ = MagicMock(return_value=cur)
    cur.__exit__ = MagicMock(return_value=False)
    conn = MagicMock()
    conn.cursor.return_value = cur
    conn.__enter__ = MagicMock(return_value=conn)
    conn.__exit__ = MagicMock(return_value=False)
    return conn, cur


def test_record_writes_tickers_as_json_with_their_count():
    conn, cur = _mock_conn()
    with patch.object(database, "get_db", return_value=conn), \
         patch.object(database, "ensure_momentum_signal_runs_table"):
        database.record_momentum_signal_run("p-1", "2026-06-30", ["AAA", "BBB"])
    sql, params = cur.execute.call_args.args
    assert "INSERT INTO momentum_signal_runs" in sql
    assert params == ("p-1", "2026-06-30", '["AAA", "BBB"]', 2)


def test_get_returns_none_when_no_run_completed_that_day():
    conn, cur = _mock_conn(fetchone=None)
    with patch.object(database, "get_db", return_value=conn), \
         patch.object(database, "ensure_momentum_signal_runs_table"):
        assert database.get_momentum_signal_run("p-1", "2026-06-30") is None
    sql, params = cur.execute.call_args.args
    assert "ORDER BY completed_at DESC" in sql and params == ("p-1", "2026-06-30")


def test_get_returns_the_latest_marker_with_an_empty_ranking_intact():
    row = {"run_date": "2026-06-30", "completed_at": "2026-06-30T16:05:00Z",
           "tickers_ranked": [], "ranked_count": 0}
    conn, _ = _mock_conn(fetchone=row)
    with patch.object(database, "get_db", return_value=conn), \
         patch.object(database, "ensure_momentum_signal_runs_table"):
        run = database.get_momentum_signal_run("p-1", "2026-06-30")
    assert run == {"run_date": "2026-06-30", "completed_at": "2026-06-30T16:05:00Z",
                   "tickers_ranked": [], "ranked_count": 0}
