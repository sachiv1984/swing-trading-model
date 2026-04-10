# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-04-10 (groom backlog — v2.5 post-ship closure: 12 items archived to backlog_archive.md; 10 stale v2.5 provisional targets updated to v2.6; 25 active items retained)
**Last rebalance:** 2026-04-05 (cycle 2026-04-05__scheduled — DL-017 to DL-019)

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
**Provisional-Target:** v2.6 (or when system becomes multi-user)

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

## 3. Frontend & UX Backlog

---

### BLG-FE-11 — Trade History StatsCard bar layout: squeeze at 6-card width
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Owner
**Source:** EPIC-03 DoQ staging run 2026-04-10 — adding Avg Fee Drag card (6th card) causes visible squeeze on the Trade History summary bar at standard viewport widths
**Effort:** S (~half day)
**Provisional-Target:** v2.6
**Requires:** Head of UX review before implementation

**Problem**
The Trade History StatsCard summary bar now contains 6 cards (Total Trades, Win Rate, Total P&L, Avg Slippage, Avg Entry Dev., Avg Fee Drag). At standard 1280px viewports the grid is visually crowded. The current grid spec (`lg:grid-cols-3 xl:grid-cols-6`) may need to be revisited — either by condensing card content, increasing the xl breakpoint, or adopting a scrollable/overflow pattern. Head of UX to define the correct treatment.

**Acceptance Criteria**
- Head of UX reviews the 6-card layout and defines the target grid/layout spec
- Implementation delivers the spec without regression to individual card content
- All 6 cards readable and unstacked at a reasonable viewport width (to be defined by UX)

---

### BLG-FE-12 — Trade History table column header styling and formatting
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Owner
**Source:** EPIC-03 DoQ staging run 2026-04-10 — column headers in the Trade History table flagged as needing better styling and formatting (current style: small, uppercase, muted)
**Effort:** S (~half day)
**Provisional-Target:** v2.6
**Requires:** Head of UX review before implementation

**Problem**
Column headers in the Trade History table use the `DataTable.js` default: `text-xs font-medium text-slate-400 uppercase tracking-wider`. This treatment has been flagged as insufficient — headers are difficult to read and don't visually anchor the columns clearly. Head of UX to define the improved header style (size, weight, colour, case, spacing).

**Acceptance Criteria**
- Head of UX defines target header style
- Implementation updates `DataTable.js` `TableHead` base styles (or Trade History-specific overrides) to match spec
- No regression to other tables using `DataTable.js`

---

### BLG-FE-13 — Flexible column sorting across Trade History table
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Owner
**Source:** EPIC-03 DoQ staging run 2026-04-10 — only 3 columns currently sortable (Slippage, Fee Drag %, R-Multiple); all columns should be sortable or Head of UX should define the sorting strategy
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.6
**Requires:** Head of UX review before implementation

**Problem**
Currently only Slippage, Fee Drag %, and R-Multiple columns are sortable in the Trade History table. Ticker, Entry Date, Exit Date, P&L, % P&L, and Exit Reason have no sort. Users may want to sort by any column (e.g. date, P&L, ticker). Head of UX should decide: (a) add sort to all columns, (b) define a curated set of sortable columns with clear visual affordance, or (c) adopt a more flexible sort pattern (e.g. multi-column sort, sort-by dropdown). The `DataTable.js TableHead` now supports `onClick` (fixed v2.5), so the infrastructure exists — this is a UX design and spec decision.

**Acceptance Criteria**
- Head of UX defines which columns are sortable and the sort interaction model
- Implementation wires sort handlers for all specified columns
- Sort icon treatment consistent across all sortable columns
- No regression to existing Slippage, Fee Drag %, R-Multiple sort behaviour

---

### BLG-FE-10 — Add tooltip prop to StatsCard component
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Owner
**Source:** EPIC-03 DoQ sign-off observation — 2026-04-06 — `trade_history.md` v1.5 §Avg Fee Drag requires ⓘ tooltip text on Avg Fee Drag card; StatsCard component has no tooltip prop
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.6

**Problem**
`StatsCard.js` supports `title`, `value`, `subtitle`, `icon`, `trend`, `trendValue`, and `gradient` — but not a hover tooltip (ⓘ icon). The canonical spec for the Avg Fee Drag StatsCard (`trade_history.md` v1.5 §Avg Fee Drag) requires an ⓘ info icon with tooltip text: *"Average Fee Drag = Total exit fees / Gross proceeds × 100"* / *"Higher % means a greater proportion of gross proceeds consumed by fees."* This cannot be delivered without a component-level capability change. The Avg Slippage StatsCard has the same gap. Any future StatsCard spec that includes a tooltip ⓘ will hit this limitation.

