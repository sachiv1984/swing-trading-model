"""
Position Lifecycle Service (Arc 3 — IT-01)

Deterministic state machine for open positions.

A display overlay that defers to strategy_rules.md §9 (ST-11, BLG-SPEC-185,
v9.10 — Strategy Rules & System Intent Owner ruling, ESC-EXEC-20261006-03).

States (priority order checked in classify_position):
    GRACE      — fewer than 10 calendar days since entry (strategy_rules.md
                 §6.2), regardless of price. Same rule as GET /positions'
                 grace_period flag (ST-12, BLG-FE-196, v9.10).
    EXIT ZONE  — post-grace and price >= entry + 2R (R = entry - initial_stop).
                 A display sub-state of §9 PROFITABLE, never of LOSING.
    PROFITABLE — post-grace, native P&L > 0 (price > entry), §9
    LOSING     — post-grace, native P&L <= 0 (price <= entry), §9
    UNKNOWN    — missing data only. The reason is returned as lifecycle_reason.

The P&L test is the same one that picks the §7.2 stop multiplier
(position_service.py: is_profitable = pnl_native > 0), so the badge and the
stop never disagree on which state a position is in.

§13 compliance: state is display-only. No automated action generated.
Service callable on demand; never mutates state autonomously.
"""

from datetime import datetime, date
from typing import Optional, Tuple

from database import (
    get_portfolio,
    get_positions,
    get_position_by_id,
    update_position_lifecycle_state,
    create_position_state_history_entry,
)
from utils.formatting import decimal_to_float
from utils.position_lifecycle_states import EXIT_ZONE, PROFITABLE, LOSING, GRACE, UNKNOWN

# strategy_rules.md §6.2 / §11: grace is 10 calendar days (days 0-9).
GRACE_PERIOD_DAYS = 10

# lifecycle_reason value, set only when the state is UNKNOWN (ST-12).
# ST-11 (v9.10) removed "flat_after_grace": §9 has no neutral post-grace zone.
REASON_MISSING_DATA = "missing_data"


def _count_calendar_days(entry_date_str: str) -> Optional[int]:
    """Calendar days from entry_date to today (0 on the entry day), or None if unparseable.

    ST-12 (BLG-FE-196, v9.10): replaces a weekday count, which let the badge's
    grace boundary drift from the calendar-day grace_period flag.
    """
    try:
        entry = date.fromisoformat(str(entry_date_str).split("T")[0].split(" ")[0])
    except (ValueError, AttributeError):
        return None
    return max(0, (date.today() - entry).days)


def classify_position(position: dict) -> Tuple[str, Optional[str]]:
    """Return (state, lifecycle_reason). The reason is non-null only for UNKNOWN."""
    days_held = _count_calendar_days(position.get("entry_date"))
    if days_held is None:
        return UNKNOWN, REASON_MISSING_DATA

    # Grace precedence (ST-12): in grace the badge is GRACE whatever the price.
    if days_held < GRACE_PERIOD_DAYS:
        return GRACE, None

    entry_price = position.get("entry_price")
    current_price = (
        position.get("current_price_native")
        or position.get("current_price")
    )
    if not entry_price or not current_price:
        return UNKNOWN, REASON_MISSING_DATA

    entry_price = float(entry_price)
    current_price = float(current_price)

    # §9: post-grace, P&L <= 0 is LOSING, whatever the distance from entry.
    if current_price <= entry_price:
        return LOSING, None

    # EXIT ZONE: a PROFITABLE position at or beyond entry + 2R (needs initial_stop).
    initial_stop = position.get("initial_stop")
    if initial_stop:
        r_value = entry_price - float(initial_stop)
        if r_value > 0 and current_price >= entry_price + 2 * r_value:
            return EXIT_ZONE, None

    return PROFITABLE, None


def compute_position_state(position: dict) -> str:
    """Determine lifecycle state from position data.

    Args:
        position: dict with at minimum entry_price, current_price (native)
                  and entry_date, and optionally initial_stop. ATR is not
                  used (ST-11, v9.10).

    Returns:
        One of: 'EXIT ZONE', 'PROFITABLE', 'LOSING', 'GRACE', 'UNKNOWN'
    """
    return classify_position(position)[0]


def compute_lifecycle_reason(position: dict) -> Optional[str]:
    """Why a position is UNKNOWN ('missing_data'), else None."""
    return classify_position(position)[1]


def compute_days_in_state(state_entered_at) -> int:
    """Days since the current state was entered."""
    if not state_entered_at:
        return 0
    if isinstance(state_entered_at, str):
        try:
            state_entered_at = datetime.fromisoformat(state_entered_at.replace("Z", "+00:00"))
        except ValueError:
            return 0
    try:
        delta = datetime.utcnow() - state_entered_at.replace(tzinfo=None)
        return max(0, delta.days)
    except Exception:
        return 0


