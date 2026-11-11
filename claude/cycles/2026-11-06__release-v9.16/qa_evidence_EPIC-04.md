Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-11

# QA Evidence — EPIC-04 — Anthropic Key Security and Operations Baselines

**EPIC:** EPIC-04 — Anthropic Key Security & Operations Baselines
**Cycle:** 2026-11-06__release-v9.16
**Branch:** `exec/2026-11-06__release-v9.16/EPIC-04`
**Sprint goal:** Ship Site Structure & Usability Phase 2 complete (job-based sidebar with parent and onward links, the Dashboard Today list, "Plan this" with suggested size, the plan-linked pre-entry acknowledgement fix `BLG-FE-271`, and the first semantic colour tokens), and close the Anthropic key exposure by rotating the overdue key (`BLG-OPS-214`, P1) and removing the key secret from the public Pages build (`BLG-OPS-213`).
**Test scenarios used:** `tests/test_staging_smoke_test.py`, `tests/test_staging_deploy_both_services.py`, `tests/e2e/trade-plan.spec.js`

## Story-Level Authority Records

- **Cybersecurity & Trust Lead; Infrastructure & Operations Owner (ST-11, ST-12 AC 3):** `DEL-20261111-01`, Human-Delegation. On 2026-11-11 the user, acting in these roles, confirmed in session that the rotation steps were done:
  - a new key was created (console expiry 2027-11-11);
  - it was set on Render staging and checked with "Improve with AI", then on production and checked again;
  - the 2026-05-25 key was revoked;
  - the Render frontend `REACT_APP_ANTHROPIC_API_KEY` held `true`, not a key, and was deleted.

  The delegation was marked `Unblocked` in session. ST-12 AC 3 was moved to after the merge at the user's choice and is tracked by `BLG-OPS-218`. Cleared.
- **FinOps & Resource Architect; Data Model & Domain Schema Owner (ST-13):** `DEL-20261111-02`. The user supplied the production DS-36 Verification rows and one production weekly attribution report in session on 2026-11-11. `Unblocked` in-session. Cleared.
- **Infrastructure & Operations Owner (ST-14):** `DEL-20261111-03`. The user supplied the production `screener_run_benchmark.py` output (exit 0) in session on 2026-11-11. `Unblocked` in-session. Cleared.
- **Design:** none of the EPIC-04 stories is design-gated at the v9.16 design gate. ST-12's "behave as before" reading is set by the design gate addendum (`stage4_backlog_slice_addendum.md` § ST-12).

