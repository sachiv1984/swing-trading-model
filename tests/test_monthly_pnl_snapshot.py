"""
ST-08 (BLG-FR-05, EPIC-02, v9.6): Month-end immutable snapshot of Monthly
P&L (and a derived Tax Year restated-month notice), with a restatement diff.

Two layers of coverage, matching this file's existing conventions
(test_null_fee_trade_audit.py, test_reflection_reminder.py):
  - Service-level (get_monthly_pnl_report / get_tax_year_report): database
    functions mocked by name, business logic exercised directly.
  - Database-level (ensure_/insert_ functions): mocked cursor, asserts SQL
    shape -- same idiom as TestEnsureTablesMigration in
    test_reflection_reminder.py. Not executed against a live PostgreSQL
    (data_model.md DS-20's disclosed verification status).
"""
import sys
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from services.reports_service import (  # noqa: E402
    get_monthly_pnl_report,
    get_tax_year_report,
    _is_closed_month,
)

MOCK_PORTFOLIO = {"id": "portfolio-test-001"}

PATCH_GET_PORTFOLIO = "services.reports_service.get_portfolio"
PATCH_GET_MONTHLY_PNL = "services.reports_service.get_monthly_pnl"
PATCH_GET_POSITIONS = "services.reports_service.get_positions"
PATCH_GET_SNAPSHOT = "services.reports_service.get_monthly_pnl_snapshot"
PATCH_INSERT_SNAPSHOT = "services.reports_service.insert_monthly_pnl_snapshot_if_absent"
PATCH_SNAPSHOTS_IN_RANGE = "services.reports_service.get_monthly_pnl_snapshots_in_range"
PATCH_GET_TAX_TRADES = "services.reports_service.get_trade_history_by_tax_year"


# ─── _is_closed_month ──────────────────────────────────────────────────────

class TestIsClosedMonth(unittest.TestCase):
    def test_prior_month_same_year_is_closed(self):
        self.assertTrue(_is_closed_month(2026, 8, date(2026, 9, 22)))

    def test_current_month_is_not_closed(self):
        self.assertFalse(_is_closed_month(2026, 9, date(2026, 9, 22)))

    def test_prior_year_is_closed(self):
        self.assertTrue(_is_closed_month(2025, 12, date(2026, 1, 5)))

    def test_future_month_is_not_closed(self):
        self.assertFalse(_is_closed_month(2026, 10, date(2026, 9, 22)))


# ─── get_monthly_pnl_report: baseline-once + restatement diff ─────────────

