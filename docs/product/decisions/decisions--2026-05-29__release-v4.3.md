**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v4.3
**Cycle:** 2026-05-29__release-v4.3
**Last Updated:** 2026-05-29
**Supersession note:** *(completed at Post-Ship Closure)*

---

# Decisions Record — v4.3 Governance Consolidation, QA Debt Clearance & Ops Hardening

---

## Scope Decisions

| Decision | Rationale | Authority |
|----------|-----------|-----------|
| Include all 3 v4.2 OA items as EPIC-01 stories | OA items have deadlines "before v4.3 sprint seal" — must land in v4.3 | PMO Lead |
| Include BLG-FE-38 (Arc 5 compliance in monthly P&L) | Provisional-Target v4.1 overdue; gates cleared since v4.0; no further reason to defer | Product Owner |
| Defer SI-02 pre-planning cluster | Gate condition (< 20 closed trades) confirmed not met; 5 consecutive deferrals — PO written rationale on record (v4.1 sprint planning) | Product Owner |
| Defer BLG-GOV-67 (SI-05 Phase 1) | Gate: SI-01+SI-03 live ≥30 days; gate clears 2026-06-21 after this sprint planning; schedule for v4.4 | Product Owner |
| Design Gate: NOT_REQUIRED | All scope items are governance, QA, ops, security, or backend/frontend spec implementation; no UX design decisions required | Head of UX & Design (per design gate language scan: 0 items flagged) |
| v4.3 roadmap section added inline | Extended-tier rebalance left [TBD] next release; PO authorized inline addition per Option A (same pattern as v4.2 planning) | Product Owner |

---

## Sequencing Decisions

| Decision | Rationale |
|----------|-----------|
| EPIC-01 first (Sprint 1) | OA items are sprint-seal prerequisites; must land before sprint planning seals |
| EPIC-04 (Sprint 1) alongside EPIC-01 | Frontend items are independent and lightweight; good Sprint 1 pairing |
| EPIC-02 + EPIC-03 (Sprint 2) | QA and ops items are data-gathering/verification tasks; staging verifications require staging env parity (EPIC-03 ST-13) to run first |
| EPIC-03 ST-13 (staging parity audit) sequenced before EPIC-02 ST-06/07/08 (staging verifications) | Staging verifications require confirmed env parity to avoid false negatives | 

---

## Accepted Risks

None — no escalations raised during release planning. All risks classified as Medium or Low with defined mitigations (see release_plan.md Risk Register).

---

## Supersession Note

*(Completed at Post-Ship Closure)*
