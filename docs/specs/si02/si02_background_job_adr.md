**Owner:** Head of Backend Engineering; Head of Engineering
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.4 (EPIC-02, ST-09, BLG-BE-20)
**Gate inputs:** ST-06 (si02_query_predesign.md), ST-07 (arc5_backend_architecture_review.md)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# SI-02 Background Job Architecture Design

## 1. Purpose

This document evaluates three background computation architectures for SI-02 (Behavioural Drift Detection) drift analysis and produces a formal Architecture Decision Record (ADR) selecting the approach for the MVP implementation sprint. It is filed as an explicit input to SI-02 sprint planning.

Gate condition verified: ST-06 (si02_query_predesign.md, commit e97745c3) and ST-07 (arc5_backend_architecture_review.md, commit e97745c3) outputs available and reviewed before commencing.

---

## 2. Problem Statement

SI-02 requires executing five SQL queries against `trade_history`, `trade_plans`, `positions`, and `signals` to compute drift metrics. These queries must produce results for display in the frontend `DriftAnalysisPanel`. The architecture question is:

**When and how should drift metrics be computed?**

Three candidate approaches exist:

| Option | Description |
|--------|-------------|
| A | On-demand per-request computation — queries execute synchronously on every `GET /analytics/behavioural-drift` request |
| B | Periodic background cron task — drift metrics pre-computed on a schedule and stored; API reads from pre-computed results |
| C | Event-triggered on trade close — drift metrics recomputed when a trade closes (triggered via trade creation/update hook) |

---

## 3. Deployment Constraints

The application runs on a single Render web service instance with the following hard constraints, established in `arc5_backend_architecture_review.md §2.3`:

| Constraint | Detail |
|-----------|--------|
| Instance count | 1 web service instance (single-user) |
| Worker dynos | None — Render free/hobby tier has no separate worker dynos |
| Redis / Celery | Not provisioned — no managed Redis, no task queue infrastructure |
| Cron Jobs | Available as a separate Render Cron Job service (separate deployment unit) |
| Persistent shared memory | Not available across restarts — in-process caches reset on deploy |
| Trade frequency | < 20 closed trades currently; PT-04 gate (≥ 20 trades) not yet met |

---

## 4. Query Cost Baseline

From `si02_query_predesign.md §5.2` and `arc5_backend_architecture_review.md §3.2`:

| Trade volume | All drift queries combined p50 | Primary risk |
|-------------|-------------------------------|-------------|
| < 20 trades | ~400ms | None |
| 20–100 | ~500ms | Low |
| 100–200 | ~700ms | Low-medium |
| 200–500 | ~1,500ms | Medium (consecutive loss self-join O(N²)) |
| 500+ | 2,000ms+ | High without pre-computation |

The **consecutive loss context query** (`si02_query_predesign.md §3.5`) is the sole non-linear query. All other SI-02 queries are O(N) and index-supported.

Scale inflection point: 150 closed trades per portfolio (per `arc5_backend_architecture_review.md §5`).

---

## 5. Option Evaluations

### 5.1 Option A — On-Demand Per-Request Computation

**Description:** Every `GET /analytics/behavioural-drift` call executes all five drift queries synchronously before returning a response.

**Trade-offs:**

| Dimension | Assessment |
|-----------|-----------|
| Infrastructure | Zero additional infrastructure — same pattern as all existing analytics endpoints |
| Latency (MVP, < 20 trades) | ~400ms p50 — within acceptable range |
| Latency (200+ trades) | ~1,500ms — unacceptable for a dashboard panel expected to load within ~500ms |
| Data freshness | Maximum — always reflects latest trade data |
| Repeated calls | Executes full query set on every request — no protection against rapid re-renders or polling |
| Failure modes | Query timeout manifests as 500 on the API response — user sees error state |

**Verdict:** Viable for MVP at current trade volume. Becomes unacceptable at 200+ trades without mitigation. Does not protect against repeated call overhead.

---

### 5.2 Option B — Periodic Background Cron Task

**Description:** Drift metrics are pre-computed on a schedule (e.g. nightly) by a background process and stored in a dedicated `drift_snapshots` table or JSONB column. The API endpoint reads pre-computed results rather than executing queries at request time.

**Sub-option B1 — Render Cron Job Service:**
A separate Render Cron Job deployment executes the drift computation script on a configurable schedule (e.g. `0 6 * * *` — 6am daily).

