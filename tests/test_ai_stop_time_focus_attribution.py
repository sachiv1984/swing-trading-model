"""
ST-16 (BLG-AI-18), EPIC-03, v9.13 — the stop-time check attributes a chat
stop citation to the focused ticker, and case-normalises action tickers.

AI Compliance & Governance Officer ruling ESC-EXEC-20261027-01 (B), extending
ESC-EXEC-20261013-01: ai_chat() passes context.ticker as the focus ticker. A
stop sentence that names no held ticker is attributed to the focus ticker,
only when that ticker is an open position; a sentence naming a held ticker is
attributed only to the tickers it names. The warning line carries
attribution=focus. compliance_check_result values are unchanged. Model call
mocked.
"""
import logging
import sys
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from services.ai_service import _append_missing_stop_times

_POSITIONS = [
    {"ticker": "NVDA", "market": "US", "current_price": 470.0, "current_stop": 450.0,
     "pnl": 40.0, "risk_off_exit": False,
     "stop_calculated_at": datetime(2026, 10, 12, 21, 5, tzinfo=timezone.utc)},
    {"ticker": "VOD.L", "market": "UK", "current_price": 70.0, "current_stop": 66.0,
     "pnl": 5.0, "risk_off_exit": False, "stop_calculated_at": None},
]
NVDA_NOTE = "(NVDA stop last recalculated 2026-10-12 21:05 UTC)"
VOD_NOTE = "(VOD.L stop not recalculated since entry)"


def _check(text, focus=None, own=None, endpoint="POST /ai/chat"):
    return _append_missing_stop_times(text, _POSITIONS, endpoint, "response", "v1.2",
                                      own_ticker=own, focus_ticker=focus)


class TestFocusAttribution:
    def test_focused_reply_without_ticker_gets_note(self, caplog):
        text = "Your stop is at £450."
        with caplog.at_level(logging.WARNING):
            assert _check(text, focus="NVDA") == (f"{text} {NVDA_NOTE}", "appended")
        assert any("ticker=NVDA action=appended prompt_version=v1.2 attribution=focus" in r.getMessage()
                   for r in caplog.records)

    def test_without_focus_still_unattributed(self):
        text = "Your stop is at £450."
        assert _check(text) == (text, "unattributed")

    def test_focus_not_held_stays_unattributed(self):
        text = "Your stop is at £450."
        assert _check(text, focus="AAPL") == (text, "unattributed")

    def test_sentence_naming_another_holding_not_given_to_focus(self, caplog):
        text = "VOD.L is below its stop."
        with caplog.at_level(logging.WARNING):
            assert _check(text, focus="NVDA") == (f"{text} {VOD_NOTE}", "appended")
        assert not any("attribution=focus" in r.getMessage() for r in caplog.records)

    def test_focus_suffix_folded(self):
        text = "Your stop has not moved."
        assert _check(text, focus="VOD") == (f"{text} {VOD_NOTE}", "appended")

    def test_focused_reply_with_time_passes(self):
        text = "Your stop, last recalculated 2026-10-12, is at £450."
        assert _check(text, focus="NVDA") == (text, None)


class TestActionTickerCase:
    def test_lower_case_held_action_ticker_gets_note(self):
        text = "Price is through the stop."
        out = _append_missing_stop_times(text, _POSITIONS, "POST /ai/daily-briefing",
                                         "actions[0].description", "v1.3", own_ticker="nvda")
        assert out == (f"{text} {NVDA_NOTE}", "appended")

    def test_action_focus_rule_not_applied(self):
        # Briefing actions keep their own_ticker behaviour only (ruling condition 4).
        text = "VOD.L is below its stop."
        out = _append_missing_stop_times(text, _POSITIONS, "POST /ai/daily-briefing",
                                         "actions[0].description", "v1.3", own_ticker="NVDA")
        assert out[1] == "appended" and NVDA_NOTE in out[0] and VOD_NOTE in out[0]


@pytest.fixture
def db(database_stub):
    sys.modules["database"] = database_stub
    database_stub.get_portfolio.return_value = {"id": "p-001", "cash": 5000, "initial_cash": 10000}
    database_stub.get_positions.return_value = [dict(p) for p in _POSITIONS]
    database_stub.get_signals.return_value = []
    database_stub.create_claude_audit_entry.reset_mock()
    return database_stub


def _chat(question, context, text):
    from services import ai_service
    resp = MagicMock()
    resp.content = [MagicMock(text=text)]
    resp.usage = MagicMock(input_tokens=1, output_tokens=1)
    with patch.object(ai_service, "_create_message", return_value=resp), \
         patch.object(ai_service, "sample_ai_output") as sample, \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
        return ai_service.ai_chat(question, context), sample


def test_chat_focused_on_position_gets_note_and_raw_text_sampled(db):
    raw = "Your stop is at £450."
    result, sample = _chat("Where is my stop?", {"ticker": "NVDA"}, raw)
    assert result["response"] == f"{raw} {NVDA_NOTE}"
    assert sample.call_args.args[1] == raw
    assert db.create_claude_audit_entry.call_args.kwargs["compliance_check_result"] == "stop_time_missing_appended"


def test_chat_without_context_unchanged(db):
    raw = "Your stop is at £450."
    result, _ = _chat("Where is my stop?", None, raw)
    assert result["response"] == raw
    assert db.create_claude_audit_entry.call_args.kwargs["compliance_check_result"] == "stop_time_missing_unattributed"
