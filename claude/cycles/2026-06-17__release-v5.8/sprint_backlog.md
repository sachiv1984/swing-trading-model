**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-06-17
**Cycle:** 2026-06-17__release-v5.8

---

# Sprint Backlog — v5.8

**Theme:** RFJ UX Design Completion, SI-05 Effectiveness Review & Production Hardening

---

## Sprint Scope

**Sprint 1 — EPIC-01 (Firm)**
4 firm stories: ST-01 (RFJ design review pre-brief), ST-02 (RFJ visual design review), ST-03 (FRONTEND_URL production env var), ST-04 (Governance complexity assessment)

**Sprint 2 — EPIC-02 (Conditional)**
3 conditional stories: ST-05, ST-06, ST-07 — gated on 2026-07-04 (BLG-GOV-113 complete). If gate not cleared by 2026-07-04, return all 3 to backlog and close Sprint 2 as gate-deferred.

---

## Merge Order

- Sprint 1: EPIC-01 (single PR — no multi-EPIC conflict)
- Sprint 2: EPIC-02 (single PR — conditional on 2026-07-04 gate)

`execution_state.json` owner: EPIC-01 (Sprint 1 initiates)

---

## Sprint 1 — EPIC-01: RFJ UX Design, Production Ops & Governance Assessment

**Branch:** `exec/2026-06-17__release-v5.8/EPIC-01`
**Owner:** Head of UX & Design; PMO Lead; Infrastructure & Operations Owner
**Effort:** ~3.75–4.75 days

---

### ST-03 — FRONTEND_URL Production Env Var Configuration

