**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-05-15
**Cycle:** 2026-05-15__release-v3.5
**Release:** v3.5
**Sprint Goal:** Complete Arc 3's Alpaca paper trading integration (§13 gate permitting) and establish Arc 4 foundations with the Plan vs Reality analysis service, while clearing all v3.4 spec, QA, and governance debt.
**Backlog Slice Source:** original stage4_backlog_slice.md

---

# Sprint Backlog — 2026-05-15__release-v3.5

---

## Sprint Scope

---

### Sprint 1

---

#### EPIC-04 — Governance Patches

**Maps to:** S2-04
**Owner:** Head of Specs Team
**Estimated effort:** ~1.5–2 days
**Risk IDs:** None
**Execution sequence:** 1 (first — governance patches before any execution EPIC)

---

##### ST-11 — BLG-GOV-22: sprint_planning_prompt.md Shared Ownership Patch

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`. Do not duplicate the full AC table here — the sprint backlog is a sequencing and ownership document.)*

**Dependencies:** None

**Notes:** Govenance patch from v3.4 LL carry-forward. Must include CLAUDE.md §6 co-updates (OPERATIONAL_GUIDE.md §14, prompt_change_log.md) in same commit.

---

##### ST-12 — execution_prompt.md: Deviation Filing Advisory Patches

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None (parallelisable with ST-11; best committed after ST-11 to avoid version conflicts on OPERATIONAL_GUIDE.md)

**Notes:** Three advisory improvements from v3.4 LL items #3–#5 carry-forward. Must include OPERATIONAL_GUIDE.md §14 update and prompt_change_log.md entry in same commit.

---

##### ST-13 — Sprint Close / LL Formatting Improvements

**Owner:** Head of Specs Team (ST-13a) + PMO Lead (ST-13b)
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None (best after ST-12 to avoid OPERATIONAL_GUIDE.md conflicts)

**Notes:** Two governance formatting improvements from v3.4 LL carry-forward items #6–#7. Must include prompt version bump and OPERATIONAL_GUIDE.md §14 update in same commit (whichever prompts are modified).

---

#### EPIC-03 — Spec & QA Debt

**Maps to:** S2-03
**Owner:** Head of Specs Team
**Estimated effort:** ~1.5–2 days
**Risk IDs:** None
**Execution sequence:** 2 (after EPIC-04; parallelisable with EPIC-01 ST-01)

---

##### ST-07 — BLG-SPEC-29: Correct grace-period-alert ux_spec.md sessionStorage

**Owner:** Head of UX & Design
**Estimated effort:** XS (~0.25 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** Design gate record notes actual file path is `docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md` — update the existing v3.3 artefact, not `docs/ux_specs/grace-period-alert/ux_spec.md`.

---

##### ST-08 — BLG-SPEC-30: Correct stop-management-workflow ux_spec.md HTTP verb

**Owner:** Head of UX & Design
**Estimated effort:** XS (~0.25 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** Design gate record notes actual file path is `docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md` — update the existing v3.3 artefact. Parallelisable with ST-07.

---

##### ST-09 — BLG-SPEC-31: React Query v5 onSuccess Codebase Scan

**Owner:** Head of Engineering
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Scan `src/` for `onSuccess` in `useQuery` calls. If none found, file closure note. If found, refactor + add test coverage.

---

##### ST-10 — BLG-QA-19: Research View Regression Test Protocol

**Owner:** QA Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** Requires QA Lead sign-off (AC-6). Delegation will be created at execution time. Protocol must cross-reference existing `tests/e2e/` test IDs as regression gate.

---

#### EPIC-01 (Sprint 1 portion) — Arc 3 Completion: §13 Review Gate

**Maps to:** S2-01 (partial — Sprint 1)
**Owner:** Head of Engineering
**Estimated effort (Sprint 1):** ~0.25 day
**Risk IDs:** RISK-01
**Execution sequence:** 3 (can run in parallel with EPIC-03)

---

##### ST-01 — §13 Compliance Review: Alpaca Paper Trading

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** XS (~0.25 day)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (must complete before Sprint 2 EPIC-01 ST-02/03 begin)

**Notes:** Hard gate for EPIC-01 implementation. Determination PASS/FAIL governs Sprint 2 scope. Determination document required at `docs/product/decisions/decisions--2026-05-15__release-v3.5--IT-06-section13-review.md`. If FAIL: ST-02 and ST-03 are removed from Sprint 2 scope; EPIC-02 absorbs freed capacity.

---

### Sprint 2

---

#### EPIC-01 (Sprint 2 portion) — Arc 3 Completion: IT-06 Implementation

**Maps to:** S2-01 (conditional)
**Owner:** Head of Engineering
**Estimated effort (Sprint 2, if §13 PASS):** ~4–5 days
**Risk IDs:** RISK-01
**Execution sequence:** 4 (first Sprint 2 EPIC; conditional on ST-01 PASS)
**Condition:** ST-01 must produce PASS determination before any story in this block begins.

---

##### ST-02 — IT-06 Backend: Alpaca Paper Trading Sync Service

**Owner:** Head of Engineering
**Estimated effort:** M (~2–3 days)
**Delegation class:** autonomous
**Prerequisite:** ST-01 PASS

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** ST-01 (§13 PASS determination required)

**Notes:** Conditional on ST-01 PASS. New endpoint `GET /portfolio/paper-positions` — must add to openapi.yaml, backend/routers/test.py, SystemStatus.js fallback count (+1), and SC-SS-01b in same commit (CLAUDE.md §2). §13 compliance note must appear in service file.

---

##### ST-03 — IT-06 Frontend: Paper Positions Display Panel

**Owner:** Head of Engineering
**Estimated effort:** M (~2 days)
**Delegation class:** delegated_frontend
**Prerequisite:** ST-02

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** ST-02 (backend endpoint required)

**Notes:** Conditional on ST-01 PASS. UX spec available at `docs/ux_specs/paper-trading/ux_spec.md` v1.0 (design gate artefact). Requires Playwright E2E test coverage (AC-7: panel visible with mock data; panel hidden when not configured).

**LL-v2.0-P4-2 note:** New UI panel introducing frontend-visible controls — `test_scenarios` must be set to `"pending — QA & Testing Owner to author before next sprint on this domain"` in execution_state.json if Playwright tests not authored at delivery time.

---

#### EPIC-02 — Arc 4 Foundation: Plan vs Reality Analysis

**Maps to:** S2-02
**Owner:** Head of Engineering
**Estimated effort:** ~6–8 days
**Risk IDs:** RISK-02, RISK-03
**Execution sequence:** 5 (last Sprint 2 EPIC — highest conflict risk)

---

##### ST-04 — BLG-GOV-21: Arc 4 Data Requirements Capture

**Owner:** Head of UX & Design + Product Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None (first story in EPIC-02; must precede ST-05)

**Notes:** Documentation-only deliverable. Product Owner + Head of UX & Design sign-off required (AC-5). Not a feature specification or implementation commitment.

---

##### ST-05 — PO-01 Backend: Plan vs Reality Calculation Service

**Owner:** Head of Engineering
**Estimated effort:** M–H (~3–4 days)
**Delegation class:** autonomous
**Prerequisite:** ST-04

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** ST-04 (data requirements capture)

**Notes:** New data model field `plan_vs_reality` (JSONB) on `trades` table. New endpoint `GET /trades/{id}/plan-vs-reality` — must add to openapi.yaml, backend/routers/test.py, SystemStatus.js fallback count (+1), and SC-SS-01b in same commit (CLAUDE.md §2). `docs/data_model.md` must be updated in same commit (AC-8).

---

##### ST-06 — PO-01 Frontend: Plan vs Reality Comparison View

**Owner:** Head of Engineering
**Estimated effort:** M (~2 days)
**Delegation class:** delegated_frontend
**Prerequisite:** ST-05

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** ST-05 (backend endpoint required)

**Notes:** Phaseable to v3.6 if Sprint 2 capacity exceeded after IT-06. UX spec at `docs/ux_specs/plan-vs-reality/ux_spec.md` v1.0 (design gate artefact). Playwright E2E test coverage required (AC-6). Trade history detail view component.

**LL-v2.0-P4-2 note:** New UI component — `test_scenarios` must be set in execution_state.json if Playwright tests not authored at delivery time.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~10–12 days |
| Total estimated effort — Scenario A (§13 PASS) | ~13–16 days |
| Total estimated effort — Scenario B (§13 FAIL) | ~9–11 days |
| Utilisation — Scenario A | ~108–160% (WARN) |
| Utilisation — Scenario B | ~75–110% (within range) |
| Over-allocation | Scenario A: Yes — ~2–4 days; Scenario B: None |
| PO acceptance | [AWAITING SIGN-OFF] |
| Primary release valves | (a) §13 FAIL eliminates EPIC-01 ST-02/03 (~4–5 days); (b) ST-06 deferral to v3.6 (~2 days) |

---

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-02, ST-03 (conditional) | EPIC-01 | §13 determination pending — included as conditional Sprint 2 items; removed from scope only if ST-01 yields FAIL |
| ST-06 (conditional) | EPIC-02 | Capacity valve — phaseable to v3.6 if Sprint 2 capacity exceeded after IT-06 |

---

## Deferred Execution Blockers Accepted

*(Section omitted — `deferred_execution_blockers` was empty in `state.json`)*

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Confirm or replace sprint goal | Product Owner | Yes |
| Acknowledge capacity WARN — Scenario A over-allocation | Product Owner | Yes |
| Accept conditional scope for EPIC-01 ST-02/03 (pending ST-01 §13 outcome) | Product Owner | Yes |
| §13 compliance determination (docs/product/decisions/decisions--2026-05-15__release-v3.5--IT-06-section13-review.md) | Strategy Rules & System Intent Owner (via ST-01 execution) | Conditional — blocks EPIC-01 ST-02/03 execution; does not block Sprint 1 or sprint sealing |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — Product Owner (2026-05-15)

**Capacity WARN acknowledged:** Confirmed — Product Owner accepts Scenario A over-allocation (~2–4 days) with release valves: (a) §13 FAIL removes EPIC-01 ST-02/03; (b) ST-06 deferral to v3.6 if capacity exceeded (2026-05-15)

**Conditional scope accepted (EPIC-01 ST-02/03 conditional on §13):** Confirmed — Product Owner accepts conditional Sprint 2 scope; ST-02/03 activate on §13 PASS, removed on §13 FAIL (2026-05-15)

**Date:** 2026-05-15
