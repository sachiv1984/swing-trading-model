"""
ST-05: Portfolio Endpoint Integration Tests

FastAPI TestClient integration tests for GET /portfolio.
Spec: docs/specs/api_contracts/portfolio_endpoints.md

CI-safe: all database and pricing calls are mocked via unittest.mock.patch.
No live DB or network connections are made.
Tests are independent — no ordering dependencies.

Deviation filed: GET /portfolio/prospective-heat is not defined in
portfolio_endpoints.md and does not exist in the backend. Tests for
that endpoint are skipped (DEV-ST05-01). See delegation_log.md
DEL-20260316-04 notes.
"""

import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from main import app

CLIENT = TestClient(app, raise_server_exceptions=False)

# ---------------------------------------------------------------------------
# Shared mock helpers
# ---------------------------------------------------------------------------

MOCK_PORTFOLIO = {
    "id": "portfolio-test-001",
    "cash": 10000.0,
    "last_updated": "2026-03-16T10:00:00",
}

def _uk_position(**overrides):
    base = {
        "id": "pos-uk-001",
        "ticker": "VOD",
        "market": "UK",
        "entry_price": 1.00,
        "fill_price": 1.00,
        "shares": 100,
        "entry_date": "2026-02-01",
        "current_price": 1.00,
        "current_stop": 0.80,
        "initial_stop": 0.80,
        "holding_days": 15,
        "fx_rate": 1.0,
        "status": "open",
        "total_cost": 100.0,
    }
    base.update(overrides)
    return base

def _us_position(**overrides):
    base = {
        "id": "pos-us-001",
        "ticker": "NVDA",
        "market": "US",
        "entry_price": 100.00,
        "fill_price": 100.00,
        "shares": 10,
        "entry_date": "2026-02-01",
        "current_price": 100.00,
        "current_stop": 85.00,
        "initial_stop": 85.00,
        "holding_days": 15,
        "fx_rate": 1.27,
        "status": "open",
        "total_cost": 787.40,
    }
    base.update(overrides)
    return base

MOCK_CASH_SUMMARY = {
    "net_cash_flow": 10000.0,
    "total_deposits": 10000.0,
    "total_withdrawals": 0.0,
}

MOCK_DRAWDOWN = {
    "current_drawdown_percent": 0.0,
    "peak_portfolio_value": 10000.0,
}

PATCH_GET_PORTFOLIO        = "services.portfolio_service.get_portfolio"
PATCH_GET_POSITIONS        = "services.portfolio_service.get_positions"
PATCH_GET_LIVE_FX_RATE     = "services.portfolio_service.get_live_fx_rate"
PATCH_GET_CURRENT_PRICE    = "services.portfolio_service.get_current_price"
PATCH_GET_DEPOSITS         = "services.portfolio_service.get_total_deposits_withdrawals"
PATCH_GET_DRAWDOWN         = "services.portfolio_service.get_drawdown_fields"


# ---------------------------------------------------------------------------
# 1. Response shape — empty portfolio
# ---------------------------------------------------------------------------

class TestGetPortfolioEmpty(unittest.TestCase):

    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    @patch(PATCH_GET_POSITIONS, return_value=[])
    @patch(PATCH_GET_LIVE_FX_RATE, return_value=1.27)
    @patch(PATCH_GET_DEPOSITS, return_value=MOCK_CASH_SUMMARY)
    @patch(PATCH_GET_DRAWDOWN, return_value=MOCK_DRAWDOWN)
    def test_status_ok(self, _dd, _dep, _fx, _pos, _port):
        resp = CLIENT.get("/portfolio")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "ok")

    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    @patch(PATCH_GET_POSITIONS, return_value=[])
    @patch(PATCH_GET_LIVE_FX_RATE, return_value=1.27)
    @patch(PATCH_GET_DEPOSITS, return_value=MOCK_CASH_SUMMARY)
    @patch(PATCH_GET_DRAWDOWN, return_value=MOCK_DRAWDOWN)
    def test_required_fields_present(self, _dd, _dep, _fx, _pos, _port):
        data = CLIENT.get("/portfolio").json()["data"]
        for field in ("cash", "cash_balance", "total_value", "open_positions_value",
                      "total_pnl", "initial_value", "net_deposits",
                      "live_fx_rate", "portfolio_heat_percent",
                      "current_drawdown_percent", "peak_portfolio_value",
                      "positions", "position_risks"):
            self.assertIn(field, data, f"Missing field: {field}")

    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    @patch(PATCH_GET_POSITIONS, return_value=[])
    @patch(PATCH_GET_LIVE_FX_RATE, return_value=1.27)
    @patch(PATCH_GET_DEPOSITS, return_value=MOCK_CASH_SUMMARY)
    @patch(PATCH_GET_DRAWDOWN, return_value=MOCK_DRAWDOWN)
    def test_empty_positions_list(self, _dd, _dep, _fx, _pos, _port):
        data = CLIENT.get("/portfolio").json()["data"]
        self.assertEqual(data["positions"], [])
        self.assertEqual(data["portfolio_heat_percent"], 0.0)
        self.assertEqual(data["open_positions_value"], 0)

    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    @patch(PATCH_GET_POSITIONS, return_value=[])
    @patch(PATCH_GET_LIVE_FX_RATE, return_value=1.27)
    @patch(PATCH_GET_DEPOSITS, return_value=MOCK_CASH_SUMMARY)
    @patch(PATCH_GET_DRAWDOWN, return_value=MOCK_DRAWDOWN)
    def test_drawdown_fields_present_when_empty(self, _dd, _dep, _fx, _pos, _port):
        data = CLIENT.get("/portfolio").json()["data"]
        self.assertEqual(data["current_drawdown_percent"], 0.0)
        self.assertEqual(data["peak_portfolio_value"], 10000.0)

    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    @patch(PATCH_GET_POSITIONS, return_value=[])
    @patch(PATCH_GET_LIVE_FX_RATE, return_value=1.27)
    @patch(PATCH_GET_DEPOSITS, return_value=MOCK_CASH_SUMMARY)
    @patch(PATCH_GET_DRAWDOWN, return_value=MOCK_DRAWDOWN)
    def test_net_deposits_and_initial_value_present_when_empty(self, _dd, _dep, _fx, _pos, _port):
        data = CLIENT.get("/portfolio").json()["data"]
        self.assertEqual(data["net_deposits"], 10000.0)
        self.assertEqual(data["initial_value"], 10000.0)

    @patch(PATCH_GET_PORTFOLIO, return_value=None)
    def test_portfolio_not_found_returns_error(self, _port):
        resp = CLIENT.get("/portfolio")
        self.assertIn(resp.status_code, (404, 200))
        body = resp.json()
        if resp.status_code == 200:
            self.assertEqual(body["status"], "error")


# ---------------------------------------------------------------------------
# 2. GBP conversion — UK position
# ---------------------------------------------------------------------------

class TestGetPortfolioUKPosition(unittest.TestCase):

    def _call(self, entry_price, live_price, shares=100, initial_stop=None):
        pos = _uk_position(
            entry_price=entry_price,
            fill_price=entry_price,
            shares=shares,
            initial_stop=initial_stop or (entry_price * 0.90),
            current_stop=initial_stop or (entry_price * 0.90),
        )
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=[pos]), \
             patch(PATCH_GET_LIVE_FX_RATE, return_value=1.27), \
             patch(PATCH_GET_CURRENT_PRICE, return_value=live_price), \
             patch(PATCH_GET_DEPOSITS, return_value=MOCK_CASH_SUMMARY), \
             patch(PATCH_GET_DRAWDOWN, return_value=MOCK_DRAWDOWN):
            return CLIENT.get("/portfolio").json()

    def test_uk_entry_price_in_gbp(self):
        body = self._call(entry_price=5.00, live_price=6.00)
        pos = body["data"]["positions"][0]
        self.assertAlmostEqual(pos["entry_price"], 5.00, places=2)

    def test_uk_current_price_in_gbp(self):
        body = self._call(entry_price=5.00, live_price=6.00)
        pos = body["data"]["positions"][0]
        self.assertAlmostEqual(pos["current_price"], 6.00, places=2)

    def test_uk_pnl_calculation(self):
        # P&L = (6.00 - 5.00) * 100 = £100
        body = self._call(entry_price=5.00, live_price=6.00, shares=100)
        pos = body["data"]["positions"][0]
        self.assertAlmostEqual(pos["pnl"], 100.00, places=2)

    def test_uk_position_fields_present(self):
        body = self._call(entry_price=5.00, live_price=6.00)
        pos = body["data"]["positions"][0]
        for field in ("id", "ticker", "market", "entry_date", "entry_price",
                      "shares", "current_price", "current_value", "pnl",
                      "pnl_pct", "current_stop", "holding_days", "status",
                      "display_status", "fx_rate", "grace_period",
                      "grace_days_remaining", "live_fx_rate"):
            self.assertIn(field, pos, f"Missing position field: {field}")


# ---------------------------------------------------------------------------
# 3. GBP conversion — US position
# ---------------------------------------------------------------------------

