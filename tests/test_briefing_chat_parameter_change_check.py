"""
ST-39 (BLG-AI-29), EPIC-07, v9.18 — the daily briefing and chat are checked
against strategy_rules.md §13.2.

§13.2: AI-written text describing the user's data, naming the daily briefing
and chat, must not suggest changing stops, position sizing, setups or any
other strategy parameter. The BLG-FEAT-50/51 §13 review (§13.5 row,
decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md)
cleared both features without an output-side check; this adds one.

AI Compliance & Governance Officer ruling ESC-EXEC-20261120-01 (2026-11-20):
(1)(a) only the trading_change category (the journal summary's
_trading_change_found) applies, so a recommendation under the existing rules
(EXIT/ENTER/MONITOR/HOLD) passes and action type and ticker are never
checked; (2)(A) a failing first output is regenerated once; a failing second
output has each failing field replaced by code-written text (chat: a fixed
withheld message with no answer_id). One claude_audit_log row per model call.
Model call mocked.
"""
import json
import logging
import sys
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from services.ai_service import (
    BRIEFING_ACTION_WITHHELD,
    BRIEFING_SUMMARY_WITHHELD,
    CHAT_WITHHELD_MESSAGE,
    _with_regenerate_result,
    parameter_change_failures,
)

_POSITIONS = [
    {"ticker": "NVDA", "market": "US", "current_price": 470.0, "current_stop": 450.0, "pnl_pct": 4.0,
     "pnl": 120.0, "holding_days": 14, "risk_off_exit": False,
     "stop_calculated_at": datetime(2026, 10, 12, 21, 5, tzinfo=timezone.utc)},
    {"ticker": "VOD.L", "market": "UK", "current_price": 70.0, "current_stop": 66.0, "pnl_pct": 1.0,
     "pnl": 5.0, "holding_days": 30, "risk_off_exit": False,
     "stop_calculated_at": datetime(2026, 10, 12, 21, 5, tzinfo=timezone.utc)},
]
_SIGNALS = [{"ticker": "AAPL", "market": "US", "rank": 1, "momentum_percent": 9.5,
             "signal_date": "2026-10-26", "status": "new"}]

ADVICE = "Consider tightening your stop on NVDA to lock in gains."
TIME = "last recalculated 2026-10-12 21:05 UTC"
EXIT_TEXT = f"NVDA closed below its trailing stop of £450.00 ({TIME}); the exit rule applies."
HOLD_TEXT = f"VOD.L is holding above its stop of £66.00 ({TIME})."


# ─── The check itself ─────────────────────────────────────────────────────

@pytest.mark.parametrize("text", [
    ADVICE,
    "Tighten the stop on NVDA to £460.",
    "Reduce your position size in AAPL.",
    "It may be worth raising your stop on VOD.L.",
    "NVDA's stop could be moved up to lock in gains.",
])
def test_parameter_change_wording_fails(text):
    assert parameter_change_failures(text) == ["trading_change"]


@pytest.mark.parametrize("text", [
    # Deterministic actions under the existing rules (ruling (1)(a)).
    EXIT_TEXT,
    "Stop breach on NVDA; exit is recommended under your rules.",
    "You should exit NVDA because it breached its stop.",
    HOLD_TEXT,
    "MONITOR VOD.L: price is within 3% of its stop.",
    "ENTER AAPL: rank 1 signal with 9.5% momentum; size per your normal risk rule.",
    "The trailing stop on NVDA was raised to £450 last night.",
    None,
    "",
])
def test_rule_based_and_descriptive_wording_passes(text):
    assert parameter_change_failures(text) == []


@pytest.mark.parametrize("result, attempt, fallback, expected", [
    ("pass", 1, None, "pass"),
    ("stop_time_missing_appended", 1, None, "stop_time_missing_appended"),
    ("pass", 2, None, "pass_on_regenerate"),
    ("ticker_outside_context_appended", 2, None, "pass_on_regenerate+ticker_outside_context_appended"),
    ("pass", 2, "trading_change", "fail_fallback:trading_change"),
    ("stop_time_missing_appended", 2, "trading_change",
     "fail_fallback:trading_change+stop_time_missing_appended"),
    (None, 1, None, "pass"),
])
def test_result_combination(result, attempt, fallback, expected):
    assert _with_regenerate_result(result, attempt, fallback) == expected


# ─── Endpoint behaviour ───────────────────────────────────────────────────

