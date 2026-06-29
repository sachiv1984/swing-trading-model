**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-06-29
**Cycle:** 2026-06-26__release-v6.3
**Release:** v6.3
**Sprint Goal:** Harden the v6.2 production system by closing P1 correctness and security gaps and establishing CI test coverage for nightly computation services (Sprint 1), then deliver the Strategy Benchmark page enabling live-to-backtest comparison alongside morning briefing progressive disclosure (Sprint 2).
**Backlog Slice Source:** original — `claude/cycles/2026-06-26__release-v6.3/stage4_backlog_slice.md`

---

# Sprint Backlog — 2026-06-26__release-v6.3

## Sprint Scope

### Merge Order

**Sprint 1 EPIC merge sequence:** EPIC-02 → EPIC-01

- EPIC-02 merges first (pure QA/spec; minimal shared file conflict)
- EPIC-01 merges second (rebase onto main after EPIC-02 merge to pick up any test.py changes before finalising EPIC-01 test.py edits)
- Both EPICs run as parallel branches during Sprint 1 execution

**Sprint 2 EPIC merge sequence:** EPIC-03 (single EPIC; starts after Sprint 1 fully merged)

**execution_state.json owner:** EPIC-01
- EPIC-01 branch initialises `execution_state.json` at Phase 3 STEP 0
- EPIC-02 branch must check for existence before initialising — if found, append EPIC-02 section rather than overwrite

**Shared files in Sprint 1:**

| File | EPIC-01 | EPIC-02 | Advisory |
|------|---------|---------|---------|
| `backend/routers/test.py` | Yes (ST-03 — 429 tests) | Yes (ST-07 CI simulation tests, ST-09 schema validation) | EPIC-02 merges first; EPIC-01 rebases before finalising |
| `docs/reference/openapi.yaml` | Yes (ST-03 rate limit docs) | No | EPIC-01 owns |
| `docs/specs/api_contracts/` | Yes (ST-03, ST-06) | No | EPIC-01 owns |

---

## Sprint 1

### EPIC-01 — Production Correctness & AI Security Hardening

**Maps to:** S2-01, S2-02, S2-03, S2-04, S2-05, S2-06
**Owner:** Head of Backend Engineering; Cybersecurity & Trust Lead
**Estimated effort:** 2.0d firm + 0.75d conditional = 2.75d
**Risk IDs:** RISK-02
**Execution sequence:** 1 (parallel with EPIC-02)
**Branch:** `exec/2026-06-26__release-v6.3/EPIC-01`

---

#### ST-01 — Fix AI journal summary on Trade History tab

**Owner:** Head of Backend Engineering
**Estimated effort:** 0.5 day
**Delegation class:** autonomous
**Sprint:** Sprint 1
**Status at sprint open: ready**
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`
**Dependencies:** None
**Staging-only ACs:** None — functional fix verifiable in CI (unit/integration tests against AI service)
**Notes:** Root cause unknown — investigate silent failure path in ai_service.py journal summarisation. May involve broken endpoint, failed Anthropic API call, missing key, or unhandled exception.

---

#### ST-02 — Fix R-multiple not displaying on Reflection page

**Owner:** Base44 Frontend Prompt Owner; Head of Backend Engineering
**Estimated effort:** 0.5 day
**Delegation class:** delegated_frontend
**Sprint:** Sprint 1
**Status at sprint open: ready**
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`
**Dependencies:** None
**Staging-only ACs:** AC-01, AC-02, AC-03 — observable UI rendering fix; numeric display of R-multiple on Reflection page requires Playwright E2E test or human staging sign-off. If staging sign-off deferred to post-merge, a backlog item must be filed before the PR opens (CLAUDE.md §2).
**Notes:** Root cause: either backend not computing/returning R-multiple field, or frontend not reading it. Investigate both layers. Delegated to Base44 Frontend Prompt Owner for UI rendering fix once root cause is confirmed.

---

#### ST-03 — AI endpoint per-endpoint rate limiting hardening

