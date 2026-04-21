# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-04-21 (cycle 2026-04-21__scheduled — 14 new items from rebalance DL-021)
**Last rebalance:** 2026-04-21 (cycle 2026-04-21__scheduled — DL-021)

> ⚠️ Standing Notice
> This backlog records prioritisation and intent only.
> All formulas, schemas, API contracts, and behavioural rules are indicative until
> confirmed in the relevant canonical specifications.
> No item may proceed to implementation without canonical owner sign-off.

> 📋 Placement Rule
> New items must be appended to the correct existing type section (§1–§8). Do not create new numbered session sections. The backlog is organised by type, not by session date.

*Completed and killed items are recorded in `claude/backlog/backlog_archive.md`.*

---

## Priority Definitions

- **P0 — Critical**: Blocks correctness, trust, or release safety
- **P1 — High**: Enables core workflows or governance
- **P2 — Medium**: High leverage but not blocking
- **P3 — Low**: Nice-to-have or future scale

---

## 1. Platform & Validation Governance Backlog

---

### BLG-TECH-05 — Prometheus metrics endpoint
**Priority:** P3 (Low)
**Type:** Observability
**Owner:** Infrastructure & Operations Owner
**Source:** Original backlog — target updated to v2.3 per backlog health scan GROOM-20260324-01
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.8+ (or when system becomes multi-user)

**Problem**
No Prometheus-compatible metrics endpoint exists. As the system grows toward multi-user operation, there is no way to monitor validation run counts, failure rates, or duration without instrumenting the application directly. Observability cannot be added retroactively without significant rework.

**Scope**
- Add `GET /metrics` Prometheus endpoint exposing: validation run count, failure count by metric and severity, validation duration
- Optional Grafana dashboard

**Acceptance Criteria**
- Metrics scrape successfully in Prometheus format
- Counters and histograms are correct

---

## 2. Product Feature Backlog (User-Facing)

---

### BLG-FEAT-18 — Consecutive losing streak metric
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** IDEA-metrics-analytics-20260321-01 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.9

**Problem**
No metric tracks consecutive losing streaks. Behavioural drift into extended losing runs is not surfaced as a risk signal.

**Scope**
- Add consecutive losing streak count (historical closed trades only) to analytics
- Display in analytics/dashboard context alongside expectancy and win rate metrics
- Scope constraint: historical closed-trade data only; not surfaced in active position views or alert flows

**Acceptance Criteria**
- Consecutive losing streak count visible in analytics view
- Metric computed from closed trades only; no reference to open positions
- Metric definition added to canonical metrics definitions spec

---

### BLG-FEAT-19 — Monthly P&L summary report
**Priority:** P2 (Medium)
**Type:** Product Feature / Reporting
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260321-01 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** S (~1 day)
**Provisional-Target:** v2.9

**Problem**
Only annual (tax-year) P&L is available. In-year performance patterns are only visible through the analytics page; no structured monthly summary exists.

**Scope**
- Month-by-month breakdown of realised P&L complementing the annual tax year report
- New endpoint or extension of existing reporting endpoint
- Display in financial reporting section of the application

**Acceptance Criteria**
- Monthly P&L breakdown available for current and prior year
- Consistent with existing realised P&L calculation
- No regression to annual tax-year report

---

## 3. Frontend & UX Backlog

---

### BLG-FE-16 — React component inventory
**Priority:** P3 (Low)
**Type:** Frontend / Documentation
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-ux-20260321-02 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.9

**Problem**
No catalogue of UI components exists. Arc 1 will add significant new frontend components. Without an inventory, Arc 1 frontend work risks duplicating existing components and design inconsistency compounds.

**Scope**
- Catalogue all existing UI components: props, variants, usage locations
- Identify existing duplication or inconsistency
- Provide a reference for Arc 1 frontend development

**Acceptance Criteria**
- Component inventory document created covering all existing components
- Each component entry includes: purpose, props summary, variants, usage locations
- Duplication or reuse opportunities noted

---

