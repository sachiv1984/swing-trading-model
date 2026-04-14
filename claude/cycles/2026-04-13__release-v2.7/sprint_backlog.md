**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-04-14
**Cycle:** 2026-04-13__release-v2.7
**Release:** v2.7
**Sprint Goal:** Ship v2.7: eliminate connection pooling latency, harden governance process gates, resolve Playwright test infrastructure, deliver market correlation analysis and supplementary signal indicators, and close spec/governance documentation debt.
**Backlog Slice Source:** original — `claude/cycles/2026-04-13__release-v2.7/stage4_backlog_slice.md`

---

# Sprint Backlog — 2026-04-13__release-v2.7

---

## Sprint Scope

---

### EPIC-01 — Performance & Connection Infrastructure

**Maps to:** S2-01, S2-02
**Sprint:** Sprint 1
**Owner:** Head of Engineering + Infrastructure & Operations Owner
**Estimated effort:** ~0.75d
**Risk IDs:** RISK-01 (Supavisor compatibility)
**Execution sequence:** 1 (first — staging baseline for EPIC-04 performance verification)
**Branch:** `exec/2026-04-13__release-v2.7/EPIC-01`

#### ST-01 — Enable Supabase Supavisor connection pooling

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** ~0.25d (XS — env var change + test)
**Delegation class:** delegated_backend
**Dependencies:** None (prerequisite for ST-02)
**Notes:** Human action required — Infrastructure/Ops Owner must update `DATABASE_URL` on Render staging and production to Supavisor pooler connection string (port 6543, `?pgbouncer=true`). Engine cannot perform this action autonomously. ST-02 may not begin measurement phase until ST-01 staging verification is confirmed.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

---

#### ST-02 — Refactor get_portfolio_summary() to use a single DB connection

**Owner:** Head of Engineering
**Estimated effort:** ~0.5d (M)
**Delegation class:** autonomous
**Dependencies:** ST-01 (Supavisor must be enabled first for independent measurement)
**Notes:** Do not begin measurement phase until ST-01 is confirmed on staging.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

---

### EPIC-02 — Governance Process Hardening

**Maps to:** S2-03, S2-04, S2-05
**Sprint:** Sprint 1
**Owner:** Director of Quality + Head of Specs Team + Infrastructure & Operations Owner
**Estimated effort:** ~1d
**Risk IDs:** RISK-02 (DoQ sign-off criteria complexity)
**Execution sequence:** 2 (Sprint 1 — independent of EPIC-01)
**Branch:** `exec/2026-04-13__release-v2.7/EPIC-02`

#### ST-03 — Require QA evidence sign-off block to be complete before PR is raised

**Owner:** Head of Specs Team
**Estimated effort:** ~0.25d (XS)
**Delegation class:** autonomous
**Dependencies:** None
**Notes:** §6 governance file edit checklist (CLAUDE.md) applies — version bump, OPERATIONAL_GUIDE §14 update, and prompt_change_log.md entry required in same commit.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

---

#### ST-04 — Define formal autonomous DoQ sign-off class for code-review-only EPICs

**Owner:** Head of Specs Team (Director of Quality reviews qualifying criteria before merge)
**Estimated effort:** ~0.5d (S)
**Delegation class:** autonomous
**Dependencies:** None
**Notes:** Director of Quality must confirm qualifying criteria in QA evidence before merge (AC requirement). §6 checklist applies to both `execution_prompt.md` and `delivery_verification_prompt.md`.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

---

#### ST-05 — Extend governance_sync.yml to trigger on push to main

**Owner:** Head of Engineering
**Estimated effort:** ~0.25d (XS)
**Delegation class:** autonomous
**Dependencies:** None
**Notes:** Existing `--state open` filter prevents double-close. Verify workflow fires after merge test.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

---

### EPIC-03 — Test Infrastructure

**Maps to:** S2-06, S2-07
**Sprint:** Sprint 1
**Owner:** QA & Testing Owner + Infrastructure & Operations Owner
**Estimated effort:** ~1.75d
**Risk IDs:** RISK-03 (Playwright intercept root cause)
**Execution sequence:** 3 (Sprint 1 — independent of EPIC-01/02)
**Branch:** `exec/2026-04-13__release-v2.7/EPIC-03`

#### ST-06 — Fix Playwright page.route() intercepts not firing in local test environment

**Owner:** QA & Testing Owner
**Estimated effort:** ~0.75d (S)
**Delegation class:** autonomous
**Dependencies:** None (prerequisite for ST-07)
**Notes:** Investigate root causes in priority order (3 hypotheses defined in backlog slice). Fix must generalise to all 4 existing spec files. If root cause cannot be fixed, ST-07 is descoped and BLG-QA-12 re-deferred to v2.8.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

