**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-06
**Cycle:** 2026-03-06__release-v1.9
**Release:** v1.9
**Sprint Goal:** Deliver a fully corrected Risk Dashboard, meaningful trading insight features (compliance metrics, trade reflection, cohort analytics, R-multiple distribution, and a session summary home page), and the quality infrastructure improvements that close the v1.8 scenario coverage gap.

---

# Sprint Backlog — 2026-03-06__release-v1.9

---

## Sprint Scope

---

### EPIC-01 — Trade Reflection & Compliance Metrics

**Maps to:** S2-01, S2-02
**Owner:** Head of Engineering (implementation); Metrics Definitions & Analytics Owner (spec)
**Estimated effort:** ~17 hours (mid)
**Risk IDs:** RISK-01 (resolved), RISK-02 (monitor), RISK-03 (monitor)
**Execution sequence:** Wave 2 (ST-01) → Wave 3 (ST-02)

---

#### ST-01 — Canonicalise Basic Compliance Metrics

**Owner:** Metrics Definitions & Analytics Owner (spec); Head of Engineering (implementation)
**Estimated effort:** 6–8 hours
**Delegation class:** delegated_backend + delegated_frontend

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | `metrics_definitions.md` version incremented; canonical definitions added for: (a) journal completion rate — formula, denominator, time window; (b) stop-based exit rate — formula, classification rules; (c) average position size as % of portfolio — formula, snapshot basis. Backend computes and exposes all three metrics via existing or extended analytics endpoint. Frontend displays the three metrics on the analytics page or a dedicated compliance panel. |
| Quality | At least one test scenario per metric confirming displayed value matches backend-computed value against a known closed-trade dataset. Edge case: zero denominator (no closed trades) renders gracefully. |
| Security | N/A — read-only analytics; no new security surface introduced. |
| Verification | Director of Quality executes 3 metric display scenarios and confirms values consistent with metrics_definitions.md formulae. `metrics_definitions.md` version number incremented and Head of Specs Team confirms lifecycle compliance. |

**Dependencies:** None
**Notes:** RISK-01 resolved (LL-05 PASS — Metrics Definitions owner available). Metric definitions for ST-03 (cohort) and ST-04 (R-multiple) may be batched into the same `metrics_definitions.md` update — confirm at ST-01 start. Pre-condition for ST-02, ST-03, ST-04.

---

#### ST-02 — Structured Trade Reflection Template

**Owner:** Frontend Specs & UX Documentation Owner (spec); Head of Engineering (implementation)
**Estimated effort:** 8–12 hours
**Delegation class:** delegated_backend + delegated_frontend

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | `docs/specs/frontend/pages/trade_reflection.md` confirmed canonical at v0.1 (already created this cycle). Reflection modal opens automatically on trade close confirmation (success response received). Modal pre-populates 8 read-only fields from trade record: ticker, entry_price, exit_price, holding_days, r_multiple, exit_reason, exit_state, exit_date — all from backend, none computed on frontend; null fields display "–". Five reflection textareas with prompts and 500-char limits rendered beneath. Skip button dismisses without saving. Save button POSTs to `POST /trades/{trade_id}/reflection`; modal closes on 200 OK; success toast displayed 2 seconds. On POST error: inline error shown, submit re-enabled, user may retry or skip. Focus trap within modal. `aria-label` = "Trade Reflection — {ticker}". `trade_reflections` storage table defined in `data_model.md` by Data Model & Domain Schema Owner before backend implementation begins. `POST /trades/{trade_id}/reflection` documented in `docs/specs/api_contracts/trade_endpoints.md`. |
| Quality | Scenarios: (a) modal opens on trade close; (b) pre-populated fields match trade record values; (c) save with all fields populated — success toast shown; (d) save with all fields empty — accepted (no validation error); (e) skip — modal dismissed, trade still closed; (f) save error — error shown, retry works; (g) character limit at 500 chars enforced per textarea; (h) Skip reachable by keyboard (focus trap). |
| Security | N/A — authenticated POST to existing trade resource; no new security surface beyond standard authenticated endpoint. Reflection text is user-authored and stored server-side with no AI processing. |
| Verification | Director of Quality executes scenarios (a)–(f) against live or seeded environment. Head of Specs Team confirms `trade_reflection.md` spec in canonical state and `trade_endpoints.md` includes the reflection endpoint. Data Model owner confirms `trade_reflections` schema in `data_model.md`. |

