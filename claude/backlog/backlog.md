# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-04-16 (post-ship closure v2.7: 11 shipped items marked ✅ COMPLETE; BLG-GOV-18 + BLG-GOV-19 added and completed; BLG-QA-13 added; BLG-QA-12 ID corrected per OA-5)
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

## 3. Frontend & UX Backlog

---

### BLG-FE-11 — Trade History StatsCard bar layout: squeeze at 6-card width
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Owner
**Source:** EPIC-03 DoQ staging run 2026-04-10 — adding Avg Fee Drag card (6th card) causes visible squeeze on the Trade History summary bar at standard viewport widths
**Effort:** S (~half day)
**Provisional-Target:** v2.8
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
**Provisional-Target:** v2.8
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
**Provisional-Target:** v2.8
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
**Provisional-Target:** v2.8

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
**Provisional-Target:** v2.8

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
**Provisional-Target:** v2.8

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
**Provisional-Target:** v2.8

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
**Provisional-Target:** v2.8

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
**Provisional-Target:** v2.8
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
**Provisional-Target:** v2.8
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
**Provisional-Target:** v2.8

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
**Provisional-Target:** v2.8
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

<!-- BLG-QA-12 (formerly BLG-QA-11 System Status spec) — Archived to backlog_archive.md 2026-04-16 (v2.7 post-ship closure) — ST-07 (EPIC-03) — ID renamed BLG-QA-11→BLG-QA-12 per OA-5 -->


## 6. Operations & Infrastructure Backlog

---


## 7. Spec Debt Backlog

---

<!-- BLG-SPEC-D17 — Archived to backlog_archive.md 2026-04-16 (v2.7 post-ship closure) — ST-10 (EPIC-05) -->

---

## 8. Governance Backlog

---

### BLG-GOV-08 — Engine prompt compression: roadmap_prompt and release_planning_prompt
**Priority:** P3 (Low)
**Type:** Governance Process / Technical Debt
**Owner:** Head of Specs Team
**Source:** AUD-2026-03-21 Tier 3 — engine prompt compression deferred (roadmap_prompt 1,581 lines; release_planning_prompt 1,534 lines)
**Effort:** L (~3–5 days)
**Provisional-Target:** v2.8 (deprioritised in v2.5 planning queue by BLG-FE-09 — 2026-04-05)

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
**Provisional-Target:** v2.8

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

<!-- BLG-GOV-14 — Archived to backlog_archive.md 2026-04-16 (v2.7 post-ship closure) — ST-11 (EPIC-05) -->

---

### BLG-GOV-15 — Upgrade decision_log.md append-only rule to structural hard gate
**Priority:** P2 (Medium)
**Type:** Governance Process / Technical Debt
**Owner:** Head of Specs Team
**Source:** AUD-2026-04-11-002 — Tier 2 (BR 4, Medium effort)
**Effort:** M (~0.5–1 day)
**Provisional-Target:** v2.8

**Problem**
`OPERATIONAL_GUIDE.md §1` currently classifies the `decision_log.md` append-only rule as "a governance convention, not a hard gate." Every roadmap rebalance writes to `decision_log.md` without a structural guard, meaning deletions or edits to prior entries are process violations that would not be caught until a manual review. With 10+ completed cycles and an ever-growing decision log, the blast radius of an undetected edit is high.

Note: `roadmap_prompt.md` v2.2 (2026-03-14) added a pre/post count check at STEP 9, but this is an assertion — it does not halt on failure — and the OPERATIONAL_GUIDE §1 description was not updated at that time.

**Scope**
- `roadmap_prompt.md` STEP 9: upgrade existing count check from assertion to STRUCTURAL (halt if line count decreases)
- `OPERATIONAL_GUIDE.md §1` Hard Rules table: update description from "governance convention, not a hard gate" to "enforced structurally in Roadmap Engine STEP 9 via pre/post line-count check"

**Acceptance Criteria**
- `roadmap_prompt.md` STEP 9 halts execution if `decision_log.md` line count after write is less than before
- `OPERATIONAL_GUIDE.md §1` Hard Rules table reflects structural enforcement
- §6 governance file edit checklist applied for both files (version bumps, §14 update, prompt_change_log.md entries)
- BP-05 compliance confirmed at next audit

---

<!-- BLG-GOV-18 — Archived to backlog_archive.md 2026-04-16 (v2.7 post-ship closure) — ST-03 (EPIC-02) -->

<!-- BLG-GOV-19 — Archived to backlog_archive.md 2026-04-16 (v2.7 post-ship closure) — ST-04 (EPIC-02) -->

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

**Cycle:** 2026-04-05__release-v2.5 | **Status:** Closed | **Published:** 2026-04-05
**Backlog slice:** `claude/cycles/2026-04-05__release-v2.5/stage4_backlog_slice.md`

---

## Active Release Slice — v2.6

<!-- release-plan-marker: RP:v2.6:2026-04-11__release-v2.6 — ARCHIVED -->

**Cycle:** 2026-04-11__release-v2.6 | **Status:** Closed | **Published:** 2026-04-11 | **Shipped:** 2026-04-11
**Backlog slice:** `claude/cycles/2026-04-11__release-v2.6/stage4_backlog_slice.md`

## Active Release Slice — v2.7

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
**Provisional-Target:** v2.8

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

<!-- BLG-OPS-14 — Archived to backlog_archive.md 2026-04-16 (v2.7 post-ship closure) — ST-01 (EPIC-01) -->

<!-- BLG-BE-07-FIX — Archived to backlog_archive.md 2026-04-16 (v2.7 post-ship closure) — ST-02 (EPIC-01) -->

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
**Provisional-Target:** v2.8

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
**Provisional-Target:** v2.8
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

<!-- BLG-BE-10 — Archived to backlog_archive.md 2026-04-16 (v2.7 post-ship closure) — ST-09 (EPIC-04) -->

<!-- BLG-FEAT-17 — Archived to backlog_archive.md 2026-04-16 (v2.7 post-ship closure) — ST-08 (EPIC-04) — AC-6 frontend rendering deferred (BLG-FE-14 to be filed) -->

<!-- BLG-GOV-16 — Archived to backlog_archive.md 2026-04-16 (v2.7 post-ship closure) — ST-05 (EPIC-02) -->

<!-- BLG-QA-11 — Archived to backlog_archive.md 2026-04-16 (v2.7 post-ship closure) — ST-06 (EPIC-03) -->

### BLG-QA-13 — Test scenario coverage gap: market correlation and supplementary indicators (v2.7)
**Priority:** P3 (Low)
**Type:** Test Coverage
**Owner:** QA & Testing Owner
**Source:** v2.7 delivery verification (TEST-GAP-v27-EPIC04-01) — EPIC-04 ST-08 and ST-09 delivered new backend functionality verified by code review; registered test_scenarios (analytics_scenarios.md v1.0, signals_scenarios.md v1.0) cover prior cohort analysis and signals page frontend, not the new v2.7 endpoints and fields
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.8

**Gap description**
Two scenario files were registered in execution_state.json for EPIC-04 (`docs/testing/analytics_scenarios.md`, `docs/testing/signals_scenarios.md`) but these predate v2.7 and cover different functionality:
- `analytics_scenarios.md` v1.0 (2026-03-17) — covers `GET /analytics/cohort`, not the new `GET /analytics/market-correlation` endpoint
- `signals_scenarios.md` v1.0 (2026-03-18) — covers Signals page frontend behaviour, not the four new supplementary indicator fields

No scenarios exist that exercise:
1. `GET /analytics/market-correlation` happy path, cache behaviour, fallback on Yahoo Finance unavailability, or severity classification
2. `POST /signals/generate` with the four new supplementary fields (`relative_strength_pct`, `week52_high_proximity_pct`, `avg_daily_volume_20d`, `price_vs_50d_ma`)

**Recommended scenarios**
- SC-CORR-01: `GET /analytics/market-correlation` returns per-position Pearson correlation with correct fields
- SC-CORR-02: portfolio-level weighted average correlation included in response
- SC-CORR-03: 8h cache returns same result on second call within TTL
- SC-CORR-04: graceful partial response when Yahoo Finance unavailable for one ticker
- SC-SIG-IND-01: `POST /signals/generate` response includes all four supplementary fields per signal object
- SC-SIG-IND-02: `relative_strength_pct` is None when benchmark data unavailable (not error)

**Acceptance Criteria**
- [ ] `docs/testing/analytics_scenarios.md` updated (or new file created) to include SC-CORR-01 through SC-CORR-04
- [ ] `docs/testing/signals_scenarios.md` updated (or new file created) to include SC-SIG-IND-01 and SC-SIG-IND-02
- [ ] All new scenarios reference `analytics_endpoints.md v2.1.0` and `signal_endpoints.md v1.1` as canonical spec
