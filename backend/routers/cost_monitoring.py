"""
Cost Monitoring Router

GET  /ops/alpaca-call-report       — Alpaca API call count aggregate (daily/weekly).
GET  /ops/research-session-report  — Research endpoint external-call count per
                                      session, with baseline + anomaly flagging.
POST /ops/purge-audit-logs         — Delete gemini_audit_log/claude_audit_log/
                                      api_call_log rows past their retention window.

ST-11 (BLG-OPS-17) / ST-12 (BLG-OPS-20) / ST-13 (BLG-OPS-94), EPIC-03, v9.3.
ST-07 (BLG-OPS-154) / ST-08 (BLG-OPS-155) / ST-06 (BLG-OPS-153), EPIC-02, v9.5:
purge extended to api_call_log (90-day window, ST-07) and now surfaces a
possible_silent_failure signal when a purge reports 0 rows deleted but
stale rows are independently confirmed still present (ST-06 sub-item 3).
GET endpoints are read-only aggregates over api_call_log (backend/database.py).
POST /ops/purge-audit-logs is a write (delete) — protected by the app-wide
X-API-Key middleware like other maintenance endpoints (POST /portfolio/snapshot
etc.), not by a route-local dependency.

Contract: docs/specs/api_contracts/ops_endpoints.md v1.2
"""
import logging

from fastapi import APIRouter, Query

router = APIRouter(prefix="/ops", tags=["Cost Monitoring"])
logger = logging.getLogger(__name__)

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
    """Delete gemini_audit_log rows older than 90 days, claude_audit_log
    rows older than 730 days (24 months), and api_call_log rows older than
    90 days — enforces the retention windows documented in
    docs/ops/ai_audit_log_retention_policy.md (ST-13, BLG-OPS-94; api_call_log
    added ST-07, BLG-OPS-154, v9.5). Idempotent: safe to call repeatedly
    (e.g. from a daily scheduled workflow, matching this codebase's other
    maintenance endpoints like POST /portfolio/snapshot) — deletes nothing
    when no rows qualify.

    Silent-purge-failure visibility (ST-06 sub-item 3, BLG-OPS-153, v9.5):
    the purge functions fail safe (return 0 on any DB error), so a 0 result
    is ambiguous between "nothing to delete" and "purge is broken" (e.g. a
    permissions issue on the cron step). After each purge, an independent
    read-only count of rows still past that table's retention window
    disambiguates the two: 0 deleted + 0 still-stale rows is healthy; 0
    deleted + stale rows present is logged as a possible silent failure and
    listed in the response."""
    from database import (
        purge_gemini_audit_log_older_than_90_days,
        purge_claude_audit_log_older_than_730_days,
        purge_api_call_log_older_than_90_days,
        count_gemini_audit_log_older_than_90_days,
        count_claude_audit_log_older_than_730_days,
        count_api_call_log_older_than_90_days,
    )
    gemini_deleted = purge_gemini_audit_log_older_than_90_days()
    claude_deleted = purge_claude_audit_log_older_than_730_days()
    api_call_deleted = purge_api_call_log_older_than_90_days()

    stale_after_purge = {
        "gemini_audit_log": gemini_deleted == 0 and count_gemini_audit_log_older_than_90_days() > 0,
        "claude_audit_log": claude_deleted == 0 and count_claude_audit_log_older_than_730_days() > 0,
        "api_call_log": api_call_deleted == 0 and count_api_call_log_older_than_90_days() > 0,
    }
    possible_silent_failure = [table for table, is_stale in stale_after_purge.items() if is_stale]
    for table in possible_silent_failure:
        logger.warning(
            "purge_audit_logs: %s reported 0 rows deleted but stale rows are still present past its "
            "retention window -- possible silent purge failure",
            table,
        )

    return {
        "status": "ok",
        "data": {
            "gemini_audit_log_rows_deleted": gemini_deleted,
            "claude_audit_log_rows_deleted": claude_deleted,
            "api_call_log_rows_deleted": api_call_deleted,
            "possible_silent_failure": possible_silent_failure,
        },
    }
