"""
ST-04: Reports Endpoint Integration Tests

FastAPI TestClient integration tests for GET /reports/tax-year.
Spec: docs/specs/api_contracts/reports_endpoints.md v0.1

CI-safe: all database calls are mocked via unittest.mock.patch.
No live DB or network connections are made.
"""

import os
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
        "trade_origin": "Manual",
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
        "trade_origin": "Manual",
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
                      "pnl_pct", "currency", "tags", "trade_origin"):
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

    def test_trade_origin_signal_when_linked_plan_has_signal_id(self):
        record = self._trade_record({"trade_origin": "Signal"})
        self.assertEqual(record["trade_origin"], "Signal")

    def test_trade_origin_manual_when_no_linked_signal(self):
        record = self._trade_record({"trade_origin": "Manual"})
        self.assertEqual(record["trade_origin"], "Manual")

    def test_trade_origin_defaults_to_manual_when_db_layer_omits_key(self):
        # Defensive default (service layer) — the live DB query's CASE always
        # returns 'Signal'/'Manual', but a mock/legacy caller might omit the
        # key entirely.
        t = _trade()
        del t["trade_origin"]
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=[]), \
             patch(PATCH_GET_TAX_TRADES, return_value=[t]):
            record = CLIENT.get("/reports/tax-year?year=2025").json()["data"]["trades"][0]
        self.assertEqual(record["trade_origin"], "Manual")


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


# ---------------------------------------------------------------------------
# 7. Tax-year CSV export — content-asserting + smoke coverage
#    ST-07 (EPIC-03, v7.1, BLG-SPEC-84) — AC-04 (reachability), AC-05 (content)
# ---------------------------------------------------------------------------

