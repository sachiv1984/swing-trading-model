**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-29

# Backlog Archive — Momentum Trading Assistant

Permanent record of completed and killed backlog items retired from `claude/backlog/backlog.md`. Listed in retirement order, most recent first. Append-only — do not edit existing entries.

---

## v3.8 Completions — Archived 2026-05-21 (Post-Ship Closure)

---

### BLG-FEAT-22 — Ticker Universe Management page

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-21
**Shipped in:** v3.8 (ST-09, cycle: 2026-05-19__release-v3.8, closed 2026-05-20)
**Evidence:** docs/product/changelog.md#v38; claude/cycles/2026-05-19__release-v3.8/verification_report.md

### BLG-FEAT-22 — Ticker Universe Management page
✅ COMPLETE v3.8 — ST-09, cycle: 2026-05-19__release-v3.8, closed 2026-05-20
**Priority:** P2 (Medium)
**Type:** Product Feature / User Configuration
**Owner:** Head of UX & Design; Head of Backend Engineering
**Source:** User request — 2026-05-19
**Effort:** M (~1–2 days)
**Provisional-Target:** v3.8

**Problem**
Users currently have no way to manage the ticker universe that drives both screener and signal generation. The `ticker_universe` table is already used as the single source by both features, but there is no UI to view, add, deactivate, or remove tickers. Additionally, a legacy `public.tickers` table is synced into `ticker_universe` on startup, creating a secondary source-of-truth and confusion about where the canonical universe lives.

**Scope**
- Retire the startup sync from `public.tickers` into `ticker_universe`; make `ticker_universe` the sole authoritative source
- Build a Ticker Universe Management page in the frontend (new route, nav entry)
- Page features: table of all tickers (ticker, market, sector, active status); add ticker form (ticker symbol, market US/UK, optional sector/industry); toggle active/inactive per ticker; delete ticker permanently
- Filter/search by market (US / UK) and active status
- Wire to existing `/ticker-universe` GET, POST, DELETE endpoints (no new backend endpoints required)

**Acceptance Criteria**
- `public.tickers` startup sync removed; `ticker_universe` is populated only via the management UI or seed defaults
- Universe Management page accessible from nav; displays all tickers with market, sector, and active status
- User can add a ticker (US or UK market); added ticker appears immediately in the table
- User can toggle a ticker inactive; inactive tickers are excluded from the next screener/signal run
- User can delete a ticker permanently; it no longer appears in the table
- Filter by market (US/UK/All) and active status works correctly
- Screener and signal generation both continue to use only active tickers from `ticker_universe`

---

### BLG-FEAT-23 — Setup type classification field on trade plans

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-21
**Shipped in:** v3.8 (ST-06, cycle: 2026-05-19__release-v3.8, closed 2026-05-20)
**Evidence:** docs/product/changelog.md#v38; claude/cycles/2026-05-19__release-v3.8/verification_report.md

### BLG-FEAT-23 — Setup type classification field on trade plans
✅ COMPLETE v3.8 — ST-06, cycle: 2026-05-19__release-v3.8, closed 2026-05-20
**Priority:** P2 (Medium)
**Type:** Product Feature / Data Model
**Owner:** Product Owner; Head of UX & Design; Backend Engineering Patterns Owner
**Source:** User session — 2026-05-19
**Effort:** S (~0.5 days)
**Provisional-Target:** v3.8

**Problem**
The trade plan form's setup thesis field is a free-text textarea with no structural anchor. Traders don't know what vocabulary to use, and without a setup type classification the app cannot in future surface behavioural patterns.

**Scope**
- Add a "Setup Type" dropdown to the trade plan form with six options
- Add `setup_type` (VARCHAR, nullable) column to the `trade_plans` table via migration
- Update POST /trade-plans and PUT /trade-plans/{id} to accept and persist `setup_type`

---

### BLG-FEAT-24 — AI-assisted setup thesis generation

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-21
**Shipped in:** v3.8 (ST-08, cycle: 2026-05-19__release-v3.8, closed 2026-05-20)
**Evidence:** docs/product/changelog.md#v38; claude/cycles/2026-05-19__release-v3.8/verification_report.md

### BLG-FEAT-24 — AI-assisted setup thesis generation
✅ COMPLETE v3.8 — ST-08, cycle: 2026-05-19__release-v3.8, closed 2026-05-20
**Priority:** P2 (Medium)
**Type:** Product Feature / UX Enhancement
**Owner:** Product Owner; Head of UX & Design; Backend Engineering Patterns Owner
**Source:** User session — 2026-05-19

---

### BLG-FE-36 — Add news context panel to trade plan form

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-21
**Shipped in:** v3.8 (ST-07, cycle: 2026-05-19__release-v3.8, closed 2026-05-20)
**Evidence:** docs/product/changelog.md#v38; claude/cycles/2026-05-19__release-v3.8/verification_report.md

### BLG-FE-36 — Add news context panel to trade plan form
✅ COMPLETE v3.8 — ST-07, cycle: 2026-05-19__release-v3.8, closed 2026-05-20
**Priority:** P2 (Medium)
**Type:** Frontend / UX
**Owner:** Head of UX & Design; Backend Engineering Patterns Owner
**Source:** User session — 2026-05-19

---

### BLG-GOV-24 — Add gh_issue_template.md to §14 governance table

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-21
**Shipped in:** v3.8 (ST-10, cycle: 2026-05-19__release-v3.8, closed 2026-05-20)
**Evidence:** docs/product/changelog.md#v38; claude/cycles/2026-05-19__release-v3.8/verification_report.md

### BLG-GOV-24 — Add gh_issue_template.md to §14 governance table
✅ COMPLETE v3.8 — ST-10, cycle: 2026-05-19__release-v3.8, closed 2026-05-20
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Governance-drift check during preflight consolidation branch gov/2026-05-17__preflight-consolidation — 2026-05-17

---

## v3.7 Completions — Archived 2026-05-19 (Post-Ship Closure)

*BLG-FE-33 (Signals page Add to Watchlist CTA — watchlisted status backend + SignalCard CTA replacement) — ✅ COMPLETE v3.7 — ST-01 + ST-02, cycle: 2026-05-18__release-v3.7*

*BLG-FE-34 (Trade plan form signal context panel — SignalContextPanel.js with entry_rationale/confirmation pre-population) — ✅ COMPLETE v3.7 — ST-03, cycle: 2026-05-18__release-v3.7*

*BLG-QA-20 (Consolidate database stub files into shared pytest conftest fixture — session-scoped stub) — ✅ COMPLETE v3.7 — ST-09, cycle: 2026-05-18__release-v3.7*

*BLG-OPS-16 (Remove tracked backend/__pycache__ files from git + .gitignore) — ✅ COMPLETE v3.7 — ST-10, cycle: 2026-05-18__release-v3.7*

*BLG-GOV-23 (scored_initiatives.md Arc 3–6 comprehensive refresh — OA-RP-05 resolved) — ✅ COMPLETE v3.7 — ST-11, cycle: 2026-05-18__release-v3.7*

---

*BLG-GOV-22 (sprint_planning_prompt.md patch: shared execution_state.json ownership + multi-EPIC Positions.js conflict guidance) — ✅ COMPLETE v3.5 (ST-11, 2026-05-15) — archived 2026-05-15*

*BLG-GOV-21 (Arc 4 data requirements capture) — ✅ COMPLETE v3.5 (ST-04, 2026-05-15; arc4_data_requirements.md v1.0 signed off) — archived 2026-05-15*

*BLG-QA-19 (Research view regression test protocol) — ✅ COMPLETE v3.5 (ST-10, 2026-05-15; research_view_regression_protocol.md v1.0, QA Lead sign-off) — archived 2026-05-15*

*BLG-SPEC-31 (Review React Query v5 onSuccess migration impact across codebase) — ✅ COMPLETE v3.5 (ST-09, 2026-05-15; 1 fix TradePlan.js; SC-TP-08 Playwright 9/9 pass) — archived 2026-05-15*

*BLG-SPEC-30 (Correct stop-management-workflow ux_spec.md §4.4 stop-update HTTP verb to PATCH) — ✅ COMPLETE v3.5 (ST-08, 2026-05-15; ux_spec.md v1.1) — archived 2026-05-15*

*BLG-SPEC-29 (Correct grace-period-alert ux_spec.md §5 dismiss storage to sessionStorage) — ✅ COMPLETE v3.5 (ST-07, 2026-05-15; ux_spec.md v1.1) — archived 2026-05-15*

---

## v3.4 Completions — Archived 2026-05-14 (GROOM-20260514-01)

### BLG-FEAT-21 — Trade plan abandonment status field

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-14
**Shipped in:** v3.3 backend (ST-17, EPIC-04) + v3.4 frontend (ST-10, EPIC-03, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

`Abandoned` status added to trade plan lifecycle with required `abandonment_reason` field. Status transition guard enforced: Active-position-linked plans cannot be abandoned. Abandoned plans surface in plan history alongside Closed plans. Backend guard on PUT/PATCH endpoint delivered v3.3 (ST-17); frontend abandonment action and reason input in TradePlan.js delivered v3.4 (ST-10).

---

### BLG-FE-31 — Research view component library

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-11, EPIC-04, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

Catalogue of PT-02 research view UI components (price card, regime/signal panel, news feed, source attribution row, freshness indicator). Each entry: component name, file path, key props, variants. Reuse candidates for Arc 3 frontend (IT-01/02/03 stories) explicitly noted. Delivered before v3.4 sprint planning as scoped.

---

### BLG-FE-22 — Screener morning routine UX spec

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-12, EPIC-04, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

Workflow spec for Arc 1→Arc 2 morning routine: screener results → shortlist → watchlist promotion → pre-trade research navigation. Information-carry decisions documented (context visible in research view from screener). Navigation model specified across three surfaces.

---

### BLG-FE-23 — Research page UK ticker suffix not stripped

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-07, EPIC-03, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

`stripUkSuffix` utility applied to Research.js page title/header. UK tickers (e.g. MTLN.L) display as MTLN in Research page heading. Consistent with screener and watchlist treatment. No regression to other suffix-stripping surfaces. Origin: v3.2 delivery verification DEV-E01-03.

---

### BLG-FE-24 — Negative earnings days display for past earnings dates

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-07, EPIC-03, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

Negative `days_until_earnings` (past earnings date) now displays `—` across all earnings columns (screener, watchlist, positions). Zero displays `Today`. Positive values unchanged. Earnings proximity warning (≤5 days amber) unaffected.

---

### BLG-FE-25 — Signals page: default to most recent day's signals

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-08, EPIC-03, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

Signals page defaults to most recent trading day's signals on load. Date picker/toggle control added for viewing historical signals. Morning-routine use case (review current day's signals) now supported directly on load. Signal data accuracy unaffected.

---

### BLG-FE-29 — Watchlist research status indicator

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-09, EPIC-03, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

Binary research status indicator added to watchlist ticker rows. Done = research record exists; Not Done = no record. Icon/badge display — no text, minimal column width. Scope constraint honoured: no research quality score or freshness judgement.

---

### BLG-FE-30 — Trade plan status badges

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-10, EPIC-03, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

Colour-coded status badges for all trade plan statuses: Draft (grey), Research Pending (amber), Research Complete (blue), Entry Conditions Set (purple), Active (green), Closed (muted), Abandoned (red). Applied in trade plan list and detail views. Colours aligned with design system tokens. Coordinate-delivered with BLG-FEAT-21 Abandoned status.

---

### BLG-AI-03 — AI Journal Summarisation quarterly review cadence

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-13, EPIC-04, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

Quarterly review process defined for AI Journal Summarisation (AI-SUM). Review checklist: output quality sample review, §13 compliance re-confirmation, BLG-AI-02 model version record update, error rate review from BLG-OPS-14 monitoring. Process documented in governance file; OPERATIONAL_GUIDE updated. First review: Q3 2026.

---

### BLG-QA-18 — Screener accuracy test protocol

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-14, EPIC-04, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

Formal QA protocol for validating screener output accuracy against §11 strategy rules. Test cases: regime gate pass/fail, ATR threshold boundary, signal score threshold cases. References `strategy_rules.md §11` as authoritative parameter source. Built on BLG-QA-08 mock harness and BLG-QA-10 screener test coverage. Owner: Director of Quality.

---

### BLG-SPEC-28 — trade_plan.md §6.2 entry checklist field reference update

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-13, EPIC-04, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

`trade_plan.md §6.2` pre-population rules corrected: `stop_defined` pre-checked when `early_exit_conditions` present (not `stop_level`); `research_reviewed` pre-checked when `r_target` set (not `risk_reward_notes`). Spec now aligned to TradePlan.js implementation. No implementation change required — implementation was correct. Origin: ST-11 (EPIC-03, v3.3) P3 deviation.

---

### TEST-GAP-EPIC-01-v33 — Position lifecycle badge Playwright E2E scenarios

**Status at retirement:** ✅ Resolved
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-01, EPIC-01, cycle 2026-05-14__release-v3.4)
**Evidence:** `claude/cycles/2026-05-14__release-v3.4/verification_report.md`; SC-LS-01–04 passing in CI

SC-LS-01–04 authored and passing: lifecycle badge visible for all states (GRACE/PROFITABLE/LOSING/EXIT ZONE/UNKNOWN), feature flag OFF suppresses badge, days_in_state display confirmed, exit zone purple colouring verified. TSG-v33-01 resolved — marked in `docs/specs/Specs_Index.md` 2026-05-14.

---

### TEST-GAP-EPIC-02-v33 — Grace period alert and trail stop Playwright E2E scenarios

**Status at retirement:** ✅ Resolved
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-02 + ST-03, EPIC-01, cycle 2026-05-14__release-v3.4)
**Evidence:** `claude/cycles/2026-05-14__release-v3.4/verification_report.md`; SC-GP-01–03 and SC-TS-01–03 passing in CI

SC-GP-01–03: alert card renders for GRACE ≥ day 8, displays ticker/days/plan context, sessionStorage dismiss confirmed. SC-TS-01–03: Trail Stop button for PROFITABLE/EXIT ZONE positions, panel shows current/ATR stop/difference/R-terms, user-confirm required (§13 compliant). TSG-v33-02 resolved — marked in `docs/specs/Specs_Index.md` 2026-05-14.

---

## v3.3 Completions — Archived 2026-05-13 (GROOM-20260513-01)

### BLG-FEAT-13 — Add gated feature rollout capability

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-16, EPIC-04, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/product/changelog.md` v3.3 entry; `claude/cycles/2026-05-09__release-v3.3/verification_report.md`

Feature flag infrastructure: `is_flag_enabled()` utility, `FEATURE_FLAGS` env var, `feature_flags.json` config, startup audit logging. `arc3_lifecycle_display` flag as proof-of-concept. Pattern documented in `docs/specs/platform/feature_flags.md`. Mandatory delivery after 3 consecutive deferrals (v3.0–v3.2).

---

### BLG-SPEC-24 — PT-02 research view canonical spec

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-09, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/product/changelog.md` v3.3 entry; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-03.md`

Class 2 canonical spec for PT-02 research view delivered at `docs/specs/frontend/pages/research_view.md`. Covers data fields, sources, freshness policy, §13 compliance, display rules. References BLG-SPEC-25, BLG-SPEC-26, BLG-FE-28.

---

### BLG-SPEC-25 — PT-02 research endpoint API contract

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-08, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/product/changelog.md` v3.3 entry; `docs/specs/api_contracts/research_endpoint.md`

Formal Class 2 API contract for `GET /research/{ticker}` at `docs/specs/api_contracts/research_endpoint.md`. Covers request parameters, response schema, source attribution, error codes (known deviation DEV-v33-02: 200+null vs 404/503/429; filed as BLG-SPEC-27), rate limit policy.

---

### BLG-SPEC-26 — Research view data source provenance spec

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-08, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/product/changelog.md` v3.3 entry; `docs/specs/data_provenance/research_view_provenance.md`

Provenance attribution spec for research view data fields. Per-field source (Yahoo Finance, Alpaca, internal), retrieval timestamp requirements, display format. Filed as prerequisite for BLG-SPEC-24 and BLG-FE-28.

---

### BLG-FE-28 — Pre-Trade Research View UX spec

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-09, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/product/changelog.md` v3.3 entry; `docs/design/2026-05-09__release-v3.3/research-view/ux_spec.md`

UX spec for PT-02 research view covering layout, data field placement, source attribution display, news feed design, freshness indicator, empty/error states. References design system tokens. Delivered before v3.3 sprint planning as required.

---

### BLG-QA-14 — Author Playwright E2E test suite for entry checklist

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-11, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `tests/e2e/entry-checklist.spec.js`; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-03.md`

`tests/e2e/entry-checklist.spec.js` authored covering SC-CL-01 to SC-CL-07. Note: DEV-v33-03 (P3) — tests cover actual field names (early_exit_conditions/r_target) not spec names (stop_level/risk_reward_notes); deviation documented. Resolves TSG-v32-01.

---

### BLG-QA-15 — PT-02 research view acceptance test protocol

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-10, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/qa/acceptance_protocols/research_view_protocol.md`; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-03.md`

Acceptance test protocol for PT-02 research view at `docs/qa/acceptance_protocols/research_view_protocol.md`. Covers observable ACs, Playwright vs human staging split, freshness threshold, error state criteria. Includes SC-RV-01–19 references. Note: SC-RV-18/19 explicit scenarios deferred (TEST-GAP-EPIC-03-v33 filed).

---

### BLG-QA-16 — Research endpoint integration test coverage

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-12, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `backend/routers/test.py`; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-03.md`

`GET /research/{ticker}` added to `backend/routers/test.py` with AAPL as representative test value. Covers success, partial source failure, full failure scenarios. Source attribution fields verified. SystemStatus.js endpoint count updated.

---

### BLG-QA-17 — Research view test scenario library

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-10, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/qa/test_scenarios/research_view_scenarios.md`; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-03.md`

Test scenario library for PT-02 research view: 19 scenarios SC-RV-01–19 covering data field rendering, source attribution, news feed, freshness indicator, error states. Library reviewed by DoQ. Referenced in BLG-QA-15 acceptance test protocol.

---

### BLG-OPS-15 — Research endpoint latency monitoring

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-12, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/ops/api_performance_baseline.md#section-11`; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-03.md`

Research endpoint latency baseline documented: `docs/ops/api_performance_baseline.md` §11. p50 2500–4000ms, p95 ≤3000ms target (multi-source external API aggregation). Latency target documented with rationale.

---

### BLG-SEC-06 — Trade plan data sensitivity classification

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-12, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/specs/security/trade_plan_data_sensitivity.md`; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-03.md`

Classification document at `docs/specs/security/trade_plan_data_sensitivity.md`. Three sensitivity levels: Public (ticker), Internal (dates, status), Private (entry zone, stop, R-target, thesis, checklist). Access control principles per level. Cybersecurity sign-off recorded.

---

### BLG-GOV-19 — PT-05 entry checklist §13 compliance review

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-15, EPIC-04, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/specs/compliance/pt05_entry_checklist_s13_review.md`; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-04.md`

Formal §13 boundary review for PT-05. Confirmed display-only, human-in-the-loop. Strategy Rules & System Intent Owner sign-off recorded. `trade_plan.md` updated to reference compliance review.

