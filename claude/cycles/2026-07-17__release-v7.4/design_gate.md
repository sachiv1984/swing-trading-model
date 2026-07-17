**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-17
**Cycle:** 2026-07-17__release-v7.4

# Design Gate Record — 2026-07-17__release-v7.4

## Gate Status: BLOCKED

Completed: 2026-07-17
PMO Lead: confirmed
Head of UX & Design: confirmed (classification only — see Blocked Items)
Product Owner: confirmed (classification only — sprint planning may not proceed until blockers clear)

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 (BLG-SPEC-95) | v7.4 readiness pass (dependencies, UX specs, design review, QA/analytics coverage) | Design Pre-Approved | Documentation/spec-and-process pass only — dependency preflight, CI tagging scheme, Playwright baseline scope, analytics event schema. It produces no shippable UI of its own. Consistent with the identical classification given to the equivalent v7.3 readiness-pass stories (`BLG-SPEC-91/92/93/94`, see `2026-07-16__release-v7.3/design_gate.md`). | N/A | N/A — no page spec touched; the produced readiness document is this story's own execution deliverable | ✅ Cleared | Head of UX & Design |
| ST-02 (BLG-FE-115) | Global Cmd/Ctrl-K command palette | Design Required | New global UI component (modal, keyboard-navigation flow, cross-page search) — squarely a "new component / changed interaction flow" per §6. `docs/specs/blg_fe_115_pre_implementation_readiness_pass.md` documents the keyboard-interaction contract and index scope in engineering-spec form, but ST-01's own acceptance criteria ("Design review pass completed for command-palette keyboard-navigation affordance") confirm the review itself has **not yet been performed** — it is scheduled as in-sprint execution work, not a pre-existing approved artefact. | PENDING — no artefact filed at `docs/design/2026-07-17__release-v7.4/`; review scheduled inside EPIC-01/ST-01 sprint execution | Not updated (no `docs/specs/frontend/pages/*.md` touches the command palette) | ❌ Blocked | — |
| ST-03 (BLG-FE-116) | User-created price alerts (data model, UI, delivery) | Design Required | New UI surface (create/view/edit/delete alert flows) — clear "new component" per §6. `docs/specs/blg_fe_116_pre_implementation_readiness_pass.md` covers schema, API, §13, and testing, but contains **no UI/interaction design** at all. Unlike EPIC-02/04/05, this item is **not referenced anywhere in ST-01's acceptance criteria** — no design-artefact production is scheduled for it in this release at all. | MISSING — no artefact exists and none is planned in this cycle's scope | Not updated | ❌ Blocked | — |
| ST-04 (BLG-FE-117) | Multi-select + bulk-action toolbar (Watchlist/TradePlans) | Design Required | New interaction flow (row multi-select, toolbar, confirm/undo-window modal) — clear "changed interaction flow" per §6. `docs/specs/blg_fe_117_pre_implementation_readiness_pass.md §6` explicitly flags the zero-selected/toolbar-consistency question "for UX confirmation rather than fixed here." ST-01's AC ("UX spec written for... bulk-actions confirmation/undo-window modal") confirms this spec has **not yet been written** — scheduled as in-sprint execution work. | PENDING — no artefact filed; UX spec scheduled inside EPIC-01/ST-01 sprint execution | Not updated | ❌ Blocked | — |
| ST-05 (BLG-FE-118) | Saved filter presets + calendar view | Design Required | New UI (named saved-filter presets, month-grid calendar view) — clear "new page / new data displayed" per §6. `docs/specs/blg_fe_118_pre_implementation_readiness_pass.md` covers schema, date sourcing, and feasibility, but ST-01's AC only schedules a UX spec for the **saved-filters empty state** — the calendar view itself (a new page-level surface) has no design-review or UX-spec step scheduled anywhere in this cycle. | PENDING — empty-state spec scheduled inside EPIC-01/ST-01; calendar-view UX review not scheduled at all | Not updated | ❌ Blocked | — |

## Blocked Items (if any)

