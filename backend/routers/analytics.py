"""
Analytics Router - Comprehensive Trading Metrics
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from services import AnalyticsService

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
    
    All calculations done server-side.
    Frontend just displays the results.
    
    Query Parameters:
        period: Time period for analysis
            - last_7_days
            - last_month
            - last_quarter
            - last_year
            - ytd (year to date)
            - all_time (default)
    
    Returns:
        Complete metrics including executive summary, advanced metrics,
        market comparison, exit reasons, monthly data, top performers, etc.
    """
    try:
        service = AnalyticsService(db)
        metrics = service.get_metrics(period=period)
        
        return {"status": "ok", "data": metrics}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analytics calculation failed: {str(e)}"
        )
