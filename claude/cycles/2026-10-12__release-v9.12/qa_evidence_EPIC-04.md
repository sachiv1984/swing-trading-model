Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-15

# QA Evidence — EPIC-04 — Security, Operations & Platform

**EPIC:** EPIC-04 — Security, Operations & Platform
**Cycle:** 2026-10-12__release-v9.12
**Branch:** exec/2026-10-12__release-v9.12/EPIC-04
**Sprint goal:** Restore AI journal summaries for UUID trade IDs (BLG-BE-162, P1); make signal sizing, stops and position status correct across Signals, Positions and Risk; and let Trade Entry show the stop, risk and size before save. Also ship v9.12's accessibility, security, operations, spec and governance hygiene items.

Per-story entries are recorded as each story completes or is delegated (STEP 3.1.A/3.1.C). The EPIC-level consolidation block and sign-off are added at STEP 3.2.A, once every story is `done`.

---

## Stop-health monitor: no false alert on the morning grace ends

- **Story:** ST-25 (BLG-OPS-184), autonomous
- **Spec references:** `scripts/check_post_grace_stop_health.py` (docstring); `tests/test_post_grace_stop_health.py`
- **Commit:** `e2008a07945cf5993025f1a3f8ea603c2e53a43c`; AC 1 and AC 2 pre-met on `main` by `3b63929d` (v9.11, `[EPIC-03][ST-18]`)
- **Acceptance criteria and evidence:**
  - AC 1, the day-10 fixture passes and `non_s11_multiplier.json` / `missing_stop.json` still fail: `test_day10_position_awaiting_first_recompute_passes`, `test_non_s11_multiplier_fails`, `test_missing_post_grace_stop_fails`. Pass.
  - AC 2, a null multiplier past the tolerance window is still a violation: `test_pending_window_ends_after_the_tolerance`, `test_null_multiplier_after_a_recompute_is_still_a_violation`. Pass.
  - AC 3, chosen option recorded in the docstring: option (a), with option (b) noted as not taken (it would change live stop behaviour and need a Strategy Rules ruling). Pinned by `test_docstring_records_the_chosen_option`. Pass.
- **Test run:** `tests/test_post_grace_stop_health.py` 13/13 locally; CI Pytest Suite green on the branch.
- **Deviations:** none found.

## Local setup installs requirements-dev.txt

- **Story:** ST-31 (BLG-OPS-185), autonomous
- **Spec references:** `README.md` (Backend setup); `docs/ops/quarterly_dependency_upgrade_cadence_policy.md` v1.2
- **Commit:** `7507ef856c9589d8aa4c48dc3cf973a65147c90a`
- **Acceptance criteria and evidence:**
  - AC 1, a fresh-clone venv built per `README.md` collects: verified 2026-10-15 from a fresh clone. The venv (`python3 -m venv`; `pip install -r requirements.txt -r requirements-dev.txt`) has pytest, and `pytest --collect-only -q tests/` collects 2674 tests with no error. The sandbox has only Python 3.14 (no pyenv), so the pinned-3.11 path is evidenced by CI (`ci-tests.yml` Phase B on 3.11, run 38701270136: 2673 collected, 2666 passed). A bare `pytest --collect-only -q` from the repo root also collects `backend/mutmut_pilot_tests/` and fails the BLG-QA-190 leak guard (2690 collected, 1 error). This is pre-existing and not caused by the setup docs; filed as **BLG-QA-225**. Pass with notes.
  - AC 2, `grep -rn "pip install -r .*requirements.txt" README.md docs/ops/quarterly_dependency_upgrade_cadence_policy.md` shows `requirements-dev.txt` on both lines. Pass.
- **Deviations:** none found. Incidental finding BLG-QA-225 (backlog item, not a deviation).

## Scheduled GitHub workflows inventory

- **Story:** ST-32 (BLG-GOV-371), autonomous
- **Spec references:** `docs/ops/scheduled_workflows_inventory.md` v1.0 (created)
- **Commit:** `ea5342456f6deaec66cb131fd8bc1509195212db`
- **Acceptance criteria and evidence:**
  - AC 1, one table in `docs/ops/` with every scheduled workflow, owner, cron, a "writes" column and minutes/month, and a statement that it is reviewed at each `run audit`: 23 workflows (`grep -l '^\s*schedule:' .github/workflows/*.yml`), writes traced from each endpoint/script to its SQL, minutes from 30 days of scheduled runs (about 1,032/month). Review cadence stated in §Why this document exists. Pass (document inspection).