| Item ID | Blocker | Owner | Required by |
|---------|---------|-------|-------------|
| ST-02 (BLG-FE-115) | No approved design-review artefact for the command-palette keyboard-navigation affordance; the review is scheduled as EPIC-01/ST-01 sprint-execution work, which cannot exist before Sprint Planning runs | Head of UX & Design | Before `plan sprint` |
| ST-03 (BLG-FE-116) | No design artefact exists or is scheduled anywhere in the v7.4 plan for the price-alert create/view/edit/delete UI | Head of UX & Design | Before `plan sprint` |
| ST-04 (BLG-FE-117) | No UX spec for the bulk-actions confirmation/undo-window modal; scheduled as EPIC-01/ST-01 sprint-execution work | Head of UX & Design | Before `plan sprint` |
| ST-05 (BLG-FE-118) | No UX spec for the saved-filters empty state (scheduled in-sprint) and no design review scheduled at all for the calendar view itself | Head of UX & Design / Frontend Specs & UX Documentation Owner | Before `plan sprint` |

## Required Decision Resolved This Run: §13 Pre-Check (RISK-05 / BLG-GOV-250)

Per `cycle_summary.md`'s Pre-sprint Planning Required Decisions checklist, this run confirms §13 (System Boundaries, `claude/strategy/strategy_rules.md §13`) applicability for `BLG-FE-115` and `BLG-FE-118` — the two v7.4 items that, unlike `BLG-FE-116`/`BLG-FE-117`, had no recorded §13 pre-check from their v7.3 readiness passes.

- **`BLG-FE-115` (command palette): PASS.** The feature is a pure client-side navigation/search surface (per `blg_fe_115_pre_implementation_readiness_pass.md §2`/§6) — it only navigates the user between pages/entities already visible to them via `react-router-dom`. It introduces no automated decision-making, no order placement, no position mutation, and no scheduled/triggered execution of any kind. It is more conservative than the already-cleared `BLG-FE-116`/`BLG-FE-117` precedents (§13.1/§13.2 — "human-in-the-loop by design"; "not an automated trading bot"). No follow-up required; no decision escalation needed.
- **`BLG-FE-118` (saved filters + calendar view): PASS.** Saved filter presets are server-persisted named query criteria with no execution semantics. The calendar view is a read-only display of already-computed realised P&L (per `blg_fe_118_pre_implementation_readiness_pass.md §2`/§3), re-grouping the same `trade_history.exit_date` data already surfaced by the shipped `GET /reports/monthly-pnl` at day granularity — no new computation, no automated decision-making, no order placement or position mutation. Consistent with the same already-cleared reporting precedent. No follow-up required; no decision escalation needed.

This resolves RISK-05/`BLG-GOV-250` independently of the classification blockers above — §13 applicability is now confirmed for both items and does not need to be re-litigated at their eventual implementation sprint planning. It does **not** clear the separate UX-artefact blockers recorded above, which are a distinct gate requirement (§6 Design Requirement Classification, not §13 System Boundaries).

## Notes

- **Structural sequencing conflict identified.** The v7.4 release plan sequences EPIC-01/ST-01 (the readiness-pass story) as Sprint 1's first-completed item specifically to produce the design review / UX specs that EPIC-02/04/05 need (`cycle_summary.md` "Key Decisions" and RISK-01/RISK-02). However, Design Gate runs *before* Sprint Planning (`OPERATIONAL_GUIDE.md` §4.1, `Release_Planning_Complete` → `Design_Gate_Passed`), and Sprint Planning itself requires `design_gate_status == Passed` before it may seal (`sprint_planning_pre_condition`). This means the artefacts ST-01 is scheduled to produce **cannot exist yet** at the point this gate must evaluate them — they are sprint-execution deliverables, not pre-sprint-planning deliverables. Running this gate today, faithfully, therefore finds 4 of 5 items without approved artefacts.
- **EPIC-03 (`BLG-FE-116`, price alerts) has no design coverage planned anywhere in this cycle** — it is not referenced in ST-01's acceptance criteria at all, unlike EPIC-02/04/05 which at least have artefact production scheduled in-sprint. This is the most exposed of the four blocked items.
- **No new design artefacts were produced this run** (STEP 2/3 not invoked). Producing wireframes/interaction specs for 4 net-new UI surfaces — including price alerts, which has zero prior design input — is substantive Head of UX & Design work product that this run is not positioned to fabricate unilaterally; it is left for the Product Owner/PMO Lead to direct (e.g., via an amendment pulling the design-artefact ACs out of ST-01 into a standalone pre-sprint pass, or a phased Sprint 1 scoped to EPIC-01 only with EPIC-02–05 deferred to a second design-gate pass once ST-01 ships).
- Recorded as `ESC-20260717-01` in `claude/cycles/2026-07-17__release-v7.4/escalations.md` (Lifecycle/Process Integrity trigger — 24-hour SLA, may never be Accepted Risk).
