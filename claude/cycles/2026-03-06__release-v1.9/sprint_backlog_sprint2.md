**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-03-11
**Cycle:** 2026-03-06__release-v1.9
**Release:** v1.9
**Sprint:** 2 of 2
**Sprint Goal:** Deliver the v1.9 user value features — canonicalise compliance metrics definitions and surface them in the frontend, implement the structured trade reflection form, add cohort analysis and R-multiple distribution to the analytics page, and launch the dashboard homepage — completing the full v1.9 release scope.
**Backlog Slice Source:** claude/cycles/2026-03-06__release-v1.9/stage4_backlog_slice.md

---

# Sprint Backlog — 2026-03-06__release-v1.9 Sprint 2

---

## Sprint Scope

---

### EPIC-01 — Trade Reflection & Compliance Metrics

**Maps to:** S2-01, S2-02
**Owner:** Head of Specs Team (spec/metrics); Head of Engineering (backend); Base44 Frontend Prompt Owner (frontend)
**Estimated effort:** ~17 hours (mid: ST-01 7 hrs + ST-02 10 hrs)
**Risk IDs:** RISK-01 (PASS), RISK-02 (monitor)
**Execution sequence:** Wave 1 (ST-01) → Wave 2 (ST-02)

---

#### ST-01 — Canonicalise Basic Compliance Metrics

**Owner:** Metrics Definitions & Analytics Owner (spec); Head of Engineering (backend); Base44 Frontend Prompt Owner (frontend)
**Estimated effort:** ~6–8 hours
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (independent; metrics batch with ST-03 cohort defs and ST-04 R-multiple formula advisable)

**Notes:** Spec-first within item — metrics_definitions.md update must commit before backend compute begins. FinOps LL-05 capacity check: PASS (Metrics Definitions owner confirmed available). Batch opportunity: include cohort metric defs (ST-03) and R-multiple formula (ST-04) in the same metrics_definitions.md version increment.

---

#### ST-02 — Structured Trade Reflection Template

**Owner:** Frontend Specs & UX Documentation Owner (spec); Head of Engineering (backend); Base44 Frontend Prompt Owner (frontend)
**Estimated effort:** ~8–12 hours
**Delegation class:** delegated_backend + delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** ST-01 complete (metrics definitions canonical before ST-02 implementation); Data Model & Domain Schema Owner schema confirmation (at-execution pre-condition — not a planning blocker)

**Notes:** Frontend spec `docs/specs/frontend/pages/trade_reflection.md` v0.1 was pre-approved by Design Gate (2026-03-06). RISK-02 — Data Model owner must confirm trade_reflections schema before backend work begins; record at execution pre-alignment.

---

### EPIC-02 — Analytics Enhancements

**Maps to:** S2-03, S2-18
**Owner:** Head of Engineering
**Estimated effort:** ~18 hours (mid: ST-03 10 hrs + ST-04 8 hrs)
**Risk IDs:** RISK-03 (mitigation active)
**Execution sequence:** Wave 2 (both items, after ST-01 metrics canonical)

---

#### ST-03 — Cohort Analysis

**Owner:** Head of Engineering
**Estimated effort:** ~8–12 hours
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** ST-01 (cohort metric definitions — may batch into ST-01 metrics_definitions.md update or add in same PR)

**Notes:** RISK-03 mitigation active — cohort defs can be batched with ST-01 R-multiple and compliance metrics into single metrics_definitions.md version increment.

---

#### ST-04 — R-Multiple Distribution Report

**Owner:** Metrics Definitions & Analytics Owner (definition); Head of Engineering (implementation)
**Estimated effort:** ~6–10 hours
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** ST-01 (R-multiple formula must be canonical in metrics_definitions.md before implementation)

**Notes:** RISK-03 mitigation — R-multiple formula batched with ST-01 metrics update.

---

### EPIC-03 — Dashboard Homepage

**Maps to:** S2-04
**Owner:** Frontend Specs & UX Documentation Owner (spec); Head of Engineering (implementation)
**Estimated effort:** ~8 hours (mid)
**Risk IDs:** RISK-04 (advisory)
**Execution sequence:** Wave 1 (independent)

---

#### ST-05 — Dashboard Homepage / Session Summary

**Owner:** Frontend Specs & UX Documentation Owner (spec); Head of Engineering (implementation)
**Estimated effort:** ~6–10 hours
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None (all data from existing endpoints)

**Notes:** RISK-04 — composite endpoint decision at ST-05 execution start. Head of Engineering to confirm whether `GET /dashboard/summary` is needed or individual endpoint calls are sufficient. New frontend spec: `docs/specs/frontend/pages/dashboard_home.md` v0.1 (pre-approved by Design Gate 2026-03-06). If composite endpoint added: document in API contracts + openapi.yaml; aggregation-only constraint enforced.

---

### EPIC-05 — QA & Test Infrastructure (Sprint 2 partial: ST-12 only)

**Maps to:** S2-16 Phase 2
**Owner:** QA & Testing Owner
**Estimated effort:** ~6 hours (mid)
**Risk IDs:** None (Sprint 1 infra delivered; this item is distributed authoring)
**Execution sequence:** Wave 3 (distributed throughout sprint as features complete)

---

#### ST-12 — Canonical Test Scenario Library Phase 2 (v1.9 Features)

**Owner:** QA & Testing Owner
**Estimated effort:** ~4–8 hours (distributed)
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** EPIC-01, EPIC-02, EPIC-03 feature delivery (scenarios authored as each feature completes — distributed)

**Notes:** ST-12 test infrastructure foundation delivered in Sprint 1 (ST-11: Playwright mock layer, 17 scenarios automated). Sprint 2 ST-12 extends with scenarios for new features as they land. Playwright test maintenance protocol applies (risk_dashboard_scenarios.md §5.5 v1.2, 2026-03-10). HashRouter routing note applies (tests/e2e/risk-dashboard.spec.js header).

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~15–25 hours |
| Total estimated effort (Sprint 2 in-scope) | ~49 hours (mid); ~38–60 hours (range) |
| Utilisation | ~200–330% |
| Over-allocation | **Yes — ~3–4 weeks elapsed at current pace** |
| Over-allocation accepted by Product Owner? | Yes — confirmed 2026-03-11 |

---

## Items Deferred This Sprint

*(None — all Sprint 2 items are in scope)*

---

## Deferred Execution Blockers Accepted

*(None — `deferred_execution_blockers` was empty in `state.json`)*

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Data Model & Domain Schema Owner: confirm trade_reflections schema before ST-02 backend | Data Model Owner | No — at-execution pre-condition only |
| Head of Engineering: composite endpoint decision for ST-05 | Head of Engineering | No — at ST-05 execution start |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** confirmed — 2026-03-11
**Scope confirmed:** confirmed — all 6 items (ST-01, ST-02, ST-03, ST-04, ST-05, ST-12), 2026-03-11
**Capacity over-allocation explicitly accepted:** confirmed — ~49 hrs (~3–4 weeks elapsed at current pace), 2026-03-11
**Deferred execution blockers accepted:** N/A
**Signed off by:** Product Owner
**Date:** 2026-03-11
