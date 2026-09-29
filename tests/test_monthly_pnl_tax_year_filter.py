"""
ST-03 (BLG-FE-190, EPIC-01, v9.8): GET /reports/monthly-pnl?year=<n> -- the
Monthly tab's Tax Year filter, and the tax-year-scoped restated-months
notice link from the Tax Year tab.

Design source: docs/design/2026-09-28__release-v9.8/tax-year-restated-notice-year-scoped-link/decision_record.md
Spec: docs/specs/api_contracts/reports_endpoints.md v0.14 §GET /reports/monthly-pnl

CI-safe: all database calls are mocked via unittest.mock.patch. No live DB
or network connections are made.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from main import app  # noqa: E402
from services.reports_service import get_monthly_pnl_report  # noqa: E402

CLIENT = TestClient(app, raise_server_exceptions=False)

MOCK_PORTFOLIO = {"id": "portfolio-test-001", "cash": 5000.0, "last_updated": "2026-03-17T10:00:00"}

PATCH_GET_PORTFOLIO = "services.reports_service.get_portfolio"
PATCH_GET_MONTHLY = "services.reports_service.get_monthly_pnl"
PATCH_GET_MONTHLY_BY_TAX_YEAR = "services.reports_service.get_monthly_pnl_by_tax_year"
PATCH_GET_UNREALISED = "services.reports_service.get_estimated_unrealised_pnl"


class TestGetMonthlyPnlReportYearScoping(unittest.TestCase):
    """Service-level: get_monthly_pnl_report(year=...) routing and date-range shape."""

    @patch(PATCH_GET_UNREALISED, return_value=None)
    @patch(PATCH_GET_MONTHLY_BY_TAX_YEAR)
    @patch(PATCH_GET_MONTHLY)
    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    def test_no_year_uses_rolling_window_unchanged(self, _port, rolling_fn, tax_year_fn, _unreal):
        """Omitting year: unchanged behaviour -- calls get_monthly_pnl, not the
        tax-year-scoped function. Regression guard for existing callers."""
        rolling_fn.return_value = []
        get_monthly_pnl_report()
        rolling_fn.assert_called_once_with(MOCK_PORTFOLIO["id"])
        tax_year_fn.assert_not_called()

    @patch(PATCH_GET_UNREALISED, return_value=None)
    @patch(PATCH_GET_MONTHLY_BY_TAX_YEAR)
    @patch(PATCH_GET_MONTHLY)
    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    def test_year_given_uses_tax_year_scoped_function_with_correct_range(self, _port, rolling_fn, tax_year_fn, _unreal):
        """year=2024 -> tax year 2024/25 -> [2024-04-06, 2025-04-05], and the
        rolling-window function is NOT called."""
        from datetime import date
        tax_year_fn.return_value = []
        get_monthly_pnl_report(year=2024)
        tax_year_fn.assert_called_once_with(MOCK_PORTFOLIO["id"], date(2024, 4, 6), date(2025, 4, 5))
        rolling_fn.assert_not_called()

    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    def test_future_year_raises_tax_year_not_started(self, _port):
        future_year = 9998  # comfortably beyond any real "today"
        with self.assertRaises(ValueError) as ctx:
            get_monthly_pnl_report(year=future_year)
        self.assertIn("not started yet", str(ctx.exception))


class TestMonthlyPnlEndpointYearParam(unittest.TestCase):
    """Endpoint-level: GET /reports/monthly-pnl?year=<n>."""

    @patch(PATCH_GET_UNREALISED, return_value=None)
    @patch(PATCH_GET_MONTHLY_BY_TAX_YEAR, return_value=[])
    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    def test_year_param_returns_200_with_scoped_data(self, _port, _tax_year_fn, _unreal):
        resp = CLIENT.get("/reports/monthly-pnl?year=2024")
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["status"], "ok")
        self.assertEqual(body["data"], [])

    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    def test_future_year_param_returns_400(self, _port):
        resp = CLIENT.get("/reports/monthly-pnl?year=9998")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("not started yet", resp.json()["message"])

    @patch(PATCH_GET_UNREALISED, return_value=None)
    @patch(PATCH_GET_MONTHLY, return_value=[])
    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    def test_no_year_param_returns_200_unchanged(self, _port, _rolling_fn, _unreal):
        """Regression guard: omitting ?year still works exactly as before."""
        resp = CLIENT.get("/reports/monthly-pnl")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "ok")


if __name__ == "__main__":
    unittest.main()
