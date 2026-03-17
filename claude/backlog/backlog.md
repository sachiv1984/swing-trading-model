# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-03-17 (v2.0 delivery verification — 3 items added: TEST-GAP-SIG-01, TEST-GAP-TAX-01, BLG-PROC-01; 2 v2.0 items closed: TEST-GAP-EPIC-02, BLG-BE-02)
**Last rebalance:** 2026-03-17 (cycle 2026-03-17__item-v1.10 — DL-009)

> ⚠️ Standing Notice
> This backlog records prioritisation and intent only.
> All formulas, schemas, API contracts, and behavioural rules are indicative until
> confirmed in the relevant canonical specifications.
> No item may proceed to implementation without canonical owner sign-off.

*Completed and killed items are recorded in `claude/backlog/backlog_archive.md`.*

---

## Priority Definitions

- **P0 — Critical**: Blocks correctness, trust, or release safety
- **P1 — High**: Enables core workflows or governance
- **P2 — Medium**: High leverage but not blocking
- **P3 — Low**: Nice-to-have or future scale

---

## 1. Platform & Validation Governance Backlog

These items ensure analytical correctness, validation integrity, and operational safety.
They are not user-facing, but they directly affect trust in outputs and release confidence.

---

### BLG-TECH-05 — Prometheus metrics endpoint
**Priority:** P3 (Low)
**Type:** Observability
**Target release:** v2.1 (or when system becomes multi-user)

**Scope**
- Add `GET /metrics` Prometheus endpoint exposing:
  - Validation run count
  - Failure count by metric and severity
  - Validation duration
- Optional Grafana dashboard.

**Acceptance Criteria**
- Metrics scrape successfully in Prometheus format.
- Counters and histograms are correct.

---

## 2. Product Feature Backlog (User-Facing)

---

### BLG-FEAT-03 — Slippage Tracking
**Priority:** P2
**Target release:** v2.1
**Effort:** Low–Medium (data model update required — schema migration + trade entry capture logic + display)

Track and display trade slippage per trade and as a portfolio average.

**Indicative Formula**

`(Fill Price - Market Price) / Market Price`

Requires data model update — Fill Price must be captured at trade entry (not currently stored). This is the primary pre-work gate: `data_model.md` must define the Fill Price field and migration path before implementation begins.

> **Disposition (2026-03-15 — Product Owner):** Assigned to v2.1 alongside Chart Interactivity and Watchlists. No displacement required — v2.1 is not yet planned. Pull into v2.1 release planning when capacity is available. Orphan status resolved.

---

## 3. Deferred / v2.1 Candidates

- Daily email portfolio summary
- FX rate history tracking
- Prometheus validation observability (BLG-TECH-05)
- Position correlation analysis
- Backtesting module
- Multi-portfolio support
- Mobile app
- Full compliance scoring system

---

## 4. Explicitly Out of Scope (Product-Level)

These are deliberate product decisions, not deferrals:

- Broker API integration
- Automated trading execution
- Configurable strategy builder
- ML-based predictions
- Social / community features
- Options and futures trading support

---

## 5. Lifecycle Governance Notes

- This backlog is not canonical and must never override:
  - Strategy rules
  - Metrics definitions
  - API contracts
- Any shipped feature must be backed by:
  - Canonical specification
  - Updated validation where applicable
- Once implemented, backlog items are superseded by canonical documentation.

---

## 6. New Backlog Items — Cycle 2026-03-15__item-5.3 and Later

---

Items promoted to backlog from idea pool during roadmap rebalance cycle 2026-03-15__item-5.3, and items raised during v1.10 sprint execution and QA sign-off.

---

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

### BLG-SPEC-G6 — `total_return_pct` not returned by GET /analytics/metrics
**Priority:** P3 (Low)
**Type:** Backend / Spec Gap
**Owner:** Head of Engineering + Metrics Definitions & Analytics Canonical Owner
**Source:** ST-17 Spec Coverage Inventory — A-01 (2026-03-17)
**Cycle added:** 2026-03-17__release-v2.0
**Target release:** v2.1

