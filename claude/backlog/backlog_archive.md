**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-24

# Backlog Archive — Momentum Trading Assistant

Permanent record of completed and killed backlog items retired from `claude/backlog/backlog.md`. Listed in retirement order, most recent first. Append-only — do not edit existing entries.

---

### v2.2 Release Slice — 2026-03-21__release-v2.2

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-24
**Shipped in:** v2.2 — Security, Alert Maturity & Quality
**Evidence:** All 15 items shipped; `claude/cycles/2026-03-21__release-v2.2/closure_record.md`

<!-- release-plan-marker: RP:v2.2:2026-03-21__release-v2.2 -->

**Cycle:** 2026-03-21__release-v2.2
**Release:** v2.2 — Security, Alert Maturity & Quality
**Planned:** 2026-03-21
**Shipped:** 2026-03-24
**Verification:** Verified_with_deviations
**Backlog slice:** `claude/cycles/2026-03-21__release-v2.2/stage4_backlog_slice.md`

Items in v2.2 sprint: EPIC-01 (ST-01 BLG-SEC-01, ST-02 BLG-SEC-02), EPIC-02 (ST-03 BLG-OPS-04, ST-04 BLG-FEAT-10, ST-05 BLG-FEAT-12), EPIC-03 (ST-06 BLG-BE-03, ST-07 BLG-FE-01, ST-08 BLG-OPS-06), EPIC-04 (ST-09 TEST-GAP-EPIC-02, ST-10 TEST-GAP-EPIC-03, ST-11 BLG-QA-02, ST-12 BLG-SPEC-T01), EPIC-05 (ST-13 BLG-GOV-04, ST-14 BLG-GOV-05, ST-15 BLG-GOV-06)

Full item definitions: in `claude/cycles/2026-03-21__release-v2.2/stage4_backlog_slice.md` and in `backlog.md` body (tombstoned in place per groom backlog 2026-03-24).

---

### v1.10 Release Slice — 2026-03-15__release-v1.10

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-16
**Shipped in:** v1.10 — Operations & Quality Foundation
**Evidence:** All EPICs shipped 2026-03-16; `claude/cycles/2026-03-15__release-v1.10/closure_record.md`

<!-- release-plan-marker: RP:v1.10:2026-03-15__release-v1.10 -->

**Cycle:** 2026-03-15__release-v1.10
**Release:** v1.10 — Operations & Quality Foundation
**Planned:** 2026-03-15
**Backlog slice:** `claude/cycles/2026-03-15__release-v1.10/stage4_backlog_slice.md`

Items in v1.10 sprint: EPIC-01 (ST-01–ST-03), EPIC-02 (ST-04), EPIC-03 (ST-05–ST-07)

---

### BLG-OPS-01 — Provision development environment

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-16
**Shipped in:** v1.10 — Operations & Quality Foundation
**Evidence:** `claude/cycles/2026-03-15__release-v1.10/verification_report.md`; EPIC-01/ST-01–ST-03

### BLG-OPS-01 — Provision development environment
**Status:** ✅ COMPLETE — 2026-03-16 (cycle 2026-03-15__release-v1.10 / EPIC-01 ST-01–ST-03)
**Priority:** P1 (High — blocks safe QA workflow)
**Type:** Operations / Infrastructure
**Origin:** v1.9 Sprint 2 post-merge QA — raised 2026-03-13
**Target release:** v1.10 (prerequisite before Sprint 1 begins)

The project has no development environment. All QA must currently be performed against the production (`main`) deployment, which means:
- Bug fixes cannot be tested before they land in production
- The merge gate condition "QA sign-off on live app" forces merging to main before a human can test
- Post-merge bug discovery (as occurred in v1.9 Sprint 2) is the only available feedback loop

This creates a structural governance gap: the human Director of Quality sign-off rule requires testing a live running application, but there is no non-production environment to test against.

**Scope**
- Provision a staging/dev environment that tracks `main` (or a designated `staging` branch)
- Environment must run both frontend and backend with real (or seeded) data
- CI/CD pipeline should deploy to staging automatically on merge to `main`
- QA sign-off process updated to use staging URL, not production

**Acceptance Criteria**
- Staging environment accessible via a stable URL
- Deploys automatically when `main` is updated
- Governance process updated: QA sign-off block references staging URL
- Production is not the first place bugs are discovered

---

### BLG-TECH-06 — Fix CohortAnalysis client-side computation

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-16
**Shipped in:** v1.10 — Operations & Quality Foundation
**Evidence:** `claude/cycles/2026-03-15__release-v1.10/verification_report.md`; EPIC-02/ST-04

### BLG-TECH-06 — Fix CohortAnalysis client-side computation (DEV-EPIC02-ST03-01)
**Status:** ✅ COMPLETE — 2026-03-16 (cycle 2026-03-15__release-v1.10 / EPIC-02 ST-04)
**Priority:** P2 (Medium — regression risk)
**Type:** Technical debt / Architecture
**Origin:** DEV-EPIC02-ST03-01 filed in analytics.md v1.4 during v1.9 QA
**Target release:** v1.10

`CohortAnalysis.js` computes cohort groupings and `avg_r` client-side via `buildCohorts()` from a `filteredTrades` prop, instead of calling the canonical `GET /analytics/cohort` endpoint that was implemented in EPIC-02/ST-03. This violates the analytics.md §15 hard rule: all values sourced from backend.

Numerical output is currently correct (same formula), but divergence risk exists if trade data shape changes server-side.

**Scope**
- Refactor `CohortAnalysis.js` to call `api.analytics.cohort(period)` via `useQuery`
- Remove `buildCohorts()` client-side computation logic
- Remove `trades`/`filteredTrades` prop dependency for computation
- Verify rendered output matches backend response field names

**Acceptance Criteria**
- `CohortAnalysis.js` sources all values from `GET /analytics/cohort`
- No client-side R-multiple or cohort aggregation computation
- analytics.md §15 hard rule fully satisfied
- Regression: existing period toggle and table display unchanged

---

### BLG-API-01 — Backend API integration tests (FastAPI TestClient)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-16
**Shipped in:** v1.10 — Operations & Quality Foundation
**Evidence:** `claude/cycles/2026-03-15__release-v1.10/verification_report.md`; EPIC-03/ST-05–ST-06; P3 deviation DEV-ST05-01 (BLG-BE-02 filed)

### BLG-API-01 — Backend API integration tests (FastAPI TestClient)
**Status:** ✅ COMPLETE — 2026-03-16 (cycle 2026-03-15__release-v1.10 / EPIC-03 ST-05–ST-06; P3 deviation DEV-ST05-01 for prospective-heat — BLG-BE-02 filed)
**Priority:** P2
**Type:** QA Infrastructure
**Owner:** QA & Testing Owner
**Source:** ST-11 decision session 2026-03-09 — Head of Engineering and Director of Quality identified gap
**Cycle added:** 2026-03-06__release-v1.9
**Target release:** v1.10

**Problem**
The Playwright mock layer (ST-11) tests frontend rendering behaviour given known API payloads. It does not test whether the backend `GET /portfolio` and `GET /portfolio/prospective-heat` routers return correctly-shaped responses for real database rows. The golden output gate tests pure-math functions; it does not test the router-to-service pipeline end-to-end.

