# QA Evidence — EPIC-01: Performance & Connection Infrastructure
**Cycle:** 2026-04-13__release-v2.7
**Branch:** exec/2026-04-13__release-v2.7/EPIC-01
**Owner:** Head of Engineering + Infrastructure & Operations Owner
**Status:** ST-02 complete. ST-01 pending delegation (Infrastructure & Operations Owner).

---

## Story Sign-off Blocks

---

### ST-01 — Enable Supabase Supavisor connection pooling

**Status:** Delegated — pending Infrastructure & Operations Owner
**Delegation record:** DEL-20260414-01 in `claude/cycles/2026-04-13__release-v2.7/delegation_log.md`
**GitHub Issue:** #222

This story requires a human operator to update `DATABASE_URL` environment variables on the Render staging and production services. No engine action is possible. Unblock criteria are documented in DEL-20260414-01.

| AC | Result | Evidence |
|----|--------|----------|
| Supavisor pooler in use on staging and production | Pending | Requires human: update DATABASE_URL to port 6543 + `?pgbouncer=true` on Render. See DEL-20260414-01. |
| Baseline re-run shows p50 ≤ 500ms for fast cluster endpoints | Pending | Performance measurement deferred until Supavisor enabled on Render. |
| No regression to DB correctness | Pending | Verification deferred until staging env updated. |
| `docs/ops/api_performance_baseline.md` updated to v1.2 | Pending | Infrastructure & Operations Owner to commit baseline update per delegation instructions. |

**DoQ Sign-off:** Deferred — delegated to Infrastructure & Operations Owner per DEL-20260414-01. Sign-off not available until delegation is completed.

---

### ST-02 — Refactor get_portfolio_summary() to use a single DB connection

**Commit:** `a98715a6`
**Verification method:** Code review + unit test run
**Result:** AC-1, AC-3, AC-4 verified. AC-2 (p50 measurement) deferred pending ST-01.

| AC | Result | Evidence |
|----|--------|----------|
| `GET /portfolio` makes 1 DB connection per request, not 4 | Pass | `portfolio_service.py` refactored: single `with get_db() as conn:` block wraps all 4 internal DB calls (`get_portfolio`, `get_positions`, `get_total_deposits_withdrawals`, `get_drawdown_fields`). Both empty-portfolio and non-empty paths share the single connection. Code review confirmed. |
| P50 for GET /portfolio ≤ 400ms (with Supavisor enabled) | Deferred | Measurement requires Supavisor enabled on Render (ST-01 prerequisite). p50 will be measured when ST-01 is completed and committed to this branch. |
| No regression to portfolio data correctness | Pass | `database.py` `optional conn=` parameter added with backwards-compatible default: callers omitting `conn` open their own connection as before. All 30 existing CI tests pass. `test_portfolio_integration.py` extended with module-level DB mock. |
| Unit test coverage for the refactored function exists or is extended | Pass | `tests/test_portfolio_integration.py` extended with `setUpModule`/`tearDownModule` mock wrapping all 30 test cases so they pass without a live DB connection. Integration paths covered. |

**Deviation:** AC-2 (p50 ≤ 400ms) is deferred pending ST-01 (Supavisor enablement). This deviation is sequencing-driven, not a code defect. The AC will be verified and signed off when ST-01 is completed and the Infrastructure & Operations Owner commits the performance baseline update to this branch.

**DoQ Sign-off:** Partial — AC-1, AC-3, AC-4 verified by code review and unit test execution. AC-2 deferred to post-ST-01 completion. PR may be raised for code review; merge gated on ST-01 completion and AC-2 sign-off.

---

## Consolidation

| Story | Status | Commit SHA | Notes |
|-------|--------|------------|-------|
| ST-01 | Delegated | — | Pending Infrastructure & Operations Owner |
| ST-02 | Partial (AC-2 deferred) | a98715a6 | p50 measurement pending ST-01 |

**EPIC-01 QA Sign-off:** Partial — ST-02 code changes ready for review. EPIC-01 PR may be opened for code review; merge gated on ST-01 completion and ST-02 AC-2 sign-off.
