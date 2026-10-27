"""
ST-19 (BLG-AI-14), EPIC-03, v9.13 — AI chat context labels available cash
and starting capital separately, as ST-03 (BLG-AI-12, v9.12) did for the
daily briefing.

The chat context rendered "Cash: £X of £{initial_cash} initial capital",
which on staging (initial_cash 0) read "of £0 initial capital" and invites
the same target-cash misreading. It now reuses _briefing_cash_line(), which
omits starting capital when it is 0 or missing. CHAT_PROMPT_VERSION
v1.1 -> v1.2, recorded in tests/fixtures/ai_prompt_template_golden_fixtures.json.
Model call mocked.
"""
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

_POSITIONS = [
    {"ticker": "MU", "market": "US", "current_price": 100.0, "current_stop": 95.0, "pnl": 40.0,
     "risk_off_exit": False, "stop_calculated_at": None},
]


def _chat_system_prompt(database_stub, initial_cash):
    from services import ai_service
    sys.modules["database"] = database_stub
    database_stub.get_portfolio.return_value = {"id": "p-001", "cash": 15006, "initial_cash": initial_cash}
    database_stub.get_positions.return_value = [dict(p) for p in _POSITIONS]
    database_stub.get_signals.return_value = []
    sent = {}

    def fake_create(api_key, **kw):
        sent.update(kw)
        resp = MagicMock()
        resp.content = [MagicMock(text="MU looks stable.")]
        resp.usage = MagicMock(input_tokens=1, output_tokens=1)
        return resp

    with patch.object(ai_service, "_create_message", side_effect=fake_create), \
         patch.object(ai_service, "sample_ai_output"), \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
        ai_service.ai_chat("How is MU doing?")
    return sent["system"]


def test_cash_and_starting_capital_labelled_separately(database_stub):
    system = _chat_system_prompt(database_stub, 10000)
    assert "Portfolio: 1 open positions, available cash £15,006; starting capital £10,000" in system
    assert " of £" not in system
    assert "initial capital" not in system


@pytest.mark.parametrize("initial_cash", [0, None])
def test_starting_capital_omitted_when_zero_or_missing(database_stub, initial_cash):
    system = _chat_system_prompt(database_stub, initial_cash)
    assert "Portfolio: 1 open positions, available cash £15,006\n" in system
    assert "starting capital" not in system
    assert " of £" not in system


def test_chat_prompt_version_bumped_and_recorded(database_stub):
    from services import ai_service
    fixtures = json.loads((Path(__file__).parent / "fixtures" / "ai_prompt_template_golden_fixtures.json").read_text())["templates"]
    assert ai_service.CHAT_PROMPT_VERSION == "v1.2"
    assert fixtures["chat (POST /ai/chat)"]["prompt_version"] == "v1.2"
    _chat_system_prompt(database_stub, 10000)
    assert database_stub.create_claude_audit_entry.call_args.kwargs["prompt_version"] == "v1.2"
