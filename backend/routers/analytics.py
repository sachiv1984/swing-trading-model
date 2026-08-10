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
import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
import numpy as np
import pandas as pd
from urllib.parse import urlparse, urlencode, urlunparse, parse_qs
from typing import Optional
from strategy_version_registry import resolve_version_window

# Run SI-02 DDL migrations only once per process — calling ensure_* on every
# /behavioural-drift request adds ~1–2s per DDL statement (BLG-OPS-64).
_si02_schema_ensured = False

# TTL cache for behavioural drift result (15-min TTL — data changes only when
# new trades close, which is infrequent relative to page load frequency).
_drift_cache: dict = {"result": None, "portfolio_id": None, "expires_at": 0.0}
_DRIFT_CACHE_TTL_SECONDS = 900


def _clean_db_url(url: str) -> str:
    """Strip Supabase-specific params (e.g. pgbouncer) not supported by libpq."""
    parsed = urlparse(url)
    params = parse_qs(parsed.query, keep_blank_values=True)
    params.pop("pgbouncer", None)
    new_query = urlencode({k: v[0] for k, v in params.items()})
    return urlunparse(parsed._replace(query=new_query))

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


def _build_trades_for_charts_with_join(cursor, since_date) -> list:
    """
    Attempt to build trades_for_charts with stop_price via positions JOIN.

    Returns list of trade dicts with stop_price populated from
    positions.initial_stop. If the position_id column does not exist in
    trade_history (migration pending), falls back to returning all trades
    with stop_price: null so analytics loads without error.
    """
    try:
        if since_date:
            cursor.execute("""
                SELECT
                    th.id,
                    th.ticker,
                    th.market,
                    th.entry_date,
                    th.exit_date,
                    th.entry_price,
                    th.exit_price,
                    th.shares,
                    CASE WHEN p.initial_stop IS NOT NULL
                              AND p.initial_stop < th.entry_price
                         THEN p.initial_stop
                         ELSE NULL
                    END AS stop_price,
                    th.pnl,
                    th.pnl_pct      AS pnl_percent,
                    th.exit_reason,
                    th.holding_days,
                    th.tags
                FROM trade_history th
                LEFT JOIN positions p ON th.position_id = p.id
                WHERE th.exit_date >= %s
                ORDER BY th.exit_date ASC
            """, (since_date,))
        else:
            cursor.execute("""
                SELECT
                    th.id,
                    th.ticker,
                    th.market,
                    th.entry_date,
                    th.exit_date,
                    th.entry_price,
                    th.exit_price,
                    th.shares,
                    CASE WHEN p.initial_stop IS NOT NULL
                              AND p.initial_stop < th.entry_price
                         THEN p.initial_stop
                         ELSE NULL
                    END AS stop_price,
                    th.pnl,
                    th.pnl_pct      AS pnl_percent,
                    th.exit_reason,
                    th.holding_days,
                    th.tags
                FROM trade_history th
                LEFT JOIN positions p ON th.position_id = p.id
                ORDER BY th.exit_date ASC
            """)

        trades_for_charts = []
        for row in cursor.fetchall():
            stop = row['stop_price']
            trades_for_charts.append({
                'id':           str(row['id']) if row['id'] else '',
                'ticker':       row['ticker'],
                'market':       row['market'],
                'entry_date':   row['entry_date'].isoformat() if row['entry_date'] else None,
                'exit_date':    row['exit_date'].isoformat() if row['exit_date'] else None,
                'entry_price':  round(float(row['entry_price']), 4) if row['entry_price'] else 0,
                'exit_price':   round(float(row['exit_price']), 4) if row['exit_price'] else 0,
                'shares':       round(float(row['shares']), 4) if row['shares'] else None,
                'stop_price':   round(float(stop), 4) if stop is not None else None,
                'pnl':          round(float(row['pnl']), 2) if row['pnl'] else 0,
                'pnl_percent':  round(float(row['pnl_percent']), 2) if row['pnl_percent'] else 0,
                'exit_reason':  row['exit_reason'],
                'holding_days': int(row['holding_days']) if row['holding_days'] else 0,
                'tags':         row['tags'] or None,
            })
        return trades_for_charts

    except psycopg2.errors.UndefinedColumn:
        # position_id column not yet in live trade_history table.
        # Migration (migration_add_position_id.sql) has not run yet.
        # Roll back the failed transaction so the cursor is still usable,
        # then fall back to trades without stop_price (all null).
        cursor.connection.rollback()
        print(
            "BLG-TECH-07: trade_history.position_id column not found. "
            "Run migration_add_position_id.sql to enable stop_price JOIN. "
            "Returning trades_for_charts with stop_price: null."
        )
        return _build_trades_for_charts_no_join(cursor, since_date)


