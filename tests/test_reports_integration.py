"""
ST-04: Reports Endpoint Integration Tests

FastAPI TestClient integration tests for GET /reports/tax-year.
Spec: docs/specs/api_contracts/reports_endpoints.md v0.1

CI-safe: all database calls are mocked via unittest.mock.patch.
No live DB or network connections are made.
"""

import unittest
from datetime import date
from unittest.mock import patch

from fastapi.testclient import TestClient

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from main import app

CLIENT = TestClient(app, raise_server_exceptions=False)

PATCH_GET_PORTFOLIO     = "services.reports_service.get_portfolio"
PATCH_GET_POSITIONS     = "services.reports_service.get_positions"
PATCH_GET_TAX_TRADES    = "services.reports_service.get_trade_history_by_tax_year"

MOCK_PORTFOLIO = {"id": "portfolio-test-001", "cash": 5000.0, "last_updated": "2026-03-17T10:00:00"}

def _trade(**overrides):
    base = {
        "id": "trade-001",
        "ticker": "VOD",
        "market": "UK",
        "entry_date": date(2025, 5, 1),
        "exit_date": date(2025, 8, 1),
        "holding_days": 92,
        "entry_price": 1.00,
        "exit_price": 1.20,
        "shares": 500,
        "total_cost": 500.00,
        "net_proceeds": 600.00,
        "pnl": 100.00,
        "pnl_pct": 20.00,
        "entry_fx_rate": None,
        "exit_fx_rate": None,
        "exit_reason": "stop_hit",
        "entry_note": None,
        "exit_note": None,
        "tags": [],
    }
    base.update(overrides)
    return base

def _us_trade(**overrides):
    base = {
        "id": "trade-002",
        "ticker": "NVDA",
        "market": "US",
        "entry_date": date(2025, 6, 1),
        "exit_date": date(2025, 9, 1),
        "holding_days": 92,
        "entry_price": 100.00,
        "exit_price": 120.00,
        "shares": 10,
        "total_cost": 800.00,
        "net_proceeds": 950.00,
        "pnl": 150.00,
        "pnl_pct": 18.75,
        "entry_fx_rate": 1.27,
        "exit_fx_rate": 1.25,
        "exit_reason": "target_reached",
        "entry_note": None,
        "exit_note": None,
        "tags": ["momentum"],
    }
    base.update(overrides)
    return base

MOCK_OPEN_POSITIONS = [
    {"pnl": 200.00, "status": "open"},
    {"pnl": 50.00, "status": "open"},
]


# ---------------------------------------------------------------------------
# 1. Validation — missing / invalid / future year
# ---------------------------------------------------------------------------

class TestTaxYearValidation(unittest.TestCase):

    def test_missing_year_returns_400(self):
        resp = CLIENT.get("/reports/tax-year")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["status"], "error")
        self.assertIn("required", resp.json()["message"])

    def test_three_digit_year_returns_400(self):
        resp = CLIENT.get("/reports/tax-year?year=999")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("four-digit", resp.json()["message"])

    def test_five_digit_year_returns_400(self):
        resp = CLIENT.get("/reports/tax-year?year=10000")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("four-digit", resp.json()["message"])

    def test_non_integer_year_returns_422(self):
        # FastAPI query param type coercion returns 422 for non-integer
        resp = CLIENT.get("/reports/tax-year?year=abcd")
        self.assertIn(resp.status_code, (400, 422))

    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    @patch(PATCH_GET_POSITIONS, return_value=[])
    @patch(PATCH_GET_TAX_TRADES, return_value=[])
    def test_future_year_returns_400(self, _t, _p, _port):
        resp = CLIENT.get("/reports/tax-year?year=2099")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("not started yet", resp.json()["message"])

    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    @patch(PATCH_GET_POSITIONS, return_value=[])
    @patch(PATCH_GET_TAX_TRADES, return_value=[])
    def test_current_year_2025_returns_200(self, _t, _p, _port):
        resp = CLIENT.get("/reports/tax-year?year=2025")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "ok")


# ---------------------------------------------------------------------------
# 2. Empty tax year — no trades
# ---------------------------------------------------------------------------

