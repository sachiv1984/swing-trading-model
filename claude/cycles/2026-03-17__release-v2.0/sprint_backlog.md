# Sprint Backlog — 2026-03-17__release-v2.0

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-03-17
**Cycle:** 2026-03-17__release-v2.0
**Release:** v2.0
**Sprint Goal:** Ship the v2.0 core product scope: fix the P1 portfolio response defect, deliver the UK tax-year P&L report endpoint and frontend view, and expose the signal exposure controls — making all three production-ready in a single sprint.
**Backlog Slice Source:** original — `claude/cycles/2026-03-17__release-v2.0/stage4_backlog_slice.md`

---

## Pre-Sprint Completed Items

The following items were completed before sprint seal and do not require execution:

| Item | Title | Evidence |
|------|-------|----------|
| ST-03 | Author tax-year P&L report spec | `docs/specs/api_contracts/reports_endpoints.md` v0.1 — signed off, registered |
| ST-11 | QA: notification delivery test scenarios | `qa_notification_planning.md` — EPIC-03 deferred v2.1; RISK-01 resolved |

---

## Sprint Scope

### EPIC-04 — Backend Completeness

**Maps to:** S2-04
**Owner:** Head of Engineering
**Estimated effort:** ~9 hrs mid (core ~3 hrs; stretch +6 hrs)
**Risk IDs:** RISK-04 (P1 open defect)
**Execution sequence:** 1 (ST-12 is Sprint item 1)

#### ST-12 — Fix GET /portfolio missing 4 fields (BLG-BE-01 P1)

**Owner:** Head of Engineering
**Estimated effort:** ~3 hrs mid
**Delegation class:** `delegated_backend`
**Priority:** P1 — Sprint item 1
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`
**Dependencies:** None
**Notes:** Must be Sprint item 1. Closes GAP-03. Director of Quality staging verification required.

---

#### ST-13 — Spec + implement GET /portfolio/prospective-heat (BLG-BE-02 stretch) ✅ DONE

**Owner:** Head of Engineering + Head of Specs Team
**Estimated effort:** ~6 hrs mid
**Delegation class:** `delegated_backend`
**Priority:** P3 — stretch; deprioritise if core capacity runs short
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`
**Dependencies:** None
**Notes:** ProspectiveHeatPanel frontend component already exists; this story adds the backend endpoint and removes `@unittest.skip`.
**Completion:** 2026-03-17 — `portfolio_endpoints.md` v2.0.0 spec authored; `routers/prospective_heat.py` implemented; `@unittest.skip` removed; 7 tests pass + 3 field-contract tests pass (10 total). DEV-ST05-01 closed. BLG-BE-02 COMPLETE. Director of Quality sign-off required before staging verification.

---

### EPIC-01 — 4.3 Signal Exposure Enhancement

**Maps to:** S2-03
**Owner:** Head of Specs Team + Base44 Frontend
**Estimated effort:** ~3.5 hrs mid
**Risk IDs:** RISK-03 (resolved at design gate)
**Execution sequence:** 2

#### ST-01 — Author signals page frontend spec

**Owner:** Head of Specs Team + Base44 Frontend Prompt Owner
**Estimated effort:** ~1 hr mid
**Delegation class:** `delegated_decision`
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`
**Dependencies:** None (signals.md v0.1 authored at design gate — remaining AC: register in Specs_Index.md + Head of Specs Team formal sign-off)
**Notes:** `docs/specs/frontend/pages/signals.md` v0.1 was produced at the design gate session. ST-01 execution = (1) register signals.md in `docs/specs/Specs_Index.md`; (2) confirm Head of Specs Team formal sign-off on record.

---

#### ST-02 — Implement top_n and lookback_days controls on signals page

**Owner:** Base44 Frontend
**Estimated effort:** ~2.5 hrs mid
**Delegation class:** `delegated_frontend`
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`
**Dependencies:** ST-01 (signals.md registered and signed off before implementation begins)
**Notes:** Frontend controls per `signals.md` spec; 500ms debounce; `GET /signals?top_n=N&lookback_days=N` re-fetch on change.

---

### EPIC-05 — Documentation & Standards Pack

**Maps to:** S2-05
**Owner:** Infrastructure & Operations Owner + Data Model Domain & Schema Owner + Backend Engineering Patterns Owner + Head of Specs Team + QA & Testing Owner
**Estimated effort:** ~14.5 hrs mid (core ~13 hrs; stretch +1.5 hrs)
**Risk IDs:** None
**Execution sequence:** 3 (parallel — begin early; run alongside EPIC-01/EPIC-02)

#### ST-16 — Database Migration Governance Standard

**Owner:** Backend Engineering Patterns Owner + Head of Engineering
**Estimated effort:** ~0.75 hrs mid
**Delegation class:** `delegated_decision`
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`
**Dependencies:** None
**Notes:** Should complete before ST-04 if any DB schema change is required. Head of Engineering sign-off required.

---

#### ST-14 — Production Deployment Runbook

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** ~0.75 hrs mid
**Delegation class:** `delegated_decision`
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`
**Dependencies:** None

