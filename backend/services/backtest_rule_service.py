"""
Backtest Rule Change Service (ST-07, BLG-FEAT-89, EPIC-02, v8.9)

In-app backtesting engine for candidate strategy_rules.md parameter changes.
Design source: docs/design/2026-08-17__release-v8.9/in-app-backtesting-engine/ux_spec.md
Spec: docs/specs/frontend/pages/strategy_benchmark.md §3

§13 compliance: deterministic simulation over historical market data, applied
to a candidate rule set instead of the live one. No ML model, no adaptive
inference. Output is comparative statistical context for a human decision
(whether to adopt the candidate rule change) — not an automated action. No
output from this module writes to strategy_rules.md or any live rule
configuration; adopting a rule change remains a separate, manual,
human-authored edit outside this feature's scope. Same §13 category as the
existing Benchmark/Version Comparison tabs.

--- Scope reduction (RISK-02, sprint_backlog.md) ---

The full production_strategy.py nightly run (.github/workflows/backtest.yml)
covers the entire ticker_universe (100+ tickers) over ~8 years of history and
is budgeted 90 minutes of CI compute — categorically infeasible to run
synchronously inside a web request. Per RISK-02's own explicit contingency
("if infeasible, scope may narrow to a smaller candidate-comparison
surface"), this module runs a BOUNDED backtest instead:
  - universe: first UNIVERSE_SIZE active tickers from ticker_universe
    (alphabetical — deterministic, reproducible)
  - window: LOOKBACK_YEARS of history ending today

Both the candidate and the live-parameter baseline are computed over the
IDENTICAL bounded universe/window in the same run, so the win-rate/R-multiple/
drawdown comparison is apples-to-apples (a valid experiment holds everything
but the rule diff constant) — the absolute figures will not match the full
nightly Benchmark tab's numbers (different universe/window by design), and
the run metadata records exactly what was used so this is never ambiguous
to a reader of a persisted run.

--- Algorithm provenance ---

compute_signals/compute_atr/compute_risk_on/transaction_fee/backtest below
are ported from production_strategy.py (repo root), not imported directly,
for two reasons: (1) production_strategy.py is a standalone script with
import-time side effects (os.makedirs) and has never been used as a library;
(2) its backtest() reads regime state (spy_risk_on/ftse_risk_on) from
MODULE-LEVEL GLOBALS, which is unsafe to mutate from a concurrent web-server
process (two simultaneous requests would race on the same globals). The port
below is behaviourally identical except regime state is threaded through as
an explicit parameter instead of module globals, making it safe for
concurrent request handling. Filed BLG-TECH-15 for the maintenance burden of
keeping this in sync if production_strategy.py's core algorithm changes.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import yfinance as yf

from database import get_db, create_backtest_rule_run

# strategy_rules.md's live parameters — mirrors production_strategy.py's
# OPTIMAL_PARAMS exactly. This is the "live rule set" baseline every
# candidate run is compared against.
LIVE_PARAMS = {
    "lookback": 252,
    "top_n": 5,
    "atr_mult": 2,
    "rebalance_freq": "ME",
    "min_position_pct": 0.05,
    "max_position_pct": 0.20,
    "min_hold_days": 10,
    "risk_off_mode": "single",
    "stop_loss_mode": "profit_lock",
    "initial_atr_mult": 5,
    "profit_atr_mult": 2,
}

# Structured candidate input (design_record.md §2.1 — structured parameter
# form, not free-form rule-diff text; deferred to implementation, resolved
# here for engineering-cost reasons: raw text diffing against
# strategy_rules.md prose has no safe, deterministic parse path).
CANDIDATE_OVERRIDABLE_FIELDS = set(LIVE_PARAMS.keys())

INITIAL_CAPITAL = 20000
UNIVERSE_SIZE = 20
LOOKBACK_YEARS = 4

R_MULTIPLE_BUCKETS = [
    ("< -3R", None, -3.0),
    ("-3R to -2R", -3.0, -2.0),
    ("-2R to -1R", -2.0, -1.0),
    ("-1R to 0R", -1.0, 0.0),
    ("0R to 1R", 0.0, 1.0),
    ("1R to 2R", 1.0, 2.0),
    ("2R to 3R", 2.0, 3.0),
    ("> 3R", 3.0, None),
]


class BacktestRuleChangeError(Exception):
    """Raised for user-facing/business-rule failures (not unexpected server errors)."""


def _load_bounded_universe(limit: int = UNIVERSE_SIZE) -> List[str]:
    """First `limit` active tickers from ticker_universe, alphabetical —
    deterministic and reproducible run-to-run (module docstring)."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT ticker FROM ticker_universe WHERE active = TRUE ORDER BY ticker LIMIT %s",
                (limit,),
            )
            rows = cur.fetchall()
    tickers = [r["ticker"] for r in rows]
    if not tickers:
        raise BacktestRuleChangeError("No active tickers in ticker_universe — cannot run a backtest.")
    return tickers