**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner; Backend Engineering Patterns Owner
**Estimated effort:** 0.5 day
**Delegation class:** autonomous
**Sprint:** Sprint 1
**Status at sprint open: ready**
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`
**Dependencies:** None
**Staging-only ACs:** None — rate limiting and 429 responses verifiable in CI; openapi.yaml documentation verified by CI OpenAPI drift detection gate
**Notes:** POST /ai/daily-briefing (~10 req/min/IP) and POST /ai/chat (~30 req/min/IP). Retry-After header required on all 429s. Must update backend/routers/test.py (429 scenario) and docs/reference/openapi.yaml + api_contracts in same commit per CLAUDE.md §2.

---

#### ST-04 — AI response injection risk assessment

**Owner:** Cybersecurity & Trust Lead; AI Compliance & Governance Officer
**Estimated effort:** 0.5 day
**Delegation class:** autonomous
**Sprint:** Sprint 1
**Status at sprint open: ready**
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`
**Dependencies:** None
**Staging-only ACs:** None — threat model document output; sign-off from named roles
**Notes:** Covers all external data inputs to POST /ai/daily-briefing and POST /ai/chat context assembly. Output: `docs/specs/security/ai_injection_risk_assessment.md`. Any open risks (classification: "open") must be filed as separate backlog items. Per RISK-02: remediation items target v6.4 unless P0 critical severity.

---

#### ST-05 — AI feature advisory disclaimer visibility assessment [CONDITIONAL]

**Owner:** AI Compliance & Governance Officer; Head of UX & Design
**Estimated effort:** 0.25 day
**Delegation class:** autonomous
**Sprint:** Sprint 1 (if capacity after ST-01 through ST-04)
**Status at sprint open: ready**
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`
**Dependencies:** None (independent assessment; can proceed concurrently with ST-03/ST-04)
**Staging-only ACs:** None — visual assessment with documented output; remediation items filed if gaps found
**Notes:** §13 disclaimer prominence check (font size, contrast, position, dismissal behaviour) for AI daily briefing and chat. Output: assessment document in `docs/product/decisions/` or `docs/specs/qa/`.

---

#### ST-06 — API contract review checklist for AI advisory endpoints [CONDITIONAL]

**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Estimated effort:** 0.5 day
**Delegation class:** autonomous
**Sprint:** Sprint 1 (if capacity after ST-01 through ST-04)
**Status at sprint open: ready**
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`
**Dependencies:** None (independent; can proceed concurrently)
**Staging-only ACs:** None — checklist document with retroactive application to v6.2 AI contracts
**Notes:** §13 boundary confirmation checklist. Output: `docs/specs/api_contracts/` (checklist document). Retroactive application to existing POST /ai/daily-briefing and POST /ai/chat contracts; gaps filed as remediation items if found.

---

### EPIC-02 — Test Infrastructure & Quality Coverage

**Maps to:** S2-07, S2-08, S2-09, S2-10
**Owner:** QA Lead; Director of Quality
**Estimated effort:** 1.5d firm + 1.0d conditional = 2.5d
**Risk IDs:** RISK-03 (indirect — contributes to overall capacity utilisation)
**Execution sequence:** 1 (parallel with EPIC-01)
**Branch:** `exec/2026-06-26__release-v6.3/EPIC-02`

---

#### ST-08 — Strategy signal regression test specification

**Owner:** QA & Testing Owner; Director of Quality
**Estimated effort:** 0.5 day
**Delegation class:** autonomous
**Sprint:** Sprint 1
**Status at sprint open: ready**
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`
**Dependencies:** None (but must be executed BEFORE ST-07 — spec defines test scenarios)
**Staging-only ACs:** None — specification document; no runtime execution required
**Notes:** Execute FIRST in EPIC-02 — ST-07 test implementation follows this spec. Output: `docs/specs/qa/strategy_signal_regression_spec.md`. Defines scenario coverage requirements, expected output formats/tolerances, and fixture maintenance procedure.

---

#### ST-07 — Nightly stop computation CI simulation tests

**Owner:** QA Lead; Backend Engineering Patterns Owner
**Estimated effort:** 1.0 day
**Delegation class:** autonomous
**Sprint:** Sprint 1
**Status at sprint open: ready**
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`
**Dependencies:** ST-08 (regression spec must exist before implementing tests)
**Staging-only ACs:** None — CI simulation tests with fixture datasets; runs in CI
**Notes:** Zero CI coverage gap from v6.2 for trailing stop, rebalance exit, and inv-vol sizing computations. Fixture datasets for known portfolio states required. All tests registered in CI to run on changes to trailing_stop_service.py, rebalance_service.py, position_sizing_service.py.

