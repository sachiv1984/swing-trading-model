# Stop Trail Endpoint Contract

**Version:** 1.2.0
**Last Updated:** 2026-11-23 (ST-27, EPIC-05, v9.18, BLG-BE-223/BLG-BE-229 — 409 while a split is pending; the trail uses the native entry); prior — 2026-11-04 (ST-06, EPIC-01, v9.15, BLG-BE-173 — `atr_trail_stop` is the §7.2 stop from `calculate_trailing_stop` with the §11 multipliers and the breakeven floor, not `current_price − ATR × 2.0`; response shape unchanged); prior history retained — see prior entries in version control
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
| `atr_trail_stop` | number | The `strategy_rules.md` §7.2 stop for the live price and stored ATR, as `calculate_trailing_stop` (`backend/utils/calculations.py`) computes it with the §11 multipliers from `backend/strategy_parameters.py` (v1.1.0, ST-06, BLG-BE-173): when `current_price > entry_price`, `max(current_price − PROFIT_ATR_MULTIPLIER × ATR, entry_price)`, where `entry_price` is the native entry (`native_entry_price()`: `fill_price` for US, else `entry_price` × `fx_rate`, else × the live rate; v1.2.0, BLG-BE-229 — before, a US position's GBP `entry_price` was compared with its USD price, which also skewed `trail_r_terms`); confirmed splits are applied (DS-42) (the breakeven floor); otherwise `current_price − INITIAL_ATR_MULTIPLIER × ATR`. Not ratcheted against `current_stop`, so `trail_difference` can be negative. Rounded to 4 decimal places. Before v1.1.0 it was `current_price − (ATR × 2.0)` with no floor. |
| `trail_difference` | number \| null | `atr_trail_stop − current_stop`; `null` if `current_stop` is null. |
| `trail_r_terms` | number \| null | `trail_difference` expressed as R-multiples; `null` if R is unavailable. |
| `recommendation` | string | Display string: `"Raise stop to {atr_trail_stop}"`. §13 display-only. |

### Errors

| HTTP Status | Condition |
|-------------|-----------|
| `404` | Position not found or not open |
| `409` | *(v1.2.0, ST-27, BLG-BE-223)* A stock split on the position is waiting for confirmation (`strategy_rules.md` §9.1): the stored entry, stop and ATR are pre-split and the live price post-split, so no trail is computed or logged |
| `422` | ATR not available for this position |
| `503` | Live price unavailable |
| `500` | Internal server error |