def _build_trades_for_charts_no_join(cursor, since_date) -> list:
    """
    Fallback: trades_for_charts without stop_price (all null).
    Used when position_id migration has not yet run.
    """
    if since_date:
        cursor.execute("""
            SELECT
                id, ticker, market, entry_date, exit_date,
                entry_price, exit_price, shares, pnl, pnl_pct AS pnl_percent,
                exit_reason, holding_days, tags
            FROM trade_history
            WHERE exit_date >= %s
            ORDER BY exit_date ASC
        """, (since_date,))
    else:
        cursor.execute("""
            SELECT
                id, ticker, market, entry_date, exit_date,
                entry_price, exit_price, shares, pnl, pnl_pct AS pnl_percent,
                exit_reason, holding_days, tags
            FROM trade_history
            ORDER BY exit_date ASC
        """)

    trades_for_charts = []
    for row in cursor.fetchall():
        trades_for_charts.append({
            'id':           str(row['id']) if row['id'] else '',
            'ticker':       row['ticker'],
            'market':       row['market'],
            'entry_date':   row['entry_date'].isoformat() if row['entry_date'] else None,
            'exit_date':    row['exit_date'].isoformat() if row['exit_date'] else None,
            'entry_price':  round(float(row['entry_price']), 4) if row['entry_price'] else 0,
            'exit_price':   round(float(row['exit_price']), 4) if row['exit_price'] else 0,
            'shares':       round(float(row['shares']), 4) if row['shares'] else None,
            'stop_price':   None,  # not available without position_id migration
            'pnl':          round(float(row['pnl']), 2) if row['pnl'] else 0,
            'pnl_percent':  round(float(row['pnl_percent']), 2) if row['pnl_percent'] else 0,
            'exit_reason':  row['exit_reason'],
            'holding_days': int(row['holding_days']) if row['holding_days'] else 0,
            'tags':         row['tags'] or None,
        })
    return trades_for_charts


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
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise Exception("DATABASE_URL not configured")

        conn = psycopg2.connect(_clean_db_url(database_url))
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            # ----------------------------------------------------------------
            # Settings
            # ----------------------------------------------------------------
            cursor.execute("""
                SELECT min_trades_for_analytics
                FROM settings
                ORDER BY created_at DESC
                LIMIT 1
            """)
            settings_row = cursor.fetchone()
            min_trades = int(settings_row['min_trades_for_analytics']) if settings_row else 10

            # ----------------------------------------------------------------
            # Closed trades — for metric calculation
            # ----------------------------------------------------------------
            cursor.execute("""
                SELECT
                    id, ticker, market, entry_date, exit_date, shares,
                    entry_price, exit_price, pnl, pnl_pct, exit_reason,
                    holding_days, entry_note, exit_note, tags
                FROM trade_history
                ORDER BY exit_date ASC
            """)

            trades = []
            for row in cursor.fetchall():
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
            trades_for_charts = _build_trades_for_charts_with_join(cursor, since_date)

            # ----------------------------------------------------------------
            # Portfolio history
            # ----------------------------------------------------------------
            portfolio_history = []
            try:
                cursor.execute("""
                    SELECT
                        snapshot_date, total_value, cash_balance,
                        positions_value, total_pnl, position_count
                    FROM portfolio_history
                    ORDER BY snapshot_date ASC
                """)
                for row in cursor.fetchall():
                    portfolio_history.append({
                        'snapshot_date':   row['snapshot_date'].isoformat() if row['snapshot_date'] else None,
                        'total_value':     float(row['total_value']) if row['total_value'] else 0,
                        'cash_balance':    float(row['cash_balance']) if row['cash_balance'] else 0,
                        'positions_value': float(row['positions_value']) if row['positions_value'] else 0,
                        'total_pnl':       float(row['total_pnl']) if row['total_pnl'] else 0,
                        'position_count':  int(row['position_count']) if row['position_count'] else 0,
                    })
            except psycopg2.errors.UndefinedTable:
                print("portfolio_history table not found, using empty history")
                portfolio_history = []
            except Exception as e:
                print(f"Error fetching portfolio history: {e}")
                portfolio_history = []

        finally:
            cursor.close()
            conn.close()

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
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise Exception("DATABASE_URL not configured")

        conn = psycopg2.connect(_clean_db_url(database_url))
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            trades_with_stop = _build_trades_for_charts_with_join(cursor, None)
        finally:
            cursor.close()
            conn.close()

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
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise Exception("DATABASE_URL not configured")

        conn = psycopg2.connect(_clean_db_url(database_url))
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            trades_with_stop = _build_trades_for_charts_with_join(cursor, None)
        finally:
            cursor.close()
            conn.close()

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
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise Exception("DATABASE_URL not configured")

        conn = psycopg2.connect(_clean_db_url(database_url))
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            # ----------------------------------------------------------------
            # Core compliance counts
            # ----------------------------------------------------------------
            cursor.execute("""
                SELECT
                    COUNT(*)                                                   AS total_trades,
                    COUNT(CASE
                        WHEN (entry_note IS NOT NULL AND entry_note != '')
                          OR (exit_note  IS NOT NULL AND exit_note  != '')
                        THEN 1 END)                                            AS trades_with_notes,
                    COUNT(CASE
                        WHEN exit_reason IN ('Stop Loss Hit', 'Trailing Stop')
                        THEN 1 END)                                            AS stop_exits
                FROM trade_history
            """)
            row = cursor.fetchone()
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
                cursor.execute("""
                    SELECT
                        th.total_cost,
                        (
                            SELECT ph.total_value
                            FROM portfolio_history ph
                            WHERE ph.snapshot_date <= th.entry_date
                            ORDER BY ph.snapshot_date DESC
                            LIMIT 1
                        ) AS portfolio_value_at_entry
                    FROM trade_history th
                """)
                size_rows = cursor.fetchall()
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
                cursor.connection.rollback()
                avg_position_size_pct = 0.0
            except Exception:
                cursor.connection.rollback()
                avg_position_size_pct = 0.0

        finally:
            cursor.close()
            conn.close()

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
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise HTTPException(status_code=500, detail="DATABASE_URL not configured")

        conn = psycopg2.connect(_clean_db_url(database_url))
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT p.id, p.ticker, p.market, p.shares, p.current_price, p.pnl
                FROM positions p
                JOIN portfolios port ON p.portfolio_id = port.id
                WHERE p.status = 'open'
                  AND p.shares > 0
            """)
            open_positions = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

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
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise Exception("DATABASE_URL not configured")

        conn = psycopg2.connect(_clean_db_url(database_url))
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            # ----------------------------------------------------------------
            # validation_pass_rate_by_rule from pre_entry_validation_log
            # ----------------------------------------------------------------
            validation_pass_rate_by_rule = {}
            try:
                cursor.execute("""
                    SELECT rule_type,
                           COUNT(*) FILTER (WHERE status = 'pass') AS pass_count,
                           COUNT(*) FILTER (WHERE status != 'pass') AS fail_count
                    FROM pre_entry_validation_log
                    WHERE validated_at >= %s::timestamptz
                    GROUP BY rule_type
                """, (since_iso,))
                for row in cursor.fetchall():
                    total = int(row['pass_count']) + int(row['fail_count'])
                    pass_rate = round(int(row['pass_count']) / total, 4) if total else None
                    validation_pass_rate_by_rule[row['rule_type']] = {
                        "pass_rate": pass_rate,
                        "pass_count": int(row['pass_count']),
                        "fail_count": int(row['fail_count']),
                    }
            except psycopg2.errors.UndefinedTable:
                cursor.connection.rollback()
                validation_pass_rate_by_rule = {}

            # ----------------------------------------------------------------
            # top_rule_breach from pre_entry_validation_log
            # (most frequently failing rule in period)
            # ----------------------------------------------------------------
            top_rule_breach = None
            try:
                cursor.execute("""
                    SELECT rule_type, COUNT(*) AS fail_count
                    FROM pre_entry_validation_log
                    WHERE validated_at >= %s::timestamptz
                      AND status = 'fail'
                    GROUP BY rule_type
                    ORDER BY fail_count DESC
                    LIMIT 1
                """, (since_iso,))
                row = cursor.fetchone()
                if row:
                    top_rule_breach = row['rule_type']
            except psycopg2.errors.UndefinedTable:
                cursor.connection.rollback()

            # ----------------------------------------------------------------
            # events_per_week: red_flag_events in last 7 days
            # ----------------------------------------------------------------
            try:
                cursor.execute("""
                    SELECT COUNT(*) AS cnt
                    FROM red_flag_events
                    WHERE created_at >= %s::timestamptz
                """, (week_ago_iso,))
                row = cursor.fetchone()
                events_count = int(row['cnt']) if row else 0
                events_per_week = round(events_count / 7.0, 2)
            except psycopg2.errors.UndefinedTable:
                cursor.connection.rollback()
                events_per_week = 0.0

            # ----------------------------------------------------------------
            # override_rate: overrides / validation attempts in last 7 days
            # ----------------------------------------------------------------
            override_rate = None
            try:
                cursor.execute("""
                    SELECT COUNT(*) AS overrides
                    FROM red_flag_events
                    WHERE created_at >= %s::timestamptz
                      AND event_type = 'pre_entry_override'
                """, (week_ago_iso,))
                row = cursor.fetchone()
                overrides = int(row['overrides']) if row else 0

                cursor.execute("""
                    SELECT COUNT(*) AS attempts
                    FROM pre_entry_validation_log
                    WHERE validated_at >= %s::timestamptz
                """, (week_ago_iso,))
                row = cursor.fetchone()
                attempts = int(row['attempts']) if row else 0
                override_rate = round(overrides / attempts, 4) if attempts > 0 else None
            except psycopg2.errors.UndefinedTable:
                cursor.connection.rollback()
                override_rate = None

            # ----------------------------------------------------------------
            # trade_plan_adherence_rate (all-time)
            # ----------------------------------------------------------------
            trade_plan_adherence_rate = None
            try:
                cursor.execute("SELECT COUNT(*) AS total FROM trade_history")
                row = cursor.fetchone()
                total_trades = int(row['total']) if row else 0

                if total_trades > 0:
                    cursor.execute("""
                        SELECT COUNT(DISTINCT th.id) AS with_plan
                        FROM trade_history th
                        JOIN trade_plans tp ON tp.position_id = th.position_id
                    """)
                    row = cursor.fetchone()
                    with_plan = int(row['with_plan']) if row else 0
                    trade_plan_adherence_rate = round(with_plan / total_trades, 4)
            except (psycopg2.errors.UndefinedColumn, psycopg2.errors.UndefinedTable):
                cursor.connection.rollback()
                trade_plan_adherence_rate = None

        finally:
            cursor.close()
            conn.close()

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


def _compute_version_trade_metrics(cursor, start_date, end_date):
    """trade_count, win_rate, avg_R for closed trades with entry_date in [start_date, end_date).

    avg_R uses the canonical per-trade formula (metrics_definitions.md v1.7.0):
    R = (exit_price - entry_price) / (entry_price - initial_stop_price), via
    positions.initial_stop LEFT JOIN (same source as GET /analytics/r-multiple-distribution).
    Trades without a determinable stop are excluded from avg_R but still counted
    in trade_count and win_rate (win/loss is determinable from pnl alone).
    """
    end_clause = "AND th.entry_date < %s" if end_date is not None else ""
    params = [start_date] + ([end_date] if end_date is not None else [])

    query = f"""
        SELECT
            th.entry_price, th.exit_price, th.pnl,
            CASE WHEN p.initial_stop IS NOT NULL AND p.initial_stop < th.entry_price
                 THEN p.initial_stop ELSE NULL END AS stop_price
        FROM trade_history th
        LEFT JOIN positions p ON th.position_id = p.id
        WHERE th.exit_date IS NOT NULL
          AND th.entry_date >= %s
          {end_clause}
    """
    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
    except (psycopg2.errors.UndefinedColumn, psycopg2.errors.UndefinedTable):
        cursor.connection.rollback()
        rows = []

    trade_count = len(rows)
    if trade_count == 0:
        return {"trade_count": 0, "win_rate": None, "avg_R": None}

    winners = sum(1 for r in rows if (r["pnl"] or 0) > 0)
    win_rate = round(winners / trade_count, 4)

    r_values = []
    for r in rows:
        ep, sp, xp = r["entry_price"], r["stop_price"], r["exit_price"]
        if sp is None or ep is None or xp is None or ep <= sp:
            continue
        r_values.append((float(xp) - float(ep)) / (float(ep) - float(sp)))
    avg_R = round(sum(r_values) / len(r_values), 4) if r_values else None

    return {"trade_count": trade_count, "win_rate": win_rate, "avg_R": avg_R}


def _compute_arc5_composite_for_range(cursor, start_date, end_date):
    """Arc 5 compliance composite score (metrics_definitions.md 'Arc 5 Compliance
    Composite Score') computed over an arbitrary [start_date, end_date) range,
    generalising GET /analytics/arc5-compliance's rolling-7/30-day window to a
    strategy-version-scoped historical slice (Strategy Rules & System Intent
    Owner decision, 2026-07-23, v7.7 ST-01 — compliance_rate sources from this
    composite, not journal_completion_rate, per role charter §6 "same field
    must mean the same thing everywhere").

    Returns None if any required input is unavailable (mirrors the composite's
    documented "Composite Score Unavailability" fallback rule) — treats null
    override_rate / trade_plan_adherence_rate as 0.0 per metrics_definitions.md.
    """
    end_clause = "AND created_at < %s::timestamptz" if end_date is not None else ""
    validated_end_clause = "AND validated_at < %s::timestamptz" if end_date is not None else ""
    range_params = [start_date] + ([end_date] if end_date is not None else [])

    # override_rate: overrides / validation attempts, over the range
    override_rate = 0.0
    try:
        cursor.execute(f"""
            SELECT COUNT(*) AS overrides FROM red_flag_events
            WHERE created_at >= %s::timestamptz {end_clause}
              AND event_type = 'pre_entry_override'
        """, range_params)
        overrides = int(cursor.fetchone()["overrides"] or 0)

        cursor.execute(f"""
            SELECT COUNT(*) AS attempts FROM pre_entry_validation_log
            WHERE validated_at >= %s::timestamptz {validated_end_clause}
        """, range_params)
        attempts = int(cursor.fetchone()["attempts"] or 0)
        override_rate = round(overrides / attempts, 4) if attempts > 0 else 0.0
    except psycopg2.errors.UndefinedTable:
        cursor.connection.rollback()

    # events_per_week: red_flag_events over the range, normalised to a weekly rate
    events_per_week = 0.0
    try:
        cursor.execute(f"""
            SELECT COUNT(*) AS cnt FROM red_flag_events
            WHERE created_at >= %s::timestamptz {end_clause}
        """, range_params)
        events_count = int(cursor.fetchone()["cnt"] or 0)
        range_days = (end_date - start_date).days if end_date else (date.today() - start_date).days
        range_weeks = max(range_days / 7.0, 1 / 7.0)
        events_per_week = round(events_count / range_weeks, 2)
    except psycopg2.errors.UndefinedTable:
        cursor.connection.rollback()

    # trade_plan_adherence_rate: trades with plan / total closed trades, entry_date in range
    trade_plan_adherence_rate = 0.0
    try:
        end_clause_entry = "AND entry_date < %s" if end_date is not None else ""
        cursor.execute(f"""
            SELECT COUNT(*) AS total FROM trade_history
            WHERE exit_date IS NOT NULL AND entry_date >= %s {end_clause_entry}
        """, range_params)
        total_trades = int(cursor.fetchone()["total"] or 0)

        if total_trades > 0:
            cursor.execute(f"""
                SELECT COUNT(DISTINCT th.id) AS with_plan
                FROM trade_history th
                JOIN trade_plans tp ON tp.position_id = th.position_id
                WHERE th.exit_date IS NOT NULL AND th.entry_date >= %s {end_clause_entry}
            """, range_params)
            with_plan = int(cursor.fetchone()["with_plan"] or 0)
            trade_plan_adherence_rate = round(with_plan / total_trades, 4)
    except (psycopg2.errors.UndefinedColumn, psycopg2.errors.UndefinedTable):
        cursor.connection.rollback()

    # top_rule_breach severity, over the range
    severity_map = {
        "regime_gate": 1.0,
        "sector_concentration": 0.5,
        "earnings_proximity": 0.5,
        "cash_constraint": 0.5,
        "sizing_validity": 0.0,
    }
    top_rule_breach_severity_normalized = 0.0
    try:
        cursor.execute(f"""
            SELECT rule_type, COUNT(*) AS fail_count
            FROM pre_entry_validation_log
            WHERE validated_at >= %s::timestamptz {validated_end_clause}
              AND status = 'fail'
            GROUP BY rule_type
            ORDER BY fail_count DESC
            LIMIT 1
        """, range_params)
        row = cursor.fetchone()
        if row:
            top_rule_breach_severity_normalized = severity_map.get(row["rule_type"], 0.0)
    except psycopg2.errors.UndefinedTable:
        cursor.connection.rollback()

    composite_score = (
        (1 - override_rate) * 0.40
        + (1 - min(events_per_week / 10, 1)) * 0.30
        + trade_plan_adherence_rate * 0.20
        + (1 - top_rule_breach_severity_normalized) * 0.10
    )
    return round(composite_score, 4)


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
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise Exception("DATABASE_URL not configured")

        conn = psycopg2.connect(_clean_db_url(database_url))
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            eff_from_start, eff_from_end = _intersect_range(window_from[0], window_from[1], range_start, range_end)
            eff_to_start, eff_to_end = _intersect_range(window_to[0], window_to[1], range_start, range_end)

            metrics_from = _compute_version_trade_metrics(cursor, eff_from_start, eff_from_end)
            if metrics_from["trade_count"] < 10:
                raise HTTPException(status_code=422, detail={
                    "status": "error",
                    "code": "insufficient_data",
                    "message": f"Version '{version_from}' has only {metrics_from['trade_count']} trades — minimum 10 required for reliable comparison",
                    "version": version_from,
                    "trade_count": metrics_from["trade_count"],
                    "min_trades_required": 10,
                })

            metrics_to = _compute_version_trade_metrics(cursor, eff_to_start, eff_to_end)
            if metrics_to["trade_count"] < 10:
                raise HTTPException(status_code=422, detail={
                    "status": "error",
                    "code": "insufficient_data",
                    "message": f"Version '{version_to}' has only {metrics_to['trade_count']} trades — minimum 10 required for reliable comparison",
                    "version": version_to,
                    "trade_count": metrics_to["trade_count"],
                    "min_trades_required": 10,
                })

            compliance_from = _compute_arc5_composite_for_range(cursor, eff_from_start, eff_from_end)
            compliance_to = _compute_arc5_composite_for_range(cursor, eff_to_start, eff_to_end)
        finally:
            cursor.close()
            conn.close()

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
