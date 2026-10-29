"""
Unknown market regime (ST-03, EPIC-01, v9.14, BLG-BE-193).

Ruling (a), Strategy Rules & System Intent Owner, 2026-10-29
(ESC-EXEC-20261029-01; strategy_rules.md §4.2.1, §8.2): while a market's
regime cannot be measured, new entries there are blocked (the pre-entry
regime gate fails and no entry signals are produced), and the unknown regime
never triggers the §8.2 risk-off exit. The API reports "unknown" with null
price, MA and is_risk_on, never a defaulted risk-on reading.
"""
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))
import main  # noqa: E402
from routers import pre_entry_validation  # noqa: E402
from services import position_service  # noqa: E402
from utils.calculations import should_exit_position  # noqa: E402
from utils.pricing import market_regime_status  # noqa: E402

CLIENT = TestClient(main.app, raise_server_exceptions=False)
SPY_UNKNOWN = {
    "spy_risk_on": None, "ftse_risk_on": True,
    "spy_regime_status": "unknown", "ftse_regime_status": "risk_on",
    "spy_price": None, "spy_ma200": None, "ftse_price": 8200.0, "ftse_ma200": 8000.0,
    "spy_source": None, "ftse_source": "yahoo_finance",
    "date": datetime(2026, 10, 29, 9, 0, 0),
}


def test_status_helper_reports_unknown_not_risk_off():
    assert market_regime_status(SPY_UNKNOWN, "US") == "unknown"
    assert market_regime_status(SPY_UNKNOWN, "UK") == "risk_on"
    assert market_regime_status({"spy_risk_on": False}, "US") == "risk_off"


def test_unknown_regime_never_triggers_the_risk_off_exit():
    assert should_exit_position(105, 100, 15, None) == (False, None)
    assert should_exit_position(105, 100, 3, None) == (False, None)


def test_unknown_regime_leaves_the_stop_in_force():
    assert should_exit_position(95, 100, 15, None) == (True, "Stop Loss Hit")


def test_measured_risk_off_still_exits():
    assert should_exit_position(105, 100, 15, False) == (True, "Risk-Off Signal")


def test_pre_entry_regime_gate_fails_when_unknown():
    with patch("position_manager.check_market_regime", return_value=SPY_UNKNOWN):
        result = pre_entry_validation._check_regime("US")
    assert result["status"] == "fail"
    assert "could not be measured" in result["detail"]
    assert "New entries in this market are blocked until it is measured." in result["detail"]


def test_pre_entry_regime_gate_unaffected_for_the_measured_market():
    with patch("position_manager.check_market_regime", return_value=SPY_UNKNOWN):
        result = pre_entry_validation._check_regime("UK")
    assert result["status"] == "pass"


def test_nightly_risk_off_job_leaves_unknown_market_flags_unchanged():
    positions = [{"id": 1, "market": "US"}, {"id": 2, "market": "UK"}]
    with patch.object(position_service, "get_portfolio", return_value={"id": 7}), \
         patch.object(position_service, "get_positions", return_value=positions), \
         patch.object(position_service, "check_market_regime", return_value=SPY_UNKNOWN), \
         patch("database.update_positions_risk_off_exit") as update:
        result = position_service.run_nightly_risk_off_alerts()
    update.assert_called_once_with("2", False)
    assert result["us_risk_off"] is False
    assert result["us_regime_status"] == "unknown"
    assert result["us_positions_flagged"] == 0 and result["us_positions_cleared"] == 0


def test_market_status_returns_unknown_with_null_values():
    with patch.object(main, "check_market_regime", return_value=SPY_UNKNOWN), \
         patch.object(main, "get_live_fx_rate", return_value=1.34), \
         patch.object(main, "record_market_status_check"):
        resp = CLIENT.get("/market/status")
    assert resp.status_code == 200
    spy = resp.json()["data"]["spy"]
    assert spy == {"price": None, "ma200": None, "is_risk_on": None, "regime_status": "unknown"}
    assert resp.json()["data"]["ftse"]["regime_status"] == "risk_on"


def test_market_regime_returns_unknown():
    with patch.object(main, "check_market_regime", return_value=SPY_UNKNOWN):
        resp = CLIENT.get("/market/regime")
    assert resp.status_code == 200
    assert resp.json()["data"] == [{"market": "US", "status": "unknown"}, {"market": "UK", "status": "risk_on"}]
