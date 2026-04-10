Owner: Head of Engineering
Class: Working Document (Class 3)
Status: Active
Last Updated: 2026-04-06

---

# Delegation Log — Cycle 2026-04-05__release-v2.5

This log records items delegated to human engineers during this sprint cycle. Each entry includes the delegation target, unblock criteria, and escalation path.

---

## DEL-01 — ST-06: Investigate high external baseline latency on DB-backed endpoints

**Story:** ST-06
**EPIC:** EPIC-02
**GitHub Issue:** #191
**Delegated to:** Head of Engineering
**Delegated at:** 2026-04-06
**Classification:** delegated_backend

**Context:**
All DB-backed FastAPI endpoints show p50 response times of 1.2–6.0s from external clients, which is consistent with Render free tier cold starts and Supabase connection overhead. Two outlier endpoints are materially worse than their peers:

- `GET /portfolio` — p50 ≈ 5,979ms
- `GET /notifications/preferences` — p50 ≈ 4,631ms

These outliers are 3–5× slower than comparable DB-backed endpoints (e.g. `GET /positions`, `GET /cash/summary`).

**Deliverables required:**
1. Root cause of `GET /portfolio` outlier latency identified and documented
2. Root cause of `GET /notifications/preferences` outlier latency identified and documented
3. Either:
   - A fix applied that brings each outlier within 2× of peer endpoint latency; OR
   - A documented architectural constraint explaining why optimisation is not feasible on free tier
4. Supabase connection pooling options evaluated (PgBouncer, SQLAlchemy pool size/overflow settings for Render free tier)
5. Findings filed at `docs/ops/api_performance_baseline.md` (update the existing document)

**Unblock criteria:**
All five deliverables above completed; `docs/ops/api_performance_baseline.md` updated; findings communicated to engine for DoQ review.

**Escalation path:**
If the Head of Engineering determines that the outlier latency is caused by an architectural constraint (Render free tier, Supabase free tier) rather than optimisable code, document this explicitly in `api_performance_baseline.md` and mark ST-06 as `done` with the constraint recorded as a known limitation.

**Notes:**
- Investigation only — implementation fixes are in scope only if they address the latency outliers identified. Broader performance work is deferred.
- `GET /notifications/preferences` may not yet be fully implemented; check router first.
- Pooling options: SQLAlchemy `pool_size` and `max_overflow` in `database.py`; PgBouncer is a Render add-on (not available on free tier) — document this if confirmed.

---
