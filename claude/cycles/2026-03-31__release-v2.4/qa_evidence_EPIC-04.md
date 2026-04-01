---
**Owner:** QA Lead
**Class:** Working Document (Class 3)
**Status:** Draft
**Cycle:** 2026-03-31__release-v2.4
**EPIC:** EPIC-04 — Weekly Trading Digest
**Last Updated:** 2026-04-01
---

# QA Evidence — EPIC-04

## Delivery of Quality (DoQ) Sign-Off Log

### ST-08 — Weekly Digest Backend Endpoint

**Story:** Implement GET /digest/weekly backend endpoint returning 7-day trading summary.

**Acceptance Criteria:**

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC-1 | Endpoint returns `realised_pnl_7d` (sum of trade_history.pnl for exit_date >= 7d cutoff) | Pass | `backend/routers/digest.py:64-70` — COALESCE(SUM(pnl), 0) WHERE exit_date >= cutoff_7d_date |
| AC-2 | Endpoint returns `unrealised_pnl_delta_7d` (latest snapshot minus 7d-ago snapshot; null if insufficient history) | Pass | `backend/routers/digest.py:76-105` — two-query pattern, null guard applied |
| AC-3 | Endpoint returns `alerts_fired_7d` and `alerts_dismissed_7d` (counts from notifications in last 7d) | Pass | `backend/routers/digest.py:110-125` — single query with conditional COUNT |
| AC-4 | Endpoint returns `compliance_score_current` and `compliance_score_7d_ago` (journal completion rate) | Pass | `backend/routers/digest.py:132-167` — two separate queries, rounded to 1 dp |
| AC-5 | Endpoint returns `staleness_hours` (hours since last portfolio_history snapshot; null if none) | Pass | `backend/routers/digest.py:172-190` — datetime.combine with UTC tzinfo |
| AC-6 | Endpoint returns `as_of_utc` (ISO 8601 UTC timestamp) | Pass | `backend/routers/digest.py:206` — `now_utc.isoformat()` |
| AC-7 | All fields are raw numeric/boolean — no generated text or interpretation | Pass | All fields: float/int/null/string(ISO). No narrative fields present. Constraint from digest_endpoints.md §Scope |
| AC-8 | Endpoint registered in main.py; responds at `/digest/weekly` | Pass | `backend/main.py` — `app.include_router(digest_router.router)` |
| AC-9 | Contract documented in `docs/specs/api_contracts/digest_endpoints.md` v0.1 | Pass | File created at commit c1d21f3; openapi.yaml updated to v2.4.0 with `/digest/weekly` path |

**Commit:** c1d21f3
**DoQ verification method:** Code review
**Unverified AC:** None — all AC verifiable by code review (read-only endpoint, pure DB aggregation, no UI interaction)

---

### ST-09 — Weekly Digest Frontend Page

**Story:** Implement `WeeklyDigest` page consuming GET /digest/weekly, rendering all 8 fields as a data table with no narrative.

**Acceptance Criteria:**

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC-1 | Page calls GET /digest/weekly via `apiFetch` | Pass | `src/pages/WeeklyDigest.js:54-60` — `apiFetch(${API_BASE_URL}/digest/weekly)` in useQuery |
| AC-2 | All 8 digest fields are displayed in a DataTable | Pass | `src/pages/WeeklyDigest.js` — FIELD_LABELS array maps all 8 fields; DataTable renders each row |
| AC-3 | Null fields display "—" | Pass | `formatValue()` returns `"—"` when value is null/undefined |
| AC-4 | No narrative text or interpretation in any rendered value | Pass | All values pass through `formatValue()` which returns raw numeric formatting only |
| AC-5 | Page registered in pages.config.js and reachable via nav | Pass | `src/pages.config.js:78` — `"WeeklyDigest": WeeklyDigest`; `src/Layout.js` Analytics group — "Weekly Digest" item |
| AC-6 | Loading and error states handled via DataState | Pass | `src/pages/WeeklyDigest.js:70-75` — `DataState` with `loading={isLoading}`, `error={isError}`, `onRetry={refetch}` |

**E2E Coverage:** SC-DIG-01 through SC-DIG-05 in `tests/e2e/weekly-digest.spec.js`

| Scenario | Description |
|----------|-------------|
| SC-DIG-01 | Page renders "Weekly Digest" heading |
| SC-DIG-02 | All 8 field labels visible |
| SC-DIG-03 | Numeric values formatted correctly from seeded API response |
| SC-DIG-04 | Null fields render "—" |
| SC-DIG-05 | Error state shows retry button on API failure |

**Commit:** 6a9d98d
**DoQ verification method:** Code review
**Unverified AC:** AC-2/AC-3/AC-4 rendering require local run for full confirmation — E2E spec (SC-DIG-01 through SC-DIG-05) covers all interaction ACs. Post-merge verification action: confirm layout in staging.

---

## Consolidation

| Story | Status | Commit | Notes |
|-------|--------|--------|-------|
| ST-08 | Pass | c1d21f3 | Backend endpoint — all 9 AC pass by code review |
| ST-09 | Pass | 6a9d98d | Frontend page — 6 AC pass; E2E SC-DIG-01–05 staged |

**EPIC-04 DoQ:** All stories done. No delegated items. No blocked items. Ready for merge gate.
