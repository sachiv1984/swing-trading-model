"""
ST-15 (BLG-AI-17), EPIC-03, v9.13 — the briefing ticker filter and the
stop-time check treat a UK `.L` ticker and its bare form as one instrument.

ST-02's filter matched tickers exactly (case-insensitive), so an EXIT or
MONITOR action for a held `VOD.L` written as `VOD` was silently dropped.
Both sides are now normalised (upper case, trailing `.L` removed), as the
trade-plan lookup in database.py already does. The stop-time check's ticker
attribution uses the same normalisation. Model call mocked.
"""
import json
import sys
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from services.ai_service import (
    _append_missing_stop_times,
    _filter_actions_to_context,
    _normalise_ticker,
)

_STOP_TIME = datetime(2026, 10, 20, 21, 5, tzinfo=timezone.utc)


def _position(ticker, market="UK"):
    return {"ticker": ticker, "market": market, "current_price": 100.0, "current_stop": 95.0,
            "pnl_pct": 1.0, "pnl": 10.0, "holding_days": 20, "risk_off_exit": False,
            "stop_calculated_at": _STOP_TIME}


@pytest.mark.parametrize("raw, expected", [
    ("VOD.L", "VOD"), ("vod.l", "VOD"), (" VOD ", "VOD"), ("VOD", "VOD"),
    ("AAPL", "AAPL"), ("", None), (None, None), (42, None),
])
def test_normalise_ticker(raw, expected):
    assert _normalise_ticker(raw) == expected


class TestFilter:
    def test_bare_action_kept_when_suffixed_ticker_held(self):
        actions = [{"type": "EXIT", "ticker": "VOD", "description": "Stop breached."}]
        assert _filter_actions_to_context(actions, {"VOD.L"}) == actions

    def test_suffixed_action_kept_when_bare_ticker_held(self):
        actions = [{"type": "MONITOR", "ticker": "VOD.L", "description": "Near stop."}]
        assert _filter_actions_to_context(actions, {"VOD"}) == actions

    def test_lower_case_suffixed_action_kept(self):
        actions = [{"type": "HOLD", "ticker": "vod.l", "description": "Stable."}]
        assert _filter_actions_to_context(actions, {"VOD.L"}) == actions

    def test_unknown_ticker_still_dropped(self):
        actions = [{"type": "ENTER", "ticker": "NEW_SIGNAL", "description": "Buy."},
                   {"type": "EXIT", "ticker": "VODA", "description": "Not VOD."}]
        assert _filter_actions_to_context(actions, {"VOD.L"}) == []


def _check(text, held, own_ticker=None):
    return _append_missing_stop_times(text, [_position(held)], "POST /ai/daily-briefing",
                                      "summary", "v1.3", own_ticker)


class TestStopTimeAttribution:
    NOTE = "(VOD.L stop last recalculated 2026-10-20 21:05 UTC)"

    def test_bare_mention_attributed_to_suffixed_holding(self):
        text = "VOD is close to its stop."
        assert _check(text, "VOD.L") == (f"{text} {self.NOTE}", "appended")

    def test_suffixed_mention_attributed_to_bare_holding(self):
        text = "VOD.L is close to its stop."
        out, outcome = _check(text, "VOD")
        assert outcome == "appended"
        assert out.endswith("(VOD stop last recalculated 2026-10-20 21:05 UTC)")

    def test_action_own_ticker_bare_for_suffixed_holding(self):
        text = "Price is through the stop."
        assert _check(text, "VOD.L", own_ticker="VOD") == (f"{text} {self.NOTE}", "appended")

    def test_longer_ticker_is_not_a_match(self):
        text = "VODA is close to its stop."
        assert _check(text, "VOD.L") == (text, "unattributed")


def test_briefing_keeps_bare_exit_for_held_uk_position(database_stub):
    from services import ai_service
    sys.modules["database"] = database_stub
    database_stub.get_portfolio.return_value = {"id": "p-001", "cash": 5000, "initial_cash": 10000}
    database_stub.get_positions.return_value = [_position("VOD.L")]
    database_stub.get_signals.return_value = []
    body = json.dumps({"summary": "One UK position open.", "actions": [
        {"type": "EXIT", "ticker": "VOD", "description": "VOD breached its stop."}]})
    resp = MagicMock()
    resp.content = [MagicMock(text=body)]
    resp.usage = MagicMock(input_tokens=1, output_tokens=1)
    with patch.object(ai_service, "_create_message", return_value=resp), \
         patch.object(ai_service, "_get_regime_data", return_value=None), \
         patch.object(ai_service, "sample_ai_output"), \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
        result = ai_service.generate_daily_briefing()
    assert [a["ticker"] for a in result["actions"]] == ["VOD"]
    assert result["actions"][0]["description"].endswith(TestStopTimeAttribution.NOTE)
