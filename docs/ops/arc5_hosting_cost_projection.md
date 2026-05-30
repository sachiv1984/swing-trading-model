**Owner:** FinOps & Resource Architect
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-30
**Story:** ST-10 (BLG-OPS-40, EPIC-03, v4.6)
**Reference baseline:** `docs/ops/api_performance_baseline.md` v2.0
**Reference ADR:** `docs/specs/si02/arc5_backend_architecture_review.md` v1.0
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Arc 5 Hosting Cost Projection — SI-02 Behavioural Drift Detection

## 1. Purpose

This document assesses the additional compute and infrastructure cost introduced by the SI-02 Behavioural Drift Detection feature (`GET /analytics/behavioural-drift`) relative to the current Render hosting tier, and states a recommendation on whether the current tier is adequate.

**Scope:** SI-02 backend only (v4.6 EPIC-01). SI-02 frontend (EPIC-02, conditional on data density gate) does not introduce additional backend load beyond what is assessed here.

---

## 2. Current Infrastructure Baseline

### 2.1 Compute Tier

| Component | Configuration |
|-----------|--------------|
| Backend API | Render Starter tier (single instance, auto-deploy from main) |
| Database | Supabase with Supavisor transaction pooling enabled (port 6543, `?pgbouncer=true`) since v2.7 (2026-04-16) |
| Workers | None — Render Starter does not support background worker dynos |
| Cron jobs | Not provisioned for this system |
| Redis / queue | Not provisioned |

### 2.2 Existing Analytics Endpoint Performance (Post-Supavisor)

From `api_performance_baseline.md §10` (v2.7 re-run, 2026-04-16):

| Metric | Value |
|--------|-------|
| DB-backed endpoint p50 range | 226–244ms |
| GET /analytics/arc5-compliance (estimated) | 250–400ms (§13, v4.1 entry) |
| POST /ai/check-daily-cost | 205ms p50 (§14) |
| Supavisor connection overhead | ~50–80ms per query (vs ~1,500ms on free tier) |

All existing DB-backed analytics endpoints operate inline (synchronous, per-request). No background jobs or caching layers beyond the `GET /analytics/market-correlation` 8h in-process TTL cache (single endpoint, not a pattern used elsewhere).

---

## 3. SI-02 Compute Load Assessment

### 3.1 Execution Pattern

SI-02 uses the **cached-synchronous** pattern recommended in `arc5_backend_architecture_review.md` (Option B). Each call to `GET /analytics/behavioural-drift` executes inline SQL queries and returns the result directly. No background job. No scheduled compute.

**Load profile: on-demand only.** The endpoint incurs compute cost only when a user navigates to the Behavioural Drift panel.

### 3.2 Query Breakdown

`get_behavioural_drift_data()` in `backend/database.py` executes 3 queries per request:

| Query | Tables touched | Filter | Estimated cost at current volume |
|-------|---------------|--------|----------------------------------|
| Q1 — Closed trades in 90-day window | `trade_history`, `positions`, `trade_plans` | `portfolio_id`, `pnl IS NOT NULL`, `entry_date >= NOW() - 90d` | < 10ms (< 50 rows) |
| Q2 — Signal timing | `trade_history`, `positions`, `trade_plans`, `signals` | Same + `signal_id IS NOT NULL` | < 10ms (subset of Q1) |
| Q3 — Current settings | `settings` | `LIMIT 1` | < 5ms |
| **Supavisor overhead** | — | — | ~50–80ms per query round-trip |
| **In-memory computation** | Python only | 4 metric aggregations over < 50 items | < 1ms |

**Total estimated p50: 250–350ms** at current trade volume (< 50 closed trades). This is consistent with the existing analytics endpoint cluster.

### 3.3 Data Volume Sensitivity

| Trade volume | Estimated p50 | Notes |
|-------------|--------------|-------|
| < 50 trades (current) | 250–350ms | Supavisor overhead dominates; query execution negligible |
| 50–200 trades | 300–450ms | Multi-row JOIN begins to add query cost; still within Supavisor cluster |
| 200–500 trades | 400–600ms | 90-day rolling window caps the active dataset; still manageable inline |
| 500+ trades | > 600ms | At this volume, consider adding a result cache (TTL 1–4h in-process, consistent with market-correlation pattern) |

**Current data volume (< 50 trades) is well within the inline synchronous comfort zone.** A caching layer is not required until trade volume exceeds ~500 closed trades.

### 3.4 Load Frequency

This is a **single-user system** (sole operator). Expected usage pattern:
- Drift panel viewed: 2–5 times per week during portfolio review sessions
- Each view: 1 endpoint call to `GET /analytics/behavioural-drift`
- Additional calls: 0 (no polling; no automated triggers; no background job)

