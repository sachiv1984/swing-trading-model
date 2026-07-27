Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-27

# QA Evidence — EPIC-05 (v7.8)

**EPIC:** EPIC-05 — Monthly realized P&L CSV export
**Cycle:** 2026-07-24__release-v7.8
**Sprint goal:** Ship all 12 v7.8 EPICs with every acceptance criterion met and QA sign-off recorded for each EPIC.
**Test scenarios used:** `tests/test_api_contracts.py` (`TestReportsEndpoints`), `tests/e2e/monthly-pnl-csv-export.spec.js` (new, SC-MCSV-01..05)

## ST-05 — Add monthly CSV export option alongside existing tax-year export

**Spec reference:** `docs/specs/api_contracts/reports_endpoints.md#CSV Export`, `docs/specs/frontend/pages/reports.md`
**Commit:** `9c1e6cd4` (implementation `e7bedcf4`)

**What was built:** `format=csv` added to the existing `GET /reports/monthly-pnl` endpoint (`build_monthly_pnl_csv`, mirrors `build_tax_year_csv` verbatim — plain header row + one row per month, no metadata block, matching the on-screen Monthly Financial Table exactly). Frontend `Download CSV` button added to `MonthlyPnlTable`'s header — verbatim reuse of `TaxYearReport`'s idle/generating/error interaction pattern, per the UX spec's explicit "no new pattern invented" decision.

**Note on CLAUDE.md §2 scope:** this story extends an *existing* endpoint with a query parameter rather than adding a new route decorator, so the `backend/routers/test.py` registration + `SystemStatus.js` fallback count + `SC-SS-01b` same-commit requirement does not apply (that rule targets new routes). `docs/reference/openapi.yaml` and `docs/specs/api_contracts/api_changelog.md` were still updated in the same commit since the endpoint's contract did change.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-05 | `reports_endpoints.md#CSV Export` | `format=csv` on `GET /reports/monthly-pnl` | Monthly CSV export available alongside existing tax-year export | Pass | None |
| ST-05 | (same) | Both exports sum `trade_history.pnl` directly, no separate computation | Monthly figures reconcile against tax-year export (no double-counting/drift) | Pass — verified at code-review level (see below) | None |
| ST-05 | `reports.md` | `Download CSV` button, verbatim Tax Year pattern | Export trigger UI follows existing export-control patterns | Pass | None |

**Reconciliation verification (code-review level, per the UX spec's own framing — "a verification check for QA evidence... not a UI-visible feature"):** read both `get_monthly_pnl()` (backend/database.py) and the tax-year trade query (`get_trade_history_by_tax_year`) — both directly `SUM`/aggregate the same `trade_history.pnl` column with no intermediate recalculation, so there is no double-counting or drift risk between the two exports at the ledger level. A literal numeric match between a *calendar*-year total in the monthly CSV and a *UK-tax*-year total in the Tax Year CSV is not expected for years where the two windows don't align (calendar Jan–Dec vs UK tax year Apr–Apr) — this is documented explicitly in `reports_endpoints.md` as an inherent property of the two different groupings, not a defect. A live database-backed reconciliation test with real seeded trade data was judged out of proportion to this story's scope given the AC's own "not a UI-visible feature" framing; the code-level verification above is the evidence.

**QA test coverage:**
- Backend: `tests/test_api_contracts.py::TestReportsEndpoints` — 2 new tests (`test_monthly_pnl_csv_format_returns_csv_download`, `test_monthly_pnl_invalid_format_returns_400`). Both pass. Also fixed a pre-existing test-file structural bug discovered while inserting these (a stray assertion line had been separated from its parent test method by a prior edit) — corrected in the same commit, unrelated to this story's own changes but caught during implementation.
- Frontend: `tests/e2e/monthly-pnl-csv-export.spec.js` — 5 scenarios (SC-MCSV-01..05: button visible, download fires with correct filename, generating-state spinner, error toast, empty-months still enabled), modeled directly on the existing `tax-year-csv-export.spec.js` pattern. **Actually executed locally on 2026-07-27** against a real Chromium (system `snap` browser via a local, uncommitted `executablePath` override, working around this sandbox's unsupported OS for Playwright's bundled browser download) — all 5 pass, no bugs found. Will still run in real CI at PR open for final confirmation.
- Regression: full backend suite (756 tests) — all pass, no behavioural change to any other endpoint.
- Known deviations filed: None.

**Shared-file rebase note:** this branch was cut from `main` before EPIC-01 merged. `openapi.yaml` (3.13.0→3.14.0) and `api_changelog.md` (new `v7.8.0` section) both need reconciliation once EPIC-01 actually merges, per the sprint's declared EPIC-01/05/06 shared-file cluster (`sprint_planning_notes.md`).

## Autonomous class eligibility check (BLG-GOV-19)

- Criterion 1 (all stories autonomous): ✓ — ST-05 is the only story, classified `autonomous`.
- Criterion 3 (no frontend-visible change): **✗ — FAILS.** This EPIC modifies `src/pages/Reports.js` (adds a new button, frontend-visible), which per the BLG-GOV-135 detection rule disqualifies the autonomous sign-off class.

**Autonomous class does not apply.** Standard sign-off (Director of Quality, human) is required below.

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [ ] Signed off by: Director of Quality
- Date: **[AWAITING SIGN-OFF]**
- Comments: Playwright tests (SC-MCSV-01..05) actually executed locally on 2026-07-27 — all 5 pass. Still needs CI-green confirmation as final confirmation before/alongside sign-off. This EPIC adds a frontend button, so BLG-GOV-19 autonomous sign-off does not apply — human Director of Quality review required per CLAUDE.md §2. Reconciliation AC verified at code-review level (documented above) rather than via a live-DB integration test — flag if DoQ wants a stronger reconciliation test before sign-off.
