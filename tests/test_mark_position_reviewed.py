"""
ST-15 (BLG-FEAT-68, EPIC-03, v7.0): Position review cadence nudge — capture side.
ST-04 (BLG-BE-61, EPIC-03, v7.1): portfolio-ownership check hardening pass.

Covers:
- ensure_last_reviewed_at_column: idempotent ALTER TABLE
- database.mark_position_reviewed: sets last_reviewed_at = NOW(), returns updated row
- database.mark_position_reviewed: returns None when position does not exist (404 upstream)
- services.position_service.mark_position_reviewed: portfolio-ownership check (AC-01) —
  routes through get_position() first, matching update_note()/update_tags(); a position
  not found in the active portfolio's position list raises ValueError (404 upstream)
  BEFORE any UPDATE is issued, closing the IDOR gap where the endpoint previously called
  database.mark_position_reviewed(position_id) directly with no ownership check at all.

Spec: docs/design/2026-07-12__release-v7.0/position-review-cadence-nudge/ux_spec.md

No live DB — mocks get_db()/cursor. Uses the private-module-import isolation
pattern (avoids the conftest.py database stub, whose function bodies are bare
MagicMocks with no real SQL-building logic to assert against).
"""

import sys
import os
import importlib.util
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import unittest
import services.position_service as position_service  # noqa: E402

_db_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'database.py')
_spec = importlib.util.spec_from_file_location('database_real_for_mark_reviewed_test', _db_path)
database = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(database)


def _make_conn_cur(fetchone_result=None):
    cur = MagicMock()
    cur.fetchone.return_value = fetchone_result
    cur_ctx = MagicMock()
    cur_ctx.__enter__ = MagicMock(return_value=cur)
    cur_ctx.__exit__ = MagicMock(return_value=False)

    conn = MagicMock()
    conn.cursor.return_value = cur_ctx
    conn.__enter__ = MagicMock(return_value=conn)
    conn.__exit__ = MagicMock(return_value=False)
    return conn, cur


class TestEnsureLastReviewedAtColumn(unittest.TestCase):

    def test_adds_column_idempotently(self):
        conn, cur = _make_conn_cur()
        with patch.object(database, 'get_db', return_value=conn):
            database.ensure_last_reviewed_at_column()
        executed = cur.execute.call_args[0][0]
        self.assertIn("ALTER TABLE positions ADD COLUMN IF NOT EXISTS last_reviewed_at", executed)
        self.assertIn("TIMESTAMP WITH TIME ZONE", executed)
        conn.commit.assert_called_once()


class TestMarkPositionReviewed(unittest.TestCase):

    def test_updates_last_reviewed_at_and_returns_row(self):
        conn, cur = _make_conn_cur({"id": "pos-1", "last_reviewed_at": "2026-07-13T10:00:00+00:00"})
        with patch.object(database, 'get_db', return_value=conn):
            result = database.mark_position_reviewed("pos-1")

        sql = cur.execute.call_args[0][0]
        params = cur.execute.call_args[0][1]
        self.assertIn("UPDATE positions SET last_reviewed_at = NOW()", sql)
        self.assertIn("WHERE id = %s", sql)
        self.assertEqual(params, ("pos-1",))
        self.assertEqual(result["id"], "pos-1")
        conn.commit.assert_called_once()

    def test_returns_none_when_position_not_found(self):
        conn, cur = _make_conn_cur(fetchone_result=None)
        with patch.object(database, 'get_db', return_value=conn):
            result = database.mark_position_reviewed("nonexistent-id")
        self.assertIsNone(result)


class TestMarkPositionReviewedOwnershipCheck(unittest.TestCase):
    """ST-04 (BLG-BE-61, v7.1, AC-01): services.position_service.mark_position_reviewed
    must perform the same portfolio-ownership check as update_note()/update_tags()."""

    def setUp(self):
        self._patches = []

    def tearDown(self):
        for p in self._patches:
            p.stop()

    def _patch(self, name, **kwargs):
        p = patch.object(position_service, name, **kwargs)
        self._patches.append(p)
        return p.start()

    def test_owned_position_is_updated(self):
        owned_position = {"id": "pos-1", "ticker": "AAPL"}
        self._patch("get_position", return_value=owned_position)
        db_mark = self._patch(
            "db_mark_position_reviewed",
            return_value={"id": "pos-1", "last_reviewed_at": "2026-07-14T10:00:00+00:00"},
        )

        result = position_service.mark_position_reviewed("pos-1")

        db_mark.assert_called_once_with("pos-1")
        self.assertEqual(result["id"], "pos-1")

    def test_position_not_in_active_portfolio_raises_before_any_update(self):
        """AC-01 — the core IDOR-fix assertion: a position_id that get_position()
        cannot resolve within the active portfolio's own position list must raise
        ValueError, and db_mark_position_reviewed (the actual UPDATE) must NEVER
        be called. Before this fix, the endpoint bypassed get_position() entirely
        and issued the UPDATE unconditionally."""
        self._patch("get_position", return_value=None)
        db_mark = self._patch("db_mark_position_reviewed")

        with self.assertRaises(ValueError):
            position_service.mark_position_reviewed("not-my-position")

        db_mark.assert_not_called()

    def test_empty_position_id_raises_before_any_lookup(self):
        get_position = self._patch("get_position")
        db_mark = self._patch("db_mark_position_reviewed")

        with self.assertRaises(ValueError):
            position_service.mark_position_reviewed("")

        get_position.assert_not_called()
        db_mark.assert_not_called()

    def test_db_layer_none_after_ownership_check_still_raises(self):
        """Defensive: even if get_position() finds the row but the row vanishes
        between the ownership check and the UPDATE (race), surface as 404, not
        a silent None returned to the caller."""
        self._patch("get_position", return_value={"id": "pos-1"})
        self._patch("db_mark_position_reviewed", return_value=None)

        with self.assertRaises(ValueError):
            position_service.mark_position_reviewed("pos-1")


if __name__ == "__main__":
    unittest.main()
