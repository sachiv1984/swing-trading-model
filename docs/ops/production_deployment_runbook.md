**Owner:** Infrastructure & Operations Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.3
**Last Updated:** 2026-06-17
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

---

## 6. SI-05 Phase 1 Operational Requirements

*Added v0.2 — 2026-06-08, ST-07 (BLG-OPS-55), v5.2 sprint. I&O Owner sign-off.*

This section covers the operational requirements for the SI-05 weekly strategy integrity digest service (Phase 1). Apply these requirements when deploying any release that includes SI-05 components.

### 6.1 Environment Variables

| Variable | Purpose | Where to obtain |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Authentication token for the Telegram bot | Obtain from BotFather (`@BotFather` in Telegram); rotate via BotFather if compromised |
| `TELEGRAM_CHAT_ID` | Target chat ID for digest delivery | Obtain from the Telegram chat where the bot should send digests (use `getUpdates` API or Telegram client) |
| `FRONTEND_URL` | Base URL of the production frontend — used by SI-05 digest service to construct deep links in Telegram messages | Set to the production frontend URL (e.g. `https://<your-frontend-domain>`). Without this, deep links in SI-05 digests will be absent. Added v0.3, ST-03 (v5.8 post-ship OA). |

All three variables are required for full SI-05 functionality. If `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID` is absent, the digest service logs a WARNING and returns `sent: false`. If `FRONTEND_URL` is absent, digests are sent but deep links are omitted.

**Security note:** Treat `TELEGRAM_BOT_TOKEN` as a secret. Do not commit to source control. Store in Render environment variables (encrypted at rest). Rotate immediately if exposed.

### 6.2 Cron Schedule Configuration

The SI-05 weekly digest is triggered by the cron scheduler configured in the backend (APScheduler or Render cron job). Verify the schedule is active:

- **Render cron job:** Check the Render dashboard → Cron Jobs section; the SI-05 digest job should be scheduled weekly (Sunday or Monday, depending on configuration)
- **APScheduler (if used):** Verify the scheduler starts on service boot and the SI-05 job is registered with the correct interval

**Expected trigger:** Once per week. The exact day/time is set in the scheduler configuration — confirm with the sprint that introduced SI-05 (v5.1 ST-01).

### 6.3 How to Verify the Digest Service is Running

After deployment, verify the SI-05 digest service is operational:

**Option A (preferred after BLG-BE-33 ships):** Check the `si05_digest_log` table in the production database:
```sql
SELECT * FROM si05_digest_log ORDER BY sent_at DESC LIMIT 5;
```
A recent row with `status = 'sent'` confirms the service is running.

**Option B — Render service logs:**
1. Open Render dashboard → Backend service → Logs
2. Filter for `SI-05`: look for `INFO: SI-05 digest sent (NNN chars)` in the weekly window
3. If `WARNING: TELEGRAM credentials not set` appears: environment variables are missing

**Option C — Telegram chat history:**
1. Open the designated digest Telegram chat
2. Verify a strategy integrity digest message was received in the expected weekly window
3. Message should contain arc5-compliance metrics formatted per BLG-GOV-86

### 6.4 Failure Detection Reference

| Failure mode | Detection method | Response |
|---|---|---|
| Telegram credentials missing | `WARNING: TELEGRAM credentials not set` in Render logs | Add/verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` env vars |
| arc5-compliance data unavailable | `WARNING: arc5-compliance data unavailable` in logs | Check database connection and arc5-compliance query |
| Telegram API error | `ERROR: SI-05 Telegram send failed: …` in logs | Check Telegram API status; verify bot token valid; check network |
| Cron job not firing | No `SI-05` log lines for >7 days | Verify cron schedule in Render dashboard or APScheduler config |

For interim health checks before BLG-BE-33 ships, use Render logs (Option B) or Telegram chat history (Option C) above. Once BLG-BE-33 (`si05_digest_log` table) is deployed, use Option A for authoritative delivery confirmation.

**Full health check procedure:** `docs/ops/si05_health_check_procedure.md`

---

## 7. Cross-References

- Database migration governance: `docs/ops/database_migration_governance.md`
- Delivery verification: `claude/cycles/<cycle_id>/verification_report.md`
- Health endpoint spec: `docs/specs/api_contracts/health_endpoints.md`
- SI-05 health check procedure: `docs/ops/si05_health_check_procedure.md`
- System status report: `docs/System_status_report.md`

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.3 | 2026-06-17 | Added `FRONTEND_URL` to §6.1 environment variables table (ST-03, v5.8 post-ship OA). Infrastructure & Operations Owner sign-off. |
| 0.2 | 2026-06-08 | Added §6 SI-05 Phase 1 Operational Requirements (ST-07, BLG-OPS-55, v5.2). Infrastructure & Operations Owner. |
| 0.1 | 2026-03-17 | Initial version. ST-14 — EPIC-05 (Documentation & Standards Pack). v2.0 sprint cycle 2026-03-17__release-v2.0. Infrastructure & Operations Owner. Reviewed by Head of Engineering. |
