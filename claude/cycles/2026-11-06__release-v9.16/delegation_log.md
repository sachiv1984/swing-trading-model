Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-11

# Delegation Log — 2026-11-06__release-v9.16

## DEL-20261110-01

- **ST Item:** ST-19 — Read production briefing ticker-caveat tokens and add any non-tickers
- **EPIC:** EPIC-05
- **Classification:** delegated_backend (production log read, Human-Delegation — `sprint_backlog.md` ST-19 Notes; LL-v8.0-P3-01 infra/ops pattern). Second attempt: v9.15 ST-24 (`DEL-20261105-01`) carried it as `BLG-AI-27`.
- **Assigned to:** AI Compliance & Governance Officer
- **GitHub Issue:** #2215
- **Branch:** exec/2026-11-06__release-v9.16/EPIC-05
- **Delegated at:** 2026-11-10T08:07:27Z
- **What is needed:** The briefing check logs one warning per caveated token: `ticker check: endpoint=POST /ai/daily-briefing field=summary ticker=<TOKEN> action=caveat_appended prompt_version=<v>`. The sandbox `DATABASE_URL` is staging and the engine has no production log access. From the production API's Render logs (or a log export), list every `ticker=<TOKEN>` on those lines since 2026-10-30 with its count, or grant the engine a one-off read. The engine then classifies each token as ticker or non-ticker, adds the non-tickers to `_NON_TICKER_WORDS` and the `ai_endpoints.md` check 3 list with `test_non_ticker_words_ignored` coverage, and records the list in `qa_evidence_EPIC-05.md`. If no line was logged, say so and the review records that none was found.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. Render log read only; no GitHub Actions run is involved.
- **Spec reference:** `docs/specs/api_contracts/ai_endpoints.md#POST /ai/daily-briefing` (check 3); `stage4_backlog_slice.md#ST-19`
- **Unblock criteria:** the token list with counts (or "no lines logged") supplied in session or in this record.
- **Commit format required:** `[EPIC-05][ST-19] <description>` on `exec/2026-11-06__release-v9.16/EPIC-05`
- **Result (supplied in session by the user, AI Compliance & Governance Officer, 2026-11-10):** **no caveated tokens found.** (1) Production Render logs, searched for `action=caveat_appended`: no matching lines (Render keeps about 7 days, `docs/ops/render_log_retention_policy.md`, so this covers roughly 2026-11-03 to 2026-11-10). (2) Production `claude_audit_log`, durable for the whole window: `endpoint = 'POST /ai/daily-briefing'`, `compliance_check_result LIKE '%ticker_outside_context_appended%'`, `generated_at >= '2026-10-30'` returned no rows. So no briefing summary got a ticker caveat from 2026-10-30 to 2026-11-10, and no word needs adding to `_NON_TICKER_WORDS`. Limitation: briefing call volume in the window was not checked, so this shows no false caveats, not how many briefings ran.
- **Sign-off:** sign_off_cleared — result supplied by the AI Compliance & Governance Officer in session, 2026-11-10.
- **Commit SHA:** fc89fdb52429063b0fa1d1f3fa1788ec31eae0d4
- **Status:** Unblocked (2026-11-10T08:34:17Z) — Unblocked in-session — production Render log search and production claude_audit_log query results, supplied by the user (AI Compliance & Governance Officer), same session as delegation. No code change was needed (none found).

## DEL-20261111-01

