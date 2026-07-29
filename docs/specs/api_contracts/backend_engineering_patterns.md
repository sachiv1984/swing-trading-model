**Owner:** Backend Engineering Patterns Owner
**Class:** Canonical Specification (Class 1)
**Status:** Active
**Version:** 1.4
**Last Updated:** 2026-07-29
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Backend Engineering Patterns

This document records canonical backend engineering decisions and patterns for the Momentum Trading Assistant. It is the authoritative cross-reference for architecture decisions that affect multiple features or the overall system design. Individual ADRs are the detailed records; this document provides the indexed summary and implementation contract.

---

## Architectural Decision Index

| ADR | Title | Decision | Status | Date |
|-----|-------|----------|--------|------|
| ADR-002 | Frontend-Only R-Multiple Calculation | R-Multiple computed client-side in `RMultipleAnalysis.js` — backend data (stop_price) not reliably available for historical trades | Accepted | 2026-02-16 |
| ADR-003 | Notification Delivery Architecture | FastAPI `BackgroundTasks` for email delivery — no external worker infrastructure; tasks enqueued after API response returns | Accepted | 2026-03-18 |

---

## ADR-003 — Notification Delivery Pattern Summary

**Full record:** `docs/adr/ADR-003-notification-delivery-architecture.md`

**Decision:** Use FastAPI `BackgroundTasks` for notification delivery.

**Pattern:** Alert evaluation triggers delivery as a background task (non-blocking). Email fires after the API response is returned to the client. No Redis, Celery, or external worker process required.

**Key constraints for implementers:**
- `deliver_notification(alert)` must never raise — catch all exceptions, log via structured logger, record on alert row
- Alert table must carry: `delivered: bool`, `delivery_attempted_at: timestamptz`, `delivery_attempts: int`, `delivery_error: text | null`
- Retry policy: re-enqueue on next evaluation cycle if `delivered = false` and `delivery_attempts < 3`; abandon after 3 failures
- Email provider selection deferred to ST-04 — recommend SendGrid or Mailgun API (not SMTP)

**Migration path:** If Celery is ever needed, abstract delivery behind `NotificationDeliveryService` protocol; swap implementation without changing callers.

---

## General Patterns

### Background work

Use FastAPI `BackgroundTasks` for non-critical post-response work (notifications, audit log writes, cache invalidation) that must not block the user. Do not use background tasks for critical-path writes that must complete atomically with the request.

### Structured logging

All backend events must use the structured logging standard defined in `docs/specs/structured_logging_standards.md`. Notification delivery events must log: `alert_id`, `alert_type`, `delivery_attempt`, `outcome`, and `error` (if failed).

### Database migrations

All schema changes must follow the migration governance standard defined in `docs/governance/database_migration_governance.md`. Alert table additions (ADR-003 delivery tracking columns) require a migration authored per that standard.

### API endpoint authoring

All new endpoints must be added to `docs/reference/openapi.yaml` in the same commit as the contract spec. See `CLAUDE.md §2`.

---

### Lazy imports for cross-router hooks

When one router needs to call a function from another router, use a **lazy import inside the calling function** rather than a module-level import. Module-level cross-router imports cause `ImportError` or silent shadowing depending on the registration order in `main.py`.

**When to use:** Any time router A needs to invoke a function defined in router B (e.g., `screener.py` triggering cache invalidation in `research.py`).

**Why module-level imports fail:** FastAPI routers are registered sequentially in `main.py`. If router A is registered before router B, a module-level `from backend.routers.b import fn` in router A will fail at import time because `b` has not yet been fully initialised. This also applies to shared utility functions that themselves import from routers.

**Pattern:**

```python
# ✗ DO NOT — module-level cross-router import
from backend.routers.research import invalidate_research_cache

@router.post("/screener/run")
async def run_screener(background_tasks: BackgroundTasks):
    background_tasks.add_task(_invalidate_after_run)

# ✓ DO — lazy import inside the function body
@router.post("/screener/run")
async def run_screener(background_tasks: BackgroundTasks):
    background_tasks.add_task(_invalidate_after_run)

def _invalidate_after_run():
    from backend.routers.research import invalidate_research_cache  # lazy
    invalidate_research_cache()
```

