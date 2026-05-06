**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-05
**Cycle:** 2026-05-05__release-v3.2

---

# Design Gate Record — 2026-05-05__release-v3.2

## Gate Status: PASSED

Completed: 2026-05-05
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed (ST-01/ST-02/ST-03 research view, ST-04 navigation integration / BLG-FE-22, ST-05/ST-06 entry checklist — all design artefacts approved)

---

## Item Classification Summary

| Item ID | Title | Classification | Design Artefact | Frontend Spec | Gate Status |
|---------|-------|----------------|-----------------|---------------|-------------|
| ST-01 | Pre-trade research view component — data display | Design Required | `docs/design/2026-05-05__release-v3.2/pre-trade-research-view/ux_spec.md` v1.0 | `docs/specs/frontend/pages/pre_trade_research.md` v0.1 (new) | ✅ Cleared |
| ST-02 | Trade plan context panel in research view | Design Required | `docs/design/2026-05-05__release-v3.2/pre-trade-research-view/ux_spec.md` v1.0 | `docs/specs/frontend/pages/pre_trade_research.md` v0.1 (§7) | ✅ Cleared |
| ST-03 | Prospective heat at entry metric integration (PT-03) | Design Required | `docs/design/2026-05-05__release-v3.2/pre-trade-research-view/ux_spec.md` v1.0 | `docs/specs/frontend/pages/pre_trade_research.md` v0.1 (§6) | ✅ Cleared |
| ST-04 | Navigation integration — screener and watchlist entry points to research view | Design Required | `docs/design/2026-05-05__release-v3.2/screener-to-research-navigation/ux_spec.md` v1.0 | `docs/specs/frontend/pages/screener_results.md` v1.1 (§11); `docs/specs/frontend/pages/watchlist.md` v0.2 (Research Navigation section) | ✅ Cleared |
| ST-05 | Entry checklist schema, component, and Trade Plan form integration | Design Required | `docs/design/2026-05-05__release-v3.2/pre-trade-entry-checklist/ux_spec.md` v1.0 | `docs/specs/frontend/pages/trade_plan.md` v0.2 (§6) | ✅ Cleared |
| ST-06 | Checklist pre-population from trade plan data and research view link | Design Required | `docs/design/2026-05-05__release-v3.2/pre-trade-entry-checklist/ux_spec.md` v1.0 | `docs/specs/frontend/pages/trade_plan.md` v0.2 (§6.2, §6.3) | ✅ Cleared |
| ST-07 | sprint_planning_prompt.md STEP 0 main-branch verification | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-08 | execution_prompt.md STEP 5.1 deviations_filed enforcement | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-09 | execution_prompt.md §3.1.A test_scenarios post-story advisory | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-10 | Playwright waitFor pattern — test authoring standard | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-11 | Trade Plan domain test scenario registration (TEST-GAP-EPIC-01) | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-12 | Earnings Calendar and UK screener test registration (TEST-GAP-EPIC-03) | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-13 | React component inventory (BLG-FE-16) | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-14 | Design system document (BLG-FE-21) | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-15 | Alpaca credential audit and rotation policy (BLG-SEC-05) | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-16 | External API dependency risk register (BLG-GOV-18) | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-17 | Cycle artefact inventory and maintenance review (BLG-GOV-11) | Design Not Applicable | N/A | N/A | ✅ Cleared |

---

## Blocked Items

None.

---

## Design Artefacts Produced This Cycle

| Item | Artefact | Location | Approved by |
|------|----------|----------|-------------|
| ST-01, ST-02, ST-03 | Pre-Trade Research View UX decision record | `docs/design/2026-05-05__release-v3.2/pre-trade-research-view/ux_spec.md` | Product Owner — 2026-05-05 |
| ST-04 / BLG-FE-22 | Screener-to-Research Navigation & Morning Routine Workflow UX spec | `docs/design/2026-05-05__release-v3.2/screener-to-research-navigation/ux_spec.md` | Product Owner — 2026-05-05 |
| ST-05, ST-06 | Pre-Trade Entry Checklist UX decision record | `docs/design/2026-05-05__release-v3.2/pre-trade-entry-checklist/ux_spec.md` | Product Owner — 2026-05-05 |

