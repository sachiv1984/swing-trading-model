"""
Analytics Router

GET /analytics/metrics — Comprehensive portfolio analytics for a given period.
GET /analytics/cohort  — Trade performance grouped by entry cohort period.
GET /analytics/r-multiple-distribution — Canonical server-side R-multiple distribution.
GET /analytics/compliance-metrics — Discipline & compliance scalars (ST-01, v1.9).
GET /analytics/market-correlation — Per-position Pearson correlation vs benchmark (ST-08, v2.7).
GET /analytics/arc5-compliance — Arc 5 signal compliance metrics (ST-01, v4.0).
GET /analytics/behavioural-drift — SI-02 behavioural drift detection (4 metrics, v4.6 ST-04).
GET /analytics/strategy-version-comparison — SI-04 strategy version performance comparison (ST-01, EPIC-01, v7.7).
GET /analytics/trade-plan-completion-rate — plans_created/completed/abandoned + completion_rate (ST-01, EPIC-01, v8.6).

BLG-TECH-07 fix: trades_for_charts attempts to source stop_price from
positions.initial_stop via LEFT JOIN on trade_history.position_id.

If the position_id column does not yet exist in the live trade_history table
(migration pending), the JOIN query falls back gracefully: stop_price returns
null for all trades, analytics loads normally, and no 500 error is raised.
Run migration_add_position_id.sql to enable the JOIN fully.

Contract: docs/specs/api_contracts/analytics_endpoints.md v2.2.0
"""

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from services.analytics_service import AnalyticsService
from datetime import date, timedelta, datetime, timezone
import time
import psycopg2
import numpy as np
import pandas as pd
from typing import Optional
from strategy_version_registry import resolve_version_window
from database import (
    get_db,
    get_trades_for_charts,
    get_min_trades_for_analytics,
    get_trade_history_for_analytics_metrics,
    get_portfolio_history_for_analytics,
    get_compliance_core_counts,
    get_position_size_entry_ratios,
    get_open_positions_for_correlation,
    get_arc5_validation_pass_rate_by_rule,
    get_arc5_top_rule_breach,
    get_arc5_events_per_week,
    get_arc5_override_rate,
    get_arc5_trade_plan_adherence_rate,
    get_version_trade_metrics,
    get_arc5_composite_for_range,
)

# Run SI-02 DDL migrations only once per process — calling ensure_* on every
# /behavioural-drift request adds ~1–2s per DDL statement (BLG-OPS-64).
_si02_schema_ensured = False

# TTL cache for behavioural drift result (15-min TTL — data changes only when
# new trades close, which is infrequent relative to page load frequency).
_drift_cache: dict = {"result": None, "portfolio_id": None, "expires_at": 0.0}
_DRIFT_CACHE_TTL_SECONDS = 900


# ST-08: module-level TTL cache for market correlation (one trading day ≈ 8 hours)
_CORRELATION_CACHE: dict = {"data": None, "cached_at": None}
_CORRELATION_CACHE_TTL_HOURS = 8

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def _period_to_since_date(period: str):
    """Convert period string to earliest exit_date cutoff. None = all_time."""
    today = date.today()
    period_map = {
        "all_time":     None,
        "last_7_days":  today - timedelta(days=7),
        "last_month":   today - timedelta(days=30),
        "last_quarter": today - timedelta(days=90),
        "last_year":    today - timedelta(days=365),
        "ytd":          date(today.year, 1, 1),
    }
    return period_map.get(period)


