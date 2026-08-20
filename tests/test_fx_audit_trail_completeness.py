"""
FX conversion audit trail completeness regression tests (ST-03, EPIC-01, v8.0,
BLG-SPEC-107).

strategy_rules.md §4.1.5: "The FX rate used must be returned in the sizing
response for auditability." The audit (docs/product/decisions/
fx-audit-trail-completeness-check--2026-07-30.md) found 3 FX-conversion
response paths that computed a rate but never returned it. This file covers
regression tests for the fix in each.

No live database/network calls — mocks follow the same pattern as
test_position_trade_plan_link.py (position_service) and test_trade_plan_tags.py
(module-level function mocking).
"""
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import services.position_service as position_service  # noqa: E402
import routers.prospective_heat as prospective_heat  # noqa: E402
import services.portfolio_service as portfolio_service  # noqa: E402
from routers.pre_entry_validation import _check_cash_constraint  # noqa: E402


# ---------------------------------------------------------------------------
# POST /portfolio/position — add_position() now returns fx_rate_used
# ---------------------------------------------------------------------------

def _portfolio():
    return {"id": "portfolio-1", "cash": 100000.0}


def _settings():
    return [{
        "uk_commission": 9.95,
        "us_commission": 0,
        "stamp_duty_rate": 0.005,
        "fx_fee_rate": 0.0015,
    }]


class TestAddPositionReturnsFxRateUsed:
    def setup_method(self):
        self._patches = []

    def teardown_method(self):
        for p in self._patches:
            p.stop()

    def _patch(self, name, **kwargs):
        p = patch.object(position_service, name, **kwargs)
        self._patches.append(p)
        return p.start()

    def _install_common_mocks(self):
        self._patch("get_portfolio", return_value=_portfolio())
        self._patch("get_settings", return_value=_settings())
        self._patch("create_position", return_value={"id": "new-position-id"})
        self._patch("update_portfolio_cash")
        self._patch("calculate_atr", return_value=1.0)
        self._patch("calculate_us_entry_fees", return_value={"commission": 0, "stamp_duty": 0, "fx_fee": 1.5, "total": 1.5})
        self._patch("calculate_uk_entry_fees", return_value={"commission": 9.95, "stamp_duty": 5.0, "total": 14.95})
        self._patch("calculate_initial_stop", return_value=90.0)
        self._patch("get_unlinked_trade_plan_for_entry", return_value=None)
        self._patch("get_current_strategy_version", return_value="1.4")

    def test_us_position_returns_provided_fx_rate(self):
        self._install_common_mocks()
        result = position_service.add_position(
            ticker="AAPL", market="US", entry_date="2026-07-09",
            shares=10, entry_price=100.0, fx_rate=1.3642,
        )
        assert result["fx_rate_used"] == 1.3642

    def test_us_position_falls_back_to_live_rate(self):
        self._install_common_mocks()
        self._patch("get_live_fx_rate", return_value=1.27)
        result = position_service.add_position(
            ticker="AAPL", market="US", entry_date="2026-07-09",
            shares=10, entry_price=100.0,
        )
        assert result["fx_rate_used"] == 1.27

    def test_uk_position_returns_1_0(self):
        self._install_common_mocks()
        result = position_service.add_position(
            ticker="FRES.L", market="UK", entry_date="2026-07-09",
            shares=10, entry_price=100.0,
        )
        assert result["fx_rate_used"] == 1.0


# ---------------------------------------------------------------------------
# GET /portfolio/prospective-heat — now returns fx_rate_used
#
# ST-05 (EPIC-02, v8.9, BLG-FEAT-91): calculation logic extracted to
# services.portfolio_service.calculate_prospective_heat (shared with
# POST /portfolio/size's heat_impact_percent). Patch targets updated to the
# new location — prospective_heat.py no longer imports get_portfolio_summary/
# get_live_fx_rate directly, it delegates to the shared function.
# ---------------------------------------------------------------------------

def test_prospective_heat_returns_fx_rate_used_for_us():
    with patch.object(portfolio_service, "get_live_fx_rate", return_value=1.35), \
         patch.object(portfolio_service, "get_portfolio_summary", return_value={
             "total_value": 10000.0,
             "position_risks": [],
         }):
        result = prospective_heat.prospective_heat_endpoint(
            ticker="AAPL", shares=10, entry_price=185.0, stop_price=175.0,
            market="US", fx_rate=None,
        )
    assert result["data"]["valid"] is True
    assert result["data"]["fx_rate_used"] == 1.35


def test_prospective_heat_returns_1_0_for_uk():
    with patch.object(portfolio_service, "get_portfolio_summary", return_value={
        "total_value": 10000.0,
        "position_risks": [],
    }):
        result = prospective_heat.prospective_heat_endpoint(
            ticker="FRES.L", shares=10, entry_price=100.0, stop_price=90.0,
            market="UK",
        )
    assert result["data"]["valid"] is True
    assert result["data"]["fx_rate_used"] == 1.0


def test_prospective_heat_respects_explicit_fx_rate_override():
    with patch.object(portfolio_service, "get_portfolio_summary", return_value={
        "total_value": 10000.0,
        "position_risks": [],
    }):
        result = prospective_heat.prospective_heat_endpoint(
            ticker="AAPL", shares=10, entry_price=185.0, stop_price=175.0,
            market="US", fx_rate=1.4,
        )
    assert result["data"]["fx_rate_used"] == 1.4


# ---------------------------------------------------------------------------
# GET /portfolio/pre-entry-validation cash_constraint check — now returns
# fx_rate_used
# ---------------------------------------------------------------------------

def test_cash_constraint_returns_fx_rate_used_for_us():
    # _check_cash_constraint imports get_portfolio/get_current_price/get_live_fx_rate
    # locally inside the function body (from database / utils.pricing), so the
    # patch target is the source module, not routers.pre_entry_validation.
    with patch("database.get_portfolio", return_value=_portfolio()), \
         patch("utils.pricing.get_current_price", return_value=185.0), \
         patch("utils.pricing.get_live_fx_rate", return_value=1.35):
        result = _check_cash_constraint(ticker="AAPL", market="US", quantity=10)
    assert result["rule"] == "cash_constraint"
    assert result["fx_rate_used"] == 1.35


def test_cash_constraint_returns_1_0_for_uk():
    with patch("database.get_portfolio", return_value=_portfolio()), \
         patch("utils.pricing.get_current_price", return_value=500.0):
        result = _check_cash_constraint(ticker="FRES.L", market="UK", quantity=10)
    assert result["rule"] == "cash_constraint"
    assert result["fx_rate_used"] == 1.0