**Scope**
- Add FastAPI `TestClient` integration tests for `GET /portfolio` and `GET /portfolio/prospective-heat` endpoints
- Use fixture data (no live DB required — inject via dependency override or in-memory SQLite)
- Verify: response shape matches `portfolio_endpoints.md` contract, GBP conversion applies for US positions, heat formula produces correct output for known inputs
- Add as a CI step in a new workflow or extend `golden-outputs.yml`

**Acceptance Criteria**
- `TestClient` tests present in `tests/` covering at minimum: portfolio endpoint response shape, US position GBP conversion, heat formula output, prospective-heat endpoint calculation
- Tests are CI-safe (no live DB, no external calls)
- Director of Quality confirms CI step present and passing

**Last Updated:** 2026-03-09

---

### TEST-GAP-EPIC-06 — v1.7 test scenario coverage gap (BLG-QA-01)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-16
**Shipped in:** v1.10 — Operations & Quality Foundation
**Evidence:** `claude/cycles/2026-03-15__release-v1.10/verification_report.md`; EPIC-03/ST-07

✅ COMPLETE — [TEST-GAP-EPIC-06] — 2026-03-16 (cycle 2026-03-15__release-v1.10 / EPIC-03 ST-07 / BLG-QA-01): 4 v1.7 QA scenario gaps authored and executed as GAP-01–GAP-04 in `docs/testing/v1.7-qa-scenario-gaps.md`. GAP-01 PASS, GAP-02 PASS, GAP-03 FAIL (new finding BLG-BE-01 P1 filed), GAP-04 BLOCKED (no closed trades in staging — deferred). BLG-QA-01 closed. Item retired.

---

### v1.9 Release Slice — 2026-03-06__release-v1.9

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-15
**Shipped in:** v1.9 — User Value & Insight
**Evidence:** Sprint 1 shipped 2026-03-09; Sprint 2 shipped 2026-03-13; `claude/cycles/2026-03-06__release-v1.9/verification_report.md`

<!-- release-plan-marker: RP:v1.9:2026-03-06__release-v1.9 -->

**Cycle:** 2026-03-06__release-v1.9
**Release:** v1.9 — User Value & Insight
**Planned:** 2026-03-06
**Backlog slice:** `claude/cycles/2026-03-06__release-v1.9/stage4_backlog_slice.md`

**Sprint 1 (✅ SHIPPED 2026-03-09):** EPIC-04 (ST-06–ST-10), EPIC-05 partial (ST-11, ST-13), EPIC-06 (ST-14–ST-19)
**Sprint 2 (✅ SHIPPED 2026-03-13):** EPIC-01 (ST-01–ST-02), EPIC-02 (ST-03, ST-05), EPIC-03 (ST-04), EPIC-05 partial (ST-12)

---

### v1.8 Release Slice — 2026-03-04__release-v1.8

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-15
**Shipped in:** v1.8 — Risk Dashboard
**Evidence:** All EPICs shipped 2026-03-05; `claude/cycles/2026-03-04__release-v1.8/closure_record.md`

<!-- release-plan-marker: RP:v1.8:2026-03-04__release-v1.8 -->

**Cycle:** 2026-03-04__release-v1.8
**Release:** v1.8 — Risk Dashboard
**Planned:** 2026-03-04
**Backlog slice:** `claude/cycles/2026-03-04__release-v1.8/stage4_backlog_slice.md`

Items in v1.8 sprint: EPIC-01 (ST-01–ST-04), EPIC-02 (ST-05–ST-08), EPIC-03 (ST-09–ST-10), EPIC-04 (ST-11–ST-12)

---

### BLG-FEAT-08 — Basic Compliance Metrics

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 2
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-03/ST-01

### BLG-FEAT-08 — Basic Compliance Metrics ✅ COMPLETE
**Priority:** P2
**Effort:** ~1 day
**Target release:** v1.9 (pre-work gate for Structured Trade Reflection Template)
**Closed:** 2026-03-13 | Cycle: 2026-03-06__release-v1.9 | EPIC-03/ST-01

Lightweight discipline metrics: journal completion rate, stop-based exit rate, average position size (% of portfolio). Definitions canonicalised in `metrics_definitions.md` first.

---

### BLG-NEW-09 — R-Multiple Distribution Report

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 2
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-02/ST-04

### BLG-NEW-09 — R-Multiple Distribution Report ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Analytics / User Value
**Owner:** Metrics Definitions & Analytics Owner
**Source:** IDEA-metrics-analytics-20260304-01, IW-20260304-01
**Cycle added:** 2026-03-06__item-3.4
**Closed:** 2026-03-13 | Cycle: 2026-03-06__release-v1.9 | EPIC-02/ST-04

**Problem**
No visualisation of R-multiple distribution existed. R-multiple is the canonical trade quality measure — users could not see whether trades were systematically achieving R > 1.

**Acceptance Criteria met**
- R-multiple formula defined and canonicalised in metrics_definitions.md
- Distribution visualisation present on analytics page
- Values computed from canonical backend formula; no client-side derivation

---

### BLG-NEW-10 — Canonical Test Scenario Library

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-15
**Shipped in:** v1.9 (Phase 1: Sprint 1; Phase 2: Sprint 2)
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-05/ST-11 (Phase 1), EPIC-05/ST-12 (Phase 2)

### BLG-NEW-10 — Canonical Test Scenario Library ✅ COMPLETE
**Priority:** P1 (High)
**Type:** QA Infrastructure
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260304-01, IW-20260304-01
**Cycle added:** 2026-03-06__item-3.4
**Closed:** Phase 1: 2026-03-09 | Phase 2: 2026-03-13 | Cycle: 2026-03-06__release-v1.9

Both phases delivered: seeded test infrastructure + TEST-GAP-EPIC-01 resolution (Phase 1); v1.9 feature scenarios added at delivery (Phase 2).

---

### BLG-NEW-11 — Canonical Terms Glossary

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06/ST-14

### BLG-NEW-11 — Canonical Terms Glossary ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Governance / Spec Quality
**Owner:** Head of Specs Team
**Cycle added:** 2026-03-06__item-3.4
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-14

Canonical terms glossary created as Class 2 Supporting document. All key trading and system terms defined with canonical source links. Registered in Specs_Index.md.

---

### BLG-NEW-12 — Service Layer Test Coverage Standard

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-05/ST-13

### BLG-NEW-12 — Service Layer Test Coverage Standard ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Engineering Quality / CI
**Owner:** Backend Engineering Patterns Owner
**Cycle added:** 2026-03-06__item-3.4
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-05/ST-13

Service Layer Test Coverage Standard authored. CI step enforces coverage threshold on services/ directory. Standard integrated with backend_engineering_patterns.md.

---

### BLG-NEW-04 — AI-Assisted Workflow Governance Policy

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06/ST-15

### BLG-NEW-04 — AI-Assisted Workflow Governance Policy ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Governance
**Owner:** Product Owner
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-15

AI-Assisted Workflow Governance Policy document authored and filed. Covers: scope of AI authority, mandatory human review checkpoints, escalation triggers, record-keeping obligations.