class TestMonthlyPnlSnapshotting(unittest.TestCase):

    @patch(PATCH_GET_POSITIONS, return_value=[])
    @patch(PATCH_INSERT_SNAPSHOT)
    @patch(PATCH_GET_SNAPSHOT, return_value=None)
    @patch(PATCH_GET_MONTHLY_PNL, return_value=[
        {"year": 2026, "month": 8, "realised_pnl_gbp": 100.0, "trade_count": 2, "null_fee_trade_count": 0},
    ])
    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    @patch("services.reports_service.datetime")
    def test_closed_month_with_no_prior_snapshot_is_baselined(self, mock_dt, *_, insert_mock=None, snap_mock=None):
        # datetime.now(timezone.utc).date() must resolve to 2026-09-22
        mock_dt.now.return_value.date.return_value = date(2026, 9, 22)
        report = get_monthly_pnl_report()
        month = report["months"][0]
        self.assertTrue(month["snapshotted"])
        self.assertFalse(month["restated"])
        self.assertEqual(month["snapshot_realised_pnl_gbp"], 100.0)
        self.assertEqual(month["restated_diff_gbp"], 0.0)

    @patch(PATCH_GET_POSITIONS, return_value=[])
    @patch(PATCH_INSERT_SNAPSHOT)
    @patch(PATCH_GET_SNAPSHOT, return_value={
        "year": 2026, "month": 8, "realised_pnl_gbp": 100.0, "trade_count": 2,
    })
    @patch(PATCH_GET_MONTHLY_PNL, return_value=[
        {"year": 2026, "month": 8, "realised_pnl_gbp": 100.0, "trade_count": 2, "null_fee_trade_count": 0},
    ])
    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    @patch("services.reports_service.datetime")
    def test_closed_month_matching_snapshot_is_not_restated(self, mock_dt, *_):
        mock_dt.now.return_value.date.return_value = date(2026, 9, 22)
        report = get_monthly_pnl_report()
        month = report["months"][0]
        self.assertTrue(month["snapshotted"])
        self.assertFalse(month["restated"])
        self.assertEqual(month["restated_diff_gbp"], 0.0)

    @patch(PATCH_GET_POSITIONS, return_value=[])
    @patch(PATCH_INSERT_SNAPSHOT)
    @patch(PATCH_GET_SNAPSHOT, return_value={
        "year": 2026, "month": 8, "realised_pnl_gbp": 100.0, "trade_count": 2,
    })
    @patch(PATCH_GET_MONTHLY_PNL, return_value=[
        # Live total now disagrees with the stored baseline.
        {"year": 2026, "month": 8, "realised_pnl_gbp": 145.50, "trade_count": 3, "null_fee_trade_count": 0},
    ])
    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    @patch("services.reports_service.datetime")
    def test_closed_month_diverging_from_snapshot_is_restated(self, mock_dt, *_):
        mock_dt.now.return_value.date.return_value = date(2026, 9, 22)
        report = get_monthly_pnl_report()
        month = report["months"][0]
        self.assertTrue(month["snapshotted"])
        self.assertTrue(month["restated"])
        self.assertEqual(month["snapshot_realised_pnl_gbp"], 100.0)
        self.assertEqual(month["restated_diff_gbp"], 45.50)

    @patch(PATCH_GET_POSITIONS, return_value=[])
    @patch(PATCH_INSERT_SNAPSHOT)
    @patch(PATCH_GET_SNAPSHOT)
    @patch(PATCH_GET_MONTHLY_PNL, return_value=[
        # The current, in-progress month (September 2026) -- never snapshotted.
        {"year": 2026, "month": 9, "realised_pnl_gbp": 40.0, "trade_count": 1, "null_fee_trade_count": 0},
    ])
    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    @patch("services.reports_service.datetime")
    def test_current_month_is_never_snapshotted(
        self, mock_dt, get_portfolio_mock, get_monthly_pnl_mock, get_snapshot_mock, insert_mock, positions_mock
    ):
        mock_dt.now.return_value.date.return_value = date(2026, 9, 22)
        report = get_monthly_pnl_report()
        month = report["months"][0]
        self.assertFalse(month["snapshotted"])
        self.assertFalse(month["restated"])
        self.assertIsNone(month["snapshot_realised_pnl_gbp"])
        self.assertIsNone(month["restated_diff_gbp"])
        get_snapshot_mock.assert_not_called()
        insert_mock.assert_not_called()

    @patch(PATCH_GET_POSITIONS, return_value=[])
    @patch(PATCH_INSERT_SNAPSHOT)
    @patch(PATCH_GET_SNAPSHOT, return_value=None)
    @patch(PATCH_GET_MONTHLY_PNL, return_value=[
        {"year": 2026, "month": 8, "realised_pnl_gbp": 100.0, "trade_count": 2, "null_fee_trade_count": 0},
    ])
    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    @patch("services.reports_service.datetime")
    def test_baselining_is_insert_if_absent_not_unconditional_write(
        self, mock_dt, get_portfolio_mock, get_monthly_pnl_mock, get_snapshot_mock, insert_mock, positions_mock
    ):
        """Baselining must go through the insert-if-absent path (immutability
        is enforced at the DB layer's ON CONFLICT DO NOTHING, not by this
        service re-checking) -- confirms the call, not a raw UPDATE."""
        mock_dt.now.return_value.date.return_value = date(2026, 9, 22)
        get_monthly_pnl_report()
        insert_mock.assert_called_once_with("portfolio-test-001", 2026, 8, 100.0, 2)


# ─── get_tax_year_report: restated_month_count / restated_months_notice ───

