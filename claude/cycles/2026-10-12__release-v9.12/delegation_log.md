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
- **Status:** Pending

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
- **Status:** Pending
