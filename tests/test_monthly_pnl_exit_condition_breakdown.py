"""
ST-24 (BLG-FEAT-99, EPIC-04, v9.14): GET /reports/monthly-pnl's per-month
by_exit_condition -- realised P&L and trade count by strategy_rules.md §8 exit
condition, reconciling to the month's realised_pnl_gbp and trade_count.

Design source: docs/design/2026-10-29__release-v9.14/monthly-pnl-exit-condition-breakdown/decision_record.md
Spec: docs/specs/api_contracts/reports_endpoints.md v0.19 §GET /reports/monthly-pnl
Category mapping: docs/specs/metrics_definitions.md §Exit Condition Category

CI-safe: all database calls are mocked via unittest.mock.patch. No live DB
or network connections are made.
"""

import sys
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from exit_reasons import EXIT_REASONS, LEGACY_ALIASES  # noqa: E402
from main import app  # noqa: E402
from services.reports_service import (  # noqa: E402
    EXIT_CONDITION_KEYS,
    _exit_condition_key,
    get_monthly_pnl_report,
)

CLIENT = TestClient(app, raise_server_exceptions=False)

MOCK_PORTFOLIO = {"id": "portfolio-test-001", "cash": 5000.0, "last_updated": "2026-03-17T10:00:00"}

PATCH_GET_PORTFOLIO = "services.reports_service.get_portfolio"
PATCH_GET_MONTHLY = "services.reports_service.get_monthly_pnl"
PATCH_GET_MONTHLY_BY_TAX_YEAR = "services.reports_service.get_monthly_pnl_by_tax_year"
PATCH_GET_BY_EXIT_REASON = "services.reports_service.get_monthly_pnl_by_exit_reason"
PATCH_GET_UNREALISED = "services.reports_service.get_estimated_unrealised_pnl"
# Every month below is in the past, so the restatement snapshot path runs; it
# is not under test here.
PATCH_GET_DB = "services.reports_service.get_db"
PATCH_ENSURE_SNAPSHOTS = "services.reports_service.ensure_monthly_pnl_snapshots_table"
PATCH_SNAPSHOT_MONTH = "services.reports_service._snapshot_month"
SNAPSHOT_FIELDS = {"snapshotted": True, "restated": False, "snapshot_realised_pnl_gbp": 0.0, "restated_diff_gbp": 0.0}

# Two months, newest first, as get_monthly_pnl returns them.
MONTH_ROWS = [
    {"year": 2026, "month": 3, "realised_pnl_gbp": 87.65, "trade_count": 5, "null_fee_trade_count": 0},
    {"year": 2026, "month": 2, "realised_pnl_gbp": -40.00, "trade_count": 2, "null_fee_trade_count": 0},
]
# The same trades grouped by stored exit_reason. March mixes every category,
# a NULL reason and a legacy alias; February has stop-loss exits only.
EXIT_REASON_ROWS = [
    {"year": 2026, "month": 3, "exit_reason": "Stop Loss Hit", "realised_pnl_gbp": -120.10, "trade_count": 1},
    {"year": 2026, "month": 3, "exit_reason": "Trailing Stop", "realised_pnl_gbp": 210.25, "trade_count": 1},
    {"year": 2026, "month": 3, "exit_reason": "Risk-Off Signal", "realised_pnl_gbp": -15.50, "trade_count": 1},
    {"year": 2026, "month": 3, "exit_reason": None, "realised_pnl_gbp": 3.00, "trade_count": 1},
    {"year": 2026, "month": 3, "exit_reason": "target_reached", "realised_pnl_gbp": 10.00, "trade_count": 1},
    {"year": 2026, "month": 2, "exit_reason": "Stop Loss Hit", "realised_pnl_gbp": -40.00, "trade_count": 2},
]


