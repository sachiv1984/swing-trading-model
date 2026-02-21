"""
Validation Router

BLG-TECH-03: Router is now thin — HTTP handling only.
             All business logic delegated to ValidationService
             per backend_engineering_patterns.md §3.

Canonical spec: analytics_endpoints.md v1.8.1
"""

from fastapi import APIRouter, HTTPException
from services.validation_service import ValidationService

router = APIRouter(prefix="/validate", tags=["Validation"])


@router.post("/calculations")
async def validate_calculations():
    """
    Validate all analytics calculations against the test portfolio.

    No request body required — validates against internal test data.
    Delegates entirely to ValidationService.

    Returns:
        dict: Validation results per analytics_endpoints.md v1.8.1
    """
    try:
        service = ValidationService()
        data = service.validate_all()
        return {"status": "ok", "data": data}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Validation failed: {str(e)}",
        )