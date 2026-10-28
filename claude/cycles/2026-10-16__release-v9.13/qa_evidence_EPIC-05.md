Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-28 (DoQ sign-off, agent-mediated, Approved with conditions; ST-31 regraded Pass_with_deviation); prior — 2026-10-28 (EPIC consolidation block added); prior — 2026-10-28 (ST-31 staging schema check and attribution report recorded, DEL-20261027-04); prior history retained — see prior entries in version control

# QA Evidence — EPIC-05: Operations, Cost & Platform

**EPIC:** EPIC-05 — Operations, Cost & Platform
**Cycle:** 2026-10-16__release-v9.13
**Branch:** `exec/2026-10-16__release-v9.13/EPIC-05`
**Sprint goal:** Make the Daily Position Monitor's exit confirmation record real exits through `POST /positions/{id}/exit` (BLG-FE-226, P1), give exit reasons one allowed list mapped to §8, and make CI fail on any frontend call to a route that does not exist. Also ship v9.13's stop and sizing correctness, AI output safety, operations and governance items.
**Test scenarios used:** `tests/test_daily_cost_fails_loudly.py`, `tests/test_staging_deploy_both_services.py`, `tests/test_staging_smoke_test.py`, `tests/test_wait_for_staging_deploy_live.py`, `tests/test_api_call_attribution.py`, `tests/test_screener_run_duration.py`, `tests/e2e/system-status.spec.js` (SC-SS-01b). ST-30, ST-33 and ST-34 are documents, verified by document inspection against their AC.

