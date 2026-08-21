"""
Nightly backtest data-integrity tests (EPIC-01, v7.1 ST-01 / ST-02).

BLG-BE-59 (ST-01): compute_signals() must gate each ticker's eligibility on
its own ticker_universe.created_at date, so adding a ticker today cannot
retroactively change historical trade selection.

BLG-BE-60 (ST-02): the nightly backtest engine (production_strategy.py's
backtest()) must be deterministic given fixed inputs, and import_backtest.py
must alert on an unexplained total_pnl_gbp swing rather than silently
logging it.
"""
import pandas as pd
import numpy as np

import production_strategy as ps
import import_backtest as ib


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _synthetic_prices(n_days=60):
    """Deterministic synthetic price panel for AAA/BBB/CCC.

    AAA: strong steady uptrend (should usually rank #1 among AAA/BBB).
    BBB: mild uptrend (weaker momentum than AAA).
    CCC: strongest uptrend of all — but its created_at is set mid-window in
    the tests below, simulating a ticker whose price history predates when
    it was added to the tracked universe.
    """
    idx = pd.bdate_range("2024-01-02", periods=n_days)
    aaa = 100 + np.arange(n_days) * 1.00
    bbb = 100 + np.arange(n_days) * 0.30
    ccc = 100 + np.arange(n_days) * 2.00
    return pd.DataFrame({"AAA": aaa, "BBB": bbb, "CCC": ccc}, index=idx)


# ---------------------------------------------------------------------------
# ST-01 (BLG-BE-59) — ticker eligibility gated on created_at
# ---------------------------------------------------------------------------

class TestComputeSignalsCreatedAtGating:
    def test_ac01_ticker_masked_false_before_its_own_created_at(self):
        prices = _synthetic_prices()
        cutoff = prices.index[40]
        created_at = {"AAA": None, "BBB": None, "CCC": cutoff}

        signals = ps.compute_signals(prices, lookback=10, top_n=1, ma_period=5, created_at=created_at)

        assert not signals.loc[signals.index < cutoff, "CCC"].any(), (
            "CCC must never be selected before its own created_at date"
        )

    def test_ac02_ac03_other_tickers_unaffected_by_later_ticker_addition(self):
        """Adding CCC (with a mid-window created_at) must not change AAA/BBB's
        historical selections before CCC's own created_at — CCC's momentum
        score must not distort the cross-sectional rank of other tickers on
        dates before it was ever tracked.
        """
        prices = _synthetic_prices()
        cutoff = prices.index[40]

        # Signals computed as if CCC were present in the DB today (gated).
        signals_with_ccc = ps.compute_signals(
            prices, lookback=10, top_n=1, ma_period=5,
            created_at={"AAA": None, "BBB": None, "CCC": cutoff},
        )

        # Signals computed as if CCC had never existed in the universe at all.
        signals_without_ccc = ps.compute_signals(
            prices[["AAA", "BBB"]], lookback=10, top_n=1, ma_period=5, created_at=None,
        )

        pre_cutoff = prices.index < cutoff
        pd.testing.assert_frame_equal(
            signals_with_ccc.loc[pre_cutoff, ["AAA", "BBB"]],
            signals_without_ccc.loc[pre_cutoff],
        )

    def test_gating_does_not_suppress_ticker_after_its_created_at(self):
        """Sanity check: the mask is a floor, not a permanent lockout — CCC
        must be eligible for selection from its created_at date forward.
        """
        prices = _synthetic_prices()
        cutoff = prices.index[40]
        created_at = {"AAA": None, "BBB": None, "CCC": cutoff}

        signals = ps.compute_signals(prices, lookback=10, top_n=1, ma_period=5, created_at=created_at)

        assert signals.loc[signals.index >= cutoff, "CCC"].any(), (
            "CCC (strongest momentum) should be selectable once past its created_at"
        )

    def test_no_created_at_map_preserves_prior_behaviour(self):
        """created_at=None (e.g. CSV fallback with no DB) must reproduce the
        original ungated computation — no behaviour change for that path.
        """
        prices = _synthetic_prices()
        gated = ps.compute_signals(prices, lookback=10, top_n=1, ma_period=5, created_at=None)
        gated_empty = ps.compute_signals(
            prices, lookback=10, top_n=1, ma_period=5,
            created_at={"AAA": None, "BBB": None, "CCC": None},
        )
        pd.testing.assert_frame_equal(gated, gated_empty)