---

### BLG-GOV-20 — Trade plan field extension governance

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-12, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/governance/trade_plan_field_extension_policy.md`; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-03.md`

Field extension governance policy at `docs/governance/trade_plan_field_extension_policy.md`. Covers field addition criteria, migration strategy, backwards compatibility, authority (Data Model owner + Product Owner), changelog format. Data Model owner sign-off recorded.

---

### BLG-FEAT-19 — Monthly P&L summary report

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-05
**Shipped in:** v3.1 (ST-08, EPIC-03, cycle 2026-04-29__release-v3.1)
**Evidence:** `docs/product/changelog.md` v3.1 entry; `claude/cycles/2026-04-29__release-v3.1/verification_report.md`

Month-by-month breakdown of realised P&L. New `GET /reports/monthly-pnl` endpoint added. Consistent with existing annual tax-year P&L calculation. No regression to annual report confirmed in verification.

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

### BLG-FEAT-18 — Consecutive losing streak metric

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-04-28
**Shipped in:** v3.0 (ST-15, cycle 2026-04-25__release-v3.0)
**Evidence:** `docs/product/changelog.md` v3.0 entry; `claude/cycles/2026-04-25__release-v3.0/verification_report.md`

Consecutive losing streak count added to analytics. `advanced_metrics.loss_streak` computed from closed trades. `metrics_definitions.md` updated v1.10.0. 7 unit tests in test_streak_metric.py.

---

### BLG-FE-19 — Keyboard shortcuts for trading actions

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-28
**Shipped in:** v3.0 (ST-11, cross-EPIC EPIC-02 branch, cycle 2026-04-25__release-v3.0)
**Evidence:** `docs/product/changelog.md` v3.0 entry; `claude/cycles/2026-04-25__release-v3.0/verification_report.md`

Keyboard shortcuts 'n', 'w', 'r' implemented in Layout.js via useEffect/keydown handler. Suppression rule for text inputs. Sidebar footer hint. Deviation documented: committed on EPIC-02 branch (co-delivered with Screener nav).

---

### BLG-FE-18 — Screener results page: attach news panel on DS-02 implementation

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-28
**Shipped in:** v3.0 (ST-07, cycle 2026-04-25__release-v3.0); resolves DEV-01 P3 from v2.9
**Evidence:** `docs/product/changelog.md` v3.0 entry; `claude/cycles/2026-04-25__release-v3.0/verification_report.md`

News panel attached to screener results page per screener_results.md §9. GET /news/{ticker} wired. Display-only per BLG-GOV-16 §13. UK tickers show '—' in news column. Strategy Rules Owner counter-sign applied.

---

### BLG-AI-02 — Model version contract for AI Journal

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-28
**Shipped in:** v3.0 (ST-16, cycle 2026-04-25__release-v3.0)
**Evidence:** `docs/product/changelog.md` v3.0 entry; `claude/cycles/2026-04-25__release-v3.0/verification_report.md`

Class 2 canonical spec created at docs/specs/ai_journal_model_contract.md. Model: claude-haiku-4-5-20251001 in ai_service.py _DEFAULT_MODEL. Contract referenced in ai_audit_service.py docstring.

---

### TEST-GAP-ST14 — AI audit service unit tests (ai_audit_service.py)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-28
**Shipped in:** v3.0 (ST-10, cycle 2026-04-25__release-v3.0)
**Evidence:** `docs/product/changelog.md` v3.0 entry; `claude/cycles/2026-04-25__release-v3.0/verification_report.md`

12 unit tests created in tests/test_ai_audit_service.py covering ensure_ai_audit_table, log_ai_summary_run, query_audit_log. Mock pattern — no live DB required. All pass in CI.

---

### BLG-OPS-14 — AI Journal monitoring metrics

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-28
**Shipped in:** v3.0 (ST-09, cycle 2026-04-25__release-v3.0)
**Evidence:** `docs/product/changelog.md` v3.0 entry; `claude/cycles/2026-04-25__release-v3.0/verification_report.md`

GET /health extended with ai_journal section: usage_rate, error_rate, p95_latency_ms sourced from ai_audit_log. Non-blocking — returns null/unavailable if data absent. 5 unit tests.

---

### BLG-OPS-12 — External API health check extension

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-04-28
**Shipped in:** v3.0 (ST-08, cycle 2026-04-25__release-v3.0)
**Evidence:** `docs/product/changelog.md` v3.0 entry; `claude/cycles/2026-04-25__release-v3.0/verification_report.md`

GET /health extended with external_apis section covering Alpaca and Yahoo Finance: last_successful_call, error_rate, p95_latency. Cache-based health check. 8 unit tests in test_health_extensions.py.

---

### BLG-FE-14 — Market Correlation frontend view

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-20
**Shipped in:** v2.8 (2026-04-17__release-v2.8 EPIC-01 ST-01)
**Evidence:** `docs/product/changelog.md` v2.8 entry; `claude/cycles/2026-04-17__release-v2.8/verification_report.md`

**Problem** `GET /analytics/market-correlation` was delivered in v2.7 (ST-08). AC-6 of ST-08 required a frontend view; deferred to v2.8. Completed as EPIC-01 ST-01 in v2.8.

**Acceptance Criteria met:** Per-position correlation and severity rendered with colour-coding; portfolio-level weighted average displayed; null values render gracefully; no regression to Analytics page.

---

### BLG-QA-13 — Test scenario coverage gap: market correlation and supplementary indicators (v2.7)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-20
**Shipped in:** v2.8 (2026-04-17__release-v2.8 EPIC-02 ST-02, ST-03)
**Evidence:** `docs/product/changelog.md` v2.8 entry; `claude/cycles/2026-04-17__release-v2.8/verification_report.md`

**Shipped:** SC-CORR-01 through SC-CORR-04 added to `docs/testing/analytics_scenarios.md`; SC-SIG-IND-01 through SC-SIG-IND-02 added to `docs/testing/signals_scenarios.md`. Test coverage gap closed. Playwright test suite consolidated (24/24 green).

---

### BLG-FEAT-16 — AI Journal Summarisation

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-20
**Shipped in:** v2.8 (2026-04-17__release-v2.8 EPIC-04 ST-07, ST-08)
**Evidence:** `docs/product/changelog.md` v2.8 entry; `claude/cycles/2026-04-17__release-v2.8/verification_report.md`

**§13 Status:** CONDITIONALLY COMPLIANT — SRB-v1.7. All 4 mandatory conditions met. Strategy Rules owner sign-off confirmed at EPIC-04 merge 2026-04-20.

**Shipped:** POST /api/ai/journal-summary and GET /api/ai/journal-summary/history delivered. AI summary displayed as UX convenience view with disclaimer label. No signal pipeline integration. External LLM API key managed via environment variable.

---

### BLG-GOV-13 — Deduplicate backlog_archive.md duplicate item headers

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-20
**Shipped in:** v2.8 (2026-04-17__release-v2.8 EPIC-03 ST-06)
**Evidence:** `docs/product/changelog.md` v2.8 entry; `claude/cycles/2026-04-17__release-v2.8/verification_report.md`

**Shipped:** backlog_archive.md deduplicated; duplicate `###` item headers resolved; Product Owner confirmation obtained; ID uniqueness scan PASS post-deduplication.

---

### v2.5 Release Slice — 2026-04-05__release-v2.5

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-04-10
**Shipped in:** v2.5 — Integration Baseline, Quick Wins & Governance Debt
**Evidence:** 13/13 items shipped; 12 backlog items completed; `claude/cycles/2026-04-05__release-v2.5/closure_record.md`

| ID | Title | Type | Sprint | Evidence |
|----|-------|------|--------|----------|
| BLG-OPS-12 | Fix auth forwarding in POST /test/endpoints | Ops | Sprint 1 | ST-01 commit 230643b |
| BLG-OPS-13 | Keep endpoint test list in sync with openapi.yaml | Ops | Sprint 1 | ST-02 commit a6a74c0 |
| BLG-FE-07 | Fix System Status endpoint categorisation | Frontend | Sprint 1 | ST-03 commit a6a74c0 |
| BLG-BE-08 | Review and document Reports page backend integration | Backend | Sprint 2 | ST-04 commit 3a645e3 |
| BLG-BE-09 | Review and document Signals page backend integration | Backend | Sprint 2 | ST-05 commit 3a645e3 |
| BLG-BE-07 | Investigate high external baseline latency | Backend | Sprint 2 | ST-06 commit 3f31b1d |
| BLG-OPS-11 | Add --max-time to GitHub Actions curl calls | Ops | Sprint 2 | ST-07 commit ce3775a |
| BLG-FE-08 | Fix Avg Slippage StatsCard gradient rendering | Frontend | Sprint 2 | ST-08 commit ce3775a |
| BLG-FEAT-15 | Fee drag metric on Trade History | Feature | Sprint 2 | ST-09 commit ce3775a |
| BLG-GOV-10 | Fix governance_sync.yml batch push issue closure | Gov | Sprint 1 | ST-10 commit 01f5e9c |
| BLG-GOV-12 | Formalise backlog entry placement standard | Gov | Sprint 1 | ST-11 commit dbb4551 |
| TEST-GAP-EPIC-01-v24 | Create test scenarios for EPIC-01 correctness fixes | QA | Sprint 1 | ST-13 commit aacbb50 |

---

### BLG-OPS-12 — Fix auth forwarding in POST /test/endpoints internal calls
**Priority:** P2 (High)
**Type:** Operational / Infrastructure
**Owner:** Head of Engineering + Infrastructure & Operations Owner
**Source:** ST-11 performance baseline review — 2026-04-03
**Effort:** XS (<1h)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-01) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
`backend/services/health_service.py` `test_all_endpoints()` makes internal HTTP calls to each endpoint without forwarding the `X-API-Key` header. All auth-protected endpoints return 401 and are reported as "fail". The System Status page "Run Tests" button currently shows 1/17 pass rate, making the system appear critically broken when all endpoints are in fact operational. This makes the monitoring tool unreliable and misleading.

**Scope**
- Modify `test_all_endpoints()` to accept and forward the API key in internal calls (e.g. accept `api_key: str = None` parameter, add `X-API-Key` header when provided)
- Update `POST /test/endpoints` route in `main.py` to extract the `X-API-Key` from the incoming request and pass it through
- Alternatively: add a middleware bypass for server-internal calls (e.g. `X-Internal: true` header checked before auth)

**Acceptance Criteria**
- `POST /test/endpoints` returns pass/fail based on actual endpoint response, not auth rejection
- All correctly implemented endpoints report "pass" when the system is healthy
- Success rate shown on System Status page reflects actual endpoint health

---

### BLG-OPS-13 — Keep endpoint test list in sync with openapi.yaml
**Priority:** P3 (Low)
**Type:** Operational / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** ST-11 performance baseline review — 2026-04-03
**Effort:** XS (<1h)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-02) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
The endpoint test list in `backend/services/health_service.py` `test_all_endpoints()` was last updated for v2.2 (12 endpoints). Endpoints added in v2.3/v2.4 are not being tested. This coverage gap will worsen each sprint if not addressed structurally.

**Scope**
- Add all missing parameterless GET endpoints to the test list in `test_all_endpoints()`
- Add a comment block above the list referencing `docs/reference/openapi.yaml` as the source of truth
- Update the System Status page placeholder text to match actual endpoint count

**Acceptance Criteria**
- All parameterless GET endpoints in `openapi.yaml` are present in the test list
- A comment in `health_service.py` documents the sync obligation
- System Status page "Run Tests" button tests the complete current endpoint set

---

### BLG-FE-07 — Fix System Status endpoint categorisation for v2.3/v2.4 routes
**Priority:** P4 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Engineer
**Source:** System Status page review — 2026-04-03
**Effort:** XS (<1h)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-03) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
`src/pages/SystemStatus.js` `categorizeEndpoint()` does not cover routes added in v2.3/v2.4. Endpoints matching `/alerts`, `/notifications`, and `/digest` fall through to "Other" category.

**Scope**
- Add categorisation rules for Alerts, Notifications, Digest, verify Health/Analytics/Validation
- Add `categoryConfig` entries for "Alerts" and "Notifications"

**Acceptance Criteria**
- Alert endpoints appear under "Alerts" category
- Notification endpoints appear under "Notifications" category
- Digest endpoints appear under "Digest" category
- No endpoints fall into "Other" except `/`

---

### BLG-BE-08 — Review and document Reports page backend integration
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Frontend Integration
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Source:** User session review — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-04) — 2026-04-10 — cycle 2026-04-05__release-v2.5 — see `docs/ops/reports_integration_review.md`

**Problem**
The Reports page is not fully integrated with the backend. No documentation mapping which Reports components are wired to which backend endpoints.

**Acceptance Criteria**
- A review document exists mapping each Reports page section to its backend endpoint
- All identified gaps have follow-up backlog items or are addressed
- Improvement proposals recorded for roadmap input

---

### BLG-BE-09 — Review and document Signals page backend integration
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Frontend Integration
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Source:** User session review — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-05) — 2026-04-10 — cycle 2026-04-05__release-v2.5 — see `docs/ops/signals_integration_review.md`

**Problem**
The Signals page integration state is undocumented. Some sections may render without live data.

**Acceptance Criteria**
- A review document exists mapping each Signals page section to its backend endpoint
- All identified gaps have follow-up backlog items
- Improvement proposals recorded for roadmap input

---

### BLG-BE-07 — Investigate high external baseline latency on DB-backed endpoints
**Priority:** P2 (High)
**Type:** Backend / Infrastructure
**Owner:** Head of Engineering
**Source:** ST-11 performance baseline — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.5
**Status:** Closed — investigation complete (ST-06, v2.5). See `docs/ops/api_performance_baseline.md` §6. Follow-up items: BLG-OPS-14 (Supavisor), BLG-BE-07-FIX (portfolio connection refactor).

**Problem**
All DB-backed endpoints have p50 response times of 1.2–6.0 seconds. Root cause: Supabase free tier connection overhead. GET /portfolio and GET /notifications/preferences were outliers.

**Acceptance Criteria**
- Root cause identified and documented
- Fix applied or architectural constraint documented
- Updated baseline document filed

---

### BLG-OPS-11 — Add `--max-time` to GitHub Actions cron curl calls
**Priority:** P3 (Low)
**Type:** Operational / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** InfraOps review of ST-10 Render tier decision record — 2026-04-02
**Effort:** XS (<1h)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-07) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
`alert-evaluation.yml` and `daily-snapshot.yml` invoke `curl` with no `--max-time` flag. Cold starts cause silent stall periods on Render free tier.

**Scope**
- Add `--max-time 120` to every `curl` call in both workflow files

**Acceptance Criteria**
- Both workflow files have `--max-time 120` on all curl invocations
- If service fails to respond within 120s workflow step fails with non-zero exit code

---

### BLG-FE-08 — Fix Avg Slippage StatsCard gradient rendering
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Owner
**Source:** DEV-ST14-01 — delivery verification 2026-03-31__release-v2.4 — 2026-04-03
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.5
**Deviation ref:** DEV-ST14-01 (P3 cosmetic — pre-accepted by Director of Quality 2026-03-20)
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-08) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
Avg Slippage StatsCard renders without gradient background. DEV-ST14-01 cosmetic deviation.

**Acceptance Criteria**
- Avg Slippage StatsCard renders with gradient background matching other StatsCards
- No regression to slippage value display or colour coding

---

### BLG-FEAT-15 — Fee drag metric on Trade History
**Priority:** P3 (Low)
**Type:** Feature — Analytics
**Owner:** Metrics Definitions & Analytics Owner + Head of Engineering
**Source:** PO/Challenger debate 2026-04-02 — action A3 from slippage metric re-scope decision
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-09) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
No always-available metric capturing friction cost of executing a trade. Fee drag = exit_fees / gross_proceeds × 100.

**Acceptance Criteria**
- `fee_drag_pct` field returned per trade; `avg_fee_drag_pct` at response envelope
- "Avg Fee Drag" StatsCard visible on Trade History
- Fee Drag % column present in TradeHistoryTable
- `docs/specs/metrics_definitions.md` contains canonical definition

---

### BLG-GOV-10 — Fix governance_sync.yml batch push issue closure
**Priority:** P2 (Medium)
**Type:** Governance Process / DevOps
**Owner:** DevOps
**Source:** EPIC-06 merge observation — delivery verification 2026-03-31__release-v2.4 — 2026-04-03
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-10) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
`governance_sync.yml` uses `git log -1` — only closes the last commit's GitHub issue in a batch push.

**Scope**
- Update to `git log $BEFORE..$AFTER` to close all issues in push range

**Acceptance Criteria**
- Multi-commit batch push closes all referenced GitHub issues
- Single-commit push behaviour unchanged

---

### BLG-GOV-12 — Formalise backlog entry placement standard
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** User session review — 2026-04-03
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-11) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
New backlog items were added to session sections instead of type-based sections. Fragments backlog structure.

**Acceptance Criteria**
- `lessons_learnt.md` has backlog-add placement rule entry
- Placement rule visible at top of `backlog.md`

---

### TEST-GAP-EPIC-01-v24 — Create test scenarios for EPIC-01 backend correctness fixes
**Priority:** P2 (Medium)
**Type:** QA Coverage
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-03-31__release-v2.4 — TSG-v24-01 — 2026-04-03
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-13) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
EPIC-01 v2.4 shipped three correctness-critical fixes with no automated test scenarios.

**Scope**
- Author SC-ATR-01, SC-DEDUP-01/02, SC-STOP-01 in `docs/testing/`

**Acceptance Criteria**
- Scenario files present covering all four scenarios
- Each scenario executable against staging or unit test suite
- Referenced in test scenario index

---

### v2.4 Release Slice — 2026-03-31__release-v2.4

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-04-03
**Shipped in:** v2.4 — Correctness, Insight & Governance Hardening
**Evidence:** 17/17 items shipped; 13 backlog items completed; `claude/cycles/2026-03-31__release-v2.4/closure_record.md`

| ID | Title | Type | Sprint | Evidence |
|----|-------|------|--------|----------|
| BLG-BE-05 | Fix ATR pence→GBP conversion for all UK (.L) tickers | Backend Bug Fix | Sprint 2 (ST-01) | changelog.md v2.4; verification_report.md |
| BLG-BE-06 | Alert evaluation idempotency (notification deduplication) | Backend Engineering | Sprint 2 (ST-02) | changelog.md v2.4; verification_report.md |
| BLG-BE-04 | R-Multiple Analysis: stop price unavailable from trade_history | Backend / Data | Sprint 2 (ST-03) | changelog.md v2.4; verification_report.md |
| BLG-FE-06 | Fix missing P&L (GBP) column on Positions page | Frontend / UX | Sprint 2 (ST-04) | changelog.md v2.4; verification_report.md |
| BLG-FE-03 | User-facing error message mapping layer | Frontend / UX | Sprint 2 (ST-05) | changelog.md v2.4; verification_report.md |
| BLG-SPEC-D15 | Reconcile data_model.md portfolios table with actual deployed schema | Spec Debt | Sprint 1 (ST-06) | changelog.md v2.4; verification_report.md |
| BLG-SPEC-D16 | Reconcile data_model.md trade_history table with database.py column names | Spec Debt | Sprint 1 (ST-07) | changelog.md v2.4; verification_report.md |
| BLG-FEAT-14 | Weekly trading review digest | Product Feature | Sprint 3 (ST-08+ST-09) | changelog.md v2.4; verification_report.md |
| BLG-OPS-10 | Render hosting tier review | Operational / Infrastructure | Sprint 1 (ST-10) | changelog.md v2.4; verification_report.md |
| BLG-OPS-05 | API endpoint performance baseline | Operational / Observability | Sprint 2 (ST-11) | changelog.md v2.4; verification_report.md |
| TEST-GAP-EPIC-05-SLIP | Create slippage tracking test scenarios | QA Coverage | Sprint 1 (ST-12) | changelog.md v2.4; verification_report.md |
| BLG-GOV-09 | Cycle velocity metric | Governance Process | Sprint 1 (ST-13) | changelog.md v2.4; verification_report.md |
| BLG-GOV-03 | Simplify cycle artefact sealing (remove SHA-256, retain sealed flag) | Governance Process | Sprint 1 (ST-17) | changelog.md v2.4; verification_report.md |

