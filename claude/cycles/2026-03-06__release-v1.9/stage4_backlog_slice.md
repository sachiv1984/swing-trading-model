# Stage 4 — Backlog Slice (v1.9)

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-03-06__release-v1.9
**Release:** v1.9
**Last Updated:** 2026-03-06

---

## Release: v1.9 — User Value & Insight

**Cycle:** 2026-03-06__release-v1.9
**EPIC structure:** EPIC-01 through EPIC-06 (6 EPICs; 30 scope items)
**Marker:** `<!-- release-plan-marker: RP:v1.9:2026-03-06__release-v1.9 -->`

---

## EPIC-01 — Trade Reflection & Compliance Metrics
**Maps to:** S2-01, S2-02
**Priority order:** S2-02 must complete before S2-01 (metrics definitions gate)

### ST-01 — Canonicalise Basic Compliance Metrics
**Backlog ref:** BLG-FEAT-08
**Owner:** Metrics Definitions & Analytics Owner
**Priority:** P2
**Effort:** ~1 day
**Type:** Spec + Backend + Frontend

**Acceptance Criteria:**
- `metrics_definitions.md` updated (version incremented) with canonical definitions for:
  - Journal completion rate (formula, denominator, time window)
  - Stop-based exit rate (formula, classification rules)
  - Average position size as % of portfolio (formula, snapshot basis)
- Backend computes and exposes all three metrics (existing or extended analytics endpoint)
- Frontend displays compliance metrics (analytics page or dedicated panel)
- FinOps & Resource Architect confirms Metrics Definitions owner available (LL-05 check)

**Pre-condition:** FinOps capacity confirmation (RISK-01). Sprint planning must not seal ST-01 without this confirmation.

---

### ST-02 — Structured Trade Reflection Template
**Backlog ref:** Roadmap 5.1
**Owner:** Frontend Specs & UX Documentation Owner (spec); Head of Engineering (implementation)
**Priority:** P2
**Effort:** 1–2 days
**Type:** Spec (new) + Backend + Frontend
**Depends on:** ST-01 complete (metrics definitions canonical)

**Acceptance Criteria:**
- Frontend spec created: `docs/specs/frontend/pages/trade_reflection.md` (Class 1 Canonical, version 0.1)
- Post-trade reflection form renders at trade close
- Form pre-populated from trade record: hold time, R-multiple, exit reason, position state history
- Structured reflection prompts: trade rationale, what worked, what didn't, discipline assessment
- Reflection entries stored and retrievable (data model confirmed by Data Model & Domain Schema Owner)
- No AI components — fully deterministic
- All new endpoints documented in API contracts
- New data fields (if any) added to data_model.md with version increment

---

## EPIC-02 — Analytics Enhancements
**Maps to:** S2-03, S2-18
**Note:** Metrics definitions for S2-03 and S2-18 may be batched with ST-01 (EPIC-01) metrics update

### ST-03 — Cohort Analysis
**Backlog ref:** Roadmap 5.2
**Owner:** Head of Engineering
**Priority:** P2
**Effort:** 1–2 days
**Type:** Spec update + Backend + Frontend

**Acceptance Criteria:**
- Cohort metric definitions added to `metrics_definitions.md` (same version update as ST-01 if batched, otherwise new increment)
- Backend: new query or analytics endpoint extension grouping closed trades by entry period (month, quarter, year)
- Frontend: cohort analysis tab or panel on Performance Analytics page
- Period selector: month / quarter / year
- Values computed from canonical backend formula; no client-side re-derivation
- Endpoint documented in API contracts; openapi.yaml updated

---

### ST-04 — R-Multiple Distribution Report
**Backlog ref:** BLG-NEW-09
**Owner:** Metrics Definitions & Analytics Owner (definition); Head of Engineering (implementation)
**Priority:** P2
**Effort:** 1–2 days
**Type:** Spec update + Backend + Frontend
**Depends on:** ST-01 metrics definitions batch (R-multiple formula must be canonical first)

**Acceptance Criteria:**
- R-multiple formula defined and canonicalised in `metrics_definitions.md`
- Backend computes R-multiple per closed trade from existing trade data
- Distribution visualisation (chart or panel) on Performance Analytics page
- Values computed from canonical backend formula; no client-side derivation

---

## EPIC-03 — Dashboard Homepage
**Maps to:** S2-04

### ST-05 — Dashboard Homepage / Session Summary
**Backlog ref:** Roadmap 5.3
**Owner:** Frontend Specs & UX Documentation Owner (spec); Head of Engineering (implementation)
**Priority:** P2
**Effort:** 1–2 days
**Type:** Spec (new) + Backend (optional) + Frontend

