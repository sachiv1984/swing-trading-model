**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-08
**Cycle:** 2026-06-08__release-v5.2 (ST-08, BLG-OPS-56)

---

# SI-05 Service Scheduled Run Health Check Procedure

## Purpose

This document defines the health check procedure for verifying that the SI-05 weekly strategy integrity digest service ran successfully. Use this procedure each week after the expected digest send time to confirm the service is operational.

---

## Check Cadence

**Frequency:** Weekly  
**When to check:** On or after the expected weekly digest send time (Sunday/Monday — confirm exact schedule in Render cron job or APScheduler config)  
**Responsible role:** Infrastructure & Operations Owner (primary); Head of Engineering (escalation)

---

## Health Check Options

Choose the most convenient option. Option A is preferred once BLG-BE-33 (`si05_digest_log` table) is deployed.

---

### Option A — si05_digest_log Table (Preferred; requires BLG-BE-33)

**Prerequisites:** BLG-BE-33 (`si05_digest_log` table) must be deployed to production.

**Status:** ⚠️ INTERIM — not yet available (BLG-BE-33 is in-sprint as of v5.2). Use Option B or C until BLG-BE-33 ships.

Once available, run:

```sql
SELECT id, sent_at, status, event_count, telegram_message_id, error_message
FROM si05_digest_log
ORDER BY sent_at DESC
LIMIT 5;
```

**Interpret results:**

| `status` | `error_message` | Verdict |
|---|---|---|
| `sent` | NULL | ✅ PASS — digest delivered successfully |
| `failed` | Not NULL | ❌ FAIL — see error_message for failure reason |
| No rows in last 7 days | — | ❌ FAIL — service did not run |

**PASS condition:** At least one row with `status = 'sent'` and `sent_at` within the last 7 days.

---

### Option B — Render Service Logs

**Always available. Recommended as interim check before BLG-BE-33 ships.**

1. Open **Render dashboard** → Backend service → **Logs**
2. Set time filter to the last 7 days (or since last expected send time)
3. Search for `SI-05` in the log stream

**Expected success log:**
```
INFO: SI-05 digest sent (NNN chars)
```
(where NNN is the character count of the Telegram message, typically 200–400)

**Failure indicators:**

| Log message | Meaning | Action |
|---|---|---|
| `WARNING: TELEGRAM credentials not set — skipping SI-05 digest` | Environment variables missing | Add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` to Render env vars |
| `WARNING: arc5-compliance data unavailable — omitting SI-05 digest` | arc5-compliance DB query failed | Check database connectivity and arc5-compliance data |
| `ERROR: SI-05 Telegram send failed: ...` | Telegram API error | Check Telegram API status; verify bot token; check error details |
| No SI-05 log lines at all | Cron job not firing | Verify cron schedule in Render dashboard or APScheduler config |

**PASS condition:** `INFO: SI-05 digest sent` appears in the log within the expected weekly window.

---

### Option C — Telegram Chat History

**Always available. Useful as a user-facing confirmation.**

1. Open the designated strategy integrity digest Telegram chat
2. Scroll to the expected weekly send time
3. Verify a digest message is present, formatted per BLG-GOV-86

**Expected message format:**

```
📊 Strategy Integrity Digest — Week of YYYY-MM-DD

Validation Pass Rate: N% (N events, past 7 days)
Red Flags: N (past 7 days)
...
```

**PASS condition:** A correctly formatted digest message is present within the expected weekly window.

**FAIL condition:** No message, or a message with missing/malformed data.

---

## Pass / Fail Summary

| Check | PASS | FAIL |
|---|---|---|
| Option A (si05_digest_log) | status='sent' row exists ≤7 days | No row, or status='failed' |
| Option B (Render logs) | `INFO: SI-05 digest sent` in logs | WARNING/ERROR or no SI-05 log lines |
| Option C (Telegram) | Digest message present, well-formed | No message or malformed data |

Any single option is sufficient to confirm PASS. Record the check method and date in the weekly ops log.

---

## Escalation Path

If the health check fails:

1. **First action:** Check Render logs (Option B) for the specific failure message
2. **Telegram credential issue:** Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in Render environment variables
3. **Database issue:** Check arc5-compliance table for recent data; check Render PostgreSQL connection
4. **Cron job not firing:** Check Render cron job dashboard; verify APScheduler started on service boot
5. **Unresolved after 30 minutes:** Escalate to Head of Engineering

Document the failure and resolution in the ops log. File a P2 backlog item if the failure reveals a systemic issue.

---

## Sign-Off

**Infrastructure & Operations Owner:** Sprint Execution Engine (autonomous class), 2026-06-08
**Head of Engineering:** Sprint Execution Engine (autonomous class), 2026-06-08