`analytics_endpoints.md` explicitly notes: "`total_return_pct` is not yet returned by `GET /analytics/metrics`." The canonical formula is documented (`total_pnl / net_cash_flow × 100`) but the field is absent from the API response. This creates a spec-to-implementation gap.

**Scope**
- Implement `total_return_pct` in `GET /analytics/metrics` response per documented formula
- Remove the "not yet returned" note from `analytics_endpoints.md` once implemented

**Acceptance Criteria**
- `GET /analytics/metrics` returns `total_return_pct` matching the canonical formula
- `analytics_endpoints.md` updated to reflect field as implemented

---

### BLG-SPEC-D10 — `api_dependencies.md` does not reflect v2.0 additions
**Priority:** P3 (Low)
**Type:** Spec Document Maintenance
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-17 Spec Coverage Inventory — A-02 (2026-03-17)
**Cycle added:** 2026-03-17__release-v2.0
**Target release:** v2.0 post-ship

`docs/specs/frontend/patterns/api_dependencies.md` (v1.1, 2026-02-19) maps surfaces to endpoints. The v2.0 additions (Reports page — `GET /reports/tax-year`; Signals controls — `GET /signals?top_n=&lookback_days=`) are not yet reflected.

**Acceptance Criteria**
- `api_dependencies.md` updated to include Reports page and updated Signals page endpoint mappings
- Version bumped; `Last Updated` set

---

### BLG-SPEC-D11 — `data_model.md` §501 trade_reflections section not updated to complete
**Priority:** P3 (Low)
**Type:** Spec Document Maintenance
**Owner:** Data Model & Domain Schema Owner
**Source:** ST-17 Spec Coverage Inventory — A-03 (2026-03-17)
**Cycle added:** 2026-03-17__release-v2.0
**Target release:** v2.1

`data_model.md §501 "Planned Future Schema Changes"` still shows the trade_reflections table as a planned v1.9 change. It was implemented in v1.9 Sprint 1. The section should be updated to mark this as complete (or the entire entry moved/removed).

**Acceptance Criteria**
- `data_model.md §501` trade_reflections entry updated to reflect implemented status
- Version bumped

---

### BLG-SPEC-D12 — Bulk lifecycle header remediation — 28 non-compliant spec documents
**Priority:** P2 (Medium)
**Type:** Governance / Spec Compliance
**Owner:** Head of Specs Team
**Source:** ST-17 Spec Coverage Inventory — A-04 (2026-03-17)
**Cycle added:** 2026-03-17__release-v2.0
**Target release:** v2.1

28 of 38 spec documents (74%) are missing `Class` and/or `Lifecycle Guide` header fields per `document_lifecycle_guide.md v2.6`. All non-compliant documents pre-date lifecycle guide adoption. A bulk update pass is required.

Full list in `docs/specs/spec_coverage_inventory.md §9`. Most affected: `api_contracts/*.md` (8 files), `frontend/components/*.md` (5 files), `frontend/patterns/*.md` (2 files), `frontend/pages/*.md` (4 files), `data_model.md`, `metrics_definitions.md`.

**Scope**
- Add `Class: [Canonical Specification (Class 1) | Supporting (Class 2)]` to each document per its domain
- Add `**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md` to each document
- Bump version on each document modified
- No content changes — header compliance only

**Acceptance Criteria**
- All 28 listed documents carry compliant lifecycle headers
- `spec_coverage_inventory.md §9` compliance count updated to 38/38

---

### BLG-SPEC-D13 — `metrics_definitions.md` Owner field lists team name, not governance role
**Priority:** P2 (Medium)
**Type:** Governance / Spec Compliance
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** ST-17 Spec Coverage Inventory — A-05 (2026-03-17)
**Cycle added:** 2026-03-17__release-v2.0
**Target release:** v2.1