- **Deviations:** none found. Incidental finding **BLG-OPS-188** (`ci-usage-report.yml` failed its only scheduled run at "Commit report").

## Settings change audit trail and last-change line

- **Story:** ST-26 (BLG-SEC-41), delegated_backend (live migration only; code autonomous)
- **Spec references:** `docs/specs/data_model.md` DS-33 (v2.62); `docs/specs/api_contracts/settings_endpoints.md` v1.5.0 (`GET /settings` §Settings change log); `docs/specs/frontend/pages/settings.md` §Last Change Line (v1.9); `tests/test_settings_change_log.py`; `tests/e2e/settings-last-change.spec.js`
- **Commit:** `87dea43a30b84f39ecec663d92db22235687b825` (engine; code, tests, docs)
- **Acceptance criteria and evidence:**
  - AC 1, every settings write produces a log row with field, old value, new value, timestamp and request source: `tests/test_settings_change_log.py` (16 tests: PATCH per-field rows, one batch per save, source tagging and fallback, same-transaction ordering, create logs every non-null column, `GET /settings` `last_change`). Interpretation, recorded under the intent check: a PATCH that changes no value logs nothing, so `last_change` always names a real change.
  - AC 2, the Settings page shows the last change (Playwright): SC-SLC-01..05, all passing locally on a fresh production build (15/15 Settings specs; axe scan 18/18). CI: Playwright run 38703606378 on `87dea43a` green (all shards). Pass.
  - AC 3, migration recorded in `data_model.md` (DS-33) and applied on staging and production with verification output: applied 2026-10-15 by the user (human, acting for the Data Model & Domain Schema Owner) on both, with Row Level Security enabled (no policies) after Supabase flagged the table. Both returned 8 columns and 2 indexes as expected. Recorded in DS-33 Live Confirmation. Pass.
  - Open check, not an AC: confirm the deployed backend's `DATABASE_URL` role is `postgres` (or `postgres.<ref>`). That role bypasses RLS. Any other role would have its change-log writes blocked. The first staging settings save after EPIC-04 deploys is the end-to-end proof.
- **Status:** done (DEL-20261015-01 unblocked in-session).

## Dependency patch/minor bumps from the October 2026 review

