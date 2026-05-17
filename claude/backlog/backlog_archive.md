**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-15

# Backlog Archive — Momentum Trading Assistant

Permanent record of completed and killed backlog items retired from `claude/backlog/backlog.md`. Listed in retirement order, most recent first. Append-only — do not edit existing entries.

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

