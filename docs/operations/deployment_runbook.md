**Owner:** Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-09

---

# Deployment Runbook

Operational procedures for the Swing Trading Model backend deployed on Render.

---

## SI-05 Telegram Digest — Delivery Failure Alerting

**Context:** `POST /digest/si05/send` triggers the weekly SI-05 strategy integrity digest via Telegram. Failure to deliver is an ops-observable event.

### Retry Policy

The service retries up to 2 times after the initial attempt with backoff delays of 30 s and 60 s respectively before failing. Total maximum wait before final failure: 90 s.

### Failure Signals

| Signal | Level | Where |
|--------|-------|-------|
| Per-attempt warning | `WARNING` | Render logs — `"SI-05 Telegram send attempt N failed: <err> — retrying in Ns"` |
| Final failure (all retries exhausted) | `ERROR` | Render logs — `"SI-05 Telegram send failed after all retries: <err>"` |
| Endpoint-level failure | `ERROR` | Render logs — `"SI-05 Telegram send failed: <err>"` |
| DB delivery log | `status='failed'` | `si05_digest_log` table — `SELECT * FROM si05_digest_log ORDER BY created_at DESC LIMIT 5` |

**Human-observable alert:** An `ERROR`-level log entry appears in the Render dashboard log stream after all retries are exhausted. No additional alerting infrastructure is required — Render log monitoring surfaces `ERROR` entries.

### Diagnosing a Delivery Failure

1. **Check Render logs** for `ERROR` lines containing `SI-05 Telegram send failed`.
2. **Query `si05_digest_log`**: `SELECT status, error_message, created_at FROM si05_digest_log ORDER BY created_at DESC LIMIT 5;`
3. **Common causes:**
   - `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID` not set or rotated → check Render environment variables.
   - Telegram API rate limit or network timeout → retry manually after a few minutes.
   - arc5-compliance DB query failed → check database connectivity and `pre_entry_validation_log`/`red_flag_events` table availability.

### Manual Re-trigger

```bash
curl -X POST https://<render-backend-url>/digest/si05/send \
  -H "X-API-Key: <API_KEY>"
```

### SLA

Delivery failure should be investigated within **24 hours** of the scheduled trigger. Missing a single weekly digest is low severity; two consecutive failures require root cause investigation before the next scheduled send.

---

## Health Check

`GET /health` — no authentication required. Returns `{"status": "ok"}` when the backend is live.

---

## Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `DATABASE_URL` | Supabase PostgreSQL connection string | Yes |
| `API_KEY` | Backend API authentication key | Yes (production) |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token for SI-05 digest | Yes (SI-05) |
| `TELEGRAM_CHAT_ID` | Telegram chat/channel ID for digest | Yes (SI-05) |
| `ANTHROPIC_API_KEY` | Claude API key for AI features | Yes (AI features) |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-09 | Initial version. ST-09 (BLG-OPS-57, v5.3): SI-05 Telegram delivery failure alerting documented. Infrastructure & Operations Owner sign-off. |
