"""
ST-08 (BLG-BE-141, EPIC-01, v9.11) — AI briefing and chat state when a
quoted stop was last recalculated.

The per-position context sent to the model carries each stop's
`stop_calculated_at` (DS-22), and both system prompts tell the model to
state that time whenever it mentions a stop or a stop breach. Fixture tests
with the model call mocked: the prompt the model receives contains the
time next to the stop, and the instruction.
"""
import sys
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

_POSITIONS = [
    {"ticker": "MU", "market": "US", "current_price": 100.0, "current_stop": 95.0, "pnl_pct": 4.0,
     "pnl": 40.0, "holding_days": 14, "risk_off_exit": False,
     "stop_calculated_at": datetime(2026, 10, 7, 21, 5, tzinfo=timezone.utc)},
    {"ticker": "WDC", "market": "US", "current_price": 50.0, "current_stop": 51.0, "pnl_pct": -2.0,
     "pnl": -20.0, "holding_days": 3, "risk_off_exit": False, "stop_calculated_at": None},
]


@pytest.fixture
def _db(database_stub):
    sys.modules["database"] = database_stub
    database_stub.get_portfolio.return_value = {"id": "p-001", "cash": 5000, "initial_cash": 10000}
    database_stub.get_positions.return_value = [dict(p) for p in _POSITIONS]
    database_stub.get_signals.return_value = []
    return database_stub


def _capture(func, *args, body='{"summary": "x", "actions": []}'):
    from services import ai_service
    captured = {}

    def fake_create(api_key, **kw):
        captured.update(kw)
        resp = MagicMock()
        resp.content = [MagicMock(text=body)]
        resp.usage = MagicMock(input_tokens=1, output_tokens=1)
        return resp

    with patch.object(ai_service, "_create_message", side_effect=fake_create), \
         patch.object(ai_service, "_get_regime_data", return_value=None), \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
        getattr(ai_service, func)(*args)
    return captured


def test_briefing_context_carries_stop_recalculation_time(_db):
    sent = _capture("generate_daily_briefing")
    context = sent["messages"][0]["content"]
    assert "trailing stop £95.00 (stop last recalculated 2026-10-07 21:05 UTC)" in context
    # The breach line for WDC (price below stop, in grace) still carries the time.
    assert "trailing stop £51.00 (stop not recalculated since entry)" in context
    assert "state when that stop was last recalculated" in sent["system"]


def test_chat_context_carries_stop_recalculation_time(_db):
    sent = _capture("ai_chat", "Where is my MU stop?", body="ok")
    assert "stop £95.00 (stop last recalculated 2026-10-07 21:05 UTC)" in sent["system"]
    assert "stop £51.00 (stop not recalculated since entry)" in sent["system"]
    assert "state when that stop was last recalculated" in sent["system"]


def test_iso_string_timestamp_is_formatted():
    from services.ai_service import _stop_recalculated_label
    assert _stop_recalculated_label({"stop_calculated_at": "2026-10-07T21:05:00Z"}) == \
        "stop last recalculated 2026-10-07 21:05 UTC"


def test_prompt_versions_bumped_for_st08():
    from services import ai_service
    assert ai_service.BRIEFING_PROMPT_VERSION == "v1.2"
    assert ai_service.CHAT_PROMPT_VERSION == "v1.1"