---

### v2.3 Release Slice — 2026-03-24__release-v2.3

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-30
**Shipped in:** v2.3 — Quality Automation & User Insight
**Evidence:** 15 of 16 items shipped (ST-17 BLG-GOV-08 returned to backlog); `claude/cycles/2026-03-24__release-v2.3/closure_record.md`

<!-- release-plan-marker: RP:v2.3:2026-03-24__release-v2.3 -->

**Cycle:** 2026-03-24__release-v2.3
**Release:** v2.3 — Quality Automation & User Insight
**Planned:** 2026-03-24
**Shipped:** 2026-03-30
**Verification:** Verified_with_deviations
**Backlog slice:** `claude/cycles/2026-03-24__release-v2.3/stage4_backlog_slice.md`

Items in v2.3 sprint: EPIC-01 (ST-01 BLG-FEAT-11, ST-02 BLG-FEAT-09), EPIC-02 (ST-03 BLG-OPS-08, ST-04 BLG-QA-06, ST-05 BLG-QA-05, ST-06 BLG-QA-01), EPIC-03 (ST-07 BLG-SPEC-D14, ST-08 BLG-OPS-09, ST-09 BLG-OPS-07), EPIC-04 (ST-10 BLG-FE-05, ST-11 BLG-FE-04, ST-12 BLG-FE-02, ST-13 BLG-UX-01), EPIC-05 (ST-14 BLG-GOV-07, ST-15 BLG-QA-03, ST-16 BLG-QA-04, ST-17 BLG-GOV-08 [returned to backlog])

**Accepted deviations:** DEV-EPIC02-ST05-03 (P2, BLG-FE-06); V-CHART-05a/b/c (P2 staging gap, BLG-BE-04)

---

### v2.2 Release Slice — 2026-03-21__release-v2.2

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-24
**Shipped in:** v2.2 — Security, Alert Maturity & Quality
**Evidence:** All 15 items shipped; `claude/cycles/2026-03-21__release-v2.2/closure_record.md`

<!-- release-plan-marker: RP:v2.2:2026-03-21__release-v2.2 -->

**Cycle:** 2026-03-21__release-v2.2
**Release:** v2.2 — Security, Alert Maturity & Quality
**Planned:** 2026-03-21
**Shipped:** 2026-03-24
**Verification:** Verified_with_deviations
**Backlog slice:** `claude/cycles/2026-03-21__release-v2.2/stage4_backlog_slice.md`

Items in v2.2 sprint: EPIC-01 (ST-01 BLG-SEC-01, ST-02 BLG-SEC-02), EPIC-02 (ST-03 BLG-OPS-04, ST-04 BLG-FEAT-10, ST-05 BLG-FEAT-12), EPIC-03 (ST-06 BLG-BE-03, ST-07 BLG-FE-01, ST-08 BLG-OPS-06), EPIC-04 (ST-09 TEST-GAP-EPIC-02, ST-10 TEST-GAP-EPIC-03, ST-11 BLG-QA-02, ST-12 BLG-SPEC-T01), EPIC-05 (ST-13 BLG-GOV-04, ST-14 BLG-GOV-05, ST-15 BLG-GOV-06)

Full item definitions: in `claude/cycles/2026-03-21__release-v2.2/stage4_backlog_slice.md` and in `backlog.md` body (tombstoned in place per groom backlog 2026-03-24).

---

### v1.10 Release Slice — 2026-03-15__release-v1.10

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-16
**Shipped in:** v1.10 — Operations & Quality Foundation
**Evidence:** All EPICs shipped 2026-03-16; `claude/cycles/2026-03-15__release-v1.10/closure_record.md`

<!-- release-plan-marker: RP:v1.10:2026-03-15__release-v1.10 -->

**Cycle:** 2026-03-15__release-v1.10
**Release:** v1.10 — Operations & Quality Foundation
**Planned:** 2026-03-15
**Backlog slice:** `claude/cycles/2026-03-15__release-v1.10/stage4_backlog_slice.md`

Items in v1.10 sprint: EPIC-01 (ST-01–ST-03), EPIC-02 (ST-04), EPIC-03 (ST-05–ST-07)

---

### BLG-OPS-01 — Provision development environment
**Status:** ✅ COMPLETE — 2026-03-16 (cycle 2026-03-15__release-v1.10 / EPIC-01 ST-01–ST-03)
**Priority:** P1 (High — blocks safe QA workflow)
**Type:** Operations / Infrastructure
**Origin:** v1.9 Sprint 2 post-merge QA — raised 2026-03-13
**Target release:** v1.10 (prerequisite before Sprint 1 begins)

The project has no development environment. All QA must currently be performed against the production (`main`) deployment, which means:
- Bug fixes cannot be tested before they land in production
- The merge gate condition "QA sign-off on live app" forces merging to main before a human can test
- Post-merge bug discovery (as occurred in v1.9 Sprint 2) is the only available feedback loop

This creates a structural governance gap: the human Director of Quality sign-off rule requires testing a live running application, but there is no non-production environment to test against.

**Scope**
- Provision a staging/dev environment that tracks `main` (or a designated `staging` branch)
- Environment must run both frontend and backend with real (or seeded) data
- CI/CD pipeline should deploy to staging automatically on merge to `main`
- QA sign-off process updated to use staging URL, not production

**Acceptance Criteria**
- Staging environment accessible via a stable URL
- Deploys automatically when `main` is updated
- Governance process updated: QA sign-off block references staging URL
- Production is not the first place bugs are discovered

---

### BLG-API-01 — Backend API integration tests (FastAPI TestClient)
**Status:** ✅ COMPLETE — 2026-03-16 (cycle 2026-03-15__release-v1.10 / EPIC-03 ST-05–ST-06; P3 deviation DEV-ST05-01 for prospective-heat — BLG-BE-02 filed)
**Priority:** P2
**Type:** QA Infrastructure
**Owner:** QA & Testing Owner
**Source:** ST-11 decision session 2026-03-09 — Head of Engineering and Director of Quality identified gap
**Cycle added:** 2026-03-06__release-v1.9
**Target release:** v1.10

**Problem**
The Playwright mock layer (ST-11) tests frontend rendering behaviour given known API payloads. It does not test whether the backend `GET /portfolio` and `GET /portfolio/prospective-heat` routers return correctly-shaped responses for real database rows. The golden output gate tests pure-math functions; it does not test the router-to-service pipeline end-to-end.

**Scope**
- Add FastAPI `TestClient` integration tests for `GET /portfolio` and `GET /portfolio/prospective-heat` endpoints
- Use fixture data (no live DB required — inject via dependency override or in-memory SQLite)
- Verify: response shape matches `portfolio_endpoints.md` contract, GBP conversion applies for US positions, heat formula produces correct output for known inputs
- Add as a CI step in a new workflow or extend `golden-outputs.yml`

**Acceptance Criteria**
- `TestClient` tests present in `tests/` covering at minimum: portfolio endpoint response shape, US position GBP conversion, heat formula output, prospective-heat endpoint calculation
- Tests are CI-safe (no live DB, no external calls)
- Director of Quality confirms CI step present and passing

**Last Updated:** 2026-03-09

---

### TEST-GAP-EPIC-06 — v1.7 test scenario coverage gap (BLG-QA-01)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-16
**Shipped in:** v1.10 — Operations & Quality Foundation
**Evidence:** `claude/cycles/2026-03-15__release-v1.10/verification_report.md`; EPIC-03/ST-07

✅ COMPLETE — [TEST-GAP-EPIC-06] — 2026-03-16 (cycle 2026-03-15__release-v1.10 / EPIC-03 ST-07 / BLG-QA-01): 4 v1.7 QA scenario gaps authored and executed as GAP-01–GAP-04 in `docs/testing/v1.7-qa-scenario-gaps.md`. GAP-01 PASS, GAP-02 PASS, GAP-03 FAIL (new finding BLG-BE-01 P1 filed), GAP-04 BLOCKED (no closed trades in staging — deferred). BLG-QA-01 closed. Item retired.

---

### v1.9 Release Slice — 2026-03-06__release-v1.9

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-15
**Shipped in:** v1.9 — User Value & Insight
**Evidence:** Sprint 1 shipped 2026-03-09; Sprint 2 shipped 2026-03-13; `claude/cycles/2026-03-06__release-v1.9/verification_report.md`

<!-- release-plan-marker: RP:v1.9:2026-03-06__release-v1.9 -->

**Cycle:** 2026-03-06__release-v1.9
**Release:** v1.9 — User Value & Insight
**Planned:** 2026-03-06
**Backlog slice:** `claude/cycles/2026-03-06__release-v1.9/stage4_backlog_slice.md`

**Sprint 1 (✅ SHIPPED 2026-03-09):** EPIC-04 (ST-06–ST-10), EPIC-05 partial (ST-11, ST-13), EPIC-06 (ST-14–ST-19)
**Sprint 2 (✅ SHIPPED 2026-03-13):** EPIC-01 (ST-01–ST-02), EPIC-02 (ST-03, ST-05), EPIC-03 (ST-04), EPIC-05 partial (ST-12)

---

### v1.8 Release Slice — 2026-03-04__release-v1.8

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-15
**Shipped in:** v1.8 — Risk Dashboard
**Evidence:** All EPICs shipped 2026-03-05; `claude/cycles/2026-03-04__release-v1.8/closure_record.md`

<!-- release-plan-marker: RP:v1.8:2026-03-04__release-v1.8 -->

**Cycle:** 2026-03-04__release-v1.8
**Release:** v1.8 — Risk Dashboard
**Planned:** 2026-03-04
**Backlog slice:** `claude/cycles/2026-03-04__release-v1.8/stage4_backlog_slice.md`

Items in v1.8 sprint: EPIC-01 (ST-01–ST-04), EPIC-02 (ST-05–ST-08), EPIC-03 (ST-09–ST-10), EPIC-04 (ST-11–ST-12)

---

### BLG-FEAT-08 — Basic Compliance Metrics ✅ COMPLETE
**Priority:** P2
**Effort:** ~1 day
**Target release:** v1.9 (pre-work gate for Structured Trade Reflection Template)
**Closed:** 2026-03-13 | Cycle: 2026-03-06__release-v1.9 | EPIC-03/ST-01

Lightweight discipline metrics: journal completion rate, stop-based exit rate, average position size (% of portfolio). Definitions canonicalised in `metrics_definitions.md` first.

---

### BLG-NEW-09 — R-Multiple Distribution Report ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Analytics / User Value
**Owner:** Metrics Definitions & Analytics Owner
**Source:** IDEA-metrics-analytics-20260304-01, IW-20260304-01
**Cycle added:** 2026-03-06__item-3.4
**Closed:** 2026-03-13 | Cycle: 2026-03-06__release-v1.9 | EPIC-02/ST-04

**Problem**
No visualisation of R-multiple distribution existed. R-multiple is the canonical trade quality measure — users could not see whether trades were systematically achieving R > 1.

**Acceptance Criteria met**
- R-multiple formula defined and canonicalised in metrics_definitions.md
- Distribution visualisation present on analytics page
- Values computed from canonical backend formula; no client-side derivation

---

### BLG-NEW-10 — Canonical Test Scenario Library ✅ COMPLETE
**Priority:** P1 (High)
**Type:** QA Infrastructure
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260304-01, IW-20260304-01
**Cycle added:** 2026-03-06__item-3.4
**Closed:** Phase 1: 2026-03-09 | Phase 2: 2026-03-13 | Cycle: 2026-03-06__release-v1.9

Both phases delivered: seeded test infrastructure + TEST-GAP-EPIC-01 resolution (Phase 1); v1.9 feature scenarios added at delivery (Phase 2).

---

### BLG-NEW-11 — Canonical Terms Glossary ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Governance / Spec Quality
**Owner:** Head of Specs Team
**Cycle added:** 2026-03-06__item-3.4
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-14

Canonical terms glossary created as Class 2 Supporting document. All key trading and system terms defined with canonical source links. Registered in Specs_Index.md.

---

### BLG-NEW-12 — Service Layer Test Coverage Standard ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Engineering Quality / CI
**Owner:** Backend Engineering Patterns Owner
**Cycle added:** 2026-03-06__item-3.4
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-05/ST-13

Service Layer Test Coverage Standard authored. CI step enforces coverage threshold on services/ directory. Standard integrated with backend_engineering_patterns.md.

---

### BLG-NEW-04 — AI-Assisted Workflow Governance Policy ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Governance
**Owner:** Product Owner
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-15

AI-Assisted Workflow Governance Policy document authored and filed. Covers: scope of AI authority, mandatory human review checkpoints, escalation triggers, record-keeping obligations.

---

### BLG-RD-01 — Entity store fallback masks API error states ✅ COMPLETE
**Priority:** P2
**Type:** Frontend Defect — Error State Coverage
**Source:** DEV-ST03-01 — Delivery verification 2026-03-04__release-v1.8
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-08

Each Risk Dashboard component now renders its own error state when GET /portfolio fails. Entity fallback no longer silently masks failure.

---

### BLG-RD-02 — GracePeriodPanel empty vs error state ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Error State UX
**Source:** DEV-ST03-02 — Delivery verification 2026-03-04__release-v1.8
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-08

GracePeriodPanel now renders a visible error card when portfolioError is set, distinct from the empty state.

---

### BLG-RD-03 — PositionRiskTable sorted descending ✅ COMPLETE
**Priority:** P2
**Type:** Frontend Defect — Sort Direction
**Source:** DEV-ST03-03
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-09

PositionRiskTable now sorts by stop distance ascending (tightest stop first) per spec §6.4.

---

### BLG-RD-04 — Stop Price column absent ✅ COMPLETE
**Priority:** P2
**Type:** Frontend Defect — Missing Column
**Source:** DEV-ST03-04
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-09

Stop Price column (current_stop, GBP, 2dp) now present in PositionRiskTable per spec §6.2.

---

### BLG-RD-05 — GRACE badge colour ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Cosmetic
**Source:** DEV-ST03-05
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-10

GRACE state badge now rendered in blue per spec §6.3.

---

### BLG-RD-06 — GBP value at risk absent from HeatGauge ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Missing Metric
**Source:** DEV-ST03-06
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-10

GBP value at risk now displayed below gauge value per spec §3.2.

---

### BLG-RD-07 — Days in Grace column absent ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Missing Column
**Source:** DEV-ST03-07
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-09

Days in Grace (holding_days) column now present in Grace Period table per spec §5.2.

---

### BLG-RD-08 — Drawdown data source resolved ✅ RESOLVED
**Priority:** P2
**Type:** Spec Alignment — Owner Decision
**Source:** DEV-ST03-08
**Closed:** 2026-03-06 | ST-06 investigation

Split-source data model confirmed: current_drawdown_percent from GET /portfolio (drawdown_service.py); days_underwater from GET /analytics/metrics (analytics_service.py). risk_dashboard.md §4.1 updated to v0.1.7 to reflect correct split sources.

---

### BLG-RD-09 — ProspectiveHeatPanel missing threshold label ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Missing Display Element
**Source:** DEV-ST03-09
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-09

Threshold label badge now present in prospective heat result row, updating when boundary is crossed per §7.5.

---

### BLG-RD-10 — US entry prices in USD not GBP ✅ COMPLETE
**Priority:** P2
**Type:** Backend + Frontend Defect — Currency Conversion
**Source:** DEV-ST03-11
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-07

portfolio_service.py now converts entry_price to GBP for US positions. Risk Dashboard displays entry prices in GBP for all positions per §6.2.

---

### BLG-RD-11 — current_stop in USD for US positions ✅ COMPLETE
**Priority:** P2
**Type:** Backend + Frontend Defect — Currency Conversion
**Source:** DEV-ST03-12
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-07

portfolio_service.py now converts current_stop to GBP for US positions. Stop Distance % calculation uses matching currencies per §6.2.

---

### TEST-GAP-EPIC-01 — Risk Dashboard scenario infrastructure gap ✅ CLOSED
**Priority:** P2
**Type:** QA Infrastructure
**Source:** Delivery verification 2026-03-04__release-v1.8
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | ST-11

Playwright mock layer delivered. All 17 unexecuted scenarios automated in tests/e2e/risk-dashboard.spec.js. CI gate at .github/workflows/playwright.yml. Mock data in tests/e2e/mocks/portfolio-mock-data.js. Scenario document updated to v1.1.

---

### BLG-SPEC-D1 — API Contracts README.md version frozen at v1.8.4 ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Documentation Drift
**Owner:** API Contracts & Documentation Owner
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

README.md version header updated to v1.9.0. Changelog includes v1.9.0 entry referencing EPIC-06 changes.

---

### BLG-SPEC-D3 — GET /market/status completely undocumented ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Documentation Gap / Drift
**Owner:** API Contracts & Documentation Owner
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-16

docs/specs/api_contracts/market_endpoints.md created. Endpoint documented, registered in Specs_Index.md, added to openapi.yaml.

---

### BLG-SPEC-D4 — GET /positions/search/tags undocumented ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Documentation Gap
**Owner:** API Contracts & Documentation Owner
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

position_endpoints.md now includes GET /positions/search/tags with request parameters and response schema.

---

### BLG-SPEC-D8 — System_status_report.md missing lifecycle header ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Lifecycle Compliance Drift
**Owner:** Director of Quality
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

Lifecycle header added to docs/System_status_report.md. Class and Status assigned per document_lifecycle_guide.md.

---

### BLG-SPEC-D9 — process_index.md and Specs_Index.md wrong path for lifecycle guide ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Documentation Drift / Broken Cross-Reference
**Owner:** Head of Specs Team
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

Both process_index.md and Specs_Index.md §5 updated to reference claude/charter/document_lifecycle_guide.md.

---

### BLG-SPEC-G1 — settings_model.md missing ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Spec Gap
**Owner:** Head of Specs Team
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-17

settings_model.md created in docs/specs/data_model/. Registered in Specs_Index.md §3. Cross-referenced from settings_endpoints.md.

---

### BLG-SPEC-G2 — Error Response Standard not defined ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Spec Gap
**Owner:** API Contracts & Documentation Owner
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-18

Error Response Standard document created. Standard error envelope shape, required fields, HTTP status code mapping defined. All existing API contract docs reference the standard. Registered in Specs_Index.md.

---

