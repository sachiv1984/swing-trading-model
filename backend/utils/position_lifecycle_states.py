"""
Canonical position_state / lifecycle_state value registry (ST-07, EPIC-02,
v8.3, BLG-BE-67).

Prior to this module, each of `position_lifecycle_service.py`,
`position_service.py`, `portfolio_service.py`, `portfolio_risk.py`, and
`main.py` independently hardcoded the same 5 literal state strings, with no
single source of truth — a drift risk (a typo or a partial rename in one
call site would silently diverge from the rest, and from the frontend).

This is the canonical backend registry. Frontend derivation status: see
`docs/specs/position_lifecycle_states_registry.md` — the frontend's own
per-component state maps (`src/pages/Positions.js`,
`src/components/positions/PositionCard.js`,
`src/components/trades/PlanVsReality.js`) were reconciled against this
registry and found already fully consistent (same 5 values, no drift); see
that doc for the full reconciliation and the reasoning for not refactoring
the frontend's per-view label/colour maps to import this registry (values
and rendering unchanged either way — only the source of truth for the
backend side moves here).
"""
from typing import Final, Tuple

EXIT_ZONE: Final[str] = "EXIT ZONE"
PROFITABLE: Final[str] = "PROFITABLE"
LOSING: Final[str] = "LOSING"
GRACE: Final[str] = "GRACE"
UNKNOWN: Final[str] = "UNKNOWN"

# Priority order matches compute_position_state()'s check order.
POSITION_LIFECYCLE_STATES: Final[Tuple[str, ...]] = (
    EXIT_ZONE, PROFITABLE, LOSING, GRACE, UNKNOWN,
)