- **Story:** ST-28 (BLG-TECH-22), delegated_qa
- **Spec references:** `docs/security/dependency_update_review_2026-10-06.md` §3–§5; `backend/requirements.txt`; `backend/requirements-dev.txt`; `package.json`; `package-lock.json`
- **Commit:** `2909e67e2fbe7d47d1d6b8d933f09aeedb42dfd4`
- **Correction (2026-10-15, after the Render staging build failed):** `numpy` 2.5.3 requires Python ≥ 3.12, and the backend is pinned to 3.11.0. The Render staging build and CI Pytest Suite failed on every push from `2909e67e` ("No matching distribution found for numpy==2.5.3"). The engine checked only the Playwright run and missed it; the local venv is Python 3.14, so the bad pin installed there. numpy is reverted to 2.4.6, the newest 3.11 release. All other requirements now resolve for Python 3.11 (`pip download --python-version 3.11`), and the full suite passes again (2668 passed, 21 skipped). AC 1 is therefore 7 of 8 backend bumps plus 20 frontend: **Pass_with_deviation**, tracked in **BLG-TECH-24**.
- **What was built:** the 8 backend and 20 frontend "Batch" bumps, each at exactly the reviewed version (npm's caret resolution first pulled newer, unreviewed releases; re-pinned). `pip check` clean; non-registry dependency check passed. CI's Playwright browser cache is keyed on the lockfile's `@playwright/test` version, so the browser install follows the bump without a workflow edit.
- **Acceptance criteria and evidence:**
  - AC 1, all bumps in one PR, full pytest and all Playwright shards pass in CI incl. focus-restoration specs: locally full pytest 2668 passed / 21 skipped; 84/84 Playwright on a fresh build (`compliance-recheck`, `entry-checklist`, `epic03-v34-frontend` focus specs; dialog, modal, Settings, axe). CI: Playwright run 38704880394 on `2909e67e` green, all shards, including the focus-restoration specs (observed in real GitHub Actions CI). No file under `src/`, `tests/e2e/`, `package.json` or `package-lock.json` changed after it. CI Pytest Suite green on `4736cf27` (38725094192) and `2fb6f888` (38725364575), Python 3.11. numpy held at 2.4.6 (see Correction). Pass_with_deviation (BLG-TECH-24).
  - AC 2, staging yfinance price and ATR for one US and one UK ticker: the user (acting for the Infrastructure & Operations Owner) pointed the staging backend at the EPIC-04 branch and deployed `2fb6f888` (yfinance 1.7.0, numpy 2.4.6; build succeeded). `GET /market/atr/AAPL?market=US` returned `status: ok`, ATR 6.5814 (period 14, as_of 2026-10-15T12:03:52Z). `GET /market/atr/VOD?market=UK` returned `status: ok`, ATR 0.03197 (period 14, as_of 2026-10-15T12:05:03Z; pounds, the existing pence-to-pounds convention). Both match the local yfinance 1.7.0 figures (AAPL 6.58, VOD.L 0.032), and the ATR path fetches the price history from yfinance, so both fetches work for both markets. The user then returns the staging backend's branch to `main`. Pass (DEL-20261015-04, human staging check, 2026-10-15).
- **Test scenarios to execute:** full `tests/` pytest; all Playwright shards in CI; the staging check above.
- **CI so far:** CI Pytest Suite green on `4736cf27` (38725094192) and `2fb6f888` (38725364575); Critical-Path Smoke Tests (Playwright) green on `2fb6f888` (38725364700). Full Playwright shards: run 38704880394 above.
- **QA findings (Director of Quality):** 27 of 28 bumps applied at the reviewed versions; numpy 2.5.3 is unreachable on the pinned Python 3.11.0, so it was held at 2.4.6. The gap is disclosed here and tracked in BLG-TECH-24 (hold numpy at 2.4.x until Python 3.12+, and add a pinned-Python resolve check). The miss came from reading only the Playwright CI conclusion. STEP 3.1.A step 4c's Playwright check passed while CI Pytest was red. Worth a lessons-learnt entry: check every CI workflow's conclusion before `done`, not just Playwright. AC 2 met by the human staging check.
- **Disposition (Pass / Pass with notes / Fail):** Pass_with_deviation (BLG-TECH-24). Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3), 2026-10-15.

## Bundled frontend API key re-assessment

- **Story:** ST-27 (BLG-SEC-42), delegated_decision, reclassified autonomous on resolution
- **Spec references:** `docs/operations/credential_policy.md` v1.1 §1.1
- **Commit:** `8aae01e672095fbe5081817db57895ccf7f619d2`
- **Acceptance criteria and evidence:**
  - AC 1, `credential_policy.md`'s classification states the key's write scope and the decision taken: the inventory row and new §1.1 state full read and write scope (single `API_KEY` on all 150 routes, 61 writes, verified against `api_key_middleware`) and the Product Owner accept-risk (ESC-EXEC-20261015-01, option (b), human, 2026-10-15) with its reason and review triggers. Pass (document inspection).
- **Deviations:** none found.

## Staging hook-deploy investigation

- **Story:** ST-29 (BLG-OPS-181), delegated_backend
- **Spec references:** `docs/ops/staging_deploy_notes.md` v1.3 §4; `.github/workflows/staging-deploy.yml`; `scripts/wait_for_staging_deploy_live.py`
- **Commit:** `745cc1f72b5159084c08b2b23cb423b65ec6e590`
- **Acceptance criteria and evidence:**
  - AC 1, cause recorded against BLG-OPS-181: Notes line added. `RENDER_STAGING_DEPLOY_HOOK` is the staging frontend's hook, while the wait polls the backend; the frontend's branch was `exec/2026-09-09__release-v9.3/EPIC-02`. Evidence: the user's Render dashboard read (no filters, no failed builds; frontend deploy at the exact second of the 2026-10-15 hook call; backend's last deploy manual on 2026-10-13) and the workflow logs. Pass.
  - AC 2, conditional on a Build Filter: not a filter, so not triggered. `staging_deploy_notes.md` §4 still states that a non-code `workflow_dispatch` deploy is expected to go live once the hook targets the right service. Pass (N/A, documented).
