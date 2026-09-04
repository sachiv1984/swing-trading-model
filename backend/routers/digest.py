"""
Weekly Trading Digest Router

GET /digest/weekly — 7-day summary of realised P&L, unrealised P&L delta,
alert activity, compliance score, and staleness.

POST /digest/si05/send — Trigger the SI-05 Phase 1 strategy integrity digest
via Telegram. Intended for weekly cron/scheduled invocation.

Contracts: docs/specs/api_contracts/digest_endpoints.md v0.4
ST-08 (BLG-FEAT-14 BE component, v2.4) / ST-01 (SI-05 Phase 1, v5.1)
ST-08 (BLG-BE-35, v5.3) — API key auth on POST /digest/si05/send
"""

import os
import logging

from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse

from database import get_weekly_digest_data


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
    - compliance_score_current: journal_completion_rate from all closed trades (%)
    - compliance_score_7d_ago: journal_completion_rate for trades closed before 7 days ago (%)
    - staleness_hours: hours since last portfolio snapshot (null if no snapshots)
    - as_of_utc: UTC timestamp this response was computed

    Scope constraint: no generated text, narrative, or interpretation in any field.

    Spec: docs/specs/api_contracts/digest_endpoints.md v0.1
    """
    try:
        data = get_weekly_digest_data()
        return {"status": "ok", "data": data}
    except Exception as e:
        logger.error("Weekly digest endpoint error: %s", e)
        return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to compute weekly digest"})


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
