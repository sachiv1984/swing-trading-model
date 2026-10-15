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
  - AC 2, the Settings page shows the last change (Playwright): SC-SLC-01..05, all passing locally on a fresh production build (15/15 Settings specs; axe scan 18/18). CI conclusion pending (Playwright run 38703606378).
  - AC 3, migration recorded in `data_model.md` (DS-33) and applied on staging and production with verification output: applied 2026-10-15 by the user (human, acting for the Data Model & Domain Schema Owner) on both, with Row Level Security enabled (no policies) after Supabase flagged the table. Both returned 8 columns and 2 indexes as expected. Recorded in DS-33 Live Confirmation. Pass.
  - Open check, not an AC: confirm the deployed backend's `DATABASE_URL` role is `postgres` (or `postgres.<ref>`). That role bypasses RLS. Any other role would have its change-log writes blocked. The first staging settings save after EPIC-04 deploys is the end-to-end proof.
- **Status:** done (DEL-20261015-01 unblocked in-session).

## Dependency patch/minor bumps from the October 2026 review

- **Story:** ST-28 (BLG-TECH-22), delegated_qa
- **Spec references:** `docs/security/dependency_update_review_2026-10-06.md` §3–§5; `backend/requirements.txt`; `backend/requirements-dev.txt`; `package.json`; `package-lock.json`
- **Commit:** `2909e67e2fbe7d47d1d6b8d933f09aeedb42dfd4`
- **What was built:** the 8 backend and 20 frontend "Batch" bumps, each at exactly the reviewed version (npm's caret resolution first pulled newer, unreviewed releases; re-pinned). `pip check` clean; non-registry dependency check passed. CI's Playwright browser cache is keyed on the lockfile's `@playwright/test` version, so the browser install follows the bump without a workflow edit.
- **Acceptance criteria and evidence:**
  - AC 1, all bumps in one PR, full pytest and all Playwright shards pass in CI incl. focus-restoration specs: locally full pytest 2668 passed / 21 skipped; 84/84 Playwright on a fresh build (`compliance-recheck`, `entry-checklist`, `epic03-v34-frontend` focus specs; dialog, modal, Settings, axe). CI evidence: the EPIC-04 PR's full run (pending).
  - AC 2, staging yfinance price and ATR for one US and one UK ticker: **pending, DEL-20261015-04** (staging is not deploying; needs ST-29 or a manual deploy after merge). Local supporting evidence in the delegation record.
- **Test scenarios to execute:** full `tests/` pytest; all Playwright shards in CI; the staging check above.
- **QA findings (Director of Quality):**
- **Disposition (Pass / Pass with notes / Fail):**

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