### BLG-SPEC-G3 — structured_logging_standards.md not in Specs_Index ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Index Gap
**Owner:** Head of Specs Team
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

Specs_Index.md §3 updated to include structured_logging_standards.md with Owner, Class, Status, Version.

---

### BLG-SPEC-G4 — ADR-002 in wrong location ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Governance Organisation Gap
**Owner:** Head of Specs Team
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

ADR-002 moved to docs/product/decisions/. Cross-references updated.

---

### BLG-SPEC-G5 — validation_system.md owner non-compliant ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Lifecycle Compliance Gap
**Owner:** Infrastructure & Operations Owner
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

validation_system.md owner field updated to a named governance role. Specs_Index.md §7.1 notation updated to reflect resolved.

---

### BLG-NEW-08 — Automated OpenAPI Drift Detection in CI ✅ COMPLETE
**Priority:** P1 (High)
**Type:** CI / Governance
**Owner:** Engineering (CI)
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-08

**Problem**
`docs/reference/openapi.yaml` was not updated during EPIC-06 when three contracts were bumped to v1.9.0 (BLG-SPEC-D7). There is no CI check that detects drift between the markdown API contracts and openapi.yaml. Drift will recur without an automated gate.

**Scope**
- Add a CI step that detects drift between `openapi.yaml` and the markdown API contracts
- Approach: either (a) generate openapi.yaml from contracts and compare, or (b) run a custom lint/diff check against known contract fields
- Block merge on detected drift

**Acceptance Criteria**
- CI step detects drift between openapi.yaml and markdown contracts
- Merge blocked if drift is detected
- Approach documented (generation vs diff) — approach decision to be made in pre-alignment

---

### BLG-NEW-07 — Running API Changelog Document ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Documentation / Governance
**Owner:** API Contracts & Documentation Owner
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-12

**Problem**
There is no single running changelog document for API contract changes. Changes to endpoint contracts (new fields, removed fields, version bumps) are recorded in individual spec files but there is no centralised, human-readable history of API evolution across versions.

**Scope**
- Create a running API Changelog document that summarises contract changes per version
- Cover all contracts under `docs/specs/api_contracts/`
- Backfill from v1.8.x → v1.9.0 changes (EPIC-06 scope)
- Document maintainer obligation: must be updated alongside every contract version bump

**Acceptance Criteria**
- API Changelog document exists and is registered in Specs_Index.md
- All v1.9.0 contract changes (EPIC-06) are backfilled
- Maintenance obligation documented alongside contract spec authoring workflow

---

### BLG-NEW-05 — Dependency Vulnerability Scanning in CI ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Security / CI
**Owner:** Engineering (CI)
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-07

**Problem**
There is no automated scanning of Python dependencies for known vulnerabilities in the CI pipeline. A compromised or vulnerable dependency could be introduced silently.

**Scope**
- Add a CI step that scans Python dependencies (e.g., using `pip-audit` or `safety`) for known CVEs
- Block merge (or warn at configurable severity) on high/critical vulnerabilities
- Integrate with existing `.github/workflows/` structure

**Acceptance Criteria**
- Dependency vulnerability scan runs on every PR
- High/critical CVEs block merge (or produce a required review comment)
- Scan tool and severity threshold documented

---

### BLG-NEW-03 — Define and Document Unavailability Failure Mode ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Policy / Governance
**Owner:** Infrastructure & Operations Owner
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-11

**Problem**
There is no documented policy for what happens when the system is unavailable during a trading session (e.g., backend down, market data feed unavailable). The system has no documented failure modes or fallback procedures for the user.

**Scope**
- Define and document the unavailability failure mode: what the user should do, what the system state is, and any manual fallback procedures
- Document where this policy lives (e.g., OPERATIONAL_GUIDE.md or a new docs/ops/ document)

**Acceptance Criteria**
- Unavailability failure mode documented: system states covered, user action required, data integrity implications
- Document registered in appropriate governance index

---

### BLG-NEW-02 — Backtest vs Live Stop Reconciliation Report ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Quality / CI
**Owner:** Engineering + QA
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Dependency:** After BLG-NEW-01 (golden output baseline must be in place first)
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-06

**Problem**
There is no automated verification that the trailing stop formula used in backtests and the formula used in the live system produce identical results for the same inputs. Silent divergence between backtest and live logic is a category of defect that cannot be caught by either gate independently.

**Scope**
- Report or CI assertion that compares backtest stop calculations vs live system stop calculations for a set of known inputs
- Output: reconciliation result confirming parity or flagging divergence

**Acceptance Criteria**
- Automated check exists that verifies backtest and live stop logic produce identical results for all golden inputs
- Any divergence between backtest and live calculation fails the check

---

### BLG-NEW-01 — Golden Output Regression Baseline for CI ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Quality / CI
**Owner:** Engineering + QA
**Source:** IDEA-director-of-quality-20260304-02 — Director of Quality, IW-20260304-01
**Cycle added:** 2026-03-04__item-3.4
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-05

**Problem**
The current CI gate (`POST /validate/calculations`, EPIC-01) checks only that `critical_failed > 0` blocks the merge. It does not verify that specific calculations return the correct numeric values. A change that silently alters the trailing stop formula from `CurrentPrice - (2 × ATR)` to `CurrentPrice - (2.1 × ATR)` would pass the current gate. Numeric regressions are the highest-risk defect class in a trading system.

**Scope**
- Define a set of deterministic golden test cases: known inputs (entry_price, ATR, risk_percent, etc.) with expected output values derived directly from the canonical strategy spec
- Store as `tests/golden_outputs.json` — treated as a canonical artefact; updated only via spec-linked PR
- Scope limited to stop/sizing calculations only (per STEP 5 scoping from IW-20260304-01)
- Add a CI step that calls the backend with each golden input and asserts output matches to required precision
- Any numeric divergence from golden values fails the build

**Acceptance Criteria**
- `tests/golden_outputs.json` exists with spec-derived golden values for stop and sizing calculations
- CI step added that runs golden output assertions on every PR
- Build fails on any numeric deviation from golden values
- Precision tolerance documented (e.g., 4 decimal places for share counts)
- Golden values derived from canonical spec, not from current implementation

**Dependencies**
- None (prerequisite: BLG-NEW-02 must follow, not precede)

---

### BLG-SPEC-D7 — openapi.yaml frozen at v1.8.1; not updated for v1.9.0 contracts ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Documentation Drift / Reference Artefact Staleness
**Owner:** API Contracts & Documentation Owner
**Raised:** 2026-03-03 — Head of Specs Team review
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-10 — openapi.yaml updated to v1.9.0

**Problem**
`docs/reference/openapi.yaml` is at version 1.8.1 (1193 lines).
Three contracts were bumped to v1.9.0 in EPIC-06:
- `sharpe_ratio_trade_method` absent from /validate/calculations validated metrics list
- portfolio positions response schema not aligned to v1.9.0 field list
- `holding_days` absent from GET /trades trade object schema
Specs_Index.md §4 states: "openapi.yaml must be reviewed inline with every contract change; markdown contracts take precedence on conflict."
This was not done during EPIC-06.

**Acceptance Criteria**
- openapi.yaml version field updated to 1.9.0
- /validate/calculations response includes sharpe_ratio_trade_method (14 validated metrics total)
- GET /trades trade object includes holding_days (integer)
- GET /portfolio positions objects reflect v1.9.0 field list
- No conflicts between openapi.yaml and markdown contracts

---

### BLG-SPEC-D2 — settings_endpoints.md spec/implementation mismatch ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Spec–Implementation Drift
**Owner:** API Contracts & Documentation Owner + Head of Engineering
**Raised:** 2026-03-03 — Head of Specs Team review
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-09 — settings_endpoints.md v1.1.0 published; PATCH/POST documented as canonical

**Problem**
`docs/specs/api_contracts/settings_endpoints.md` specifies `PUT /settings` (replace all settings).
Live implementation in `backend/main.py` uses `PATCH /settings/{settings_id}` (update single setting by ID).
Additionally, `POST /settings` is implemented but not documented anywhere.
This is a P1 drift: clients relying on the spec will call the wrong method and path.

**Decision Required**
Product Owner + API Contracts owner to choose:
(a) Update spec to document `PATCH /settings/{settings_id}` and `POST /settings` as the canonical interface, or
(b) Align backend to implement `PUT /settings` as specced (breaking change to existing frontend).

**Acceptance Criteria**
- settings_endpoints.md accurately documents the live HTTP method, path, and request/response schema
- No divergence between spec and implementation
- Decision record filed if option (b) chosen (breaking change)

---

### §6 v1.7 Release Slice — 2026-03-02__release-v1.7

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** All 6 EPICs shipped 2026-03-03; verified 2026-03-03 — `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

<!-- release-plan-marker: RP:v1.7:2026-03-02__release-v1.7 -->

**Cycle:** 2026-03-02__release-v1.7
**Planning Date:** 2026-03-02
**Status:** ✅ Complete — all 6 EPICs shipped 2026-03-03; verified 2026-03-03
**Reference:** claude/cycles/2026-03-02__release-v1.7/stage4_backlog_slice.md

| S2 ID | Item | Epic | Priority | Effort |
|-------|------|------|----------|--------|
| S2-01 | BLG-TECH-04 — CI/CD GitHub Actions Validation Workflow | EPIC-01 | P2 | ~1 day |
| S2-02 | Strategy Rules §13 Boundary Review | EPIC-02 | P1 | ~0.5 day |
| S2-03 | Metrics Definitions — Portfolio Heat Formula & Thresholds | EPIC-03 | P1 | ~0.5 day |
| S2-04 | Structured Logging / Observability Standards | EPIC-04 | P2 | ~1 day |
| S2-05 | API Versioning Strategy Decision Record | EPIC-05 | P2 | ~0.5 day |
| S2-06 | BLG-TECH-06 — Canonicalise sharpe_ratio_trade_method | EPIC-06 | P2 | ~30 min–1 hr |
| S2-07 | BLG-TECH-08 — Align portfolio_endpoints.md positions summary | EPIC-06 | P3 | ~30 min + decision |
| S2-08 | BLG-TECH-09 — Add holding_days to GET /trades | EPIC-06 | P3 | ~30 min + decision |

**Total estimated effort:** ~3.5–4 days
**Capacity assessment:** PASS (workforce_capacity.md — no constraints violated)
**Key gates unlocked by this release:**
- EPIC-02 → §13-gated features may enter pre-alignment
- EPIC-03 → v1.8 Risk Dashboard pre-alignment
- EPIC-04 + EPIC-05 → v2.0 Alerts pre-alignment (2 of 3 gates)

---

### BLG-SPEC-D6 — changelog.md has no v1.7 entry

**Status at retirement:** ✅ Complete — Resolved
**Priority at retirement:** P3
**Retired:** 2026-03-04
**Shipped in:** N/A — documentation fix
**Evidence:** v1.7 entry confirmed present in `docs/product/changelog.md` (verified 2026-03-04)

**BLG-SPEC-D6** — changelog.md has no v1.7 entry
**Priority:** P3 (Low)
**Type:** Documentation Drift
**Owner:** Product Owner
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`docs/product/changelog.md` last entry is v1.6.1 (2026-03-01).
v1.7 Foundation & Governance sprint was fully delivered and verified (2026-03-03).
No entry exists for v1.7.

**Acceptance Criteria**
- v1.7 changelog entry added covering: CI/CD merge gate (EPIC-01), §13 boundary review (EPIC-02), Portfolio Heat metrics (EPIC-03), Structured Logging Standards (EPIC-04), API Versioning Decision Record (EPIC-05), Spec Debt Resolution — analytics/portfolio/trade endpoints v1.9.0 (EPIC-06)

---

### BLG-SPEC-D5 — current_roadmap.md v1.7 section not closed out

**Status at retirement:** ✅ Complete — Resolved
**Priority at retirement:** P3
**Retired:** 2026-03-04
**Shipped in:** N/A — documentation fix
**Evidence:** Resolved by `manage roadmap` run 2026-03-04 — v1.7 section retired to `claude/roadmap/roadmap_archive.md`; release summary updated; footer already referenced correct backlog path

**BLG-SPEC-D5** — current_roadmap.md v1.7 section not closed out
**Priority:** P3 (Low)
**Type:** Documentation Drift
**Owner:** Product Owner
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`claude/roadmap/current_roadmap.md` v1.7 section items still show "Status: Planned".
Release Summary table has no ✅ for v1.7.
v1.7 was fully delivered (2026-03-02) and verified (2026-03-03).
Additionally, footer references `docs/product/feature_backlog.md` which does not exist (actual backlog: `claude/backlog/backlog.md`).

**Acceptance Criteria**
- v1.7 section marked Complete with delivery date
- Release Summary table updated (✅ v1.7)
- Footer corrected to reference correct backlog path

---

### BLG-NEW-06 — Realised vs Unrealised P&L Labelling

**Status at retirement:** ❌ Killed — merged into 4.1b pre-work scope
**Priority at retirement:** N/A
**Retired:** 2026-03-04
**Shipped in:** N/A — merged
**Evidence:** DL-005 (2026-03-04); merged into roadmap item 4.1b Tax-Year P&L Statement pre-work scope

**BLG-NEW-06** — Realised vs Unrealised P&L Labelling
**Status:** Merged into 4.1b pre-work scope — not a standalone backlog item
**Source:** IW-20260304-01
**Cycle added:** 2026-03-04__item-3.4

This item (clear distinction of realised vs unrealised P&L amounts in the tax-year P&L statement) has been merged into the 4.1b Tax-Year P&L Statement scope as pre-work. See current_roadmap.md §4.1b scope note (2026-03-04). No standalone delivery required.

---

### BLG-TECH-09 — Add holding_days to GET /trades

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** Cycle 2026-03-02__release-v1.7, EPIC-06/TASK-28–30; `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

**BLG-TECH-09** — Add holding_days to GET /trades
**Priority:** P3
**Effort:** ~1 hour
**Target release:** v1.7
**Status:** ✅ COMPLETE — 2026-03-03 (cycle: 2026-03-02__release-v1.7, EPIC-06/TASK-28–30; backend fix path chosen)
**Source:** OBS-QWB-R3-01 — QA Lead observation, QWB verification, 2026-03-01
holding_days is absent from trade objects in the GET /trades response.
trade_endpoints.md v1.8.4 lists it as a required field. Pre-existing behaviour,
not introduced by QWB.
Decision required: Either (a) add holding_days to the backend GET /trades
response (the spec-compliant fix); or (b) remove holding_days from trade_endpoints.md
documented schema. Product Owner + API Contracts owner to decide.
Acceptance Criteria

GET /trades trade objects include holding_days (integer), OR
trade_endpoints.md schema is corrected to remove the field, with a note explaining
its absence and where the value can be sourced (e.g. trades_for_charts)

**Owner:** API Contracts & Documentation Owner
Raised by: QA Lead, 2026-03-01

---

### BLG-TECH-08 — Align portfolio_endpoints.md positions summary field list

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** Cycle 2026-03-02__release-v1.7, EPIC-06/TASK-25–27; `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

**BLG-TECH-08** — Align portfolio_endpoints.md positions summary field list
**Priority:** P3
**Effort:** ~30 min
**Target release:** v1.7
**Status:** ✅ COMPLETE — 2026-03-03 (cycle: 2026-03-02__release-v1.7, EPIC-06/TASK-25–27; spec update path chosen)
**Source:** OBS-QWB-R1-01 — QA Lead observation, QWB verification, 2026-03-01
GET /portfolio positions summary objects omit current_price_native, stop_price,
stop_price_native, and pnl_percent — fields listed in R-01 test scenario step 3
and in portfolio_endpoints.md. Pre-existing behaviour, not introduced by QWB.
Decision required: Either (a) update portfolio_endpoints.md to accurately document
the lightweight summary shape, explicitly distinguishing it from the full position object
on GET /positions; or (b) add the missing fields to the backend response. Product Owner

API Contracts owner to decide.

**Acceptance Criteria**

portfolio_endpoints.md positions summary field list matches the live API response
No discrepancy between spec and implementation for /portfolio positions objects

Owner: API Contracts & Documentation Owner
Raised by: QA Lead, 2026-03-01

---

### BLG-TECH-06 — Canonicalise sharpe_ratio_trade_method as 14th validation metric

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** Cycle 2026-03-02__release-v1.7, EPIC-06/TASK-21–24; `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

**BLG-TECH-06** — Canonicalise sharpe_ratio_trade_method as 14th validation metric in analytics_endpoints.md
**Priority:** P2 (Medium)
**Type:** Spec Accuracy / Governance
**Target release:** v1.7 *(updated from v1.6.1 — v1.6.1 has shipped; DL-001 cycle 2026-03-01__item-3.2)*
**Status:** ✅ COMPLETE — 2026-03-03 (cycle: 2026-03-02__release-v1.7, EPIC-06/TASK-21–24)
**Problem**
POST /validate/calculations returns 14 validation results. analytics_endpoints.md v1.8.1
describes 13 metrics and does not document sharpe_ratio_trade_method.
The 14th metric was introduced under BLG-TECH-01 Addendum 1 (PMO-confirmed scope, 2026-02-20)
to exercise the trade-based Sharpe fallback path. The implementation is correct and the result
passes. The spec is incomplete.
This was recorded as OBS-01 by the QA Lead during BLG-TECH-02/03 re-verification
(2026-02-21T21:25:00Z) and formally acknowledged by the Product Owner (2026-02-21).
Per document_lifecycle_guide.md v2.2 — deviation must have priority, target release,
and owner at time of documentation. These are recorded here.
Scope

Update analytics_endpoints.md to add sharpe_ratio_trade_method as a formally
documented 14th validation metric
Add to the validated metrics table with: severity critical, formula, tolerance
Update the response example to show 14 results and correct by_severity.critical.total: 4
No code change required — implementation is correct

**Acceptance Criteria**

analytics_endpoints.md validated metrics table includes sharpe_ratio_trade_method
Response schema example reflects 14 results
by_severity.critical.total shown as 4 in example (not 3)
No deviation exists between the spec and the live POST /validate/calculations response

**Owner**

API Contracts & Documentation Owner

**Source**

OBS-01 — QA Lead, BLG-TECH-02/03 re-verification, 2026-02-21T21:25:00Z
Product Owner disposition: backlog item, v1.6.1 target, 2026-02-21

---

### BLG-TECH-04 — CI/CD validation workflow (GitHub Actions)
**Priority:** P2 (Medium)
**Type:** Delivery Quality / Automation
**Status:** ✅ COMPLETE — 2026-03-03 (cycle: 2026-03-02__release-v1.7, EPIC-01)
**Target release:** v1.7

**Problem**
- Validation is manual and not enforced at merge time.

**Scope**
- Add `.github/workflows/validate-analytics.yml`.
- Run `POST /validate/calculations` on:
  - Pull requests
  - Pushes to `main` and `develop`
- Block merge if any **critical-severity** validation fails.
- Post validation summary as PR comment.

**Acceptance Criteria**
- Workflow reliably runs on all PRs.
- Merge is blocked only for critical severity failures.
- Clear PR feedback is visible.

**Dependencies**
- BLG-TECH-02 (severity model must exist).

**Owners**
- Engineering
- QA

---

### BLG-FEAT-07 — CSV Export of Trade History
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

