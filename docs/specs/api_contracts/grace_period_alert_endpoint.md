# Grace Period Alert Endpoint Contract

**Version:** 1.0.0
**Last Updated:** 2026-05-12
**Spec Owner:** Engineering
**Governed by:** docs/specs/api_contracts/conventions.md

---

## GET /positions/grace-period-alerts

Returns positions in `GRACE` lifecycle state where `days_in_state >= 8` (nearing end of grace period). Includes linked trade plan summary if available.

§13 display-only: the system surfaces contextual information; the human decides next action.

### Authentication

None required (single-user local application).

### Query Parameters

None.

### Response — 200 OK

```json
{
  "status": "ok",
  "data": [
    {
      "position_id": "uuid",
      "ticker": "AAPL",
      "market": "US",
      "days_in_state": 9,
      "trade_plan_id": "uuid or null",
      "trade_plan_summary": {
        "setup_thesis": "string excerpt or null",
        "entry_rationale": "string or null",
        "stop_level": 142.50,
        "r_target": 2.0
      }
    }
  ]
}
```

**Per-alert fields:**

| Field | Type | Notes |
|-------|------|-------|
| `position_id` | string (UUID) | Matches `id` in `GET /positions`. |
| `ticker` | string | Display ticker (no `.L` suffix for UK stocks). |
| `market` | string | `"UK"` or `"US"`. |
| `days_in_state` | integer | Days since `state_entered_at` (or approximated from `entry_date` if unavailable). |
| `trade_plan_id` | string (UUID) \| null | Linked trade plan, `null` if none. |
| `trade_plan_summary` | object \| null | Excerpt of linked plan fields; `null` if no plan linked. |

**`trade_plan_summary` fields:**

| Field | Type | Notes |
|-------|------|-------|
| `setup_thesis` | string \| null | First 200 characters of setup thesis. |
| `entry_rationale` | string \| null | Entry rationale text. |
| `stop_level` | number \| null | Current stop price from trade plan. |
| `r_target` | number \| null | R-target from trade plan. |

### Errors

| HTTP Status | Condition |
|-------------|-----------|
| `404` | Portfolio not found |
| `500` | Internal server error |