@pytest.fixture
def db(database_stub):
    sys.modules["database"] = database_stub
    database_stub.get_portfolio.return_value = {"id": "p-001", "cash": 5000, "initial_cash": 10000}
    database_stub.get_positions.return_value = [dict(p) for p in _POSITIONS]
    database_stub.get_signals.return_value = [dict(s) for s in _SIGNALS]
    database_stub.create_claude_audit_entry.reset_mock()
    database_stub.create_claude_audit_entry.side_effect = [f"row-{i}" for i in range(1, 10)]
    yield database_stub
    database_stub.create_claude_audit_entry.side_effect = None


def _resp(text):
    resp = MagicMock()
    resp.content = [MagicMock(text=text)]
    resp.usage = MagicMock(input_tokens=10, output_tokens=10)
    return resp


def _body(summary, actions=()):
    return json.dumps({"summary": summary, "actions": list(actions)})


def _run(fn, *args, outputs):
    from services import ai_service
    with patch.object(ai_service, "_create_message", side_effect=[_resp(o) for o in outputs]) as create, \
         patch.object(ai_service, "_get_regime_data", return_value=None), \
         patch.object(ai_service, "sample_ai_output") as sample, \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
        result = getattr(ai_service, fn)(*args)
    return result, create, sample


def _results(db):
    return [c.kwargs["compliance_check_result"] for c in db.create_claude_audit_entry.call_args_list]


class TestBriefing:
    def test_advice_in_summary_regenerates_once_and_second_output_is_shown(self, db, caplog):
        first = _body(ADVICE, [{"type": "HOLD", "ticker": "VOD.L", "description": HOLD_TEXT}])
        second = _body(f"NVDA is up 4% and above its stop ({TIME}).",
                       [{"type": "HOLD", "ticker": "VOD.L", "description": HOLD_TEXT}])
        with caplog.at_level(logging.WARNING, logger="services.ai_service"):
            result, create, sample = _run("generate_daily_briefing", outputs=[first, second])
        assert create.call_count == 2
        assert result["summary"] == f"NVDA is up 4% and above its stop ({TIME})."
        assert _results(db) == ["fail_regenerate:trading_change", "pass_on_regenerate"]
        # Each attempt's raw output reaches the sampling hook; logs carry no model text.
        assert [c.args[1] for c in sample.call_args_list] == [first, second]
        msgs = [r.getMessage() for r in caplog.records]
        assert any("attempt 1, fields=summary, categories=trading_change, prompt_version=v1.4" in m for m in msgs)
        assert not any("lock in gains" in m for m in msgs)

    def test_second_failure_withholds_summary_only(self, db):
        actions = [{"type": "HOLD", "ticker": "VOD.L", "description": HOLD_TEXT}]
        result, create, _ = _run("generate_daily_briefing", outputs=[_body(ADVICE, actions)] * 2)
        assert create.call_count == 2
        assert result["summary"] == BRIEFING_SUMMARY_WITHHELD
        assert result["actions"] == actions
        assert _results(db) == ["fail_regenerate:trading_change", "fail_fallback:trading_change"]

    def test_second_failure_in_exit_action_keeps_type_and_ticker(self, db):
        summary = f"NVDA has breached its stop ({TIME})."
        actions = [{"type": "EXIT", "ticker": "NVDA",
                    "description": "Exit NVDA, and consider tightening stops on the rest."},
                   {"type": "HOLD", "ticker": "VOD.L", "description": HOLD_TEXT}]
        result, _, _ = _run("generate_daily_briefing", outputs=[_body(summary, actions)] * 2)
        assert result["summary"] == summary
        assert result["actions"][0] == {"type": "EXIT", "ticker": "NVDA", "description": BRIEFING_ACTION_WITHHELD}
        assert result["actions"][1] == actions[1]
        assert _results(db)[-1] == "fail_fallback:trading_change"

    def test_fallback_result_keeps_stop_time_result(self, db):
        actions = [{"type": "MONITOR", "ticker": "NVDA", "description": "NVDA is close to its stop."}]
        result, _, _ = _run("generate_daily_briefing", outputs=[_body(ADVICE, actions)] * 2)
        assert result["actions"][0]["description"].startswith("NVDA is close to its stop. (NVDA stop")
        assert _results(db)[-1] == "fail_fallback:trading_change+stop_time_missing_appended"

    def test_deterministic_exit_and_hold_actions_pass_first_time(self, db):
        actions = [{"type": "EXIT", "ticker": "NVDA", "description": EXIT_TEXT},
                   {"type": "HOLD", "ticker": "VOD.L", "description": HOLD_TEXT}]
        summary = f"One position breached its stop ({TIME} for NVDA); the exit rule applies."
        result, create, _ = _run("generate_daily_briefing", outputs=[_body(summary, actions)])
        assert create.call_count == 1
        assert result["summary"] == summary
        assert result["actions"] == actions
        assert _results(db) == ["pass"]


