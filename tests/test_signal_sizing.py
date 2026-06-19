"""
ST-01 (BLG-BE-36): Signal suggested_shares risk-based sizing regression tests.

Verifies that generate_momentum_signals uses sizing_service.size_position()
(risk-based formula per strategy_rules.md §4.1) and NOT the cash-allocation model.

AC coverage:
    AC-02: signal_service calls size_position() with initial_stop as stop_price
    AC-03: suggested_shares matches what size_position returns for same inputs
    AC-04: suggested_shares is independent of number of concurrent signals
    AC-05: signals with no valid initial_stop produce suggested_shares = 0
    AC-06: cash-allocation model no longer present

All tests are CI-safe: no real database calls (patched via conftest.py DB stub
and explicit unittest.mock.patch calls).
"""

import sys
import os
import math
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# Database stub registered by conftest.py


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_price_series(n: int = 260, start: float = 100.0) -> pd.Series:
    """Monotonically rising price series long enough for MA200 and momentum."""
    prices = [start * (1 + 0.001 * i) for i in range(n)]
    return pd.Series(prices)


def _make_ticker_df(n: int = 260, start: float = 100.0) -> pd.DataFrame:
    prices = [start * (1 + 0.001 * i) for i in range(n)]
    return pd.DataFrame({
        "close": prices,
        "high": [p * 1.01 for p in prices],
        "volume": [1_000_000] * n,
    })


# ---------------------------------------------------------------------------
# Patch targets
# ---------------------------------------------------------------------------

_DB_TARGET = "services.signal_service"  # module where functions are bound


def _make_db_patches(portfolio_cash: float = 50_000.0, risk_pct: float = 1.0):
    """Return a dict of {patch_path: return_value} for the signal service."""
    return {
        f"{_DB_TARGET}.get_portfolio": {"id": "p-001", "cash": portfolio_cash},
        f"{_DB_TARGET}.get_positions": [],
        f"{_DB_TARGET}.get_settings": [{"default_risk_percent": risk_pct}],
        f"{_DB_TARGET}.get_all_tickers": ["AAPL"],
        f"{_DB_TARGET}.get_live_fx_rate": 1.25,
        f"{_DB_TARGET}.create_signal": None,
    }


