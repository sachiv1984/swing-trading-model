"""
Red Flag Journal router (SI-03 / ST-07, EPIC-03, v3.9)

§13 compliance: display-only audit log; no automated decisions.
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from database import ensure_red_flag_events_table, ensure_red_flag_events_severity_column, get_red_flag_events

router = APIRouter(tags=["Portfolio"])


def _serialize_event(event: dict) -> dict:
    out = dict(event)
    for k, v in out.items():
        if hasattr(v, "isoformat"):
            out[k] = v.isoformat()
    if out.get("id") is not None:
        out["id"] = str(out["id"])
    if out.get("position_id") is not None:
        out["position_id"] = str(out["position_id"])
    return out


@router.get("/portfolio/red-flag-journal")
def get_red_flag_journal(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    event_type: Optional[str] = Query(default=None),
    ticker: Optional[str] = Query(default=None),
    since: Optional[str] = Query(default=None),
    severity: Optional[str] = Query(default=None, description="Filter by severity: info | warning | critical"),
):
    """GET /portfolio/red-flag-journal — paginated deviation event log.

    §13: display-only audit log; no automated decisions.
    ST-09 (v4.6): severity filter added (info / warning / critical).
    """
    try:
        ensure_red_flag_events_table()
        ensure_red_flag_events_severity_column()
        result = get_red_flag_events(
            page=page,
            page_size=page_size,
            event_type=event_type,
            ticker=ticker,
            since=since,
            severity=severity,
        )
        result["items"] = [_serialize_event(e) for e in result["items"]]
        return {"status": "ok", "data": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
