# digest_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 0.7
**Last Updated:** 2026-11-27 (ST-16, EPIC-03, v9.18, BLG-UX-12 — `GET /digest/weekly` gains `red_flags_7d`); prior — 2026-11-27 (ST-14, EPIC-03, v9.18, BLG-SPEC-204 — `GET /digest/weekly` gains `journal_completion_rate_*`, `closed_trades_total`, `closed_trades_total_7d_ago`; `compliance_score_*` deprecated); prior — 2026-09-29 (ST-20, EPIC-05, v9.8, BLG-API-04 — added an Idempotency subsection to POST /digest/si05/send); prior history retained — see prior entries in version control
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
  "journal_completion_rate_current": 72.5,
  "journal_completion_rate_7d_ago": 70.3,
  "closed_trades_total": 40,
  "closed_trades_total_7d_ago": 37,
  "compliance_score_current": 72.5,
  "compliance_score_7d_ago": 70.3,
  "red_flags_7d": 2,
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
| `journal_completion_rate_current` | float \| null | Journal completion rate across all closed trades: `(trades_with_notes / total_trades) × 100`, 1 dp, range 0–100. Same formula and predicate as `GET /analytics/compliance-metrics` `journal_completion_rate` (`metrics_definitions.md` §Journal Completion Rate), so both surfaces show the same figure. `0.0` when there are no closed trades; read `closed_trades_total`. `null` when its query fails. (v0.6, ST-14) |
| `journal_completion_rate_7d_ago` | float \| null | The same rate over trades with `exit_date` before the 7-day cutoff (baseline for trend), using today's notes. `0.0` when no trade closed before the cutoff; read `closed_trades_total_7d_ago`. `null` when its query fails. (v0.6, ST-14) |
| `closed_trades_total` | integer \| null | Count of all `trade_history` rows: the denominator of `journal_completion_rate_current`. `0` means "no closed trades", not "no notes"; `null` (query failed) means unknown, never "none". (v0.6, ST-14) |
| `closed_trades_total_7d_ago` | integer \| null | Count of `trade_history` rows with `exit_date` before the cutoff: the denominator of `journal_completion_rate_7d_ago`; `null` when its query fails. (v0.6, ST-14; Metrics Definitions & Analytics Owner / Product Owner ruling 2026-11-27) |
| `compliance_score_current` | float | **Deprecated (v0.6)** alias of `journal_completion_rate_current`, same value, except `0.0` (never null) when the query fails, as before v0.6. It is a journal completion rate, not a compliance score; kept for existing callers. |
| `compliance_score_7d_ago` | float | **Deprecated (v0.6)** alias of `journal_completion_rate_7d_ago`, same value, except `0.0` (never null) when the query fails. |
| `red_flags_7d` | integer \| null | Count of `red_flag_events` rows with `created_at` in the last 7 × 24h (the same rolling window as `alerts_fired_7d`). The Weekly Digest links it to Journal → Red flags. `null` when its query fails. (v0.7, ST-16; Product Owner decision 2026-11-18) |
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
| `journal_completion_rate_*`, `closed_trades_total*` (and the deprecated `compliance_score_*`) | `trade_history` | `entry_note`, `exit_note`, `exit_date` |
| `red_flags_7d` | `red_flag_events` | `created_at` |
| `staleness_hours` | `portfolio_history` | `snapshot_date` |

---

---

## POST /digest/si05/send

**Purpose**

Trigger the SI-05 Phase 1 weekly strategy integrity digest via Telegram. Fetches arc5-compliance metrics from SI-01 (pre-entry validation) and SI-03 (red flag journal) and sends a formatted MarkdownV2 message per the SI-05 Telegram message format specification (BLG-GOV-86).

Intended for weekly cron/scheduled invocation. Safe to retry — message content reflects current DB state at call time.

**Method & Path**

- `POST /digest/si05/send`

**Idempotency**

- Not idempotent — sends a fresh Telegram message on every successful call (no send-once-per-window dedup). A double-submit sends two messages; this is an accepted trade-off for a manually/cron-triggered digest, not a defect — no state is written or corrupted either way ("safe to retry" per Purpose above refers to retry-safety of the read side, not message-count suppression).

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

✅ **Authenticated** — `POST /digest/si05/send` requires `X-API-Key` header matching the `API_KEY` environment variable. Unauthenticated requests return `401 Unauthorized`. Implemented via `_verify_api_key` dependency in `backend/routers/digest.py` (ST-08, BLG-BE-35, v5.3).

**Response (401 — unauthenticated)**
```json
{"status": "error", "message": "Unauthorized"}
```

This endpoint is intended for internal cron/scheduled invocation only. The scheduler must supply `X-API-Key: <API_KEY>` in its request headers.

**Format spec:** `docs/product/decisions/si05-telegram-message-format-spec.md` (BLG-GOV-86)
**Backend:** `backend/services/si05_digest_service.py`

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.7 | 2026-11-27 | v9.18 ST-16 (EPIC-03, BLG-UX-12): `GET /digest/weekly` adds `red_flags_7d` (`red_flag_events` created in the last 7 × 24h; null on a failed query), per the Product Owner decision of 2026-11-18. |
| 0.6 | 2026-11-27 | v9.18 ST-14 (EPIC-03, BLG-SPEC-204): `GET /digest/weekly` adds `journal_completion_rate_current`, `journal_completion_rate_7d_ago`, `closed_trades_total` and `closed_trades_total_7d_ago`; `compliance_score_current`/`_7d_ago` kept as deprecated aliases with the same values. Each new field is `null` when its query fails (no longer read as 0), and a failed optional query is rolled back so later fields still compute. Predicate confirmed the same as `GET /analytics/compliance-metrics` (real-Postgres test). `closed_trades_total_7d_ago` per Metrics Definitions & Analytics Owner / Product Owner ruling 2026-11-27. |
| 0.5 | 2026-09-29 | v9.8 ST-20 (EPIC-05, BLG-API-04): Idempotency subsection added to POST /digest/si05/send. (Row restored at v0.6; it was missing from this table.) |
| 0.4 | 2026-06-09 | v5.3 ST-08 (BLG-BE-35): API key authentication implemented on POST /digest/si05/send via _verify_api_key Depends injection; unauthenticated requests now return 401. Authentication requirements section updated to reflect shipped state. Cybersecurity & Trust Lead and Head of Engineering sign-off. |
| 0.3 | 2026-06-08 | v5.2 ST-04 (BLG-SPEC-48): Authentication requirements section added — POST /digest/si05/send is currently unauthenticated (security gap per security_register.md Review 003); BLG-BE-35 filed for fix. Consistent with ST-11 security review findings. API Contracts & Documentation Owner and Head of Specs Team sign-off. |
| 0.2 | 2026-06-21 | Add POST /digest/si05/send endpoint: SI-05 Phase 1 weekly strategy integrity Telegram digest. Data from SI-01 (pre_entry_validation_log) + SI-03 (red_flag_events). Format per BLG-GOV-86. ST-01 (EPIC-01, v5.1). |
| 0.1 | 2026-04-01 | Initial version. ST-08 (BLG-FEAT-14 BE component, v2.4). GET /digest/weekly endpoint. Scope constraint: raw numeric/boolean fields only. |