@router.get("/metrics")
async def get_analytics_metrics(
    period: str = Query(
        "all_time",
        pattern="^(last_7_days|last_month|last_quarter|last_year|ytd|all_time)$"
    )
):
    """
    Get comprehensive analytics metrics.

    trades_for_charts attempts to include stop_price from positions.initial_stop
    via LEFT JOIN (BLG-TECH-07). Falls back to stop_price: null for all trades
    if the position_id migration has not yet run.
    """
    try:
        with get_db() as conn:
            # ----------------------------------------------------------------
            # Settings
            # ----------------------------------------------------------------
            min_trades = get_min_trades_for_analytics(conn=conn)

            # ----------------------------------------------------------------
            # Closed trades — for metric calculation
            # ----------------------------------------------------------------
            trades = []
            for row in get_trade_history_for_analytics_metrics(conn=conn):
                trades.append({
                    'id':           str(row['id']) if row['id'] else '',
                    'ticker':       row['ticker'],
                    'market':       row['market'],
                    'entry_date':   row['entry_date'].isoformat() if row['entry_date'] else None,
                    'exit_date':    row['exit_date'].isoformat() if row['exit_date'] else None,
                    'shares':       float(row['shares']) if row['shares'] else 0,
                    'entry_price':  float(row['entry_price']) if row['entry_price'] else 0,
                    'exit_price':   float(row['exit_price']) if row['exit_price'] else 0,
                    'pnl':          float(row['pnl']) if row['pnl'] else 0,
                    'pnl_percent':  float(row['pnl_pct']) if row['pnl_pct'] else 0,
                    'exit_reason':  row['exit_reason'],
                    'holding_days': int(row['holding_days']) if row['holding_days'] else 0,
                    'entry_note':   row['entry_note'],
                    'exit_note':    row['exit_note'],
                    'tags':         row['tags'],
                })

            # ----------------------------------------------------------------
            # trades_for_charts — with stop_price via JOIN, or null fallback
            # ----------------------------------------------------------------
            since_date = _period_to_since_date(period)
            trades_for_charts = get_trades_for_charts(since_date, conn=conn)

            # ----------------------------------------------------------------
            # Portfolio history
            # ----------------------------------------------------------------
            portfolio_history = []
            for row in get_portfolio_history_for_analytics(conn=conn):
                portfolio_history.append({
                    'snapshot_date':   row['snapshot_date'].isoformat() if row['snapshot_date'] else None,
                    'total_value':     float(row['total_value']) if row['total_value'] else 0,
                    'cash_balance':    float(row['cash_balance']) if row['cash_balance'] else 0,
                    'positions_value': float(row['positions_value']) if row['positions_value'] else 0,
                    'total_pnl':       float(row['total_pnl']) if row['total_pnl'] else 0,
                    'position_count':  int(row['position_count']) if row['position_count'] else 0,
                })

        # ----------------------------------------------------------------
        # Calculate metrics via AnalyticsService
        # ----------------------------------------------------------------
        service = AnalyticsService()
        metrics = service.calculate_metrics_from_data(
            trades=trades,
            portfolio_history=portfolio_history,
            period=period,
            min_trades=min_trades,
        )

        # Override trades_for_charts with the JOIN result (or fallback)
        metrics["trades_for_charts"] = trades_for_charts

        # ST-02 (BLG-FEAT-09): data freshness — UTC timestamp of this computation
        metrics["last_sync_at"] = datetime.now(timezone.utc).isoformat()

        return {"status": "ok", "data": metrics}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Analytics calculation failed: {str(e)}"},
        )


@router.get("/cohort")
async def get_cohort_analysis(
    period: str = Query(
        "month",
        pattern="^(month|quarter|year)$"
    )
):
    """
    Get trade performance grouped by entry cohort period.

    Groups all closed trades by entry_date (month/quarter/year) and computes
    per-cohort trade count, win rate, avg R-multiple, and total P&L.

    R-multiple uses canonical server-side formula from metrics_definitions.md v1.7.0
    (requires positions.initial_stop via LEFT JOIN — null if migration not run).

    Contract: docs/specs/api_contracts/analytics_endpoints.md §GET /analytics/cohort
    """
    try:
        trades_with_stop = get_trades_for_charts(None)

        service = AnalyticsService()
        result = service.calculate_cohort(trades_with_stop, period)
        return {"status": "ok", "data": result}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Cohort analysis failed: {str(e)}"},
        )


