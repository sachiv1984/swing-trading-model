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

--- Algorithm provenance (ST-05, BLG-TECH-15, v9.0) ---

compute_signals/compute_atr/compute_risk_on/transaction_fee/backtest are no
longer ported/duplicated here — they are imported from
backend/services/strategy_engine.py, the single shared implementation also
used by production_strategy.py (repo root). Previously each caller carried
its own independently-maintained copy (the maintenance burden BLG-TECH-15
tracked, most concretely realised as BLG-BE-109/ST-01 needing the same fix
applied twice). See strategy_engine.py's own module docstring for the design
notes on reconciling the two callers' prior behavioural differences (regime
state as an explicit parameter — already this module's own convention,
adopted because production_strategy.py's globals-based version is unsafe to
mutate from this module's concurrent web-server process; and the trade
record field-naming schema).
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import yfinance as yf

from database import get_db, create_backtest_rule_run
from services.strategy_engine import (
    compute_risk_on,
    compute_atr,
    compute_signals,
    transaction_fee,
    compute_rebalance_dates,
    backtest,
)

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


def _max_drawdown_pct(returns: pd.Series) -> float:
    equity = (1 + returns).cumprod()
    dd = equity / equity.cummax() - 1
    return round(float(dd.min()) * 100, 2)


def _r_multiples(trades_df: pd.DataFrame) -> List[float]:
    """Canonical R formula (metrics_definitions.md 'R-Multiple (Canonical
    Server-Side)'): R = (exit - entry) / (entry - initial_stop). Trades
    without a qualifying initial stop (entry <= stop) are excluded, same
    qualifying conditions as the canonical server-side formula.

    Column names are strategy_engine.backtest()'s canonical schema (ST-05,
    BLG-TECH-15) — "Initial Stop"/"Entry"/"Exit", not the lower_snake_case
    names this function used before the consolidation."""
    if trades_df.empty:
        return []
    r_values = []
    for _, row in trades_df.iterrows():
        stop = row.get("Initial Stop")
        entry = row["Entry"]
        exitp = row["Exit"]
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
        round(float(trades_df["Was Profitable"].mean()) * 100, 2)
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
        pv, returns, trades_df = backtest(
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