def compute_risk_on(price: pd.Series, ma_period: int = 200) -> pd.Series:
    """Ported from production_strategy.py::compute_risk_on (unchanged)."""
    price_filled = price.ffill()
    ma = price_filled.rolling(ma_period).mean()
    return price_filled > ma


def compute_atr(prices: pd.DataFrame) -> pd.DataFrame:
    """Ported from production_strategy.py::compute_atr (unchanged)."""
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


def compute_signals(prices: pd.DataFrame, lookback: int, top_n: int, ma_period: int = 200) -> pd.DataFrame:
    """Ported from production_strategy.py::compute_signals (unchanged; the
    ticker_created_at eligibility mask is omitted — this bounded run's
    universe is small/fixed per run, not the full growing ticker_universe
    the mask protects against retroactive rank distortion for)."""
    momentum = prices.pct_change(lookback)
    ranks = momentum.rank(axis=1, ascending=False, na_option="bottom", method="first")
    trend = prices > prices.rolling(ma_period).mean()
    signals = (trend) & (ranks <= top_n)
    return signals.fillna(False).astype(bool)


def transaction_fee(ticker: str, side: str) -> float:
    """Ported from production_strategy.py::transaction_fee (unchanged)."""
    if ticker.endswith(".L"):
        return 0.005 if side == "buy" else 0.0
    return 0.0015


def compute_rebalance_dates(
    price_index: pd.DatetimeIndex, rebalance_freq: str, as_of: Optional[pd.Timestamp] = None
) -> pd.DatetimeIndex:
    """Ported from production_strategy.py::compute_rebalance_dates (same
    BLG-BE-109 fix, mirrored here per this module's ported-not-imported
    provenance note above). Excludes any rebalance date whose period is
    still the real current period as of wall-clock "now" (or the injected
    `as_of`, for deterministic testing), so an in-progress current calendar
    month is never mistaken for a completed rebalance point."""
    period_freq = rebalance_freq[:-1] if rebalance_freq.endswith("E") else rebalance_freq
    rebalance_dates = price_index.to_series().groupby(price_index.to_period(period_freq)).tail(1).index

    now = as_of if as_of is not None else pd.Timestamp.now(tz=price_index.tz)
    current_real_period = now.to_period(period_freq)
    return rebalance_dates[rebalance_dates.to_period(period_freq) != current_real_period]