**Acceptance Criteria:**
- Frontend spec created: `docs/specs/frontend/pages/dashboard_home.md` (Class 1 Canonical, version 0.1)
- Dashboard home page renders on load with:
  - Open positions count (from GET /positions)
  - Total portfolio heat (from GET /portfolio)
  - Positions in grace period today (from GET /portfolio or GET /positions)
  - Today's signal status (from GET /signals)
  - Recent trade activity summary (from GET /trades or existing endpoint)
- If composite endpoint added (`GET /dashboard/summary`): documented in API contracts + openapi.yaml
- Composite endpoint, if present, aggregation only — no new computations
- All values sourced from existing canonical endpoints

---

## EPIC-04 — Risk Dashboard Defect Resolution
**Maps to:** S2-05 through S2-15

### ST-06 — Drawdown Data Source Spec Alignment
**Backlog ref:** BLG-RD-08 (DEV-ST03-08)
**Owner:** Head of Specs Team
**Priority:** P2
**Effort:** Small (<0.5 day — documentation only)
**Type:** Spec alignment
**Sequencing:** Complete before EPIC-04 verification; does not block implementation of other EPIC-04 items

**Acceptance Criteria:**
- Head of Specs Team reviews ST-02 alignment outcome (v1.8 pre-alignment confirmed GET /portfolio)
- `docs/specs/frontend/pages/risk_dashboard.md` §4.1 updated to reflect confirmed canonical data source
- If GET /portfolio confirmed: §4.1 updated, DEV-ST03-08 resolved
- If GET /analytics/metrics remains canonical: scope expansion required; raise escalation before sprint planning seal (RISK-06)

---

### ST-07 — Risk Dashboard Backend: US Currency Conversion
**Backlog ref:** BLG-RD-10 (DEV-ST03-11), BLG-RD-11 (DEV-ST03-12)
**Owner:** Head of Engineering
**Priority:** P2
**Effort:** Small–Medium (~0.5–1 day)
**Type:** Backend fix
**Maps to:** S2-14, S2-15

**Acceptance Criteria:**
- `backend/services/portfolio_service.py` converts `entry_price` to GBP for US positions using stored FX rate (consistent with existing FX conversion pattern)
- `portfolio_service.py` converts `current_stop` to GBP for US positions using same FX conversion
- All position prices in GBP on Risk Dashboard for both US and UK positions
- Stop Distance % calculation uses matching currencies
- Golden output tests pass; no regression on existing CI

---

### ST-08 — Risk Dashboard Frontend: Error States & Entity Fallback
**Backlog ref:** BLG-RD-01 (DEV-ST03-01), BLG-RD-02 (DEV-ST03-02)
**Owner:** Head of Engineering / Base44 Frontend Prompt Owner
**Priority:** P2 / P3
**Effort:** Small
**Type:** Frontend fix
**Maps to:** S2-05, S2-06
**Depends on:** ST-07 (deploy backend first or mock)

**Acceptance Criteria:**
- Each Risk Dashboard component renders its own error state independently when GET /portfolio fails
- Entity store fallback does not silently mask API failure (error indicator shown while fallback active, or fallback removed)
- GracePeriodPanel renders distinct error card when `portfolioError` is set — distinct from empty state

---

### ST-09 — Risk Dashboard Frontend: Table and Column Fixes
**Backlog ref:** BLG-RD-03 (DEV-ST03-03), BLG-RD-04 (DEV-ST03-04), BLG-RD-07 (DEV-ST03-07), BLG-RD-09 (DEV-ST03-09)
**Owner:** Head of Engineering
**Priority:** P2 / P3
**Effort:** Small
**Type:** Frontend fix
**Maps to:** S2-07, S2-08, S2-11, S2-13

**Acceptance Criteria:**
- PositionRiskTable sorted by stop distance ascending (tightest first) within each state group
- Stop Price column (`current_stop`, GBP, 2 dp) present in PositionRiskTable per spec §6.2
- Days in Grace (`holding_days`) column present in Grace Period table per spec §5.2
- Threshold label badge present in ProspectiveHeatPanel result row, updating when boundary crossed per §7.5

---

### ST-10 — Risk Dashboard Frontend: HeatGauge and Cosmetic Fixes
**Backlog ref:** BLG-RD-05 (DEV-ST03-05), BLG-RD-06 (DEV-ST03-06)
**Owner:** Head of Engineering
**Priority:** P3
**Effort:** Small
**Type:** Frontend fix
**Maps to:** S2-09, S2-10

**Acceptance Criteria:**
- GRACE state badge colour is blue per spec §6.3 (was amber)
- GBP value at risk displayed below gauge value per spec §3.2

---

## EPIC-05 — QA & Test Infrastructure
**Maps to:** S2-16, S2-17

### ST-11 — Canonical Test Scenario Library (Phase 1: Risk Dashboard)
**Backlog ref:** TEST-GAP-EPIC-01 / BLG-NEW-10
**Owner:** QA & Testing Owner
**Priority:** P1
**Effort:** Medium (1–2 days)
**Type:** QA Infrastructure