class TestGetPortfolioUSPosition(unittest.TestCase):

    FX = 1.27

    def _call(self, entry_price_usd, live_price_usd, shares=10, initial_stop_usd=None):
        pos = _us_position(
            entry_price=entry_price_usd,
            fill_price=entry_price_usd,
            shares=shares,
            initial_stop=initial_stop_usd or (entry_price_usd * 0.90),
            current_stop=initial_stop_usd or (entry_price_usd * 0.90),
            fx_rate=self.FX,
        )
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=[pos]), \
             patch(PATCH_GET_LIVE_FX_RATE, return_value=self.FX), \
             patch(PATCH_GET_CURRENT_PRICE, return_value=live_price_usd), \
             patch(PATCH_GET_DEPOSITS, return_value=MOCK_CASH_SUMMARY), \
             patch(PATCH_GET_DRAWDOWN, return_value=MOCK_DRAWDOWN):
            return CLIENT.get("/portfolio").json()

    def test_us_current_price_converted_to_gbp(self):
        # live price $110 USD → £110 / 1.27 = £86.61
        body = self._call(entry_price_usd=100.00, live_price_usd=110.00)
        pos = body["data"]["positions"][0]
        expected_gbp = round(110.00 / self.FX, 2)
        self.assertAlmostEqual(pos["current_price"], expected_gbp, places=1)

    def test_us_entry_price_converted_to_gbp(self):
        # entry $100 USD / fx_rate 1.27 → £78.74
        body = self._call(entry_price_usd=100.00, live_price_usd=110.00)
        pos = body["data"]["positions"][0]
        expected_gbp = round(100.00 / self.FX, 2)
        self.assertAlmostEqual(pos["entry_price"], expected_gbp, places=1)

    def test_us_pnl_in_gbp(self):
        # P&L = (110 - 100) * 10 shares / 1.27 = £78.74
        body = self._call(entry_price_usd=100.00, live_price_usd=110.00, shares=10)
        pos = body["data"]["positions"][0]
        expected_pnl = round((110.00 - 100.00) * 10 / self.FX, 2)
        self.assertAlmostEqual(pos["pnl"], expected_pnl, places=1)

    def test_us_current_stop_converted_to_gbp(self):
        # stop $85 / fx 1.27 = £66.93
        body = self._call(entry_price_usd=100.00, live_price_usd=110.00,
                          initial_stop_usd=85.00)
        pos = body["data"]["positions"][0]
        expected_stop = round(85.00 / self.FX, 2)
        self.assertAlmostEqual(pos["current_stop"], expected_stop, places=1)


# ---------------------------------------------------------------------------
# 4. Portfolio heat calculation
# ---------------------------------------------------------------------------

class TestPortfolioHeat(unittest.TestCase):

    def test_heat_correct_for_known_inputs(self):
        # UK position: entry=10.00, initial_stop=8.00, shares=50
        # position_risk = (10 - 8) * 50 = £100
        # cash = 10000, current_price = 10.00, current_value = 500
        # total_value = 10000 + 500 = 10500
        # heat = 100 / 10500 * 100 = 0.95%
        pos = _uk_position(
            entry_price=10.00, fill_price=10.00, shares=50,
            initial_stop=8.00, current_stop=8.00,
        )
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=[pos]), \
             patch(PATCH_GET_LIVE_FX_RATE, return_value=1.27), \
             patch(PATCH_GET_CURRENT_PRICE, return_value=10.00), \
             patch(PATCH_GET_DEPOSITS, return_value=MOCK_CASH_SUMMARY), \
             patch(PATCH_GET_DRAWDOWN, return_value=MOCK_DRAWDOWN):
            data = CLIENT.get("/portfolio").json()["data"]

        position_risk = (10.00 - 8.00) * 50   # £100
        total_value = 10000.0 + (10.00 * 50)  # £10500
        expected_heat = round(position_risk / total_value * 100, 2)
        self.assertAlmostEqual(data["portfolio_heat_percent"], expected_heat, places=1)

    def test_heat_zero_when_no_positions(self):
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=[]), \
             patch(PATCH_GET_LIVE_FX_RATE, return_value=1.27), \
             patch(PATCH_GET_DEPOSITS, return_value=MOCK_CASH_SUMMARY), \
             patch(PATCH_GET_DRAWDOWN, return_value=MOCK_DRAWDOWN):
            data = CLIENT.get("/portfolio").json()["data"]
        self.assertEqual(data["portfolio_heat_percent"], 0.0)

    def test_heat_zero_when_no_initial_stop(self):
        # position_risk = 0 when initial_stop is None → heat = 0
        pos = _uk_position(entry_price=10.00, initial_stop=None, current_stop=8.00)
        pos["initial_stop"] = None
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=[pos]), \
             patch(PATCH_GET_LIVE_FX_RATE, return_value=1.27), \
             patch(PATCH_GET_CURRENT_PRICE, return_value=10.00), \
             patch(PATCH_GET_DEPOSITS, return_value=MOCK_CASH_SUMMARY), \
             patch(PATCH_GET_DRAWDOWN, return_value=MOCK_DRAWDOWN):
            data = CLIENT.get("/portfolio").json()["data"]
        self.assertEqual(data["portfolio_heat_percent"], 0.0)


