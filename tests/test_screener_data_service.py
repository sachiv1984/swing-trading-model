"""
Unit tests for screener_data_service (DS-01 / ST-02)
Uses BLG-QA-08 mock harness for external API isolation.
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from tests.mock_harness.api_mock_harness import ScreenerMockHarness, AlpacaMockHarness, YahooFinanceMockHarness


# ---------------------------------------------------------------------------
# Reset Yahoo Finance module state before every test so cooldown and
# consecutive-401 counters from one test cannot affect subsequent tests.
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def reset_yahoo_state():
    import services.screener_data_service as svc
    svc._yahoo_crumb = None
    svc._yahoo_session = None
    svc._yahoo_cooldown_until = 0.0
    svc._crumb_consecutive_401s = 0
    if hasattr(svc._yahoo_fetch_ohlcv, "_consecutive_401"):
        del svc._yahoo_fetch_ohlcv._consecutive_401
    yield
    svc._yahoo_crumb = None
    svc._yahoo_session = None
    svc._yahoo_cooldown_until = 0.0
    svc._crumb_consecutive_401s = 0
    if hasattr(svc._yahoo_fetch_ohlcv, "_consecutive_401"):
        del svc._yahoo_fetch_ohlcv._consecutive_401


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_yahoo_chart(ticker, closes, currency="USD", timestamps=None):
    if timestamps is None:
        # generate sequential unix timestamps (one per close, starting 2026-04-01)
        base = 1743465600  # 2026-04-01 UTC
        timestamps = [base + i * 86400 for i in range(len(closes))]
    n = len(closes)
    opens = [c - 1 for c in closes]
    highs = [c + 2 for c in closes]
    lows = [c - 2 for c in closes]
    volumes = [1000000] * n
    return {
        "chart": {
            "result": [
                {
                    "meta": {"regularMarketPrice": closes[-1], "symbol": ticker, "currency": currency},
                    "timestamp": timestamps,
                    "indicators": {
                        "quote": [{"open": opens, "high": highs, "low": lows, "close": closes, "volume": volumes}]
                    },
                }
            ],
            "error": None,
        }
    }


def _make_alpaca_bars(ticker, closes):
    bars = []
    base_ts = "2026-04-01T04:00:00Z"
    for i, c in enumerate(closes):
        date = f"2026-04-{i+1:02d}T04:00:00Z"
        bars.append({"t": date, "o": c - 1, "h": c + 2, "l": c - 2, "c": c, "v": 1000000})
    return {"bars": bars, "symbol": ticker, "next_page_token": None}


# ---------------------------------------------------------------------------
# US ticker — Alpaca primary path
# ---------------------------------------------------------------------------

def test_us_ticker_returns_ohlcv_from_alpaca():
    bars = _make_alpaca_bars("AAPL", [150, 152, 154, 155, 156])["bars"]
    with patch("services.screener_data_service.get_ohlcv_bars", return_value=bars):
        from services.screener_data_service import fetch_ohlcv
        result = fetch_ohlcv("AAPL", "US", days=5)
    assert result is not None
    assert len(result) == 5
    assert result[0]["close"] == pytest.approx(150.0)
    assert "date" in result[0]
    assert "volume" in result[0]


def test_us_ticker_records_sorted_ascending():
    bars = list(reversed(_make_alpaca_bars("MSFT", [300, 302, 305])["bars"]))
    with patch("services.screener_data_service.get_ohlcv_bars", return_value=bars):
        from services.screener_data_service import fetch_ohlcv
        result = fetch_ohlcv("MSFT", "US", days=3)
    assert result is not None
    dates = [r["date"] for r in result]
    assert dates == sorted(dates)


def test_us_ticker_falls_back_to_yahoo_when_alpaca_returns_none():
    yahoo = YahooFinanceMockHarness()
    yahoo.set_chart("NVDA", _make_yahoo_chart("NVDA", [500, 505, 510]))
    with patch("services.screener_data_service.get_ohlcv_bars", return_value=None):
        with yahoo.patch():
            from services.screener_data_service import fetch_ohlcv
            result = fetch_ohlcv("NVDA", "US", days=3)
    assert result is not None
    assert len(result) == 3


def test_us_ticker_falls_back_to_yahoo_when_alpaca_returns_empty():
    yahoo = YahooFinanceMockHarness()
    yahoo.set_chart("AMZN", _make_yahoo_chart("AMZN", [180, 182]))
    with patch("services.screener_data_service.get_ohlcv_bars", return_value=[]):
        with yahoo.patch():
            from services.screener_data_service import fetch_ohlcv
            result = fetch_ohlcv("AMZN", "US", days=2)
    assert result is not None


# ---------------------------------------------------------------------------
# UK ticker — Yahoo Finance only
# ---------------------------------------------------------------------------

def test_uk_ticker_uses_yahoo_never_alpaca():
    yahoo = YahooFinanceMockHarness()
    yahoo.set_chart("HSBA.L", _make_yahoo_chart("HSBA.L", [620, 625, 630]))
    alpaca_called = []
    with patch("services.screener_data_service.get_ohlcv_bars", side_effect=lambda *a, **kw: alpaca_called.append(True) or None):
        with yahoo.patch():
            from services.screener_data_service import fetch_ohlcv
            result = fetch_ohlcv("HSBA.L", "UK", days=3)
    assert not alpaca_called, "Alpaca must not be called for UK tickers"
    assert result is not None


def test_uk_ticker_pence_divided_by_100():
    yahoo = YahooFinanceMockHarness()
    yahoo.set_chart("AZN.L", _make_yahoo_chart("AZN.L", [12800, 12900, 13000], currency="GBp"))
    with yahoo.patch():
        from services.screener_data_service import fetch_ohlcv
        result = fetch_ohlcv("AZN.L", "UK", days=3)
    assert result is not None
    assert result[-1]["close"] == pytest.approx(130.0)  # 13000 / 100


def test_uk_ticker_gbp_not_divided():
    yahoo = YahooFinanceMockHarness()
    yahoo.set_chart("BP.L", _make_yahoo_chart("BP.L", [4.5, 4.6, 4.7], currency="GBP"))
    with yahoo.patch():
        from services.screener_data_service import fetch_ohlcv
        result = fetch_ohlcv("BP.L", "UK", days=3)
    assert result is not None
    assert result[-1]["close"] == pytest.approx(4.7)


# ---------------------------------------------------------------------------
# Error / edge cases
# ---------------------------------------------------------------------------

def test_returns_none_when_all_sources_fail():
    with patch("services.screener_data_service.get_ohlcv_bars", return_value=None):
        with patch("services.screener_data_service._yahoo_fetch_ohlcv", return_value=None):
            from services.screener_data_service import fetch_ohlcv
            result = fetch_ohlcv("UNKNOWN", "US", days=10)
    assert result is None


def test_ticker_normalised_to_uppercase():
    alpaca = AlpacaMockHarness()
    alpaca.set_bars("AAPL", _make_alpaca_bars("AAPL", [150]))
    with alpaca.patch() as mock_get:
        from services.screener_data_service import fetch_ohlcv
        fetch_ohlcv("aapl", "US", days=1)
    # Verify the URL built by alpaca_service used the uppercase ticker
    if mock_get.called:
        url_called = mock_get.call_args[0][0]
        assert "AAPL" in url_called or "aapl" not in url_called


# ---------------------------------------------------------------------------
# ST-01 — Crumb refresh and retry on 401
# ---------------------------------------------------------------------------

def _make_resp(status_code, json_body=None):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_body or {}
    resp.text = ""
    return resp


def _make_yahoo_resp(closes):
    chart = _make_yahoo_chart("AAPL", closes)
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = chart
    return resp


def test_yahoo_401_triggers_crumb_refresh_and_retries():
    """ST-01 AC-01: 401 response triggers crumb refresh and one retry."""
    import services.screener_data_service as svc

    crumb_resp = MagicMock()
    crumb_resp.status_code = 200
    crumb_resp.text = "new-crumb-token"

    call_count = {"n": 0}

    def mock_session_get(url, **kwargs):
        if "getcrumb" in url or "finance.yahoo.com" == url.split("/")[2]:
            return crumb_resp
        call_count["n"] += 1
        if call_count["n"] == 1:
            return _make_resp(401)
        return _make_yahoo_resp([150, 155, 160])

    mock_sess = MagicMock()
    mock_sess.get.side_effect = mock_session_get

    with patch("services.screener_data_service.requests") as mock_requests, \
         patch("services.screener_data_service._time.sleep"), \
         patch("services.screener_data_service.random.uniform", return_value=0.0):
        mock_requests.Session.return_value = mock_sess
        mock_requests.RequestException = Exception

        svc._yahoo_crumb = None
        svc._yahoo_session = None
        if hasattr(svc._yahoo_fetch_ohlcv, "_consecutive_401"):
            del svc._yahoo_fetch_ohlcv._consecutive_401

        result = svc._yahoo_fetch_ohlcv("AAPL", 30)

    assert result is not None
    assert len(result) == 3


def test_yahoo_crumb_refresh_updates_module_state():
    """ST-01 AC-05: crumb refresh updates _yahoo_crumb and _yahoo_session."""
    import services.screener_data_service as svc

    crumb_resp = MagicMock()
    crumb_resp.status_code = 200
    crumb_resp.text = "test-crumb-xyz"

    consent_resp = MagicMock()
    consent_resp.status_code = 200

    mock_sess = MagicMock()
    mock_sess.get.side_effect = [consent_resp, crumb_resp]

    with patch("services.screener_data_service.requests") as mock_requests:
        mock_requests.Session.return_value = mock_sess
        mock_requests.RequestException = Exception

        svc._yahoo_crumb = None
        svc._yahoo_session = None
        result = svc._refresh_yahoo_crumb()

    assert result == "test-crumb-xyz"
    assert svc._yahoo_crumb == "test-crumb-xyz"
    assert svc._yahoo_session is mock_sess
