"""
ST-20 (BLG-AI-28, EPIC-05, v9.16) — non-ticker words that are also real tickers.

PM (Philip Morris), MA (Mastercard) and ON (ON Semiconductor) are scan-universe
tickers that were on the non-ticker list. AI Compliance & Governance Officer
ruling ESC-EXEC-20261110-01, option (A), with its 2026-11-10 clarification: each
(and AM, ruled with PM) is a non-ticker only in its usual non-ticker usage, and
otherwise a ticker, on both the briefing summary check and the chat focus rule.

- PM / AM: only directly after a time ("3 PM", "3:30 PM").
- MA: only directly after a number or period ("200 MA", "50-day MA"), or a
  determiner ("above the MA", "its MA").
- ON: only directly after RISK ("RISK ON").

A held collision ticker is still cited first; note text and outcomes are
unchanged. Model call mocked; no network.
"""
from datetime import datetime, timezone

import pytest

from services.ai_service import _append_missing_stop_times, _summary_ticker_caveat

_MU = {"ticker": "MU", "market": "US", "current_price": 100.0, "current_stop": 95.0, "pnl": 1.0,
       "risk_off_exit": False, "stop_calculated_at": datetime(2026, 10, 20, 21, 5, tzinfo=timezone.utc)}
_PM = {"ticker": "PM", "market": "US", "current_price": 120.0, "current_stop": 110.0, "pnl": 1.0,
       "risk_off_exit": False, "stop_calculated_at": datetime(2026, 10, 21, 21, 5, tzinfo=timezone.utc)}
MU_NOTE = "(MU stop last recalculated 2026-10-20 21:05 UTC)"
PM_NOTE = "(PM stop last recalculated 2026-10-21 21:05 UTC)"


def _chat(text, positions=(_MU,), focus="MU"):
    return _append_missing_stop_times(text, list(positions), "POST /ai/chat", "response", "v1.2",
                                      focus_ticker=focus)


class TestChatFocusRule:
    def test_pm_as_a_ticker_is_not_given_to_the_focus(self):
        # ST-20 AC 2, first sentence: focus MU held, PM not held -> no MU note.
        text = "PM's stop was hit last week."
        out, outcome = _chat(text)
        assert (out, outcome) == (text, "unattributed")
        assert "MU stop" not in out

    def test_pm_after_a_time_still_gets_the_focus_note(self):
        # ST-20 AC 2, second sentence.
        text = "Your stop was hit at 3 PM."
        assert _chat(text) == (f"{text} {MU_NOTE}", "appended")

    @pytest.mark.parametrize("text", [
        "Your stop was hit at 3:30 PM.",
        "Your stop moved at 9 AM.",
        "Your stop is above the 50-day MA.",
        "Your stop is above the 200 MA.",
        "Your stop is above its MA.",
        "Your stop held while RISK ON.",
    ])
    def test_usual_usages_still_get_the_focus_note(self, text):
        assert _chat(text) == (f"{text} {MU_NOTE}", "appended")

    @pytest.mark.parametrize("text", [
        "MA's stop was hit last week.",
        "ON's stop was hit last week.",
        "AM stop was hit.",
    ])
    def test_other_collisions_as_tickers_are_not_given_to_the_focus(self, text):
        assert _chat(text) == (text, "unattributed")

    def test_a_held_collision_ticker_is_still_cited(self):
        text = "PM's stop was hit last week."
        assert _chat(text, positions=(_MU, _PM)) == (f"{text} {PM_NOTE}", "appended")


class TestBriefingSummaryCheck:
    @pytest.mark.parametrize("summary", [
        "Review exits before 3 PM.",
        "Price is above the 50-day MA.",
        "SPY sits above its MA.",
        "Markets are RISK ON.",
        "The open is at 9:30 AM.",
    ])
    def test_usual_usages_get_no_caveat(self, summary):
        assert _summary_ticker_caveat(summary, [], "") == (None, None)

    @pytest.mark.parametrize("token,summary", [
        ("PM", "PM rallied after earnings."),
        ("MA", "MA reported strong volumes."),
        ("ON", "ON fell 4% today."),
    ])
    def test_a_collision_used_as_a_ticker_is_caveated(self, token, summary):
        assert _summary_ticker_caveat(summary, [], "") == (
            f"(Note: {token} is not one of your open positions or today's top signals.)", "appended")

    def test_a_held_or_context_collision_ticker_is_not_caveated(self):
        assert _summary_ticker_caveat("PM rallied after earnings.", ["PM"], "") == (None, None)
        assert _summary_ticker_caveat("MA reported strong volumes.", [], "Signals: MA rank 2") == (None, None)
