# trade_endpoints.md

## Overview

This document defines **Trade** domain endpoints.

- Retrieve immutable, closed trade history
- Includes trade-level statistics and a list of closed trades

Global response envelopes, error shape, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [GET /trades](#get-trades)

---

## GET /trades

**Purpose**

Retrieve all **closed trades** along with summary statistics.

- Records are immutable (closed positions only).
- Results are sorted by `exit_date` descending (newest first).

**Method & Path**

- `GET /trades`

**Idempotency**

- Safe to refresh (read-only).

### Request

No parameters.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "total_trades": 42,
  "win_rate": 58.5,
  "total_pnl": 5200.00,
  "trades": [
    {
      "id": "750e8400-e29b-41d4-a716-446655440000",
      "ticker": "NVDA",
      "market": "US",
      "entry_date": "2026-01-15",
      "exit_date": "2026-02-15",
      "shares": 10.5,
      "entry_price": 622.00,
      "exit_price": 920.00,
      "pnl": 3200.00,
      "pnl_pct": 35.8,
      "pnl_percent": 35.8,
      "exit_reason": "Target Reached",
      "holding_days": 31,
      "entry_note": "Breakout above $800",
      "exit_note": "Hit target",
      "tags": ["momentum", "winner"]
    }
  ]
}
```

#### Field notes

- `trades` contains **closed** trades only.
- `pnl_pct` and `pnl_percent` are both returned for compatibility.
- Notes (`entry_note`, `exit_note`) may be `string` or `null`.

### Validation rules & constraints

- The endpoint returns an empty `trades` array when there are no closed trades.
- Trade records are read-only via this endpoint.

### Errors

Errors use the standard error envelope from **conventions.md**.
