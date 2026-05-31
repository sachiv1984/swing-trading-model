**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v4.7
**Cycle:** 2026-05-31__release-v4.7
**Last Updated:** 2026-05-31

---

# Decisions Record — v4.7

---

## Scope Decisions

| Decision | Rationale | Authority |
|----------|-----------|-----------|
| Use double capacity (~24–28 days/sprint) — same as v4.6 | User instruction: "keep same capacity." Double capacity baseline set for v4.6 (2026-05-27 workforce revision); carried forward to v4.7. | Product Owner |
| Promote BLG-FEAT-38 (aged 3+ cycles) to firm scope | Provisional-Target v4.1 — aged 3+ cycles without story; backlog age advisory triggered. Gate cleared (BLG-FEAT-36/37 complete v4.0). | Product Owner |
| Promote BLG-OPS-28 (aged 4+ cycles) to firm scope | Provisional-Target v4.1 — aged 4+ cycles without story; backlog age advisory triggered. | Product Owner |
| Include BLG-GOV-62 (SI-04 §13 pre-assessment) as P1 firm item | P1 priority; SI-04 planning is approaching (Arc 5 near-complete); pre-assessment blocks SI-04 sprint planning from sealing. Proactive risk elimination. | Head of Specs Team |
| Include BLG-GOV-67 (SI-05 Phase 1) as conditional Sprint 2 item | Gate (SI-01 + SI-03 live ≥30 days) clears 2026-06-21 — within expected Sprint 2 window. Conditional gate model used per prior cycles. | Product Owner |
| Defer BLG-OPS-13 (API performance baseline re-run) | P3, M effort, requires live environment coordination. OA-02 advisory only. No capacity constraint requires inclusion. | PMO Lead |
| Defer all Arc 4 PO-02–05 and Arc 6 features | Data density gates not met; earliest gate clear ~Oct 2026. | Product Owner |
| Defer SI-02 Frontend (EPIC-02 from v4.6) | 7th consecutive deferral; gate NOT MET (0 closed trades with linked trade_plans; ~Nov 2026). | Product Owner |

---

## Sequencing Decisions

| Decision | Rationale |
|----------|-----------|
| Staging verifications (EPIC-03) Sprint 1, merge first | Clear v4.6 OAs (BLG-OPS-44/45) and aged item (BLG-OPS-28) before feature work. Isolated; no dependencies. |
| Feature work (EPIC-02) and assessments (EPIC-04) Sprint 1, parallel | BLG-FEAT-38 and assessment items are independent. Parallel delivery within Sprint 1. |
| Arc 5 pre-work (EPIC-01 ST-01) Sprint 1 | SI-04 §13 pre-assessment is a P1 item that unblocks SI-04 sprint planning. Must ship before next relevant sprint planning cycle. |
| EPIC-01 ST-02 (SI-05 Phase 1) Sprint 2, conditional | Gate clears 2026-06-21; conditional on PO confirming gate before Sprint 2 seals. |
| Merge order: EPIC-03 → EPIC-04 → EPIC-02 → EPIC-01 (Sprint 1 firm); EPIC-01 (Sprint 2 conditional) | EPIC-03 first (OA clearance); EPIC-04 parallel (independent assessments); EPIC-02 after (feature requiring staging verification first); EPIC-01 Sprint 1 firm ST-01 can merge alongside. |

---

## Accepted Risks

None — no escalations raised; no accepted risk escalations.

---

## Supersession Note

*(Completed at Post-Ship Closure — leave blank.)*
