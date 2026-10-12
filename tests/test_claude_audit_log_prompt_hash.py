"""
ST-06 (BLG-AI-08, EPIC-01, v9.11) — claude_audit_log records prompt_hash and
response_length, and a failed model call writes an audit row marked
'model_call_failed' (DS-27).
"""
import hashlib
import json
import sys
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def db(database_stub):
    sys.modules["database"] = database_stub
    database_stub.get_portfolio.return_value = {"id": "p-001", "cash": 5000, "initial_cash": 10000}
    database_stub.get_positions.return_value = []
    database_stub.get_signals.return_value = []
    database_stub.create_claude_audit_entry.reset_mock()
    database_stub.create_claude_audit_entry.side_effect = None
    return database_stub


def _resp(text):
    r = MagicMock()
    r.content = [MagicMock(text=text)]
    r.usage = MagicMock(input_tokens=10, output_tokens=5)
    return r


def _run(func, *args, text=None, fail=False):
    from services import ai_service
    captured = {}

    def fake_create(api_key, **kw):
        captured.update(kw)
        if fail:
            raise RuntimeError("model unavailable after retries")
        return _resp(text)

    with patch.object(ai_service, "_create_message", side_effect=fake_create), \
         patch.object(ai_service, "_get_regime_data", return_value=None), \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
        result = getattr(ai_service, func)(*args)
    return result, captured


def _expected_hash(captured):
    user = captured["messages"][0]["content"]
    return hashlib.sha256(f"{captured['system']}\n{user}".encode()).hexdigest()[:16]


class TestSuccessfulCallsWriteHashAndLength:
    def test_daily_briefing(self, db):
        body = json.dumps({"summary": "All quiet.", "actions": []})
        _, sent = _run("generate_daily_briefing", text=body)
        kw = db.create_claude_audit_entry.call_args.kwargs
        assert kw["endpoint"] == "POST /ai/daily-briefing"
        assert kw["prompt_hash"] == _expected_hash(sent) and len(kw["prompt_hash"]) == 16
        assert kw["response_length"] == len(body)
        assert kw.get("compliance_check_result") is None

    def test_chat(self, db):
        _, sent = _run("ai_chat", "What do I hold?", text="You hold nothing.")
        kw = db.create_claude_audit_entry.call_args.kwargs
        assert kw["endpoint"] == "POST /ai/chat"
        assert kw["prompt_hash"] == _expected_hash(sent)
        assert kw["response_length"] == len("You hold nothing.")

    def test_hash_differs_when_the_user_message_differs(self, db):
        _, a = _run("ai_chat", "Question A", text="x")
        h1 = db.create_claude_audit_entry.call_args.kwargs["prompt_hash"]
        _, b = _run("ai_chat", "Question B", text="x")
        assert db.create_claude_audit_entry.call_args.kwargs["prompt_hash"] != h1


class TestFailedModelCallWritesFailedRow:
    def test_daily_briefing(self, db):
        result, sent = _run("generate_daily_briefing", fail=True)
        assert result["error"]
        kw = db.create_claude_audit_entry.call_args.kwargs
        assert kw["compliance_check_result"] == "model_call_failed"
        assert kw["endpoint"] == "POST /ai/daily-briefing"
        assert kw["prompt_hash"] == _expected_hash(sent)
        assert "input_tokens" not in kw or kw["input_tokens"] is None

    def test_chat(self, db):
        result, _ = _run("ai_chat", "Hello?", fail=True)
        assert result["response"] == "Unable to get a response. Please try again."
        assert db.create_claude_audit_entry.call_args.kwargs["compliance_check_result"] == "model_call_failed"

    def test_failed_audit_write_does_not_change_the_fallback(self, db):
        db.create_claude_audit_entry.side_effect = RuntimeError("audit store down")
        result, _ = _run("ai_chat", "Hello?", fail=True)
        assert result["response"] == "Unable to get a response. Please try again."

    def test_debrief(self):
        from services import debrief_service
        trade = {"id": "t1", "portfolio_id": "pf", "position_id": None, "ticker": "AAPL",
                 "entry_price": 100.0, "exit_price": 108.5, "pnl": 8.5, "pnl_pct": 8.5,
                 "exit_reason": "Target Reached", "holding_days": 12}
        with patch.object(debrief_service, "ANTHROPIC_API_KEY", "k"), \
             patch.object(debrief_service, "get_trade_by_id", return_value=trade), \
             patch.object(debrief_service, "get_red_flag_events", return_value={"items": []}), \
             patch.object(debrief_service, "create_trade_debrief", side_effect=lambda t, p, d: dict(d, generated_at=None)), \
             patch.object(debrief_service, "create_claude_audit_entry") as audit, \
             patch.object(debrief_service, "_call_claude", side_effect=RuntimeError("down")):
            result = debrief_service.generate_trade_debrief("t1")
        assert result["generation_status"] == "ai_unavailable"
        assert audit.call_count == 1
        assert audit.call_args.kwargs["compliance_check_result"] == "model_call_failed"
        assert len(audit.call_args.kwargs["prompt_hash"]) == 16


def test_insert_names_both_columns():
    """The writer's INSERT and its ensure_* migration both carry the columns."""
    from pathlib import Path
    src = (Path(__file__).resolve().parent.parent / "backend" / "database.py").read_text()
    start = src.index("def create_claude_audit_entry(")
    body = src[start:src.index("\ndef ", start + 10)]
    assert "prompt_hash, response_length" in body
    assert "ADD COLUMN IF NOT EXISTS prompt_hash VARCHAR(16)" in src
    assert "ADD COLUMN IF NOT EXISTS response_length INTEGER" in src
