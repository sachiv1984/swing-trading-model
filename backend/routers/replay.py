"""
Replay Router — ST-01b (EPIC-01, v9.7, BLG-FEAT-74, PO-05 Lightweight Replay Mode)

Contract: docs/specs/api_contracts/replay_endpoints.md
Wire contract locked in: docs/product/decisions/po05_replay_scope_confirmation.md (rev 3)

Manual body parsing/validation (D2) rather than a pydantic model with `extra="forbid"`:
the backend has no `RequestValidationError` handler, so FastAPI's default response for
a missing/malformed/non-object body is `422 {"detail": [...]}`, which is neither this
repository's canonical envelope (`conventions.md` §13.3) nor the 400 status this
contract deliberately uses for validation (§13.2's canonical mapping) instead of the
422 precedent a few other routers use. Parsing and validating by hand here is what
lets every rejection return the same `{"status": "error", "message": ..., "code": ...}`
shape regardless of what was wrong with the request -- confirmed against a live
TestClient probe during the scope note's independent review (see that document §9,
Pass 2 / P2-1) that `Body(...)` alone cannot do this.
"""
import json
import uuid
from datetime import date, datetime, timezone
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse

from services.replay_service import (
    ReplayPriceDataUnavailableError,
    ReplayScopeTooLargeError,
    run_replay,
)

router = APIRouter(prefix="/replay", tags=["Replay"])

_ALLOWED_TRADE_SET_FIELDS = {"trade_ids"}
_ALLOWED_DATE_RANGE_FIELDS = {"date_from", "date_to"}


def _error(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"status": "error", "message": message, "code": code})


def _validate_body(body) -> tuple:
    """Returns (mode, date_from, date_to, trade_ids) on success, or a JSONResponse
    error to return immediately on failure. D2's full validation surface."""
    if not isinstance(body, dict):
        return _error(400, "validation_error", "Request body must be a JSON object.")

    has_trade_ids = "trade_ids" in body
    has_date_range = "date_from" in body or "date_to" in body

    if has_trade_ids and has_date_range:
        return _error(400, "validation_error", "Provide either trade_ids or a date range, not both.")
    if not has_trade_ids and not has_date_range:
        return _error(400, "validation_error", "Provide either trade_ids or both date_from and date_to.")

    if has_trade_ids:
        extra = set(body.keys()) - _ALLOWED_TRADE_SET_FIELDS
        if extra:
            return _error(400, "validation_error", f"Unrecognised field(s): {sorted(extra)}.")
        trade_ids = body["trade_ids"]
        if not isinstance(trade_ids, list) or len(trade_ids) == 0:
            return _error(400, "validation_error", "trade_ids must be a non-empty array of UUID strings.")
        for tid in trade_ids:
            if not isinstance(tid, str):
                return _error(400, "validation_error", "trade_ids must be an array of UUID strings.")
            try:
                uuid.UUID(tid)
            except ValueError:
                return _error(400, "validation_error", f"'{tid}' is not a valid UUID.")
        return ("trade_set", None, None, trade_ids)

    extra = set(body.keys()) - _ALLOWED_DATE_RANGE_FIELDS
    if extra:
        return _error(400, "validation_error", f"Unrecognised field(s): {sorted(extra)}.")
    if "date_from" not in body or "date_to" not in body:
        return _error(400, "validation_error", "A date range request requires both date_from and date_to.")

    parsed = {}
    for field_name in ("date_from", "date_to"):
        raw = body[field_name]
        if not isinstance(raw, str):
            return _error(400, "validation_error", f"{field_name} must be an ISO date string (YYYY-MM-DD).")
        try:
            parsed[field_name] = date.fromisoformat(raw)
        except ValueError:
            return _error(400, "validation_error", f"{field_name} must be an ISO date string (YYYY-MM-DD).")

    if parsed["date_from"] > parsed["date_to"]:
        return _error(400, "validation_error", "date_from must not be after date_to.")
    if parsed["date_to"] > datetime.now(timezone.utc).date():
        return _error(400, "validation_error", "date_to must not be in the future.")

    return ("date_range", parsed["date_from"], parsed["date_to"], None)


@router.post("/run")
async def replay_run(request: Request):
    """
    Replay each of the user's own closed trades (a date range, or an explicit list of
    trade ids) independently through the current strategy engine's exit rules.
    Read-only: reads trade_history only, writes nothing, makes no Alpaca call.

    Returns HTTP 200 with the replay result (0 trades replayed is a normal success).
    Returns HTTP 400 for a request validation problem or an over-large scope.
    Returns HTTP 500 if the price provider has no usable data, or on an unexpected error.
    """
    raw_body = await request.body()
    if not raw_body:
        return _error(400, "validation_error", "Request body must be a JSON object.")
    try:
        body = json.loads(raw_body)
    except ValueError:
        return _error(400, "validation_error", "Request body must be valid JSON.")

    validated = _validate_body(body)
    if isinstance(validated, JSONResponse):
        return validated
    mode, date_from, date_to, trade_ids = validated

    try:
        data = await run_in_threadpool(run_replay, mode=mode, date_from=date_from, date_to=date_to, trade_ids=trade_ids)
        return {"status": "ok", "data": data}
    except ReplayScopeTooLargeError as e:
        return _error(400, "replay_scope_too_large", str(e))
    except ReplayPriceDataUnavailableError as e:
        return _error(500, "price_data_unavailable", str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return _error(500, "replay_failed", f"Replay run failed: {e}")
