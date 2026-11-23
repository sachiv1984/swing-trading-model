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

# ST-28 (BLG-BE-179, v9.18): the v9.12 currency correction (ST-13, PR #2025)
# made classify_position() compare a US position's native entry with its native
# price. On the first recompute after it reached production, affected US
# positions changed state with no market move. Those transitions are tagged, not
# rewritten: a reader of state_history / position_state_history that measures
# real lifecycle behaviour (days in state, transition counts) excludes them.
# Cut-off: PR #2025's merge to main, 2026-10-13T19:04:30Z (Product Owner, in
# session, 2026-11-23; the production deploy time is not recorded). data_model.md
# §Lifecycle Transition Reasons documents the convention.
BASIS_CORRECTION_CUTOFF_UTC = datetime(2026, 10, 13, 19, 4, 30)
REASON_BASIS_CORRECTION = "basis_correction"
# A transition from or to these states cannot come from the basis change:
# GRACE ignores price (ST-12) and UNKNOWN means missing data.
_NOT_PRICE_STATES = (GRACE, UNKNOWN)


def _naive_utc(value) -> Optional[datetime]:
    """A datetime or ISO string as a naive UTC datetime, or None."""
    if value is None:
        return None
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if not isinstance(value, datetime):
        return None
    if value.tzinfo is not None:
        from datetime import timezone as _tz
        value = value.astimezone(_tz.utc).replace(tzinfo=None)
    return value


def _entered_before_cutoff(position: dict) -> bool:
    try:
        entry = date.fromisoformat(str(position.get("entry_date")).split("T")[0].split(" ")[0])
    except (ValueError, AttributeError):
        return False
    return entry < BASIS_CORRECTION_CUTOFF_UTC.date()


def _first_correction_index(position: dict, transitions: list) -> Optional[int]:
    """Index into `transitions` (each (from_state, to_state, at), oldest first) of
    the basis-correction transition, or None.

    It is the position's first transition at or after the cut-off, for a US
    position entered before it, when neither side is GRACE or UNKNOWN. Only that
    first transition is tagged: later ones are real moves. If the first
    post-cut-off transition involves GRACE or UNKNOWN, none is tagged.
    """
    if position.get("market") != "US" or not _entered_before_cutoff(position):
        return None
    for i, (from_state, to_state, at) in enumerate(transitions):
        when = _naive_utc(at)
        if when is None or when < BASIS_CORRECTION_CUTOFF_UTC:
            continue
        if from_state is None or from_state in _NOT_PRICE_STATES or to_state in _NOT_PRICE_STATES:
            return None
        return i
    return None


def tag_basis_correction_transitions(position: dict) -> list:
    """The position's state_history with the basis-correction entry, if any,
    carrying "reason": "basis_correction" (ST-28, BLG-BE-179). A copy; the
    stored column is not changed. Entry 0 is the seed, not a transition."""
    history = position.get("state_history") or []
    if isinstance(history, str):
        import json
        history = json.loads(history)
    history = [dict(h) for h in history]
    transitions = [
        (history[i - 1].get("state"), history[i].get("state"), history[i].get("entered_at"))
        for i in range(1, len(history))
    ]
    idx = _first_correction_index(position, transitions)
    if idx is not None:
        history[idx + 1]["reason"] = REASON_BASIS_CORRECTION
    return history


def basis_correction_history_row_id(position: dict, rows: list):
    """The id of the position_state_history row that is the basis correction, or
    None. `rows` are that position's rows (id, from_state, to_state, entered_at),
    in any order; a NULL from_state is the first-seen row, not a transition."""
    ordered = sorted(rows, key=lambda r: _naive_utc(r.get("entered_at")) or datetime.min)
    idx = _first_correction_index(
        position, [(r.get("from_state"), r.get("to_state"), r.get("entered_at")) for r in ordered]
    )
    return ordered[idx].get("id") if idx is not None else None


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


def _native_entry(position: dict) -> Optional[float]:
    """The native entry the badge compares with (ST-17, BLG-BE-176, v9.16).

    - native_entry_price, when the caller already resolved it. GET /positions
      passes its API row, whose entry_price is already native and which has no
      fill_price, so re-deriving here multiplied a US entry by fx_rate twice.
    - UK: entry_price.
    - US: fill_price, else entry_price (GBP) x the stored fx_rate, else x the
      live rate: the fallback native_entry_price() (position_service) and
      get_portfolio_summary() use for display_status and stop arithmetic, so
      the badge and display_status agree for a row with neither (BLG-BE-176).
      The live rate is the caller's live_fx_rate if given, else fetched.
    """
    if position.get("native_entry_price") is not None:
        return float(position["native_entry_price"])
    entry_price = position.get("entry_price")
    if position.get("market") != "US":
        return entry_price
    if not position.get("fill_price") and not entry_price:
        return None
    # ST-25 (BLG-BE-208, v9.18): the fallback itself lives in native_entry_price().
    # The live rate is fetched only when the row has neither fill_price nor fx_rate.
    live_fx_rate = position.get("live_fx_rate")
    if not position.get("fill_price") and not position.get("fx_rate") and not live_fx_rate:
        from utils.pricing import get_live_fx_rate
        live_fx_rate = get_live_fx_rate()
    from services.position_service import native_entry_price
    return native_entry_price(position, live_fx_rate)


def classify_position(position: dict) -> Tuple[str, Optional[str]]:
    """Return (state, lifecycle_reason). The reason is non-null only for UNKNOWN."""
    days_held = _count_calendar_days(position.get("entry_date"))
    if days_held is None:
        return UNKNOWN, REASON_MISSING_DATA

    # Grace precedence (ST-12): in grace the badge is GRACE whatever the price.
    if days_held < GRACE_PERIOD_DAYS:
        return GRACE, None

    # ST-13 (BLG-BE-149, v9.12): compare native with native. positions.entry_price
    # is GBP for every market (data_model_positions_dictionary.md v0.4), while
    # current_price and initial_stop are native, so a US row's native entry is
    # fill_price, else entry_price × fx_rate. Comparing the GBP entry with a USD
    # price showed a US position down by up to ~20% in dollars as PROFITABLE.
    entry_price = _native_entry(position)
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