- **Deviations:** none found. Fix filed as **BLG-OPS-189**.

## Stale-staging check live fire from main

- **Story:** ST-30 (BLG-OPS-182), delegated_backend
- **Spec references:** `scripts/staging_smoke_test.py`; `.github/workflows/staging-smoke-test.yml`
- **Live fire (2026-10-15, user acting for the Infrastructure & Operations Owner, DEL-20261015-03):**
  - Precondition: both staging services deployed to `main` (`efdd9494`) after the ST-29 fixes (frontend branch reset to `main`; `STAGING_API_URL` reset to the staging backend). Baseline pass: run 38721722314.
  - Deliberate divergence: the user rolled the staging backend back to `90099bec` in the Render dashboard (live).
  - AC 1, failing `main` run with `STALE STAGING DEPLOY` and the Telegram alert received: https://github.com/sachiv1984/swing-trading-model/actions/runs/38722585429 (`main` at `efdd9494`). "STALE STAGING DEPLOY: staging is running commit '90099bec…' but the latest staging-deploying commit is 'f3f732fd…'". Telegram API returned `message_id` 1355, and the user confirmed receiving the alert (11:46 local). Pass.
  - Restore: the user ran Manual Deploy → Deploy latest commit on the staging backend (live on `efdd9494`).
  - AC 2, passing `main` run after restore: https://github.com/sachiv1984/swing-trading-model/actions/runs/38723949916 (`main` at `efdd9494`). Staging is on the latest merged commit and all 4 smoke checks pass. Pass.
- **Not counted as AC 1 evidence:** runs 38714787907 and 38715664252 (the stale `STAGING_API_URL` host; accidental, not the deliberate divergence).
- **Deviations:** none found.

---

## EPIC-level consolidation

**EPIC:** EPIC-04 — Security, Operations & Platform
**Cycle:** 2026-10-12__release-v9.12
**Sprint goal:** as in the header above.
**Test scenarios used:** `tests/test_post_grace_stop_health.py`, `tests/test_settings_change_log.py`, `tests/e2e/settings-last-change.spec.js`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-25 | `scripts/check_post_grace_stop_health.py` docstring | Docstring records option (a), the pending window; option (b) not taken | AC 1 day-10 fixture passes, `non_s11_multiplier`/`missing_stop` fail; AC 2 null multiplier past the window is a violation; AC 3 option recorded in the docstring | Pass | None |
| ST-26 | `data_model.md` DS-33 v2.62; `settings_endpoints.md` v1.5.0; `settings.md` §Last Change Line v1.9 | `settings_change_log` table, logging on create/update, `X-Request-Source`, `last_change` on GET /settings, Settings last-change line | AC 1 log row per write (16 pytest); AC 2 Settings shows the last change (Playwright SC-SLC-01..05, run 38703606378); AC 3 migration recorded and applied on staging and production with verification output (human, 2026-10-15) | Pass with notes | None. Note: confirm the deployed `DATABASE_URL` role bypasses RLS (open check, not an AC) |
| ST-27 | `credential_policy.md` v1.1 §1.1 | Key write scope stated; Product Owner accept-risk recorded | AC 1 scope and decision recorded | Pass | None (ESC-EXEC-20261015-01 Resolved) |
| ST-28 | `dependency_update_review_2026-10-06.md` §3–§5 | 7 of 8 backend and 20 of 20 frontend bumps at reviewed versions | AC 1 bumps in one PR, full pytest and all Playwright shards green in CI incl. focus-restoration (runs 38704880394, 38725364575); AC 2 staging US/UK price and ATR (human, 2026-10-15) | Pass_with_deviation | BLG-TECH-24 (numpy 2.5.3 needs Python 3.12; held at 2.4.6) |
| ST-29 | `staging_deploy_notes.md` v1.3 §4 | Cause recorded against BLG-OPS-181 | AC 1 cause recorded; AC 2 Build Filter clause (N/A, not a filter) | Pass | None; fix filed as BLG-OPS-189 |
| ST-30 | `scripts/staging_smoke_test.py`; `staging-smoke-test.yml` | Live fire from `main` | AC 1 failing run 38722585429 + Telegram 1355; AC 2 passing run 38723949916 | Pass | None |
| ST-31 | `README.md`; `quarterly_dependency_upgrade_cadence_policy.md` v1.2 | Setup installs `requirements-dev.txt` | AC 1 fresh-clone collect succeeds; AC 2 grep shows `requirements-dev.txt` | Pass with notes | None; incidental BLG-QA-225 |
| ST-32 | `docs/ops/scheduled_workflows_inventory.md` v1.0 | Inventory of 23 scheduled workflows | AC 1 table with owner, cron, writes, minutes, `run audit` review | Pass | None; incidental BLG-OPS-188 |