@router.get("/r-multiple-distribution")
async def get_r_multiple_distribution():
    """
    Get canonical server-side R-multiple distribution across all closed trades.

    Uses formula: R = (exit_price - entry_price) / (entry_price - initial_stop_price)
    per metrics_definitions.md v1.7.0. Requires positions.initial_stop via LEFT JOIN.

    Returns 7-bucket distribution plus summary stats (median_r, pct_above_1r,
    avg_winner_r, avg_loser_r). Minimum 5 qualifying trades required.

    Contract: docs/specs/api_contracts/analytics_endpoints.md §GET /analytics/r-multiple-distribution
    """
    try:
        trades_with_stop = get_trades_for_charts(None)

        service = AnalyticsService()
        result = service.calculate_r_multiple_distribution(trades_with_stop)
        return {"status": "ok", "data": result}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"R-multiple distribution failed: {str(e)}"},
        )


@router.get("/compliance-metrics")
async def get_compliance_metrics():
    """
    GET /analytics/compliance-metrics

    Returns discipline and compliance scalars for all closed trades:
      - journal_completion_rate: % of trades with at least one journal note
      - stop_exit_rate: % of trades exited via stop-loss or trailing-stop
      - avg_position_size_pct: mean(total_cost / portfolio_value_at_entry) × 100
      - trade_count: denominator (total closed trades)

    Canonical formulas: metrics_definitions.md §Discipline & Compliance Metrics (v1.7.0)
    Spec: docs/specs/frontend/pages/analytics.md §17
    """
    try:
        with get_db() as conn:
            # ----------------------------------------------------------------
            # Core compliance counts
            # ----------------------------------------------------------------
            row = get_compliance_core_counts(conn=conn)
            total_trades    = int(row['total_trades'])   if row else 0
            trades_with_notes = int(row['trades_with_notes']) if row else 0
            stop_exits      = int(row['stop_exits'])     if row else 0

            journal_completion_rate = round((trades_with_notes / total_trades) * 100, 1) if total_trades else 0.0
            stop_exit_rate          = round((stop_exits / total_trades) * 100, 1)        if total_trades else 0.0

            # ----------------------------------------------------------------
            # Average position size % of portfolio at entry
            # Correlates each trade's entry_date to the closest portfolio
            # snapshot on or before that date.
            # ----------------------------------------------------------------
            avg_position_size_pct = 0.0
            try:
                size_rows = get_position_size_entry_ratios(conn=conn)
                ratios = []
                for sr in size_rows:
                    pv = float(sr['portfolio_value_at_entry']) if sr['portfolio_value_at_entry'] else None
                    tc = float(sr['total_cost'])               if sr['total_cost']               else None
                    if pv and pv > 0 and tc is not None:
                        ratios.append((tc / pv) * 100)
                if ratios:
                    avg_position_size_pct = round(sum(ratios) / len(ratios), 2)
            except psycopg2.errors.UndefinedTable:
                # portfolio_history table not yet created — return 0.0
                conn.rollback()
                avg_position_size_pct = 0.0
            except Exception:
                conn.rollback()
                avg_position_size_pct = 0.0

        return {
            "status": "ok",
            "data": {
                "journal_completion_rate": journal_completion_rate,
                "stop_exit_rate":          stop_exit_rate,
                "avg_position_size_pct":   avg_position_size_pct,
                "trade_count":             total_trades,
            }
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Compliance metrics calculation failed: {str(e)}"},
        )


# ---------------------------------------------------------------------------
# Helper — download price series via Yahoo Finance (reuses database utility)
# ---------------------------------------------------------------------------

def _download_series(ticker: str, lookback_days: int) -> pd.Series | None:
    """Return daily close price Series for ticker over lookback_days window.

    Uses the existing download_ticker_data utility so network behaviour is
    consistent with signal generation. Returns None on failure.
    """
    from database import download_ticker_data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=lookback_days + 60)  # buffer for weekends
    df = download_ticker_data(
        ticker,
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d'),
    )
    if df is None or 'close' not in df.columns or len(df) < 30:
        return None
    return df['close'].dropna()


