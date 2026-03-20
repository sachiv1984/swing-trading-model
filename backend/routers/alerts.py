"""
Alerts Router

Endpoints for alert rules, evaluation, notification feed, and notification preferences.

IMPORTANT — router ordering constraint (spec §Router ordering constraint):
  POST /notifications/mark-all-read MUST be declared before PATCH /notifications/{id}.
  If declared after, FastAPI routes mark-all-read to the PATCH handler with id="mark-all-read".

Contract: docs/specs/api_contracts/alerts_endpoints.md v0.1
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, field_validator
from typing import Optional
from database import get_portfolio
from services.alerts_service import (
    get_alert_rules,
    create_alert_rule,
    update_alert_rule,
    delete_alert_rule,
    evaluate_alerts,
    get_notifications,
    mark_notification_read,
    mark_all_notifications_read,
    get_preferences,
    update_preferences,
    deliver_notification,
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
        return {"status": "ok", "data": result}
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
def get_notifications_endpoint(page: int = 1):
    """
    Return notification feed, newest first, paginated (50/page).
    Contract: alerts_endpoints.md §GET /notifications
    """
    try:
        if page < 1:
            raise HTTPException(status_code=400, detail="page must be a positive integer")
        portfolio_id = _get_portfolio_id()
        data = get_notifications(portfolio_id, page)
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


# ---------------------------------------------------------------------------
# Notification Preferences
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
def update_preferences_endpoint(request: dict):
    """
    Partial update of notification preferences.
    Body: {alert_type: {"email_enabled": bool}, ...}
    Contract: alerts_endpoints.md §PATCH /notifications/preferences
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
