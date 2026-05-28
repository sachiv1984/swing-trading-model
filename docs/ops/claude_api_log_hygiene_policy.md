Owner: Infrastructure & Operations Owner
Class: Operational Policy (Class 2)
Status: Active
Version: 1.0
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

## 5. Production Log Verification (AC-02)

**Status: CONFIRMED CLEAN — 2026-05-28**

Infrastructure & Operations Owner inspected Render staging logs on 2026-05-28 during ST-06 live timing run. The following was confirmed:

| Check | Result |
|-------|--------|
| `ANTHROPIC_API_KEY` present in staging logs | ✅ **Not found** — zero matches in full log output |
| Full prompt text present in staging logs | ✅ **Not found** — `generate-thesis` log entry shows uvicorn access log format only: `"POST /trade-plans/{plan_id}/generate-thesis HTTP/1.1" 200 OK` |
| Request body captured in logs | ✅ **Not captured** — Render/uvicorn default logging records method, path, HTTP version, and status code only; no request or response bodies |
| Log format confirmed | Render application logs (uvicorn INFO level): timestamp, server process info, HTTP access lines only |
| Remediation required | ✅ **None** — log output is clean at current uvicorn INFO level |

**Evidence source:** Infrastructure & Operations Owner inspected Render staging service logs covering the redeployment at 15:00 UTC and subsequent test calls to `POST /trade-plans/5aed7fc2.../generate-thesis` at 15:14 UTC (2026-05-28). The log line observed:
```
2026-05-28T15:14:28.22724873Z INFO: 132.145.73.237:0 - "POST /trade-plans/5aed7fc2-39ac-4eb2-bbd3-5a7770713cdc/generate-thesis HTTP/1.1" 200 OK
```
No API key value, prompt text, or response body visible.

---

## 6. Sign-Off

| Role | Status | Date | Notes |
|------|--------|------|-------|
| Infrastructure & Operations Owner | ✅ APPROVED | 2026-05-28 | Render staging logs inspected 2026-05-28. ANTHROPIC_API_KEY: not present. Full prompt text: not present. Log format: uvicorn access log (path + status only). No remediation needed. |
| Cybersecurity & Trust Lead | ✅ APPROVED | 2026-05-28 | §3 log level policy reviewed — INFO/DEBUG boundary correct; API key exclusion rule appropriate. §5 verification evidence reviewed and accepted. |
