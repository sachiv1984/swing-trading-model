Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-21

## Consolidation Block

**EPIC:** EPIC-03 — Operational Resilience & Deploy-Path Safeguards
**Cycle:** 2026-08-21__release-v9.0
**Sprint goal:** Close out the correctness and data-integrity follow-through surfaced directly by v8.9's own PR-review process, while hardening operational resilience (deploy-path and staging safeguards) and expanding QA and cost/capacity hygiene coverage.
**Test scenarios used:** tests/test_deploy_path_filter_drift_check.py, tests/test_staging_smoke_test.py, a real local dry run (npm build + Playwright-adjacent manual verification for ST-16; a real locally-running backend instance against a local PostgreSQL server for ST-13), `.github/workflows/production-db-backup.yml`'s own live run history (ST-12, pre-met verification)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-12 | `docs/ops/database_backup_disaster_recovery_runbook.md`; `.github/workflows/production-db-backup.yml` | **Pre-met on main.** No new work — this story's full scope (document the current backup mechanism; perform one full restore drill against a non-production target) was already delivered by BLG-OPS-126/BLG-OPS-127 (`2026-07-31__release-v8.0` ST-17, `2026-08-03__release-v8.1` ST-02, commits `5165e828`/`5d32b06b`/`caf9b215`/`e20cc0a9`/`27ab9f1b`), predating this backlog item's own idea-intake date (2026-07-10) being formally scoped into a sprint. The runbook (§2) documents the confirmed backup mechanism (Supabase Free tier, no automated backups/PITR, daily manual `pg_dump` via the workflow) and the workflow's second job, `restore_dry_run`, performs a genuine restore into a disposable `postgres:17` container and verifies row counts — not a documentation-only claim. | Current backup mechanism documented; one full restore drill performed against a non-production target confirming the procedure works | Pass | None — pre-met verification only, no implementation change |
| ST-13 | `scripts/staging_smoke_test.py`; `.github/workflows/staging-deploy.yml`; `.github/workflows/staging-smoke-test.yml` | Smoke test suite (4 read-only critical endpoints: `/health`, `/positions`, `/market/status`, `/portfolio`) triggered post-deploy in `staging-deploy.yml` (failure fails that job — the "staging ready" signal's absence) and independently every 6h via a new scheduled workflow with Telegram alerting on failure. | Suite authored and triggered on staging deploy/merge; ≥3 critical endpoints; failure prevents "staging ready" signal; scheduled independent cadence with alerting; confirmed to fail correctly on a deliberately-broken deploy (dry run) | Pass | None |
| ST-14 | `scripts/check_deploy_path_filter_drift.py`; `docs/ops/render_production_build_filter_snapshot.json` | Automated drift detector covering both confirmed incident shapes (missing-deploy, BLG-OPS-82; dashboard-only filter drift, this item's own gate-clearing incident) — wired into `quality_gate.yml` as a hard PR gate. | Tooling built covering both confirmed incident shapes | Pass | None |
| ST-15 | `docs/ops/test_environment_parity_check_2026-08-16.md` | Delegated (`DEL-20260821-03`) — binary live Render dashboard fact, no proxy possible. Not yet resolved. | Production `PUBLIC_URL` dashboard value confirmed one way or the other, documented | Pending (delegated) | None |
| ST-16 | `.github/workflows/deploy.yml` | CI safeguard step verifying `build/index.html`'s asset paths are correctly scoped to the GitHub Pages subpath, catching the exact regression class behind the 2026-08-21 white-page incident. | `deploy.yml` fails fast on wrong-subpath asset paths; deliberate local test confirms the check catches the regression | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_deploy_path_filter_drift_check.py` (10 tests), `tests/test_staging_smoke_test.py` (12 tests); real dry runs performed in-session for ST-13 (genuinely broken local instance, real Postgres) and ST-16 (real `npm run build` twice, with/without the PUBLIC_URL override); ST-12 pre-met verification via `.github/workflows/production-db-backup.yml`'s own live run history (`gh run list` — daily successful runs including the morning of this cycle's own start date, 2026-08-21T03:48:09Z)
- Regression areas checked: full backend test suite (1282 passed, 5 skipped, no regressions from ST-08/09/10/11's carried-forward changes plus this EPIC's own additions); YAML syntax validated for all 4 modified/added workflow files
- Known deviations: None found — all stories' deviation checks completed with nothing to file

---

## Sign-Off

**Not yet complete.** ST-15 remains open (`DEL-20260821-03`, blocked on Infrastructure & Operations Owner Render dashboard access) — per `execution_prompt.md` §3.2, an EPIC is not "done" until all of its ST items are done, so the EPIC-level sign-off block below is deferred until ST-15 resolves. This file is created early (mid-EPIC) specifically to record ST-12's pre-met verification per the pre-met path's own requirement that a qa_evidence entry exists even for pre-met items, not to imply the EPIC as a whole is ready for PR.

**Mixed-Class EPIC Signer Format (ST-11/LL-v5.2-P4-01) — to be completed once ST-15 resolves:** EPIC-03 contains both `delegated_backend` stories (ST-15; ST-12, pre-met) and `autonomous` stories (ST-13, ST-14, ST-16) — the agent-mediated format will be used, not the BLG-GOV-19 autonomous-class block. Individual story sign-offs already on record: ST-13/ST-14/ST-16 each independently reviewed and Approved by agent-mediated Infrastructure & Operations Owner sign-off (see each story's own commit message for detailed findings).

- Signed off by: <pending — do not open the EPIC-03 PR until this is completed>
- Date: <pending>
- Comments: <pending>
