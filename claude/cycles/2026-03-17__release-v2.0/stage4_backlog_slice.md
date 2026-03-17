**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.0
**Cycle:** 2026-03-17__release-v2.0
**Last Updated:** 2026-03-17

---

# Sprint Backlog Slice — v2.0 Reporting & Alerts

---

## EPIC-01 — 4.3 Signal Exposure Enhancement

**Maps to:** S2-03
**Effort:** S (~3–5 hrs total)
**Owner:** Base44 Frontend + Head of Specs Team
**Sprint:** 1 (no dependencies; quick win)

### ST-01 — Author signals page frontend spec

**Type:** Spec
**Effort:** S (~1–2 hrs)
**Owner:** Head of Specs Team + Base44 Frontend Prompt Owner
**Delegation:** Delegated (spec authoring within existing architectural pattern)

**Description:** Create `docs/specs/frontend/pages/signals.md` defining the signals page with `top_n` and `lookback_days` as user-facing controls. Document: control placement, default values (top_n=5, lookback_days=252 per signal_endpoints.md), input validation, and how the page re-fetches `GET /signals` on control change.

**Acceptance Criteria**
- `docs/specs/frontend/pages/signals.md` created as Class 2 Supporting document
- Defines top_n control (integer, positive, default 5) and lookback_days control (integer, positive, default 252)
- Specifies how page triggers re-fetch on value change
- Cross-references `docs/specs/api_contracts/signal_endpoints.md` parameter definitions
- Registered in `docs/specs/Specs_Index.md`
- Head of Specs Team sign-off obtained

---

### ST-02 — Implement top_n and lookback_days controls on signals page

**Type:** Frontend implementation
**Effort:** S (~2–3 hrs)
**Owner:** Base44 Frontend
**Delegation:** Delegated (UI implementation against existing backend endpoint)
**Depends on:** ST-01 (signals page spec must be signed off)

**Description:** Implement the controls defined in ST-01 spec on the signals page in the Base44 frontend. Pass `top_n` and `lookback_days` as query parameters to `GET /signals`. Controls should be visible and clearly labelled. Default to spec values (5 and 252).

**Acceptance Criteria**
- top_n and lookback_days controls rendered on signals page with correct defaults
- Changing either control triggers a new `GET /signals` request with updated parameters
- Signal list updates to reflect new parameters
- Invalid inputs (non-positive integers) handled gracefully (validation or disabled state)
- All existing signals page behaviour preserved
- Director of Quality sign-off obtained (QA against staging)

---

## EPIC-02 — 4.1b Tax-Year P&L Statement

**Maps to:** S2-02
**Effort:** Low–Medium (~10–16 hrs total)
**Owner:** Head of Specs Team + Head of Engineering + Base44 Frontend
**Sprint:** 1 (spec); Sprint 2 (implementation)
**Note:** Realised vs Unrealised P&L labelling (BLG-NEW-06, merged into 4.1b) must be covered in ST-03 spec.

### ST-03 — Author tax-year P&L report spec

**Type:** Spec
**Effort:** S–M (~2–4 hrs)
**Owner:** Head of Specs Team + Financial Reporting & Records Owner
**Delegation:** Delegated

**Description:** Author the tax-year P&L endpoint spec. Define `GET /reports/tax-year?year=YYYY` (or equivalent path). Specify: response schema, GBP-adjustment rules, fee inclusion, realised/unrealised distinction, tax-year boundaries (UK: 6 April to 5 April). Must be a separate spec file from portfolio_endpoints.md (per roadmap: "This is a financial record, not an analytics view — it requires its own canonical specification").

**Acceptance Criteria**
- New spec file `docs/specs/api_contracts/reports_endpoints.md` created (or financial_reporting_endpoints.md)
- `GET /reports/tax-year` defined: path, query params, response schema, error responses
- Response includes: all realised trades in tax year, per-trade P&L (GBP, fee-inclusive), tax-year total P&L, currency conversion notes
- Realised vs unrealised P&L clearly distinguished in response (per BLG-NEW-06 merged pre-work)
- Tax-year boundary defined (UK: 6 April to 5 April) or parameterised
- Cross-references `data_model.md` and `metrics_definitions.md` for derivation rules
- Registered in `docs/specs/Specs_Index.md`
- Head of Specs Team + Financial Reporting & Records Owner sign-off obtained

---

### ST-04 — Implement GET /reports/tax-year endpoint

**Type:** Backend
**Effort:** M (~4–8 hrs)
**Owner:** Head of Engineering
**Delegation:** Delegated
**Depends on:** ST-03 (spec signed off); ST-16 (migration governance) recommended before any schema change

**Description:** Implement the tax-year P&L endpoint in `backend/main.py` per ST-03 spec. Query all closed trades in the specified tax year (filtering by close_date), apply GBP conversion, include fees, distinguish realised vs unrealised. If a new table or schema migration is required, apply migration governance standard (ST-16) first.

**Acceptance Criteria**
- `GET /reports/tax-year?year=YYYY` returns correctly structured response per ST-03 spec
- All closed trades in the tax year included; open positions excluded from realised figures
- GBP conversion applied correctly for non-GBP positions
- Fees included in net P&L calculation
- Response correctly distinguishes realised vs unrealised amounts
- Returns 400 for invalid year; 200 with empty trades array if no trades in year
- Integration tests added in `tests/test_reports_integration.py`
- Director of Quality sign-off obtained (staging verification)

---

### ST-05 — Frontend: tax-year P&L report view

**Type:** Frontend
**Effort:** M (~3–5 hrs)
**Owner:** Base44 Frontend
**Delegation:** Delegated
**Depends on:** ST-04 (backend endpoint implemented)

**Description:** Implement the tax-year P&L report view in the Base44 frontend. Year selector. Table of closed trades with per-trade GBP P&L. Summary row: total realised P&L for tax year. Realised/unrealised distinction visible. Accessible from the analytics or portfolio section.

**Acceptance Criteria**
- Tax-year P&L report page accessible in frontend
- Year selector defaults to current tax year; navigable to prior years
- Table shows all closed trades in year: date, ticker, entry/exit price, GBP P&L, fees
- Summary shows total realised P&L for tax year, clearly labelled as realised (not unrealised)
- Empty state handled ("No closed trades in this tax year")
- Director of Quality sign-off obtained (QA against staging)

---

## EPIC-03 — 3.5 Alerts & Notifications *(Conditional — QA Gate 3 Required)*

**Maps to:** S2-01
**Effort:** Medium–High (~24–40 hrs total)
**Owner:** Head of Engineering + Base44 Frontend + Director of Quality
**Sprint:** 2 (if QA gate clears before sprint planning seal) OR Deferred to v2.1
**Condition:** QA gate 3 (DL-003) — QA planning session for notification delivery — must be completed and documented before EPIC-03 enters sprint execution. Session must specify: test types required, notification delivery modes to be tested, expected test infrastructure.

### ST-06 — Spec: alerts endpoint + notification preference model

**Type:** Spec
**Effort:** M (~3–5 hrs)
**Owner:** Head of Specs Team
**Delegation:** Delegated (conditional on QA gate)

**Description:** Author alert rules spec and notification preference API spec. Define: alert types (stop loss approach, grace period ending warning, market regime change to risk-off, daily summary), delivery modes (email, optional SMS), preference model (per-user, per-alert-type, on/off). Create `docs/specs/api_contracts/alerts_endpoints.md`. Database schema for user_notification_preferences must be defined in `data_model.md`.

**Acceptance Criteria**
- `docs/specs/api_contracts/alerts_endpoints.md` created
- Alert types defined: stop_loss_approach, grace_period_warning_day8, grace_period_warning_day9, regime_change_risk_off, daily_portfolio_summary
- Notification preference model specced: `GET/PUT /settings/notifications` (or similar)
- Database schema for user_notification_preferences defined in `data_model.md`
- Email delivery mode specified; SMS optional/configurable
- Head of Specs Team sign-off obtained

---

### ST-07 — Backend: alert rules engine

**Type:** Backend
**Effort:** M–H (~8–14 hrs)
**Owner:** Head of Engineering
**Delegation:** Delegated (conditional on QA gate + ST-06 spec)
**Depends on:** ST-06

**Description:** Implement alert rules engine in backend. Per-alert-type trigger logic. Integrates with existing portfolio, position, and market data endpoints. Writes to notification queue or triggers delivery directly. Respects user notification preferences.

**Acceptance Criteria**
- All 5 alert types implemented with correct trigger conditions
- Alert generation respects user notification preferences
- Alert history stored (queryable)
- Integration tests for alert trigger conditions