**Dependencies:** ST-01 (metrics definitions canonical — must complete before ST-02 implementation begins)
**Notes:** RISK-02 — Data Model & Domain Schema Owner must confirm `trade_reflections` schema before backend implementation. Not a sprint seal blocker but must precede ST-02 execution.

---

### EPIC-02 — Analytics Enhancements

**Maps to:** S2-03, S2-18
**Owner:** Head of Engineering
**Estimated effort:** ~18 hours (mid)
**Risk IDs:** RISK-03 (monitor)
**Execution sequence:** Wave 3 (both items, after ST-01 metrics batch)

---

#### ST-03 — Cohort Analysis

**Owner:** Head of Engineering
**Estimated effort:** 8–12 hours
**Delegation class:** delegated_backend + delegated_frontend

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Cohort metric definitions added to `metrics_definitions.md` (same version update as ST-01 if batched). Backend: new query or analytics endpoint extension returning closed-trade performance grouped by entry period (month, quarter, year). Frontend: cohort analysis tab or panel on Performance Analytics page with period selector (Month / Quarter / Year). Values sourced exclusively from backend — no client-side re-derivation. New endpoint documented in `docs/specs/api_contracts/analytics_endpoints.md` and `openapi.yaml` updated. `analytics.md` frontend spec §15 already created this cycle — confirm implementation matches spec. |
| Quality | Scenarios: (a) period selector — each of month/quarter/year returns correctly grouped data; (b) values verified against manual grouping of known closed trades for at least one period; (c) panel renders with no closed trades — graceful empty state; (d) endpoint documented in openapi.yaml — openapi-drift CI passes. |
| Security | N/A — read-only analytics; no new security surface. |
| Verification | Director of Quality confirms period selector produces correct groupings against a known dataset. Head of Engineering confirms openapi-drift CI passes after openapi.yaml update. |

**Dependencies:** ST-01 (cohort metric definitions may be batched into ST-01 metrics update)
**Notes:** RISK-03 — metrics batching. Confirm at ST-01 start whether cohort defs are included in the same `metrics_definitions.md` increment. If batched, no additional version increment needed for ST-03.

---

#### ST-04 — R-Multiple Distribution Report

**Owner:** Metrics Definitions & Analytics Owner (definition); Head of Engineering (implementation)
**Estimated effort:** 6–10 hours
**Delegation class:** delegated_backend + delegated_frontend

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | R-multiple formula defined and canonicalised in `metrics_definitions.md` (batched with ST-01 if possible). Backend computes R-multiple per closed trade from existing trade data using canonical formula. Distribution visualisation (chart or panel) rendered on Performance Analytics page. All values computed from backend formula — no client-side derivation. `analytics.md` frontend spec §16 already created this cycle — confirm implementation matches spec (§16 is canonical; §9 remains client-side visualisation aid and is not removed). |
| Quality | Scenarios: (a) chart renders with 5+ closed trades; (b) minimum trade count guard: fewer than 5 trades renders "Insufficient data" or equivalent; (c) positive R values shown in green buckets, negative in red; (d) distribution values cross-checked against manual R-multiple calculation for at least 3 known trades. |
| Security | N/A — read-only analytics. |
| Verification | Director of Quality cross-checks at least 3 R-multiple values against manual calculation from trade records. Confirms §9 (client-side) and §16 (backend canonical) both render and coexist on the analytics page. |

**Dependencies:** ST-01 (R-multiple formula must be canonical in metrics_definitions.md before implementation)
**Notes:** Coexistence with §9 (client-side R-multiple) documented in analytics.md API Dependency note. §16 is canonical; §9 remains. No removal of §9 required.

---

### EPIC-03 — Dashboard Homepage

**Maps to:** S2-04
**Owner:** Head of Engineering (implementation); Frontend Specs & UX Documentation Owner (spec)
**Estimated effort:** ~8 hours (mid)
**Risk IDs:** RISK-04 (advisory)
**Execution sequence:** Wave 3 (independent; placed last to allow composite endpoint pre-alignment decision)

---

#### ST-05 — Dashboard Homepage / Session Summary

