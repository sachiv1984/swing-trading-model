"""
ST-05 regression tests (BLG-FEAT-91, EPIC-02, v8.9).

POST /portfolio/size gains heat_impact_percent, reusing
services.portfolio_service.calculate_prospective_heat (the same calculation
GET /portfolio/prospective-heat exposes) rather than duplicating the
risk-basis math a second time — design_record.md / ux_spec.md §2.3:
"reuse, do not introduce a second endpoint call."

CI-safe: all database, pricing, and settings calls are mocked. No live DB or
network connections.
"""
import sys
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import services.sizing_service as sizing_service  # noqa: E402

MOCK_PORTFOLIO = {"id": "test-portfolio-001", "cash": 5000.0}
MOCK_SNAPSHOT = {"total_value": 20000.0}


def _base_patches(heat_result):
    stack = ExitStack()
    stack.enter_context(patch("services.sizing_service.get_portfolio", return_value=MOCK_PORTFOLIO))
    stack.enter_context(patch("services.sizing_service.get_latest_snapshot", return_value=MOCK_SNAPSHOT))
    stack.enter_context(patch("services.sizing_service.get_settings", return_value=[]))
    stack.enter_context(patch("services.sizing_service.calculate_prospective_heat", return_value=heat_result))
    return stack


def _size(ticker=None, entry_price=100.0, stop_price=90.0, risk_percent=1.0, market="UK"):
    return sizing_service.size_position(
        entry_price=entry_price,
        stop_price=stop_price,
        risk_percent=risk_percent,
        market=market,
        ticker=ticker,
    )


class TestHeatImpactHappyPath:
    def test_heat_impact_populated_from_shared_calculation(self):
        heat_result = {
            "valid": True,
            "current_heat_percent": 2.0,
            "prospective_heat_percent": 2.5,
            "incremental_heat_percent": 0.5,
            "prospective_risk_gbp": 100.0,
            "portfolio_value_gbp": 20000.0,
            "fx_rate_used": 1.0,
        }
        with _base_patches(heat_result):
            result = _size()

        assert result["valid"] is True
        assert result["heat_impact_percent"] == 0.5

    def test_heat_calculation_receives_final_adjusted_shares(self):
        """heat_impact_percent must be computed against the (possibly
        concentration-reduced) final suggested_shares, not the pre-adjustment
        baseline."""
        heat_result = {"valid": True, "incremental_heat_percent": 0.3}
        with (
            patch("services.sizing_service.get_portfolio", return_value=MOCK_PORTFOLIO),
            patch("services.sizing_service.get_latest_snapshot", return_value=MOCK_SNAPSHOT),
            patch("services.sizing_service.get_settings", return_value=[]),
            patch("services.sizing_service.get_ticker_sector", return_value="Technology"),
            patch("services.sizing_service.get_sector_exposure", return_value={
                "sector_value_gbp": 5000.0, "total_portfolio_value_gbp": 20000.0,
                "position_count": 2, "fx_rate": 1.0,
            }),
            patch("services.sizing_service.calculate_prospective_heat", return_value=heat_result) as mock_heat,
        ):
            result = _size(ticker="MSFT")

        # Baseline would be 20 shares; concentration caps it to 10 (see
        # test_sizing_concentration.py::test_reduction_math_and_reason_string
        # for the same inputs/derivation).
        assert result["suggested_shares"] == 10.0
        mock_heat.assert_called_once()
        assert mock_heat.call_args.kwargs["shares"] == 10.0


class TestHeatImpactEdgeCases:
    def test_zero_shares_returns_none_not_error(self):
        """Fully concentration-capped-to-zero position: no shares to price,
        heat_impact_percent is None (not an error)."""
        with (
            patch("services.sizing_service.get_portfolio", return_value=MOCK_PORTFOLIO),
            patch("services.sizing_service.get_latest_snapshot", return_value=MOCK_SNAPSHOT),
            patch("services.sizing_service.get_settings", return_value=[]),
            patch("services.sizing_service.get_ticker_sector", return_value="Technology"),
            patch("services.sizing_service.get_sector_exposure", return_value={
                "sector_value_gbp": 6800.0, "total_portfolio_value_gbp": 20000.0,
                "position_count": 3, "fx_rate": 1.0,
            }),
            patch("services.sizing_service.calculate_prospective_heat") as mock_heat,
        ):
            result = _size(ticker="MSFT")

        assert result["suggested_shares"] == 0.0
        assert result["heat_impact_percent"] is None
        mock_heat.assert_not_called()  # short-circuits before calling — nothing to price

    def test_heat_calculation_unavailable_returns_none(self):
        with _base_patches({"valid": False, "error": "portfolio value is zero; cannot calculate heat"}):
            result = _size()

        assert result["valid"] is True  # sizing itself still succeeds
        assert result["heat_impact_percent"] is None

    def test_heat_calculation_exception_does_not_break_sizing(self):
        with (
            patch("services.sizing_service.get_portfolio", return_value=MOCK_PORTFOLIO),
            patch("services.sizing_service.get_latest_snapshot", return_value=MOCK_SNAPSHOT),
            patch("services.sizing_service.get_settings", return_value=[]),
            patch("services.sizing_service.calculate_prospective_heat", side_effect=Exception("boom")),
        ):
            result = _size()

        assert result["valid"] is True
        assert result["heat_impact_percent"] is None