def _pearson_corr(a: pd.Series, b: pd.Series) -> float | None:
    """Compute Pearson correlation of daily returns between two aligned series."""
    # Align on common dates
    common_idx = a.index.intersection(b.index)
    if len(common_idx) < 30:
        return None
    ret_a = a.loc[common_idx].pct_change().dropna()
    ret_b = b.loc[common_idx].pct_change().dropna()
    common_ret = ret_a.index.intersection(ret_b.index)
    if len(common_ret) < 30:
        return None
    corr = np.corrcoef(ret_a.loc[common_ret].values, ret_b.loc[common_ret].values)
    val = float(corr[0, 1])
    if np.isnan(val):
        return None
    return round(val, 4)


def _correlation_severity(corr: float | None) -> str:
    """Map correlation coefficient to severity label."""
    if corr is None:
        return "unknown"
    abs_corr = abs(corr)
    if abs_corr > 0.7:
        return "high"
    if abs_corr >= 0.3:
        return "moderate"
    return "low"


@router.get("/market-correlation")
async def get_market_correlation(
    lookback: int = Query(252, ge=30, le=756, description="Lookback window in trading days (default 252)")
):
    """
    GET /analytics/market-correlation

    Returns Pearson correlation coefficients between each open position and its
    relevant market benchmark over the requested lookback window:
      - US positions vs SPY
      - UK positions vs ^FTSE (FTSE 100 index)

    Also returns a portfolio-level equal-weighted average correlation.

    Response is cached with a TTL of 8 hours (approximately one trading day).
    Repeated calls within the TTL return the cached result.

    If Yahoo Finance data is unavailable for a position, that position is excluded
    from the correlation array and the portfolio average. The endpoint does not
    return 500 — it returns a partial result with an informational note.

    Severity thresholds: high > 0.7, moderate 0.3–0.7, low < 0.3 (absolute value).

    Contract: docs/specs/api_contracts/analytics_endpoints.md §GET /analytics/market-correlation
    """
    global _CORRELATION_CACHE

    # -----------------------------------------------------------------------
    # Check TTL cache
    # -----------------------------------------------------------------------
    now = datetime.now(timezone.utc)
    cached_at = _CORRELATION_CACHE.get("cached_at")
    if (
        _CORRELATION_CACHE.get("data") is not None
        and cached_at is not None
        and (now - cached_at).total_seconds() < _CORRELATION_CACHE_TTL_HOURS * 3600
    ):
        cached_response = dict(_CORRELATION_CACHE["data"])
        cached_response["cached"] = True
        return {"status": "ok", "data": cached_response}

    # -----------------------------------------------------------------------
    # Fetch open positions from DB
    # -----------------------------------------------------------------------
    try:
        open_positions = get_open_positions_for_correlation()

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"status": "error", "message": e.detail if isinstance(e.detail, str) else str(e.detail)},
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"DB error fetching positions: {str(e)}"},
        )

    if not open_positions:
        result = {
            "correlations": [],
            "portfolio_correlation": {"value": None, "severity": "unknown", "method": "equal_weighted_average"},
            "lookback_days": lookback,
            "computed_at": now.isoformat(),
            "cached": False,
            "data_source": "Yahoo Finance",
            "note": "No open positions found.",
        }
        return {"status": "ok", "data": result}

    # -----------------------------------------------------------------------
    # Download benchmarks once (re-used for all positions)
    # -----------------------------------------------------------------------
    spy_series = _download_series("SPY", lookback)
    ftse_series = _download_series("^FTSE", lookback)

    benchmarks_unavailable = spy_series is None and ftse_series is None

    # -----------------------------------------------------------------------
    # Compute per-position correlation
    # -----------------------------------------------------------------------
    correlations = []
    for pos in open_positions:
        ticker = pos['ticker']
        market = pos.get('market', 'US')

        benchmark_label = "SPY" if market == 'US' else "FTSE"
        benchmark_series = spy_series if market == 'US' else ftse_series

        if benchmark_series is None:
            correlations.append({
                "ticker": ticker,
                "market": market,
                "benchmark": benchmark_label,
                "correlation": None,
                "severity": "unknown",
                "lookback_days": lookback,
                "data_points": 0,
                "note": "Benchmark data unavailable",
            })
            continue

        stock_series = _download_series(
            ticker if market == 'US' else f"{ticker}.L",
            lookback
        )

        if stock_series is None:
            correlations.append({
                "ticker": ticker,
                "market": market,
                "benchmark": benchmark_label,
                "correlation": None,
                "severity": "unknown",
                "lookback_days": lookback,
                "data_points": 0,
                "note": "Price data unavailable for this ticker",
            })
            continue

        # Count common data points for transparency
        common = stock_series.index.intersection(benchmark_series.index)
        corr = _pearson_corr(stock_series, benchmark_series)

        correlations.append({
            "ticker": ticker,
            "market": market,
            "benchmark": benchmark_label,
            "correlation": corr,
            "severity": _correlation_severity(corr),
            "lookback_days": lookback,
            "data_points": len(common),
        })

    # -----------------------------------------------------------------------
    # Portfolio-level equal-weighted average
    # -----------------------------------------------------------------------
    valid_corrs = [c["correlation"] for c in correlations if c["correlation"] is not None]
    if valid_corrs:
        portfolio_corr_value = round(float(np.mean(valid_corrs)), 4)
    else:
        portfolio_corr_value = None

    portfolio_correlation = {
        "value": portfolio_corr_value,
        "severity": _correlation_severity(portfolio_corr_value),
        "method": "equal_weighted_average",
    }

    # -----------------------------------------------------------------------
    # Build and cache result
    # -----------------------------------------------------------------------
    note = None
    if benchmarks_unavailable:
        note = "Yahoo Finance data unavailable. Correlation data could not be computed. Retry later or check connectivity."

    result = {
        "correlations": correlations,
        "portfolio_correlation": portfolio_correlation,
        "lookback_days": lookback,
        "computed_at": now.isoformat(),
        "cached": False,
        "data_source": "Yahoo Finance",
    }
    if note:
        result["note"] = note

    _CORRELATION_CACHE["data"] = result
    _CORRELATION_CACHE["cached_at"] = now

    return {"status": "ok", "data": result}