**Real-world example (v5.6, ST-07):** `screener.py` triggers `invalidate_research_cache()` from `research.py` via a background task. Because `screener` is registered before `research` in `main.py`, a module-level import raises `ImportError`. The lazy import inside `_invalidate_after_run` resolves correctly at call time.

**AC-03 findability:** Cross-router hooks using lazy imports should include an inline comment such as:
```python
    from backend.routers.research import invalidate_research_cache  # lazy import — avoids circular dep; see backend_engineering_patterns.md
```

---

### CSV/export response-body pattern

**Added:** v1.2 — ST-07 (EPIC-03, v7.1, BLG-SPEC-84)

Canonical pattern for any endpoint that returns a downloadable file (CSV, and by extension the sibling PDF pattern) instead of a JSON envelope. Extracted from `GET /reports/tax-year?format=csv` (`backend/main.py`, `backend/services/reports_service.py`), the first and — as of this writing — only export endpoint in the codebase; use this as the template for future export endpoints rather than inventing a new shape.

**Pattern:**

```python
# 1. Build the file content as a pure, independently-testable function —
#    no request/response objects, no I/O. Takes the already-fetched data
#    dict, returns a string (CSV) or bytes (PDF).
def build_x_csv(data: dict) -> str:
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow([...])   # metadata / header rows
    for row in data["items"]:
        writer.writerow([...])
    return output.getvalue()

# 2. In the route handler, branch on a `format` query param (not a
#    separate endpoint/path) — the JSON, CSV, and PDF forms of the same
#    resource share one URL and one `format` parameter with a validated,
#    small enum ("pdf", "csv"); an unrecognised value returns 400, not a
#    fallback to JSON.
@app.get("/resource")
def get_resource_endpoint(format: Optional[str] = None):
    if format is not None and format not in ("pdf", "csv"):
        return JSONResponse(status_code=400, content={"status": "error", "message": "format must be one of: pdf, csv"})
    data = get_resource_data()
    if format == "csv":
        csv_text = build_x_csv(data)
        return Response(
            content=csv_text.encode("utf-8"),
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{resource}-{id}.csv"'},
        )
    return {"status": "ok", "data": data}
```

**Key constraints for implementers:**
- **Auth is automatic, do not special-case it.** `api_key_middleware` (`backend/main.py`) validates `X-API-Key` globally, before any route handler runs — export formats need no additional auth code and must not add a bypass.
- **Charset:** encode the body explicitly as UTF-8 (`.encode("utf-8")`). The response header ends up as `text/csv; charset=utf-8` even though the handler only sets `media_type="text/csv"` — Starlette's `Response` class auto-appends `charset=utf-8` for any `text/*` media type. Don't assume the header matches exactly what you pass to `media_type`; verify with a direct `TestClient` assertion (see `docs/specs/api_contracts/reports_endpoints.md` §Charset note, corrected after an initial source-only-inference documentation error).
- **Filename convention:** `Content-Disposition: attachment; filename="{resource}-{identifying-params}.{ext}"` — human-readable, includes the disambiguating query param(s) (e.g. the tax year) so a user downloading multiple exports doesn't get silently-overwritten same-named files.
- **Classification:** a CSV/PDF export is an analytics/convenience *view*, not the system of record — the database table it reads from remains authoritative. Do not persist the generated file server-side; generate on every request.
- **Testing:** the builder function (`build_x_csv`) must have a dedicated content-asserting test (parses/greps the actual returned string for expected rows/values), not only an integration test that checks the response fired — a download that fires with wrong/truncated content is a silent data-integrity bug a "did it download" test cannot catch. See `tests/test_reports_integration.py::TestTaxYearCsvExport` for the reference pattern.

---

### Error-response envelope conformance

**Added:** v1.3 — ST-04 (EPIC-04, v7.6, BLG-BE-65)

**Canonical envelope:** The single canonical error-response shape for this codebase is defined in `docs/specs/api_contracts/conventions.md` §13 (Error Response Standard): `{"status": "error", "message": "<human-readable>"}`, returned with the correct non-200 HTTP status code per §13.2 (400/404/500). This document does not redefine that shape — it records this sprint's audit of conformance against it, and the resulting follow-up scope.

