"""
Pytest fixtures for the API mock harness (BLG-QA-08 / ST-09).

Import in tests/conftest.py or individual test files as needed.

Fixtures:
    alpaca_mock_harness  — AlpacaMockHarness, ready for per-test configuration
    yahoo_mock_harness   — YahooFinanceMockHarness, ready for per-test configuration
    screener_mocks       — ScreenerMockHarness loaded with baseline_us_ticker scenario
    scenario_mocks       — factory: call with scenario name to load a named fixture
"""
import pytest
from tests.mock_harness import (
    AlpacaMockHarness,
    YahooFinanceMockHarness,
    ScreenerMockHarness,
)


@pytest.fixture
def alpaca_mock_harness():
    """Empty AlpacaMockHarness — configure per test with set_bars / set_news."""
    return AlpacaMockHarness()


@pytest.fixture
def yahoo_mock_harness():
    """Empty YahooFinanceMockHarness — configure per test with set_chart."""
    return YahooFinanceMockHarness()


@pytest.fixture
def screener_mocks():
    """ScreenerMockHarness pre-loaded with baseline_us_ticker scenario."""
    return ScreenerMockHarness.from_scenario("baseline_us_ticker")


@pytest.fixture
def scenario_mocks():
    """
    Factory fixture — load any named scenario.

    Usage in test:
        def test_foo(scenario_mocks):
            mocks = scenario_mocks("nvda_passes_all_filters")
            with mocks.patch():
                ...
    """
    def _factory(scenario_name: str) -> ScreenerMockHarness:
        return ScreenerMockHarness.from_scenario(scenario_name)
    return _factory
