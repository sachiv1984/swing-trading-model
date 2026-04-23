"""
Smoke tests for the external API mock harness (BLG-QA-08 / ST-09).

Verifies that the harness intercepts requests.get deterministically for both
Alpaca Markets and Yahoo Finance URLs when a mock scenario is active.
"""
import requests
from tests.mock_harness import AlpacaMockHarness, YahooFinanceMockHarness, ScreenerMockHarness


def test_alpaca_bars_mock():
    harness = AlpacaMockHarness()
    harness.set_bars("NVDA", {
        "bars": [{"t": "2026-04-22T04:00:00Z", "c": 890.0, "o": 880.0, "h": 895.0, "l": 875.0, "v": 12000000}],
        "symbol": "NVDA",
        "next_page_token": None,
    })

    with harness.patch():
        resp = requests.get("https://data.alpaca.markets/v2/stocks/NVDA/bars", params={"timeframe": "1Day", "limit": 15})
        assert resp.status_code == 200
        data = resp.json()
        assert data["symbol"] == "NVDA"
        assert len(data["bars"]) == 1
        assert data["bars"][0]["c"] == 890.0


def test_alpaca_news_mock():
    harness = AlpacaMockHarness()
    harness.set_news("NVDA", [
        {"id": 1, "headline": "Test headline", "symbols": ["NVDA"]},
    ])

    with harness.patch():
        resp = requests.get(
            "https://data.alpaca.markets/v1beta1/news",
            params={"symbols": "NVDA", "limit": 5},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["news"]) == 1
        assert data["news"][0]["headline"] == "Test headline"


def test_yahoo_finance_chart_mock():
    harness = YahooFinanceMockHarness()
    harness.set_chart("NVDA", {
        "chart": {
            "result": [{"meta": {"regularMarketPrice": 890.0, "symbol": "NVDA"}, "indicators": {"quote": [{"close": [880.0, 890.0]}]}}],
            "error": None,
        }
    })

    with harness.patch():
        resp = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/NVDA", params={"interval": "1d", "range": "1d"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["chart"]["result"][0]["meta"]["regularMarketPrice"] == 890.0


def test_screener_mocks_from_scenario():
    mocks = ScreenerMockHarness.from_scenario("baseline_us_ticker")

    with mocks.patch():
        # Alpaca bars
        resp = requests.get("https://data.alpaca.markets/v2/stocks/NVDA/bars")
        assert resp.status_code == 200
        assert resp.json()["symbol"] == "NVDA"

        # Alpaca news
        resp = requests.get("https://data.alpaca.markets/v1beta1/news", params={"symbols": "NVDA"})
        assert resp.status_code == 200
        assert len(resp.json()["news"]) > 0

        # Yahoo Finance
        resp = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/SPY", params={"interval": "1d"})
        assert resp.status_code == 200
        assert resp.json()["chart"]["result"][0]["meta"]["regularMarketPrice"] == 520.0


def test_mock_unknown_ticker_returns_empty():
    harness = AlpacaMockHarness()
    with harness.patch():
        resp = requests.get("https://data.alpaca.markets/v2/stocks/UNKNOWN/bars")
        assert resp.status_code == 200
        assert resp.json()["bars"] == []


def test_yahoo_mock_unknown_ticker_returns_404():
    harness = YahooFinanceMockHarness()
    with harness.patch():
        resp = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/UNKNOWN")
        assert resp.status_code == 404


def test_configurable_per_scenario():
    """Verify two different scenarios produce different data — no cross-contamination."""
    harness_a = AlpacaMockHarness()
    harness_a.set_bars("NVDA", {"bars": [{"c": 890.0}], "symbol": "NVDA", "next_page_token": None})

    harness_b = AlpacaMockHarness()
    harness_b.set_bars("NVDA", {"bars": [{"c": 500.0}], "symbol": "NVDA", "next_page_token": None})

    with harness_a.patch():
        data_a = requests.get("https://data.alpaca.markets/v2/stocks/NVDA/bars").json()

    with harness_b.patch():
        data_b = requests.get("https://data.alpaca.markets/v2/stocks/NVDA/bars").json()

    assert data_a["bars"][0]["c"] == 890.0
    assert data_b["bars"][0]["c"] == 500.0
