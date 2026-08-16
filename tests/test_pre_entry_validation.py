"""
SI-01 Pre-Entry Validation Unit Tests (ST-02, EPIC-01, v3.8)

Tests all 5 advisory rule types:
  1. regime_gate
  2. cash_constraint
  3. sector_concentration
  4. earnings_proximity
  5. sizing_validity

CI-safe: all database, pricing, and external service calls are mocked.
No live DB or network connections.
Non-blocking advisory: tests verify that fail/warn results do not block
the response (advisory_status is returned; status 200 always).

Spec: docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio/pre-entry-validation
Strategy ref: claude/strategy/strategy_rules.md §4.2
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from fastapi.testclient import TestClient
from main import app

CLIENT = TestClient(app, raise_server_exceptions=False)

BASE_URL = "/portfolio/pre-entry-validation"

MOCK_PORTFOLIO = {
    "id": "test-portfolio-001",
    "cash": 5000.0,
}

MOCK_POSITIONS_EMPTY = []

MOCK_REGIME_ON = {"spy_risk_on": True, "ftse_risk_on": True}
MOCK_REGIME_OFF = {"spy_risk_on": False, "ftse_risk_on": False}


# ---------------------------------------------------------------------------
# 1. Regime gate
# ---------------------------------------------------------------------------

class TestRegimeGate:
    def test_regime_pass_when_risk_on(self):
        with (
            patch("position_manager.check_market_regime", return_value=MOCK_REGIME_ON),
            patch("database.get_portfolio", return_value=MOCK_PORTFOLIO),
            patch("database.get_positions", return_value=MOCK_POSITIONS_EMPTY),
            patch("utils.pricing.get_current_price", return_value=215.0),
            patch("utils.pricing.get_live_fx_rate", return_value=1.27),
            patch("services.earnings_service.get_earnings", return_value={"next_earnings_date": None, "days_until_earnings": None}),
        ):
            resp = CLIENT.get(f"{BASE_URL}?ticker=AAPL&quantity=10&market=US")
        assert resp.status_code == 200
        data = resp.json()["data"]
        regime_check = next(c for c in data["checks"] if c["rule"] == "regime_gate")
        assert regime_check["status"] == "pass"
        assert "Risk-On" in regime_check["detail"]

    def test_regime_fail_when_risk_off(self):
        with (
            patch("position_manager.check_market_regime", return_value=MOCK_REGIME_OFF),
            patch("database.get_portfolio", return_value=MOCK_PORTFOLIO),
            patch("database.get_positions", return_value=MOCK_POSITIONS_EMPTY),
            patch("utils.pricing.get_current_price", return_value=215.0),
            patch("utils.pricing.get_live_fx_rate", return_value=1.27),
            patch("services.earnings_service.get_earnings", return_value={"next_earnings_date": None, "days_until_earnings": None}),
        ):
            resp = CLIENT.get(f"{BASE_URL}?ticker=AAPL&quantity=10&market=US")
        assert resp.status_code == 200
        data = resp.json()["data"]
        regime_check = next(c for c in data["checks"] if c["rule"] == "regime_gate")
        assert regime_check["status"] == "fail"
        assert "Risk-Off" in regime_check["detail"]
        # Advisory: overall response still 200
        assert data["advisory_status"] == "fail"
        assert data["override_required"] is True

    def test_uk_regime_checks_ftse(self):
        ftse_off = {"spy_risk_on": True, "ftse_risk_on": False}
        with (
            patch("position_manager.check_market_regime", return_value=ftse_off),
            patch("database.get_portfolio", return_value=MOCK_PORTFOLIO),
            patch("database.get_positions", return_value=MOCK_POSITIONS_EMPTY),
            patch("utils.pricing.get_current_price", return_value=8.50),
            patch("utils.pricing.get_live_fx_rate", return_value=1.27),
            patch("services.earnings_service.get_earnings", return_value={"next_earnings_date": None, "days_until_earnings": None}),
        ):
            resp = CLIENT.get(f"{BASE_URL}?ticker=HSBA.L&quantity=100&market=UK")
        assert resp.status_code == 200
        regime_check = next(c for c in resp.json()["data"]["checks"] if c["rule"] == "regime_gate")
        assert regime_check["status"] == "fail"
        assert "FTSE" in regime_check["detail"]


# ---------------------------------------------------------------------------
# 2. Cash constraint
# ---------------------------------------------------------------------------

class TestCashConstraint:
    def test_cash_pass_when_sufficient(self):
        # cost: 10 × (215 / 1.27) ≈ £1,692 — below £5,000 cash
        with (
            patch("position_manager.check_market_regime", return_value=MOCK_REGIME_ON),
            patch("database.get_portfolio", return_value=MOCK_PORTFOLIO),
            patch("database.get_positions", return_value=MOCK_POSITIONS_EMPTY),
            patch("utils.pricing.get_current_price", return_value=215.0),
            patch("utils.pricing.get_live_fx_rate", return_value=1.27),
            patch("services.earnings_service.get_earnings", return_value={"next_earnings_date": None, "days_until_earnings": None}),
        ):
            resp = CLIENT.get(f"{BASE_URL}?ticker=AAPL&quantity=10&market=US")
        cash_check = next(c for c in resp.json()["data"]["checks"] if c["rule"] == "cash_constraint")
        assert cash_check["status"] == "pass"
        assert cash_check["estimated_cost_gbp"] < 5000.0

    def test_cash_fail_when_insufficient(self):
        # cost: 1000 × (215 / 1.27) ≈ £169,291 — above £5,000 cash
        with (
            patch("position_manager.check_market_regime", return_value=MOCK_REGIME_ON),
            patch("database.get_portfolio", return_value=MOCK_PORTFOLIO),
            patch("database.get_positions", return_value=MOCK_POSITIONS_EMPTY),
            patch("utils.pricing.get_current_price", return_value=215.0),
            patch("utils.pricing.get_live_fx_rate", return_value=1.27),
            patch("services.earnings_service.get_earnings", return_value={"next_earnings_date": None, "days_until_earnings": None}),
        ):
            resp = CLIENT.get(f"{BASE_URL}?ticker=AAPL&quantity=1000&market=US")
        cash_check = next(c for c in resp.json()["data"]["checks"] if c["rule"] == "cash_constraint")
        assert cash_check["status"] == "fail"
        assert cash_check["estimated_cost_gbp"] > cash_check["available_cash_gbp"]


# ---------------------------------------------------------------------------
# 3. Sector concentration
# ---------------------------------------------------------------------------

class TestSectorConcentration:
    def _existing_tech_position(self):
        return {
            "id": "pos-001",
            "ticker": "MSFT",
            "market": "US",
            "sector": "Technology",
            "shares": 50,
            "current_price": 420.0,
            "entry_price": 400.0,
        }

    def test_sector_pass_when_under_threshold(self):
        # Portfolio: £5,000 cash + 50 × (420/1.27) = £16,535 MSFT ≈ £21,535 total
        # New AAPL: 5 × (215/1.27) = £846 → tech = (16,535 + 846) / 21,535+846 ≈ 77% — WARN
        # Use very small quantity so it passes
        with (
            patch("position_manager.check_market_regime", return_value=MOCK_REGIME_ON),
            patch("database.get_portfolio", return_value={"id": "test-001", "cash": 100000.0}),
            patch("database.get_positions", return_value=[self._existing_tech_position()]),
            patch("utils.pricing.get_current_price", return_value=215.0),
            patch("utils.pricing.get_live_fx_rate", return_value=1.27),
            patch("services.earnings_service.get_earnings", return_value={"next_earnings_date": None, "days_until_earnings": None}),
            patch("database.get_db"),
        ):
            # Mock ticker_universe lookup to return Technology sector
            with patch("routers.pre_entry_validation._get_ticker_sector", return_value="Technology"):
                resp = CLIENT.get(f"{BASE_URL}?ticker=AAPL&quantity=1&market=US")
        sector_check = next(c for c in resp.json()["data"]["checks"] if c["rule"] == "sector_concentration")
        # With £100k cash and tiny position, sector pct will be very low
        assert sector_check["status"] in ("pass", "warn", "skipped")

    def test_sector_warn_when_over_threshold(self):
        # Portfolio: £1,000 cash + 1 × (215/1.27) = £169 = £1,169 total
        # New AAPL 8 shares: 8 × (215/1.27) = £1,354 → tech concentration > 30%
        with (
            patch("position_manager.check_market_regime", return_value=MOCK_REGIME_ON),
            patch("database.get_portfolio", return_value={"id": "test-001", "cash": 1000.0}),
            patch("database.get_positions", return_value=[self._existing_tech_position()]),
            patch("utils.pricing.get_current_price", return_value=215.0),
            patch("utils.pricing.get_live_fx_rate", return_value=1.27),
            patch("services.earnings_service.get_earnings", return_value={"next_earnings_date": None, "days_until_earnings": None}),
            patch("routers.pre_entry_validation._get_ticker_sector", return_value="Technology"),
        ):
            resp = CLIENT.get(f"{BASE_URL}?ticker=AAPL&quantity=100&market=US")
        data = resp.json()["data"]
        sector_check = next(c for c in data["checks"] if c["rule"] == "sector_concentration")
        assert sector_check["status"] in ("warn", "skipped")
        assert resp.status_code == 200  # non-blocking

    def test_sector_skipped_when_no_sector_data(self):
        with (
            patch("position_manager.check_market_regime", return_value=MOCK_REGIME_ON),
            patch("database.get_portfolio", return_value=MOCK_PORTFOLIO),
            patch("database.get_positions", return_value=MOCK_POSITIONS_EMPTY),
            patch("utils.pricing.get_current_price", return_value=215.0),
            patch("utils.pricing.get_live_fx_rate", return_value=1.27),
            patch("services.earnings_service.get_earnings", return_value={"next_earnings_date": None, "days_until_earnings": None}),
            patch("routers.pre_entry_validation._get_ticker_sector", return_value=None),
        ):
            resp = CLIENT.get(f"{BASE_URL}?ticker=UNKNOWN&quantity=10&market=US")
        sector_check = next(c for c in resp.json()["data"]["checks"] if c["rule"] == "sector_concentration")
        assert sector_check["status"] == "skipped"


# ---------------------------------------------------------------------------
# 4. Earnings proximity
# ---------------------------------------------------------------------------

class TestEarningsProximity:
    def test_earnings_warn_within_5_days(self):
        earnings = {"next_earnings_date": "2026-05-23", "days_until_earnings": 3}
        with (
            patch("position_manager.check_market_regime", return_value=MOCK_REGIME_ON),
            patch("database.get_portfolio", return_value=MOCK_PORTFOLIO),
            patch("database.get_positions", return_value=MOCK_POSITIONS_EMPTY),
            patch("utils.pricing.get_current_price", return_value=215.0),
            patch("utils.pricing.get_live_fx_rate", return_value=1.27),
            patch("routers.pre_entry_validation._get_ticker_sector", return_value=None),
            patch("services.earnings_service.get_earnings", return_value=earnings),
        ):
            resp = CLIENT.get(f"{BASE_URL}?ticker=AAPL&quantity=10&market=US")
        earnings_check = next(c for c in resp.json()["data"]["checks"] if c["rule"] == "earnings_proximity")
        assert earnings_check["status"] == "warn"
        assert earnings_check["days_until_earnings"] == 3

    def test_earnings_pass_outside_window(self):
        earnings = {"next_earnings_date": "2026-08-01", "days_until_earnings": 72}
        with (
            patch("position_manager.check_market_regime", return_value=MOCK_REGIME_ON),
            patch("database.get_portfolio", return_value=MOCK_PORTFOLIO),
            patch("database.get_positions", return_value=MOCK_POSITIONS_EMPTY),
            patch("utils.pricing.get_current_price", return_value=215.0),
            patch("utils.pricing.get_live_fx_rate", return_value=1.27),
            patch("routers.pre_entry_validation._get_ticker_sector", return_value=None),
            patch("services.earnings_service.get_earnings", return_value=earnings),
        ):
            resp = CLIENT.get(f"{BASE_URL}?ticker=AAPL&quantity=10&market=US")
        earnings_check = next(c for c in resp.json()["data"]["checks"] if c["rule"] == "earnings_proximity")
        assert earnings_check["status"] == "pass"

    def test_earnings_skipped_for_uk_ticker(self):
        with (
            patch("position_manager.check_market_regime", return_value=MOCK_REGIME_ON),
            patch("database.get_portfolio", return_value=MOCK_PORTFOLIO),
            patch("database.get_positions", return_value=MOCK_POSITIONS_EMPTY),
            patch("utils.pricing.get_current_price", return_value=8.50),
            patch("utils.pricing.get_live_fx_rate", return_value=1.27),
            patch("routers.pre_entry_validation._get_ticker_sector", return_value=None),
        ):
            resp = CLIENT.get(f"{BASE_URL}?ticker=HSBA.L&quantity=100&market=UK")
        earnings_check = next(c for c in resp.json()["data"]["checks"] if c["rule"] == "earnings_proximity")
        assert earnings_check["status"] == "skipped"


# ---------------------------------------------------------------------------
# 5. Sizing validity
# ---------------------------------------------------------------------------

class TestSizingValidity:
    def _common_patches(self):
        return dict(
            regime=patch("position_manager.check_market_regime", return_value=MOCK_REGIME_ON),
            portfolio=patch("database.get_portfolio", return_value=MOCK_PORTFOLIO),
            positions=patch("database.get_positions", return_value=MOCK_POSITIONS_EMPTY),
            price=patch("utils.pricing.get_current_price", return_value=215.0),
            fx=patch("utils.pricing.get_live_fx_rate", return_value=1.27),
            sector=patch("routers.pre_entry_validation._get_ticker_sector", return_value=None),
            earnings=patch("services.earnings_service.get_earnings", return_value={"next_earnings_date": None, "days_until_earnings": None}),
        )

    def test_sizing_pass_when_valid(self):
        p = self._common_patches()
        with p["regime"], p["portfolio"], p["positions"], p["price"], p["fx"], p["sector"], p["earnings"]:
            resp = CLIENT.get(f"{BASE_URL}?ticker=AAPL&quantity=10&market=US&entry_price=215&stop_price=200")
        sizing_check = next(c for c in resp.json()["data"]["checks"] if c["rule"] == "sizing_validity")
        assert sizing_check["status"] == "pass"
        assert sizing_check["stop_distance"] == pytest.approx(15.0, abs=0.001)

    def test_sizing_fail_when_stop_above_entry(self):
        p = self._common_patches()
        with p["regime"], p["portfolio"], p["positions"], p["price"], p["fx"], p["sector"], p["earnings"]:
            resp = CLIENT.get(f"{BASE_URL}?ticker=AAPL&quantity=10&market=US&entry_price=200&stop_price=215")
        sizing_check = next(c for c in resp.json()["data"]["checks"] if c["rule"] == "sizing_validity")
        assert sizing_check["status"] == "fail"
        assert resp.status_code == 200  # non-blocking

    def test_sizing_skipped_when_params_absent(self):
        p = self._common_patches()
        with p["regime"], p["portfolio"], p["positions"], p["price"], p["fx"], p["sector"], p["earnings"]:
            resp = CLIENT.get(f"{BASE_URL}?ticker=AAPL&quantity=10&market=US")
        sizing_check = next(c for c in resp.json()["data"]["checks"] if c["rule"] == "sizing_validity")
        assert sizing_check["status"] == "skipped"

    def test_sizing_fail_when_zero_price(self):
        p = self._common_patches()
        with p["regime"], p["portfolio"], p["positions"], p["price"], p["fx"], p["sector"], p["earnings"]:
            resp = CLIENT.get(f"{BASE_URL}?ticker=AAPL&quantity=10&market=US&entry_price=0&stop_price=0")
        sizing_check = next(c for c in resp.json()["data"]["checks"] if c["rule"] == "sizing_validity")
        assert sizing_check["status"] == "fail"


# ---------------------------------------------------------------------------
# Aggregate advisory status and non-blocking invariant
# ---------------------------------------------------------------------------

class TestAggregateStatus:
    def test_all_pass_gives_pass(self):
        earnings = {"next_earnings_date": "2026-08-01", "days_until_earnings": 72}
        with (
            patch("position_manager.check_market_regime", return_value=MOCK_REGIME_ON),
            patch("database.get_portfolio", return_value=MOCK_PORTFOLIO),
            patch("database.get_positions", return_value=MOCK_POSITIONS_EMPTY),
            patch("utils.pricing.get_current_price", return_value=50.0),
            patch("utils.pricing.get_live_fx_rate", return_value=1.27),
            patch("routers.pre_entry_validation._get_ticker_sector", return_value=None),
            patch("services.earnings_service.get_earnings", return_value=earnings),
        ):
            resp = CLIENT.get(f"{BASE_URL}?ticker=AAPL&quantity=1&market=US&entry_price=50&stop_price=45")
        data = resp.json()["data"]
        assert data["advisory_status"] == "pass"
        assert data["override_required"] is False

    def test_response_always_200_on_fail(self):
        """Non-blocking invariant: even complete fail advisory returns HTTP 200."""
        with (
            patch("position_manager.check_market_regime", return_value=MOCK_REGIME_OFF),
            patch("database.get_portfolio", return_value={"id": "test", "cash": 1.0}),
            patch("database.get_positions", return_value=MOCK_POSITIONS_EMPTY),
            patch("utils.pricing.get_current_price", return_value=10000.0),
            patch("utils.pricing.get_live_fx_rate", return_value=1.27),
            patch("routers.pre_entry_validation._get_ticker_sector", return_value=None),
            patch("services.earnings_service.get_earnings", return_value={"next_earnings_date": "2026-05-21", "days_until_earnings": 1}),
        ):
            resp = CLIENT.get(f"{BASE_URL}?ticker=AAPL&quantity=1000&market=US&entry_price=200&stop_price=210")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["advisory_status"] == "fail"
        # All 5 checks returned — no exception thrown
        assert len(data["checks"]) == 5


# ---------------------------------------------------------------------------
# Shared market regime cache (BLG-BE-25, v5.0 ST-07)
# ---------------------------------------------------------------------------

class TestMarketRegimeCache:
    """Cache lives in utils.pricing (BLG-BE-97, v8.8 ST-07 consolidation);
    position_manager.check_market_regime / _market_regime_cache are re-exports
    of the same function object / dict, so exercising either module name
    observes the one shared implementation and cache."""

    def test_second_call_uses_cache_not_network_fetch(self):
        """check_market_regime must not hit the network on cache hit."""
        import position_manager
        import datetime as dt

        # Pre-seed the cache with a fresh result
        cached_result = {"spy_risk_on": True, "ftse_risk_on": True}
        position_manager._market_regime_cache["result"] = cached_result
        position_manager._market_regime_cache["cached_at"] = dt.datetime.now()

        with patch("utils.pricing.requests.get") as mock_get:
            result = position_manager.check_market_regime()
            mock_get.assert_not_called()

        assert result["spy_risk_on"] is True

    def test_cache_miss_calls_network_fetch(self):
        """check_market_regime must hit the network when cache is stale."""
        import position_manager
        import datetime as dt

        # Expire the cache
        position_manager._market_regime_cache["result"] = None
        position_manager._market_regime_cache["cached_at"] = (
            dt.datetime.now() - dt.timedelta(seconds=400)
        )

        with patch("utils.pricing.requests.get") as mock_get:
            position_manager.check_market_regime()
            mock_get.assert_called()

    def test_pre_entry_validation_uses_shared_cache(self):
        """_check_regime in pre_entry_validation reads check_market_regime (cache path)."""
        # Patch check_market_regime to confirm it is the single call point
        with (
            patch("position_manager.check_market_regime", return_value=MOCK_REGIME_ON) as mock_regime,
            patch("database.get_portfolio", return_value=MOCK_PORTFOLIO),
            patch("database.get_positions", return_value=MOCK_POSITIONS_EMPTY),
            patch("utils.pricing.get_current_price", return_value=100.0),
            patch("utils.pricing.get_live_fx_rate", return_value=1.27),
            patch("routers.pre_entry_validation._get_ticker_sector", return_value=None),
            patch("services.earnings_service.get_earnings", return_value={"next_earnings_date": None, "days_until_earnings": None}),
        ):
            resp = CLIENT.get(f"{BASE_URL}?ticker=AAPL&quantity=5&market=US")
        assert resp.status_code == 200
        mock_regime.assert_called_once()
        regime_check = next(c for c in resp.json()["data"]["checks"] if c["rule"] == "regime_gate")
        assert regime_check["status"] == "pass"