class TestChat:
    def test_advice_regenerates_once_and_answer_id_is_the_shown_answer(self, db):
        answer = f"NVDA's stop is £450.00 ({TIME}), about 4% below the price."
        result, create, sample = _run("ai_chat", "Should I tighten my stop?", outputs=[ADVICE, answer])
        assert create.call_count == 2
        assert result["response"] == answer
        assert result["answer_id"] == "row-2"
        assert _results(db) == ["fail_regenerate:trading_change", "pass_on_regenerate"]
        assert [c.args[1] for c in sample.call_args_list] == [ADVICE, answer]

    def test_second_failure_returns_withheld_message_without_answer_id(self, db):
        result, create, _ = _run("ai_chat", "Should I tighten my stop?", outputs=[ADVICE, ADVICE])
        assert create.call_count == 2
        assert result["response"] == CHAT_WITHHELD_MESSAGE
        assert result["advisory"] is True
        assert "answer_id" not in result
        assert _results(db) == ["fail_regenerate:trading_change", "fail_fallback:trading_change"]

    def test_rule_based_answer_passes_first_time(self, db):
        answer = "You should exit NVDA because it breached its stop, " + TIME + "."
        result, create, _ = _run("ai_chat", "What now?", outputs=[answer])
        assert create.call_count == 1
        assert result["response"] == answer
        assert result["answer_id"] == "row-1"
        assert _results(db) == ["pass"]


# ─── Code review fixes (ST-39, before commit) ─────────────────────────────

@pytest.mark.parametrize("text", [
    "Your stop should not be moved; the strategy's rules set it.",
    "Your stop shouldn't be moved.",
    "I cannot suggest whether stops should be tightened; that is your decision.",
    "The stop should stay where it is; it does not need to be tightened.",
    "There is no need to adjust your stop.",
    "I can't say whether your stop should be tightened.",
    "I can't say whether your stop should be tightened, but the exit rule applies to NVDA.",
    "I can't advise if stops should be tightened.",
    "I cannot suggest whether your stop or position size should be changed, as the rules set them.",
    "MU is near its stop but the stop has not moved since Monday.",
    "Stops should never be loosened under the strategy's rules.",
    "The position size should not be reduced, and the stop should not be moved.",
    "Your stop and position size do not need to be changed.",
])
def test_negated_or_declined_change_passes(text):
    assert parameter_change_failures(text) == []


@pytest.mark.parametrize("text", [
    "Your stop is fine. Consider tightening the stop on AAPL though.",
    "I would not move the stop; however, consider tightening stops on the rest.",
])
def test_advice_beside_a_negated_clause_still_fails(text):
    assert parameter_change_failures(text) == ["trading_change"]


class TestRegenerationFailure:
    def test_briefing_keeps_first_output_with_fallback_when_regeneration_raises(self, db):
        from services import ai_service
        actions = [{"type": "EXIT", "ticker": "NVDA", "description": EXIT_TEXT}]
        first = _resp(_body(ADVICE, actions))
        with patch.object(ai_service, "_create_message", side_effect=[first, RuntimeError("529")]), \
             patch.object(ai_service, "_get_regime_data", return_value=None), \
             patch.object(ai_service, "sample_ai_output"), \
             patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
            result = ai_service.generate_daily_briefing()
        assert "error" not in result
        assert result["summary"] == BRIEFING_SUMMARY_WITHHELD
        assert result["actions"] == actions
        assert _results(db) == ["fail_regenerate:trading_change", "fail_fallback:model_call_failed"]

    def test_briefing_keeps_first_output_with_fallback_when_regeneration_unparseable(self, db):
        actions = [{"type": "HOLD", "ticker": "VOD.L", "description": HOLD_TEXT}]
        result, _, _ = _run("generate_daily_briefing", outputs=[_body(ADVICE, actions), "not json"])
        assert result["summary"] == BRIEFING_SUMMARY_WITHHELD
        assert result["actions"] == actions
        assert _results(db) == ["fail_regenerate:trading_change", "fail_fallback:trading_change"]

    def test_chat_returns_withheld_message_when_regeneration_raises(self, db):
        from services import ai_service
        with patch.object(ai_service, "_create_message", side_effect=[_resp(ADVICE), RuntimeError("529")]), \
             patch.object(ai_service, "sample_ai_output"), \
             patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
            result = ai_service.ai_chat("Should I tighten my stop?")
        assert result["response"] == CHAT_WITHHELD_MESSAGE
        assert "answer_id" not in result
        assert _results(db) == ["fail_regenerate:trading_change", "fail_fallback:model_call_failed"]

    def test_briefing_null_actions_with_failing_summary_does_not_error(self, db):
        result, _, _ = _run("generate_daily_briefing",
                            outputs=[json.dumps({"summary": ADVICE, "actions": None})] * 2)
        assert result["summary"] == BRIEFING_SUMMARY_WITHHELD
        assert result["actions"] == []


