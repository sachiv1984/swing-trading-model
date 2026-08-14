**Owner:** Head of UX & Design
**Status:** Approved (Product Owner confirmed)
**Cycle:** 2026-08-14__release-v8.8
**Story:** ST-16 (EPIC-03, BLG-FE-159)

# Decision Record — `PositionEntryModal.js` Dead-Code Resolution

## 1. Problem

`BLG-FE-159` (filed 2026-08-12, v8.7 ST-06) found `src/components/signals/PositionEntryModal.js` has no reachable mount point anywhere in the app — the only other reference to its name in `src/` is a code comment in `Layout.js`. It was theme-token-converted alongside 3 real modals (`BLG-FE-156`) via code review only, since there is no way to navigate to it and no Playwright coverage was possible.

**Repo-check confirmed at this gate (2026-08-14):** still zero live imports/mounts. No other story in this cycle's scope introduces one.

## 2. Decision

**Remove `PositionEntryModal.js` from the codebase (Option B of `BLG-FE-159`'s two named options).**

Rationale:
- No product requirement for a signals-to-position-entry modal flow has surfaced since it was left orphaned; reviving it would mean designing a new trigger and interaction flow from scratch (out of proportion to this item's XS effort budget) rather than resolving existing dead code.
- Rebuilding a real, user-navigable trigger for it is a distinct product decision (a new entry point into position creation from the Signals surface) that has not been requested and would need its own scoping, not a byproduct of a dead-code cleanup item.
- Removal directly satisfies both ACs: no reachable/unreachable ambiguity remains, and the explicit decision is recorded here.

## 3. Scope

- Delete `src/components/signals/PositionEntryModal.js`.
- Remove the stale comment reference in `src/Layout.js` (currently lists it as an example of a Dialog-based consumer affected by the historical dark-class-sync bug — the fixed bug's own note in `navigation.md` §Group Structure already names it only as a historical example, not a live dependency; safe to drop from the comment).
- No frontend spec references this component (no page in `docs/specs/frontend/pages/` ever documented it), so no spec-file update is required beyond removing it from `design_system.md`'s Modal / Dialog Theming "known non-compliant instances" list (it is being deleted, not converted — no longer applicable there either way).

## 4. Constraints Checked

- Frontend-visible-change / Playwright rule (`CLAUDE.md` §2): removal of an unreachable component has no observable AC to cover — nothing renders, so nothing regresses. Not subject to the Playwright-or-staging-sign-off requirement.
