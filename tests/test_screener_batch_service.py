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
    assert cur.execute.call_count >= 4
    all_calls = [call[0][0] for call in cur.execute.call_args_list]
    assert any("CREATE TABLE IF NOT EXISTS screener_runs" in c for c in all_calls)
    assert any("CREATE TABLE IF NOT EXISTS screener_results" in c for c in all_calls)


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


def test_run_screener_persists_risk_off_not_null_on_regime_fetch_failure():
    """
    ST-11 (BLG-BE-88, EPIC-04, v8.6): a real fetch-failure scenario --
    _fetch_index_regime returns None (as it does on any unrecoverable
    error, per test_fetch_regime_returns_none_on_http_error above) -- must
    persist regime_us/regime_uk as the literal string "risk_off", not NULL.
    This is the behaviour get_regime_distribution()'s docstring now
    documents (corrected from its previous, unreachable NULL-exclusion
    claim); this test is the fetch-failure-scenario verification the
    story's AC requires.
    """
    tickers = [{"ticker": "MOCK-US", "market": "US", "active": True}]
    ohlcv = _make_ohlcv(n=30)

    conn, cur = _mock_db_write()
    with patch("services.screener_batch_service.get_db", return_value=conn), \
         patch("services.screener_batch_service.get_all_tickers", return_value=tickers), \
         patch("services.screener_batch_service.fetch_ohlcv", return_value=ohlcv), \
         patch("services.screener_batch_service._fetch_index_regime", return_value=None):
        import services.screener_batch_service as svc
        svc._run_in_progress = False
        result = svc.run_screener()

    assert result["regime_us"] == "risk_off"
    assert result["regime_uk"] == "risk_off"

    # Confirm the persisted DB row also carries "risk_off", not NULL/None --
    # the INSERT INTO screener_runs call's regime_us/regime_uk positional
    # params (5th and 6th args per _persist_run's SQL column order).
    insert_calls = [c for c in cur.execute.call_args_list if "INSERT INTO screener_runs" in c.args[0]]
    assert len(insert_calls) == 1
    persisted_params = insert_calls[0].args[1]
    regime_us_param, regime_uk_param = persisted_params[4], persisted_params[5]
    assert regime_us_param == "risk_off"
    assert regime_uk_param == "risk_off"
    assert regime_us_param is not None
    assert regime_uk_param is not None


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


# ---------------------------------------------------------------------------
# ST-02 — Sector/industry propagation
# ---------------------------------------------------------------------------

def test_sector_industry_passed_to_compute_screener_result():
    """ST-02 AC-03: sector/industry from ticker_universe row passed to compute_screener_result."""
    tickers = [{
        "ticker": "AAPL", "market": "US", "active": True,
        "sector": "Technology", "industry": "Consumer Electronics",
    }]
    ohlcv = _make_ohlcv(n=30)
    captured = {}

    def mock_compute(ticker, market, ohlcv_data, run_id, run_timestamp,
                     regime_status, regime_index, regime_index_price, regime_index_ma200,
                     sector=None, industry=None, **kwargs):
        captured["sector"] = sector
        captured["industry"] = industry
        return None  # filtered by engine — doesn't matter for this test

    conn, _ = _mock_db_write()
    with patch("services.screener_batch_service.get_db", return_value=conn), \
         patch("services.screener_batch_service.get_all_tickers", return_value=tickers), \
         patch("services.screener_batch_service.fetch_ohlcv", return_value=ohlcv), \
         patch("services.screener_batch_service._fetch_index_regime", return_value=_risk_on()), \
         patch("services.screener_batch_service.compute_screener_result", side_effect=mock_compute):
        import services.screener_batch_service as svc
        svc._run_in_progress = False
        svc.run_screener()

    assert captured.get("sector") == "Technology"
    assert captured.get("industry") == "Consumer Electronics"


# ---------------------------------------------------------------------------
# ST-04 — Degraded run detection
# ---------------------------------------------------------------------------

def test_degraded_run_set_when_failure_rate_exceeds_20_pct():
    """ST-04 AC-01: degraded_run True when >20% tickers have no OHLCV."""
    tickers = [{"ticker": f"T{i}", "market": "US", "active": True} for i in range(10)]
    ohlcv = _make_ohlcv(n=30)

    call_count = {"n": 0}

    def mock_fetch(ticker, market, days):
        call_count["n"] += 1
        # First 3 fail, rest succeed → 3/10 = 30% failure rate → degraded
        return None if call_count["n"] <= 3 else ohlcv

    conn, _ = _mock_db_write()
    with patch("services.screener_batch_service.get_db", return_value=conn), \
         patch("services.screener_batch_service.get_all_tickers", return_value=tickers), \
         patch("services.screener_batch_service.fetch_ohlcv", side_effect=mock_fetch), \
         patch("services.screener_batch_service._fetch_index_regime", return_value=_risk_on()):
        import services.screener_batch_service as svc
        svc._run_in_progress = False
        result = svc.run_screener()

    assert result["degraded_run"] is True
    assert result["failure_rate"] > 0.20