**Source:** v5.7 post-ship OA (Infrastructure & Operations Owner)
**Priority:** P1
**Effort:** XS (~0.25 day)
**Delegation class:** `delegated_backend`
**Status at sprint open: ready**
**Spec reference:** `stage4_backlog_slice.md#ST-03`
**Staging-only ACs:** AC-04

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-03`
- AC-01: FRONTEND_URL set on production backend (Render dashboard: trading-assistant-api-c0f9.onrender.com)
- AC-02: Deployment runbook or ops notes updated
- AC-03: Infrastructure & Operations Owner sign-off
- AC-04: `[staging-only evidence]` Deep links confirmed working in next SI-05 digest delivery post-deploy

**DoQ verification:** Infrastructure & Operations Owner sign-off + env var confirmation.

**Backlog obligation (AC-04 staging-only):** If AC-04 sign-off cannot be obtained before PR opens, file a backlog item before the PR opens (per CLAUDE.md §2).

---

### ST-04 — Governance Model Complexity Assessment

**Source:** BLG-GOV-101
**Priority:** P2
**Effort:** M (~2 days)
**Delegation class:** `delegated_decision`
**Status at sprint open: ready**
**Spec reference:** `stage4_backlog_slice.md#ST-04`
**Staging-only ACs:** None

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-04`
- AC-01: Complexity assessment report produced covering all 6 governance phase engines
- AC-02: Per-engine step count and complexity indicators documented
- AC-03: Hypothesis test outcome stated
- AC-04: If complexity IS a factor: simplification candidates enumerated and filed as backlog items
- AC-05: Director of HR, PMO Lead, and Head of Specs Team sign-off

**DoQ verification:** Sign-off from Director of HR, PMO Lead, and Head of Specs Team. Assessment document filed.

---

### ST-01 — RFJ Design Review Pre-Brief

**Source:** BLG-FE-64
**Priority:** P2
**Effort:** XS (~0.5 day)
**Delegation class:** `delegated_decision`
**Status at sprint open: conditional — gate 2026-06-21**
**Spec reference:** `stage4_backlog_slice.md#ST-01`
**Staging-only ACs:** None
**Depends on:** Gate 2026-06-21 (ST-02 depends on ST-01 completing within sprint)

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-01`
- AC-01: Design review brief document produced (Markdown, filed in docs/product/ux/ or equivalent)
- AC-02: Brief covers scope definition, evaluation criteria, deliverable format
- AC-03: Head of UX & Design sign-off on brief scope recorded
- AC-04: Brief completed ≥ gate date 2026-06-21

**DoQ verification:** Head of UX & Design sign-off on brief. No staging or Playwright required (documentation deliverable).

---

### ST-02 — Red Flag Journal Visual Design Review

**Source:** BLG-FE-41
**Priority:** P3
**Effort:** M (~1–2 days design + spec)
**Delegation class:** `delegated_decision`
**Status at sprint open: conditional — gate 2026-06-21**
**Spec reference:** `stage4_backlog_slice.md#ST-02`
**Staging-only ACs:** None
**Depends on:** ST-01 (pre-brief must be signed off before ST-02 begins)

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-02`
- AC-01: Design recommendation document produced
- AC-02: Rationale covers severity hierarchy, event type colour coding, timeline vs list layout
- AC-03: If redesign recommended: UX spec produced and implementation backlog item filed
- AC-04: Head of UX & Design sign-off recorded
- AC-05: Completed after gate date 2026-06-21

**DoQ verification:** Head of UX & Design sign-off on recommendation. No staging or Playwright required (design review deliverable).

---

## Sprint 1 Sign-Off

**Head of Specs Team:** Acceptance criteria confirmed for all Sprint 1 items — technical criteria are testable/observable, quality criteria name specific deliverables, security criteria explicitly waived (no security surface changed), verification criteria sufficient for DoQ sign-off.

**Director of Quality:** QA criteria sufficient for qa_evidence_EPIC-01.md. No test coverage gaps that would block sign-off. All items are documentation/ops/governance deliverables — no CI test automation required; human sign-off is the verification mechanism for all items.

**Product Owner:** Sprint goal confirmed. Sprint 1 scope accepted. Capacity WARN not applicable (PASS). All deferred execution blockers: none.

Product Owner: Confirmed — Sprint 1 scope sealed.
Date: 2026-06-17

---

## Sprint 2 — EPIC-02: SI-05 Effectiveness Review (Conditional)

**Branch:** `exec/2026-06-17__release-v5.8/EPIC-02`
**Owner:** Product Owner; Infrastructure & Operations Owner; Metrics Definitions & Analytics Owner
**Effort:** ~1.5–2 days
**Gate:** 2026-07-04 — BLG-GOV-113 (SI-05 Phase 1 first effectiveness review) must be complete

> **Gate check required at Sprint 2 opening (2026-07-04):** Before executing any Sprint 2 story, confirm BLG-GOV-113 is complete and ≥4 weeks of POST /digest/si05/send production operation have elapsed. If gate not cleared: return ST-05, ST-06, ST-07 to backlog and record Sprint 2 as gate-deferred.

---

### ST-05 — SI-05 Digest Weekly Cadence Review

**Source:** BLG-GOV-112
**Priority:** P2
**Effort:** S (~0.5 day)
**Delegation class:** `delegated_decision`
**Status at sprint open: conditional — gate 2026-07-04**
**Spec reference:** `stage4_backlog_slice.md#ST-05`
**Staging-only ACs:** None

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-05`
- AC-01: Cadence review document produced after 2026-07-04 effectiveness review
- AC-02: Review covers delivery count, action signals, user feedback
- AC-03: Recommendation made with data backing
- AC-04: Product Owner sign-off
- AC-05: Gate condition verified: BLG-GOV-113 complete

**DoQ verification:** Product Owner sign-off. Cadence recommendation document filed.

---

### ST-06 — SI-05 Digest Actionability Metric Definition

**Source:** BLG-GOV-115
**Priority:** P2
**Effort:** S (~0.5–1 day)
**Delegation class:** `delegated_decision`
**Status at sprint open: conditional — gate 2026-07-04**
**Spec reference:** `stage4_backlog_slice.md#ST-06`
**Staging-only ACs:** None

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-06`
- AC-01: 2–4 actionability metrics formally defined with data source mapping
- AC-02: Metrics document reviewed and signed off by Metrics Definitions & Analytics Owner
- AC-03: Each metric specifies: name, definition, data source query, expected range
- AC-04: Gate condition verified: BLG-GOV-113 complete
- AC-05: Metrics added to metrics_definitions.md

**DoQ verification:** Metrics Definitions & Analytics Owner sign-off. Metrics document filed.

---

### ST-07 — SI-05 Service Production p99 Latency Baseline Review

**Source:** BLG-OPS-59
**Priority:** P2
**Effort:** S (~0.5 day)
**Delegation class:** `delegated_backend`
**Status at sprint open: conditional — gate 2026-07-04**
**Spec reference:** `stage4_backlog_slice.md#ST-07`
**Staging-only ACs:** None

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-07`
- AC-01: Post-4-week p99 latency extracted from Render logs and documented
- AC-02: Comparison against BLG-OPS-54 pre-launch baseline made
- AC-03: Performance PASS determination recorded OR investigation item filed
- AC-04: Infrastructure & Operations Owner sign-off recorded
- AC-05: Gate condition verified: ≥2026-07-04

**DoQ verification:** Infrastructure & Operations Owner sign-off. Performance review note filed.

---

## Sprint 2 Sign-Off

**Head of Specs Team:** Acceptance criteria confirmed for all Sprint 2 items — criteria are testable/observable, security criteria explicitly waived (no security surface changed), verification criteria sufficient.

**Director of Quality:** QA criteria sufficient for qa_evidence_EPIC-02.md pending gate clearance. No test coverage gaps identified for Sprint 2 items.

**Product Owner:** Sprint 2 scope accepted as conditional. Gate check required at 2026-07-04 before execution begins.

Product Owner: Confirmed — Sprint 2 conditional scope sealed; gate check required at 2026-07-04.
Date: 2026-06-17