**Sub-option B2 — APScheduler In-Process:**
A background scheduler (APScheduler or equivalent) runs within the existing FastAPI process on a schedule, computing and storing drift results without a separate deployment.

**Trade-offs:**

| Dimension | B1 (Render Cron) | B2 (APScheduler) |
|-----------|-----------------|-----------------|
| Infrastructure | Second Render deployment unit (separate Git deploy, env vars, health monitoring) | No new infrastructure — runs in existing process |
| Request latency | ~50ms (simple table read) | ~50ms (simple table read) |
| Data freshness | Stale up to schedule period (e.g. 24h if daily) | Stale up to schedule period |
| Failure mode | Cron failure → stale data; no fallback | Process restart kills scheduler; thread errors may be silent |
| Schema change | New `drift_snapshots` table required | New `drift_snapshots` table required |
| Operational complexity | High — second deployment to monitor and debug | Medium — thread lifecycle tied to web process; harder to debug |
| Trade closures mid-period | Missed until next cron run | Missed until next scheduled run |

**Render Cron Job specifics:**
- Requires a separate `render.yaml` or Render dashboard cron configuration
- Incurs additional Render service cost
- Cron failures are not automatically visible in the main web service logs
- Acceptable if drift data staleness of 24h is tolerable for advisory display (it is, per §13 criteria)

**APScheduler specifics:**
- In-process threads on Render are fragile: Render may restart the dyno without warning (spinning down on inactivity for free tier)
- A restarted dyno loses all scheduler state; the next computation runs only when the scheduler next ticks
- Thread exceptions in background schedulers are often swallowed unless explicitly logged
- APScheduler adds a library dependency; requires careful lifecycle management with FastAPI startup/shutdown events

**Verdict:** Not recommended for MVP. Both sub-options add significant complexity (schema migration + operational overhead) that is disproportionate to the problem at current trade volume. Re-evaluate at the scale trigger point (150 closed trades).

---

### 5.3 Option C — Event-Triggered on Trade Close

**Description:** Drift metrics are recomputed each time a trade is closed. The trade close event (via `POST /trade-history` or `position_service.py` close hook) triggers a synchronous or async drift recomputation, and the result is stored.

**Trade-offs:**

| Dimension | Assessment |
|-----------|-----------|
| Infrastructure | No new deployment; computation triggered in-process on trade close |
| Data freshness | Maximum — drift updated immediately after each trade closes |
| Request latency | ~50ms (read from stored result) |
| Coupling | Tight coupling between trade close path and drift computation — a drift query failure can impact trade close success |
| Trade close latency | Adds ~400ms to the trade close response if drift computed synchronously; or adds async complexity if deferred |
| Failure isolation | Drift failure in the trade close handler risks blocking trade persistence — violates the advisory-only principle |
| Schema change | New storage for drift result required (column on trade_history or separate table) |

**Failure mode risk:** The most significant concern is that a drift computation error on trade close would surface as a trade close failure — directly violating the `section13_criteria.md §3.4` requirement that SI-02 has no automated action pathway or side-effect on trade operations. Even if the drift computation is made non-blocking (async), it couples the trade close event to drift logic, creating a hidden operational dependency.

**Verdict:** Rejected. The event-triggered model is the highest-freshness option, but coupling drift computation to the trade close path creates unacceptable risk of SI-02 affecting trade operations. Violates the spirit of display-only / no-side-effects (§13 criterion 3.4). Not recommended even at scale.

---

## 6. Architecture Decision Record

### ADR-SI02-001: SI-02 Drift Analysis Uses Cached Synchronous Pattern for MVP; Background Computation Deferred

**Status:** Accepted

**Date:** 2026-05-29

**Decision makers:** Head of Backend Engineering, Head of Engineering

**Context:**
SI-02 (Behavioural Drift Detection) requires executing five SQL drift queries to populate the frontend `DriftAnalysisPanel`. The application runs on a single Render web service instance with no background worker infrastructure. Current trade volume is < 20 closed trades (PT-04 gate not yet met). The feature is advisory-only per `section13_criteria.md`.

Three background computation approaches were evaluated: (A) on-demand synchronous, (B) periodic background cron/scheduler, and (C) event-triggered on trade close.

**Decision:**
Implement SI-02 as **cached synchronous computation** (a variant of Option A with in-process TTL caching):