## Consolidation

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-28 | `ai_endpoints.md` §POST /ai/check-daily-cost (v1.32); `.github/workflows/ai-daily-cost-check.yml` | A failed cost query raises; the service logs it and returns `status: "error"`, the endpoint answers 503; the workflow's `curl --fail-with-body` fails the step and a final `if: failure()` step sends a Telegram message (`a058fa60`). | AC 1: a simulated cost-query failure is logged, reported as an error and fails the step: `tests/test_daily_cost_fails_loudly.py` (CI Pytest 40505711397). AC 2: a failed run sends a Telegram message: run 40582931117, receipt confirmed by the user (section below). | Pass | None |
| ST-29 | `staging_deploy_notes.md` §4 (v1.4); `health_endpoints.md` §GET /health/detailed (v1.8); `.github/workflows/staging-deploy.yml` | One deploy-hook secret per staging service; `scripts/trigger_staging_deploy.py` calls each with `?ref=<sha>` and checks the returned deploy belongs to the expected service; a wait step per service; `render_service_id` on `GET /health/detailed` and a smoke-test host check; secrets map updated (`d81af9b0`). | AC 1: both secrets replace the old one and each deploy ID is checked: code and tests, secrets set by the user 2026-10-27 (`5dd04ba5`). AC 2: a green run on `main` with both services live: **not yet run**, `main` still has the old workflow until merge. AC 3: `tests/test_staging_deploy_both_services.py` fails on one hook or an undeployed wait. AC 4: host check code and tests done, `staging_deploy_notes.md` §4 and the secrets map updated; the live confirmation is part of AC 2's run. | Pass_with_deviation | BLG-OPS-196 (AC 2 and the live half of AC 4, after merge; `DEL-20261027-03`) |
| ST-30 | `docs/ops/data_pipeline_cost_baseline.md` (v1.0) | Combined weekly cost baseline across Alpaca (data, news, paper) and Yahoo: $0.00, every source free, basis per source; the baseline that can move is call volume. Advisory at >2× baseline volume, cost or failures (`b48ebe75`). Automating the check filed as BLG-OPS-195. | AC 1: combined weekly cost baseline filed in `docs/ops/`: the cost baseline is filed; the per-source weekly call volumes are **pending** a week of production data (sprint backlog: "uses live usage figures"). AC 2: >2× advisory defined (§5). AC 3: gate `BLG-OPS-17` verified at Release Planning 2026-10-16. | Pass_with_deviation | BLG-OPS-197 (weekly volumes from production; `DEL-20261027-06`) |
| ST-31 | `ops_endpoints.md` §GET /ops/api-call-attribution (v1.4); `data_model.md` DS-36 (v2.65); `backend/utils/api_attribution.py` | Every HTTP request to a market-data provider is recorded at the transport layer (`requests` and `curl_cffi` sessions) with the route template that triggered it, carried into background tasks and screener worker threads; batched writes to `api_call_log.feature`; `GET /ops/api-call-attribution` returns calls and estimated cost by feature and by provider with the top 3 (`e31a6b56`). | AC 1: each call tagged with its trigger: `tests/test_api_call_attribution.py` (43 tests). AC 2: report computable and names the top contributors: staging, 2026-10-28, `POST /screener/run` and `GET /earnings/{ticker}`, no `unattributed` rows (section below). Only 2 features made provider calls that day, so 2 were named; ranking and the 3-entry cut are unit-tested. AC 3: gate `BLG-OPS-17` verified at Release Planning. DS-36 Live Confirmation on staging recorded; production after merge. | Pass_with_deviation | BLG-OPS-197 (AC 2 on production data: weekly report naming the top 3; production DS-36 check; `DEL-20261027-04`). Regraded from Pass at DoQ review: the sprint backlog defines AC 2 as the report on live data naming the top 3, and staging named 2. |
| ST-32 | `api_performance_baseline.md` §53 (v2.43); `screener_api_contract.md` §GET /screener/history (v1.6) | Each screener run stores `screener_runs.duration_seconds` (DS-36), returned by `GET /screener/history`; `scripts/screener_run_benchmark.py` computes nearest-rank p50/p95 over non-degraded full-universe runs (`e31a6b56`). | AC 1: full-universe p50/p95 measured and filed: **pending**; runs before v9.13 have no duration, so the baseline needs about 10 nightly production runs after merge. Recording and computation tested (`tests/test_screener_run_duration.py`). AC 2: >1.5× threshold defined (§53). AC 3: gate `BLG-OPS-13` verified at Release Planning. | Pass_with_deviation | BLG-OPS-198 (p50/p95 from production; `DEL-20261027-05`) |
| ST-33 | `docs/operations/data_provider_risk_assessment.md` (v1.1); `docs/ops/external_api_dependency_register.md` | Assessment of every active market-data provider (Alpaca data, news and paper; Yahoo) with failure modes, impact and current behaviour; quick-win failover paths; accepted-risk statement with the Twelve Data cost basis; re-evaluation conditions (`02d4a2b3`, `afcd8906`). | AC 1: every active provider with failure modes and impact (§1–§2). AC 2: quick wins (§3) and re-evaluation conditions (§5). AC 3: accepted-risk statement (§4) signed off by both roles (agent-mediated, `execution_prompt.md` §5.3, approved on retry 1; `ESC-EXEC-20261027-04`, Resolved). | Pass | None. Findings filed as BLG-BE-192/193/194, BLG-FE-234, BLG-SPEC-209, BLG-OPS-194. |
| ST-34 | `docs/security/dependency_major_upgrade_assessment_2026-10-27.md` | Dated assessment of the 8 packages with breaking changes, effort and a decision for each: 7 upgrade (one is removing unused SQLAlchemy, one replaces moment with date-fns), eslint 10 held (`eslint-plugin-react` peer range) (`fd7d7788`). | AC 1: all 8 packages covered, each with breaking changes, effort and decision. AC 2: one backlog item per approved upgrade, BLG-TECH-25 to BLG-TECH-31; tailwindcss 4 stays with `BLG-TECH-21`. | Pass | None |

**Story-level authority sign-offs (BLG-GOV-14):**
- ST-28: Infrastructure & Operations Owner, human (the user), 2026-10-27, `DEL-20261027-02` (Unblocked).
- ST-31: Infrastructure & Operations Owner and Data Model & Domain Schema Owner, human (the user), staging checks 2026-10-28, `DEL-20261027-04` (staging half).
- ST-33: Infrastructure & Operations Owner and FinOps & Resource Architect, agent-mediated (§5.3), Approved on retry 1, 2026-10-27, `ESC-EXEC-20261027-04` (Resolved).
- ST-29: secrets set by the user for the Infrastructure & Operations Owner, 2026-10-27 (`DEL-20261027-03`, carried to post-sprint).

**Live-data access disclosure:** all live interaction in this EPIC was done by the user: the forced failed workflow run (ST-28), setting the hook secrets (ST-29), the staging branch switch, screener run, DS-36 query and attribution call (ST-31). The engine ran no query against a live database.

**Autonomous class (BLG-GOV-19):** not used. ST-28 and ST-31 were verified through live system interaction (Criterion 1, BLG-GOV-335), and `src/pages/SystemStatus.js` changed (Criterion 3). The EPIC takes the standard Director of Quality sign-off block.

**Frontend testing gate (LL-v3.1-EX-01):** EPIC-05's only frontend change is the System Status endpoint-count fallback, 131 → 132 (ST-31, `src/pages/SystemStatus.js`). It is covered by Playwright SC-SS-01b in `tests/e2e/system-status.spec.js`, updated in the same commit, observed passing in real CI (Critical-Path Smoke Tests run 40655296125 on `a2553bf8`). No observable AC is code-review-only.

**QA test coverage:**
- Scenarios run: the test files above. Full backend suite locally on `e31a6b56`: 2,972 passed, 30 skipped. CI on every push of this branch green (CI Pytest Suite, Playwright, Endpoint Coverage, OpenAPI drift).
- Regression areas checked: AI cost monitoring (`ai_endpoints.md`, cost workflow); staging deployment (workflows, health endpoint, smoke test); external API call logging (`api_call_log`: the existing `alpaca` and `research` rows and their reports keep their meaning, tested); screener runs and history (`screener_api_contract.md`); data model (DS-36); API contracts (`openapi.yaml` 3.39.0, endpoint registration 132, OpenAPI drift gate passing on every push); performance baseline drift check.
- Known deviations: ST-29, ST-30, ST-31 and ST-32 are graded Pass_with_deviation. Their remaining ACs need a run on `main` or production data, so they can only be verified after merge; tracked by BLG-OPS-196, BLG-OPS-197 (ST-30 and ST-31) and BLG-OPS-198 (v9.14, user-approved 2026-10-28). No canonical-spec deviation was filed: every story's deviation check finished with nothing to file.
- Pre-existing, not this EPIC: `scripts/check_contract_example_freshness.py` exits 1 on `main` with the same 8 findings with and without this EPIC's changes.

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, the only frontend change is the System Status fallback count
- [x] **Strategy values checked:** N/A — no stop/grace/ATR/exit/sizing logic touched. The `screener_batch_service.py` changes only add run timing and attribution context.
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-10-28
- Comments:
  - [Agent-mediated review — on behalf of the Director of Quality, user-directed (in-session 2026-10-28, chose "Agent-mediated" for the EPIC-05 sign-off), pending human confirmation at the PR merge gate.]
  - 7/7 stories covered and every slice AC appears in the table. The six named test files pass locally (127 tests), and CI is green on the branch, including the Playwright, endpoint-coverage, OpenAPI drift and performance-baseline gates.
  - ST-29, ST-30, ST-31 and ST-32 are Pass_with_deviation. Their remaining ACs need a run on `main` or production data after merge, tracked by BLG-OPS-196, BLG-OPS-197 and BLG-OPS-198 (v9.14, user-approved 2026-10-28). The ST-31 staging report named 2 contributors because only 2 features made provider calls; the top-3 cut is unit-tested.
  - Story-level authority sign-offs are cleared: ST-28 human (DEL-20261027-02), ST-31 staging half human (DEL-20261027-04), ST-33 agent-mediated (ESC-EXEC-20261027-04, Resolved; the risk document notes human confirmation is still pending).
  - Frontend gate: the only frontend change is the `SystemStatus.js` fallback count (132). It is covered by Playwright SC-SS-01b, changed in the same commit (`e31a6b56`), with CI passing. No observable AC relies on code review alone.
  - Testing-gap consistency: every story whose remaining ACs need production data has its own backlog item. No testing-gap items were filed.
  - First pass: Approved with conditions. C1 regrade ST-31 to Pass_with_deviation (BLG-OPS-197); C2 tighten BLG-OPS-197's top-contributors AC and add ST-31 AC 2 to its Source; C3 complete this block and set `qa_signed_off`. All three applied in the commit that adds this block.
  - The engine queried no live database. All live steps were done by the user. Human QA sign-off and Product Owner acceptance on the PR are still required before merge.