### BLG-FE-17 — Screener results page UX spec
**Priority:** P1 (High)
**Type:** Frontend / UX Specification
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-ux-20260421-01 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** M (~2 days)
**Provisional-Target:** v2.9

**Problem**
DS-02 (Screener Results Page) has no UX spec. Frontend implementation cannot begin without a formal specification. Design decisions made ad-hoc during implementation create inconsistencies.

**Scope**
- UX specification for the screener results page: column layout, sort/filter controls, candidate card design, promotion flow trigger
- Include: data freshness indicator (last updated timestamp + manual refresh, per IDEA-challenger-20260421-01 scope)
- Include: empty states design (no results, no market data, stale data)
- Include: watchlist promotion confirmation flow (DS-07 detail)
- Include: progressive loading pattern (skeleton UI)

**Acceptance Criteria**
- UX spec created as Class 2 or Class 5 document
- All DS-02 interaction patterns documented
- Empty states, freshness indicator, and promotion flow covered
- DoQ sign-off with Date field populated

---

### BLG-FE-15 — SystemStatus.js: add `/ai` prefix to `categorizeEndpoint()`
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Owner
**Source:** OA-v28-02 — v2.8 post-ship closure 2026-04-20; endpoint drift check confirmed 0 drift but `/ai` prefix unhandled
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.9

**Problem**
`SystemStatus.js` `categorizeEndpoint()` does not handle the `/ai` prefix introduced by EPIC-04 (AI Journal Summarisation). The `POST /api/ai/journal-summary` and `GET /api/ai/journal-summary/history` endpoints fall to the `'Other'` category in the System Status UI. This is a cosmetic issue only — no functional impact, but the AI endpoints should appear in a named category for clarity and future maintenance.

**Scope**
- Add `/ai` prefix case to `categorizeEndpoint()` in `SystemStatus.js`
- Assign AI endpoints to an appropriate category (e.g. `'AI'` or `'Features'`)
- Verify no regression to other endpoint categories in System Status UI

**Acceptance Criteria**
- `POST /api/ai/journal-summary` and `GET /api/ai/journal-summary/history` appear in a named category (not `'Other'`) in the System Status page
- No regression to categorisation of existing endpoints
- Change verified by code review (no observable UI behaviour change required beyond category label)

---

## 4. Backend & Data Backlog

---

### BLG-AI-01 — AI Journal summary audit log
**Priority:** P2 (Medium)
**Type:** Backend / AI Governance
**Owner:** AI Compliance & Governance Officer + Backend Engineering Patterns Owner
**Source:** IDEA-ai-compliance-20260421-01 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** S (~1 day)
**Provisional-Target:** v2.9

**Problem**
AI Journal Summarisation is live in production (v2.8). No persistent audit record exists of which summaries were generated, for which trades, at what time, by which model version. This is a §3 human-in-loop compliance gap.

**Scope**
- Persistent audit log recording each summary run: timestamp, trade_ids included, model version, output hash
- Queryable/durable storage (not just application logs)
- Integrates with BLG-AI-02 (model version contract)

**Acceptance Criteria**
- Every AI summary run is persisted in the audit log with required fields
- Log is queryable by trade_id and date range
- Model version recorded per run (see BLG-AI-02)
- DoQ sign-off with Date field populated

---

### BLG-AI-02 — Model version contract for AI Journal
**Priority:** P3 (Low)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer
**Source:** IDEA-ai-compliance-20260321-02 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.9

**Problem**
The Claude model version used for AI Journal summarisation is not formally specified or recorded per run. If the model is upgraded, there is no way to identify which summaries were generated under which capability level.

**Scope**
- Document specifying which Claude model version executes AI journal summarisation
- Version contract referenced in BLG-AI-01 audit log implementation
- Process for incrementing the contract when model version changes

**Acceptance Criteria**
- Model version contract document created (Class 2 or Class 3)
- Contract referenced in audit log implementation (BLG-AI-01)
- Process for model version changes documented

---

## 5. QA & Test Automation Backlog

---

