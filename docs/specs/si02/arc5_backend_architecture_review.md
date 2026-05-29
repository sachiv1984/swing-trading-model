**Owner:** Head of Engineering; Head of Backend Engineering
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.4 (EPIC-02, ST-07, BLG-BE-18)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Arc 5 Backend Architecture Review

## 1. Purpose

This document reviews the current synchronous FastAPI backend architecture against the query complexity requirements of SI-02 (Behavioural Drift Detection) and SI-04 (future arc). It produces a concrete recommendation on whether SI-02 drift analysis should be served synchronously on-demand, via cached synchronous computation, or via periodic background computation — with rationale grounded in single-user Render deployment constraints.

Input documents:
- `backend/routers/analytics.py` — current synchronous endpoint pattern
- `docs/specs/si02/query_performance_assessment.md` — query cost estimates (BLG-GOV-51)
- `docs/specs/si02/si02_query_predesign.md` — SI-02 draft query patterns (ST-06, v4.4)

---

## 2. Current Architecture Baseline

### 2.1 Synchronous FastAPI Pattern

All existing analytics endpoints follow a synchronous, on-demand request pattern:

1. Request arrives at FastAPI router
2. Router opens a direct `psycopg2` connection to Supabase via `DATABASE_URL`
3. SQL queries execute synchronously (blocking the async event loop via synchronous psycopg2 driver)
4. Results are processed in-memory by the analytics service layer
5. Response returned; connection closed in `finally` block

**Observed p50 latency:** ~230ms base (Supabase + Supavisor pooling, per `query_performance_assessment.md §4`). Endpoint-specific p50 values:
- `GET /analytics/metrics` — ~400ms (multiple queries, service-layer computation)
- `GET /analytics/arc5-compliance` — ~350ms (multi-table aggregation)
- `GET /analytics/market-correlation` — cached at 8h TTL; first-call p50 varies (Yahoo Finance network dependency)

### 2.2 Existing Caching Pattern

One TTL cache pattern is already in production: `GET /analytics/market-correlation` uses a module-level Python dict (`_CORRELATION_CACHE`) with an 8-hour TTL. This demonstrates the project already accepts in-process caching as a valid pattern for expensive, slowly-changing data.

### 2.3 Render Deployment Constraints

The application runs on Render with the following architectural constraints:

| Constraint | Detail |
|-----------|--------|
| Instance count | 1 web service instance (single-user) |
| Worker dynos | None — Render free/hobby tier does not support separate worker dynos |
| Redis / Celery | Not available — no managed Redis service provisioned |
| Cron Jobs | Available as a separate Render Cron Job service (separate deployment) |
| Persistent shared memory | Not available across restarts (in-process dict cache resets on deploy) |
| Supabase connection pool | Supavisor (pooled mode enabled v2.7); max ~20 concurrent connections |

---

## 3. SI-02 Query Complexity Assessment

### 3.1 Query Cost at Current Volume

Per `si02_query_predesign.md §5.2`, all SI-02 drift queries are estimated at 250-400ms p50 at < 20 trades. This is on par with existing analytics endpoints. No query exhibits complexity that would push response time above acceptable thresholds at this volume.

### 3.2 Query Cost at Scale

| Trade Volume | Estimated p50 (all drift metrics combined) | Risk |
|-------------|-------------------------------------------|------|
| < 20 trades | ~400ms | Low |
| 20-100 trades | ~500ms | Low |
| 100-200 trades | ~700ms | Low-Medium |
| 200-500 trades | ~1,500ms | Medium (consecutive loss self-join) |
| 500+ trades | 2,000ms+ | High (consecutive loss without pre-computation) |

**Key risk:** The consecutive loss self-join (`O(N²)` per `query_performance_assessment.md §2.2`) is the only query that exhibits non-linear scaling. All other SI-02 queries are O(N) and index-supported.

### 3.3 SI-04 Scope Note

SI-04 (future arc) has not yet been fully specced. This review focuses on SI-02 only. SI-04 architecture must be reviewed separately when its query patterns are defined.

---