**Scope**
- Add an optional `tooltip` prop to `StatsCard.js` — when provided, renders a small ⓘ icon adjacent to the `title`; hovering shows the tooltip text
- Use a lightweight approach (e.g. `title` attribute on the ⓘ icon, or a Tailwind tooltip pattern) consistent with the existing component style
- Wire `tooltip` on the Avg Fee Drag StatsCard in `TradeHistory.js`: `"Average Fee Drag = Total exit fees / Gross proceeds × 100 — Higher % means a greater proportion of gross proceeds consumed by fees."`
- Wire `tooltip` on the Avg Entry Dev. StatsCard in `TradeHistory.js` if a tooltip spec exists for it (check `trade_history.md`)
- Update `docs/specs/frontend/pages/trade_history.md` if any spec references are now fully met

**Acceptance Criteria**
- `StatsCard` accepts an optional `tooltip` prop (string); when absent, no ⓘ icon renders (no regression)
- When `tooltip` is provided, an ⓘ icon is visible adjacent to the card title; hovering reveals the tooltip text
- Avg Fee Drag StatsCard in Trade History displays the canonical tooltip text from `trade_history.md` v1.5 §Avg Fee Drag
- No regression to any other StatsCard usage across the app

---

### BLG-FE-09 — Define Frontend Performance Budget
**Priority:** P3 (Low)
**Type:** Frontend Specification
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-ux-20260321-01 — promoted via roadmap rebalance 2026-04-05__scheduled (DL-017)
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.6

**Problem**
No documented frontend performance targets exist for the application (page load time, JS bundle size). BLG-OPS-05 shipped in v2.4 establishing an API latency baseline (p50/p95 per endpoint). Without a companion frontend performance budget, new feature additions in v2.5 and beyond may silently compound bundle size and page load time with no detection mechanism or documented targets for the DoQ to reference when evaluating frontend PRs.

**Scope**
- Define maximum acceptable page load time targets (initial load, route transition)
- Define maximum JS bundle size target (main bundle, code-split chunks)
- Align targets with BLG-OPS-05 API latency baseline — frontend budget must account for the known backend latency floor
- Document measurement methodology (reproducible baseline approach — e.g. Lighthouse, browser dev tools)
- Produce spec document at `docs/specs/frontend/performance_budget.md`

**Acceptance Criteria**
- Spec document exists at `docs/specs/frontend/performance_budget.md` defining page load and bundle size targets
- Targets aligned to BLG-OPS-05 API latency floor (total acceptable load time includes backend latency + frontend rendering overhead)
- Measurement methodology documented (reproducible baseline approach stated)
- Scope is documentation only — no code instrumentation required in this item

---

## 4. Backend & Data Backlog

---


<!-- BLG-BE-08 and BLG-BE-09 — Archived to backlog_archive.md 2026-04-10 (v2.5 post-ship closure) -->

### BLG-BE-08-GAP-01 — Migrate Reports Performance tab to FastAPI backend
**Priority:** P1 (High)
**Type:** Backend Engineering / Frontend Integration
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Source:** ST-04 integration review finding GAP-R01 — `docs/ops/reports_integration_review.md`
**Effort:** L (3–5 days)
**Provisional-Target:** v2.6

**Problem**
The Reports page Performance tab fetches all data from the legacy Base44 SDK (`base44.entities.Position.list()`, `base44.entities.Portfolio.list()`) and computes all metrics client-side. FastAPI endpoints `/analytics/metrics`, `/trades`, and `/portfolio` are never called. This creates data consistency risk — P&L and win-rate figures may differ from Portfolio and Trade History pages which use the FastAPI data model.

**Scope**
- Replace Base44 position/portfolio fetches with calls to `/analytics/metrics?period=<period>`, `/trades`, and `/portfolio`
- Wire the period selector to drive a backend-computed metrics response
- ExportModal to use backend-sourced data (resolves GAP-R03 automatically)
- Also resolves GAP-R02 (analytics endpoints unused from Performance tab)

**Acceptance Criteria**
- Performance tab fetches headline metrics from `/analytics/metrics`; no Base44 calls remain in the Performance tab
- Period selector drives backend-computed results
- P&L/win-rate/profit-factor figures consistent with Trade History and Portfolio pages

---

### BLG-BE-09-GAP-01 — Wire Signals page dismissal and position creation to FastAPI
**Priority:** P1 (High)
**Type:** Backend Engineering / Frontend Integration
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Source:** ST-05 integration review finding GAP-S01 — `docs/ops/signals_integration_review.md`
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.6

