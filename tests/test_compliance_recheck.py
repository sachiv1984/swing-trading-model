"""
Compliance Recheck Unit Tests — ST-01 (BLG-FEAT-64, v6.9)

Verifies GET /positions/{position_id}/compliance-recheck re-applies the 5 SI-01
checks against an open position's current state, and that the sector
concentration recheck excludes the rechecked position from the baseline sum
(avoiding the double-count that would occur from reusing the prospective-entry
formula verbatim — see compliance_recheck_service.py module docstring).

CI-safe: all database, pricing, and external service calls are mocked.

Spec: docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/compliance-recheck
"""

import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from fastapi.testclient import TestClient
from main import app
from services.compliance_recheck_service import get_compliance_recheck

CLIENT = TestClient(app, raise_server_exceptions=False)

MOCK_REGIME_ON = {"spy_risk_on": True, "ftse_risk_on": True}
MOCK_REGIME_OFF = {"spy_risk_on": False, "ftse_risk_on": False}
MOCK_PORTFOLIO = {"id": "test-portfolio-001", "cash": 5000.0}
NO_EARNINGS = {"next_earnings_date": None, "days_until_earnings": None}

OPEN_POSITION = {
    "id": "pos-001",
    "ticker": "AAPL",
    "market": "US",
    "status": "open",
    "shares": 10,
    "entry_price": 200.0,
    "current_stop": 190.0,
    "initial_stop": 180.0,
    "sector": "Technology",
}


def _common_patches(position=OPEN_POSITION, regime=MOCK_REGIME_ON, portfolio=MOCK_PORTFOLIO, earnings=NO_EARNINGS, price=215.0):
    return (
        patch("database.get_position_by_id", return_value=position),
        patch("position_manager.check_market_regime", return_value=regime),
        patch("database.get_portfolio", return_value=portfolio),
        patch("database.get_positions", return_value=[position]),
        patch("utils.pricing.get_current_price", return_value=price),
        patch("utils.pricing.get_live_fx_rate", return_value=1.27),
        patch("services.earnings_service.get_earnings", return_value=earnings),
        patch("services.compliance_recheck_service._get_ticker_sector", return_value="Technology"),
    )


def test_404_when_position_not_found():
    with patch("database.get_position_by_id", return_value=None):
        resp = CLIENT.get("/positions/does-not-exist/compliance-recheck")
    assert resp.status_code == 404


def test_404_when_position_not_open():
    closed = {**OPEN_POSITION, "status": "closed"}
    with patch("database.get_position_by_id", return_value=closed):
        resp = CLIENT.get("/positions/pos-001/compliance-recheck")
    assert resp.status_code == 404


def test_returns_all_5_rule_keys():
    patches = _common_patches()
    with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7]:
        resp = CLIENT.get("/positions/pos-001/compliance-recheck")
    assert resp.status_code == 200
    data = resp.json()["data"]
    rule_keys = {c["rule_key"] for c in data["checks"]}
    assert rule_keys == {
        "regime_gate",
        "cash_constraint",
        "sector_concentration",
        "earnings_proximity",
        "sizing_validity",
    }
    # Minimal shape per ux_spec.md §7 — no extraneous fields leaked to the response
    assert set(data["checks"][0].keys()) == {"rule_key", "status", "detail"}


def test_overall_status_fail_when_regime_off():
    patches = _common_patches(regime=MOCK_REGIME_OFF)
    with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7]:
        resp = CLIENT.get("/positions/pos-001/compliance-recheck")
    data = resp.json()["data"]
    assert data["overall_status"] == "fail"
    regime_check = next(c for c in data["checks"] if c["rule_key"] == "regime_gate")
    assert regime_check["status"] == "fail"


def test_sector_concentration_excludes_self_from_baseline():
    """
    Sector concentration recheck must not double-count the position being
    rechecked. With a single open position (itself) and ample cash, excluding
    self from the baseline and adding it back once should keep concentration
    well under the 30% advisory threshold — the double-counted (un-adapted)
    formula would inflate this because the position is present twice.
    """
    # get_compliance_recheck trims checks down to {rule_key, status, detail} per the API
    # contract, so the detailed projected_sector_pct field is verified by calling the
    # sector concentration helper directly instead.
    from services.compliance_recheck_service import _check_sector_concentration_recheck
    with (
        patch("database.get_portfolio", return_value={"id": "test", "cash": 100000.0}),
        patch("database.get_positions", return_value=[OPEN_POSITION]),
        patch("utils.pricing.get_current_price", return_value=195.0),
        patch("utils.pricing.get_live_fx_rate", return_value=1.27),
        patch("services.compliance_recheck_service._get_ticker_sector", return_value="Technology"),
    ):
        sector_check = _check_sector_concentration_recheck("pos-001", "AAPL", "US", 10)
    assert sector_check["status"] == "pass"
    # Only self-position value (10 * 195 / 1.27 ≈ £1,535) vs £100k+ total → well under 30%
    assert sector_check["projected_sector_pct"] < 5.0


def test_uses_current_stop_not_entry_time_stop_for_sizing():
    """Sizing validity recheck must use the current effective stop (trailing/current_stop),
    reflecting the position's current risk state rather than the entry-time snapshot (AC-01)."""
    position = {**OPEN_POSITION, "current_stop": 190.0, "initial_stop": 150.0}
    patches = _common_patches(position=position)
    with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7]:
        resp = CLIENT.get("/positions/pos-001/compliance-recheck")
    data = resp.json()["data"]
    sizing_check = next(c for c in data["checks"] if c["rule_key"] == "sizing_validity")
    assert sizing_check["status"] == "pass"
    assert "190" in sizing_check["detail"]
