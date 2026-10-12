"""
ST-03 (BLG-BE-151, EPIC-01, v9.11) — the AI-output sampling hook must never
break or hide an AI response.

Before this story every AI endpoint imported
`services.ai_output_sampling_service` inside the same `try` block that
returns the endpoint's fallback message, so an import failure (the PR #1921
defect, v9.4-v9.10) replaced a good generated response with the generic
"unavailable" text, with nothing logged. Each AI endpoint now calls
`utils.ai_sampling.sample_ai_output`, which guards the import and the call.

For each of the six AI features this runs the endpoint three times with the
model call mocked: sampling working, sampling failing at import, and
sampling raising inside the hook. The response must be identical each time.
It also checks that the daily briefing and chat log their fallback with
`exc_info`.
"""
import json
import logging
import sys
from unittest.mock import MagicMock, patch

import pytest

from utils.ai_sampling import sample_ai_output

_SAMPLING_MODULE = "services.ai_output_sampling_service"


@pytest.fixture(autouse=True)
def _ensure_db_stub(database_stub):
    # Same reason as test_ai_chat_schema.py: ai_service imports from database
    # inside its function bodies, so re-register the conftest stub per test.
    sys.modules["database"] = database_stub
    database_stub.get_portfolio.return_value = {"id": "p-001", "cash": 5000, "initial_cash": 10000}
    database_stub.get_positions.return_value = []
    database_stub.get_signals.return_value = []
    database_stub.create_claude_audit_entry.return_value = None
    yield


def _anthropic_response(text):
    block = MagicMock()
    block.text = text
    resp = MagicMock()
    resp.content = [block]
    resp.usage = MagicMock(input_tokens=10, output_tokens=5)
    return resp


class _HookRaises:
    """Sampling module whose hook raises."""
    @staticmethod
    def maybe_sample_output(*a, **k):
        raise RuntimeError("sampling store exploded")


def _run_three_ways(call):
    """Run `call` with sampling working, failing at import, and raising."""
    working = MagicMock()
    working.maybe_sample_output.return_value = True
    with patch.dict(sys.modules, {_SAMPLING_MODULE: working}):
        ok = call()
    # A None entry in sys.modules makes `import` raise ImportError.
    with patch.dict(sys.modules, {_SAMPLING_MODULE: None}):
        import_fail = call()
    with patch.dict(sys.modules, {_SAMPLING_MODULE: _HookRaises}):
        hook_fail = call()
    return ok, import_fail, hook_fail


def _strip_time(result):
    r = dict(result)
    r.pop("generated_at", None)
    return r


class TestSampleAiOutputHelper:
    def test_import_failure_is_swallowed_and_logged(self, caplog):
        with patch.dict(sys.modules, {_SAMPLING_MODULE: None}), caplog.at_level(logging.WARNING):
            assert sample_ai_output("feature", "text", "model") is False
        assert any(r.exc_info for r in caplog.records)

    def test_hook_exception_is_swallowed_and_logged(self, caplog):
        with patch.dict(sys.modules, {_SAMPLING_MODULE: _HookRaises}), caplog.at_level(logging.WARNING):
            assert sample_ai_output("feature", "text", "model") is False
        assert any(r.exc_info for r in caplog.records)