@router.get("/arc5-compliance")
async def get_arc5_compliance(
    period: str = Query("7d", pattern="^(7d|30d)$")
):
    """
    GET /analytics/arc5-compliance

    Returns Arc 5 signal compliance metrics:
      - validation_pass_rate_by_rule: pass/fail rate per pre-entry rule in the period
      - events_per_week: red flag events in the last 7 days
      - override_rate: overrides / validation attempts in last 7 days
      - top_rule_breach: most frequent failing rule in the period
      - trade_plan_adherence_rate: trades with plan / total closed trades (all-time)

    period: 7d (default) | 30d

    Canonical metrics: docs/specs/metrics_definitions.md §Arc 5 Compliance Metrics
    Spec: docs/specs/api_contracts/analytics_endpoints.md §GET /analytics/arc5-compliance
    """
    days = 30 if period == "30d" else 7
    since_iso = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    week_ago_iso = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()

    try:
        with get_db() as conn:
            validation_pass_rate_by_rule = get_arc5_validation_pass_rate_by_rule(since_iso, conn=conn)
            top_rule_breach = get_arc5_top_rule_breach(since_iso, conn=conn)
            events_per_week = get_arc5_events_per_week(week_ago_iso, conn=conn)
            override_rate = get_arc5_override_rate(week_ago_iso, conn=conn)
            trade_plan_adherence_rate = get_arc5_trade_plan_adherence_rate(conn=conn)

        return {
            "status": "ok",
            "data": {
                "period": period,
                "validation_pass_rate_by_rule": validation_pass_rate_by_rule,
                "events_per_week": events_per_week,
                "override_rate": override_rate,
                "top_rule_breach": top_rule_breach,
                "trade_plan_adherence_rate": trade_plan_adherence_rate,
            },
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Arc 5 compliance metrics failed: {str(e)}"},
        )


