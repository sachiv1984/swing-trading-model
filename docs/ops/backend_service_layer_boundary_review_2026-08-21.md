**Owner:** Backend Engineering Patterns Owner; Head of Engineering
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-08-21
**Story:** ST-23 (BLG-BE-56, EPIC-05, v9.0)

# Backend Service-Layer Boundary Review

## 1. Purpose

`BLG-BE-56`: recent `BLG-BE-*` items have touched router/service/database layers; no recent review confirmed the layering boundary — `router → service → database`, per `claude/agents/backend_engineering_patterns_owner.md` §"Routers must be thin. No business logic, no SQL, no calculations in a router" — still holds cleanly. This reviews the current state and corrects what's found, in proportion to what a single review story can safely fix.

## 2. Method

Grepped every file in `backend/routers/*.py` for signs of business logic or SQL execution happening directly in the router layer (rather than delegated to `backend/services/*.py` or `backend/database.py`):

```
grep -l "import psycopg2\|from sqlalchemy\|import sqlalchemy\|cursor.execute\|conn.execute" backend/routers/*.py
```

3 of 28 router files flagged: `analytics.py`, `digest.py`, `ai.py`. All other routers correctly delegate to the service/database layers with no direct SQL.

## 3. Findings

| File | `cursor.execute()` call sites | First introduced | Assessment |
|------|-------------------------------|-------------------|-------------|
| `backend/routers/analytics.py` | ~25 | 2026-02-16 (3 days before the layered-architecture pattern doc itself, 2026-02-19) | Pre-existing debt predating the standard's adoption, not "recent drift" — large (spans ~1200+ lines), not safely fixable within this review story |
| `backend/routers/digest.py` | 7 | 2026-04-01 (after the pattern was established) | Genuine violation, but still too large (7 call sites) to safely refactor within an S-effort review alongside `analytics.py`'s larger fix |
| `backend/routers/ai.py` | 2 | 2026-04-18 | Small, bounded, genuine violation — **fixed directly in this story** (§4 below) |

`backend/routers/trade_plans.py` was also checked (13 endpoints, the most of any router) for business-logic-in-router smells — it has a small `_maybe_write_override_event()` helper that orchestrates two `database.py` calls with light error handling. This is a thin orchestration wrapper, not SQL or business logic in the router itself; assessed as acceptable and not requiring correction.

## 4. Correction Applied

`backend/routers/ai.py`'s `POST /ai/journal-summary` handler built and executed raw SQL directly (including dynamic `WHERE`-clause construction for the date-range filter case) instead of delegating to the database layer. Fixed:

- Added `fetch_journal_notes(trade_ids, date_from, date_to)` to `backend/database.py` — SQL only, matching the existing `get_trade_history()`-style convention.
- Updated `backend/routers/ai.py`'s `journal_summary()` handler to call it instead of building/executing SQL inline. Removed the now-unused `from database import get_db` import (replaced with `from database import fetch_journal_notes`).
- No behavioural change — the query logic (both the `trade_ids` branch and the dynamic date-range-filter branch) was moved verbatim, not rewritten.

**Verification:** full backend test suite run (from repo root, per CLAUDE.md §9's required invocation) before and after: **1260 passed, 5 skipped**, no regressions. `tests/test_rate_limit_endpoints.py` and `tests/test_router_error_envelope_conformance.py` (the two files with direct coverage of this endpoint) both pass unchanged.

## 5. Deferred (Filed as Backlog Debt)

`analytics.py` (~25 call sites) and `digest.py` (7 call sites) are genuine, larger violations of the same pattern. Attempting to refactor 32 call sites across two production-critical files (analytics reporting, weekly digest) within a single S-effort (~0.5–2 day) review story carries disproportionate regression risk relative to the story's own scope. Filed as `BLG-BE-110` (`claude/backlog/backlog.md`, L effort ~3-5 days) for a dedicated follow-up story with its own full regression-test pass.

## 6. Sign-Off

```
Backend Engineering Patterns Owner

Layering-boundary review complete. 3 of 28 routers found with direct SQL
execution bypassing the service/database layers. The smallest, most
bounded violation (ai.py, 2 call sites) corrected in this story — moved to
database.fetch_journal_notes(), full backend suite re-verified passing
(1260 passed, 5 skipped, zero regressions). The two larger violations
(analytics.py ~25 sites, digest.py 7 sites) are genuine pre-existing debt,
correctly deferred to a dedicated follow-up story (BLG-BE-110) rather than
risked under this review's own S-effort scope. trade_plans.py's small
orchestration helper reviewed and assessed as acceptable, not a violation.

Signed: Sprint Execution Engine (agent-mediated, Backend Engineering Patterns Owner role — §5.3) — 2026-08-21
```