## 4. Architecture Options Evaluated

### Option A — Synchronous On-Demand per Request

**Description:** SI-02 drift analysis runs synchronously on each `GET /analytics/behavioural-drift` request, exactly as existing analytics endpoints run.

**Pros:**
- Zero additional infrastructure
- Consistent with existing codebase pattern
- Response always reflects latest trade data
- No cold-start latency for first user after deploy

**Cons:**
- At 200+ trades, consecutive loss query will push response to ~1,500ms
- Supabase connection is held for the full query duration on every request
- No protection against repeated calls within seconds (e.g. frontend polling)

**Verdict:** Viable for MVP at current trade volume (< 20). Requires re-evaluation when portfolio reaches 200 trades.

---

### Option B — Cached Synchronous with TTL

**Description:** SI-02 drift data is computed on the first request and cached in-process (module-level dict) for a configurable TTL. Subsequent requests within the TTL window return the cached result. Mirrors the `_CORRELATION_CACHE` pattern already in production.

**Pros:**
- Zero additional infrastructure — uses pattern already proven in production
- Protects against repeated API calls (frontend refresh, accidental polling)
- First-call latency is the same as Option A; subsequent calls return cached result in < 5ms
- TTL is configurable (e.g. 8h, matching `market-correlation`; or shorter, e.g. 1h)
- Cache resets on deploy, which is acceptable for advisory drift data (staleness on restart is non-material)

**Cons:**
- Data is stale within the TTL window — a new closed trade will not appear in drift output until cache expires
- In-process dict does not survive Render restarts (acceptable; cache resets gracefully)
- Does not solve the underlying query cost at 200+ trades — mitigates only repeated call overhead

**Verdict:** Recommended for MVP. Drift data is advisory and does not require real-time freshness. An 8-hour TTL is appropriate — drift patterns do not change within hours. Consistent with existing codebase.

---

### Option C — Periodic Background Computation

**Description:** SI-02 drift metrics are pre-computed on a schedule (e.g. nightly) and stored in a database table or JSONB column. `GET /analytics/behavioural-drift` reads pre-computed results rather than executing queries in real time.

**Pros:**
- No request-time query cost — endpoint becomes a simple table read (~50ms)
- Solves scale problem definitively: computation runs once per period regardless of trade volume
- Enables trend analysis over time (store historical snapshots)

**Cons:**
- Requires Render Cron Job service as a second deployment or APScheduler in-process thread
- Requires a new `drift_snapshots` table (schema migration, additional complexity)
- Adds operational surface: cron failure means stale drift data with no fallback
- In-process background thread (APScheduler) is fragile on Render: restarts kill threads; thread errors are silent unless explicitly monitored
- Overkill at current trade volume where queries take < 400ms and the user is single-person

**Verdict:** Not recommended for MVP. Adds infrastructure complexity disproportionate to the problem at current trade volume. Re-evaluate when portfolio exceeds 200 trades, at which point the consecutive loss query may breach acceptable latency thresholds.

---

## 5. Recommendation

**Implement SI-02 as Option B: cached synchronous with TTL.**

**Rationale:**

1. **Query cost is acceptable at current volume.** All SI-02 drift queries complete in < 400ms p50 at < 20 trades. Option A (pure synchronous) would be functionally sufficient; Option B adds protective caching at zero infrastructure cost.

2. **The caching pattern is already proven in production.** The `_CORRELATION_CACHE` pattern in `analytics.py` is a direct precedent. Drift data is advisory and non-time-critical — an 8-hour TTL is appropriate and consistent with the existing market-correlation cache TTL.

3. **Single-user Render deployment precludes background workers.** There is no worker dyno, no Redis, no managed task queue. Option C would require either a Render Cron Job (a separate deployment with its own failure modes) or an in-process APScheduler thread (fragile on restart). Neither is justified at this trade volume.

4. **The scale inflection point is well-defined.** The consecutive loss query becomes problematic at 200+ trades. Before that threshold is reached, the architecture can be upgraded. The upgrade path is clear: materialise `prior_losses_60d` into `trade_plans` at entry time (a single-field addition), eliminating the self-join entirely. This is preferable to adding background infrastructure prematurely.