def _report(month_rows, exit_rows, year=None):
    with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
         patch(PATCH_GET_MONTHLY, return_value=[dict(r) for r in month_rows]), \
         patch(PATCH_GET_MONTHLY_BY_TAX_YEAR, return_value=[dict(r) for r in month_rows]), \
         patch(PATCH_GET_BY_EXIT_REASON, return_value=exit_rows) as by_reason, \
         patch(PATCH_GET_UNREALISED, return_value=None), \
         patch(PATCH_GET_DB), patch(PATCH_ENSURE_SNAPSHOTS), \
         patch(PATCH_SNAPSHOT_MONTH, return_value=dict(SNAPSHOT_FIELDS)):
        return get_monthly_pnl_report(year=year), by_reason


class TestExitConditionKey(unittest.TestCase):
    """The mapping is metrics_definitions.md §Exit Condition Category."""

    def test_every_allowed_exit_reason_maps_to_its_section_8_category(self):
        for reason, category in EXIT_REASONS.items():
            self.assertEqual(_exit_condition_key(reason), EXIT_CONDITION_KEYS[category], reason)

    def test_expected_category_per_exit_reason(self):
        self.assertEqual(_exit_condition_key("Stop Loss Hit"), "stop_loss")
        self.assertEqual(_exit_condition_key("Trailing Stop"), "stop_loss")
        self.assertEqual(_exit_condition_key("Risk-Off Signal"), "risk_off")
        self.assertEqual(_exit_condition_key("Manual Exit"), "manual")
        self.assertEqual(_exit_condition_key("Target Reached"), "manual")
        self.assertEqual(_exit_condition_key("Partial Profit Taking"), "manual")

    def test_null_reads_as_manual_exit(self):
        self.assertEqual(_exit_condition_key(None), "manual")

    def test_legacy_aliases_resolve(self):
        for alias, reason in LEGACY_ALIASES.items():
            self.assertEqual(_exit_condition_key(alias), _exit_condition_key(reason), alias)

    def test_unknown_value_raises(self):
        with self.assertRaises(KeyError):
            _exit_condition_key("Gut Feeling")


class TestByExitConditionReconciles(unittest.TestCase):
    """AC 2: each month's categories sum to its realised P&L and trade count."""

    def test_categories_sum_to_month_totals(self):
        report, _ = _report(MONTH_ROWS, EXIT_REASON_ROWS)
        for m in report["months"]:
            cats = m["by_exit_condition"]
            self.assertEqual(set(cats), {"stop_loss", "risk_off", "manual"})
            self.assertAlmostEqual(sum(c["realised_pnl_gbp"] for c in cats.values()), m["realised_pnl_gbp"], places=2)
            self.assertEqual(sum(c["trade_count"] for c in cats.values()), m["trade_count"])

    def test_category_values(self):
        report, _ = _report(MONTH_ROWS, EXIT_REASON_ROWS)
        march, february = report["months"]
        self.assertEqual(march["by_exit_condition"], {
            "stop_loss": {"realised_pnl_gbp": 90.15, "trade_count": 2},
            "risk_off": {"realised_pnl_gbp": -15.50, "trade_count": 1},
            "manual": {"realised_pnl_gbp": 13.00, "trade_count": 2},
        })
        self.assertEqual(february["by_exit_condition"], {
            "stop_loss": {"realised_pnl_gbp": -40.00, "trade_count": 2},
            "risk_off": {"realised_pnl_gbp": 0.0, "trade_count": 0},
            "manual": {"realised_pnl_gbp": 0.0, "trade_count": 0},
        })

    def test_tax_year_bounds_passed_to_breakdown_query(self):
        _, by_reason = _report(MONTH_ROWS, EXIT_REASON_ROWS, year=2025)
        by_reason.assert_called_once_with(MOCK_PORTFOLIO["id"], date(2025, 4, 6), date(2026, 4, 5))

    def test_rolling_window_passes_no_bounds(self):
        _, by_reason = _report(MONTH_ROWS, EXIT_REASON_ROWS)
        by_reason.assert_called_once_with(MOCK_PORTFOLIO["id"], None, None)

    def test_no_months_skips_breakdown_query(self):
        report, by_reason = _report([], [])
        self.assertEqual(report["months"], [])
        by_reason.assert_not_called()


