Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-16

---

## EPIC-02 — Performance & Latency Hardening

**EPIC:** EPIC-02 — Performance & Latency Hardening
**Cycle:** 2026-06-16__release-v5.6
**Sprint goal:** Ship the PT-04 governance gate re-verification, Arc 5 QA completion criteria, and SI-05 UX improvements in Sprint 1; deliver research and portfolio performance optimisations in Sprint 2.
**Test scenarios used:** Derived from spec + AC (no dedicated test file — all stories are infrastructure changes with staging-only latency ACs)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-04 (BLG-OPS-62) | backend/utils/pricing.py | 5-min TTL in-memory cache for `get_live_fx_rate()` — eliminates live HTTP call + 200ms sleep on every `/portfolio/concentration-status` request (root cause identified: external Yahoo Finance HTTP call per request with intentional 200ms rate-limit delay) | AC-01: Root cause identified ✓ (code review) | AC-02: Fix applied ✓ (TTL cache, code review) | AC-03: p95 ≤1,000ms on production — staging-deferred (BLG-OPS-66) | AC-04: I&O Owner sign-off after re-measurement — staging-deferred (BLG-OPS-66) | Pass with notes (AC-03/04 staging-deferred) | None |
| ST-05 (BLG-OPS-63) | backend/routers/red_flag_journal.py | Module-level `_schema_ensured` singleton guard — `ensure_red_flag_events_table()` and `ensure_red_flag_events_severity_column()` now run once per process lifetime instead of on every request (root cause identified: DDL round-trips ~1–2s each, called on every GET /portfolio/red-flag-journal) | AC-01: Root cause identified ✓ (code review) | AC-02: Fix applied ✓ (schema-once guard, code review) | AC-03: p95 ≤1,000ms on production — staging-deferred (BLG-OPS-67) | AC-04: I&O Owner sign-off after re-measurement — staging-deferred (BLG-OPS-67) | Pass with notes (AC-03/04 staging-deferred) | None |
| ST-06 (BLG-OPS-64) | backend/routers/analytics.py | (a) Module-level `_si02_schema_ensured` singleton guard — `ensure_si02_trade_plans_columns()` and `ensure_si02_trade_history_indexes()` now run once per process lifetime; (b) 15-min TTL result cache for drift computation — `_drift_cache` keyed by portfolio_id, expires after 900s. Root cause: DDL on every request + full 90-day trade scan per request | AC-01: Root cause identified ✓ (code review) | AC-02: TTL-based result cache implemented ✓ (code review) | AC-03: p95 ≤1,000ms for cached calls — staging-deferred (BLG-OPS-68) | AC-04: Cache hit rate ≥50% — staging-deferred (BLG-OPS-68) | AC-05: I&O Owner sign-off after re-measurement — staging-deferred (BLG-OPS-68) | Pass with notes (AC-03/04/05 staging-deferred) | None |
| ST-07 (BLG-OPS-22) | backend/routers/research.py; backend/routers/screener.py | (a) Per-ticker 15-min TTL in-memory cache (`_research_cache`) for GET /research/{ticker}; (b) Cache hit/miss logging via Python logger (`[research_cache] HIT/MISS ticker`); (c) Cache invalidated on screener run via lazy import of `invalidate_research_cache()` in screener background task; (d) Gate condition BLG-OPS-13 + p95>3,000ms documented in QA evidence | AC-01: TTL cache implemented ✓ (code review) | AC-02: Cache invalidation on screener run ✓ (code review) | AC-03: Hit/miss logging added ✓ (code review) | AC-04: p95 ≤2,000ms for cached tickers — staging-deferred (BLG-OPS-69) | AC-05: Cache hit rate ≥50% — staging-deferred (BLG-OPS-69) | AC-06: Gate condition (BLG-OPS-13 + p95>3,000ms) verified and documented ✓ (gate cleared 2026-06-11: p95=4,601ms > 3,000ms threshold, confirmed per execution_state.json notes) | Pass with notes (AC-04/05 staging-deferred) | None |

**QA test coverage:**
- Scenarios run: 507 existing backend tests pass (0 new test files for infrastructure cache changes — caching layer is verified by code review; staging-only ACs deferred with backlog items)
- Regression areas checked: All 507 backend tests pass post-change (`python3 -m pytest tests/ -x -q --ignore=tests/e2e` — 507 passed, 2 skipped, 2026-06-16)
- No Playwright E2E tests affected (no frontend-visible changes)
- Known deviations filed: None
- Staging-deferred ACs: ST-04 AC-03/04 (BLG-OPS-66), ST-05 AC-03/04 (BLG-OPS-67), ST-06 AC-03/04/05 (BLG-OPS-68), ST-07 AC-04/05 (BLG-OPS-69)

**Gate verification (ST-07 AC-06):**
- BLG-OPS-13 gate condition: research view p95 > 3,000ms
- Confirmed cleared 2026-06-11: p95=4,601ms measured on production (execution_state.json ST-07 notes)
- Gate condition documented: ST-07 implementation proceeded on cleared gate; TTL cache deployed to bring p95 below threshold

---

## Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓
- [ ] Criterion 2: All AC verifiable by code review alone — ✗ (AC-03/04 for ST-04/05, AC-03/04/05 for ST-06, AC-04/05 for ST-07 are staging-only; production latency re-measurement required)
- [x] Criterion 3: No frontend-visible change — ✓ (all changes are backend Python and utility modules; no React pages or UI components modified)
- [ ] Criterion 4: N/A — autonomous class does not apply (Criterion 2 fails)

Autonomous class does NOT apply. Standard DoQ sign-off with I&O Owner agent-mediated review.

**Infrastructure & Operations Owner sign-off (implementable ACs):**
Root cause analysis (AC-01): confirmed via code review for all 4 stories. External HTTP call (`get_live_fx_rate`) is the concentration-status bottleneck; DDL-on-every-request pattern is the red-flag-journal and behavioural-drift bottleneck; sequential external API calls are the research view bottleneck. All root causes are well-documented in the code change and match the baseline latency measurements.

Fix verification (AC-02 for ST-04/05, AC-01/02/03 for ST-06/07): all fixes confirmed applied by code review. TTL caches use `time.monotonic()` for monotonic clock comparison (not wall-clock). Schema-once guards use process-lifetime module-level flags. Cache invalidation uses lazy import to avoid circular import (screener imports before research in main.py registration order). Implementation is correct.

Staging ACs: deferred with backlog items BLG-OPS-66/67/68/69 filed in backlog.md. All staging-deferred ACs will be verified on production after v5.6 deployment.

- [x] All implementable acceptance criteria verified against spec (code review)
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked (507 tests pass)
- [x] No frontend components modified — URL construction check N/A
- Signed off by: Infrastructure & Operations Owner (agent-mediated, 2026-06-16) + Director of Quality (agent-mediated, 2026-06-16)
- Date: 2026-06-16
- Comments: All implementable ACs (root cause identification + code fix) verified by code review. 4 staging-only ACs (latency re-measurement + cache hit rate on production) deferred to post-deployment with backlog items BLG-OPS-66–69 filed. 507 backend tests pass; no regressions. No frontend changes. No deviations.
