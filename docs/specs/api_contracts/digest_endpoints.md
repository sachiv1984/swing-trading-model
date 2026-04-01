# digest_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 0.1
**Last Updated:** 2026-04-01
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

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-04-01 | Initial version. ST-08 (BLG-FEAT-14 BE component, v2.4). GET /digest/weekly endpoint. Scope constraint: raw numeric/boolean fields only. |