### BLG-QA-08 — External API mock harness for CI
**Priority:** P1 (High)
**Type:** QA / Test Infrastructure
**Owner:** Director of Quality + QA & Testing Owner
**Source:** IDEA-director-of-quality-20260421-01 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** M (~2 days)
**Provisional-Target:** v2.9

**Problem**
CI tests that depend on live Alpaca and Yahoo Finance APIs are flaky. Arc 1 screener tests will require deterministic CI without live external API calls.

**Scope**
- Test harness mocking Alpaca Markets API and Yahoo Finance API responses for CI
- Enables deterministic screener engine CI runs without live external API calls
- Works in conjunction with BLG-QA-09 (screener test data library)

**Acceptance Criteria**
- Mock harness operational in CI for both Alpaca and Yahoo Finance APIs
- Screener CI tests pass deterministically without live API calls
- Mock responses configurable per test scenario
- DoQ sign-off with Date field populated

---

### BLG-QA-09 — Screener test data library
**Priority:** P1 (High)
**Type:** QA / Test Infrastructure
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260421-01 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** M (~2 days)
**Provisional-Target:** v2.9

**Problem**
No synthetic ticker test data library exists. Screener engine tests would require live market data without it, making CI non-deterministic.

**Scope**
- Library of synthetic ticker data: price history, ATR values, regime states, signal scores
- Covers known edge cases: regime gate pass/fail, ATR threshold boundaries, signal threshold boundaries
- Designed for use with BLG-QA-08 (external API mock harness)

**Acceptance Criteria**
- Test data library created with minimum 10 synthetic tickers covering key screener filter scenarios
- Edge cases documented: passes all filters, fails regime gate, fails ATR threshold, fails signal threshold
- Used by BLG-QA-08 mock harness
- DoQ sign-off with Date field populated

---

### TEST-GAP-EPIC-04 — AI Journal Summarisation test scenario coverage
**Priority:** P3 (Low)
**Type:** Test Automation / Scenario Documentation
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-04-17__release-v2.8 (TSG-v28-01) — see verification_report.md §6
**Effort:** S (~0.5 day)
**Provisional-Target:** Before next sprint that modifies AI journal feature

**Problem**
EPIC-04 (AI Journal Summarisation) shipped with no test scenario documentation in `docs/testing/`. The POST /ai/journal-summary graceful failure path and the frontend collapsed-by-default/non-dismissible-disclaimer behaviours are untested by any formal scenario.

**Scope**
Create `docs/testing/ai_scenarios.md` covering:
- AI summary happy path (POST with trade_ids returns summarised text)
- AI summary graceful LLM failure (LLM unreachable → HTTP 200 with summary:null)
- Frontend collapsed by default on page load
- Disclaimer always visible when section is expanded (all states)

**Acceptance Criteria**
- `docs/testing/ai_scenarios.md` created with at minimum 4 scenarios covering the above
- All scenarios reference `ai_endpoints.md` and `trade_history.md v1.7` as canonical specs
- DoQ sign-off with Date field populated

---

## 6. Operations & Infrastructure Backlog

---

### BLG-OPS-12 — External API health check extension
**Priority:** P2 (Medium)
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260421-01 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.9

**Problem**
`GET /health` currently covers only internal services (DB, market status). Arc 1 introduces Alpaca and Yahoo Finance external API dependencies. External API failures are invisible until screener results fail — no proactive operational alerting exists.

**Scope**
- Extend `GET /health` to include external API connectivity status: last successful call timestamp, error rate (rolling window), p95 latency
- Cover Alpaca Markets API and Yahoo Finance API
- Non-blocking: health endpoint returns partial status if external check fails

**Acceptance Criteria**
- `GET /health` response includes external API status section
- Each external API shows: last_successful_call, error_rate, p95_latency
- Health endpoint does not fail if external API is down (returns degraded status)

---

## 7. Spec Debt Backlog

---

### BLG-SPEC-20 — Machine-readable spec front-matter standard
**Priority:** P3 (Low)
**Type:** Spec Debt / Governance Tooling
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260321-02 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.9

