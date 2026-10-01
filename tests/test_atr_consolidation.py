"""
ST-01, EPIC-01, v9.9, BLG-BE-135: ATR implementation consolidation.

Confirms the close-to-close ATR approximation formerly duplicated across
services/strategy_engine.py::compute_atr and database.py::compute_atr_simple
now both delegate to the single canonical
utils.pricing.compute_atr_close_approximation, and produce numerically
identical output to the pre-consolidation formulas (no behaviour change).

Does not cover utils/pricing.py::calculate_atr or
services/screener_engine.py::compute_atr -- those are deliberately distinct,
real-OHLC formulas per strategy_rules.md §7.1's RISK-01 ruling, not part of
this consolidation.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from services.strategy_engine import compute_atr

# NOTE: utils.pricing is deliberately NOT imported at module level here.
# tests/test_alerts_service.py and tests/test_trade_service.py replace
# sys.modules["utils.pricing"] with a MagicMock stub at THEIR module-import
# time (restored only via a fixture that fires during test execution, not
# during pytest's upfront collection phase) -- a top-level import in this
# file would race that stub during collection, depending on file collection
# order. Importing inside each test function instead defers to run time,
# after any such stub has already been restored. See ST-14 (this sprint)
# for the broader cleanup of this sys.modules swap pattern across the suite.


def _sample_prices(n=30, seed=7):
    rng = np.random.default_rng(seed)
    return pd.Series(100 + np.cumsum(rng.normal(0, 1, n)))


def _load_real_database_module():
    """Load backend/database.py as an independent module object, isolated
    from tests/conftest.py's sys.modules["database"] MagicMock stub (which
    would otherwise shadow compute_atr_simple). Does NOT touch sys.modules
    globally -- avoids the unrestored-swap leakage pattern ST-14 (this same
    sprint) is clearing from other test files."""
    backend_dir = Path(__file__).parent.parent / "backend"
    spec = importlib.util.spec_from_file_location("database_real_copy_for_test", backend_dir / "database.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestCanonicalCloseApproximation:

    def test_compute_atr_simple_delegates_to_canonical(self):
        from utils.pricing import compute_atr_close_approximation
        prices = _sample_prices()
        expected = compute_atr_close_approximation(prices, 14)
        real_database = _load_real_database_module()
        actual = real_database.compute_atr_simple(prices, 14)
        pd.testing.assert_series_equal(actual, expected)

    def test_strategy_engine_compute_atr_matches_canonical_per_column(self):
        from utils.pricing import compute_atr_close_approximation
        df = pd.DataFrame({
            "AAA": _sample_prices(seed=1),
            "BBB": _sample_prices(seed=2),
        })
        result = compute_atr(df)
        for col in df.columns:
            expected = compute_atr_close_approximation(df[col], 14)
            pd.testing.assert_series_equal(result[col], expected, check_names=False)

    def test_pre_consolidation_formula_unchanged(self):
        """Pins the exact pre-refactor formula so a future edit to the
        canonical function can't silently change backtest/signal output."""
        from utils.pricing import compute_atr_close_approximation
        prices = _sample_prices()
        close_to_close = prices.diff().abs()
        pre_refactor = close_to_close.rolling(window=14, min_periods=14).mean()
        pd.testing.assert_series_equal(
            compute_atr_close_approximation(prices, 14), pre_refactor
        )
