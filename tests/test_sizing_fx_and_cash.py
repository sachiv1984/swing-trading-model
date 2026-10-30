"""
ST-09 (BLG-QA-205, EPIC-02, v9.12): size_position() FX handling (strategy_rules.md
§4.1.5) and cash constraint (§4.1.6), asserted in CI.

Traceability matrix rows (docs/testing/strategy_rule_test_traceability_matrix.md):
    C4.1.5-01  A user-provided FX rate overrides the live rate
    C4.1.5-02  Default FX is the system-provided live rate
    C4.1.5-03  The FX rate used is returned in the sizing response
    C4.1.6-01  EstimatedCost > AvailableCash -> cash_sufficient: false
    C4.1.6-02  The insufficient-cash result includes max_affordable_shares

ST-09 (BLG-BE-190, EPIC-02, v9.14) adds the §4.1.3 US worked example.

Before this file the only backend tests of these paths were in
backend/mutmut_pilot_tests/, which no CI workflow runs.

CI-safe: database, pricing, settings and heat calls are mocked. No ticker is
passed, so the concentration adjustment does not run.
"""
import sys
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import services.sizing_service as sizing_service  # noqa: E402
from utils.calculations import calculate_uk_entry_fees, calculate_us_entry_fees  # noqa: E402

SETTINGS = {"uk_commission": 9.95, "stamp_duty_rate": 0.005, "us_commission": 0.0, "fx_fee_rate": 0.0015}
SNAPSHOT = {"total_value": 20000.0}
LIVE_FX = 1.25


def _size(market="UK", fx_rate=None, cash=50000.0, entry_price=100.0, stop_price=90.0):
    """Return (result, live_fx_mock). Risk 1% of £20,000 = £200; stop distance 10."""
    with ExitStack() as stack:
        stack.enter_context(patch.object(sizing_service, "get_portfolio", return_value={"id": "p-1", "cash": cash}))
        stack.enter_context(patch.object(sizing_service, "get_latest_snapshot", return_value=SNAPSHOT))
        stack.enter_context(patch.object(sizing_service, "get_settings", return_value=[SETTINGS]))
        stack.enter_context(patch.object(sizing_service, "calculate_prospective_heat", return_value={"valid": False}))
        live = stack.enter_context(patch.object(sizing_service, "get_live_fx_rate", return_value=LIVE_FX))
        result = sizing_service.size_position(
            entry_price=entry_price, stop_price=stop_price, risk_percent=1.0, market=market, fx_rate=fx_rate,
        )
    return result, live


class TestUsShareCalculation:
    def test_worked_example_divides_stop_distance_by_fx(self):
        """ST-09 (BLG-BE-190, v9.14): §4.1.3 US formula RawShares = RiskAmount x FX /
        StopDistance. £100 risk (0.5% of £20,000), $10 stop distance, FX 1.27 -> 12.7."""
        with ExitStack() as stack:
            stack.enter_context(patch.object(sizing_service, "get_portfolio", return_value={"id": "p-1", "cash": 50000.0}))
            stack.enter_context(patch.object(sizing_service, "get_latest_snapshot", return_value=SNAPSHOT))
            stack.enter_context(patch.object(sizing_service, "get_settings", return_value=[SETTINGS]))
            stack.enter_context(patch.object(sizing_service, "calculate_prospective_heat", return_value={"valid": False}))
            result = sizing_service.size_position(
                entry_price=100.0, stop_price=90.0, risk_percent=0.5, market="US", fx_rate=1.27,
            )
        assert result["risk_amount"] == 100.0
        assert result["suggested_shares"] == 12.7
        risk_gbp = result["suggested_shares"] * result["stop_distance"] / result["fx_rate_used"]
        assert 0 <= result["risk_amount"] - risk_gbp < 0.0001 * result["stop_distance"] / 1.27 + 1e-9


class TestFxHandling:
    def test_us_without_override_uses_live_rate(self):
        """C4.1.5-02: no fx_rate supplied for a US position -> get_live_fx_rate() is used."""
        result, live = _size(market="US")
        live.assert_called_once()
        assert result["valid"] is True
        # £200 × 1.25 / $10 = 25 shares, so the live rate drove the share count
        assert result["suggested_shares"] == 25.0

    def test_us_live_rate_is_echoed(self):
        """C4.1.5-03: the live rate used is returned as fx_rate_used."""
        result, _ = _size(market="US")
        assert result["fx_rate_used"] == LIVE_FX

    def test_us_override_replaces_live_rate_and_is_echoed(self):
        """C4.1.5-01 / C4.1.5-03: a supplied fx_rate overrides the live rate and is echoed."""
        result, live = _size(market="US", fx_rate=1.30)
        live.assert_not_called()
        assert result["fx_rate_used"] == 1.30
        # £200 × 1.30 / $10 = 26 shares
        assert result["suggested_shares"] == 26.0

    def test_uk_fx_rate_used_is_one(self):
        """C4.1.5-03: a UK position reports fx_rate_used 1.0 and never reads the live rate."""
        result, live = _size(market="UK", fx_rate=1.30)
        live.assert_not_called()
        assert result["fx_rate_used"] == 1.0
        assert result["suggested_shares"] == 20.0


class TestCashConstraint:
    def test_cost_above_cash_is_insufficient(self):
        """C4.1.6-01: estimated cost (£2,000 + fees) above £500 cash -> cash_sufficient false."""
        result, _ = _size(market="UK", cash=500.0)
        assert result["estimated_cost"] > 500.0
        assert result["cash_sufficient"] is False
        assert result["available_cash"] == 500.0

    def test_insufficient_result_includes_affordable_max_shares(self):
        """C4.1.6-02: max_affordable_shares is present, and that many shares plus fees fit in cash."""
        result, _ = _size(market="UK", cash=500.0)
        max_shares = result["max_affordable_shares"]
        assert 0 < max_shares < result["suggested_shares"]
        gross = max_shares * 100.0
        assert gross + calculate_uk_entry_fees(gross, SETTINGS)["total"] <= 500.0

    def test_us_insufficient_result_includes_affordable_max_shares(self):
        """C4.1.6-01/02 (US): GBP cash against a USD cost converted at fx_rate_used."""
        result, _ = _size(market="US", fx_rate=1.25, cash=500.0)
        assert result["cash_sufficient"] is False
        max_shares = result["max_affordable_shares"]
        assert max_shares > 0
        gross_usd = max_shares * 100.0
        cost_gbp = (gross_usd + calculate_us_entry_fees(gross_usd, SETTINGS)["total"]) / 1.25
        assert cost_gbp <= 500.0

    def test_cost_within_cash_is_sufficient_without_max_shares(self):
        """C4.1.6-01 (negative): cost within cash -> cash_sufficient true, no max_affordable_shares."""
        result, _ = _size(market="UK", cash=5000.0)
        assert result["cash_sufficient"] is True
        assert "max_affordable_shares" not in result
