"""
ST-07 regression tests (BLG-FEAT-89, EPIC-02, v8.9).

In-app Backtest Rule Change engine (services/backtest_rule_service.py).
Verifies: bounded-universe/window scoping, candidate-vs-live comparison
math (win rate, R-multiple buckets, max drawdown), unknown-parameter
rejection, and the persisted-run field shape (AC-03).

CI-safe: yfinance downloads and database calls are mocked with small
synthetic price series. No live network or DB connections.
"""
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import services.backtest_rule_service as svc  # noqa: E402


# ---------------------------------------------------------------------------
# Synthetic price fixture — 3 tickers, ~500 trading days, deterministic
# ---------------------------------------------------------------------------

def _synthetic_prices(n_days=500, tickers=("AAPL", "MSFT", "VOD.L")):
    dates = pd.bdate_range("2024-01-02", periods=n_days)
    rng = np.random.default_rng(42)
    data = {}
    for i, t in enumerate(tickers):
        # Gentle uptrend + noise, deterministic seed -> reproducible test data
        base = 100 + i * 20
        walk = rng.normal(0.0006, 0.012, n_days).cumsum()
        data[t] = base * (1 + walk)
    return pd.DataFrame(data, index=dates)


class TestPureFunctions:
    def test_compute_signals_shape(self):
        prices = _synthetic_prices()
        signals = svc.compute_signals(prices, lookback=60, top_n=2)
        assert signals.shape == prices.shape
        assert signals.dtypes.apply(lambda d: d == bool).all()

    def test_compute_atr_shape(self):
        prices = _synthetic_prices()
        atr = svc.compute_atr(prices)
        assert atr.shape == prices.shape

    def test_transaction_fee_uk_vs_us(self):
        assert svc.transaction_fee("VOD.L", "buy") == 0.005
        assert svc.transaction_fee("VOD.L", "sell") == 0.0
        assert svc.transaction_fee("AAPL", "buy") == 0.0015
        assert svc.transaction_fee("AAPL", "sell") == 0.0015

    def test_bucket_r_multiples_covers_all_ranges(self):
        r_values = [-4.0, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 4.0]
        buckets = svc._bucket_r_multiples(r_values)
        assert len(buckets) == 8
        assert sum(b["count"] for b in buckets) == 8
        labels = [b["label"] for b in buckets]
        assert labels == ["< -3R", "-3R to -2R", "-2R to -1R", "-1R to 0R",
                           "0R to 1R", "1R to 2R", "2R to 3R", "> 3R"]

    def test_bucket_boundary_is_half_open(self):
        # -2.0 belongs to "-2R to -1R" (lo <= r < hi), not "-3R to -2R"
        buckets = svc._bucket_r_multiples([-2.0])
        counts = {b["label"]: b["count"] for b in buckets}
        assert counts["-2R to -1R"] == 1
        assert counts["-3R to -2R"] == 0

    def test_r_multiples_excludes_trades_without_qualifying_stop(self):
        trades_df = pd.DataFrame([
            {"entry_price": 100.0, "exit_price": 110.0, "initial_stop_price": 90.0},   # R = 1.0
            {"entry_price": 100.0, "exit_price": 90.0, "initial_stop_price": None},     # excluded: no stop
            {"entry_price": 100.0, "exit_price": 95.0, "initial_stop_price": 100.0},    # excluded: entry <= stop
        ])
        r_values = svc._r_multiples(trades_df)
        assert r_values == [1.0]

    def test_diff_summary_no_changes(self):
        assert svc._diff_summary(dict(svc.LIVE_PARAMS)) == "No parameter changes from live rule set"

    def test_diff_summary_lists_changed_fields(self):
        candidate = {**svc.LIVE_PARAMS, "min_hold_days": 15, "atr_mult": 3}
        summary = svc._diff_summary(candidate)
        assert "min_hold_days: 10 -> 15" in summary
        assert "atr_mult: 2 -> 3" in summary


