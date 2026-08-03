**Owner:** Infrastructure & Operations Owner
**Class:** Operational Runbook (Class 5)
**Status:** Active
**Version:** 1.2
**Last Updated:** 2026-08-03
**Story:** ST-17 (BLG-OPS-126, EPIC-04, v8.0); ST-02 (BLG-OPS-127, EPIC-02, v8.1)

---

# Production Database Backup & Disaster Recovery Runbook

## 1. Scope

Production database: Supabase (Postgres), per `docs/infrastructure/staging_setup.md` §Architecture Decision. This runbook covers backup frequency/retention as configured on the hosting provider, and a step-by-step recovery procedure. It does not cover application-code rollback (see `docs/operations/render_rollback_runbook.md` for that, a separate concern — code rollback does not restore data, and this runbook does not roll back code).

**Prior state:** No documented backup/DR runbook existed for the production database before this story — a real incident would have relied on ad hoc knowledge rather than a tested procedure (`BLG-OPS-126`).

---

## 2. Backup Frequency & Retention — As Currently Configured

**Pending live confirmation.** This repo does not record which Supabase plan tier the production project is on, and Supabase's backup capability differs materially by tier:

| Supabase plan | Automated backup capability (as of Supabase's published tiers) |
|---------------|------------------------------------------------------------------|
| Free | No automated daily backups. Manual `pg_dump` is the only backup mechanism unless the user runs one themselves on a schedule. |
| Pro | Daily automated backups, 7-day retention by default (not point-in-time — a specific daily snapshot). |
| Team / Enterprise | Daily automated backups with configurable retention, plus optional Point-in-Time Recovery (PITR) add-on (continuous WAL-based recovery to any second within the retention window). |

**Action required (Infrastructure & Operations Owner):** Confirm the actual plan tier and backup configuration for the production Supabase project (`trading-assistant-staging`'s sibling production project — see `docs/infrastructure/staging_setup.md` line 19 for the production/staging project split) via the Supabase dashboard → Project Settings → Database → Backups, and record it here:

> **Confirmed configuration (2026-07-31):** **Free plan.** Confirmed via Project Settings → Billing/Subscription. Consistent with the absence of a Database → Backups management page in the dashboard (Supabase does not expose backup management UI on the Free tier — its absence is corroborating evidence, not just the plan label). **No automated daily backups. No Point-in-Time Recovery (PITR).** The only backup mechanism available is a manual `pg_dump`, and per §3.4 below, no recurring manual backup schedule currently exists for the production database.

---

## 3. Recovery Runbook

### 3.1 Decide the recovery approach

| Scenario | Approach |
|----------|----------|
| Accidental data deletion/corruption, caught quickly, PITR available | Point-in-time restore to just before the incident (Supabase dashboard → Backups → Point in Time Recovery, if enabled on the confirmed plan) |
| Accidental data deletion/corruption, PITR not available | Restore from the most recent daily automated backup (Pro+) or the most recent manual `pg_dump` snapshot (Free tier — see §3.4) |
| Full project loss (Supabase project deleted/corrupted) | Provision a new Supabase project and restore the most recent backup/dump into it, following the same schema-recreation steps as `docs/infrastructure/staging_setup.md` §1.2 (schema-only `pg_dump`/`psql` pattern), then restore data on top |

### 3.2 Prerequisites

- Access to the Supabase dashboard with Owner/Admin role on the production project
- Confirm the incident is genuinely a data-loss/corruption event, not an application bug producing incorrect-but-present data (a code rollback per `render_rollback_runbook.md` may be the correct response instead — cross-reference before restoring from backup, since restoring loses any legitimate writes made after the restore point)

### 3.3 Restore from an automated backup or PITR (Pro+ tiers)

1. Supabase dashboard → production project → **Database** → **Backups**
2. Select either a specific daily backup or a point-in-time timestamp (if PITR is enabled and confirmed per §2)
3. Follow Supabase's in-dashboard restore flow — this typically restores into a **new** project or a fork, not in-place, to avoid destroying the current (possibly partially-recoverable) state
4. Once restored into the new/forked project, obtain its connection string and follow §3.5 (cutover) below

### 3.4 Restore from a manual `pg_dump` snapshot (Free tier, or as a supplementary backup regardless of tier)

**Confirmed applicable: production is on the Free tier — this is the only available recovery path.** No automated backup/PITR exists.

**Gap closed (2026-08-03, ST-02, BLG-OPS-127):** A recurring manual `pg_dump` schedule now exists — `.github/workflows/production-db-backup.yml`, daily at 3 AM UTC (`workflow_dispatch` also available for on-demand runs). Confirmed live via manual trigger: produces a ~1.2M `.sql` dump, uploaded as a GitHub Actions artifact with 90-day retention. The prior gap ("no recovery path exists if an incident occurred today") is closed.

**Restore procedure has been dry-run tested, not just documented.** The same workflow includes a second job, `restore_dry_run`, which runs automatically after every backup: restores the just-produced dump into a disposable `postgres:17` service container (never staging, never production) and verifies application data landed correctly (`portfolios` table row count check). Confirmed live (2026-08-03): both jobs succeeded — hundreds of rows across `portfolios`/`positions`/`trade_history`/etc. restored correctly, `portfolios` table showed 1 row post-restore as expected for this single-portfolio system.

**Known, deliberate exclusion from the dry-run verification:** the dry-run filters out `CREATE EXTENSION`/`COMMENT ON EXTENSION` statements and `COPY` data blocks for Supabase-managed internals (`supabase_vault`, `pg_graphql`, `pgjwt`, `pgsodium`, `pg_net`, `pg_cron` — schemas `vault`/`cron`/`graphql`/`net`/`pgsodium`) before restoring into the vanilla Postgres container, since those extensions/schemas don't exist outside Supabase's own hosted image. This is not a gap in the *real* backup — the actual dump artifact still contains this data unmodified; only the disposable verification container skips it, since a genuine recovery restores into another Supabase project, which already has these extensions.

To restore an existing dump (production incident, or the artifact from the workflow above):
```bash
psql "$NEW_DATABASE_URL" -f <dump_file>.sql
```

### 3.5 Cutover to the restored database

1. Update the production API's `DATABASE_URL` environment variable (Render dashboard → production API service → Environment) to point at the restored/new database
2. Render will automatically redeploy the API service on environment variable change
3. Run the same verification steps as `docs/operations/render_rollback_runbook.md` §Step 4 (Verify Health) — `GET /health`, `GET /health/detailed`, and a sample authenticated critical-endpoint check
4. Confirm data completeness: spot-check the most recent positions/trades against any external record (broker statement, manual notes) to identify how much data (if any) was lost between the restore point and the incident

### 3.6 Post-recovery actions

1. Inform Product Owner of the recovery, the restore point used, and any data loss window
2. File a post-incident note in the current cycle's QA evidence log: date, what was lost/restored, root cause if known
3. If the incident was caused by an application bug (not infrastructure failure), ensure a hotfix is deployed before resuming normal write traffic, to avoid immediately recreating the same corruption
4. Re-run `docs/operations/render_rollback_runbook.md`'s post-rollback checklist if a code rollback was also part of the response

---

## 4. Sign-Off

| Role | Decision | Date |
|------|----------|------|
| Infrastructure & Operations Owner | Approved — §2 live-confirmed as Free plan (no automated backups, no PITR). Recovery procedure (§3) is accurate for this tier. The absent recurring manual `pg_dump` schedule (§3.4) is acknowledged as a genuine, currently-unmitigated production risk — recommended for a P1 backlog item at next sprint planning, not silently accepted. | 2026-07-31 |
| Infrastructure & Operations Owner | Approved — §3.4 gap closed (ST-02, BLG-OPS-127). Recurring `pg_dump` schedule (`production-db-backup.yml`) confirmed live, producing a real ~1.2M dump. Restore procedure dry-run tested via an automated `restore_dry_run` job restoring into a disposable Postgres container — confirmed live, application data (portfolios/positions/trade_history/etc.) restores correctly. No production or staging data was touched during testing. | 2026-08-03 |