# ---------------------------------------------------------------------------
# Hotfix — compute_risk_on() must not treat a malformed NaN price bar as
# risk-off (2026-07-27: SPY's Close came back NaN with Volume populated,
# spuriously force-closing every open US position).
# ---------------------------------------------------------------------------

class TestComputeRiskOnNanHandling:
    def test_isolated_nan_bar_carries_forward_prior_state(self):
        idx = pd.bdate_range("2024-01-02", periods=210)
        price = pd.Series(150.0, index=idx)
        price.iloc[:20] = 50.0  # low tail still inside the trailing 200MA window,
        # so the window average (145) sits below the flat 150 plateau

        # Malform the last bar only — mirrors SPY's 2026-07-24 Close=NaN report.
        nan_price = price.copy()
        nan_price.iloc[-1] = np.nan

        clean = ps.compute_risk_on(price)
        with_gap = ps.compute_risk_on(nan_price)

        assert clean.iloc[-1] == True
        assert with_gap.iloc[-1] == True, (
            "a single malformed NaN bar must carry forward the prior day's "
            "risk-on state, not silently flip to risk-off"
        )

    def test_ma_window_touching_the_nan_bar_is_not_poisoned(self):
        idx = pd.bdate_range("2024-01-02", periods=205)
        price = pd.Series(150.0, index=idx)
        price.iloc[:5] = 50.0
        nan_price = price.copy()
        nan_price.iloc[100] = np.nan  # gap in the middle of a later MA window

        result = ps.compute_risk_on(nan_price)
        assert not result.iloc[100:200].isna().any(), (
            "an old NaN bar should not propagate NaN through every rolling "
            "window that includes it"
        )


# ---------------------------------------------------------------------------
# ST-02 (BLG-BE-60) — backtest() determinism given fixed inputs
# ---------------------------------------------------------------------------

class TestBacktestDeterminism:
    def test_ac02_identical_inputs_produce_byte_identical_output(self):
        """Controlled re-run comparison: backtest() called twice with byte-
        identical inputs must produce byte-identical pv/returns/trades_df.
        This guards against incidental nondeterminism in the engine itself,
        distinct from the external yfinance historical-price-revision issue
        that check_drift_alert (below) guards against in production.
        """
        prices = _synthetic_prices(n_days=80)
        atr = ps.compute_atr(prices)
        signals = ps.compute_signals(prices, lookback=10, top_n=1, ma_period=5)
        volatility = prices.pct_change().rolling(10).std()

        # ST-05 (BLG-TECH-15, v9.0): regime state is an explicit parameter
        # on the consolidated backtest(), not a module global to monkeypatch.
        always_on = pd.Series(True, index=prices.index)

        kwargs = dict(
            rebalance_freq="ME", atr_mult=2, min_position_pct=0.05,
            max_position_pct=0.20, min_hold_days=5, risk_off_mode="single",
            stop_loss_mode="profit_lock", initial_atr_mult=5, profit_atr_mult=2,
        )

        pv1, returns1, trades1 = ps.backtest(signals, prices, volatility, atr, always_on, always_on, **kwargs)
        pv2, returns2, trades2 = ps.backtest(signals, prices, volatility, atr, always_on, always_on, **kwargs)

        pd.testing.assert_series_equal(pv1, pv2)
        pd.testing.assert_series_equal(returns1, returns2)
        pd.testing.assert_frame_equal(trades1, trades2)
        assert trades1["PnL (£)"].sum() == trades2["PnL (£)"].sum()


# ---------------------------------------------------------------------------
# ST-01 (BLG-BE-109, v9.0) — rebalance_dates excludes the current,
# in-progress calendar month
# ---------------------------------------------------------------------------