---

### ST-08 — Backend: notification delivery (email)

**Type:** Backend
**Effort:** M (~4–8 hrs)
**Owner:** Head of Engineering
**Delegation:** Delegated (conditional on QA gate)
**Depends on:** ST-07

**Description:** Implement email notification delivery. Integrate with email service (provider TBD — per infrastructure decision). Retry logic, failure handling. Email templates for each alert type.

**Acceptance Criteria**
- Email delivery implemented for all alert types
- Delivery failures logged; retry attempted
- Email templates defined and tested
- Director of Quality sign-off obtained (per QA gate 3 session output)

---

### ST-09 — Frontend: notification preferences page

**Type:** Frontend
**Effort:** S–M (~2–4 hrs)
**Owner:** Base44 Frontend
**Delegation:** Delegated (conditional on QA gate)
**Depends on:** ST-06, ST-07

**Description:** Notification preferences page. Per-alert-type on/off toggles. Email address confirmation field. Accessible from settings.

**Acceptance Criteria**
- Notification preferences page accessible from settings
- Per-alert-type toggles: stop loss, grace period, regime change, daily summary
- Email address field (pre-populated from user settings)
- Preferences persisted via PUT /settings/notifications (or equivalent)
- Director of Quality sign-off obtained

---

### ST-10 — Frontend: in-app notification feed

**Type:** Frontend
**Effort:** S–M (~3–5 hrs)
**Owner:** Base44 Frontend
**Delegation:** Delegated (conditional on QA gate)
**Depends on:** ST-06, ST-07

**Description:** In-app notification feed (bell icon or sidebar). Shows recent alerts regardless of email preference. Unread count badge. Mark as read.

**Acceptance Criteria**
- In-app notification feed rendered in UI (bell icon or sidebar)
- Shows N most recent alerts with type, message, and timestamp
- Unread count displayed
- Mark-as-read functionality
- Director of Quality sign-off obtained

---

### ST-11 — QA: notification delivery test scenarios and infrastructure

**Type:** QA / test planning
**Effort:** S (~1–2 hrs)
**Owner:** Director of Quality
**Delegation:** Delegated (conditional on QA gate — this story IS the DL-003 gate clearance output)
**Note:** This story is the materialisation of the DL-003 auto-advance trigger. Completing ST-11 clears QA gate 3 and enables EPIC-03 implementation stories (ST-07 through ST-10) to enter sprint execution.

**Description:** Run the QA planning session for notification delivery. Produce: (1) test types required for alert delivery, (2) notification delivery modes to be tested (email, in-app), (3) expected test infrastructure (mock email service, notification queue inspection). Document output and update DL-003 trigger confirmation in the cycle record.

**Acceptance Criteria**
- QA session completed and output documented (test types, delivery modes, test infrastructure)
- Output filed as `claude/cycles/2026-03-17__release-v2.0/qa_notification_planning.md`
- DL-003 auto-advance trigger recorded as cleared in this cycle's state
- Director of Quality sign-off obtained on the test plan output
- Sprint Planning Engine pre-sprint required decisions section can be marked resolved for RISK-01

---

## EPIC-04 — Backend Completeness

**Maps to:** S2-04
**Effort:** M (~8–14 hrs total)
**Owner:** Head of Engineering
**Sprint:** 1 (ST-12 is P1 — first story)

### ST-12 — Fix GET /portfolio missing 4 fields (BLG-BE-01 P1)

**Type:** Backend bug fix
**Effort:** S (~2–4 hrs)
**Owner:** Head of Engineering
**Delegation:** Delegated
**Priority:** P1 — SPRINT 1 ITEM 1

**Description:** Add the 4 fields required by `portfolio_endpoints.md` v1.9.0 to `GET /portfolio` response: `initial_value` (portfolio initial capital value in GBP), `net_deposits` (total deposits minus total withdrawals), `current_drawdown_percent` (current value vs all-time peak; default 0.0 when no history), `peak_portfolio_value` (all-time high of portfolio_history.total_value; default 0.0 when no history). Closes GAP-03.

