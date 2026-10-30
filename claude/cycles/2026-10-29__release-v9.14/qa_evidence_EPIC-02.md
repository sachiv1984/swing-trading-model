Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-30

# QA Evidence — EPIC-02 — Sizing, Exit & Position Correctness

**EPIC:** EPIC-02 — Sizing, Exit & Position Correctness
**Cycle:** 2026-10-29__release-v9.14
**Sprint goal:** Restore the production frontend deploy (BLG-OPS-193, P1) so shipped UI reaches GitHub Pages again, and stop a Yahoo Finance outage from silently giving a risk-on regime and a frozen 1.27 FX rate while System Status reports healthy. Also fix US position sizing's FX inversion (BLG-BE-190) and ship v9.14's AI output safety, reporting, test, operations and governance items.
**Test scenarios used:** `tests/test_sizing_fx_and_cash.py`, `tests/test_strategy_invariants_property.py`, `tests/test_golden_outputs.py`, `tests/test_strategy_version_registry.py`, `tests/test_exit_position_errors.py`, `tests/test_portfolio_null_fill_price_pnl.py`, `tests/e2e/monitor-grace-aware-suggestions.spec.js`, `tests/e2e/monitor-exit-queue.spec.js`, `tests/e2e/position-review-cadence-nudge.spec.js`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-09 | `strategy_rules.md` §4.1.3, §4.1.5; `portfolio_endpoints.md` §POST /portfolio/size | `size_position()` divides the US stop distance by FX: `RawShares = RiskAmount × FX / StopDistance` (`bde25685`). `strategy_rules.md` v1.21 states the US formula in §4.1.3 and resolves §4.1.5's Known Deviation; `STRATEGY_VERSION_REGISTRY` 1.21 (behavioural). | AC 1: owner confirmation dated 2026-10-30 (`ESC-EXEC-20261030-01`, in-session). AC 2: worked test, £100 / $10 / 1.27 → 12.7 shares (`test_sizing_fx_and_cash.py::TestUsShareCalculation`). AC 3: property oracle corrected; `test_old_inverted_fx_formula_falsifies_the_property` shows the old formula's 7.874 fails it. AC 4: §4.1.5 closed, §4.1.3 states the US formula, Change Log row, registry entry, §15 re-run 0 actionable. AC 5: no other inversion (Trade Entry risk display, What-If preview, heat impact, estimated cost, `MaxAffordableShares` all divide); `portfolio_endpoints.md` 2.14.1 examples recomputed; golden PS-04/PS-05 and mutmut pilot US cases corrected. | Pass | None (closes the v1.19 Known Deviation) |
| ST-10 | `position_endpoints.md` §POST /positions/{position_id}/exit | The endpoint maps `exit_position`'s `ValueError`s: missing position or portfolio → 404, everything else → 400, each with `detail` (`41c79733`). Contract 2.19.1 lists every status, detail and condition. | AC 1: each `ValueError` maps to its documented 404 or 400 with `detail`. AC 2: `test_exit_position_errors.py`, one test per case (8), through the real service with reads mocked; all 8 fail against the old endpoint. | Pass | None |
| ST-11 | `positions.md` §Monitor Suggestions; `monitor-grace-aware-suggestions/decision_record.md` | `MonitorModal` derives suggestions from `getExitCondition()`; risk-off from `risk_off_exit` (precedence); in-grace breach holds with "In grace: stop not enforced"; `marketRegimes` prop removed; "Stop price hit" note names trailing stop and grace (`3118e0b7`). | AC 1: uses `getExitCondition()`. AC 2: in-grace breach not suggested (Playwright SC-MGS-01). AC 3: post-grace breach and risk-off still suggested, risk-off wins when both (SC-MGS-02, SC-MGS-03). | Pass | None |
| ST-12 | `portfolio_endpoints.md` §GET /portfolio | Code fix pre-met on `main` (v9.12 ST-13, `cc7774e9`: `fill_price or entry_price × fx_rate`). Added the AC's unit test (`262a0376`). | AC: US position, `fill_price` None, live price → the row uses `entry_price` (`test_portfolio_null_fill_price_pnl.py`: pnl £76.92, pnl_pct 10.0). Fails with the original `TypeError` against the old line. | Pass | None |
| ST-13 | `data_model_positions_dictionary.md` §3.3; `data_model.md` §2; `metrics_definitions.md` §Position Risk | Dictionary v0.6 adds `user_fill_price`; `metrics_definitions.md` 1.33.1 corrects the Position Risk data source (`57bccb1d`). | AC 1: dictionary and `data_model.md` §2 agree with `add_position()` for `entry_price`, `fill_price`, `user_fill_price`, `total_cost` and `pnl`. AC 2: repo-wide search; the one native-currency description of `positions.entry_price` (`metrics_definitions.md`) is corrected. Wording-only: verified by document review against `add_position()` (no rendered output). | Pass | None. Out-of-scope finding filed: `BLG-BE-198` |
| ST-14 | `positions.md` §Last Reviewed Column; `last-reviewed-ended-grace/decision_record.md` | Option (a): shared `src/lib/reviewCadence.js` suppresses the flag for stored GRACE with `grace_days_remaining ≤ 2`, or null with `holding_days ≥ 10`; used by the table and the grid (`f62bda83`). | AC 1: predicate handles the ended-grace case. AC 2: Playwright SC-RCN-09 (stored GRACE, null, holding days 11, review 20d ago: text renders without amber, table and grid; fails on the old predicate) and SC-RCN-10 (LOSING is flagged). | Pass | None |

**QA test coverage:**
- Scenarios run: full backend suite locally (3032 passed, 30 skipped, before the registry update; affected suites re-run after); CI per story SHA: CI Pytest Suite success on `bde25685` (41027565430), `41c79733` (41027810330), `262a0376` (41027905652), `3118e0b7` (41029266298), `f62bda83` (41030029440). Playwright E2E Acceptance Tests success on `3118e0b7` (41029266343); on `f62bda83` (41030029516) pending at writing — must be confirmed before sign-off. Locally: monitor specs 7/7, review-cadence spec 10/10.
- Regression areas checked: position sizing (UK unchanged, golden vectors, property tests, concentration/heat/signal sizing suites), exit endpoint (exit-reason validation suite), GET /portfolio P&L, Daily Position Monitor exit queue (SC-MEQ-01..04), Positions Last Reviewed column (SC-RCN-01..08), strategy version registry.
- Known deviations: None found — all stories' deviation checks completed with nothing to file.

**Frontend testing gate (CLAUDE.md §2):** every observable AC has Playwright coverage. ST-11 AC 2/3: `monitor-grace-aware-suggestions.spec.js` SC-MGS-01..03, observed passing in real CI run 41029266343. ST-14 AC 2: `position-review-cadence-nudge.spec.js` SC-RCN-09/10, CI run 41030029516 (confirm before sign-off). ST-13 is wording-only (FI-P3-02). No AC is "code review only".

**Story-level authority sign-offs:** ST-09 — Strategy Rules & System Intent Owner ruling `ESC-EXEC-20261030-01`, given in-session by the user acting in that role, 2026-10-30 (cleared).

## Standard Sign-Off Block

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object
- [ ] **Strategy values checked:** ST-09 — §4.1.2 risk basis, §4.1.3 share calculation, §4.1.5 FX, §4.1.6 cash constraint; ST-11 — §6.3 grace (stop not enforced), §8.1 stop-loss trigger, §8.2 risk-off precedence; ST-14 — §6.2 grace length (10 calendar days).
- Signed off by:
- Date:
- Comments:
