"""
ST-39 (BLG-QA-220, EPIC-07, v9.15) — behavioural tests for live holding days
in the compliance and AI daily-briefing readers.

ST-12 (BLG-BE-153, v9.11) moved both readers to live_holding_days(), but only
a source-scan test guarded them. Here a position whose stored holding_days
is 9 (one day stale) and whose entry_date is 10 days ago (GRACE_PERIOD_DAYS
is 10) must be treated as out of grace by both readers: read from the stored
column it would still be in grace.
"""
import json
import sys
from datetime import date, timedelta
from unittest.mock import MagicMock, patch

from strategy_parameters import GRACE_PERIOD_DAYS


def _position():
    return {
        "id": "pos-1", "ticker": "MU", "market": "US", "status": "open",
        "entry_date": (date.today() - timedelta(days=10)).isoformat(),
        "holding_days": 9,                       # stale stored value: would read as in grace
        "entry_price": 100.0, "initial_stop": 90.0, "current_stop": 95.0, "atr": 2.0,
        "shares": 10.0, "fx_rate": 1.27,
        "current_price": 94.0, "pnl_pct": -6.0,  # below the stop: a breach
        "risk_off_exit": False, "stop_calculated_at": None,
    }


def test_fixture_straddles_the_grace_boundary():
    assert GRACE_PERIOD_DAYS == 10
    assert _position()["holding_days"] < GRACE_PERIOD_DAYS <= 10


def test_compliance_reports_the_position_out_of_grace():
    from services import compliance_service
    with patch.object(compliance_service, "get_portfolio", return_value={"id": "p-1"}), \
         patch.object(compliance_service, "get_positions", return_value=[_position()]), \
         patch.object(compliance_service, "get_latest_snapshot", return_value=None), \
         patch.object(compliance_service, "get_settings", return_value=[]):
        result = compliance_service.get_position_compliance()
    (row,) = result["positions"]
    # In grace, stop_age_days and stop_compliant are both None (not assessed).
    assert row["stop_age_days"] == 10
    assert row["stop_compliant"] is not None


def test_ai_briefing_context_marks_the_position_not_in_grace(database_stub):
    from services import ai_service
    sys.modules["database"] = database_stub
    database_stub.get_portfolio.return_value = {"id": "p-1", "cash": 1000, "initial_cash": 0}
    database_stub.get_positions.return_value = [_position()]
    database_stub.get_signals.return_value = []
    sent = {}

    def fake_create(api_key, **kw):
        sent.update(kw)
        resp = MagicMock()
        resp.content = [MagicMock(text=json.dumps({"summary": "MU breached its stop.", "actions": []}))]
        resp.usage = MagicMock(input_tokens=1, output_tokens=1)
        return resp

    with patch.object(ai_service, "_create_message", side_effect=fake_create), \
         patch.object(ai_service, "_get_regime_data", return_value=None), \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
        ai_service.generate_daily_briefing()
    context = sent["messages"][0]["content"]
    mu_line = next(line for line in context.splitlines() if line.strip().startswith("- MU"))
    assert "[STOP BREACH]" in mu_line
    assert "grace" not in mu_line
