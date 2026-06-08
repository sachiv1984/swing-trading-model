# digest_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 0.3
**Last Updated:** 2026-06-08
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Sprint:** 2026-03-31__release-v2.4 — ST-08 (BLG-FEAT-14 BE component)
**Signed off by:** Head of Specs Team

---

# Weekly Digest Endpoints

## Scope constraint

All response fields must be raw numeric or boolean values. No generated text, narrative, or interpretation is permitted in any response field. This constraint was confirmed in Challenger debate (roadmap rebalance 2026-03-31).

---

## GET /digest/weekly

**Purpose**

Return a 7-day summary of trading activity for the weekly digest display. All fields cover the last 7 UTC calendar days unless otherwise noted.

**Method & Path**

- `GET /digest/weekly`

**Idempotency**

- Safe to refresh (read-only). Values reflect current DB state at call time.

---

### Request

No parameters.

---

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "realised_pnl_7d": 166.10,
  "unrealised_pnl_delta_7d": -42.80,
  "alerts_fired_7d": 5,
  "alerts_dismissed_7d": 3,
  "compliance_score_current": 80.0,
  "compliance_score_7d_ago": 75.0,
  "staleness_hours": 18.5,
  "as_of_utc": "2026-04-01T10:30:00+00:00"
}
```

#### Field definitions

| Field | Type | Notes |
|-------|------|-------|
| `realised_pnl_7d` | float | Sum of `trade_history.pnl` for trades with `exit_date >= today − 7 days`. In GBP. |
| `unrealised_pnl_delta_7d` | float \| null | Change in total unrealised P&L over 7 days: most recent `portfolio_history.unrealised_pnl` minus the closest snapshot on or before the 7-day cutoff. Null if insufficient snapshot history. |
| `alerts_fired_7d` | integer | Count of `notifications` rows created in the last 7 days. |
| `alerts_dismissed_7d` | integer | Count of `notifications` rows with `read = TRUE` created in the last 7 days. |
| `compliance_score_current` | float | Journal completion rate across all closed trades: `(trades_with_notes / total_trades) × 100`. Range 0–100. |
| `compliance_score_7d_ago` | float | Journal completion rate for trades closed before the 7-day window (baseline for trend). Range 0–100. |
| `staleness_hours` | float \| null | Hours elapsed since the most recent `portfolio_history` snapshot. Null if no snapshots exist. |
| `as_of_utc` | string (ISO 8601 UTC) | Timestamp this response was computed. |

**No generated text:** All fields are raw numeric or boolean values. No narrative, interpretation, or recommendation fields are present or permitted in this endpoint.

---

### Error responses

Errors use the standard error envelope from **conventions.md §13**.

| HTTP Status | Condition |
|-------------|-----------|
| `500` | Database connection failed or query error |

---

## Data Model Cross-Reference

| Field | Source table | Source column |
|-------|-------------|---------------|
| `realised_pnl_7d` | `trade_history` | `pnl`, filtered by `exit_date` |
| `unrealised_pnl_delta_7d` | `portfolio_history` | `unrealised_pnl`, `snapshot_date` |
| `alerts_fired_7d` | `notifications` | `created_at` |
| `alerts_dismissed_7d` | `notifications` | `read`, `created_at` |
| `compliance_score_*` | `trade_history` | `entry_note`, `exit_note`, `exit_date` |
| `staleness_hours` | `portfolio_history` | `snapshot_date` |

---

---

## POST /digest/si05/send

**Purpose**

Trigger the SI-05 Phase 1 weekly strategy integrity digest via Telegram. Fetches arc5-compliance metrics from SI-01 (pre-entry validation) and SI-03 (red flag journal) and sends a formatted MarkdownV2 message per the SI-05 Telegram message format specification (BLG-GOV-86).

Intended for weekly cron/scheduled invocation. Safe to retry — message content reflects current DB state at call time.

**Method & Path**

- `POST /digest/si05/send`

**Request**

No body required. No query parameters.

**Response (200 — sent)**

```json
{
  "status": "ok",
  "sent": true,
  "message_length": 265,
  "error": null
}
```

**Response (200 — not sent)**

```json
{
  "status": "error",
  "sent": false,
  "message_length": 0,
  "error": "arc5-compliance data unavailable"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `"ok"` if sent successfully; `"error"` if not sent |
| `sent` | boolean | Whether the Telegram message was delivered |
| `message_length` | integer | Length of the formatted message in characters |
| `error` | string \| null | Error description if not sent; `null` on success |

**Failure modes** (per BLG-GOV-86 §7)

| Condition | Behaviour |
|-----------|-----------|
| `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID` not set | Returns `sent: false`, `error: "Telegram credentials not configured"` |
| arc5-compliance DB query fails | Returns `sent: false`, `error: "arc5-compliance data unavailable"` |
| Message > 4,096 chars | Truncated to summary line only before send |
| Telegram API error | Returns `sent: false`, error logged |

**Data sources**

| SI-05 field | Source table | Logic |
|-------------|-------------|-------|
| `pass_rate` | `pre_entry_validation_log` | Overall pass/total ratio (7d) |
| `red_flag_count` | `red_flag_events` | COUNT(*) last 7 days |
| `override_rate` | `pre_entry_validation_log` + `red_flag_events` | Override events / total validations (7d) |
| `top_rule_breach` | `pre_entry_validation_log` | Most frequent failing rule_type (7d) |

**Authentication requirements**

⚠️ **Current status: UNAUTHENTICATED** — `POST /digest/si05/send` does not currently require authentication (`backend/routers/digest.py:227`). This is a known security gap documented in `docs/security/security_register.md` Review 003 (ST-11, v5.2). Fix tracked as **BLG-BE-35** (P2).

**Expected authentication (post BLG-BE-35):** API key authentication per the existing pattern (Depends injection, consistent with other protected endpoints). Unauthenticated requests should return `401 Unauthorized`.

This endpoint is intended for internal cron/scheduled invocation only. Until BLG-BE-35 ships, access should be restricted at the network layer (e.g., restrict to Render internal network) if feasible.

**Format spec:** `docs/product/decisions/si05-telegram-message-format-spec.md` (BLG-GOV-86)
**Backend:** `backend/services/si05_digest_service.py`

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.3 | 2026-06-08 | v5.2 ST-04 (BLG-SPEC-48): Authentication requirements section added — POST /digest/si05/send is currently unauthenticated (security gap per security_register.md Review 003); BLG-BE-35 filed for fix. Consistent with ST-11 security review findings. API Contracts & Documentation Owner and Head of Specs Team sign-off. |
| 0.2 | 2026-06-21 | Add POST /digest/si05/send endpoint: SI-05 Phase 1 weekly strategy integrity Telegram digest. Data from SI-01 (pre_entry_validation_log) + SI-03 (red_flag_events). Format per BLG-GOV-86. ST-01 (EPIC-01, v5.1). |
| 0.1 | 2026-04-01 | Initial version. ST-08 (BLG-FEAT-14 BE component, v2.4). GET /digest/weekly endpoint. Scope constraint: raw numeric/boolean fields only. |
