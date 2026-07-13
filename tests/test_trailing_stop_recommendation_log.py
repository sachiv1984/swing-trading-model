"""
ST-07 (BLG-BE-50, EPIC-02, v7.0): trailing_stop_recommendation_log capture.

Covers:
- trailing_stop_recommendation_log table created (ensure_trailing_stop_recommendation_log_table)
- log_trailing_stop_recommendation writes one row per GET /positions/{id}/stop-trail call
- fire-and-forget: DB errors never raise out of log_trailing_stop_recommendation

Spec: docs/specs/metrics_definitions.md #Trailing Stop Action Rate

No live DB — mocks get_db()/cursor. Uses the same private-module-import
isolation as test_claude_audit_log_filters.py (avoids the conftest.py
database stub, which only exposes functions found via `from database import
(...)` scans and would otherwise return bare MagicMocks with no real
SQL-building logic to assert against).
"""

import sys
import os
import importlib.util
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import unittest

_db_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'database.py')
_spec = importlib.util.spec_from_file_location('database_real_for_trailing_stop_log_test', _db_path)
database = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(database)


def _make_conn_cur():
    cur = MagicMock()
    cur_ctx = MagicMock()
    cur_ctx.__enter__ = MagicMock(return_value=cur)
    cur_ctx.__exit__ = MagicMock(return_value=False)

    conn = MagicMock()
    conn.cursor.return_value = cur_ctx
    conn.__enter__ = MagicMock(return_value=conn)
    conn.__exit__ = MagicMock(return_value=False)
    return conn, cur


class TestEnsureTrailingStopRecommendationLogTable(unittest.TestCase):

    def test_creates_table_and_indexes(self):
        conn, cur = _make_conn_cur()
        with patch.object(database, 'get_db', return_value=conn):
            database.ensure_trailing_stop_recommendation_log_table()
        executed = [c[0][0] for c in cur.execute.call_args_list]
        self.assertTrue(any("CREATE TABLE IF NOT EXISTS trailing_stop_recommendation_log" in s for s in executed))
        self.assertTrue(any("idx_tsrl_position_id" in s for s in executed))
        self.assertTrue(any("idx_tsrl_recommended_at" in s for s in executed))
        conn.commit.assert_called_once()


class TestLogTrailingStopRecommendation(unittest.TestCase):

    def test_writes_one_row_per_call(self):
        conn, cur = _make_conn_cur()
        with patch.object(database, 'get_db', return_value=conn), \
             patch.object(database, 'ensure_trailing_stop_recommendation_log_table'):
            database.log_trailing_stop_recommendation("pos-1", 100.0, 105.5)

        insert_calls = [c for c in cur.execute.call_args_list if "INSERT INTO trailing_stop_recommendation_log" in c[0][0]]
        self.assertEqual(len(insert_calls), 1)
        self.assertEqual(insert_calls[0][0][1], ("pos-1", 100.0, 105.5))
        conn.commit.assert_called_once()

    def test_null_current_stop_at_recommendation_allowed(self):
        # position with no current_stop set yet — still a valid recommendation event
        conn, cur = _make_conn_cur()
        with patch.object(database, 'get_db', return_value=conn), \
             patch.object(database, 'ensure_trailing_stop_recommendation_log_table'):
            database.log_trailing_stop_recommendation("pos-2", None, 90.0)

        insert_calls = [c for c in cur.execute.call_args_list if "INSERT INTO trailing_stop_recommendation_log" in c[0][0]]
        self.assertEqual(insert_calls[0][0][1], ("pos-2", None, 90.0))

    def test_ensures_table_before_insert(self):
        conn, cur = _make_conn_cur()
        with patch.object(database, 'get_db', return_value=conn), \
             patch.object(database, 'ensure_trailing_stop_recommendation_log_table') as ensure_mock:
            database.log_trailing_stop_recommendation("pos-3", 80.0, 85.0)
        ensure_mock.assert_called_once()

    def test_db_error_is_swallowed_fire_and_forget(self):
        with patch.object(database, 'ensure_trailing_stop_recommendation_log_table', side_effect=Exception("db down")):
            try:
                database.log_trailing_stop_recommendation("pos-4", 80.0, 85.0)
            except Exception:
                self.fail("log_trailing_stop_recommendation must not raise (fire-and-forget)")


if __name__ == "__main__":
    unittest.main()