@router.get("/tag-performance")
def get_tag_performance_endpoint(tags: str = Query(..., description="Comma-separated trade-plan tags")):
    """GET /analytics/tag-performance?tags={csv} — win rate & avg R per trade-plan tag (ST-05 BLG-FEAT-52).

    Reads only trade_plans.trade_tags and existing closed-trade linkage — no
    dependency on trade_annotations/PO-02 structures (ST-05 AC-04).
    Spec: docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md §4

    ST-01 (BLG-BE-86, v8.5): calls ensure_trade_plans_table() before querying
    trade_tags, matching the pattern already used by every trade_plans.py route.
    Without this, a staging DB whose trade_plans table predates the ST-05
    trade_tags migration (i.e. no request ever routed through trade_plans.py's
    own ensure_trade_plans_table() calls) 500s here on "column trade_tags does
    not exist" — this endpoint is the only trade_tags reader that skipped the
    ensure call.
    """
    from database import get_portfolio, get_tag_performance, ensure_trade_plans_table

    try:
        tag_list = [t.strip().lower() for t in tags.split(",") if t.strip()]
        if not tag_list:
            raise HTTPException(status_code=400, detail="At least one tag is required")

        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        ensure_trade_plans_table()
        result = get_tag_performance(str(portfolio["id"]), tag_list)
        return {"status": "ok", "data": result}
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"status": "error", "message": e.detail if isinstance(e.detail, str) else str(e.detail)},
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Tag performance failed: {str(e)}"},
        )


@router.get("/trade-plan-completion-rate")
def get_trade_plan_completion_rate_endpoint():
    """GET /analytics/trade-plan-completion-rate — plans_created, plans_completed,
    plans_abandoned, completion_rate (ST-01, BLG-FEAT-32, EPIC-01, v8.6).

    Calls ensure_trade_plans_table() before querying, matching the defensive
    pattern established by /tag-performance (ST-01, BLG-BE-86, v8.5).
    Spec: docs/specs/frontend/pages/analytics.md §21
    Design source: docs/design/2026-08-11__release-v8.6/trade-plan-completion-rate-metric/decision_record.md
    """
    from database import get_portfolio, get_trade_plan_completion_rate, ensure_trade_plans_table

    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        ensure_trade_plans_table()
        result = get_trade_plan_completion_rate(str(portfolio["id"]))
        return {"status": "ok", "data": result}
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"status": "error", "message": e.detail if isinstance(e.detail, str) else str(e.detail)},
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Trade plan completion rate failed: {str(e)}"},
        )


