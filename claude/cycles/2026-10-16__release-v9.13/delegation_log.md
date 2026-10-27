Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-16

# Delegation Log — 2026-10-16__release-v9.13

## DEL-20261016-01

- **ST Item:** ST-02 — Define the allowed exit reasons and map each to one of §8's three exit conditions
- **EPIC:** EPIC-01
- **Classification:** delegated_backend (live backfill and CHECK constraint, Human-Delegation — `sprint_backlog.md` ST-02 Notes / Staging-only AC 2, live half; RISK-01, DS-23 pattern)
- **Assigned to:** Data Model & Domain Schema Owner (with Infrastructure & Operations Owner)
- **GitHub Issue:** #2032
- **Branch:** exec/2026-10-16__release-v9.13/EPIC-01
- **Delegated at:** 2026-10-16T11:05:32Z
- **What is needed:** The engine has written AC 1 and the documentation half of AC 2 (`aded4d63`): the allowed values and their §8 condition in `data_model.md` §3 and `metrics_definitions.md` §Exit Condition Category, `backend/exit_reasons.py`, the 400 on an unlisted value at `POST /positions/{position_id}/exit`, and DS-34. The sandbox `DATABASE_URL` is staging and this engine has no authorisation to write to it, so the live steps remain. On **staging, then production**, in the Supabase SQL editor: (1) run DS-34's **Pre-check** and paste the output. Every `allowed = false` row must be a legacy alias from DS-34's table or blank; if any other value appears, stop and report it, because the Up Migration would roll back. (2) Run the **Up Migration** (one transaction: backfill, then both constraints). (3) Run the **Verification** query and re-run the Pre-check, and paste both outputs. Expected: 2 constraint rows (`chk_positions_exit_reason`, `chk_trade_history_exit_reason`), and every Pre-check row `allowed = true`.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. Manual SQL in the Supabase SQL editor; no GitHub Actions run is involved.
- **Spec reference:** `docs/specs/data_model.md#DS-34 — Allowed exit_reason values with CHECK constraints on positions and trade_history (v2.63, 2026-10-16)`; `docs/specs/data_model.md#Exit Reason Values`; `stage4_backlog_slice.md#ST-02` AC 2
- **Unblock criteria:** each environment's Pre-check counts and Verification output, recorded in DS-34's Live Confirmation (status changed from PENDING to CONFIRMED APPLIED) and in `qa_evidence_EPIC-01.md` under ST-02.
- **Commit format required:** `[EPIC-01][ST-02] <description>` pushed to `exec/2026-10-16__release-v9.13/EPIC-01` (or a `[GOVERNANCE]` commit on `main` if EPIC-01 has merged)
- **Status:** Unblocked — 2026-10-16, unblocked in-session by the user (human, acting for the Data Model & Domain Schema Owner with the Infrastructure & Operations Owner), in the same session as the delegation. (a) Sign-off: sign_off_cleared, DS-34 applied and verified on staging, then production (Pre-check, Up Migration, line-break check and Pre-check re-run in each; every row `allowed = true`, both constraints present). Staging backfilled 12 `trade_history` rows (`manual` 1, `stop_hit` 5, `target` 6); production needed none. Staging's first constraint pass stored a line-wrapped `'Partial Profit Taking'` literal from the pasted one-line script; it was recreated and verified the same day, and the script was reformatted before production. Recorded in `data_model.md` DS-34 Live Confirmation. (b) Commit SHA: `7eed6d38aca455c230c31be62ac0e877d13e1f8c` (evidence commit; engine implementation commit `aded4d63549a3a156fb4a0d027fc808861f020b3`).

## DEL-20261017-01