---

### BLG-RD-01 — Entity store fallback masks API error states

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04/ST-08

### BLG-RD-01 — Entity store fallback masks API error states ✅ COMPLETE
**Priority:** P2
**Type:** Frontend Defect — Error State Coverage
**Source:** DEV-ST03-01 — Delivery verification 2026-03-04__release-v1.8
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-08

Each Risk Dashboard component now renders its own error state when GET /portfolio fails. Entity fallback no longer silently masks failure.

---

### BLG-RD-02 — GracePeriodPanel empty vs error state indistinguishable

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04/ST-08

### BLG-RD-02 — GracePeriodPanel empty vs error state ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Error State UX
**Source:** DEV-ST03-02 — Delivery verification 2026-03-04__release-v1.8
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-08

GracePeriodPanel now renders a visible error card when portfolioError is set, distinct from the empty state.

---

### BLG-RD-03 — PositionRiskTable sorted descending

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04/ST-09

### BLG-RD-03 — PositionRiskTable sorted descending ✅ COMPLETE
**Priority:** P2
**Type:** Frontend Defect — Sort Direction
**Source:** DEV-ST03-03
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-09

PositionRiskTable now sorts by stop distance ascending (tightest stop first) per spec §6.4.

---

### BLG-RD-04 — Stop Price column absent from PositionRiskTable

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04/ST-09

### BLG-RD-04 — Stop Price column absent ✅ COMPLETE
**Priority:** P2
**Type:** Frontend Defect — Missing Column
**Source:** DEV-ST03-04
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-09

Stop Price column (current_stop, GBP, 2dp) now present in PositionRiskTable per spec §6.2.

---

### BLG-RD-05 — GRACE badge colour amber instead of blue

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04/ST-10

### BLG-RD-05 — GRACE badge colour ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Cosmetic
**Source:** DEV-ST03-05
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-10

GRACE state badge now rendered in blue per spec §6.3.

---

### BLG-RD-06 — GBP value at risk absent from HeatGauge

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04/ST-10

### BLG-RD-06 — GBP value at risk absent from HeatGauge ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Missing Metric
**Source:** DEV-ST03-06
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-10

GBP value at risk now displayed below gauge value per spec §3.2.

---

### BLG-RD-07 — Days in Grace column absent from GracePeriodPanel

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04/ST-09

### BLG-RD-07 — Days in Grace column absent ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Missing Column
**Source:** DEV-ST03-07
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-09

Days in Grace (holding_days) column now present in Grace Period table per spec §5.2.

---

### BLG-RD-08 — Drawdown data source Head of Specs Team verification

**Status at retirement:** ✅ Resolved
**Priority at retirement:** P2
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1 (resolved 2026-03-06 via ST-06 investigation)
**Evidence:** risk_dashboard.md §4.1 updated to v0.1.7; Head of Specs Team decision 2026-03-06

### BLG-RD-08 — Drawdown data source resolved ✅ RESOLVED
**Priority:** P2
**Type:** Spec Alignment — Owner Decision
**Source:** DEV-ST03-08
**Closed:** 2026-03-06 | ST-06 investigation

Split-source data model confirmed: current_drawdown_percent from GET /portfolio (drawdown_service.py); days_underwater from GET /analytics/metrics (analytics_service.py). risk_dashboard.md §4.1 updated to v0.1.7 to reflect correct split sources.

---

### BLG-RD-09 — ProspectiveHeatPanel missing threshold label

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04/ST-09

### BLG-RD-09 — ProspectiveHeatPanel missing threshold label ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Missing Display Element
**Source:** DEV-ST03-09
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-09

Threshold label badge now present in prospective heat result row, updating when boundary is crossed per §7.5.

---

### BLG-RD-10 — US entry prices in USD not GBP

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04/ST-07

### BLG-RD-10 — US entry prices in USD not GBP ✅ COMPLETE
**Priority:** P2
**Type:** Backend + Frontend Defect — Currency Conversion
**Source:** DEV-ST03-11
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-07

portfolio_service.py now converts entry_price to GBP for US positions. Risk Dashboard displays entry prices in GBP for all positions per §6.2.

---

### BLG-RD-11 — current_stop in USD for US positions

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-04/ST-07

### BLG-RD-11 — current_stop in USD for US positions ✅ COMPLETE
**Priority:** P2
**Type:** Backend + Frontend Defect — Currency Conversion
**Source:** DEV-ST03-12
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-07

portfolio_service.py now converts current_stop to GBP for US positions. Stop Distance % calculation uses matching currencies per §6.2.

---

### TEST-GAP-EPIC-01 — Risk Dashboard scenario execution infrastructure gap

**Status at retirement:** ✅ Closed
**Priority at retirement:** P2
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | ST-11

### TEST-GAP-EPIC-01 — Risk Dashboard scenario infrastructure gap ✅ CLOSED
**Priority:** P2
**Type:** QA Infrastructure
**Source:** Delivery verification 2026-03-04__release-v1.8
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | ST-11

Playwright mock layer delivered. All 17 unexecuted scenarios automated in tests/e2e/risk-dashboard.spec.js. CI gate at .github/workflows/playwright.yml. Mock data in tests/e2e/mocks/portfolio-mock-data.js. Scenario document updated to v1.1.

---

### BLG-SPEC-D1 — API Contracts README version frozen

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06/ST-19

### BLG-SPEC-D1 — API Contracts README.md version frozen at v1.8.4 ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Documentation Drift
**Owner:** API Contracts & Documentation Owner
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

README.md version header updated to v1.9.0. Changelog includes v1.9.0 entry referencing EPIC-06 changes.

---

### BLG-SPEC-D3 — GET /market/status undocumented

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06/ST-16

### BLG-SPEC-D3 — GET /market/status completely undocumented ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Documentation Gap / Drift
**Owner:** API Contracts & Documentation Owner
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-16

docs/specs/api_contracts/market_endpoints.md created. Endpoint documented, registered in Specs_Index.md, added to openapi.yaml.

---

### BLG-SPEC-D4 — GET /positions/search/tags undocumented

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06/ST-19

### BLG-SPEC-D4 — GET /positions/search/tags undocumented ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Documentation Gap
**Owner:** API Contracts & Documentation Owner
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

position_endpoints.md now includes GET /positions/search/tags with request parameters and response schema.

---

### BLG-SPEC-D8 — docs/System_status_report.md missing governance header

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06/ST-19

### BLG-SPEC-D8 — System_status_report.md missing lifecycle header ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Lifecycle Compliance Drift
**Owner:** Director of Quality
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

Lifecycle header added to docs/System_status_report.md. Class and Status assigned per document_lifecycle_guide.md.

---

### BLG-SPEC-D9 — Broken cross-references to lifecycle guide

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06/ST-19

### BLG-SPEC-D9 — process_index.md and Specs_Index.md wrong path for lifecycle guide ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Documentation Drift / Broken Cross-Reference
**Owner:** Head of Specs Team
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

Both process_index.md and Specs_Index.md §5 updated to reference claude/charter/document_lifecycle_guide.md.

---

### BLG-SPEC-G1 — settings_model.md missing

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06/ST-17

### BLG-SPEC-G1 — settings_model.md missing ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Spec Gap
**Owner:** Head of Specs Team
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-17

settings_model.md created in docs/specs/data_model/. Registered in Specs_Index.md §3. Cross-referenced from settings_endpoints.md.

---

### BLG-SPEC-G2 — Error Response Standard not defined

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06/ST-18

### BLG-SPEC-G2 — Error Response Standard not defined ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Spec Gap
**Owner:** API Contracts & Documentation Owner
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-18

Error Response Standard document created. Standard error envelope shape, required fields, HTTP status code mapping defined. All existing API contract docs reference the standard. Registered in Specs_Index.md.

---

### BLG-SPEC-G3 — structured_logging_standards.md not registered in Specs_Index

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06/ST-19

### BLG-SPEC-G3 — structured_logging_standards.md not in Specs_Index ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Index Gap
**Owner:** Head of Specs Team
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

Specs_Index.md §3 updated to include structured_logging_standards.md with Owner, Class, Status, Version.

---

### BLG-SPEC-G4 — ADR-002 in wrong location

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06/ST-19

### BLG-SPEC-G4 — ADR-002 in wrong location ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Governance Organisation Gap
**Owner:** Head of Specs Team
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

ADR-002 moved to docs/product/decisions/. Cross-references updated.

---

### BLG-SPEC-G5 — validation_system.md owner field non-compliant

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-15
**Shipped in:** v1.9 Sprint 1
**Evidence:** Cycle 2026-03-06__release-v1.9 | EPIC-06/ST-19

### BLG-SPEC-G5 — validation_system.md owner non-compliant ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Lifecycle Compliance Gap
**Owner:** Infrastructure & Operations Owner
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

validation_system.md owner field updated to a named governance role. Specs_Index.md §7.1 notation updated to reflect resolved.

---

### BLG-NEW-08 — Automated OpenAPI Drift Detection in CI

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-06
**Shipped in:** v1.8
**Evidence:** Cycle 2026-03-04__release-v1.8 | ST-08

### BLG-NEW-08 — Automated OpenAPI Drift Detection in CI ✅ COMPLETE
**Priority:** P1 (High)
**Type:** CI / Governance
**Owner:** Engineering (CI)
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-08

**Problem**
`docs/reference/openapi.yaml` was not updated during EPIC-06 when three contracts were bumped to v1.9.0 (BLG-SPEC-D7). There is no CI check that detects drift between the markdown API contracts and openapi.yaml. Drift will recur without an automated gate.

**Scope**
- Add a CI step that detects drift between `openapi.yaml` and the markdown API contracts
- Approach: either (a) generate openapi.yaml from contracts and compare, or (b) run a custom lint/diff check against known contract fields
- Block merge on detected drift

**Acceptance Criteria**
- CI step detects drift between openapi.yaml and markdown contracts
- Merge blocked if drift is detected
- Approach documented (generation vs diff) — approach decision to be made in pre-alignment

---

### BLG-NEW-07 — Running API Changelog Document

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-06
**Shipped in:** v1.8
**Evidence:** Cycle 2026-03-04__release-v1.8 | ST-12

### BLG-NEW-07 — Running API Changelog Document ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Documentation / Governance
**Owner:** API Contracts & Documentation Owner
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-12

**Problem**
There is no single running changelog document for API contract changes. Changes to endpoint contracts (new fields, removed fields, version bumps) are recorded in individual spec files but there is no centralised, human-readable history of API evolution across versions.

**Scope**
- Create a running API Changelog document that summarises contract changes per version
- Cover all contracts under `docs/specs/api_contracts/`
- Backfill from v1.8.x → v1.9.0 changes (EPIC-06 scope)
- Document maintainer obligation: must be updated alongside every contract version bump

**Acceptance Criteria**
- API Changelog document exists and is registered in Specs_Index.md
- All v1.9.0 contract changes (EPIC-06) are backfilled
- Maintenance obligation documented alongside contract spec authoring workflow

---

### BLG-NEW-05 — Dependency Vulnerability Scanning in CI

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-06
**Shipped in:** v1.8
**Evidence:** Cycle 2026-03-04__release-v1.8 | ST-07

### BLG-NEW-05 — Dependency Vulnerability Scanning in CI ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Security / CI
**Owner:** Engineering (CI)
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-07

**Problem**
There is no automated scanning of Python dependencies for known vulnerabilities in the CI pipeline. A compromised or vulnerable dependency could be introduced silently.

**Scope**
- Add a CI step that scans Python dependencies (e.g., using `pip-audit` or `safety`) for known CVEs
- Block merge (or warn at configurable severity) on high/critical vulnerabilities
- Integrate with existing `.github/workflows/` structure

**Acceptance Criteria**
- Dependency vulnerability scan runs on every PR
- High/critical CVEs block merge (or produce a required review comment)
- Scan tool and severity threshold documented

---

### BLG-NEW-03 — Define and Document Unavailability Failure Mode

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-06
**Shipped in:** v1.8
**Evidence:** Cycle 2026-03-04__release-v1.8 | ST-11

### BLG-NEW-03 — Define and Document Unavailability Failure Mode ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Policy / Governance
**Owner:** Infrastructure & Operations Owner
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-11

**Problem**
There is no documented policy for what happens when the system is unavailable during a trading session (e.g., backend down, market data feed unavailable). The system has no documented failure modes or fallback procedures for the user.

**Scope**
- Define and document the unavailability failure mode: what the user should do, what the system state is, and any manual fallback procedures
- Document where this policy lives (e.g., OPERATIONAL_GUIDE.md or a new docs/ops/ document)

**Acceptance Criteria**
- Unavailability failure mode documented: system states covered, user action required, data integrity implications
- Document registered in appropriate governance index

---

### BLG-NEW-02 — Backtest vs Live Stop Reconciliation Report

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-06
**Shipped in:** v1.8
**Evidence:** Cycle 2026-03-04__release-v1.8 | ST-06

### BLG-NEW-02 — Backtest vs Live Stop Reconciliation Report ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Quality / CI
**Owner:** Engineering + QA
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Dependency:** After BLG-NEW-01 (golden output baseline must be in place first)
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-06

**Problem**
There is no automated verification that the trailing stop formula used in backtests and the formula used in the live system produce identical results for the same inputs. Silent divergence between backtest and live logic is a category of defect that cannot be caught by either gate independently.

**Scope**
- Report or CI assertion that compares backtest stop calculations vs live system stop calculations for a set of known inputs
- Output: reconciliation result confirming parity or flagging divergence

**Acceptance Criteria**
- Automated check exists that verifies backtest and live stop logic produce identical results for all golden inputs
- Any divergence between backtest and live calculation fails the check

---

### BLG-NEW-01 — Golden Output Regression Baseline for CI

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-06
**Shipped in:** v1.8
**Evidence:** Cycle 2026-03-04__release-v1.8 | ST-05

### BLG-NEW-01 — Golden Output Regression Baseline for CI ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Quality / CI
**Owner:** Engineering + QA
**Source:** IDEA-director-of-quality-20260304-02 — Director of Quality, IW-20260304-01
**Cycle added:** 2026-03-04__item-3.4
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-05

