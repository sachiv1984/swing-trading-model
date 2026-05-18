**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-18
**Cycle:** 2026-05-18__release-v3.7

# Design Gate Record — 2026-05-18__release-v3.7

## Gate Status: PASSED

Completed: 2026-05-18
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

---

## EPIC-02 Gate Decision (Pre-Sprint Required Decision — RISK-01)

**Gate condition:** Product Owner must confirm ≥ 20 closed trades before sprint planning seals. If not confirmed, entire EPIC-02 (ST-04, ST-05, ST-06) defers to v3.8.

**Required action before `plan sprint`:** Product Owner to confirm or deny the closed-trade count at sprint planning. This decision gates EPIC-02 scope; all other EPICs (EPIC-01, EPIC-03, EPIC-04) are unconditional.

**Design gate posture for ST-06:** Design artefacts and frontend spec updates have been produced unconditionally so they are ready if the gate is confirmed. If EPIC-02 defers, §7a in trade_plan.md and the §5 quality score row in pre_trade_research.md remain as spec pre-work for v3.8 — no runtime cost.

---

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Signals backend — watchlisted status support | Design Pre-Approved | Backend only: DB constraint + PATCH endpoint + spec/data_model updates. No UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-02 | Signals frontend — Add to Watchlist CTA | Design Required | New primary CTA on signal cards; watchlisted state; "View in Watchlist" link | `docs/design/2026-05-18__release-v3.7/signals-add-to-watchlist/ux_spec.md` | `docs/specs/frontend/pages/signals.md` v0.3 | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-03 | Trade plan form — signal context panel | Design Required | New read-only panel in trade plan creation form; pre-population of rationale and stop fields | `docs/design/2026-05-18__release-v3.7/signal-context-panel/ux_spec.md` | `docs/specs/frontend/pages/trade_plan.md` v0.5 | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-04 | PT-04 spec authoring + gate confirmation | Design Not Applicable | Spec doc creation + PO gate decision; no user-visible UI from this story alone | N/A | N/A | ✅ Cleared (conditional on EPIC-02 gate) | Head of UX & Design |
| ST-05 | PT-04 backend — quality score endpoint | Design Not Applicable | Backend endpoint only | N/A | N/A | ✅ Cleared (conditional on EPIC-02 gate) | Head of UX & Design |
| ST-06 | PT-04 frontend — quality score display | Design Required (conditional) | Score displayed on Trade Plan detail + Research View — new UI on two pages. Conditional on EPIC-02 gate. | `docs/design/2026-05-18__release-v3.7/quality-score-display/ux_spec.md` | `docs/specs/frontend/pages/trade_plan.md` v0.6; `docs/specs/frontend/pages/pre_trade_research.md` v0.2 | ✅ Cleared (design pre-work complete; activation conditional on EPIC-02 gate at sprint planning) | Head of UX & Design + Product Owner |
| ST-07 | execution_prompt.md patches ×3 | Design Not Applicable | Governance prompt edits only; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | qa_evidence_template.md fail-path | Design Not Applicable | Template update only; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | Database stub conftest consolidation | Design Not Applicable | Test infrastructure refactor; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | Pycache hygiene + Research page font staging | Design Pre-Approved | BLG-OPS-16: git hygiene only. BLG-FE-35: staging audit against existing design_system.md — no new design required | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | scored_initiatives.md refresh | Design Not Applicable | Governance document refresh; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |

---

## Frontend Spec Versions Locked for Sprint Planning

| Spec File | Version | Notes |
|-----------|---------|-------|
| `docs/specs/frontend/pages/signals.md` | **v0.3** | Signal card CTA change + watchlisted state (ST-02) |
| `docs/specs/frontend/pages/trade_plan.md` | **v0.6** | Signal Context Panel (ST-03, §5a) + Quality Score (ST-06, §7a conditional) |
| `docs/specs/frontend/pages/pre_trade_research.md` | **v0.2** | Quality Score row in §5 (ST-06, conditional) |

All other frontend specs unchanged and pre-approved at their current versions.

---

## Design Artefacts Produced This Cycle

| Artefact | Story | Path |
|----------|-------|------|
| Signals — Add to Watchlist UX Spec | ST-02 | `docs/design/2026-05-18__release-v3.7/signals-add-to-watchlist/ux_spec.md` |
| Signal Context Panel UX Spec | ST-03 | `docs/design/2026-05-18__release-v3.7/signal-context-panel/ux_spec.md` |
| Quality Score Display UX Spec | ST-06 | `docs/design/2026-05-18__release-v3.7/quality-score-display/ux_spec.md` |

---

## Notes

- RISK-01 (EPIC-02 gate): Pre-sprint required decision for Sprint Planning STEP -1. Product Owner must confirm ≥ 20 closed trades. If not confirmed, EPIC-02 (ST-04/ST-05/ST-06) defers to v3.8 and sprint scope = 8 stories (EPICs 01/03/04).
- No items left in BLOCKED state.
- Design gate produces 3 artefacts and updates 3 frontend specs. All Design Required items cleared.