One-click CSV export for tax and analysis use.

---

### BLG-FEAT-06 — Grace Period Indicator
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Show remaining grace period days in open positions table.
Example: "Day 6 of 10"

---

### BLG-FEAT-05 — Win Rate by Month Chart
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Bar chart of win rate grouped by calendar month.

---

### BLG-FEAT-04 — Best / Worst Trades Widget
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Show top 3 and bottom 3 trades by R-multiple or P&L.

---

### BLG-FEAT-02 — R-Multiple Column in Trade History
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Add R-multiple column to trade history table.

**Indicative Formula**

`(Exit Price - Entry Price) / (Entry Price - Stop Price)`

**Notes**
- Formula must be confirmed by Metrics Definitions owner.
- Decide server-side vs frontend-only calculation.

---

### BLG-FEAT-01 — Current Drawdown Widget
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Display current drawdown from peak and days underwater.
Example: "Drawdown: -8.2%, 12 days underwater"

**Dependency**
- Metrics Definitions owner must confirm drawdown calculation before implementation.

---

### BLG-TECH-03 — Consolidate ValidationService into service layer

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-04
**Shipped in:** v1.6.1 (co-delivered with BLG-TECH-02)
**Evidence:** Director of Quality sign-off 2026-02-21T21:30:00Z; `docs/product/phase_gates/BLG-TECH-03-validationservice-consolidation-phase-gate.md`

BLG-TECH-03 — Consolidate ValidationService into service layer
Priority: P1 (High)
Type: Architecture / Maintainability
Status: ✅ COMPLETE — 2026-02-21
Closed

All validation logic moved from routers/validation.py into services/validation_service.py
Router thinned to HTTP in/out only — delegates entirely to ValidationService.validate_all()
Stub replaced with full 13-metric + trade-Sharpe implementation
Delivered in same branch as BLG-TECH-02 per co-delivery constraint
Director of Quality sign-off: 2026-02-21T21:30:00Z
Phase Gate Document filed: docs/product/phase_gates/BLG-TECH-03-validationservice-consolidation-phase-gate.md

---

### BLG-TECH-02 — Implement validation severity model

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** Director of Quality sign-off 2026-02-21T21:30:00Z; `docs/product/phase_gates/BLG-TECH-02-validation-severity-model-phase-gate.md`

BLG-TECH-02 — Implement validation severity model
Priority: P1 (High)
Type: Governance / Operational Control
Status: ✅ COMPLETE — 2026-02-21
Closed

severity field added to every validation result object (critical / high / medium / low)
by_severity aggregation added to summary — all four tiers always present
Severity mapping implemented in ValidationService per analytics_endpoints.md v1.8.1
Director of Quality sign-off: 2026-02-21T21:30:00Z
Phase Gate Document filed: docs/product/phase_gates/BLG-TECH-02-validation-severity-model-phase-gate.md

---

### BLG-TECH-01 — Fix Sharpe variance method + Capital Efficiency currency basis
**Priority:** P0 (Critical)
**Type:** Metrics Correctness / Validation Integrity
**Status:** ✅ COMPLETE — 2026-02-21

**Closed**
- `_calculate_sharpe()` updated to use sample variance (÷ n−1) for portfolio and trade-level Sharpe methods
- Capital efficiency updated to use `Mean(total_cost)` in GBP from `trade_history`
- `validation_data.py` expected values updated: `capital_efficiency` 0.17 → 0.22; `total_cost` fields added
- Validation: 13/13 pass confirmed at 2026-02-21T00:24:41Z
- Canonical Owner sign-off: 2026-02-21
- `metrics_definitions.md` v1.5.7 — Appendix E both items marked resolved
- `analytics_endpoints.md` v1.8.1 — resolved known limitations removed
- v1.6 quality gate: satisfied

---

### v2.0 Release Items — 2026-03-17__release-v2.0 (Backlog Grooming 2026-03-17)

**Retired:** 2026-03-17
**Shipped in:** v2.0 — Reporting & Alerts
**Evidence:** `claude/cycles/2026-03-17__release-v2.0/verification_report.md`; `closure_record.md`

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

### v2.1 Backlog Items — 2026-03-18__release-v2.1

**Status at retirement:** ✅ Complete
**Retired:** 2026-03-21
**Shipped in:** v2.1 — Alerts, Watchlists & Enhancements
**Evidence:** `claude/cycles/2026-03-18__release-v2.1/verification_report.md` — all 19 items delivered

| Item ID | Title | Story | Notes |
|---------|-------|-------|-------|
| BLG-SPEC-G6 | total_return_pct not returned by GET /analytics/metrics | ST-17 | Spec updated; implementation shipped |
| BLG-SPEC-D10 | api_dependencies.md v2.0 additions | ST-17 | Spec updated to include Reports + Signals mappings |
| BLG-SPEC-D11 | data_model.md §501 trade_reflections section | ST-17 | Section updated to reflect implemented status |
| BLG-SPEC-D12 | Bulk lifecycle header remediation (28 docs) | ST-16 | All 28 docs updated to Class 1/2 headers |
| BLG-SPEC-D13 | metrics_definitions.md Owner field non-compliant | ST-17 | Owner field corrected to governance role |
| TEST-GAP-SIG-01 | Signals page controls test scenarios | ST-18 | signals_scenarios.md authored |
| TEST-GAP-TAX-01 | Tax Year P&L report test scenarios | ST-18 | reports_scenarios.md authored |
| BLG-PROC-01 | Cross-EPIC process compliance check | ST-19 | v2.1 sprint compliance confirmed; EPIC-03 cherry-pick deviation documented |
| BLG-OPS-03 | Pre-merge frontend preview environments | ST-15 | seed-preview.yml psql approach shipped; frontend preview blocker documented |
| BLG-FR-01 | Tax Year P&L Report PDF Export | ST-12 | GET /reports/tax-year?format=pdf implemented with server-side PDF generation |

---

### v2.7 Release Slice — 2026-04-13__release-v2.7

**Status at retirement:** ✅ Complete
**Retired:** 2026-04-16
**Shipped in:** v2.7 — Performance, Governance Hardening & Market Intelligence
**Evidence:** 11/11 items shipped; `claude/cycles/2026-04-13__release-v2.7/closure_record.md`

| ID | Title | Story | Notes |
|----|-------|-------|-------|
| BLG-OPS-14 | Enable Supabase Supavisor connection pooling | ST-01 | Delegated; p50=234ms (PASS ≤400ms) |
| BLG-BE-07-FIX | Refactor get_portfolio_summary() single DB connection | ST-02 | GET /portfolio 1 connection/request; p50 ≤400ms |
| BLG-GOV-18 | Require QA sign-off block complete before PR | ST-03 | execution_prompt.md §3.2.B gated |
| BLG-GOV-19 | Define autonomous DoQ sign-off class | ST-04 | delivery_verification_prompt.md STEP -1.3 updated |
| BLG-GOV-16 | Extend governance_sync.yml to trigger on push to main | ST-05 | Issues now auto-close on main push |
| BLG-QA-11 | Fix Playwright page.route() intercepts (LIFO fix) | ST-06 | 46/46 Playwright tests pass |
| BLG-QA-12 | System Status Playwright spec | ST-07 | system-status.spec.js — 16 scenarios pass |
| BLG-FEAT-17 | Market Correlation Analysis | ST-08 | GET /analytics/market-correlation; AC-6 frontend deferred |
| BLG-BE-10 | Supplementary indicator fields (display-only) | ST-09 | 4 fields added; §13 COMPLIANT |
| BLG-SPEC-D17 | Spec Dependency Map | ST-10 | docs/specs/spec_dependency_map.md v1.0 |
| BLG-GOV-14 | Governance Health Score | ST-11 | OPERATIONAL_GUIDE §15; roadmap_prompt STEP -1.7 |

---

### v2.6 Release Slice — 2026-04-11__release-v2.6

**Status at retirement:** ✅ Complete
**Retired:** 2026-04-17 (post-ship cleanup — execution_state.json was not sealed; items identified by cross-referencing git log)
**Shipped in:** v2.6 — Backend Integration Completion, Test Automation & Governance Hardening
**Evidence:** 15/15 stories shipped; PRs #218–#221 merged to main; `claude/cycles/2026-04-11__release-v2.6/`

| ID | Title | Story | PR | Notes |
|----|-------|-------|----|-------|
| BLG-BE-08-GAP-01 | Migrate Reports Performance Tab to FastAPI | ST-01 | #218 / 5a6982d | No Base44 calls remain in Performance tab |
| BLG-BE-09-GAP-01 | Wire Signals dismissal and position creation to FastAPI | ST-02 | #218 / 5a6982d | Pre-existing FastAPI wiring confirmed |
| BLG-BE-09-GAP-02 | Replace Base44 cash balance on Signals page | ST-03 | #218 / 5a6982d | GET /cash/summary wired |
| BLG-QA-09 | Fix 4 pytest collection errors | ST-04 | #219 / 39efe64 | 129 tests pass, 0 collection errors |
| BLG-QA-10 | Add CI test runner workflow | ST-05 | #219 / 39efe64 | ci-tests.yml; Phase A + B delivered |
| BLG-QA-07 | Fee drag Playwright spec | ST-06 | #219 / 39efe64 | SC-FEE-01–04 pass |
| BLG-QA-08 | Pytest unit tests for fee drag | ST-07 | #219 / 39efe64 | 17 tests; SC-FEE-05, SC-FEE-06 pass |
| BLG-FE-10 | Add tooltip prop to StatsCard | ST-08 | #220 / a640719 | Avg Fee Drag card wired |
| BLG-FE-11 | Trade History StatsCard bar layout (6-card) | ST-09 | #220 / a640719 | 7-card bar; grid-cols-2 md:grid-cols-4 xl:grid-cols-7 |
| BLG-FE-12 | Trade History column header styling | ST-10 | #220 / a640719 | font-semibold text-slate-300 tracking-wide |
| BLG-FE-13 | Flexible column sorting | ST-11 | #220 / a640719 | 5 new sort states; Days Held column added |
| BLG-GOV-15 | Upgrade decision_log.md hard gate | ST-14 | #221 / 27902b7 | roadmap_prompt STEP 9 structural halt |
| BLG-FE-09 | Frontend Performance Budget spec | ST-15 | #221 / 27902b7 | docs/specs/frontend/performance_budget.md |

---

### v2.9 Release Slice — 2026-04-22__release-v2.9

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-04-24
**Shipped in:** v2.9 — Arc 1 Foundation: Stock Discovery & Screening Spec & Infrastructure
**Evidence:** 15/15 stories shipped (DEV-01 P3 accepted); `claude/cycles/2026-04-22__release-v2.9/closure_record.md`

| ID | Title | Type | Story | Evidence |
|----|-------|------|-------|----------|
| BLG-SPEC-21 | Screener results schema spec | Spec | ST-01 | changelog.md v2.9; verification_report.md |
| BLG-SPEC-22 | Alpaca API integration contract | Spec | ST-02 | changelog.md v2.9; verification_report.md |
| BLG-SPEC-23 | Screener internal API contract | Spec | ST-03 | changelog.md v2.9; verification_report.md |
| BLG-FE-17 | Screener results page UX spec | Frontend | ST-04 | changelog.md v2.9; verification_report.md |
| BLG-GOV-16 | §13 review record for DS-06 | Gov | ST-08 | changelog.md v2.9; verification_report.md |
| BLG-QA-08 | External API mock harness for CI | QA | ST-09 | changelog.md v2.9; verification_report.md |
| BLG-QA-09 | Screener test data library | QA | ST-10 | changelog.md v2.9; verification_report.md |
| BLG-GOV-14 | execution_prompt.md §3.2 governance patches | Gov | ST-11 | changelog.md v2.9; verification_report.md |
| BLG-GOV-15 | execution_prompt.md STEP 5.1.B cross-check | Gov | ST-12 | changelog.md v2.9; verification_report.md |
| BLG-FE-15 | SystemStatus.js `/ai` prefix fix | Frontend | ST-13 | changelog.md v2.9; verification_report.md |
| BLG-AI-01 | AI Journal summary audit log | Backend | ST-14 | changelog.md v2.9; verification_report.md |
| TEST-GAP-EPIC-04 | AI Journal test scenarios | QA | ST-15 | changelog.md v2.9; verification_report.md |

---

### BLG-SPEC-21 — Screener results schema spec
**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-01 ST-01)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

Canonical specification for screener output data structure authored as Class 2 document. All screener output fields defined with types and derivation source. §11 parameter reference explicit. DoQ sign-off obtained.

---

### BLG-SPEC-22 — Alpaca API integration contract
**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-01 ST-02)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

Formal Class 2 API contract for Alpaca US market data integration. All DS-05 Alpaca endpoints documented with request/response schemas. Fallback strategy explicitly defined. DoQ sign-off obtained.

---

### BLG-SPEC-23 — Screener internal API contract
**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-01 ST-03)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

Formal API contract for internal screener API endpoints (GET /screener/results, POST /screener/run). Request/response schemas, pagination, error codes documented. OpenAPI entries added. DoQ sign-off obtained.

---

### BLG-FE-17 — Screener results page UX spec
**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-01 ST-04)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

UX specification for screener results page authored as Class 2 canonical document. Column layout, sort/filter controls, data freshness indicator, empty states, watchlist promotion flow, and progressive loading pattern all documented. DoQ sign-off obtained.

---

### BLG-GOV-16 — §13 review record for DS-06 (Alpaca News Panel)
**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-03 ST-08)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

Formal §13 review record created for DS-06. DS-06 confirmed display-only Alpaca news context; not a sentiment signal or automated advisory. Strategy Rules owner sign-off recorded.

---

### BLG-QA-08 — External API mock harness for CI
**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-03 ST-09)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

Mock harness operational in CI for Alpaca Markets API and Yahoo Finance API. Screener CI tests pass deterministically without live API calls. Mock responses configurable per test scenario. DoQ sign-off obtained.

---

### BLG-QA-09 — Screener test data library
**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-03 ST-10)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

Synthetic ticker test data library created with minimum 10 synthetic tickers covering key screener filter scenarios. Edge cases documented: passes all filters, fails regime gate, fails ATR threshold, fails signal threshold. DoQ sign-off obtained.

---

### BLG-GOV-14 — execution_prompt.md §3.2 governance patches (2 deferred from v2.8)
**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-04 ST-11)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

Two governance patches applied to execution_prompt.md: §3.2.A reclassification note (delegated_frontend→autonomous with frontend-visible changes requires DoQ counter-sign at STEP 5); §3.2 DoQ EPIC template updated (EPIC-level consolidation block required when story-level authority is domain-specific). §6 CLAUDE.md checklist applied. Head of Specs Team sign-off obtained.

---

### BLG-GOV-15 — execution_prompt.md STEP 5.1.B capability count cross-check
**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-04 ST-12)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

STEP 5.1.B advisory inserted in execution_prompt.md after existing QA Evidence File Existence Check. Advisory instructs verification of System_status_report.md SC-* scenario counts before writing Sprint_Complete. §6 CLAUDE.md checklist applied. Head of Specs Team sign-off obtained.

---

### BLG-FE-15 — SystemStatus.js: add `/ai` prefix to `categorizeEndpoint()`
**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-04 ST-13)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

`/ai` prefix case added to `categorizeEndpoint()` in `SystemStatus.js`. AI endpoints now appear in named category (not 'Other'). No regression to categorisation of existing endpoints.

---

### BLG-AI-01 — AI Journal summary audit log
**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-04 ST-14)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

Persistent AI audit log implemented (ai_audit_service.py). Every summary run persisted with required fields (timestamp, trade_ids, model version, output hash). Log queryable by trade_id and date range. DoQ sign-off obtained.

---

### TEST-GAP-EPIC-04 — AI Journal Summarisation test scenario coverage
**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-04 ST-15)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

`docs/testing/ai_scenarios.md` created with 4 scenarios: AI summary happy path, graceful LLM failure, collapsed-by-default frontend, disclaimer always visible. All scenarios reference ai_endpoints.md and trade_history.md v1.7. TSG-v28-01 resolved. DoQ sign-off obtained.

---

### BLG-GOV-08 — Engine prompt compression: roadmap_prompt and release_planning_prompt
**Status at retirement:** ❌ Killed — 5 consecutive deferrals; retirement decision v2.9 groom
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-24
**Decision authority:** PMO Lead + Head of Specs Team (per closure_record.md §5 item 4)
**Decision rationale:** 5 consecutive deferrals (v2.3→v2.4→v2.5→v2.6/v2.7→v2.8→v2.9); L effort (~3–5 days); prompts functional and governed — compression value does not justify cost given ongoing arc delivery cadence. Deferred to P3 permanent backlog (initiative_register.md Priority 3 or organic improvement) rather than active backlog tracking.

Engine prompt compression was identified as a governance improvement in AUD-2026-03-21. With v2.9 Arc 1 delivery complete and v3.0 Arc 1 remainder on the roadmap, the active backlog should not carry an L-effort low-priority item that has been consistently displaced by higher-value work across 5 cycles.


---

## Archived — Post-ship Closure v3.2 (2026-05-09)

---

### BLG-FE-16 — React component inventory
**Status:** ✅ COMPLETE v3.2
**Archived:** 2026-05-09 (post-ship closure groom backlog STEP 12)
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

### BLG-FE-21 — Design system document
**Status:** ✅ COMPLETE v3.2
**Archived:** 2026-05-09 (post-ship closure groom backlog STEP 12)
**Priority:** P3 (Low)
**Type:** Frontend / Documentation
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-head-of-ux-20260321-02 — promoted cycle 2026-05-05__scheduled (DL-024)
**Effort:** M (~1–2 days)
**Provisional-Target:** v3.2

**Problem**
The system UI has accumulated organically across 17 releases. Arc 1 added significant new components (screener results, watchlist promotion, news panel). Arc 2 will add more (pre-trade research view, trade plan form, entry checklist). Without a documented design system, each new UI surface risks inconsistent patterns because the single developer is not consistent across sessions separated by weeks.

**Scope**
- Document the implicit design system: colour palette, typography scale, spacing tokens, icon conventions
- Reference document for use when adding new UI surfaces in Arc 2+
- Capture current patterns as-is (not aspirational); note any existing inconsistencies
- Coordinate with BLG-FE-16 (React component inventory) — sequence BLG-FE-16 first if both in-scope

**Acceptance Criteria**
- Design system document created covering colour palette, typography, spacing, icon conventions
- Each pattern entry includes current usage and any known inconsistencies
- Usable as a reference when starting new Arc 2 UI surfaces

---

### BLG-SEC-05 — Alpaca API key rotation policy and credential audit
**Status:** ✅ COMPLETE v3.2
**Archived:** 2026-05-09 (post-ship closure groom backlog STEP 12)
**Priority:** P2 (Medium)
**Type:** Security / Operations
**Owner:** Cybersecurity & Trust Lead
**Source:** IDEA-cybersecurity-20260421-01 + IDEA-cybersecurity-20260421-02 — promoted cycle 2026-05-05__scheduled (DL-024)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v3.2

**Problem**
Alpaca API key is in production (stored in Render environment variables) with no documented rotation policy — no specification of rotation frequency, rotation procedure, validation after rotation, or incident response if key is compromised. Additionally, multiple API credentials are now in production (Alpaca, Anthropic/Claude) with no inventory documenting storage location, last rotation, or system dependencies.