**Problem**
The current CI gate (`POST /validate/calculations`, EPIC-01) checks only that `critical_failed > 0` blocks the merge. It does not verify that specific calculations return the correct numeric values. A change that silently alters the trailing stop formula from `CurrentPrice - (2 × ATR)` to `CurrentPrice - (2.1 × ATR)` would pass the current gate. Numeric regressions are the highest-risk defect class in a trading system.

**Scope**
- Define a set of deterministic golden test cases: known inputs (entry_price, ATR, risk_percent, etc.) with expected output values derived directly from the canonical strategy spec
- Store as `tests/golden_outputs.json` — treated as a canonical artefact; updated only via spec-linked PR
- Scope limited to stop/sizing calculations only (per STEP 5 scoping from IW-20260304-01)
- Add a CI step that calls the backend with each golden input and asserts output matches to required precision
- Any numeric divergence from golden values fails the build

**Acceptance Criteria**
- `tests/golden_outputs.json` exists with spec-derived golden values for stop and sizing calculations
- CI step added that runs golden output assertions on every PR
- Build fails on any numeric deviation from golden values
- Precision tolerance documented (e.g., 4 decimal places for share counts)
- Golden values derived from canonical spec, not from current implementation

**Dependencies**
- None (prerequisite: BLG-NEW-02 must follow, not precede)

---

### BLG-SPEC-D7 — openapi.yaml frozen at v1.8.1

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-06
**Shipped in:** v1.8
**Evidence:** Cycle 2026-03-04__release-v1.8 | ST-10

### BLG-SPEC-D7 — openapi.yaml frozen at v1.8.1; not updated for v1.9.0 contracts ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Documentation Drift / Reference Artefact Staleness
**Owner:** API Contracts & Documentation Owner
**Raised:** 2026-03-03 — Head of Specs Team review
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-10 — openapi.yaml updated to v1.9.0

**Problem**
`docs/reference/openapi.yaml` is at version 1.8.1 (1193 lines).
Three contracts were bumped to v1.9.0 in EPIC-06:
- `sharpe_ratio_trade_method` absent from /validate/calculations validated metrics list
- portfolio positions response schema not aligned to v1.9.0 field list
- `holding_days` absent from GET /trades trade object schema
Specs_Index.md §4 states: "openapi.yaml must be reviewed inline with every contract change; markdown contracts take precedence on conflict."
This was not done during EPIC-06.

**Acceptance Criteria**
- openapi.yaml version field updated to 1.9.0
- /validate/calculations response includes sharpe_ratio_trade_method (14 validated metrics total)
- GET /trades trade object includes holding_days (integer)
- GET /portfolio positions objects reflect v1.9.0 field list
- No conflicts between openapi.yaml and markdown contracts

---

### BLG-SPEC-D2 — settings_endpoints.md spec/implementation mismatch

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-06
**Shipped in:** v1.8
**Evidence:** Cycle 2026-03-04__release-v1.8 | ST-09

### BLG-SPEC-D2 — settings_endpoints.md spec/implementation mismatch ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Spec–Implementation Drift
**Owner:** API Contracts & Documentation Owner + Head of Engineering
**Raised:** 2026-03-03 — Head of Specs Team review
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-09 — settings_endpoints.md v1.1.0 published; PATCH/POST documented as canonical

**Problem**
`docs/specs/api_contracts/settings_endpoints.md` specifies `PUT /settings` (replace all settings).
Live implementation in `backend/main.py` uses `PATCH /settings/{settings_id}` (update single setting by ID).
Additionally, `POST /settings` is implemented but not documented anywhere.
This is a P1 drift: clients relying on the spec will call the wrong method and path.

**Decision Required**
Product Owner + API Contracts owner to choose:
(a) Update spec to document `PATCH /settings/{settings_id}` and `POST /settings` as the canonical interface, or
(b) Align backend to implement `PUT /settings` as specced (breaking change to existing frontend).

**Acceptance Criteria**
- settings_endpoints.md accurately documents the live HTTP method, path, and request/response schema
- No divergence between spec and implementation
- Decision record filed if option (b) chosen (breaking change)

---

### §6 v1.7 Release Slice — 2026-03-02__release-v1.7

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** All 6 EPICs shipped 2026-03-03; verified 2026-03-03 — `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

<!-- release-plan-marker: RP:v1.7:2026-03-02__release-v1.7 -->

**Cycle:** 2026-03-02__release-v1.7
**Planning Date:** 2026-03-02
**Status:** ✅ Complete — all 6 EPICs shipped 2026-03-03; verified 2026-03-03
**Reference:** claude/cycles/2026-03-02__release-v1.7/stage4_backlog_slice.md

| S2 ID | Item | Epic | Priority | Effort |
|-------|------|------|----------|--------|
| S2-01 | BLG-TECH-04 — CI/CD GitHub Actions Validation Workflow | EPIC-01 | P2 | ~1 day |
| S2-02 | Strategy Rules §13 Boundary Review | EPIC-02 | P1 | ~0.5 day |
| S2-03 | Metrics Definitions — Portfolio Heat Formula & Thresholds | EPIC-03 | P1 | ~0.5 day |
| S2-04 | Structured Logging / Observability Standards | EPIC-04 | P2 | ~1 day |
| S2-05 | API Versioning Strategy Decision Record | EPIC-05 | P2 | ~0.5 day |
| S2-06 | BLG-TECH-06 — Canonicalise sharpe_ratio_trade_method | EPIC-06 | P2 | ~30 min–1 hr |
| S2-07 | BLG-TECH-08 — Align portfolio_endpoints.md positions summary | EPIC-06 | P3 | ~30 min + decision |
| S2-08 | BLG-TECH-09 — Add holding_days to GET /trades | EPIC-06 | P3 | ~30 min + decision |

**Total estimated effort:** ~3.5–4 days
**Capacity assessment:** PASS (workforce_capacity.md — no constraints violated)
**Key gates unlocked by this release:**
- EPIC-02 → §13-gated features may enter pre-alignment
- EPIC-03 → v1.8 Risk Dashboard pre-alignment
- EPIC-04 + EPIC-05 → v2.0 Alerts pre-alignment (2 of 3 gates)

---

### BLG-SPEC-D6 — changelog.md has no v1.7 entry

**Status at retirement:** ✅ Complete — Resolved
**Priority at retirement:** P3
**Retired:** 2026-03-04
**Shipped in:** N/A — documentation fix
**Evidence:** v1.7 entry confirmed present in `docs/product/changelog.md` (verified 2026-03-04)

**BLG-SPEC-D6** — changelog.md has no v1.7 entry
**Priority:** P3 (Low)
**Type:** Documentation Drift
**Owner:** Product Owner
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`docs/product/changelog.md` last entry is v1.6.1 (2026-03-01).
v1.7 Foundation & Governance sprint was fully delivered and verified (2026-03-03).
No entry exists for v1.7.

**Acceptance Criteria**
- v1.7 changelog entry added covering: CI/CD merge gate (EPIC-01), §13 boundary review (EPIC-02), Portfolio Heat metrics (EPIC-03), Structured Logging Standards (EPIC-04), API Versioning Decision Record (EPIC-05), Spec Debt Resolution — analytics/portfolio/trade endpoints v1.9.0 (EPIC-06)

---

### BLG-SPEC-D5 — current_roadmap.md v1.7 section not closed out

**Status at retirement:** ✅ Complete — Resolved
**Priority at retirement:** P3
**Retired:** 2026-03-04
**Shipped in:** N/A — documentation fix
**Evidence:** Resolved by `manage roadmap` run 2026-03-04 — v1.7 section retired to `claude/roadmap/roadmap_archive.md`; release summary updated; footer already referenced correct backlog path

**BLG-SPEC-D5** — current_roadmap.md v1.7 section not closed out
**Priority:** P3 (Low)
**Type:** Documentation Drift
**Owner:** Product Owner
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`claude/roadmap/current_roadmap.md` v1.7 section items still show "Status: Planned".
Release Summary table has no ✅ for v1.7.
v1.7 was fully delivered (2026-03-02) and verified (2026-03-03).
Additionally, footer references `docs/product/feature_backlog.md` which does not exist (actual backlog: `claude/backlog/backlog.md`).

**Acceptance Criteria**
- v1.7 section marked Complete with delivery date
- Release Summary table updated (✅ v1.7)
- Footer corrected to reference correct backlog path

---

### BLG-NEW-06 — Realised vs Unrealised P&L Labelling

**Status at retirement:** ❌ Killed — merged into 4.1b pre-work scope
**Priority at retirement:** N/A
**Retired:** 2026-03-04
**Shipped in:** N/A — merged
**Evidence:** DL-005 (2026-03-04); merged into roadmap item 4.1b Tax-Year P&L Statement pre-work scope

**BLG-NEW-06** — Realised vs Unrealised P&L Labelling
**Status:** Merged into 4.1b pre-work scope — not a standalone backlog item
**Source:** IW-20260304-01
**Cycle added:** 2026-03-04__item-3.4

This item (clear distinction of realised vs unrealised P&L amounts in the tax-year P&L statement) has been merged into the 4.1b Tax-Year P&L Statement scope as pre-work. See current_roadmap.md §4.1b scope note (2026-03-04). No standalone delivery required.

---

### BLG-TECH-09 — Add holding_days to GET /trades

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** Cycle 2026-03-02__release-v1.7, EPIC-06/TASK-28–30; `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