**Problem**
Canonical spec files have inconsistent or absent YAML front-matter. Arc 1 will add multiple new canonical documents. Inconsistent headers prevent automated CI compliance checks and increase audit overhead.

**Scope**
- Define YAML front-matter standard for canonical spec files (Class 2 documents)
- Document the standard in a reference spec or update OPERATIONAL_GUIDE
- Apply to new Arc 1 spec files created in v2.9

**Acceptance Criteria**
- Front-matter standard documented with required fields
- New Arc 1 spec files (BLG-SPEC-21/22/23 outputs) comply with the standard
- CI-checkable pattern defined (even if CI check is deferred to a later item)

---

### BLG-SPEC-21 — Screener results schema spec
**Priority:** P1 (High)
**Type:** Spec Debt / Architecture
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260421-02 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.9

**Problem**
No canonical spec exists for the Arc 1 screener output data structure before DS-01 implementation begins. Without a schema spec, DS-01 backend and DS-02 frontend cannot agree on the interface.

**Scope**
- Canonical specification for screener output data structure: ticker, market, ATR, regime status, signal score, sector, proximity to entry zone
- Must explicitly reference strategy_rules.md §11 as the parameter source
- Include logging requirement for screener parameter audit trail (per IDEA-strategy-owner-20260421-01)

**Acceptance Criteria**
- Schema spec created as Class 2 canonical document
- All screener output fields defined with types and derivation source
- §11 parameter reference explicit
- DoQ sign-off with Date field populated

---

### BLG-SPEC-22 — Alpaca API integration contract
**Priority:** P1 (High)
**Type:** Spec Debt / API Contract
**Owner:** API Contracts & Documentation Owner
**Source:** IDEA-api-contracts-20260421-01 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** S (~1 day)
**Provisional-Target:** v2.9

**Problem**
DS-05 (Alpaca US Market Data Integration) has no API contract document. DS-05 implementation cannot begin without a formal spec documenting which endpoints are used, error handling, rate limits, and fallback strategy.

**Scope**
- Formal Class 2 API contract for Alpaca US market data integration
- Endpoints used: OHLCV bars, and any other endpoints required for DS-05
- Rate limits, error handling, retry strategy, fallback strategy (Yahoo Finance fallback vs explicit error)
- Must include governed fallback specification (addresses IDEA-challenger-20260421-02 scope)

**Acceptance Criteria**
- Contract created as Class 2 canonical document in `docs/specs/api_contracts/`
- All DS-05 Alpaca endpoints documented with request/response schemas
- Fallback strategy explicitly defined
- DoQ sign-off with Date field populated

---

### BLG-SPEC-23 — Screener internal API contract
**Priority:** P1 (High)
**Type:** Spec Debt / API Contract
**Owner:** API Contracts & Documentation Owner
**Source:** IDEA-api-contracts-20260421-02 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.9

**Problem**
The internal screener API endpoints (GET /screener/results, POST /screener/run) have no formal contract before Arc 1 implementation begins. Frontend and backend work on DS-02 and DS-01 cannot proceed without a shared interface spec.

**Scope**
- Formal API contract for internal screener API endpoints
- Request/response schemas, pagination, error codes, authentication requirements
- Must be added to `docs/reference/openapi.yaml` per CLAUDE.md rule

**Acceptance Criteria**
- Contract created as Class 2 canonical document in `docs/specs/api_contracts/`
- All screener endpoints documented at `##` heading level
- Corresponding OpenAPI entries added to `docs/reference/openapi.yaml`
- DoQ sign-off with Date field populated

---

## 8. Governance Backlog

---

### BLG-GOV-16 — §13 review record for DS-06 (Alpaca News Panel)
**Priority:** P1 (High)
**Type:** Governance / Strategy Compliance
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260421-02 — promoted cycle 2026-04-21__scheduled (DL-021); SPS=4 (boundary-adjacent)
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.9

