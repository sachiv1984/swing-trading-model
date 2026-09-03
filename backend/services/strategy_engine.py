"""
Momentum Strategy Engine — shared backtest algorithm (ST-05, BLG-TECH-15,
EPIC-01, v9.0)

Single canonical implementation of the core backtesting algorithm
(compute_signals / compute_atr / compute_risk_on / transaction_fee /
compute_rebalance_dates / backtest), used by BOTH:
- production_strategy.py (repo root) — the full nightly backtest
  (.github/workflows/backtest.yml), 100+ tickers over ~8 years of history
- backend/services/backtest_rule_service.py — the in-app, request-scoped
  "Backtest Rule Change" bounded comparison feature

Prior to this consolidation, these two callers each carried their own
independently-maintained copy of this algorithm (backtest_rule_service.py's
module docstring called this out explicitly as "ported, not imported... for
two reasons"). BLG-TECH-15 tracked the resulting maintenance burden — most
concretely realised as BLG-BE-109/ST-01 (v9.0), where the rebalance-date
bug had to be fixed in both files independently because there was no single
place to fix it once. This module is that single place.

--- Design notes on the two behavioural differences this consolidation had
    to reconcile (both call sites verified byte-identical elsewhere) ---

1. Regime state (US/UK risk-on) is an EXPLICIT parameter (`regime_us`,
   `regime_uk`) here, not read from module-level globals. This was already
   backtest_rule_service.py's own convention, adopted specifically because
   its caller runs inside a concurrent web-server process where two
   simultaneous requests mutating shared module globals would race.
   production_strategy.py previously read `spy_risk_on`/`ftse_risk_on` as
   module globals set once per single-process nightly run — safe there
   only because nothing else runs concurrently in that process, but not a
   pattern worth preserving once there's one canonical implementation.

2. Trade records use production_strategy.py's CAPITALIZED-with-spaces field
   names ("Ticker", "Entry Date", "PnL (£)", "Exit Reason", ...), not
   backtest_rule_service.py's prior lower_snake_case names ("ticker",
   "entry_date", "pnl_gbp", "exit_reason", ...). production_strategy.py's
   schema was kept as canonical because it has a real external dependency:
   import_backtest.py parses production_results/all_trades_*.csv by these
   exact column names (DictReader-style named access), a dependency
   backtest_rule_service.py's newer, self-contained, no-CSV bounded-run
   feature does not share. backtest_rule_service.py's own downstream code
   (_r_multiples/_summarise_run) was updated to read the canonical names
   instead. One new field, "Initial Stop", was added to the trade record —
   production_strategy.py never tracked this (its stop_prices dict is
   overwritten in place as a stop tightens, discarding the original), but
   backtest_rule_service.py needs the ENTRY-time stop separately for its
   R-multiple calculation (metrics_definitions.md 'R-Multiple (Canonical
   Server-Side)': R = (exit - entry) / (entry - initial_stop)). Adding it
   is purely additive for production_strategy.py's CSV consumers (named
   access, not positional).
"""

import numpy as np
import pandas as pd

INITIAL_CAPITAL = 20000


def compute_risk_on(price: pd.Series, ma_period: int = 200) -> pd.Series:
    """True where price is above its own ma_period-day moving average.

    Forward-fills the raw price series *before* computing the moving average
    and the comparison — not after. A malformed/incomplete daily bar from the
    data provider (e.g. SPY's Close coming back NaN while Volume is populated,
    seen 2026-07-24) would otherwise poison both sides: the rolling mean drops
    below min_periods and returns NaN, and `NaN > NaN` evaluates to a real
    `False`, not a NaN — so a downstream `.ffill()` on the comparison result
    can't recover it, and the day gets silently recorded as risk-off even
    though the last known close was solidly risk-on. Forward-filling the
    price itself first means one missing bar just carries the prior day's
    price forward into both calculations, as intended.
    """
    price_filled = price.ffill()
    ma = price_filled.rolling(ma_period).mean()
    return price_filled > ma


