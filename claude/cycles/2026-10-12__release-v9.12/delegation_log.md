Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-13

# Delegation Log — 2026-10-12__release-v9.12

## DEL-20261013-01

- **ST Item:** ST-01 — Accept UUID trade IDs in the journal summary, end to end
- **EPIC:** EPIC-01
- **Classification:** delegated_backend (live migration and staging run, Human-Delegation, RISK-01; DS-27/28/29 precedent)
- **Assigned to:** Data Model & Domain Schema Owner (with Infrastructure & Operations Owner)
- **GitHub Issue:** #1974
- **Branch:** exec/2026-10-12__release-v9.12/EPIC-01
- **Delegated at:** 2026-10-13T07:25:55Z
- **What is needed:** The engine has written the code (router `routers/ai.py`, service `services/ai_audit_service.py`, database `database.fetch_journal_notes`), the backend test and the docs. The sandbox `DATABASE_URL` is staging and read-only to this engine, so three live steps remain. (1) On **staging, then production**, run the DS-31 Pre-check, then the Up Migration, then the Verification query from `docs/specs/data_model.md` § DS-31, and paste each environment's Pre-check and Verification output back. Expected Verification: 1 row, `trade_ids`, `ARRAY`, `_uuid`, `YES`. (The app's startup `ensure_ai_audit_table()` also runs the same guarded block, so the column may already be `_uuid` after the EPIC-01 deploy; the Verification output is still required.) (2) After EPIC-01 is deployed to staging, open Trade History, expand **AI Journal Summary** and click **Generate Summary**. Record the date and whether generated content was returned. (3) Run `SELECT run_id, invoked_at, trade_ids, trade_count, summary_produced FROM ai_audit_log ORDER BY invoked_at DESC LIMIT 1;` on staging and paste the row, confirming `trade_ids` holds the UUIDs of the trades shown.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. Manual SQL in the Supabase SQL editor and a manual UI run on staging; no GitHub Actions run is involved.
- **Spec reference:** `docs/specs/data_model.md#DS-31 — Store journal-summary trade IDs as UUIDs in ai_audit_log (v2.59, 2026-10-13)`; `docs/specs/api_contracts/ai_endpoints.md#POST /ai/journal-summary`; `stage4_backlog_slice.md#ST-01` AC 1, AC 2, AC 4
- **Unblock criteria:** DS-31 Verification output from staging and production (AC 4); a dated staging journal-summary run returning generated content (AC 1); the `ai_audit_log` row with UUID `trade_ids` (AC 2). All recorded in DS-31's Live Confirmation and in `qa_evidence_EPIC-01.md` under ST-01.
- **Commit format required:** `[EPIC-01][ST-01] <description>` pushed to `exec/2026-10-12__release-v9.12/EPIC-01`
- **Status:** Unblocked — 2026-10-13, unblocked in-session by the user (human, acting for the Data Model & Domain Schema Owner with the Infrastructure & Operations Owner), in the same session as the delegation. (1) DS-31 applied on staging, then production. Both Pre-checks showed `_int4` with 0 rows holding `trade_ids`, and both Verifications showed `trade_ids | ARRAY | _uuid | YES` (`data_model.md` DS-31 Live Confirmation). (2) AC 1: on 2026-10-13, with the staging API temporarily deployed from `exec/2026-10-12__release-v9.12/EPIC-01` (Render branch switch, head `def0bc0d`; staging is deployed only from `main` otherwise), a journal summary requested from Trade History returned generated content: a three-paragraph summary of 14 trades' notes. (3) AC 2: the newest `ai_audit_log` row is `run_id f7ab028e-c76b-421c-b77c-23d964316e77`, `invoked_at 2026-10-13 08:18:54`, `trade_ids` holding 14 UUIDs (`09593bd9-…` to `4245f8bb-…`), `trade_count 14`, `summary_produced true`. Commit SHA: `5b667160f21304334a27800f9e03d5ba9c2688fd`.

