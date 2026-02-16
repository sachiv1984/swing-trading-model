"""
Analytics Router - Uses database session directly
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from services import AnalyticsService
from datetime import datetime

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/metrics")
async def get_analytics_metrics(
    period: str = Query(
        "all_time",
        regex="^(last_7_days|last_month|last_quarter|last_year|ytd|all_time)$"
    ),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive analytics metrics.
    
    Queries database directly for trades and portfolio history,
    then calculates metrics server-side.
    """
    try:
        # Query closed trades directly from database
        trades_query = text("""
            SELECT 
                id, ticker, market, entry_date, exit_date, shares,
                entry_price, exit_price, pnl, pnl_percent, exit_reason,
                entry_note, exit_note, tags, status
            FROM positions
            WHERE status = 'closed' AND exit_date IS NOT NULL
            ORDER BY exit_date ASC
        """)
        
        trades_result = db.execute(trades_query)
        trades = [
            {
                'id': str(row[0]),
                'ticker': row[1],
                'market': row[2],
                'entry_date': row[3].isoformat() if row[3] else None,
                'exit_date': row[4].isoformat() if row[4] else None,
                'shares': float(row[5]) if row[5] else 0,
                'entry_price': float(row[6]) if row[6] else 0,
                'exit_price': float(row[7]) if row[7] else 0,
                'pnl': float(row[8]) if row[8] else 0,
                'pnl_percent': float(row[9]) if row[9] else 0,
                'exit_reason': row[10],
                'entry_note': row[11],
                'exit_note': row[12],
                'tags': row[13],
                'status': row[14]
            }
            for row in trades_result
        ]
        
        # Query portfolio history
        history_query = text("""
            SELECT snapshot_date, total_value, cash_balance, positions_value, total_pnl
            FROM portfolio_snapshots
            ORDER BY snapshot_date ASC
        """)
        
        history_result = db.execute(history_query)
        portfolio_history = [
            {
                'snapshot_date': row[0].isoformat() if row[0] else None,
                'total_value': float(row[1]) if row[1] else 0,
                'cash_balance': float(row[2]) if row[2] else 0,
                'positions_value': float(row[3]) if row[3] else 0,
                'total_pnl': float(row[4]) if row[4] else 0
            }
            for row in history_result
        ]
        
        # Calculate metrics
        service = AnalyticsService(db)
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