class TestComputeRebalanceDatesExcludesInProgressMonth:
    def test_last_row_in_current_real_month_is_excluded(self):
        """Mid-month case: price data extends through 2026-08-14 (a Friday)
        and 'now' is also within August 2026 (the nightly-run shape) — the
        naive tail(1)-per-period grab would treat 2026-08-14 as August's
        rebalance date even though August has not actually finished yet.
        """
        idx = pd.bdate_range("2026-06-01", "2026-08-14")
        as_of = pd.Timestamp("2026-08-14")

        rebalance_dates = ps.compute_rebalance_dates(idx, "ME", as_of=as_of)

        assert pd.Timestamp("2026-08-14") not in rebalance_dates
        # June and July, both fully elapsed relative to as_of, are unaffected.
        assert pd.Timestamp(idx[idx.to_period("M") == pd.Period("2026-06", "M")][-1]) in rebalance_dates
        assert pd.Timestamp(idx[idx.to_period("M") == pd.Period("2026-07", "M")][-1]) in rebalance_dates

    def test_completed_month_last_row_is_included(self):
        """Once 'now' has moved into the next calendar month, that prior
        month's last trading row is a genuine rebalance date."""
        idx = pd.bdate_range("2026-06-01", "2026-07-31")
        as_of = pd.Timestamp("2026-08-03")  # now in August; July has closed

        rebalance_dates = ps.compute_rebalance_dates(idx, "ME", as_of=as_of)

        assert idx[-1] in rebalance_dates

    def test_defaults_to_real_wall_clock_now_when_as_of_omitted(self):
        """Without an injected as_of, the function must use the real current
        time — proven by comparing behaviour for an index whose last row is
        'today' (via pd.Timestamp.now(), same live current period, must be
        excluded) against a clearly-completed historical month (must not
        be excluded)."""
        today = pd.Timestamp.now().normalize()
        live_idx = pd.bdate_range(today - pd.Timedelta(days=45), today)
        rebalance_dates = ps.compute_rebalance_dates(live_idx, "ME")
        assert live_idx[-1] not in rebalance_dates

        historical_idx = pd.bdate_range("2020-01-01", "2020-03-31")
        rebalance_dates_historical = ps.compute_rebalance_dates(historical_idx, "ME")
        assert historical_idx[-1] in rebalance_dates_historical

    def test_end_to_end_backtest_does_not_rebalance_on_in_progress_month(self):
        """Full backtest() integration: with as_of pinned mid-month, no trade
        entry/rebalance activity should key off the in-progress month's last
        available row."""
        idx = pd.bdate_range("2026-01-02", "2026-08-14")
        prices = pd.DataFrame(
            {"AAA": 100 + np.arange(len(idx)) * 0.5, "BBB": 100 + np.arange(len(idx)) * 0.3},
            index=idx,
        )
        atr = ps.compute_atr(prices)
        signals = ps.compute_signals(prices, lookback=20, top_n=1, ma_period=10)
        volatility = prices.pct_change().rolling(20).std()

        # ST-05 (BLG-TECH-15, v9.0): regime state is an explicit parameter
        # on the consolidated backtest(), not a module global to monkeypatch.
        always_on = pd.Series(True, index=prices.index)

        as_of = pd.Timestamp("2026-08-14")
        # backtest() must run end-to-end without error using the same
        # as_of-pinned rebalance_dates computation exercised directly below.
        ps.backtest(
            signals, prices, volatility, atr, always_on, always_on,
            rebalance_freq="ME", atr_mult=2, min_position_pct=0.05,
            max_position_pct=0.20, min_hold_days=5, risk_off_mode="single",
            stop_loss_mode="profit_lock", initial_atr_mult=5, profit_atr_mult=2,
            as_of=as_of,
        )

        rebalance_dates = ps.compute_rebalance_dates(prices.index, "ME", as_of=as_of)
        assert pd.Timestamp("2026-08-14") not in rebalance_dates


# ---------------------------------------------------------------------------
# ST-02 (BLG-BE-60) — import_backtest.py drift-check alert (fix vehicle: option c)
# ---------------------------------------------------------------------------

class TestDriftAlert:
    def test_alerts_when_zero_new_exits_and_swing_exceeds_threshold(self):
        alert = ib.check_drift_alert(trades_imported=587, trades_deleted=587, delta=27000.0)
        assert alert is not None
        assert "BACKTEST_DRIFT_ALERT" in alert

    def test_no_alert_when_new_exits_occurred(self):
        # trades_imported != trades_deleted means the trade count genuinely
        # changed this run — a swing is expected and not anomalous.
        assert ib.check_drift_alert(trades_imported=592, trades_deleted=587, delta=27000.0) is None

    def test_no_alert_when_swing_within_threshold(self):
        assert ib.check_drift_alert(trades_imported=587, trades_deleted=587, delta=12.5) is None

    def test_no_alert_on_first_import(self):
        # delta is None when there was no previous import to compare against.
        assert ib.check_drift_alert(trades_imported=587, trades_deleted=0, delta=None) is None

    def test_negative_swing_also_alerts(self):
        alert = ib.check_drift_alert(trades_imported=587, trades_deleted=587, delta=-500.0)
        assert alert is not None

    def test_threshold_is_exclusive_boundary(self):
        assert ib.check_drift_alert(trades_imported=587, trades_deleted=587, delta=50.0, threshold_gbp=50.0) is None
        assert ib.check_drift_alert(trades_imported=587, trades_deleted=587, delta=50.01, threshold_gbp=50.0) is not None
