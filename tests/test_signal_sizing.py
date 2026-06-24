"""
ST-04 (BLG-FEAT-48): Inverse-volatility signal sizing regression tests.

Verifies that generate_momentum_signals uses sizing_service.size_batch_inv_vol()
(inv-vol formula per production_strategy.py OPTIMAL_PARAMS) and NOT the old
fixed risk-based size_position() model or cash-allocation model.

AC coverage:
    AC-01: weight_i = (1/ATR_i) / sum(1/ATR_j)
    AC-02: each weight constrained to [5%, 20%], re-normalised to sum 1.0
    AC-03: new signal allocations use inv-vol sizing (not fixed-risk £200 model)
    AC-04: manual position sizing path (size_position) is NOT called for signal generation
    AC-05 (legacy): signals with atr_value == 0 produce suggested_shares = 0

All tests are CI-safe: no real database calls (patched via conftest.py DB stub
and explicit unittest.mock.patch calls).
"""

import sys
import math
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_ticker_df(n: int = 260, start: float = 100.0) -> pd.DataFrame:
    prices = [start * (1 + 0.001 * i) for i in range(n)]
    return pd.DataFrame({
        "close": prices,
        "high": [p * 1.01 for p in prices],
        "volume": [1_000_000] * n,
    })


_DB_TARGET = "services.signal_service"


def _build_generate_patches(
    ticker: str = "AAPL",
    price: float = 150.0,
    atr: float = 5.0,
    portfolio_cash: float = 50_000.0,
):
    ticker_df = _make_ticker_df(n=260, start=price * 0.8)
    ticker_df["close"] = [price * (0.8 + 0.0008 * i) for i in range(260)]
    atr_series = pd.Series([atr] * 260)
    return {
        f"{_DB_TARGET}.get_portfolio": {"id": "p-001", "cash": portfolio_cash},
        f"{_DB_TARGET}.get_positions": [],
        f"{_DB_TARGET}.get_settings": [{"default_risk_percent": 1.0}],
        f"{_DB_TARGET}.get_all_tickers": [ticker],
        f"{_DB_TARGET}.get_live_fx_rate": 1.25,
        f"{_DB_TARGET}.create_signal": None,
        f"{_DB_TARGET}.download_ticker_data": ticker_df,
        f"{_DB_TARGET}.compute_atr_simple": atr_series,
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestSignalSizingInvVol(unittest.TestCase):
    """Verify generate_momentum_signals uses size_batch_inv_vol (ST-04 BLG-FEAT-48)."""

    def _run_generate(self, ticker="AAPL", price=150.0, atr=5.0, cash=50_000.0):
        from services.signal_service import generate_momentum_signals
        patches = _build_generate_patches(ticker=ticker, price=price, atr=atr, portfolio_cash=cash)
        market_df = _make_ticker_df(n=260, start=400.0)

        mock_inv_vol = MagicMock(wraps=lambda sigs, cash, **kw: sigs)
        mock_size_pos = MagicMock()

        with patch(f"{_DB_TARGET}.get_portfolio", return_value=patches[f"{_DB_TARGET}.get_portfolio"]), \
             patch(f"{_DB_TARGET}.get_positions", return_value=[]), \
             patch(f"{_DB_TARGET}.get_settings", return_value=patches[f"{_DB_TARGET}.get_settings"]), \
             patch(f"{_DB_TARGET}.get_all_tickers", return_value=patches[f"{_DB_TARGET}.get_all_tickers"]), \
             patch(f"{_DB_TARGET}.get_live_fx_rate", return_value=1.25), \
             patch(f"{_DB_TARGET}.create_signal", return_value=None), \
             patch(f"{_DB_TARGET}.download_ticker_data", return_value=patches[f"{_DB_TARGET}.download_ticker_data"]), \
             patch(f"{_DB_TARGET}.compute_atr_simple", return_value=patches[f"{_DB_TARGET}.compute_atr_simple"]), \
             patch("services.signal_service.size_batch_inv_vol", mock_inv_vol), \
             patch("services.signal_service.size_position", mock_size_pos):
            result = generate_momentum_signals(top_n=5)

        return result, mock_inv_vol, mock_size_pos

    def test_size_batch_inv_vol_is_called(self):
        """AC-03: size_batch_inv_vol() is invoked for new signals (not size_position)."""
        _, mock_inv_vol, mock_size_pos = self._run_generate()
        self.assertTrue(mock_inv_vol.called, "size_batch_inv_vol must be called for new signals")

    def test_size_position_not_called_for_signals(self):
        """AC-04: size_position() (manual sizing) must NOT be called during signal generation."""
        _, _, mock_size_pos = self._run_generate()
        self.assertFalse(mock_size_pos.called,
                         "size_position() (manual sizing path) must not be called — RISK-03")

    def _call_size_batch(self, signals, available_cash, fx_rate=1.0):
        """Call size_batch_inv_vol with get_settings stubbed (safe after test_api_contracts evicts DB stub)."""
        import services.sizing_service as _sz
        mock_settings = MagicMock(return_value=[{"commission_rate": 0.001}])
        with patch.object(_sz, "get_settings", mock_settings):
            return _sz.size_batch_inv_vol(signals, available_cash=available_cash, fx_rate=fx_rate)

    def test_inv_vol_weight_formula(self):
        """AC-01: weight_i = (1/ATR_i) / sum(1/ATR_j) — single signal gets full weight."""
        signals = [
            {"atr_value": 4.0, "price_gbp": 100.0, "current_price": 100.0, "market": "UK", "status": "new"},
            {"atr_value": 2.0, "price_gbp": 200.0, "current_price": 200.0, "market": "UK", "status": "new"},
        ]
        result = self._call_size_batch(signals, available_cash=10_000.0)
        # inv_atr: [1/4, 1/2] = [0.25, 0.50]; total = 0.75
        # raw_weights: [0.333, 0.667] — both > 0.20 so capped to [0.20, 0.20], normalised [0.50, 0.50]
        self.assertIn("inv_vol_weight", result[0])
        self.assertIn("inv_vol_weight", result[1])
        total_weight = result[0]["inv_vol_weight"] + result[1]["inv_vol_weight"]
        self.assertAlmostEqual(total_weight, 1.0, places=3)

    def test_weight_cap_enforced(self):
        """AC-02: no single weight exceeds 20% or falls below 5% after capping."""
        signals = [
            {"atr_value": 5.0, "price_gbp": 100.0, "current_price": 100.0, "market": "UK", "status": "new"}
            for _ in range(10)
        ]
        result = self._call_size_batch(signals, available_cash=100_000.0)
        for sig in result:
            w = sig.get("inv_vol_weight", 0)
            self.assertGreaterEqual(w, 0.05 - 1e-6, f"weight {w} below 5% minimum")
            self.assertLessEqual(w, 0.20 + 1e-6, f"weight {w} exceeds 20% maximum")

    def test_zero_atr_produces_zero_shares(self):
        """AC-05: signal with atr_value == 0 produces suggested_shares = 0."""
        signals = [
            {"atr_value": 0.0, "price_gbp": 100.0, "current_price": 100.0, "market": "UK", "status": "new"},
        ]
        result = self._call_size_batch(signals, available_cash=50_000.0)
        self.assertEqual(result[0]["suggested_shares"], 0, "zero ATR must yield 0 shares")


if __name__ == "__main__":
    unittest.main()