## Evidence Table

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-11 | `external_api_credential_inventory.md` §3; `api_key_rotation_and_audit_schedule.md` row 2; `api_key_security_register.md` §3 | Human-Delegation rotation (`DEL-20261111-01`), then the dates were recorded at `f97ff562`. Rotated 2026-11-11; next due 2027-10-28, two weeks before the new key's 2027-11-11 console expiry. Updated: inventory v1.3 (90-day wording corrected to annual), schedule v1.1, register v1.11, policy v1.5. | (1) The console lists one active key created on the rotation date, and the 2026-05-25 key is revoked. (2) An AI endpoint succeeds on staging and production with the new key. (3) The inventory's `Last rotated` field and the schedule's next-due date are filled in. | Pass. (1) and (2) are user-confirmed in session on 2026-11-11 under `DEL-20261111-01`. For (1), the delegation's step 4 asked for the old key(s) to be revoked "so the console lists one active key", and the user confirmed that step done; both are console or Render ACs, staging-only per the sealed sprint backlog. (3) is shown by the `f97ff562` diff. | None |
| ST-12 | `.github/workflows/deploy.yml`; `src/pages/TradePlan.js`; `trade_plan.md` §5b; `stage4_backlog_slice_addendum.md` § ST-12 | `HAS_AI` removed: "Improve with AI" now shows whenever a ticker is entered. The secret was removed from `deploy.yml`, and the dead flag from `playwright.config.js`, `.env.staging` and `.env.production`. Commit `596c427c`. A local `CI=false npm run build` exits 0, and the bundle contains no key string. | (1) `grep -rn REACT_APP_ANTHROPIC .github src` finds nothing. (2) `gh secret list` no longer lists the secret. (3) Any key the secret held shows as revoked in the console. (4) The Trade Plan AI controls behave as before. | Pass_with_deviation. (1) Re-run 2026-11-11 on `406c7ef2`: 0 matches. (2) Post-merge, marked at seal, tracked by `BLG-OPS-215`. (3) Not met before merge, and **not** marked post-merge at seal. GitHub cannot show a secret's value, and the user chose to confirm after the merge, so it is tracked by `BLG-OPS-218`. If AC 1 holds (one active key, dated 2026-11-11), any key from this organisation that the secret held is already revoked. BLG-OPS-218 confirms this directly. (4) Playwright `trade-plan.spec.js` SC-TP-23a–f passed in CI (Playwright E2E 42985197871 on `596c427c`). The same commit removed the flag from `playwright.config.js`, so SC-TP-23b passing shows the button renders with no flag set. The production Pages half is post-merge, marked at seal, `BLG-OPS-215`. | `BLG-OPS-218` (AC 3); `DEV-v9.16-ST12-01` (P3, `trade_plan.md` §5b still names `HAS_AI`, tracked by `BLG-SPEC-229`) |
| ST-13 | `data_model.md` DS-36 (Verification, Live Confirmation); `data_pipeline_cost_baseline.md` §4, §6 | The production DS-36 Live Confirmation was recorded in `data_model.md` at `4995b075`. `data_pipeline_cost_baseline.md` v1.1 §4 was filled from one production weekly report (2026-11-11): 7,105 calls, 665 failures (all Yahoo), $0.00, plus `top_contributors`. The §6 volume line was ticked at `ba2b965e`. The window-note wording was corrected at `a9f657fe` (DS-36 reached production 2026-10-28, not 2026-11-02). | (1) DS-36 production Live Confirmation recorded (`feature` text YES, `duration_seconds` numeric YES, `idx_acl_called_at_feature`). (2) §4 has weekly calls and failures per source and combined from one production report, with its date and `top_contributors`; the §6 volume line is ticked. | Pass. (1) Rows supplied by the user and recorded. (2) Per-source rows (alpaca_data, alpaca_news, alpaca_paper, yahoo) and the combined row are filled, with the 2026-11-11 date, three `top_contributors` and §6 ticked. Conditional story, promoted to firm on dated production data on 2026-11-11. Closes `DEL-20261027-04` and `DEL-20261027-06`. | None. Incidental finding: `BLG-OPS-217` (P2), Yahoo failures in on-demand features. |
| ST-14 | `api_performance_baseline.md` §53 | `api_performance_baseline.md` v2.44 §53.2 and §53.4 at `ae785cfe`. 10 runs, `min_tickers` 545, p50 237.6 s, p95 249.2 s, threshold 356.4 s, from 2026-10-29T01:30:20Z to 2026-11-11T01:41:56Z. | The script exits 0 (at least 10 qualifying runs), and its p50, p95 and 1.5× threshold in seconds are recorded in §53 with the run date range. | Pass. The user supplied the exit-0 output, and all values are recorded with the range. Three of the 10 runs predate 2026-11-02 and were kept: DS-36 reached production 2026-10-28, nothing that affects duration changed in between, and p95 is within 5% of p50 (window note in §53.2). Closes `DEL-20261027-05`. | None |
| ST-15 | `scripts/staging_smoke_test.py`; `docs/ops/staging_deploy_notes.md` v1.6 §4; `tests/test_staging_smoke_test.py` | A missing, null or empty `render_service_id` now fails the host check with "UNIDENTIFIED STAGING HOST", and `main()` exits 1. The warning branch is gone. The expected ID is read from `check_staging_deploy_drift.STAGING_SERVICES`. Commit `324eae36`. | (1) A `/health/detailed` response without `render_service_id` fails the smoke test (test). (2) The expected service ID has one definition in the repo. | Pass. (1) `TestHostCheckMissingServiceId` and `test_staging_deploy_both_services.py::test_missing_field_fails`. (2) `test_expected_service_id_has_one_definition_in_the_repo`; the tests read the ID from `STAGING_SERVICES`. Mutation check: 6 tests fail against the previous script. `render-si05-log-query.yml`'s `SERVICE_ID` is a separate consumer (YAML) and is left unchanged. | None |

