**Owner:** API Contracts & Documentation Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-06
**Cycle:** 2026-08-05__release-v8.3 (ST-19 — BLG-SPEC-88)

---

# OpenAPI Response-Example Drift Spot-Check

## Purpose

`BLG-SPEC-88`'s problem statement: the CI OpenAPI Drift Detection gate (`.github/workflows/openapi-drift.yml`) checks structural presence of endpoints (does a `## METHOD /path` heading exist in both the contract and `openapi.yaml`?) but never checks whether the documented **example payloads** still match what the live code actually returns. This is a one-time spot-check of a sample, not an exhaustive audit — per the story's own Effort (S, ~0.5–1 day) and Acceptance Criteria ("sample check performed and documented").

## Method

For each sampled endpoint: read the actual response-construction code (the route handler and, where it delegates, the underlying service/query function) to determine the definitive live field set, then diff that field set against the endpoint's documented example in `docs/specs/api_contracts/`. Reading the source directly (rather than mocking through `TestClient`) was chosen because several of these endpoints mock at a level (e.g. `main.get_positions_with_prices`) that would bypass the very serialisation logic being checked — reading the function body is the more reliable check of what a live response actually contains.

## Sample (6 endpoints)

| Endpoint | Contract file | Result |
|---|---|---|
| `GET /settings` | `settings_endpoints.md` | Drift found — `BLG-SPEC-112` |
| `GET /positions` | `position_endpoints.md` | Drift found — `BLG-SPEC-113` |
| `GET /health` | `health_endpoints.md` | Drift found — `BLG-SPEC-114` |
| `GET /watchlist` | `watchlist_endpoints.md` | Drift found — `BLG-SPEC-115` (largest gap) |
| `GET /portfolio` | `portfolio_endpoints.md` | Envelope shape confirmed correct (`{"status":"ok","data":...}` matches `get_portfolio_summary()`'s wrapping); full field-by-field diff not performed — out of sample budget |
| `GET /trades` | `trade_endpoints.md` | Envelope shape confirmed correct (`{"status":"ok","data":trade_data}` matches the `data`-schema-only example in the contract); full field-by-field diff of `trades[]` item shape not performed — out of sample budget |

### Findings detail

**`GET /settings`** (`BLG-SPEC-112`): handler runs `SELECT * FROM settings` — includes every table column. `created_at`/`updated_at` (both present per `data_model.md`'s `CREATE TABLE settings`) are missing from the documented example.

**`GET /positions`** (`BLG-SPEC-113`): `position_service.py::get_positions_with_prices()` builds an explicit response dict containing `total_cost`, `sector`, `industry` (not documented anywhere in `position_endpoints.md`) plus `exit_reason`, `stop_reason` (documented elsewhere in the file for other position-related shapes, but missing from the `GET /positions` example specifically).

**`GET /health`** (`BLG-SPEC-114`): `health_service.py::get_operational_health()` returns `external_apis` and `ai_journal` nested objects in addition to the 4 documented top-level fields.

**`GET /watchlist`** (`BLG-SPEC-115`): `watchlist_service.py::_row_to_dict()` returns `company_name`, `tags`, `updated_at`, `added_at`, `days_on_watchlist`, `is_stale` — none in the illustrative JSON example — and the example includes `portfolio_id`, which the actual SQL query does not select. **Correction (post agent-mediated sign-off review, 2026-08-06):** `is_stale`/`days_on_watchlist` are, on closer reading, correctly documented in the contract's own field table and version history (just not in the stale JSON example) — the item was originally filed claiming they were "entirely absent from the contract" and raised to P2 on that basis; corrected to P3, the narrower and accurate severity. Still the largest example-completeness gap in this sample (6 fields), just not the mis-stated "whole feature undocumented" severity.

## Disposition

4 genuine drift findings, filed as individual `BLG-SPEC-*` follow-up items per the story's AC:
- `BLG-SPEC-112` (settings — XS)
- `BLG-SPEC-113` (positions — S)
- `BLG-SPEC-114` (health — S)
- `BLG-SPEC-115` (watchlist — S, P3, corrected from an initially-overstated P2 — see finding detail above)

No fixes applied in this story — per the AC's own scope ("spot-check... file individual BLG-SPEC-* items for any drift found"), this is a detection pass, not a remediation pass. Each filed item scopes its own fix.

## Known Deviations

None. This is a net-new artefact — no prior canonical spec governed this work.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-08-06 | 1.0 | Initial spot-check — 6 endpoints sampled, 4 drift findings filed (ST-19, EPIC-04, v8.3, BLG-SPEC-88) |
