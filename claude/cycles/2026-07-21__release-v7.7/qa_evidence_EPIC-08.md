Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-24

# QA Evidence Log — EPIC-08 (v7.7)

## Consolidation Block

**EPIC:** EPIC-08 — numpy-scalar regression coverage for create_rebalance_exit_signal
**Cycle:** 2026-07-21__release-v7.7
**Sprint goal:** Ship the four design-gated Strategy Intelligence & Notification UX items and clear seven ready capacity-fill items to fully utilise this sprint's confirmed capacity.
**Test scenarios used:** tests/test_rebalance_exit_signal_numpy_regression.py (new, 2 scenarios)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-08 | `tests/test_rebalance_exit_signal_numpy_regression.py` | New regression test guarding `create_rebalance_exit_signal` (`backend/database.py`) against the PR #971 defect class. Exercises the REAL `generate_rebalance_exit_signals()` → `decimal_to_float()` → `create_rebalance_exit_signal()` call chain end-to-end with numpy-typed position data, asserting every parameter reaching the mocked psycopg2 cursor is a native Python type. | Automated test added confirming `create_rebalance_exit_signal` safely handles numpy scalar inputs via `decimal_to_float()` upstream; test guards against recurrence of the PR #971 defect class; runs in CI on every PR touching `backend/database.py` | Pass | None |

**QA test coverage:**
- Scenarios run: `test_create_rebalance_exit_signal_direct_call_binds_native_types_when_given_native_args` (baseline sanity), `test_generate_rebalance_exit_signals_end_to_end_with_numpy_position_data` (end-to-end regression, numpy-typed `current_price`/`current_stop`) — both passing standalone and within the full 747-test suite, verified across multiple runs
- Regression areas checked: full backend suite (`backend/.venv/bin/python3 -m pytest tests/ -q` — 747 passed, 2 skipped, no regressions)
- Known deviations filed: None

**Falsifiability verified (non-tautological test):** temporarily disabled `backend/services/signal_service.py`'s `pos = decimal_to_float(pos)` call — the end-to-end test failed with exactly the expected numpy-scalar assertion, confirming the test's guarantee genuinely depends on that upstream conversion rather than passing vacuously. Change reverted cleanly (`git checkout`) before commit.

**Process note (test-isolation bugs found and fixed during implementation):**
1. Initially popped/reimported `sys.modules["services.signal_service"]` (mirroring an established pattern used for `database` elsewhere in this test suite) — this created a second, divergent module object that broke `test_nightly_computations.py`'s RX-02/03/05 tests when both files ran in the same pytest session (that file holds a function reference bound to the original module object). Fixed by leaving `services.signal_service`'s module identity untouched and using `patch.object` instead.
2. Agent-mediated QA & Testing Owner review (§5.3) found the initial `patch.object(signal_service, "decimal_to_float", ...)` line was a no-op, since `generate_rebalance_exit_signals()` re-imports `decimal_to_float` locally from `utils.formatting` on every call (shadowing the module attribute). Fixed by evicting `sys.modules["utils"]`/`["utils.formatting"]`/`["utils.pricing"]` up front instead, guaranteeing the local re-import always resolves to the real implementation regardless of what other test files in the session may have stubbed.

Both fixes are reflected in the final committed test file; full suite re-verified clean after each fix (747 passed, 2 skipped, stable across multiple runs).

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, backend test-only change, no frontend code
- Signed off by: Sprint Execution Engine (agent-mediated, QA & Testing Owner role — §5.3)
- Date: 2026-07-24
- Comments: No frontend-visible change. Agent-mediated review independently re-ran the tests, confirmed the falsifiability check, verified the CI trigger path, and found one non-blocking imprecision (documented above), which was fixed in the same session before this sign-off was recorded. Human Director of Quality review and Product Owner acceptance still required before merge per §5.3 "Always-human gates".