# ---------------------------------------------------------------------------
# 5. Grace period / display_status
# ---------------------------------------------------------------------------

class TestDisplayStatus(unittest.TestCase):

    def _call_with_holding_days(self, holding_days, pnl_positive=True):
        live_price = 6.00 if pnl_positive else 4.00
        pos = _uk_position(entry_price=5.00, fill_price=5.00,
                           holding_days=holding_days)
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=[pos]), \
             patch(PATCH_GET_LIVE_FX_RATE, return_value=1.27), \
             patch(PATCH_GET_CURRENT_PRICE, return_value=live_price), \
             patch(PATCH_GET_DEPOSITS, return_value=MOCK_CASH_SUMMARY), \
             patch(PATCH_GET_DRAWDOWN, return_value=MOCK_DRAWDOWN):
            return CLIENT.get("/portfolio").json()["data"]["positions"][0]

    def test_grace_period_when_holding_days_lt_10(self):
        pos = self._call_with_holding_days(holding_days=5)
        self.assertEqual(pos["display_status"], "GRACE")
        self.assertTrue(pos["grace_period"])

    def test_profitable_when_holding_days_gte_10_and_pnl_positive(self):
        pos = self._call_with_holding_days(holding_days=15, pnl_positive=True)
        self.assertEqual(pos["display_status"], "PROFITABLE")

    def test_losing_when_holding_days_gte_10_and_pnl_negative(self):
        pos = self._call_with_holding_days(holding_days=15, pnl_positive=False)
        self.assertEqual(pos["display_status"], "LOSING")


# ---------------------------------------------------------------------------
# 6. Portfolio-level field contract — non-empty path (GAP-03)
# ---------------------------------------------------------------------------

class TestGetPortfolioFieldContract(unittest.TestCase):
    """
    Asserts all required portfolio-level fields are present in the non-empty
    path response. Covers GAP-03 from docs/testing/v1.7-qa-scenario-gaps.md.
    Canonical field list: portfolio_endpoints.md §GET /portfolio data schema.
    """

    def _call(self):
        pos = _uk_position(entry_price=5.00, fill_price=5.00, shares=100,
                           initial_stop=4.50, current_stop=4.50, holding_days=15)
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=[pos]), \
             patch(PATCH_GET_LIVE_FX_RATE, return_value=1.27), \
             patch(PATCH_GET_CURRENT_PRICE, return_value=5.00), \
             patch(PATCH_GET_DEPOSITS, return_value=MOCK_CASH_SUMMARY), \
             patch(PATCH_GET_DRAWDOWN, return_value=MOCK_DRAWDOWN):
            return CLIENT.get("/portfolio").json()

    def test_all_portfolio_level_fields_present(self):
        data = self._call()["data"]
        required = (
            "cash", "cash_balance", "total_value", "open_positions_value",
            "total_pnl", "initial_value", "net_deposits", "live_fx_rate",
            "last_updated", "current_drawdown_percent", "peak_portfolio_value",
            "portfolio_heat_percent", "position_risks", "positions",
        )
        for field in required:
            self.assertIn(field, data, f"GAP-03: missing portfolio-level field: {field}")

    def test_drawdown_fields_correct_type(self):
        data = self._call()["data"]
        self.assertIsInstance(data["current_drawdown_percent"], float)
        self.assertIsInstance(data["peak_portfolio_value"], float)
        self.assertLessEqual(data["current_drawdown_percent"], 0.0)

    def test_net_deposits_and_initial_value_correct_type(self):
        data = self._call()["data"]
        self.assertIsInstance(data["net_deposits"], (int, float))
        self.assertIsInstance(data["initial_value"], (int, float))


# ---------------------------------------------------------------------------
# 7. Skipped: GET /portfolio/prospective-heat
#    DEV-ST05-01 (P3): Endpoint not defined in portfolio_endpoints.md and
#    not implemented in backend/main.py. Tests cannot pass without a spec
#    update and backend implementation. Deferred to a future spec cycle.
# ---------------------------------------------------------------------------

@unittest.skip(
    "DEV-ST05-01: GET /portfolio/prospective-heat is not defined in "
    "portfolio_endpoints.md and does not exist in backend/main.py. "
    "Tests skipped pending spec authoring and backend implementation."
)
class TestProspectiveHeat(unittest.TestCase):
    def test_placeholder(self):
        pass


if __name__ == "__main__":
    unittest.main()
