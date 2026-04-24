"""
AI Router

POST /ai/journal-summary — Summarise trade journal notes via external LLM API.

AI output is display-only and must NOT feed into any signal, scoring,
or recommendation pipeline. SRB-v1.7 CONDITIONALLY COMPLIANT.

Contract: docs/specs/api_contracts/ai_endpoints.md v1.0
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from database import get_db
from services.ai_service import summarise_journal_notes
from services.ai_audit_service import log_ai_summary_run, query_audit_log

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
def journal_summary(body: JournalSummaryRequest):
    """
    Summarise entry/exit journal notes from closed trades.
    Accepts trade_ids or date_from/date_to range.
    Returns LLM-generated plain-text summary.
    AI output is display-only — not used in any calculation.
    """
    if not body.trade_ids and not body.date_from and not body.date_to:
        raise HTTPException(
            status_code=422,
            detail="Provide trade_ids or at least one of date_from / date_to.",
        )

    with get_db() as conn:
        cursor = conn.cursor()

        if body.trade_ids:
            cursor.execute(
                """
                SELECT entry_note, exit_note
                FROM trade_history
                WHERE id = ANY(%s) AND exit_date IS NOT NULL
                """,
                (body.trade_ids,),
            )
        else:
            params: list = []
            filters = ["exit_date IS NOT NULL"]
            if body.date_from:
                filters.append("exit_date >= %s")
                params.append(body.date_from)
            if body.date_to:
                filters.append("exit_date <= %s")
                params.append(body.date_to)
            where = " AND ".join(filters)
            cursor.execute(
                f"SELECT entry_note, exit_note FROM trade_history WHERE {where}",
                params,
            )

        rows = cursor.fetchall()

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
