**Owner:** Head of Specs Team
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-06

---

# Stage 2 — Backlog Health Review

**Cycle:** 2026-03-06__item-3.4
**Date:** 2026-03-06
**Authorities:** Head of Specs Team (process), Product Owner (planning ownership)

---

## Overview

Backlog reviewed across all sections. 3.4 Risk Dashboard items (BLG-RD-01–11, TEST-GAP-EPIC-01) are new to this cycle.

---

## Section 1 — Platform & Validation Governance

| Item | Status | Assessment |
|------|--------|------------|
| BLG-TECH-05 — Prometheus metrics endpoint | P3 — v2.1 candidate | Valid. No orphan risk. Correctly deferred. |

**Health:** Healthy. No action required.

---

## Section 2 — Product Feature Backlog (User-Facing)

| Item | Status | Assessment |
|------|--------|------------|
| BLG-FEAT-03 — Slippage Tracking | P2 — Orphan notice active | Still orphaned. No roadmap home. Assign home at v1.9 or v2.0 release planning, or close if de-prioritised. |
| BLG-FEAT-08 — Basic Compliance Metrics | P2 — Active, v1.9 pre-work | Valid. Gate for 5.1. No issues. |

**Health concern:** BLG-FEAT-03 has been orphaned for at least 2 cycles. Product Owner should make an explicit decision at v1.9 release planning: assign to a release or kill.

---

## Section 3 — Deferred / v2.1 Candidates

Deferred items remain valid. No action required.

---

## Section 6 — Test Coverage Gaps

| Item | Status | Assessment |
|------|--------|------------|
| TEST-GAP-EPIC-06 (v1.7) | Orphan notice active | No BLG-ID assigned; no roadmap home. QA & Testing Owner to create scenarios per verification_report.md §6. Still unresolved. Flag for action at v1.9 pre-alignment. |
| TEST-GAP-EPIC-01 (v1.8) | New — P2, v1.9 target | Valid. Correctly filed with all required fields. No action required from backlog perspective. |

---

## Section 7 — Spec & Documentation Debt

| Item | Status | Assessment |
|------|--------|------------|
| BLG-SPEC-D1 — API Contracts README frozen | P3 | Still open. Low priority. Valid. |
| BLG-SPEC-D2 — settings_endpoints.md mismatch | ✅ COMPLETE | Closed in v1.8 (ST-09). No action. |
| BLG-SPEC-D3 — GET /market/status undocumented | P2 | Still open. Assign to v1.9 or v2.0 spec work. |
| BLG-SPEC-D4 — GET /positions/search/tags undocumented | P3 | Still open. Low priority. |
| BLG-SPEC-D7 — openapi.yaml frozen | ✅ COMPLETE | Closed in v1.8 (ST-10). No action. |
| BLG-SPEC-D8 — System_status_report.md missing header | P3 | Still open. Low priority. |
| BLG-SPEC-D9 — Wrong path references to lifecycle guide | P3 | Still open. Low priority. |
| BLG-SPEC-G1 — settings_model.md missing | P2 | Still open. Third cycle open (since 2026-02-21). Flag: approaching P1 threshold — consider resolution in v1.9. |
| BLG-SPEC-G2 — Error Response Standard missing | P2 | Still open. Third cycle open (since 2026-02-21). Flag: approaching P1 threshold. |
| BLG-SPEC-G3 — logging_standards.md not in Specs_Index | P3 | Still open. Low priority. |
| BLG-SPEC-G4 — ADR-002 in wrong location | P3 | Still open. Low priority. |
| BLG-SPEC-G5 — validation_system.md non-compliant owner | P3 | Still open. Third cycle open. |

**Health concern:** BLG-SPEC-G1 and BLG-SPEC-G2 are in their third consecutive cycle open. Both are P2. They risk becoming de facto P1 if v1.9 spec authoring begins without resolving them — settings model and error response standard are foundational for new endpoint spec work. Product Owner should prioritise at v1.9 pre-alignment.

---

## Section 8 — New Backlog Items (IW-20260304-01)

| Item | Status | Assessment |
|------|--------|------------|
| BLG-NEW-01 — Golden Output CI Baseline | ✅ COMPLETE (v1.8 ST-05) | Done. Archive candidate. |
| BLG-NEW-02 — Backtest Stop Reconciliation | ✅ COMPLETE (v1.8 ST-06) | Done. Archive candidate. |
| BLG-NEW-03 — Unavailability Failure Mode | ✅ COMPLETE (v1.8 ST-11) | Done. Archive candidate. |
| BLG-NEW-04 — AI Governance Policy | Open — P2 | Still open. No roadmap home. Eligible for v1.9 backlog slice consideration. |
| BLG-NEW-05 — Dependency Vulnerability Scanning | ✅ COMPLETE (v1.8 ST-07) | Done. Archive candidate. |
| BLG-NEW-07 — Running API Changelog | ✅ COMPLETE (v1.8 ST-12) | Done. Archive candidate. |
| BLG-NEW-08 — OpenAPI Drift Detection | ✅ COMPLETE (v1.8 ST-08) | Done. Archive candidate. |

**Health concern:** 5 of 7 items in §8 are complete. Backlog management engine (`groom backlog`) should archive BLG-NEW-01, 02, 03, 05, 07, 08 after this cycle closes. This is not in scope for the roadmap rebalance engine.

---

## Section 9 — Risk Dashboard Deviation Backlog

| Item | Priority | Assessment |
|------|----------|------------|
| BLG-RD-01 through BLG-RD-11 | P2–P3 | All valid. All target v1.9. All correctly filed with required deviation fields. No compliance issues. |

**Oldest/highest risk items:** BLG-RD-01, BLG-RD-03, BLG-RD-04, BLG-RD-08, BLG-RD-10, BLG-RD-11 are P2. BLG-RD-08 requires Head of Specs Team verification (owner decision, not engineering fix).

---

## Backlog Health Summary

| Category | Count | Health |
|----------|-------|--------|
| Quick win / tech debt (active) | 1 (BLG-TECH-05) | Healthy |
| Feature items (active) | 2 (BLG-FEAT-03, BLG-FEAT-08) | BLG-FEAT-03 orphan requires decision |
| Spec debt (active) | 10 (D1, D3, D4, D8, D9, G1–G5) | G1, G2 approaching escalation threshold |
| New quality items (v1.8 additions — active) | 1 (BLG-NEW-04) | Healthy |
| Risk Dashboard deviations (v1.9) | 11 (BLG-RD-01–11) | Healthy — all filed correctly |
| Test coverage gaps | 2 (TEST-GAP-EPIC-01, 06) | EPIC-06 orphan — needs assignment |

**No backlog items are obsolete.**
**No duplicate items identified.**
**No strategic misalignment identified — all items trace to documented roadmap initiatives or delivery verification outputs.**
**Quick wins being ignored:** None — BLG-NEW items delivered in v1.8. BLG-FEAT-03 is a candidate for action or kill at v1.9 planning.
**Technical debt accumulation:** BLG-SPEC-G1, G2 are the highest-priority unresolved spec debt items. Alert raised.

---

## Recommendations for v1.9 Release Planning

1. Explicitly resolve BLG-FEAT-03 (assign release or kill)
2. Prioritise BLG-SPEC-G1 (settings_model.md) — pre-work for any v1.9 settings-adjacent spec authoring
3. Prioritise BLG-SPEC-G2 (Error Response Standard) — foundational for new endpoint documentation
4. Assign TEST-GAP-EPIC-06 a BLG-ID and owner at v1.9 pre-alignment
5. Trigger `groom backlog` after this cycle to archive completed BLG-NEW items
