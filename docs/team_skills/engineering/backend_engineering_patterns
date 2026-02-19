# Backend Engineering Patterns

**Role:** Backend Engineering Patterns Owner
**Reports to:** Head of Engineering
**Governance alignment:** Head of Specs Team (documentation lifecycle, document classes, headers, naming conventions)
**Scope:** Backend implementation patterns, conventions, and engineering standards for the FastAPI / PostgreSQL codebase
**Status:** Canonical

---

## 1. Purpose

This document exists to ensure that backend engineering work is:

- **Consistent** — new endpoints, services, and models follow the same patterns as existing ones
- **Predictable** — engineers can read existing code and know how to add to it without reverse-engineering conventions
- **Aligned** — implementation always conforms to canonical specifications without interpreting or extending them
- **Safe** — changes to shared infrastructure (database layer, models, routers) do not introduce regressions

The backend engineering patterns document is the **implementation handbook** for this codebase. It encodes the conventions that have emerged across versions so they do not have to be rediscovered for each feature.

---

## 2. Core Responsibility

This document owns:

- The layered architecture pattern (router → service → database)
- Conventions for adding new endpoints, services, models, and database functions
- Error handling standards
- Pydantic model conventions
- How canonical specifications map to implementation artifacts

This document does **not** own:
- What the system does (that is `strategy_rules.md` and other canonical specs)
- API response shapes (that is `portfolio_endpoints.md` and other API contracts)
- Database schema (that is `data_model.md`)

---

## 3. Architecture Overview

The backend follows a strict three-layer architecture. Each layer has a single responsibility.

```
FastAPI Router  ←  HTTP in/out, request validation, error translation
      ↓
Service Layer   ←  Business logic, orchestration, all calculations
      ↓
Database Layer  ←  SQL queries only, no business logic
```

**Rules that are non-negotiable:**

- Routers must be thin. No business logic, no SQL, no calculations in a router.
- Services contain all business logic. Services are testable without FastAPI.
- `database.py` contains all SQL. No raw SQL anywhere else.
- Canonical spec rules are implemented in services, not inferred in routers or database functions.

---

## 4. Adding a New Endpoint

Follow this sequence for every new endpoint. Do not skip steps.

### Step 1 — Confirm the canonical spec is locked

Never implement an endpoint without a committed, locked API contract in `docs/specs/api_contracts/`. If the contract is in draft, stop and raise it with the API Contracts owner.

### Step 2 — Add the Pydantic request model

Add to `backend/models/requests.py`. Follow the existing pattern:

```python
class MyFeatureRequest(BaseModel):
    """Request model for [feature name]"""
    required_field: float
    optional_field: Optional[str] = None

    @validator('required_field')
    def validate_required_field(cls, v):
        if v <= 0:
            raise ValueError('required_field must be greater than 0')
        return v
```

Rules:
- All required fields have no default value
- All optional fields default to `None` (not a non-None default) unless the API contract specifies a default
- Validators raise `ValueError` — FastAPI translates these to HTTP 400 automatically
- Field names must exactly match the API contract request schema

Export the new model from `backend/models/__init__.py`.

### Step 3 — Add the service function

Create a new file `backend/services/{feature}_service.py` or add to an existing service if the domain is the same. Follow the existing pattern:

```python
"""
{Feature} Service

[One paragraph describing what this service does and which canonical spec
it implements. Reference the spec explicitly.]
"""

from typing import Dict, Optional
from database import get_portfolio  # import only what you need


def my_feature_function(param: float) -> Dict:
    """
    [Docstring: what it does, args, returns, raises]

    Implements [spec reference].
    """
    # Business logic here
    pass
```

Rules:
- Services never import from FastAPI
- Services never raise HTTPException — they raise ValueError or domain-specific exceptions
- Services are self-contained and can be unit-tested by calling them directly
- All calculations follow the canonical spec exactly — no interpretation

Export the new function from `backend/services/__init__.py`.

### Step 4 — Add the database function (if needed)

Add to `backend/database.py`. Follow the existing pattern:

```python
def get_my_data(portfolio_id: str) -> Optional[Dict]:
    """Get [description] for a portfolio"""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT ...
                FROM ...
                WHERE portfolio_id = %s
            """, (portfolio_id,))
            result = cur.fetchone()
            return dict(result) if result else None
```

Rules:
- Database functions contain SQL only — no business logic
- Always use parameterised queries (`%s`) — never string interpolation
- Always use `with get_db() as conn` context manager
- Return `None` (not an exception) when a record is not found, unless the absence is an error

### Step 5 — Create the router

