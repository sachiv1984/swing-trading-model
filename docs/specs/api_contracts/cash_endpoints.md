# cash_endpoints.md

## Overview

This document defines **Cash Management** domain endpoints:

- Record deposits/withdrawals
- List cash transactions
- Retrieve cash summary totals

Global response envelopes, error shape, defaults, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [POST /cash/transaction](#post-cashtransaction)
- [GET /cash/transactions](#get-cashtransactions)
- [GET /cash/summary](#get-cashsummary)

---

## POST /cash/transaction

**Purpose**

Record a cash **deposit** or **withdrawal**.

- Deposits increase available cash.
- Withdrawals decrease available cash.

**Method & Path**

- `POST /cash/transaction`

**Idempotency**

- Mutating (non-idempotent). Repeating the request records additional transactions.

### Request

#### Body

```json
{
  "type": "deposit",
  "amount": 5000.00,
  "date": "2026-02-15",
  "note": "Initial funding"
}
```

#### Required fields

- `type` (string): `"deposit"` or `"withdrawal"`
- `amount` (number, min `0.01`)

#### Optional fields

- `date` (string, `YYYY-MM-DD`): defaults to today (UTC) if omitted
- `note` (string, max 200)

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "transaction": {
    "id": "850e8400-e29b-41d4-a716-446655440000",
    "type": "deposit",
    "amount": 5000.00,
    "date": "2026-02-15",
    "note": "Initial funding",
    "created_at": "2026-02-15T10:30:00Z"
  },
  "new_balance": 10000.00
}
```

### Validation rules & constraints

- `type` must be exactly `deposit` or `withdrawal`.
- `amount` must be greater than 0.
- For withdrawals, the amount must not exceed available cash.
- `note` must not exceed 200 characters.

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` Withdrawal exceeds available cash
- `400` Invalid transaction type

---

## GET /cash/transactions

**Purpose**

List all recorded cash transactions.

**Method & Path**

- `GET /cash/transactions`

**Idempotency**

- Safe to refresh (read-only).

### Request

#### Query parameters

- `order` (string, optional): `"ASC"` or `"DESC"` (default: `"DESC"`)

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema (array)

```json
[
  {
    "id": "850e8400-e29b-41d4-a716-446655440000",
    "type": "deposit",
    "amount": 5000.00,
    "date": "2026-02-15",
    "note": "Initial funding",
    "created_at": "2026-02-15T10:30:00Z"
  }
]
```

### Notes

- `order=DESC` returns newest first.
- Returns an empty array `[]` if there are no transactions.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## GET /cash/summary

**Purpose**

Return a summary of cash flows and current cash.

**Method & Path**

- `GET /cash/summary`

**Idempotency**

- Safe to refresh (read-only).

### Request

No parameters.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "total_deposits": 15000.00,
  "total_withdrawals": 1000.00,
  "net_cash_flow": 14000.00,
  "current_cash": 5000.00
}
```

### Validation rules & constraints

- Values are calculated server-side from recorded transactions.

### Errors

Errors use the standard error envelope from **conventions.md**.