## Failed-Run Alert Check — AI Daily Cost

Story: ST-28, AC 2 (real-receipt half), `DEL-20261027-02`. Method: the delegation's suggested forced failure.

- **Date:** 2026-10-27
- **Checked by:** the user (human, acting for the Infrastructure & Operations Owner), who set the `API_KEY` repository secret to an invalid value, dispatched the workflow and confirmed the Telegram message arrived.
- **Run:** `ai-daily-cost-check.yml` run 40582931117, `workflow_dispatch`, branch `exec/2026-10-16__release-v9.13/EPIC-05`, head `5dd04ba5` (contains the ST-28 workflow from `a058fa60`), 2026-10-27T20:59:47Z, conclusion failure.

| Step | Conclusion | Log |
|------|------------|-----|
| Trigger daily AI cost check | failure | `curl: (22) The requested URL returned error: 401`, body `{"status":"error","message":"Unauthorized"}` printed by `--fail-with-body`, exit code 22 |
| Send Telegram alert on failure | success | message "AI daily cost check FAILED: today's Claude API spend is unknown (query or workflow error). <run URL>" |

- **Telegram receipt:** confirmed by the user, 2026-10-27.
- **Result:** AC 2 met. A failed run fails its step and sends a Telegram message.
- **Note:** an earlier dispatch, run 40582391679 (20:55:56Z), ran from `main` at `6f70a976`. That version of the workflow has no Telegram step, so it is not evidence for this AC. The 401 path does not exercise the cost-query failure itself; that half of AC 1 (logged, 503, `status: "error"`) is covered by `tests/test_daily_cost_fails_loudly.py` (CI Pytest 40505711397 on `a058fa60`).

## Provider Call Attribution — Staging Check

Story: ST-31, `DEL-20261027-04` (staging half). Production half after merge.

- **Date:** 2026-10-28
- **Checked by:** the user (human, acting for the Data Model & Domain Schema Owner and the Infrastructure & Operations Owner).
- **Environment:** staging backend switched to `exec/2026-10-16__release-v9.13/EPIC-05`, then one screener run to completion.

**DS-36 Verification query** (Supabase SQL editor, staging):

| table_name | column_name | data_type | is_nullable |
|------------|-------------|-----------|-------------|
| screener_runs | duration_seconds | numeric | YES |
| api_call_log | feature | text | YES |

Index query: `idx_acl_called_at_feature` (1 row). Matches the expected output. The columns and index were created by the ensure-functions on first use; no manual migration was run.

**Attribution report** (`GET /ops/api-call-attribution?window=daily`, staging, called by the user with curl):

| Feature | Calls | Failures | By provider | Estimated cost |
|---------|-------|----------|-------------|----------------|
| `POST /screener/run` | 23 | 3 | `alpaca_data` 5, `yahoo` 18 | $0.00 |
| `GET /earnings/{ticker}` | 15 | 1 | `yahoo` 15 | $0.00 |

- **By provider:** `yahoo` 33 calls (4 failures), `alpaca_data` 5 (0 failures). Total 38, estimated cost $0.00.
- **`top_contributors`:** `["POST /screener/run", "GET /earnings/{ticker}"]`.
- **Result:** calls are tagged with the route that triggered them, including the screener run's background task and worker threads (`POST /screener/run`, not `unattributed`). No `unattributed` rows. Only 2 features made provider calls in the window, so the top 3 has 2 entries.

**Staging half of `DEL-20261027-04`: complete.** Remaining: the DS-36 Verification query on production after merge.