**AI evidence (ST-11, ST-12 — AI-touching addendum):**
- **Prompt-template version:** unchanged. Neither story edits a prompt template. ST-11 replaces a credential, and ST-12 changes only when the "Improve with AI" button renders.
- **Boundary-language sample:** none. Neither story changes generated or code-written text. `scan_prescriptive` and `scan_prediction` were not run because no generated text changed.

## QA Test Coverage

- **Scenarios run (local, 2026-11-11, project venv, stub `DATABASE_URL`):** `tests/test_staging_smoke_test.py` and `tests/test_staging_deploy_both_services.py`, 66 passed.
- **CI on the branch:** every workflow succeeded on each story commit:
  - `324eae36`: CI Pytest 42984744161, Critical-Path Smoke 42984744329.
  - `596c427c`: Playwright E2E 42985197871, Frontend Production Build 42985197838, CI Pytest 42985198198, Critical-Path Smoke 42985198210.
  - `ba2b965e`, `ae785cfe` and `f97ff562`: all completed workflows succeeded.
  - On the head before this record (`406c7ef2`), CI Pytest was still in progress when this was written. It is restated at sign-off.
- **Regression areas checked:**
  - Staging smoke host check and the deploy drift check (shared `STAGING_SERVICES`).
  - Trade Plan AI controls (SC-TP-23a–f): feedback control, "Improve with AI" draft, save payload.
  - Pages production build (no key in the bundle).
- **Pre-PR checks (2026-11-11):**
  - `check_api_performance_baseline_drift.py` exit 0.
  - `git log origin/main..HEAD`: only `[EPIC-04]` and `[GOVERNANCE]` commits.
  - A test merge with `origin/main` has no conflicts.
- **Known deviations:**
  - `DEV-v9.16-ST12-01` (P3, spec wording, `BLG-SPEC-229`).
  - ST-12 AC 3 moved post-merge after seal (`BLG-OPS-218`).
  - All other stories' deviation checks completed with nothing to file.
- **Backlog items filed during this EPIC:** `BLG-SPEC-229` (P3), `BLG-OPS-217` (P2), `BLG-OPS-218` (P2).
- **PR #2233 review (2026-11-11, agent-mediated for the Director of Quality and the Product Owner, user-directed, pending human confirmation):**
  - **Verdicts:** DoQ ⚠️ Approved with Comments; PO ⚠️ Approved with Comments. Posted on the PR (comment 6795099417). No blocking finding; grades unchanged.
  - **Checked during the review:** the scheduled staging smoke run 42962434894 (2026-11-11, `main`) logged the host check passing (`✓ … is the staging backend`), so ST-15 will not turn the next run red. The smoke script's new import uses only the standard library.
  - **Follow-ups filed:**
    - `BLG-FE-287` (P3): "Improve with AI" gives no feedback on `available: false` or an error.
    - `BLG-QA-261` (P3): CI guard against `REACT_APP_*` variables fed from third-party secrets.
    - `BLG-OPS-219` (P3): Anthropic key Scope and key-type rows (workspace, service account); replaces the earlier "record only" note on this.
  - **PO note:** `BLG-OPS-217` (P2, Yahoo failures) is recommended for v9.17 planning. Suggested release-notes line: the Trade Plan AI button no longer depends on a build-time key, and the Anthropic key was rotated.
- **Post-merge items (for `sprint_close.md` "Items Delegated and outstanding"):**
  - `BLG-OPS-215`: delete the GitHub secret after the Pages redeploy; production Trade Plan AI check (ST-12 AC 2 and the production half of AC 4).
  - `BLG-OPS-218`: console check for ST-12 AC 3, run before the secret is deleted.
