# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-03-17 (roadmap rebalance — cycle 2026-03-17__item-v1.10 — DL-009 — 3 items added)
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

### BLG-OPS-02 — Production Deployment Runbook
**Priority:** P2 (Medium)
**Type:** Operations / Documentation
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260304-01 (IW-20260304-01 — promoted 2026-03-17)
**Cycle added:** 2026-03-17__item-v1.10
**Effort:** S (~0.5–1 day)
**Target release:** v2.0

**Problem**
v1.10 shipped the staging environment (BLG-OPS-01), but there is no documented procedure for deploying to production. The deployment process is informal — no runbook, no rollback procedure, no checkpoint list. With staging now separate from production, an undocumented deployment workflow is an operational risk.

**Scope**
- Document the production deployment procedure: steps from staging-verified build to production push
- Include: pre-deployment checklist, deployment steps, post-deployment verification, rollback procedure
- Cross-reference staging environment configuration (BLG-OPS-01 output)
- Store as `docs/ops/production_deployment_runbook.md` (Class 2 Supporting document)

**Acceptance Criteria**
- Production deployment runbook exists at `docs/ops/production_deployment_runbook.md`
- Runbook includes: pre-deployment checklist, deployment steps, verification steps, rollback procedure
- Reviewed and signed off by Head of Engineering

---

### BLG-DATA-01 — Positions Table Data Dictionary
**Priority:** P2 (Medium)
**Type:** Data Documentation / Spec
**Owner:** Data Model Domain & Schema Owner
**Source:** IDEA-data-model-owner-20260304-01 (IW-20260304-01 — promoted 2026-03-17)
**Cycle added:** 2026-03-17__item-v1.10
**Effort:** S (~0.5–1 day)
**Target release:** v2.0
**Scope constraint:** Positions table only (not all tables). Complements BLG-NEW-13 (Spec Coverage Inventory) — distinct scope: this is field-level semantics documentation, not coverage mapping.

**Problem**
The positions table has no formal data dictionary. BLG-BE-01 (GET /portfolio missing 4 fields) surfaced the risk — field semantics are under-documented, making spec/implementation divergence hard to detect. A data dictionary provides the authoritative reference for field naming, types, constraints, and derivation rules.

**Scope**
- Document each field in the `positions` table: name, type, nullable, description, derivation rule where applicable
- Cross-reference `portfolio_endpoints.md` and `data_model.md` for existing definitions
- Store as a Class 2 Supporting document under `docs/specs/data_model_positions_dictionary.md`
- Flag any fields without canonical definitions as gaps for follow-up

**Acceptance Criteria**
- Data dictionary covers all fields in the `positions` table
- Each field documented: name, type, nullable, description, derivation (where applicable)
- Cross-references to canonical spec sections where definitions exist
- Gap list produced for any undocumented fields
- Registered in `docs/specs/Specs_Index.md`

---

### BLG-TECH-07 — Database Migration Governance Standard
**Priority:** P2 (Medium)
**Type:** Engineering Governance / Process
**Owner:** Backend Engineering Patterns Owner + Head of Engineering
**Source:** IDEA-backend-engineering-20260304-02 (IW-20260304-01 — promoted 2026-03-17)
**Cycle added:** 2026-03-17__item-v1.10
**Effort:** S (~0.5–1 day)
**Target release:** v2.0

**Problem**
No documented process exists for how database schema migrations are created, reviewed, applied, and rolled back. v2.0 will introduce schema changes (4.1b Tax-Year P&L will require a new report table or schema update). An undocumented migration process is an operational risk — if a migration partially applies, there is no documented recovery path.

**Scope**
- Define migration naming convention
- Define required migration file fields: description, reversibility assessment, rollback SQL
- Define review requirements: second-engineer review, schema owner sign-off for structural changes
- Define production application procedure: transaction where possible, staging-tested first
- Define incident procedure if migration fails mid-apply
- Store as `docs/ops/database_migration_governance.md` (Class 2 Supporting; reference from `backend_engineering_patterns.md`)

