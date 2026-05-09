# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-05-08 (rebalance 2026-05-08__scheduled — DL-025 backlog adds × 16)
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

### BLG-FEAT-21 — Trade plan abandonment status field
**Priority:** P2 (Medium)
**Type:** Product Feature / Data Model
**Owner:** Product Owner
**Source:** IDEA-challenger-20260508-02 — promoted cycle 2026-05-08__scheduled (DL-025)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v3.3

**Problem**
Trade plans can currently be in Active or Closed states but there is no mechanism to record that a plan was abandoned before a position was opened (e.g. entry conditions never met, thesis invalidated, sizing constraints made the trade unfeasible). Abandoned plans currently sit in an ambiguous incomplete state with no rationale captured, making retrospective plan quality review impossible.

**Scope**
- Add `Abandoned` as a valid trade plan status
- Add a required `abandonment_reason` field (free text, short — required when status is set to Abandoned)
- Surface abandoned plans alongside closed plans in the trade plan history view
- Backend: add status transition logic (Draft/Research → Abandoned; Active positions may not be abandoned)
- Frontend: abandonment action with reason input

**Acceptance Criteria**
- Trade plan can be set to Abandoned status via UI with a required reason
- Abandoned plans appear in plan history with abandonment reason displayed
- Active positions linked to a plan cannot be abandoned (guard enforced)
- No regression in existing plan status transitions

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

### BLG-FE-22 — Screener morning routine UX spec
**Priority:** P2 (Medium)
**Type:** Frontend / UX Specification
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-product-owner-20260421-01 — promoted cycle 2026-05-05__scheduled (DL-024)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Before v3.2 sprint planning

**Problem**
The screener is live (v3.0) with DS-07 watchlist promotion. The current multi-surface flow (screener results → watchlist → pre-trade research) has no designed continuity. Arc 2 PT-02 (Pre-Trade Research View) needs a clear workflow spec for how users navigate from screener discovery to research — otherwise PT-02 UX risks being designed in isolation from the Arc 1→Arc 2 transition.

**Scope**
- UX workflow spec for the Arc 1→Arc 2 morning routine: screener results → shortlist → watchlist promotion → pre-trade research navigation
- Answers: after promoting candidates, how does the user navigate to research? What context carries between screens?
- Not a UI design spec (wireframes/mockups) — a workflow and information-carry spec
- Input to PT-02 UX design at v3.2 sprint planning

**Acceptance Criteria**
- Workflow spec documents the step-by-step morning routine from screener to research
- Information-carry decisions documented: what data from the screener should be visible in the research view
- Navigation model specified: how the user moves between screener, watchlist, and research views
- Delivered before v3.2 sprint planning so it informs PT-02 UX story authoring

---

### BLG-FE-23 — Research page UK ticker suffix not stripped
**Priority:** P3 (Low)
**Type:** Frontend / Bug Fix
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** v3.2 delivery verification — manual staging 2026-05-06 (DEV-E01-03)
**Effort:** XS (~30 min)
**Provisional-Target:** v3.3 (or alongside EPIC-01 P1 fix)

**Problem**
`stripUkSuffix` was applied to the screener and watchlist table displays in v3.1 (BLG-FE-20) but was not applied to the Research page (`Research.js`) ticker display in the page title/header. UK tickers therefore appear with `.L` suffix (e.g. `MTLN.L`) in the Research page heading, inconsistent with the rest of the application.

**Acceptance Criteria**
- Research page title/header strips `.L` suffix from UK tickers using the existing `stripUkSuffix` utility
- `MTLN.L` displays as `MTLN` in the Research page header
- No regression in screener or watchlist UK suffix stripping

---

### BLG-FE-24 — Negative earnings days display for past earnings dates
**Priority:** P3 (Low)
**Type:** Frontend / Bug Fix
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** v3.2 delivery verification — manual staging 2026-05-06; origin v3.1 EPIC-03 earnings calendar
**Effort:** XS (~30 min)
**Provisional-Target:** v3.3

**Problem**
When a ticker's `next_earnings_date` is in the past, `days_until_earnings` is returned as a negative integer (e.g. `-27` for MTLN.L). The earnings display renders this as a negative number rather than showing `—` (the convention for unavailable/not-applicable data). Users see confusing negative counts.

**Acceptance Criteria**
- When `days_until_earnings` is negative (past earnings date), display `—` in all earnings columns (screener, watchlist, positions)
- When `days_until_earnings` is zero: display `Today`
- No regression in positive days display or earnings proximity warning (≤5 days amber)

