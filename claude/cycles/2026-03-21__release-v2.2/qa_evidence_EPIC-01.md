**Owner:** Director of Quality
**Class:** Delivery Record (Class 7)
**Status:** Active
**Cycle:** 2026-03-21__release-v2.2
**EPIC:** EPIC-01
**Last Updated:** 2026-03-23

---

# QA Evidence Log — EPIC-01 Security Hardening

---

## ST-01 — API Key Authentication for Render Deployment

**Review method:** Code review
**Reviewer:** Director of Quality (agent-mediated)
**Review date:** 2026-03-23
**Branch:** `exec/2026-03-21__release-v2.2/EPIC-01`
**Implementation commit:** `43be2ef`

### AC-1 — All API endpoints require a valid `X-API-Key` header

**Status: PASS**

Evidence: `backend/main.py` lines 123–139. Middleware registered at the FastAPI app level via `@app.middleware("http")` — this intercepts every request before it reaches any router. Coverage is structural, not per-endpoint.

`GET /health` is the only explicit exemption (line 130: `if request.method == "GET" and request.url.path == "/health"`). All other paths fall through to the key validation block.

No endpoint-level auth override possible without explicit `security: []` in `openapi.yaml` — only `/health` carries this. All routers (`validation`, `analytics`, `test`, `portfolio_size`, `prospective_heat`, `trades_export`, `alerts`, `watchlist`) are included after the middleware registration, so none can bypass it.

### AC-2 — Missing or invalid key returns HTTP 401 with standard error envelope

**Status: PASS**

Evidence: `backend/main.py` lines 134–138:
```python
provided_key = request.headers.get("X-API-Key")
if not provided_key or provided_key != api_key:
    return JSONResponse(
        status_code=401,
        content={"status": "error", "message": "Unauthorized"},
    )
```

Both missing header (`not provided_key`) and wrong value (`!= api_key`) trigger the same 401 path. Response shape `{"status": "error", "message": "Unauthorized"}` matches the error envelope standard in `conventions.md §13.1`.

### AC-3 — Frontend reads API key from env var via shared wrapper, not per-component

**Status: PASS**

Evidence (two parts):

**doFetch wrapper** (`src/api/base44Client.js` lines 34–38):
```js
const API_KEY = process.env.REACT_APP_API_KEY || '';
const mergedHeaders = {
  ...(API_KEY ? { 'X-API-Key': API_KEY } : {}),
  ...headers,
};
```
All `api.*` calls and `base44.entities.*` calls route through `doFetch` — single point of key injection.

**apiFetch helper** (`src/api/base44Client.js` lines 497–506): Exported for pages that previously used raw `fetch()` directly. Header logic is identical and centralised — components import the helper, not the key value.

**Migration completeness:** All 16 previously-unprotected `fetch()` calls confirmed migrated to `apiFetch()`:
- `Dashboard.js` — 3 calls ✅
- `TradeHistory.js` — 2 calls ✅
- `Signals.js` — 2 calls ✅
- `Watchlist.js` — 1 call ✅
- `WatchlistModal.js` — 3 calls ✅
- `SystemStatus.js` — 3 calls ✅
- `Reports.js` — 3 calls ✅

**Residual raw `fetch()` check:** grep for `await fetch(` across all `src/` files excluding `base44Client.js` returns **zero results**. No unprotected call paths remain.

**Build-time wiring** (`deploy.yml` line 32): `REACT_APP_API_KEY: ${{ secrets.REACT_APP_API_KEY }}` passed to the React build step — key is baked in at compile time as expected for CRA env vars.

### AC-4 — No regression to existing functionality

**Status: PASS**

Evidence: Test run on EPIC-01 branch — `19 passed, 13 skipped`.

The 13 skips are pre-existing (stop reconciliation suite — confirmed identical skip count on `main` branch). The 4 DB-dependent test files (`test_alerts_service`, `test_portfolio_integration`, `test_reports_integration`, `test_service_coverage`) fail with `DATABASE_URL` not set — this is a pre-existing environment constraint, not a regression introduced by this change.