`metrics_definitions.md` lists `Owner: Analytics Team`. Per `document_lifecycle_guide.md §7`, the Owner field must be a named governance role, not a team name. The correct role is `Metrics Definitions & Analytics Canonical Owner`.

**Acceptance Criteria**
- `metrics_definitions.md` `Owner` updated to `Metrics Definitions & Analytics Canonical Owner`
- Version bumped

---

### TEST-GAP-SIG-01 — Test scenario coverage gap: Signals page controls (v2.0)
**Priority:** P3
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner
**Source:** TSG-v20-01 — verification_report.md §6, cycle 2026-03-17__release-v2.0
**Cycle added:** 2026-03-17__release-v2.0
**Target release:** before next sprint touching signals page

Test scenario coverage gap from 2026-03-17__release-v2.0: QA & Testing Owner to author scenarios for signals page controls (ST-02). Create `docs/testing/signals_scenarios.md` covering:
- SC-SIG-01: Controls render with correct defaults (top_n=5, lookback_days=252); changing either fires GET /signals with updated params after 500ms debounce
- SC-SIG-02: Invalid input (0 or negative) resets to default; no API call made
- SC-SIG-03: Empty state when API returns no signals; controls remain active
Spec references: `docs/specs/frontend/pages/signals.md v0.1 §Controls/§Validation/§Empty State`

---

### TEST-GAP-TAX-01 — Test scenario coverage gap: Tax Year P&L report (v2.0)
**Priority:** P3
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner
**Source:** TSG-v20-02 — verification_report.md §6, cycle 2026-03-17__release-v2.0
**Cycle added:** 2026-03-17__release-v2.0
**Target release:** before next sprint touching reports or tax year functionality

Test scenario coverage gap from 2026-03-17__release-v2.0: QA & Testing Owner to author scenarios for the Tax Year P&L report frontend and boundary. Create `docs/testing/reports_scenarios.md` covering:
- SC-TAX-01: Year selector defaults to current tax year; changing year triggers API re-fetch; summary bar updates
- SC-TAX-02: Empty state when no closed trades in selected year
- SC-TAX-03: Tax year boundary — trade exited 5 Apr YYYY → year YYYY-1; trade exited 6 Apr YYYY → year YYYY
Note: 29 backend integration tests exist in `tests/test_reports_integration.py` (these need not be duplicated).
Spec references: `docs/specs/frontend/pages/reports.md v0.1`; `docs/specs/api_contracts/reports_endpoints.md v0.1 §Tax Year Boundary`

---

### BLG-PROC-01 — Process adherence: cross-EPIC branch commits (v2.0 deviation follow-up)
**Priority:** P3
**Type:** Process / Governance
**Owner:** PMO Lead
**Source:** DEV-v2.0-01 — ST-20 cross-branch process deviation, cycle 2026-03-17__release-v2.0
**Cycle added:** 2026-03-17__release-v2.0
**Target release:** v2.1 sprint retrospective

CLAUDE.md §2 action-now patch applied ("Story commits must land on the branch matching their EPIC prefix"). This item tracks compliance at next sprint execution. At the next sprint close, PMO Lead to confirm: (a) no cross-EPIC commits occurred, or (b) any occurring were escalated and documented. If 3+ sprints pass with zero recurrence, this item may be closed as pattern established.

---

## Closed Items

Items archived in `claude/backlog/backlog_archive.md`. Listed most recent first.

| Item ID | Title | Shipped | Cycle | Story |
|---------|-------|---------|-------|-------|
| TEST-GAP-EPIC-02 | CohortAnalysis backend integration regression scenario | v2.0 | 2026-03-17__release-v2.0 | EPIC-05/ST-20 |
| BLG-BE-02 | Spec and implement GET /portfolio/prospective-heat | v2.0 | 2026-03-17__release-v2.0 | EPIC-04/ST-13 |
| BLG-NEW-13 | Spec Coverage Inventory | v2.0 | 2026-03-17__release-v2.0 | EPIC-05/ST-17 |
| BLG-BE-01 | GET /portfolio missing 4 required fields (GAP-03) | v2.0 | 2026-03-17__release-v2.0 | EPIC-04/ST-12 |
| BLG-OPS-02 | Production Deployment Runbook | v2.0 | 2026-03-17__release-v2.0 | EPIC-05/ST-14 |
| BLG-DATA-01 | Positions Table Data Dictionary | v2.0 | 2026-03-17__release-v2.0 | EPIC-05/ST-15 |
| BLG-TECH-07 | Database Migration Governance Standard | v2.0 | 2026-03-17__release-v2.0 | EPIC-05/ST-16 |
| BLG-OPS-01 | Provision development environment | v1.10 | 2026-03-15__release-v1.10 | EPIC-01/ST-01–ST-03 |
| BLG-TECH-06 | Fix CohortAnalysis client-side computation | v1.10 | 2026-03-15__release-v1.10 | EPIC-02/ST-04 |
| BLG-API-01 | Backend API integration tests (FastAPI TestClient) | v1.10 | 2026-03-15__release-v1.10 | EPIC-03/ST-05–ST-06 |
| TEST-GAP-EPIC-06 | v1.7 test scenario coverage gap (BLG-QA-01) | v1.10 | 2026-03-15__release-v1.10 | EPIC-03/ST-07 |
| BLG-FEAT-08 | Basic Compliance Metrics | v1.9 Sprint 2 | 2026-03-06__release-v1.9 | EPIC-03/ST-01 |
| BLG-NEW-09 | R-Multiple Distribution Report | v1.9 Sprint 2 | 2026-03-06__release-v1.9 | EPIC-02/ST-04 |
| BLG-NEW-10 | Canonical Test Scenario Library | v1.9 | 2026-03-06__release-v1.9 | EPIC-05/ST-11, ST-12 |
| BLG-RD-01 | Entity store fallback masks API error states | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-08 |
| BLG-RD-02 | GracePeriodPanel empty vs error state | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-08 |
| BLG-RD-03 | PositionRiskTable sorted descending | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-04 | Stop Price column absent | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-05 | GRACE badge colour amber instead of blue | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-10 |
| BLG-RD-06 | GBP value at risk absent from HeatGauge | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-10 |
| BLG-RD-07 | Days in Grace column absent | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-08 | Drawdown data source resolved | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-06 |
| BLG-RD-09 | ProspectiveHeatPanel missing threshold label | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-10 | US entry prices in USD not GBP | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-07 |
| BLG-RD-11 | current_stop in USD for US positions | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-07 |
| TEST-GAP-EPIC-01 | Risk Dashboard scenario execution infrastructure gap | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-11 |
| BLG-NEW-04 | AI-Assisted Workflow Governance Policy | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-15 |
| BLG-NEW-11 | Canonical Terms Glossary | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-14 |
| BLG-NEW-12 | Service Layer Test Coverage Standard | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-13 |
| BLG-SPEC-D1 | API Contracts README version frozen | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-D3 | GET /market/status undocumented | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-16 |
| BLG-SPEC-D4 | GET /positions/search/tags undocumented | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-D8 | System_status_report.md missing header | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-D9 | Broken cross-references to lifecycle guide | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-G1 | settings_model.md missing | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-17 |
| BLG-SPEC-G2 | Error Response Standard not defined | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-18 |
| BLG-SPEC-G3 | structured_logging_standards.md not in Specs Index | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-G4 | ADR-002 in wrong location | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-G5 | validation_system.md owner field non-compliant | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-NEW-08 | Automated OpenAPI Drift Detection in CI | v1.8 | 2026-03-04__release-v1.8 | ST-08 |
| BLG-NEW-07 | Running API Changelog Document | v1.8 | 2026-03-04__release-v1.8 | ST-12 |
| BLG-NEW-05 | Dependency Vulnerability Scanning in CI | v1.8 | 2026-03-04__release-v1.8 | ST-07 |
| BLG-NEW-03 | Define and Document Unavailability Failure Mode | v1.8 | 2026-03-04__release-v1.8 | ST-11 |
| BLG-NEW-02 | Backtest vs Live Stop Reconciliation Report | v1.8 | 2026-03-04__release-v1.8 | ST-06 |
| BLG-NEW-01 | Golden Output Regression Baseline for CI | v1.8 | 2026-03-04__release-v1.8 | ST-05 |
| BLG-SPEC-D7 | openapi.yaml frozen at v1.8.1 | v1.8 | 2026-03-04__release-v1.8 | ST-10 |
| BLG-SPEC-D2 | settings_endpoints.md spec/implementation mismatch | v1.8 | 2026-03-04__release-v1.8 | ST-09 |
| BLG-NEW-06 | Realised vs Unrealised P&L Labelling | N/A | 2026-03-04__item-3.4 | Merged into 4.1b |

