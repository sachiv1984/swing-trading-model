"""
Configurable API mock harness for Alpaca Markets and Yahoo Finance (BLG-QA-08 / ST-09).

Design:
- Wraps requests.get with a URL-routing mock.
- Each API has a registry of (url_pattern, fixture_data) entries.
- Scenario fixtures loaded from tests/mock_harness/fixtures/<scenario>.json.
- Compatible with BLG-QA-09 test data library.

Fixture JSON schema:
{
  "alpaca": {
    "bars/<TICKER>": { ...AlpacaBarsResponse... },
    "news/<TICKER>": { ...AlpacaNewsResponse... }
  },
  "yahoo": {
    "<TICKER>": { ...YahooChartResponse... }
  }
}
"""
import json
import re
from pathlib import Path
from typing import Any, Dict, Optional
from unittest.mock import MagicMock, patch

FIXTURES_DIR = Path(__file__).parent / "fixtures"

ALPACA_BARS_URL = "https://data.alpaca.markets/v2/stocks/{symbol}/bars"
ALPACA_NEWS_URL = "https://data.alpaca.markets/v1beta1/news"
YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"


class MockResponse:
    """Minimal requests.Response stand-in."""

    def __init__(self, data: Any, status_code: int = 200):
        self._data = data
        self.status_code = status_code

    def json(self):
        return self._data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")


def load_scenario(scenario_name: str) -> Dict:
    """Load fixture data for a named scenario from fixtures/<scenario>.json."""
    path = FIXTURES_DIR / f"{scenario_name}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"Scenario fixture '{scenario_name}' not found at {path}. "
            "Add a fixture file in tests/mock_harness/fixtures/."
        )
    with open(path) as fh:
        return json.load(fh)


class AlpacaMockHarness:
    """
    Mock harness for Alpaca Markets API.

    Intercepts requests.get calls to Alpaca URLs and returns configured fixtures.

    Usage:
        harness = AlpacaMockHarness()
        harness.set_bars("NVDA", bars_fixture_dict)
        harness.set_news("NVDA", news_fixture_list)
        with harness.patch():
            # code under test that calls Alpaca API
            ...

    Or load a full scenario:
        harness = AlpacaMockHarness.from_scenario("nvda_passes_all_filters")
    """

    def __init__(self):
        self._bars: Dict[str, Dict] = {}
        self._news: Dict[str, list] = {}

    def set_bars(self, symbol: str, data: Dict) -> "AlpacaMockHarness":
        self._bars[symbol.upper()] = data
        return self

    def set_news(self, symbol: str, data: list) -> "AlpacaMockHarness":
        self._news[symbol.upper()] = data
        return self

    @classmethod
    def from_scenario(cls, scenario_name: str) -> "AlpacaMockHarness":
        fixture = load_scenario(scenario_name)
        harness = cls()
        for key, data in fixture.get("alpaca", {}).items():
            if key.startswith("bars/"):
                harness.set_bars(key[5:], data)
            elif key.startswith("news/"):
                harness.set_news(key[5:], data)
        return harness

    def _handle_request(self, url: str, **kwargs) -> MockResponse:
        # Alpaca bars: /v2/stocks/{symbol}/bars
        bars_match = re.search(r"/v2/stocks/([^/]+)/bars", url)
        if bars_match:
            symbol = bars_match.group(1).upper()
            if symbol in self._bars:
                return MockResponse(self._bars[symbol])
            return MockResponse({"bars": [], "symbol": symbol, "next_page_token": None})

        # Alpaca news: /v1beta1/news
        if "/v1beta1/news" in url:
            params = kwargs.get("params", {})
            symbols = params.get("symbols", "")
            if isinstance(symbols, str):
                symbol = symbols.split(",")[0].strip().upper()
            else:
                symbol = ""
            news_data = self._news.get(symbol, [])
            return MockResponse({"news": news_data, "next_page_token": None})

        return MockResponse({}, status_code=404)

    def patch(self):
        """Return a context manager that patches requests.get for Alpaca URLs."""
        return _ConditionalPatch(
            predicate=lambda url, **kw: "alpaca.markets" in url,
            handler=self._handle_request,
        )


