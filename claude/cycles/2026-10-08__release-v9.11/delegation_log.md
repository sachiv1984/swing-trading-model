Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-08

# Delegation Log — 2026-10-08__release-v9.11

## DEL-20261008-01

- **ST Item:** ST-02 — Verify all six AI features after the PR #1921 import fix, and file the escaped-defect note
- **EPIC:** EPIC-01
- **Classification:** delegated_qa (sub-step: staging run, Human-Delegation, RISK-02)
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1926
- **Branch:** exec/2026-10-08__release-v9.11/EPIC-01
- **Delegated at:** 2026-10-08T11:01:30Z
- **What is needed:** On the staging deploy, with a working Anthropic key, run each of the six AI features once from the UI: post-trade debrief (Trade History → a closed trade → Regenerate), journal summary, daily briefing, chat (one question), generate-plan and generate-thesis. For each, record the date and whether it returned generated content, the generic "unavailable" message or an error. Then opt in to AI-output sampling in Settings, trigger one feature again, and confirm a sampled row was written (or paste the sampling-path log line). The debrief may instead cite the 2026-10-07 production verification.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. This is a manual UI run on staging, so no GitHub Actions run is involved.
- **Spec reference:** `stage4_backlog_slice.md#ST-02` AC 1 and AC 2; `docs/specs/api_contracts/ai_endpoints.md`
- **Unblock criteria:** A dated six-row result table and the sampling evidence, recorded in `qa_evidence_EPIC-01.md` under ST-02. Any feature returning an error or the generic message is a defect and is filed before ST-02 closes.
- **Commit format required:** `[EPIC-01][ST-02] <description>` pushed to `exec/2026-10-08__release-v9.11/EPIC-01`
- **Status:** Pending

## DEL-20261008-02

- **ST Item:** ST-42 — Make the Non-Registry Dependency Check a required status check on main
- **EPIC:** EPIC-06
- **Classification:** delegated_backend (repository admin action, Human-Delegation, RISK-08)
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1966
- **Branch:** exec/2026-10-08__release-v9.11/EPIC-06
- **Delegated at:** 2026-10-08T11:01:30Z
- **What is needed:** Add the status check context `Non-Registry Dependency Check (ST-29)` to `main`'s branch protection `required_status_checks`, keeping the four existing contexts (`verify_governance`, `Pytest Phase A (clean tests — no DB required)`, `Endpoint Coverage Report (ST-16)`, `OpenAPI Drift Detection (ST-08)`). Via the GitHub UI (Settings → Branches → main → Require status checks), or with repository admin rights: `gh api -X POST repos/sachiv1984/swing-trading-model/branches/main/protection/required_status_checks/contexts -f 'contexts[]=Non-Registry Dependency Check (ST-29)'`. Then paste the output of `gh api repos/sachiv1984/swing-trading-model/branches/main --jq .protection.required_status_checks`.
- **Workflow viability (LL-v9.10-P3-01):** `non-registry-dependency-check.yml`, most recent success run 37764573094 (2026-10-08T10:36:23Z); 5 of the last 5 runs succeeded. The workflow triggers on every `pull_request` to `main` with no `paths:` filter, so a PR that does not touch dependency files still gets a run and is not left waiting on the check (AC 2).
- **Spec reference:** `.github/workflows/non-registry-dependency-check.yml`; `stage4_backlog_slice.md#ST-42`
- **Unblock criteria:** The `gh api` read lists the new context under `protection.required_status_checks`, and one later PR that does not touch dependency files shows the check completing. Both recorded in `qa_evidence_EPIC-06.md` under ST-42.
- **Commit format required:** `[EPIC-06][ST-42] <description>` pushed to `exec/2026-10-08__release-v9.11/EPIC-06`
- **Status:** Pending

## DEL-20261008-03

- **ST Item:** ST-06 — claude_audit_log: add prompt_hash and response_length, and log failed model calls
- **EPIC:** EPIC-01
- **Classification:** delegated_backend (live migration, Human-Delegation, RISK-03; DS-17/DS-25 precedent)
- **Assigned to:** Data Model & Domain Schema Owner (with Infrastructure & Operations Owner)
- **GitHub Issue:** #1930
- **Branch:** exec/2026-10-08__release-v9.11/EPIC-01
- **Delegated at:** 2026-10-08T11:18:41Z
- **What is needed:** Run the DS-27 Up Migration on **staging, then production** (the sandbox `DATABASE_URL` is staging and read-only to this engine):
  ```sql
  ALTER TABLE claude_audit_log ADD COLUMN IF NOT EXISTS prompt_hash VARCHAR(16);
  ALTER TABLE claude_audit_log ADD COLUMN IF NOT EXISTS response_length INTEGER;
  ```
  Then run the Verification query in each environment and paste both outputs back:
  ```sql
  SELECT column_name, data_type, character_maximum_length, is_nullable
  FROM information_schema.columns
  WHERE table_name = 'claude_audit_log' AND column_name IN ('prompt_hash', 'response_length')
  ORDER BY column_name;
  ```
  Expected in each: `prompt_hash`, `character varying`, `16`, `YES`; `response_length`, `integer`, `NULL`, `YES`.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch; a manual SQL run in the Supabase SQL editor.