---

### BLG-FE-25 — Signals page: default to most recent day's signals
**Priority:** P2 (Medium)
**Type:** Frontend / Bug or UX
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** v3.2 delivery verification — manual staging 2026-05-06
**Effort:** S (~0.5 day)
**Provisional-Target:** v3.3

**Problem**
The Signals page currently shows all historical signals rather than defaulting to the most recent trading day. This makes the page cluttered and harder to action — the morning-routine use case is to review the current day's signals, not a full history. It is unclear whether this is a regression or original behaviour; investigation needed.

**Acceptance Criteria**
- Signals page defaults to displaying only the most recent trading day's signals on load
- A control exists to view older signals (e.g. date picker or "Show all" toggle)
- If this is a regression, root cause identified and documented
- No regression in signal data accuracy

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

### BLG-FE-28 — Pre-Trade Research View UX spec
**Priority:** P1 (High)
**Type:** Frontend / UX Specification
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-ux-20260508-01 — promoted cycle 2026-05-08__scheduled (DL-025)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Before v3.3 sprint planning

**Problem**
PT-02 (Pre-Trade Research View) requires a frontend implementation in v3.3, but no UX specification exists for the research view layout, data field placement, source attribution display, news feed design, or empty/error state handling. Without a UX spec, frontend implementation risks inconsistency with BLG-FE-21 (design system) and BLG-FE-22 (morning routine workflow).

**Scope**
- Layout specification: panel arrangement, data field hierarchy, visual hierarchy
- Data field placement: price, change, market cap, ATR, regime, news — with source attribution positioning
- Source attribution display: how Yahoo Finance / Alpaca provenance is shown (per BLG-SPEC-26 provenance requirement)
- News feed design: article format, truncation, link behaviour
- Freshness indicator: where displayed, format, staleness threshold
- Empty states: no data available, ticker not found, external API unavailable
- Error states: partial data (some fields missing), full failure
- References: BLG-FE-21 (design system), BLG-FE-22 (morning routine workflow), BLG-SPEC-24 (canonical spec)

**Acceptance Criteria**
- UX spec document covers all layout, field placement, source attribution, news feed, freshness indicator, and state designs
- Empty and error states explicitly specified (not left to implementation discretion)
- Document references design system tokens and workflow spec for consistency
- Delivered before v3.3 sprint planning to inform PT-02 frontend story authoring

---

### BLG-FE-29 — Watchlist research status indicator
**Priority:** P2 (Medium)
**Type:** Frontend / UX Enhancement
**Owner:** Product Owner
**Source:** IDEA-product-owner-20260508-02 — promoted cycle 2026-05-08__scheduled (DL-025)
**Effort:** XS (~0.5 day)
**Provisional-Target:** v3.3
**Scope constraint:** Binary flag only (done/not done) — no research quality signal

**Problem**
The watchlist shows tickers but provides no indication of whether pre-trade research has been completed for a given ticker. Users must navigate to the Research view to check. A binary status indicator on the watchlist would allow users to quickly identify which watchlisted tickers still need research before trade planning can begin.

**Scope**
- Add a binary research status indicator to each watchlist ticker row
- Done = PT-02 research was performed for this ticker (research record exists)
- Not Done = no research record found for this ticker
- Display: icon or badge — not text, to minimise column width impact
- No research quality score, no freshness judgement — binary only

**Acceptance Criteria**
- Watchlist table includes a Research Status column or indicator per ticker row
- Indicator shows done/not done state correctly based on research record existence
- No research quality or freshness information displayed (scope constraint)
- No regression in watchlist loading performance or existing columns

---

### BLG-FE-30 — Trade plan status badges
**Priority:** P2 (Medium)
**Type:** Frontend / UX Enhancement
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-base44-frontend-20260508-02 — promoted cycle 2026-05-08__scheduled (DL-025)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v3.3 (coordinate with BLG-FEAT-21 — Abandoned status)

**Problem**
Trade plans display status as plain text. As the trade plan lifecycle grows to include Abandoned status (BLG-FEAT-21) alongside existing states, consistent colour-coded status badges will be needed to make plan status immediately scannable across the trade plan list and detail views.