Create `backend/routers/{feature}.py`. Follow the existing pattern:

```python
"""
{Feature} Router

[One line: what endpoint(s) this router provides]

Contract: [path to API contract spec]
"""

from fastapi import APIRouter, HTTPException
from models.requests import MyFeatureRequest
from services.my_feature_service import my_feature_function

router = APIRouter(prefix="/{prefix}", tags=["{Tag}"])


@router.post("/{path}")
def my_endpoint(request: MyFeatureRequest):
    """[One line description from the API contract]"""
    try:
        result = my_feature_function(
            param=request.param,
        )
        return {"status": "ok", "data": result}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
```

Rules:
- Routers translate HTTP to service calls and back — nothing else
- `ValueError` from services → HTTP 400
- Unexpected exceptions → HTTP 500 with traceback printed
- Business rule failures that return HTTP 200 with `valid: false` are handled in the service, not the router — the router just passes through the result

### Step 6 — Register the router in main.py

```python
from routers import my_feature

app.include_router(my_feature.router)
```

---

## 5. Settings Pattern

Settings are stored as a single row in the `settings` table. `GET /settings` returns the full row. `PATCH /settings/{id}` updates specific fields.

When adding a new settings field:

1. The database migration must already be applied (column exists)
2. Add the field to `SettingsRequest` in `models/requests.py` with `Optional[{type}] = None`
3. Add a Pydantic validator if the field has constraints (e.g. `> 0 AND <= 100`)
4. No changes required to `database.py` — `get_settings()` and `update_settings()` are dynamic and will include the new column automatically
5. No changes required to the settings endpoint handlers in `main.py` — they pass the full request dict through

---

## 6. Error Handling Standards

| Situation | What to do |
|-----------|-----------|
| Missing required field in request | Pydantic raises `ValueError` → HTTP 400 automatically |
| Invalid field value (bad enum, out of range) | Pydantic validator raises `ValueError` → HTTP 400 |
| Business rule failure (e.g. invalid stop distance) | Service returns a structured result with `valid: false` → HTTP 200 |
| Record not found | Service raises `ValueError` with descriptive message → router returns HTTP 404 or 400 depending on context |
| Unexpected server error | Router catches `Exception`, prints traceback, returns HTTP 500 |

Never swallow exceptions silently. Always print the traceback for unexpected errors so they are visible in logs.

---

## 7. Response Envelope

All endpoints return the standard success envelope:

```json
{
  "status": "ok",
  "data": { ... }
}
```

Error responses:

```json
{
  "status": "error",
  "message": "..."
}
```

Or via FastAPI's `HTTPException` (which produces `{"detail": "..."}` — this is consistent with existing endpoints).

Business rule failures that return HTTP 200 use the success envelope with a `valid: false` data payload. This is intentional — it distinguishes "the server handled the request correctly and the answer is invalid" from "the request was malformed".

---

## 8. Canonical Spec Alignment (Non-Negotiable)

### 8.1 The spec is authoritative

If the implementation would produce a different result from what the canonical spec defines, the implementation is wrong. Fix the implementation, not the spec.

If the spec is ambiguous or appears infeasible, surface it to the relevant spec owner and the Head of Engineering. Do not work around it silently.

### 8.2 Field names must match the contract exactly

Request field names, response field names, and reason codes must match the API contract verbatim. Do not rename fields for "clarity" — the frontend depends on exact names.

### 8.3 Calculations are authoritative on the backend

The frontend must not recalculate or derive any value returned by a backend endpoint. If a value is in the response, the frontend uses it. This applies especially to financial calculations (sizing, fees, P&L).

### 8.4 HTTP status semantics

Business rule failures return HTTP 200 with structured data, not HTTP 4xx. This is specified in `conventions.md` and applies to endpoints like `POST /portfolio/size`. Do not change this to return 4xx without a contract change approved by the API Contracts owner.

---

## 9. Lifecycle & Versioning Compliance

All documentation owned by this role must follow the lifecycle states, header block, and versioning rules defined in:

- `docs/governance/document_lifecycle_guide.md`

---

## 10. Definition of Success

This document is doing its job when:

- A new engineer can add a new endpoint by following the patterns here without asking how
- Code reviews focus on correctness and spec alignment, not style debates
- No two endpoints handle the same concern (errors, responses, validation) in different ways
- The spec is the source of truth — the code reflects it faithfully

The backend becomes **predictable and safe to change**, not a source of surprises.

---

## Guiding Principle

> The spec defines what the system does.
> This document defines how that is expressed in code.
>
> One without the other produces either undocumented behavior or unimplementable specs.
> Both together produce a system engineers can trust.
