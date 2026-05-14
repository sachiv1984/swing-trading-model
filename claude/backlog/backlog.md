# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-05-14 (groom backlog GROOM-20260514-01 — 11 BLG items + 2 TEST-GAP items archived; all COMPLETE/RESOLVED v3.4 entries replaced with one-line archive notes; see backlog_archive.md GROOM-20260514-01)
**Last rebalance:** 2026-05-08 (cycle 2026-05-08__scheduled — DL-025 backlog adds × 16)

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

### BLG-FEAT-20 — Net-of-costs performance tracking
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260321-02 — promoted cycle 2026-05-05__scheduled (DL-024)
**Effort:** M (~2–3 days)
**Provisional-Target:** Arc 3/4 context (deliver alongside Arc 3 or Arc 4 data model work — not a standalone sprint item)

**Problem**
Performance metrics (R-multiple, win rate, expectancy) use gross P&L figures. When evaluating edge in Arc 4/6, R-multiples that ignore transaction costs overstate performance and may mask a genuinely unprofitable strategy. The Fee Drag % metric (v2.4) surfaces aggregate cost impact but per-trade R-multiples remain gross.

**Scope**
- Add brokerage cost fields per trade (commission, spread cost in GBP) — optional capture, not mandatory
- Recalculate R-multiple as net-of-costs where cost data is present
- Surface net-of-costs vs gross R-multiple on trade records and performance reports
- Sequence alongside Arc 3/4 data model work to avoid standalone migration overhead

**Acceptance Criteria**
- Brokerage cost fields capturable per trade (optional — not all trades will have explicit cost data)
- Net-of-costs R-multiple calculated and displayed where cost data exists
- Performance report breakdowns show gross vs net comparison where material
- No impact to existing R-multiple calculations where cost data is absent

---

*BLG-FEAT-21 (Trade plan abandonment status field) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

## 3. Frontend & UX Backlog

---

*BLG-FE-16 (React component inventory) — ✅ COMPLETE v3.2 — archived to backlog_archive.md 2026-05-09*


---

*BLG-FE-19 (Keyboard shortcuts) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*
*BLG-FE-18 (Screener news panel attachment) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-FE-21 (Design system document) — ✅ COMPLETE v3.2 — archived to backlog_archive.md 2026-05-09*

---

