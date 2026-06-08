**Owner:** QA & Testing Owner; Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-08
**Cycle:** 2026-06-08__release-v5.2 (ST-14, BLG-QA-47)

---

# SI-05 Phase 1 Acceptance Test Protocol

## Purpose

This document defines the acceptance test protocol for verifying the v5.1 staging-only deferred ACs for SI-05 Phase 1. It is a companion to the Delivery Verification Protocol (`si05_delivery_verification_protocol.md`).

These deferred ACs require staging environment verification and cannot be verified by automated tests alone.

---

## Deferred ACs Covered

| AC Ref | Story | Description | Deferred from |
|---|---|---|---|
| v5.1-ST-01-AC-09 | v5.1 EPIC-01 ST-01 | Telegram digest delivery confirmed on staging — actual Telegram message received in designated chat | v5.1 delivery verification |
| v5.1-ST-05-AC-01 | v5.1 EPIC-01 ST-05 | compliance_summary live data on staging — arc5-compliance endpoint returns live data (not mock/test data) on staging environment | v5.1 delivery verification |

---

## Test Environment Requirements

- **Staging environment:** Must be running the v5.1+ backend (includes SI-05 Phase 1 implementation)
- **Telegram credentials:** `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` set in staging environment variables
- **Database:** arc5-compliance data present in staging DB (pre_entry_validation_log and red_flag_events tables populated with at least some rows)
- **Network:** Telegram API accessible from staging environment

---

## Test Scenario: AC-09 — Telegram Digest Delivery on Staging

**AC Reference:** v5.1-ST-01-AC-09
**Test type:** Manual staging run
**Responsible:** Infrastructure & Operations Owner; Director of Quality

### Pre-conditions

- [ ] Staging backend is running and healthy (`GET /health` returns 200)
- [ ] `TELEGRAM_BOT_TOKEN` set in staging environment
- [ ] `TELEGRAM_CHAT_ID` set to the designated digest chat
- [ ] The tester has access to the designated digest Telegram chat

### Test Steps

1. **Trigger digest send:**
   ```bash
   curl -X POST https://<staging-api-url>/digest/si05/send
   ```
   Expected HTTP response: `200 OK` with `{"status": "ok", "sent": true, ...}`

2. **Verify Telegram delivery:**
   - Open the designated digest Telegram chat
   - Confirm a strategy integrity digest message was received within 30 seconds
   - Message must contain the SI-05 format: `📋 Strategy Integrity` header, pass rate, red flag count, override rate, summary line

3. **Record evidence:**
   - Note the curl response body (confirm `"sent": true`)
   - Screenshot or note the Telegram message timestamp and content

### Pass Condition

**PASS:** HTTP 200 with `{"sent": true, ...}` AND Telegram message received in designated chat.

**FAIL:** HTTP error, `{"sent": false, ...}`, or no Telegram message received.

### Notes

- If `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID` is not configured: test is BLOCKED — configure credentials before running
- If Telegram API is rate-limited: wait 60 seconds and retry once

---

## Test Scenario: AC-01 — compliance_summary Live Data on Staging

**AC Reference:** v5.1-ST-05-AC-01
**Test type:** Manual staging run
**Responsible:** Infrastructure & Operations Owner; Director of Quality

### Pre-conditions

- [ ] Staging backend is running and healthy
- [ ] arc5-compliance data is present in staging database (at least some pre_entry_validation_log and/or red_flag_events rows)

### Test Steps

1. **Call arc5-compliance endpoint:**
   ```bash
   curl https://<staging-api-url>/analytics/arc5-compliance
   ```

2. **Verify live data:**
   - Response must return `200 OK`
   - Response body must contain arc5-compliance metrics fields (validation_pass_rate, events_per_week, etc.)
   - Fields must reflect actual database values — NOT hardcoded test/mock data

3. **Cross-check with digest:**
   - Optionally, run `POST /digest/si05/send` and compare the digest pass_rate with the arc5-compliance endpoint's `validation_pass_rate` field
   - They should be consistent (within rounding)

4. **Record evidence:**
   - Note the curl response body including `validation_pass_rate`, `events_per_week`, `override_rate`, `top_rule_breach`

### Pass Condition

**PASS:** HTTP 200 with non-null arc5-compliance fields reflecting staging database contents.

**FAIL:** HTTP error, empty response, or values that do not correspond to actual staging data.

### Notes

- If arc5-compliance data is absent from staging DB: test is BLOCKED — seed representative data before running
- A staging pass_rate of 0.0 with no events is acceptable if no recent trade validation activity exists — confirm against DB query before calling FAIL

---

## Evidence Recording Template

Complete this section when the staging run is performed:

```
Date of staging run: YYYY-MM-DD
Tester: <name / role>
Staging URL: <url>

AC-09 (Telegram Digest Delivery):
- curl response: [paste response body]
- Telegram message received: YES / NO
- Telegram message timestamp: YYYY-MM-DD HH:MM
- Result: PASS / FAIL / BLOCKED
- Notes: 

AC-01 (compliance_summary Live Data):
- curl response: [paste response body]
- validation_pass_rate: 
- events_per_week:
- override_rate:
- Result: PASS / FAIL / BLOCKED
- Notes:

Overall: PASS / FAIL / BLOCKED
Signed off by: Director of Quality
Date:
```

---

## Cross-References

- Companion document: `docs/qa/si05_delivery_verification_protocol.md`
- Staged verification sprint protocol: `docs/operations/staged_verification_sprint_protocol.md`
- SI-05 health check procedure: `docs/ops/si05_health_check_procedure.md`

---

## Sign-Off

**Director of Quality:** [Pending staging run — to be completed at staged verification sprint]