**Scope**
- Credential inventory: document all production API credentials (Alpaca, Anthropic, others), storage location, last rotation date, system dependencies
- Rotation policy: rotation frequency guidance, step-by-step rotation procedure for Alpaca key, validation procedure after rotation
- Incident response note: what to do if a credential is compromised
- Not a compliance document — procedural memory for the developer

**Acceptance Criteria**
- Credential inventory lists all production API credentials with storage location and last rotation
- Rotation policy documented with step-by-step procedure for Alpaca key rotation
- Validation procedure after rotation specified
- Incident response steps documented (rotate, validate, check audit logs)

---

### BLG-GOV-18 — External API dependency risk register
**Status:** ✅ COMPLETE v3.2
**Archived:** 2026-05-09 (post-ship closure groom backlog STEP 12)
**Priority:** P3 (Low)
**Type:** Governance Process / Operational Risk
**Owner:** PMO Lead + Infrastructure & Operations Owner
**Source:** IDEA-pmo-lead-20260421-01 — promoted cycle 2026-05-05__scheduled (DL-024)
**Effort:** S (~0.5 day)
**Provisional-Target:** v3.2

**Problem**
Alpaca Markets API is now production-critical — the screener engine depends on it for daily OHLCV bars. Yahoo Finance is also in the data pipeline. No formal register tracks which endpoints are used, reliability record, known failure modes, fallback status, or SLA concerns. GET /health provides real-time health but not risk assessment or response planning.

**Scope**
- Lightweight register documenting each external API dependency (Alpaca, Yahoo Finance, Anthropic Claude)
- Per dependency: endpoints used, reliability record, fallback status, API tier/plan, renewal/rotation requirements
- Register surfaced at each roadmap rebalance for operational awareness
- Not an incident response playbook — a risk inventory

**Acceptance Criteria**
- Register created covering all production external API dependencies
- Each entry includes: endpoints used, current status, known failure modes, fallback behaviour, renewal/tier info
- Register referenced in run_manifest.md template for future rebalances

---

### BLG-GOV-11 — Cycle artefact inventory and maintenance review
**Status:** ✅ COMPLETE v3.2
**Archived:** 2026-05-09 (post-ship closure groom backlog STEP 12)
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

### BLG-FE-35 — ST-08 AC-02: Human staging sign-off for Research page font conformance
**Archived:** 2026-05-18
**Completed in:** v3.7 (EPIC-04, ST-10)
**Resolution:** Human staging run performed 2026-05-18 by Head of UX & Design — Research page typography confirmed conformant against design_system.md. Playwright test `tests/e2e/research-typography.spec.js` (SC-RV-TYP-01) added for permanent CI regression coverage. BLG-FE-26 was already archived 2026-05-17.

---

### BLG-TECH-10 — Fix Yahoo Finance crumb/401 rate-limiting in screener batch
**Archived:** 2026-05-22
**Completed in:** v3.9 (EPIC-01, ST-01)
**Resolution:** Crumb refresh logic implemented; exponential backoff with jitter on 401/429; concurrent request cap via environment variable; crumb refresh events logged. All AC met. P3 process notation: AC-04 integration test deferred to staging (BLG-QA-24).

---

### BLG-BE-10 — Fix sector/industry data dropped in screener batch
**Archived:** 2026-05-22
**Completed in:** v3.9 (EPIC-01, ST-02)
**Resolution:** Full ticker dict (including sector/industry) retained and passed to compute_screener_result(). Screener results now persist non-null sector/industry. Unit test verifies propagation.

---

### BLG-BE-11 — Remove DAY from ticker universe (invalid Yahoo Finance symbol)
**Archived:** 2026-05-22
**Completed in:** v3.9 (EPIC-01, ST-03)
**Resolution:** DAY removed from tickers_full_list.csv; deactivate_invalid_tickers() added to startup; PHNX.L retained as valid FTSE 250 ticker (Phoenix Group Holdings). No OHLCV FAILED for DAY log entries post-deploy.

---

### BLG-FE-38 — Add degraded-run warning to screener when OHLCV failure rate exceeds 20%
**Archived:** 2026-05-22
**Completed in:** v3.9 (EPIC-01, ST-04)
**Resolution:** degraded_run/failure_rate fields added to screener_runs table and GET /screener/results response; DegradedRunBanner component shows amber warning with failure_rate percentage; SC-SCR-DEG-01/02 Playwright pass.

---

### BLG-FE-37 — Strip .L suffix from Ticker Universe page display labels
**Archived:** 2026-05-22
**Completed in:** v3.9 (EPIC-02, ST-05)
**Resolution:** displayTicker() function strips .L from display labels; API requests (add/toggle/delete) still use full ticker; US tickers unaffected. SC-TU-DISP-01 Playwright pass.

---

### BLG-BE-12 — Add company_name column to ticker universe
**Archived:** 2026-05-22
**Completed in:** v3.9 (EPIC-02, ST-06)
**Resolution:** ensure_company_name_column() adds TEXT column; backfill from tickers_full_list.csv on startup; company_name included in GET /ticker-universe response; management page displays company name as 2nd column. SC-TU-COMP-01 Playwright pass.

---

### BLG-GOV-25 — Add --dry-run support to plan release and run delivery verification engines
**Archived:** 2026-05-22
**Completed in:** v3.9 (EPIC-04, ST-11)
**Resolution:** --dry-run flag added to release_planning_prompt.md v2.31 and delivery_verification_prompt.md v2.5; two rows added to shared_standards.md §13 dry-run table; all three files version-bumped; prompt_change_log.md entries added.


---

## v4.1 Completions — Archived 2026-05-27 (Post-Ship Cleanup)

---

### BLG-FEAT-40 — SI-05 composite compliance score formula
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Metrics Definitions & Analytics Owner
**Source:** IDEA-metrics-analytics-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Problem**
SI-05 (Weekly Strategy Integrity Digest) will surface a compliance score trend. No formal definition exists for the composite compliance score formula — what it includes, how it is weighted, and what denominator it uses. Without a pre-defined formula, the SI-05 sprint will produce an ad-hoc metric that cannot be referenced in the monthly P&L report (BLG-FEAT-38) or tracked for trend.

**Scope**
- Define composite compliance score: formula, components (validation pass rate, override rate, red flag event rate), weighting rationale
- Document in metrics_definitions.md
- Input to SI-05 sprint planning and BLG-FEAT-38 P&L integration

**Acceptance Criteria**
- Formula defined and documented in metrics_definitions.md
- Components and weightings explained with rationale
- Reviewed by Strategy Rules & System Intent Owner before SI-05 sprint planning

---

---

### BLG-FEAT-42 — Arc 5 compliance metrics monthly P&L report integration
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P2 (Medium)
**Type:** Product Feature / Reporting
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** M (~2 days)
**Provisional-Target:** v4.1

**Problem**
BLG-FEAT-38 (Arc 5 compliance score in P&L report) has its gate cleared as of rebalance 2026-05-25. BLG-FEAT-42 is the implementation spec and integration work to add the compliance metrics section to the monthly P&L report using the Arc5ComplianceSection data already available from the v4.0 analytics endpoint. A separate implementation item is warranted because BLG-FEAT-38 defines what should appear; BLG-FEAT-42 defines how to integrate it into the existing report infrastructure.

**Scope**
- Add Arc 5 compliance summary section to monthly P&L report output
- Source data from GET /analytics/arc5-compliance endpoint (shipped v4.0)
- Fields: validation_pass_rate_by_rule (top 3 rules), override_rate, events_per_week, top_rule_breach
- Requires BLG-FEAT-38 (gate cleared) and BLG-FEAT-40 (composite score formula) as preconditions before sprint

**Acceptance Criteria**
- Monthly P&L report includes Arc 5 compliance summary section
- Data sourced from GET /analytics/arc5-compliance
- Composite score formula (BLG-FEAT-40) applied if defined; else individual components only
- Reviewed by Financial Reporting & Records Owner and Product Owner before sprint planning

---

---

### BLG-FE-44 — Research view: surface signal_type as Setup Type column
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P3 (Low)
**Type:** Frontend / Backend
**Owner:** Head of Engineering; Head of UX & Design
**Source:** v4.0 sprint execution — out-of-scope change stashed and deferred
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
The Research page signal card shows Current Price, Signal, Status, ATR, and Entry Price but does not surface `signal_type` (e.g. "strong_momentum", "momentum"). This field is already in the signals table and available in `GET /research/{ticker}` response. Adding it gives traders immediate context on setup quality without navigating away.

**Scope**
- `backend/routers/research.py`: include `signal_type` in `_get_signal()` response dict (1-line change)
- `src/pages/Research.js`: add `SetupTypeBadge` component; add 5th column to Price & Signal grid showing setup type with colour-coded badge (violet for strong_momentum, cyan for momentum)
- No new endpoint, no schema change, no migration required

**Acceptance Criteria**
- AC-01: `GET /research/{ticker}` response includes `signal_type` field
- AC-02: Research page Price & Signal section shows Setup Type badge alongside ATR and Entry Price
- AC-03: strong_momentum → violet badge; momentum → cyan badge; null → dash

---

---

### BLG-FE-48 — Arc5ComplianceSection frontend spec
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Frontend / Spec
**Owner:** Frontend Specs & UX Documentation Owner
**Source:** IDEA-frontend-ux-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~1 day)
**Provisional-Target:** v4.1

**Problem**
Arc5ComplianceSection.js shipped v4.0 without a formal frontend spec. The component was implemented from acceptance criteria. A retrospective spec document is needed for: (a) future maintenance reference, (b) input to BLG-FE-45 expandability review, (c) Arc 6 extension planning.

**Scope**
- Produce frontend component spec for Arc5ComplianceSection.js
- Cover: data contract (from GET /analytics/arc5-compliance), component props, display states (loading, empty, populated), responsive layout, test coverage (SC-AC5-xx)
- Reviewed by Head of UX & Design and Product Owner

**Acceptance Criteria**
- Frontend spec filed in docs/specs/frontend/ (or equivalent)
- Data contract documented against current openapi.yaml endpoint
- Reviewed and accepted by Head of UX & Design

---

---

### BLG-OPS-29 — Add v4.0 new endpoints to api_performance_baseline.md re-run
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** Post-ship closure 2026-05-22__release-v4.0 — endpoint coverage drift check
**Effort:** S (~1 day)
**Provisional-Target:** v4.1

**Problem**
`docs/ops/api_performance_baseline.md` was last updated at v2.7 (Supavisor re-run). v4.0 introduced two new endpoints not present in the baseline: GET /analytics/arc5-compliance (ST-01) and POST /trade-plans/{plan_id}/generate-thesis (ST-12). These endpoints have no p50/p95 measurement, no HTTP status expectation, and no ⚠️ flag threshold. Additional endpoints added since v2.7 may also be absent.

**Scope**
- Run api_performance_baseline measurement against staging environment
- Include all endpoints in openapi.yaml not yet in the baseline table
- Specifically confirm GET /analytics/arc5-compliance and POST /trade-plans/{plan_id}/generate-thesis are measured
- Flag any p95 > 500ms per existing methodology
- Update docs/ops/api_performance_baseline.md version header and Last Updated date

**Acceptance Criteria**
- All openapi.yaml endpoints present in api_performance_baseline.md measurement table
- p50/p95 measurements recorded for GET /analytics/arc5-compliance and POST /trade-plans/{plan_id}/generate-thesis
- Document version bumped and Last Updated set to run date

---

*BLG-OPS-16 (Remove tracked backend/__pycache__ files from git + .gitignore) — ✅ COMPLETE v3.7 — ST-10, cycle: 2026-05-18__release-v3.7*

---

---

### BLG-OPS-30 — Gemini API usage first monthly review
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Operations / Cost Management
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IDEA-finops-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
Gemini Flash API (shipped v4.0, ST-12) is now live for thesis generation. BLG-OPS-26 (Gemini API cost tracking) was added in IW-20260522-01. The first monthly review should be conducted ~30 days after v4.0 ship to: verify gemini_audit_log is populating correctly, review actual token consumption and cost, and set a monthly review cadence going forward.

**Scope**
- Run first monthly review of gemini_audit_log: request count, total tokens, estimated cost
- Verify cost tracking accuracy against Gemini API billing dashboard
- Establish review cadence (monthly scheduled review added to governance calendar)
- Document findings in a brief ops note

**Acceptance Criteria**
- gemini_audit_log reviewed: data integrity confirmed
- Cost estimate produced for first 30 days
- Monthly review cadence established and documented
- Findings reviewed by FinOps & Resource Architect

---

---

### BLG-OPS-32 — Trade plan P&L attribution gate check
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P2 (Medium)
**Type:** Operations / Data Quality
**Owner:** Financial Reporting & Records Owner; Infrastructure & Operations Owner
**Source:** IDEA-financial-reporting-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
Monthly P&L reports attribute P&L to closed trades. Trade plans (Arc 2, shipped v3.1) link to positions at entry. Verifying that P&L attribution correctly reflects which positions had trade plans (vs. pre-Arc-2 positions without plans) is a data quality gate check before BLG-FEAT-38 (Arc 5 compliance metrics in P&L) and BLG-FEAT-42 can produce accurate compliance-linked P&L analysis.

**Scope**
- Query: trades with plan_id vs. trades without plan_id in closed trade history
- Confirm P&L report handles both cases correctly (plan-linked vs. legacy trades)
- Flag any attribution anomalies for remediation before compliance integration

**Acceptance Criteria**
- Plan-linked vs. non-plan trade count confirmed
- P&L attribution verified accurate for both trade types
- Any anomalies documented and flagged to Product Owner

---

---

### BLG-OPS-34 — Gemini API daily cost threshold alert via Telegram
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P2 (Medium)
**Type:** Operations / Cost Monitoring
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IDEA-finops-20260525-02 — Promoted-Backlog (STEP 5 debate, modified scope) cycle 2026-05-25__scheduled (DL-034)
**Effort:** M (~2–3 days)
**Provisional-Target:** v4.1

**Problem**
Gemini thesis generation (shipped v4.0) incurs per-request API costs. Currently there is no automated alert if Gemini API spend exceeds a daily threshold. BLG-OPS-26 provides manual monthly cost review; BLG-OPS-34 provides automated daily threshold monitoring using the existing Telegram notification infrastructure (shipped v2.4).

**Scope**
- Configurable daily Gemini spend threshold (default: $1.00/day)
- Daily check of gemini_audit_log: sum estimated_cost_usd for current day
- If threshold exceeded: send Telegram alert with daily total and request count
- No new UI — Telegram notification only (existing infrastructure)

**Acceptance Criteria**
- Daily threshold check implemented (scheduled task or startup check)
- Telegram alert fires when daily spend exceeds configurable threshold
- Threshold configurable via env var
- Test coverage: unit test for threshold logic; staging verification

---

---

### BLG-SPEC-33 — SI-03 Red Flag Journal API contract document
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Spec Debt
**Owner:** API Contracts Documentation Owner
**Source:** IDEA-api-contracts-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0

**Problem**
`GET /portfolio/red-flag-journal` shipped v3.9 (SI-03) without a formal API contract document in `docs/specs/api_contracts/`. SI-04 and SI-05 will extend or reference the Red Flag Journal endpoint; without a contract, downstream implementations lack an authoritative spec for filter parameters, pagination schema, response structure, and error codes.

**Scope**
- Author `docs/specs/api_contracts/red_flag_journal.md`
- Document: endpoint URL, HTTP method, authentication requirement, query parameters (date range, event type, severity when BLG-BE-16 ships), pagination schema, response fields, error codes
- Register in `docs/reference/openapi.yaml` per CLAUDE.md §2
- Use `## METHOD /path` heading format per CLAUDE.md §2

**Acceptance Criteria**
- API contract document produced and filed
- Contract registered in openapi.yaml with correct heading format
- All filter parameters and response fields documented
- Reviewed by Head of Specs Team and API Contracts Documentation Owner

---

---

### BLG-SPEC-34 — SI-01 Pre-Entry Validation API contract document
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Spec Debt
**Owner:** API Contracts Documentation Owner
**Source:** IDEA-api-contracts-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0

**Problem**
`GET /portfolio/pre-entry-validation` shipped v3.8 (SI-01) without a formal API contract document. SI-02 and SI-05 will reference the validation rule taxonomy and response schema; without a contract, there is no authoritative source for rule enumeration, response structure, or override acknowledgement path.

**Scope**
- Author `docs/specs/api_contracts/pre_entry_validation.md`
- Document: endpoint URL, HTTP method, query parameters, response fields (per-rule pass/fail, override_required), override acknowledgement path, error codes
- Enumerate all 5 validation rules per strategy_rules.md v1.4 §4.2
- Register in `docs/reference/openapi.yaml`

**Acceptance Criteria**
- API contract document produced and filed
- All 5 validation rules documented with pass/fail conditions
- Override acknowledgement path specified
- Contract registered in openapi.yaml
- Reviewed by Head of Specs Team

---

---

### BLG-SPEC-38 — Gemini thesis endpoint API contract
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Spec Debt / API Contract
**Owner:** API Contracts Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~1 day)
**Provisional-Target:** v4.1

**Gate criteria:** BLG-SPEC-33 (SI-03 Red Flag Journal API contract) closed — Gemini thesis endpoint contract follows SI-03 contract closure to ensure consistent contract format.

**Problem**
POST /trade-plans/{plan_id}/generate-thesis (shipped v4.0, ST-12) has no formal API contract document in docs/specs/api_contracts/. BLG-GOV-55 (API contract same-sprint delivery rule) will prevent future recurrence; BLG-SPEC-38 addresses the existing debt from v4.0. Additionally: CLAUDE.md §2 requires every new API endpoint to be added to openapi.yaml in the same commit as the contract — this item will verify the v4.0 openapi.yaml entry is complete.

**Scope**
- Write formal API contract document for POST /trade-plans/{plan_id}/generate-thesis
- Cover: request schema (plan_id path param), response schema ({thesis, model_version, prompt_version}), error cases (missing key, invalid plan_id, Gemini error)
- Verify corresponding openapi.yaml entry is complete and at ## level
- Filed in docs/specs/api_contracts/

**Acceptance Criteria**
- API contract document produced at docs/specs/api_contracts/
- Endpoint heading at ## level (OpenAPI drift gate compliant)
- openapi.yaml entry verified complete
- Reviewed by API Contracts Documentation Owner and Head of Specs Team
- Gate condition (BLG-SPEC-33 closed) verified before commencing

---

---

### BLG-SPEC-39 — SI-02 data model gap analysis
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Spec / Data Model
**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Source:** IDEA-data-model-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** M (~1–2 days)
**Provisional-Target:** v4.1

**Problem**
SI-02 (Behavioural Drift Detection) requires comparing actual trade entries against stated setup criteria — specifically: regime_at_entry, signal_type, setup_type, and entry_proximity fields. BLG-SPEC-37 defined the schema pre-definition approach (gate-conditional on sprint planning). BLG-SPEC-39 is a standalone gap analysis that can be done now to identify which fields are missing from the current trade/position data model, enabling proactive planning before SI-02 sprint planning is triggered.