**Weekly incremental load: 2–5 requests/week.** This is negligible relative to existing endpoint call frequency.

---

## 4. Render Compute Tier Headroom

### 4.1 CPU

SI-02 in-memory computation consists of:
- Looping over < 50 trade records (4 metric passes)
- Simple arithmetic (AVG, COUNT, threshold comparisons)
- No ML inference, no matrix operations, no heavy sorting

**CPU impact: negligible.** Python arithmetic on < 50 records executes in < 1ms. No change to CPU usage profile at current volume.

### 4.2 Memory

- Q1 result: < 50 rows × ~200 bytes/row ≈ < 10KB
- Q2 result: subset of Q1
- Q3 result: 1 row ≈ < 500 bytes
- Total per-request working memory: < 25KB

**Memory impact: negligible.** No persistent in-memory state is added (inline pattern, no cache allocated at this volume).

### 4.3 Database Connections

Supavisor transaction pooler allocates connections from a shared pool:
- SI-02 holds a single transaction for ~50–80ms per query call (3 calls sequential)
- Total connection hold time per request: ~150–240ms
- At 2–5 calls/week: ~0.3–1.2 seconds of connection hold time per week

**Supavisor headroom impact: negligible.** The 20-connection pool (per arc5_backend_architecture_review.md §2.3) is not meaningfully stressed by 2–5 calls/week from a single user.

### 4.4 Render Monthly Cost

SI-02 adds no new Render services. The existing single web service instance handles the endpoint. At Render Starter pricing:

| Item | Current cost | Change from SI-02 |
|------|-------------|-------------------|
| Web service (Starter) | Fixed monthly fee | No change |
| Supabase (existing tier) | Fixed or usage-based | Negligible: < 10KB data transferred per call, 2–5 calls/week |
| Additional services | None | None (no worker, no cron, no Redis) |

**Estimated incremental cost: $0.00/month** at current usage patterns and Render Starter pricing.

---

## 5. Arc 5 Projected Cumulative Load (SI-01 through SI-05)

| Signal | Status | Endpoint(s) | Load pattern | Incremental p50 contribution |
|--------|--------|-------------|-------------|------------------------------|
| SI-01 | Live | `GET /portfolio/pre-entry-validation` | On-demand (per trade entry) | ~300ms/call |
| SI-02 | Shipping v4.6 | `GET /analytics/behavioural-drift` | On-demand (panel view) | ~300ms/call |
| SI-03 | Live | `GET /portfolio/red-flag-journal` | On-demand (journal view) | ~230ms/call |
| SI-04 | Future | TBD | TBD | TBD |
| SI-05 | Future | Weekly digest trigger | Weekly batch (Telegram) | ~500ms/week batch |

**SI-02 is the 4th Arc 5 signal.** The cumulative load from SI-01, SI-02, SI-03 remains well within current tier headroom. All three are on-demand, single-user endpoints. No Arc 5 feature introduces background compute or continuous polling.

---

## 6. Recommendation

**Current Render Starter tier is adequate for SI-02 load at current data volume and usage patterns.**

Quantified basis:
- SI-02 adds ~300ms of Supavisor-pooled query time per call (consistent with existing analytics cluster)
- Expected frequency: 2–5 calls/week (single-user system)
- Zero incremental compute cost at current volume
- No new infrastructure required (no background workers, no Redis, no cron jobs)

**Conditions that would trigger a tier upgrade review:**

| Trigger condition | Threshold | Recommended action |
|------------------|-----------|-------------------|
| Trade volume growth | > 500 closed trades | Add in-process result cache (TTL 1–4h) — no tier change required |
| Concurrent users | > 1 active user | Re-evaluate Render tier and Supavisor pool sizing |
| SI-02 endpoint p95 > 1,000ms sustained | — | Instrument and investigate; consider caching before tier upgrade |
| Monthly Render cost > budget ceiling | — | Review service tier options; Render Pro (~$7/month) adds persistent disk; evaluate ROI |

---

## 7. Sign-Off

| Role | Status | Date |
|------|--------|------|
| FinOps & Resource Architect | ✅ Approved | 2026-05-30 |

**FinOps & Resource Architect notes:** SI-02 compute load is negligible at current data volume (< 50 trades). The inline cached-synchronous pattern (per arc5_backend_architecture_review.md ADR-SI02-001) is the cost-optimal choice for a single-user system at this scale — it incurs zero idle compute cost and adds < 350ms to on-demand endpoint latency. No upgrade to the current Render Starter tier is warranted before trade volume exceeds 500 closed trades. This assessment should be revisited when the data density gate for PO-04 (50+ trades) is met.
