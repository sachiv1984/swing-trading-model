"""
Analytics Router

GET /analytics/metrics — Comprehensive portfolio analytics for a given period.
GET /analytics/compliance-metrics — Discipline & compliance scalars (ST-01, v1.9).

BLG-TECH-07 fix: trades_for_charts attempts to source stop_price from
positions.initial_stop via LEFT JOIN on trade_history.position_id.

If the position_id column does not yet exist in the live trade_history table
(migration pending), the JOIN query falls back gracefully: stop_price returns
null for all trades, analytics loads normally, and no 500 error is raised.
Run migration_add_position_id.sql to enable the JOIN fully.

Contract: docs/specs/api_contracts/analytics_endpoints.md v1.8.1
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

        conn = psycopg2.connect(database_url)
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
        raise HTTPException(
            status_code=500,
            detail=f"Compliance metrics calculation failed: {str(e)}"
        )
