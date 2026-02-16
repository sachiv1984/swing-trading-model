"""
Analytics Router - Queries database tables directly
"""

from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.analytics_service import AnalyticsService

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
    
    Queries database tables directly and calculates metrics.
    """
    try:
        # Import table models - these should exist in your database
        from sqlalchemy import Table, MetaData
        
        metadata = MetaData()
        metadata.reflect(bind=db.bind)
        
        # Get positions table
        positions_table = metadata.tables.get('positions')
        if positions_table is None:
            raise Exception("Positions table not found")
        
        # Query closed positions
        from sqlalchemy import select
        stmt = select(positions_table).where(
            positions_table.c.status == 'closed',
            positions_table.c.exit_date.isnot(None)
        ).order_by(positions_table.c.exit_date)
        
        result = db.execute(stmt)
        
        # Convert to dicts
        trades = []
        for row in result:
            trades.append({
                'id': str(row.id) if hasattr(row, 'id') else '',
                'ticker': row.ticker if hasattr(row, 'ticker') else '',
                'market': row.market if hasattr(row, 'market') else '',
                'entry_date': row.entry_date.isoformat() if hasattr(row, 'entry_date') and row.entry_date else None,
                'exit_date': row.exit_date.isoformat() if hasattr(row, 'exit_date') and row.exit_date else None,
                'shares': float(row.shares) if hasattr(row, 'shares') and row.shares else 0,
                'entry_price': float(row.entry_price) if hasattr(row, 'entry_price') and row.entry_price else 0,
                'exit_price': float(row.exit_price) if hasattr(row, 'exit_price') and row.exit_price else 0,
                'pnl': float(row.pnl) if hasattr(row, 'pnl') and row.pnl else 0,
                'pnl_percent': float(row.pnl_percent) if hasattr(row, 'pnl_percent') and row.pnl_percent else 0,
                'exit_reason': row.exit_reason if hasattr(row, 'exit_reason') else None
            })
        
        # Get portfolio snapshots table
        portfolio_history = []
        snapshots_table = metadata.tables.get('portfolio_snapshots')
        if snapshots_table is not None:
            stmt = select(snapshots_table).order_by(snapshots_table.c.snapshot_date)
            result = db.execute(stmt)
            
            for row in result:
                portfolio_history.append({
                    'snapshot_date': row.snapshot_date.isoformat() if hasattr(row, 'snapshot_date') and row.snapshot_date else None,
                    'total_value': float(row.total_value) if hasattr(row, 'total_value') and row.total_value else 0,
                    'cash_balance': float(row.cash_balance) if hasattr(row, 'cash_balance') and row.cash_balance else 0,
                    'positions_value': float(row.positions_value) if hasattr(row, 'positions_value') and row.positions_value else 0,
                    'total_pnl': float(row.total_pnl) if hasattr(row, 'total_pnl') and row.total_pnl else 0
                })
        
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
