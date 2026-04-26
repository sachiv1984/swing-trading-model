"""
Tests for ai_audit_service.py (ST-10 / TEST-GAP-ST14).

Covers ensure_ai_audit_table, log_ai_summary_run, query_audit_log.
No live DB — uses mocks consistent with existing test suite patterns.
"""

import sys
import os
from unittest.mock import MagicMock, patch
from datetime import date
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

_PATCH_TARGET = 'services.ai_audit_service.get_db'


def _make_conn_cur():
    """Return (conn, cur) mock pair for with-get_db()-as-conn / with-conn.cursor()-as-cur."""
    cur = MagicMock()
    cur_ctx = MagicMock()
    cur_ctx.__enter__ = MagicMock(return_value=cur)
    cur_ctx.__exit__ = MagicMock(return_value=False)

    conn = MagicMock()
    conn.cursor.return_value = cur_ctx
    conn.__enter__ = MagicMock(return_value=conn)
    conn.__exit__ = MagicMock(return_value=False)
    return conn, cur


# ---------------------------------------------------------------------------
# ensure_ai_audit_table
# ---------------------------------------------------------------------------

class TestEnsureAiAuditTable:

    def test_idempotent_does_not_raise_on_second_call(self):
        conn, cur = _make_conn_cur()
        with patch(_PATCH_TARGET, return_value=conn):
            from services.ai_audit_service import ensure_ai_audit_table
            ensure_ai_audit_table()
            ensure_ai_audit_table()
        assert conn.commit.call_count == 2

    def test_creates_table_index_and_duration_column(self):
        conn, cur = _make_conn_cur()
        with patch(_PATCH_TARGET, return_value=conn):
            from services.ai_audit_service import ensure_ai_audit_table
            ensure_ai_audit_table()
        executed = " ".join(str(c) for c in cur.execute.call_args_list)
        assert "ai_audit_log" in executed
        assert "idx_ai_audit_invoked" in executed
        assert "duration_ms" in executed

    def test_commits_after_ddl(self):
        conn, cur = _make_conn_cur()
        with patch(_PATCH_TARGET, return_value=conn):
            from services.ai_audit_service import ensure_ai_audit_table
            ensure_ai_audit_table()
        conn.commit.assert_called_once()


# ---------------------------------------------------------------------------
# log_ai_summary_run
# ---------------------------------------------------------------------------

class TestLogAiSummaryRun:

    def test_happy_path_inserts_row(self):
        conn, cur = _make_conn_cur()
        with patch(_PATCH_TARGET, return_value=conn):
            from services.ai_audit_service import log_ai_summary_run
            run_id = log_ai_summary_run(
                trade_ids=[1, 2, 3],
                date_from=None,
                date_to=None,
                trade_count=3,
                model_version="claude-haiku-4-5-20251001",
                summary_text="Test summary",
                duration_ms=500,
            )
        assert run_id is not None
        cur.execute.assert_called_once()
        insert_sql = cur.execute.call_args[0][0]
        assert "INSERT INTO ai_audit_log" in insert_sql

    def test_summary_produced_false_when_text_none(self):
        conn, cur = _make_conn_cur()
        with patch(_PATCH_TARGET, return_value=conn):
            from services.ai_audit_service import log_ai_summary_run
            log_ai_summary_run(
                trade_ids=None,
                date_from=date(2024, 1, 1),
                date_to=date(2024, 1, 31),
                trade_count=0,
                model_version=None,
                summary_text=None,
            )
        params = cur.execute.call_args[0][1]
        # summary_produced is the 9th param (index 8)
        assert params[8] is False

    def test_output_hash_none_when_text_none(self):
        conn, cur = _make_conn_cur()
        with patch(_PATCH_TARGET, return_value=conn):
            from services.ai_audit_service import log_ai_summary_run
            log_ai_summary_run(None, None, None, 0, None, None)
        params = cur.execute.call_args[0][1]
        assert params[7] is None  # output_hash

    def test_db_error_propagates(self):
        conn, cur = _make_conn_cur()
        cur.execute.side_effect = Exception("DB write error")
        with patch(_PATCH_TARGET, return_value=conn):
            from services.ai_audit_service import log_ai_summary_run
            with pytest.raises(Exception, match="DB write error"):
                log_ai_summary_run(None, None, None, 0, None, "text")

    def test_duration_ms_passed_as_last_parameter(self):
        conn, cur = _make_conn_cur()
        with patch(_PATCH_TARGET, return_value=conn):
            from services.ai_audit_service import log_ai_summary_run
            log_ai_summary_run(None, None, None, 0, None, "t", duration_ms=1234)
        params = cur.execute.call_args[0][1]
        assert params[-1] == 1234


# ---------------------------------------------------------------------------
# query_audit_log
# ---------------------------------------------------------------------------

class TestQueryAuditLog:

    def _make_conn_with_rows(self, rows):
        conn, cur = _make_conn_cur()
        cur.fetchall.return_value = rows
        return conn, cur

    def test_filter_by_trade_id(self):
        conn, cur = self._make_conn_with_rows([])
        with patch(_PATCH_TARGET, return_value=conn):
            from services.ai_audit_service import query_audit_log
            query_audit_log(trade_id=42)
        sql = cur.execute.call_args[0][0]
        assert "ANY(trade_ids)" in sql

    def test_filter_by_date_range(self):
        conn, cur = self._make_conn_with_rows([])
        with patch(_PATCH_TARGET, return_value=conn):
            from services.ai_audit_service import query_audit_log
            query_audit_log(date_from=date(2024, 1, 1), date_to=date(2024, 1, 31))
        sql = cur.execute.call_args[0][0]
        assert "invoked_at >=" in sql
        assert "invoked_at <=" in sql

    def test_limit_parameter_applied(self):
        conn, cur = self._make_conn_with_rows([])
        with patch(_PATCH_TARGET, return_value=conn):
            from services.ai_audit_service import query_audit_log
            query_audit_log(limit=10)
        params = cur.execute.call_args[0][1]
        assert 10 in params

    def test_empty_result_returns_empty_list(self):
        conn, cur = self._make_conn_with_rows([])
        with patch(_PATCH_TARGET, return_value=conn):
            from services.ai_audit_service import query_audit_log
            result = query_audit_log()
        assert result == []