**Audit method:** Every file in `backend/routers/` (23 files, 79 `@router.` endpoints) was scanned for `HTTPException`, `JSONResponse`, and bare-dict error-path returns. `backend/main.py` was checked only to confirm no global `@app.exception_handler` exists that would translate `HTTPException`'s default body — none does.

**Findings — three non-conformance patterns identified:**

1. **Default FastAPI envelope (`{"detail": "..."}`) instead of canonical (`{"status": "error", "message": "..."}`).** The dominant pattern: `raise HTTPException(status_code=X, detail=...)` with no global handler to translate it. Affects the large majority of error paths across: `alerts.py`, `analytics.py`, `digest.py` (401 case), `ai.py` (422 case), `paper_trading.py`, `plan_vs_reality.py`, `portfolio_size.py`, `red_flag_journal.py`, `saved_filters.py`, `screener.py` (400/404/409 cases), `strategy_benchmark.py`, `ticker_universe.py`, `trade_plans.py` (404 case), `trades_export.py`, `validation.py` (500 case), `watchlist.py`. `earnings.py` and `news.py` have no explicit error handling at all and fall through to this same default shape on any uncaught exception.
2. **Errors masked as HTTP 200 success — most severe finding.** `portfolio_risk.py`'s four endpoints (`/drawdown-status`, `/concentration-status`, `/sector-weights`, `/gate-metrics`) catch all exceptions and return `{"status": "ok", "data": {..., "error": str(e)}}` (first three) or `{"status": "error", "error": str(e)}` (last one) as a bare dict — implicit HTTP 200 in all four cases. This directly violates conventions.md §13.3 ("error responses must not use HTTP 200 with an error body"): a frontend caller checking only `response.status === "ok"` would treat a backend failure as success for the first three endpoints.
3. **Correct shape, wrong status code.** `digest.py`'s `GET /weekly` catch-all returns the canonical `{"status": "error", "message": ...}` body but as a bare dict (implicit HTTP 200), not via `JSONResponse(status_code=500, ...)`.

**Conforming reference implementations:** `research.py` (`get_research`, 503/404/500 cases) and most of `trade_plans.py`'s catch-all blocks correctly use `JSONResponse(status_code=..., content={"status": "error", "message": ...})` — use these as the template for remediation rather than inventing a new shape.

**Exempt endpoints:** `/health`, `/health/detailed`, `/test/endpoints` (conventions.md §13.3) — `test.py` was audited and confirmed exempt, not flagged.

