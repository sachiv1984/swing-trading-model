Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-09

# QA Evidence — EPIC-05: Spec & Contract Hygiene

**EPIC:** EPIC-05 — Spec & Contract Hygiene
**Cycle:** 2026-10-08__release-v9.11
**Sprint goal:** Make the post-trade debrief state R achieved and the stop at exit, confirm every AI feature works after the v9.4–v9.10 import defect, and make the Risk Dashboard and Positions page show real prices, GBP entry values, true stop distance and calendar-day grace (BLG-BE-152, BLG-BE-150, BLG-BE-154, BLG-FE-206), while shipping the AI monthly P&L narrative and clearing v9.11's records, spec and governance hygiene items. See `sprint_goal.md`.
**Test scenarios used:** `tests/test_trade_plan_status_enum_parity.py`; plus the repository check scripts named per row (`scripts/check_contract_example_freshness.py`, `scripts/check_openapi_drift.py`). The other stories are documentation-only, verified by inspection against the code.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-29 | `reports.md` §Monthly Restatement Marker (v0.22); `reports_endpoints.md#GET /reports/monthly-pnl` (v0.16) | Spec moved to match the API and shipped UI: "As reviewed" undated; the unavailable state defined as "no month carries a boolean `restated`"; the contract states what the response does not carry | AC1 the two documents now agree on both points (read side by side). AC2 the shipped UI already uses that trigger (`Reports.js`, `restatementCheckUnavailable`), so it matches with no code change; the remaining backend gap (a snapshot-store failure fails the whole report, so the line never shows for a real failure) is filed as `BLG-BE-156`. AC3 DEV-v9.7-ST04-01 marked ✅ RESOLVED with BLG-SPEC-170, Target resolution release v9.11 | Pass | DEV-v9.7-ST04-01 closed. Follow-up for the backend difference: `BLG-BE-156` (AC2 permits "a follow-up is filed for the difference") |
| ST-30 | `data_model.md` §2 Positions Table, DS-04 Field Reference (v2.55) | Provenance tag (user-entered / derived / system-stamped) on all 40 `positions` and 35 `trade_plans` fields; 3 missing `positions` rows added; `trade_plans` reference rebuilt from the live DDL; `entry_price`/`fill_price` currency descriptions corrected to match `add_position()` | AC1 every field in both tables carries a tag (75 rows, counted). AC2 mixed fields carry an explicit note (`fx_rate`, `atr`, `shares`, `position_id`, the four AI-draftable narrative fields), so none is ambiguous. Each tag was checked against the code that writes the field (`position_service.add_position` / `exit_position`, the stop recompute paths, `routers/trade_plans.py`, `database.py` DDL) | Pass | None against this AC. Findings filed: `BLG-BE-159` (Trail Stop apply calls a non-existent `PATCH /positions/{id}`; a supplied entry `stop_price` is ignored) and `BLG-SPEC-190` (positions dictionary still describes `entry_price` as native) |
| ST-31 | `openapi.yaml` (v3.26.0); `data_model.md` DS-21 | All 4 TradePlan status enum sites list DS-21's 7 values | AC1 `tests/test_trade_plan_status_enum_parity.py` (2 passed) asserts every status enum equals DS-21's CHECK list. AC2 `check_openapi_drift.py` passes; `check_contract_example_freshness.py` reports no new finding (its success-example key drift is pre-existing and unchanged; 0 error-envelope violations) | Pass | None found |
| ST-32 | `conventions.md` §13.1; 5 contract files | 4 error examples corrected to the `{status, message}` envelope the code already returns; 1 heading label corrected (503 → 200) | AC1 all 5 flagged cases resolved: ai_thesis_generation and gemini_thesis_generation 404 and arc5_compliance_analytics 500 (documentation corrected; `routers/trade_plans.py` and `routers/analytics.py` return the envelope), behavioural_drift_contract 401 (documentation corrected; the API-key middleware in `main.py` returns the envelope), ai_endpoints journal-summary (heading label corrected; the endpoint returns 200). AC2 `check_contract_example_freshness.py` reports 0 error-envelope violations | Pass | None found |

**QA test coverage:**
- Scenarios run (2026-10-09, branch head `121db1b1`): `tests/test_trade_plan_status_enum_parity.py` (2 passed); `scripts/check_openapi_drift.py` (PASSED); `scripts/check_contract_example_freshness.py` (0 error-envelope violations, down from 5 on `main`; it still exits 1 on 8 success-example key-drift findings that are identical on `main`, so pre-existing and outside this EPIC's AC); `scripts/check_api_performance_baseline_drift.py` (PASSED). Real CI on `121db1b1`: CI Pytest Suite, Critical-Path Smoke Tests, Portfolio Integration Tests, Golden Output Regression Gate, Service Layer Coverage Gate and Endpoint Coverage Report all succeeded.
- Regression areas checked: API contract set (drift and envelope checks), `openapi.yaml` validity, data model (`data_model.md` header and footer both v2.55; no migration block changed), Monthly P&L restatement UI (no code change; trigger confirmed in `Reports.js`).
- Known deviations: DEV-v9.7-ST04-01 closed by ST-29. No new deviation found in any story's deviation check. Backlog follow-ups filed this EPIC: `BLG-BE-156`, `BLG-BE-159`, `BLG-SPEC-190`.

**Merge note:** this EPIC merges last per `sprint_backlog.md` Merge Order. It shares `data_model.md`, `openapi.yaml`, `ai_endpoints.md`, `reports.md`, `ai_thesis_generation.md` and `backlog.md` with other EPICs; the version numbers used here (data_model 2.55, openapi 3.26.0, ai_endpoints 1.21, ai_thesis_generation 2.1.2, reports.md 0.22 with 0.21 left for ST-25) were chosen not to collide. Resolve per CLAUDE.md §8 when rebasing.

---

## BLG-GOV-19 Autonomous Class Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-29, ST-30, ST-31, ST-32)
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓. Verification used documentation inspection against code, one unit test and repository check scripts; no live system was queried (BLG-GOV-335 live-interaction bar: met by the method actually used)
- [x] Criterion 3: No frontend-visible change — ✓. `git diff --name-only origin/main...HEAD` lists no file under `src/components/` or `src/pages/` (BLG-GOV-135 detection rule)
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓
- [x] **Strategy values checked (conditional — ST-36, BLG-GOV-370):** ST-30 states stop and grace values in `data_model.md`. Checked: `initial_stop` = entry − 5 × ATR against `strategy_rules.md` §5 and §11 (initial multiplier 5.0); `current_stop` written only by the recompute paths, consistent with §7.2/§7.3; `holding_days` / grace described as calendar days against §6.2. ST-29, ST-31 and ST-32 touch no stop, grace, ATR, exit or sizing logic.

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-10-09
- Comments: Autonomous class sign-off — all four qualifying criteria met (all stories autonomous, all AC code-review-verifiable, no frontend changes, engine signer populated). The Director of Quality may review and override before merge (execution_prompt.md §3.2.A). PR not yet opened, by user direction (2026-10-09): opens when the earlier EPICs have merged.
