# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-04-28 (roadmap rebalance 2026-04-28__scheduled — DL-024: 5 items added, 3 deprioritised; BLG-GOV-11 target updated v3.1→v3.2; BLG-FEAT-13 moved to §9; BLG-FE-16 further deferred)
**Last rebalance:** 2026-04-28 (cycle 2026-04-28__scheduled — DL-024 backlog adds/defers)

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

### BLG-FEAT-19 — Monthly P&L summary report
**Priority:** P2 (Medium)
**Type:** Product Feature / Reporting
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260321-01 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** S (~1 day)
**Provisional-Target:** v3.1

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
**Provisional-Target:** v3.2 (further deferred from v3.1 — DL-024 2026-04-28; displaced by BLG-QA-10/11 at higher priority; dependency gate not met; lower priority vs. screener QA items)

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

### BLG-QA-10 — Screener scenario library
**Priority:** P2 (Medium)
**Type:** QA / Test Data
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260421-02 — promoted cycle 2026-04-28__scheduled (DL-024)
**Effort:** M (~1–2 days)
**Provisional-Target:** v3.1

**Problem**
The screener engine is live but has no documented scenario library covering known edge cases (zero results, max results, single-sector sweeps, conflicting filters). Without a reference library, regression testing relies on ad-hoc checks and QA sign-off is undocumented.

**Scope**
- Define a library of screener test scenarios covering: normal results, zero results, boundary conditions, filter combinations
- Each scenario specifies: input filters, expected behaviour, pass/fail criteria
- Library serves as the reference for both manual QA and future automation

**Acceptance Criteria**
- Scenario library document created with ≥10 scenarios covering core paths and edge cases
- Each scenario has defined inputs, expected outputs, and pass/fail criteria
- Reviewed and accepted by QA & Testing Owner

---

### BLG-QA-11 — Screener accuracy test protocol
**Priority:** P2 (Medium)
**Type:** QA / Process
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260421-02 — promoted cycle 2026-04-28__scheduled (DL-024)
**Effort:** S (~1 day)
**Provisional-Target:** v3.1

**Problem**
No formal protocol exists for verifying screener result accuracy against known data. The screener may return technically valid responses that contain incorrect scores, missing tickers, or wrong sector classifications without a structured accuracy check.

**Scope**
- Define a protocol for periodically verifying screener output accuracy against known-good reference data
- Specify: frequency, sample size, comparison methodology, pass/fail thresholds
- Document how discrepancies are escalated and resolved

**Acceptance Criteria**
- Written protocol document covering frequency, sample selection, comparison method, and thresholds
- Protocol references BLG-QA-10 scenario library where applicable
- Accepted by Director of Quality

---

*TEST-GAP-ST14 (AI audit service unit tests) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

## 6. Operations & Infrastructure Backlog

---

### BLG-OPS-13 — Add new v2.8/v2.9/v3.0 endpoints to api_performance_baseline.md re-run
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** v2.9 post-ship closure 2026-04-24 (3 endpoints); v3.0 post-ship closure 2026-04-28 OA-v30-01 (5 additional endpoints)
**Effort:** S (~1 day — 8 endpoints total)
**Provisional-Target:** Before next performance baseline review

**Problem**
Eight endpoints shipped in v2.8/v2.9/v3.0 are absent from `docs/ops/api_performance_baseline.md`. Performance re-runs require a live environment and human coordination — baseline updates cannot be automated.

**Scope (updated 2026-04-28):**
- v2.8/v2.9 endpoints (3): `POST /ai/journal-summary`, `GET /ai/journal-summary/history`, `GET /v1beta1/news`
- v3.0 endpoints (5): `GET /ticker-universe`, `POST /ticker-universe`, `DELETE /ticker-universe/{ticker}`, `GET /screener/results`, `POST /screener/run`
- Run each against staging to obtain p50/p95 latencies and add to `docs/ops/api_performance_baseline.md`

**Acceptance Criteria**
- All 8 endpoints have p50 and p95 latency entries in the baseline document
- Entries consistent with existing baseline measurement methodology

---

