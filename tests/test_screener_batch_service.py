"""
Integration tests for screener_batch_service (DS-01 / ST-04)
Uses BLG-QA-08 mock harness to isolate external API calls.
"""
import pytest
import json
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_ohlcv(n=20, base=200.0, atr_mult=5.0):
    records = []
    for i in range(n):
        c = base + i
        records.append({
            "date": f"2026-04-{(i % 28) + 1:02d}",
            "open": c - 0.5, "high": c + atr_mult,
            "low": c - atr_mult, "close": c, "volume": 1_000_000 + i * 10_000,
        })
    return records


def _risk_on():
    return {
        "regime_status": "risk_on",
        "regime_index": "SPY",
        "regime_index_price": 520.0,
        "regime_index_ma200": 490.0,
    }


def _mock_db_write():
    """Return a no-op DB context manager mock."""
    cur = MagicMock()
    cur.rowcount = 1
    cur_ctx = MagicMock()
    cur_ctx.__enter__ = MagicMock(return_value=cur)
    cur_ctx.__exit__ = MagicMock(return_value=False)
    conn = MagicMock()
    conn.__enter__ = lambda s: conn
    conn.__exit__ = MagicMock(return_value=False)
    conn.cursor.return_value = cur_ctx
    return conn, cur


def _mock_db_query(rows):
    """Return a DB context manager that yields given rows on fetchone/fetchall."""
    cur = MagicMock()
    # Set up to return rows for multiple queries
    run_row = MagicMock()
    run_row.__getitem__ = lambda s, k: {"run_id": "test-run-id", "run_timestamp": None, "cnt": len(rows)}[k]
    run_row.keys = lambda: ["run_id", "run_timestamp", "cnt"]
    cur.fetchone.side_effect = [run_row, MagicMock(__getitem__=lambda s, k: len(rows), keys=lambda: ["cnt"])]
    cur.fetchall.return_value = rows
    cur.__enter__ = lambda s: cur
    cur.__exit__ = MagicMock(return_value=False)
    conn = MagicMock()
    conn.__enter__ = lambda s: conn
    conn.__exit__ = MagicMock(return_value=False)
    conn.cursor.return_value = cur
    return conn


# ---------------------------------------------------------------------------
# ensure_screener_results_table
# ---------------------------------------------------------------------------

def test_ensure_table_runs_create_statements():
    conn, cur = _mock_db_write()
    with patch("services.screener_batch_service.get_db", return_value=conn):
        from services.screener_batch_service import ensure_screener_results_table
        ensure_screener_results_table()
    assert cur.execute.call_count >= 3
    first_call = cur.execute.call_args_list[0][0][0]
    assert "CREATE TABLE IF NOT EXISTS screener_results" in first_call


# ---------------------------------------------------------------------------
# run_screener — happy path
# ---------------------------------------------------------------------------

def test_run_screener_returns_run_id_and_count():
    tickers = [{"ticker": "MOCK-US", "market": "US", "active": True}]
    ohlcv = _make_ohlcv(n=30)

    conn, _ = _mock_db_write()
    with patch("services.screener_batch_service.get_db", return_value=conn), \
         patch("services.screener_batch_service.get_all_tickers", return_value=tickers), \
         patch("services.screener_batch_service.fetch_ohlcv", return_value=ohlcv), \
         patch("services.screener_batch_service._fetch_index_regime", return_value=_risk_on()):
        import services.screener_batch_service as svc
        svc._run_in_progress = False
        result = svc.run_screener()
    assert "run_id" in result
    assert result["status"] == "completed"
    assert result["tickers_evaluated"] == 1


def test_run_screener_skips_ticker_when_ohlcv_unavailable():
    tickers = [{"ticker": "STALE", "market": "US", "active": True}]
    conn, _ = _mock_db_write()
    with patch("services.screener_batch_service.get_db", return_value=conn), \
         patch("services.screener_batch_service.get_all_tickers", return_value=tickers), \
         patch("services.screener_batch_service.fetch_ohlcv", return_value=None), \
         patch("services.screener_batch_service._fetch_index_regime", return_value=_risk_on()):
        import services.screener_batch_service as svc
        svc._run_in_progress = False
        result = svc.run_screener()
    assert result["tickers_evaluated"] == 0
    assert result["count"] == 0


def test_run_screener_rejects_concurrent_run():
    import services.screener_batch_service as svc
    svc._run_in_progress = True
    try:
        with pytest.raises(RuntimeError, match="RUN_IN_PROGRESS"):
            svc.run_screener()
    finally:
        svc._run_in_progress = False


def test_run_screener_routes_uk_ticker_to_uk_regime():
    tickers = [{"ticker": "HSBA.L", "market": "UK", "active": True}]
    ohlcv = _make_ohlcv(n=30)
    regime_calls = []

    def mock_regime(index):
        regime_calls.append(index)
        return {"regime_status": "risk_on", "regime_index": index,
                "regime_index_price": 8400.0, "regime_index_ma200": 8000.0}

    conn, _ = _mock_db_write()
    with patch("services.screener_batch_service.get_db", return_value=conn), \
         patch("services.screener_batch_service.get_all_tickers", return_value=tickers), \
         patch("services.screener_batch_service.fetch_ohlcv", return_value=ohlcv), \
         patch("services.screener_batch_service._fetch_index_regime", side_effect=mock_regime):
        import services.screener_batch_service as svc
        svc._run_in_progress = False
        svc.run_screener()
    assert "^FTSE" in regime_calls


def test_run_screener_accepts_custom_ticker_universe():
    ohlcv = _make_ohlcv(n=30)
    conn, _ = _mock_db_write()
    with patch("services.screener_batch_service.get_db", return_value=conn), \
         patch("services.screener_batch_service.get_all_tickers") as mock_get, \
         patch("services.screener_batch_service.fetch_ohlcv", return_value=ohlcv), \
         patch("services.screener_batch_service._fetch_index_regime", return_value=_risk_on()):
        import services.screener_batch_service as svc
        svc._run_in_progress = False
        result = svc.run_screener(ticker_universe=["AAPL", "MSFT"])
    mock_get.assert_not_called()
    assert result["tickers_evaluated"] == 2


# ---------------------------------------------------------------------------
# _fetch_index_regime
# ---------------------------------------------------------------------------

def test_fetch_regime_returns_risk_on_when_price_above_ma():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "chart": {
            "result": [
                {
                    "meta": {"regularMarketPrice": 520.0, "symbol": "SPY"},
                    "indicators": {"quote": [{"close": [450.0] * 250}]},
                }
            ]
        }
    }
    with patch("services.screener_batch_service.requests.get", return_value=mock_resp):
        from services.screener_batch_service import _fetch_index_regime
        result = _fetch_index_regime("SPY")
    assert result is not None
    assert result["regime_status"] == "risk_on"


def test_fetch_regime_returns_risk_off_when_price_below_ma():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "chart": {
            "result": [
                {
                    "meta": {"regularMarketPrice": 400.0, "symbol": "SPY"},
                    "indicators": {"quote": [{"close": [500.0] * 250}]},
                }
            ]
        }
    }
    with patch("services.screener_batch_service.requests.get", return_value=mock_resp):
        from services.screener_batch_service import _fetch_index_regime
        result = _fetch_index_regime("SPY")
    assert result["regime_status"] == "risk_off"


def test_fetch_regime_returns_none_on_http_error():
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    with patch("services.screener_batch_service.requests.get", return_value=mock_resp):
        from services.screener_batch_service import _fetch_index_regime
        result = _fetch_index_regime("SPY")
    assert result is None
