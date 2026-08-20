"""
ST-04 regression tests (BLG-BE-104, EPIC-02, v8.9).

Position Sizing Calculator (POST /portfolio/size, sizing_service.size_position)
extended to reduce or flag a candidate position's suggested size when it would
push sector exposure toward/past strategy_rules.md §4.2.2's canonical 30%
sector-concentration threshold, reflecting the user's *existing open-position*
sector concentration rather than just the candidate ticker's own volatility.

Design record: docs/design/2026-08-17__release-v8.9/correlation-sector-concentration-sizing/decision_record.md

Core AC-03 test (TestConcentrationVsUncorrelated) confirms two same-sector
(correlated) positions produce a smaller second suggested size than two
uncorrelated positions would, for otherwise-identical sizing inputs.

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
MOCK_SNAPSHOT = {"total_value": 20000.0}  # portfolio_value used for risk basis


def _size(ticker=None, entry_price=100.0, stop_price=90.0, risk_percent=1.0):
    """Baseline sizing call: risk_amount=200, stop_distance=10, raw_shares=20 (UK, fx=1.0)."""
    return sizing_service.size_position(
        entry_price=entry_price,
        stop_price=stop_price,
        risk_percent=risk_percent,
        market="UK",
        ticker=ticker,
    )


def _patches(sector, exposure):
    """ExitStack of the standard mocks for a full size_position() call with
    concentration adjustment enabled. Use as a context manager."""
    stack = ExitStack()
    stack.enter_context(patch("services.sizing_service.get_portfolio", return_value=MOCK_PORTFOLIO))
    stack.enter_context(patch("services.sizing_service.get_latest_snapshot", return_value=MOCK_SNAPSHOT))
    stack.enter_context(patch("services.sizing_service.get_settings", return_value=[]))
    stack.enter_context(patch("services.sizing_service.get_ticker_sector", return_value=sector))
    stack.enter_context(patch("services.sizing_service.get_sector_exposure", return_value=exposure))
    return stack


class TestNoTickerBackwardCompatible:
    """Omitting ticker must reproduce pre-ST-04 sizing behaviour exactly."""

    def test_no_ticker_no_adjustment(self):
        with (
            patch("services.sizing_service.get_portfolio", return_value=MOCK_PORTFOLIO),
            patch("services.sizing_service.get_latest_snapshot", return_value=MOCK_SNAPSHOT),
            patch("services.sizing_service.get_settings", return_value=[]),
        ):
            result = _size(ticker=None)

        assert result["valid"] is True
        assert result["suggested_shares"] == 20.0
        assert result["concentration_adjusted"] is False
        assert result["concentration_reason"] is None


class TestConcentrationVsUncorrelated:
    """AC-03: two same-sector (correlated) positions produce a smaller second
    size than two uncorrelated positions would, for identical sizing inputs."""

    def test_correlated_sector_reduces_size_below_uncorrelated(self):
        # Correlated: 2 existing Technology positions, 25% of portfolio (5000/20000).
        # Candidate (also Technology) would add another 2000 GBP (10%) -> projected 35%,
        # over the 30% canonical threshold -> capped.
        correlated_exposure = {
            "sector_value_gbp": 5000.0,
            "total_portfolio_value_gbp": 20000.0,
            "position_count": 2,
            "fx_rate": 1.0,
        }
        with _patches("Technology", correlated_exposure):
            correlated_result = _size(ticker="MSFT")

        # Uncorrelated: candidate's sector has zero existing exposure.
        uncorrelated_exposure = {
            "sector_value_gbp": 0.0,
            "total_portfolio_value_gbp": 20000.0,
            "position_count": 0,
            "fx_rate": 1.0,
        }
        with _patches("Healthcare", uncorrelated_exposure):
            uncorrelated_result = _size(ticker="JNJ")

        assert correlated_result["valid"] is True
        assert uncorrelated_result["valid"] is True
        assert correlated_result["suggested_shares"] < uncorrelated_result["suggested_shares"]
        assert uncorrelated_result["suggested_shares"] == 20.0  # baseline, unadjusted

    def test_reduction_math_and_reason_string(self):
        exposure = {
            "sector_value_gbp": 5000.0,
            "total_portfolio_value_gbp": 20000.0,
            "position_count": 2,
            "fx_rate": 1.0,
        }
        with _patches("Technology", exposure):
            result = _size(ticker="MSFT")

        # max_new_value_gbp = 0.30*20000 - 5000 = 1000; capped_shares = 1000/100 = 10.0
        assert result["suggested_shares"] == 10.0
        assert result["concentration_adjusted"] is True
        assert result["concentration_reason"] == (
            "Reduced 50% — 2 open positions already in Technology (25.0% of portfolio value)."
        )

    def test_estimated_cost_reflects_reduced_shares(self):
        """Fees/cost downstream of the adjustment must use the final (reduced)
        share count, not the pre-adjustment baseline (design_record.md §2)."""
        exposure = {
            "sector_value_gbp": 5000.0,
            "total_portfolio_value_gbp": 20000.0,
            "position_count": 2,
            "fx_rate": 1.0,
        }
        with _patches("Technology", exposure):
            result = _size(ticker="MSFT")

        # 10 shares * 100 entry_price = 1000 gross (no fee-affecting settings mocked -> defaults)
        assert result["estimated_cost"] < 2000.0  # would be ~2000+ at the unreduced 20 shares


class TestConcentrationFlaggedNotReduced:
    """Design record §2: a position may be flagged (concentration_reason set)
    without concentration_adjusted becoming true, when projected exposure is
    elevated but below the canonical reduce threshold."""

    def test_elevated_exposure_flags_without_reducing(self):
        exposure = {
            "sector_value_gbp": 2000.0,  # 10% pre-existing
            "total_portfolio_value_gbp": 20000.0,
            "position_count": 2,
            "fx_rate": 1.0,
        }
        # Candidate adds 2000 (10%) -> projected 20.0%: at the WARN threshold, below 30%.
        with _patches("Technology", exposure):
            result = _size(ticker="MSFT")

        assert result["suggested_shares"] == 20.0  # unchanged
        assert result["concentration_adjusted"] is False
        assert result["concentration_reason"] == (
            "2 open positions already in Technology (10.0% of portfolio value) — "
            "approaching 30% concentration limit."
        )


class TestConcentrationEdgeCases:
    def test_no_sector_data_no_adjustment(self):
        with _patches(None, None):
            result = _size(ticker="UNKNOWN")

        assert result["suggested_shares"] == 20.0
        assert result["concentration_adjusted"] is False
        assert result["concentration_reason"] is None

    def test_zero_existing_positions_in_sector_no_adjustment(self):
        exposure = {
            "sector_value_gbp": 0.0,
            "total_portfolio_value_gbp": 20000.0,
            "position_count": 0,
            "fx_rate": 1.0,
        }
        with _patches("Technology", exposure):
            result = _size(ticker="MSFT")

        assert result["suggested_shares"] == 20.0
        assert result["concentration_adjusted"] is False
        assert result["concentration_reason"] is None

    def test_sector_already_fully_saturated_caps_to_zero(self):
        """Pre-existing sector exposure already at/above the 30% cap on its own
        (independent of the candidate) -> candidate is capped to 0, not a
        negative or nonsensical value."""
        exposure = {
            "sector_value_gbp": 6800.0,  # 34% pre-existing, already over cap
            "total_portfolio_value_gbp": 20000.0,
            "position_count": 3,
            "fx_rate": 1.0,
        }
        with _patches("Technology", exposure):
            result = _size(ticker="MSFT")

        assert result["suggested_shares"] == 0.0
        assert result["concentration_adjusted"] is True
        assert "Reduced 100%" in result["concentration_reason"]

    def test_invalid_sizing_input_skips_concentration_entirely(self):
        """Invalid inputs (§4.1.4) short-circuit before concentration logic runs."""
        with (
            patch("services.sizing_service.get_portfolio", return_value=MOCK_PORTFOLIO),
        ):
            result = _size(ticker="MSFT", stop_price=110.0)  # stop >= entry -> invalid

        assert result["valid"] is False
        assert "concentration_adjusted" not in result