class TestByExitConditionUnavailable(unittest.TestCase):
    """reports.md §Exit Condition Breakdown "Unavailable": the field is omitted
    from every month and the realised P&L figures are unaffected."""

    def _assert_omitted(self, report):
        self.assertEqual(len(report["months"]), 2)
        for m in report["months"]:
            self.assertNotIn("by_exit_condition", m)
        self.assertEqual(report["months"][0]["realised_pnl_gbp"], 87.65)
        self.assertEqual(report["months"][0]["trade_count"], 5)

    def test_not_reconciling_omits_field(self):
        # A trade closed between the two queries: March's groups miss one trade.
        self._assert_omitted(_report(MONTH_ROWS, EXIT_REASON_ROWS[1:])[0])

    def test_unknown_exit_reason_omits_field(self):
        rows = EXIT_REASON_ROWS + [
            {"year": 2026, "month": 2, "exit_reason": "Gut Feeling", "realised_pnl_gbp": 0.0, "trade_count": 1},
        ]
        self._assert_omitted(_report(MONTH_ROWS, rows)[0])

    def test_query_failure_omits_field(self):
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_MONTHLY, return_value=[dict(r) for r in MONTH_ROWS]), \
             patch(PATCH_GET_BY_EXIT_REASON, side_effect=RuntimeError("db down")), \
             patch(PATCH_GET_UNREALISED, return_value=None), \
             patch(PATCH_GET_DB), patch(PATCH_ENSURE_SNAPSHOTS), \
             patch(PATCH_SNAPSHOT_MONTH, return_value=dict(SNAPSHOT_FIELDS)), \
             self.assertLogs("services.reports_service", level="ERROR"):
            report = get_monthly_pnl_report()
        self._assert_omitted(report)


class TestMonthlyPnlEndpointByExitCondition(unittest.TestCase):

    def test_endpoint_returns_by_exit_condition_per_month(self):
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_MONTHLY_BY_TAX_YEAR, return_value=[dict(r) for r in MONTH_ROWS]), \
             patch(PATCH_GET_BY_EXIT_REASON, return_value=EXIT_REASON_ROWS), \
             patch(PATCH_GET_UNREALISED, return_value=None), \
             patch(PATCH_GET_DB), patch(PATCH_ENSURE_SNAPSHOTS), \
             patch(PATCH_SNAPSHOT_MONTH, return_value=dict(SNAPSHOT_FIELDS)), \
             patch("main.get_arc5_compliance_summary", return_value=None):
            resp = CLIENT.get("/reports/monthly-pnl?year=2025")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()["data"]
        self.assertEqual(data[0]["by_exit_condition"]["stop_loss"], {"realised_pnl_gbp": 90.15, "trade_count": 2})

    def test_csv_export_unchanged(self):
        with patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO), \
             patch(PATCH_GET_MONTHLY_BY_TAX_YEAR, return_value=[dict(r) for r in MONTH_ROWS]), \
             patch(PATCH_GET_BY_EXIT_REASON, return_value=EXIT_REASON_ROWS), \
             patch(PATCH_GET_UNREALISED, return_value=None), \
             patch(PATCH_GET_DB), patch(PATCH_ENSURE_SNAPSHOTS), \
             patch(PATCH_SNAPSHOT_MONTH, return_value=dict(SNAPSHOT_FIELDS)):
            resp = CLIENT.get("/reports/monthly-pnl?year=2025&format=csv")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text.splitlines()[0], "Year,Month,Realised P&L (GBP),Trades")
        self.assertNotIn("stop_loss", resp.text)


if __name__ == "__main__":
    unittest.main()