**Owner:** Head of Engineering (implementation)
**Estimated effort:** 6–10 hours
**Delegation class:** delegated_frontend

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Dashboard home page renders at route `/` on load with 5 data cards: (1) Open Positions — count + state breakdown from `GET /positions`; (2) Portfolio Heat — `portfolio_heat_percent` with colour coding (green <15%, amber 15–25%, red >25%) from `GET /portfolio`; (3) In Grace Today — count + earliest `grace_end_date` from `GET /portfolio` or `GET /positions`; (4) Signal Status — regime per market (SPY/FTSE) + signals today count from `GET /market/status` and `GET /signals`; (5) Recent Activity — last 3–5 trade events from `GET /trades`. Each card click navigates to its target route (/positions, /risk, /signals, /trades). Individual card failure renders error indicator without breaking other cards. Skeleton loading state for all 5 cards during initial load. If composite endpoint `GET /dashboard/summary` introduced: aggregation only, documented in `docs/specs/api_contracts/` and `openapi.yaml`. `dashboard.md` spec v2.0 already created this cycle — implementation must match. |
| Quality | Scenarios: (a) all 5 cards render with live data; (b) individual card API failure — affected card shows error, others render normally; (c) each card click navigates to correct route; (d) mobile: all 5 cards stack vertically in order; (e) all-endpoints-failed: full page error with Retry button. |
| Security | N/A — aggregation of existing authenticated endpoints; no new data or computation exposed. Composite endpoint, if added, must not introduce new computation. |
| Verification | Director of Quality confirms all 5 cards render and navigation works. Confirms individual card failure isolation by simulating one endpoint failure. If composite endpoint added: Head of Specs Team confirms API contract documented and openapi-drift CI passes. |

**Dependencies:** None
**Notes:** RISK-04 — composite endpoint decision deferred to ST-05 execution pre-alignment. Engineering to confirm at sprint start whether to implement composite endpoint or use individual calls. Either approach satisfies the spec.

---

### EPIC-04 — Risk Dashboard Defect Resolution

**Maps to:** S2-05 through S2-15
**Owner:** Head of Engineering (implementation); Head of Specs Team (ST-06 spec alignment)
**Estimated effort:** ~14.5 hours remaining (mid; ST-06 pre-completed)
**Risk IDs:** RISK-05 (monitor), RISK-06 (resolved)
**Execution sequence:** Wave 1 (ST-06 done, ST-07, ST-10) → Wave 2 (ST-08, ST-09)

---

#### ST-06 — Drawdown Data Source Spec Alignment

**Owner:** Head of Specs Team
**Estimated effort:** N/A — **PRE-COMPLETED 2026-03-06**
**Delegation class:** autonomous

**Status:** COMPLETE. Decision made 2026-03-06 by Head of Specs Team:
- `current_drawdown_percent` → `GET /portfolio` (confirmed)
- `days_underwater` → `GET /analytics/metrics` (confirmed)
- `risk_dashboard.md §4.1` updated to v0.1.7; DEV-ST03-08 resolved; BLG-RD-08 closed.

**No execution work required.**

---

#### ST-07 — Risk Dashboard Backend: US Currency Conversion

**Owner:** Head of Engineering
**Estimated effort:** 3–6 hours
**Delegation class:** delegated_backend

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | `backend/services/portfolio_service.py` converts `entry_price` to GBP for US positions using stored `fx_rate` (same pattern as `current_price` FX conversion). `portfolio_service.py` converts `current_stop` to GBP for US positions using same `fx_rate`. All position prices returned in GBP for both US and UK positions. Stop Distance % calculation uses matching currencies (both GBP). |
| Quality | Golden output tests updated to include US position with GBP entry_price and GBP current_stop. Golden output CI passes (no regression). Existing UK position values unchanged. Scenario: US position entry price displays as GBP value on Risk Dashboard. |
| Security | N/A — backend computation change; no new endpoint, no new data exposure. |
| Verification | Director of Quality confirms golden output CI passes after change. SC-RD scenarios for US position currency display pass against live or seeded environment. |

**Dependencies:** None
**Notes:** Deploy before ST-08 and ST-09 frontend changes, or provide mock for frontend development.

---

#### ST-08 — Risk Dashboard Frontend: Error States & Entity Fallback

**Owner:** Head of Engineering / Base44 Frontend Prompt Owner
**Estimated effort:** 2–4 hours
**Delegation class:** delegated_frontend

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Each Risk Dashboard component (HeatGauge, DrawdownSummary, GracePeriodPanel, PositionRiskTable, ProspectiveHeatPanel) renders its own error state independently when `GET /portfolio` fails. Entity store fallback (`base44.entities`) does not silently mask API failure — either error indicator is shown while fallback data is displayed, or fallback is removed. GracePeriodPanel renders a distinct error card (not empty state) when `portfolioError` is set. |
| Quality | Scenarios SC-RD-02 (portfolio API error → error state shown) and SC-RD-03 (GracePeriodPanel error vs empty state) from test scenario library. Verified by simulating API failure (mock 500 or network error). Confirms error indicator is visible and distinct from "no data" state. |
| Security | N/A — frontend display logic only. |
| Verification | Director of Quality executes SC-RD-02 and SC-RD-03 against seeded test environment. Confirms error state is visually distinct from empty state for GracePeriodPanel. |

**Dependencies:** ST-07 (soft — deploy backend first or use mock for currency display)
**Notes:** RISK-05 — Base44 entity store fallback approach to be agreed at execution pre-alignment. Base44 Frontend Prompt Owner must be consulted if platform-level configuration change is required.

---

#### ST-09 — Risk Dashboard Frontend: Table and Column Fixes

**Owner:** Head of Engineering
**Estimated effort:** 2–4 hours
**Delegation class:** delegated_frontend

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | PositionRiskTable sorted by stop distance ascending (tightest/smallest first = most at risk) within each state group, per spec §6.4. Stop Price column (`current_stop`, GBP, 2 dp) present in PositionRiskTable per spec §6.2. Days in Grace (`holding_days`) column present in Grace Period table per spec §5.2. Threshold label badge present in ProspectiveHeatPanel result row, updating when boundary crossed, per spec §7.5. |
| Quality | Scenarios SC-RD-04 (sort ascending verified with 3+ positions), SC-RD-05 (Stop Price column present), SC-RD-07 (Days in Grace column present), SC-RD-08 (threshold label badge updates on boundary cross). Verified against known position data. |
| Security | N/A — frontend display. |
| Verification | Director of Quality executes all four scenarios. Confirms sort direction by inspecting rendered table with multiple positions. Confirms column presence visually and in DOM. |

**Dependencies:** ST-07 (soft — ST-08 and ST-09 may be developed together)
**Notes:** 4 independent fixes; can be implemented in a single Base44 prompt session.

---

#### ST-10 — Risk Dashboard Frontend: HeatGauge and Cosmetic Fixes

**Owner:** Head of Engineering
**Estimated effort:** 1–3 hours
**Delegation class:** delegated_frontend

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | GRACE state badge colour is blue (not amber) per spec §6.3. GBP value at risk displayed below gauge percentage value per spec §3.2 (value = portfolio_heat_percent × portfolio_value expressed as GBP). |
| Quality | Scenarios SC-RD-05 (GRACE badge is blue), SC-RD-06 (GBP value at risk visible below gauge). Verified visually. |
| Security | N/A — cosmetic frontend changes. |
| Verification | Director of Quality visually confirms badge colour is blue. Confirms GBP value at risk displayed beneath gauge percentage. |

**Dependencies:** None (cosmetic; no backend dependency)
**Notes:** Can be implemented independently of ST-07 backend deploy.

---

### EPIC-05 — QA & Test Infrastructure

**Maps to:** S2-16, S2-17
**Owner:** QA & Testing Owner (ST-11, ST-12); Backend Engineering Patterns Owner (ST-13)
**Estimated effort:** ~18.5 hours (mid)
**Risk IDs:** RISK-07 (monitor)
**Execution sequence:** Wave 1 (ST-11 infra setup, ST-13) → Wave 4 distributed (ST-12)

---

#### ST-11 — Canonical Test Scenario Library Phase 1 (Risk Dashboard)

**Owner:** QA & Testing Owner
**Estimated effort:** 6–10 hours
**Delegation class:** delegated_qa

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Seeded test infrastructure created — approach agreed at pre-alignment (seeded SQLite, mock/stub API layer, or test fixture API). Infrastructure supports: specific `portfolio_heat_percent` values, positions with specific `grace_days_remaining`, empty position state, controlled prospective heat API responses. "Test Infrastructure Preconditions" section added to `docs/testing/risk_dashboard_scenarios.md` documenting how to initialise the seeded environment (Director of Quality requirement — outstanding action from v1.8 closure). All 17 NOT EXECUTED Risk Dashboard scenarios (SC-RD-02–06, SC-RD-07–12, SC-RD-15, SC-RD-16–18, SC-RD-24–25) re-run against seeded environment. Results recorded in `risk_dashboard_scenarios.md`. |
| Quality | Infrastructure is reproducible — another developer can follow the "Test Infrastructure Preconditions" section to initialise the environment and re-run scenarios independently. No scenario relies on live external data or non-deterministic state. |
| Security | N/A — test infrastructure; no production data used. Seeded data must not include real user data. |
| Verification | Director of Quality confirms all 17 scenarios have a recorded result (PASS/FAIL/BLOCKED) in `risk_dashboard_scenarios.md`. Confirms "Test Infrastructure Preconditions" section is present and sufficient for independent replication. |

**Dependencies:** None
**Notes:** RISK-07 — approach decision (seeded DB vs mock layer) to be made at ST-11 start by QA & Testing Owner and Head of Engineering. Record chosen approach in risk_dashboard_scenarios.md "Test Infrastructure Preconditions" section.

---

#### ST-12 — Canonical Test Scenario Library Phase 2 (v1.9 Features)

**Owner:** QA & Testing Owner
**Estimated effort:** 4–8 hours (distributed across sprint)
**Delegation class:** delegated_qa

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Test scenarios authored and added to canonical library as each v1.9 feature completes: EPIC-01 (compliance metrics + reflection template), EPIC-02 (cohort analysis + R-multiple distribution), EPIC-03 (dashboard home), EPIC-04 (all 11 resolved deviations), EPIC-06 (lifecycle compliance checks where applicable). Each scenario record includes: SC-ID, precondition, steps, expected result, actual result, status. No retroactive full-endpoint coverage mandate. |
| Quality | Each new scenario is independently executable with the seeded test infrastructure established in ST-11. Scenario IDs follow existing SC-RD-xx convention; new features use SC-{EPIC-ID}-xx numbering. |
| Security | N/A — scenario authoring only. |
| Verification | Director of Quality reviews scenario library at sprint close and confirms: at least 2 scenarios per new feature; all EPIC-04 deviation items have at least one scenario confirming resolution. |

**Dependencies:** ST-11 (seeded infra enables scenario execution); EPIC-01, EPIC-02, EPIC-03 delivery (scenarios authored as features complete)
**Notes:** Distributed throughout sprint. No fixed capacity block — author scenarios incrementally as features are verified.

---

#### ST-13 — Service Layer Test Coverage Standard

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 3–6 hours
**Delegation class:** delegated_backend + delegated_qa

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Service Layer Test Coverage Standard document authored (as section of or reference from `docs/specs/backend_engineering_patterns.md`, version incremented). Document includes: named coverage threshold (% agreed at pre-alignment), scope definition (backend/services/ directory), tool (pytest-cov or equivalent). CI step added to enforce threshold: GitHub Actions workflow runs pytest-cov on `backend/services/`; build fails if coverage falls below threshold. BLG-NEW-01 prerequisite (golden output baseline) confirmed complete (shipped v1.8). |
| Quality | CI run with current test suite demonstrates threshold enforcement: a test run with coverage at or above threshold passes; behaviour below threshold is confirmed to fail build (can be demonstrated with a single dummy test removal and revert). |
| Security | N/A — CI/quality tooling addition only. |
| Verification | Director of Quality confirms CI workflow YAML contains the coverage step. Confirms `backend_engineering_patterns.md` version incremented and standard is referenced. Confirms threshold is named and agreed. |

**Dependencies:** None (BLG-NEW-01 confirmed complete)
**Notes:** Threshold value to be agreed between Backend Engineering Patterns Owner and Head of Engineering at execution start. Record agreed threshold in standard document.

---

### EPIC-06 — Documentation Hygiene & Governance

**Maps to:** S2-19 through S2-30
**Owner:** Head of Specs Team (coordinator)
**Estimated effort:** ~18 hours (mid; all 6 items × ~3 hrs average)
**Risk IDs:** RISK-08 (closed), RISK-09 (monitor)
**Execution sequence:** Wave 1 — all items autonomous, parallelisable

---

#### ST-14 — Canonical Terms Glossary

**Owner:** Head of Specs Team
**Estimated effort:** 2–4 hours
**Delegation class:** autonomous

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Glossary created as Class 2 Supporting document with lifecycle-compliant header (Owner, Class, Status, Version, Last Updated). Minimum terms defined: portfolio heat, grace period, stop distance, R-multiple, cohort, journal completion rate, stop-based exit rate. Each term: definition + link to Class 1 canonical source. No new canonical definitions introduced — cross-references only. Registered in `docs/specs/Specs_Index.md`. |
| Quality | Lifecycle compliance check: all required header fields present. Spot-check: 3 terms — definition matches the referenced Class 1 source. |
| Security | N/A — documentation only. |
| Verification | Head of Specs Team confirms lifecycle compliance. Director of Quality spot-checks 3 terms for accuracy. |

**Dependencies:** None
**Notes:** Terms like "portfolio heat" link to `metrics_definitions.md`; "grace period" links to `strategy_rules.md` or appropriate canonical source. Do not redefine — only cross-reference.

---

#### ST-15 — AI-Assisted Workflow Governance Policy

**Owner:** Product Owner / AI Compliance & Governance Officer
**Estimated effort:** 2–4 hours
**Delegation class:** autonomous

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Policy document authored and filed under `docs/governance/` or `claude/charter/` (path confirmed by Product Owner). Lifecycle-compliant header present (Class, Owner, Status, Last Updated). Policy covers all 4 required areas: (a) AI authority scope — what the engine may decide autonomously vs what requires human override; (b) mandatory human review checkpoints — explicit list; (c) escalation triggers — conditions requiring halt; (d) record-keeping obligations — what must be logged and where. |
| Quality | Lifecycle compliance check: all required header fields present. Content spot-check: all 4 required policy areas present and non-empty. |
| Security | N/A — governance document. |
| Verification | Product Owner confirms policy covers all 4 areas and is filed in the correct governance path. |

**Dependencies:** None

---

#### ST-16 — Document GET /market/status Endpoint

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 2–4 hours
**Delegation class:** autonomous

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | `docs/specs/api_contracts/market_endpoints.md` created as Class 1 Canonical document (v0.1). Covers: GET /market/status — request parameters, response schema (SPY regime, FTSE regime, live FX rate), error behaviour. Registered in `docs/specs/Specs_Index.md §3`. `docs/reference/openapi.yaml` updated with GET /market/status schema (replacing or expanding the current `additionalProperties: true` placeholder). |
| Quality | openapi-drift CI passes after openapi.yaml update. Lifecycle compliance check on market_endpoints.md passes. Response schema in openapi.yaml is consistent with the backend implementation (verified by inspection of backend route). |
| Security | N/A — documentation of existing endpoint; no code change. |
| Verification | Director of Quality confirms openapi-drift CI passes after update. Head of Specs Team confirms Specs_Index.md updated. |

**Dependencies:** None
**Notes:** Backend `GET /market/status` already exists (noted as undocumented in current openapi.yaml). This item closes that gap.

---

#### ST-17 — Create settings_model.md

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 2–4 hours
**Delegation class:** autonomous

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | `docs/specs/data_model/settings_model.md` created as Class 1 Canonical document (v0.1). Covers: settings schema — all field names, types, validation rules, defaults based on the confirmed PATCH /settings/{settings_id} + POST /settings shape (resolved ST-09 v1.8). Registered in `docs/specs/Specs_Index.md §3`. Cross-referenced from `docs/specs/api_contracts/settings_endpoints.md`. |
| Quality | Lifecycle compliance check passes. Field list spot-checked against actual settings endpoint response (confirmed by inspection). |
| Security | N/A — data model documentation; no code change. |
| Verification | Head of Specs Team confirms field list matches settings endpoint implementation. Specs_Index.md and settings_endpoints.md cross-references confirmed. |

**Dependencies:** None (BLG-SPEC-D2 resolved in v1.8 — PATCH /settings canonical)
**Notes:** RISK-08 closed — no blocker. `docs/specs/data_model/` directory may need to be created if it does not yet exist.

---

#### ST-18 — Define Error Response Standard

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 2–4 hours
**Delegation class:** autonomous

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | Error Response Standard document created as a new Class 1 Canonical document, or added as a new canonical section to an existing API contracts document. Covers: standard error envelope shape, required fields (status_code, error_code, message, detail), HTTP status code mapping. All existing API contract docs (`portfolio_endpoints.md`, `trade_endpoints.md`, `analytics_endpoints.md`, `settings_endpoints.md`, `position_endpoints.md`) updated to reference the Error Response Standard for their error sections. Registered in `docs/specs/Specs_Index.md`. |
| Quality | Lifecycle compliance check passes for the new standard document. Spot-check: at least 2 existing API contract error sections reference the standard. |
| Security | N/A — documentation only. |
| Verification | Head of Specs Team confirms all existing API contract docs reference the standard. Director of Quality spot-checks 2 cross-references. |

**Dependencies:** None

---

#### ST-19 — Spec/Doc Debt Small Fixes (7 items)

**Owner:** Head of Specs Team (coordinator); individual domain owners per item
**Estimated effort:** 2–4 hours (all 7 items)
**Delegation class:** autonomous

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | All 7 items complete: (BLG-SPEC-D1) `docs/specs/api_contracts/README.md` header + changelog updated to v1.9.0. (BLG-SPEC-D4) `position_endpoints.md` includes GET /positions/search/tags with parameters + response schema. (BLG-SPEC-D8) `docs/System_status_report.md` lifecycle header added (Owner, Class, Status, Version, Last Updated). (BLG-SPEC-D9) `docs/governance/process_index.md` and `docs/specs/Specs_Index.md §5` updated to reference `claude/charter/document_lifecycle_guide.md`. (BLG-SPEC-G3) `docs/specs/Specs_Index.md §3` updated to include structured_logging_standards.md. (BLG-SPEC-G4) ADR-002 confirmed present in `docs/product/decisions/`; cross-references updated. (BLG-SPEC-G5) `docs/specs/validation_system.md` owner field updated to a named governance role. |
| Quality | Lifecycle compliance check passes for all 7 documents touched. Spot-check: at least 3 items verified by Head of Specs Team. |
| Security | N/A — documentation only; no code changes. |
| Verification | Head of Specs Team spot-checks all 7 items and confirms each acceptance criterion is met. |

**Dependencies:** None (RISK-09 — Head of Specs Team to verify ADR-002 location at sprint start before attempting BLG-SPEC-G4)
**Notes:** Can be batched and delivered as a single commit. ~30 min per item.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity (sprint) | ~15–25 hours |
| ST-06 pre-completed (not counted) | ~2 hours consumed pre-sprint |
| Total estimated effort (18 remaining items, mid) | ~88 hours |
| Utilisation | ~350–590% (over-allocated) |
| Over-allocation | **Yes — requires explicit Product Owner acceptance** |
| Over-allocation rationale | v1.9 is a full release (6 EPICs, ~90 hrs). Solo dev at 10–15 hrs/week = 6–9 weeks elapsed. Pre-anticipated at release planning (stage4_5_capacity_check.md §3). Product Owner to decide: single extended sprint vs phased approach. |

---

## Items Deferred This Sprint

None — all 19 items included. Over-allocation accepted pending Product Owner sign-off.

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Confirm sprint goal wording | Product Owner | Yes |
| Confirm scope (single sprint vs phased) | Product Owner | Yes |
| Confirm over-allocation explicitly accepted | Product Owner | Yes |
| Confirm trade_reflections schema in data_model.md (before ST-02 execution) | Data Model & Domain Schema Owner | No (execution pre-condition only) |
| Confirm ADR-002 location before ST-19/BLG-SPEC-G4 (RISK-09) | Head of Specs Team | No (execution pre-condition only) |
| Agree ST-11 test infra approach at sprint start | QA & Testing Owner + Head of Engineering | No (execution pre-condition only) |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** [AWAITING SIGN-OFF]
**Scope confirmed:** [AWAITING SIGN-OFF]
**Capacity over-allocation explicitly accepted:** [AWAITING SIGN-OFF]
**Signed off by:** Product Owner
**Date:** [AWAITING SIGN-OFF]