---

### BLG-TECH-08 — Async notification delivery architecture decision record
**Priority:** P2 (Medium)
**Type:** Architecture / Engineering Decision
**Owner:** Head of Engineering + Backend Engineering Patterns Owner
**Source:** QA notification planning session 2026-03-17 (qa_notification_planning.md — DL-003 session output)
**Cycle added:** 2026-03-17__release-v2.0 (post-planning session)
**Effort:** S (~0.5–1 day)
**Target release:** v2.1 (prerequisite — must be completed before v2.1 sprint planning seals for EPIC-03)

**Problem**
Before 3.5 Alerts (EPIC-03) can be specced or implemented, an architectural decision must be made on notification delivery: (a) synchronous inline delivery (email sent on the API response that triggers the alert — simpler, no infrastructure change), or (b) asynchronous delivery via a background worker + task queue (Celery + Redis or equivalent — more scalable but requires adding worker infrastructure to the current synchronous FastAPI application). Without this decision, the notification spec (ST-06) cannot be written to a stable baseline.

**Scope**
- Document trade-offs of sync vs. async notification delivery for current single-user deployment
- Produce an Architecture Decision Record (ADR) capturing: options considered, decision, rationale, consequences
- File as `docs/adr/ADR-NNN-notification-delivery-architecture.md`
- Update `backend_engineering_patterns.md` with the decision reference

**Acceptance Criteria**
- ADR produced covering: sync inline email vs. async worker + queue
- Decision recorded with rationale appropriate to current scale (single-user, self-hosted)
- If async decided: spike or proof of concept for worker setup confirmed feasible in staging
- Head of Engineering sign-off obtained
- Sprint Planning Engine must verify this item is Complete before sealing v2.1 sprint backlog containing any EPIC-03 story

---

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

### BLG-OPS-03 — Pre-merge preview environments (Render PR previews)
**Priority:** P2 (Medium)
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** DoQ sign-off session — 2026-03-17 (identified during v2.0 staging verification gap)
**Cycle added:** 2026-03-17__release-v2.0
**Effort:** S (~0.5 day)
**Target release:** v2.1

**Problem**
Staging auto-deploys from `main`, so feature branch changes can only be verified on staging after merging. During v2.0 sign-off, the Director of Quality could not verify frontend behaviour (ST-02 Signals controls, ST-05 Tax Year view) on a deployed environment without merging first. This is a process gap: the merge gate should be verifiable before merge, not after.

**Scope**
- Enable Render Preview Environments on the existing Render Blueprint (one-click in Render dashboard)
- Each PR automatically gets a unique preview URL (`https://trading-assistant-api-pr-{N}.onrender.com`)
- Preview environments share the staging Supabase DB (acceptable at current scale)
- Document the preview URL pattern in `OPERATIONAL_GUIDE.md §8` and add to DoQ sign-off checklist

