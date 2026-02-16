"""
Analytics Router - Uses database connection directly
"""

from fastapi import APIRouter, Query, HTTPException
from services.analytics_service import AnalyticsService
import os
import psycopg2
from psycopg2.extras import RealDictCursor

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/metrics")
async def get_analytics_metrics(
    period: str = Query(
        "all_time",
        regex="^(last_7_days|last_month|last_quarter|last_year|ytd|all_time)$"
    )
):
    """
    Get comprehensive analytics metrics.
    
    Queries database directly and calculates metrics.
    """
    try:
        # Get database URL from environment
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise Exception("DATABASE_URL not configured")
        
        # Connect to database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Query closed positions
            cursor.execute("""
                SELECT 
                    id, ticker, market, entry_date, exit_date, shares,
                    entry_price, exit_price, pnl, pnl_percent, exit_reason
                FROM positions
                WHERE status = 'closed' AND exit_date IS NOT NULL
                ORDER BY exit_date ASC
            """)
            
            trades = []
            for row in cursor.fetchall():
                trades.append({
                    'id': str(row['id']) if row['id'] else '',
                    'ticker': row['ticker'],
                    'market': row['market'],
                    'entry_date': row['entry_date'].isoformat() if row['entry_date'] else None,
                    'exit_date': row['exit_date'].isoformat() if row['exit_date'] else None,
                    'shares': float(row['shares']) if row['shares'] else 0,
                    'entry_price': float(row['entry_price']) if row['entry_price'] else 0,
                    'exit_price': float(row['exit_price']) if row['exit_price'] else 0,
                    'pnl': float(row['pnl']) if row['pnl'] else 0,
                    'pnl_percent': float(row['pnl_percent']) if row['pnl_percent'] else 0,
                    'exit_reason': row['exit_reason']
                })
            
            # Query portfolio snapshots
            cursor.execute("""
                SELECT 
                    snapshot_date, total_value, cash_balance, 
                    positions_value, total_pnl
                FROM portfolio_snapshots
                ORDER BY snapshot_date ASC
            """)
            
            portfolio_history = []
            for row in cursor.fetchall():
                portfolio_history.append({
                    'snapshot_date': row['snapshot_date'].isoformat() if row['snapshot_date'] else None,
                    'total_value': float(row['total_value']) if row['total_value'] else 0,
                    'cash_balance': float(row['cash_balance']) if row['cash_balance'] else 0,
                    'positions_value': float(row['positions_value']) if row['positions_value'] else 0,
                    'total_pnl': float(row['total_pnl']) if row['total_pnl'] else 0
                })
            
        finally:
            cursor.close()
            conn.close()
        
        # Calculate metrics
        service = AnalyticsService()
        metrics = service.calculate_metrics_from_data(
            trades=trades,
            portfolio_history=portfolio_history,
            period=period
        )
        
        return {"status": "ok", "data": metrics}
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Analytics calculation failed: {str(e)}"
        )