class TestTaxYearRestatedMonthsNotice(unittest.TestCase):

    @patch(PATCH_GET_POSITIONS, return_value=[])
    @patch(PATCH_GET_TAX_TRADES, return_value=[])
    @patch(PATCH_GET_MONTHLY_PNL, return_value=[])
    @patch(PATCH_SNAPSHOTS_IN_RANGE, return_value=[])
    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    def test_no_snapshots_in_range_gives_null_notice(self, *_):
        report = get_tax_year_report(2025)
        self.assertEqual(report["summary"]["restated_month_count"], 0)
        self.assertIsNone(report["summary"]["restated_months_notice"])

    @patch(PATCH_GET_POSITIONS, return_value=[])
    @patch(PATCH_GET_TAX_TRADES, return_value=[])
    @patch(PATCH_GET_MONTHLY_PNL, return_value=[
        {"year": 2025, "month": 7, "realised_pnl_gbp": 200.0, "trade_count": 4},
    ])
    @patch(PATCH_SNAPSHOTS_IN_RANGE, return_value=[
        {"year": 2025, "month": 7, "realised_pnl_gbp": 150.0, "trade_count": 3},
    ])
    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    def test_one_diverging_month_counted_and_worded_singular(self, *_):
        report = get_tax_year_report(2025)
        self.assertEqual(report["summary"]["restated_month_count"], 1)
        self.assertEqual(report["summary"]["restated_months_notice"], "Includes 1 restated month")

    @patch(PATCH_GET_POSITIONS, return_value=[])
    @patch(PATCH_GET_TAX_TRADES, return_value=[])
    @patch(PATCH_GET_MONTHLY_PNL, return_value=[
        {"year": 2025, "month": 7, "realised_pnl_gbp": 200.0, "trade_count": 4},
        {"year": 2025, "month": 8, "realised_pnl_gbp": 50.0, "trade_count": 1},
    ])
    @patch(PATCH_SNAPSHOTS_IN_RANGE, return_value=[
        {"year": 2025, "month": 7, "realised_pnl_gbp": 150.0, "trade_count": 3},
        {"year": 2025, "month": 8, "realised_pnl_gbp": 50.0, "trade_count": 1},
    ])
    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    def test_matching_month_not_counted_diverging_month_is_plural_worded(self, *_):
        report = get_tax_year_report(2025)
        self.assertEqual(report["summary"]["restated_month_count"], 1)
        self.assertIn("1 restated month", report["summary"]["restated_months_notice"])

    @patch(PATCH_GET_POSITIONS, return_value=[])
    @patch(PATCH_GET_TAX_TRADES, return_value=[])
    @patch(PATCH_GET_MONTHLY_PNL, return_value=[])  # aged out of the rolling window
    @patch(PATCH_SNAPSHOTS_IN_RANGE, return_value=[
        {"year": 2020, "month": 5, "realised_pnl_gbp": 10.0, "trade_count": 1},
    ])
    @patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
    def test_snapshot_with_no_matching_live_row_is_not_guessed_as_restated(self, *_):
        """A month aged out of get_monthly_pnl's rolling window has no live
        figure to compare against -- must not be silently counted either way."""
        report = get_tax_year_report(2020)
        self.assertEqual(report["summary"]["restated_month_count"], 0)
        self.assertIsNone(report["summary"]["restated_months_notice"])


# ─── Database-layer: SQL shape (mocked cursor, same idiom as
#     TestEnsureTablesMigration in test_reflection_reminder.py) ───────────
#
# The session-scoped stub in conftest.py replaces sys.modules["database"]
# with a MagicMock-attribute stub whose function list is AST-derived from
# `from database import (...)` sites -- it does not include
# ensure_monthly_pnl_snapshots_table (only called internally, never
# imported by name elsewhere), so it cannot be exercised through that stub.
# Loaded here directly from its file via importlib instead of touching
# sys.modules["database"] -- per ST-21 (EPIC-05, this cycle, BLG-QA-178),
# an unrestored sys.modules["database"] swap is itself a known
# test-isolation hazard; this avoids reproducing that pattern.

import importlib.util as _importlib_util  # noqa: E402

_DATABASE_PY = Path(__file__).parent.parent / "backend" / "database.py"
_spec = _importlib_util.spec_from_file_location("database_real_for_ds20_test", _DATABASE_PY)
_real_database = _importlib_util.module_from_spec(_spec)
_spec.loader.exec_module(_real_database)


class TestMonthlyPnlSnapshotsTableMigration(unittest.TestCase):

    def _run(self, fn, *args):
        cur = MagicMock()
        cur.fetchone.return_value = None
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value = cur
        ctx = MagicMock()
        ctx.__enter__.return_value = conn
        with patch.object(_real_database, "get_db", return_value=ctx):
            fn(*args)
        return [c.args[0] for c in cur.execute.call_args_list], conn

    def test_ensure_table_is_idempotent_create_if_not_exists(self):
        sql, conn = self._run(_real_database.ensure_monthly_pnl_snapshots_table)
        self.assertTrue(any("CREATE TABLE IF NOT EXISTS monthly_pnl_snapshots" in q for q in sql))
        self.assertTrue(any("UNIQUE (portfolio_id, year, month)" in q for q in sql))
        conn.commit.assert_called()

    def test_insert_if_absent_uses_on_conflict_do_nothing(self):
        sql, conn = self._run(
            _real_database.insert_monthly_pnl_snapshot_if_absent,
            "portfolio-test-001", 2026, 8, 100.0, 2,
        )
        insert_sql = [q for q in sql if "INSERT INTO monthly_pnl_snapshots" in q]
        self.assertEqual(len(insert_sql), 1)
        self.assertIn("ON CONFLICT (portfolio_id, year, month) DO NOTHING", insert_sql[0])
        conn.commit.assert_called()


if __name__ == "__main__":
    unittest.main()