class TestTaxYearCsvExport(unittest.TestCase):
    """AC-05: asserts the actual returned CSV body content, not just that a
    request fired — a download that fires with wrong/truncated content is a
    silent data-integrity bug an integration-only test cannot catch.
    """

    def _call(self, year=2025, trades=None, positions=None):
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=positions if positions is not None else []), \
             patch(PATCH_GET_TAX_TRADES, return_value=trades if trades is not None else []):
            return CLIENT.get(f"/reports/tax-year?year={year}&format=csv")

    def test_ac04_smoke_endpoint_reachable_returns_200(self):
        """AC-04: minimal smoke/health-check style assertion — the export
        endpoint is reachable and returns success for a normal request."""
        resp = self._call(trades=[_trade()])
        self.assertEqual(resp.status_code, 200)

    def test_ac01_content_type_header(self):
        resp = self._call(trades=[_trade()])
        self.assertEqual(resp.headers["content-type"], "text/csv; charset=utf-8")

    def test_ac01_content_disposition_filename(self):
        resp = self._call(year=2025, trades=[_trade()])
        self.assertIn('attachment; filename="tax-year-2025-pnl.csv"', resp.headers["content-disposition"])

    def test_ac05_metadata_rows_present_with_correct_values(self):
        resp = self._call(year=2025, trades=[_trade()])
        rows = resp.text.splitlines()
        self.assertEqual(rows[0], "Tax Year,2025/26")
        self.assertTrue(rows[1].startswith("Generated At,"))
        self.assertEqual(rows[2], "Total Realised P&L (GBP),100.0")
        self.assertEqual(rows[3], "Total Closed Trades,1")
        self.assertEqual(rows[4], "Win Rate (%),100.0")
        self.assertEqual(rows[5], "")  # blank separator row

    def test_ac05_header_row_has_18_columns(self):
        resp = self._call(trades=[_trade()])
        header_row = resp.text.splitlines()[6]
        columns = header_row.split(",")
        self.assertEqual(len(columns), 18)
        self.assertEqual(columns[0], "Trade ID")
        self.assertEqual(columns[13], "Realised P&L (GBP)")
        self.assertEqual(columns[17], "Trade Origin")

    def test_ac05_uk_trade_data_row_values(self):
        resp = self._call(trades=[_trade(id="trade-uk-1")])
        data_row = resp.text.splitlines()[7]
        self.assertIn("trade-uk-1", data_row)
        self.assertIn("VOD", data_row)
        self.assertIn("UK", data_row)
        self.assertIn("100.0", data_row)   # realised P&L
        self.assertIn("GBP", data_row)     # currency

    def test_ac05_us_trade_row_includes_fx_rates(self):
        resp = self._call(trades=[_us_trade()])
        data_row = resp.text.splitlines()[7]
        self.assertIn("NVDA", data_row)
        self.assertIn("US", data_row)
        self.assertIn("1.27", data_row)   # entry_fx_rate
        self.assertIn("1.25", data_row)   # exit_fx_rate
        self.assertIn("USD", data_row)

    def test_ac05_tags_joined_with_semicolon(self):
        resp = self._call(trades=[_us_trade(tags=["momentum", "breakout"])])
        data_row = resp.text.splitlines()[7]
        self.assertIn("momentum; breakout", data_row)

    def test_trade_origin_signal_in_csv_row(self):
        resp = self._call(trades=[_us_trade(trade_origin="Signal")])
        data_row = resp.text.splitlines()[7]
        self.assertTrue(data_row.endswith(",Signal"))

    def test_trade_origin_manual_in_csv_row(self):
        resp = self._call(trades=[_trade(trade_origin="Manual")])
        data_row = resp.text.splitlines()[7]
        self.assertTrue(data_row.endswith(",Manual"))

    def test_ac05_empty_tax_year_still_has_valid_structure(self):
        """Empty year (zero closed trades) — CSV structure must remain valid
        (metadata block + header row), not just an empty/error body."""
        resp = self._call(trades=[])
        rows = resp.text.splitlines()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(rows[2], "Total Realised P&L (GBP),0")
        self.assertEqual(rows[3], "Total Closed Trades,0")
        # Header row still present even with zero trade rows following it
        self.assertEqual(len(rows[6].split(",")), 18)
        self.assertEqual(len(rows), 7)  # metadata(5) + blank(1) + header(1), no trade rows

    def test_ac02_csv_format_returns_401_without_api_key_when_configured(self):
        """AC-02: with API_KEY configured (production-like), format=csv must
        be rejected pre-route exactly like every other financial endpoint —
        confirms no per-format auth bypass exists in the route handler."""
        with patch.dict(os.environ, {"API_KEY": "test-secret"}):
            resp = CLIENT.get("/reports/tax-year?year=2025&format=csv")
        self.assertEqual(resp.status_code, 401)

    def test_ac02_csv_format_returns_200_with_valid_api_key(self):
        """AC-02: the same request succeeds with a valid key — proving the
        401 above is genuinely the auth gate, not an unrelated failure, and
        that format=csv works normally once authenticated."""
        with patch.dict(os.environ, {"API_KEY": "test-secret"}), \
             patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=[]), \
             patch(PATCH_GET_TAX_TRADES, return_value=[]):
            resp = CLIENT.get("/reports/tax-year?year=2025&format=csv", headers={"X-API-Key": "test-secret"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers["content-type"], "text/csv; charset=utf-8")



# ---------------------------------------------------------------------------
# 8. GET /reports/reconciliation — ST-01, EPIC-01, v8.2, BLG-FEAT-88
# ---------------------------------------------------------------------------

PATCH_GET_EXPORT_SUM = "services.reports_service.get_trade_history_pnl_sum_by_tax_year"


class TestReconciliation(unittest.TestCase):

    def _call(self, year=2025, trades=None, export_total=100.00, export_count=1):
        trades = trades if trades is not None else [_trade()]
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_POSITIONS, return_value=[]), \
             patch(PATCH_GET_TAX_TRADES, return_value=trades), \
             patch(PATCH_GET_EXPORT_SUM, return_value={"total": export_total, "trade_count": export_count}):
            return CLIENT.get(f"/reports/reconciliation?year={year}")

    def test_missing_year_returns_400(self):
        resp = CLIENT.get("/reports/reconciliation")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("required", resp.json()["message"])

    def test_future_year_returns_400(self):
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO):
            resp = CLIENT.get("/reports/reconciliation?year=2099")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("not started yet", resp.json()["message"])

    def test_matched_when_totals_equal(self):
        resp = self._call(trades=[_trade(pnl=100.00)], export_total=100.00)
        data = resp.json()["data"]
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data["matched"])
        self.assertEqual(data["system_total_pnl_gbp"], 100.00)
        self.assertEqual(data["export_total_pnl_gbp"], 100.00)

    def test_matched_within_rounding_tolerance(self):
        resp = self._call(trades=[_trade(pnl=100.004)], export_total=100.00)
        self.assertTrue(resp.json()["data"]["matched"])

    def test_not_matched_when_totals_diverge(self):
        resp = self._call(trades=[_trade(pnl=100.00)], export_total=95.00)
        data = resp.json()["data"]
        self.assertFalse(data["matched"])
        self.assertEqual(data["export_total_pnl_gbp"], 95.00)

    def test_empty_year_zero_trades_matched_true(self):
        resp = self._call(trades=[], export_total=0.0, export_count=0)
        data = resp.json()["data"]
        self.assertEqual(data["total_closed_trades"], 0)
        self.assertTrue(data["matched"])

    def test_tax_year_label_present(self):
        resp = self._call(year=2025)
        self.assertEqual(resp.json()["data"]["tax_year_label"], "2025/26")


if __name__ == "__main__":
    unittest.main()
