Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-27 (created; ST-28 failed-run Telegram receipt recorded, DEL-20261027-02)

# QA Evidence — EPIC-05: Operations, Cost & Platform

**EPIC:** EPIC-05 — Operations, Cost & Platform
**Cycle:** 2026-10-16__release-v9.13
**Branch:** `exec/2026-10-16__release-v9.13/EPIC-05`
**Sprint goal:** Make the Daily Position Monitor's exit confirmation record real exits through `POST /positions/{id}/exit` (BLG-FE-226, P1), give exit reasons one allowed list mapped to §8, and make CI fail on any frontend call to a route that does not exist. Also ship v9.13's stop and sizing correctness, AI output safety, operations and governance items.
**Test scenarios used:** `tests/test_daily_cost_fails_loudly.py`, `tests/test_staging_deploy_both_services.py`, `tests/test_staging_smoke_test.py`, `tests/test_wait_for_staging_deploy_live.py`

The consolidation block and DoQ sign-off are added at EPIC completion (STEP 3.2.A).

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
