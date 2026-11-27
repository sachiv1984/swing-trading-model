"""
Weekly Trading Digest Router

GET /digest/weekly — 7-day summary of realised P&L, unrealised P&L delta,
alert activity, journal completion rate, and staleness.

POST /digest/events — Record one core-loop event (ST-17, v9.18): the
Weekly Digest opened, or a Today list action taken.

POST /digest/si05/send — Trigger the SI-05 Phase 1 strategy integrity digest
via Telegram. Intended for weekly cron/scheduled invocation.

Contracts: docs/specs/api_contracts/digest_endpoints.md v0.8
ST-08 (BLG-FEAT-14 BE component, v2.4) / ST-01 (SI-05 Phase 1, v5.1)
ST-08 (BLG-BE-35, v5.3) — API key auth on POST /digest/si05/send
"""

import os
import logging
import threading

from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from database import (
    ensure_loop_events_table,
    get_weekly_digest_data,
    record_loop_event,
)


def _verify_api_key(x_api_key: str = Header(default=None)) -> bool:
    """
    Require X-API-Key header matching API_KEY env var.
    When API_KEY is not set the dependency is a no-op (local dev parity with
    the global middleware in main.py).

    Returns True when authorised, False otherwise — the caller endpoint
    returns the canonical error envelope itself (ST-08, BLG-BE-69) rather
    than this dependency raising HTTPException directly, since a FastAPI
    Depends() callable cannot itself produce a JSONResponse body: an
    exception raised here propagates straight to FastAPI's default handler
    (the {"detail": ...} shape this story exists to eliminate), bypassing any
    try/except the endpoint function might otherwise use to translate it.
    """
    expected = os.environ.get("API_KEY")
    return not (expected and x_api_key != expected)


logger = logging.getLogger(__name__)

from services.si05_digest_service import send_si05_digest

router = APIRouter(prefix="/digest", tags=["Digest"])


@router.get("/weekly")
def get_weekly_digest():
    """
    GET /digest/weekly

    Returns a 7-day trading digest with raw numeric/boolean fields:

    - realised_pnl_7d: sum of P&L for trades closed in the last 7 calendar days (GBP)
    - unrealised_pnl_delta_7d: change in total unrealised P&L over the last 7 days
      (current unrealised P&L minus unrealised P&L 7 days ago from portfolio snapshots)
    - alerts_fired_7d: count of notifications created in the last 7 days
    - alerts_dismissed_7d: count of notifications marked read in the last 7 days
    - journal_completion_rate_current: % of all closed trades with an entry or exit note
    - journal_completion_rate_7d_ago: the same rate for trades closed before the 7-day window
    - closed_trades_total / closed_trades_total_7d_ago: the two denominators
    - compliance_score_current / compliance_score_7d_ago: deprecated aliases of
      journal_completion_rate_* (ST-14, v9.18, BLG-SPEC-204)
    - loop: this ISO week's five core-loop counts (ST-17; week_start, signals,
      plans, entries, reflections, reviews; a count is null when its query fails)
    - red_flags_7d: count of red_flag_events created in the last 7 days (ST-16; null on query failure)
    - staleness_hours: hours since last portfolio snapshot (null if no snapshots)
    - as_of_utc: UTC timestamp this response was computed

    Scope constraint: no generated text, narrative, or interpretation in any field.

    Spec: docs/specs/api_contracts/digest_endpoints.md v0.8
    """
    try:
        data = get_weekly_digest_data()
        return {"status": "ok", "data": data}
    except Exception as e:
        logger.error("Weekly digest endpoint error: %s", e)
        return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to compute weekly digest"})


# The two recorded events (data_model.md DS-43 CHECK). Kept here, not imported,
# so the tests' database stub cannot replace it; tests/test_digest_events_router.py
# asserts it equals database.LOOP_EVENT_TYPES.
LOOP_EVENT_TYPES = ("weekly_digest_opened", "due_today_action")


class LoopEventRequest(BaseModel):
    event_type: str
    dry_run: bool = False


_loop_events_table_ready = False
# Sync handlers run in a threadpool: two first calls after a deploy must not
# both run CREATE TABLE (Postgres can raise a pg_type UniqueViolation).
_loop_events_table_lock = threading.Lock()


@router.post("/events")
def post_loop_event(body: LoopEventRequest):
    """
    POST /digest/events

    Record one core-loop event (metrics_definitions.md §Core Loop Metrics):
    `weekly_digest_opened` (the Weekly Digest page, once per load) or
    `due_today_action` (a click on a Today list link). Nothing else is
    tracked. `dry_run: true` validates the request and writes nothing, so the
    System Status endpoint test never adds an event that would count as a
    review.

    Spec: docs/specs/api_contracts/digest_endpoints.md v0.8 (ST-17, v9.18)
    """
    global _loop_events_table_ready
    if body.event_type not in LOOP_EVENT_TYPES:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": f"event_type must be one of: {', '.join(LOOP_EVENT_TYPES)}"},
        )
    if body.dry_run:
        return {"status": "ok", "data": {"event_type": body.event_type, "written": False}}
    try:
        if not _loop_events_table_ready:
            with _loop_events_table_lock:
                if not _loop_events_table_ready:
                    ensure_loop_events_table()
                    _loop_events_table_ready = True
        record_loop_event(body.event_type)
        return {"status": "ok", "data": {"event_type": body.event_type, "written": True}}
    except Exception as e:
        logger.error("Loop event write failed: %s", e)
        return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to record event"})


@router.post("/si05/send")
def send_si05_digest_endpoint(authorized: bool = Depends(_verify_api_key)):
    """
    POST /digest/si05/send

    Trigger the SI-05 Phase 1 weekly strategy integrity digest via Telegram.
    Fetches arc5-compliance data (SI-01 + SI-03) and sends a formatted MarkdownV2
    message per docs/product/decisions/si05-telegram-message-format-spec.md (BLG-GOV-86).

    Intended to be called by a weekly scheduler (Render cron or external scheduler).
    Safe to retry — idempotent per call (message reflects current DB state).

    Spec: docs/specs/api_contracts/digest_endpoints.md v0.2
    ST-01 (SI-05 Phase 1, EPIC-01, v5.1)
    """
    if not authorized:
        return JSONResponse(status_code=401, content={"status": "error", "message": "Unauthorized"})
    result = send_si05_digest()
    if result["sent"]:
        return {"status": "ok", **result}
    return {"status": "error", **result}
