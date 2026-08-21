Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-21

## Consolidation Block

**EPIC:** EPIC-02 — Live Risk-Data Integrity (Stop Invariant Audit & Setup Classification)
**Cycle:** 2026-08-21__release-v9.0
**Sprint goal:** Close out the correctness and data-integrity follow-through surfaced directly by v8.9's own PR-review process, while hardening operational resilience (deploy-path and staging safeguards) and expanding QA and cost/capacity hygiene coverage.
**Test scenarios used:** `tests/test_ensure_trade_plans_table_memoization.py`, `tests/test_schema_rollback_verification.py`, `tests/e2e/what-if-sizing-preview.spec.js`, `tests/e2e/trade-plan.spec.js`, `tests/e2e/position-stop-currency-basis.spec.js`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-06 | `backend/services/position_service.py` | Code-read investigation narrowed the work to a verification-first runbook: `analyze_positions()` already runs nightly (`daily-snapshot.yml`) and applies the fixed breakeven-floor logic (commit `b410cfa3c`) — a live-DB query is needed to confirm 0 non-compliant rows exist, not assumed. Full runbook documented in the delegation record. | Open positions audited against the breakeven-floor invariant; any violations backfilled | **Blocked (delegated)** — requires live production database access this sandbox does not have; correcting real financial data is also a high-consequence action correctly reserved for a human operator regardless of access | Delegated via `DEL-20260821-02` to Backend Engineering Patterns Owner (+ Infrastructure & Operations Owner for DB access) |
| ST-07 | — | Requires a Product Owner decision (`BLG-FEAT-93`) on how to distinguish "explicitly Other" from "never classified" `setup_type` values before any implementation can proceed | Product Owner decision recorded; if implemented, `win_rate_by_setup_type` query logic updated | **Blocked (escalated)** — genuinely a product/analytics-precision tradeoff decision, not an engineering task | Escalated via `ESC-EXEC-20260821-02` |
| ST-08 | `tests/test_ensure_trade_plans_table_memoization.py` | Added `threading.Lock()` around `ensure_trade_plans_table()`'s memoization flag, split into a check-and-lock wrapper plus a locked inner function. Added a concurrency regression test using `threading.Barrier` to prove the DDL block runs exactly once under concurrent first-callers. | Memoization flag protected by a lock; concurrent-first-call regression test added; full suite re-verified | Pass | None |
| ST-09 | `tests/test_schema_rollback_verification.py`; `docs/ops/database_migration_governance.md` | Added rollback-verification tests for the 5 most recent schema-changing functions, run against a real local PostgreSQL 18 server installed in this sandbox (not just a Phase-A skip path). | Down-migration rollback verified for the 5 most recent schema migrations | Pass | AC intent adapted to the actual codebase mechanism (inline `ensure_*_table()`/`ensure_*_column()` functions, not the `backend/migrations/*.sql` files `database_migration_governance.md` describes but was never adopted) — documented as an implementation note correcting a stale Supporting Document description, not filed as a spec deviation (nothing implemented diverges from what's actually built) |
| ST-10 | `docs/specs/frontend/pages/trade_plan.md#5d.2`, `#5d.3` | Added an FX Rate override input to `WhatIfSizingPreview.js` for US-market plans, closing the reproducibility gap where the preview's FX assumption wasn't user-visible/overridable. | US-market What-If preview FX rate is visible and overridable; UK-market unaffected; spec updated | Pass | None — corrected a §5d.3 claim during review, verified technically sound against `sizing_service.py` |
| ST-11 | `tests/e2e/position-stop-currency-basis.spec.js` | Added Playwright coverage for a UK-market position's `current_trailing_stop_native` field (genuine UI-level assertion, not backend dict equality). | UK-market trailing-stop-native rendering covered by Playwright | Pass | None — one inherent coverage gap noted (no distinct-wrong-value negative assertion possible for the UK case) but assessed as proportionate for a P3/S story |

**QA test coverage:**
- Scenarios run: all listed test files independently executed in-session (concurrency test with `threading.Barrier`, schema rollback tests against a real local Postgres 18 instance, Playwright tests against a real browser — `what-if-sizing-preview.spec.js` 8/8, `trade-plan.spec.js` 41/41, `position-stop-currency-basis.spec.js` 4/4).
- Regression areas checked: ST-08/ST-09 touch shared DB-initialization code paths (`ensure_trade_plans_table()`, schema-change functions) — verified via full backend suite re-run clean, not just the new targeted tests in isolation.
- Known deviations: two genuine blockers correctly delegated/escalated (ST-06 needs live production DB access plus human authorization for a high-consequence financial-data correction; ST-07 needs a Product Owner analytics-precision tradeoff decision) — neither is an engineering shortfall.

---

## Sign-Off

**Not yet complete.** ST-06 (`DEL-20260821-02`, blocked on live production database access and human authorization for a high-consequence data correction) and ST-07 (`ESC-EXEC-20260821-02`, blocked on Product Owner decision) remain open — per `execution_prompt.md` §3.2 ("An EPIC is `done` (not yet `merged`) when all of its ST items are `done`"), EPIC-02 is not done and the EPIC-level sign-off block below is deferred until both resolve. This file is maintained incrementally per STEP 3.1.C — the per-story table above is current and accurate for ST-08/09/10/11; it does not imply the EPIC as a whole is ready for PR.

**Mixed-Class EPIC Signer Format (to be completed once ST-06/ST-07 resolve):** EPIC-02 contains `autonomous` stories (ST-08, ST-09, ST-10, ST-11) and `delegated_backend`/`delegated_decision` stories (ST-06, ST-07). Individual story sign-offs already on record: ST-10 (Frontend Specifications & UX Documentation Owner, Approved) and ST-11 (Director of Quality, Approved) each independently reviewed by agent-mediated sign-off; ST-08/ST-09 had no explicit sign-off role named in their own AC and were verified via direct test execution (real concurrency test, real local Postgres schema-rollback verification).

- Signed off by: <pending — do not open the EPIC-02 PR until this is completed>
- Date: <pending>
- Comments: <pending>
