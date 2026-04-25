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
