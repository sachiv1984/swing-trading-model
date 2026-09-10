"""
Cost Monitoring Router

GET  /ops/alpaca-call-report       — Alpaca API call count aggregate (daily/weekly).
GET  /ops/research-session-report  — Research endpoint external-call count per
                                      session, with baseline + anomaly flagging.
POST /ops/purge-audit-logs         — Delete gemini_audit_log/claude_audit_log
                                      rows past their retention window.

ST-11 (BLG-OPS-17) / ST-12 (BLG-OPS-20) / ST-13 (BLG-OPS-94), EPIC-03, v9.3.
GET endpoints are read-only aggregates over api_call_log (backend/database.py).
POST /ops/purge-audit-logs is a write (delete) — protected by the app-wide
X-API-Key middleware like other maintenance endpoints (POST /portfolio/snapshot
etc.), not by a route-local dependency.

Contract: docs/specs/api_contracts/ops_endpoints.md v1.1
"""
from fastapi import APIRouter, Query

router = APIRouter(prefix="/ops", tags=["Cost Monitoring"])

# ST-12 (BLG-OPS-20): anomaly threshold, single source of truth for the
# ">2x baseline" acceptance criterion. database.py's get_api_session_report()
# default mirrors this value — kept here as the one configurable constant
# callers/operators would actually tune.
ANOMALY_MULTIPLIER = 2.0


@router.get("/alpaca-call-report")
def alpaca_call_report(window: str = Query(default="daily", pattern="^(daily|weekly)$")):
    """Alpaca API call count for the requested window (ST-11)."""
    from database import get_api_call_report
    return {"status": "ok", "data": get_api_call_report("alpaca", window)}


@router.get("/research-session-report")
def research_session_report():
    """Research endpoint per-session external-call counts, baseline, and
    anomaly-flagged sessions over the last 7 days (ST-12)."""
    from database import get_api_session_report
    return {"status": "ok", "data": get_api_session_report("research", anomaly_multiplier=ANOMALY_MULTIPLIER)}


@router.post("/purge-audit-logs")
def purge_audit_logs():
    """Delete gemini_audit_log rows older than 90 days and claude_audit_log
    rows older than 730 days (24 months) — enforces the retention windows
    documented in docs/ops/ai_audit_log_retention_policy.md (ST-13,
    BLG-OPS-94). Idempotent: safe to call repeatedly (e.g. from a daily
    scheduled workflow, matching this codebase's other maintenance endpoints
    like POST /portfolio/snapshot) — deletes nothing when no rows qualify."""
    from database import purge_gemini_audit_log_older_than_90_days, purge_claude_audit_log_older_than_730_days
    gemini_deleted = purge_gemini_audit_log_older_than_90_days()
    claude_deleted = purge_claude_audit_log_older_than_730_days()
    return {
        "status": "ok",
        "data": {
            "gemini_audit_log_rows_deleted": gemini_deleted,
            "claude_audit_log_rows_deleted": claude_deleted,
        },
    }