### BLG-SEC-03 — Alpaca API key rotation policy
**Priority:** P3 (Low)
**Type:** Security / Operations
**Owner:** Cybersecurity & Trust Lead
**Source:** IDEA-cybersecurity-20260421-01 — promoted cycle 2026-04-28__scheduled (DL-024)
**Effort:** S (~1 day)
**Provisional-Target:** v3.1

**Problem**
No documented policy exists for rotating the Alpaca API key. If a key is compromised, there is no defined response procedure or rotation schedule. The v3.0 hotfix cycle (ST-01, ST-04) confirmed Alpaca as a live production dependency.

**Scope**
- Define a key rotation policy: rotation schedule, trigger conditions (suspected compromise, staff change), rotation procedure
- Document the steps to update the key in the deployment environment without downtime
- Policy document only — no code changes required

**Acceptance Criteria**
- Written policy covering rotation schedule, trigger conditions, and step-by-step procedure
- Policy references the deployment environment (Render) configuration method
- Accepted by Cybersecurity & Trust Lead

---

### BLG-SEC-04 — External API credential audit
**Priority:** P3 (Low)
**Type:** Security / Audit
**Owner:** Cybersecurity & Trust Lead
**Source:** IDEA-cybersecurity-20260421-02 — promoted cycle 2026-04-28__scheduled (DL-024)
**Effort:** XS (~hours)
**Provisional-Target:** v3.1

**Problem**
No consolidated record exists of all external API credentials (Alpaca, news APIs, etc.) in use by the system, their access scopes, expiry conditions, or storage locations.

**Scope**
- Audit all external API credentials currently in use
- For each credential: service, scope, storage location, expiry/rotation conditions
- Produce a credential inventory document (sensitive fields omitted — reference to secure storage only)

**Acceptance Criteria**
- Credential inventory document created listing all external credentials
- Each entry: service name, credential type, scope/permissions, storage location reference, rotation policy reference (BLG-SEC-03 for Alpaca)
- Accepted by Cybersecurity & Trust Lead

---

*BLG-OPS-14 (AI Journal monitoring metrics) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*
*BLG-OPS-12 (External API health check extension) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

## 7. Spec Debt Backlog

*No active items in this section — BLG-SPEC-20 deferred to §9 (DL-023, 2026-04-24).*

---

## 8. Governance Backlog

---

### BLG-GOV-17 — External API dependency risk register
**Priority:** P3 (Low)
**Type:** Governance / Risk Management
**Owner:** PMO Lead
**Source:** IDEA-pmo-lead-20260421-01 — promoted cycle 2026-04-28__scheduled (DL-024)
**Effort:** XS (~hours)
**Provisional-Target:** v3.1

**Problem**
No consolidated register exists for external API dependencies (Alpaca, news APIs). The v3.0 hotfix cycle demonstrated that Alpaca API behavioural changes can cause production failures without warning. A dependency risk register provides forward-reference visibility and enables proactive monitoring.

**Scope**
- Create a risk register for all external API dependencies
- For each dependency: service name, version/contract status, failure modes identified, mitigation in place, monitoring approach
- Register is a living document — updated when new dependencies are added or incidents occur

**Acceptance Criteria**
- Risk register document created with entries for all current external API dependencies (minimum: Alpaca, news API)
- Each entry includes: service, failure modes, current mitigations, monitoring approach
- Accepted by PMO Lead

---

### BLG-GOV-11 — Cycle artefact inventory and maintenance review
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead + Head of Specs Team
**Source:** User session review — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v3.2 (was v3.1 — further deferred; DL-024 2026-04-28; 3 consecutive cycle deferrals; displaced by BLG-SEC-03/04 and BLG-GOV-17)

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
- **BLG-FEAT-13 — Add gated feature rollout capability** (P3, M effort — moved to §9; DL-024 2026-04-28; no active trigger at single-user scale; review when multi-user deployment or experimental feature staging requirement arises)

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

## Last Release Slice — v3.0 ✅ COMPLETE

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

*BLG-FEAT-13 (Gated feature rollout) — moved to §9 Deferred 2026-04-28 (DL-024 — no active trigger at single-user scale). All §14 items (BLG-GOV-13, BLG-FEAT-16, BLG-QA-13) shipped in v2.8 — archived to backlog_archive.md 2026-04-20 (GROOM-20260420-01).*
