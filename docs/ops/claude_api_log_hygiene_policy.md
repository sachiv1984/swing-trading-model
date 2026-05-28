**Owner:** Infrastructure & Operations Owner
**Class:** Operational Policy (Class 2)
**Status:** Draft
**Version:** 0.1
**Last Updated:** 2026-05-28
**Cycle:** 2026-05-27__release-v4.2 (ST-03)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Claude API Log Hygiene Policy

## 1. Scope

This policy governs logging behaviour for all Claude API calls originating from the swing-trading-model backend. The Claude API is used in the following contexts:

| Endpoint / Function | File | Purpose |
|--------------------|------|---------|
| `POST /trade-plans/{plan_id}/generate-thesis` | `backend/services/gemini_service.py` — `generate_setup_thesis()` | Generate a pre-trade thesis (legacy single-field) |
| `POST /trade-plans/generate-plan` | `backend/services/gemini_service.py` — `generate_full_plan()` | Generate all trade plan fields in one call |
| `POST /ai/journal-summary` | `backend/services/ai_service.py` — `summarise_journal_notes()` | Summarise trade journal notes |
| `POST /ai/check-daily-cost` | `backend/services/gemini_service.py` — `check_and_alert_daily_cost()` | Check daily Claude API spend and send Telegram alert if threshold exceeded |
| `GET /ai/claude-audit-log` | `backend/routers/ai.py` | Query the immutable Claude API call audit trail (read-only, no API call made) |

The permanent structured audit record of every Claude API call is stored in the `gemini_audit_log` and `claude_audit_log` database tables. That database record is the authoritative cost and compliance trail; this policy governs the ephemeral platform log stream (e.g. Render log drain, stdout).

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
- Exception truncation: `str(exc)[:120]` is applied to Anthropic API exceptions before they appear in error responses. Engineers must verify that Anthropic SDK exceptions do not embed the API key in the exception message string. This is a known vector — see §5.

### 3.2 Full Prompt Text

- Full prompt text (the formatted `_FULL_PLAN_PROMPT` or `_THESIS_PROMPT_TEMPLATE` output) must not appear at INFO level in any log stream.
- Rationale: Prompts include ticker identifiers, signal scores, and momentum metrics that are proprietary operational data.
- Permitted: `input_hash` (SHA-256 truncated to 16 hex chars) may appear at INFO level as a non-reversible reference.

### 3.3 Full Response Text

- Full AI response text must not appear at INFO level in any log stream.
- Permitted: The first 100 characters of the response text may be logged at INFO for operational diagnostics (e.g. confirming a non-empty response was received).
- Permitted: `output_hash` (SHA-256 truncated to 16 hex chars) may appear at INFO level.
- Permanent record: The full response text is not stored in `gemini_audit_log` or `claude_audit_log` — only hashes and token counts are persisted. This is the correct design.

### 3.4 Journal Note Content

- `POST /ai/journal-summary` concatenates user-authored trade journal notes into the prompt. This content must not appear at INFO level in production logs.
- The `log_ai_summary_run()` audit function stores `summary_text` in the `ai_summary_audit_log` table. This is a database record, not a log stream entry, and is governed by §4.

---

## 4. Log Retention Policy

This section defines the retention policy for Claude API log data in the pre-SI-02 phase. SI-02 (observability infrastructure) will supersede this policy when shipped.

### 4.1 Platform Log Stream (Render Logs)

| Environment | Retention Period | Authority |
|-------------|-----------------|-----------|
| Production | 30 days | Render platform default; reviewed at SI-02 |
| Staging | 7 days | Render platform default; reviewed at SI-02 |

The platform log stream is ephemeral and operational. It is not the primary compliance record for Claude API usage.

Rationale for 30-day retention: sufficient for operational incident investigation; beyond 30 days, the structured database audit record is the authoritative source.

### 4.2 Database Audit Records (Primary Compliance Record)

