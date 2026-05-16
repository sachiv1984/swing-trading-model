**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-16
**Cycle:** 2026-05-16__release-v3.6

# Design Gate Record — 2026-05-16__release-v3.6

## Gate Status: BLOCKED

Completed: 2026-05-16
PMO Lead: confirmed
Head of UX & Design: confirmed (ST-02, ST-07, ST-08 cleared; ST-05 pending EPIC-02 gate resolution)
Product Owner: pending (EPIC-02 gate confirmation required — see Blocked Items)

**Blocker:** ST-05 design artefact is pending the EPIC-02 gate condition (Product Owner must confirm 20+ closed trades). Resolution is binary:
- If gate NOT confirmed → EPIC-02 defers entirely (ST-03/04/05 all defer) → gate PASSES automatically
- If gate IS confirmed → Head of UX & Design confirms conditional pass: ST-05 artefact will be produced in ST-03 (Sprint 1 delegated_decision story) before Sprint 2 execution begins → gate PASSES

Sprint Planning may proceed once Product Owner issues EPIC-02 gate confirmation. No further design gate artefact work is required beyond that confirmation.

---

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Capture planned_entry_price at trade entry | Design Not Applicable | Backend-only: schema migration, service computation, API response. No user-visible UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-02 | Update PlanVsReality component to display entry_delta_pct | Design Required | New comparison row in Plan vs Reality with colour-coded signed %, green/red styling, null placeholder message. | Spec update sufficient — no wireframe needed for single row addition to established component | `docs/specs/frontend/pages/trade_history.md` v1.9 | ✅ Cleared | Head of UX & Design |
| ST-03 | PT-04 spec authoring and gate confirmation | Design Not Applicable | This IS the spec authoring story (delegated_decision) — creates design artefacts for ST-04/05, not a UI implementation story. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 | Setup Quality Score backend endpoint | Design Not Applicable | Backend-only: deterministic API computation. No UI. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 | Setup Quality Score frontend display | Design Required | Score badge, band label, factor breakdown tooltip in Pre-Trade Research View. `pre_trade_research.md` has no §Setup Quality Score section. Spec will be authored in ST-03 (Sprint 1). | PENDING — to be produced in ST-03 (Sprint 1, delegated_decision) | `docs/specs/frontend/pages/pre_trade_research.md` v0.1 — §Setup Quality Score not yet present | ❌ Blocked | — |
| ST-06 | SC-RV-18 and SC-RV-19 Playwright coverage | Design Not Applicable | QA/testing story: Playwright tests + protocol doc updates. No UI component changes. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 | Research endpoint HTTP error code differentiation | Design Required | Frontend must handle new 404/503 codes. `research_view.md §6` previously lacked 404/503 display states. | Spec update sufficient — error pattern established, 404/503 display follows existing 500 pattern | `docs/specs/frontend/pages/research_view.md` v1.1 | ✅ Cleared | Head of UX & Design |
| ST-08 | Research page UX fix: regime lozenge and font consistency | Design Required | Direct visual fix: regime badge single-line constraint + font conformance to design_system.md. | Spec update sufficient — constraint defined by design_system.md badge/chip scale | `docs/specs/frontend/pages/research_view.md` v1.1 | ✅ Cleared | Head of UX & Design |
| ST-09 | execution_prompt.md §13 gate story pattern formalisation | Design Not Applicable | Governance file edit only. No UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | execution_prompt.md metadata + sprint_close + Phase 3 patches | Design Not Applicable | Governance file edit only. No UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |

---

## Blocked Items

| Item ID | Blocker | Owner | Required by |
|---------|---------|-------|-------------|
| ST-05 | EPIC-02 gate condition (20+ closed trades) not yet confirmed by Product Owner. If confirmed: frontend spec §Setup Quality Score to be authored in ST-03 (Sprint 1) before Sprint 2 execution. | Product Owner (gate confirmation) + Head of UX & Design (conditional sign-off) | Product Owner confirmation before Sprint Planning seals |

---

## Frontend Spec Updates (STEP 3)

| File | Version | Change Summary |
|------|---------|---------------|
| `docs/specs/frontend/pages/trade_history.md` | v1.8 → v1.9 | Entry Delta row added to Plan vs Reality comparison table (ST-02) |
| `docs/specs/frontend/pages/research_view.md` | v1.0 → v1.1 | §6 Error States: 404 + 503 rows added (ST-07); §4.3: regime badge single-line constraint added (ST-08) |

---

## Clearing Path

To move gate status from BLOCKED → PASSED:

1. Product Owner confirms EPIC-02 gate condition (20+ closed trades):
   - **Gate NOT met:** EPIC-02 (ST-03/04/05) defers to v3.7. ST-05 block cleared. Gate PASSES.
   - **Gate IS met:** Head of UX & Design confirms conditional pass — ST-05 artefact will be produced in ST-03 (Sprint 1) before Sprint 2 begins. Sprint Planning must record ST-05 dependency on ST-03 closure. Gate PASSES.

2. PMO Lead updates `state.json` `design_gate_status` → `Passed`.

3. `plan sprint` may then be issued.

---

## Notes

- ST-05's "blocked" status is architectural, not a process failure. The EPIC-02 gate story pattern (Sprint 1 spec authoring → Sprint 2 implementation) is intentional and consistent with the §13 gate story pattern being formalised in ST-09.
- ST-07 and ST-08 both update `research_view.md` in the same version bump (v1.0 → v1.1) — consolidated into a single spec edit per STEP 3 efficiency.
- ST-01 feeds ST-02's backend API; design gate confirms ST-02 spec is updated so implementation can reference the locked spec immediately.
- No design artefacts (wireframes/UX decision records) required this cycle — all Design Required items were resolvable via direct spec update, confirmed by Head of UX & Design.