**Problem**
DS-06 (Alpaca News Panel) is labelled §13 COMPLIANT in the roadmap but has no formal §13 review decision record. Implementation cannot begin without Strategy Rules owner sign-off on record.

**Scope**
- Formal §13 review document confirming DS-06 display-only Alpaca news context does not constitute a sentiment signal or automated advisory
- Scope constraint: §13 compliance is conditioned on display-only headlines with no sentiment scoring or automated advisory generation
- Required before DS-06 enters sprint planning

**Acceptance Criteria**
- §13 review record document created (Class 3 — Operational Record or equivalent)
- Document explicitly states: DS-06 compliance conditioned on display-only headlines, no sentiment scoring
- Strategy Rules & System Intent Owner sign-off recorded
- Gate marked complete in roadmap (per hard gate marking rule)

---

### BLG-GOV-15 — execution_prompt.md STEP 5.1.B — System_status_report capability count cross-check
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** AUD-2026-04-20-001 — OBSERVED; blast radius 3; priority weight 9; Tier 2
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.9 planning sprint

**Problem**
`System_status_report.md` capability row counts (SC-CORR, SC-SIG-IND) were incorrect at v2.8 delivery verification entry — counts were set at sprint planning time and not updated post-execution. This required a Type A action-now correction at Phase 4 and was the highest-impact friction item in v2.8. There is no prompt-enforced cross-check in STEP 5.1 (sprint close) to catch this before Phase 4.

**Scope**
Insert STEP 5.1.B advisory in `claude/system/execution_prompt.md` immediately after the existing "QA Evidence File Existence Check":

> **STEP 5.1.B — System_status_report Capability Row Cross-Check (advisory):**
> Before writing Sprint_Complete, open `docs/System_status_report.md` and locate the row for the current release. For each `SC-*` scenario count cell, verify the count matches the actual number of scenario entries in the referenced test file. If any cell value was set at sprint planning time and not updated post-execution, correct it now. Record any corrections in `sprint_close.md` notes column. Also verify `execution_prompt.md` version reference matches the actual current version. Non-blocking: if discrepancies are found, correct in-session; do not halt sprint close.

**Acceptance Criteria**
- `execution_prompt.md` STEP 5.1 contains STEP 5.1.B advisory as above
- §6 CLAUDE.md checklist applied: version bump (v3.8→v3.9), OPERATIONAL_GUIDE §14 row updated, phase section header updated, prompt_change_log entry appended
- Head of Specs Team sign-off on the patch

---

### BLG-GOV-08 — Engine prompt compression: roadmap_prompt and release_planning_prompt
**Priority:** P3 (Low)
**Type:** Governance Process / Technical Debt
**Owner:** Head of Specs Team
**Source:** AUD-2026-03-21 Tier 3 — engine prompt compression deferred (roadmap_prompt 1,581 lines; release_planning_prompt 1,534 lines)
**Effort:** L (~3–5 days)
**Provisional-Target:** v2.9 (was v2.8 — 5 consecutive deferrals; retirement review at v2.9 planning)

**Problem**
`claude/system/roadmap_prompt.md` (1,581 lines) and `claude/system/release_planning_prompt.md` (1,534 lines) are the two largest engine prompts in the governance system. Inline schemas, repeated examples, and verbose explanatory prose are opportunities for extraction and tightening without removing instructional precision or hard gate logic.

**Scope**
- Reduce both files by at least 10% in line count without removing governance intent or hard gate logic
- Extract schemas or reference material to `shared_standards.md` with cross-references added in-engine
- Update OPERATIONAL_GUIDE §14 and §6/§6B source prompt headers accordingly

**Acceptance Criteria**
- Both files reduced by at least 10% in line count
- No governance intent or hard gate logic removed
- Extracted material moved to `shared_standards.md` with cross-reference
- §6 checklist applied per CLAUDE.md for both files
- OPERATIONAL_GUIDE §14 and §6/§6B headers updated

---


### BLG-GOV-14 — execution_prompt.md §3.2 governance patches (2 deferred from v2.8)
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** OA-v28-03 — v2.8 post-ship closure lessons_learnt_closure.md Friction Items 3 & 4
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.9 planning sprint

