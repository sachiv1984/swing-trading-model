# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-05-05 (GROOM-20260505-01 — BLG-FEAT-19 archived; BLG-FE-16 + BLG-FEAT-13 Provisional-Target updated v3.1→v3.2)
**Last rebalance:** 2026-04-24 (cycle 2026-04-24__scheduled — DL-022 backlog adds; DL-023 defers)

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

*No active items in this section — BLG-TECH-05 deferred to §9 (DL-023, 2026-04-24).*

---

## 2. Product Feature Backlog (User-Facing)

---

*BLG-FEAT-18 (Consecutive losing streak metric) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-FEAT-19 (Monthly P&L summary report) — ✅ COMPLETE v3.1 — archived to backlog_archive.md 2026-05-05*

---

## 3. Frontend & UX Backlog

---

### BLG-FE-16 — React component inventory
**Priority:** P3 (Low)
**Type:** Frontend / Documentation
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-ux-20260321-02 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** M (~1–2 days)
**Provisional-Target:** v3.2 (was v3.1 — not in v3.1 sprint scope; updated GROOM-20260505-01)

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

*BLG-FE-19 (Keyboard shortcuts) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*
*BLG-FE-18 (Screener news panel attachment) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

## 4. Backend & Data Backlog


---

*BLG-AI-02 (Model version contract for AI Journal) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

## 5. QA & Test Automation Backlog



---

*TEST-GAP-ST14 (AI audit service unit tests) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

## 6. Operations & Infrastructure Backlog

---

### BLG-OPS-13 — Add new v2.8/v2.9/v3.0 endpoints to api_performance_baseline.md re-run
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** v2.9 post-ship closure 2026-04-24 (3 endpoints); v3.0 post-ship closure 2026-04-28 OA-v30-01 (5 additional endpoints); v3.1 post-ship closure 2026-05-05 (10 additional endpoints)
**Effort:** S–M (~1–2 days — 18 endpoints total)
**Provisional-Target:** Before next performance baseline review

**Problem**
Eighteen endpoints shipped in v2.8/v2.9/v3.0/v3.1 are absent from `docs/ops/api_performance_baseline.md`. Performance re-runs require a live environment and human coordination — baseline updates cannot be automated.

**Scope (updated 2026-05-05):**
- v2.8/v2.9 endpoints (3): `POST /ai/journal-summary`, `GET /ai/journal-summary/history`, `GET /v1beta1/news`
- v3.0 endpoints (5): `GET /ticker-universe`, `POST /ticker-universe`, `DELETE /ticker-universe/{ticker}`, `GET /screener/results`, `POST /screener/run`
- v3.1 endpoints (10): `POST /trade-plans`, `GET /trade-plans/{id}`, `PUT /trade-plans/{id}`, `DELETE /trade-plans/{id}`, `GET /trade-plans/by-position/{position_id}`, `GET /trade-plans/by-ticker/{ticker}`, `GET /research/{ticker}`, `GET /earnings/{ticker}`, `GET /reports/monthly-pnl`, plus any additional v3.1 routes
- Run each against staging to obtain p50/p95 latencies and add to `docs/ops/api_performance_baseline.md`

**Acceptance Criteria**
- All 18 endpoints have p50 and p95 latency entries in the baseline document
- Entries consistent with existing baseline measurement methodology

---

*BLG-OPS-14 (AI Journal monitoring metrics) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*
*BLG-OPS-12 (External API health check extension) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

## 7. Spec Debt Backlog

*No active items in this section — BLG-SPEC-20 deferred to §9 (DL-023, 2026-04-24).*

---

## 8. Governance Backlog



---

### BLG-GOV-11 — Cycle artefact inventory and maintenance review
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead + Head of Specs Team
**Source:** User session review — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v3.2 (was v3.1 — deferred; 3 consecutive cycle deferrals as of v3.1)

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
- **BLG-TECH-05 — Prometheus metrics endpoint** (P3, M effort — permanently deferred at single-user scale; DL-023 2026-04-24)
- Position correlation analysis
- Backtesting module
- Multi-portfolio support
- Mobile app
- Full compliance scoring system
- **BLG-SPEC-20 — Machine-readable spec front-matter standard** (P3, S effort — deferred; Arc 1 specs shipped without requiring this standard; DL-023 2026-04-24)

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

