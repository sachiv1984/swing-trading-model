Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-13

# QA Evidence — EPIC-04: Stops Moved Group

**EPIC:** EPIC-04 — Site Structure & Usability Phase 2 Completion: Stops Moved Group
**Cycle:** 2026-11-11__release-v9.17
**Sprint goal:** Ship Site Structure & Usability Phase 3 complete (decision-first Positions page with narrow-screen cards, one warning strip and one grace view; the single Journal area; one Performance page; section indexes on Trade Plan and Strategy Benchmark; the semantic colour token sweep), finish Phase 2's Stops moved group, and fix the four v9.16 Trade Plan found defects.
**Test scenarios used:** `tests/test_stop_last_moved.py`, `tests/e2e/dashboard-today-list.spec.js`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-09 | `data_model.md` v2.69 DS-40; `data_model_positions_dictionary.md` v0.9; `position_endpoints.md` v2.21.0 §GET /positions, §POST /positions/nightly-stop-update, §GET /positions/analyze; `openapi.yaml` 3.49.0 | `positions.stop_last_moved_date` (DATE) and `previous_stop` (DECIMAL(10,4)), added at startup by `ensure_stop_last_moved_columns()`. `record_stop_move()` writes both when a recompute raises a non-null stored stop by a visible (2 dp) amount, keeping the day's first `previous_stop` across same-day raises. Both recompute paths record (ruling below). `GET /positions` returns both read-only. `RecentActivityCard.js` dead `stop_updated_date` branch removed (no visible change). Commits `c50dd966`, `bf6ac67b`. | AC 1 (raised stop → that run's date and the stop before the move): `TestNightlyStopLastMoved::test_raised_stop_records_run_date_and_previous_stop`, `test_second_move_overwrites_with_the_newer_run`, on-load `test_on_load_raise_records_the_move`. AC 2 (unchanged stop → both unchanged): `test_unchanged_stop_leaves_both_fields_unchanged`, `test_sub_rounding_rise_is_not_a_move`, `test_rise_hidden_at_2dp_is_not_a_move`, `test_in_grace_writes_neither_field`, `test_no_atr_skip_writes_neither_field`, `test_on_load_unchanged_stop_records_nothing`. AC 3 (contract and OpenAPI document the fields; drift checks pass): `check_openapi_drift.py`, `openapi_3way_drift_sweep.py`, `check_api_performance_baseline_drift.py`, `lint_api_contract_headings.py` pass; `test_positions_dictionary_coverage.py` passes; CI Pytest Suite run 43390721278 on `c50dd966` and 43393813008 on `2d52ac16`. | Pass | None found against DS-40 / v2.21.0. The same-UTC-day `previous_stop` rule and the 2 dp visibility rule from `bf6ac67b` are documented in DS-40, the dictionary, `position_endpoints.md` and `openapi.yaml` (commit after the DoQ round 1 review); AC 1's "the stop before the move" is read as before the day's move, an intent match (LL-v3.4-P3-03), stated in the contract with a worked example. Scope extension by ruling: on-load path also records moves (see Rulings). Filed BLG-SPEC-237 (P3, `DS-nn` headings vs CLAUDE.md §2) from the pre-commit review |
| ST-10 | `dashboard.md` v4.3 §1B (TL-09, TL-10, Groups and order, States, Quiet day) | Today list group 4, Stops moved: "{TICKER} Stop moved from {previous} to {current}" in native currency (`formatCurrency` + `currencyForMarket`, current = `current_trailing_stop_native`), A–Z, cap 5 with "+N more" → `/Positions`, rows link to `/Positions?position={id}`; skeleton and error line follow `GET /positions`; counts toward quiet day. Window: moves dated today or the previous weekday (UTC), current stop above `previous_stop`. Grace and Stops share `PositionLinkGroup`. Commit `2d52ac16`. | AC 1 (TL-09 and TL-10 Playwright coverage passing in light and dark): SC-TL-09, SC-TL-09b, SC-TL-09c, SC-TL-10, with SC-TL-02 (five-group order), SC-TL-15b (stops skeleton), SC-TL-26 (stops error line), SC-TL-STOPS (absent without moves) updated; all in both themes. Playwright E2E Acceptance Tests run 43393813050 success on `2d52ac16` (step 4c, real CI). AC 2 (with ST-09 merged, `BLG-FE-254` can be bannered ✅ COMPLETE at Post-Ship Closure): planned Post-Ship Closure action per sprint backlog notes, not an in-sprint write; ST-09 is on this branch, so the banner condition is met at merge. | Pass_with_deviation | DEV-EPIC04-ST10-01 (P3, `dashboard.md` §1B Known Deviations): data written by both recompute paths; TL-09's "latest nightly run date" read as today or the previous weekday. Tracking `BLG-SPEC-238` |

