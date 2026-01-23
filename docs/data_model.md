# Data Model

This document describes the data structures used in the **Position Manager Web App**.

---

## 1. Portfolio

```json
{
  "cash": 10000.0,
  "positions": {
    "AAPL": {
      "entry_date": "2026-01-10",
      "entry_price": 150.0,
      "shares": 20,
      "initial_stop": 140.0,
      "current_stop": 145.0,
      "current_price": 155.0,
      "holding_days": 13,
      "pnl": 100.0,
      "pnl_pct": 3.33
    }
  },
  "trade_history": [
    {
      "ticker": "GOOG",
      "entry_date": "2026-01-01",
      "exit_date": "2026-01-15",
      "entry_price": 2500.0,
      "exit_price": 2600.0,
      "shares": 5,
      "pnl": 500.0,
      "pnl_pct": 4.0,
      "holding_days": 14,
      "exit_reason": "Stop Loss Hit"
    }
  ],
  "last_updated": "2026-01-23 12:00:00"
}
```
## 2. Position Object

| Field         | Type   | Description                               |
| ------------- | ------ | ----------------------------------------- |
| entry_date    | string | Date the position was opened (YYYY-MM-DD) |
| entry_price   | float  | Price at which the position was entered   |
| shares        | int    | Number of shares held                     |
| initial_stop  | float  | Initial stop-loss value                   |
| current_stop  | float  | Current trailing stop-loss value          |
| current_price | float  | Latest market price                       |
| holding_days  | int    | Days since entry                          |
| pnl           | float  | Current profit/loss in absolute terms     |
| pnl_pct       | float  | Current profit/loss in percentage         |

## 3. Trade History Object