**Problem**
Two process gaps were identified at v2.8 delivery verification (STEP -1.3) that caused mid-verification remediation stalls. Both require patches to `claude/system/execution_prompt.md` under Head of Specs Team sign-off and cannot be applied without a governed prompt-edit session.

**Scope — Patch 1 (§3.2.A reclassification note):**
When a `delegated_frontend` story is reclassified to `autonomous` per LL-v2.3-EX-02 but the EPIC contains frontend-visible changes, the autonomous class DoQ criteria (criterion 3: no frontend-visible change) is not fully met at EPIC level. A Director of Quality counter-sign is required at sprint close (STEP 5), not deferred to delivery verification STEP -1.3. Add this note near the LL-v2.3-EX-02 reference in §3.2.A.

**Scope — Patch 2 (§3.2 DoQ EPIC template):**
When a `delegated_frontend` story has a domain-specific gate authority (Strategy Rules, Security, etc.) as its primary sign-off, the qa_evidence file must also include a Director of Quality EPIC-level consolidation block summarising all story sign-offs. The template should note: "EPIC-level DoQ sign-off block required regardless of story-level authority delegation."

**Acceptance Criteria**
- `execution_prompt.md` §3.2.A contains note: when delegated_frontend→autonomous reclassification involves frontend-visible changes, Director of Quality counter-sign required at STEP 5 sprint close
- `execution_prompt.md` §3.2 DoQ template contains explicit note: EPIC-level DoQ consolidation block required when story-level authority is domain-specific (Strategy Rules, Security, etc.)
- §6 CLAUDE.md checklist applied (version bump, OPERATIONAL_GUIDE §14 + phase section updated, prompt_change_log entry)
- Head of Specs Team sign-off on both patches

---

### BLG-GOV-11 — Cycle artefact inventory and maintenance review
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead + Head of Specs Team
**Source:** User session review — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.9 (was v2.8 — deferred)

**Problem**
As cycles accumulate, documents are created in each cycle directory but there is no consolidated inventory of what exists across all closed cycles, nor a documented lifecycle for each artefact type (maintained vs. point-in-time). Without this review it is impossible to audit historical artefacts, identify stale documents, or enforce consistent maintenance practices going forward.

**Scope**
- Inventory all documents created across all closed cycles (`claude/cycles/`)
- Categorise by type: planning, execution, QA evidence, governance, run manifests, etc.
- Document the expected lifecycle for each type: point-in-time artefact vs. living document
- Identify any maintenance gaps, stale artefacts, or documents that should be archived
- Produce a reference document or update the OPERATIONAL_GUIDE with the artefact lifecycle model

**Acceptance Criteria**
- A consolidated artefact inventory exists covering all closed cycles
- Each document type has a documented lifecycle (point-in-time vs. maintained)
- Any maintenance gaps are identified; each either resolved or filed as a follow-up backlog item
- Reference document or OPERATIONAL_GUIDE section added

---

## 9. Deferred / Future Candidates

- Daily email portfolio summary
- FX rate history tracking
- Prometheus validation observability (BLG-TECH-05)
- Position correlation analysis
- Backtesting module
- Multi-portfolio support
- Mobile app
- Full compliance scoring system

---

## 10. Explicitly Out of Scope (Product-Level)

These are deliberate product decisions, not deferrals:

- Broker API integration
- Automated trading execution
- Configurable strategy builder
- ML-based predictions
- Social / community features
- Options and futures trading support

---

## 11. Lifecycle Governance Notes

- This backlog is not canonical and must never override: strategy rules, metrics definitions, API contracts
- Any shipped feature must be backed by: a canonical specification, updated validation where applicable
- Once implemented, backlog items are superseded by canonical documentation

---

## 12. Last Release Slice

## Active Release Slice — v2.8

<!-- release-plan-marker: RP:v2.8:2026-04-17__release-v2.8 -->

