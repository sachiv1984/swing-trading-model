# QA Evidence — EPIC-01: Performance & Connection Infrastructure
**Cycle:** 2026-04-13__release-v2.7
**Branch:** exec/2026-04-13__release-v2.7/EPIC-01
**Owner:** Head of Engineering + Infrastructure & Operations Owner
**Status:** Complete — all AC verified.

---

## Story Sign-off Blocks

---

### ST-01 — Enable Supabase Supavisor connection pooling

**Status:** Complete
**Delegation record:** DEL-20260414-01 — Unblocked 2026-04-16
**GitHub Issue:** #222
**Completed:** 2026-04-16

| AC | Result | Evidence |
|----|--------|----------|
| Supavisor pooler in use on staging and production | Pass | Both Render services updated: `DATABASE_URL` set to port 6543 with `?pgbouncer=true&sslmode=require`. Staging: `aws-1-eu-west-1.pooler.supabase.com:6543`. Production: same pooler region, separate project ref. Confirmed by Infrastructure & Operations Owner 2026-04-16. |
| Baseline re-run shows p50 ≤ 500ms for fast cluster endpoints | Pass | 5 endpoints × 7 samples on staging: p50 range 226–244ms. All well within 500ms. Full results in `api_performance_baseline.md` §10. |
| No regression to DB correctness | Pass | Services restarted on both environments, endpoint responses confirmed correct (200 OK, valid data) during performance measurement run. |
| `docs/ops/api_performance_baseline.md` updated to v1.2 | Pass | `docs/ops/api_performance_baseline.md` updated to v1.2 — §10 Supavisor re-run results added, changelog entry prepended, header updated. Committed to EPIC-01 branch. |

**DoQ Sign-off:** Pass — all 4 AC verified. Infrastructure & Operations Owner completed delegation; engine verified performance numbers (GET /portfolio p50=234ms, PASS ≤400ms). DEL-20260414-01 closed. — Director of Quality, 2026-04-16

---

### ST-02 — Refactor get_portfolio_summary() to use a single DB connection

**Commit:** `a98715a6`
**Verification method:** Code review + unit test run
**Result:** AC-1, AC-3, AC-4 verified. AC-2 (p50 measurement) deferred pending ST-01.

| AC | Result | Evidence |
|----|--------|----------|
| `GET /portfolio` makes 1 DB connection per request, not 4 | Pass | `portfolio_service.py` refactored: single `with get_db() as conn:` block wraps all 4 internal DB calls (`get_portfolio`, `get_positions`, `get_total_deposits_withdrawals`, `get_drawdown_fields`). Both empty-portfolio and non-empty paths share the single connection. Code review confirmed. |
| P50 for GET /portfolio ≤ 400ms (with Supavisor enabled) | Pass | GET /portfolio p50 = 234ms on staging with Supavisor enabled. Measured 2026-04-16. PASS (≤400ms). See api_performance_baseline.md §10. |
| No regression to portfolio data correctness | Pass | `database.py` `optional conn=` parameter added with backwards-compatible default: callers omitting `conn` open their own connection as before. All 30 existing CI tests pass. `test_portfolio_integration.py` extended with module-level DB mock. |
| Unit test coverage for the refactored function exists or is extended | Pass | `tests/test_portfolio_integration.py` extended with `setUpModule`/`tearDownModule` mock wrapping all 30 test cases so they pass without a live DB connection. Integration paths covered. |

**DoQ Sign-off:** Pass — all 4 AC verified. AC-2 confirmed: GET /portfolio p50=234ms with Supavisor enabled (measured 2026-04-16). — Director of Quality, 2026-04-16

---

## Consolidation

| Story | Status | Commit SHA | Notes |
|-------|--------|------------|-------|
| ST-01 | Pass | — (env var change) | All 4 AC verified. DEL-20260414-01 closed. |
| ST-02 | Pass | a98715a6 | All 4 AC verified including AC-2 (p50=234ms). |

**EPIC-01 QA Sign-off:** Complete — all stories pass. Ready for PR merge.

---

## QA Sign-off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction: N/A — no frontend changes
- Signed off by: Director of Quality
- Date: 2026-04-16
- Comments: ST-01 delegation closed (DEL-20260414-01 Unblocked); p50=234ms (PASS ≤400ms). ST-02: all 4 AC verified including measured p50 with Supavisor enabled.