**Acceptance Criteria:**
- Seeded test infrastructure created (database seed, mock/stub API layer, or test data management mechanism — approach agreed at pre-alignment)
- Infrastructure supports: specific portfolio_heat_percent values, positions with specific grace_days_remaining, empty position state, controlled prospective heat API responses
- All 17 NOT EXECUTED Risk Dashboard scenarios (SC-RD-02–06, SC-RD-07–12, SC-RD-15, SC-RD-16–18, SC-RD-24–25) re-run against seeded environment
- Results recorded in `docs/testing/risk_dashboard_scenarios.md`
- "Test Infrastructure Preconditions" section added to risk_dashboard_scenarios.md (Director of Quality requirement — outstanding action from v1.8)

---

### ST-12 — Canonical Test Scenario Library (Phase 2: v1.9 Features)
**Backlog ref:** BLG-NEW-10 Phase 2
**Owner:** QA & Testing Owner
**Priority:** P1
**Effort:** Distributed (scenarios authored as each feature completes)
**Type:** QA — scenario authoring
**Depends on:** EPIC-01, EPIC-02, EPIC-03, EPIC-04, EPIC-06 feature delivery

**Acceptance Criteria:**
- Test scenarios authored for each new v1.9 feature at time of delivery:
  - EPIC-01: compliance metrics + reflection template scenarios
  - EPIC-02: cohort analysis + R-multiple distribution scenarios
  - EPIC-03: dashboard home scenarios
  - EPIC-04: all 11 deviation items verified in scenario form
  - EPIC-06: lifecycle compliance check scenarios (where applicable)
- No retroactive full-endpoint coverage mandate

---

### ST-13 — Service Layer Test Coverage Standard
**Backlog ref:** BLG-NEW-12
**Owner:** Backend Engineering Patterns Owner
**Priority:** P1
**Effort:** Small–Medium
**Type:** Engineering quality + CI

**Acceptance Criteria:**
- Service Layer Test Coverage Standard authored with named threshold (agreed at pre-alignment)
- CI step adds pytest-cov (or equivalent) coverage check on `backend/services/` directory
- Build fails if coverage falls below threshold
- Standard integrated with / referenced from `docs/specs/backend_engineering_patterns.md` (version incremented)
- Prerequisite BLG-NEW-01 (golden output baseline) confirmed complete ✅ (shipped v1.8)

---

## EPIC-06 — Documentation Hygiene & Governance
**Maps to:** S2-19 through S2-30

### ST-14 — Canonical Terms Glossary
**Backlog ref:** BLG-NEW-11
**Owner:** Head of Specs Team
**Priority:** P2
**Effort:** Small

**Acceptance Criteria:**
- Glossary created as Class 2 Supporting document with lifecycle-compliant header
- All key trading and system terms defined: portfolio heat, grace period, stop distance, R-multiple, cohort, and others as identified
- Each term includes definition + link to Class 1 canonical source
- No new canonical definitions introduced — cross-references only
- Registered in Specs_Index.md

---

### ST-15 — AI-Assisted Workflow Governance Policy
**Backlog ref:** BLG-NEW-04
**Owner:** Product Owner / AI Compliance & Governance Officer
**Priority:** P2
**Effort:** ~0.5 day

**Acceptance Criteria:**
- Policy document authored and filed under appropriate governance path
- Policy covers: AI authority scope, mandatory human review checkpoints, escalation triggers, record-keeping obligations
- Lifecycle-compliant header (Class + Owner + Status + Last Updated)

---

### ST-16 — Document GET /market/status Endpoint
**Backlog ref:** BLG-SPEC-D3
**Owner:** API Contracts & Documentation Owner
**Priority:** P2
**Effort:** Small

**Acceptance Criteria:**
- `docs/specs/api_contracts/market_endpoints.md` created (Class 1 Canonical, v0.1)
- Covers: GET /market/status request, response schema (SPY/FTSE regime, live FX rate), error behaviour
- Registered in Specs_Index.md §3
- Added to `docs/reference/openapi.yaml`

---

### ST-17 — Create settings_model.md
**Backlog ref:** BLG-SPEC-G1
**Owner:** Data Model & Domain Schema Owner
**Priority:** P2
**Effort:** Small

**Acceptance Criteria:**
- `docs/specs/data_model/settings_model.md` created (Class 1 Canonical, v0.1)
- Covers: settings schema, all field names, types, validation rules, defaults
- Registered in Specs_Index.md §3
- Cross-referenced from `docs/specs/api_contracts/settings_endpoints.md`
- Based on confirmed PATCH /settings/{settings_id} + POST /settings shape (resolved ST-09 v1.8)

---

### ST-18 — Define Error Response Standard
**Backlog ref:** BLG-SPEC-G2
**Owner:** API Contracts & Documentation Owner
**Priority:** P2
**Effort:** Small