---

#### ST-09 — AI chat response schema validation tests [CONDITIONAL]

**Owner:** QA Lead; API Contracts & Documentation Owner
**Estimated effort:** 0.5 day
**Delegation class:** autonomous
**Sprint:** Sprint 1 (if capacity after ST-07 and ST-08)
**Status at sprint open: ready**
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`
**Dependencies:** None (independent; can run once ST-07/08 complete)
**Staging-only ACs:** None — schema validation tests against mock/stub responses in CI
**Notes:** POST /ai/chat advisory-only constraint validation and JSON schema conformance. Tests registered in `backend/routers/test.py` or equivalent CI entry point.

---

#### ST-10 — §13 boundary test suite for AI advisory endpoints [CONDITIONAL]

**Owner:** QA & Testing Owner; AI Compliance & Governance Officer
**Estimated effort:** 0.5 day
**Delegation class:** autonomous
**Sprint:** Sprint 1 (if capacity after ST-07 and ST-08)
**Status at sprint open: ready**
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`
**Dependencies:** None (independent; can run once ST-07/08 complete)
**Staging-only ACs:** None — specification document; no runtime execution required
**Notes:** §13 boundary test scenario document for POST /ai/daily-briefing, POST /ai/chat, and future AI endpoints. Template for future AI endpoint §13 assessment. Output: `docs/specs/qa/ai_s13_boundary_test_suite.md`.

---

## Sprint 2

### EPIC-03 — Strategy Benchmark & UX Enhancement

**Maps to:** S2-11, S2-12, S2-13, S2-14, S2-15
**Owner:** Product Owner; Head of Engineering
**Estimated effort:** 5.5d firm + 1.0d conditional = 6.5d
**Risk IDs:** RISK-01
**Execution sequence:** 2 (starts after Sprint 1 EPIC-01 and EPIC-02 merge to main)
**Branch:** `exec/2026-06-26__release-v6.3/EPIC-03`

---

#### ST-11 — Strategy Benchmark page: compare live trades against backtest

**Owner:** Product Owner
**Estimated effort:** 5.0 days
**Delegation class:** delegated_frontend
**Sprint:** Sprint 2
**Status at sprint open: ready**
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`
**Dependencies:** Internal sequencing — DB schema migration → API implementation → frontend. `import_backtest.py` can develop in parallel with API.
**Staging-only ACs:** AC-06 (POST /strategy/benchmark/import upsert with real CSV data requires production-like environment with actual backtest CSVs), AC-07 (`import_backtest.py` reading from `production_results/` requires production CSV files not available in CI)
**Notes:** Flagship feature. Three internal implementation phases:
1. DB schema: `backtest_trades` + `backtest_yearly_performance` migration tables
2. Backend API: POST /strategy/benchmark/import (upsert), GET /strategy/benchmark/summary, GET /strategy/benchmark/trades — all must be registered in backend/routers/test.py and docs/reference/openapi.yaml in same commit (CLAUDE.md §2)
3. Frontend: 3-panel page (Performance Parity stat cards + PnL bar chart, Yearly Breakdown table, Trade Log with toggle modes) + sticky filter bar (year/market)
4. `import_backtest.py` companion script (runs against production_results/ CSVs)
Exit reason badge language: Stop (red) / Risk-Off (amber) / Rebalance (teal) — consistent with existing Positions/Signals badge language. Per LL-v2.0-P4-2: test_scenarios for EPIC-03 set to pending at execution_state.json initialisation; QA & Testing Owner to author Playwright test scenarios before next sprint on this domain.

---

#### ST-12 — Morning briefing progressive disclosure

**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design
**Estimated effort:** 0.5 day
**Delegation class:** delegated_frontend
**Sprint:** Sprint 2
**Status at sprint open: ready**
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`
**Dependencies:** None (independent; can run in parallel with ST-11 phases)
**Staging-only ACs:** None — AC-05 explicitly specifies a Playwright test (expand all → collapse market context → reload → verify still collapsed); all ACs verifiable via Playwright or CI
**Notes:** AiDailyBriefing.js (v6.2). Three sections: market context, signals, chat prompt. localStorage persistence (versioned key). Default state: all sections expanded. AC-05 Playwright test is a required deliverable — must exist and pass.