---

#### ST-15 — Positions Table Data Dictionary

**Owner:** Data Model Domain & Schema Owner
**Estimated effort:** ~0.75 hrs mid
**Delegation class:** `delegated_decision`
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`
**Dependencies:** None

---

#### ST-17 — Spec Coverage Inventory

**Owner:** Head of Specs Team
**Estimated effort:** ~12 hrs mid
**Delegation class:** `delegated_decision`
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`
**Dependencies:** None
**Notes:** Large item (~1–2 days). Begin early; run in parallel with product EPICs.

---

#### ST-20 — CohortAnalysis backend integration regression scenario (stretch)

**Owner:** QA & Testing Owner
**Estimated effort:** ~1.5 hrs mid
**Delegation class:** `delegated_qa`
**Priority:** P3 — stretch
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`
**Dependencies:** None

---

### EPIC-02 — 4.1b Tax-Year P&L Statement

**Maps to:** S2-02
**Owner:** Head of Engineering + Base44 Frontend
**Estimated effort:** ~10 hrs mid (ST-04 + ST-05; ST-03 pre-completed)
**Risk IDs:** RISK-02 (resolved — ST-03 pre-completed)
**Execution sequence:** 4 (ST-04 after ST-16 recommended; ST-05 after ST-04 live on staging)

#### ST-04 — Implement GET /reports/tax-year endpoint

**Owner:** Head of Engineering
**Estimated effort:** ~6 hrs mid
**Delegation class:** `delegated_backend`
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`
**Dependencies:** ST-03 ✅ pre-completed; ST-16 recommended before (DB migration governance)
**Notes:** Spec: `docs/specs/api_contracts/reports_endpoints.md` v0.1. Integration tests in `tests/test_reports_integration.py`. Director of Quality staging verification required.

---

#### ST-05 — Frontend: tax-year P&L report view

**Owner:** Base44 Frontend
**Estimated effort:** ~4 hrs mid
**Delegation class:** `delegated_frontend`
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`
**Dependencies:** ST-04 (endpoint live on staging)
**Notes:** Spec: `docs/specs/frontend/pages/reports.md` v0.1. Year selector, summary bar, trades table, unrealised card, empty state, disclaimer banner.

---

### EPIC-06 — Governance Tooling *(Parallel Track)*

**Maps to:** S2-06
**Owner:** Head of Specs Team
**Estimated effort:** ~40 hrs mid
**Risk IDs:** RISK-05 (active — low priority; governance checklist mitigates)
**Execution sequence:** Parallel (not blocked by or blocking any product EPIC)
**Note:** EPIC-06 runs as a parallel governance track alongside the sprint. Changes take effect at the next `run roadmap` invocation after v2.0 ships. All CLAUDE.md §6 governance edit checklist requirements apply to ST-18 and ST-19.

#### ST-18 — Roadmap stage document consolidation (BLG-GOV-01)

**Owner:** Head of Specs Team
**Estimated effort:** ~20 hrs mid
**Delegation class:** `delegated_decision`
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`
**Dependencies:** None
**Notes:** Large governance rewrite. Validate against one `run roadmap` cycle before sealing. CLAUDE.md §6 checklist mandatory.

---

#### ST-19 — Ideas register (BLG-GOV-02)

**Owner:** Head of Specs Team
**Estimated effort:** ~20 hrs mid
**Delegation class:** `delegated_decision`
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`
**Dependencies:** None
**Notes:** Replace per-file idea submission model with ideas_register.md. Migration instruction required. CLAUDE.md §6 checklist mandatory.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~40 hrs |
| Total estimated effort — core (excl stretch, excl EPIC-06) | ~31 hrs mid |
| Total estimated effort — core + stretch (excl EPIC-06) | ~38 hrs mid |
| EPIC-06 (parallel track) | ~40 hrs mid (not counted against sprint capacity) |
| Utilisation (core) | ~77% |
| Utilisation (core + stretch) | ~95% |
| Over-allocation | No |
| Capacity WARN from release planning | ✅ Resolved — EPIC-03 deferral reduces scope below capacity threshold |

---

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-06 | EPIC-03 | EPIC-03 deferred to v2.1 — no async notification infrastructure |
| ST-07 | EPIC-03 | Same |
| ST-08 | EPIC-03 | Same |
| ST-09 | EPIC-03 | Same |
| ST-10 | EPIC-03 | Same |

---

## Deferred Execution Blockers Accepted

None. `deferred_execution_blockers` was empty in `state.json`. *(Section omitted — no items)*

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Install pip-audit and run pre-sprint scan before ST-04 backend work begins | Head of Engineering | No (advisory) |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Product Owner — confirmed (2026-03-17)
**Scope confirmed:** Product Owner — confirmed (2026-03-17)
**Capacity confirmed:** Product Owner — confirmed; capacity WARN from release planning acknowledged and resolved by EPIC-03 deferral (2026-03-17)
**Deferred execution blockers accepted:** N/A — none present
**Signed off by:** Product Owner
**Date:** 2026-03-17