**Acceptance Criteria**
- Migration governance standard exists at `docs/ops/database_migration_governance.md`
- Covers: naming convention, required fields, review requirements, application procedure, incident procedure
- Cross-referenced from `backend_engineering_patterns.md` as new §N
- Head of Engineering sign-off obtained

Items promoted to backlog from idea pool during roadmap rebalance cycle 2026-03-15__item-5.3, and items raised during v1.10 sprint execution and QA sign-off.

---

### BLG-NEW-13 — Spec Coverage Inventory
**Priority:** P2 (Medium)
**Type:** Governance / Spec
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260304-02 (IW-20260304-01 — promoted 2026-03-15)
**Cycle added:** 2026-03-15__item-5.3
**Effort:** ~1–2 days (analysis + documentation)
**Target release:** v2.0 (or v1.10 if capacity allows)

Systematic audit of all canonical spec sections (docs/specs/) against implementation coverage. Produces a living inventory identifying which spec sections are tested, which are partially covered, and which have no coverage or implementation verification. Complements BLG-NEW-11 (Canonical Terms Glossary). Creates an actionable gap list for future backlog prioritisation.

**Scope**
- Review all docs/specs/ sections against live implementation and test coverage
- Rate each section: covered / partial / gap
- Cross-reference open backlog items against identified gaps
- Define a review cadence (e.g. per audit cycle or per major release)
- Output: a structured Coverage Inventory document (Class 2 Supporting document)

**Acceptance Criteria**
- Coverage Inventory document produced covering all docs/specs/ sections
- Each spec section rated: covered / partial / gap
- Gap items cross-referenced against open backlog items where possible
- Review cadence defined
- Registered in Specs_Index.md

---

### BLG-BE-01 — GET /portfolio missing 4 required fields (GAP-03 finding)
**Priority:** P1
**Type:** Backend Bug
**Owner:** Head of Engineering
**Source:** GAP-03 staging execution — DoQ sign-off 2026-03-16 (EPIC-03 ST-07)
**Cycle added:** 2026-03-15__release-v1.10
**Target release:** v1.11

**Problem**
`GET /portfolio` does not return `initial_value`, `net_deposits`, `current_drawdown_percent`, or `peak_portfolio_value` in the staging API response. These 4 fields are required by `portfolio_endpoints.md` v1.9.0 (added at v1.8.2 per changelog). The backend implementation is diverged from the spec.

**Evidence**
Staging response (`2026-03-16`) contained only: `cash`, `cash_balance`, `total_value`, `open_positions_value`, `total_pnl`, `last_updated`, `live_fx_rate`, `portfolio_heat_percent`, `position_risks`, `positions`. The 4 fields above were absent.

**Scope**
- Add `initial_value` (portfolio initial capital value in GBP)
- Add `net_deposits` (total deposits minus total withdrawals — cost basis for portfolio-level return)
- Add `current_drawdown_percent` (current value vs all-time peak; default `0.0` when no history)
- Add `peak_portfolio_value` (all-time high of portfolio_history.total_value; default `0.0` when no history)
- Per `portfolio_endpoints.md` §GET /portfolio and §Field Derivation Notes
- Update ST-05 integration tests (`tests/test_portfolio_integration.py`) to assert these 4 fields

**Acceptance Criteria**
- `GET /portfolio` response includes all 4 fields with correct values
- `current_drawdown_percent` and `peak_portfolio_value` default to `0.0` when no portfolio_history exists
- `net_deposits` equals total deposits minus total withdrawals
- ST-05 integration tests extended to assert these fields
- GAP-03 scenario (`docs/testing/v1.7-qa-scenario-gaps.md`) passes on staging

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

## Closed Items

Items archived in `claude/backlog/backlog_archive.md`. Listed most recent first.

| Item ID | Title | Shipped | Cycle | Story |
|---------|-------|---------|-------|-------|
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

*For delivery history, see `docs/product/changelog.md`.*
*For the active roadmap, see `claude/roadmap/current_roadmap.md`.*
