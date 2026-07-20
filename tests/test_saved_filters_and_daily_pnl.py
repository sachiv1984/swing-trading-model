"""
ST-04 (BLG-FE-118, EPIC-04, v7.5): Saved Filters & Daily P&L — Unit Tests

Tests the saved_filters CRUD service and the daily-pnl reporting logic in
isolation. No database or network calls are made — all I/O is mocked.

Coverage:
  - create_saved_filter: name/filter_state validation, duplicate-name rejection
  - delete_saved_filter: not-found handling
  - get_saved_filters / _row serialisation
  - get_daily_pnl_report: day-bucketed shape, no-portfolio path
"""

import sys
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch
from contextlib import contextmanager

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# Database stub is registered by tests/conftest.py (BLG-QA-20).

import importlib.util as _ilu

_sf_spec = _ilu.spec_from_file_location(
    "saved_filters_service",
    Path(__file__).parent.parent / "backend" / "services" / "saved_filters_service.py",
)
saved_filters_service = _ilu.module_from_spec(_sf_spec)
_sf_spec.loader.exec_module(saved_filters_service)


def _make_ctx(cur):
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=cur)
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

    @contextmanager
    def _ctx():
        yield mock_conn

    return _ctx


# ---------------------------------------------------------------------------
# create_saved_filter
# ---------------------------------------------------------------------------

class TestCreateSavedFilter(unittest.TestCase):

    def test_rejects_missing_name(self):
        with self.assertRaises(ValueError):
            saved_filters_service.create_saved_filter("portfolio-1", {"name": "", "filter_state": {}})

    def test_rejects_name_over_100_chars(self):
        with self.assertRaises(ValueError):
            saved_filters_service.create_saved_filter(
                "portfolio-1", {"name": "x" * 101, "filter_state": {}}
            )

    def test_rejects_non_dict_filter_state(self):
        with self.assertRaises(ValueError):
            saved_filters_service.create_saved_filter(
                "portfolio-1", {"name": "My Winners", "filter_state": "not-a-dict"}
            )

    def test_rejects_missing_filter_state(self):
        with self.assertRaises(ValueError):
            saved_filters_service.create_saved_filter("portfolio-1", {"name": "My Winners"})

    def test_rejects_duplicate_name(self):
        cur = MagicMock()
        cur.fetchone.return_value = {"id": "existing-id"}
        ctx = _make_ctx(cur)

        with patch.object(saved_filters_service, "get_db", ctx):
            with self.assertRaises(ValueError) as ctxmgr:
                saved_filters_service.create_saved_filter(
                    "portfolio-1", {"name": "My Winners", "filter_state": {"result": "win"}}
                )
        self.assertIn("already exists", str(ctxmgr.exception))

    def test_creates_when_name_is_unique(self):
        cur = MagicMock()
        cur.fetchone.side_effect = [
            None,  # duplicate check — no existing row
            {
                "id": "sf-1", "name": "My Winners", "filter_state": {"result": "win"},
                "created_at": "2026-07-20T10:00:00Z", "updated_at": "2026-07-20T10:00:00Z",
            },
        ]
        ctx = _make_ctx(cur)

        with patch.object(saved_filters_service, "get_db", ctx):
            result = saved_filters_service.create_saved_filter(
                "portfolio-1", {"name": "My Winners", "filter_state": {"result": "win"}}
            )
        self.assertEqual(result["name"], "My Winners")
        self.assertEqual(result["filter_state"], {"result": "win"})


class TestDeleteSavedFilter(unittest.TestCase):

    def test_raises_lookup_error_when_not_found(self):
        cur = MagicMock()
        cur.fetchone.return_value = None
        ctx = _make_ctx(cur)

        with patch.object(saved_filters_service, "get_db", ctx):
            with self.assertRaises(LookupError):
                saved_filters_service.delete_saved_filter("portfolio-1", "missing-id")

    def test_returns_deleted_true_on_success(self):
        cur = MagicMock()
        cur.fetchone.return_value = {"id": "sf-1"}
        ctx = _make_ctx(cur)

        with patch.object(saved_filters_service, "get_db", ctx):
            result = saved_filters_service.delete_saved_filter("portfolio-1", "sf-1")
        self.assertEqual(result, {"deleted": True, "id": "sf-1"})


class TestGetSavedFilters(unittest.TestCase):

    def test_returns_serialised_rows(self):
        cur = MagicMock()
        cur.fetchall.return_value = [
            {
                "id": "sf-1", "name": "My Winners", "filter_state": {"result": "win"},
                "created_at": "2026-07-20T10:00:00Z", "updated_at": "2026-07-20T10:00:00Z",
            }
        ]
        ctx = _make_ctx(cur)

        with patch.object(saved_filters_service, "get_db", ctx):
            result = saved_filters_service.get_saved_filters("portfolio-1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "sf-1")
        self.assertEqual(result[0]["filter_state"], {"result": "win"})

    def test_returns_empty_list_when_no_presets(self):
        cur = MagicMock()
        cur.fetchall.return_value = []
        ctx = _make_ctx(cur)

        with patch.object(saved_filters_service, "get_db", ctx):
            result = saved_filters_service.get_saved_filters("portfolio-1")
        self.assertEqual(result, [])


# ---------------------------------------------------------------------------
# get_daily_pnl_report (reports_service.py)
# ---------------------------------------------------------------------------

_config_stub = types.ModuleType("config")
sys.modules.setdefault("config", _config_stub)

_reports_spec = _ilu.spec_from_file_location(
    "reports_service",
    Path(__file__).parent.parent / "backend" / "services" / "reports_service.py",
)
reports_service = _ilu.module_from_spec(_reports_spec)
_reports_spec.loader.exec_module(reports_service)


class TestGetDailyPnlReport(unittest.TestCase):

    def test_no_portfolio_returns_empty_days(self):
        with patch.object(reports_service, "get_portfolio", return_value=None):
            result = reports_service.get_daily_pnl_report(2026, 7)
        self.assertEqual(result["days"], [])
        self.assertIsNone(result["estimated_unrealised_pnl"])

    def test_returns_day_bucketed_rows(self):
        with patch.object(reports_service, "get_portfolio", return_value={"id": "portfolio-1"}), \
             patch.object(reports_service, "get_daily_pnl", return_value=[
                 {"day": 3, "realised_pnl_gbp": 240.5, "trade_count": 3},
                 {"day": 17, "realised_pnl_gbp": -85.0, "trade_count": 1},
             ]), \
             patch.object(reports_service, "get_estimated_unrealised_pnl", return_value=340.5):
            result = reports_service.get_daily_pnl_report(2026, 7)

        self.assertEqual(len(result["days"]), 2)
        self.assertEqual(result["days"][0], {"day": 3, "realised_pnl_gbp": 240.5, "trade_count": 3})
        self.assertEqual(result["days"][1], {"day": 17, "realised_pnl_gbp": -85.0, "trade_count": 1})
        self.assertEqual(result["estimated_unrealised_pnl"], 340.5)
        self.assertIn("Indicative only", result["unrealised_note"])

    def test_empty_month_returns_empty_days_not_none(self):
        with patch.object(reports_service, "get_portfolio", return_value={"id": "portfolio-1"}), \
             patch.object(reports_service, "get_daily_pnl", return_value=[]), \
             patch.object(reports_service, "get_estimated_unrealised_pnl", return_value=0.0):
            result = reports_service.get_daily_pnl_report(2026, 8)
        self.assertEqual(result["days"], [])
        self.assertEqual(result["estimated_unrealised_pnl"], 0.0)


if __name__ == "__main__":
    unittest.main()
