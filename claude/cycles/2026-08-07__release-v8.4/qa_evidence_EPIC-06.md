Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-08

# QA Evidence — EPIC-06: QA & Test Infrastructure Hardening

**EPIC:** EPIC-06 — QA & Test Infrastructure Hardening
**Cycle:** 2026-08-07__release-v8.4
**Sprint goal:** Ship both available user-facing reporting enhancements while clearing a full-capacity slate of API contract & spec debt, backend hardening, frontend code health & security, operational reliability & cost monitoring, QA/test infrastructure, and governance-process integrity work across all 31 scoped stories.
**Test scenarios used:** `tests/test_api_contracts.py::TestPortfolioEndpoints::test_get_portfolio_history_returns_ok` (ST-25 fix), `tests/test_reports_integration.py::TestTaxYearCsvExport` + `tests/test_monthly_pnl_cost_basis.py` + `tests/test_api_contracts.py::TestReportsEndpoints::test_monthly_pnl_csv_format_returns_csv_download` (ST-27 regression check contents)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-25 | `tests/test_api_contracts.py` | Fixed wrong patch target in `test_get_portfolio_history_returns_ok` — was patching `main.get_portfolio`/`database.get_portfolio_snapshots` (definition/re-export sites, never actually called by the endpoint under test); corrected to `services.portfolio_service.get_portfolio`/`get_portfolio_snapshots` (the actual import site), per the file's own "Patch target rule" | Test passes with no outbound network/DB connection attempt; fix follows the file's documented Patch target rule | Pass | None |
| ST-26 | `docs/qa/regression_test_suite_baseline.md` | Backfilled Part 2 with all 41 previously-uncatalogued Playwright spec files (v5.9–v8.4), removed 1 stale entry for a deleted file (`si05-digest-delivery.spec.js`), corrected 7 stale scenario counts on already-catalogued rows. Totals: 86 files / 732 scenarios — verified to match `tests/e2e/` exactly (programmatic set-difference, zero files missing either direction) | Part 2 lists all spec files present in `tests/e2e/` at execution time; totals match exactly; Part 3 Arc coverage references every new file; DoQ sign-off recorded | Pass | None |
| ST-27 | `.github/workflows/csv-export-content-regression-check.yml` | Quarterly GitHub Actions scheduled workflow re-running the 3 existing CSV-content pytest targets (tax-year + monthly P&L) on a calendar cadence, independent of whether those files were touched by a given PR — catches drift introduced via shared utilities. Alerts via Telegram on failure, following the `api-key-cross-environment-check.yml` precedent pattern | Lightweight recurring regression check added confirming CSV export content stays correct; first instance run clean or findings filed | Pass | None |
| ST-28 | `docs/ops/blg_be_40_impact_measurement_query.sql`, `docs/ops/blg_be_40_impact_measurement_findings_2026-08-08.md` | Authored and ran (via Infrastructure & Operations Owner, production DB access) the `BLG-BE-40` impact measurement query — signals generated before the fix, for tickers not in the current active `ticker_universe`. Result: 0 of 300 pre-fix signals affected (genuine, non-vacuous zero, verified via a non-zero denominator) | Impact measurement query run against historical signals; count and magnitude of affected `suggested_shares` values identified; findings documented; reviewed by Metrics Definitions & Analytics Owner and Product Owner | Pass | None |

**QA test coverage:**
- Scenarios run: ST-25's fixed test (1/1 pass, verified with `DATABASE_URL` unset — no real DB/network reachable); ST-27's 3-target pytest suite (18/18 pass, run locally as pre-merge equivalent evidence since `workflow_dispatch` isn't available pre-merge — see the workflow file's own note); ST-26's 86-file/732-scenario table cross-checked programmatically against the live `tests/e2e/` directory.
- Regression areas checked: portfolio history endpoint (ST-25), CSV export content for both report types (ST-27), full Playwright/Part-1-endpoint regression baseline accuracy (ST-26).
- Known deviations filed: None. ST-23 (a *different* EPIC-05 story, reclassified for the same reason as ST-28) and ST-28 both matched the LL-v8.0-P3-01 infra/ops verification pattern — ST-28's own reclassification (`autonomous` → `delegated_backend`) is recorded in `execution_state.json`, not a spec deviation.

## Verification Readiness

| Field | Status |
|-------|--------|
| All spec references populated in execution_state.json | Yes |
| All P1–P3 deviations filed and backlog references updated | Yes — none found this EPIC; 1 out-of-scope finding filed as `BLG-BE-85` (EPIC-05's ST-19, not this EPIC — noted for cross-reference only) |
| QA evidence logs complete and DoQ sign-off non-blank for all EPICs | Yes (this EPIC) |

## BLG-GOV-19 Autonomous Class Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ via the **verification-class sub-criterion (LL-v4.5-EX-01)**: ST-25/26/27 are `autonomous`; ST-28 is `delegated_backend` (execution class, reclassified mid-sprint per LL-v8.0-P3-01 — production DB access required), but its *verification* is by document inspection only (the query and findings doc are reviewed as text/data, not by observing a running system component) — the sub-criterion's exclusion ("does not apply to EPICs with delegated_backend execution where the deliverable is a running system component") does not apply here, since ST-28's deliverable is an informational query + findings document, not a running system component.
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓ (test fixes, a documentation backfill, a CI workflow, and a query+findings doc — all reviewed as text/code; ST-28's underlying production data was supplied by a human in-session, not queried live by the engine)
- [x] Criterion 3: No frontend-visible change — ✓ (no `src/pages/` or `src/components/` files touched by any story in this EPIC)
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-08-08
- Comments: Autonomous class sign-off for the EPIC-level consolidation. **ST-28 carries its own additional, real human Product Owner sign-off** (not agent-mediated) recorded directly in `docs/ops/blg_be_40_impact_measurement_findings_2026-08-08.md` — the human confirmed the zero-impact finding in-session, going beyond what this autonomous-class block alone would represent. Product Owner acceptance of the PR itself and the merge-gate QA sign-off remain separate human gates per `CLAUDE.md` §2/§13 — not satisfied by this record alone.
