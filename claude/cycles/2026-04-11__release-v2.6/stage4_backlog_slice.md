**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.6
**Cycle:** 2026-04-11__release-v2.6
**Last Updated:** 2026-04-11

---

# Backlog Slice — v2.6 Backend Integration Completion, Test Automation & Governance Hardening

---

## EPIC-01 — Backend Integration Completion

**Maps to:** S2-01
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Sprint:** Sprint 1

Completes the migration from Base44 SDK data sources to authoritative FastAPI backend across the Reports Performance tab and Signals page. Eliminates data consistency risk between pages that use different data sources for P&L, positions, and cash balance.

### ST-01 — Migrate Reports Performance Tab to FastAPI Backend

**Backlog ref:** BLG-BE-08-GAP-01
**Effort:** L (~3–5 days)
**Priority:** P1

**Description:** The Reports page Performance tab fetches all data from the legacy Base44 SDK and computes all metrics client-side. Replace with calls to `/analytics/metrics`, `/trades`, and `/portfolio` FastAPI endpoints.

**Acceptance Criteria:**
- Performance tab fetches headline metrics from `/analytics/metrics`; no Base44 calls remain in the Performance tab
- Period selector drives backend-computed results
- P&L/win-rate/profit-factor figures consistent with Trade History and Portfolio pages
- ExportModal uses backend-sourced data (resolves GAP-R03 automatically)

---

### ST-02 — Wire Signals Page Dismissal and Position Creation to FastAPI

**Backlog ref:** BLG-BE-09-GAP-01
**Effort:** M (~1–2 days)
**Priority:** P1

**Description:** Signal dismissal and position creation on the Signals page use `base44.entities.Signal.update()` and `base44.entities.Position.create()`. Replace with FastAPI endpoints so signal state and positions are stored in the authoritative database.

**Acceptance Criteria:**
- Dismissing or entering a signal writes to FastAPI; no Base44 mutation calls remain for signal state or position creation
- Dismissed/entered signals are reflected in backend analytics
- Positions created via Signals page appear in Trade History and Portfolio pages

---

### ST-03 — Replace Base44 Cash Balance on Signals Page with GET /cash/summary

**Backlog ref:** BLG-BE-09-GAP-02
**Effort:** XS (<1 hour)
**Priority:** P2

**Description:** The `availableCash` value on the Signals page is sourced from `base44.entities.Portfolio.list()`. Replace with `apiFetch(GET /cash/summary)` for consistency with the authoritative backend cash balance.

**Acceptance Criteria:**
- `availableCash` on Signals page matches the value shown on the Cash/Portfolio pages
- No Base44 portfolio query remains solely for cash balance purposes

---

## EPIC-02 — Test Automation & CI Hardening

**Maps to:** S2-02
**Owner:** QA & Testing Owner + Infrastructure & Operations Owner
**Sprint:** Sprint 1

Fixes blocking pytest collection errors, adds a CI test runner workflow, and delivers Playwright and backend unit tests for the fee drag metric (SC-FEE-01 through SC-FEE-06).

### ST-04 — Fix 4 Pytest Collection Errors

**Backlog ref:** BLG-QA-09
**Effort:** S (~2–3 hours)
**Priority:** P1

**Description:** Four test files fail at collection time, making 0% of integration tests runnable in CI. Fix `API_TITLE` export, `update_position` stub, and `DATABASE_URL` conftest.

**Acceptance Criteria:**
- `pytest tests/` collects all test files without collection errors
- All previously clean tests (`test_stop_reconciliation.py`, `test_watchlist_service.py`) still pass after changes
- `conftest.py` does not interfere with test isolation (dummy DATABASE_URL not used in test logic)
- Fixes: Add `API_TITLE` to `backend/config.py`; stub `update_position` in `test_service_coverage.py`; add `tests/conftest.py` setting dummy `DATABASE_URL`

---

### ST-05 — Add CI Test Runner Workflow

**Backlog ref:** BLG-QA-10
**Effort:** S (~1 hour)
**Priority:** P2
**Dependency:** ST-04 (for Phase B)

**Description:** No GitHub Actions workflow runs pytest on PR. Add `.github/workflows/ci-tests.yml` — Phase A (clean tests) runnable immediately; Phase B (all tests) after ST-04.

**Acceptance Criteria:**
- `.github/workflows/ci-tests.yml` exists and runs on PR
- Phase A: `test_stop_reconciliation.py` and `test_watchlist_service.py` run on every PR
- A deliberate formula break in `position_manager.py` causes the workflow to fail
- Workflow does not require `DATABASE_URL` secret for Phase A tests

---

### ST-06 — Fee Drag Playwright Spec

**Backlog ref:** BLG-QA-07
**Effort:** M (~1–2 days)
**Priority:** P2

**Description:** Write `tests/e2e/fee-drag-trade-history.spec.js` covering SC-FEE-01 through SC-FEE-04. Follow the `slippage-tracking.spec.js` mock pattern.

**Acceptance Criteria:**
- `tests/e2e/fee-drag-trade-history.spec.js` exists covering SC-FEE-01 to SC-FEE-04
- All 4 scenarios pass in headless Playwright (Chromium)
- Spec runs cleanly alongside `slippage-tracking.spec.js` without interference
- `fee-drag-scenarios.md` updated: SC-FEE-01–04 automation entries updated from pending to confirmed spec file path

---

### ST-07 — Fee Drag Backend Pytest Unit Tests

**Backlog ref:** BLG-QA-08
**Effort:** S (~0.5 day)
**Priority:** P2

**Description:** Write `tests/test_trade_service.py` covering SC-FEE-05 and SC-FEE-06. Stub DB imports using the `sys.modules` pattern from `test_alerts_service.py`.

**Acceptance Criteria:**
- `tests/test_trade_service.py` exists and runs cleanly under `pytest` (no collection errors)
- SC-FEE-05 and SC-FEE-06 assertions pass
- No live DB call — all DB dependencies stubbed at import time
- Added to clean test suite runnable in CI alongside `test_stop_reconciliation.py` and `test_watchlist_service.py`

---

## EPIC-03 — Frontend UX Polish

**Maps to:** S2-03
**Owner:** Frontend Specifications & UX Owner + Head of UX & Design
**Sprint:** Sprint 2

Addresses UX observations from the v2.5 Trade History staging run: StatsCard tooltip capability, 6-card layout squeeze, column header legibility, and flexible column sorting. ST-09/ST-10/ST-11 require Head of UX design decisions before implementation.

### ST-08 — StatsCard Tooltip Prop

**Backlog ref:** BLG-FE-10
**Effort:** XS (<1 hour)
**Priority:** P3

**Description:** Add an optional `tooltip` prop to `StatsCard.js`. Wire tooltip on Avg Fee Drag and Avg Entry Dev. StatsCards per canonical spec requirements.

**Acceptance Criteria:**
- `StatsCard` accepts an optional `tooltip` prop (string); when absent, no ⓘ icon renders (no regression)
- When `tooltip` is provided, an ⓘ icon is visible adjacent to the card title; hovering reveals the tooltip text
- Avg Fee Drag StatsCard in Trade History displays the canonical tooltip text from `trade_history.md` v1.5 §Avg Fee Drag
- No regression to any other StatsCard usage across the app

---

### ST-09 — Trade History StatsCard Bar Layout (6-Card Width)

**Backlog ref:** BLG-FE-11
**Effort:** S (~0.5 day)
**Priority:** P3
**Design dependency:** Head of UX to define target grid/layout spec before implementation

**Description:** The Trade History StatsCard summary bar is visually crowded at 6 cards at standard viewports. Head of UX to define the correct treatment (grid spec, xl breakpoint, or overflow pattern); implement per spec.

**Acceptance Criteria:**
- Head of UX reviews the 6-card layout and defines the target grid/layout spec
- Implementation delivers the spec without regression to individual card content
- All 6 cards readable and unstacked at a reasonable viewport width (to be defined by UX)

---

### ST-10 — Trade History Column Header Styling and Formatting

**Backlog ref:** BLG-FE-12
**Effort:** S (~0.5 day)
**Priority:** P3
**Design dependency:** Head of UX to define improved header style before implementation

**Description:** Column headers in the Trade History table use the `DataTable.js` default (`text-xs font-medium text-slate-400 uppercase`). Head of UX to define improved header style; implement per spec.

**Acceptance Criteria:**
- Head of UX defines target header style
- Implementation updates `DataTable.js` `TableHead` base styles (or Trade History-specific overrides) to match spec
- No regression to other tables using `DataTable.js`

---

### ST-11 — Flexible Column Sorting Across Trade History Table

**Backlog ref:** BLG-FE-13
**Effort:** M (~1–2 days)
**Priority:** P3
**Design dependency:** Head of UX to define sorting strategy before implementation

**Description:** Only 3 columns currently sortable in Trade History (Slippage, Fee Drag %, R-Multiple). Head of UX to decide sorting strategy (all columns, curated set, or multi-column). `DataTable.js TableHead` onClick infrastructure exists (fixed v2.5). Implement per spec.

**Acceptance Criteria:**
- Head of UX defines which columns are sortable and the sort interaction model
- Implementation wires sort handlers for all specified columns
- Sort icon treatment consistent across all sortable columns
- No regression to existing Slippage, Fee Drag %, R-Multiple sort behaviour

---

## EPIC-04 — Governance & Spec Debt

**Maps to:** S2-04
**Owner:** Head of Specs Team
**Sprint:** Sprint 2

Applies two v2.5 carry-forward governance patches, upgrades the decision_log.md guard to a structural hard gate (BLG-GOV-15), and delivers the Frontend Performance Budget spec (BLG-FE-09).

### ST-12 — execution_prompt.md STEP 5.1 Unpushed-Commit Check

**Backlog ref:** v2.5 CF-1 (lessons_learnt_closure.md carry-forward)
**Effort:** S (~0.5 day)
**Priority:** P1 governance

**Description:** Extend execution_prompt.md STEP 5.1 QA Evidence File Existence Check to also verify the exec branch has been pushed to origin before sprint close. Unpushed commits containing qa_evidence files should be a soft gate requiring explicit push before sprint close is accepted.

**Acceptance Criteria:**
- execution_prompt.md STEP 5.1 includes a check: `git log --not origin/<branch>` — if any unpushed commits are present at sprint close, they must be listed and the engine must push or flag
- An unpushed commit including a qa_evidence file is a soft gate requiring explicit push before sprint close proceeds
- §6 governance file edit checklist applied: version bump, OPERATIONAL_GUIDE §14 update, prompt_change_log.md entry
- CF-1 carry-forward item closed

---

### ST-13 — Prompt Log Hygiene: §6 Edit Reminders for 3 Engines

**Backlog ref:** v2.5 CF-2 (lessons_learnt_closure.md carry-forward)
**Effort:** M (~1–2 days)
**Priority:** P2 governance

**Description:** Add CLAUDE.md §6 governance file edit reminders to design_gate_prompt.md, amendment_cycle_prompt.md, and roadmap_prompt.md. Same STEP 8 pattern already applied to execution_prompt.md via ST-12 in v2.5.

**Acceptance Criteria:**
- `design_gate_prompt.md`: applicable commit/finish step includes §6 edit reminder — if any §6-governed file was modified during design gate execution, append to prompt_change_log.md
- `amendment_cycle_prompt.md`: applicable commit step includes §6 edit reminder per CLAUDE.md §6
- `roadmap_prompt.md`: applicable commit step includes §6 edit reminder per CLAUDE.md §6
- §6 governance file edit checklist applied to all 3 files (version bumps, OPERATIONAL_GUIDE §14 updates, prompt_change_log.md entries)
- CF-2 carry-forward item closed

---

### ST-14 — Upgrade decision_log.md Hard Gate in roadmap_prompt.md

**Backlog ref:** BLG-GOV-15
**Effort:** M (~0.5–1 day)
**Priority:** P2

**Description:** roadmap_prompt.md STEP 9 currently has a pre/post count check as an assertion (does not halt on failure). Upgrade to a structural hard gate that halts if decision_log.md line count decreases. Update OPERATIONAL_GUIDE.md §1 description from "governance convention" to "enforced structurally."

**Acceptance Criteria:**
- `roadmap_prompt.md` STEP 9 halts execution if `decision_log.md` line count after write is less than before
- `OPERATIONAL_GUIDE.md §1` Hard Rules table reflects structural enforcement
- §6 governance file edit checklist applied for both files (version bumps, §14 update, prompt_change_log.md entries)
- BP-05 compliance confirmed at next audit

---

### ST-15 — Frontend Performance Budget Spec

**Backlog ref:** BLG-FE-09
**Effort:** S (~0.5 day)
**Priority:** P3

**Description:** Define maximum acceptable frontend performance targets (page load time, JS bundle size) and document measurement methodology. Produce spec at `docs/specs/frontend/performance_budget.md`.

**Acceptance Criteria:**
- Spec document exists at `docs/specs/frontend/performance_budget.md` defining page load and bundle size targets
- Targets aligned to BLG-OPS-05 API latency floor (total acceptable load time includes backend latency + frontend rendering overhead)
- Measurement methodology documented (reproducible baseline approach stated)
- Scope is documentation only — no code instrumentation required in this item
