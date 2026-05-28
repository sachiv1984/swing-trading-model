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

| Endpoint / Function | File | Purpose |
|--------------------|------|---------|
| `POST /trade-plans/{plan_id}/generate-thesis` | `backend/services/gemini_service.py` — `generate_setup_thesis()` | Generate a pre-trade thesis (legacy single-field) |
| `POST /trade-plans/generate-plan` | `backend/services/gemini_service.py` — `generate_full_plan()` | Generate all trade plan fields in one call |
| `POST /ai/journal-summary` | `backend/services/ai_service.py` — `summarise_journal_notes()` | Summarise trade journal notes |
| `POST /ai/check-daily-cost` | `backend/services/gemini_service.py` — `check_and_alert_daily_cost()` | Check daily Claude API spend and send Telegram alert if threshold exceeded |
| `GET /ai/claude-audit-log` | `backend/routers/ai.py` | Query the immutable Claude API call audit trail (read-only, no API call made) |

The `ANTHROPIC_API_KEY` environment variable and full Claude prompt/response text are the primary sensitive assets this policy governs. The permanent structured audit record of every Claude API call is stored in the `gemini_audit_log` and `claude_audit_log` database tables.

---

## 2. Log Level Policy

### 2.1 Permitted at INFO Level (Production Default)

The following data items are permitted to appear in platform logs at INFO level:

| Item | Permitted | Example |
|------|-----------|---------|
| Endpoint called | Yes | `POST /trade-plans/{plan_id}/generate-thesis` |
| Model version | Yes | `claude-haiku-4-5` |
| Prompt version | Yes | `v3.0` |
| Input token count | Yes | `prompt_tokens=142` |
| Output token count | Yes | `completion_tokens=87` |
| Estimated cost (USD) | Yes | `estimated_cost_usd=0.00000142` |
| Input hash (SHA-256 truncated) | Yes | `input_hash=a3f1b2c4` (first 16 hex chars — not reversible) |
| Output hash (SHA-256 truncated) | Yes | `output_hash=d9e7f123` |
| Response summary | Yes — first 100 characters maximum | Truncated thesis preview for operational diagnostics |
| Error messages from API failures | Yes — truncated to 120 characters | `Claude API error: Connection timeout` |

### 2.2 Restricted to DEBUG Level Only

The following data items must NEVER appear at INFO level in production logs. They may be emitted at DEBUG level in local development environments only:

| Item | Restriction | Rationale |
|------|-------------|-----------|
| Full prompt text | DEBUG only — never INFO in production | Prompts may contain sensitive trade context (ticker, signal scores, plan fields) |
| Full response text | DEBUG only — never INFO in production | Responses contain AI-generated trade thesis content |
| ANTHROPIC_API_KEY value | Never logged at any level | Secret credential — must not appear in any log stream |
| Raw `signal_data` dict | DEBUG only — never INFO in production | Contains proprietary signal parameters |
| Raw `plan_data` dict | DEBUG only — never INFO in production | Contains proprietary plan fields |

### 2.3 Production Log Level Requirement

Production deployments (Render staging and production environments) must be configured with log level `INFO` or higher. The `DEBUG` log level must never be the active log level in a production or staging environment.

---

## 3. Sensitive Data Exclusions

The following rules are mandatory and non-negotiable:

### 3.1 ANTHROPIC_API_KEY

- The `ANTHROPIC_API_KEY` value must never appear in any log line, error message, exception traceback, or audit record at any log level.
- Current implementation: `gemini_service.py` reads the key via `os.getenv("ANTHROPIC_API_KEY", "")` and passes it to `anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)`. The key value is not present in any log statement in that file (confirmed by code inspection 2026-05-28).
- Current implementation: `ai_service.py` reads the key via `os.getenv("ANTHROPIC_API_KEY")` and passes it to `anthropic.Anthropic(api_key=api_key)`. The key value is not present in any log statement in that file (confirmed by code inspection 2026-05-28).
- Error paths: `generate_setup_thesis()` and `generate_full_plan()` return `{"available": False, "error": "ANTHROPIC_API_KEY not configured"}` when the key is absent. This string does not contain the key value. Confirmed safe.
- Exception truncation: `str(exc)[:120]` is applied to Anthropic API exceptions before they appear in error responses. Engineers must verify that Anthropic SDK exceptions do not embed the API key in the exception message string.

### 3.2 Full Prompt Text

- Full prompt text (the formatted `_FULL_PLAN_PROMPT` or `_THESIS_PROMPT_TEMPLATE` output) must not appear at INFO level in any log stream.
- Rationale: Prompts include ticker identifiers, signal scores, and momentum metrics that are proprietary operational data.
- Permitted: `input_hash` (SHA-256 truncated to 16 hex chars) may appear at INFO level as a non-reversible reference.

### 3.3 Full Response Text

- Full AI response text must not appear at INFO level in any log stream.
- Permitted: The first 100 characters of the response text may be logged at INFO for operational diagnostics.
- Permitted: `output_hash` (SHA-256 truncated to 16 hex chars) may appear at INFO level.
- Permanent record: The full response text is not stored in `gemini_audit_log` or `claude_audit_log` — only hashes and token counts are persisted. This is the correct design.

### 3.4 Journal Note Content

- `POST /ai/journal-summary` concatenates user-authored trade journal notes into the prompt. This content must not appear at INFO level in production logs.
- The `log_ai_summary_run()` audit function stores `summary_text` in the `ai_summary_audit_log` table. This is a database record, not a log stream entry, and is governed by §4.

---

## 4. Log Retention Policy

### 4.1 Platform Log Stream (Render Logs)

| Environment | Retention Period | Authority |
|-------------|-----------------|-----------|
| Production | 30 days | Render platform default; reviewed at SI-02 |
| Staging | 7 days | Render platform default; reviewed at SI-02 |

The platform log stream is ephemeral and operational. It is not the primary compliance record for Claude API usage.

### 4.2 Database Audit Records (Primary Compliance Record)

| Table | Retention | Notes |
|-------|-----------|-------|
| `gemini_audit_log` | Permanent (no TTL) | Contains model version, prompt version, token counts, cost per call, input/output hashes. No prompt or response text stored. |
| `claude_audit_log` | Permanent (no TTL) | Contains endpoint, model, prompt version, token counts, cost per call. No prompt or response text stored. |
| `ai_summary_audit_log` | Permanent (no TTL) | Contains journal summary metadata: trade IDs, date range, trade count, model version, and the summary text itself. |

### 4.3 Pre-SI-02 Review Trigger

When SI-02 (observability and monitoring infrastructure) is scoped and planned, the Infrastructure & Operations Owner must review and update this section with:
- The target log aggregation platform and its retention configuration
- Any cost/compliance requirements that necessitate longer retention
- Structured log format for Claude API events

---

## 5. Production Log Verification

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

---

## Appendix A — Related Documents

| Document | Relationship |
|----------|-------------|
| `docs/security/anthropic_api_key_scope_review.md` | Canonical security posture for `ANTHROPIC_API_KEY` — key scope, application controls, audit logging status |
| `docs/ops/external_api_credential_inventory.md` | Full inventory of external API credentials including `ANTHROPIC_API_KEY` |
| `docs/ops/gemini_cost_tracking.md` | Claude API cost tracking policy (advisory threshold, monitoring) |
| `backend/services/gemini_service.py` | Primary implementation — thesis generation, full plan generation, cost check |
| `backend/services/ai_service.py` | Secondary implementation — journal summarisation |
| `backend/routers/ai.py` | AI router — journal summary, audit log query, daily cost check endpoints |
