# Stop Trail Endpoint Contract

**Version:** 1.0.0
**Last Updated:** 2026-05-12
**Spec Owner:** Engineering
**Governed by:** docs/specs/api_contracts/conventions.md

---

## GET /positions/{position_id}/stop-trail

Returns an ATR-based trailing stop recommendation for an open position. The recommendation is display-only (§13): the system surfaces the calculation; the human must confirm any stop change.

### Authentication

None required (single-user local application).

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `position_id` | string (UUID) | ID of the open position. |

### Response — 200 OK

```json
{
  "status": "ok",
  "data": {
    "position_id": "uuid",
    "ticker": "AAPL",
    "current_stop": 142.50,
    "atr_trail_stop": 147.80,
    "trail_difference": 5.30,
    "trail_r_terms": 0.75,
    "recommendation": "Raise stop to 147.80"
  }
}
```

**Response fields:**

| Field | Type | Notes |
|-------|------|-------|
| `position_id` | string (UUID) | Matches the request `position_id`. |
| `ticker` | string | Display ticker. |
| `current_stop` | number \| null | Current stop price from the position record; `null` if not set. |
| `atr_trail_stop` | number | `current_price − (ATR × 2.0)`, rounded to 4 decimal places. |
| `trail_difference` | number \| null | `atr_trail_stop − current_stop`; `null` if `current_stop` is null. |
| `trail_r_terms` | number \| null | `trail_difference` expressed as R-multiples; `null` if R is unavailable. |
| `recommendation` | string | Display string: `"Raise stop to {atr_trail_stop}"`. §13 display-only. |

### Errors

| HTTP Status | Condition |
|-------------|-----------|
| `404` | Position not found or not open |
| `422` | ATR not available for this position |
| `503` | Live price unavailable |
| `500` | Internal server error |