**BLG-TECH-09** — Add holding_days to GET /trades
**Priority:** P3
**Effort:** ~1 hour
**Target release:** v1.7
**Status:** ✅ COMPLETE — 2026-03-03 (cycle: 2026-03-02__release-v1.7, EPIC-06/TASK-28–30; backend fix path chosen)
**Source:** OBS-QWB-R3-01 — QA Lead observation, QWB verification, 2026-03-01
holding_days is absent from trade objects in the GET /trades response.
trade_endpoints.md v1.8.4 lists it as a required field. Pre-existing behaviour,
not introduced by QWB.
Decision required: Either (a) add holding_days to the backend GET /trades
response (the spec-compliant fix); or (b) remove holding_days from trade_endpoints.md
documented schema. Product Owner + API Contracts owner to decide.
Acceptance Criteria

GET /trades trade objects include holding_days (integer), OR
trade_endpoints.md schema is corrected to remove the field, with a note explaining
its absence and where the value can be sourced (e.g. trades_for_charts)

**Owner:** API Contracts & Documentation Owner
Raised by: QA Lead, 2026-03-01

---

### BLG-TECH-08 — Align portfolio_endpoints.md positions summary field list

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** Cycle 2026-03-02__release-v1.7, EPIC-06/TASK-25–27; `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

**BLG-TECH-08** — Align portfolio_endpoints.md positions summary field list
**Priority:** P3
**Effort:** ~30 min
**Target release:** v1.7
**Status:** ✅ COMPLETE — 2026-03-03 (cycle: 2026-03-02__release-v1.7, EPIC-06/TASK-25–27; spec update path chosen)
**Source:** OBS-QWB-R1-01 — QA Lead observation, QWB verification, 2026-03-01
GET /portfolio positions summary objects omit current_price_native, stop_price,
stop_price_native, and pnl_percent — fields listed in R-01 test scenario step 3
and in portfolio_endpoints.md. Pre-existing behaviour, not introduced by QWB.
Decision required: Either (a) update portfolio_endpoints.md to accurately document
the lightweight summary shape, explicitly distinguishing it from the full position object
on GET /positions; or (b) add the missing fields to the backend response. Product Owner

API Contracts owner to decide.

**Acceptance Criteria**

portfolio_endpoints.md positions summary field list matches the live API response
No discrepancy between spec and implementation for /portfolio positions objects

Owner: API Contracts & Documentation Owner
Raised by: QA Lead, 2026-03-01

---

### BLG-TECH-06 — Canonicalise sharpe_ratio_trade_method as 14th validation metric

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** Cycle 2026-03-02__release-v1.7, EPIC-06/TASK-21–24; `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

**BLG-TECH-06** — Canonicalise sharpe_ratio_trade_method as 14th validation metric in analytics_endpoints.md
**Priority:** P2 (Medium)
**Type:** Spec Accuracy / Governance
**Target release:** v1.7 *(updated from v1.6.1 — v1.6.1 has shipped; DL-001 cycle 2026-03-01__item-3.2)*
**Status:** ✅ COMPLETE — 2026-03-03 (cycle: 2026-03-02__release-v1.7, EPIC-06/TASK-21–24)
**Problem**
POST /validate/calculations returns 14 validation results. analytics_endpoints.md v1.8.1
describes 13 metrics and does not document sharpe_ratio_trade_method.
The 14th metric was introduced under BLG-TECH-01 Addendum 1 (PMO-confirmed scope, 2026-02-20)
to exercise the trade-based Sharpe fallback path. The implementation is correct and the result
passes. The spec is incomplete.
This was recorded as OBS-01 by the QA Lead during BLG-TECH-02/03 re-verification
(2026-02-21T21:25:00Z) and formally acknowledged by the Product Owner (2026-02-21).
Per document_lifecycle_guide.md v2.2 — deviation must have priority, target release,
and owner at time of documentation. These are recorded here.
Scope

Update analytics_endpoints.md to add sharpe_ratio_trade_method as a formally
documented 14th validation metric
Add to the validated metrics table with: severity critical, formula, tolerance
Update the response example to show 14 results and correct by_severity.critical.total: 4
No code change required — implementation is correct

**Acceptance Criteria**

analytics_endpoints.md validated metrics table includes sharpe_ratio_trade_method
Response schema example reflects 14 results
by_severity.critical.total shown as 4 in example (not 3)
No deviation exists between the spec and the live POST /validate/calculations response

**Owner**

API Contracts & Documentation Owner

**Source**

OBS-01 — QA Lead, BLG-TECH-02/03 re-verification, 2026-02-21T21:25:00Z
Product Owner disposition: backlog item, v1.6.1 target, 2026-02-21

---

### BLG-TECH-04 — CI/CD validation workflow (GitHub Actions)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** Cycle 2026-03-02__release-v1.7, EPIC-01; PR #11 merged; `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