class TestTaxYearEmpty(unittest.TestCase):

    def _call(self, year=2025):
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=MOCK_OPEN_POSITIONS), \
             patch(PATCH_GET_TAX_TRADES, return_value=[]):
            return CLIENT.get(f"/reports/tax-year?year={year}").json()

    def test_status_ok(self):
        self.assertEqual(self._call()["status"], "ok")

    def test_tax_year_envelope_fields(self):
        data = self._call()["data"]
        self.assertEqual(data["tax_year_start"], "2025-04-06")
        self.assertEqual(data["tax_year_end"], "2026-04-05")
        self.assertEqual(data["tax_year_label"], "2025/26")
        self.assertIn("generated_at", data)

    def test_empty_summary_zeros(self):
        summary = self._call()["data"]["summary"]
        self.assertEqual(summary["total_closed_trades"], 0)
        self.assertEqual(summary["total_realised_pnl"], 0.0)
        self.assertEqual(summary["total_gross_profit"], 0.0)
        self.assertEqual(summary["total_gross_loss"], 0.0)
        self.assertEqual(summary["win_count"], 0)
        self.assertEqual(summary["loss_count"], 0)
        self.assertEqual(summary["win_rate"], 0.0)

    def test_unrealised_pnl_from_open_positions(self):
        summary = self._call()["data"]["summary"]
        # MOCK_OPEN_POSITIONS has pnl 200 + 50 = 250
        self.assertAlmostEqual(summary["estimated_unrealised_pnl"], 250.0, places=2)

    def test_unrealised_note_present(self):
        summary = self._call()["data"]["summary"]
        self.assertIn("unrealised_note", summary)
        self.assertIn("Indicative only", summary["unrealised_note"])

    def test_trades_empty_list(self):
        self.assertEqual(self._call()["data"]["trades"], [])


# ---------------------------------------------------------------------------
# 3. Summary arithmetic — with trades
# ---------------------------------------------------------------------------

class TestTaxYearSummary(unittest.TestCase):

    def _call(self, trades):
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=[]), \
             patch(PATCH_GET_TAX_TRADES, return_value=trades):
            return CLIENT.get("/reports/tax-year?year=2025").json()["data"]

    def test_total_realised_pnl(self):
        # trade 1: pnl=100, trade 2: pnl=150 → total 250
        data = self._call([_trade(pnl=100.0, total_cost=500.0, net_proceeds=600.0),
                           _us_trade(pnl=150.0, total_cost=800.0, net_proceeds=950.0)])
        self.assertAlmostEqual(data["summary"]["total_realised_pnl"], 250.0, places=2)

    def test_gross_profit_and_loss(self):
        # winner: pnl=100, loser: pnl=-50
        data = self._call([
            _trade(pnl=100.0, total_cost=500.0, net_proceeds=600.0),
            _trade(id="t2", pnl=-50.0, total_cost=500.0, net_proceeds=450.0),
        ])
        self.assertAlmostEqual(data["summary"]["total_gross_profit"], 100.0, places=2)
        self.assertAlmostEqual(data["summary"]["total_gross_loss"], -50.0, places=2)

    def test_win_rate(self):
        # 2 wins, 1 loss → 66.7%
        data = self._call([
            _trade(pnl=100.0, total_cost=500.0, net_proceeds=600.0),
            _trade(id="t2", pnl=50.0, total_cost=500.0, net_proceeds=550.0),
            _trade(id="t3", pnl=-30.0, total_cost=500.0, net_proceeds=470.0),
        ])
        self.assertAlmostEqual(data["summary"]["win_rate"], 66.7, places=1)
        self.assertEqual(data["summary"]["win_count"], 2)
        self.assertEqual(data["summary"]["loss_count"], 1)

    def test_total_closed_trades_count(self):
        data = self._call([_trade(), _us_trade()])
        self.assertEqual(data["summary"]["total_closed_trades"], 2)


# ---------------------------------------------------------------------------
# 4. Trade record field contract
# ---------------------------------------------------------------------------

