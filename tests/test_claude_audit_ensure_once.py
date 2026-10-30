"""
ST-21 (BLG-BE-166, EPIC-03, v9.14): create_claude_audit_entry() ran four
ensure_* DDL calls (CREATE TABLE / ALTER TABLE ... ADD COLUMN IF NOT EXISTS)
before every insert. Each opens a connection and takes an ACCESS EXCLUSIVE
lock even when it changes nothing. The insert paths' ensure_* functions now
run once per process (database.ensure_once).

Loads a private copy of the real database.py, for the same reason as
tests/test_claude_audit_entry_failure_logging.py (conftest stubs
sys.modules["database"]).
"""
import importlib.util
import os
import sys
import threading
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

_db_path = os.path.join(os.path.dirname(__file__), "..", "backend", "database.py")
_spec = importlib.util.spec_from_file_location("database_real_for_st21_test", _db_path)
database = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(database)


def _fake_db():
    """A get_db() stand-in that records every SQL statement executed."""
    executed = []
    cur = MagicMock()
    cur.execute.side_effect = lambda sql, *a: executed.append(" ".join(sql.split()))
    cur.fetchone.return_value = {"id": "00000000-0000-0000-0000-000000000001"}
    cur_ctx = MagicMock(__enter__=MagicMock(return_value=cur), __exit__=MagicMock(return_value=False))
    conn = MagicMock(__exit__=MagicMock(return_value=False))
    conn.__enter__ = MagicMock(return_value=conn)
    conn.cursor.return_value = cur_ctx
    return conn, executed


def _insert():
    return database.create_claude_audit_entry(
        endpoint="POST /ai/chat", model_id="claude-test", prompt_version="v1.0",
        input_tokens=10, output_tokens=20, cost_usd=0.0001, latency_ms=5,
    )


def _ddl(statements):
    return [s for s in statements if s.upper().startswith(("CREATE", "ALTER"))]


@pytest.fixture(autouse=True)
def _fresh_process():
    database.reset_ensure_once()
    yield
    database.reset_ensure_once()


def test_first_insert_adds_missing_columns():
    conn, executed = _fake_db()
    with patch.object(database, "get_db", return_value=conn):
        assert _insert() == "00000000-0000-0000-0000-000000000001"
    ddl = _ddl(executed)
    assert any(s.startswith("CREATE TABLE IF NOT EXISTS claude_audit_log") for s in ddl)
    for column in ("compliance_check_result", "latency_ms", "prompt_hash", "response_length"):
        assert any(f"ADD COLUMN IF NOT EXISTS {column}" in s for s in ddl), column
    assert executed[-1].startswith("INSERT INTO claude_audit_log")


def test_second_insert_in_the_same_process_runs_no_ddl():
    conn, executed = _fake_db()
    with patch.object(database, "get_db", return_value=conn):
        _insert()
        executed.clear()
        _insert()
    assert _ddl(executed) == []
    assert len(executed) == 1 and executed[0].startswith("INSERT INTO claude_audit_log")


def test_failed_ensure_is_retried_on_the_next_insert():
    conn, executed = _fake_db()
    with patch.object(database, "get_db", side_effect=RuntimeError("db down")):
        assert _insert() is None  # non-blocking, as before
    with patch.object(database, "get_db", return_value=conn):
        _insert()
    assert any(s.startswith("CREATE TABLE IF NOT EXISTS claude_audit_log") for s in _ddl(executed))


def test_reset_makes_the_next_call_run_again():
    conn, executed = _fake_db()
    with patch.object(database, "get_db", return_value=conn):
        database.ensure_gemini_audit_log_table()
        database.ensure_gemini_audit_log_table()
        assert len(_ddl(executed)) >= 1
        n = len(executed)
        database.reset_ensure_once()
        database.ensure_gemini_audit_log_table()
    assert len(executed) > n


def test_nested_decorated_ensure_does_not_deadlock():
    # DoQ review finding 1: ensure_chat_answer_ratings_table (decorated)
    # calls the decorated claude_audit_log ensures. With a non-reentrant
    # lock the inner call waited on the outer and the thread hung.
    conn, executed = _fake_db()
    with patch.object(database, "get_db", return_value=conn):
        t = threading.Thread(target=database.ensure_chat_answer_ratings_table, daemon=True)
        t.start()
        t.join(5)
    assert not t.is_alive(), "ensure_chat_answer_ratings_table deadlocked"
    assert any("claude_audit_log" in s for s in _ddl(executed))
