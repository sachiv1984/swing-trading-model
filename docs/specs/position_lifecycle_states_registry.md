**Owner:** Data Model & Domain Schema Owner
**Class:** Spec (Class 5)
**Status:** Active
**Version:** 1.2
**Last Updated:** 2026-10-07 (ST-11, EPIC-03, v9.10, BLG-SPEC-185 — the badge is a display overlay that defers to strategy_rules.md §9; post-grace LOSING/PROFITABLE follow §9's P&L sign, ±0.5 ATR bands and flat_after_grace removed); prior — 2026-10-06 (ST-12, EPIC-03, v9.10, BLG-FE-196 — GRACE row now calendar days with grace precedence, matching the code; UNKNOWN reason); prior — 2026-08-06
**Cycle:** 2026-08-05__release-v8.3 (ST-07 — BLG-BE-67)

---

# Canonical Position Lifecycle State Registry

## Purpose

`BLG-BE-67` requires a canonical registry for `position_state` values shared frontend/backend, with either (a) both sides deriving from it, or (b) a documented reconciliation showing they were already consistent. This document records both: the canonical backend registry, and the frontend reconciliation.

## Canonical Values

Five values, defined by `backend/services/position_lifecycle_service.py::classify_position()` (Arc 3 / IT-01 lifecycle badge):

| Value | Meaning | §9 state it displays |
|---|---|---|
| `GRACE` | Fewer than 10 calendar days since entry (`strategy_rules.md` §6.2), whatever the price. Checked first. | GRACE |
| `LOSING` | Past grace, native current price at or below entry (P&L ≤ 0) | LOSING |
| `PROFITABLE` | Past grace, native current price above entry (P&L > 0), and below entry + 2R | PROFITABLE |
| `EXIT ZONE` | Past grace, price ≥ entry + 2R (R = entry − initial_stop). Only reachable from a profitable position. | PROFITABLE (display sub-state) |
| `UNKNOWN` | Entry price, current price or entry date missing. `lifecycle_reason` is `missing_data`. | none: a data fallback, not a state |

`strategy_rules.md` §9's EXITED is not a badge value: the badge is shown only for open positions.

## Relationship to strategy_rules.md §9

**Ruling (ST-11, `BLG-SPEC-185`, 2026-10-07):** the lifecycle badge is a **display overlay that defers to §9**. It is not a second state machine, and §9 is not amended.

- After grace, LOSING and PROFITABLE are decided by §9's P&L sign alone. The test is the one that picks the §7.2 stop multiplier (`position_service.py`: `is_profitable = pnl_native > 0`), so the badge and the stop always agree on which state a position is in. The earlier ±0.5 ATR bands, and the post-grace `UNKNOWN` neutral zone (`flat_after_grace`) they created, are removed.
- `EXIT ZONE` is a refinement of PROFITABLE, shown when the 2R target is reached. It changes nothing in §7 or §8 and never applies to a losing position. §9's "exactly one state" holds: an EXIT ZONE position is in the PROFITABLE state.
- `UNKNOWN` is a missing-data fallback, not a §9 state.
- If §9 changes, this table changes with it. The overlay may add display sub-states of a §9 state; it may not split, merge or redefine §9 states without a §9 amendment under §16.

Ruled by the Strategy Rules & System Intent Owner (agent-mediated, `execution_prompt.md` §5.3, on the user's explicit direction): `claude/cycles/2026-10-06__release-v9.10/execution_escalations.md` `ESC-EXEC-20261006-03`.

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