def run_backtest(
    signals: pd.DataFrame,
    prices: pd.DataFrame,
    volatility: pd.DataFrame,
    atr: pd.DataFrame,
    regime_us: pd.Series,
    regime_uk: pd.Series,
    rebalance_freq: str,
    atr_mult: float,
    min_position_pct: float = 0.05,
    max_position_pct: float = 0.15,
    min_hold_days: int = 7,
    risk_off_mode: str = "single",
    stop_loss_mode: str = "simple",
    initial_atr_mult: Optional[float] = None,
    profit_atr_mult: Optional[float] = None,
    as_of: Optional[pd.Timestamp] = None,
):
    """Ported from production_strategy.py::backtest. Behaviourally identical
    except regime state is an explicit parameter (regime_us/regime_uk) rather
    than module-level globals — safe for concurrent request handling. See
    module docstring for full provenance/rationale."""

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
    entry_prices: Dict[str, float] = {}
    entry_dates: Dict[str, pd.Timestamp] = {}
    stop_prices: Dict[str, float] = {}
    initial_stop_prices: Dict[str, float] = {}
    trades: List[Dict] = []
    cash = INITIAL_CAPITAL
    portfolio_values = []

    for date in prices.index:
        current_positions = list(holdings[holdings > 0].index)

        # Stop loss with profit-lock logic
        for t in current_positions:
            if holdings[t] == 0:
                continue
            shares = holdings[t]
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
                exit_price = current_price
                fee = transaction_fee(t, "sell")
                exit_adj = exit_price * (1 - fee)
                pnl = (exit_adj - entry_price) * shares
                trades.append({
                    "ticker": t, "entry_date": entry_dates[t], "exit_date": date,
                    "holding_days": holding_days, "entry_price": entry_price, "exit_price": exit_adj,
                    "initial_stop_price": initial_stop_prices.get(t),
                    "pnl_gbp": pnl, "pnl_pct": round(current_profit_pct * 100, 2),
                    "market": "UK" if t.endswith(".L") else "US", "exit_reason": "Stop",
                    "was_profitable": current_profit_pct > 0,
                })
                cash += shares * exit_adj
                holdings[t] = 0
                entry_prices.pop(t, None); entry_dates.pop(t, None)
                stop_prices.pop(t, None); initial_stop_prices.pop(t, None)

        # Risk-off exits
        for t in current_positions:
            if holdings[t] == 0:
                continue
            shares = holdings[t]
            if not is_risk_on(t, date):
                holding_days = (date - entry_dates[t]).days
                exit_price = prices.loc[date, t]
                entry_price = entry_prices[t]
                current_profit_pct = (exit_price - entry_price) / entry_price
                fee = transaction_fee(t, "sell")
                exit_adj = exit_price * (1 - fee)
                pnl = (exit_adj - entry_price) * shares
                trades.append({
                    "ticker": t, "entry_date": entry_dates[t], "exit_date": date,
                    "holding_days": holding_days, "entry_price": entry_price, "exit_price": exit_adj,
                    "initial_stop_price": initial_stop_prices.get(t),
                    "pnl_gbp": pnl, "pnl_pct": round(current_profit_pct * 100, 2),
                    "market": "UK" if t.endswith(".L") else "US", "exit_reason": "Risk-Off",
                    "was_profitable": current_profit_pct > 0,
                })
                cash += shares * exit_adj
                holdings[t] = 0
                entry_prices.pop(t, None); entry_dates.pop(t, None)
                stop_prices.pop(t, None); initial_stop_prices.pop(t, None)

        selected = signals.loc[date][signals.loc[date]].index.tolist()
        selected = [t for t in selected if is_risk_on(t, date)]

        if date in rebalance_dates:
            exits = [t for t in list(holdings[holdings > 0].index) if t not in selected]
            for t in exits:
                shares = holdings[t]
                holding_days = (date - entry_dates[t]).days
                exit_price = prices.loc[date, t]
                entry_price = entry_prices[t]
                current_profit_pct = (exit_price - entry_price) / entry_price
                fee = transaction_fee(t, "sell")
                exit_adj = exit_price * (1 - fee)
                pnl = (exit_adj - entry_price) * shares
                trades.append({
                    "ticker": t, "entry_date": entry_dates[t], "exit_date": date,
                    "holding_days": holding_days, "entry_price": entry_price, "exit_price": exit_adj,
                    "initial_stop_price": initial_stop_prices.get(t),
                    "pnl_gbp": pnl, "pnl_pct": round(current_profit_pct * 100, 2),
                    "market": "UK" if t.endswith(".L") else "US", "exit_reason": "No longer qualifies",
                    "was_profitable": current_profit_pct > 0,
                })
                cash += shares * exit_adj
                holdings[t] = 0
                entry_prices.pop(t, None); entry_dates.pop(t, None)
                stop_prices.pop(t, None); initial_stop_prices.pop(t, None)

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
                    weights_constrained = {t: max(min_position_pct, min(w, max_position_pct)) for t, w in weights.items()}
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

    last_date = prices.index[-1]
    for t in list(holdings[holdings > 0].index):
        shares = holdings[t]
        entry_price = entry_prices[t]
        current_price = prices.loc[last_date, t]
        current_profit_pct = (current_price - entry_price) / entry_price
        holding_days = (last_date - entry_dates[t]).days
        trades.append({
            "ticker": t, "entry_date": entry_dates[t], "exit_date": last_date,
            "holding_days": holding_days, "entry_price": entry_price, "exit_price": current_price,
            "initial_stop_price": initial_stop_prices.get(t),
            "pnl_gbp": (current_price - entry_price) * shares, "pnl_pct": round(current_profit_pct * 100, 2),
            "market": "UK" if t.endswith(".L") else "US", "exit_reason": "Open (Unrealized)",
            "was_profitable": current_profit_pct > 0,
        })

    pv = pd.Series(portfolio_values, index=prices.index)
    returns = pv.pct_change().fillna(0)
    trades_df = pd.DataFrame(trades)
    return pv, returns, trades_df


