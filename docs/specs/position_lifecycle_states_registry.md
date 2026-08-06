**Owner:** Data Model & Domain Schema Owner
**Class:** Spec (Class 5)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-06
**Cycle:** 2026-08-05__release-v8.3 (ST-07 — BLG-BE-67)

---

# Canonical Position Lifecycle State Registry

## Purpose

`BLG-BE-67` requires a canonical registry for `position_state` values shared frontend/backend, with either (a) both sides deriving from it, or (b) a documented reconciliation showing they were already consistent. This document records both: the canonical backend registry, and the frontend reconciliation.

## Canonical Values

Five states, defined by `backend/services/position_lifecycle_service.py::compute_position_state()` (Arc 3 / IT-01 lifecycle state machine):

| Value | Meaning |
|---|---|
| `EXIT ZONE` | Price >= entry + 2R (R = entry − initial_stop) |
| `PROFITABLE` | Price > entry + 0.5 × ATR |
| `LOSING` | Price < entry − 0.5 × ATR |
| `GRACE` | Trading days since entry <= 10 AND price within ±0.5 ATR |
| `UNKNOWN` | Missing ATR or ambiguous zone after grace period |

## Backend Registry

`backend/utils/position_lifecycle_states.py` is the canonical source of truth — named constants (`EXIT_ZONE`, `PROFITABLE`, `LOSING`, `GRACE`, `UNKNOWN`) plus the `POSITION_LIFECYCLE_STATES` tuple.

Prior to this story, the same 5 literal strings were hardcoded independently in 5 backend locations, each a drift risk (a typo or partial rename in any one site would silently diverge from the rest and from the frontend):

| File | Prior usage |
|---|---|
| `services/position_lifecycle_service.py` | Canonical state-machine implementation (`compute_position_state`) |
| `services/position_service.py` | `display_status` field (separate, simpler pnl/holding-days-based classification — same vocabulary) |
| `services/portfolio_service.py` | `display_status` field (same pattern as `position_service.py`) |
| `routers/portfolio_risk.py` | `_get_lifecycle_state_counts()` — count-by-state aggregation, including the raw SQL `GROUP BY position_state` fallback default |
| `main.py` | `GET` alerts endpoint — raw SQL `WHERE p.position_state = 'GRACE'` filter (now parametrised: `%s` placeholder bound to the `GRACE` constant, replacing the inline SQL literal) |

All 5 sites now import from `utils.position_lifecycle_states` instead of hardcoding the literal strings. `tests/test_position_lifecycle_states_registry.py` additionally cross-checks that `compute_position_state()` never returns a value outside the registry, across every branch of its logic.

## Frontend Reconciliation

The frontend was **not** refactored to import a shared JS constants module in this story — this section is the documented reconciliation instead, per the acceptance criteria's explicit "or" clause. Rationale: the frontend's per-view state maps also carry rendering metadata (label text, Tailwind colour class, tooltip copy) tightly coupled to each component's own presentation, not just the bare state key; refactoring three UI files (two of them shared, high-traffic components) purely to relocate an already-correct string literal carries UI regression risk for zero behavioural or correctness benefit, well outside this story's S (0.5 day) scope and design-gate disposition ("Design Not Applicable — shared-constant/reconciliation refactor; values and rendering unchanged, only the source of truth moves").

Frontend locations inspected (`grep` for each of the 5 state values across `src/`):

| File | Values found |
|---|---|
| `src/pages/Positions.js` | `GRACE`, `LOSING`, `PROFITABLE`, `"EXIT ZONE"`, `UNKNOWN` (all 5, in the `STATE_CONFIG`-equivalent label/colour/tooltip map and in direct equality checks) |
| `src/components/positions/PositionCard.js` | `GRACE` (equality check, grace-suppression logic) |
| `src/components/trades/PlanVsReality.js` | `GRACE`, `LOSING`, `PROFITABLE`, `"EXIT ZONE"`, `UNKNOWN` (all 5, in its own label/colour map) |

**Result: fully consistent.** All 5 values found in the frontend match the backend registry exactly — same 5 strings, same spelling (including the `"EXIT ZONE"` space, not `EXIT_ZONE` or `exit_zone`), no drift found in either direction. No correction was required.

## Maintenance Note

If a 6th state or a rename is ever introduced, update `backend/utils/position_lifecycle_states.py` first, then this document's Frontend Reconciliation table in the same change (re-run the `grep` sweep above) — do not let the two drift out of sync silently, which is the exact failure mode this registry exists to prevent.