*BLG-FE-31 (Research view component library) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-22 (Screener morning routine UX spec) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-23 (Research page UK ticker suffix not stripped) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-24 (Negative earnings days display for past earnings dates) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-25 (Signals page: default to most recent day's signals) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

### BLG-FE-26 — Research page UX review: regime lozenge and font consistency
**Priority:** P3 (Low)
**Type:** Frontend / UX Quality
**Owner:** Head of UX & Design
**Source:** v3.2 delivery verification — manual staging 2026-05-06
**Effort:** XS–S (review + spec, ~0.5 day)
**Provisional-Target:** v3.3

**Problem**
Manual staging of the v3.2 Research page revealed two UX quality issues:
1. **Regime lozenge wraps to two lines** — the regime status lozenge (signal/regime indicator) displays on two lines rather than one, suggesting the container width or text is not constrained correctly.
2. **Font inconsistency** — the Research page uses inconsistent font weights or sizes compared to the design system documented in `docs/frontend/design_system.md` (BLG-FE-21, shipped v3.2).

**Acceptance Criteria**
- Head of UX & Design reviews Research page against `docs/frontend/design_system.md`
- Regime lozenge constrained to single line (max-width or text truncation applied)
- Font usage on Research page conforms to the design system typography scale
- Any deviations from design system noted for backlog or immediate fix

---

### BLG-FE-27 — Nav bar redesign exploration
**Priority:** P3 (Low)
**Type:** Frontend / UX Design
**Owner:** Head of UX & Design
**Source:** v3.2 delivery verification — user feedback 2026-05-06
**Effort:** M (~1–2 days design + spec)
**Provisional-Target:** Arc 3 (design exploration — not urgent; no current blocking workflow)

**Problem**
The current nav bar occupies a fixed portion of the visible screen area. As the application grows in Arc 2 and beyond, the navigation structure may benefit from a redesign to reclaim vertical space. Options to evaluate: Sticky/Fixed Header (current pattern, optimised), mega menu (grouped sections), or breadcrumb navigation (context-sensitive, minimal footprint).

**Scope**
- Head of UX & Design to evaluate the three navigation patterns in the context of current and Arc 2 page inventory
- Produce a design recommendation with rationale (no implementation required at this stage)
- If redesign is recommended, produce a UX spec and create a follow-on implementation backlog item

**Acceptance Criteria**
- Design recommendation document produced (one of: maintain current, redesign to pattern X)
- Rationale covers: screen real-estate impact, mobile responsiveness, Arc 2 page count
- If redesign: UX spec produced and implementation backlog item filed

---

*BLG-FE-28 (Pre-Trade Research View UX spec) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-FE-29 (Watchlist research status indicator) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-30 (Trade plan status badges) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

## 4. Backend & Data Backlog


---

*BLG-AI-02 (Model version contract for AI Journal) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-AI-03 (AI Journal Summarisation quarterly review cadence) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

## 5. QA & Test Automation Backlog

---

*BLG-QA-18 (Screener accuracy test protocol) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-QA-14 (Author Playwright E2E test suite for entry checklist) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*TEST-GAP-ST14 (AI audit service unit tests) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-QA-15 (PT-02 research view acceptance test protocol) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-QA-16 (Research endpoint integration test coverage) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-QA-17 (Research view test scenario library) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

## 6. Operations & Infrastructure Backlog

---

### BLG-OPS-13 — Add new v2.8/v2.9/v3.0/v3.4 endpoints to api_performance_baseline.md re-run
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** v2.9 post-ship closure 2026-04-24 (3 endpoints); v3.0 post-ship closure 2026-04-28 OA-v30-01 (5 additional endpoints); v3.1 post-ship closure 2026-05-05 (10 additional endpoints); v3.4 post-ship closure 2026-05-14 (2 additional endpoints)
**Effort:** M (~2 days — 20 endpoints total)
**Provisional-Target:** Before next performance baseline review

**Problem**
Twenty endpoints shipped in v2.8/v2.9/v3.0/v3.1/v3.4 are absent from `docs/ops/api_performance_baseline.md`. Performance re-runs require a live environment and human coordination — baseline updates cannot be automated.

**Scope (updated 2026-05-14):**
- v2.8/v2.9 endpoints (3): `POST /ai/journal-summary`, `GET /ai/journal-summary/history`, `GET /v1beta1/news`
- v3.0 endpoints (5): `GET /ticker-universe`, `POST /ticker-universe`, `DELETE /ticker-universe/{ticker}`, `GET /screener/results`, `POST /screener/run`
- v3.1 endpoints (10): `POST /trade-plans`, `GET /trade-plans/{id}`, `PUT /trade-plans/{id}`, `DELETE /trade-plans/{id}`, `GET /trade-plans/by-position/{position_id}`, `GET /trade-plans/by-ticker/{ticker}`, `GET /research/{ticker}`, `GET /earnings/{ticker}`, `GET /reports/monthly-pnl`, plus any additional v3.1 routes
- v3.4 endpoints (2): `GET /portfolio/drawdown-status`, `GET /portfolio/concentration-status`
- Run each against staging to obtain p50/p95 latencies and add to `docs/ops/api_performance_baseline.md`

**Acceptance Criteria**
- All 20 endpoints have p50 and p95 latency entries in the baseline document
- Entries consistent with existing baseline measurement methodology

---

*BLG-OPS-14 (AI Journal monitoring metrics) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*
*BLG-OPS-12 (External API health check extension) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-OPS-15 (Research endpoint latency monitoring) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-SEC-06 (Trade plan data sensitivity classification) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-SEC-05 (Alpaca API key rotation policy and credential audit) — ✅ COMPLETE v3.2 — archived to backlog_archive.md 2026-05-09*

---

## 7. Spec Debt Backlog

*BLG-SPEC-20 deferred to §9 (DL-023, 2026-04-24).*

---

*BLG-SPEC-24 (PT-02 research view canonical spec) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-SPEC-25 (PT-02 research endpoint API contract) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-SPEC-26 (Research view data source provenance spec) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

### BLG-SPEC-27 — Research endpoint: surface per-source error codes as distinct HTTP responses
**Priority:** P3 (Low)
**Type:** Specification / API Contract
**Owner:** API Contracts & Documentation Owner
**Source:** ST-08 (EPIC-03, v3.3) — P3 delivery deviation (DoQ reclassification from P2 sprint_close filing)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v3.4 or v4.x (non-blocking; current behaviour is documented)

**Problem**
The research_endpoint.md AC specified distinct HTTP error codes (404 ticker-not-found, 503 source-unavailable, 429 rate-limited). The implementation always returns 200 with null sub-fields on sub-source failure. This is a known limitation documented in research_endpoint.md §Error Responses, but the spec-vs-impl divergence remains an open deviation (filed at sprint close v3.3 as P2; DoQ counter-confirmed P3 in qa_evidence_EPIC-03.md).

**Scope**
- Update GET /research/{ticker} to return 404 when ticker does not exist in any source
- Return 503 when a required external source (Yahoo Finance) is entirely unavailable
- Update research_endpoint.md §Error Responses to reflect new HTTP codes
- Update openapi.yaml 4xx/5xx response entries for this endpoint

**Acceptance Criteria**
- 404 returned when ticker lookup fails across all sources
- 503 returned for critical source failure (not partial field-level null)
- research_endpoint.md §Error Responses updated; BLG-SPEC-25 backlog reference corrected to BLG-SPEC-27
- No regression in 200+null behaviour for partial source failures

---

*BLG-SPEC-28 (Update trade_plan.md §6.2 entry checklist field references) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

### BLG-SPEC-29 — Correct grace-period-alert ux_spec.md §5 dismiss storage to sessionStorage
**Priority:** P3 (Low)
**Type:** Specification / Documentation
**Owner:** Head of UX & Design
**Source:** EPIC-01 ST-02 DEV-01 (v3.4 delivery deviation — 2026-05-14)
**Effort:** XS (~0.25 day)
**Provisional-Target:** v3.5

**Problem**
grace-period-alert/ux_spec.md §5 specifies `localStorage` for dismiss persistence, but the v3.4 implementation uses `sessionStorage`. The AC wording ("does not reappear on page reload within the same browser session") matches sessionStorage behaviour. The spec needs updating to reflect the delivered implementation.

**Acceptance Criteria**
- §5 updated to reference `sessionStorage` (not `localStorage`) for dismiss persistence
- §5 note added: dismiss resets on tab close; alert reappears on next browser session
- No implementation change required — implementation is correct

---

### BLG-SPEC-30 — Correct stop-management-workflow ux_spec.md §4.4 stop-update HTTP verb to PATCH
**Priority:** P3 (Low)
**Type:** Specification / Documentation
**Owner:** Head of UX & Design
**Source:** EPIC-01 ST-03 DEV-02 (v3.4 delivery deviation — 2026-05-14)
**Effort:** XS (~0.25 day)
**Provisional-Target:** v3.5

**Problem**
stop-management-workflow/ux_spec.md §4.4 specifies `PUT /positions/{id}` for the stop update call, but the v3.4 implementation uses `PATCH /positions/{id}`. PATCH is the correct HTTP verb for partial field updates; the existing endpoint supports it. The spec needs updating to match.

**Acceptance Criteria**
- §4.4 updated to reference `PATCH /positions/{id}` instead of `PUT /positions/{id}`
- No implementation change required — implementation is correct

---

### BLG-SPEC-31 — Review React Query v5 onSuccess migration impact across codebase
**Priority:** P3 (Low)
**Type:** Specification / Engineering
**Owner:** Head of Engineering
**Source:** EPIC-03 ST-10 DEV-01 (v3.4 delivery deviation — 2026-05-14)
**Effort:** S (~0.5 day)
**Provisional-Target:** v3.5

**Problem**
React Query v5 removed `onSuccess` from `useQuery`. In ST-10, this affected `isAbandoned` derivation (fixed by deriving from `existingPlan?.status`). Other useQuery calls in the codebase may still have `onSuccess` that silently does not fire. A codebase scan is needed to confirm no other behavioural gaps exist.

**Acceptance Criteria**
- Scan all `useQuery` calls for `onSuccess` usage
- Any affected patterns fixed or documented
- If no issues found: file closure note in backlog

---

## 8. Governance Backlog



---

*BLG-GOV-19 (PT-05 entry checklist §13 compliance review) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-GOV-20 (Trade plan field extension governance) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

### BLG-GOV-21 — Arc 4 data requirements capture
**Priority:** P3 (Low)
**Type:** Governance / Planning
**Owner:** Head of UX & Design + Product Owner
**Source:** IDEA-head-of-ux-20260508-02 — promoted cycle 2026-05-08__scheduled (DL-025)
**Effort:** XS–S (~0.5 day)
**Provisional-Target:** Before Arc 4 planning begins (v3.4+)
**Scope constraint:** Data needs only — no UX design, no feature specification, no implementation commitment

**Problem**
Arc 4 (AI Integration) and future arcs will require data that is not currently stored in the system (e.g. qualitative trade setup notes, pre-entry research snapshot, confidence level). If Arc 4 planning begins without a prior data requirements capture, the team will discover missing data mid-arc, requiring retroactive data model changes or compromised AI features.

**Scope**
- Lightweight document capturing data points not currently stored that Arc 4 features will likely need
- Format: field name, purpose, type, source (user input / calculated / external), and why it cannot be derived from existing data
- Covers: AI context inputs, qualitative annotations, pre-entry state snapshots
- Explicitly not: UX design, feature specification, or implementation commitment
- Delivered as a reference input for Arc 4 sprint planning

**Acceptance Criteria**
- Data requirements capture document lists Arc 4 data needs not currently stored
- Each entry specifies purpose and why existing data is insufficient
- Document explicitly notes it is not a feature specification or implementation commitment
- Delivered before Arc 4 planning begins

---

### BLG-GOV-22 — sprint_planning_prompt.md patch: shared execution_state.json ownership + multi-EPIC Positions.js conflict guidance
**Priority:** P2 (Medium)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** v3.4 lessons_learnt Phase 3 items #1 and #4 (2026-05-14) — cross-EPIC merge conflict recurrence; note: referenced as BLG-GOV-21 in lessons_learnt, but that ID was already assigned (Arc 4 data requirements) — corrected to BLG-GOV-22
**Effort:** S (~0.5 day)
**Provisional-Target:** v3.5

**Problem**
Three of four v3.4 EPICs required manual conflict resolution at merge time due to: (a) `execution_state.json` created independently on each branch, and (b) `src/pages/Positions.js` modified by three branches (EPIC-01, EPIC-02, EPIC-03). This is a recurrence from v3.3 Phase 3 item #2.

**Scope**
- sprint_planning_prompt.md: add rule for shared execution_state.json ownership (first EPIC branch creates; others check for existence before creating)
- sprint_backlog.md template: note merge order and shared file ownership explicitly
- UX spec guidance: document component stacking order for shared pages (Positions.js) so conflict resolution has a reference

**Acceptance Criteria**
- sprint_planning_prompt.md updated with shared execution_state.json rule
- Merge order and shared file notes in sprint_backlog.md template
- Head of Specs Team sign-off applied

---

*BLG-GOV-18 (External API dependency risk register) — ✅ COMPLETE v3.2 — archived to backlog_archive.md 2026-05-09*

---

*BLG-GOV-11 (Cycle artefact inventory and maintenance review) — ✅ COMPLETE v3.2 — archived to backlog_archive.md 2026-05-09*

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

*BLG-FEAT-13 (Add gated feature rollout capability) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*Items from §13 (BLG-FEAT-13) remain active. All §14 items (BLG-GOV-13, BLG-FEAT-16, BLG-QA-13) shipped in v2.8 — archived to backlog_archive.md 2026-04-20 (GROOM-20260420-01).*

---

## Test Scenario Gaps — v3.1 Delivery Verification

*Added by Delivery Verification Engine — 2026-05-05*

### TEST-GAP-EPIC-01 — Trade Plan test scenario coverage gap (v3.1) ✅ COMPLETE v3.2

**Source:** Delivery verification 2026-04-29__release-v3.1
**Priority:** P3
**Target:** v3.2 (before next sprint touching Trade Plan domain)

Test coverage gap from 2026-04-29__release-v3.1: `tests/e2e/trade-plan.spec.js` (SC-TP-01–07) was created as part of EPIC-01 delivery but not registered in `execution_state.json test_scenarios` field. QA & Testing Owner to verify Playwright test coverage and register in test_scenarios for the Trade Plan domain. Backend CRUD integration test scenarios for `/trade-plans` endpoints also warranted.

---

### TEST-GAP-EPIC-03 — Earnings Calendar and UK screener test registration gap (v3.1) ✅ COMPLETE v3.2

**Source:** Delivery verification 2026-04-29__release-v3.1
**Priority:** P3
**Target:** v3.2 (before next sprint touching Earnings/Screener domain)

Test coverage gap from 2026-04-29__release-v3.1: `tests/e2e/earnings-calendar.spec.js` (SC-EARN-01–09) and `tests/e2e/screener-uk-suffix.spec.js` (SC-UK-01–04) were created during EPIC-03 delivery but not registered in `execution_state.json test_scenarios` field. QA & Testing Owner to verify coverage completeness and ensure test files are registered per `execution_prompt.md §3.1.A` advisory.

---

## Release Slice — v3.2 Arc 2 Pre-Trade Research & Planning

<!-- release-plan-marker: RP:v3.2:2026-05-05__release-v3.2 -->

*Added by Release Planning Engine — 2026-05-05*
*Cycle: 2026-05-05__release-v3.2*
*Backlog slice: claude/cycles/2026-05-05__release-v3.2/stage4_backlog_slice.md*

| Story | EPIC | Sprint | Title |
|-------|------|--------|-------|
| ST-01 | EPIC-01 | 1 | Pre-trade research view component — data display |
| ST-02 | EPIC-01 | 1 | Trade plan context panel in research view |
| ST-03 | EPIC-01 | 1 | Prospective heat at entry metric integration (PT-03) |
| ST-04 | EPIC-01 | 1 | Navigation integration — screener and watchlist entry points to research view |
| ST-05 | EPIC-02 | 2 | Entry checklist schema, component, and Trade Plan form integration |
| ST-06 | EPIC-02 | 2 | Checklist pre-population from trade plan data and research view link |
| ST-07 | EPIC-03 | 1 | sprint_planning_prompt.md STEP 0 main-branch verification |
| ST-08 | EPIC-03 | 1 | execution_prompt.md STEP 5.1 deviations_filed enforcement |
| ST-09 | EPIC-03 | 1 | execution_prompt.md §3.1.A test_scenarios post-story advisory |
| ST-10 | EPIC-03 | 1 | Playwright waitFor pattern — test authoring standard |
| ST-11 | EPIC-03 | 1 | Trade Plan domain test scenario registration (TEST-GAP-EPIC-01) |
| ST-12 | EPIC-03 | 1 | Earnings Calendar and UK screener test registration (TEST-GAP-EPIC-03) |
| ST-13 | EPIC-04 | 2 | React component inventory (BLG-FE-16) |
| ST-14 | EPIC-04 | 2 | Design system document (BLG-FE-21) |
| ST-15 | EPIC-04 | 2 | Alpaca credential audit and rotation policy (BLG-SEC-05) |
| ST-16 | EPIC-04 | 2 | External API dependency risk register (BLG-GOV-18) |
| ST-17 | EPIC-04 | 2 | Cycle artefact inventory and maintenance review (BLG-GOV-11) |

*✅ ALL 17 STORIES SHIPPED — COMPLETE v3.2 — 2026-05-08 — cycle: 2026-05-05__release-v3.2*

---

## Release Slice — v3.3 Arc 3 In-Trade Risk Management

<!-- release-plan-marker: RP:v3.3:2026-05-09__release-v3.3 -->

*Added by Release Planning Engine — 2026-05-09*
*Cycle: 2026-05-09__release-v3.3*
*Backlog slice: claude/cycles/2026-05-09__release-v3.3/stage4_backlog_slice.md*

| Story | EPIC | Sprint | Title |
|-------|------|--------|-------|
| ST-01 | EPIC-01 | 1 | Positions data model — lifecycle state fields and migration |
| ST-02 | EPIC-01 | 1 | Position lifecycle state machine backend service |
| ST-03 | EPIC-01 | 1 | Position lifecycle state — frontend display |
| ST-04 | EPIC-02 | 2 | Grace Period Decision Support backend (IT-02) |
| ST-05 | EPIC-02 | 2 | Grace Period Decision Support frontend (IT-02) |
| ST-06 | EPIC-02 | 2 | Stop Management Workflow backend (IT-03) |
| ST-07 | EPIC-02 | 2 | Stop Management Workflow frontend (IT-03) |
| ST-08 | EPIC-03 | 1 | PT-02 research API contract (BLG-SPEC-25) + data source provenance spec (BLG-SPEC-26) |
| ST-09 | EPIC-03 | 1 | PT-02 canonical research view spec (BLG-SPEC-24) + UX spec (BLG-FE-28) |
| ST-10 | EPIC-03 | 1 | Research view test scenario library (BLG-QA-17) + acceptance test protocol (BLG-QA-15) |
| ST-11 | EPIC-03 | 1 | Entry checklist Playwright E2E tests (BLG-QA-14) |
| ST-12 | EPIC-03 | 1 | Research endpoint integration tests (BLG-QA-16) + latency baseline (BLG-OPS-15) + trade plan sensitivity classification (BLG-SEC-06) + field extension governance (BLG-GOV-20) |
| ST-13 | EPIC-04 | 1 | execution_prompt.md governance patches: sealed-file check (OA-01/CF-01) + mock payload advisory (OA-02/CF-02) |
| ST-14 | EPIC-04 | 1 | Governance policy patches: design gate check (OA-05) + backlog deferral policy (OA-03/CF-03) |
| ST-15 | EPIC-04 | 1 | PT-05 entry checklist §13 compliance review (BLG-GOV-19) |
| ST-16 | EPIC-04 | 2 | Feature flag rollout — mandatory (BLG-FEAT-13) |
| ST-17 | EPIC-04 | 2 | Trade plan abandonment + status badges + frontend quick wins (BLG-FEAT-21, BLG-FE-30, BLG-FE-23/24/25/29) |

*✅ 14 STORIES SHIPPED — COMPLETE v3.3 — 2026-05-13 — cycle: 2026-05-09__release-v3.3*
*3 stories returned to backlog: ST-03 (lifecycle badge frontend), ST-05 (grace period alert frontend), ST-07 (stop trail frontend) — see "Returned to Backlog v3.3" section below*
*ST-17 partial: backend (DS-06 + abandonment API) done; frontend sub-deliverables (BLG-FE-30, BLG-FE-23/24/25/29) deferred to v3.4*

---

## Returned to Backlog — v3.3 Sprint Close (2026-05-12)

*ST-03 — Position lifecycle state: frontend display (EPIC-01 / 2026-05-09__release-v3.3)*
✅ DELIVERED v3.4 (ST-01 EPIC-01 — 2026-05-14): LifecycleBadge component with arc3_lifecycle_display flag, SC-LS-01–04 Playwright pass.

*ST-05 — Grace Period Decision Support frontend (IT-02) (EPIC-02 / 2026-05-09__release-v3.3)*
✅ DELIVERED v3.4 (ST-02 EPIC-01 — 2026-05-14): GracePeriodAlertZone with sessionStorage dismiss, SC-GP-01–03 Playwright pass.

*ST-07 — Stop Management Workflow frontend (IT-03) (EPIC-02 / 2026-05-09__release-v3.3)*
✅ DELIVERED v3.4 (ST-03 EPIC-01 — 2026-05-14): TrailStopModal with PATCH /positions/{id} stop update, SC-TS-01–03 Playwright pass.

---

## Test Scenario Gaps — v3.3 Delivery Verification

*Added by Delivery Verification Engine — 2026-05-13*

*TEST-GAP-EPIC-01-v33 (Position lifecycle badge Playwright E2E scenarios) — ✅ RESOLVED v3.4 — archived to backlog_archive.md 2026-05-14*

---

*TEST-GAP-EPIC-02-v33 (Grace period alert and trail stop Playwright E2E scenarios) — ✅ RESOLVED v3.4 — archived to backlog_archive.md 2026-05-14*

---

## Release Slice — v3.4 Arc 3 In-Trade Risk Management (continued)

<!-- release-plan-marker: RP:v3.4:2026-05-14__release-v3.4 -->

*Added by Release Planning Engine — 2026-05-14*
*Cycle: 2026-05-14__release-v3.4*
*Backlog slice: claude/cycles/2026-05-14__release-v3.4/stage4_backlog_slice.md*

| Story | EPIC | Sprint | Title |
|-------|------|--------|-------|
| ST-01 | EPIC-01 | 2 | Position lifecycle state: frontend display (IT-01) |
| ST-02 | EPIC-01 | 2 | Grace Period Decision Support frontend (IT-02) |
| ST-03 | EPIC-01 | 2 | Stop Management Workflow frontend (IT-03) |
| ST-04 | EPIC-02 | 2 | Drawdown-Triggered Review Prompt backend (IT-04) |
| ST-05 | EPIC-02 | 2 | Drawdown-Triggered Review Prompt frontend (IT-04) |
| ST-06 | EPIC-02 | 2 | Position Concentration Limits backend + frontend (IT-05) |
| ST-07 | EPIC-03 | 1 | Research page UK suffix strip + negative earnings days (BLG-FE-23 + BLG-FE-24) |
| ST-08 | EPIC-03 | 1 | Signals page: default to most recent day's signals (BLG-FE-25) |
| ST-09 | EPIC-03 | 1 | Watchlist research status indicator (BLG-FE-29) |
| ST-10 | EPIC-03 | 1 | Trade plan status badges + abandonment UI (BLG-FE-30 + BLG-FEAT-21 frontend) |
| ST-11 | EPIC-04 | 1 | Research view component library (BLG-FE-31) |
| ST-12 | EPIC-04 | 1 | Screener morning routine UX spec (BLG-FE-22) |
| ST-13 | EPIC-04 | 1 | trade_plan.md §6.2 spec update + AI journal review cadence (BLG-SPEC-28 + BLG-AI-03) |
| ST-14 | EPIC-04 | 1 | Screener accuracy test protocol (BLG-QA-18) |

**Theme:** Arc 3 Frontend Completion + IT-04/05 Risk Prompts + Frontend Quick Wins + Spec/QA Debt

*✅ ALL 14 STORIES SHIPPED — COMPLETE v3.4 — 2026-05-14 — cycle: 2026-05-14__release-v3.4*

---

### TEST-GAP-EPIC-03-v33 — SC-RV-18 and SC-RV-19 explicit Playwright coverage for null handling

**Source:** Delivery verification 2026-05-09__release-v3.3 (STEP 5)
**Priority:** P3
**Target:** v3.4 (before research view frontend implementation)

research_view_protocol.md §2.3 notes SC-RV-18 (regime null only) and SC-RV-19 (all fields null — degraded mode) as needing explicit Playwright scenarios and flags "backlog item filed". The backlog item was not actually filed at sprint close — this is that item.

Required scenarios (to be added alongside SC-RV-01 through SC-RV-17 when research view frontend is implemented):
- SC-RV-18: GET /research/{ticker} returns regime null → UI shows regime panel in "unavailable" state
- SC-RV-19: All data fields null (all sources failed) → degraded mode display, no crash, user-visible error state per UX spec

QA & Testing Owner to add these scenarios to `docs/qa/test_scenarios/research_view_scenarios.md` and update `docs/qa/acceptance_protocols/research_view_protocol.md` to mark item as resolved.
