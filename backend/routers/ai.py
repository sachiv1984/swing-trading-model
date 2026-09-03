"""
AI Router

POST /ai/journal-summary      — Summarise trade journal notes via external LLM API.
POST /ai/daily-briefing       — Plain-English portfolio briefing + ordered action list.
POST /ai/chat                 — Stateless per-request AI trade advisor.
GET  /ai/claude-audit-log     — Query the immutable Claude API call audit trail.
GET  /ai/monthly-cost         — Current calendar month's Claude API spend total.

AI output is display-only and must NOT feed into any signal, scoring,
or recommendation pipeline. SRB-v1.7 CONDITIONALLY COMPLIANT.

Contract: docs/specs/api_contracts/ai_endpoints.md v1.7
"""

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import date
from database import fetch_journal_notes
from services.ai_service import summarise_journal_notes
from services.ai_audit_service import log_ai_summary_run, query_audit_log
from services.rate_limiter import _ai_limiter
from config import AI_DAILY_COST_THRESHOLD

# Per-endpoint rate limits (requests per minute per IP)
_DAILY_BRIEFING_LIMIT = 10
_CHAT_LIMIT = 30
_JOURNAL_SUMMARY_LIMIT = 10  # ST-08 (EPIC-08, v7.8, BLG-SEC-21) — calls Claude directly, was previously unlimited

router = APIRouter(prefix="/ai", tags=["AI"])


class JournalSummaryRequest(BaseModel):
    trade_ids: Optional[list[int]] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None


class JournalSummaryResponse(BaseModel):
    summary: Optional[str]
    trade_count: int
    model: Optional[str]
    cached: bool
    message: Optional[str]


@router.post("/journal-summary", response_model=JournalSummaryResponse)
def journal_summary(body: JournalSummaryRequest, request: Request):
    """
    Summarise entry/exit journal notes from closed trades.
    Accepts trade_ids or date_from/date_to range.
    Returns LLM-generated plain-text summary.
    AI output is display-only — not used in any calculation.

    Rate limit: 10 requests/minute/IP (ST-08, EPIC-08, v7.8, BLG-SEC-21) —
    calls Claude directly via services.ai_service; was previously unlimited.
    """
    client_ip = request.client.host if request.client else "unknown"
    allowed, retry_after = _ai_limiter.is_allowed(
        f"journal-summary:{client_ip}", limit=_JOURNAL_SUMMARY_LIMIT
    )
    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"status": "error", "message": "Rate limit exceeded. Try again later."},
            headers={"Retry-After": str(retry_after)},
        )
    if not body.trade_ids and not body.date_from and not body.date_to:
        return JSONResponse(
            status_code=422,
            content={"status": "error", "message": "Provide trade_ids or at least one of date_from / date_to."},
        )

    rows = fetch_journal_notes(
        trade_ids=body.trade_ids, date_from=body.date_from, date_to=body.date_to
    )

    notes = []
    for row in rows:
        if row.get("entry_note") and str(row["entry_note"]).strip():
            notes.append(str(row["entry_note"]).strip())
        if row.get("exit_note") and str(row["exit_note"]).strip():
            notes.append(str(row["exit_note"]).strip())

    result = summarise_journal_notes(notes)

    # Audit log — record every invocation (BLG-AI-01)
    try:
        log_ai_summary_run(
            trade_ids=body.trade_ids,
            date_from=body.date_from,
            date_to=body.date_to,
            trade_count=len(rows),
            model_version=result.get("model"),
            summary_text=result.get("summary"),
        )
    except Exception:
        pass  # Audit log failure must not block the summary response

    return JournalSummaryResponse(
        summary=result["summary"],
        trade_count=len(rows),
        model=result["model"],
        cached=False,
        message=result["message"],
    )


@router.get("/journal-summary/history")
def journal_summary_history(
    trade_id: Optional[int] = Query(default=None, description="Filter by trade ID"),
    date_from: Optional[date] = Query(default=None),
    date_to: Optional[date] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
):
    """
    Query the AI journal summary audit log.

    Supports filtering by trade_id (array contains) and invoked_at date range.
    Returns audit records newest first — no summary text stored, only metadata.
    """
    records = query_audit_log(
        trade_id=trade_id,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
    )
    return {"ok": True, "data": {"records": records, "count": len(records)}}


@router.post("/check-daily-cost")
def check_daily_cost():
    """
    Check today's Claude API spend against the configured threshold.
    Sends Telegram alert if threshold exceeded.
    Intended to be called by a daily scheduler (Render cron / external scheduler).
    """
    from services.gemini_service import check_and_alert_daily_cost
    return check_and_alert_daily_cost(threshold_usd=AI_DAILY_COST_THRESHOLD)