def compute_atr(prices: pd.DataFrame) -> pd.DataFrame:
    high = prices.copy()
    low = prices.copy()
    close = prices.copy()
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1)
    tr.columns = pd.MultiIndex.from_tuples([(c, "tr") for c in tr.columns])
    tr = tr.T.groupby(level=0).max().T
    return tr.rolling(14).mean()


def compute_signals(prices: pd.DataFrame, lookback: int, top_n: int, ma_period: int = 200,
                     created_at: dict = None) -> pd.DataFrame:
    """`created_at`, if given, maps ticker -> the date it was added to the
    tracked universe. Each ticker's momentum/signal is masked to
    NaN/False before its own created_at date so a ticker added today cannot
    retroactively change historical trade selection for other tickers
    (AC-01/AC-02/AC-03, BLG-BE-59). backtest_rule_service.py's bounded run
    never passes this (its universe is small/fixed per run, not the full
    growing ticker_universe the mask protects against) — omitting it
    reproduces the exact prior ungated computation (see
    tests/test_production_strategy.py::test_no_created_at_map_preserves_prior_behaviour)."""
    momentum = prices.pct_change(lookback)
    if created_at:
        for ticker in momentum.columns:
            cutoff = created_at.get(ticker)
            if cutoff is not None and not pd.isna(cutoff):
                momentum.loc[momentum.index < cutoff, ticker] = np.nan
    ranks = momentum.rank(axis=1, ascending=False, na_option="bottom", method="first")
    trend = prices > prices.rolling(ma_period).mean()
    signals = (trend) & (ranks <= top_n)
    signals = signals.fillna(False).astype(bool)
    if created_at:
        for ticker in signals.columns:
            cutoff = created_at.get(ticker)
            if cutoff is not None and not pd.isna(cutoff):
                signals.loc[signals.index < cutoff, ticker] = False
    return signals


def transaction_fee(ticker: str, side: str) -> float:
    if ticker.endswith(".L"):
        return 0.005 if side == "buy" else 0.0
    return 0.0015


def compute_rebalance_dates(price_index: pd.DatetimeIndex, rebalance_freq: str,
                             as_of: pd.Timestamp = None) -> pd.DatetimeIndex:
    """Return the subset of price_index at which a rebalance occurs.

    price_index.resample(rebalance_freq).last().index would return calendar
    period-end labels (e.g. 2026-01-31) even when that exact date is a
    weekend and never appears in price_index — silently skipping monthly
    rotation for any month whose last calendar day falls on a Sat/Sun.
    Group the actual (business-day) index by period and take each period's
    real last row instead, so the result only ever contains dates that
    genuinely exist in price_index.

    BLG-BE-109 (ST-01, v9.0): a nightly run always fetches prices through
    "today", so the naive tail(1)-per-period grab above treats today's row
    as if it were that period's true close even when the period (e.g. the
    current calendar month) has not actually finished yet — a premature/
    incorrect rebalance signal. Exclude any rebalance date whose period is
    still the real current period as of wall-clock "now" (or the injected
    `as_of`, for deterministic testing). Purely historical windows are
    unaffected, since their last row's period will already be strictly
    before the real current period.
    """
    period_freq = rebalance_freq[:-1] if rebalance_freq.endswith("E") else rebalance_freq
    rebalance_dates = price_index.to_series().groupby(price_index.to_period(period_freq)).tail(1).index

    now = as_of if as_of is not None else pd.Timestamp.now(tz=price_index.tz)
    current_real_period = now.to_period(period_freq)
    return rebalance_dates[rebalance_dates.to_period(period_freq) != current_real_period]


