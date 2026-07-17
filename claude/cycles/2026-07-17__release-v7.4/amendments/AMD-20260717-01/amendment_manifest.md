**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Sealed
**Last Updated:** 2026-07-17
**Amendment ID:** AMD-20260717-01
**Original Cycle:** 2026-07-17__release-v7.4
**Release:** v7.4
**Amendment Reason:** hard-blocker
**Raised by:** PMO Lead
**Raised at:** 2026-07-17T13:15:00Z
**Required ratifying authorities:** Product Owner + Head of Specs Team
**Ratification status:** Ratified

---

## Emergency Evidence

- **Blocked item reference:** ST-02 (`BLG-FE-115`, EPIC-02), ST-03 (`BLG-FE-116`, EPIC-03), ST-04 (`BLG-FE-117`, EPIC-04), ST-05 (`BLG-FE-118`, EPIC-05).
- **Blocker description:** `run design-gate --cycle 2026-07-17__release-v7.4` (2026-07-17, record: `claude/cycles/2026-07-17__release-v7.4/design_gate.md`) classified all four as Design Required and found no approved design artefact for any of them. For ST-02/04/05, artefact production was scheduled inside EPIC-01/ST-01's own acceptance criteria — but ST-01 is sprint-execution work, sequenced *after* Sprint Planning seals, and Design Gate must clear *before* Sprint Planning (`sprint_planning_prompt.md` §2 Lifecycle Guard: valid from-state `Design_Gate_Passed`). Those artefacts structurally cannot exist at the point this gate evaluates them. ST-03 (price alerts) has no design-artefact production scheduled anywhere in the v7.4 plan at all. Per `design_gate_prompt.md` STEP 3's hard rule ("No Design Required item may proceed to Sprint Planning until its frontend spec is updated and confirmed compliant"), all four are confirmed undeliverable within this Sprint Planning pass as currently scoped.
- **Discovery date:** 2026-07-17 (via `run design-gate`).
- **Head of Specs Team assessment:** Confirmed — this is not a spec-authoring gap that can be closed by editing an existing document; it requires net-new Head of UX & Design artefacts for four distinct UI surfaces (one, price alerts, with zero prior design input) plus corresponding `docs/specs/frontend/pages/` updates, none of which exist and none of which can be produced inside this Sprint Planning pass. The blocker cannot be resolved within the current planning cycle. No replacement item is proposed — this is a pure removal, reducing v7.4's Sprint Planning scope to the one item (EPIC-01/ST-01) already cleared as Design Pre-Approved. EPIC-02/03/04/05 remain valid backlog scope for a future release once their design artefacts are produced; this amendment does not cancel them, only removes them from this sprint's pass.

---

## Proposed Changes

### Change 1

Type: Remove
Item: ST-02 — Wire global Cmd/Ctrl-K command palette (`BLG-FE-115`, EPIC-02)
EPIC: EPIC-02
Reason: Design Gate BLOCKED (2026-07-17) — no approved design-review artefact; review scheduled as EPIC-01/ST-01 sprint-execution work, which cannot pre-satisfy a gate that must clear before Sprint Planning.
Effort delta: -1 to -2 capacity units (M)
Dependency impact: none — EPIC-02 has no other item depending on it; EPIC-01/ST-01 does not depend on EPIC-02 being implemented (the dependency runs the other way).

### Change 2

Type: Remove
Item: ST-03 — Add user-created price-alert data model, UI, and delivery integration (`BLG-FE-116`, EPIC-03)
EPIC: EPIC-03
Reason: Design Gate BLOCKED (2026-07-17) — no design artefact exists or is scheduled anywhere in the v7.4 plan for the price-alert UI.
Effort delta: -3 to -5 capacity units (L)
Dependency impact: none.

### Change 3

Type: Remove
Item: ST-04 — Add multi-select and bulk-action toolbar to Watchlist/TradePlans (`BLG-FE-117`, EPIC-04)
EPIC: EPIC-04
Reason: Design Gate BLOCKED (2026-07-17) — no UX spec for the confirmation/undo-window modal; scheduled as EPIC-01/ST-01 sprint-execution work.
Effort delta: -1 to -2 capacity units (M)
Dependency impact: none.

### Change 4

Type: Remove
Item: ST-05 — Add named saved filter presets and a calendar view (`BLG-FE-118`, EPIC-05)
EPIC: EPIC-05
Reason: Design Gate BLOCKED (2026-07-17) — no UX spec for the saved-filters empty state (scheduled in-sprint) and no design review scheduled at all for the calendar view.
Effort delta: -3 to -5 capacity units (L)
Dependency impact: none.

**Net effort delta:** -8 to -14 capacity units (removal only, no addition) — well within the confirmed capacity ceiling; no over-allocation flag needed (§2.1 — proceeds automatically, delta ≤ 0).

**Remaining scope after amendment:** EPIC-01/ST-01 (`BLG-SPEC-95`) only — Design Pre-Approved, already cleared at the 2026-07-17 design gate run.
