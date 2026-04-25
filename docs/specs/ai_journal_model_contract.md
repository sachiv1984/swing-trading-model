**Owner:** AI Compliance & Governance Officer
**Class:** Class 2 Canonical Specification
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-04-25
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Backlog reference:** BLG-AI-02

---

# AI Journal Model Version Contract

## Purpose

This document is the canonical contract specifying which Claude model version executes AI Journal summarisation, where the model version is configured, and the process for incrementing the contract when the model version changes.

It is referenced from `backend/services/ai_service.py` and must be updated whenever the model version is changed. Audit log entries in `ai_audit_log.model_version` are the runtime trace of actual model versions used.

---

## Current Model Version

| Field | Value |
|-------|-------|
| Model version | `claude-haiku-4-5-20251001` |
| Effective from | 2026-04-25 |
| Anthropic model family | Claude Haiku 4.5 |
| Use case | AI Journal trade summarisation (POST /ai/journal-summary) |

---

## Configuration Location

The model version is configured as a constant in:

```
backend/services/ai_service.py
_DEFAULT_MODEL = "claude-haiku-4-5-20251001"
```

This constant is the single authoritative location. No other file should hardcode the model version — all callers must reference this constant or the environment variable override (see below).

**Environment variable override:** If the `AI_JOURNAL_MODEL` environment variable is set, it takes precedence over `_DEFAULT_MODEL`. This allows runtime version pinning without code changes.

---

## Change Process

When the model version must be changed (e.g., a model is retired, a newer model is mandated, or a performance/cost review warrants upgrade):

1. **Update `ai_service.py`:** Change `_DEFAULT_MODEL` to the new model ID.
2. **Update this contract:** Update the "Current Model Version" table above — set the new model ID, effective date, and family.
3. **Append a change record** to the "Version History" section below.
4. **Notify AI Compliance & Governance Officer:** The change must be reviewed for compliance implications before deployment.
5. **Verify `ai_audit_log`:** Post-change, confirm the `model_version` column in new audit log rows reflects the updated model ID.

Changing the model version without updating this contract is a compliance deviation.

---

## Audit Log Integration

Every AI Journal summarisation run logs the actual model version used to `ai_audit_log.model_version` (BLG-AI-01 schema). This provides a historical audit trail of which model was used for each summarisation event.

The contract version and the audit log version should match for all runs after the contract effective date. If they diverge, investigate whether the environment variable override is active.

---

## Version History

| Date | Old Model | New Model | Authority | Reason |
|------|-----------|-----------|-----------|--------|
| 2026-04-25 | (initial) | `claude-haiku-4-5-20251001` | Head of Specs Team (ST-16, BLG-AI-02) | Initial contract creation |
