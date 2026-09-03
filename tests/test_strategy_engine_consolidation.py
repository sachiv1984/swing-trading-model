"""
ST-05 (BLG-TECH-15, EPIC-01, v9.0) consolidation regression test.

Proves the new single shared implementation
(backend/services/strategy_engine.py) produces identical results to BOTH
pre-consolidation implementations — production_strategy.py's backtest()
(which read regime state from module globals) and
backend/services/backtest_rule_service.py's run_backtest() (which already
took regime state as explicit parameters) — on a fixed, deterministic
synthetic dataset. This is the best available proxy for "a fixed historical
run": the real nightly backtest needs live yfinance data over ~8 years for
100+ tickers and is budgeted 90 minutes of CI compute, categorically
infeasible inside a test suite (same constraint class documented in
backtest_rule_service.py's own module docstring, RISK-02).

The pre-consolidation source is loaded directly from git history (the last
commit before this consolidation) via importlib/exec, rather than kept as a
literal second copy in this repo — retaining a copy of the very duplication
BLG-TECH-15 exists to eliminate would defeat the point of the fix.
"""
import subprocess
import sys
import types
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "backend"))

# [EPIC-01][ST-04] commit — last commit on this branch before the ST-05
# consolidation. Both production_strategy.py and backend/services/
# backtest_rule_service.py at this SHA already carry ST-01's independent
# BLG-BE-109 fix (compute_rebalance_dates/as_of), applied to both files
# before this consolidation existed — so this comparison isolates exactly
# the ST-05 change (single implementation, explicit regime params, added
# "Initial Stop" tracking) from the earlier ST-01 change.
PRE_CONSOLIDATION_SHA = "c6b9c950"


def _load_module_from_git(path: str, module_name: str) -> types.ModuleType:
    result = subprocess.run(
        ["git", "show", f"{PRE_CONSOLIDATION_SHA}:{path}"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    if result.returncode != 0:
        pytest.skip(f"could not read {path} @ {PRE_CONSOLIDATION_SHA} from git: {result.stderr}")
    module = types.ModuleType(module_name)
    module.__file__ = str(REPO_ROOT / path)
    sys.modules[module_name] = module
    exec(compile(result.stdout, str(REPO_ROOT / path), "exec"), module.__dict__)
    return module


@pytest.fixture(scope="module")
def old_production_strategy():
    return _load_module_from_git("production_strategy.py", "_old_production_strategy_st05")


@pytest.fixture(scope="module")
def old_backtest_rule_service():
    return _load_module_from_git(
        "backend/services/backtest_rule_service.py", "_old_backtest_rule_service_st05"
    )


def _synthetic_dataset(n_days=300, tickers=("AAA", "BBB", "CCC", "DDD.L")):
    idx = pd.bdate_range("2023-01-02", periods=n_days)
    rng = np.random.default_rng(7)
    data = {}
    for i, t in enumerate(tickers):
        base = 100 + i * 15
        walk = rng.normal(0.0005, 0.015, n_days).cumsum()
        data[t] = base * (1 + walk)
    return pd.DataFrame(data, index=idx)


# Far in the future relative to the synthetic dataset (2023-2024), so
# compute_rebalance_dates never excludes anything as "the current,
# in-progress period" — isolates the ST-05 comparison from ST-01's
# unrelated behaviour.
_AS_OF = pd.Timestamp("2099-01-01")

_KWARGS = dict(
    rebalance_freq="ME", atr_mult=2, min_position_pct=0.05,
    max_position_pct=0.20, min_hold_days=5, risk_off_mode="single",
    stop_loss_mode="profit_lock", initial_atr_mult=5, profit_atr_mult=2,
    as_of=_AS_OF,
)


class TestConsolidationParityAgainstProductionStrategy:
    def test_new_backtest_matches_old_production_strategy_backtest(
        self, old_production_strategy, monkeypatch
    ):
        from services import strategy_engine as new_se

        prices = _synthetic_dataset()
        atr = new_se.compute_atr(prices)
        signals = new_se.compute_signals(prices, lookback=60, top_n=2, ma_period=50)
        volatility = prices.pct_change().rolling(20).std()
        regime_us = pd.Series(True, index=prices.index)
        regime_uk = pd.Series(True, index=prices.index)

        # OLD: production_strategy.py's backtest() reads regime state from
        # module globals, set here the same way its own main() sets them.
        monkeypatch.setattr(old_production_strategy, "spy_risk_on", regime_us, raising=False)
        monkeypatch.setattr(old_production_strategy, "ftse_risk_on", regime_uk, raising=False)
        old_pv, old_returns, old_trades = old_production_strategy.backtest(
            signals, prices, volatility, atr, **_KWARGS
        )

        # NEW: shared strategy_engine.backtest() takes regime state explicitly.
        new_pv, new_returns, new_trades = new_se.backtest(
            signals, prices, volatility, atr, regime_us, regime_uk, **_KWARGS
        )

        pd.testing.assert_series_equal(old_pv, new_pv)
        pd.testing.assert_series_equal(old_returns, new_returns)
        assert len(old_trades) > 0, "synthetic dataset must actually exercise trade logic"
        # New trades carry one additional column ("Initial Stop") the old
        # production_strategy.py implementation never tracked — purely
        # additive (strategy_engine.py module docstring note 2).
        pd.testing.assert_frame_equal(
            old_trades.reset_index(drop=True),
            new_trades.drop(columns=["Initial Stop"]).reset_index(drop=True),
        )


class TestConsolidationParityAgainstBacktestRuleService:
    def test_new_backtest_matches_old_run_backtest(self, old_backtest_rule_service):
        from services import strategy_engine as new_se

        prices = _synthetic_dataset()
        atr = new_se.compute_atr(prices)
        signals = new_se.compute_signals(prices, lookback=60, top_n=2, ma_period=50)
        volatility = prices.pct_change().rolling(20).std()
        regime_us = pd.Series(True, index=prices.index)
        regime_uk = pd.Series(True, index=prices.index)

        old_pv, old_returns, old_trades = old_backtest_rule_service.run_backtest(
            signals, prices, volatility, atr, regime_us, regime_uk, **_KWARGS
        )
        new_pv, new_returns, new_trades = new_se.backtest(
            signals, prices, volatility, atr, regime_us, regime_uk, **_KWARGS
        )

        pd.testing.assert_series_equal(old_pv, new_pv)
        pd.testing.assert_series_equal(old_returns, new_returns)
        assert len(old_trades) > 0, "synthetic dataset must actually exercise trade logic"

        # Old backend trades use lower_snake_case column names; map the new
        # canonical capitalized schema down to the same shape/order first.
        column_map = {
            "Ticker": "ticker", "Entry Date": "entry_date", "Exit Date": "exit_date",
            "Holding Days": "holding_days", "Entry": "entry_price", "Exit": "exit_price",
            "Initial Stop": "initial_stop_price", "PnL (£)": "pnl_gbp", "PnL %": "pnl_pct",
            "Market": "market", "Exit Reason": "exit_reason", "Was Profitable": "was_profitable",
        }
        new_trades_mapped = new_trades.rename(columns=column_map)[list(old_trades.columns)]
        pd.testing.assert_frame_equal(
            old_trades.reset_index(drop=True),
            new_trades_mapped.reset_index(drop=True),
        )