**Scope**
- Visual status badges for all trade plan statuses: Draft, Research Pending, Research Complete, Entry Conditions Set, Active, Closed, Abandoned
- Consistent colour coding: e.g. grey (Draft), amber (Research Pending), blue (Research Complete), purple (Entry Conditions Set), green (Active), muted (Closed), red (Abandoned)
- Apply in trade plan list view and trade plan detail view header
- Reference BLG-FE-21 (design system) for colour token alignment

**Acceptance Criteria**
- Status badges rendered consistently in trade plan list and detail views
- Each status has a distinct, accessible colour (contrast ratio ≥ 4.5:1)
- Colours aligned with design system tokens where applicable
- Abandoned status badge displays correctly (coordinate with BLG-FEAT-21)
- No regression in trade plan list rendering performance

---

## 4. Backend & Data Backlog


---

*BLG-AI-02 (Model version contract for AI Journal) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

### BLG-AI-03 — AI Journal Summarisation quarterly review cadence
**Priority:** P3 (Low)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer
**Source:** IDEA-ai-compliance-20260508-02 — promoted cycle 2026-05-08__scheduled (DL-025)
**Effort:** XS (~0.5 day per review, governance process definition)
**Provisional-Target:** Define process before v3.4; first review Q3 2026

**Problem**
AI Journal Summarisation (AI-SUM, shipped v2.8) is live in production using a specific Claude model version. As Claude model versions evolve, the feature's output quality, §13 compliance (display-only, no automated recommendation), and BLG-AI-02 model version contract may drift without a scheduled review mechanism. No cadence exists to verify the AI feature remains compliant and fit-for-purpose.

**Scope**
- Define a quarterly review process for AI Journal Summarisation
- Review checklist: output quality sample review, §13 compliance re-confirmation, BLG-AI-02 model version record update, error rate review from BLG-OPS-14 monitoring
- Document the process in a governance file; reference from OPERATIONAL_GUIDE
- First review: Q3 2026 (before v3.4 planning cycle)

**Acceptance Criteria**
- Quarterly review process defined and documented
- Review checklist specifies observable criteria (not subjective judgement)
- Process documented with authority (AI Compliance & Governance Officer) and escalation path if §13 concerns arise
- OPERATIONAL_GUIDE references the review process

---

## 5. QA & Test Automation Backlog

---

### BLG-QA-14 — Author Playwright E2E test suite for entry checklist (EPIC-02 / PT-05)
**Priority:** P2 (Medium)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** v3.2 EPIC-02 frontend testing gate (LL-v3.1-EX-01) — observable AC deferred — 2026-05-06
**Effort:** M (~1–2 days)
**Provisional-Target:** v3.3
**Reference:** `claude/cycles/2026-05-05__release-v3.2/qa_evidence_EPIC-02.md`

**Problem**
EPIC-02 delivered the pre-trade entry checklist (`EntryChecklist` component in `TradePlan.js` and `Research.js` read-only display) without Playwright E2E coverage. The frontend testing gate (LL-v3.1-EX-01) requires Playwright coverage for all observable AC, or a filed backlog item when deferred. 7 scenarios were identified but not authored, leaving the feature unverified at the E2E layer.

**Scope**
Author `tests/e2e/entry-checklist.spec.js` covering SC-CL-01 through SC-CL-07:
- SC-CL-01: Checklist renders in Trade Plan form with 4 default items
- SC-CL-02: Items can be toggled (checked/unchecked)
- SC-CL-03: State persists on save
- SC-CL-04: Pre-population — `stop_defined` pre-checked when `early_exit_conditions` present
- SC-CL-05: Pre-population — `research_reviewed` pre-checked when `r_target` set
- SC-CL-06: Review research link navigates to `/research/{ticker}`
- SC-CL-07: Read-only checklist renders correctly in Research view trade plan panel

**Acceptance Criteria**
- `tests/e2e/entry-checklist.spec.js` exists and all 7 scenarios pass in CI
- Scenarios registered in `execution_state.json test_scenarios` for the relevant EPIC
- No regression in existing test suite

---

*TEST-GAP-ST14 (AI audit service unit tests) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

### BLG-QA-15 — PT-02 research view acceptance test protocol
**Priority:** P1 (High)
**Type:** QA / Test Protocol
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260508-01 — promoted cycle 2026-05-08__scheduled (DL-025)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Before v3.3 sprint planning (prerequisite for PT-02 DoQ sign-off design)

**Problem**
The PT-02 Pre-Trade Research View will include observable UI behaviour (data field rendering, source attribution display, freshness indicator, news feed, error states). Per CLAUDE.md §2 governance, observable AC requires either Playwright coverage or human staging sign-off with date recorded. Without a pre-defined acceptance test protocol, DoQ sign-off criteria for PT-02 are undefined at sprint start, leading to ambiguous QA gates.