- **Spec reference:** `docs/specs/data_model.md#DS-27`; `stage4_backlog_slice.md#ST-06` AC 3
- **Unblock criteria:** Both verification outputs recorded in `data_model.md` DS-27 (Live Confirmation) and in `qa_evidence_EPIC-01.md` under ST-06. The code is already on the branch: `create_claude_audit_entry()` also adds the columns idempotently, and the audit write never blocks an AI response, so deploy order is not a hard risk.
- **Commit format required:** `[EPIC-01][ST-06] <description>` pushed to `exec/2026-10-08__release-v9.11/EPIC-01`
- **Status:** Pending

## DEL-20261008-04

- **ST Item:** ST-20 — DB-level unique constraint for active price alerts
- **EPIC:** EPIC-03
- **Classification:** delegated_backend (live migration, Human-Delegation, RISK-03; DS-17 precedent)
- **Assigned to:** Data Model & Domain Schema Owner (with Infrastructure & Operations Owner)
- **GitHub Issue:** #1944
- **Branch:** exec/2026-10-08__release-v9.11/EPIC-03
- **Delegated at:** 2026-10-08T13:34:42Z
- **What is needed:** Run the DS-28 Up Migration (`docs/specs/data_model.md` § DS-28, the full `BEGIN … COMMIT` block with its duplicate pre-check) on **staging, then production**. If the pre-check raises, deactivate the listed duplicate active alerts first and re-run. Then run the Verification query in each environment and paste both outputs back:
  ```sql
  SELECT indexname, indexdef FROM pg_indexes
  WHERE tablename = 'price_alerts' AND indexname = 'idx_price_alerts_active_unique';
  ```
  Expected: `CREATE UNIQUE INDEX idx_price_alerts_active_unique ON public.price_alerts USING btree (portfolio_id, ticker, condition, threshold_price) WHERE (active = true)`.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch; a manual SQL run in the Supabase SQL editor.
- **Spec reference:** `docs/specs/data_model.md#DS-28`; `stage4_backlog_slice.md#ST-20` AC 2
- **Unblock criteria:** Both verification outputs recorded in `data_model.md` DS-28 (Live Confirmation) and in `qa_evidence_EPIC-03.md` under ST-20. AC 1 (concurrent double-submit absorbed at the DB layer) is already shown by `tests/test_price_alert_db_uniqueness.py` against a real Postgres (CI Phase B). Deploy order is not a hard risk: without the index the service behaves as before.
- **Commit format required:** `[EPIC-03][ST-20] <description>` pushed to `exec/2026-10-08__release-v9.11/EPIC-03`
- **Status:** Unblocked — 2026-10-09T13:06:08Z. Unblocked in-session: the user (human, with live write access, acting for the Data Model & Domain Schema Owner) applied DS-28 on staging, then production; the duplicate pre-check passed in both. The Verification query returned `idx_price_alerts_active_unique` with the expected partial unique definition in both environments. Sign-off cleared; recorded in `data_model.md` DS-28 Live Confirmation, and carried into `qa_evidence_EPIC-03.md` §ST-20 when that file is created at EPIC completion.

## DEL-20261009-01

- **ST Item:** ST-17 — Snapshot the strategy parameters in force onto each closed trade
- **EPIC:** EPIC-03
- **Classification:** delegated_backend (live migration, Human-Delegation, RISK-03; DS-25/DS-26 precedent)
- **Assigned to:** Data Model & Domain Schema Owner (with Financial Reporting & Records Owner)
- **GitHub Issue:** #1941
- **Branch:** exec/2026-10-08__release-v9.11/EPIC-03
- **Delegated at:** 2026-10-09T12:51:19Z
- **What is needed:** Run the DS-29 Up Migration (`docs/specs/data_model.md` § DS-29) on **staging, then production**:
  ```sql
  ALTER TABLE trade_history
      ADD COLUMN IF NOT EXISTS active_atr_multiplier NUMERIC(4, 2),
      ADD COLUMN IF NOT EXISTS atr NUMERIC(10, 4),
      ADD COLUMN IF NOT EXISTS grace_period_days INTEGER,
      ADD COLUMN IF NOT EXISTS parameter_source VARCHAR(40);
  ```
  Then run the DS-29 Verification query in each environment and paste both outputs back. Expected: 4 rows, all nullable — `active_atr_multiplier` numeric(4,2), `atr` numeric(10,4), `grace_period_days` integer, `parameter_source` character varying(40).
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch; a manual SQL run in the Supabase SQL editor.
- **Spec reference:** `docs/specs/data_model.md#DS-29`; `stage4_backlog_slice.md#ST-17` AC 2
- **Unblock criteria:** Both verification outputs recorded in `data_model.md` DS-29 (Live Confirmation) and in `qa_evidence_EPIC-03.md` under ST-17. AC 1 (new closed trades carry the four fields) is shown by `tests/test_trade_parameter_snapshot.py`. **Deploy order is a hard risk:** `create_trade_history()`'s INSERT names the new columns, so EPIC-03 must not deploy before the migration is applied in that environment, or every exit fails.
- **Commit format required:** `[EPIC-03][ST-17] <description>` pushed to `exec/2026-10-08__release-v9.11/EPIC-03`
- **Status:** Unblocked — 2026-10-09T12:58:25Z. Unblocked in-session: the user (human, with live write access, acting for the Data Model & Domain Schema Owner) applied DS-29 on staging, then production. The Verification query returned the 4 expected nullable columns (`active_atr_multiplier` numeric(4,2), `atr` numeric(10,4), `grace_period_days` integer, `parameter_source` varchar(40)) in both environments. Sign-off cleared; recorded in `data_model.md` DS-29 Live Confirmation, and carried into `qa_evidence_EPIC-03.md` §ST-17 when that file is created at EPIC completion.
