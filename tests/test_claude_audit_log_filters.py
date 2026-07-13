"""
ST-11 (BLG-BE-51, EPIC-02, v7.0): endpoint + date-range filters for
GET /ai/claude-audit-log (database.query_claude_audit_log).

Covers:
- endpoint filter applied alone (AC-01)
- date_from/date_to filters applied alone and combined with endpoint (AC-02)
- existing unfiltered behaviour unchanged when no filters given (AC-03)

No live DB — mocks get_db()/cursor consistent with existing test suite patterns
(tests/test_ai_audit_service.py).
"""

import sys
import os
import importlib.util
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import unittest

# conftest.py replaces sys.modules["database"] (session-wide, process-global)
# with an auto-derived stub whose function bodies are bare MagicMocks — see
# tests/conftest.py. query_claude_audit_log's own SQL-building logic under
# test lives in the real database.py. Loading a private, independent copy of
# the real module via importlib (rather than sys.modules.pop()/reimport, which
# mutates the shared sys.modules["database"] entry and is fragile to full-suite
# execution order) means this file never touches sys.modules["database"] and
# cannot be affected by, or interfere with, other test files' use of the stub.
_db_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'database.py')
_spec = importlib.util.spec_from_file_location('database_real_for_claude_audit_log_test', _db_path)
database = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(database)


def _make_conn_cur(rows=None):
    cur = MagicMock()
    cur.fetchall.return_value = rows or []
    cur_ctx = MagicMock()
    cur_ctx.__enter__ = MagicMock(return_value=cur)
    cur_ctx.__exit__ = MagicMock(return_value=False)

    conn = MagicMock()
    conn.cursor.return_value = cur_ctx
    conn.__enter__ = MagicMock(return_value=conn)
    conn.__exit__ = MagicMock(return_value=False)
    return conn, cur


class TestQueryClaudeAuditLogFilters(unittest.TestCase):

    def setUp(self):
        self.ensure_patcher = patch.object(database, 'ensure_claude_audit_log_table')
        self.ensure_patcher.start()
        self.addCleanup(self.ensure_patcher.stop)

    def test_no_filters_unfiltered_behaviour_unchanged(self):
        conn, cur = _make_conn_cur([])
        with patch.object(database, 'get_db', return_value=conn):
            database.query_claude_audit_log(limit=50)
        sql = cur.execute.call_args[0][0]
        params = cur.execute.call_args[0][1]
        self.assertNotIn("WHERE", sql)
        self.assertEqual(params, (50,))

    def test_endpoint_filter_applied_alone(self):
        conn, cur = _make_conn_cur([])
        with patch.object(database, 'get_db', return_value=conn):
            database.query_claude_audit_log(limit=50, endpoint="POST /ai/daily-briefing")
        sql = cur.execute.call_args[0][0]
        params = cur.execute.call_args[0][1]
        self.assertIn("endpoint = %s", sql)
        self.assertNotIn("generated_at >=", sql)
        self.assertEqual(params, ("POST /ai/daily-briefing", 50))

    def test_date_from_and_date_to_applied_alone(self):
        conn, cur = _make_conn_cur([])
        with patch.object(database, 'get_db', return_value=conn):
            database.query_claude_audit_log(limit=50, date_from="2026-07-01", date_to="2026-07-13")
        sql = cur.execute.call_args[0][0]
        params = cur.execute.call_args[0][1]
        self.assertIn("generated_at >= %s", sql)
        self.assertIn("generated_at < (%s::date + INTERVAL '1 day')", sql)
        self.assertNotIn("endpoint = %s", sql)
        self.assertEqual(params, ("2026-07-01", "2026-07-13", 50))

    def test_endpoint_and_date_range_combined(self):
        conn, cur = _make_conn_cur([])
        with patch.object(database, 'get_db', return_value=conn):
            database.query_claude_audit_log(
                limit=25,
                endpoint="POST /ai/daily-briefing",
                date_from="2026-07-01",
                date_to="2026-07-13",
            )
        sql = cur.execute.call_args[0][0]
        params = cur.execute.call_args[0][1]
        self.assertIn("endpoint = %s", sql)
        self.assertIn("generated_at >= %s", sql)
        self.assertIn("generated_at < (%s::date + INTERVAL '1 day')", sql)
        self.assertIn(" AND ", sql)
        self.assertEqual(params, ("POST /ai/daily-briefing", "2026-07-01", "2026-07-13", 25))

    def test_date_to_only_still_scopes_full_day(self):
        conn, cur = _make_conn_cur([])
        with patch.object(database, 'get_db', return_value=conn):
            database.query_claude_audit_log(limit=50, date_to="2026-07-13")
        sql = cur.execute.call_args[0][0]
        params = cur.execute.call_args[0][1]
        self.assertIn("generated_at < (%s::date + INTERVAL '1 day')", sql)
        self.assertNotIn("generated_at >= %s", sql)
        self.assertEqual(params, ("2026-07-13", 50))

    def test_returns_rows_shaped_as_before(self):
        row = {
            "id": "abc-123",
            "endpoint": "POST /ai/daily-briefing",
            "model_id": "claude-haiku-4-5",
            "prompt_version": "v3.0",
            "input_tokens": 100,
            "output_tokens": 50,
            "cost_usd": 0.001,
            "generated_at": MagicMock(isoformat=lambda: "2026-07-13T10:00:00+00:00"),
        }
        conn, cur = _make_conn_cur([row])
        with patch.object(database, 'get_db', return_value=conn):
            result = database.query_claude_audit_log(limit=50, endpoint="POST /ai/daily-briefing")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["endpoint"], "POST /ai/daily-briefing")
        self.assertEqual(result[0]["cost_usd"], 0.001)


if __name__ == "__main__":
    unittest.main()
