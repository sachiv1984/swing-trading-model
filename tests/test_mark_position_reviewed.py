"""
ST-15 (BLG-FEAT-68, EPIC-03, v7.0): Position review cadence nudge — capture side.

Covers:
- ensure_last_reviewed_at_column: idempotent ALTER TABLE
- mark_position_reviewed: sets last_reviewed_at = NOW(), returns updated row
- mark_position_reviewed: returns None when position does not exist (404 upstream)

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


if __name__ == "__main__":
    unittest.main()