**Cycle:** 2026-04-17__release-v2.8 | **Status:** Closed | **Published:** 2026-04-17 | **Shipped:** 2026-04-20 (Verified)
**Backlog slice:** `claude/cycles/2026-04-17__release-v2.8/stage4_backlog_slice.md`

| EPIC | Sprint | Stories | Theme |
|------|--------|---------|-------|
| EPIC-01 | Sprint 2 | ST-01 | Market Correlation Frontend |
| EPIC-02 | Sprint 1 | ST-02, ST-03 | Test Scenario Coverage |
| EPIC-03 | Sprint 1 | ST-04, ST-05, ST-06 | Governance Process Hardening |
| EPIC-04 | Sprint 2 | ST-07, ST-08 | AI Journal Summarisation |

**Theme:** Frontend Completion, Test Quality & AI Journal Feature

---

## Prior Release Slice — v2.7

<!-- release-plan-marker: RP:v2.7:2026-04-13__release-v2.7 — COMPLETE -->

**Cycle:** 2026-04-13__release-v2.7 | **Status:** Closed | **Published:** 2026-04-13 | **Shipped:** 2026-04-16 (Verified)
**Backlog slice:** `claude/cycles/2026-04-13__release-v2.7/stage4_backlog_slice.md`

| Epic | Stories | Theme |
|------|---------|-------|
| EPIC-01 | ST-01, ST-02, ST-03 | Backend Integration Completion |
| EPIC-02 | ST-04, ST-05, ST-06, ST-07 | Test Automation & CI Hardening |
| EPIC-03 | ST-08, ST-09, ST-10, ST-11 | Frontend UX Polish |
| EPIC-04 | ST-12, ST-13, ST-14, ST-15 | Governance & Spec Debt |

**Theme:** Integration Baseline, Quick Wins & Governance Debt

| EPIC | Sprint | Stories | Theme |
|------|--------|---------|-------|
| EPIC-01 | Sprint 1 | ST-01, ST-02, ST-03 | System Status Reliability |
| EPIC-02 | Sprint 2 | ST-04, ST-05, ST-06 | Backend Integration & Performance |
| EPIC-03 | Sprint 2 | ST-07, ST-08, ST-09 | Frontend & Operations Quick Wins |
| EPIC-04 | Sprint 1 | ST-10, ST-11, ST-12, ST-13 | Governance, Process & QA Hardening |

---

## 13. New Backlog Items — Roadmap Rebalance 2026-03-31

*Items from roadmap rebalance cycle 2026-03-31__scheduled (DL-013 to DL-016) and prior session addition (BLG-FEAT-13). Target releases are indicative.*

---

### BLG-FEAT-13 — Add gated feature rollout capability
**Priority:** P3 (Low)
**Type:** Product Feature / Platform
**Owner:** Head of Engineering + Product Owner
**Source:** User request — 2026-03-31
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.9 (was v2.8 — deferred)

**Problem**
The application has no mechanism to roll out new features to a subset of users or environments. Any new capability ships immediately to all users with no ability to stage a rollout, run a controlled trial, or roll back a single feature without reverting the entire deployment. As the product grows this creates risk for experimental features and makes it impossible to validate new UI flows with a limited audience before full release.

**Scope**
- Define a feature flag schema (flag name, enabled boolean, optional env/user scope)
- Implement a lightweight flag evaluation mechanism driven by config file or environment variables — no external service dependency required at first
- Wrap at least one new feature behind a flag as a proof-of-concept on first use
- Document the gating pattern in a spec file or OPERATIONAL_GUIDE

**Acceptance Criteria**
- A feature can be toggled on/off without a code change (env var or config file)
- Flag state is auditable (logged at startup or accessible via a lightweight admin check)
- At least one shipped feature uses a gate as proof-of-concept
- Gating pattern documented for use in future story authoring

---

*Items from §13 (BLG-FEAT-13) remain active. All §14 items (BLG-GOV-13, BLG-FEAT-16, BLG-QA-13) shipped in v2.8 — archived to backlog_archive.md 2026-04-20 (GROOM-20260420-01).*
