**Owner:** AI Compliance & Governance Officer
**Class:** Governance Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-29
**Review Cadence:** On addition of any new AI-touching feature or model change
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# AI Feature Inventory

This document provides a formal inventory of all AI-touching features in the swing trading model application, for compliance, audit, and §13 review traceability. Maintained by the AI Compliance & Governance Officer; reviewed by the Strategy Rules & System Intent Owner on any new entry.

**Governing principle:** AI output in this system is display-only and must NOT feed into any signal, scoring, or recommendation pipeline. All features in this inventory are subject to this constraint (SRB-v1.7).

---

## Feature Inventory

### Feature 1 — Claude Trade Setup Thesis Generation

| Field | Value |
|-------|-------|
| **Feature name** | Claude Trade Setup Thesis Generation |
| **Endpoint** | `POST /trade-plans/{plan_id}/generate-thesis` |
| **Router file** | `backend/routers/trade_plans.py` |
| **Service** | `backend/services/gemini_service.py` → `generate_setup_thesis()` |
| **Model used** | Claude Haiku (Anthropic API via `ANTHROPIC_API_KEY`) |
| **Purpose** | Generates a plain-text trade setup thesis for a given trade plan, incorporating ticker, market, setup type, entry rationale, and confirmation criteria. Output is displayed in the TradePlan edit view ("Improve with AI" button). |
| **§13 compliance status** | Conditionally compliant — display-only output; thesis text is a writing aid and must not be used as a trading signal, entry trigger, or position sizing input. Reviewed at v4.1 (Claude API migration from Gemini). |
| **Data inputs** | `plan_id` (path param); from trade plan record: `ticker`, `market`, `setup_type`, `entry_rationale`, `confirmation_criteria` |
| **Data outputs** | `status`, `data.thesis` (plain text thesis string), `data.model` (model version), audit record written to `claude_audit_log` |
| **Audit trail** | Every invocation logged to `claude_audit_log` table (ST-07/ST-08 v4.1) |
| **Environment dependency** | `ANTHROPIC_API_KEY` — graceful degradation when absent (HTTP 200 with error payload) |

---

### Feature 2 — AI Journal Summarisation

| Field | Value |
|-------|-------|
| **Feature name** | AI Journal Summarisation |
| **Endpoint** | `POST /ai/journal-summary` |
| **Router file** | `backend/routers/ai.py` |
| **Service** | `backend/services/ai_service.py` → `summarise_journal_notes()` |
| **Model used** | Claude API (Anthropic; model version returned in response `model` field) |
| **Purpose** | Summarises entry and exit journal notes from closed trades over a specified date range or trade ID list. Output is displayed in the research view. AI output is display-only — not used in any calculation. |
| **§13 compliance status** | Conditionally compliant — SRB-v1.7 CONDITIONALLY COMPLIANT; output is display-only; must not feed into signals, scoring, or recommendation pipeline. Contract: `docs/specs/api_contracts/ai_endpoints.md` v1.2. |
| **Data inputs** | `trade_ids` (optional list of int), `date_from` (optional date), `date_to` (optional date); fetches `entry_note`, `exit_note` from `trade_history` table |
| **Data outputs** | `summary` (plain-text LLM summary), `trade_count` (int), `model` (string), `cached` (bool), `message` (optional string) |
| **Audit trail** | Every invocation logged to AI audit log via `log_ai_summary_run()` (non-blocking — audit failure does not block response) |
| **Environment dependency** | Anthropic API key; graceful degradation expected when key absent |

---

### Feature 3 — Claude API Daily Cost Threshold Alert

| Field | Value |
|-------|-------|
| **Feature name** | Claude API Daily Cost Threshold Alert |
| **Endpoint** | `POST /ai/check-daily-cost` |
| **Router file** | `backend/routers/ai.py` |
| **Service** | `backend/services/gemini_service.py` → `check_and_alert_daily_cost()` |
| **Model used** | None — reads `claude_audit_log` table; sends Telegram alert (no LLM call) |
| **Purpose** | Operational monitoring feature. Checks today's Claude API spend against a configured threshold (`AI_DAILY_COST_THRESHOLD`). If threshold is exceeded, sends a Telegram alert to notify the operations team. Intended for daily scheduler invocation (Render cron / external scheduler). |
| **§13 compliance status** | Not applicable — this is operational monitoring, not an AI output feature. No §13 review required. No AI-generated content is produced or displayed. |
| **Data inputs** | `AI_DAILY_COST_THRESHOLD` (env var, USD); `claude_audit_log` table rows (today's invocations) |
| **Data outputs** | Threshold check result (JSON); Telegram alert message (if threshold exceeded) |
| **Audit trail** | Reads from `claude_audit_log`; no separate audit trail for the check itself |
| **Environment dependency** | `AI_DAILY_COST_THRESHOLD` (config), `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` |

---

## Compliance Summary

| Feature | §13 Status | Display-Only Enforced | Audit Trail |
|---------|------------|----------------------|-------------|
| Claude thesis generation | Conditionally compliant | Yes — thesis text shown in UI, not used in calculations | Yes — claude_audit_log |
| AI journal summarisation | Conditionally compliant (SRB-v1.7) | Yes — summary shown in research view, no data pipeline use | Yes — ai audit log |
| Daily cost alert | N/A (operational monitoring) | N/A | Reads from claude_audit_log |

---

## Review History

| Date | Reviewer | Outcome |
|------|----------|---------|
| 2026-05-29 | AI Compliance & Governance Officer | Initial inventory created — 3 features documented |
| 2026-05-29 | Strategy Rules & System Intent Owner | Reviewed — all features confirmed display-only; §13 conditionally compliant designations confirmed |
