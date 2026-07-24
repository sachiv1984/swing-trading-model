"""
Alerts Router

Endpoints for alert rules, evaluation, notification feed, and notification preferences.

IMPORTANT — router ordering constraint (spec §Router ordering constraint):
  POST /notifications/mark-all-read MUST be declared before PATCH /notifications/{id}.
  If declared after, FastAPI routes mark-all-read to the PATCH handler with id="mark-all-read".

Contract: docs/specs/api_contracts/alerts_endpoints.md v0.1
"""

from fastapi import APIRouter, BackgroundTasks, Body, HTTPException
from pydantic import BaseModel, field_validator
from typing import Any, Dict, Optional
from database import get_portfolio
from services.health_service import record_alert_evaluation
from services.alerts_service import (
    get_alert_rules,
    create_alert_rule,
    update_alert_rule,
    delete_alert_rule,
    evaluate_alerts,
    get_alert_history,
    get_notifications,
    mark_notification_read,
    mark_all_notifications_read,
    get_preferences,
    update_preferences,
    deliver_notification,
    get_price_alerts,
    create_price_alert,
    delete_price_alert,
    ALERT_TYPES,
)

router = APIRouter(tags=["Alerts"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_portfolio_id() -> str:
    portfolio = get_portfolio()
    if not portfolio:
        raise HTTPException(status_code=500, detail="Portfolio not found")
    return str(portfolio["id"])


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class CreateAlertRuleRequest(BaseModel):
    type: str
    enabled: bool = True
    threshold_percent: Optional[float] = None

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        if v not in ALERT_TYPES:
            raise ValueError(f"type must be one of: {ALERT_TYPES}")
        return v

    @field_validator("threshold_percent")
    @classmethod
    def validate_threshold(cls, v):
        if v is not None and not (0 < v <= 100):
            raise ValueError("threshold_percent must be > 0 and <= 100")
        return v


class UpdateAlertRuleRequest(BaseModel):
    enabled: Optional[bool] = None
    threshold_percent: Optional[float] = None

    @field_validator("threshold_percent")
    @classmethod
    def validate_threshold(cls, v):
        if v is not None and not (0 < v <= 100):
            raise ValueError("threshold_percent must be > 0 and <= 100")
        return v


class CreatePriceAlertRequest(BaseModel):
    ticker: str
    condition: str
    threshold_price: float

    @field_validator("condition")
    @classmethod
    def validate_condition(cls, v):
        if v not in ("above", "below"):
            raise ValueError("condition must be 'above' or 'below'")
        return v


# ---------------------------------------------------------------------------
# Alert Rules
# ---------------------------------------------------------------------------

@router.get("/alerts/rules")
def get_alert_rules_endpoint():
    """
    Return all alert rules for the portfolio.
    Seeds defaults on first use.
    Contract: alerts_endpoints.md §GET /alerts/rules
    """
    try:
        portfolio_id = _get_portfolio_id()
        rules = get_alert_rules(portfolio_id)
        return {"status": "ok", "data": rules}
    except HTTPException:
        raise
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alerts/rules")
def create_alert_rule_endpoint(request: CreateAlertRuleRequest):
    """
    Create an alert rule. Returns 400 if type already exists.
    Contract: alerts_endpoints.md §POST /alerts/rules
    """
    try:
        portfolio_id = _get_portfolio_id()
        if request.type == "stop_loss_approach" and request.threshold_percent is None:
            raise HTTPException(status_code=400, detail="threshold_percent is required for stop_loss_approach")
        rule = create_alert_rule(portfolio_id, request.model_dump())
        return {"status": "ok", "data": rule}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/alerts/rules/{rule_id}")
def update_alert_rule_endpoint(rule_id: str, request: UpdateAlertRuleRequest):
    """
    Partial update of an alert rule.
    Contract: alerts_endpoints.md §PATCH /alerts/rules/{rule_id}
    """
    try:
        portfolio_id = _get_portfolio_id()
        rule = update_alert_rule(portfolio_id, rule_id, request.model_dump(exclude_none=True))
        return {"status": "ok", "data": rule}
    except HTTPException:
        raise
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/alerts/rules/{rule_id}")
def delete_alert_rule_endpoint(rule_id: str):
    """
    Delete an alert rule.
    Contract: alerts_endpoints.md §DELETE /alerts/rules/{rule_id}
    """
    try:
        portfolio_id = _get_portfolio_id()
        result = delete_alert_rule(portfolio_id, rule_id)
        return {"status": "ok", "data": result}
    except HTTPException:
        raise
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Custom Price Alerts (ST-02, BLG-FE-116, EPIC-02, v7.5)
# Contract: docs/specs/api_contracts/alerts_endpoints.md §Custom Price Alerts
# ---------------------------------------------------------------------------

@router.get("/price-alerts")
def get_price_alerts_endpoint():
    """
    Return all custom price alerts for the portfolio, most recently created first.
    Contract: alerts_endpoints.md §GET /price-alerts
    """
    try:
        portfolio_id = _get_portfolio_id()
        data = get_price_alerts(portfolio_id)
        return {"status": "ok", "data": data}
    except HTTPException:
        raise
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/price-alerts")
def create_price_alert_endpoint(request: CreatePriceAlertRequest):
    """
    Create a custom price alert. Returns 400 for invalid input or when the
    per-portfolio active-alert cap (50) is exceeded.
    Contract: alerts_endpoints.md §POST /price-alerts
    """
    try:
        portfolio_id = _get_portfolio_id()
        alert = create_price_alert(portfolio_id, request.model_dump())
        return {"status": "ok", "data": alert}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/price-alerts/{alert_id}")
def delete_price_alert_endpoint(alert_id: str):
    """
    Delete a custom price alert.
    Contract: alerts_endpoints.md §DELETE /price-alerts/{id}
    """
    try:
        portfolio_id = _get_portfolio_id()
        result = delete_price_alert(portfolio_id, alert_id)
        return {"status": "ok", "data": result}
    except HTTPException:
        raise
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Alert Evaluation
# ---------------------------------------------------------------------------

@router.post("/alerts/evaluate")
def evaluate_alerts_endpoint(background_tasks: BackgroundTasks):
    """
    Evaluate all enabled alert rules. Enqueues email delivery as BackgroundTasks.
    Contract: alerts_endpoints.md §POST /alerts/evaluate
    """
    try:
        portfolio_id = _get_portfolio_id()

        def enqueue(notification_id: str):
            background_tasks.add_task(deliver_notification, notification_id)

        result = evaluate_alerts(portfolio_id, enqueue)
        record_alert_evaluation()
        return {"status": "ok", "data": result}
    except HTTPException:
        raise
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts/history")
def get_alert_history_endpoint(last_n_days: Optional[int] = None, last_n_records: Optional[int] = None):
    """
    Return alert evaluation history, newest first.
    Contract: alerts_endpoints.md §GET /alerts/history
    """
    try:
        portfolio_id = _get_portfolio_id()
        data = get_alert_history(portfolio_id, last_n_days=last_n_days, last_n_records=last_n_records)
        return {"status": "ok", "data": data}
    except HTTPException:
        raise
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Notifications
# IMPORTANT: mark-all-read MUST be declared before /{id} — see module docstring
# ---------------------------------------------------------------------------

@router.get("/notifications")
def get_notifications_endpoint(page: int = 1, since_days: Optional[int] = None, read: Optional[bool] = None):
    """
    Return notification feed, newest first, paginated (50/page).
    Optional `since_days` / `read` filters (v0.6, ST-02/EPIC-02/v7.7).
    Contract: alerts_endpoints.md §GET /notifications
    """
    try:
        if page < 1:
            raise HTTPException(status_code=400, detail="page must be a positive integer")
        if since_days is not None and since_days < 1:
            raise HTTPException(status_code=400, detail="since_days must be a positive integer")
        portfolio_id = _get_portfolio_id()
        data = get_notifications(portfolio_id, page, since_days=since_days, read=read)
        return {"status": "ok", "data": data}
    except HTTPException:
        raise
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/notifications/mark-all-read")
def mark_all_read_endpoint():
    """
    Mark all unread notifications as read.
    Contract: alerts_endpoints.md §POST /notifications/mark-all-read
    NOTE: Must be declared before PATCH /notifications/{id} in this file.
    """
    try:
        portfolio_id = _get_portfolio_id()
        result = mark_all_notifications_read(portfolio_id)
        return {"status": "ok", "data": result}
    except HTTPException:
        raise
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Notification Preferences
# NOTE: Both preferences routes must be declared before PATCH /notifications/{id}
#       so that the literal path segment "preferences" is not swallowed by the
#       {notification_id} wildcard.
# ---------------------------------------------------------------------------

@router.get("/notifications/preferences")
def get_preferences_endpoint():
    """
    Return notification preferences. Seeds defaults on first use.
    Contract: alerts_endpoints.md §GET /notifications/preferences
    """
    try:
        portfolio_id = _get_portfolio_id()
        data = get_preferences(portfolio_id)
        return {"status": "ok", "data": data}
    except HTTPException:
        raise
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/notifications/preferences")
def update_preferences_endpoint(request: Dict[str, Any] = Body(...)):
    """
    Partial update of notification preferences.
    Body: {alert_type: {"email_enabled": bool}, ...}
    Contract: alerts_endpoints.md §PATCH /notifications/preferences
    NOTE: Must be declared before PATCH /notifications/{id} in this file.
    """
    try:
        portfolio_id = _get_portfolio_id()
        if not request:
            raise HTTPException(status_code=400, detail="No alert type keys provided")
        data = update_preferences(portfolio_id, request)
        return {"status": "ok", "data": data}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/notifications/{notification_id}")
def mark_notification_read_endpoint(notification_id: str):
    """
    Mark a single notification as read. Idempotent.
    Contract: alerts_endpoints.md §PATCH /notifications/{id}
    """
    try:
        portfolio_id = _get_portfolio_id()
        notif = mark_notification_read(portfolio_id, notification_id)
        return {"status": "ok", "data": notif}
    except HTTPException:
        raise
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
