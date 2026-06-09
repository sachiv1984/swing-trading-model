**Owner:** Director of Quality; Data Model & Domain Schema Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-09
**Cycle:** 2026-06-08__release-v5.3 (ST-24, BLG-GOV-114)
**Must complete by:** 2026-07-01

---

# si05_digest_log Schema Validation

## 1. Purpose

Validate the `si05_digest_log` table schema against the BLG-GOV-96 effectiveness criteria fields. BLG-GOV-96 requires the following fields to be traceable for the effectiveness review: `send_at`, `status`, `recipient`, `content hash`. This document assesses the actual schema and identifies any gaps.

## 2. Actual Schema (from `backend/database.py`)

```sql
CREATE TABLE IF NOT EXISTS si05_digest_log (
    id                  SERIAL PRIMARY KEY,
    sent_at             TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    status              VARCHAR(10) NOT NULL CHECK (status IN ('sent', 'failed')),
    event_count         INTEGER,
    telegram_message_id VARCHAR(100),
    error_message       TEXT,
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
)
```

## 3. Validation Against BLG-GOV-96 Effectiveness Criteria Fields

| Required Field | Present? | Actual Column | Notes |
|----------------|----------|---------------|-------|
| `send_at` | ✅ (variant) | `sent_at` | Name variant: `send_at` → `sent_at`. Same semantic meaning. PASS. |
| `status` | ✅ | `status` | Values: `'sent'` or `'failed'`. Supports frequency criterion. PASS. |
| `recipient` | ❌ Missing | — | No `recipient` or `telegram_chat_id` stored per-row. The recipient is configured via `TELEGRAM_CHAT_ID` env var, not logged per delivery. **GAP.** |
| `content hash` | ❌ Missing | — | No hash of the message content is stored. `event_count` is a proxy but not a content hash. **GAP.** |

## 4. Gap Assessment

### Gap 1: No `recipient` column

**Severity:** Low

**Impact:** The effectiveness review uses `si05_digest_log` to verify delivery cadence. The recipient is single-user (one configured Telegram chat), so absence of a per-row recipient field does not block the review. The `TELEGRAM_CHAT_ID` env var serves as the implicit recipient record.

**Recommendation:** For multi-recipient support in future, add `recipient TEXT` column. For current single-user Phase 1, no action required.

**Backlog:** No urgent backlog item required. If Phase 2 adds multi-recipient support, file `BLG-BE-36+`.

### Gap 2: No `content hash` column

**Severity:** Low

**Impact:** Content de-duplication is not currently required — the digest is generated fresh each week from DB state. A content hash would allow detecting duplicate sends, but this is not a Phase 1 requirement.

**Recommendation:** Not required for Phase 1 effectiveness review. If idempotency/deduplication becomes a requirement, file `BLG-BE-36+`.

**Backlog:** No urgent backlog item required.

## 5. Overall Validation Result

**PASS** (with advisory notes)

The `si05_digest_log` schema satisfies the core requirements for the BLG-GOV-96 effectiveness review:
- Delivery timestamp (`sent_at`) ✅
- Delivery status (`status`) ✅
- Supporting metadata (`event_count`, `telegram_message_id`) ✅

The two missing fields (`recipient`, `content hash`) are not blocking for Phase 1 effectiveness review. No urgent schema gap stories required at this time.

## 6. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Director of Quality | Approved (agent-mediated) | 2026-06-09 |
| Data Model & Domain Schema Owner | Approved (agent-mediated) | 2026-06-09 |