def backtest(signals, prices, volatility, atr, regime_us, regime_uk, rebalance_freq, atr_mult,
             min_position_pct=0.05, max_position_pct=0.15, min_hold_days=7,
             risk_off_mode="single", stop_loss_mode="simple", initial_atr_mult=None,
             profit_atr_mult=None, as_of=None):
    """Core momentum backtest engine. regime_us/regime_uk are boolean
    Series (risk-on flag per date), explicit parameters rather than module
    globals — see module docstring note 1."""

    if initial_atr_mult is None:
        initial_atr_mult = atr_mult * 1.5
    if profit_atr_mult is None:
        profit_atr_mult = atr_mult

    def is_risk_on(ticker: str, date) -> bool:
        us_on = bool(regime_us.at[date]) if date in regime_us.index else False
        uk_on = bool(regime_uk.at[date]) if date in regime_uk.index else False
        if risk_off_mode == "single":
            return uk_on if ticker.endswith(".L") else us_on
        elif risk_off_mode == "dual":
            return us_on or uk_on
        elif risk_off_mode == "dual_strict":
            return us_on and uk_on
        return us_on

    rebalance_dates = compute_rebalance_dates(prices.index, rebalance_freq, as_of=as_of)
    holdings = pd.Series(0.0, index=prices.columns)
    entry_prices = {}
    entry_dates = {}
    stop_prices = {}
    initial_stop_prices = {}
    trades = []
    cash = INITIAL_CAPITAL
    portfolio_values = []

    def _record_exit(t, date, exit_price, exit_reason, charge_fee=True):
        """charge_fee=False for the still-open/unrealized case at the end of
        the run below: no sale actually occurred, so no sell fee applies —
        matches the pre-consolidation behaviour exactly (neither prior
        implementation charged a fee on an unrealized mark)."""
        shares = holdings[t]
        entry_price = entry_prices[t]
        holding_days = (date - entry_dates[t]).days
        current_profit_pct = (exit_price - entry_price) / entry_price
        if charge_fee:
            fee = transaction_fee(t, "sell")
            exit_adj = exit_price * (1 - fee)
        else:
            exit_adj = exit_price
        pnl = (exit_adj - entry_price) * shares
        trades.append({
            "Ticker": t, "Entry Date": entry_dates[t], "Exit Date": date,
            "Holding Days": holding_days, "Entry": entry_price, "Exit": exit_adj,
            "Initial Stop": initial_stop_prices.get(t),
            "PnL (£)": pnl, "PnL %": round(current_profit_pct * 100, 2),
            "Market": "UK" if t.endswith(".L") else "US", "Exit Reason": exit_reason,
            "Was Profitable": current_profit_pct > 0,
        })
        return exit_adj

    for date in prices.index:
        current_positions = list(holdings[holdings > 0].index)

        # Stop loss with profit-lock logic
        for t in current_positions:
            if holdings[t] == 0:
                continue
            if date not in atr.index or t not in atr.columns:
                continue
            atr_val = atr.loc[date, t]
            if np.isnan(atr_val):
                continue

            holding_days = (date - entry_dates[t]).days
            if holding_days < min_hold_days:
                continue

            current_price = prices.loc[date, t]
            entry_price = entry_prices[t]
            current_profit_pct = (current_price - entry_price) / entry_price

            if stop_loss_mode == "simple":
                active_atr_mult = atr_mult
            elif stop_loss_mode == "tiered":
                active_atr_mult = initial_atr_mult if holding_days < min_hold_days * 2 else atr_mult
            elif stop_loss_mode == "profit_lock":
                active_atr_mult = profit_atr_mult if current_profit_pct > 0 else initial_atr_mult
            else:
                active_atr_mult = atr_mult

            current_stop = stop_prices.get(t, -np.inf)
            new_stop = current_price - active_atr_mult * atr_val
            stop_prices[t] = max(current_stop, new_stop)

            if current_price <= stop_prices[t]:
                exit_adj = _record_exit(t, date, current_price, "Stop")
                cash += holdings[t] * exit_adj
                holdings[t] = 0
                entry_prices.pop(t, None); entry_dates.pop(t, None)
                stop_prices.pop(t, None); initial_stop_prices.pop(t, None)

        # Risk-off exits
        for t in current_positions:
            if holdings[t] == 0:
                continue
            if not is_risk_on(t, date):
                exit_adj = _record_exit(t, date, prices.loc[date, t], "Risk-Off")
                cash += holdings[t] * exit_adj
                holdings[t] = 0
                entry_prices.pop(t, None); entry_dates.pop(t, None)
                stop_prices.pop(t, None); initial_stop_prices.pop(t, None)

        # Today's qualifying, risk-on candidates — used both for the monthly
        # rotation-out below and the daily slot fill-in that follows it.
        selected = signals.loc[date][signals.loc[date]].index.tolist()
        selected = [t for t in selected if is_risk_on(t, date)]

        # Monthly rebalance: rotate out any holding that has fallen out of
        # the current top-n qualifying set. Only evaluated on rebalance
        # dates so a position isn't force-sold mid-month over a temporary
        # rank dip.
        if date in rebalance_dates:
            exits = [t for t in list(holdings[holdings > 0].index) if t not in selected]
            for t in exits:
                exit_adj = _record_exit(t, date, prices.loc[date, t], "No longer qualifies")
                cash += holdings[t] * exit_adj
                holdings[t] = 0
                entry_prices.pop(t, None); entry_dates.pop(t, None)
                stop_prices.pop(t, None); initial_stop_prices.pop(t, None)

        # Daily slot fill-in: whenever fewer than top-n positions are held
        # (a stop, risk-off, or rotation exit freed up a slot), buy a
        # qualifying candidate as soon as one is available rather than
        # waiting for the next month-end rebalance to deploy the cash.
        num_existing = (holdings > 0).sum()
        num_new_slots = len(selected) - num_existing

        if num_new_slots > 0:
            existing_tickers = holdings[holdings > 0].index.tolist()
            new_candidates = [t for t in selected if t not in existing_tickers][:num_new_slots]

            if len(new_candidates) > 0:
                available_cash = cash
                vols = volatility.loc[date, new_candidates].replace(0, np.nan).dropna()

                if len(vols) > 0:
                    inv_vol = 1 / vols
                    weights = inv_vol / inv_vol.sum()

                    weights_constrained = {}
                    for t, w in weights.items():
                        weights_constrained[t] = max(min_position_pct, min(w, max_position_pct))

                    total_weight = sum(weights_constrained.values())
                    weights_final = {t: w / total_weight for t, w in weights_constrained.items()}

                    for t, w in weights_final.items():
                        buy_fee = transaction_fee(t, "buy")
                        price = prices.loc[date, t] * (1 + buy_fee)
                        alloc = available_cash * w
                        shares = alloc / price

                        holdings[t] = shares
                        entry_prices[t] = price
                        entry_dates[t] = date

                        atr_val = atr.loc[date, t]
                        if stop_loss_mode == "simple":
                            initial_stop = price - atr_mult * atr_val
                        else:
                            initial_stop = price - initial_atr_mult * atr_val
                        stop_prices[t] = initial_stop
                        initial_stop_prices[t] = initial_stop

                        cash -= shares * price

        daily_value = cash + (holdings * prices.loc[date]).sum()
        portfolio_values.append(daily_value)

    # Positions still open when the price data ends never hit a stop, risk-off,
    # or rebalance exit, so the loop above never appends a trade for them —
    # without this they vanish from trades_df entirely, making the final
    # weeks of a run look like no activity took place even though capital
    # is deployed.
    last_date = prices.index[-1]
    for t in list(holdings[holdings > 0].index):
        _record_exit(t, last_date, prices.loc[last_date, t], "Open (Unrealized)", charge_fee=False)

    pv = pd.Series(portfolio_values, index=prices.index)
    returns = pv.pct_change().fillna(0)
    trades_df = pd.DataFrame(trades)

    return pv, returns, trades_df
