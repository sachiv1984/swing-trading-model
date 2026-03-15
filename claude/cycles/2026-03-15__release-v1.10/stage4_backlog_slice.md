**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v1.10
**Cycle:** 2026-03-15__release-v1.10
**Last Updated:** 2026-03-15

---

# Backlog Slice — v1.10 Operations & Quality Foundation

**Cycle:** 2026-03-15__release-v1.10
**Release:** v1.10 — Operations & Quality Foundation
**Planned:** 2026-03-15
**Scope reference:** docs/product/scope/scope--2026-03-15__release-v1.10-operations-quality.md

---

## EPIC-01 — Development Environment Foundation

**Maps to:** S2-01 (BLG-OPS-01)
**Owner:** Infrastructure & Operations Owner
**Risk:** RISK-01 — staging environment scope ambiguity

Provision a staging/development environment that tracks `main`. Addresses the structural governance gap identified in LL-01 (cycle 2026-03-15__item-5.3): no non-production environment exists; all QA runs against production. This is a P1 prerequisite item — it must ship before or alongside Sprint 1; it may not be deferred to Sprint 2.

---

### ST-01 — Provision staging environment infrastructure

**Epic:** EPIC-01
**Priority:** P1

**Description:** Provision a stable staging/development environment that runs both frontend and backend with real or seeded data.

**Acceptance Criteria:**
- Staging environment accessible via a stable, consistent URL (≠ production URL)
- Frontend and backend both running in staging
- Environment uses real data or a documented seeded data set
- Environment is accessible to the Director of Quality for QA sign-off
- Infrastructure approach documented (cloud service choice, or same-host isolation method)

**Pre-conditions:**
- Infrastructure & Operations Owner decides the hosting approach (cloud service vs same-host isolation) before implementation begins. Decision is a Medium-priority risk (RISK-01); constrain to the simplest viable approach.

**Effort estimate:** Medium (1–2 days)
**Reviewer:** Director of Quality + PMO Lead

---

### ST-02 — Configure CI/CD auto-deploy to staging

**Epic:** EPIC-01
**Priority:** P1

**Description:** CI/CD pipeline deploys the application to staging automatically when `main` is updated.

**Acceptance Criteria:**
- On every merge to `main`, an automated deployment to staging triggers
- Deployment completes without manual intervention
- Deployment status visible (CI/CD dashboard or GitHub Actions output)
- Staging URL reflects latest `main` within a reasonable time after merge (< 15 mins)

**Dependencies:** ST-01 (staging environment must exist)
**Effort estimate:** Low–Medium (0.5–1 day)
**Reviewer:** Infrastructure & Operations Owner

---

### ST-03 — Update QA sign-off governance process

**Epic:** EPIC-01
**Priority:** P1

**Description:** Update the Director of Quality sign-off workflow to reference the staging URL rather than production. Closes the governance gap where "QA sign-off on live app" forced merging before testing.

**Acceptance Criteria:**
- Governance documentation updated: Director of Quality sign-off block references staging URL explicitly
- QA sign-off process no longer requires testing against production as the primary environment
- Updated reference in at least: OPERATIONAL_GUIDE.md QA section (or equivalent governance doc)
- Director of Quality confirms the updated process is workable

**Dependencies:** ST-01 + ST-02 (staging must be live and auto-deploying)
**Effort estimate:** Low (0.25 day)
**Reviewer:** Director of Quality

---

## EPIC-02 — Analytics Architecture Correctness

**Maps to:** S2-02 (BLG-TECH-06)
**Owner:** Head of Engineering
**Risk:** RISK-02 — CohortAnalysis refactor regression

Refactor `CohortAnalysis.js` to source all data from the canonical `GET /analytics/cohort` backend endpoint rather than computing cohort groupings client-side. Resolves the analytics.md §15 hard rule violation (DEV-EPIC02-ST03-01). This is a targeted architectural correction — no new functionality.

---

### ST-04 — Refactor CohortAnalysis.js to use backend endpoint

**Epic:** EPIC-02
**Priority:** P2

**Description:** Remove `buildCohorts()` client-side computation from `CohortAnalysis.js`; replace with `api.analytics.cohort(period)` via `useQuery`. Eliminates divergence risk if backend trade data shape changes.

**Acceptance Criteria:**
- `CohortAnalysis.js` sources all cohort values from `GET /analytics/cohort` endpoint
- `buildCohorts()` function removed from `CohortAnalysis.js`
- `filteredTrades` / `trades` prop dependency for computation removed
- Rendered cohort table output and period toggle behaviour match pre-refactor behaviour exactly (regression check)
- analytics.md §15 hard rule satisfied: no client-side R-multiple or cohort aggregation
- Director of Quality sign-off on regression verification

**Effort estimate:** Low–Medium (0.5–1 day)
**Reviewer:** Head of Engineering + Director of Quality (regression sign-off)

---

## EPIC-03 — QA Infrastructure & Coverage

**Maps to:** S2-03 (BLG-API-01) + S2-04 (BLG-QA-01 / TEST-GAP-EPIC-06)
**Owner:** QA & Testing Owner
**Risk:** RISK-03 — integration test database dependency

Implement FastAPI `TestClient` integration tests for the portfolio endpoints (BLG-API-01) and author the missing v1.7 QA test scenarios (BLG-QA-01). The Playwright mock layer (ST-11, v1.9) tests frontend rendering — this EPIC adds backend pipeline testing.

---

### ST-05 — FastAPI TestClient integration tests for portfolio endpoints

**Epic:** EPIC-03
**Priority:** P2

**Description:** Add `TestClient` integration tests for `GET /portfolio` and `GET /portfolio/prospective-heat`. Tests must be CI-safe (no live DB).

**Acceptance Criteria:**
- `TestClient` tests present in `tests/` for `GET /portfolio`:
  - Response shape matches `portfolio_endpoints.md` contract
  - GBP conversion applies for US positions (entry_price, current_stop in GBP)
  - Portfolio heat value produces correct output for known inputs
- `TestClient` tests present in `tests/` for `GET /portfolio/prospective-heat`:
  - Prospective heat calculation produces correct output for known inputs
  - Response shape matches `portfolio_endpoints.md` contract
- Tests are CI-safe: no live DB connections; use dependency override or in-memory SQLite
- All tests pass in isolation (no ordering dependencies)

**Effort estimate:** Medium (1–2 days)
**Reviewer:** Director of Quality

---

### ST-06 — Add integration test CI step

**Epic:** EPIC-03
**Priority:** P2

**Description:** Add a CI step that runs the FastAPI `TestClient` integration tests on every PR and push to `main`. Integrates with existing GitHub Actions workflows.

**Acceptance Criteria:**
- CI step runs ST-05 integration tests on every PR and push to `main`
- Integrated into a new workflow or extended `golden-outputs.yml`
- Build fails if any integration test fails
- CI run time visible in PR checks (step named clearly)
- Director of Quality confirms CI step present and passing on a test PR

**Dependencies:** ST-05 (tests must exist before CI step)
**Effort estimate:** Low (0.5 day)
**Reviewer:** Director of Quality

---

### ST-07 — Author v1.7 missing QA test scenarios (BLG-QA-01)

**Epic:** EPIC-03
**Priority:** P2

**Description:** Author the 3 missing test scenarios identified in verification_report.md §6 (cycle 2026-03-02__release-v1.7). Resolves the TEST-GAP-EPIC-06 orphan item and assigns it the BLG-ID BLG-QA-01.

**Background:** verification_report.md §6 (cycle 2026-03-02__release-v1.7) identified 3 test coverage gaps that were never addressed:
1. No scenario asserting `sharpe_ratio_trade_method` presence in `POST /validate/calculations` response (14 metrics total)
2. No scenario asserting `portfolio_endpoints.md` field alignment in `GET /portfolio`
3. No scenario asserting `holding_days` field in `GET /trades`

**Acceptance Criteria:**
- Test scenario document created or updated for the 3 gap scenarios
- Each scenario follows the canonical scenario format (scenario ID, preconditions, steps, expected result)
- Scenarios are executable against the staging environment (ST-01)
- Registered in the canonical test scenario library (created in BLG-NEW-10 / v1.9 Sprint 1)
- BLG-QA-01 assigned as the BLG-ID for this item; TEST-GAP-EPIC-06 orphan notice resolved in backlog

**Dependencies:** Staging environment (ST-01) recommended for execution, but authoring may proceed independently
**Effort estimate:** Low–Medium (0.5–1 day)
**Reviewer:** QA & Testing Owner + Director of Quality

---

## Story Summary

| ST-ID | Epic | Title | Priority | Effort (Mid) |
|-------|------|-------|----------|--------------|
| ST-01 | EPIC-01 | Provision staging environment infrastructure | P1 | 1.5 days |
| ST-02 | EPIC-01 | Configure CI/CD auto-deploy to staging | P1 | 0.75 days |
| ST-03 | EPIC-01 | Update QA sign-off governance process | P1 | 0.25 days |
| ST-04 | EPIC-02 | Refactor CohortAnalysis.js to use backend endpoint | P2 | 0.75 days |
| ST-05 | EPIC-03 | FastAPI TestClient integration tests for portfolio endpoints | P2 | 1.5 days |
| ST-06 | EPIC-03 | Add integration test CI step | P2 | 0.5 days |
| ST-07 | EPIC-03 | Author v1.7 missing QA test scenarios (BLG-QA-01) | P2 | 0.75 days |

**Total mid estimate:** 6.0 days / ~48 hours

**Total scope items:** 4 (S2-01 through S2-04)
**Total epics:** 3 (EPIC-01 through EPIC-03)
**Total stories:** 7 (ST-01 through ST-07)