---

## Frontend Spec Versions Locked for Sprint Planning

| Item | Spec | Version |
|------|------|---------|
| ST-01, ST-02, ST-03 | `docs/specs/frontend/pages/pre_trade_research.md` | v0.1 (new) |
| ST-04 | `docs/specs/frontend/pages/screener_results.md` | v1.1 |
| ST-04 | `docs/specs/frontend/pages/watchlist.md` | v0.2 |
| ST-05, ST-06 | `docs/specs/frontend/pages/trade_plan.md` | v0.2 |

---

## Classification Rationale Notes

**ST-01 through ST-04 (Design Required → Cleared):** EPIC-01 delivers a new page (`/research/{ticker}`) with four distinct UI regions (price/signal, prospective heat, trade plan context, news) plus navigation integration across two existing pages. All four stories have user-visible rendering. No prior design artefacts existed for these stories. Head of UX & Design produced a single combined UX spec covering ST-01/ST-02/ST-03 (research view layout and regions) and a separate spec for ST-04/BLG-FE-22 (navigation workflow). Product Owner approved both. Frontend spec `pre_trade_research.md` v0.1 authored (new). `screener_results.md` updated to v1.1 (§11 Research Navigation). `watchlist.md` updated to v0.2 (Research Navigation section). Head of Specs Team confirmed lifecycle compliance.

**ST-05, ST-06 (Design Required → Cleared):** EPIC-02 embeds a checklist component in the Trade Plan creation/edit form (new UI element) and adds a "Review research" link. Both stories have user-visible rendering changes. Head of UX & Design produced `pre-trade-entry-checklist/ux_spec.md` v1.0. `trade_plan.md` v0.2 authored — this file also recovers the v3.1 gap (see Notes). Product Owner approved.

**ST-07 through ST-17 (Design Not Applicable):** EPIC-03 stories are governance prompt patches and test scenario registration — no user-visible UI change. EPIC-04 stories are documentation and security operations documents — no UI change. Confirmed Design Not Applicable by Head of UX & Design.

---

## Notes

**BLG-FE-22 fulfilment:** BLG-FE-22 (Screener morning routine UX spec) was flagged in the v3.2 release plan as a mandatory design gate prerequisite deliverable, not a sprint story. The `screener-to-research-navigation/ux_spec.md` v1.0 produced at this design gate fulfils BLG-FE-22. Sprint Planning may mark BLG-FE-22 as delivered at this gate.

**v3.1 gap — trade_plan.md missing:** The v3.1 design gate record (`claude/cycles/2026-04-29__release-v3.1/design_gate.md`) stated that `docs/specs/frontend/pages/trade_plan.md` v0.1 was created for ST-03. The file was not present in the repository at the start of the v3.2 design gate. The v3.1 design artefact `docs/design/2026-04-29__release-v3.1/trade-plan/ux_spec.md` was also absent. `trade_plan.md` v0.2 has been created at this design gate, combining the recovery of the v3.1 content (creation flow, detail view, entry points) with the v3.2 checklist additions. This is a process deviation from v3.1; the recovery is complete as of this gate.

**screener_results.md baseline version:** At the start of this design gate, `screener_results.md` was at v1.0 (not v1.2 as stated in the v3.1 design gate record). The v3.1 updates for ST-06 (v1.1) and ST-08 (v1.2) were not committed to the repository. This design gate applies only the v3.2 ST-04 navigation update (v1.0 → v1.1). The v3.1 content gap (UK ticker display and Earnings Calendar column specs) should be filed as a follow-up item if those features are implemented in the codebase without their spec updates.

**watchlist.md baseline version:** At the start of this design gate, `watchlist.md` was at v0.1 (not v0.2 as stated in the v3.1 design gate record). Updated to v0.2 at this gate for ST-04 Research Navigation.