def test_degraded_run_false_when_failure_rate_below_20_pct():
    """ST-04 AC-04: degraded_run False when failure_rate ≤ 20%."""
    tickers = [{"ticker": f"T{i}", "market": "US", "active": True} for i in range(10)]
    ohlcv = _make_ohlcv(n=30)

    call_count = {"n": 0}

    def mock_fetch(ticker, market, days):
        call_count["n"] += 1
        # Only 1 failure out of 10 = 10% → not degraded
        return None if call_count["n"] == 1 else ohlcv

    conn, _ = _mock_db_write()
    with patch("services.screener_batch_service.get_db", return_value=conn), \
         patch("services.screener_batch_service.get_all_tickers", return_value=tickers), \
         patch("services.screener_batch_service.fetch_ohlcv", side_effect=mock_fetch), \
         patch("services.screener_batch_service._fetch_index_regime", return_value=_risk_on()):
        import services.screener_batch_service as svc
        svc._run_in_progress = False
        result = svc.run_screener()

    assert result["degraded_run"] is False
    assert result["failure_rate"] <= 0.20


# ---------------------------------------------------------------------------
# get_regime_distribution (ST-21, BLG-FEAT-29, EPIC-06, v8.5)
# ---------------------------------------------------------------------------

def _mock_regime_dist_row(us_risk_on=0, us_risk_off=0, uk_risk_on=0, uk_risk_off=0, run_count=0):
    data = {
        "us_risk_on": us_risk_on,
        "us_risk_off": us_risk_off,
        "uk_risk_on": uk_risk_on,
        "uk_risk_off": uk_risk_off,
        "run_count": run_count,
    }
    row = MagicMock()
    row.__getitem__ = lambda s, k: data[k]
    cur = MagicMock()
    cur.fetchone.return_value = row
    cur_ctx = MagicMock()
    cur_ctx.__enter__ = MagicMock(return_value=cur)
    cur_ctx.__exit__ = MagicMock(return_value=False)
    conn = MagicMock()
    conn.__enter__ = lambda s: conn
    conn.__exit__ = MagicMock(return_value=False)
    conn.cursor.return_value = cur_ctx
    return conn, cur


def test_regime_distribution_rejects_invalid_window():
    from services.screener_batch_service import get_regime_distribution
    with pytest.raises(ValueError):
        get_regime_distribution(window="7d")


def test_regime_distribution_defaults_to_30d():
    conn, cur = _mock_regime_dist_row(us_risk_on=10, us_risk_off=2, uk_risk_on=5, uk_risk_off=3, run_count=15)
    with patch("services.screener_batch_service.get_db", return_value=conn):
        from services.screener_batch_service import get_regime_distribution
        result = get_regime_distribution()
    assert result["window"] == "30d"
    # A WHERE clause with the 30-day interval must be present for the default window.
    executed_sql = cur.execute.call_args[0][0]
    assert "run_timestamp >=" in executed_sql


def test_regime_distribution_all_window_has_no_time_filter():
    conn, cur = _mock_regime_dist_row(us_risk_on=1, us_risk_off=1, run_count=2)
    with patch("services.screener_batch_service.get_db", return_value=conn):
        from services.screener_batch_service import get_regime_distribution
        result = get_regime_distribution(window="all")
    assert result["window"] == "all"
    executed_sql = cur.execute.call_args[0][0]
    assert "run_timestamp >=" not in executed_sql


def test_regime_distribution_sums_both_markets():
    """Each run contributes one observation per market — US and UK counts sum together."""
    conn, _ = _mock_regime_dist_row(us_risk_on=10, us_risk_off=2, uk_risk_on=5, uk_risk_off=3, run_count=12)
    with patch("services.screener_batch_service.get_db", return_value=conn):
        from services.screener_batch_service import get_regime_distribution
        result = get_regime_distribution(window="60d")
    assert result["risk_on_count"] == 15  # 10 + 5
    assert result["risk_off_count"] == 5  # 2 + 3
    assert result["total_observations"] == 20
    assert result["risk_on_pct"] == 75.0
    assert result["risk_off_pct"] == 25.0
    assert result["run_count"] == 12


def test_regime_distribution_zero_observations_returns_null_percentages():
    """No runs in window (or all had unresolved regimes) — percentages must be null,
    not a misleading 0%/0% split (per the design decision record's DataState empty-branch rule)."""
    conn, _ = _mock_regime_dist_row(us_risk_on=0, us_risk_off=0, uk_risk_on=0, uk_risk_off=0, run_count=0)
    with patch("services.screener_batch_service.get_db", return_value=conn):
        from services.screener_batch_service import get_regime_distribution
        result = get_regime_distribution(window="30d")
    assert result["total_observations"] == 0
    assert result["risk_on_pct"] is None
    assert result["risk_off_pct"] is None


def test_regime_distribution_endpoint_returns_200():
    from fastapi.testclient import TestClient
    from fastapi import FastAPI
    from routers.screener import router

    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    conn, _ = _mock_regime_dist_row(us_risk_on=3, us_risk_off=1, run_count=4)
    with patch("services.screener_batch_service.get_db", return_value=conn):
        resp = client.get("/screener/regime-distribution?window=60d")

    assert resp.status_code == 200
    body = resp.json()
    assert body["ok"] is True
    assert body["data"]["window"] == "60d"
    assert body["data"]["risk_on_count"] == 3


def test_regime_distribution_endpoint_rejects_invalid_window():
    from fastapi.testclient import TestClient
    from fastapi import FastAPI
    from routers.screener import router

    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    resp = client.get("/screener/regime-distribution?window=7d")
    assert resp.status_code == 400