- **Process note:** the planning premise that DS-36 deployed on 2026-11-02 was wrong (PR #2075, 2026-10-28). It was corrected in both baseline documents and in `execution_state.json` `process_notes`.

## Frontend Testing Gate

ST-12 changes `src/pages/TradePlan.js`, so the gate applies and the autonomous DoQ class is unavailable (BLG-GOV-135).
- **AC 4:** covered by Playwright `tests/e2e/trade-plan.spec.js` SC-TP-23a–f, observed passing in real GitHub Actions CI (run 42985197871, `596c427c`). The production Pages check is post-merge (`BLG-OPS-215`, filed before seal).
- **No AC is "code review only".**
- **Same-EPIC testing-gap consistency check:** no story in this EPIC filed a testing-gap item.

## DoQ Sign-Off

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): N/A. ST-12 removes a build-time flag and adds no URL construction.
- [x] **Strategy values checked:** N/A. No stop, grace, ATR, exit or sizing logic is touched.
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-11-11
- Comments: Agent-mediated review, pass 1 (2026-11-11, directed by the user in session): **Approved with comments**, no blocking finding. Grades unchanged: ST-11, ST-13, ST-14 and ST-15 Pass; ST-12 Pass_with_deviation (`BLG-OPS-218`, `DEV-v9.16-ST12-01`).

  **Checks made:**
  - Read the full `origin/main...HEAD` diff (22 files).
  - Re-ran `grep -rn REACT_APP_ANTHROPIC .github src`: 0 matches.
  - Re-ran both staging smoke test files: 66 passed.
  - Read the "Improve with AI" handler: it acts only on `data.available && data.fields`.
  - Checked CI on every story commit with `gh run list`; all workflows succeeded, including on `406c7ef2`.
  - Checked every AC in `stage4_backlog_slice.md` (ST-11 to ST-15) against a row above.

  **Findings (all non-blocking):**
  1. **Overstated line, corrected in this pass.** The ST-12 AC 3 cell stated as fact that the console's only active key is dated 2026-11-11. The user confirmed the delegation steps, not a separate console reading. The cell now states it as conditional on AC 1, and BLG-OPS-218 verifies it.
  2. **Staging gap until merge.** The Render staging frontend's `REACT_APP_ANTHROPIC_API_KEY` was deleted, and `main` still has the `HAS_AI` check. Any staging frontend deploy from `main` before this PR merges will hide "Improve with AI" on staging. Do not read a missing button on staging in that window as a regression. Production Pages is unaffected: the GitHub secret stays until BLG-OPS-215.
  3. **Silent no-op, pre-existing.** When the backend has no key, `generate-plan` returns `available: false` and the button does nothing, with no message. Production and staging both hold the key, so no user-facing change; only local builds without a backend key now show the button. Recorded only.
  4. **Stale Scope row, outside this EPIC's ACs.** `external_api_credential_inventory.md` §3 Scope still says the platform "does not support key-level scope restriction". Anthropic keys can now be scoped to a workspace. Recorded for the next quarterly audit (`api_key_rotation_and_audit_schedule.md`); not filed.
  5. **Next due date.** The new key expires on its first anniversary, 2027-11-11, so a late rotation would stop AI features that day. The next due date of 2027-10-28 (two weeks earlier) is the mitigation.

  **Frontend gate:** ST-12 AC 4 observed passing in real GitHub Actions CI (SC-TP-23a–f, run 42985197871, `596c427c`). No AC is "code review only".

  **Post-open CI-fix restatement:** not applicable; no PR is open yet.

## Merge Gate Confirmations