- **ST Item:** ST-11 — Rotate the Anthropic API key (overdue since 2026-08-25) and revoke the old key; also ST-12 AC 3 (any key the `REACT_APP_ANTHROPIC_API_KEY` secret held shows as revoked)
- **EPIC:** EPIC-04
- **Classification:** delegated_backend (Human-Delegation — `sprint_backlog.md` ST-11/ST-12 Notes; LL-v8.0-P3-01 infra/ops pattern). P1, `BLG-OPS-214`.
- **Assigned to:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
- **GitHub Issue:** #2207 (ST-11), #2208 (ST-12)
- **Branch:** exec/2026-11-06__release-v9.16/EPIC-04
- **Delegated at:** 2026-11-11T08:13:03Z
- **What is needed:** (1) Anthropic console → Settings → API Keys: create a new key. (2) Render `trading-assistant-api-staging`: set `ANTHROPIC_API_KEY` to the new key, redeploy, and check one AI endpoint (e.g. "Improve with AI" on Trade Plan, or `POST /trade-plans/generate-plan` returning `available: true`). (3) The same on the production backend. (4) Revoke the 2026-05-25 key, and any other key whose value is in the `REACT_APP_ANTHROPIC_API_KEY` GitHub secret, so the console lists one active key. (5) Also check the Render **static sites** (staging and production frontend) for a `REACT_APP_ANTHROPIC_API_KEY` env var: v4.3 set it to `true` on staging. Since ST-12 (`596c427c`) nothing reads it, so delete it. If it holds a real key, say so, because that key was in the Render frontend bundle too. Do not delete the GitHub secret yet. That is ST-12's post-merge step (`BLG-OPS-215`), after Pages has redeployed.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. Console and Render dashboard only.
- **Spec reference:** `docs/ops/external_api_credential_inventory.md` §3 Anthropic API Key (rotation policy steps); `docs/ops/api_key_rotation_and_audit_schedule.md` row 2; `stage4_backlog_slice.md#ST-11`, `#ST-12`
- **Unblock criteria:** in session or in this record: the rotation date; confirmation that the console shows one active key created that date with the old key(s) revoked; an AI endpoint succeeded on staging and on production; the Render static-site env var outcome. The engine then records the date in the inventory (`Last rotated`) and the schedule's next-due date (ST-11 AC 3).
- **Commit format required:** `[EPIC-04][ST-11] <description>` on `exec/2026-11-06__release-v9.16/EPIC-04` (engine commits the doc dates)
- **Result (supplied in session by the user, 2026-11-11):** steps 1–6 confirmed done: new key created 2026-11-11 (console expiry 2027-11-11), set on Render staging and checked ("Improve with AI"), then production and checked; 2026-05-25 key revoked; the Render frontend `REACT_APP_ANTHROPIC_API_KEY` held `true`, not a key, and was deleted; GitHub secret left in place for `BLG-OPS-215`. Recorded at `f97ff562`: rotated 2026-11-11, next due 2027-10-28 (two weeks ahead of the expiry) in the credential inventory, schedule, register and policy. ST-12 AC 3 (the key the GitHub secret held is revoked): the user chose to confirm after merge, since GitHub cannot show a secret's value; tracked by `BLG-OPS-218` (P2), run with `BLG-OPS-215`.
- **Sign-off:** sign_off_cleared — rotation steps confirmed by the user in session, 2026-11-11; ST-12 AC 3 deferred post-merge to `BLG-OPS-218`.
- **Commit SHA:** f97ff5624ef62080312b09b45aa749867a66554c
- **Status:** Unblocked (2026-11-11T11:37:08Z) — Unblocked in-session — rotation confirmed by the user, same session as delegation.

## DEL-20261111-02