## DEL-20261013-02

- **ST Item:** ST-06 — Make the daily AI cost alert count Claude calls
- **EPIC:** EPIC-01
- **Classification:** delegated_backend (scheduler run record, Human-Delegation — `sprint_backlog.md` ST-06 Notes / Staging-only AC 2, last-successful-run half)
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1979
- **Branch:** exec/2026-10-12__release-v9.12/EPIC-01
- **Delegated at:** 2026-10-13T07:36:41Z
- **What is needed:** No scheduler called `POST /ai/check-daily-cost` (no workflow references it; Render cron needs a paid tier). ST-06 adds `.github/workflows/ai-daily-cost-check.yml` (every 6 hours plus `workflow_dispatch`). A scheduled or dispatched workflow only runs once the file is on `main`, so the engine cannot produce a run before EPIC-01 merges. (1) Confirm whether anything outside this repository already calls the endpoint (for example a Render dashboard cron job or an external cron service). If one exists, name it and paste its last successful run, so it can be recorded and the two schedulers reconciled. (2) After EPIC-01 merges, run **Actions → AI Daily Cost Check → Run workflow** (or wait for the next 6-hourly run), then paste the run ID, its conclusion and the endpoint's JSON response from the log, or run `gh run list --workflow ai-daily-cost-check.yml --limit 1 --json databaseId,conclusion,createdAt`.
- **Workflow viability (LL-v9.10-P3-01):** `ai-daily-cost-check.yml` is new, so it has no run history. It uses the same `API_URL`/`API_KEY` secrets and curl step as `ai-endpoint-anomaly-check.yml`, whose most recent successful run is 38276795575 (2026-10-12T16:21:14Z); 10 of its last 10 runs succeeded. The endpoint's own 200 response is covered by `backend/routers/test.py` and its performance baseline.
- **Spec reference:** `docs/specs/api_contracts/ai_endpoints.md#POST /ai/check-daily-cost` (Scheduler paragraph); `stage4_backlog_slice.md#ST-06` AC 2
- **Unblock criteria:** (1) answered; (2) one successful `ai-daily-cost-check.yml` run ID and date, recorded in the contract's "Last successful run" line and in `qa_evidence_EPIC-01.md` under ST-06.
- **Commit format required:** `[EPIC-01][ST-06] <description>` pushed to `exec/2026-10-12__release-v9.12/EPIC-01` (or a `[GOVERNANCE]` commit on `main` if EPIC-01 has merged)
- **Status:** Unblocked — 2026-10-13, in-session; post-merge. Step (1): the user, acting for the Infrastructure & Operations Owner, confirmed no external scheduler. Step (2), with the tightened criteria (PR #2022 review): (a) the user confirmed the production deploy is at `90099bec`, the EPIC-01 merge commit, and so is staging. `ai-daily-cost-check.yml` run 38374258055 (workflow_dispatch, 2026-10-13T09:09:07Z, head 90099bec, conclusion success), endpoint response `{"total_cost_usd":0.0,"request_count":0,"threshold_usd":1.0,"threshold_exceeded":false,"alert_sent":false}`. (b) The production `claude_audit_log` count for the day is 1 row / $0.001628, and that row was written at 09:12:10, after the 09:09:12 run, so the run's `request_count: 0` was correct. (c) A post-merge staging journal summary from Trade History wrote `claude_audit_log` `endpoint POST /ai/journal-summary`, `prompt_version v1.0`, `cost_usd 0.00162800`, `generated_at 2026-10-13 09:12:10+00`. The production and staging counts were identical (one row, $0.001628), so the summary was generated against, or both queries read, the same database. In either case the only row today post-dates the run, and only v9.12 code writes journal-summary audit rows. Story commit: `7c49f038` (ST-06 `commit_sha`); evidence recorded in the closing `[GOVERNANCE]` commit on `main`.

## DEL-20261013-03

- **ST Item:** ST-34 — Triage the drift detector's new live-vs-doc findings
- **EPIC:** EPIC-05
- **Classification:** delegated_backend (production `pg_indexes` read, Human-Delegation — `sprint_backlog.md` ST-34 Notes / Staging-only AC 1, finding 1 only; RISK-01)
- **Assigned to:** Data Model & Domain Schema Owner
- **GitHub Issue:** #2007
- **Branch:** exec/2026-10-12__release-v9.12/EPIC-05
- **Delegated at:** 2026-10-13T15:32:47Z
- **What is needed:** Findings 2–5 are triaged and committed (`255f10b4`, `data_model.md` v2.60 §Drift Detector Triage). Finding 1 needs a production read, which this engine has no access to. On **production**, run this read-only query in the Supabase SQL editor and paste the output back:
  ```sql
  SELECT tablename, indexname, indexdef FROM pg_indexes
  WHERE schemaname = 'public'
    AND indexname IN ('idx_positions_open_ticker_entry_date_unique', 'idx_portfolio_history_portfolio',
                      'idx_trade_reflections_trade', 'idx_position_audit_log_position_id',
                      'idx_sector_regime_history_portfolio_date', 'idx_trade_plan_audit_log_trade_plan_id')
  ORDER BY 1, 2;
  ```
  The first name is finding 1 (DS-17, expected present per its 2026-09-23 confirmation). The other five confirm that finding 5's staging dispositions also hold on production. Applying DS-17 to staging is not part of this delegation; it is BLG-SPEC-197.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. A manual read-only query in the Supabase SQL editor; no GitHub Actions run is involved.
- **Spec reference:** `docs/specs/data_model.md#Drift Detector Triage (2026-10-13, v2.60)`; `docs/specs/data_model.md#DS-17 — positions unique constraint on (portfolio_id, ticker, entry_date) for open positions (v2.33, 2026-09-14)`; `stage4_backlog_slice.md#ST-34` AC 1
- **Unblock criteria:** The production query output, recorded in `data_model.md` §Drift Detector Triage (finding 1 row and the finding 5 table) and in `qa_evidence_EPIC-05.md` under ST-34. If DS-17's index is absent on production, finding 1's disposition becomes "needs live action, production" and a new migration-scheduling item is filed before ST-34 closes.
- **Commit format required:** `[EPIC-05][ST-34] <description>` pushed to `exec/2026-10-12__release-v9.12/EPIC-05`
- **Status:** Unblocked — 2026-10-13, unblocked in-session: production `pg_indexes` output supplied by the user (human, acting for the Data Model & Domain Schema Owner) in the same session as the delegation. (a) Sign-off: the production result confirms DS-17's `idx_positions_open_ticker_entry_date_unique` is present (`USING btree (portfolio_id, ticker, entry_date) WHERE status = 'open'`), so finding 1 is staging-only (BLG-SPEC-197). `idx_sector_regime_history_portfolio_date` and `idx_trade_plan_audit_log_trade_plan_id` are present; `idx_portfolio_history_portfolio`, `idx_trade_reflections_trade` and `idx_position_audit_log_position_id` are absent. Status `sign_off_cleared`. (b) Push: recorded in `data_model.md` §Drift Detector Triage. Commit SHA: `3f96d2252545c9ba59eb6286d4c7d304e7037366`.

## DEL-20261013-04

- **ST Item:** ST-15 — Show the user when a position's stop is frozen for lack of ATR
- **EPIC:** EPIC-02
- **Classification:** delegated_backend (live migration, Human-Delegation; DS-25/DS-26/DS-31 precedent). The story code is engine-autonomous and pushed (`52debab3`).
- **Assigned to:** Data Model & Domain Schema Owner (with Infrastructure & Operations Owner)
- **GitHub Issue:** #1988
- **Branch:** exec/2026-10-12__release-v9.12/EPIC-02
- **Delegated at:** 2026-10-13T17:48:46Z
- **What is needed:** Both stop recompute paths now write `positions.stop_frozen_reason`, and `GET /positions` reads it. The sandbox `DATABASE_URL` is read-only staging, so the engine cannot apply DS-32. On **staging, then production**, run the DS-32 Up Migration (`ALTER TABLE positions ADD COLUMN IF NOT EXISTS stop_frozen_reason VARCHAR(20) CHECK (stop_frozen_reason IN ('atr_unavailable'));`), then the Verification query. This must happen **before EPIC-02 deploys**. Otherwise every post-grace stop recompute fails on the unknown column.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. Manual SQL in the Supabase SQL editor; no GitHub Actions run is involved.
- **Spec reference:** `docs/specs/data_model.md#DS-32 — Add stop_frozen_reason to positions (v2.61, 2026-10-13)`; `docs/specs/api_contracts/position_endpoints.md#GET /positions`; `stage4_backlog_slice.md#ST-15`
- **Unblock criteria:** DS-32 Verification output from staging and production (expect `stop_frozen_reason | character varying | 20 | YES`), recorded in DS-32's Live Confirmation.
- **Commit format required:** `[EPIC-02][ST-15] <description>` (DS-32 Live Confirmation) pushed to `exec/2026-10-12__release-v9.12/EPIC-02`
- **Status:** Unblocked — 2026-10-13, unblocked in-session by the user (human, acting for the Data Model & Domain Schema Owner), in the same session as the delegation. (a) Sign-off: DS-32 applied on staging, then production. Both Up Migrations returned "Success. No rows returned", and both Verifications returned `stop_frozen_reason | character varying | 20 | YES`. Recorded in `data_model.md` DS-32 Live Confirmation; status `sign_off_cleared`. (b) Push: story commit `52debab3697edf66df13708df37577ea4b1c3d37`; Live Confirmation commit follows on the EPIC-02 branch. Terminal: Unblocked (2026-10-13T18:16:30Z).

## DEL-20261015-01

- **ST Item:** ST-26 — Audit trail for strategy-parameter changes in Settings
- **EPIC:** EPIC-04
- **Classification:** delegated_backend (live migration, Human-Delegation; DS-32 precedent, RISK-01). The story code, tests and docs are engine-autonomous.
- **Assigned to:** Data Model & Domain Schema Owner (with Infrastructure & Operations Owner)
- **GitHub Issue:** #1999
- **Branch:** exec/2026-10-12__release-v9.12/EPIC-04
- **Delegated at:** 2026-10-15T08:05:59Z
- **What is needed:** Every `POST /settings` and `PATCH /settings/{settings_id}` now inserts into the new `settings_change_log` table in the same transaction, and `GET /settings` reads it for `last_change`. The sandbox `DATABASE_URL` is read-only staging, so the engine cannot apply DS-33. On **staging, then production**, run the DS-33 Up Migration in `docs/specs/data_model.md` (`CREATE TABLE IF NOT EXISTS settings_change_log (...)` plus `idx_settings_change_log_changed_at`), then the two Verification queries. This must happen **before EPIC-04 deploys to production**. Otherwise settings saves and `GET /settings` fail.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. Manual SQL in the Supabase SQL editor; no GitHub Actions run is involved.
- **Spec reference:** `docs/specs/data_model.md#DS-33 — Add settings_change_log (v2.62, 2026-10-15)`; `docs/specs/api_contracts/settings_endpoints.md#GET /settings`; `stage4_backlog_slice.md#ST-26` AC 3
- **Unblock criteria:** DS-33 Verification output from staging and production (8 columns as listed; indexes `idx_settings_change_log_changed_at` and `settings_change_log_pkey`), recorded in DS-33's Live Confirmation and in `qa_evidence_EPIC-04.md` under ST-26.
- **Commit format required:** `[EPIC-04][ST-26] <description>` (DS-33 Live Confirmation) pushed to `exec/2026-10-12__release-v9.12/EPIC-04`
- **Status:** Unblocked — 2026-10-15, unblocked in-session by the user (human, acting for the Data Model & Domain Schema Owner), in the same session as the delegation. (a) Sign-off: DS-33 applied on staging, then production, each with Row Level Security enabled (no policies) after Supabase flagged the table; both Up Migrations returned "Success. No rows returned", both column verifications returned the 8 expected rows and both index checks `idx_settings_change_log_changed_at`, `settings_change_log_pkey`. Recorded in `data_model.md` DS-33 Live Confirmation; status `sign_off_cleared`. (b) Push: story commit `87dea43a30b84f39ecec663d92db22235687b825`; Live Confirmation commit `6fb36482fff03267fad035d36d51c9760217afc1`. Terminal: Unblocked (2026-10-15T08:57:10Z).

## DEL-20261015-02

- **ST Item:** ST-29 — Find out why a staging-deploy.yml hook deploy of a governance-only commit never went live
- **EPIC:** EPIC-04
- **Classification:** delegated_backend (Render dashboard read, Human-Delegation; `sprint_backlog.md` ST-29 Notes, RISK-01)
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #2002
- **Branch:** exec/2026-10-12__release-v9.12/EPIC-04
- **Delegated at:** 2026-10-15T08:05:59Z
- **What is needed:** In the Render dashboard, for the **staging backend** service: (1) the final state of deploy `dep-db310hp42hec7387gh90` (BLG-OPS-181); (2) Settings → Build Filters (included/ignored paths), which the repo cannot see; (3) the deploy history since 2026-10-12. **New evidence (engine, 2026-10-15):** the symptom is not limited to governance-only commits. Every `staging-deploy.yml` run since 2026-09-03 has failed, the last 10 (2026-10-12 to 2026-10-15) on the same step: the Render hook is accepted, then "Timed out after 480s waiting for staging backend to deploy <sha>". These include code merges (EPIC-01 `90099bec`, EPIC-02 `61317385`, EPIC-03 `1200e1b0`). Staging went live on `90099bec` some time after its run timed out and has stayed there, so it is now 4 EPIC merges behind `main`. Scheduled `staging-smoke-test.yml` runs on `main` report `STALE STAGING DEPLOY` (staging `90099bec`, expected `1b4068ff`) and Telegram alerts are sent (e.g. run 38676419956, message 1350). Please record which it is for these recent deploys: skipped by a filter, failed build, build slower than 480s, or queued behind another deploy.
- **Workflow viability (LL-v9.10-P3-01):** `staging-deploy.yml`: no success in the last 10 runs; last success run 33769711448 (2026-09-03). The failure is the subject of this item, so it is not a prerequisite to fix first.
- **Spec reference:** `docs/ops/staging_deploy_notes.md`; `.github/workflows/staging-deploy.yml`; `stage4_backlog_slice.md#ST-29`
- **Unblock criteria:** The cause, from the dashboard, supplied in-session or in a comment on #2002. The engine records it as a `Notes` line on `BLG-OPS-181` (named-file write, `sprint_backlog.md` ST-29 Notes) and, if it is a Build Filter, states in `docs/ops/staging_deploy_notes.md` whether a `workflow_dispatch` deploy of a non-code commit is expected to go live (AC 2). If the cause needs a fix outside ST-29 (e.g. a longer wait or a filter change), a backlog item is filed.
- **Commit format required:** `[EPIC-04][ST-29] <description>` pushed to `exec/2026-10-12__release-v9.12/EPIC-04`
- **Status:** Pending

## DEL-20261015-03

- **ST Item:** ST-30 — Live-fire the stale-staging check from main against a deliberate divergence
- **EPIC:** EPIC-04
- **Classification:** delegated_backend (control of staging deploys and a real Telegram receipt, Human-Delegation; `sprint_backlog.md` ST-30 Notes, RISK-01)
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #2003
- **Branch:** exec/2026-10-12__release-v9.12/EPIC-04
- **Delegated at:** 2026-10-15T08:05:59Z
- **What is needed:** (1) Bring staging level with `main` (prerequisite; see below). (2) Deliberately put staging behind `main` on a deploy-path commit (e.g. redeploy an older commit from the Render dashboard). (3) Run `staging-smoke-test.yml` on `main` (`gh workflow run staging-smoke-test.yml --ref main`); confirm it fails with `STALE STAGING DEPLOY` and the Telegram alert arrives. (4) Restore staging to `main`'s commit and run it again; confirm it passes. Supply both run URLs and confirm the Telegram receipt.
- **Workflow viability (LL-v9.10-P3-01):** `staging-smoke-test.yml` on `main`: most recent success run 38406834420 (2026-10-13T13:40Z). 7 of the last 10 scheduled runs failed, all because staging is genuinely stale, not a workflow fault: `STALE STAGING DEPLOY`, staging on `90099bec` (the Telegram alert step works, e.g. run 38676419956). **Prerequisite:** the passing run (AC 2) needs staging deployed at `main`'s latest staging-deploying commit, which `staging-deploy.yml` has not achieved since 2026-09-03 (DEL-20261015-02). Restoring staging manually from the dashboard is acceptable for this item. These scheduled failures are an accidental divergence; they do not count as the deliberate one AC 1 asks for.
- **Spec reference:** `scripts/staging_smoke_test.py`; `.github/workflows/staging-smoke-test.yml`; `stage4_backlog_slice.md#ST-30`
- **Unblock criteria:** A failing `main` run URL showing `STALE STAGING DEPLOY` for the deliberate divergence with the Telegram alert received (AC 1), and a passing `main` run URL after restore (AC 2), recorded in `qa_evidence_EPIC-04.md` under ST-30.
- **Commit format required:** `[EPIC-04][ST-30] <description>` (evidence record) pushed to `exec/2026-10-12__release-v9.12/EPIC-04`
- **Status:** Pending

## DEL-20261015-04

- **ST Item:** ST-28 — Apply the in-range dependency patch/minor bumps from the October 2026 quarterly review
- **EPIC:** EPIC-04
- **Classification:** delegated_qa (Director of Quality sign-off) with a Human-Delegation for AC 2's staging check (`sprint_backlog.md` ST-28 Notes)
- **Assigned to:** Infrastructure & Operations Owner (staging check); Director of Quality (sign-off)
- **GitHub Issue:** #2001
- **Branch:** exec/2026-10-12__release-v9.12/EPIC-04
- **Delegated at:** 2026-10-15T08:20:11Z
- **What is needed:** Once the bumped build (commit `2909e67e`, yfinance 1.7.0) is live on staging, call `GET /market/atr/AAPL?market=US` and `GET /market/atr/VOD?market=UK` and confirm a current price fetch works for both tickers (e.g. `GET /positions` on a seeded US and UK position, or Trade Entry's ATR preview). Supply the responses. Local supporting evidence (not a substitute): on yfinance 1.7.0, the backend's own `get_current_price`/`calculate_atr` returned AAPL 342.96 / ATR 6.58 and VOD.L 120.40 / ATR 0.032 (pence-to-pounds conversion, existing convention) on 2026-10-15.
- **Workflow viability (LL-v9.10-P3-01):** depends on `staging-deploy.yml`, which has no success in its last 10 runs (last success 33769711448, 2026-09-03); staging is stuck on `90099bec`. Prerequisite: DEL-20261015-02 (ST-29), or a manual Render "Deploy latest commit" after EPIC-04 merges. Staging deploys from `main`, so this check can only run after merge.
- **Spec reference:** `docs/security/dependency_update_review_2026-10-06.md` §3; `stage4_backlog_slice.md#ST-28` AC 2
- **Unblock criteria:** the two staging responses recorded in `qa_evidence_EPIC-04.md` under ST-28; AC 1's full CI (pytest and all Playwright shards) green on the EPIC-04 PR; Director of Quality disposition.
- **Commit format required:** `[EPIC-04][ST-28] <description>` (evidence record)
- **Status:** Pending