def _max_drawdown_pct(returns: pd.Series) -> float:
    equity = (1 + returns).cumprod()
    dd = equity / equity.cummax() - 1
    return round(float(dd.min()) * 100, 2)


def _r_multiples(trades_df: pd.DataFrame) -> List[float]:
    """Canonical R formula (metrics_definitions.md 'R-Multiple (Canonical
    Server-Side)'): R = (exit - entry) / (entry - initial_stop). Trades
    without a qualifying initial_stop_price (entry <= stop) are excluded,
    same qualifying conditions as the canonical server-side formula."""
    if trades_df.empty:
        return []
    r_values = []
    for _, row in trades_df.iterrows():
        stop = row.get("initial_stop_price")
        entry = row["entry_price"]
        exitp = row["exit_price"]
        if stop is None or pd.isna(stop) or entry <= stop:
            continue
        r_values.append((exitp - entry) / (entry - stop))
    return r_values


def _bucket_r_multiples(r_values: List[float]) -> List[Dict]:
    buckets = []
    for label, lo, hi in R_MULTIPLE_BUCKETS:
        if lo is None:
            count = sum(1 for r in r_values if r < hi)
        elif hi is None:
            count = sum(1 for r in r_values if r >= lo)
        else:
            count = sum(1 for r in r_values if lo <= r < hi)
        buckets.append({"label": label, "count": count})
    return buckets


def _summarise_run(trades_df: pd.DataFrame, returns: pd.Series) -> Dict:
    trade_count = len(trades_df)
    win_rate = (
        round(float(trades_df["was_profitable"].mean()) * 100, 2)
        if trade_count > 0 else None
    )
    r_values = _r_multiples(trades_df)
    return {
        "trade_count": trade_count,
        "win_rate_pct": win_rate,
        "max_drawdown_pct": _max_drawdown_pct(returns),
        "r_multiple_buckets": _bucket_r_multiples(r_values),
        "median_r": round(float(np.median(r_values)), 2) if r_values else None,
    }


def _diff_summary(candidate_params: Dict) -> str:
    diffs = []
    for k, v in candidate_params.items():
        if k in LIVE_PARAMS and LIVE_PARAMS[k] != v:
            diffs.append(f"{k}: {LIVE_PARAMS[k]} -> {v}")
    return "; ".join(diffs) if diffs else "No parameter changes from live rule set"


