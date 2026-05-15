# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-05-15 (groom backlog — v3.5 post-ship: 6 items archived BLG-SPEC-29/30/31, BLG-QA-19, BLG-GOV-21/22; release slice §12 removed)
**Last rebalance:** 2026-05-15 (cycle 2026-05-15__scheduled — DL-029 backlog add × 1 BLG-QA-19)

> ⚠️ Standing Notice
> This backlog records prioritisation and intent only.
> All formulas, schemas, API contracts, and behavioural rules are indicative until
> confirmed in the relevant canonical specifications.
> No item may proceed to implementation without canonical owner sign-off.

> 📋 Placement Rule
> New items must be appended to the correct existing type section (§1–§8). Do not create new numbered session sections. The backlog is organised by type, not by session date.
> **Ephemeral sections** (Release Slice tables, Test Scenario Gap sections, and "Returned to Backlog" sections appended by governance engines) are temporary. They must be removed during the next `groom backlog` run after the cycle closes. Any still-open items within them must be promoted to the appropriate §1–§8 type section before the ephemeral section is removed.

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

### BLG-FE-32 — Research view: SC-RV-18/SC-RV-19 Playwright coverage for null/degraded state scenarios
**Priority:** P3 (Low)
**Type:** Frontend / QA
**Owner:** QA Lead
**Source:** research_view_protocol.md §5 (v3.3 sign-off gap); regression_protocol.md §2.2 (v3.5 ST-10)
**Effort:** S (~0.5 day)
**Provisional-Target:** v3.6

**Problem**
SC-RV-18 (regime field null) and SC-RV-19 (all research fields null) were identified as partially covered in v3.3 QA evidence and confirmed as pending in the v3.5 regression protocol. Until these scenarios have explicit Playwright tests, they require human staging sign-off in each sprint that touches the research view.

**Acceptance Criteria**
- Playwright test added for SC-RV-18: regime field null — regime badge degrades gracefully (no crash, placeholder shown)
- Playwright test added for SC-RV-19: all research fields null — no crash, all sections show appropriate placeholders
- Tests added to `tests/e2e/pre-trade-research.spec.js`
- `research_view_regression_protocol.md` §2.2 updated to reflect Playwright coverage (remove staging caveat)

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

### TEST-GAP-EPIC-03-v33 — SC-RV-18 and SC-RV-19 explicit Playwright coverage for null handling
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-05-09__release-v3.3 (STEP 5) — backlog item formally filed 2026-05-15
**Effort:** S (~0.5 day)
**Provisional-Target:** Before next research view frontend enhancement

**Problem**
research_view_protocol.md §2.3 notes SC-RV-18 (regime null only) and SC-RV-19 (all fields null — degraded mode) as requiring explicit Playwright scenarios. The item was flagged at sprint close but never formally filed.

**Scope**
- Add SC-RV-18 to `docs/qa/test_scenarios/research_view_scenarios.md`: GET /research/{ticker} returns regime null → UI shows regime panel in "unavailable" state
- Add SC-RV-19: all data fields null (all sources failed) → degraded mode display, no crash, user-visible error state per UX spec
- Update `docs/qa/acceptance_protocols/research_view_protocol.md` §2.3 to mark item as resolved

**Acceptance Criteria**
- SC-RV-18 and SC-RV-19 added to `docs/qa/test_scenarios/research_view_scenarios.md`
- research_view_protocol.md §2.3 updated to reference both scenarios as filed
- Playwright coverage or human staging sign-off recorded for both null states

---

*BLG-QA-19 (Research view regression test protocol) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

## 6. Operations & Infrastructure Backlog

---

### BLG-OPS-13 — Add new v2.8/v2.9/v3.0/v3.4 endpoints to api_performance_baseline.md re-run
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** v2.9 post-ship closure 2026-04-24 (3 endpoints); v3.0 post-ship closure 2026-04-28 OA-v30-01 (5 additional endpoints); v3.1 post-ship closure 2026-05-05 (10 additional endpoints); v3.4 post-ship closure 2026-05-14 (2 additional endpoints); v3.5 post-ship closure 2026-05-15 (2 additional endpoints)
**Effort:** M (~2 days — 22 endpoints total)
**Provisional-Target:** Before next performance baseline review

**Problem**
Twenty-two endpoints shipped in v2.8/v2.9/v3.0/v3.1/v3.4/v3.5 are absent from `docs/ops/api_performance_baseline.md`. Performance re-runs require a live environment and human coordination — baseline updates cannot be automated.

**Scope (updated 2026-05-15):**
- v2.8/v2.9 endpoints (3): `POST /ai/journal-summary`, `GET /ai/journal-summary/history`, `GET /v1beta1/news`
- v3.0 endpoints (5): `GET /ticker-universe`, `POST /ticker-universe`, `DELETE /ticker-universe/{ticker}`, `GET /screener/results`, `POST /screener/run`
- v3.1 endpoints (10): `POST /trade-plans`, `GET /trade-plans/{id}`, `PUT /trade-plans/{id}`, `DELETE /trade-plans/{id}`, `GET /trade-plans/by-position/{position_id}`, `GET /trade-plans/by-ticker/{ticker}`, `GET /research/{ticker}`, `GET /earnings/{ticker}`, `GET /reports/monthly-pnl`, plus any additional v3.1 routes
- v3.4 endpoints (2): `GET /portfolio/drawdown-status`, `GET /portfolio/concentration-status`
- v3.5 endpoints (2): `GET /portfolio/paper-positions`, `GET /trades/{trade_id}/plan-vs-reality`
- Run each against staging to obtain p50/p95 latencies and add to `docs/ops/api_performance_baseline.md`

**Acceptance Criteria**
- All 22 endpoints have p50 and p95 latency entries in the baseline document
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

*BLG-SPEC-29 (Correct grace-period-alert ux_spec.md §5 dismiss storage to sessionStorage) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

*BLG-SPEC-30 (Correct stop-management-workflow ux_spec.md §4.4 stop-update HTTP verb to PATCH) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

*BLG-SPEC-31 (Review React Query v5 onSuccess migration impact across codebase) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

## 8. Governance Backlog



---

*BLG-GOV-19 (PT-05 entry checklist §13 compliance review) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-GOV-20 (Trade plan field extension governance) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-GOV-21 (Arc 4 data requirements capture) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

*BLG-GOV-22 (sprint_planning_prompt.md patch: shared execution_state.json ownership + multi-EPIC Positions.js conflict guidance) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

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

