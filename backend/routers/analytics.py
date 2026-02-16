"""
Analytics Router - Uses existing service functions
"""

from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from services import AnalyticsService, get_trade_history_with_stats, get_performance_history


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
    
    Uses existing service functions to fetch data,
    then calculates metrics server-side.
    """
    try:
        # Use existing trade service to get trades
        # get_trade_history_with_stats returns {trades: [...], ...}
        trade_data = get_trade_history_with_stats(db)
        trades = trade_data.get("trades", [])
        
        # Convert trade objects to dicts
        trades_list = []
        for trade in trades:
            trades_list.append({
                'id': str(trade.get('id', '')),
                'ticker': trade.get('ticker'),
                'market': trade.get('market'),
                'entry_date': trade.get('entry_date'),
                'exit_date': trade.get('exit_date'),
                'shares': trade.get('shares', 0),
                'entry_price': trade.get('entry_price', 0),
                'exit_price': trade.get('exit_price', 0),
                'pnl': trade.get('pnl', 0),
                'pnl_percent': trade.get('pnl_percent', 0),
                'exit_reason': trade.get('exit_reason')
            })
        
        # Use existing portfolio service to get history
        # get_performance_history returns list of snapshots
        try:
            portfolio_history_raw = get_performance_history(db, days=365)
            portfolio_history = []
            for snapshot in portfolio_history_raw:
                portfolio_history.append({
                    'snapshot_date': snapshot.get('date') or snapshot.get('snapshot_date'),
                    'total_value': snapshot.get('total_value', 0),
                    'cash_balance': snapshot.get('cash_balance', 0),
                    'positions_value': snapshot.get('positions_value', 0),
                    'total_pnl': snapshot.get('total_pnl', 0)
                })
        except Exception as e:
            print(f"Error fetching portfolio history: {e}")
            portfolio_history = []
        
        # Calculate metrics
        service = AnalyticsService()
        metrics = service.calculate_metrics_from_data(
            trades=trades_list,
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