def test_rating_queries_exclude_withheld_chat_rows():
    import inspect
    from tests._real_database import load_real_database
    real_db = load_real_database("_st39_real_database")
    for fn in (real_db.create_chat_answer_rating, real_db.get_response_acceptance_rate):
        assert "NOT LIKE 'fail\\\\_%%'" in inspect.getsource(fn)


# ─── Exemption logging (ruling ESC-EXEC-20261120-01 confirmation, 2026-11-20) ─

def test_exempted_sentence_is_logged_without_model_text(caplog):
    text = "Your stop should not be moved; the strategy's rules set it."
    with caplog.at_level(logging.WARNING, logger="services.ai_service"):
        assert parameter_change_failures(text, "POST /ai/chat", "response") == []
    msgs = [r.getMessage() for r in caplog.records]
    assert msgs == ["§13.2 check: endpoint=POST /ai/chat field=response action=negation_exempt"]


def test_failing_and_plain_sentences_log_no_exemption(caplog):
    with caplog.at_level(logging.WARNING, logger="services.ai_service"):
        parameter_change_failures(ADVICE, "POST /ai/chat", "response")
        parameter_change_failures(HOLD_TEXT, "POST /ai/chat", "response")
    assert not any("negation_exempt" in r.getMessage() for r in caplog.records)


def test_briefing_exemption_logged_with_field(db, caplog):
    actions = [{"type": "HOLD", "ticker": "VOD.L",
                "description": f"VOD.L's stop should not be moved ({TIME})."}]
    with caplog.at_level(logging.WARNING, logger="services.ai_service"):
        result, create, _ = _run("generate_daily_briefing", outputs=[_body(HOLD_TEXT, actions)])
    assert create.call_count == 1
    assert result["actions"] == actions
    assert any("endpoint=POST /ai/daily-briefing field=actions[0].description action=negation_exempt"
               in r.getMessage() for r in caplog.records)


# ─── PR review (Director of Quality and Product Owner finding 1, 2026-11-20) ─
# The exemption covers only the negated phrase or a declined suggestion; any
# advice elsewhere in the sentence still fails.

@pytest.mark.parametrize("text", [
    "Consider tightening stops since NVDA has not moved.",
    "Consider tightening your stop on NVDA, and do not widen it.",
    "Your stop should be raised, not lowered.",
    "There's no need to wait: consider tightening your stop on NVDA.",
    "If the stop is not moved, consider reducing your position size.",
    "I don't say this lightly, but consider tightening your stop.",
    "I can't recommend strongly enough that you consider tightening your stop.",
    "Consider tightening your stop on NVDA before earnings, which are not reviewed here.",
    "I can't recommend changes to your strategy, but your stop on NVDA could be tightened.",
    "I cannot advise on trades, but you should consider tightening your stop on NVDA.",
    "While I don't recommend acting hastily, reducing position size would be prudent.",
    "There is no need to exit yet, though your stop should be raised to lock in gains.",
    "No need to panic, but consider tightening your stop.",
    "I can't say for sure, but your stop should be tightened.",
    # Round 2 (Product Owner): advice after a declined suggestion and a contrast.
    "I can't say whether NVDA will recover, but your stop should be tightened.",
    "I won't recommend that you sell, but consider tightening your stop.",
    "I cannot say that the trend is over, but tightening stops could help.",
    "I can't say whether it rebounds \u2014 consider tightening your stop.",
    # Round 2 (Director of Quality R1).
    "I can't say whether NVDA will rise, but consider tightening your stop.",
    "I can't say that enough: consider tightening your stop on NVDA.",
    "I won't suggest that the trend is over, but you might consider reducing your position size.",
])
def test_advice_beside_a_negation_or_disclaimer_fails(text, caplog):
    with caplog.at_level(logging.WARNING, logger="services.ai_service"):
        assert parameter_change_failures(text, "POST /ai/chat", "response") == ["trading_change"]
    assert not any("negation_exempt" in r.getMessage() for r in caplog.records)