class DailyBriefingResponse(BaseModel):
    summary: Optional[str]
    actions: List[Any]
    generated_at: str
    advisory: bool
    model: Optional[str] = None
    error: Optional[str] = None


@router.post("/daily-briefing", response_model=DailyBriefingResponse)
def daily_briefing(request: Request):
    """
    Assemble live portfolio context and call claude-sonnet-4-6 to produce a
    plain-English daily briefing with an ordered action list.
    Advisory-only — SRB-v1.7. Not integrated with trade execution.
    Rate limit: 10 requests/minute/IP. Contract: docs/specs/api_contracts/ai_endpoints.md v1.5
    """
    client_ip = request.client.host if request.client else "unknown"
    allowed, retry_after = _ai_limiter.is_allowed(
        f"daily-briefing:{client_ip}", limit=_DAILY_BRIEFING_LIMIT
    )
    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"status": "error", "message": "Rate limit exceeded. Try again later."},
            headers={"Retry-After": str(retry_after)},
        )
    from services.ai_service import generate_daily_briefing
    return generate_daily_briefing()


class ChatRequest(BaseModel):
    question: str
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    response: str
    advisory: bool
    model: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
def ai_chat_endpoint(body: ChatRequest, request: Request):
    """
    Stateless per-request AI trade advisor grounded in live portfolio and signal state.
    No session memory is stored or returned across calls.
    Advisory-only — SRB-v1.7. Not integrated with trade execution.
    Rate limit: 30 requests/minute/IP. Contract: docs/specs/api_contracts/ai_endpoints.md v1.5
    """
    client_ip = request.client.host if request.client else "unknown"
    allowed, retry_after = _ai_limiter.is_allowed(
        f"chat:{client_ip}", limit=_CHAT_LIMIT
    )
    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"status": "error", "message": "Rate limit exceeded. Try again later."},
            headers={"Retry-After": str(retry_after)},
        )
    from services.ai_service import ai_chat
    return ai_chat(question=body.question, context_opts=body.context)


@router.get("/claude-audit-log")
def get_claude_audit_log(
    limit: int = Query(default=50, ge=1, le=200),
    endpoint: str = Query(default=None, description="Filter to an exact endpoint value, e.g. 'POST /ai/daily-briefing'"),
    date_from: str = Query(default=None, description="Inclusive lower bound, YYYY-MM-DD, applied to generated_at"),
    date_to: str = Query(default=None, description="Inclusive upper bound, YYYY-MM-DD, applied to generated_at"),
):
    """
    Query the Claude API audit trail (claude_audit_log table).
    Returns the most recent Claude API call records, newest first.
    Intended for cost review and compliance monitoring.
    AI-generated content is NOT included — audit metadata only.

    ST-11 (BLG-BE-51, v7.0): optional `endpoint` and `date_from`/`date_to`
    filters — independently or combined with each other and with `limit`.
    Omitting all three preserves the original unfiltered behaviour.
    """
    from database import query_claude_audit_log
    records = query_claude_audit_log(limit=limit, endpoint=endpoint, date_from=date_from, date_to=date_to)
    return {"ok": True, "data": {"records": records, "count": len(records)}}


@router.get("/monthly-cost")
def get_monthly_cost():
    """
    Return the current calendar month's Claude API spend total.

    Read-only, no side effects (unlike POST /ai/check-daily-cost, which sends
    a Telegram alert as a side effect and is not suitable for a page-load
    fetch). Source: claude_audit_log, the immutable Claude API call audit
    trail. Claude is the only AI provider integrated in this codebase.

    ST-07 (EPIC-07, v7.6, BLG-FEAT-77 — reframed per ESC-EXEC-20260720-01).
    Contract: docs/specs/api_contracts/ai_endpoints.md#GET /ai/monthly-cost
    """
    from database import get_monthly_claude_cost
    result = get_monthly_claude_cost()
    return {"status": "ok", "data": result}


@router.get("/spend-trend")
def get_spend_trend():
    """
    Return Claude API spend for the last 6 release cycles, oldest to
    newest, for the Settings page's AI spend trend chart.

    Read-only. Source: claude_audit_log (existing data, no new collection),
    bucketed by release-cycle date windows parsed from
    docs/product/changelog.md's version headings. Renders whatever cycles
    exist if fewer than 6 are available -- no zero-padding.

    ST-06 (EPIC-06, v7.8, BLG-FEAT-82).
    Contract: docs/specs/api_contracts/ai_endpoints.md#GET /ai/spend-trend
    """
    from services.ai_spend_trend_service import get_ai_spend_trend
    return {"status": "ok", "data": get_ai_spend_trend()}