- **ST Item:** ST-10 — Define a stop-freshness metric and show it on System Status
- **EPIC:** EPIC-02
- **Classification:** delegated_backend (Human-Delegation for the staging-only half of AC 2 — `sprint_backlog.md` ST-10 Staging-only ACs: "AC 2, manual-check half only (the displayed value checked by hand against a deployed environment's open positions, recorded). The live DB needs the user's permission before any query.")
- **Assigned to:** Infrastructure & Operations Owner (with the user's permission for the read-only query)
- **GitHub Issue:** #2040
- **Branch:** exec/2026-10-16__release-v9.13/EPIC-02
- **Delegated at:** 2026-10-17T16:06:04Z
- **What is needed:** The engine has delivered AC 1 and the automated half of AC 2 at `5c4b38e7` (metric in `metrics_definitions.md` v1.32.0 §Stop Freshness; `GET /positions/stop-freshness`; the System Status panel; pytest and Playwright SC-SS-09a–e). Remaining: on an environment running `5c4b38e7` or later, (1) open System Status and note the Stop Freshness panel's median, oldest (with ticker), coverage and never-recalculated values and the "As of" time; (2) at about the same moment run the read-only query in `metrics_definitions.md` §Stop Freshness → Manual check against that environment's database; (3) paste both. They match if the median and maximum of `age_hours` over non-NULL rows equal the panel's (allowing for the seconds between reads), the oldest ticker matches, and the NULL row count equals "never recalculated".
- **Workflow viability (LL-v9.10-P3-01):** `staging-deploy.yml` has no success in its last 40 runs (latest `39046299773`, 2026-10-17: timed out waiting for the staging backend to deploy `27430d29`; staging backend still live at `2fb6f888`). Staging therefore does not run this code yet. That deploy fault is EPIC-05 ST-29's scope (deploy both staging services from `staging-deploy.yml`) and BLG-TECH-24. Options: (a) run the check on production after EPIC-02 merges and deploys; or (b) on staging once ST-29 restores deploys.
- **Spec reference:** `docs/specs/metrics_definitions.md#Stop Freshness`; `docs/specs/frontend/pages/system_status.md#Stop Freshness Panel (v1.3 — ST-10, BLG-SPEC-188)`; `docs/specs/api_contracts/position_endpoints.md#GET /positions/stop-freshness`
- **Unblock criteria:** the panel values and the query output from one deployed environment, recorded in `qa_evidence_EPIC-02.md` under ST-10 with the date and environment.
- **Commit format required:** `[EPIC-02][ST-10] <description>` on `exec/2026-10-16__release-v9.13/EPIC-02` (or a `[GOVERNANCE]` commit on `main` if EPIC-02 has merged)
- **Status:** Unblocked — 2026-10-27. (a) Sign-off: sign_off_cleared. The user (human, acting for the Infrastructure & Operations Owner) deployed both staging services from this branch at `826ee17a`, read the System Status panel (As of 08:12, 27 Oct 2026: median —, oldest —, coverage 0 of 2, 2 never recalculated) and ran the read-only manual-check query on staging (BARC and LGEN, both `stop_calculated_at` NULL). They match. Recorded in `qa_evidence_EPIC-02.md` §Staging Manual Check — Stop Freshness. (b) Commit SHA: `49055e805d5beee4efa8cdad38d492ec9c7644be` (evidence commit; engine implementation commit `5c4b38e77ab512536f53f28891e3c5dc6d9586f4`). ST-10 set to done in `execution_state.json` in the same commit as this entry.

## DEL-20261027-01

- **ST Item:** ST-22 — Add a useful / not-useful rating to each AI chat answer
- **EPIC:** EPIC-03
- **Classification:** delegated_backend (Human-Delegation for the live half of AC 2 — `sprint_backlog.md` ST-22 Staging-only ACs: "AC 2, live half only (DS entry's Live Confirmation on staging and production)"; RISK-01)
- **Assigned to:** Data Model & Domain Schema Owner (with the Infrastructure & Operations Owner; live database write access is the user's)
- **GitHub Issue:** #2052
- **Branch:** exec/2026-10-16__release-v9.13/EPIC-03
- **Delegated at:** 2026-10-27T09:25:54Z
- **What is needed:** The engine has delivered AC 1, AC 3 and the documentation half of AC 2 in the ST-22 commit on this branch (`chat_answer_ratings`, `data_model.md` DS-35 v2.64; `POST /ai/chat/{answer_id}/rating`; the widget control; pytest, real-Postgres tests and Playwright SC-CAR-01..05). Remaining, on **staging, then production**, in the Supabase SQL editor: (1) run DS-35's Up Migration (`CREATE TABLE IF NOT EXISTS chat_answer_ratings …`, idempotent; the app also creates it on first use, so order against deploy does not matter); (2) run DS-35's Verification (two queries); (3) paste both outputs. It passes if the first query returns 4 rows (`id`, `answer_id`, `rating`, `rated_at`, all `is_nullable = NO`) and the second returns the 4 named constraints.
- **Workflow viability (LL-v9.10-P3-01):** not applicable — the action is SQL run in the Supabase editor, not a GitHub Actions workflow.
- **Spec reference:** `docs/specs/data_model.md#DS-35 — Add chat_answer_ratings (v2.64, 2026-10-27)`; `docs/specs/api_contracts/ai_endpoints.md#POST /ai/chat/{answer_id}/rating`
- **Unblock criteria:** both environments' Verification output recorded in DS-35's Live Confirmation lines, with the date.
- **Commit format required:** `[EPIC-03][ST-22] <description>` on `exec/2026-10-16__release-v9.13/EPIC-03` (or a `[GOVERNANCE]` commit on `main` if EPIC-03 has merged)
- **Status:** Unblocked — 2026-10-27, unblocked in-session by the user (human, acting for the Data Model & Domain Schema Owner), in the same session as the delegation. (a) Sign-off: sign_off_cleared. DS-35 Up Migration and Verification run in the Supabase SQL editor on staging, then production. Both returned 4 columns (`id`, `answer_id`, `rating`, `rated_at`), all `is_nullable = NO`, and the 4 expected constraints (`chat_answer_ratings_answer_id_fkey`, `chat_answer_ratings_pkey`, `ck_chat_answer_ratings_rating`, `uq_chat_answer_ratings_answer`). Staging's first paste showed only the constraints result (the editor displays the last statement's output); the columns query was re-run on its own. Recorded in `data_model.md` DS-35 Live Confirmation. (b) Commit SHA: `2cc67cf2af01e559f1c905fb1449bf8675731df8` (production evidence commit; staging evidence `b18163f8`; engine implementation commit `0922a448066333ad7cf8c62bf0e742f1bb611bc2`, test-setup fix `278229a3`). ST-22 set to done in `execution_state.json` in the same commit as this entry.

## DEL-20261027-02

- **ST Item:** ST-28 — Make the daily AI cost alert fail loudly on query or workflow failure
- **EPIC:** EPIC-05
- **Classification:** delegated_backend (Human-Delegation for AC 2's real receipt — `sprint_backlog.md` ST-28 Staging-only ACs: "AC 2 (a failed `ai-daily-cost-check.yml` run sends a Telegram notification; real receipt)"; RISK-01)
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #2058
- **Branch:** exec/2026-10-16__release-v9.13/EPIC-05
- **Delegated at:** 2026-10-27T12:49:59Z
- **What is needed:** The engine has delivered AC 1 and the automated half of AC 2 at `a058fa60` (failed cost query → logged, 503 with `status: "error"`; `curl --fail-with-body`; a final `if: failure()` Telegram step; `tests/test_daily_cost_fails_loudly.py`). Remaining: one real failed run and its Telegram message. Suggested way to force a failure: temporarily set the `API_KEY` repository secret to an invalid value, dispatch **Actions → AI Daily Cost Check → Run workflow** on branch `exec/2026-10-16__release-v9.13/EPIC-05` (the endpoint answers 401, so `curl --fail-with-body` fails the step and the Telegram step runs), then restore `API_KEY` immediately. Production is only read (no alert is evaluated on a 401). Then confirm a Telegram message "AI daily cost check FAILED: …" arrived, and paste the run ID and the message time.
- **Workflow viability (LL-v9.10-P3-01):** `ai-daily-cost-check.yml` last succeeded at run 40502770492 (schedule, 2026-10-27T12:18:49Z, `main`); all of its last 10 runs succeeded. `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` are already set (used by 9 other workflows, e.g. `staging-smoke-test.yml`).
- **Spec reference:** `docs/specs/api_contracts/ai_endpoints.md#POST /ai/check-daily-cost`; `.github/workflows/ai-daily-cost-check.yml`
- **Unblock criteria:** a failed `ai-daily-cost-check.yml` run ID and the user's confirmation that its Telegram message arrived, recorded in `qa_evidence_EPIC-05.md`.
- **Commit format required:** `[EPIC-05][ST-28] <description>` on `exec/2026-10-16__release-v9.13/EPIC-05` (or a `[GOVERNANCE]` commit on `main` if EPIC-05 has merged)
- **Status:** Pending

## DEL-20261027-03

- **ST Item:** ST-29 — Deploy both staging services from staging-deploy.yml and wait on each
- **EPIC:** EPIC-05
- **Classification:** delegated_backend (Human-Delegation — `sprint_backlog.md` ST-29 Staging-only ACs: "AC 1, live half only (the two secrets set from the Render dashboard). AC 2 (a live `staging-deploy.yml` run on `main` with both services on the run's commit). AC 4 (smoke test confirms the host behind `STAGING_API_URL`)"; RISK-01)
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #2059
- **Branch:** exec/2026-10-16__release-v9.13/EPIC-05
- **Delegated at:** 2026-10-27T12:49:59Z
- **What is needed:** The engine has delivered AC 3 and the code halves of AC 1 and AC 4 at `d81af9b0` (`scripts/trigger_staging_deploy.py`, per-service waits, `render_service_id` on `GET /health/detailed`, smoke-test host check, `tests/test_staging_deploy_both_services.py`, `staging_deploy_notes.md` §4, secrets map). Remaining: (1) in Render, copy **trading-assistant-api-staging → Settings → Deploy Hook** into a new repo secret `RENDER_STAGING_BACKEND_DEPLOY_HOOK`, and **trading-assistant-staging → Settings → Deploy Hook** into `RENDER_STAGING_FRONTEND_DEPLOY_HOOK`; (2) after EPIC-05 merges (the workflow runs from `main`), dispatch **Actions → Deploy to Staging (Render) → Run workflow** on `main` (or let the merge's push run it) and paste the run ID; it passes when all steps are green: both trigger steps report a deploy on the expected `srv-…`, both waits report live on the run's commit, and the smoke test prints "is the staging backend (srv-d6rtdg94tr6s73ce2j6g)"; (3) delete `RENDER_STAGING_DEPLOY_HOOK`.
- **Workflow viability (LL-v9.10-P3-01):** `staging-deploy.yml` has no success in its last 10 runs (latest failure: run 40504434239, push, 2026-10-27T12:31:30Z). Cause known and is this story's subject: `RENDER_STAGING_DEPLOY_HOOK` holds the frontend's hook while the wait step watches the backend (BLG-OPS-181/BLG-OPS-189, `staging_deploy_notes.md` §4). The prerequisite fix is step (1) above, raised in this same delegation. `RENDER_PLATFORM_API_KEY`, `STAGING_API_URL` and `STAGING_API_KEY` are already set (used by `staging-deploy-drift-check.yml` and `staging-smoke-test.yml`).
- **Spec reference:** `docs/ops/staging_deploy_notes.md#4. Render Deploy Hook Setup`; `docs/specs/api_contracts/health_endpoints.md#GET /health/detailed`; `.github/workflows/staging-deploy.yml`
- **Unblock criteria:** both secrets set (user confirmation) and a green `staging-deploy.yml` run on `main` whose log shows both services live on its commit and the smoke-test host check passing, recorded in `qa_evidence_EPIC-05.md`.
- **Commit format required:** `[EPIC-05][ST-29] <description>` on `exec/2026-10-16__release-v9.13/EPIC-05` (or a `[GOVERNANCE]` commit on `main` if EPIC-05 has merged)
- **Progress:** 2026-10-27 — step (1) done. The user (human, acting for the Infrastructure & Operations Owner) set both secrets; `gh secret list` shows `RENDER_STAGING_BACKEND_DEPLOY_HOOK` (updated 2026-10-27T15:57:29Z) and `RENDER_STAGING_FRONTEND_DEPLOY_HOOK` (2026-10-27T15:58:13Z). The hooks have not been called yet; whether each holds its own service's hook is proven by the trigger steps' deploy-ID check on the first post-merge run. Engine-side CI on `d81af9b0` green (CI Pytest 40506739549, Playwright 40506739503). Steps (2) and (3) remain.
- **Status:** Pending
