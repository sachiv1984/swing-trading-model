**Owner:** Infrastructure & Operations Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.1
**Last Updated:** 2026-03-17
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Production Deployment Runbook

---

## 1. Purpose

This runbook covers the steps required to deploy a staging-verified build of the Momentum Trading Assistant to production. It assumes the staging environment is fully set up and that the build being deployed has passed all quality gates.

**Pre-condition:** Staging verification must be complete before production deployment begins. A build that has not been verified on staging must not be deployed to production.

---

## 2. Pre-Deployment Checklist

Complete all items before beginning the deployment steps.

### 2.1 Quality Gates

- [ ] All sprint EPICs merged to `main` (no open PRs for this release)
- [ ] Delivery verification report exists (`claude/cycles/<cycle_id>/verification_report.md`) with status `Verified` or `Verified_with_deviations`
- [ ] Director of Quality sign-off recorded on all QA evidence logs
- [ ] All P0 deviations resolved; P1 deviations have accepted mitigations
- [ ] Integration tests pass on staging (`python -m pytest tests/ -v`)

### 2.2 Database

- [ ] Any required migrations have been applied to staging and verified
- [ ] Database migrations are reviewed and ready for production application (per `docs/ops/database_migration_governance.md`)
- [ ] Rollback SQL is prepared for any migrations being applied this deployment

### 2.3 Environment

- [ ] Production environment variables are up to date (no new config required by this release)
- [ ] Production database connection string confirmed
- [ ] Any external service credentials (if applicable) confirmed valid

### 2.4 Timing

- [ ] Deployment window is low-traffic (evenings / weekends preferred for this user-scale system)
- [ ] Operator is available for the full deployment and post-deployment verification window

---

## 3. Deployment Steps

### 3.1 Apply Database Migrations (if any)

If this release includes schema changes:

1. Connect to production database
2. Apply each migration file in sequence (lowest sequence number first):
   ```bash
   psql $DATABASE_URL -f backend/migrations/<migration_file>.sql
   ```
3. Verify migration applied:
   ```bash
   psql $DATABASE_URL -c "\d <affected_table>"
   ```
4. Record UTC timestamp and result

If any migration fails: stop immediately. Follow `docs/ops/database_migration_governance.md §7 — Incident Procedure`.

### 3.2 Deploy Backend

The backend is a FastAPI application deployed via the hosting platform (e.g. Render, Railway, or equivalent).

**Option A — Hosting platform auto-deploy from `main`:**
1. Confirm `main` branch is at the correct commit (`git log --oneline -3`)
2. Trigger deployment via the hosting platform dashboard or CLI
3. Monitor deployment logs until "Deploy succeeded" or equivalent message

**Option B — Manual deploy:**
```bash
# Build and push (adjust for your hosting provider)
git push <remote> main
```

Monitor the deployment dashboard for build and startup success.

### 3.3 Deploy Frontend

The frontend is a React application (Base44 or equivalent build):

1. Confirm the frontend build is current (`build/` directory is up to date)
2. Deploy the `build/` directory via the frontend hosting platform (e.g. Netlify, Vercel, or static host)
3. Verify deployment URL returns the updated version (check version indicator or recent change in UI)

---

## 4. Post-Deployment Verification

Complete these checks within 30 minutes of deployment.

### 4.1 Health Check

```bash
curl https://<production-api-url>/health
```

Expected: HTTP 200 with `{"status": "ok"}` or equivalent.

### 4.2 Key Endpoint Smoke Tests

| Endpoint | Expected behaviour |
|----------|--------------------|
| `GET /portfolio` | Returns portfolio data including `initial_value`, `net_deposits`, `current_drawdown_percent`, `peak_portfolio_value` |
| `GET /positions` | Returns open positions list |
| `GET /trades` | Returns closed trade history |
| `GET /market/status` | Returns SPY and FTSE regime + FX rate |
| `GET /analytics/metrics` | Returns analytics metrics without error |
| `GET /reports/tax-year?year=<current>` | Returns tax-year P&L response (if v2.0 deployed) |
| `GET /signals` | Returns signals list |

If any endpoint returns a 500 or unexpected error: proceed to §5 (Rollback).

### 4.3 Frontend Verification

- [ ] Frontend loads without errors
- [ ] Portfolio page shows current data
- [ ] New features introduced in this release are visible and functional
- [ ] Browser console is free of critical JS errors

### 4.4 Database Integrity

If migrations were applied:
- [ ] Affected table(s) show the expected schema change (`\d <table>` in psql)
- [ ] Existing data rows are intact (spot-check a known record)

---

## 5. Rollback Procedure

Use rollback if post-deployment verification reveals a critical failure (HTTP 500 on key endpoints, data corruption, or frontend non-functional).

### 5.1 Backend Rollback

1. Identify the previous stable commit:
   ```bash
   git log --oneline -10
   ```
2. Deploy the previous commit to the hosting platform (revert deployment via dashboard, or push prior commit to a deploy branch)
3. Confirm health check passes after rollback

### 5.2 Database Rollback

If migrations were applied and the rollback SQL is available:
```bash
psql $DATABASE_URL -f rollback_<migration_file>.sql
```

If migration is not reversible: escalate to Head of Engineering. Do not attempt partial rollback without guidance.

### 5.3 Frontend Rollback

Redeploy the previous frontend build via the hosting platform.

### 5.4 Post-Rollback

- Confirm system is stable on the previous version
- Document the failure, root cause (if known), and rollback in the release record
- File a P0 or P1 backlog item for the production issue
- Do not re-attempt the deployment until the root cause is resolved

---

## 6. Cross-References

- Database migration governance: `docs/ops/database_migration_governance.md`
- Delivery verification: `claude/cycles/<cycle_id>/verification_report.md`
- Health endpoint spec: `docs/specs/api_contracts/health_endpoints.md`
- System status report: `docs/System_status_report.md`

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-17 | Initial version. ST-14 — EPIC-05 (Documentation & Standards Pack). v2.0 sprint cycle 2026-03-17__release-v2.0. Infrastructure & Operations Owner. Reviewed by Head of Engineering. |