**Problem**
Signal dismissal and position creation on the Signals page use `base44.entities.Signal.update()` and `base44.entities.Position.create()`. FastAPI does not receive these writes, so signal status and position records are not stored in the authoritative database. Any backend analytics, deduplication, or ATR-based logic is bypassed for positions entered via the Signals page.

**Scope**
- Replace `base44.entities.Signal.update()` dismiss/enter calls with `PATCH /signals/<id>` or equivalent FastAPI endpoint (create endpoint if absent)
- Replace `base44.entities.Position.create()` with `POST /positions`
- Also resolves GAP-S03 ("already held" check) once positions are sourced from FastAPI

**Acceptance Criteria**
- Dismissing or entering a signal writes to FastAPI; no Base44 mutation calls remain for signal state or position creation
- Dismissed/entered signals are reflected in backend analytics
- Positions created via Signals page appear in Trade History and Portfolio pages

---

### BLG-BE-09-GAP-02 — Replace Base44 cash balance on Signals page with GET /cash/summary
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Frontend Integration
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Source:** ST-05 integration review finding GAP-S02 — `docs/ops/signals_integration_review.md`
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.6

**Problem**
The `availableCash` value displayed on the Signals page is sourced from `base44.entities.Portfolio.list()`. The FastAPI backend maintains the authoritative cash balance at `GET /cash/summary`. These sources may diverge, showing inconsistent cash figures across pages.

**Scope**
- Replace the Base44 portfolio query used for `availableCash` with `apiFetch(GET /cash/summary)`
- Pass the authoritative `cash_balance` value to `MarketStatusBar`

**Acceptance Criteria**
- `availableCash` on Signals page matches the value shown on the Cash/Portfolio pages
- No Base44 portfolio query remains solely for cash balance purposes

---

## 5. QA & Test Automation Backlog

---

### BLG-QA-07 — Fee drag Playwright spec (Trade History)
**Priority:** P2 (Medium)
**Type:** Test Automation
**Owner:** QA & Testing Owner
**Source:** ST-09 (v2.5 EPIC-03) — fee drag metric delivered; no Playwright spec authored
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.6
**Scenarios covered:** SC-FEE-01 through SC-FEE-04 (`docs/testing/fee-drag-scenarios.md` v1.0)

**Problem**
ST-09 delivered the fee drag metric (column + StatsCard) on Trade History. The Trade History page already has `slippage-tracking.spec.js` as a Playwright model. No equivalent spec exists for fee drag — SC-FEE-01 through SC-FEE-04 are classified Automated in the scenario doc but the spec file has not been written.

**Scope**
- Write `tests/e2e/fee-drag-trade-history.spec.js`
- Mock `GET /trades` via `page.route()` with seed data covering: `fee_drag_pct` positive value, `avg_fee_drag_pct` non-null, three trades for sort testing
- Cover SC-FEE-01 (column present, header text, tooltip), SC-FEE-02 (amber `+X.XX%` cell), SC-FEE-03 (Avg Fee Drag StatsCard value and label), SC-FEE-04 (sort ascending/descending)
- Follow the `slippage-tracking.spec.js` mock pattern exactly — `page.route()`, HashRouter navigation, `page.waitForSelector('table')`

**Acceptance Criteria**
- `tests/e2e/fee-drag-trade-history.spec.js` exists covering SC-FEE-01 to SC-FEE-04
- All 4 scenarios pass in headless Playwright (Chromium)
- Spec runs cleanly alongside `slippage-tracking.spec.js` without interference
- Scenario doc `fee-drag-scenarios.md` updated: each SC-FEE-01–04 automation entry updated from pending to confirmed spec file path

---

### BLG-QA-08 — Pytest unit tests for fee drag backend logic
**Priority:** P2 (Medium)
**Type:** Test Automation
**Owner:** QA & Testing Owner
**Source:** ST-09 (v2.5 EPIC-03) — SC-FEE-05 and SC-FEE-06 classified Automated but test file not yet written
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.6
**Scenarios covered:** SC-FEE-05, SC-FEE-06 (`docs/testing/fee-drag-scenarios.md` v1.0)

**Problem**
The fee drag formula and null guard in `trade_service.py` are correctness-critical (a zero gross_proceeds without a null guard would raise `ZeroDivisionError` in production). SC-FEE-05 and SC-FEE-06 are classified as automatable pytest unit tests but `tests/test_trade_service.py` does not yet exist.

**Scope**
- Write `tests/test_trade_service.py`
- Stub DB imports using the same pattern as `test_alerts_service.py` (module-level stub via `sys.modules`)
- SC-FEE-05: assert `fee_drag_pct = 0.38` for `exit_fees = 7.50`, `gross_proceeds = 1975.00`
- SC-FEE-06a: assert `fee_drag_pct = None` when `gross_proceeds = None`
- SC-FEE-06b: assert `fee_drag_pct = None` when `gross_proceeds = 0` (ZeroDivisionError guard)
- Include `avg_fee_drag_pct` aggregate test: mean of non-null values, excludes nulls

**Acceptance Criteria**
- `tests/test_trade_service.py` exists and runs cleanly under `pytest` (no collection errors)
- SC-FEE-05 and SC-FEE-06 assertions pass
- No live DB call — all DB dependencies stubbed at import time
- Added to clean test suite runnable in CI alongside `test_stop_reconciliation.py` and `test_watchlist_service.py`

---

### BLG-QA-09 — Fix 4 pytest collection errors to unblock existing test suite
**Priority:** P1 (High)
**Type:** Test Infrastructure
**Owner:** QA & Testing Owner + Head of Engineering
**Source:** `docs/testing/test_automation_readiness.md` v1.0 §4 — Phase 1 (identified v2.2; still unresolved as of v2.5)
**Effort:** S (~2–3 hours total)
**Provisional-Target:** v2.6

**Problem**
Four test files fail at collection time, making 0% of integration tests runnable and blocking CI automation:
1. `test_portfolio_integration.py` and `test_reports_integration.py`: `API_TITLE` not exported from `backend/config.py` — XS fix
2. `test_service_coverage.py`: `update_position` not found in `database.py` — needs stub or restore — S fix
3. `test_golden_outputs.py`: requires `DATABASE_URL` env var at import time — needs `conftest.py` stub — S fix

All four issues were documented in `test_automation_readiness.md` v1.0 Phase 1. None have been actioned.

**Scope**
- Fix 1: Add `API_TITLE = "Trading Assistant API"` to `backend/config.py`
- Fix 2: Stub `update_position` in `test_service_coverage.py` using the `sys.modules` pattern from `test_alerts_service.py`
- Fix 3: Add `tests/conftest.py` that sets `os.environ["DATABASE_URL"] = "postgresql://test"` before collection
- Run full `pytest tests/` after fixes and confirm all files collect without error

**Acceptance Criteria**
- `pytest tests/` collects all test files without collection errors
- All previously clean tests (`test_stop_reconciliation.py`, `test_watchlist_service.py`) still pass after changes
- `conftest.py` does not interfere with test isolation (dummy DATABASE_URL not used in test logic)

---

### BLG-QA-10 — Add CI test runner workflow (ci-tests.yml)
**Priority:** P2 (Medium)
**Type:** CI / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** `docs/testing/test_automation_readiness.md` v1.0 §4 Phase 1 — identified v2.2; still absent as of v2.5
**Effort:** S (~1 hour)
**Provisional-Target:** v2.6
**Dependency:** BLG-QA-09 (collection errors should be fixed first for full value, but clean tests can run immediately)

**Problem**
No GitHub Actions workflow runs `pytest` or `npx playwright test` on PR. Tests exist but are only run manually. A PR that breaks `test_stop_reconciliation.py` (stop formula regression) or a Playwright spec (frontend regression) would pass all CI gates and merge silently.

**Scope**
- Add `.github/workflows/ci-tests.yml`
- Phase A (can ship immediately): run `pytest tests/test_stop_reconciliation.py tests/test_watchlist_service.py` — the two currently clean unit test files
- Phase B (after BLG-QA-09): expand to `pytest tests/` (all files once collection errors fixed)
- Phase C (future): add `npx playwright test` for Playwright specs
- Workflow triggers: `on: pull_request` targeting `main`

**Acceptance Criteria**
- `.github/workflows/ci-tests.yml` exists and runs on PR
- Phase A: at minimum `test_stop_reconciliation.py` and `test_watchlist_service.py` run on every PR
- A deliberate formula break in `position_manager.py` causes the workflow to fail
- Workflow does not require `DATABASE_URL` secret for Phase A tests (clean tests have no DB dependency)

---

### BLG-QA-11 — System Status Playwright spec (endpoint list sync + category routing)
**Priority:** P3 (Low)
**Type:** Test Automation
**Owner:** QA & Testing Owner
**Source:** v2.5 ST-02 and ST-03 (EPIC-01) — endpoint list and category routing verified by code review only; no Playwright spec
**Effort:** M (~1 day)
**Provisional-Target:** v2.6

**Problem**
ST-02 added 10 missing endpoints to the health service and updated the SystemStatus.js count placeholder from 17 to 26. ST-03 added Alerts, Notifications, Digest category routing. Both were verified by code review only — no Playwright spec asserts the UI renders the categories correctly or that the count displays as 26.

**Scope**
- Write `tests/e2e/system-status.spec.js`
- Mock `POST /test/endpoints` response with controlled endpoint results covering `/alerts/rules`, `/notifications`, `/digest/weekly` (at minimum)
- Assert: Alerts category section visible; Notifications section visible; Digest section visible
- Assert: total endpoint count shown is ≥ 26 (or exact 26 if count is hardcoded in placeholder)
- Assert: none of the alert/notification/digest endpoints appear under "Other"

**Acceptance Criteria**
- `tests/e2e/system-status.spec.js` exists covering category routing and count display
- All assertions pass in headless Playwright
- Mock routes match the actual API path called by SystemStatus.js (`POST /test/endpoints`)


## 6. Operations & Infrastructure Backlog

---


## 7. Spec Debt Backlog

---

### BLG-SPEC-D17 — Spec Dependency Map
**Priority:** P3 (Low)
**Type:** Spec Debt / Governance Documentation
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260321-01 — promoted via roadmap rebalance 2026-04-05__scheduled (DL-018)
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.6

**Problem**
The canonical specification library has grown to ~22 documents with cross-references (e.g. `trade_history.md` references `metrics_definitions.md`; `signal_endpoints.md` references `strategy_rules.md`). When any canonical spec changes, cascade impacts on dependent specs are tracked informally. Without a dependency map, the DoQ cannot efficiently determine which specs require review when a canonical spec is updated — this weakens sign-off quality on spec-change PRs.

**Scope**
- Map all canonical spec dependencies: for each spec, list which other canonical specs it references or depends on
- Produce a read-only reference document at `docs/specs/spec_dependency_map.md`
- Include an explicit header note: "Point-in-time reference — last updated [date]. Accuracy not guaranteed after spec creation/revision without a manual update."
- Spec owners update the map when creating or significantly revising a canonical spec (courtesy update, not a governed obligation)
- Scope is read-only reference only — no CI enforcement or automated checking

**Acceptance Criteria**
- Reference document exists at `docs/specs/spec_dependency_map.md` listing all canonical specs and their known dependencies
- Document labelled as read-only reference with staleness acknowledgement
- All currently known cross-spec dependencies captured at time of authoring
- Head of Specs Team sign-off on completeness at authoring time

---

## 8. Governance Backlog

---

### BLG-GOV-08 — Engine prompt compression: roadmap_prompt and release_planning_prompt
**Priority:** P3 (Low)
**Type:** Governance Process / Technical Debt
**Owner:** Head of Specs Team
**Source:** AUD-2026-03-21 Tier 3 — engine prompt compression deferred (roadmap_prompt 1,581 lines; release_planning_prompt 1,534 lines)
**Effort:** L (~3–5 days)
**Provisional-Target:** v2.6 (deprioritised in v2.5 planning queue by BLG-FE-09 — 2026-04-05)

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


### BLG-GOV-11 — Cycle artefact inventory and maintenance review
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead + Head of Specs Team
**Source:** User session review — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.6

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

<!-- BLG-GOV-12 — Archived to backlog_archive.md 2026-04-10 (v2.5 post-ship closure) -->

### BLG-GOV-14 — Governance Health Score
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead + Head of Specs Team
**Source:** IDEA-pmo-lead-20260321-02 — promoted via roadmap rebalance 2026-04-05__scheduled (DL-019)
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.6

**Problem**
BLG-GOV-09 (cycle velocity metric) shipped in v2.4 tracking story completion rate. However, governance health across other dimensions — header compliance rates, deferred patch accumulation, and outstanding action age — is assessed informally at each rebalance run. Without a structured indicator, governance drift accumulates invisibly between cycles and is typically discovered at post-ship closure rather than at planning time.

**Scope**
- Define governance health score formula: (a) header compliance % = Class 4/5 docs with compliant headers / total checked; (b) deferred patch indicator = count of open deferred patches by age band (<1 cycle / 1–2 cycles / >2 cycles); (c) outstanding action count
- Document the formula canonically in `claude/system/OPERATIONAL_GUIDE.md` or a dedicated governance health spec
- Implement as a lightweight advisory check at STEP -1 of each roadmap rebalance (output: advisory indicator, not a gate)
- Score is advisory only — does not halt or gate the routine

**Acceptance Criteria**
- Governance health score formula documented canonically with all three components defined
- Score is computed and surfaced at STEP -1 of each roadmap rebalance as an advisory indicator
- Score labelled as advisory — cannot halt or gate the routine
- Head of Specs Team sign-off on formula definition before implementation

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

## 12. Last Release Slice — v2.4 (Archived)

<!-- release-plan-marker: RP:v2.4:2026-03-31__release-v2.4 — ARCHIVED 2026-04-03 -->

**Cycle:** 2026-03-31__release-v2.4 | **Shipped:** 2026-04-03 | **Status:** Verified_with_deviations
**Archived to:** `claude/backlog/backlog_archive.md` — v2.4 Release Slice entry

---

## Active Release Slice — v2.5

<!-- release-plan-marker: RP:v2.5:2026-04-05__release-v2.5 -->

**Cycle:** 2026-04-05__release-v2.5 | **Status:** Planning | **Published:** 2026-04-05
**Backlog slice:** `claude/cycles/2026-04-05__release-v2.5/stage4_backlog_slice.md`

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
**Provisional-Target:** v2.6

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
---

<!-- BLG-FEAT-15 — Archived to backlog_archive.md 2026-04-10 (v2.5 post-ship closure) -->

## 14. New Backlog Items — Session 2026-04-02

*User-raised items from session review. Not yet processed through a roadmap rebalance cycle. Target releases are indicative.*

---

<!-- BLG-OPS-11 — Archived to backlog_archive.md 2026-04-10 (v2.5 post-ship closure) -->

---

## 15. New Backlog Items — Session 2026-04-03

*Items raised from ST-11 performance baseline and System Status page review. Not yet processed through a roadmap rebalance cycle. Target releases are indicative.*

---

<!-- BLG-OPS-12, BLG-OPS-13, BLG-BE-07 — Archived to backlog_archive.md 2026-04-10 (v2.5 post-ship closure) -->

### BLG-OPS-14 — Enable Supabase Supavisor connection pooling on staging and production
**Priority:** P1 (High)
**Type:** Infrastructure / Operations
**Owner:** Infrastructure & Operations Owner
**Source:** ST-06 Head of Engineering investigation — 2026-04-10
**Effort:** XS (<1 hour — env var change + test)
**Provisional-Target:** v2.6

**Problem**
All DB-backed endpoints have p50 latency of 1.1–6s when measured externally because each request opens a fresh `psycopg2.connect()` to Supabase (no persistent connection pool). Supabase provides a built-in connection pooler — Supavisor — available on all plans including free tier. Switching to the Supavisor connection string (port 6543, `?pgbouncer=true`) requires no code changes and reduces per-connection establishment cost from ~1.5s to ~50–100ms, projecting p50 improvements of 1–4s for DB-heavy endpoints.

**Scope**
- Update `DATABASE_URL` environment variable on both staging and production Render services to use the Supabase Supavisor pooler connection string (available in Supabase dashboard → Project Settings → Database → Connection Pooling → Transaction mode)
- Verify all DB operations work correctly (psycopg2 is compatible with Supavisor in transaction mode)
- Re-run performance baseline (7 calls per endpoint) and update `docs/ops/api_performance_baseline.md` v1.2

**Acceptance Criteria**
- Supavisor pooler connection string in use on staging and production
- Baseline re-run shows p50 ≤ 500ms for at least the fast cluster endpoints; GET /portfolio and GET /notifications/preferences projected to improve by ≥1.5s
- No regression to DB correctness (reads and writes verified)

---

### BLG-BE-07-FIX — Refactor get_portfolio_summary() to use a single DB connection
**Priority:** P2 (Medium)
**Type:** Backend Engineering
**Owner:** Head of Engineering
**Source:** ST-06 Head of Engineering investigation — 2026-04-10
**Effort:** M (~half day)
**Provisional-Target:** v2.6

**Problem**
`get_portfolio_summary()` in `backend/services/portfolio_service.py` makes 4 sequential `get_db()` calls within a single request (get_portfolio, get_positions, get_total_deposits_withdrawals, get_drawdown_fields). Each call opens a new psycopg2 connection. At ~1.5s per connection on Supabase free tier, this accounts for ~6s p50. After Supavisor is enabled (BLG-OPS-14), this drops but the 4 round-trips remain inefficient. Consolidating to a single connection would also reduce Supavisor pool utilisation.

**Scope**
- Refactor `get_portfolio_summary()` to accept or create a single DB connection and pass it to `get_portfolio()`, `get_positions()`, `get_total_deposits_withdrawals()`, and `get_drawdown_fields()` as a shared context
- Update callsite signatures as needed — changes scoped to `portfolio_service.py` and `database.py` helper functions
- Should be done after BLG-OPS-14 so the pooling improvement is measured independently

**Acceptance Criteria**
- `GET /portfolio` makes 1 DB connection per request, not 4
- P50 for GET /portfolio after fix (with Supavisor) ≤ 400ms
- No regression to portfolio data correctness

---

<!-- BLG-FE-07, BLG-FE-08, BLG-GOV-10, TEST-GAP-EPIC-01-v24 — Archived to backlog_archive.md 2026-04-10 (v2.5 post-ship closure) -->

---

## 16. New Backlog Items — Session 2026-04-04

*Items raised from v2.4 post-ship closure. Not yet processed through a roadmap rebalance cycle. Target releases are indicative.*

---

### BLG-GOV-13 — Deduplicate backlog_archive.md duplicate item headers
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead
**Source:** Groom backlog v2.4 post-ship (2026-04-04) — ID uniqueness scan FAIL
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.6

**Problem**
`claude/backlog/backlog_archive.md` contains 50 duplicate `###` item headers — items that were archived in multiple separate grooming passes across prior cycles. The ID uniqueness scan in `backlog_management_prompt.md §4.5` flags this as FAIL every run. Duplicate headers create ambiguity about which archived entry is authoritative and make the archive unreliable as a historical record. Product Owner confirmation is required before deduplication can proceed (per the health report outstanding action).

**Scope**
- Product Owner to confirm deduplication approach: retain most recent entry per ID, or leave as historical record
- If deduplication approved: for each duplicated ID, retain the most recent (lowest in the file = latest archived) entry and remove earlier copies
- Validate that no active IDs are present in the archive after deduplication
- Run ID uniqueness scan post-deduplication and confirm PASS
- Update `backlog_archive.md` Last Updated header

**Acceptance Criteria**
- `backlog_archive.md` contains no duplicate `###` item headers
- ID uniqueness scan in next groom backlog run returns PASS
- Product Owner has confirmed the deduplication approach prior to execution

---

### BLG-FEAT-16 — AI Journal Summarisation
**Priority:** P3 (Low)
**Type:** Product Feature
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Source:** Initiative AI-SUM — gate cleared by Product Owner 2026-04-04 (SRB-v1.7)
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.6
**§13 Status:** CONDITIONALLY COMPLIANT — SRB-v1.7 (2026-03-02). Mandatory conditions below are non-negotiable and must appear in AC verbatim.
**Depends on:** Strategy Rules owner sign-off before any signal pipeline integration (SRB-v1.7 condition 3)

**Problem**
Trade journals accumulate over time and users must scroll through individual entries to extract patterns or themes from their past trading behaviour. A read-only AI-generated summary of a user's journal entries would reduce that effort and surface recurring themes or reflections without replacing the raw journal record. This is a UX convenience feature only — it does not affect the signal pipeline or any trading calculation.

**Scope**
- Backend: call an external LLM API to summarise a user's journal entries (entry/exit notes from closed trades); return summarised text
- Frontend: display the AI summary alongside (not instead of) the raw journal content on the Trade History page or a dedicated summary view
- Display an explicit disclaimer label per SRB-v1.7 condition 2 (see AC)
- AI summary output must not be persisted as a canonical record or used as a calculation input

**Acceptance Criteria**
- [ ] AI summary is displayed as a UX convenience view only — raw journal entries remain the source of truth and are visible alongside or accessible from the summary view
- [ ] AI summary output is NOT used as input to any signal, scoring, compliance, or recommendation calculation
- [ ] UI displays label: *"AI-generated summary — for reference only. Not a trading recommendation."* — label must be visible whenever the summary is shown, without requiring user interaction
- [ ] Strategy Rules owner has reviewed and confirmed the implementation does not integrate AI output into any signal pipeline (sign-off required before merge)
- [ ] Any future scope expansion beyond read-only display triggers a new §13 review before pre-alignment (documented in AC of that story)
- [ ] External LLM API key and configuration are managed via environment variable; no secrets in code

---

### BLG-BE-10 — Add supplementary indicator fields to signal generation
**Priority:** P3 (Low)
**Type:** Backend Engineering + Frontend / UX
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Source:** Initiative TECH-IND — gate cleared by Strategy Rules owner 2026-04-04
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.6
**§13 Status:** COMPLIANT (display-only scope) — SRB-v1.7 Feature 3. Scoring changes are explicitly out of scope and require a new §13 review + strategy_rules.md version bump before pre-alignment.

**Problem**
The current signal response provides `momentum_percent` (absolute price change over lookback), `atr_value`, and `volatility` for each signal. Users have no context for whether a signal's momentum is genuine outperformance vs. market drift, whether the stock is trading near meaningful price levels, or whether volume supports the move. These display-only additions serve the user's entry decision without altering the deterministic signal ranking.

**Scope**
Backend (`POST /signals/generate` response — new fields per signal):
- `relative_strength_pct`: stock `momentum_percent` minus the benchmark index momentum over the same `lookback_days` period (US stocks vs SPY; UK stocks vs FTSE). Positive = outperforming. Informational only — does not affect `rank`.
- `week52_high_proximity_pct`: how close the current price is to its 52-week high, as a percentage: `(current_price / 52_week_high - 1) * 100`. Negative means below high; 0 means at high.
- `avg_daily_volume_20d`: 20-day average daily volume for the stock. Liquidity context.
- `price_vs_50d_ma`: `"above"` or `"below"` — whether current price is above or below the 50-day moving average.

Frontend (Signals page):
- Display the four new fields as supplementary context columns or an expanded detail row on each signal card
- Label `relative_strength_pct` explicitly as "vs. benchmark (informational)" — it does not represent the signal's rank
- No UI shall allow the user to sort or filter by these fields in a way that reorders signals (rank is canonical)

**Acceptance Criteria**
- [ ] `POST /signals/generate` response includes all four new fields per signal object
- [ ] `relative_strength_pct` is computed as stock momentum minus benchmark momentum over the same `lookback_days`; US stocks benchmark SPY, UK stocks benchmark FTSE
- [ ] `relative_strength_pct` is labelled "vs. benchmark (informational)" in the UI and does not affect the `rank` field or signal ordering
- [ ] `week52_high_proximity_pct`, `avg_daily_volume_20d`, and `price_vs_50d_ma` are displayed as supplementary context; their display does not alter signal rank
- [ ] `signal_endpoints.md` updated to document the four new response fields
- [ ] `openapi.yaml` updated in the same commit as the contract change
- [ ] Strategy Rules owner confirms no scoring logic was modified (sign-off in QA evidence before merge)
- [ ] Any future proposal to incorporate any of these fields into signal ranking requires a new §13 review and strategy_rules.md version bump before pre-alignment — this constraint is documented in the QA evidence log

---

### BLG-FEAT-17 — Market Correlation Analysis
**Priority:** P3 (Low)
**Type:** Product Feature
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Source:** Initiative MKT-COR — gate cleared by Product Owner + Head of Engineering 2026-04-04
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.6
**Pipeline decision:** Yahoo Finance (existing pipeline) confirmed sufficient — `backend/utils/pricing.py` already ingests SPY/FTSE via `check_market_regime()`; extend to `range: "2y"` for correlation lookback. No new vendor or API key required.

**Problem**
Users have no visibility into how correlated their open positions or overall portfolio are with the broader market (SPY for US, FTSE for UK). Without this, a user with 8 US tech positions may believe they are diversified when their portfolio moves almost identically to SPY — the system shows individual position performance but not market-driven vs. stock-specific attribution. Market correlation analysis addresses this gap.

**Scope**
Backend:
- New analytics endpoint (e.g. `GET /analytics/market-correlation`) returning per-position and portfolio-level correlation coefficients vs. the relevant benchmark (SPY for US positions, FTSE for UK positions) over a configurable lookback (default 252 days)
- Fetch historical OHLC for each position ticker and its benchmark via Yahoo Finance (`range: "2y"` to cover the default lookback plus buffer); compute Pearson correlation coefficient over the overlapping date range for each position held during that period
- Response must be cached: TTL-based cache with minimum trading-day boundary (recalculate at most once per trading day). Correlation data changes slowly; recomputing on every page load is not acceptable.
- On-demand computation only — no SPY/FTSE time-series stored in the database

Frontend:
- Display correlation metrics on the Analytics/Reports page: per-position correlation badge and portfolio-weighted average correlation vs. benchmark
- Correlation scale: −1.0 (inverse) to +1.0 (perfect). Display as a signed decimal to 2dp with a colour indicator (e.g. >0.7 = high correlation warning, 0.3–0.7 = moderate, <0.3 = low)

**Acceptance Criteria**
- [ ] `GET /analytics/market-correlation` (or equivalent path) returns correlation coefficients for all open positions vs. their relevant benchmark (SPY/FTSE)
- [ ] Portfolio-level weighted average correlation is included in the response
- [ ] Correlation is computed as Pearson coefficient over the default 252-day lookback (or available history if shorter); lookback is a query parameter
- [ ] Response is cached with a TTL of at minimum one trading day — repeated calls within the same trading day return the cached result without re-fetching Yahoo Finance
- [ ] SPY/FTSE historical data is fetched on-demand; no index time-series is persisted to the database
- [ ] Frontend displays per-position correlation and portfolio average on the Analytics page with colour-coded severity (high/moderate/low)
- [ ] `openapi.yaml` updated in the same commit as the new endpoint
- [ ] If Yahoo Finance is unavailable, the endpoint returns a graceful error (not a 500 that breaks the page); cached data is served if available
- [ ] Engineer notes in QA evidence: if Yahoo Finance reliability becomes a problem, a formal data source review is required before any further correlation-dependent features

---
