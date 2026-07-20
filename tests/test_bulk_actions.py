"""
ST-03 (BLG-FE-117, EPIC-03, v7.5): Bulk Actions — Unit Tests

Tests the bulk-tag/bulk-archive/bulk-delete service-layer logic for Watchlist
and Trade Plans in isolation. No database or network calls — all I/O is mocked.

Coverage:
  - watchlist_service.bulk_tag_watchlist / bulk_delete_watchlist / get_all_watchlist_tags
  - database.bulk_tag_trade_plans / bulk_archive_trade_plans / bulk_delete_trade_plans
  - Partial-failure response shape ({succeeded, failed}) per readiness pass AC-01
  - Batch size cap (100 IDs)
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch
from contextlib import contextmanager

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# Database stub is registered by tests/conftest.py (BLG-QA-20) — sets a dummy
# DATABASE_URL so the real database.py module can be loaded directly below.

import importlib.util as _ilu

_wl_spec = _ilu.spec_from_file_location(
    "watchlist_service",
    Path(__file__).parent.parent / "backend" / "services" / "watchlist_service.py",
)
watchlist_service = _ilu.module_from_spec(_wl_spec)
_wl_spec.loader.exec_module(watchlist_service)

_db_spec = _ilu.spec_from_file_location(
    "database_real",
    Path(__file__).parent.parent / "backend" / "database.py",
)
database_real = _ilu.module_from_spec(_db_spec)
_db_spec.loader.exec_module(database_real)


def _make_ctx(cur):
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=cur)
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

    @contextmanager
    def _ctx():
        yield mock_conn

    return _ctx


# ---------------------------------------------------------------------------
# Watchlist — bulk_tag_watchlist
# ---------------------------------------------------------------------------

class TestBulkTagWatchlist(unittest.TestCase):

    def test_rejects_empty_ids(self):
        with self.assertRaises(ValueError):
            watchlist_service.bulk_tag_watchlist("portfolio-1", [], ["momentum"])

    def test_rejects_batch_over_cap(self):
        with self.assertRaises(ValueError):
            watchlist_service.bulk_tag_watchlist("portfolio-1", [f"id-{i}" for i in range(101)], ["momentum"])

    def test_merges_tags_not_replace(self):
        cur = MagicMock()
        cur.fetchone.return_value = {"tags": ["existing"]}
        ctx = _make_ctx(cur)

        with patch.object(watchlist_service, "get_db", ctx):
            result = watchlist_service.bulk_tag_watchlist("portfolio-1", ["wl-1"], ["momentum"])

        self.assertEqual(result["succeeded"], ["wl-1"])
        self.assertEqual(result["failed"], [])
        update_call = [c for c in cur.execute.call_args_list if "UPDATE watchlist" in c[0][0]][0]
        merged_tags = update_call[0][1][0]
        self.assertEqual(set(merged_tags), {"existing", "momentum"})

    def test_not_found_row_reported_in_failed(self):
        cur = MagicMock()
        cur.fetchone.return_value = None
        ctx = _make_ctx(cur)

        with patch.object(watchlist_service, "get_db", ctx):
            result = watchlist_service.bulk_tag_watchlist("portfolio-1", ["missing-id"], ["momentum"])

        self.assertEqual(result["succeeded"], [])
        self.assertEqual(result["failed"], [{"id": "missing-id", "reason": "not_found"}])

    def test_invalid_tags_filtered_out(self):
        cur = MagicMock()
        cur.fetchone.return_value = {"tags": []}
        ctx = _make_ctx(cur)

        with patch.object(watchlist_service, "get_db", ctx):
            result = watchlist_service.bulk_tag_watchlist("portfolio-1", ["wl-1"], ["Invalid Tag!", "valid-tag"])

        update_call = [c for c in cur.execute.call_args_list if "UPDATE watchlist" in c[0][0]][0]
        merged_tags = update_call[0][1][0]
        self.assertEqual(merged_tags, ["valid-tag"])
        self.assertEqual(result["succeeded"], ["wl-1"])


class TestBulkDeleteWatchlist(unittest.TestCase):

    def test_rejects_empty_ids(self):
        with self.assertRaises(ValueError):
            watchlist_service.bulk_delete_watchlist("portfolio-1", [])

    def test_partial_failure_shape(self):
        cur = MagicMock()
        # First id deletes successfully, second not found
        cur.fetchone.side_effect = [{"id": "wl-1"}, None]
        ctx = _make_ctx(cur)

        with patch.object(watchlist_service, "get_db", ctx):
            result = watchlist_service.bulk_delete_watchlist("portfolio-1", ["wl-1", "wl-2"])

        self.assertEqual(result["succeeded"], ["wl-1"])
        self.assertEqual(result["failed"], [{"id": "wl-2", "reason": "not_found"}])


class TestGetAllWatchlistTags(unittest.TestCase):

    def test_returns_unique_tags(self):
        cur = MagicMock()
        cur.fetchall.return_value = [{"tag": "momentum"}, {"tag": "breakout"}]
        ctx = _make_ctx(cur)

        with patch.object(watchlist_service, "get_db", ctx):
            result = watchlist_service.get_all_watchlist_tags("portfolio-1")

        self.assertEqual(result, ["momentum", "breakout"])


# ---------------------------------------------------------------------------
# Trade Plans — bulk_tag_trade_plans
# ---------------------------------------------------------------------------

class TestBulkTagTradePlans(unittest.TestCase):

    def test_rejects_empty_ids(self):
        with self.assertRaises(ValueError):
            database_real.bulk_tag_trade_plans("portfolio-1", [], ["momentum"])

    def test_rejects_batch_over_cap(self):
        with self.assertRaises(ValueError):
            database_real.bulk_tag_trade_plans("portfolio-1", [f"id-{i}" for i in range(101)], ["momentum"])

    def test_merges_tags_not_replace(self):
        cur = MagicMock()
        cur.fetchone.return_value = {"trade_tags": ["swing"]}
        ctx = _make_ctx(cur)

        with patch.object(database_real, "get_db", ctx):
            result = database_real.bulk_tag_trade_plans("portfolio-1", ["tp-1"], ["momentum"])

        self.assertEqual(result["succeeded"], ["tp-1"])
        update_call = [c for c in cur.execute.call_args_list if "UPDATE trade_plans" in c[0][0]][0]
        merged_tags = update_call[0][1][0]
        self.assertEqual(set(merged_tags), {"swing", "momentum"})

    def test_not_found_reported_in_failed(self):
        cur = MagicMock()
        cur.fetchone.return_value = None
        ctx = _make_ctx(cur)

        with patch.object(database_real, "get_db", ctx):
            result = database_real.bulk_tag_trade_plans("portfolio-1", ["missing"], ["momentum"])

        self.assertEqual(result["failed"], [{"id": "missing", "reason": "not_found"}])


class TestBulkArchiveTradePlans(unittest.TestCase):

    def test_rejects_empty_ids(self):
        with self.assertRaises(ValueError):
            database_real.bulk_archive_trade_plans("portfolio-1", [], "reason")

    def test_active_status_excluded(self):
        cur = MagicMock()
        cur.fetchone.return_value = {"status": "active"}
        ctx = _make_ctx(cur)

        with patch.object(database_real, "get_db", ctx):
            result = database_real.bulk_archive_trade_plans("portfolio-1", ["tp-1"], "bulk reason")

        self.assertEqual(result["succeeded"], [])
        self.assertEqual(result["failed"], [{"id": "tp-1", "reason": "active_status_excluded"}])

    def test_eligible_plan_archived(self):
        cur = MagicMock()
        cur.fetchone.return_value = {"status": "draft"}
        ctx = _make_ctx(cur)

        with patch.object(database_real, "get_db", ctx):
            result = database_real.bulk_archive_trade_plans("portfolio-1", ["tp-1"], "bulk reason")

        self.assertEqual(result["succeeded"], ["tp-1"])
        update_call = [c for c in cur.execute.call_args_list if "UPDATE trade_plans" in c[0][0]][0]
        self.assertIn("abandoned", update_call[0][0])
        self.assertIn("bulk reason", update_call[0][1])

    def test_not_found_reported_in_failed(self):
        cur = MagicMock()
        cur.fetchone.return_value = None
        ctx = _make_ctx(cur)

        with patch.object(database_real, "get_db", ctx):
            result = database_real.bulk_archive_trade_plans("portfolio-1", ["missing"], "reason")

        self.assertEqual(result["failed"], [{"id": "missing", "reason": "not_found"}])

    def test_mixed_batch_partial_result(self):
        cur = MagicMock()
        cur.fetchone.side_effect = [{"status": "draft"}, {"status": "active"}, None]
        ctx = _make_ctx(cur)

        with patch.object(database_real, "get_db", ctx):
            result = database_real.bulk_archive_trade_plans("portfolio-1", ["tp-1", "tp-2", "tp-3"], "reason")

        self.assertEqual(result["succeeded"], ["tp-1"])
        self.assertEqual(result["failed"], [
            {"id": "tp-2", "reason": "active_status_excluded"},
            {"id": "tp-3", "reason": "not_found"},
        ])


class TestBulkDeleteTradePlans(unittest.TestCase):

    def test_rejects_empty_ids(self):
        with self.assertRaises(ValueError):
            database_real.bulk_delete_trade_plans("portfolio-1", [])

    def test_partial_failure_shape(self):
        cur = MagicMock()
        cur.fetchone.side_effect = [{"id": "tp-1"}, None]
        ctx = _make_ctx(cur)

        with patch.object(database_real, "get_db", ctx):
            result = database_real.bulk_delete_trade_plans("portfolio-1", ["tp-1", "tp-2"])

        self.assertEqual(result["succeeded"], ["tp-1"])
        self.assertEqual(result["failed"], [{"id": "tp-2", "reason": "not_found"}])


if __name__ == "__main__":
    unittest.main()