**Acceptance Criteria:**
- Error Response Standard document created or added as section to existing canonical spec
- Covers: standard error envelope shape, required fields (status_code, error_code, message, detail), HTTP status code mapping
- All existing API contract docs updated to reference the Error Response Standard for their error sections
- Registered in Specs_Index.md

---

### ST-19 — Spec/Doc Debt Small Fixes
**Backlog ref:** BLG-SPEC-D1, BLG-SPEC-D4, BLG-SPEC-D8, BLG-SPEC-D9, BLG-SPEC-G3, BLG-SPEC-G4, BLG-SPEC-G5
**Owner:** Head of Specs Team (coordinator); individual domain owners per item
**Priority:** P3
**Effort:** Small per item (~30 min each; 3.5 hours total)

**Acceptance Criteria (per item):**
- BLG-SPEC-D1: `docs/specs/api_contracts/README.md` header + changelog updated to v1.9.0
- BLG-SPEC-D4: `position_endpoints.md` includes GET /positions/search/tags with parameters + response schema
- BLG-SPEC-D8: `docs/System_status_report.md` lifecycle header added (Owner, Class, Status, Version, Last Updated)
- BLG-SPEC-D9: `docs/governance/process_index.md` and `docs/specs/Specs_Index.md §5` updated to reference `claude/charter/document_lifecycle_guide.md`
- BLG-SPEC-G3: `docs/specs/Specs_Index.md §3` updated to include structured_logging_standards.md
- BLG-SPEC-G4: ADR-002 moved or confirmed present in `docs/product/decisions/`; cross-references updated
- BLG-SPEC-G5: `docs/specs/validation_system.md` owner field updated to a named governance role

---

## Story Item Summary

| ST-ID | EPIC | Title | Priority |
|-------|------|-------|----------|
| ST-01 | EPIC-01 | Canonicalise Basic Compliance Metrics | P2 |
| ST-02 | EPIC-01 | Structured Trade Reflection Template | P2 |
| ST-03 | EPIC-02 | Cohort Analysis | P2 |
| ST-04 | EPIC-02 | R-Multiple Distribution Report | P2 |
| ST-05 | EPIC-03 | Dashboard Homepage / Session Summary | P2 |
| ST-06 | EPIC-04 | Drawdown Data Source Spec Alignment | P2 |
| ST-07 | EPIC-04 | Risk Dashboard Backend: US Currency Conversion | P2 |
| ST-08 | EPIC-04 | Risk Dashboard Frontend: Error States & Entity Fallback | P2/P3 |
| ST-09 | EPIC-04 | Risk Dashboard Frontend: Table and Column Fixes | P2/P3 |
| ST-10 | EPIC-04 | Risk Dashboard Frontend: HeatGauge and Cosmetic Fixes | P3 |
| ST-11 | EPIC-05 | Canonical Test Scenario Library Phase 1 (Risk Dashboard) | P1 |
| ST-12 | EPIC-05 | Canonical Test Scenario Library Phase 2 (v1.9 Features) | P1 |
| ST-13 | EPIC-05 | Service Layer Test Coverage Standard | P1 |
| ST-14 | EPIC-06 | Canonical Terms Glossary | P2 |
| ST-15 | EPIC-06 | AI-Assisted Workflow Governance Policy | P2 |
| ST-16 | EPIC-06 | Document GET /market/status Endpoint | P2 |
| ST-17 | EPIC-06 | Create settings_model.md | P2 |
| ST-18 | EPIC-06 | Define Error Response Standard | P2 |
| ST-19 | EPIC-06 | Spec/Doc Debt Small Fixes (7 items) | P3 |

**Total story items: 19** spanning 6 EPICs and 30 S2 scope items.

---

## Recommended Sprint Sequencing

**Sprint start:**
1. ST-06 (drawdown spec alignment — parallel, no-code, must complete before verification)
2. ST-07 (backend currency conversion — backend-only, unblocks frontend)
3. ST-11 (seeded test infra Phase 1 — enables EPIC-04 verification + Risk Dashboard scenarios)
4. ST-01 (compliance metrics definitions — spec first, unblocks ST-02, ST-03, ST-04)

**Sprint mid:**
5. ST-08, ST-09, ST-10 (frontend Risk Dashboard fixes — after ST-07 backend deployed)
6. ST-13 (service coverage standard — independent)
7. ST-14–ST-19 (documentation hygiene — independent, can parallelise)

**Sprint late:**
8. ST-02 (reflection template — after ST-01 metrics canonical)
9. ST-03, ST-04 (analytics features — after ST-01 metrics canonical)
10. ST-05 (dashboard homepage — independent but last due to composite endpoint decision)
11. ST-12 (Phase 2 test scenarios — as each feature completes)