**Scope**
- Review current trade, position, and trade_plan schemas for fields required by SI-02
- Identify missing fields with: data type, source (captured at entry? derivable? new collection?), migration complexity
- Output: gap analysis document for input to SI-02 sprint planning
- Complements BLG-SPEC-37 (gate-conditional version); this item proceeds without gate constraint

**Acceptance Criteria**
- Gap analysis document produced
- Missing fields enumerated with type and migration estimate
- Reviewed by Data Model & Domain Schema Owner, Head of Specs Team, and Head of Backend Engineering before SI-02 sprint planning

---

---

### BLG-SPEC-40 — Arc 5 analytics endpoint API contract
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Spec Debt / API Contract
**Owner:** API Contracts Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~1 day)
**Provisional-Target:** v4.1

**Problem**
GET /analytics/arc5-compliance (shipped v4.0, ST-01) has no formal API contract document in docs/specs/api_contracts/. The endpoint was implemented from acceptance criteria. A formal contract document enables: frontend spec alignment (BLG-FE-48), future Arc 6 extension planning (BLG-BE-21), and compliance with CLAUDE.md §2 API contract requirements.

**Scope**
- Write formal API contract document for GET /analytics/arc5-compliance
- Cover: response schema (validation_pass_rate_by_rule, events_per_week, override_rate, top_rule_breach, trade_plan_adherence_rate), query params (if any), error cases
- Verify openapi.yaml entry is complete and at ## level
- Filed in docs/specs/api_contracts/

**Acceptance Criteria**
- API contract document produced at docs/specs/api_contracts/
- Endpoint heading at ## level
- openapi.yaml entry verified complete
- Reviewed by API Contracts Documentation Owner and Head of Specs Team

---

---

### BLG-GOV-44 — SI-02 §13 review evidence criteria pre-definition
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Governance / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner; Head of Specs Team
**Source:** IDEA-strategy-owner-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
BLG-GOV-39 (SI-02 §13 formal boundary review, gate-conditional on sprint planning imminent) was added in IW-20260522-01. BLG-GOV-44 pre-defines the evidence criteria that the §13 review for SI-02 must satisfy — what "PASS" looks like, what binding conditions are expected, and what test scenarios confirm determinism. Pre-definition before sprint planning prevents the §13 review from being conducted without a clear pass/fail framework.

**Scope**
- Define §13 review evidence criteria for SI-02: what assertions must be verifiable (determinism, display-only output, no adaptive learning, no automated action)
- Document expected binding conditions (e.g., "drift alerts informational only; no automated position management")
- Input to BLG-GOV-39 when gate clears

**Acceptance Criteria**
- Evidence criteria document produced
- Reviewed by Strategy Rules & System Intent Owner
- Document filed for reference when BLG-GOV-39 gate triggers

---

---

### BLG-GOV-46 — SI-02 data prerequisite audit
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Governance / Release Gate
**Owner:** Challenger; Product Owner
**Source:** IDEA-challenger-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
SI-02 (Behavioural Drift Detection) requires trade history with regime_at_entry, setup_type, and signal_conditions captured. These fields may not be present on all historical trades. Before sprint planning, the Challenger's mandatory data prerequisite audit confirms: how many trades have complete data, whether the sample is sufficient for meaningful drift analysis, and whether any data backfill is required as a pre-sprint story.

**Scope**
- Query trade history: count trades with regime_at_entry, setup_type, and plan_id present
- Assess: is the sample sufficient for drift analysis? (target: 10+ trades with complete data)
- If insufficient: identify backfill options or document that drift analysis will have limited early utility
- Findings reviewed by Product Owner before SI-02 sprint planning

**Acceptance Criteria**
- Audit query run and results documented
- Sufficiency assessment produced
- Product Owner informed; sprint planning decision documented

---

---

### BLG-GOV-49 — Gemini API key scope minimization review
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Governance / Security
**Owner:** Cybersecurity & Trust Lead
**Source:** IDEA-cybersecurity-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
GEMINI_API_KEY (shipped v4.0) is used for thesis generation via the generative AI API. The key scope (what the key can access on the Google AI platform) should be reviewed to confirm it is minimally scoped: text generation only, no other Google API access, rate-limited where possible. Key scope minimization is a security hygiene requirement for any external AI API credential.

**Scope**
- Review GEMINI_API_KEY scope on Google AI platform
- Confirm: restricted to generative AI text generation only
- Confirm: key is not shared with other Google services
- Document findings in security review note

**Acceptance Criteria**
- Key scope confirmed (or remediation action filed if overly permissive)
- Findings documented in docs/security/
- Reviewed by Cybersecurity & Trust Lead

---

---

### BLG-GOV-51 — SI-02 database query performance pre-assessment
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P2 (Medium)
**Type:** Governance / Performance Pre-work
**Owner:** Head of Engineering; Head of Backend Engineering
**Source:** IDEA-head-of-engineering-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~1 day)
**Provisional-Target:** v4.1

**Problem**
SI-02 (Behavioural Drift Detection) involves rolling analysis across trade history. Depending on the query design, this could be computationally expensive on a Supabase PostgreSQL instance with 50+ trades. A pre-assessment of expected query patterns against the current data model confirms whether any performance concerns exist before sprint planning, preventing mid-sprint performance surprises.

**Scope**
- Profile expected SI-02 query patterns against current trade/position schema
- Estimate query complexity for typical dataset size (20–100 trades)
- Identify: any full-table scans, missing indexes, or aggregate patterns requiring optimisation
- Input to BLG-BE-20 (background job architecture) and SI-02 sprint planning

**Acceptance Criteria**
- Query patterns profiled (may be desk analysis, not live benchmark)
- Performance concerns (if any) documented with severity estimate
- Findings reviewed by Head of Engineering and Head of Backend Engineering before SI-02 sprint planning

---

---

### BLG-GOV-54 — SI-05 Phase 1 scope annotation — Red Flag + compliance trend delivery
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P2 (Medium)
**Type:** Governance / Roadmap Annotation
**Owner:** Product Owner; Head of Specs Team
**Source:** IDEA-product-owner-20260525-01 — Promoted-Backlog (STEP 5 debate) cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
SI-05 (Weekly Strategy Integrity Digest) depends on SI-02 for its drift signal component. SI-02 may not ship until v4.2+. To avoid blocking all of SI-05, this item formalises a phased delivery approach: Phase 1 (Red Flag Journal summary + compliance score trend via Telegram, no SI-02 component) can ship as soon as SI-03 and Arc5ComplianceSection are live (both shipped v4.0). Phase 2 (drift signal integration) ships when SI-02 is complete.

**Scope**
- Annotate SI-05 on current_roadmap.md with phased delivery note
- Create SI-05 Phase 2 follow-on backlog item (separate BLG, filed at sprint planning time)
- Update relevant specs/acceptance criteria to reflect Phase 1 scope
- Phase 1 scope: weekly Telegram digest of Red Flag Journal events (count + top event type) + compliance score trend (7-day rolling validation pass rate)

**Acceptance Criteria**
- SI-05 roadmap entry annotated with phased delivery approach
- Phase 1 scope defined and documented
- Phase 2 follow-on scope identified (to be filed as a backlog item at v4.1 sprint planning)
- Product Owner sign-off on Phase 1 scope definition

---

---

### BLG-GOV-56 — STEP 12.1 artefact presence check
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P2 (Medium)
**Type:** Governance / Prompt Engineering
**Owner:** Head of Specs Team; PMO Lead
**Source:** IDEA-pmo-lead-20260525-02 — Promoted-Backlog (STEP 5 debate, modified scope) cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
STEP 12.1 of governance engines updates .claude_current_state.json regardless of whether required cycle artefacts exist on disk. A cycle can be marked complete in state even if run_manifest.md, cycle_summary.md, or lessons_learnt.md were never written. Adding an artefact presence check produces a visible warning in STEP 12.1 output for missing artefacts, with a soft halt only for required Class-3 Operational Records.

**Scope**
- Add artefact presence check to STEP 12.1 of roadmap_prompt.md, sprint_planning_prompt.md, delivery_verification_prompt.md, and post_ship_closure.md
- Advisory warning output for missing non-required artefacts
- Soft halt (STEP 12.1 completes but records a governance warning in state) if required Class-3 Operational Record (run_manifest.md, sprint_goal.md) is absent
- Per CLAUDE.md §6 governance file edit checklist: bump version, update OPERATIONAL_GUIDE.md §14, append prompt_change_log.md for each affected prompt

**Acceptance Criteria**
- Artefact presence check added to STEP 12.1 of all four prompt files
- Prompt versions bumped; OPERATIONAL_GUIDE.md §14 updated; prompt_change_log.md appended
- Soft halt condition: absent required Class-3 record produces governance warning in state file
- False-halt risk addressed: check uses canonical artefact paths only (not temp/worktree paths)

---

---

## v3.7/v3.9 Completions — Archived 2026-05-27 (Backlog Cleanup)

*BLG-TECH-10 (Fix Yahoo Finance crumb/401 rate-limiting in screener batch) — ✅ COMPLETE v3.9 — ST-01, cycle: 2026-05-21__release-v3.9*
*BLG-FE-34 (Trade plan form signal context panel — SignalContextPanel.js with entry_rationale/confirmation pre-population) — ✅ COMPLETE v3.7 — ST-03, cycle: 2026-05-18__release-v3.7*
*BLG-FE-33 (Signals page Add to Watchlist CTA — watchlisted status backend + SignalCard CTA replacement) — ✅ COMPLETE v3.7 — ST-01 + ST-02, cycle: 2026-05-18__release-v3.7*
*BLG-FE-37 (Strip .L suffix from Ticker Universe page display labels) — ✅ COMPLETE v3.9 — ST-05, cycle: 2026-05-21__release-v3.9*
*BLG-FE-38 (Add degraded-run warning to screener when OHLCV failure rate exceeds 20%) — ✅ COMPLETE v3.9 — ST-04, cycle: 2026-05-21__release-v3.9*
*BLG-BE-10 (Fix sector/industry data dropped in screener batch) — ✅ COMPLETE v3.9 — ST-02, cycle: 2026-05-21__release-v3.9*
*BLG-BE-11 (Remove DAY from ticker universe — invalid Yahoo Finance symbol) — ✅ COMPLETE v3.9 — ST-03, cycle: 2026-05-21__release-v3.9*
*BLG-BE-12 (Add company_name column to ticker universe) — ✅ COMPLETE v3.9 — ST-06, cycle: 2026-05-21__release-v3.9*
*BLG-QA-20 (Consolidate database stub files into shared pytest conftest fixture — session-scoped stub) — ✅ COMPLETE v3.7 — ST-09, cycle: 2026-05-18__release-v3.7*
*BLG-OPS-16 (Remove tracked backend/__pycache__ files from git + .gitignore) — ✅ COMPLETE v3.7 — ST-10, cycle: 2026-05-18__release-v3.7*
*BLG-GOV-23 (scored_initiatives.md Arc 3–6 comprehensive refresh — OA-RP-05 resolved) — ✅ COMPLETE v3.7 — ST-11, cycle: 2026-05-18__release-v3.7*
*BLG-GOV-25 (Add --dry-run support to plan release and run delivery verification engines) — ✅ COMPLETE v3.9 — ST-11, cycle: 2026-05-21__release-v3.9*


---

## v4.0 Completions — Archived 2026-05-27 (Post-Ship Cleanup)

---

### BLG-FEAT-36 — SI-01 validation pass/fail rate by rule
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** IDEA-metrics-analytics-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~2–3 days)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-01 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
GET /portfolio/pre-entry-validation (SI-01, shipped v3.8) returns per-attempt pass/fail results but no aggregate metric tracks pass/fail rate broken down by individual rule type over time. Understanding which rules most frequently block entries reveals behavioural patterns (e.g., "regime gate fails 40% of the time") without requiring SI-02 (drift detection).

**Scope**
- Define named metric: validation_pass_rate_by_rule — pass count / (pass + fail count) per rule per rolling period
- Backend: query pre-entry validation log for rule-level pass/fail aggregation
- Frontend: surface metric in SI-05 Weekly Digest or standalone compliance dashboard
- Requires confirmation that the pre-entry validation log captures per-rule outcomes (may require minor schema addition)

**Acceptance Criteria**
- Pass/fail rate per rule computable and displayable
- Rolling period configurable (7d / 30d)
- Backend analysis of current log schema completed before sprint planning

---

---

### BLG-FEAT-37 — Red flag event frequency metric
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** IDEA-metrics-analytics-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-02 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
No canonical metric tracks red flag event frequency over time. Override rate and rule-breach-by-type distribution are queryable from red_flag_events (shipped v3.9) but not defined as named product metrics with specified aggregation periods and display locations. Defining these metrics makes them inputs to SI-05 Weekly Digest and the monthly P&L compliance section.

**Scope**
- Named metrics: events_per_week, override_rate (overrides / validation attempts), event_type_distribution
- Backend: aggregate query on red_flag_events table
- Metric definitions registered in metrics_definitions.md

**Acceptance Criteria**
- Three named metrics defined and queryable
- Metrics definitions registered per canonical standards
- Data available for SI-05 and BLG-FEAT-38 (monthly P&L compliance section) consumption

---

---

### BLG-FEAT-39 — Trade plan adherence rate metric
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-04 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Gate criteria:** plan_id linkage actively captured on closed trades (requires active use of trade plan creation workflow).

**Problem**
No metric tracks what percentage of closed trades have an associated trade plan (plan_id linkage). This metric measures systematic discipline adoption — whether the operator is consistently using trade plans before entry. It is a direct input to Arc 4 PO-04 (reflection/outcome correlation) and a candidate for the compliance section of the monthly P&L report.

**Scope**
- Named metric: trade_plan_adherence_rate — trades_with_plan_id / total_closed_trades
- Backend: aggregate query on closed trades
- Metric definition registered in metrics_definitions.md
- Surface in performance reports and SI-05 Weekly Digest

**Acceptance Criteria**
- Metric defined and queryable
- Registered in metrics definitions
- Gate condition verified by Product Owner before sprint planning

---

---

### BLG-BE-15 — Validate ticker symbol on add (sector/industry lookup)
**Priority:** P1 (High)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering
**Source:** User request — 2026-05-22
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-05 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
When a user adds a ticker symbol and market to the universe, no validation is performed to confirm the ticker actually exists. Any arbitrary string can be saved, leading to junk entries that silently produce empty screener results or data fetch errors. Validating sector and industry at add-time gives immediate feedback and prevents invalid tickers from polluting the universe.

**Scope**
- On ticker add (POST `/tickers` or equivalent), call the market data provider (Yahoo Finance) to fetch sector and industry for the submitted symbol+market
- If the lookup returns no data or raises an error, reject the request with a clear 400/422 response and message (e.g. "Ticker XXXX not found — please check the symbol and market")
- If the lookup succeeds, optionally auto-populate sector/industry fields from the returned data
- Frontend to surface the rejection error inline on the add-ticker form

**Acceptance Criteria**
- Submitting a non-existent ticker symbol returns an error response and the ticker is not saved
- Submitting a valid ticker returns success; sector and industry are confirmed present
- Error message displayed to user is specific and actionable (not a generic 500)
- Existing tickers already in the universe are unaffected

---

---

### BLG-BE-19 — Base Gemini Flash API wiring — thesis generation service + endpoint
**Priority:** P1 (High)
**Type:** Backend Engineering / Frontend
**Owner:** Head of Backend Engineering
**Source:** Session observation 2026-05-22 — BLG-FEAT-24 marked complete v3.8 but Gemini not wired into codebase; prerequisite for BLG-GOV-35 and BLG-OPS-26
**Effort:** S (~1 day)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-12 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
BLG-FEAT-24 (AI thesis generation) was marked complete in v3.8 but no Gemini code exists in the codebase — no `google-generativeai` dependency, no env var, no service, no endpoint. BLG-GOV-35 (Gemini audit trail) and BLG-OPS-26 (cost tracking) both instrument Gemini API calls; they have nothing to build on until the base wiring exists. This is a blocking prerequisite for both v4.0 EPIC-03 Sprint 2 stories.

**Scope**
- Add `google-generativeai` to `backend/requirements.txt`
- Wire `GEMINI_API_KEY` env var (Render + local `.env`)
- Create `backend/services/gemini_service.py` with `generate_setup_thesis(ticker, signal_data, plan_data) -> dict` using `gemini-1.5-flash`; returns `{thesis, model_version, prompt_version}` or graceful error
- Add `POST /trade-plans/{plan_id}/generate-thesis` endpoint in `backend/routers/trade_plans.py`
- Frontend: "Generate Thesis" button on TradePlan page that calls the endpoint and populates `setup_thesis` field

**Acceptance Criteria**
- `google-generativeai` present in `requirements.txt`
- `GEMINI_API_KEY` env var documented in `.env.example`
- `POST /trade-plans/{plan_id}/generate-thesis` returns `{thesis, model_version, prompt_version}` when key is set
- Returns graceful error (not 500) when `GEMINI_API_KEY` is absent
- Frontend button triggers generation and populates `setup_thesis` textarea
- New endpoint registered in `backend/routers/test.py` and `docs/reference/openapi.yaml`

---

---

### BLG-QA-25 — Red Flag Journal E2E Playwright test (SI-01→SI-03 integration path)
**Priority:** P2 (Medium)
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner; QA Lead
**Source:** IDEA-qa-testing-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-03 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
SC-RFJ-01/02/03 (v3.9) cover RFJ component-level display. The SI-01 → SI-03 integration path — where a SI-01 override event is written and subsequently appears in the Red Flag Journal — is not tested end-to-end. This integration path is the primary produce of the Arc 5 data pipeline and is critical to validate before SI-02/SI-04/SI-05 extend the event model.

**Scope**
- Playwright E2E test: navigate to a position → trigger pre-entry validation → acknowledge override → navigate to Red Flag Journal → verify override event is present with correct metadata (type, timestamp, rule breached)
- Cover: filter by event type → verify filtered results contain the override event
- Integrate into existing Playwright test suite

**Acceptance Criteria**
- Full SI-01→SI-03 integration path covered by Playwright test
- Test passes in CI
- Override event metadata (type, timestamp, rule) verified in RFJ display

---

---

### BLG-OPS-26 — Gemini API cost tracking
**Priority:** P2 (Medium)
**Type:** Operations / Cost Monitoring
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IDEA-finops-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-08 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
BLG-FEAT-24 (AI thesis generation, shipped v3.8) uses the Gemini API in production with no cost monitoring. The Gemini free tier is not unlimited; tracking monthly call volume and projected costs provides early warning of approaching tier boundaries before unexpected billing occurs.

**Scope**
- Instrument Gemini API call count per day/week (count of `generate_content` requests)
- Log call count to structured log or ops metrics table
- Monthly aggregate report: call count, projected monthly total, tier proximity
- Alert threshold: > 80% of free-tier monthly limit

**Acceptance Criteria**
- Gemini API call count logged per request
- Monthly aggregate computable
- Alert threshold defined and documented
- No change to BLG-FEAT-24 user-facing behaviour

---

---

### BLG-OPS-27 — Automated staging re-deployment on main merge
**Priority:** P2 (Medium)
**Type:** Operations / CI/CD
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-09 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
Staging environment is currently manually re-synced after each main branch merge. This introduces risk of forgotten staging updates and adds lag to delivery verification runs. Automating the staging re-deployment trigger on main merges removes the manual step and ensures staging is always current.