**Acceptance Criteria**
- `GET /portfolio` returns all 4 fields: initial_value, net_deposits, current_drawdown_percent, peak_portfolio_value
- current_drawdown_percent and peak_portfolio_value default to 0.0 when no portfolio_history exists
- net_deposits equals total deposits minus total withdrawals
- ST-05 integration tests in `tests/test_portfolio_integration.py` extended to assert these 4 fields
- GAP-03 scenario (`docs/testing/v1.7-qa-scenario-gaps.md`) passes on staging
- Director of Quality sign-off obtained

---

### ST-13 — Spec + implement GET /portfolio/prospective-heat (BLG-BE-02 P3 stretch)

**Type:** Backend + Spec
**Effort:** M (~4–8 hrs)
**Owner:** Head of Engineering + Head of Specs Team
**Delegation:** Delegated
**Priority:** P3 — stretch item; deprioritise if Sprint 1 capacity runs short

**Description:** Author `GET /portfolio/prospective-heat` spec in `portfolio_endpoints.md`. Implement endpoint in `backend/main.py`. Remove `@unittest.skip` from `TestProspectiveHeat` in `tests/test_portfolio_integration.py`.

**Acceptance Criteria**
- `GET /portfolio/prospective-heat` defined in `portfolio_endpoints.md` (response shape, calculation definition)
- Endpoint implemented and returning correct prospective heat calculation
- `@unittest.skip` removed from `TestProspectiveHeat`; tests pass on staging
- Director of Quality sign-off obtained

---

## EPIC-05 — Documentation & Standards Pack

**Maps to:** S2-05
**Effort:** M (~10–16 hrs total)
**Owner:** Infrastructure & Operations Owner + Data Model Domain & Schema Owner + Backend Engineering Patterns Owner + Head of Specs Team + QA & Testing Owner
**Sprint:** Parallel track (can run in Sprint 1 and Sprint 2 concurrently with product EPICs)

### ST-14 — BLG-OPS-02: Production Deployment Runbook

**Type:** Operations documentation
**Effort:** S (~0.5–1 hr)
**Owner:** Infrastructure & Operations Owner
**Delegation:** Delegated

**Description:** Create `docs/ops/production_deployment_runbook.md`. Steps from staging-verified build to production push. Includes: pre-deployment checklist, deployment steps, post-deployment verification, rollback procedure. Cross-references staging environment configuration (v1.10 BLG-OPS-01 output).

**Acceptance Criteria**
- `docs/ops/production_deployment_runbook.md` created (Class 2 Supporting document)
- Pre-deployment checklist, deployment steps, post-deployment verification, rollback procedure all present
- Cross-references staging environment docs
- Reviewed and signed off by Head of Engineering

---

### ST-15 — BLG-DATA-01: Positions Table Data Dictionary

**Type:** Data documentation
**Effort:** S (~0.5–1 hr)
**Owner:** Data Model Domain & Schema Owner
**Delegation:** Delegated

**Description:** Create `docs/specs/data_model_positions_dictionary.md`. Document each field in the `positions` table: name, type, nullable, description, derivation rule where applicable. Cross-reference `portfolio_endpoints.md` and `data_model.md`. Flag any fields without canonical definitions as gaps.

**Acceptance Criteria**
- Data dictionary covers all fields in positions table
- Each field: name, type, nullable, description, derivation (where applicable)
- Cross-references to canonical spec sections where definitions exist
- Gap list produced for any undocumented fields
- Registered in `docs/specs/Specs_Index.md`

---

### ST-16 — BLG-TECH-07: Database Migration Governance Standard

**Type:** Engineering governance documentation
**Effort:** S (~0.5–1 hr)
**Owner:** Backend Engineering Patterns Owner + Head of Engineering
**Delegation:** Delegated

**Description:** Create `docs/ops/database_migration_governance.md`. Define: migration naming convention, required migration file fields (description, reversibility assessment, rollback SQL), review requirements, production application procedure, incident procedure if migration fails mid-apply. Cross-reference from `backend_engineering_patterns.md`.

**Acceptance Criteria**
- `docs/ops/database_migration_governance.md` created (Class 2 Supporting document)
- Covers: naming convention, required fields, review requirements (second-engineer + schema owner), application procedure, incident procedure
- Cross-referenced from `backend_engineering_patterns.md` as new section
- Head of Engineering sign-off obtained

---

### ST-17 — BLG-NEW-13: Spec Coverage Inventory

**Type:** Governance / spec audit
**Effort:** M (~1–2 days)
**Owner:** Head of Specs Team
**Delegation:** Delegated

**Description:** Systematic audit of all `docs/specs/` sections against implementation and test coverage. Rate each section: covered / partial / gap. Cross-reference open backlog items against gaps. Define a review cadence. Produce a structured Coverage Inventory document.

**Acceptance Criteria**
- Coverage Inventory document produced covering all `docs/specs/` sections
- Each spec section rated: covered / partial / gap
- Gap items cross-referenced against open backlog items where possible
- Review cadence defined (e.g. per audit cycle or per major release)
- Registered in `docs/specs/Specs_Index.md`

---

### ST-20 — TEST-GAP-EPIC-02: CohortAnalysis backend integration regression scenario (stretch)

**Type:** QA / test coverage
**Effort:** S (~1–2 hrs)
**Owner:** QA & Testing Owner
**Delegation:** Delegated
**Priority:** P3 — stretch

**Description:** Author CohortAnalysis backend integration regression scenario (`SC-CA-BACKEND-01`): period toggle triggers API refetch and table updates; `has_enough_data = false` shows insufficient data warning; column values match `GET /analytics/cohort` response fields. Register in `docs/testing/analytics_scenarios.md` (new) or `docs/testing/risk_dashboard_scenarios.md`.

**Acceptance Criteria**
- SC-CA-BACKEND-01 scenario authored and registered
- Covers: period toggle behaviour, insufficient data state, column value correctness
- Spec references: `docs/specs/frontend/pages/analytics.md §15`, `docs/specs/api_contracts/analytics_endpoints.md#GET /analytics/cohort`

---

## EPIC-06 — Governance Tooling

**Maps to:** S2-06
**Effort:** M (~10–16 hrs total)
**Owner:** Head of Specs Team
**Sprint:** Parallel track (takes effect next roadmap cycle)
**Note:** EPIC-06 changes take effect at the next `run roadmap` invocation after v2.0 ships. All CLAUDE.md §6 governance edit checklist requirements apply.

### ST-18 — BLG-GOV-01: Roadmap stage document consolidation

**Type:** Governance process / prompt rewrite
**Effort:** M (~2–3 days)
**Owner:** Head of Specs Team
**Delegation:** Delegated

**Description:** Rewrite `claude/system/roadmap_prompt.md` to consolidate STEP 2–7 write targets into sections of `cycle_record.md` for Standard and Extended tiers (Lightweight already does this). Collapse the 5 working-paper stage files into a single `cycle_record.md`. Keep `run_manifest.md`, `cycle_summary.md`, and `lessons_learnt.md` as separate files. Update OPERATIONAL_GUIDE.md §6 and §14. Validate against one `run roadmap` cycle before sealing.

**Acceptance Criteria**
- `roadmap_prompt.md` updated: STEP 2–7 write targets changed to sections of `cycle_record.md` for Standard and Extended tiers
- Write scope restriction (§5) updated accordingly
- STEP 9 Write Plan template updated to reference `cycle_record.md`
- STEP 10 completion condition updated
- `OPERATIONAL_GUIDE.md` §6 artefact list updated
- CLAUDE.md §6 governance edit checklist satisfied (version bump, OPERATIONAL_GUIDE §14 update, prompt_change_log entry)
- At least one `run roadmap` cycle validated against new format before sealing

---

### ST-19 — BLG-GOV-02: Ideas register

**Type:** Governance process / prompt rewrite
**Effort:** M (~2–3 days)
**Owner:** Head of Specs Team
**Delegation:** Delegated

**Description:** Replace per-file idea submission model with a single `claude/ideas/ideas_register.md` — structured table, one row per idea. Update `idea_intake_prompt.md` and `roadmap_prompt.md`. Provide migration script/instruction to convert existing submissions into register rows. Archive prior submission files.

**Acceptance Criteria**
- `idea_intake_prompt.md` updated: submissions write to `ideas_register.md` (append/update row)
- `roadmap_prompt.md` STEP 4 updated: reads from `ideas_register.md` instead of scanning individual files
- `ideas_register.md` schema defined in `shared_standards.md` §16 (new entry)
- Migration instruction provided; prior files moved to `claude/ideas/submissions/archive/`
- `OPERATIONAL_GUIDE.md` updated to reflect new artefact
- CLAUDE.md §6 governance edit checklist satisfied for all affected prompt files