---

#### ST-07 — System Status Playwright spec

**Owner:** QA & Testing Owner
**Estimated effort:** ~1d (M)
**Delegation class:** autonomous
**Dependencies:** ST-06 (intercept fix must be in place and verified before this story begins)
**Notes:** Do not begin until ST-06 is complete and all 4 existing spec files verified with fix pattern. If ST-06 cannot generalise the fix: ST-07 is descoped; BLG-QA-12 re-deferred to v2.8.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

---

### EPIC-04 — Market Intelligence

**Maps to:** S2-08, S2-09
**Sprint:** Sprint 2
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Estimated effort:** ~3d
**Risk IDs:** RISK-04 (Yahoo Finance data availability)
**Execution sequence:** 4 (Sprint 2 — independent of Sprint 1)
**Branch:** `exec/2026-04-13__release-v2.7/EPIC-04`

#### ST-08 — Market Correlation Analysis

**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Estimated effort:** ~1.5d (M)
**Delegation class:** autonomous
**Dependencies:** None
**Notes:** `openapi.yaml` must be updated in the same commit as the new endpoint (CLAUDE.md hard requirement). Yahoo Finance graceful error handling required. §13 status: no review required (new analytical endpoint, display-only). Engineer note in QA evidence: if Yahoo Finance reliability becomes a problem, a formal data source review is required before further correlation-dependent features.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

---

#### ST-09 — Add supplementary indicator fields to signal generation

**Owner:** Head of Engineering
**Estimated effort:** ~1.5d (M)
**Delegation class:** autonomous
**Dependencies:** None (§13 COMPLIANT pre-existing — SRB-v1.7 Feature 3)
**Notes:** `openapi.yaml` updated in same commit. Strategy Rules owner sign-off in QA evidence confirming no scoring logic modified. Documented in QA evidence: future incorporation of fields into signal ranking requires new §13 review and strategy_rules.md bump.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

---

### EPIC-05 — Spec & Governance Documentation

**Maps to:** S2-10, S2-11
**Sprint:** Sprint 2
**Owner:** Head of Specs Team + PMO Lead + Director of Quality
**Estimated effort:** ~3d
**Risk IDs:** RISK-05 (SPEC-D17 scope coverage)
**Execution sequence:** 5 (Sprint 2 — independent of Sprint 1 and EPIC-04)
**Branch:** `exec/2026-04-13__release-v2.7/EPIC-05`

#### ST-10 — Spec Dependency Map

**Owner:** Head of Specs Team
**Estimated effort:** ~1.5d (M)
**Delegation class:** autonomous
**Dependencies:** None
**Notes:** Explicit staleness acknowledgement header required in the document. Head of Specs Team sign-off on completeness in QA evidence.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

---

#### ST-11 — Governance Health Score

**Owner:** Head of Specs Team + PMO Lead
**Estimated effort:** ~1.5d (M)
**Delegation class:** autonomous
**Dependencies:** None
**Notes:** Score labelled advisory — cannot halt or gate any routine. Head of Specs Team sign-off on formula definition in QA evidence. §6 checklist applies to any prompt files modified.

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~20d (2 sprints) |
| Total estimated effort (in-scope) | ~9.5d (conservative) / ~12d (mid-point) |
| Utilisation | ~48–60% |
| Over-allocation | No |

---

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| — | — | No deferrals — all 11 items included in sprint scope |

---

## Deferred Execution Blockers Accepted

*(Section omitted — `deferred_execution_blockers` was confirmed empty in state.json at STEP -1.2)*

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| RISK-03: QA & Testing Owner to formally confirm ST-06 investigation approach and ST-07 descope criteria at sprint start. Content already ratified in `stage4_backlog_slice.md#ST-06`. | QA & Testing Owner | No |
| Upgrade pytest 9.0.2 → 9.0.3 (CVE-2025-71176, medium severity, local DoS in test env). | Head of Engineering | No |
| EPIC-04 test_scenarios: QA & Testing Owner to author test scenarios for ST-08 Analytics page display before Sprint 2 execution begins. | QA & Testing Owner | No |

No outstanding actions are marked `Blocker? Yes`. Sprint seal gate: PASS.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — sourced from Phase 1B `cycle_summary.md` (2026-04-13); no replacement requested.
**Scope confirmed:** Confirmed — 11 stories across 5 EPICs, 2 sprints; capacity PASS; no deferrals.
**Capacity confirmed:** Confirmed — ~9.5–12d estimated effort within ~20d confirmed capacity; utilisation ~48–60%; no over-allocation.
**Deferred execution blockers accepted (if any):** N/A — no deferred execution blockers.
**Signed off by:** Product Owner
**Date:** 2026-04-14
