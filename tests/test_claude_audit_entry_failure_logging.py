"""
ST-16 (BLG-GOV-141, EPIC-04, v9.10): database.create_claude_audit_entry() must
stay non-blocking when the insert fails, but must no longer fail silently.

The v9.9 AI feature usage review (docs/ops/ai_feature_usage_review_2026-09-24.md)
found the function swallowed every insert error with `except Exception: pass`,
so a dropped audit row left no trace. It now logs a warning naming the
endpoint and model.

Loads a private copy of the real database.py, for the same reason as
tests/test_claude_audit_log_filters.py (conftest stubs sys.modules["database"]).
"""
import importlib.util
import logging
import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

_db_path = os.path.join(os.path.dirname(__file__), "..", "backend", "database.py")
_spec = importlib.util.spec_from_file_location("database_real_for_st16_test", _db_path)
database = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(database)


def _ensure_patches():
    return (
        patch.object(database, "ensure_claude_audit_log_table"),
        patch.object(database, "ensure_claude_audit_log_compliance_check_column"),
        patch.object(database, "ensure_claude_audit_log_latency_column"),
    )


def _call():
    database.create_claude_audit_entry(
        endpoint="POST /ai/chat", model_id="claude-test", prompt_version="v1.0",
        input_tokens=10, output_tokens=20, cost_usd=0.0001, latency_ms=5,
    )


def test_insert_failure_is_logged_not_raised(caplog):
    a, b, c = _ensure_patches()
    with a, b, c, patch.object(database, "get_db", side_effect=RuntimeError("db down")):
        with caplog.at_level(logging.WARNING, logger=database.logger.name):
            _call()  # must not raise
    messages = [r.getMessage() for r in caplog.records]
    assert any("claude_audit_log insert failed for POST /ai/chat" in m and "db down" in m for m in messages)


def test_successful_insert_logs_nothing(caplog):
    cur = MagicMock()
    cur_ctx = MagicMock(__enter__=MagicMock(return_value=cur), __exit__=MagicMock(return_value=False))
    conn = MagicMock(__enter__=MagicMock(), __exit__=MagicMock(return_value=False))
    conn.__enter__.return_value = conn
    conn.cursor.return_value = cur_ctx
    a, b, c = _ensure_patches()
    with a, b, c, patch.object(database, "get_db", return_value=conn):
        with caplog.at_level(logging.WARNING, logger=database.logger.name):
            _call()
    assert cur.execute.called
    assert not [r for r in caplog.records if "claude_audit_log" in r.getMessage()]
