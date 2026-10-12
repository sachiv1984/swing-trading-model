# Grace Period Alert Endpoint Contract

**Version:** 1.2.0
**Last Updated:** 2026-10-08 (ST-14, EPIC-02, v9.11, BLG-BE-147 — selects on grace_days_remaining <= 2, calendar days since entry, not days_in_state); prior — 2026-10-06 (ST-12, EPIC-03, v9.10, BLG-FE-196 — adds grace_days_remaining; days_in_state fallback counts calendar days); prior — 2026-05-12; prior history retained — see prior entries in version control
**Spec Owner:** Engineering
**Governed by:** docs/specs/api_contracts/conventions.md

---

## GET /positions/grace-period-alerts

Returns positions in `GRACE` lifecycle state with `grace_days_remaining <= 2`, that is, at least 8 calendar days since `entry_date` (nearing the end of the grace period). Includes linked trade plan summary if available.

**Selection rule (v1.2.0 — ST-14, BLG-BE-147, v9.11):** the alert list selects on calendar days since entry, not on `days_in_state`. `days_in_state` restarts whenever `state_entered_at` is rewritten, so a day-8 position whose `state_entered_at` is today was previously dropped. Only when `entry_date` cannot be parsed (so `grace_days_remaining` is `null`) does the endpoint fall back to `days_in_state >= 8`. Design source: `docs/design/2026-10-08__release-v9.11/grace-alert-calendar-days/decision_record.md`.

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
      "grace_days_remaining": 1,
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
| `days_in_state` | integer | Days since `state_entered_at`. If that is unavailable, calendar days since `entry_date` (weekdays before v9.10). Informational only from v9.11: the Positions page reads no grace value from it (`positions.md` §Grace Period Alert Zone). |
| `grace_days_remaining` | integer \| null | Calendar days of grace left: `max(0, 10 − calendar days since entry_date)`, the same rule as `GET /positions`' `grace_days_remaining` (`strategy_rules.md` §6.2). `null` if `entry_date` is unreadable. The Positions page alert text uses this, not `10 − days_in_state`. (v9.10 ST-12 BLG-FE-196) |
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