def _build_lifecycle_fields(position: dict) -> dict:
    """Compute lifecycle state fields for a position dict (no DB write)."""
    new_state, lifecycle_reason = classify_position(position)
    stored_state = position.get("position_state")
    state_entered_at = position.get("state_entered_at")

    if stored_state != new_state:
        state_entered_at = datetime.utcnow()
    elif not state_entered_at:
        state_entered_at = datetime.utcnow()

    days_in_state = compute_days_in_state(state_entered_at)
    return {
        "position_state": new_state,
        "state_entered_at": state_entered_at.isoformat() if hasattr(state_entered_at, "isoformat") else str(state_entered_at),
        "days_in_state": days_in_state,
        "lifecycle_reason": lifecycle_reason,
    }


def refresh_position_lifecycle(position_id: str, prefetched_position: Optional[dict] = None) -> Optional[dict]:
    """Compute and persist lifecycle state for one position.

    Returns the raw DB row after update, or None if position not found.
    State history is appended when state transitions occur.

    ST-11 (BLG-BE-90, EPIC-04, v8.7 — N+1 query audit): `prefetched_position`
    lets a caller that has already fetched the full position row (any
    `SELECT *`-shaped dict carrying `position_state`/`state_history`/
    `state_entered_at`, e.g. via `get_position_by_id()` or
    `get_positions()`) pass it straight through, skipping the redundant
    re-fetch this function otherwise always performed. Every current caller
    of this function already has such a row in hand by the time it calls
    in (see `get_lifecycle_fields_for_position()` below and its own
    callers) — this was a clearly-attributable N+1/duplicate-query case,
    not a broader refactor. If omitted, behaviour is unchanged: fetches the
    row itself.
    """
    if prefetched_position is not None:
        raw = prefetched_position
    else:
        raw = get_position_by_id(position_id)
        if not raw:
            return None
    pos = decimal_to_float(dict(raw))

    new_state = compute_position_state(pos)
    stored_state = pos.get("position_state")

    now = datetime.utcnow()

    if stored_state != new_state:
        existing_history = pos.get("state_history") or []
        if isinstance(existing_history, str):
            import json
            existing_history = json.loads(existing_history)
        new_entry = {"state": new_state, "entered_at": now.isoformat()}
        updated_history = existing_history + [new_entry]
        # ST-08 (BLG-BE-58, EPIC-02, v8.8): also log the transition to the
        # normalized position_state_history table, alongside (not instead
        # of) the JSONB column above — additive, fail-open, no change to
        # the state machine or the existing persistence path.
        #
        # ST-10 (BLG-BE-100, EPIC-03, v8.9): primary write runs *first*, the
        # audit-log write only after it succeeds — the two writes use
        # separate get_db() connections/transactions (no cross-connection
        # atomicity available without a broader refactor), so ordering is
        # what prevents a phantom position_state_history row for a
        # transition that never actually landed on `positions` (the
        # previous audit-before-primary order meant a primary-write failure
        # right after a successful audit insert would leave exactly that:
        # a state_history row of record for a transition that didn't
        # happen). Matches the already-safe primary-then-audit ordering
        # used by every position_audit_log call site
        # (services/position_service.py — update_note/mark_reviewed/
        # update_tags all call create_position_audit_log_entry() after
        # their own primary write, not before).
        result = update_position_lifecycle_state(position_id, new_state, now, updated_history)
        create_position_state_history_entry(position_id, stored_state, new_state, now)
        return result
    else:
        # State unchanged — ensure state_entered_at is set if missing
        if not pos.get("state_entered_at"):
            existing_history = pos.get("state_history") or []
            if isinstance(existing_history, str):
                import json
                existing_history = json.loads(existing_history)
            if not existing_history:
                existing_history = [{"state": new_state, "entered_at": now.isoformat()}]
            return update_position_lifecycle_state(position_id, new_state, now, existing_history)
        return raw


def get_lifecycle_fields_for_position(position: dict) -> dict:
    """Return lifecycle fields for inclusion in API response dict.

    Calls DB update if state has changed (lazy recalculation).
    Falls back to in-memory computation if the DB columns don't exist yet
    (migration not yet applied — graceful degradation).
    """
    position_id = str(position.get("id") or "")
    if not position_id:
        return {"position_state": UNKNOWN, "state_entered_at": None, "days_in_state": 0,
                "lifecycle_reason": REASON_MISSING_DATA}

    try:
        updated = refresh_position_lifecycle(position_id, prefetched_position=position)
        if updated:
            updated = decimal_to_float(dict(updated))
            state_entered_at = updated.get("state_entered_at")
            return {
                "position_state": updated.get("position_state", UNKNOWN),
                "state_entered_at": state_entered_at.isoformat() if hasattr(state_entered_at, "isoformat") else str(state_entered_at) if state_entered_at else None,
                "days_in_state": compute_days_in_state(state_entered_at),
                # ST-12 (BLG-FE-196, v9.10): why an UNKNOWN badge is UNKNOWN.
                # Derived from the same inputs as the state just persisted.
                "lifecycle_reason": compute_lifecycle_reason(position),
            }
    except Exception:
        pass

    return _build_lifecycle_fields(position)
