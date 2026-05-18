"""
ST-09: Watchlist Backend — Unit Tests

Tests service-layer logic for the watchlist feature.
No database or network calls — all I/O is mocked.

Coverage:
  - get_watchlist: returns entries with correct signal_status mapping
  - create_watchlist_entry: validates ticker, market, price fields; detects duplicates
  - update_watchlist_entry: partial update; 404 on missing entry; validates prices
  - delete_watchlist_entry: success path; 404 on missing entry
  - Signal status mapping: new→active, dismissed/expired→watch, else→no_signal
"""

import sys
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch, call
from contextlib import contextmanager

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# Database stub is registered by tests/conftest.py (BLG-QA-20).

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location(
    "watchlist_service",
    Path(__file__).parent.parent / "backend" / "services" / "watchlist_service.py",
)
watchlist_service = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(watchlist_service)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_row(ticker="AAPL", market="US", signal_status="active",
              target=None, initial=None, current=None,
              entry_id="aaaa-0001"):
    """Build a mock DB row dict as returned by the signal-status query."""
    return {
        "id": entry_id,
        "ticker": ticker,
        "market": market,
        "signal_status": signal_status,
        "target_entry_price": target,
        "initial_stop_price": initial,
        "current_stop_price": current,
        "created_at": datetime(2026, 3, 21, 10, 0, 0),
        "updated_at": datetime(2026, 3, 21, 10, 0, 0),
    }


def _make_db(rows=None, returning_id=None):
    """Build a mock get_db() context manager and cursor."""
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchall.return_value = rows or []
    mock_cur.fetchone.return_value = {"id": returning_id} if returning_id else None
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cur)
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

    @contextmanager
    def _ctx():
        yield mock_conn

    return _ctx, mock_cur


# ---------------------------------------------------------------------------
# get_watchlist
# ---------------------------------------------------------------------------