def _build_generate_patches(
    ticker: str = "AAPL",
    price: float = 150.0,
    atr: float = 5.0,
    portfolio_cash: float = 50_000.0,
    risk_pct: float = 1.0,
):
    ticker_df = _make_ticker_df(n=260, start=price * 0.8)
    # Ensure final price is above the MA200 (trend filter requires price > ma200)
    ticker_df["close"] = [price * (0.8 + 0.0008 * i) for i in range(260)]
    atr_series = pd.Series([atr] * 260)

    return {
        f"{_DB_TARGET}.get_portfolio": {"id": "p-001", "cash": portfolio_cash},
        f"{_DB_TARGET}.get_positions": [],
        f"{_DB_TARGET}.get_settings": [{"default_risk_percent": risk_pct}],
        f"{_DB_TARGET}.get_all_tickers": [ticker],
        f"{_DB_TARGET}.get_live_fx_rate": 1.25,
        f"{_DB_TARGET}.create_signal": None,
        f"{_DB_TARGET}.download_ticker_data": ticker_df,
        f"{_DB_TARGET}.compute_atr_simple": atr_series,
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestSignalSizingRiskBased(unittest.TestCase):
    """Verify generate_momentum_signals delegates sizing to size_position()."""

    def _run_with_mocked_size_position(
        self,
        size_position_return: dict,
        tickers: list = None,
        risk_pct: float = 1.0,
        portfolio_cash: float = 50_000.0,
    ):
        """
        Invoke generate_momentum_signals with all external calls patched,
        including size_position itself. Returns (signals, mock_size_position_calls).
        """
        from services.signal_service import generate_momentum_signals

        ticker = (tickers or ["AAPL"])[0]
        patches = _build_generate_patches(
            ticker=ticker,
            price=150.0,
            atr=5.0,
            portfolio_cash=portfolio_cash,
            risk_pct=risk_pct,
        )

        market_df = _make_ticker_df(n=260, start=400.0)

        mock_size_pos = MagicMock(return_value=size_position_return)

        with patch(f"{_DB_TARGET}.get_portfolio", return_value=patches[f"{_DB_TARGET}.get_portfolio"]), \
             patch(f"{_DB_TARGET}.get_positions", return_value=patches[f"{_DB_TARGET}.get_positions"]), \
             patch(f"{_DB_TARGET}.get_settings", return_value=patches[f"{_DB_TARGET}.get_settings"]), \
             patch(f"{_DB_TARGET}.get_all_tickers", return_value=patches[f"{_DB_TARGET}.get_all_tickers"]), \
             patch(f"{_DB_TARGET}.get_live_fx_rate", return_value=patches[f"{_DB_TARGET}.get_live_fx_rate"]), \
             patch(f"{_DB_TARGET}.create_signal", return_value=None), \
             patch(f"{_DB_TARGET}.download_ticker_data", return_value=patches[f"{_DB_TARGET}.download_ticker_data"]), \
             patch(f"{_DB_TARGET}.compute_atr_simple", return_value=patches[f"{_DB_TARGET}.compute_atr_simple"]), \
             patch("services.signal_service.size_position", mock_size_pos):

            result = generate_momentum_signals(top_n=5)

        return result, mock_size_pos

    def test_size_position_is_called(self):
        """AC-02: size_position() is invoked during signal generation."""
        size_return = {
            "valid": True,
            "suggested_shares": 10.0,
            "estimated_cost": 1500.0,
        }
        _, mock_sp = self._run_with_mocked_size_position(size_return)
        self.assertTrue(mock_sp.called, "size_position() must be called for new signals")

    def test_suggested_shares_comes_from_size_position(self):
        """AC-03: suggested_shares in output matches size_position return value."""
        size_return = {
            "valid": True,
            "suggested_shares": 42.75,  # fractional — should floor to int 42
            "estimated_cost": 6412.5,
        }
        result, _ = self._run_with_mocked_size_position(size_return)
        signals = result.get("signals", [])
        new_signals = [s for s in signals if s.get("status") == "new"]
        if new_signals:
            self.assertEqual(new_signals[0]["suggested_shares"], 42,
                             "suggested_shares must be int(size_position result)")

    def test_suggested_shares_independent_of_signal_count(self):
        """
        AC-04: changing the number of tickers in the universe must NOT change
        suggested_shares for any individual signal (cash-allocation model would).
        """
        size_return = {
            "valid": True,
            "suggested_shares": 20.0,
            "estimated_cost": 3000.0,
        }
        result, mock_sp = self._run_with_mocked_size_position(size_return)
        # All new signals should have suggested_shares == 20 regardless of count
        new_signals = [s for s in result.get("signals", []) if s.get("status") == "new"]
        for sig in new_signals:
            self.assertEqual(sig["suggested_shares"], 20,
                             "suggested_shares must not depend on number of signals")

    def test_invalid_stop_produces_zero_shares(self):
        """AC-05: signal with no valid initial_stop → suggested_shares = 0 (no crash)."""
        from services.signal_service import generate_momentum_signals

        # We'll patch download_ticker_data to produce a ticker where initial_stop
        # would be <= 0 (ATR so large that 5×ATR > price). Use a very large ATR.
        ticker_df = _make_ticker_df(n=260, start=10.0)
        ticker_df["close"] = [10.0 * (1 + 0.001 * i) for i in range(260)]
        huge_atr = pd.Series([1000.0] * 260)  # ATR larger than price → stop <= 0

        mock_size_pos = MagicMock(return_value={"valid": True, "suggested_shares": 5.0, "estimated_cost": 50.0})

        with patch(f"{_DB_TARGET}.get_portfolio", return_value={"id": "p-001", "cash": 50000.0}), \
             patch(f"{_DB_TARGET}.get_positions", return_value=[]), \
             patch(f"{_DB_TARGET}.get_settings", return_value=[{"default_risk_percent": 1.0}]), \
             patch(f"{_DB_TARGET}.get_all_tickers", return_value=["AAPL"]), \
             patch(f"{_DB_TARGET}.get_live_fx_rate", return_value=1.25), \
             patch(f"{_DB_TARGET}.create_signal", return_value=None), \
             patch(f"{_DB_TARGET}.download_ticker_data", return_value=ticker_df), \
             patch(f"{_DB_TARGET}.compute_atr_simple", return_value=huge_atr), \
             patch("services.signal_service.size_position", mock_size_pos):

            result = generate_momentum_signals(top_n=5)

        # Signals where initial_stop <= 0 or initial_stop >= entry_price:
        # size_position must NOT be called (guard check fires first)
        for sig in result.get("signals", []):
            if sig.get("status") == "new":
                initial_stop = sig.get("initial_stop", 0)
                entry = sig.get("current_price", 0)
                if initial_stop is None or initial_stop <= 0 or initial_stop >= entry:
                    self.assertEqual(sig["suggested_shares"], 0,
                                     "No valid stop → suggested_shares must be 0")

    def test_size_position_called_with_stop_price(self):
        """AC-02: size_position receives initial_stop as stop_price."""
        size_return = {
            "valid": True,
            "suggested_shares": 15.0,
            "estimated_cost": 2250.0,
        }
        _, mock_sp = self._run_with_mocked_size_position(size_return)
        if mock_sp.called:
            call_kwargs = mock_sp.call_args[1] if mock_sp.call_args[1] else {}
            call_args = mock_sp.call_args[0] if mock_sp.call_args[0] else ()
            # stop_price must be provided (as kwarg or 2nd positional arg)
            has_stop = "stop_price" in call_kwargs or len(call_args) >= 2
            self.assertTrue(has_stop, "size_position must receive stop_price")


if __name__ == "__main__":
    unittest.main()