5. **Display-only advisory data tolerates TTL staleness.** Per `section13_criteria.md §3.2`, SI-02 outputs are advisory only. A trade closed after the cache was populated will not appear in drift analysis until the next cache expiry — this is acceptable behaviour for an advisory feature.

**Recommended TTL:** 8 hours (matching `market-correlation`). Configurable via a `DRIFT_CACHE_TTL_HOURS` environment variable for future adjustment without a code change.

**Scaling trigger:** When `trade_history` row count for a portfolio exceeds 150, re-evaluate. Action at that point: materialise `prior_losses_60d` computation into trade_plans at entry time via a trade creation hook in `position_service.py`.

---

## 6. Architecture Decision Record

ADR filed per AC-03 requirement: background layer is not recommended; however, the decision not to implement background computation is a material architectural choice that warrants documentation.

### ADR-001: SI-02 Uses Cached Synchronous Pattern, Not Background Computation

**Status:** Accepted

**Context:**
SI-02 (Behavioural Drift Detection) requires joining trade_history, trade_plans, positions, and signals tables to compute drift metrics. The application runs on a single Render web service with no background worker, no Redis, and no Celery. Current trade volume is < 20 closed trades.

**Decision:**
Use cached synchronous computation (Option B) with an 8-hour in-process TTL cache. Do not implement a background computation layer for SI-02 at MVP.

**Rationale:**
- Query latency is within acceptable range (< 400ms p50) at current volume
- The in-process TTL cache pattern is already proven in production (`_CORRELATION_CACHE`)
- Background computation requires Render Cron Job or APScheduler, both of which add operational risk disproportionate to the problem at current scale
- SI-02 data is advisory; TTL staleness of up to 8 hours is acceptable

**Consequences:**
- No new infrastructure required
- Drift data is stale within the TTL window (acceptable for advisory use case)
- Architecture must be re-evaluated when trade_history exceeds 150 rows per portfolio
- The consecutive loss self-join must be replaced with a pre-computed field before trade volume reaches 200 — this is a backlog item to file at SI-02 sprint planning

**Alternatives rejected:**
- Background computation (Option C): excessive complexity for current scale; no suitable Render-native infrastructure without a second deployment
- Pure synchronous with no caching (Option A): functionally sufficient but provides no protection against repeated calls; no reason not to add caching given the precedent

**Review trigger:** Re-open this ADR when trade_history row count for the primary portfolio exceeds 150 closed trades, or when SI-04 query patterns are defined (whichever comes first).

---

## 7. Impact on SI-02 Sprint Planning

This review produces the following inputs for SI-02 sprint planning capacity estimation:

| Item | Effort | Notes |
|------|--------|-------|
| Implement `GET /analytics/behavioural-drift` endpoint (synchronous) | M | Standard analytics endpoint; follows analytics.py pattern |
| Add module-level TTL cache (8h) | XS | Mirrors `_CORRELATION_CACHE` pattern; ~10 lines |
| Add `DRIFT_CACHE_TTL_HOURS` env var with default | XS | Config change only |
| Write DS-07 migration (3 columns + signal index) | S | Per `si02_query_predesign.md §4` |
| Write SI-02 P2 index migration (2 indexes) | XS | Per `si02_index_preassessment.md §4.2` |
| Register new endpoint in `backend/routers/test.py` | XS | Governance requirement |
| Update `docs/reference/openapi.yaml` | XS | Governance requirement (same commit as contract) |
| Write API contract for SI-02 endpoint | XS | Required before sprint planning seals (section13_criteria.md §4) |

**Total backend story capacity estimate for SI-02 sprint:** 1 M story (endpoint + cache) + 3 XS tasks (indexes, test registration, openapi) + 1 S story (DS-07 migration). Well within standard sprint capacity.

---

## 8. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Head of Engineering | Approved | 2026-05-29 |
| Head of Backend Engineering | Approved | 2026-05-29 |
