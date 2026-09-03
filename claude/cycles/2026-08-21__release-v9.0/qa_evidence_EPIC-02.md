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
| ST-06 | `backend/services/position_service.py`; `docs/ops/breakeven_floor_stop_audit_2026-09-03.md` | Code-read investigation narrowed the work to a verification-first runbook: `analyze_positions()` already runs nightly (`daily-snapshot.yml`) and applies the fixed breakeven-floor logic (commit `b410cfa3c`) — a live-DB query was needed to confirm 0 non-compliant rows exist, not assumed. Product Owner ran the Step 1 audit query directly against production (live DB access this sandbox lacks): 0 rows returned. | Open positions audited against the breakeven-floor invariant; any violations backfilled | Pass — 0 open, currently-profitable positions found with `current_stop < entry_price`; correction (Step 2) and re-verification (Step 3) not applicable | Delegated via `DEL-20260821-02` to Backend Engineering Patterns Owner (+ Infrastructure & Operations Owner for DB access); resolved 2026-09-03, DEL-20260821-02 given its final resolution addendum; closes deferred `BLG-BE-102`/ST-01 (v8.9) AC |
| ST-07 | `docs/product/decisions/setup-type-other-conflation-decision--2026-08-21.md`; `docs/specs/api_contracts/trade_plan_endpoints.md` | Product Owner decision (`BLG-FEAT-93`, resolves `ESC-EXEC-20260821-02`): accept the `setup_type="Other"` conflation as-is — no new distinguishing field/enum, since `win_rate_by_setup_type` is a future, unbuilt SI-02 query still far from its own trigger gate. `PUT /trade-plans/{id}` explicitly not extended with `POST`'s null→"Other" default. | Product Owner decision recorded; if implemented, `win_rate_by_setup_type` query logic updated | Pass | None — 2 new regression tests (`TestSetupTypePutDoesNotDefault`) lock in the accepted behaviour; `trade_plan_endpoints.md` v0.13→v0.14 |
| ST-08 | `tests/test_ensure_trade_plans_table_memoization.py` | Added `threading.Lock()` around `ensure_trade_plans_table()`'s memoization flag, split into a check-and-lock wrapper plus a locked inner function. Added a concurrency regression test using `threading.Barrier` to prove the DDL block runs exactly once under concurrent first-callers. | Memoization flag protected by a lock; concurrent-first-call regression test added; full suite re-verified | Pass | None |
| ST-09 | `tests/test_schema_rollback_verification.py`; `docs/ops/database_migration_governance.md` | Added rollback-verification tests for the 5 most recent schema-changing functions, run against a real local PostgreSQL 18 server installed in this sandbox (not just a Phase-A skip path). | Down-migration rollback verified for the 5 most recent schema migrations | Pass | AC intent adapted to the actual codebase mechanism (inline `ensure_*_table()`/`ensure_*_column()` functions, not the `backend/migrations/*.sql` files `database_migration_governance.md` describes but was never adopted) — documented as an implementation note correcting a stale Supporting Document description, not filed as a spec deviation (nothing implemented diverges from what's actually built) |
| ST-10 | `docs/specs/frontend/pages/trade_plan.md#5d.2`, `#5d.3` | Added an FX Rate override input to `WhatIfSizingPreview.js` for US-market plans, closing the reproducibility gap where the preview's FX assumption wasn't user-visible/overridable. | US-market What-If preview FX rate is visible and overridable; UK-market unaffected; spec updated | Pass | None — corrected a §5d.3 claim during review, verified technically sound against `sizing_service.py` |
| ST-11 | `tests/e2e/position-stop-currency-basis.spec.js` | Added Playwright coverage for a UK-market position's `current_trailing_stop_native` field (genuine UI-level assertion, not backend dict equality). | UK-market trailing-stop-native rendering covered by Playwright | Pass | None — one inherent coverage gap noted (no distinct-wrong-value negative assertion possible for the UK case) but assessed as proportionate for a P3/S story |

**QA test coverage:**
- Scenarios run: all listed test files independently executed in-session (concurrency test with `threading.Barrier`, schema rollback tests against a real local Postgres 18 instance, Playwright tests against a real browser — `what-if-sizing-preview.spec.js` 8/8, `trade-plan.spec.js` 41/41, `position-stop-currency-basis.spec.js` 4/4).
- Regression areas checked: ST-08/ST-09 touch shared DB-initialization code paths (`ensure_trade_plans_table()`, schema-change functions) — verified via full backend suite re-run clean, not just the new targeted tests in isolation.
- Known deviations: ST-06 was a genuine, correctly-delegated blocker (needed live production DB access plus human authorization for a high-consequence financial-data correction) — not an engineering shortfall; resolved 2026-09-03 with a clean (0-row) audit result, requiring no correction. ST-07's Product Owner escalation (`ESC-EXEC-20260821-02`) has also been resolved — see its own row above.

---

## Sign-Off

**Mixed-Class EPIC Signer Format:** EPIC-02 contains `autonomous` stories (ST-08, ST-09, ST-10, ST-11) and `delegated_backend`/`delegated_decision` stories (ST-06, ST-07). All 6 stories are `done`.

Individual story sign-offs on record:
- ST-06: Backend Engineering Patterns Owner agent-mediated sign-off + Product Owner (human, ran the live audit query), Approved 2026-09-03 (0 rows found, correction not required — see `execution_state.json` `sign_off_record` and `docs/ops/breakeven_floor_stop_audit_2026-09-03.md`)
- ST-07: Product Owner agent-mediated sign-off, Approved 2026-08-21 (accept-as-is decision, resolves `ESC-EXEC-20260821-02` — see `execution_state.json` `sign_off_record`)
- ST-08: verified via direct test execution (real concurrency test, `threading.Barrier`) — no explicit sign-off role named in the story's own AC
- ST-09: verified via direct test execution (real local Postgres 18 schema-rollback verification) — no explicit sign-off role named in the story's own AC
- ST-10: Frontend Specifications & UX Documentation Owner agent-mediated sign-off, Approved 2026-08-21 (1 pass, no findings blocking)
- ST-11: Director of Quality agent-mediated sign-off, Approved 2026-08-21 (1 pass, no findings blocking; one inherent, proportionate coverage gap noted)

```
Director of Quality

EPIC-02 consolidation reviewed. All 6 stories done, acceptance criteria
verified, spec_references populated. No P0/P1 deviations. ST-06's
delegation was a genuine live-data-access blocker, not an engineering
shortfall, and resolved cleanly (0-row audit, no correction needed) --
closes the deferred BLG-BE-102/ST-01 (v8.9) AC that originated it.
ST-07's Product Owner escalation independently resolved. EPIC-02 ready
for PR.

Signed: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
Date: 2026-09-03
```