def run_candidate_backtest(candidate_overrides: Dict, initiated_by: Optional[str] = None) -> Dict:
    """Run both the live-parameter baseline and the candidate over an
    identical bounded universe/window, persist the run, and return the
    comparison result. Raises BacktestRuleChangeError for business-rule
    failures (e.g. unknown parameter field, no active tickers)."""
    unknown = set(candidate_overrides.keys()) - CANDIDATE_OVERRIDABLE_FIELDS
    if unknown:
        raise BacktestRuleChangeError(f"Unknown parameter field(s): {sorted(unknown)}")

    candidate_params = {**LIVE_PARAMS, **candidate_overrides}
    live_params = dict(LIVE_PARAMS)

    tickers = _load_bounded_universe(UNIVERSE_SIZE)

    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=365 * LOOKBACK_YEARS)

    spy = yf.download("SPY", start=start_date.isoformat(), auto_adjust=True, progress=False)["Close"].squeeze()
    ftse = yf.download("^FTSE", start=start_date.isoformat(), auto_adjust=True, progress=False)["Close"].squeeze()
    today = pd.Timestamp.now().normalize()
    spy = spy[spy.index < today]
    ftse = ftse[ftse.index < today]

    chunks = []
    data = yf.download(tickers, start=start_date.isoformat(), auto_adjust=True, progress=False)["Close"]
    if isinstance(data, pd.Series):
        data = data.to_frame()
    data = data.dropna(axis=1, how="all")
    chunks.append(data)
    prices = pd.concat(chunks, axis=1).sort_index()
    prices = prices.reindex(spy.index).ffill().bfill()
    # Bounded run — no 3-year minimum history filter (would zero out a
    # 4-year window entirely for recently-listed tickers); tickers with
    # materially incomplete history simply produce fewer/no signals.
    prices = prices.dropna(axis=1, how="all")

    if prices.shape[1] == 0:
        raise BacktestRuleChangeError("No usable price data returned for the bounded universe.")

    regime_us = compute_risk_on(spy).reindex(prices.index).ffill().fillna(False).astype(bool)
    regime_uk = compute_risk_on(ftse).reindex(prices.index).ffill().fillna(False).astype(bool)
    atr = compute_atr(prices)
    volatility = prices.pct_change().rolling(60).std()

    def _run(params: Dict) -> Dict:
        signals = compute_signals(prices, params["lookback"], params["top_n"])
        pv, returns, trades_df = run_backtest(
            signals, prices, volatility, atr, regime_us, regime_uk,
            rebalance_freq=params["rebalance_freq"],
            atr_mult=params["atr_mult"],
            min_position_pct=params["min_position_pct"],
            max_position_pct=params["max_position_pct"],
            min_hold_days=params["min_hold_days"],
            risk_off_mode=params["risk_off_mode"],
            stop_loss_mode=params["stop_loss_mode"],
            initial_atr_mult=params["initial_atr_mult"],
            profit_atr_mult=params["profit_atr_mult"],
        )
        return _summarise_run(trades_df, returns)

    live_result = _run(live_params)
    candidate_result = _run(candidate_params)

    rule_diff_summary = _diff_summary(candidate_params)

    saved = create_backtest_rule_run(
        initiated_by=initiated_by,
        rule_diff_summary=rule_diff_summary,
        candidate_params=candidate_params,
        live_params=live_params,
        universe_tickers=list(prices.columns),
        universe_start_date=prices.index.min().date().isoformat(),
        universe_end_date=prices.index.max().date().isoformat(),
        candidate_result=candidate_result,
        live_result=live_result,
    )

    return {
        "id": str(saved["id"]),
        "created_at": saved["created_at"].isoformat(),
        "initiated_by": initiated_by,
        "rule_diff_summary": rule_diff_summary,
        "candidate_params": candidate_params,
        "live_params": live_params,
        "universe_tickers": list(prices.columns),
        "universe_start_date": prices.index.min().date().isoformat(),
        "universe_end_date": prices.index.max().date().isoformat(),
        "candidate_result": candidate_result,
        "live_result": live_result,
    }
