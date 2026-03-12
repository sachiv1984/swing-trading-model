"""
Analytics Router

GET /analytics/metrics — Comprehensive portfolio analytics for a given period.
GET /analytics/cohort  — Trade performance grouped by entry cohort period.
GET /analytics/r-multiple-distribution — Canonical server-side R-multiple distribution.

BLG-TECH-07 fix: trades_for_charts attempts to source stop_price from
positions.initial_stop via LEFT JOIN on trade_history.position_id.

If the position_id column does not yet exist in the live trade_history table
(migration pending), the JOIN query falls back gracefully: stop_price returns
null for all trades, analytics loads normally, and no 500 error is raised.
Run migration_add_position_id.sql to enable the JOIN fully.

Contract: docs/specs/api_contracts/analytics_endpoints.md v1.9.2
"""

from fastapi import APIRouter, Query, HTTPException
from services.analytics_service import AnalyticsService
from datetime import date, timedelta
import os
import psycopg2
from psycopg2.extras import RealDictCursor

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
                entry_price, exit_price, pnl, pnl_pct AS pnl_percent,
                exit_reason, holding_days, tags
            FROM trade_history
            WHERE exit_date >= %s
            ORDER BY exit_date ASC
        """, (since_date,))
    else:
        cursor.execute("""
            SELECT
                id, ticker, market, entry_date, exit_date,
                entry_price, exit_price, pnl, pnl_pct AS pnl_percent,
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
        regex="^(last_7_days|last_month|last_quarter|last_year|ytd|all_time)$"
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

        conn = psycopg2.connect(database_url)
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

        return {"status": "ok", "data": metrics}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Analytics calculation failed: {str(e)}"
        )


@router.get("/cohort")
async def get_cohort_analysis(
    period: str = Query(
        "month",
        regex="^(month|quarter|year)$"
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

        conn = psycopg2.connect(database_url)
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
        raise HTTPException(
            status_code=500,
            detail=f"Cohort analysis failed: {str(e)}"
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

        conn = psycopg2.connect(database_url)
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
        raise HTTPException(
            status_code=500,
            detail=f"R-multiple distribution failed: {str(e)}"
        )