## Last Release Slice — v3.1 ✅ COMPLETE

<!-- release-plan-marker: RP:v3.1:2026-04-29__release-v3.1 — COMPLETE -->

**Cycle:** 2026-04-29__release-v3.1 | **Status:** Complete — Shipped 2026-05-05 | **Published:** 2026-04-29
**Backlog slice:** `claude/cycles/2026-04-29__release-v3.1/stage4_backlog_slice.md`

| EPIC | Sprint | Stories | Theme |
|------|--------|---------|-------|
| EPIC-01 | Sprint 1+2 | ST-01, ST-02, ST-03 | PT-01 Trade Plan Object |
| EPIC-02 | Sprint 2 | ST-04, ST-05 | PT-02 Pre-Trade Research View (backend) |
| EPIC-03 | Sprint 1+2 | ST-06, ST-07, ST-08, ST-09, ST-10 | Arc 1 Completion & Screener Quality |
| EPIC-04 | Sprint 1 | ST-11, ST-12, ST-13, ST-14 | Operations, Governance & Quick Wins |

**Theme:** Arc 2 Trade Plan Foundation

---

## Prior Release Slice — v3.0 ✅ COMPLETE

<!-- release-plan-marker: RP:v3.0:2026-04-25__release-v3.0 — COMPLETE -->

**Cycle:** 2026-04-25__release-v3.0 | **Status:** Complete — Shipped 2026-04-27 | **Published:** 2026-04-25
**Backlog slice:** `claude/cycles/2026-04-25__release-v3.0/stage4_backlog_slice.md`

| EPIC | Sprint | Stories | Theme |
|------|--------|---------|-------|
| EPIC-01 | Sprint 1 | ST-01, ST-02, ST-03, ST-04 | Arc 1 Screener Engine |
| EPIC-02 | Sprint 2 | ST-05, ST-06, ST-07 | Arc 1 Screener Frontend |
| EPIC-03 | Sprint 2 | ST-08, ST-09, ST-10, ST-11 | Operations, Observability & Test Quality |
| EPIC-04 | Sprint 1 | ST-12, ST-13, ST-14, ST-15, ST-16 | Governance, Deferred Patches & Quick Wins |

**Theme:** Arc 1 Remainder — Screener Engine & Results Page

---

## Prior Release Slice — v2.9

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
**Provisional-Target:** v3.2 (was v3.1 — deferred; not in v3.0 or v3.1 sprint scope; updated GROOM-20260505-01)

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

---

## Test Scenario Gaps — v3.1 Delivery Verification

*Added by Delivery Verification Engine — 2026-05-05*

### TEST-GAP-EPIC-01 — Trade Plan test scenario coverage gap (v3.1)

**Source:** Delivery verification 2026-04-29__release-v3.1
**Priority:** P3
**Target:** v3.2 (before next sprint touching Trade Plan domain)

Test coverage gap from 2026-04-29__release-v3.1: `tests/e2e/trade-plan.spec.js` (SC-TP-01–07) was created as part of EPIC-01 delivery but not registered in `execution_state.json test_scenarios` field. QA & Testing Owner to verify Playwright test coverage and register in test_scenarios for the Trade Plan domain. Backend CRUD integration test scenarios for `/trade-plans` endpoints also warranted.

---

### TEST-GAP-EPIC-03 — Earnings Calendar and UK screener test registration gap (v3.1)

**Source:** Delivery verification 2026-04-29__release-v3.1
**Priority:** P3
**Target:** v3.2 (before next sprint touching Earnings/Screener domain)

Test coverage gap from 2026-04-29__release-v3.1: `tests/e2e/earnings-calendar.spec.js` (SC-EARN-01–09) and `tests/e2e/screener-uk-suffix.spec.js` (SC-UK-01–04) were created during EPIC-03 delivery but not registered in `execution_state.json test_scenarios` field. QA & Testing Owner to verify coverage completeness and ensure test files are registered per `execution_prompt.md §3.1.A` advisory.
