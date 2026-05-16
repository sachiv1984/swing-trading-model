**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-16
**Cycle:** 2026-05-16__release-v3.6

# Design Gate Record — 2026-05-16__release-v3.6

## Gate Status: PASSED

Completed: 2026-05-16
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed — EPIC-02 gate NOT met (fewer than 20 closed trades in live environment, confirmed 2026-05-16). EPIC-02 (ST-03/04/05) defers to v3.7. ST-05 block cleared.

---

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Capture planned_entry_price at trade entry | Design Not Applicable | Backend-only: schema migration, service computation, API response. No user-visible UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-02 | Update PlanVsReality component to display entry_delta_pct | Design Required | New comparison row in Plan vs Reality with colour-coded signed %, green/red styling, null placeholder message. | Spec update sufficient — no wireframe needed for single row addition to established component | `docs/specs/frontend/pages/trade_history.md` v1.9 | ✅ Cleared | Head of UX & Design |
| ST-03 | PT-04 spec authoring and gate confirmation | Design Not Applicable | This IS the spec authoring story (delegated_decision) — creates design artefacts for ST-04/05, not a UI implementation story. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 | Setup Quality Score backend endpoint | Design Not Applicable | Backend-only: deterministic API computation. No UI. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 | Setup Quality Score frontend display | Design Required | Score badge, band label, factor breakdown tooltip in Pre-Trade Research View. EPIC-02 gate NOT met — EPIC defers to v3.7. | DEFERRED (EPIC-02 gate not met — < 20 closed trades) | N/A — deferred | ✅ Cleared (EPIC deferred) | Product Owner (2026-05-16) |
| ST-06 | SC-RV-18 and SC-RV-19 Playwright coverage | Design Not Applicable | QA/testing story: Playwright tests + protocol doc updates. No UI component changes. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 | Research endpoint HTTP error code differentiation | Design Required | Frontend must handle new 404/503 codes. `research_view.md §6` previously lacked 404/503 display states. | Spec update sufficient — error pattern established, 404/503 display follows existing 500 pattern | `docs/specs/frontend/pages/research_view.md` v1.1 | ✅ Cleared | Head of UX & Design |
| ST-08 | Research page UX fix: regime lozenge and font consistency | Design Required | Direct visual fix: regime badge single-line constraint + font conformance to design_system.md. | Spec update sufficient — constraint defined by design_system.md badge/chip scale | `docs/specs/frontend/pages/research_view.md` v1.1 | ✅ Cleared | Head of UX & Design |
| ST-09 | execution_prompt.md §13 gate story pattern formalisation | Design Not Applicable | Governance file edit only. No UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | execution_prompt.md metadata + sprint_close + Phase 3 patches | Design Not Applicable | Governance file edit only. No UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |

---

## Blocked Items

None. All items cleared.

---

## Frontend Spec Updates (STEP 3)

| File | Version | Change Summary |
|------|---------|---------------|
| `docs/specs/frontend/pages/trade_history.md` | v1.8 → v1.9 | Entry Delta row added to Plan vs Reality comparison table (ST-02) |
| `docs/specs/frontend/pages/research_view.md` | v1.0 → v1.1 | §6 Error States: 404 + 503 rows added (ST-07); §4.3: regime badge single-line constraint added (ST-08) |

---

## Notes

- EPIC-02 (ST-03/04/05) defers to v3.7. Product Owner confirmed < 20 closed trades in live environment (2026-05-16). Sprint Planning must exclude ST-03, ST-04, ST-05 from the v3.6 sprint backlog.
- ST-07 and ST-08 both update `research_view.md` in the same version bump (v1.0 → v1.1) — consolidated into a single spec edit per STEP 3 efficiency.
- ST-01 feeds ST-02's backend API; design gate confirms ST-02 spec is updated so implementation can reference the locked spec immediately.
- No design artefacts (wireframes/UX decision records) required this cycle — all Design Required items were resolvable via direct spec update, confirmed by Head of UX & Design.
