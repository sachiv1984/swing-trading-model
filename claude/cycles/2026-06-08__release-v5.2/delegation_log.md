Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-08

---

# Delegation Log — 2026-06-08__release-v5.2

---

## DEL-20260608-01

- **ST Item:** ST-05 — BLG-BE-32: SI-05 Telegram delivery retry and failure handling
- **EPIC:** EPIC-02
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering
- **GitHub Issue:** #682
- **Branch:** exec/2026-06-08__release-v5.2/EPIC-02
- **Delegated at:** 2026-06-08T11:30:00Z
- **What is needed:** Implement retry and failure handling for Telegram delivery in `backend/services/si05_digest_service.py`. Specifically:
  1. **Document current failure mode:** Confirm whether the exception at line 273–275 logs at ERROR level and returns `{"sent": False, ...}` — document this as the baseline.
  2. **Implement retry policy:** Choose one of: (a) exponential backoff with max 2 retries (30s/60s delays) — update `send_si05_digest()` to retry on Telegram API exception, OR (b) explicit no-retry decision — add a code comment at line 273 with rationale (e.g., "No retry — weekly cadence means stale digest is worse than silence; retry on next scheduled run").
  3. **Ensure ERROR logging:** Confirm `logger.error("SI-05 Telegram send failed: %s", e)` at line 274 is preserved in both paths.
  4. **Add unit test:** In `tests/test_si05_digest_service.py`, add at least 1 test verifying that a Telegram API failure is logged at ERROR level. Use `unittest.mock.patch` to mock the requests call and raise an exception.
  5. **Staging verification:** After implementation, confirm the failure mode is observable in Render logs (AC-04 — staging-only evidence acceptable).
- **Spec reference:** `backend/services/si05_digest_service.py` (implementation spec); `docs/ops/production_deployment_runbook.md §6.4` (failure modes reference)
- **Unblock criteria:** Commit `[EPIC-02][ST-05] ...` pushed to `exec/2026-06-08__release-v5.2/EPIC-02`; unit test for ERROR logging added and passing; retry policy choice documented in code or ops runbook
- **Commit format required:** `[EPIC-02][ST-05] <description>` pushed to `exec/2026-06-08__release-v5.2/EPIC-02`
- **Status:** Pending

---

## DEL-20260608-02

- **ST Item:** ST-06 — BLG-BE-33: SI-05 digest delivery log table (si05_digest_log)
- **EPIC:** EPIC-02
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering; Data Model & Domain Schema Owner
- **GitHub Issue:** #683
- **Branch:** exec/2026-06-08__release-v5.2/EPIC-02
- **Delegated at:** 2026-06-08T11:30:00Z
- **What is needed:** Create the `si05_digest_log` table and write a log row on each send attempt. Specifically:
  1. **Database migration:** In `backend/database.py` (or equivalent startup script), add a `CREATE TABLE IF NOT EXISTS si05_digest_log` statement with the following schema:
     ```sql
     CREATE TABLE IF NOT EXISTS si05_digest_log (
       id SERIAL PRIMARY KEY,
       sent_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
       status VARCHAR(10) NOT NULL CHECK (status IN ('sent', 'failed')),
       event_count INTEGER,
       telegram_message_id VARCHAR(100),
       error_message TEXT,
       created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
     );
     ```
     The `CREATE TABLE IF NOT EXISTS` guard is mandatory (RISK-02 — safe to run on repeated restarts).
  2. **Log row on send:** In `backend/services/si05_digest_service.py`, after each Telegram send attempt (both success and failure paths), write a row to `si05_digest_log`:
     - On success (line ~271): `status='sent'`, `event_count` from the digest data, `telegram_message_id` from the Telegram API response if available
     - On failure (line ~273): `status='failed'`, `error_message=str(e)`
  3. **Optional endpoint:** If scoping allows, implement `GET /digest/si05/log` to expose recent log entries. If implemented: register in `backend/routers/test.py`, add `openapi.yaml` entry, author API contract document, update `SystemStatus.js` fallback count and `SC-SS-01b` in `tests/e2e/system-status.spec.js` — per CLAUDE.md §2.
  4. **Staging verification:** Confirm the table is present in the staging database (AC-04 — staging-only evidence acceptable). Infrastructure & Operations Owner sign-off required.
  5. **Data Model sign-off:** Data Model & Domain Schema Owner must sign off on the schema before merge.
- **Spec reference:** `docs/specs/api_contracts/digest_endpoints.md` (if GET endpoint implemented); `backend/services/si05_digest_service.py` (write location)
- **Unblock criteria:** Commit `[EPIC-02][ST-06] ...` pushed to `exec/2026-06-08__release-v5.2/EPIC-02`; migration in database.py with `IF NOT EXISTS` guard; log row written on success and failure paths; Data Model & Domain Schema Owner sign-off; staging confirmation by I&O Owner
- **Commit format required:** `[EPIC-02][ST-06] <description>` pushed to `exec/2026-06-08__release-v5.2/EPIC-02`
- **Status:** Pending