- **ST Item:** ST-13 — Record the weekly market-data call-volume baseline from production
- **EPIC:** EPIC-04
- **Classification:** delegated_backend (Human-Delegation, production reads — `sprint_backlog.md` ST-13). Conditional (§1.4b): the 2026-11-09 gate (7 days of production data after the 2026-11-02 deploy) has passed by date. Closes `DEL-20261027-04` and `DEL-20261027-06` when recorded.
- **Assigned to:** FinOps & Resource Architect; Data Model & Domain Schema Owner; Infrastructure & Operations Owner
- **GitHub Issue:** #2209
- **Branch:** exec/2026-11-06__release-v9.16/EPIC-04
- **Delegated at:** 2026-11-11T08:13:03Z
- **What is needed:** (1) In the production Supabase SQL editor, run DS-36's Verification query (`data_model.md` DS-36 §Verification) and paste the rows (expect `feature` text YES, `duration_seconds` numeric YES, index `idx_acl_called_at_feature`). (2) Call `GET /ops/api-call-attribution?window=weekly` on the production API (with the production API key) and paste the JSON, or the per-source calls and failures, the combined totals, the report date and `top_contributors`. The sandbox `DATABASE_URL` is staging, and the engine has no production access.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. SQL editor and one API call.
- **Spec reference:** `docs/specs/data_model.md#DS-36` (Verification, Live Confirmation); `docs/ops/data_pipeline_cost_baseline.md` §4, §6; `stage4_backlog_slice.md#ST-13`
- **Unblock criteria:** both outputs supplied in session or in this record, or a dated statement that production data is not available in-sprint (ST-13 is then returned at close, the expected path for a conditional story).
- **Commit format required:** `[EPIC-04][ST-13] <description>` (engine records the values)
- **Result (supplied in session by the user, 2026-11-11):** (1) production DS-36 Verification, queries run one at a time in the Supabase SQL editor: `api_call_log.feature` text YES, `screener_runs.duration_seconds` numeric YES, index `idx_acl_called_at_feature`, as expected; recorded in `data_model.md` DS-36 (`4995b075`). (2) production `GET /ops/api-call-attribution?window=weekly`: 7,105 calls, 665 failures (all Yahoo), $0.00; recorded in `data_pipeline_cost_baseline.md` §4 (`ba2b965e`). The Yahoo failure rate is filed as `BLG-OPS-217` (P2). Closes `DEL-20261027-04` and `DEL-20261027-06` (v9.13 log, sealed; closure recorded here).
- **Sign-off:** sign_off_cleared — production outputs supplied by the user in session, 2026-11-11.
- **Commit SHA:** ba2b965e227814f801297096b9d2ba809a518d3d (AC 1 at 4995b075)
- **Status:** Unblocked (2026-11-11T08:34:37Z) — Unblocked in-session — production SQL results and weekly attribution report, supplied by the user, same session as delegation.

## DEL-20261111-03

- **ST Item:** ST-14 — Record the full screener run p50/p95 baseline from production
- **EPIC:** EPIC-04
- **Classification:** delegated_backend (Human-Delegation, production API key — `sprint_backlog.md` ST-14). Conditional (§1.4b): needs at least 10 nightly production screener runs after the 2026-11-02 deploy (about 2026-11-12). Closes `DEL-20261027-05` when recorded.
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #2210
- **Branch:** exec/2026-11-06__release-v9.16/EPIC-04
- **Delegated at:** 2026-11-11T08:13:03Z
- **What is needed:** Once at least 10 nightly production runs exist, run `API_URL=<production API> API_KEY=<production key> python3 scripts/screener_run_benchmark.py` and paste its full output (runs counted, min tickers, p50, p95, regression threshold, first and last run, exit code). If it exits non-zero for too few runs, paste that too and re-run after the next nightly run.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. Local script run against the production API.
- **Spec reference:** `docs/ops/api_performance_baseline.md` §53 Full Screener Run Benchmark; `stage4_backlog_slice.md#ST-14`
- **Unblock criteria:** script output with exit 0 supplied in session or in this record, or a dated statement that 10 qualifying runs will not exist in-sprint (ST-14 is then returned at close).
- **Commit format required:** `[EPIC-04][ST-14] <description>` (engine records the values)
- **Result (supplied in session by the user, 2026-11-11):** `screener_run_benchmark.py` against production, exit 0: 10 qualifying runs, `min_tickers` 545, p50 237.6 s, p95 249.2 s, threshold 356.4 s, runs 2026-10-29T01:30:20Z to 2026-11-11T01:41:56Z. Recorded in `api_performance_baseline.md` v2.44 §53.2 (`ae785cfe`). 3 runs predate 2026-11-02; DS-36 actually reached production with v9.13 EPIC-05 (merged 2026-10-28), so they are kept (window note in §53.2). Closes `DEL-20261027-05` (v9.13 log, sealed; closure recorded here).
- **Sign-off:** sign_off_cleared — production benchmark output supplied by the user in session, 2026-11-11.
- **Commit SHA:** ae785cfee003130f13555858b9a9aafe3381c396
- **Status:** Unblocked (2026-11-11T08:40:47Z) — Unblocked in-session — production benchmark output, supplied by the user, same session as delegation.
