"""
External API mock harness for screener CI tests (BLG-QA-08 / ST-09).

Provides configurable per-scenario mocks for Alpaca Markets API and Yahoo Finance API.
Compatible with the BLG-QA-09 test data library (ST-10).

Usage:
    from tests.mock_harness import AlpacaMockHarness, YahooFinanceMockHarness

Fixtures (defined in conftest.py):
    alpaca_mock    — patches requests.get for Alpaca API calls
    yahoo_mock     — patches requests.get for Yahoo Finance calls
    screener_mocks — combined patch for both APIs

Fixture data lives in tests/mock_harness/fixtures/*.json.
"""
from tests.mock_harness.api_mock_harness import (
    AlpacaMockHarness,
    YahooFinanceMockHarness,
    ScreenerMockHarness,
    MockResponse,
    load_scenario,
)

__all__ = [
    "AlpacaMockHarness",
    "YahooFinanceMockHarness",
    "ScreenerMockHarness",
    "MockResponse",
    "load_scenario",
]