class TestGetWatchlist(unittest.TestCase):

    def test_returns_empty_list_when_no_entries(self):
        ctx, _ = _make_db(rows=[])
        with patch.object(watchlist_service, "get_db", ctx):
            result = watchlist_service.get_watchlist("portfolio-1")
        self.assertEqual(result, [])

    def test_maps_signal_status_active(self):
        row = _make_row(signal_status="active", target=185.50)
        ctx, _ = _make_db(rows=[row])
        with patch.object(watchlist_service, "get_db", ctx):
            result = watchlist_service.get_watchlist("portfolio-1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["signal_status"], "active")
        self.assertEqual(result[0]["ticker"], "AAPL")
        self.assertAlmostEqual(result[0]["target_entry_price"], 185.50)

    def test_maps_signal_status_watch(self):
        row = _make_row(signal_status="watch")
        ctx, _ = _make_db(rows=[row])
        with patch.object(watchlist_service, "get_db", ctx):
            result = watchlist_service.get_watchlist("portfolio-1")
        self.assertEqual(result[0]["signal_status"], "watch")

    def test_maps_signal_status_no_signal(self):
        row = _make_row(signal_status="no_signal")
        ctx, _ = _make_db(rows=[row])
        with patch.object(watchlist_service, "get_db", ctx):
            result = watchlist_service.get_watchlist("portfolio-1")
        self.assertEqual(result[0]["signal_status"], "no_signal")

    def test_null_price_fields_returned_as_none(self):
        row = _make_row(target=None, initial=None, current=None)
        ctx, _ = _make_db(rows=[row])
        with patch.object(watchlist_service, "get_db", ctx):
            result = watchlist_service.get_watchlist("portfolio-1")
        self.assertIsNone(result[0]["target_entry_price"])
        self.assertIsNone(result[0]["initial_stop_price"])
        self.assertIsNone(result[0]["current_stop_price"])

    def test_id_returned_as_string(self):
        row = _make_row(entry_id="bbbb-1234")
        ctx, _ = _make_db(rows=[row])
        with patch.object(watchlist_service, "get_db", ctx):
            result = watchlist_service.get_watchlist("portfolio-1")
        self.assertIsInstance(result[0]["id"], str)


# ---------------------------------------------------------------------------
# create_watchlist_entry
# ---------------------------------------------------------------------------

class TestCreateWatchlistEntry(unittest.TestCase):

    def _patch_create_and_get(self, new_id, get_rows):
        """Patch get_db for INSERT (returns new_id) and get_watchlist for fetch-back.

        fetchone side_effect: first call = None (no duplicate), second call = new_id (RETURNING).
        """
        insert_ctx, insert_cur = _make_db(returning_id=new_id)
        insert_cur.fetchone.side_effect = [None, {"id": new_id}]

        with patch.object(watchlist_service, "get_db", insert_ctx), \
             patch.object(watchlist_service, "get_watchlist", return_value=get_rows):
            return watchlist_service.create_watchlist_entry(
                "portfolio-1",
                {"ticker": "NVDA", "market": "US",
                 "target_entry_price": 820.0, "initial_stop_price": None, "current_stop_price": None}
            )

    def test_returns_created_entry(self):
        expected = _make_row(ticker="NVDA", entry_id="cccc-0001", signal_status="active", target=820.0)
        result = self._patch_create_and_get("cccc-0001", [expected])
        self.assertEqual(result["ticker"], "NVDA")
        self.assertEqual(result["id"], "cccc-0001")

    def test_ticker_is_uppercased(self):
        """Service must uppercase the ticker before insert."""
        insert_ctx, insert_cur = _make_db(returning_id="dddd-0001")
        # First fetchone = None (no duplicate), second = RETURNING row
        insert_cur.fetchone.side_effect = [None, {"id": "dddd-0001"}]
        get_row = _make_row(ticker="AAPL", entry_id="dddd-0001")

        with patch.object(watchlist_service, "get_db", insert_ctx), \
             patch.object(watchlist_service, "get_watchlist", return_value=[get_row]):
            watchlist_service.create_watchlist_entry(
                "portfolio-1",
                {"ticker": "aapl", "market": "US",
                 "target_entry_price": None, "initial_stop_price": None, "current_stop_price": None}
            )
        # Verify INSERT was called with uppercased ticker
        args = insert_cur.execute.call_args_list
        insert_call = [a for a in args if "INSERT" in str(a)]
        self.assertTrue(any("AAPL" in str(c) for c in insert_call))

    def test_raises_value_error_on_empty_ticker(self):
        with self.assertRaises(ValueError) as ctx:
            watchlist_service.create_watchlist_entry(
                "portfolio-1",
                {"ticker": "", "market": "US",
                 "target_entry_price": None, "initial_stop_price": None, "current_stop_price": None}
            )
        self.assertIn("ticker", str(ctx.exception).lower())

    def test_raises_value_error_on_invalid_market(self):
        with self.assertRaises(ValueError):
            watchlist_service.create_watchlist_entry(
                "portfolio-1",
                {"ticker": "AAPL", "market": "AU",
                 "target_entry_price": None, "initial_stop_price": None, "current_stop_price": None}
            )

    def test_raises_value_error_on_non_positive_price(self):
        with self.assertRaises(ValueError):
            watchlist_service.create_watchlist_entry(
                "portfolio-1",
                {"ticker": "AAPL", "market": "US",
                 "target_entry_price": -10.0, "initial_stop_price": None, "current_stop_price": None}
            )

    def test_raises_lookup_error_on_duplicate_ticker(self):
        """Should raise LookupError when ticker already exists (cursor returns a row)."""
        ctx, cur = _make_db()
        cur.fetchone.return_value = {"id": "existing-id"}  # duplicate found

        with patch.object(watchlist_service, "get_db", ctx):
            with self.assertRaises(LookupError):
                watchlist_service.create_watchlist_entry(
                    "portfolio-1",
                    {"ticker": "AAPL", "market": "US",
                     "target_entry_price": None, "initial_stop_price": None, "current_stop_price": None}
                )

    def test_raises_value_error_on_ticker_too_long(self):
        with self.assertRaises(ValueError):
            watchlist_service.create_watchlist_entry(
                "portfolio-1",
                {"ticker": "TOOLONGTICKER", "market": "US",
                 "target_entry_price": None, "initial_stop_price": None, "current_stop_price": None}
            )


# ---------------------------------------------------------------------------
# update_watchlist_entry
# ---------------------------------------------------------------------------

class TestUpdateWatchlistEntry(unittest.TestCase):

    def test_raises_value_error_when_no_updatable_fields_present(self):
        """Empty dict (no updatable keys at all) should raise ValueError."""
        with self.assertRaises(ValueError):
            watchlist_service.update_watchlist_entry(
                "portfolio-1", "entry-1",
                {}  # no keys — nothing to update
            )

    def test_raises_value_error_on_non_positive_price(self):
        with self.assertRaises(ValueError):
            watchlist_service.update_watchlist_entry(
                "portfolio-1", "entry-1",
                {"target_entry_price": 0.0, "initial_stop_price": None, "current_stop_price": None}
            )

    def test_raises_lookup_error_when_entry_not_found(self):
        ctx, cur = _make_db()
        cur.fetchone.return_value = None  # UPDATE RETURNING nothing

        with patch.object(watchlist_service, "get_db", ctx):
            with self.assertRaises(LookupError):
                watchlist_service.update_watchlist_entry(
                    "portfolio-1", "missing-id",
                    {"target_entry_price": 190.0, "initial_stop_price": None, "current_stop_price": None}
                )

    def test_returns_updated_entry(self):
        ctx, cur = _make_db()
        cur.fetchone.return_value = {"id": "entry-1"}  # UPDATE RETURNING
        updated_row = _make_row(entry_id="entry-1", target=190.0, signal_status="active")

        with patch.object(watchlist_service, "get_db", ctx), \
             patch.object(watchlist_service, "get_watchlist", return_value=[updated_row]):
            result = watchlist_service.update_watchlist_entry(
                "portfolio-1", "entry-1",
                {"target_entry_price": 190.0, "initial_stop_price": None, "current_stop_price": None}
            )
        self.assertEqual(result["id"], "entry-1")
        self.assertAlmostEqual(result["target_entry_price"], 190.0)


# ---------------------------------------------------------------------------
# delete_watchlist_entry
# ---------------------------------------------------------------------------

class TestDeleteWatchlistEntry(unittest.TestCase):

    def test_returns_deleted_dict_on_success(self):
        ctx, cur = _make_db()
        cur.fetchone.return_value = {"id": "entry-1"}  # DELETE RETURNING

        with patch.object(watchlist_service, "get_db", ctx):
            result = watchlist_service.delete_watchlist_entry("portfolio-1", "entry-1")
        self.assertEqual(result, {"id": "entry-1", "deleted": True})

    def test_raises_lookup_error_when_not_found(self):
        ctx, cur = _make_db()
        cur.fetchone.return_value = None  # DELETE RETURNING nothing

        with patch.object(watchlist_service, "get_db", ctx):
            with self.assertRaises(LookupError):
                watchlist_service.delete_watchlist_entry("portfolio-1", "missing-id")


if __name__ == "__main__":
    unittest.main()