**Story-level authority sign-offs (BLG-GOV-14), all cleared:**
- ST-26 migration: the user, human, acting for the Data Model & Domain Schema Owner, 2026-10-15 (DEL-20261015-01 Unblocked).
- ST-27 accept-risk: the human Product Owner, 2026-10-15 (ESC-EXEC-20261015-01 Resolved).
- ST-29 dashboard investigation, ST-30 live fire, ST-28 staging check: the user, human, acting for the Infrastructure & Operations Owner, 2026-10-15 (DEL-20261015-02, -03, -04).

**Frontend testing gate:** ST-26 is the only story with a frontend-visible change (`src/components/settings/SettingsLastChange.js`, Settings page). All observable behaviour is covered by Playwright SC-SLC-01..05 (rendering of one and several changes, the tooltip list, the empty state, the "API" source label, the save-and-refresh path), green in CI run 38703606378. No AC is "code review only". ST-28's focus-restoration specs were observed passing in real GitHub Actions CI (run 38704880394, `2909e67e`), as the environment-parity sub-clause requires. No story filed a testing-gap item, so the cross-story consistency check has nothing to compare.

**QA test coverage:**
- Scenarios run: the 3 files above; full backend suite at `4736cf27` (2668 passed, 21 skipped; CI Pytest on Python 3.11 green at `2fb6f888`, run 38725364575); full Playwright shards at `2909e67e` (run 38704880394); Critical-Path Smoke Tests green at `2fb6f888` (run 38725364700).
- Regression areas checked: settings read/write and PATCH semantics, the stop-health monitor, the dependency surface (yfinance price/ATR on staging for US and UK, all Playwright specs incl. dialog/modal focus restoration and axe), staging deploy and smoke workflows.
- Known deviations: ST-28 AC 1 narrowed (numpy), tracked in BLG-TECH-24. Every story's deviation check is complete.

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object. N/A: `SettingsLastChange.js` makes no request; GET /settings goes through the existing `api.*` wrapper.
- [x] **Strategy values checked:** ST-25 — §6.2 grace length (10 days, via `strategy_parameters.GRACE_PERIOD_DAYS`) and §5/§7.2/§11 multipliers (5.0 initial, 2.0 profit); the monitor reads them from `backend/strategy_parameters.py` and changes none. ST-28 — §7.1/§11 ATR period 14 (staging responses report `atr_period: 14`); no formula changed. ST-26 displays logged settings values only and computes nothing.
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-10-15
- Comments: [Agent-mediated review — on behalf of the Director of Quality, user-directed (in-session 2026-10-15, chose "Agent-mediated" for the EPIC-04 sign-off), pending human confirmation at the PR merge gate.] Review in-session by the engine in the Director of Quality role. All 13 ACs across 8 stories appear in the table above. One deviation: ST-28 AC 1 is graded Pass_with_deviation (BLG-TECH-24), per the §3.2.A self-check. ST-28 post-push CI fix: CI Pytest was red from `2909e67e` until the numpy revert. The final green run is 38725364575 at head `2fb6f888`; Playwright all shards are green at 38704880394 (`2909e67e`), with no frontend change since. Non-blocking: ST-26's open check of the deployed `DATABASE_URL` role. The first staging settings save after deploy proves the change-log write end to end. **Product Owner acceptance:** not yet given; required at the merge gate.

