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
- **Status:** Pending