class TestComputeRebalanceDatesExcludesInProgressMonth:
    """ST-01 (BLG-BE-109, v9.0) — mirrors production_strategy.py's fix
    (same duplicated-algorithm surface flagged by BLG-TECH-15 / ST-05)."""

    def test_last_row_in_current_real_month_is_excluded(self):
        idx = pd.bdate_range("2026-06-01", "2026-08-14")
        as_of = pd.Timestamp("2026-08-14")

        rebalance_dates = svc.compute_rebalance_dates(idx, "ME", as_of=as_of)

        assert pd.Timestamp("2026-08-14") not in rebalance_dates

    def test_completed_month_last_row_is_included(self):
        idx = pd.bdate_range("2026-06-01", "2026-07-31")
        as_of = pd.Timestamp("2026-08-03")

        rebalance_dates = svc.compute_rebalance_dates(idx, "ME", as_of=as_of)

        assert idx[-1] in rebalance_dates


class TestRunCandidateBacktest:
    def _mock_yf_download(self, prices, spy, ftse):
        """Returns a function mimicking yf.download's dict-like column access."""
        def _download(arg, start=None, auto_adjust=None, progress=None):
            if arg == "SPY":
                df = pd.DataFrame({"Close": spy})
                return df
            if arg == "^FTSE":
                df = pd.DataFrame({"Close": ftse})
                return df
            # bulk ticker download
            return pd.concat({"Close": prices}, axis=1)
        return _download

    def test_unknown_parameter_field_rejected(self):
        with pytest.raises(svc.BacktestRuleChangeError, match="Unknown parameter field"):
            svc.run_candidate_backtest({"not_a_real_field": 1})

    def test_no_active_tickers_raises(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_conn

        with patch("services.backtest_rule_service.get_db", mock_get_db):
            with pytest.raises(svc.BacktestRuleChangeError, match="No active tickers"):
                svc.run_candidate_backtest({})

    def test_full_run_persists_and_returns_comparison(self):
        prices = _synthetic_prices()
        spy = pd.Series(100 + np.linspace(0, 20, len(prices)), index=prices.index, name="Close")
        ftse = pd.Series(100 + np.linspace(0, 15, len(prices)), index=prices.index, name="Close")

        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"ticker": t} for t in prices.columns]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_conn

        saved_row = {"id": "test-run-id", "created_at": pd.Timestamp("2026-08-18T10:00:00Z")}

        with (
            patch("services.backtest_rule_service.get_db", mock_get_db),
            patch("services.backtest_rule_service.create_backtest_rule_run", return_value=saved_row) as mock_create,
            patch("services.backtest_rule_service.yf.download") as mock_download,
        ):
            def _download_side_effect(arg, start=None, auto_adjust=None, progress=None):
                if arg == "SPY":
                    return pd.DataFrame({"Close": spy})
                if arg == "^FTSE":
                    return pd.DataFrame({"Close": ftse})
                return pd.concat({"Close": prices}, axis=1)
            mock_download.side_effect = _download_side_effect

            result = svc.run_candidate_backtest({"min_hold_days": 15}, initiated_by="Test Owner")

        assert result["id"] == "test-run-id"
        assert result["rule_diff_summary"] == "min_hold_days: 10 -> 15"
        assert result["candidate_params"]["min_hold_days"] == 15
        assert result["live_params"]["min_hold_days"] == 10
        assert set(result["universe_tickers"]) <= set(prices.columns)
        assert "win_rate_pct" in result["candidate_result"]
        assert "r_multiple_buckets" in result["candidate_result"]
        assert len(result["candidate_result"]["r_multiple_buckets"]) == 8
        assert "max_drawdown_pct" in result["candidate_result"]
        assert "win_rate_pct" in result["live_result"]

        # Persisted with both candidate and live results, per AC-03.
        mock_create.assert_called_once()
        call_kwargs = mock_create.call_args.kwargs
        assert call_kwargs["initiated_by"] == "Test Owner"
        assert call_kwargs["candidate_params"]["min_hold_days"] == 15
        assert call_kwargs["live_params"]["min_hold_days"] == 10
        assert "candidate_result" in call_kwargs
        assert "live_result" in call_kwargs