class YahooFinanceMockHarness:
    """
    Mock harness for Yahoo Finance API.

    Intercepts requests.get calls to Yahoo Finance chart URLs.

    Usage:
        harness = YahooFinanceMockHarness()
        harness.set_chart("NVDA", chart_fixture_dict)
        with harness.patch():
            ...

    Or load from scenario:
        harness = YahooFinanceMockHarness.from_scenario("nvda_passes_all_filters")
    """

    def __init__(self):
        self._charts: Dict[str, Dict] = {}

    def set_chart(self, ticker: str, data: Dict) -> "YahooFinanceMockHarness":
        self._charts[ticker.upper()] = data
        return self

    @classmethod
    def from_scenario(cls, scenario_name: str) -> "YahooFinanceMockHarness":
        fixture = load_scenario(scenario_name)
        harness = cls()
        for ticker, data in fixture.get("yahoo", {}).items():
            harness.set_chart(ticker, data)
        return harness

    def _handle_request(self, url: str, **kwargs) -> MockResponse:
        # Yahoo Finance chart: /v8/finance/chart/{ticker}
        chart_match = re.search(r"/finance/chart/([^/?]+)", url)
        if chart_match:
            ticker = chart_match.group(1).upper()
            if ticker in self._charts:
                return MockResponse(self._charts[ticker])
            return MockResponse(
                {"chart": {"result": None, "error": {"code": "Not Found", "description": f"{ticker} not in fixture"}}},
                status_code=404,
            )
        return MockResponse({}, status_code=404)

    def patch(self):
        return _ConditionalPatch(
            predicate=lambda url, **kw: "finance.yahoo.com" in url,
            handler=self._handle_request,
        )


class ScreenerMockHarness:
    """
    Combined harness for both Alpaca and Yahoo Finance APIs.

    Routes requests to the appropriate sub-harness based on URL.
    Use this when code under test may call either API.

    Usage:
        mocks = ScreenerMockHarness.from_scenario("nvda_passes_all_filters")
        with mocks.patch():
            result = run_screener(["NVDA"])
            assert result[0]["ticker"] == "NVDA"
    """

    def __init__(self):
        self.alpaca = AlpacaMockHarness()
        self.yahoo = YahooFinanceMockHarness()

    @classmethod
    def from_scenario(cls, scenario_name: str) -> "ScreenerMockHarness":
        fixture = load_scenario(scenario_name)
        harness = cls()
        for key, data in fixture.get("alpaca", {}).items():
            if key.startswith("bars/"):
                harness.alpaca.set_bars(key[5:], data)
            elif key.startswith("news/"):
                harness.alpaca.set_news(key[5:], data)
        for ticker, data in fixture.get("yahoo", {}).items():
            harness.yahoo.set_chart(ticker, data)
        return harness

    def _handle_request(self, url: str, **kwargs) -> MockResponse:
        if "alpaca.markets" in url:
            return self.alpaca._handle_request(url, **kwargs)
        if "finance.yahoo.com" in url:
            return self.yahoo._handle_request(url, **kwargs)
        return MockResponse({}, status_code=404)

    def patch(self):
        return _ConditionalPatch(
            predicate=lambda url, **kw: (
                "alpaca.markets" in url or "finance.yahoo.com" in url
            ),
            handler=self._handle_request,
        )


class _ConditionalPatch:
    """
    Patches requests.get so that matching URLs are handled by handler,
    and non-matching URLs pass through to a MagicMock (returns 404 stub).

    This avoids accidentally intercepting unrelated HTTP calls in tests
    that only need partial mocking.
    """

    def __init__(self, predicate, handler):
        self._predicate = predicate
        self._handler = handler
        self._patcher = None

    def _side_effect(self, url, *args, **kwargs):
        if self._predicate(url, **kwargs):
            return self._handler(url, **kwargs)
        return MockResponse({}, status_code=404)

    def __enter__(self):
        mock = MagicMock(side_effect=self._side_effect)
        self._patcher = patch("requests.get", mock)
        self._patcher.start()
        return mock

    def __exit__(self, *args):
        if self._patcher:
            self._patcher.stop()