### BLG-TECH-04 — CI/CD validation workflow (GitHub Actions)
**Priority:** P2 (Medium)
**Type:** Delivery Quality / Automation
**Status:** ✅ COMPLETE — 2026-03-03 (cycle: 2026-03-02__release-v1.7, EPIC-01)
**Target release:** v1.7

**Problem**
- Validation is manual and not enforced at merge time.

**Scope**
- Add `.github/workflows/validate-analytics.yml`.
- Run `POST /validate/calculations` on:
  - Pull requests
  - Pushes to `main` and `develop`
- Block merge if any **critical-severity** validation fails.
- Post validation summary as PR comment.

**Acceptance Criteria**
- Workflow reliably runs on all PRs.
- Merge is blocked only for critical severity failures.
- Clear PR feedback is visible.

**Dependencies**
- BLG-TECH-02 (severity model must exist).

**Owners**
- Engineering
- QA

---

### BLG-FEAT-07 — CSV Export of Trade History

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0; `docs/product/changelog.md` v1.6.1

### BLG-FEAT-07 — CSV Export of Trade History
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

One-click CSV export for tax and analysis use.

---

### BLG-FEAT-06 — Grace Period Indicator

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0; `docs/product/changelog.md` v1.6.1

### BLG-FEAT-06 — Grace Period Indicator
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Show remaining grace period days in open positions table.
Example: "Day 6 of 10"

---

### BLG-FEAT-05 — Win Rate by Month Chart

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0; `docs/product/changelog.md` v1.6.1

### BLG-FEAT-05 — Win Rate by Month Chart
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Bar chart of win rate grouped by calendar month.

---

### BLG-FEAT-04 — Best / Worst Trades Widget

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0; `docs/product/changelog.md` v1.6.1

### BLG-FEAT-04 — Best / Worst Trades Widget
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Show top 3 and bottom 3 trades by R-multiple or P&L.

---

### BLG-FEAT-02 — R-Multiple Column in Trade History

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0; `docs/product/changelog.md` v1.6.1

### BLG-FEAT-02 — R-Multiple Column in Trade History
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Add R-multiple column to trade history table.

**Indicative Formula**

`(Exit Price - Entry Price) / (Entry Price - Stop Price)`

**Notes**
- Formula must be confirmed by Metrics Definitions owner.
- Decide server-side vs frontend-only calculation.

---

### BLG-FEAT-01 — Current Drawdown Widget

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0; `docs/product/changelog.md` v1.6.1

### BLG-FEAT-01 — Current Drawdown Widget
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Display current drawdown from peak and days underwater.
Example: "Drawdown: -8.2%, 12 days underwater"

**Dependency**
- Metrics Definitions owner must confirm drawdown calculation before implementation.

---

### BLG-TECH-03 — Consolidate ValidationService into service layer

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-04
**Shipped in:** v1.6.1 (co-delivered with BLG-TECH-02)
**Evidence:** Director of Quality sign-off 2026-02-21T21:30:00Z; `docs/product/phase_gates/BLG-TECH-03-validationservice-consolidation-phase-gate.md`

BLG-TECH-03 — Consolidate ValidationService into service layer
Priority: P1 (High)
Type: Architecture / Maintainability
Status: ✅ COMPLETE — 2026-02-21
Closed

All validation logic moved from routers/validation.py into services/validation_service.py
Router thinned to HTTP in/out only — delegates entirely to ValidationService.validate_all()
Stub replaced with full 13-metric + trade-Sharpe implementation
Delivered in same branch as BLG-TECH-02 per co-delivery constraint
Director of Quality sign-off: 2026-02-21T21:30:00Z
Phase Gate Document filed: docs/product/phase_gates/BLG-TECH-03-validationservice-consolidation-phase-gate.md

---

### BLG-TECH-02 — Implement validation severity model

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** Director of Quality sign-off 2026-02-21T21:30:00Z; `docs/product/phase_gates/BLG-TECH-02-validation-severity-model-phase-gate.md`

BLG-TECH-02 — Implement validation severity model
Priority: P1 (High)
Type: Governance / Operational Control
Status: ✅ COMPLETE — 2026-02-21
Closed

severity field added to every validation result object (critical / high / medium / low)
by_severity aggregation added to summary — all four tiers always present
Severity mapping implemented in ValidationService per analytics_endpoints.md v1.8.1
Director of Quality sign-off: 2026-02-21T21:30:00Z
Phase Gate Document filed: docs/product/phase_gates/BLG-TECH-02-validation-severity-model-phase-gate.md

---

### BLG-TECH-01 — Fix Sharpe variance method + Capital Efficiency currency basis

**Status at retirement:** ✅ Complete
**Priority at retirement:** P0
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** Canonical Owner sign-off 2026-02-21; 13/13 pass at 2026-02-21T00:24:41Z; `metrics_definitions.md` v1.5.7; `analytics_endpoints.md` v1.8.1

### BLG-TECH-01 — Fix Sharpe variance method + Capital Efficiency currency basis
**Priority:** P0 (Critical)
**Type:** Metrics Correctness / Validation Integrity
**Status:** ✅ COMPLETE — 2026-02-21

**Closed**
- `_calculate_sharpe()` updated to use sample variance (÷ n−1) for portfolio and trade-level Sharpe methods
- Capital efficiency updated to use `Mean(total_cost)` in GBP from `trade_history`
- `validation_data.py` expected values updated: `capital_efficiency` 0.17 → 0.22; `total_cost` fields added
- Validation: 13/13 pass confirmed at 2026-02-21T00:24:41Z
- Canonical Owner sign-off: 2026-02-21
- `metrics_definitions.md` v1.5.7 — Appendix E both items marked resolved
- `analytics_endpoints.md` v1.8.1 — resolved known limitations removed
- v1.6 quality gate: satisfied

---

### v2.0 Release Items — 2026-03-17__release-v2.0 (Backlog Grooming 2026-03-17)

**Retired:** 2026-03-17
**Shipped in:** v2.0 — Reporting & Alerts
**Evidence:** `claude/cycles/2026-03-17__release-v2.0/verification_report.md`; `closure_record.md`

---

### TEST-GAP-EPIC-02 — CohortAnalysis backend integration regression scenario

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-17
**Shipped in:** v2.0 — Reporting & Alerts
**Evidence:** `claude/cycles/2026-03-17__release-v2.0/verification_report.md`; EPIC-05/ST-20

### TEST-GAP-EPIC-02 — CohortAnalysis backend integration regression scenario
**Priority:** P3
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner
**Source:** TSG-V110-01 — verification_report.md §6, cycle 2026-03-15__release-v1.10
**Cycle added:** 2026-03-15__release-v1.10
**Target release:** before next sprint touching analytics components

Test scenario coverage gap from 2026-03-15__release-v1.10: QA & Testing Owner to author CohortAnalysis backend integration regression scenario (`SC-CA-BACKEND-01`) covering: period toggle (Monthly / Quarterly / Yearly) triggers API refetch and table updates; `has_enough_data = false` shows insufficient data warning; column values match `GET /analytics/cohort` response fields. Spec references: `docs/specs/frontend/pages/analytics.md §15`; `docs/specs/api_contracts/analytics_endpoints.md#GET /analytics/cohort`. Register in `docs/testing/risk_dashboard_scenarios.md` or new `analytics_scenarios.md`.