class TestTaxYearTradeFields(unittest.TestCase):

    def _trade_record(self, trade_override=None):
        t = _trade(**(trade_override or {}))
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=[]), \
             patch(PATCH_GET_TAX_TRADES, return_value=[t]):
            return CLIENT.get("/reports/tax-year?year=2025").json()["data"]["trades"][0]

    def test_all_required_fields_present(self):
        record = self._trade_record()
        for field in ("id", "ticker", "market", "entry_date", "exit_date",
                      "holding_days", "entry_price_native", "exit_price_native",
                      "entry_fx_rate", "exit_fx_rate", "shares",
                      "total_cost_gbp", "exit_proceeds_gbp", "realised_pnl_gbp",
                      "pnl_pct", "currency", "tags"):
            self.assertIn(field, record, f"Missing trade field: {field}")

    def test_uk_trade_currency_gbp(self):
        record = self._trade_record()
        self.assertEqual(record["currency"], "GBP")
        self.assertIsNone(record["entry_fx_rate"])
        self.assertIsNone(record["exit_fx_rate"])

    def test_us_trade_currency_usd_and_fx_rates(self):
        t = _us_trade()
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=[]), \
             patch(PATCH_GET_TAX_TRADES, return_value=[t]):
            record = CLIENT.get("/reports/tax-year?year=2025").json()["data"]["trades"][0]
        self.assertEqual(record["currency"], "USD")
        self.assertAlmostEqual(record["entry_fx_rate"], 1.27, places=4)
        self.assertAlmostEqual(record["exit_fx_rate"], 1.25, places=4)

    def test_exit_proceeds_uses_net_proceeds(self):
        # net_proceeds=600, gross_proceeds would be higher — confirm net is used
        record = self._trade_record({"net_proceeds": 600.00, "total_cost": 500.00, "pnl": 100.00})
        self.assertAlmostEqual(record["exit_proceeds_gbp"], 600.00, places=2)

    def test_realised_pnl_from_pnl_column(self):
        record = self._trade_record({"pnl": 100.00, "total_cost": 500.00, "net_proceeds": 600.00})
        self.assertAlmostEqual(record["realised_pnl_gbp"], 100.00, places=2)

    def test_tags_empty_list_when_none(self):
        record = self._trade_record({"tags": None})
        self.assertEqual(record["tags"], [])

    def test_tags_passed_through(self):
        record = self._trade_record({"tags": ["momentum", "tech"]})
        self.assertEqual(record["tags"], ["momentum", "tech"])


# ---------------------------------------------------------------------------
# 5. Tax year boundary attribution
# ---------------------------------------------------------------------------

class TestTaxYearBoundary(unittest.TestCase):
    """
    Verifies the mock is called with the correct date range.
    Tax year 2025 = 2025-04-06 to 2026-04-05 inclusive.
    Attribution is by exit_date — the DB query enforces BETWEEN.
    These tests confirm the service passes the right boundaries.
    """

    def _dates_passed_to_db(self, year):
        captured = {}
        def fake_query(portfolio_id, year_start, year_end):
            captured['year_start'] = year_start
            captured['year_end'] = year_end
            return []
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=[]), \
             patch(PATCH_GET_TAX_TRADES, side_effect=fake_query):
            CLIENT.get(f"/reports/tax-year?year={year}")
        return captured

    def test_2025_start_is_april_6(self):
        dates = self._dates_passed_to_db(2025)
        from datetime import date
        self.assertEqual(dates['year_start'], date(2025, 4, 6))

    def test_2025_end_is_april_5_next_year(self):
        dates = self._dates_passed_to_db(2025)
        from datetime import date
        self.assertEqual(dates['year_end'], date(2026, 4, 5))

    def test_2024_boundaries(self):
        dates = self._dates_passed_to_db(2024)
        from datetime import date
        self.assertEqual(dates['year_start'], date(2024, 4, 6))
        self.assertEqual(dates['year_end'], date(2025, 4, 5))


# ---------------------------------------------------------------------------
# 6. Tax year label format
# ---------------------------------------------------------------------------

class TestTaxYearLabel(unittest.TestCase):

    def _label(self, year):
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=[]), \
             patch(PATCH_GET_TAX_TRADES, return_value=[]):
            return CLIENT.get(f"/reports/tax-year?year={year}").json()["data"]["tax_year_label"]

    def test_2025_label(self):
        self.assertEqual(self._label(2025), "2025/26")

    def test_2024_label(self):
        self.assertEqual(self._label(2024), "2024/25")

    def test_2099_is_future_not_labelled(self):
        # future year → 400, no label
        resp = CLIENT.get("/reports/tax-year?year=2099")
        self.assertEqual(resp.status_code, 400)


if __name__ == "__main__":
    unittest.main()
