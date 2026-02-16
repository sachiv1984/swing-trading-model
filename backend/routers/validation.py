from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from validation_service import ValidationService
from analytics_service import AnalyticsService

router = APIRouter(prefix="/validate", tags=["Validation"])


@router.post("/calculations")
async def validate_calculations(db: Session = Depends(get_db)):
    """
    Validate all analytics calculations against test portfolio.

    No request body required - validates against internal test data.

    Returns:
        dict: Validation results with pass/warn/fail for each metric
    """
    try:
        # Initialize services
        analytics_service = AnalyticsService(db)
        validation_service = ValidationService(analytics_service)

        # Run all validations
        results = validation_service.validate_all()

        return {"status": "ok", "data": results}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Validation failed: {str(e)}"
        )