---

### BLG-BE-02 — Spec and implement GET /portfolio/prospective-heat endpoint

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-17
**Shipped in:** v2.0 — Reporting & Alerts
**Evidence:** `claude/cycles/2026-03-17__release-v2.0/verification_report.md`; EPIC-04/ST-13; commit 279e832

### BLG-BE-02 — Spec and implement GET /portfolio/prospective-heat endpoint
**Priority:** P3
**Type:** Backend + Spec
**Owner:** Head of Engineering + Head of Specs Team
**Source:** DEV-ST05-01 — ST-05 (v1.10 EPIC-03) integration tests could not cover this endpoint because it is absent from `portfolio_endpoints.md` and not implemented in `backend/main.py`. Discovered during sprint execution 2026-03-16.
**Cycle added:** 2026-03-15__release-v1.10
**Target release:** v2.0 (or earlier if ProspectiveHeatPanel becomes a priority)

**Problem**
The ProspectiveHeatPanel frontend component exists and makes reference to portfolio heat projection, but `GET /portfolio/prospective-heat` (a prospective heat calculation endpoint) is not defined in `portfolio_endpoints.md` and has no backend implementation. BLG-API-01 acceptance criteria referenced this endpoint, resulting in DEV-ST05-01 (P3) when integration tests could not be written for it.

**Scope**
- Author `GET /portfolio/prospective-heat` spec in `portfolio_endpoints.md` (response shape, calculation definition)
- Implement the endpoint in `backend/main.py`
- Add TestClient integration tests in `tests/test_portfolio_integration.py` (currently skipped with `@unittest.skip` per DEV-ST05-01)

**Acceptance Criteria**
- `GET /portfolio/prospective-heat` defined in `portfolio_endpoints.md`
- Endpoint implemented and returning correct prospective heat calculation
- `@unittest.skip` removed from `TestProspectiveHeat` in `tests/test_portfolio_integration.py`; tests pass

---

### BLG-GOV-01 — Roadmap stage document consolidation

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-17
**Shipped in:** v2.0 — Reporting & Alerts
**Evidence:** `claude/cycles/2026-03-17__release-v2.0/verification_report.md`; EPIC-06/ST-18

### BLG-GOV-01 — Roadmap stage document consolidation
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Roadmap process reflection 2026-03-16
**Cycle added:** 2026-03-16 (governance improvement session)
**Effort:** M (2–3 days — prompt rewrite + template updates)
**Target release:** v2.0 (governance prep)

Currently Standard and Extended roadmap runs produce 5–8 separate stage files per cycle (`stage1_validation.md`, `stage2_backlog_health.md`, `stage3_ideas.md`, `stage4_debate.md`, `stage5_rebalance.md`, `run_manifest.md`, `cycle_summary.md`, `lessons_learnt.md`). The Lightweight tier (added v3.0) already consolidates STEP 2–7 output into a single `cycle_record.md`. This item extends that consolidation to Standard and Extended runs — collapsing the 5 working-paper stage files into sections of `cycle_record.md` while keeping `run_manifest.md`, `cycle_summary.md`, and `lessons_learnt.md` as separate files.

**Acceptance Criteria**
- `roadmap_prompt.md` updated: STEP 2–7 write targets changed to sections of `cycle_record.md` for all tiers
- Write scope restriction (§5) updated accordingly
- STEP 9 Write Plan template updated to reference `cycle_record.md`
- STEP 10 completion condition updated
- `OPERATIONAL_GUIDE.md` §6 artefact list updated
- At least one `run roadmap` cycle validated against the new format before sealing

---

### BLG-GOV-02 — Ideas register (replace per-file idea submissions)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-17
**Shipped in:** v2.0 — Reporting & Alerts
**Evidence:** `claude/cycles/2026-03-17__release-v2.0/verification_report.md`; EPIC-06/ST-19

### BLG-GOV-02 — Ideas register (replace per-file idea submissions)
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Roadmap process reflection 2026-03-16
**Cycle added:** 2026-03-16 (governance improvement session)
**Effort:** M (2–3 days — prompt rewrite + migration)
**Target release:** v2.0 (governance prep)

The current idea intake model produces one file per idea per agent per window (44+ files from a single intake window). Status tracking requires bulk `sed` updates across dozens of files. This item replaces the per-file model with a single `claude/ideas/ideas_register.md` — a structured table with one row per idea containing: ID, agent, title, status, effort band, submission date, last-actioned date, and park rationale. The window summary (`window_summary_<window_id>.md`) is retained as the per-window record. Individual historical submission files are archived but not deleted.

**Acceptance Criteria**
- `idea_intake_prompt.md` updated: submissions write to `ideas_register.md` (append/update row) instead of individual files
- `roadmap_prompt.md` STEP 4 updated: reads from `ideas_register.md` table instead of scanning individual files
- `ideas_register.md` schema defined in `shared_standards.md` §16 (new entry)
- Migration script or instruction provided to convert existing `claude/ideas/submissions/` files into register rows
- Prior submission files moved to `claude/ideas/submissions/archive/`
- `OPERATIONAL_GUIDE.md` updated to reflect new artefact

---

### v2.1 Backlog Items — 2026-03-18__release-v2.1

**Status at retirement:** ✅ Complete
**Retired:** 2026-03-21
**Shipped in:** v2.1 — Alerts, Watchlists & Enhancements
**Evidence:** `claude/cycles/2026-03-18__release-v2.1/verification_report.md` — all 19 items delivered

| Item ID | Title | Story | Notes |
|---------|-------|-------|-------|
| BLG-SPEC-G6 | total_return_pct not returned by GET /analytics/metrics | ST-17 | Spec updated; implementation shipped |
| BLG-SPEC-D10 | api_dependencies.md v2.0 additions | ST-17 | Spec updated to include Reports + Signals mappings |
| BLG-SPEC-D11 | data_model.md §501 trade_reflections section | ST-17 | Section updated to reflect implemented status |
| BLG-SPEC-D12 | Bulk lifecycle header remediation (28 docs) | ST-16 | All 28 docs updated to Class 1/2 headers |
| BLG-SPEC-D13 | metrics_definitions.md Owner field non-compliant | ST-17 | Owner field corrected to governance role |
| TEST-GAP-SIG-01 | Signals page controls test scenarios | ST-18 | signals_scenarios.md authored |
| TEST-GAP-TAX-01 | Tax Year P&L report test scenarios | ST-18 | reports_scenarios.md authored |
| BLG-PROC-01 | Cross-EPIC process compliance check | ST-19 | v2.1 sprint compliance confirmed; EPIC-03 cherry-pick deviation documented |
| BLG-OPS-03 | Pre-merge frontend preview environments | ST-15 | seed-preview.yml psql approach shipped; frontend preview blocker documented |
| BLG-FR-01 | Tax Year P&L Report PDF Export | ST-12 | GET /reports/tax-year?format=pdf implemented with server-side PDF generation |