**Scope**
- Configure Render staging auto-deploy trigger on main branch push
- Scope: trigger only when backend or frontend source files change (not on docs/governance-only commits) to conserve free-tier build minutes
- Confirm free-tier build minute impact is acceptable
- Coordinate with BLG-OPS-25 (smoke test) which depends on this deploy hook

**Acceptance Criteria**
- Staging auto-deploys on main merge for code changes
- Documentation-only commits do not trigger a deploy
- Free-tier build minute impact assessed and documented
- BLG-OPS-25 dependency satisfied (deploy hook available for smoke test integration)

---

---

### BLG-GOV-35 — Gemini thesis generation audit trail
**Priority:** P2 (Medium)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer; Head of Backend Engineering
**Source:** IDEA-ai-compliance-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-07 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
BLG-FEAT-24 (AI thesis generation, shipped v3.8) generates AI setup thesis text using Gemini API in production. No audit trail records the model version, prompt version, or output hash per generation. As Gemini usage scales, retroactive compliance tracking becomes impossible. An audit trail should be implemented before usage volume increases.

**Scope**
- Audit trail record per generation: plan_id, model_version, prompt_version, input_hash (thesis generation request), output_hash, generated_at, user_acknowledged (bool)
- Storage: append-only table (gemini_audit_log) or structured log file
- Retention policy: minimum 90 days
- No change to user-facing BLG-FEAT-24 behaviour

**Acceptance Criteria**
- Audit log created for each Gemini thesis generation call
- Record fields present: model_version, prompt_version, input_hash, output_hash, generated_at
- Retention policy enforced (90-day minimum)
- No performance impact on thesis generation response time

---

---

### BLG-GOV-37 — Red flag endpoint authentication and PII review
**Priority:** P2 (Medium)
**Type:** Governance / Security Review
**Owner:** Cybersecurity & Trust Lead
**Source:** IDEA-cybersecurity-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-06 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
SI-03 Red Flag Journal endpoint (GET /portfolio/red-flag-journal, shipped v3.9) exposes trading strategy override events. A targeted review confirms: (1) the endpoint is protected by API key authentication (shipped v2.2), (2) response payloads do not expose PII or sensitive strategy parameters beyond event type and timestamp, (3) pagination does not leak adjacent users' data (single-user system, but confirm).

**Scope**
- Verify API key auth covers /portfolio/red-flag-journal
- Review response payload: confirm no PII, no sensitive position data, no information beyond event_type, rule_type, timestamp, severity
- Document findings in security review note filed in `docs/security/`

**Acceptance Criteria**
- Authentication confirmed (API key auth active on endpoint)
- Response payload reviewed: PII-free, no sensitive strategy data confirmed
- Review findings documented
- If gap found: remediation backlog item filed

---



## v4.2 Completions — Archived 2026-05-29 (Post-Ship Closure)

---

### BLG-BE-22 — Claude API prompt caching implementation assessment
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-10; assessment: DEFER — prefix <1,024 tokens, <10 calls/day)
**Priority:** P2 (Medium)
**Type:** Backend / Performance Optimisation
**Owner:** Head of Backend Engineering
**Source:** IDEA-backend-engineering-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** v4.2

**Problem**
Anthropic SDK supports prompt caching for large, static prompt components. The thesis generation system prompt is a fixed structure repeated on every API call. If the system prompt qualifies for caching, cache hits would reduce input token costs and latency. No assessment has been done to determine cache eligibility or expected cost reduction.

**Scope**
- Assess thesis generation prompt structure for caching eligibility (>1024 tokens, static component)
- Estimate expected cache hit rate based on call patterns
- Estimate cost reduction from caching
- Produce assessment document; input to BLG-OPS-30 cost review

**Acceptance Criteria**
- Caching eligibility assessed (yes/no with evidence)
- If eligible: expected cache hit rate and cost reduction estimated
- Assessment document produced and reviewed by Head of Engineering

---

---

### BLG-QA-37 — Claude API Playwright mock strategy definition
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-09)
**Priority:** P1 (High)
**Type:** QA / Test Infrastructure
**Owner:** QA & Testing Owner; Head of Backend Engineering
**Source:** IDEA-qa-testing-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** v4.2

**Problem**
POST /trade-plans/{plan_id}/generate-thesis now calls Claude API in production. No mock strategy has been defined for CI/Playwright tests. Without a mock, CI tests may make real API calls (incurring cost and introducing flakiness) or tests may be skipped entirely. A defined mock strategy ensures reproducible, cost-free CI test execution.

**Scope**
- Evaluate mock strategies: router-level fixture mock vs ANTHROPIC_API_KEY=mock env var vs test-mode response stub
- Select and document the preferred strategy
- Produce implementation guide for applying the strategy to existing Playwright tests for thesis generation

**Acceptance Criteria**
- Mock strategy selected and documented
- Implementation guide produced
- Reviewed by QA & Testing Owner and Head of Backend Engineering

---

---

### BLG-OPS-35 — Add v4.1 new endpoint to api_performance_baseline.md re-run
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-04; POST /ai/check-daily-cost baseline added: p50=205ms, p95=518ms)
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** Post-ship closure v4.1 — endpoint coverage drift advisory (STEP 6)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.2

**Problem**
POST /ai/check-daily-cost was added in v4.1 (ST-09) and is present in openapi.yaml but absent from api_performance_baseline.md. Performance re-runs require a live environment and human coordination — cannot be done during post-ship closure.

**Scope**
- Add POST /ai/check-daily-cost to api_performance_baseline.md measurement table with baseline timing data
- Coordinate with Infrastructure & Operations Owner for live environment timing run

**Acceptance Criteria**
- POST /ai/check-daily-cost appears in api_performance_baseline.md with at least estimated p50 latency
- Reviewed by Infrastructure & Operations Owner

---

---

### BLG-OPS-36 — Claude API usage first monthly review
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-05)
**Priority:** P1 (High)
**Type:** Operations / Cost Monitoring
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IDEA-finops-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** v4.2

**Problem**
v4.1 switched thesis generation from Gemini to Claude API. No cost monitoring is in place for Claude API usage. BLG-OPS-30 (originally Gemini cost tracking) should be updated to track Claude API costs. The first monthly review of actual Claude API call volume and cost establishes the monitoring baseline and alert threshold.

**Scope**
- Review actual Claude API call volume and cost from claude_audit_log (or equivalent) data
- Establish monitoring cadence (monthly) and cost alert threshold
- Update BLG-OPS-30 scope to reflect Claude API instead of Gemini
- Produce first monthly review report

**Acceptance Criteria**
- First monthly review report produced
- Monthly cadence and alert threshold defined
- BLG-OPS-30 scope update confirmed

---

---

### BLG-OPS-38 — Claude API log hygiene policy
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-03)
**Priority:** P2 (Medium)
**Type:** Operations / Security Hygiene
**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead
**Source:** IDEA-infra-ops-20260527-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.2

**Problem**
Render application logs for Claude API calls may inadvertently capture API keys, full prompt text, or sensitive data. No log level guidance exists for Claude API trace events. With SI-02 adding more AI-adjacent queries in future, establishing log hygiene policy pre-SI-02 is operationally prudent.

**Scope**
- Confirm Render logs do not capture ANTHROPIC_API_KEY or full prompt text
- Define log level for Claude API trace events (INFO for request metadata; DEBUG for full prompt — never in production)
- Define log retention policy pre-SI-02
- Document in ops notes

**Acceptance Criteria**
- Log hygiene policy document produced
- API key and full prompt exclusion from production logs confirmed
- Log retention policy defined

---

---

### BLG-OPS-39 — Claude API thesis generation latency baseline
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-06)
**Priority:** P2 (Medium)
**Type:** Operations / Performance Baseline
**Owner:** Head of Engineering; Infrastructure & Operations Owner
**Source:** IDEA-head-of-engineering-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** v4.2

**Problem**
POST /trade-plans/{plan_id}/generate-thesis switched from Gemini to Claude API in v4.1. No p50/p95 latency baseline exists for the Claude-backed endpoint. Without a baseline, future AI feature additions (PO-02, Arc 4) cannot be regression-tested for latency impact.

**Scope**
- Establish p50/p95 latency baseline for POST /trade-plans/{plan_id}/generate-thesis (Claude API)
- Record in api_performance_baseline.md
- Define regression threshold (e.g. p95 > 2× baseline triggers review)

**Acceptance Criteria**
- p50/p95 latency measured (minimum 10 sample calls)
- Baseline recorded in api_performance_baseline.md
- Regression threshold defined

---

---

### BLG-SPEC-42 — AI thesis endpoint contract update for Claude
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-08; ai_thesis_generation.md v2.1.0; gemini_thesis_generation.md Superseded)
**Priority:** P1 (High)
**Type:** Spec Debt / API Contract
**Owner:** API Contracts Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.2

**Problem**
docs/specs/api_contracts/ai_thesis_generation.md was authored for the Gemini-backed thesis generation endpoint. v4.1 replaced Gemini with Claude API. The response schema now returns different fields (model_id, usage.input_tokens, usage.output_tokens, cache_hit). The contract must be updated to reflect the current Claude-backed implementation and openapi.yaml updated accordingly per BLG-GOV-55 rule.

**Scope**
- Update docs/specs/api_contracts/ai_thesis_generation.md to reflect Claude API response fields
- Update openapi.yaml to match updated contract schema
- Verify all field names and types match the v4.1 implementation

**Acceptance Criteria**
- Contract document updated with Claude API response fields
- openapi.yaml updated and consistent with contract
- No drift between contract and implementation for thesis generation endpoint

---

## 8. Governance Backlog


---

---

### BLG-GOV-57 — SI-04 Strategy Version Comparison pre-planning
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-12; si04_scope_definition.md v1.0)
**Priority:** P2 (Medium)
**Type:** Governance / Pre-Sprint Planning
**Owner:** Product Owner; Head of Specs Team
**Source:** IDEA-product-owner-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** v4.2

**Problem**
SI-04 (Strategy Version Comparison) scope is not formally defined. Without pre-planning (strategy versions to compare, performance delta computation method, UI view), mid-sprint scope discovery risks will materialise. Pre-planning prevents last-minute sprint gate discovery.

**Scope**
- Define SI-04 feature scope: which strategy versions to compare, how performance delta is computed
- Define UI view: layout, data source, interaction model
- Output: SI-04 scope definition document; input to SI-04 sprint planning and BLG-GOV-62 §13 review

**Acceptance Criteria**
- SI-04 scope definition document produced
- Reviewed by Product Owner and Head of Specs Team

---

---

### BLG-GOV-59 — Backlog ID namespace integrity audit
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-13; 287 BLG IDs audited, 0 collisions)
**Priority:** P3 (Low)
**Type:** Governance / Hygiene
**Owner:** Head of Specs Team; PMO Lead
**Source:** IDEA-head-of-specs-20260527-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.2

**Problem**
With 80+ BLG items across 10 namespaces, no verification pass has been run to confirm no sequence gaps or ID collisions exist. A namespace count summary provides governance health visibility and catches any numbering errors introduced by concurrent backlog additions.

**Scope**
- Audit all BLG IDs in backlog.md and backlog_archive.md
- Verify: no sequence gaps, no ID collisions, namespace counts consistent with history
- Produce namespace count summary in run_manifest.md or cycle_record.md

**Acceptance Criteria**
- Audit complete with no gaps or collisions found (or gaps documented with explanation)
- Namespace count summary produced

---

---

### BLG-GOV-60 — SI-02 sprint planning prerequisites checklist
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-11; si02_prerequisites_checklist.md v1.0: 13 items, 4 Complete, 1 gate-conditional, 8 Open)
**Priority:** P1 (High)
**Type:** Governance / Sprint Planning Gate
**Owner:** PMO Lead; Head of Specs Team
**Source:** IDEA-pmo-lead-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~0.5 day)
**Provisional-Target:** Before SI-02 sprint planning seals

**Problem**
SI-02 has 8+ pre-planning backlog items across 5 domains (BLG-GOV-39/44/46/51, BLG-SPEC-37/39/41, BLG-BE-17/20/23). No consolidated readiness gate ensures all prerequisites are verified before sprint planning seals. Without a checklist, individual prerequisite misses are only discovered mid-sprint.

**Scope**
- Produce SI-02 sprint planning prerequisites checklist consolidating all pre-sprint items
- Integrate into release_planning_prompt.md or sprint_planning_prompt.md as a gated advisory step
- Sprint planning may not seal until all checklist items verified

**Acceptance Criteria**
- Prerequisites checklist produced and filed
- Integration point in sprint planning engine defined
- PMO Lead and Head of Specs Team sign-off

---

---

### BLG-GOV-61 — v4.1 staging sign-off process effectiveness review
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-13; deviation trend IMPROVED: v4.1=2 vs v4.0=4)
**Priority:** P2 (Medium)
**Type:** Governance / Process Review
**Owner:** Director of Quality; PMO Lead
**Source:** IDEA-director-of-quality-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** v4.2

**Problem**
BLG-GOV-30 (staging-only AC designation, shipped v4.1) was intended to reduce last-minute P3 staging deviations. This review assesses whether the intervention worked: comparing staging deviation count in v4.1 against the v3.9/v4.0 baseline. Evidence-based governance quality check.

**Scope**
- Count P3 staging deviations in v4.1 vs v3.9/v4.0 baseline
- Assess whether BLG-GOV-30 staging-only AC designation reduced surprise deviations
- Produce findings note; input to future governance process decisions

**Acceptance Criteria**
- Deviation count comparison produced
- Effectiveness finding documented (improved / no change / insufficient data)
- Reviewed by Director of Quality

---

---

### BLG-GOV-63 — Claude API audit trail implementation
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-07; claude_audit_log table + GET /ai/claude-audit-log endpoint)
**Priority:** P2 (Medium)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer; Head of Backend Engineering
**Source:** IDEA-ai-compliance-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** M (~2 days)
**Provisional-Target:** v4.2

**Problem**
v4.1 replaced Gemini with Claude API. BLG-GOV-35 (Gemini audit trail) is COMPLETE but covered Gemini-specific logging. A Claude API equivalent audit trail must log per-request: request_id, endpoint, model_id, prompt_version, input_tokens, output_tokens, cost_usd, generated_at. Without this, AI usage volume growth proceeds without compliance logging.

**Scope**
- Implement per-request Claude API audit log (claude_audit_log table or equivalent)
- Log fields: request_id, endpoint, model_id, prompt_version, input_tokens, output_tokens, cost_usd, generated_at
- Analogous to BLG-GOV-35 implementation pattern

**Acceptance Criteria**
- Claude API audit log implemented and populated on each thesis generation call
- Log queryable for BLG-OPS-36 cost review
- Reviewed by AI Compliance & Governance Officer

---

---

### BLG-GOV-64 — Anthropic model version pinning policy
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-02; ai_model_version_pinning_policy.md v1.0; AI_MODEL env-var override removed)
**Priority:** P2 (Medium)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer; Head of Specs Team
**Source:** IDEA-ai-compliance-20260527-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.2

**Problem**
All Claude-backed features must pin to a specific Anthropic model ID (never use "latest" alias or unversioned model references). Unversioned model references create silent behaviour change risk when Anthropic updates model versions. This policy supersedes BLG-GOV-48 scope (displaced; Gemini retired v4.1).

**Scope**
- Define policy: all Claude-backed features must pin to a specific model ID (e.g., claude-3-5-sonnet-20241022)
- Define change management: model version update requires AI Compliance sign-off and QA re-test
- Apply immediately to thesis generation endpoint
- Document in AI governance notes or CLAUDE.md

**Acceptance Criteria**
- Policy document produced
- Thesis generation endpoint confirmed to use pinned model ID (not "latest")
- Reviewed by AI Compliance & Governance Officer and Head of Specs Team

---

---

### BLG-GOV-65 — Anthropic API key scope and security review
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-01; anthropic_api_key_scope_review.md; 3 sign-offs)
**Priority:** P1 (High)
**Type:** Governance / Security
**Owner:** Cybersecurity & Trust Lead
**Source:** IDEA-cybersecurity-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.2

**Problem**
BLG-GOV-49 (Gemini key scope minimisation review) is COMPLETE. The Anthropic API key introduced in v4.1 requires the equivalent review: confirm minimum required permissions, stored as env var only, not exposed in application logs or error traces. Without this review, the Claude key's security posture is unconfirmed.

**Scope**
- Confirm Anthropic API key has minimum required permissions
- Confirm key is stored as env var only (not in code or logs)
- Confirm key not exposed in application logs or error traces
- Document confirmation in api_key_register.md (BLG-GOV-50 scope)

**Acceptance Criteria**
- Security confirmation produced and documented
- No key exposure in logs confirmed
- Reviewed by Cybersecurity & Trust Lead

---

---

### BLG-GOV-66 — Anthropic API accountability assignment
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-01; AI Compliance Officer charter §4.1 updated with Anthropic provider coverage)
**Priority:** P2 (Medium)
**Type:** Governance / Role Clarity
**Owner:** Director of HR; AI Compliance & Governance Officer
**Source:** IDEA-director-of-hr-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** XS (~0.25 day)
**Provisional-Target:** v4.2

**Problem**
v4.1 introduced Claude API integration. It must be confirmed which agent role owns the Anthropic integration for compliance and governance. If the AI Compliance & Governance Officer's charter does not explicitly cover Anthropic (vs. Gemini), the charter must be updated. Accountability clarity is required before BLG-GOV-63/64/65 are sprint-planned.

**Scope**
- Review AI Compliance & Governance Officer charter for explicit Anthropic coverage
- If charter gap found: update charter to include Anthropic API accountability
- Document ownership confirmation in governance notes

**Acceptance Criteria**
- Charter review complete
- Ownership confirmed (or charter updated to add Anthropic coverage)
- Reviewed by Director of HR and AI Compliance & Governance Officer

---


---

## v4.2 Additional Completions — BLG-GOV-58 Archived 2026-05-29

---

### BLG-GOV-58 — STEP 5.2 returned_to_backlog in-flight clarification
**Shipped:** ✅ COMPLETE — pre-resolved by AUD-2026-05-27-003 (execution_prompt.md v3.29) before v4.2 planning; confirmed COMPLETE at groom backlog 2026-05-29
**Priority:** P2 (Medium)
**Type:** Governance / Prompt Patch
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** XS (~0.25 day)
**Provisional-Target:** v4.2 sprint seal (carry-forward OA-2 from v4.1)

**Problem**
execution_prompt.md STEP 5.2 does not explicitly confirm that `returned_to_backlog` is a valid status for PO-authorized in-flight story deferrals during sprint execution (not only at sprint close). ST-11 deferral in v4.1 required this path but STEP 5.2 language was ambiguous.

**Scope**
- Amend execution_prompt.md STEP 5.2 to clarify returned_to_backlog is valid for in-flight PO-authorized deferrals
- Head of Specs Team sign-off; bump execution_prompt.md version

**Acceptance Criteria**
- execution_prompt.md STEP 5.2 amended with in-flight deferral clarification
- Version bumped and prompt_change_log.md updated
- OPERATIONAL_GUIDE.md §14 updated

---

