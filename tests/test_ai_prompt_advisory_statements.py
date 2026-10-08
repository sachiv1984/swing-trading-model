"""
ST-07 (BLG-AI-09, EPIC-01, v9.11) — §13 self-audit check A1, automated.

`docs/ops/ai_chat_section13_quarterly_self_audit_checklist.md` check A1:
both the daily-briefing and the chat system prompts state that the output
is advisory and that the model cannot execute trades. The briefing prompt
also frames its action items as recommendations (check A4). Before v9.11
the briefing prompt said neither (baseline Fail, 2026-10-06).
"""
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from test_ai_prompt_template_golden_fixtures import _load_fixtures, _rendered_text_for_scan  # noqa: E402


def _prompt(key_fragment):
    for key, entry in _load_fixtures().items():
        if key_fragment in key:
            return " ".join(_rendered_text_for_scan(entry).split()).lower()
    raise AssertionError(f"no fixture entry matching {key_fragment!r}")


@pytest.mark.parametrize("key", ["daily-briefing", "chat (POST /ai/chat)"])
def test_check_a1_prompt_states_advisory_and_no_execution(key):
    text = _prompt(key)
    assert "advisory only" in text
    assert "cannot execute trades" in text


def test_check_a4_briefing_frames_actions_as_recommendations():
    text = _prompt("daily-briefing")
    assert "recommended actions" in text
    assert "recommendation for the user to decide on" in text


@pytest.fixture
def _db(database_stub):
    sys.modules["database"] = database_stub
    database_stub.get_portfolio.return_value = {"id": "p-001", "cash": 5000, "initial_cash": 10000}
    database_stub.get_positions.return_value = []
    database_stub.get_signals.return_value = []
    database_stub.create_claude_audit_entry.reset_mock()
    return database_stub


def test_briefing_audit_row_records_bumped_prompt_version(_db):
    from services import ai_service
    resp = MagicMock()
    resp.content = [MagicMock(text='{"summary": "ok", "actions": []}')]
    resp.usage = MagicMock(input_tokens=1, output_tokens=1)
    with patch.object(ai_service, "_create_message", return_value=resp), \
         patch.object(ai_service, "_get_regime_data", return_value=None), \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
        ai_service.generate_daily_briefing()
    assert _db.create_claude_audit_entry.call_args.kwargs["prompt_version"] == ai_service.BRIEFING_PROMPT_VERSION == "v1.1"