**Scope**
- Define observable acceptance criteria for each PT-02 UI component
- Specify which AC will be covered by Playwright vs human staging sign-off
- Define freshness indicator acceptance threshold (e.g. data ≤ N minutes old)
- Define source attribution acceptance criteria (correct attribution per data field)
- Define error state test scenarios (partial data, full API failure)
- Reference BLG-FE-28 (UX spec) and BLG-SPEC-24/25 (canonical spec and API contract)

**Acceptance Criteria**
- Acceptance test protocol document defines observable AC for all PT-02 UI components
- Each AC explicitly marked: Playwright (automated) or human staging sign-off
- Protocol reviewed by DoQ before v3.3 sprint planning
- Document filed in QA evidence path for EPIC tracking PT-02

---

### BLG-QA-16 — Research endpoint integration test coverage
**Priority:** P1 (High)
**Type:** QA / Test Automation
**Owner:** Head of Engineering + QA & Testing Owner
**Source:** IDEA-head-of-engineering-20260508-01 — promoted cycle 2026-05-08__scheduled (DL-025)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v3.3 (in-sprint alongside PT-02 backend)

**Problem**
`GET /research/{ticker}` was added in v3.2 hotfixes but integration test coverage for the research endpoint was not included. Per CLAUDE.md §2, every new backend route must be registered in `backend/routers/test.py` in the same commit. The endpoint exists without integration test coverage, leaving it unverified for response schema compliance, error handling, and data source fallback behaviour.

**Scope**
- Add `GET /research/{ticker}` to `backend/routers/test.py` with representative safe value (e.g. `AAPL`)
- Cover: successful response schema, partial data response (one source unavailable), full failure response
- Verify source attribution fields present in response
- Update hardcoded fallback count in `src/pages/SystemStatus.js` if endpoint count has changed

**Acceptance Criteria**
- `backend/routers/test.py` includes test entry for `GET /research/{ticker}`
- Test scenarios cover: success, partial source failure, full failure
- `SystemStatus.js` endpoint count updated if changed
- No regression in existing test suite

---

### BLG-QA-17 — Research view test scenario library
**Priority:** P1 (High)
**Type:** QA / Test Scenarios
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260508-01 — promoted cycle 2026-05-08__scheduled (DL-025)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Before v3.3 sprint planning (prerequisite for PT-02 sprint authoring)

**Problem**
No test scenarios exist for the PT-02 Pre-Trade Research View. Analogous to BLG-QA-09 (screener test data library, shipped v2.9), the research view needs a pre-defined scenario library before implementation begins. Without pre-defined scenarios, implementation-time test authoring is rushed and incomplete, leaving coverage gaps post-merge.

**Scope**
- Define test scenarios for: data field rendering (price, change, market cap, ATR, regime, earnings)
- Source attribution display scenarios (Yahoo Finance vs Alpaca attribution)
- News feed scenarios: articles present, no articles, Alpaca unavailable
- Freshness indicator scenarios: fresh data, stale data (threshold exceeded)
- Error state scenarios: ticker not found, Yahoo Finance unavailable, all sources unavailable
- Reference BLG-SPEC-24 (canonical spec) and BLG-FE-28 (UX spec) for expected behaviour

**Acceptance Criteria**
- Scenario library document exists covering all PT-02 research view observable scenarios
- Each scenario specifies: precondition, action, expected result
- Library reviewed by DoQ before v3.3 sprint planning
- Scenarios referenced in BLG-QA-15 (acceptance test protocol)

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

### BLG-OPS-15 — Research endpoint latency monitoring
**Priority:** P2 (Medium)
**Type:** Operations / Performance Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260508-01 — promoted cycle 2026-05-08__scheduled (DL-025)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v3.3 (alongside PT-02 backend delivery)

**Problem**
`GET /research/{ticker}` calls multiple external data sources (Yahoo Finance for price/news, Alpaca for additional data). Response times will be higher than internal endpoints and will vary as Arc 2 adds more data fields. No latency baseline exists for this endpoint, making regression detection impossible.

**Scope**
- Instrument `GET /research/{ticker}` with p50/p95 latency logging
- Add to `docs/ops/api_performance_baseline.md` (alongside BLG-OPS-13 scope)
- Define a latency target (e.g. p95 ≤ 3s for multi-source external API aggregation)
- Add monitoring note if latency exceeds target threshold