**Acceptance Criteria**
- Opening a PR against `main` automatically provisions a Render preview environment
- Preview URL is accessible and points to the PR branch's backend code
- `OPERATIONAL_GUIDE.md §8` documents the preview URL pattern
- DoQ can verify frontend behaviour on the preview URL before approving merge

---

<!-- release-plan-marker: RP:v2.0:2026-03-17__release-v2.0 -->

---

## 7. v2.0 Release Slice — Reporting & Alerts

*Planned: 2026-03-17 | Cycle: 2026-03-17__release-v2.0 | Backlog slice: claude/cycles/2026-03-17__release-v2.0/stage4_backlog_slice.md*

| EPIC | Story | Title | Priority | Effort | Conditional |
|------|-------|-------|----------|--------|-------------|
| EPIC-01 | ST-01 | Author signals page frontend spec | P2 | S | No |
| EPIC-01 | ST-02 | Implement top_n + lookback_days controls on signals page | P2 | S | No |
| EPIC-02 | ST-03 | Author tax-year P&L report spec | P2 | S–M | No |
| EPIC-02 | ST-04 | Implement GET /reports/tax-year endpoint | P2 | M | No |
| EPIC-02 | ST-05 | Frontend: tax-year P&L report view | P2 | M | No |
| ~~EPIC-03~~ | ~~ST-06~~ | ~~Spec: alerts endpoint + notification preference model~~ | ~~P2~~ | ~~M~~ | **Deferred to v2.1** (DoQ session 2026-03-17) |
| ~~EPIC-03~~ | ~~ST-07~~ | ~~Backend: alert rules engine~~ | ~~P2~~ | ~~M–H~~ | **Deferred to v2.1** |
| ~~EPIC-03~~ | ~~ST-08~~ | ~~Backend: notification delivery (email)~~ | ~~P2~~ | ~~M~~ | **Deferred to v2.1** |
| ~~EPIC-03~~ | ~~ST-09~~ | ~~Frontend: notification preferences page~~ | ~~P2~~ | ~~S–M~~ | **Deferred to v2.1** |
| ~~EPIC-03~~ | ~~ST-10~~ | ~~Frontend: in-app notification feed~~ | ~~P2~~ | ~~S–M~~ | **Deferred to v2.1** |
| ~~EPIC-03~~ | ~~ST-11~~ | ~~QA: notification delivery test scenarios~~ | ~~P2~~ | ~~S~~ | **Deferred to v2.1** — DL-003 session complete; gate documented; prerequisite BLG-TECH-08 required |
| EPIC-04 | ST-12 | Fix GET /portfolio missing 4 fields (BLG-BE-01 P1) — **Sprint 1 item 1** | P1 | S | No |
| EPIC-04 | ST-13 | Spec + implement GET /portfolio/prospective-heat (BLG-BE-02 stretch) | P3 | M | No (stretch) |
| EPIC-05 | ST-14 | BLG-OPS-02: Production Deployment Runbook | P2 | S | No |
| EPIC-05 | ST-15 | BLG-DATA-01: Positions Table Data Dictionary | P2 | S | No |
| EPIC-05 | ST-16 | BLG-TECH-07: Database Migration Governance Standard | P2 | S | No |
| EPIC-05 | ST-17 | BLG-NEW-13: Spec Coverage Inventory | P2 | M | No |
| EPIC-06 | ST-18 | BLG-GOV-01: Roadmap stage document consolidation | P2 | M | No |
| EPIC-06 | ST-19 | BLG-GOV-02: Ideas register | P2 | M | No |
| EPIC-05 | ST-20 | TEST-GAP-EPIC-02: CohortAnalysis regression scenario (stretch) | P3 | S | No (stretch) |

*Full acceptance criteria in stage4_backlog_slice.md.*

---

*For delivery history, see `docs/product/changelog.md`.*
*For the active roadmap, see `claude/roadmap/current_roadmap.md`.*
