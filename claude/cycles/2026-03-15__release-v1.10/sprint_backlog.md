**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-03-15
**Cycle:** 2026-03-15__release-v1.10
**Release:** v1.10
**Sprint Goal:** Establish staging as the canonical pre-merge QA environment and close the CohortAnalysis architecture violation, backend integration test gap, and v1.7 QA scenario gaps that have been carried since v1.7–v1.9.
**Backlog Slice Source:** original — `claude/cycles/2026-03-15__release-v1.10/stage4_backlog_slice.md`

---

# Sprint Backlog — 2026-03-15__release-v1.10

## Sprint Scope

### EPIC-01 — Development Environment Foundation

**Maps to:** S2-01 (BLG-OPS-01)
**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 20 hrs mid (ST-01: 12 hrs, ST-02: 6 hrs, ST-03: 2 hrs)
**Risk IDs:** RISK-01 (staging environment scope ambiguity)
**Execution sequence:** 1 — must start first; P1 prerequisite (LL-01 mandate)

#### ST-01 — Provision staging environment infrastructure

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 12 hrs mid (1–2 days)
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Security:** N/A — no externally-facing security surface changed. Infrastructure provisioning; access control is inherited from the chosen hosting approach.

**Dependencies:** None

**Notes:** Pre-execution prerequisite — Infrastructure & Operations Owner must document the hosting approach decision (cloud service vs same-host isolation) before implementation begins. Constrain to simplest viable approach (RISK-01 mitigation). This is the P1 LL-01 item; it may not be deferred to a later sprint.

---

#### ST-02 — Configure CI/CD auto-deploy to staging

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 6 hrs mid (0.5–1 day)
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Security:** N/A — CI/CD pipeline scope-limited to staging; no production access path changed.

**Dependencies:** ST-01 (staging environment must exist before CI/CD can deploy to it)

**Notes:** None.

---

#### ST-03 — Update QA sign-off governance process

**Owner:** Director of Quality (governance update); PMO Lead (document authority)
**Estimated effort:** 2 hrs mid (0.25 day)
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Security:** N/A — governance documentation update; no code surface changed.

**Dependencies:** ST-01 + ST-02 (staging must be live and auto-deploying before governance references it)

**Notes:** This story closes the governance gap documented in LL-01 (cycle 2026-03-15__item-5.3). Update must reference the staging URL explicitly — do not reference a generic environment name.

---

### EPIC-02 — Analytics Architecture Correctness

**Maps to:** S2-02 (BLG-TECH-06)
**Owner:** Head of Engineering
**Estimated effort:** 6 hrs mid (ST-04: 6 hrs)
**Risk IDs:** RISK-02 (CohortAnalysis refactor regression)
**Execution sequence:** 2 — independent; can run in parallel with EPIC-01 or EPIC-03

#### ST-04 — Refactor CohortAnalysis.js to use backend endpoint

**Owner:** Head of Engineering
**Estimated effort:** 6 hrs mid (0.5–1 day)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Security:** N/A — client-side JS refactoring; no new data exposure or API surface created.

**Dependencies:** None

**Notes:** Locked spec reference: `docs/specs/frontend/pages/analytics.md` v1.4 (set by Design Gate). Regression check is mandatory — period toggle and cohort table output must match pre-refactor behaviour exactly. Director of Quality sign-off required before merge (RISK-02 mitigation).

---

### EPIC-03 — QA Infrastructure & Coverage

**Maps to:** S2-03 (BLG-API-01) + S2-04 (BLG-QA-01)
**Owner:** QA & Testing Owner
**Estimated effort:** 22 hrs mid (ST-05: 12 hrs, ST-06: 4 hrs, ST-07: 6 hrs)
**Risk IDs:** RISK-03 (integration test database dependency)
**Execution sequence:** 3 — independent start; ST-06 depends on ST-05; ST-07 recommended after ST-01

#### ST-05 — FastAPI TestClient integration tests for portfolio endpoints

**Owner:** QA & Testing Owner
**Estimated effort:** 12 hrs mid (1–2 days)
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Security:** N/A — test code only; no production code security surface changed.

**Dependencies:** None

**Notes:** Tests must be CI-safe (no live DB). Use dependency override or in-memory SQLite (RISK-03 mitigation). Tests must pass in isolation — no ordering dependencies.

---

#### ST-06 — Add integration test CI step

**Owner:** QA & Testing Owner
**Estimated effort:** 4 hrs mid (0.5 day)
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Security:** N/A — CI workflow extension; no application security surface changed.

**Dependencies:** ST-05 (integration tests must exist before CI step can run them)

**Notes:** None.

---

#### ST-07 — Author v1.7 missing QA test scenarios (BLG-QA-01)

**Owner:** QA & Testing Owner
**Estimated effort:** 6 hrs mid (0.5–1 day)
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Security:** N/A — test scenario authoring; no code or security surface changed.

**Dependencies:** ST-01 (advisory — staging recommended for scenario execution; authoring may proceed independently)

**Notes:** Resolves the TEST-GAP-EPIC-06 orphan item (3 cycles unassigned; promoted by STEP 1.1 advisory). BLG-QA-01 is the formal BLG-ID. The 3 gap scenarios from `verification_report.md §6` (cycle 2026-03-02__release-v1.7) must be addressed. Scenarios must be registered in the canonical test scenario library (BLG-NEW-10 / v1.9 Sprint 1).

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | Not confirmed (no --capacity specified) — WARN |
| Total estimated effort (in-scope) | 48 hrs mid (6.0 days) |
| Utilisation | Approximately 80–92% at full-time (1.5-week sprint) |
| Over-allocation | No — feasible at full-time; constrained at evenings-only. WARN acknowledged by Product Owner. |

## Items Deferred This Sprint

None. All 7 stories from `stage4_backlog_slice.md` are included in this sprint.

| Item | EPIC | Reason |
|------|------|--------|
| — | — | — |

## Deferred Execution Blockers Accepted

*(Section omitted — `deferred_execution_blockers` was empty in `state.json`.)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Infrastructure & Operations Owner documents staging hosting approach before ST-01 execution begins (RISK-01 / LL-01) | Infrastructure & Operations Owner | No (execution prerequisite, not seal prerequisite) |
| pip-audit: install and run before first sprint execution session | PMO Lead / Head of Engineering | No (advisory) |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** confirmed — "Establish staging as the canonical pre-merge QA environment and close the CohortAnalysis architecture violation, backend integration test gap, and v1.7 QA scenario gaps that have been carried since v1.7–v1.9."
**Scope confirmed:** confirmed — all 7 stories (ST-01 through ST-07) across EPIC-01, EPIC-02, EPIC-03
**Capacity confirmed:** confirmed — capacity WARN acknowledged; single-sprint scope accepted; phasing option available as mid-sprint fallback if capacity over-run materialises
**Deferred execution blockers accepted (if any):** N/A
**Signed off by:** Product Owner
**Date:** 2026-03-15