**Acceptance Criteria**
- Research endpoint latency measured and documented in the performance baseline
- p50/p95 values recorded after v3.3 implementation
- Latency target documented with rationale (multi-source aggregation baseline)

---

### BLG-SEC-06 — Trade plan data sensitivity classification
**Priority:** P2 (Medium)
**Type:** Security / Governance
**Owner:** Cybersecurity & Trust Lead
**Source:** IDEA-cybersecurity-20260508-01 — promoted cycle 2026-05-08__scheduled (DL-025)
**Effort:** XS–S (~0.5 day)
**Provisional-Target:** Before Arc 3 sprint planning

**Problem**
The `trade_plans` table contains fields of varying sensitivity: ticker (semi-public), entry zone (proprietary strategy detail), stop level (proprietary), R-target (proprietary), thesis (private journal content), entry checklist (private). No formal sensitivity classification exists. Arc 3/4 features may involve exporting, sharing, or displaying plan data in new contexts. Without a classification, access control decisions will be made ad-hoc.

**Scope**
- Classify each `trade_plans` field by sensitivity: Public (ticker), Internal (dates, status), Private (entry zone, stop, R-target, thesis, checklist)
- Document classification in a security reference document
- Define access control principles per classification level for Arc 3/4 feature design
- Not a compliance document — a design prerequisite for Arc 3/4

**Acceptance Criteria**
- Classification document covers all current `trade_plans` fields
- Three sensitivity levels defined (or equivalent) with access control principle per level
- Document referenced as input for any Arc 3/4 feature involving trade plan data exposure
- Document filed in `docs/specs/security/` or equivalent path

---

*BLG-SEC-05 (Alpaca API key rotation policy and credential audit) — ✅ COMPLETE v3.2 — archived to backlog_archive.md 2026-05-09*

---

## 7. Spec Debt Backlog

*BLG-SPEC-20 deferred to §9 (DL-023, 2026-04-24).*

---

### BLG-SPEC-24 — PT-02 research view canonical spec
**Priority:** P1 (High)
**Type:** Specification / Canonical
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260508-01 — promoted cycle 2026-05-08__scheduled (DL-025)
**Effort:** M (~1–2 days)
**Provisional-Target:** Before v3.3 sprint planning