@router.get("/behavioural-drift")
async def get_behavioural_drift():
    """GET /analytics/behavioural-drift — SI-02 Behavioural Drift Detection.

    Returns 4 drift metrics (entry timing, sizing adherence, post-loss sizing,
    regime adherence) over a 90-day rolling window. Requires ≥10 closed trades.
    §13 PASS: display-only; no automated recommendations; no ML inference.
    Contract: docs/specs/api_contracts/behavioural_drift_contract.md
    Spec: docs/specs/metrics/si02_drift_score.md §2–§4
    """
    global _si02_schema_ensured
    from database import get_portfolio, get_behavioural_drift_data, get_closed_trade_entry_dates, ensure_si02_trade_plans_columns, ensure_si02_trade_history_indexes
    from services.behavioural_drift_service import compute_drift, compute_insufficient_data_streak, STREAK_LOOKBACK_DAYS

    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        portfolio_id = str(portfolio["id"])

        if not _si02_schema_ensured:
            ensure_si02_trade_plans_columns()
            ensure_si02_trade_history_indexes()
            _si02_schema_ensured = True

        now = time.monotonic()
        if (
            _drift_cache["result"] is not None
            and _drift_cache["portfolio_id"] == portfolio_id
            and now < _drift_cache["expires_at"]
        ):
            return {"status": "ok", "data": _drift_cache["result"]}

        drift_data = get_behavioural_drift_data(portfolio_id)
        result = compute_drift(drift_data)

        # ST-05 (EPIC-01, v8.2, BLG-FEAT-86): insufficient_data streak metric,
        # surfaced alongside the existing SI-02 gate note. Only computed when
        # relevant (status == insufficient_data) to avoid the extra query on
        # every request.
        if result.get("status") == "insufficient_data":
            entry_dates = get_closed_trade_entry_dates(portfolio_id, STREAK_LOOKBACK_DAYS)
            result.update(compute_insufficient_data_streak(entry_dates))

        _drift_cache["result"] = result
        _drift_cache["portfolio_id"] = portfolio_id
        _drift_cache["expires_at"] = now + _DRIFT_CACHE_TTL_SECONDS
        return {"status": "ok", "data": result}

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"status": "error", "message": e.detail if isinstance(e.detail, str) else str(e.detail)},
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "status": "ok",
            "data": {
                "status": "error",
                "analysis_window_days": 90,
                "trade_count_in_window": 0,
                "metrics": [],
                "computed_at": datetime.now(timezone.utc).isoformat(),
                "error_detail": str(e),
            },
        }


# -----------------------------------------------------------------------
# SI-04 Strategy Version Comparison (ST-01, EPIC-01, v7.7, BLG-FEAT-75)
# -----------------------------------------------------------------------

def _intersect_range(window_start, window_end, range_start, range_end):
    """Intersect a version's [start, end) window with an optional date_range filter.

    window_end/range_end of None means open-ended (no upper bound).
    Returns (effective_start, effective_end_or_None).
    """
    effective_start = max(window_start, range_start) if range_start else window_start
    if window_end is None and range_end is None:
        effective_end = None
    elif window_end is None:
        effective_end = range_end
    elif range_end is None:
        effective_end = window_end
    else:
        effective_end = min(window_end, range_end)
    return effective_start, effective_end