- **Director of Quality QA sign-off:** given by the human repository owner, acting as Director of Quality, in session at 2026-11-11T11:54:34Z ("give DoQ and PO acceptance"), before the merge. It accepts:
  - this evidence: ST-11, ST-13, ST-14 and ST-15 Pass; ST-12 Pass_with_deviation (`BLG-OPS-218`, `DEV-v9.16-ST12-01`);
  - the agent-mediated sign-off block above (pass 1 Approved with comments, 5 non-blocking findings);
  - the agent-mediated PR #2233 review (comment 6795099417), DoQ ⚠️ Approved with Comments, no blocking finding, with follow-ups filed as `BLG-FE-287`, `BLG-QA-261` and `BLG-OPS-219`.

  At the time of acceptance the PR head was `8f50c928`, with 21 checks passed, 29 pending, 5 skipped and no failures. The pending checks must be green before merge.
- **Product Owner acceptance:** given by the human repository owner, acting as Product Owner, in the same instruction at 2026-11-11T11:54:34Z, before the merge. It accepts ST-11 to ST-15 against `stage4_backlog_slice.md`, read with `stage4_backlog_slice_addendum.md` § ST-12. That includes:
  - the next rotation date of 2027-10-28, set two weeks ahead of the key's 2027-11-11 expiry;
  - ST-12 AC 3 moving to after the merge (`BLG-OPS-218`).

  Post-merge ACs: ST-12 AC 2 and the production half of AC 4 (`BLG-OPS-215`), and ST-12 AC 3 (`BLG-OPS-218`). Follow-ups: `BLG-OPS-217`, `BLG-SPEC-229`, `BLG-FE-287`, `BLG-QA-261`, `BLG-OPS-219`.
- **Merged:** PR #2233, by the human repository owner (`sachiv1984`), at 2026-11-11T12:59:20Z, merge commit `7fb39495`. The merger holds both roles, so under `ESC-CLOSE-20261103-01` the QA sign-off and PO acceptance are confirmed by the merge, in addition to the explicit in-session acceptances above. The orphaned-commit check found no commits left on the branch after the merge.
- **Post-merge status at recording (2026-11-11T13:00Z):** the Pages deploy from `7fb39495` (run 43025075223) was in progress. `gh secret list` still lists `REACT_APP_ANTHROPIC_API_KEY` (last updated 2026-05-25T20:00:59Z, the same day the revoked key was created). `BLG-OPS-218` and `BLG-OPS-215` are open.
- **ST-12 AC 3 met post-merge (`BLG-OPS-218`), 2026-11-11:** the human repository owner, acting as Cybersecurity & Trust Lead, checked the Anthropic console after the merge and reported in session that it shows one active key, the one created 2026-11-11. Any key the `REACT_APP_ANTHROPIC_API_KEY` secret held (last set 2026-05-25) is therefore revoked. Both `BLG-OPS-218` ACs are now met: this dated console check and this AC 3 record. The ST-12 grade above stays Pass_with_deviation as signed, because AC 3 was met after the merge rather than in-sprint. `BLG-OPS-218` is left for the ✅ COMPLETE banner at sprint close / post-ship closure.
- **ST-12 AC 2 and the production half of AC 4 met post-merge (`BLG-OPS-215`), 2026-11-11:**
  - After the Pages deploy from `7fb39495` succeeded (run 43025075223), the human repository owner deleted the `REACT_APP_ANTHROPIC_API_KEY` repository secret. The engine confirmed `gh secret list` no longer lists it at 2026-11-11T14:49:31Z (AC 2).
  - The owner then checked the production Trade Plan and reported in session that "Improve with AI" shows and works (AC 4, production half).
  - Both `BLG-OPS-215` ACs are met. All ST-12 ACs are now met. Its grade stays Pass_with_deviation as signed. `BLG-OPS-215` and `BLG-OPS-218` are left for their ✅ COMPLETE banners at sprint close / post-ship closure.
- **Sprint-close acceptance of P2 found defect (Product Owner and Director of Quality, the human repository owner, in session, 2026-11-11T15:13:05Z, `execution_prompt.md` STEP 5.3, LL-v9.15-P4-02):** `BLG-OPS-217` (P2, Yahoo failures in on-demand features, found by ST-13) is accepted as open at the v9.16 close. Rationale: the problem existed before this sprint and no v9.16 code introduced it. ST-13 only measured it. It is tracked at P2 for v9.17 planning, as the PO's PR #2233 note recommended.
