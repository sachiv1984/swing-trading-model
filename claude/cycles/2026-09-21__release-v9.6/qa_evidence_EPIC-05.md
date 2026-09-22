Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-22

---

# QA Evidence — EPIC-05: QA & Test Coverage Debt

**EPIC:** EPIC-05 — QA & Test Coverage Debt
**Cycle:** 2026-09-21__release-v9.6
**Sprint goal:** Ship the two build-and-ship product features committed at the 2026-09-19 rebalance — Clone-as-new-plan (`BLG-FEAT-96`) and CSV export for Screener and Watchlist (`BLG-FEAT-97`) — within the full 32-item, 7-EPIC v9.6 scope at the top of confirmed sprint capacity, landing the live-capital trailing-stop formula decision (`BLG-BE-119`) early so the nightly stop-update path can be hardened on a single agreed formula.
**Test scenarios used:** `tests/test_trade_plan_audit_log.py` (ST-21, 6 tests, unchanged behaviour), `tests/test_openapi_drift_gate.py` (ST-20, 9 tests incl. a real mutation check), plus a full backend suite re-run (1694 passed / 3 skipped / 7 pre-existing unrelated failures)

**Note:** This file is being built incrementally as EPIC-05 stories complete (STEP 3.1.C/3.1.A pattern) — not all stories in the EPIC are done yet. The Evidence Table below will be completed at EPIC-05 close (STEP 3.2.A).

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-18 | `docs/testing/quarterly_playwright_staging_reseed_procedure.md` | AC-01 (cadence/procedure) delivered. Documented an architecture finding that needed disclosure rather than silent reinterpretation: the existing Playwright suite is entirely mock-based (`page.route()` interception, no live backend/DB dependency by design — confirmed by reading `playwright.config.js`'s own `webServer`/`use` blocks), so "a fresh staging seed" does not literally apply to it. Proposed a two-part redefinition (Part 1: Playwright re-run on a fresh CI build; Part 2: Phase-B backend suite against a freshly reset staging seed), routed to Director of Quality via `DEL-20260921-07`. **Director of Quality triggered Part 1 directly** — run [`35729627868`](https://github.com/sachiv1984/swing-trading-model/actions/runs/35729627868), all 8 E2E shards + Visual Snapshots green | AC-01 Cadence and seed procedure documented — done. AC-02 First quarterly run completed with results recorded — **partially done**: Part 1 (Playwright, fresh CI build) completed with real evidence, recorded in the procedure doc's Run Log. Part 2 (Phase-B backend suite, freshly reset staging) still outstanding — destructive step, not triggered without a further explicit human-observed decision | Pending DoQ (Part 2) | DEL-20260921-07 |
| ST-19 | `claude/system/templates/qa_evidence_template.md#Flaky-Test Disposition Addendum` | New Flaky-Test Disposition Addendum section (v1.15→v1.16): retry/quarantine/fix-now decision framework for DoQ sign-off, cross-referencing the shipped quarantine mechanism (`docs/testing/flaky_test_quarantine_process.md`, `BLG-QA-117`) and distinguishing it from `BLG-QA-75`'s separate, still gate-conditional item | AC-01 Addendum added to the DoQ checklist — done. AC-02 Cross-reference confirmed correct against the existing quarantine item — done, both source documents read directly rather than assumed | Pass | None |
| ST-20 | `scripts/check_openapi_drift.py`; `tests/test_openapi_drift_gate.py`; `.github/workflows/openapi-drift.yml` | Extracted the OpenAPI Drift Detection gate's inline CI heredoc logic into an importable script (behaviourally identical, verified against the real repo tree pre/post); added a deliberate-drift fixture (2 directions) and a compliant-case fixture (9 tests total) | AC-01 Both fixtures exist and pass in CI — done. AC-02 A deliberate revert of the gate's logic confirmed to fail the fixture — done via a real mutation on `compute_drift()` (3 tests genuinely failed, then restored and re-confirmed green) | Pass | None |
| ST-21 | `tests/test_trade_plan_audit_log.py`; `tests/test_position_audit_log.py` (existing isolated-copy pattern followed) | Replaced the permanent, unrestored `sys.modules.pop("database", None); import database` at module level with the same isolated-copy `importlib.util.spec_from_file_location` pattern `test_position_audit_log.py` already uses — never touches the shared `sys.modules["database"]` slot, so there is nothing to leak or restore | AC-01 File no longer mutates the shared `sys.modules["database"]` entry — confirmed via a manual reordering canary (see Deviations). AC-02 Full backend suite still passes; manual reordering check confirms no leakage remains — confirmed (1685 passed, 3 skipped, 7 pre-existing unrelated `test_schema*.py` failures). AC-03 Any other file with the same unrestored pattern fixed in the same commit — **partially met**, see DEV-EPIC05-ST21-01 | Pass_with_deviation | DEV-EPIC05-ST21-01 |

**QA test coverage:**
- Scenarios run: `tests/test_trade_plan_audit_log.py` (6/6, isolated run); full backend suite (`backend/.venv/bin/python3 -m pytest tests/`) — 1685 passed, 3 skipped, 7 failed (all 7 pre-existing `test_schema*.py` live-staging-DB-permission failures, confirmed present on `main` before this change, already documented as unrelated by ST-12/ST-13 this same cycle); a throwaway reordering canary (scratchpad only, not committed) confirming `sys.modules["database"]` remains the `conftest.py` stub after `test_trade_plan_audit_log.py`'s own tests run.
- Regression areas checked: `test_trade_plan_audit_log.py`'s own 6 tests (unchanged assertions/behaviour, only the import mechanism changed); full backend suite for any incidental leakage from the fix itself.
- Known deviations: DEV-EPIC05-ST21-01 (P3, AC-03 partially met — see below).

## Deviations

### DEV-EPIC05-ST21-01
**Priority:** P3
**Story:** ST-21
**AC:** AC-03 — "Any other file found with the same unrestored pattern is fixed in the same commit."
**Expected:** Every test file in `tests/` sharing `test_trade_plan_audit_log.py`'s exact hazard (a permanent, module-level `sys.modules.pop("database", None)` swap with no restore) is converted to a safe pattern in the same commit as the named file's own fix.
**Actual:** A grep audit (performed per the story's own scope instruction) found approximately 29 other test files matching the literal `sys.modules.pop("database", None)` text. They are not structurally uniform, so a single mechanical fix does not safely apply to all of them:
- A subset are simple, direct `database.X()`-call files structurally identical to `test_trade_plan_audit_log.py` — convertible to the same isolated-copy fix with low risk.
- Several (`test_api_contracts.py`, `test_backtest_rule_runs_pagination.py`, `test_main_500_no_raw_exception_text.py`, `test_idempotency_endpoints.py`, `test_job_registration_screener_risk_off.py`, `test_rate_limit_endpoints.py`, `test_router_error_envelope_conformance.py`, `test_st04_implicit_200_error_paths_fixed.py`, `test_tag_performance_ensure_table_call.py`, `test_trade_plan_setup_type_default.py`, `test_cost_monitoring.py`, and others) import FastAPI's `TestClient`/`main.app`, whose router-level `from database import X` bindings resolve against whatever is in `sys.modules["database"]` at `main` import time — the isolated-copy pattern does **not** apply to these; they would need a different, restore-based fix (e.g. a module-scoped teardown re-installing the `conftest.py` stub) instead.
- At least one (`test_ensure_trade_plans_table_memoization.py`) already re-acquires the real module fresh per-test with its own documented rationale for why that specific design is order-independent within itself, even though it still leaves the real module installed in the shared slot after its own tests run.
- Several pop additional modules in the same call (e.g. `test_rebalance_exit_signal_numpy_regression.py` also pops `utils.formatting`), widening the blast radius of any fix beyond `database` alone.

Fully and safely fixing all ~29 files in the same commit would require individual per-file review to select the correct fix strategy (isolated-copy vs. restore-based) and to verify no FastAPI import-binding regression for the `TestClient`-dependent subset — a materially larger, higher-risk piece of work than this story's XS (<1h) effort estimate anticipated. Rather than rush a mass edit across the test suite without that review, this deviation discloses the finding and routes the remaining work to a dedicated follow-up.
**Impact:** Low — this is a latent test-isolation risk (files "not yet triggered," per the source backlog item's own problem statement), not a currently-failing test or a production defect. No user-facing or live-capital impact. The specific file this story was filed to fix (`test_trade_plan_audit_log.py`) is fully resolved.
**Backlog action:** BLG-QA-190 filed (P3) — carries the full file-by-file audit (the categorised list above) as the starting point for the follow-up fix.
**Notes:** AC-01 and AC-02 are fully met — only AC-03's "any other file" clause is partially met (the audit was completed as scoped; the fix was not, for the reasons above). Per `delivery_verification_prompt.md` §2.1's `Pass_with_deviation` definition, this is `Pass_with_deviation`, not `Fail`: the gap is disclosed transparently (not fabricated or silently omitted) and a confirmed backlog item tracks it.

---