---

#### ST-13 — Background scheduler health monitoring endpoint [CONDITIONAL]

**Owner:** Infrastructure & Operations Owner; Backend Engineering Patterns Owner
**Estimated effort:** 0.5 day
**Delegation class:** autonomous
**Sprint:** Sprint 2
**Status at sprint open: conditional — architecture review of v6.2 scheduler required before implementation begins**
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`
**Dependencies:** Architecture review of v6.2 background scheduler (available data fields, job tracking mechanism) must be documented (AC-01) before API implementation begins
**Staging-only ACs:** None — GET /health/scheduler verifiable in CI once endpoint is implemented
**Notes:** Architecture review (AC-01) is the gate for this story. Endpoint registered in `backend/routers/test.py` and `docs/reference/openapi.yaml` in same commit per CLAUDE.md §2.

---

#### ST-14 — Measure live latency for POST /ai/daily-briefing and POST /ai/chat [CONDITIONAL]

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.25 day
**Delegation class:** autonomous
**Sprint:** Sprint 2
**Status at sprint open: conditional — requires production deployment to be live for timing measurements**
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`
**Dependencies:** Production deployment of Sprint 2 EPIC-03 merge must be live
**Staging-only ACs:** AC-01 (minimum 5 authenticated warm requests against production), AC-02 (p50/p95 populated in api_performance_baseline.md), AC-03 (regression threshold documented) — all require production deployment. If deferred to post-merge staging, a backlog item must be filed before the PR opens (CLAUDE.md §2).
**Notes:** Execute at end of Sprint 2, after EPIC-03 merges to production. Populates `docs/operations/api_performance_baseline.md §22.3` per §19 methodology. Regression threshold = p95 > 2× measured p95 (§22.2 formula).

---

#### ST-15 — Render deployment rollback procedure documentation [CONDITIONAL]

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.25 day
**Delegation class:** autonomous
**Sprint:** Sprint 2
**Status at sprint open: ready**
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`
**Dependencies:** None (standalone documentation; no code dependencies)
**Staging-only ACs:** None — documentation output; no runtime verification required
**Notes:** Output: runbook in `docs/operations/`. Covers: rollback steps (Render dashboard navigation, prior deploy identification, rollback initiation, verification), rollback decision criteria, and verification steps post-rollback.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 days (2 sprints × 12–14 days/sprint) |
| Sprint 1 confirmed capacity | ~12–14 days |
| Sprint 2 confirmed capacity | ~12–14 days |
| Sprint 1 estimated effort | ~5.25 days (all items incl. conditional) |
| Sprint 2 estimated effort | ~6.5 days (all items incl. conditional) |
| Total estimated effort | ~11.75 days |
| Sprint 1 utilisation | ~38–44% |
| Sprint 2 utilisation | ~46–54% |
| Over-allocation | No (WARN acknowledged — within revised baseline) |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| — | — | No items deferred |

## Deferred Execution Blockers Accepted

*(No deferred execution blockers from release planning. This section is not applicable.)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| BLG-BE-39 and BLG-FE-79: update Provisional-Target `v6.2` → `v6.3` in backlog.md | Product Owner | No |
| ST-13: architecture review of v6.2 scheduler before implementation | Infrastructure & Operations Owner | No at seal; yes before ST-13 starts |
| Action FI-P3-01: Base44 prompt draft §6 strict mode advisory | Director of Quality | No |
| Action FI-P3-02: Frontend testing gate clarification | Head of Specs Team | No |
| Action FI-P4-01: CI/infra spec_references convention | Head of Specs Team | No |
| pip-audit scan before Sprint 1 execution | Head of Engineering | No — advisory |

No blockers outstanding at seal.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed *(via `plan sprint` invocation — standard mode, 2026-06-29)*
**Scope confirmed:** Confirmed — 15 stories (8 firm + 7 conditional) across Sprint 1 (EPIC-01 + EPIC-02) and Sprint 2 (EPIC-03)
**Capacity confirmed:** Confirmed — capacity WARN acknowledged; all items within revised 12–14 day per-sprint baseline
**Deferred execution blockers accepted:** N/A — no deferred execution blockers from release planning
**Signed off by:** Product Owner
**Date:** 2026-06-29
