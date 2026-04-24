# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-04-24 (GROOM-20260424-01 — post-ship closure v2.9; 12 items archived COMPLETE + 1 killed BLG-GOV-08; 8 provisional targets updated v2.9→v3.0)
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
**Provisional-Target:** v3.0

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
**Provisional-Target:** v3.0

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
**Provisional-Target:** v3.0

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

### BLG-FE-18 — Screener results page: attach news panel on DS-02 implementation
**Priority:** P3 (Low)
**Type:** Frontend / Feature Completion
**Owner:** Backend Engineering Patterns Owner + Frontend Specifications & UX Documentation Owner
**Source:** DEV-01 — v2.9 delivery verification 2026-04-24; ST-07 (DS-06) AC-1 partial deferral
**Effort:** S (~0.5 day)
**Provisional-Target:** v3.0 (DS-02 implementation prerequisite must ship first)

**Problem**
The `GET /news/{ticker}` backend endpoint is available (shipped v2.9 ST-07), but the UI attachment to the screener results page is deferred because DS-02 (screener results page implementation) does not yet exist. When DS-02 is implemented in v3.0, the news panel must be wired to the screener results page to complete ST-07 AC-1.

**Scope**
- Wire the existing `GET /news/{ticker}` backend endpoint to the screener results page news panel
- Per `screener_results.md §9`: panel triggered by news count badge click; inline expanded below row; last 5 headlines; UK tickers show `—` in news column (no badge)
- Display-only, per BLG-GOV-16 §13 sign-off conditions

**Acceptance Criteria**
- News panel renders on screener results page per `screener_results.md §9`
- Consistent with watchlist news panel implementation (v2.9 ST-07)
- UK ticker handling: `—` in news column, no badge, no panel
- Empty news state handled per `screener_results.md §7`
- DoQ sign-off including local run or staging verification of toggle behaviour


---

## 4. Backend & Data Backlog


---

### BLG-AI-02 — Model version contract for AI Journal
**Priority:** P3 (Low)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer
**Source:** IDEA-ai-compliance-20260321-02 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** S (~0.5 day)
**Provisional-Target:** v3.0

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

### TEST-GAP-ST14 — AI audit service unit tests (ai_audit_service.py)
**Priority:** P3 (Low)
**Type:** Test Automation / Backend Coverage
**Owner:** QA & Testing Owner
**Source:** v2.9 delivery verification 2026-04-24 — qa_evidence_EPIC-04.md ST-14 note: "no unit tests for audit service — in scope for future sprint"
**Effort:** S (~0.5 day)
**Provisional-Target:** Before next sprint modifying AI audit or journal summary features

**Problem**
`backend/services/ai_audit_service.py` (shipped v2.9 ST-14) has no unit tests. The audit log table creation (`ensure_ai_audit_table`), row insertion (`log_ai_summary_run`), and query (`query_audit_log`) functions are untested at unit level.

**Scope**
- Unit tests for `ai_audit_service.py` covering: `ensure_ai_audit_table` idempotency, `log_ai_summary_run` happy path and exception handling, `query_audit_log` filter behaviour (by trade_id, date range, limit)
- Tests should not require a live DB (use mock or TestClient pattern per existing integration test pattern)

**Acceptance Criteria**
- Unit tests created covering at minimum: happy path insert, query by trade_id, query by date range, graceful handling of DB error in `log_ai_summary_run`
- Tests pass in CI
- DoQ sign-off with Date field populated


---

## 6. Operations & Infrastructure Backlog

---

### BLG-OPS-13 — Add 3 new v2.9/v2.8 endpoints to api_performance_baseline.md re-run
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** v2.9 post-ship closure 2026-04-24 — endpoint coverage drift check; 3 implemented endpoints absent from api_performance_baseline.md
**Effort:** S (~0.5 day)
**Provisional-Target:** Before next performance baseline review

**Problem**
Three endpoints shipped in v2.8/v2.9 are absent from `docs/ops/api_performance_baseline.md`: `POST /ai/journal-summary` (v2.8), `GET /ai/journal-summary/history` (v2.9 ST-14), `GET /v1beta1/news` (v2.9 ST-07). Performance re-runs require a live environment and human coordination — baseline updates cannot be automated.

**Scope**
- Run `POST /ai/journal-summary`, `GET /ai/journal-summary/history`, and `GET /v1beta1/news` against staging to obtain p50/p95 latencies
- Add entries to `docs/ops/api_performance_baseline.md`

**Acceptance Criteria**
- All three endpoints have p50 and p95 latency entries in the baseline document
- Entries consistent with existing baseline measurement methodology

---

### BLG-OPS-12 — External API health check extension
**Priority:** P2 (Medium)
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260421-01 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** S (~0.5 day)
**Provisional-Target:** v3.0

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
**Provisional-Target:** v3.0

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

## 8. Governance Backlog



---

### BLG-GOV-11 — Cycle artefact inventory and maintenance review
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead + Head of Specs Team
**Source:** User session review — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v3.0 (was v2.9 — deferred)

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

## Active Release Slice — v2.9

<!-- release-plan-marker: RP:v2.9:2026-04-22__release-v2.9 -->

**Cycle:** 2026-04-22__release-v2.9 | **Status:** Closed | **Published:** 2026-04-22 | **Shipped:** 2026-04-24 (Verified_with_deviations)
**Backlog slice:** `claude/cycles/2026-04-22__release-v2.9/stage4_backlog_slice.md`

| EPIC | Sprint | Stories | Theme |
|------|--------|---------|-------|
| EPIC-01 | Sprint 1 | ST-01, ST-02, ST-03, ST-04 | Arc 1 Specification Foundation |
| EPIC-02 | Sprint 2 | ST-05, ST-06, ST-07 | Arc 1 Implementation Start |
| EPIC-03 | Sprint 1 | ST-08, ST-09, ST-10 | Arc 1 Governance & QA Foundation |
| EPIC-04 | Sprint 1+2 | ST-11, ST-12, ST-13, ST-14, ST-15 | Governance Debt & Quick Wins |

**Theme:** Arc 1 Foundation — Stock Discovery & Screening Spec & Infrastructure

---

## Prior Release Slice — v2.8

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
**Provisional-Target:** v3.0 (was v2.9 — deferred)

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
