Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-06

# Delegation Log — 2026-10-06__release-v9.10

> EPIC-04 branch copy. `DEL-20261006-01`/`-02` (EPIC-01) live on the EPIC-01 branch; union the files at merge (CLAUDE.md §8).

## DEL-20261006-03

- **ST Item:** ST-18 — Confirm the stale-staging-deploy alert fires on a real stale-staging condition
- **EPIC:** EPIC-04
- **Classification:** delegated_backend (live Render/GitHub Actions control; RISK-04)
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1911
- **Branch:** exec/2026-10-06__release-v9.10/EPIC-04
- **Delegated at:** 2026-10-06T16:00:56Z
- **What is needed:** (1) Make staging fall one commit behind `main`: pause Render auto-deploy for the staging backend, then let any commit land on `main`, or redeploy an older commit from the Render dashboard. (2) Trigger `staging-smoke-test.yml` via `workflow_dispatch` (GitHub Actions UI or `gh workflow run staging-smoke-test.yml`). Confirm the run fails with the `STALE STAGING DEPLOY` message from `scripts/staging_smoke_test.py` and that the Telegram alert arrives. (3) Re-enable auto-deploy, or redeploy the current `main` commit, then re-run the workflow and confirm it passes. Paste both run URLs back.
- **Spec reference:** `scripts/staging_smoke_test.py` stale-deploy check (BLG-OPS-169, v9.8 ST-17); `.github/workflows/staging-smoke-test.yml`
- **Unblock criteria:** Both run URLs recorded in `qa_evidence_EPIC-04.md` under ST-18: a failing run showing `STALE STAGING DEPLOY` for a real divergence, and a passing run after restore.
- **Commit format required:** `[EPIC-04][ST-18] <description>` pushed to `exec/2026-10-06__release-v9.10/EPIC-04`
- **Status:** Open
