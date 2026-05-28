Owner: Infrastructure & Operations Owner
Class: Operational Policy (Class 2)
Status: Draft
Version: 0.1
Last Updated: 2026-05-28
Lifecycle Guide: claude/charter/document_lifecycle_guide.md

---

# Claude API Log Hygiene Policy

**Backlog item:** BLG-OPS-38

---

## 1. Scope

This policy covers log hygiene for all Claude API calls made by this project:

| Endpoint | Backend path | Purpose |
|----------|-------------|---------|
| `POST /trade-plans/{plan_id}/generate-thesis` | `backend/services/gemini_service.py` (Claude-backed) | Pre-trade thesis generation |
| `POST /ai/check-daily-cost` | `backend/routers/ai.py` | Daily cost check |
| `GET /ai/claude-audit-log` | `backend/routers/ai.py` | Audit log query |

The `ANTHROPIC_API_KEY` environment variable and full Claude prompt/response text are the primary sensitive assets this policy governs.

---

## 2. Application-Level Logging Assessment

A code review of `backend/services/gemini_service.py` and `backend/routers/ai.py` confirms:

| Assessment item | Finding |
|----------------|---------|
| Python `logging` module used | ✅ Not used — neither file imports or calls `logging.*` |
| `ANTHROPIC_API_KEY` value in log statements | ✅ No — key is loaded via `os.getenv()` and passed only to the Anthropic SDK client |
| Full prompt text in log statements | ✅ No — prompt text is passed to the Anthropic SDK; no `print()` or `logging.*` calls exist in the call path |
| Full response text in log statements | ✅ No — response text is returned to the caller; not logged at application level |

**Application-level finding:** The Python application does not log the API key, full prompt text, or full response text via Python's logging framework. The only persistent record of API calls is the `claude_audit_log` table in the database, which captures metadata only (model version, token counts, estimated cost, hashed input/output).

---

## 3. Log Level Policy (AC-03)

The following log level policy applies to Claude API trace events:

| Log level | What is logged | Permitted in production? |
|-----------|---------------|-------------------------|
| **INFO** | Request metadata: endpoint called, model version, token counts (input/output), estimated cost, request latency | ✅ Yes |
| **DEBUG** | Full prompt text, full response text, raw API request/response bodies | ❌ No — DEBUG level must never be enabled in production |
| **ERROR** | Exception messages, error codes from the Anthropic API | ✅ Yes — must NOT include the API key value in the error message |

**Rule:** Production Render services must run at log level `INFO` or higher. `DEBUG` is permitted only in local development environments.

**ANTHROPIC_API_KEY exclusion rule:** The API key value must never appear in any log entry at any level. If an exception message would include the key value, it must be masked (e.g., `ANTHROPIC_API_KEY=***`) before logging.

---

## 4. Log Retention Policy (AC-04)

| Log store | Retention period | Notes |
|-----------|-----------------|-------|
| Render application logs (stdout/stderr) | 7 days (Render default) | Operational logs; no sensitive content if this policy is followed |
| `claude_audit_log` database table | Indefinite (pre-SI-02) | Metadata only; does not contain prompt text or API key |
| Render access logs (HTTP request/response) | 7 days (Render default) | Request path and status only; body not captured by default |

**Pre-SI-02 advisory:** Before the SI-02 position drift monitoring sprint, define a formal log retention policy (duration, archival, deletion). The current 7-day Render default is acceptable for the interim period. File as: complete `docs/ops/log_retention_policy.md` during SI-02 sprint planning.

---

## 5. Production Log Verification Requirement (AC-02 — Pending)

**Status: PENDING — human action required**

AC-02 of ST-03 requires confirmation that Render production logs do NOT capture `ANTHROPIC_API_KEY` or full prompt text.

**Evidence required from Infrastructure & Operations Owner:**

1. Access the Render dashboard for both staging (`swing-trading-model`) and production environments
2. Search logs for the string `ANTHROPIC_API_KEY` — confirm zero matches
3. Make one test call to `POST /trade-plans/{plan_id}/generate-thesis` in staging
4. Inspect the resulting Render log entry — confirm it does not contain the full prompt text or the API key value
5. If any exposure is found: remediate by adjusting Render log level settings, then re-verify

**Documentation of confirmation:**
Record the result in §6 Sign-Off below. If remediation was required, describe the change made.

---

## 6. Sign-Off

| Role | Status | Date | Notes |
|------|--------|------|-------|
| Infrastructure & Operations Owner | Pending — AC-02 Render log inspection required | — | Must confirm §5 evidence before Status → Active |
| Cybersecurity & Trust Lead | Pending | — | Review §3 log level policy and §5 verification result |
