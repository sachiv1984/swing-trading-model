"""
ST-17 (BLG-AI-16), EPIC-03, v9.13 — the daily briefing summary is checked for
tickers outside the context.

AI Compliance & Governance Officer ruling ESC-EXEC-20261027-02 (B): a
ticker-like token in the raw summary that is not an open position or a
context signal (ST-15 normalised), does not appear in the context sent to the
model, and is not a known non-ticker word gets a code-written caveat after the
model's text and any stop-time notes. Each hit is logged (token only) and
counted in claude_audit_log.compliance_check_result alongside the stop-time
result. The check fails open; the sampling hook gets the raw output. Model
call mocked.
"""
import json
import logging
import sys
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from services.ai_service import (
    _NON_TICKER_WORDS,
    _summary_ticker_caveat,
    _with_ticker_result,
)

_POSITIONS = [
    {"ticker": "NVDA", "market": "US", "current_price": 470.0, "current_stop": 450.0, "pnl_pct": 4.0,
     "holding_days": 14, "risk_off_exit": False,
     "stop_calculated_at": datetime(2026, 10, 12, 21, 5, tzinfo=timezone.utc)},
    {"ticker": "VOD.L", "market": "UK", "current_price": 70.0, "current_stop": 66.0, "pnl_pct": 1.0,
     "holding_days": 30, "risk_off_exit": False, "stop_calculated_at": None},
]
_SIGNALS = [{"ticker": "AAPL", "market": "US", "rank": 1, "momentum_percent": 9.5,
             "signal_date": "2026-10-26", "status": "new"}]
_CONTEXT = "Market regime: Risk-On\n  SPY: 500.00 vs MA200 450.00\n  FTSE: 8000.00 vs MA200 7800.00"
_TICKERS = ["NVDA", "VOD.L", "AAPL"]


class TestDetection:
    def test_unknown_ticker_caught(self):
        assert _summary_ticker_caveat("Consider NEW_SIGNAL today.", _TICKERS, _CONTEXT) == (
            "(Note: NEW_SIGNAL is not one of your open positions or today's top signals.)", "appended")

    def test_several_unknown_tickers_in_first_appearance_order_once_each(self):
        caveat, outcome = _summary_ticker_caveat("TSLA rallied; MSFT too. TSLA again.", _TICKERS, _CONTEXT)
        assert outcome == "appended"
        assert caveat == "(Note: TSLA, MSFT are not among your open positions or today's top signals.)"

    def test_context_tickers_pass_unchanged(self):
        text = "NVDA and VOD are held; AAPL leads today's signals. SPY is above its MA200 and FTSE is Risk-On."
        assert _summary_ticker_caveat(text, _TICKERS, _CONTEXT) == (None, None)

    def test_suffixed_and_bare_forms_are_known(self):
        assert _summary_ticker_caveat("VOD.L and NVDA are open.", ["VOD", "NVDA"], "") == (None, None)

    @pytest.mark.parametrize("word", sorted(_NON_TICKER_WORDS))
    def test_non_ticker_words_ignored(self, word):
        assert _summary_ticker_caveat(f"The {word} line is noted.", [], "") == (None, None)

    def test_mixed_case_and_single_letters_not_tokens(self):
        assert _summary_ticker_caveat("I hold A position; P&L is up and Risk-On holds.", [], "") == (None, None)

    def test_word_in_context_is_known(self):
        assert _summary_ticker_caveat("MA200 is rising.", [], _CONTEXT) == (None, None)

    def test_fails_open(self, caplog):
        with patch("services.ai_service._TICKER_TOKEN_RE") as bad, caplog.at_level(logging.ERROR):
            bad.finditer.side_effect = RuntimeError("boom")
            assert _summary_ticker_caveat("NEW_SIGNAL", _TICKERS, _CONTEXT) == (None, "error")


@pytest.mark.parametrize("stop, outcome, expected", [
    ("pass", None, "pass"),
    ("pass", "appended", "ticker_outside_context_appended"),
    ("stop_time_missing_appended", "appended", "stop_time_missing_appended+ticker_outside_context_appended"),
    ("stop_time_missing_unattributed", "appended",
     "stop_time_missing_unattributed+ticker_outside_context_appended"),
    ("pass", "error", "pass+ticker_check_error"),
    ("stop_time_missing_appended", None, "stop_time_missing_appended"),
])
def test_compliance_result_combination(stop, outcome, expected):
    assert _with_ticker_result(stop, outcome) == expected


@pytest.fixture
def db(database_stub):
    sys.modules["database"] = database_stub
    database_stub.get_portfolio.return_value = {"id": "p-001", "cash": 5000, "initial_cash": 10000}
    database_stub.get_positions.return_value = [dict(p) for p in _POSITIONS]
    database_stub.get_signals.return_value = [dict(s) for s in _SIGNALS]
    database_stub.create_claude_audit_entry.reset_mock()
    return database_stub


def _brief(summary):
    from services import ai_service
    body = json.dumps({"summary": summary, "actions": []})
    resp = MagicMock()
    resp.content = [MagicMock(text=body)]
    resp.usage = MagicMock(input_tokens=1, output_tokens=1)
    with patch.object(ai_service, "_create_message", return_value=resp), \
         patch.object(ai_service, "_get_regime_data", return_value=None), \
         patch.object(ai_service, "sample_ai_output") as sample, \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
        result = ai_service.generate_daily_briefing()
    return result, sample, body


def _audit(db):
    return db.create_claude_audit_entry.call_args.kwargs["compliance_check_result"]


def test_briefing_unknown_ticker_gets_caveat_logged_and_counted(db, caplog):
    raw = "NEW_SIGNAL shows strong momentum."
    with caplog.at_level(logging.WARNING):
        result, sample, body = _brief(raw)
    assert result["summary"] == f"{raw} (Note: NEW_SIGNAL is not one of your open positions or today's top signals.)"
    assert sample.call_args.args[1] == body
    assert _audit(db) == "ticker_outside_context_appended"
    msgs = [r.getMessage() for r in caplog.records]
    assert any("ticker=NEW_SIGNAL action=caveat_appended" in m for m in msgs)
    assert not any("strong momentum" in m for m in msgs)


def test_briefing_caveat_follows_stop_time_note(db):
    raw = "NVDA is near its stop; TSLA is rising."
    result, _, _ = _brief(raw)
    assert result["summary"] == (f"{raw} (NVDA stop last recalculated 2026-10-12 21:05 UTC) "
                                 "(Note: TSLA is not one of your open positions or today's top signals.)")
    assert _audit(db) == "stop_time_missing_appended+ticker_outside_context_appended"


def test_briefing_context_only_summary_unchanged(db):
    raw = "NVDA and VOD.L are open; AAPL leads the signals."
    result, _, _ = _brief(raw)
    assert result["summary"] == raw
    assert _audit(db) == "pass"
