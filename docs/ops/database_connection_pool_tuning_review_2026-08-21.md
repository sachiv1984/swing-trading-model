**Owner:** Backend Engineering Patterns Owner; Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-08-21
**Story:** ST-24 (BLG-BE-54, EPIC-05, v9.0)
**Prior related assessment:** `docs/specs/si02/arc5_backend_architecture_review.md` §2.3 (records the current Supavisor ceiling); `docs/ops/api_performance_baseline.md` v1.2 (records Supavisor's original 2026-04-16 enablement and its latency impact)

---

# Database Connection Pool Tuning Review

## 1. Purpose

`BLG-BE-54`: "the database connection pool size has not been reviewed against actual concurrent load since v6.8's added traffic; it may be mis-sized in either direction." This reviews the actual current state and records a recommendation.

## 2. Finding: there is no application-level connection pool to tune (AC reframed)

The story's proposed solution ("measure current concurrent connection usage and compare against the configured pool size; adjust if warranted") assumes an application-level pool config exists in this codebase. It does not.

**Verified against `backend/database.py`:**
```python
@contextmanager
def get_db():
    """Database connection context manager"""
    conn = psycopg2.connect(_clean_db_url(DATABASE_URL), cursor_factory=RealDictCursor)
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
```

Every call to `get_db()` opens a fresh `psycopg2.connect()` and closes it in the `finally` block — there is no `psycopg2.pool.SimpleConnectionPool`/`ThreadedConnectionPool`, no SQLAlchemy engine (despite `sqlalchemy==2.0.23` being listed in `requirements.txt` — confirmed via `grep -rln "sqlalchemy\|create_engine" backend/` returning zero matches; it is an unused dependency, not a pool mechanism in use), and no other client-side pooling construct anywhere in `backend/`.

**Actual pooling happens entirely on the Supabase side**, via Supavisor (transaction-pooling mode, port 6543, enabled v2.7/2026-04-16 per `api_performance_baseline.md` v1.2). `docs/specs/si02/arc5_backend_architecture_review.md` §2.3 records its current ceiling: **max ~20 concurrent connections**. This is a Supabase-plan-level setting, not a value configured anywhere in this repository — there is no code-level "pool size" for this story to measure against or adjust.

## 3. Load signal (proxy, same constraint class as `render_starter_tier_headroom_reassessment_2026-08-13.md`)

This sandbox has no live Supabase dashboard access to pull actual concurrent-connection utilization graphs (same constraint disclosed in that document for Render's CPU/memory metrics). Available proxy signals:

- **Supavisor's own enablement history is the strongest evidence available**: `api_performance_baseline.md` v1.2 (2026-04-16) recorded the *before* state directly — without pooling, p50 latency was 1,100–6,000ms; after enabling Supavisor, p50 dropped to 226–244ms across the 5-endpoint sample. This confirms pooling itself is working as intended.
- **No connection-exhaustion incident since**: scanning `api_performance_baseline.md`'s full Document History (v1.2 → v2.31, 2026-04-16 → 2026-08-11, ~30 version bumps across ~4 months of continuous endpoint registrations and live timing runs) finds no entry flagging a "too many connections", pool-exhaustion, or connection-timeout regression. Several entries do flag latency regressions for other reasons (e.g. §18's 4 high-latency endpoints, 2026-06-11) — none attribute the cause to connection pool pressure.
- **Traffic remains low**: consistent with `render_starter_tier_headroom_reassessment_2026-08-13.md` §4's trade-volume signal (single-digit-to-low-tens of trades in the trailing 90-day window) and single-Render-instance deployment (no worker dynos, no horizontal scaling) — the realistic number of concurrent in-flight requests from this application is small, well within Supavisor's ~20-connection ceiling.

## 4. Recommendation

**Hold — no pool-size change actionable or warranted.** There is no application-level pool for this story to adjust. Supavisor's externally-managed ~20-connection ceiling shows no sign of being a binding constraint at current traffic (no incidents on record across 4+ months since its enablement; latency has remained in its post-enablement 226–400ms p50 band per `api_performance_baseline.md`'s continued registrations). If Supavisor's own ceiling needs to change, that requires a live Supabase dashboard/plan-tier change — out of this sandbox's reach, the same class of constraint as `render_starter_tier_headroom_reassessment_2026-08-13.md`'s Render dashboard limitation.

**Residual gap (disclosed):** this recommendation is proxy-derived (enablement-history + incident-absence), not confirmed against a live Supavisor connection-utilization graph. Recorded as a follow-up condition, not a blocking gap, consistent with this cycle's other proxy-derived infra reviews (ST-13, ST-15/`render_starter_tier_headroom_reassessment_2026-08-13.md`).

**Scope note:** `connect_timeout`/`statement_timeout` were not reviewed here — `grep -rn "connect_timeout\|statement_timeout" backend/` returns nothing, so neither is set anywhere. This is adjacent to pool tuning (a hung connection attempt against Supavisor's ceiling could compound pressure under load) but outside this story's literal scope (pool *size*, not connection *timeout* behaviour). Worth a follow-up review if connection-related latency ever becomes a live concern; not treated as a gap in this story's own AC.

## 5. Sign-off

**Backend Engineering Patterns Owner (agent-mediated, §5.3):** Approved — 2026-08-21. All findings independently verified: no application-level connection pool exists (raw psycopg2.connect() per request; sqlalchemy dependency unused); Supavisor's externally-managed ~20-connection ceiling is the real pooling layer, confirmed via arc5_backend_architecture_review.md §2.3; no connection-exhaustion incident found across 4+ months of api_performance_baseline.md history since Supavisor's 2026-04-16 enablement. Hold recommendation confirmed sound.
