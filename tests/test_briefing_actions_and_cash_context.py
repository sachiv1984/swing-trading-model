"""
ST-02 (BLG-AI-11) and ST-03 (BLG-AI-12), EPIC-01, v9.12 — daily briefing.

ST-02: on staging the briefing returned ENTER for the placeholder ticker
NEW_SIGNAL. Actions naming a ticker that is neither a held position nor one
of the signals given to the model are dropped and logged, and the prompt
says actions may only name tickers from the snapshot.

ST-03: the context rendered cash as "cash £X of £{initial_cash}", which the
model read as a target cash level ("£15,006 against a £0 target"). Each
figure is labelled, and starting capital is omitted when it is 0.

Both share one BRIEFING_PROMPT_VERSION bump (v1.2 -> v1.3), recorded in
tests/fixtures/ai_prompt_template_golden_fixtures.json. Model call mocked.
"""
import json
import logging
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

_POSITIONS = [
    {"ticker": "MU", "market": "US", "current_price": 100.0, "current_stop": 95.0, "pnl_pct": 4.0,
     "holding_days": 14, "risk_off_exit": False, "stop_calculated_at": None},
]
_SIGNALS = [
    {"ticker": "AAPL", "market": "US", "rank": 1, "momentum_percent": 9.5,
     "signal_date": "2026-10-12", "status": "new"},
]


def _db(database_stub, initial_cash=10000):
    sys.modules["database"] = database_stub
    database_stub.get_portfolio.return_value = {"id": "p-001", "cash": 15006, "initial_cash": initial_cash}
    database_stub.get_positions.return_value = [dict(p) for p in _POSITIONS]
    database_stub.get_signals.return_value = [dict(s) for s in _SIGNALS]
    return database_stub


def _brief(body):
    from services import ai_service
    sent = {}

    def fake_create(api_key, **kw):
        sent.update(kw)
        resp = MagicMock()
        resp.content = [MagicMock(text=body)]
        resp.usage = MagicMock(input_tokens=1, output_tokens=1)
        return resp

    with patch.object(ai_service, "_create_message", side_effect=fake_create), \
         patch.object(ai_service, "_get_regime_data", return_value=None), \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
        result = ai_service.generate_daily_briefing()
    return result, sent


_ACTIONS_BODY = json.dumps({"summary": "One position open; one strong signal.", "actions": [
    {"type": "HOLD", "ticker": "MU", "description": "Stable."},
    {"type": "ENTER", "ticker": "AAPL", "description": "Rank #1 signal."},
    {"type": "ENTER", "ticker": "NEW_SIGNAL", "description": "Placeholder."},
    {"type": "ENTER", "ticker": "TSLA", "description": "Not in the context."},
]})


class TestActionsLimitedToContextTickers:
    def test_unknown_ticker_enter_is_dropped_and_logged(self, database_stub, caplog):
        _db(database_stub)
        with caplog.at_level(logging.WARNING, logger="services.ai_service"):
            result, _ = _brief(_ACTIONS_BODY)
        assert [a["ticker"] for a in result["actions"]] == ["MU", "AAPL"]
        dropped = [r.getMessage() for r in caplog.records if "dropped action" in r.getMessage()]
        assert len(dropped) == 2
        assert "'NEW_SIGNAL'" in dropped[0] and "type=ENTER" in dropped[0]
        assert "'TSLA'" in dropped[1]

    def test_held_and_signal_tickers_kept_case_insensitively(self, database_stub):
        _db(database_stub)
        body = json.dumps({"summary": "s", "actions": [{"type": "HOLD", "ticker": "mu", "description": "d"}]})
        result, _ = _brief(body)
        assert [a["ticker"] for a in result["actions"]] == ["mu"]

    def test_action_without_ticker_is_dropped(self, database_stub):
        _db(database_stub)
        body = json.dumps({"summary": "s", "actions": [{"type": "MONITOR", "description": "d"}]})
        result, _ = _brief(body)
        assert result["actions"] == []

    def test_prompt_tells_model_to_name_only_context_tickers(self, database_stub):
        _db(database_stub)
        _, sent = _brief(_ACTIONS_BODY)
        assert "never invent a ticker or use a placeholder" in sent["system"]

    def test_filter_helper_ignores_non_list(self):
        from services.ai_service import _filter_actions_to_context
        assert _filter_actions_to_context(None, {"MU"}) == []


class TestCashLabels:
    def test_cash_and_starting_capital_labelled_separately(self, database_stub):
        _db(database_stub, initial_cash=10000)
        _, sent = _brief(_ACTIONS_BODY)
        context = sent["messages"][0]["content"]
        assert "available cash £15,006; starting capital £10,000" in context
        assert " of £" not in context

    @pytest.mark.parametrize("initial_cash", [0, None])
    def test_starting_capital_omitted_when_zero_or_missing(self, database_stub, initial_cash):
        _db(database_stub, initial_cash=initial_cash)
        _, sent = _brief(_ACTIONS_BODY)
        context = sent["messages"][0]["content"]
        assert "Portfolio: 1 open positions, available cash £15,006\n" in context
        assert "starting capital" not in context
        assert " of £" not in context


def test_briefing_prompt_version_bumped_once_for_st02_and_st03():
    from services import ai_service
    fixtures = json.loads((Path(__file__).parent / "fixtures" / "ai_prompt_template_golden_fixtures.json").read_text())["templates"]
    assert ai_service.BRIEFING_PROMPT_VERSION == "v1.3"
    assert fixtures["daily-briefing (POST /ai/daily-briefing)"]["prompt_version"] == "v1.3"
