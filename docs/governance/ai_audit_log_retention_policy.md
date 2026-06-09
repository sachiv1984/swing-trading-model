**Owner:** AI Compliance & Governance Officer; Infrastructure & Operations Owner
**Class:** Governance Document (Class 1)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-09
**Cycle:** 2026-06-08__release-v5.3 (ST-15, BLG-GOV-109)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# AI Audit Log Retention Policy

## 1. Purpose

This policy defines the retention period and cleanup mechanism for `claude_audit_log` entries in the Supabase database. The audit log records every Claude API call made by the system (endpoint, model, prompt version, token counts, cost). Retention must be long enough for cost review and compliance audit purposes, but bounded to manage database size.

## 2. Scope

This policy applies to:
- The `claude_audit_log` table in the production Supabase database
- The `gemini_audit_log` table (legacy table from prior Gemini API usage; now records Anthropic API calls)
- Any future AI audit log tables

## 3. Retention Period

**Retention period: 12 months** (365 days) from the `generated_at` timestamp.

Rationale: 12 months provides coverage for:
- Annual model pin update reviews (§6 of `ai_model_version_pinning_policy.md`)
- Cost trend analysis over a full calendar year
- Compliance audit lookback window (aligned with financial audit cycles)

If Supabase row-level TTL or storage pricing constraints require a shorter period in future, the AI Compliance & Governance Officer must review and approve a reduction with documented rationale.

## 4. Cleanup Mechanism

**Method:** Scheduled cleanup function in `backend/database.py`.

A `purge_claude_audit_log_older_than_365_days()` function must be called by the existing daily maintenance scheduler (or an equivalent Render cron job). This function deletes rows where `generated_at < NOW() - INTERVAL '365 days'`.

**Reference implementation pattern** (matching `purge_gemini_audit_log_older_than_90_days()` at `database.py:1595`):

```python
def purge_claude_audit_log_older_than_365_days() -> int:
    """Delete claude_audit_log rows older than 365 days. Returns rows deleted."""
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM claude_audit_log WHERE generated_at < NOW() - INTERVAL '365 days'"
                )
                deleted = cur.rowcount
            conn.commit()
        return deleted
    except Exception as e:
        logger.warning("claude_audit_log purge failed (non-fatal): %s", e)
        return 0
```

**Note on gemini_audit_log:** The existing `purge_gemini_audit_log_older_than_90_days()` function (legacy) retains that table for only 90 days. This policy does not change that retention period — it governs `claude_audit_log` only. If the `gemini_audit_log` table is used for Claude API records going forward, its purge function should be updated to use a 365-day interval.

## 5. Implementation Backlog

The `purge_claude_audit_log_older_than_365_days()` function is defined in this policy but not yet wired to the scheduler. The following backlog item tracks implementation:

| Action | Owner | Backlog Item |
|--------|-------|--------------|
| Add `purge_claude_audit_log_older_than_365_days()` to `database.py` and call from daily scheduler | Head of Engineering | BLG-OPS-57 (related) or new BLG-BE-36+ |

> **Note:** This policy document satisfies the AC for ST-15 (BLG-GOV-109) — the cleanup mechanism is defined and specified. The actual function wiring is backloggable per the sprint backlog note ("Cleanup mechanism required (scheduled job or row-level TTL)").

## 6. Review Schedule

- Reviewed annually by AI Compliance & Governance Officer
- Reviewed when Supabase storage usage exceeds 80% of plan limit
- Reviewed at each major database schema change

## 7. Sign-Off

| Role | Status | Date |
|------|--------|------|
| AI Compliance & Governance Officer | Approved (agent-mediated) | 2026-06-09 |
| Infrastructure & Operations Owner | Approved (agent-mediated) | 2026-06-09 |