@router.get("/strategy-version-comparison")
async def get_strategy_version_comparison(
    version_from: str = Query(..., description="Baseline strategy version label"),
    version_to: str = Query(..., description="Comparison strategy version label (must be chronologically after version_from)"),
    date_range: Optional[str] = Query(None, description="ISO 8601 date range filter: YYYY-MM-DD/YYYY-MM-DD"),
):
    """GET /analytics/strategy-version-comparison — SI-04 strategy version performance comparison.

    Trades are attributed to a strategy version by entry_date falling within
    that version's active window (see backend/strategy_version_registry.py —
    there is no strategy_version column on trade_history; windows are derived
    from claude/strategy/strategy_rules.md's own Change Log dates).

    compliance_rate sources from the Arc 5 compliance composite score
    (metrics_definitions.md), generalised to the version's date window —
    Strategy Rules & System Intent Owner decision, 2026-07-23 (v7.7 ST-01):
    journal_completion_rate was rejected as measuring reflection habit, not
    rule-following discipline; reusing the "compliance_rate" name for a
    different concept than Arc 5's existing composite would be intent drift
    (role charter §6).

    §13 binding conditions (6, cleared v4.7): read-only, closed trades only,
    no strategy/position modification, advisory only, read-only registry access.
    Contract: docs/specs/api_contracts/strategy_version_comparison_contract.md v0.2.0
    """
    window_from = resolve_version_window(version_from)
    window_to = resolve_version_window(version_to)

    if window_from is None or window_to is None:
        missing = version_from if window_from is None else version_to
        return JSONResponse(status_code=404, content={
            "status": "error",
            "code": "version_not_found",
            "message": f"Strategy version '{missing}' not found in version registry",
            "missing_version": missing,
        })

    if window_to[0] <= window_from[0]:
        return JSONResponse(status_code=400, content={
            "status": "error",
            "code": "version_order_error",
            "message": "version_to must be chronologically after version_from",
        })

    range_start, range_end = None, None
    if date_range:
        try:
            start_str, end_str = date_range.split("/")
            range_start = date.fromisoformat(start_str)
            range_end = date.fromisoformat(end_str)
            if range_end < range_start:
                raise ValueError("date_range end before start")
        except ValueError:
            return JSONResponse(status_code=422, content={
                "status": "error",
                "code": "invalid_date_range",
                "message": "date_range must be formatted YYYY-MM-DD/YYYY-MM-DD with end on or after start",
            })

    try:
        with get_db() as conn:
            eff_from_start, eff_from_end = _intersect_range(window_from[0], window_from[1], range_start, range_end)
            eff_to_start, eff_to_end = _intersect_range(window_to[0], window_to[1], range_start, range_end)

            metrics_from = get_version_trade_metrics(eff_from_start, eff_from_end, conn=conn)
            if metrics_from["trade_count"] < 10:
                raise HTTPException(status_code=422, detail={
                    "status": "error",
                    "code": "insufficient_data",
                    "message": f"Version '{version_from}' has only {metrics_from['trade_count']} trades — minimum 10 required for reliable comparison",
                    "version": version_from,
                    "trade_count": metrics_from["trade_count"],
                    "min_trades_required": 10,
                })

            metrics_to = get_version_trade_metrics(eff_to_start, eff_to_end, conn=conn)
            if metrics_to["trade_count"] < 10:
                raise HTTPException(status_code=422, detail={
                    "status": "error",
                    "code": "insufficient_data",
                    "message": f"Version '{version_to}' has only {metrics_to['trade_count']} trades — minimum 10 required for reliable comparison",
                    "version": version_to,
                    "trade_count": metrics_to["trade_count"],
                    "min_trades_required": 10,
                })

            compliance_from = get_arc5_composite_for_range(eff_from_start, eff_from_end, conn=conn)
            compliance_to = get_arc5_composite_for_range(eff_to_start, eff_to_end, conn=conn)

        performance_delta = round(metrics_to["avg_R"] - metrics_from["avg_R"], 4) if (metrics_to["avg_R"] is not None and metrics_from["avg_R"] is not None) else None
        win_rate_delta = round(metrics_to["win_rate"] - metrics_from["win_rate"], 4) if (metrics_to["win_rate"] is not None and metrics_from["win_rate"] is not None) else None
        avg_R_delta = performance_delta
        trade_count_delta = metrics_to["trade_count"] - metrics_from["trade_count"]
        assessment = "Improved" if (avg_R_delta is not None and avg_R_delta >= 0) else "Degraded"

        return {
            "version_from": version_from,
            "version_to": version_to,
            "date_range": date_range,
            "version_from_metrics": {
                "trade_count": metrics_from["trade_count"],
                "win_rate": metrics_from["win_rate"],
                "avg_R": metrics_from["avg_R"],
                "performance_delta": None,
                "compliance_rate": compliance_from,
            },
            "version_to_metrics": {
                "trade_count": metrics_to["trade_count"],
                "win_rate": metrics_to["win_rate"],
                "avg_R": metrics_to["avg_R"],
                "performance_delta": performance_delta,
                "compliance_rate": compliance_to,
            },
            "comparison_summary": {
                "win_rate_delta": win_rate_delta,
                "avg_R_delta": avg_R_delta,
                "trade_count_delta": trade_count_delta,
                "assessment": assessment,
            },
        }

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"status": "error", "message": e.detail if isinstance(e.detail, str) else str(e.detail)},
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Strategy version comparison failed: {str(e)}"},
        )
