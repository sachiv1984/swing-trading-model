# conventions.md

## 1. Authentication & Authorization

Authentication and authorization mechanisms are **not defined** in the current API contract.

- No OAuth, JWT, API key, or session-based scheme is specified.
- Authentication is assumed to be handled by environment or infrastructure controls.
- All endpoints described in this contract assume an already-authenticated context.

Until explicitly defined, authentication behavior is considered **out of scope** for these contracts.

---

## 2. Standard Request & Response Formats

### 2.1 Success Response Envelope

All successful responses **must** use the following wrapper:

```json
{
  "status": "ok",
  "data": {}
}
```

**Rules**
- `data` must always be present.
- `data` may be an object or an array.
- No endpoint may return a raw object or array at the top level.
- Successful responses use HTTP `200 OK`.

---

### 2.2 Error Response Envelope

All error responses **must** use the following wrapper:

```json
{
  "status": "error",
  "message": "Human-readable explanation"
}
```

---

## 3. Error Handling Conventions

| Category | HTTP Status | Description |
|--------|-------------|-------------|
| Validation error | 400 | Invalid or missing input |
| Business rule violation | 400 | Valid input but invalid system state |
| Resource not found | 404 | Requested entity does not exist |
| System error | 500 | Internal failure |

---

## 4. Defaults & Optional Field Behavior

Unless explicitly overridden by an endpoint, the following defaults apply **server-side**.

| Field | Default |
|-----|---------|
| `exit_reason` | "Manual Exit" |
| `exit_date` | Current date (UTC) |
| `shares` (exit) | All remaining shares |
| `fx_rate` (UK stocks) | `1.0` |
| `stop_price` (entry) | `entry_price - (5 × ATR)` |
| `atr_value` | Auto-fetched by server |
| `entry_note` | `null` |
| `tags` | `[]` |

---

## 5. Multi-Currency & Pricing Conventions

- All prices and stops include GBP and native currency values.
- Stops are stored and enforced in native currency only.

---

## 6. Idempotency

- GET endpoints are idempotent and safe to refresh.
- POST/PATCH/DELETE endpoints mutate state unless explicitly stated otherwise.

---

## 7. Exit & FX Rules

- Exit prices are always user-provided.
- US exits require `exit_fx_rate`.
- UK exits default to `fx_rate = 1.0`.

---

## 8. Validation Rules

- UUIDs for identifiers
- Dates: `YYYY-MM-DD`
- Timestamps: ISO 8601
- Tags: lowercase, numbers, hyphens only

---

## 9. Pagination & Filtering

- No generic pagination is defined.
- Endpoint-specific filtering may apply.

---

## 10. Versioning

- Contract version is tracked in **README.md**.

---

## 11. Health Endpoint Exception

Health endpoints do not use the standard `{ status, data }` response envelope.

---

## 12. DELETE Response Convention

Successful `DELETE` operations return HTTP 200 with the standard success envelope. The `data` object confirms the deletion:

```json
{
  "status": "ok",
  "data": {
    "deleted": true,
    "id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

- `deleted: true` confirms the record was removed.
- `id` echoes the identifier of the deleted record.
- DELETE endpoints are **non-idempotent**: a second call to the same resource returns `404 Not Found`.