**Observation (not in this item's scope):** `news.py` and part of `screener.py` also diverge on the *success* envelope (`{"ok": true, "data": ...}` instead of `{"status": "ok", "data": ...}`). Noted for awareness; BLG-BE-65's acceptance criteria scope this audit to error-response shapes only, so no follow-up item is filed for it here.

**Out of audit scope:** `backend/main.py` exhibits the same default-envelope pattern (44 `HTTPException(detail=str(e))` call sites) but is not a file under `backend/routers/`; already tracked separately as an internal-detail-leakage concern (distinct from envelope shape).

**Disposition:** Per BLG-BE-65's acceptance criteria, non-conforming endpoints are not fixed in this item. Follow-up backlog items: `BLG-BE-67` (fix HTTP-200-masked errors in `portfolio_risk.py`, P2) and `BLG-BE-68` (conform remaining routers to the canonical `{status, message}` envelope + correct status codes, P3).

---

### Idempotency-key pattern for state-mutating POST endpoints

**Added:** v1.4 — ST-03 (EPIC-01, v7.10, BLG-BE-76)

**Purpose:** Let a client safely retry a state-mutating POST (e.g. after a timeout or dropped connection) without risking a duplicate resource, without changing any existing behaviour for callers that don't opt in.

**Additive, opt-in only (RISK-02 — non-negotiable):** The pattern activates only when the caller supplies a non-empty `idempotency_key` field in the request body. When it is absent, the endpoint's behaviour is byte-for-byte identical to before this pattern existed — zero extra database access, zero change to the response. Do not make `idempotency_key` required, and do not add any always-on check (e.g. a lookup keyed by request-body hash) — the dedup mechanism must be invisible unless explicitly requested.

**Implementation:**
1. Add `idempotency_key: Optional[str] = None` to the endpoint's Pydantic request model.
2. Wrap the existing create logic in a closure with no signature change: `def _create(): ...` (unchanged body).
3. At the top of the route handler, branch: if `idempotency_key` is falsy, call `_create()` directly (existing code path, unchanged). If present, call `utils/idempotency.py::replay_or_create(portfolio_id, "<METHOD> <path>", idempotency_key, _create)`.
4. `replay_or_create` is generic and reusable — it does not know or care what `_create()` builds. It checks the `idempotency_keys` table (`portfolio_id`, `endpoint`, `idempotency_key`) for a prior response; if found, returns it verbatim instead of re-running `_create()`; otherwise runs `_create()` once and stores the result.

**Current scope (v7.10):** Applied to `POST /portfolio/position` (trade entry, `backend/main.py`) and `POST /trade-plans` (trade-plan creation, `backend/routers/trade_plans.py`). Extending to additional state-mutating POST endpoints is a mechanical repeat of the same 3 steps above — no changes to `utils/idempotency.py` or the `idempotency_keys` table are needed.

**Storage:** A single generic `idempotency_keys` table (`database.py::ensure_idempotency_keys_table`) — not a per-endpoint column — keyed by `(portfolio_id, endpoint, idempotency_key)` with a `UNIQUE` constraint, storing the full JSON response body. Concurrent duplicate inserts are resolved via `ON CONFLICT DO NOTHING` (the race loser doesn't overwrite the winner's cached response).

**Known limitation, accepted for v7.10 scope:** the replayed response reflects the JSON-serialized form of what was originally sent to the client (via `json.dumps(..., default=str)`) — equivalent to what the original caller already received over the wire, not a live re-fetch of current resource state.

**Not applied to:** external, non-idempotent mutating calls this codebase makes to third parties (e.g. Alpaca paper-order sync) — that is a distinct problem (the *client-supplied* key pattern here protects *our* API surface from client retries; protecting an *outbound* call to Alpaca from network retries needs Alpaca's own `client_order_id` mechanism, tracked separately as `BLG-BE-80`).

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.4 | 2026-07-29 | ST-03 (EPIC-01, v7.10, BLG-BE-76): Add §Idempotency-key pattern for state-mutating POST endpoints — additive, opt-in-only (client-supplied key) dedup pattern via a generic `idempotency_keys` table and `utils/idempotency.py::replay_or_create`. Applied to `POST /portfolio/position` and `POST /trade-plans`; no change to behaviour when the key is absent (RISK-02). |
| 1.3 | 2026-07-20 | ST-04 (EPIC-04, v7.6, BLG-BE-65): Add §Error-response envelope conformance — full audit of `backend/routers/` (23 files, 79 endpoints) against the canonical envelope in `conventions.md` §13. Three non-conformance patterns found (default FastAPI `{detail}` shape; errors masked as HTTP 200 in `portfolio_risk.py`; correct shape but wrong status code in `digest.py`). Non-conforming endpoints filed as follow-up items (`BLG-BE-67`, `BLG-BE-68`) per this item's acceptance criteria — no router code changed in this item. |
| 1.2 | 2026-07-14 | ST-07 (EPIC-03, v7.1, BLG-SPEC-84): Add §CSV/export response-body pattern — canonical pattern for downloadable-file endpoints, extracted from `GET /reports/tax-year?format=csv` (the first export endpoint in the codebase). Documents the pure-builder-function pattern, format-param branching, auth (automatic via global middleware), charset convention, filename convention, classification, and testing requirement (content-asserting, not download-fired-only). No prior Changelog section existed in this file — added here for consistency with sibling canonical specs. |
| 1.1 | 2026-06-16 | (prior history not retroactively reconstructed — this changelog starts at v1.2; see git history for earlier changes.) |

---

*For detailed rationale behind each decision, see the referenced ADR.*