**Problem**
The PT-02 Pre-Trade Research View has no canonical specification. The v3.2 hotfix delivered the research endpoint but the frontend implementation (PT-02's primary deliverable) has not been specced. Without a Class 2 canonical spec, frontend implementation will proceed without a defined source of truth for data fields, display rules, data freshness policy, and source attribution requirements.

**Scope**
- Class 2 canonical specification for the PT-02 research view
- Data fields: which fields are displayed (price, % change, market cap, ATR, regime, news, earnings)
- Data sources: which fields come from Yahoo Finance vs Alpaca, with attribution requirements
- Data freshness policy: maximum acceptable data age per field, staleness display behaviour
- Display rules: formatting, units, empty/null handling per field
- Reference: BLG-SPEC-25 (API contract), BLG-FE-28 (UX spec), BLG-SPEC-26 (provenance spec)
- References strategy_rules.md §13 for §13 compliance confirmation

**Acceptance Criteria**
- Class 2 canonical spec document created covering all data fields, sources, freshness policy, and display rules
- §13 compliance confirmed in spec front-matter
- Document references openapi.yaml entry for `GET /research/{ticker}`
- Reviewed and signed off by Head of Specs Team before v3.3 sprint planning

---

### BLG-SPEC-25 — PT-02 research endpoint API contract
**Priority:** P1 (High)
**Type:** Specification / API Contract
**Owner:** API Contracts & Documentation Owner
**Source:** IDEA-api-contracts-20260508-01 — promoted cycle 2026-05-08__scheduled (DL-025)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Before v3.3 sprint planning (alongside BLG-SPEC-24)

**Problem**
`GET /research/{ticker}` was added in v3.2 hotfixes and is in `openapi.yaml`, but no formal Class 2 API contract document exists in `docs/specs/api_contracts/`. Without a formal contract, response schema, error codes, data source attribution fields, and rate limit behaviour are undocumented — creating ambiguity for frontend implementation and integration test authoring.

**Scope**
- Formal Class 2 API contract for `GET /research/{ticker}`
- Request parameters: ticker format, market inference behaviour
- Response schema: all fields with types, nullable flags, and source attribution fields
- Error codes: ticker not found (404), external source unavailable (partial/503), rate limit (429)
- Rate limit policy: which external sources apply rate limits and how errors surface
- Reference BLG-SPEC-24 (canonical spec) and BLG-SPEC-26 (provenance spec)

**Acceptance Criteria**
- API contract document in `docs/specs/api_contracts/` covering all request/response fields
- Error codes and source attribution fields explicitly documented
- Rate limit behaviour specified per external source
- Contract consistent with openapi.yaml entry for `GET /research/{ticker}`

---

### BLG-SPEC-26 — Research view data source provenance spec
**Priority:** P1 (High)
**Type:** Specification / Data Integrity
**Owner:** Head of Specs Team
**Source:** IDEA-challenger-20260508-01 — promoted cycle 2026-05-08__scheduled (DL-025)
**Effort:** S (~0.5 day)
**Provisional-Target:** Before v3.3 sprint planning (prerequisite for BLG-SPEC-24 and BLG-FE-28)

**Problem**
The PT-02 research view aggregates data from multiple sources (Yahoo Finance, Alpaca, internal calculations). Without a provenance specification, the UI may display data fields without clear attribution, making it impossible for users to assess data freshness or identify which source is responsible for incorrect or stale data.

**Scope**
- Specification document defining the provenance attribution requirements for the research view
- Per data field: named source (Yahoo Finance, Alpaca, internal), retrieval timestamp display requirement
- Display format: how source attribution is shown in the UI (tooltip, label, icon)
- Retrieval timestamp: format and placement requirements per field or per panel
- Applies to all fields in BLG-SPEC-24 scope

**Acceptance Criteria**
- Provenance spec document defines source attribution for every data field in the research view
- Display format specified (not left to implementation discretion)
- Retrieval timestamp requirement specified per field/panel
- Incorporated as a required section reference in BLG-SPEC-24 (canonical spec)

---

## 8. Governance Backlog



---

### BLG-GOV-19 — PT-05 entry checklist §13 compliance review
**Priority:** P1 (High)
**Type:** Governance / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260508-01 — promoted cycle 2026-05-08__scheduled (DL-025)
**Effort:** XS (~0.5 day)
**Provisional-Target:** Before PT-05 sprint entry (prerequisite for PT-05 implementation)

**Problem**
PT-05 (Entry Conditions Checklist) involves the system prompting the user to confirm entry conditions before opening a position. This is a structured decision support feature. A formal §13 boundary review is required to confirm this does not constitute automated advisory or signal generation — the system must remain display-only and human-in-the-loop per strategy_rules.md §13.

**Scope**
- Formal §13 boundary review document for PT-05
- Confirm: entry checklist is display-only (user confirms each condition manually)
- Confirm: no automated condition evaluation or automated recommendation generated
- Confirm: system does not determine whether entry conditions are met — only presents them
- Decision record stored as prerequisite artefact before PT-05 sprint planning

**Acceptance Criteria**
- §13 compliance review document created for PT-05
- Document confirms display-only scope and human-in-the-loop confirmation
- Strategy Rules owner sign-off recorded in document
- Document referenced in PT-05 sprint story acceptance criteria

---

### BLG-GOV-20 — Trade plan field extension governance
**Priority:** P2 (Medium)
**Type:** Governance Process / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260508-01 — promoted cycle 2026-05-08__scheduled (DL-025)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Before v3.3 sprint planning

**Problem**
The `trade_plans` table was established in PT-01 (v3.1) with an initial field set. Arc 2/3/4 will add fields (entry conditions, quality score, abandonment reason, cost attribution). Without a documented governance process, each addition is ad-hoc — no consistent criteria for whether a field belongs in the trade plan object, no migration strategy requirement, no backwards compatibility rules, and no documented authority for schema changes.

**Scope**
- Document the field addition criteria: what makes a field appropriate for the trade_plans table vs a separate table
- Migration strategy requirement: when must a migration script be provided vs nullable column addition
- Backwards compatibility rules: how existing plans must be handled when new fields are added
- Authority: who must approve a trade_plans schema change (Data Model owner + Product Owner)
- Changelog format: how schema changes are recorded

**Acceptance Criteria**
- Field extension governance document covers: addition criteria, migration strategy, backwards compatibility, authority, changelog format
- Document reviewed and signed off by Data Model owner before v3.3 sprint planning
- Referenced in future sprint planning when PT-03/04/05 field additions are proposed

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