| Table | Retention | Notes |
|-------|-----------|-------|
| `gemini_audit_log` | Permanent (no TTL) | Contains model version, prompt version, token counts, cost per call, input/output hashes. No prompt or response text stored. |
| `claude_audit_log` | Permanent (no TTL) | Contains endpoint, model, prompt version, token counts, cost per call. No prompt or response text stored. |
| `ai_summary_audit_log` | Permanent (no TTL) | Contains journal summary metadata: trade IDs, date range, trade count, model version, and the summary text itself. |

The permanent database record is the authoritative Claude API audit trail for cost tracking, compliance, and the SI-02 observability foundation.

### 4.3 Pre-SI-02 Review Trigger

The retention periods above are interim. When SI-02 (observability and monitoring infrastructure) is scoped and planned, the Infrastructure & Operations Owner must review and update this section with:
- The target log aggregation platform and its retention configuration
- Any cost/compliance requirements that necessitate longer retention
- Structured log format for Claude API events

---

## 5. AC-02 Compliance Pending — Render Production Log Inspection

**Status: Pending — human action required**

AC-02 of ST-03 requires confirmation that the Render production environment does not capture `ANTHROPIC_API_KEY` or full prompt text in its log drain. This cannot be verified by code inspection alone; it requires inspection of actual Render log output.

### 5.1 Evidence Required

The Infrastructure & Operations Owner must provide the following evidence before this policy can be promoted from `Draft` to `Active`:

1. A Render log sample for the production environment showing log entries produced during a `POST /trade-plans/{plan_id}/generate-thesis` or `POST /trade-plans/generate-plan` call, confirming:
   - No line contains the string value of `ANTHROPIC_API_KEY`
   - No line contains the full prompt text (look for the string "You are a systematic swing trader" as a sentinel — its presence would indicate full prompt logging from an unexpected source such as the Anthropic SDK's own debug output or a Render access log capturing request bodies)
   - No HTTP access log entry contains the raw request body (which could contain signal data)

2. Confirmation of the active log level (`INFO` or `WARNING`) in the Render production environment.

3. Confirmation that Render's HTTP access log (if enabled) does not capture POST request bodies.

### 5.2 Items Requiring Verification in Current Codebase

The following items were identified during code inspection (2026-05-28) that warrant specific verification in the Render log sample:

| Item | Location | Risk | Verification Required |
|------|----------|------|-----------------------|
| Anthropic SDK exception messages | `gemini_service.py:161`, `gemini_service.py:228`, `ai_service.py:71` | Anthropic SDK exceptions could theoretically embed request metadata (including partial prompt) in the exception string. Truncation to 120 chars reduces but does not eliminate risk. | Confirm no production exception log contains prompt text or key fragments |
| FastAPI default request logging | `backend/main.py` — Uvicorn/FastAPI middleware | Uvicorn's default access log emits HTTP method, path, and status code — it does NOT log request bodies. However, confirm this is the case in the Render environment. | Confirm Render access log format does not include request body |
| `summary_text` in `ai_summary_audit_log` | `backend/routers/ai.py:96–101` | The journal summary text is stored in the database table (not a log stream). Confirm this write does not emit the summary to stdout. | Inspect log output from `POST /ai/journal-summary` calls |

### 5.3 Remediation Path (If Violations Found)

If any of the above verification checks fail:

1. **API key in logs:** Rotate `ANTHROPIC_API_KEY` immediately. Audit `gemini_service.py` and `ai_service.py` for any code path that could pass the key to a logging call. File a P1 security backlog item.
2. **Full prompt in logs:** Identify the source (application code, Anthropic SDK debug mode, or infrastructure). Disable debug logging at the source. File a P2 security backlog item.
3. **Request body in access logs:** Disable request body capture in Render log configuration. File a P2 security backlog item.

---

## 6. Sign-Off

This policy requires sign-off from the following roles before promotion to `Active` status:

| Role | Status | Date | Notes |
|------|--------|------|-------|
| Infrastructure & Operations Owner | Pending | — | Must confirm Render production log sample per §5.1 evidence requirements |
| Cybersecurity & Trust Lead | Pending | — | Must review §3 sensitive data exclusions and §5.2 verification items against security posture documented in `docs/security/anthropic_api_key_scope_review.md` |

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