**AC coverage:** ST-09 has three ACs and ST-10 two (stage4_backlog_slice.md#ST-09, #ST-10); each is named in its row above. No AC was marked staging-only or post-merge at the seal; ST-10 AC 2 is a Post-Ship Closure action by its own wording.

**Rulings made in session (2026-11-13, the user):**
1. As Head of Specs Team and Data Model & Domain Schema Owner: both stop recompute paths record moves, not only the nightly job, because `daily-snapshot.yml`'s 16:00 UTC `GET /positions/analyze` usually raises a stop before the 22:30 UTC nightly run (found by ST-09's pre-commit `/code-review` high). Recorded in DS-40, `position_endpoints.md` v2.21.0 and DEV-EPIC04-ST10-01.
2. As Frontend Specifications & UX Documentation Owner and Head of UX & Design: the Stops moved group shows moves dated today or the previous weekday (UTC), because `GET /positions` has no run date and "most recent move date" kept old moves under "Due today" and blocked the quiet-day line (found by ST-10's pre-commit `/code-review` medium). Recorded in DEV-EPIC04-ST10-01.

**QA test coverage:**
- Scenarios run: `tests/test_stop_last_moved.py` (15); full local pytest 3562 passed before the follow-up (stub `DATABASE_URL`); `tests/e2e/dashboard-today-list.spec.js` 50/50 locally on an E2E-env production build and in CI; the 15 other DashboardHome Playwright specs 141/141 locally; CI on `2d52ac16`: all 9 workflows success (Playwright E2E 43393813050, Critical-Path Smoke 43393813169, CI Pytest 43393813008, Frontend Production Build 43393813095).
- Regression areas checked: stop ratchet on both recompute paths (`test_atr_provenance.py`, `test_trailing_stop_breakeven_floor.py`, `test_strategy_parameter_parity.py`, `test_live_exit_decision.py`), positions dictionary coverage, OpenAPI/contract drift, Dashboard Today list groups and states, Recent Activity card.
- Known deviations: DEV-EPIC04-ST10-01 (P3, BLG-SPEC-238). ST-09's deviation check found none.
- Frontend testing gate: every observable ST-10 AC (TL-09 rendering and text, TL-10 link and navigation, cap, quiet day, skeleton, error line) has Playwright coverage observed passing in real CI (run 43393813050). ST-09's frontend change removes unreachable code with no rendered difference. No "code review only" AC.
- Same-EPIC testing-gap consistency: no testing-gap backlog item was filed in this EPIC.
- P1/P2 found defects filed during this EPIC: none (BLG-SPEC-237 and BLG-SPEC-238 are P3).
- Deploy: the DS-40 columns are added by the startup ensure-function, so deploy order is not a risk; if they cannot be added, stops still ratchet and no move is recorded. Staging and production Live Confirmation remains the planned Human-Delegation deploy step (Infrastructure & Operations Owner, RISK-03), recorded in DS-40 when supplied.
- Autonomous DoQ class: not available (ST-09 and ST-10 change `src/components/**`; BLG-GOV-135).

## Standard Sign-Off Block

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object
- [ ] **Strategy values checked:** ST-09 — §7.1 (both recompute paths), §7.3 (ratchet: a move is a rise of the stored stop; nothing lowers it), §6.3 (in-grace positions record nothing); stop arithmetic and §11 parameters unchanged. ST-10 — displays the stored stops only; no formula.
- Signed off by:
- Date:
- Comments:
