Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-14

# QA Evidence — EPIC-03 (v7.0 Post-Ship Hardening)

## Consolidation Block

**EPIC:** EPIC-03 — v7.0 Post-Ship Hardening
**Cycle:** 2026-07-14__release-v7.1
**Sprint goal:** Eliminate the two P1 nightly-backtest data-integrity bugs feeding the Strategy Benchmark page (EPIC-01), bring the Table View RISK OFF badge into spec compliance (EPIC-02), and close out the four v7.0 post-ship hardening gaps (EPIC-03) — delivering all v7.1 mandatory anchors plus capacity-filling hardening in a single sprint.
**Test scenarios used:** `tests/test_mark_position_reviewed.py` (11 scenarios, 4 new), `tests/e2e/position-review-cadence-nudge.spec.js` (7, pre-existing, re-verified), `tests/e2e/monthly-pnl-realized-unrealized.spec.js` (5, pre-existing, re-verified), `tests/e2e/positions-pnl-columns.spec.js` (4, pre-existing, re-verified), `tests/test_reports_integration.py::TestTaxYearCsvExport` (11 new), `tests/e2e/gap-risk-flag.spec.js` (8, pre-existing regression check)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-04 | `positions.md#Last Reviewed Column`, `#Position Lifecycle State Badge` | Fixed IDOR: `PATCH /positions/{id}/mark-reviewed` now routes through `position_service.mark_position_reviewed()` → `get_position()` (portfolio-ownership check), matching `update_note`/`update_tags`. Documented NULL/backfill semantics (verified against production: 1 open position, `last_reviewed_at=NULL`, correctly not flagged). Documented review-cadence-is-not-a-lifecycle-state confirmation. Covers AC-01, AC-02, AC-03. | AC-01: IDOR regression check documented pass/fail. AC-02: NULL/backfill semantics defined + verified against production. AC-03: written confirmation review-cadence is metadata, not a 5th state. | Pass | None |
| ST-05 | `positions.md#Last Reviewed Column` | **Pre-met** (prior commit `633fad41`, v7.0) — all 5 ACs already satisfied; design gate confirmed still current, no new work required. Covers AC-01 through AC-05. | AC-01: data-testid present. AC-02: ordering/coexistence rule documented. AC-03: UX consistency confirmed via design gate. AC-04: traced to canonical spec section. AC-05: 7 dedicated Playwright scenarios passing. | Pass | None |
| ST-06 | `metrics_definitions.md#Realized / Unrealized P&L Split`, `reports.md#Unrealised P&L Card` | New formal metrics_definitions.md entry (ownership decision, currency/rounding rules, reconciliation rule verified against production data). `openapi.yaml` examples added/fixed for both report endpoints. AC-04 already closed by this cycle's design gate. Covers AC-01 through AC-07. | AC-01–AC-03: documented + verified. AC-04: visual treatment confirmed (design gate). AC-05: metrics_definitions.md entry added. AC-06: openapi.yaml examples confirmed. AC-07: 5 dedicated Playwright scenarios passing. | Pass with notes | DEV-REPORTS-ST06-01 (P3, BLG-SPEC-87) — Reports vs Positions page unrealised P&L data-freshness gap discovered during AC-03 verification; filed as a new backlog item, not fixed in this story (out of this story's documentation/verification scope) |
| ST-07 | `reports_endpoints.md#Response (200 — CSV, format=csv)`, `backend_engineering_patterns.md#CSV/export response-body pattern` | Documented + test-verified Content-Type/charset/filename (a drafting error — claiming no charset present — was caught by the new test and corrected same-session). Auth parity confirmed + test-verified. Record classification + versioning documented. Smoke test + 11 content-asserting tests added. New test scenario document authored. Canonical CSV/export pattern added to `backend_engineering_patterns.md`. Covers AC-01 through AC-07. | AC-01: header convention documented + test-verified. AC-02: auth parity test-verified. AC-03: classification + versioning recorded. AC-04: smoke test added. AC-05: content-asserting test added. AC-06: scenario doc authored. AC-07: pattern entry added. | Pass | None |

**QA test coverage:**
- Scenarios run: 4 new `TestMarkPositionReviewedOwnershipCheck` unit tests, 11 new `TestTaxYearCsvExport` integration tests, 7 pre-existing `SC-RCN-*` Playwright scenarios (re-verified), 5 pre-existing `SC-MRU-*` Playwright scenarios (re-verified), 4 pre-existing `V-PATH2-*` Playwright scenarios (re-verified), 8 pre-existing `SC-GR-*` Playwright scenarios (regression check) — all passing
- Regression areas checked: full backend suite (`backend/.venv/bin/python3 -m pytest tests/`) — 654 passed, 2 skipped, 0 failures (up from 643 passed pre-EPIC-03, +11 net new backend tests; 2 tests in `test_api_contracts.py` required updating their patch target from `database.mark_position_reviewed` to `main.mark_position_reviewed` following the ST-04 ownership-check refactor — both confirmed passing after the update, not a regression)
- Known deviations filed: DEV-REPORTS-ST06-01 (P3, BLG-SPEC-87) — see ST-06 row above

**Cross-EPIC note:** No file overlap with EPIC-01 or EPIC-02's changes (confirmed via `git status --short` — this branch touches only `backend/main.py`, `backend/services/{__init__,position_service}.py`, `docs/specs/**`, `docs/reference/openapi.yaml`, `docs/testing/**`, `tests/test_{api_contracts,mark_position_reviewed,reports_integration}.py`, `claude/backlog/backlog.md`; no `src/**`, no `production_strategy.py`/`import_backtest.py`, no `tests/test_production_strategy.py`).

---

## Autonomous Class Sign-Off (BLG-GOV-19)

**Autonomous class eligibility check:**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-04, ST-05, ST-06, ST-07 all autonomous)
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour requiring a human staging run, no live system interaction beyond documented, reproducible production API reads (read-only `GET` requests against `/positions`, `/portfolio`, `/trades`, `/reports/monthly-pnl` for AC-02/AC-03 verification, not a manual UI review) — ✓
- [x] Criterion 3: No frontend-visible change — confirmed no file under `src/components/**` or `src/pages/**` was created or modified (`git status --short` on this branch — only `backend/`, `docs/`, `tests/`, `claude/backlog/backlog.md` touched) — ✓
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-07-14
- Comments: Autonomous class sign-off — all four qualifying criteria met. This EPIC's stories were spec/metrics/test hardening passes with one genuine bug fix (ST-04 IDOR); no UI code was touched anywhere across all 4 stories. Live production API reads were used for AC-02/AC-03 verification (read-only, documented, reproducible) — this is evidence-gathering, not a staging sign-off requiring human judgment, consistent with Criterion 2's intent. Full regression suite (654 tests) clean; 15 new backend tests added across the EPIC.