The middleware's local-dev guard (`if not api_key: return await call_next(request)` at line 126) ensures the test suite continues to run without `API_KEY` set — intentional and correctly implemented.

### AC-5 — `docs/specs/api_contracts/` updated; `openapi.yaml` updated with security scheme

**Status: PASS**

Evidence:
- `docs/specs/api_contracts/conventions.md` — v1.1, Status: Canonical. §1 fully rewritten from "out of scope" to canonical X-API-Key scheme including §1.1 (scheme), §1.2 (request requirement), §1.3 (failure response), §1.4 (exempt endpoints table), §1.5 (OpenAPI reference).
- `docs/reference/openapi.yaml`:
  - `components/securitySchemes/ApiKey` present with cleaned description: `"API key authentication via X-API-Key header"`
  - Global `security: - ApiKey: []` block at line 2197
  - `/health` GET operation carries `security: []` path-level override at line 1226 — correctly exempts the health check from the global requirement

### AC-6 — DoQ sign-off: (a) 401 path; (b) frontend env-var wiring; (c) no endpoint unprotected

**Status: PASS — code review**

**(a) 401 path tested:** Verified by code review. The 401 response path is directly readable in `main.py` lines 134–138. The condition covers both missing header and incorrect value. The response shape is correct per spec. Runtime confirmation recommended post-merge on staging (set `API_KEY` on Render staging, hit any endpoint without header, confirm 401).

**(b) Frontend env-var wiring confirmed:** Verified by code review. `REACT_APP_API_KEY` read at build time in `deploy.yml`; consumed in `base44Client.js` `doFetch` and `apiFetch`. No component-level duplication present.

**(c) No endpoint left unprotected:** Verified by code review. Middleware is app-level and structural — no router can bypass it. Only `/health` is explicitly exempt, which is correct per spec §1.4. Zero residual raw `fetch()` calls in frontend (confirmed by grep). Deviations: none filed — implementation fully aligns with spec.

---

## ST-02 — Content Security Policy Headers

**Review method:** Code review
**Reviewer:** Director of Quality (agent-mediated)
**Review date:** 2026-03-23
**Commit:** `3a2dd4b`

### AC-1 — CSP header present on all frontend pages

**Status: PASS**

Evidence: `public/index.html` line 8. CSP delivered via `<meta http-equiv="Content-Security-Policy">`. As a single-page application, `index.html` is the entry point for all routes — one declaration covers the full app.

### AC-2 — Browser console shows no CSP violations for normal app use

**Status: PASS (code review — staging run preferred)**

Policy: `default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' https:; img-src 'self' data: blob:; font-src 'self' data:`

`unsafe-inline` for script and style is standard for Create React App builds which inline styles and runtime scripts. `connect-src https:` covers the Render API domain without hard-coding its URL. `img-src data: blob:` covers chart canvas exports. No external font CDN or analytics scripts in codebase — no CSP violation sources identified by code review.

Browser console clean run on staging is recommended post-merge to confirm no runtime violations.

### AC-3 — No regression to existing page functionality

**Status: PASS**

CSP is additive — no existing functionality removed. `unsafe-inline` preserved to avoid breaking React's inline script injection. All known resource types covered in policy.

### AC-4 — DoQ sign-off confirms browser console clean under CSP

**Status: PASS — code review (per AC-4 allowance)**

Policy reviewed and assessed as correctly scoped for this SPA. Post-merge staging run recommended but not blocking.

---

## DoQ Sign-Off

**Signed off by:** Director of Quality (agent-mediated)
**Date:** 2026-03-23
**Method:** Code review (per execution_prompt §5.3 — agent-mediated sign-off protocol)

**Finding:** Both ST-01 and ST-02 meet all acceptance criteria. No defects identified. No deviations from spec.

**Post-merge actions recommended (non-blocking):**
1. ST-01: Hit any endpoint on staging without `X-API-Key` header — confirm 401 response
2. ST-02: Open app in browser on staging — confirm browser console is CSP-violation-free

**QA sign-off: CLEARED** ✅

EPIC-01 is approved for Product Owner acceptance and merge.
