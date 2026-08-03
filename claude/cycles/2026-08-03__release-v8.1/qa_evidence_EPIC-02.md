Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-03

# QA Evidence Log — EPIC-02

**EPIC:** EPIC-02 — Operational Safety
**Cycle:** 2026-08-03__release-v8.1
**Sprint goal:** Ship v8.1's operational-safety, governance-process, QA-debt, spec-debt, and backend-hardening scope — including the cross-EPIC execution-state structural fix and the release's one ready user-facing accessibility fix.
**Test scenarios used:** Live production/live-adjacent verification (no CI-reproducible test suite applies — this is an infra/ops story). Verified via direct GitHub Actions run inspection (`gh run view`).

## Consolidation Block

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-02 | `docs/ops/database_backup_disaster_recovery_runbook.md#3.4` | `.github/workflows/production-db-backup.yml` — daily `pg_dump` against production Supabase (Infrastructure & Operations Owner-supplied `PROD_DATABASE_URL` secret), uploaded as a GitHub Actions artifact; plus an automated `restore_dry_run` job restoring into a disposable Postgres container with data verification | Recurring schedule configured and confirmed running; restore procedure documented and dry-run tested against a non-production target; runbook updated; Infrastructure & Operations Owner sign-off | Pass | None |

**QA test coverage:**
- Scenarios run: live `workflow_dispatch` runs of `production-db-backup.yml`, iterated to a working state across 6 fix commits (connection string format, IPv6 unreachability, pg_dump/server version mismatch, PATH resolution, Supabase-internal extension/schema filtering)
- Regression areas checked: N/A (new workflow, no existing code touched)
- Known deviations filed: None

**Delivery detail — iterative live debugging (all fixes confirmed against real GitHub Actions runs, not assumed):**
1. `a77c3acc` — initial workflow (daily cron + `workflow_dispatch`, artifact upload, size-sanity check)
2. `2fb310ca` — fixed `pg_dump: error: invalid URI query parameter: "pgbouncer"` (pooler connection string incompatible with `pg_dump`) → switched to direct connection, which then hit `Network is unreachable` (direct connection host is IPv6-only, GitHub Actions runners have no IPv6) → Infrastructure & Operations Owner switched `PROD_DATABASE_URL` to the Session pooler (IPv4, port 5432) instead
3. `2fb310ca` — fixed `pg_dump: error: aborting because of server version mismatch` (server 17.6, runner's default `postgresql-client` v16) by installing `postgresql-client-17` via the official PGDG apt repo
4. `10e63c86` — fixed `pg_dump` still resolving to v16 on `PATH` after the v17 install (pre-installed v16 isn't wired into `update-alternatives`) by calling `/usr/lib/postgresql/17/bin/pg_dump` directly
5. **Live confirmed working:** `Backup complete: 1.2M backup-2026-08-03.sql`
6. `e95cc14e` — added the `restore_dry_run` job (disposable `postgres:17` service container, `psql -v ON_ERROR_STOP=1`, row-count verification)
7. `7bc1049f` → `e9b5584a` — fixed two rounds of Supabase-internal-extension restore failures (`supabase_vault` extension unavailable in vanilla Postgres; then a `COPY vault.secrets` data block failing since the extension/schema was never created) by filtering `CREATE EXTENSION`/`COMMENT ON EXTENSION` lines and whole schema-scoped `COPY ... \.` blocks for known Supabase-managed extensions (`supabase_vault`, `pg_graphql`, `pgjwt`, `pgsodium`, `pg_net`, `pg_cron`) before the dry-run restore only — the real backup artifact is never filtered, only the disposable verification copy
8. **Live confirmed working (final):** both `backup` and `restore_dry_run` jobs succeed; hundreds of rows across `portfolios`/`positions`/`trade_history`/etc. restored correctly; `portfolios` table shows 1 row post-restore (expected — single-portfolio system)

Each fix commit was propagated to `main` via a small scoped `[GOVERNANCE]`-titled PR (`workflow_dispatch` only fires for workflows present on the default branch), per the established pattern from `2026-07-30__release-v8.0` ST-08/ST-13. PRs: #1191 (initial), #1192 (client version), #1193 (explicit path), #1194 (restore dry-run job), #1195 (extension filter), #1196 (COPY block filter) — all merged by Infrastructure & Operations Owner (human), consistent with the always-human merge gate.

---

## Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend components in this EPIC
- Signed off by: Infrastructure & Operations Owner
- Date: 2026-08-03
- Comments: Configured `PROD_DATABASE_URL` secret, ran and iterated on the workflow live across 6 fix rounds, merged all 6 follow-up PRs. Both the recurring backup and the automated restore dry-run are confirmed working against real production data. Runbook (`database_backup_disaster_recovery_runbook.md` v1.1→v1.2) updated to close the gap it previously flagged.