- Drift queries execute synchronously on the first `GET /analytics/behavioural-drift` request
- Results cached in-process (module-level dict) with an 8-hour TTL — mirrors the existing `_CORRELATION_CACHE` pattern in `analytics.py`
- Background computation options (B1, B2, C) are deferred to the scale trigger point

**Rationale:**

1. **Query cost is acceptable at MVP volume.** All SI-02 queries complete in < 400ms p50 at < 20 trades. The consecutive loss self-join becomes problematic at 200+ trades — this is the explicit re-evaluation trigger.

2. **Background computation adds infrastructure disproportionate to the problem.** Option B1 (Render Cron) requires a second deployment unit with its own failure modes. Option B2 (APScheduler) is fragile on Render's dyno restart behaviour. Neither is justified until the scale inflection point is reached.

3. **Event-triggered computation (Option C) is rejected categorically.** Coupling drift logic to the trade close path risks SI-02 affecting trade operations, violating `section13_criteria.md §3.4` (no automated action or side-effect on trade paths). This constraint is absolute and applies at any trade volume.

4. **The caching pattern is already proven.** `analytics.py` uses `_CORRELATION_CACHE` with an 8-hour TTL. Drift data is advisory and tolerates the same staleness window. Adding a second cache dict is a < 10 line change.

5. **The upgrade path is well-defined.** When trade_history exceeds 150 rows per portfolio, two targeted changes resolve the scale issue: (a) materialise `prior_losses_60d` into `trade_plans` at entry time, eliminating the O(N²) self-join; (b) optionally reduce the TTL or add explicit cache invalidation on trade close (without full drift recomputation on the close path). Full background computation remains a future option but is not required at this scale.

**Constraints:**

- Cached synchronous pattern must not be applied to the trade close path (no coupling)
- Cache TTL: 8 hours (default, matching `market-correlation`); configurable via `DRIFT_CACHE_TTL_HOURS` env var
- Cache key: `portfolio_id` (scoped per portfolio)
- Cache reset: on deploy (acceptable; advisory data tolerates restart-induced reset)

**Failure modes:**

| Failure | Impact | Mitigation |
|---------|--------|-----------|
| Drift query timeout | API returns 504; frontend shows error state | Standard FastAPI timeout handling; no trade operation impact |
| Cache miss (first request post-deploy) | ~400ms latency on first call | Acceptable; subsequent calls return cached result |
| Stale cache showing old drift data | User sees drift data up to 8h old | Acceptable for advisory-only feature; data will refresh on next TTL expiry |

**Review trigger:**
Re-open this ADR when `trade_history` row count for the primary portfolio exceeds 150 closed trades, or when SI-04 query patterns are defined (whichever comes first). At that point, evaluate:
- Materialising `prior_losses_60d` into `trade_plans` (preferred mitigation — avoids background infrastructure)
- If materialisation insufficient: evaluate Render Cron Job (B1) with a `drift_snapshots` table

**Alternatives rejected:**
- Option B1 (Render Cron): Adds second deployment unit, schema migration, and operational complexity before scale justifies it
- Option B2 (APScheduler): Fragile on Render restart; thread errors may be silent; schema migration still required
- Option C (event-triggered): Categorically rejected — couples drift to trade close path; violates §13 display-only constraint regardless of scale

---

## 7. Impact on SI-02 Sprint Planning

This ADR produces the following capacity inputs for SI-02 sprint planning:

| Item | Effort | Sprint |
|------|--------|--------|
| No background job infrastructure required | — | No additional story needed |
| Module-level TTL cache for drift endpoint | XS (~10 lines) | Include in backend endpoint story |
| `DRIFT_CACHE_TTL_HOURS` env var | XS | Include in endpoint story |
| **No `drift_snapshots` table needed** | — | No migration required for background job |

**Net SI-02 sprint planning impact:** Background computation is deferred. The backend implementation story for `GET /analytics/behavioural-drift` is simpler than if a background layer were required — it follows the existing `arc5-compliance` endpoint pattern with the addition of a TTL cache.

**Backlog item to file at SI-02 sprint planning:** File a `BLG-BE` item for "materialise `prior_losses_60d` into trade_plans at trade close — pre-computation mitigation for consecutive loss query at 150+ trades". This ensures the upgrade path is tracked before it becomes urgent.

---

## 8. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Head of Backend Engineering | Approved | 2026-05-29 |
| Head of Engineering | Approved | 2026-05-29 |