class TestEachAiEndpointUnchangedBySamplingFailure:
    def test_journal_summary(self):
        from services import ai_service
        with patch.object(ai_service, "_create_message", return_value=_anthropic_response("Summary text.")), \
             patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
            ok, imp, hook = _run_three_ways(lambda: ai_service.summarise_journal_notes(["note one"]))
        assert ok["summary"] == "Summary text."
        assert ok == imp == hook

    def test_daily_briefing(self):
        from services import ai_service
        body = json.dumps({"summary": "All quiet.", "actions": []})
        with patch.object(ai_service, "_create_message", return_value=_anthropic_response(body)), \
             patch.object(ai_service, "_get_regime_data", return_value=None), \
             patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
            ok, imp, hook = _run_three_ways(ai_service.generate_daily_briefing)
        assert ok["summary"] == "All quiet." and "error" not in ok
        assert _strip_time(ok) == _strip_time(imp) == _strip_time(hook)

    def test_chat(self):
        from services import ai_service
        with patch.object(ai_service, "_create_message", return_value=_anthropic_response("You hold nothing.")), \
             patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
            ok, imp, hook = _run_three_ways(lambda: ai_service.ai_chat("What do I hold?"))
        assert ok["response"] == "You hold nothing."
        assert ok == imp == hook

    def test_generate_plan(self):
        from services import gemini_service
        fields = {"setup_thesis": "Thesis.", "entry_rationale": "Why.", "early_exit_conditions": "When."}
        with patch.object(gemini_service, "ANTHROPIC_API_KEY", "k"), \
             patch.object(gemini_service, "_call_claude", return_value=(json.dumps(fields), MagicMock())), \
             patch.object(gemini_service, "_log_audit"):
            ok, imp, hook = _run_three_ways(lambda: gemini_service.generate_full_plan("AAPL"))
        assert ok["available"] is True and ok["fields"] == fields
        assert ok == imp == hook

    def test_generate_thesis(self):
        from services import gemini_service
        with patch.object(gemini_service, "ANTHROPIC_API_KEY", "k"), \
             patch.object(gemini_service, "_call_claude", return_value=("A thesis.", MagicMock())), \
             patch.object(gemini_service, "_log_audit"):
            ok, imp, hook = _run_three_ways(lambda: gemini_service.generate_setup_thesis("AAPL"))
        assert ok["thesis"] == "A thesis."
        assert ok == imp == hook

    def test_post_trade_debrief(self):
        from services import debrief_service
        trade = {"id": "t1", "portfolio_id": "pf", "position_id": None, "ticker": "AAPL",
                 "entry_price": 100.0, "exit_price": 108.5, "pnl": 8.5, "pnl_pct": 8.5,
                 "exit_reason": "Target Reached", "holding_days": 12}
        persisted = []

        def fake_create(trade_id, portfolio_id, data):
            persisted.append(dict(data))
            return dict(data, generated_at=None)

        with patch.object(debrief_service, "ANTHROPIC_API_KEY", "k"), \
             patch.object(debrief_service, "get_trade_by_id", return_value=trade), \
             patch.object(debrief_service, "get_red_flag_events", return_value={"items": []}), \
             patch.object(debrief_service, "create_claude_audit_entry"), \
             patch.object(debrief_service, "create_trade_debrief", side_effect=fake_create), \
             patch.object(debrief_service, "_call_claude",
                          return_value=("Your exit at 108.5 matched your plan.", MagicMock(input_tokens=1, output_tokens=1))):
            ok, imp, hook = _run_three_ways(lambda: debrief_service.generate_trade_debrief("t1"))
        assert ok["focus_area_text"] == "Your exit at 108.5 matched your plan."
        assert ok == imp == hook
        assert persisted[0] == persisted[1] == persisted[2]


class TestFallbackPathsLogWithExcInfo:
    def test_daily_briefing_logs_exception_on_fallback(self, caplog):
        from services import ai_service
        with patch.object(ai_service, "_create_message", side_effect=RuntimeError("upstream down")), \
             patch.object(ai_service, "_get_regime_data", return_value=None), \
             patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}), caplog.at_level(logging.ERROR):
            result = ai_service.generate_daily_briefing()
        assert result["error"] == "AI briefing temporarily unavailable. Please try again."
        assert any(r.exc_info and "upstream down" in str(r.exc_info[1]) for r in caplog.records)

    def test_chat_logs_exception_on_fallback(self, caplog):
        from services import ai_service
        with patch.object(ai_service, "_create_message", side_effect=RuntimeError("upstream down")), \
             patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}), caplog.at_level(logging.ERROR):
            result = ai_service.ai_chat("Hello?")
        assert result["response"] == "Unable to get a response. Please try again."
        assert any(r.exc_info and "upstream down" in str(r.exc_info[1]) for r in caplog.records)
