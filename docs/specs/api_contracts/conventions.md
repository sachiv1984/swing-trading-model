# conventions.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.3
**Last Updated:** 2026-08-06 (v1.3)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

## 1. Authentication & Authorization

All API endpoints **must** require a valid `X-API-Key` header, except those listed in §1.4 (Exempt Endpoints).

### 1.1 Scheme

| Property | Value |
|----------|-------|
| Header name | `X-API-Key` |
| Type | API key (static, per-environment) |
| Storage — server | Environment variable `API_KEY` |
| Storage — client | Environment variable `REACT_APP_API_KEY` |
| Scope | All non-exempt endpoints (see §1.4) |

### 1.2 Request Requirement

Every request to a protected endpoint **must** include:

```
X-API-Key: <value of API_KEY environment variable>
```

- The key is read server-side from the `API_KEY` environment variable.
- The frontend reads the key from `REACT_APP_API_KEY` and includes it on all API calls via a **shared API wrapper** — not duplicated per component.
- The key value must not be hard-coded in source files.

### 1.3 Failure Response

A missing or invalid `X-API-Key` must return:

```
HTTP 401 Unauthorized
```

```json
{
  "status": "error",
  "message": "Unauthorized"
}
```

This follows the standard error envelope defined in §13.

### 1.4 Exempt Endpoints

The following endpoints are exempt from the `X-API-Key` requirement:

| Endpoint | Reason |
|----------|--------|
| `GET /health` | Public health check for infrastructure monitoring |
| `OPTIONS *` | Browser CORS preflight — method-level exemption, not an endpoint. No data returned; actual request that follows is still authenticated. |

Any new exemption requires an explicit entry in this table and must be approved by the Head of Specs Team.

### 1.5 OpenAPI Security Reference

The `ApiKey` security scheme in `docs/reference/openapi.yaml` (`components/securitySchemes/ApiKey`) defines this scheme. The global `security:` block in `openapi.yaml` must apply this scheme to all paths. Exempt endpoints must declare `security: []` at the path level to override the global requirement.

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

## 13. Error Response Standard (Canonical)

This section defines the canonical error response standard for all API endpoints. It expands on the basic envelope in §2.2 to cover all required fields, HTTP status code mapping, and usage rules.

### 13.1 Standard Error Envelope

All non-health endpoint error responses **must** use the following shape:

```json
{
  "status": "error",
  "message": "Human-readable explanation of what went wrong"
}
```

**Field definitions:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | Yes | Always `"error"` for error responses |
| `message` | string | Yes | Human-readable explanation. Must not expose internal stack traces or system internals in production. |

### 13.2 HTTP Status Code Mapping (Canonical)

| HTTP Status | Use case | Example |
|-------------|----------|---------|
| `400 Bad Request` | Validation error (invalid/missing input fields) | Negative commission value, missing required field |
| `400 Bad Request` | Business rule violation (valid input, invalid system state) | Position already closed, stop would move downward |
| `404 Not Found` | Resource does not exist | Position ID not found, settings record not found |
| `500 Internal Server Error` | Backend failure | Database error, external API unavailable |

### 13.3 Usage Rules

- Error responses **must not** use HTTP 200 with an error body (except `POST /validate/calculations` which uses 200 with per-metric severity fields — this is a documented exception).
- Error responses **must** use the `{ "status": "error", "message": "..." }` envelope.
- Error `message` fields **must** be human-readable and actionable where possible.
- `message` must not expose internal stack traces, SQL errors, or file paths in production.
- Health endpoints (`/health`, `/health/detailed`, `/test/endpoints`) are exempt from this envelope per §11.

### 13.4 Relationship to `openapi.yaml`

`docs/reference/openapi.yaml` reusable components (`components/responses/BadRequest`, `components/responses/NotFound`, `components/responses/InternalError`) must align with this standard. If they diverge, this Markdown spec prevails.

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

---

## 14. API Endpoint Deprecation-Window Policy

No endpoint in this API has ever been formally deprecated (confirmed: no `deprecat*` occurrence in `api_changelog.md` or `docs/reference/openapi.yaml` as of this policy's authoring) — this section is a genuinely new policy, not a codification of existing practice, written ahead of the first real deprecation so that event doesn't have to invent the process under time pressure.

### 14.1 When to deprecate vs. remove directly

A canonical contract endpoint that is no longer wanted follows this policy only if it has, or may still have, an active consumer (the frontend, an external integration, or a documented third party). An endpoint added and removed within the same release cycle with no shipped consumer may be deleted directly — this policy governs the removal of *live, consumed* surface area.

### 14.2 Minimum notice window

- **30 days minimum** between an endpoint being marked deprecated and its removal, for any endpoint with a known internal (frontend) consumer.
- **90 days minimum** for any endpoint documented as consumed by an external/third-party integration (see `_external_api_template.md`-pattern contracts).
- The window starts from the date the deprecation is recorded in `api_changelog.md` (§14.4), not from when the replacement first became available.

### 14.3 Marking an endpoint deprecated

1. In the endpoint's `openapi.yaml` operation object, set `deprecated: true`.
2. In the endpoint's canonical markdown contract, add a `**Deprecated:** <date> — removal no earlier than <date + notice window>. Replacement: <new endpoint, or "none — feature removed">.` line directly under the `## METHOD /path` heading.
3. If a replacement endpoint exists, its own contract entry should cross-reference the deprecated one (`**Replaces:** METHOD /old-path`) so a reader arriving at either finds the other.

### 14.4 Recording in `api_changelog.md`

Every deprecation and every completed removal gets its own `api_changelog.md` entry (per `BLG-GOV-205`'s canonical entry template, once that item lands — until then, follow the file's existing entry format), so the deprecation timeline is visible in one place rather than only inside individual contract files.

### 14.5 Removal

- The endpoint may be removed from `backend/routers/`/`backend/main.py`, its contract file, and `openapi.yaml` only after the notice window (§14.2) has elapsed.
- Removal is a normal contract change: same-commit `openapi.yaml` update, same-sprint contract removal, per `CLAUDE.md`'s standing API-contract rules.
- If usage telemetry shows the endpoint is still receiving live traffic when the window elapses, extend the window and re-notify rather than removing on schedule — do not remove a still-used endpoint solely because the calendar window has passed.

### 14.6 Sign-off

A deprecation-window policy exception (shorter notice, or removal without a deprecation period) requires Head of Specs Team sign-off, recorded in the removing story's QA evidence log.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-08-06 | 1.3 | Added §14 API Endpoint Deprecation-Window Policy — genuinely new policy, no endpoint has ever been formally deprecated (ST-20, EPIC-04, v8.3, BLG-SPEC-96) |
