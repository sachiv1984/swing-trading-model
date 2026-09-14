Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-14

---

## Consolidation Block

**EPIC:** EPIC-02 — QA & Test Coverage Debt
**Cycle:** 2026-09-14__release-v9.4
**Sprint goal:** Clear the full v9.4 debt-reduction scope — 28 items across 6 EPICs — at the top of confirmed sprint capacity, including standing up the AI-output boundary-language sampling hook (`BLG-AI-06`/ST-23). See `sprint_goal.md`.
**Test scenarios used:** `tests/e2e/arc5-compliance-section.spec.js`, `tests/test_arc5_total_closed_trades_null_vs_zero.py`, `tests/e2e/settings-heading-order-and-aria-labelledby-regression.spec.js`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-06 | `tests/e2e/arc5-compliance-section.spec.js` | Added SC-ARC5-11 (strict `<20` boundary: advisory shown at `total_closed_trades = 19`, hidden at `= 20`) and SC-ARC5-12 (singular "1 closed trade" copy at count 1, "0 closed trades" at count 0) to the existing Playwright suite. No source component change — `Arc5ComplianceSection.js` already implements the correct `< LOW_VOLUME_THRESHOLD` boundary and singular/plural interpolation; this story pins that behaviour so a future refactor cannot silently regress it. | Advisory shown at 19 / hidden at 20 (strict `<20` boundary) — met, SC-ARC5-11a/b. Copy reads "1 closed trade" at count 1, "0 closed trades" at count 0 — met, SC-ARC5-12a/b. All added scenarios pass in CI — met (16/16 scenarios in the file pass locally via `npx playwright test`, no live backend required). | Pass | None |
| ST-07 | `tests/test_arc5_total_closed_trades_null_vs_zero.py` | Pre-met (LL-v2.4-P4-02). Verified the existing test file (filed under EPIC-01/ST-04, v9.3, BLG-BE-111) already covers all three return paths of `get_arc5_trade_plan_adherence_rate` and asserts `total_closed_trades` is present in the endpoint response. No new code required. | New unit test(s) covering success/zero-trades/`UndefinedTable` paths — met: `test_trades_with_plans_computes_rate_and_real_count` (success), `test_genuine_zero_trades_returns_zero_not_none` (zero-trades), `test_missing_trade_history_table_returns_none_not_zero` (`UndefinedTable`) — plus bonus `test_broken_column_returns_none_not_zero` (`UndefinedColumn`). Integration assertion confirms `total_closed_trades` present — met: `test_endpoint_returns_json_null_not_zero_on_schema_error`, `test_endpoint_returns_zero_for_genuine_empty_portfolio`. New tests pass in CI — met: re-ran `backend/.venv/bin/python3 -m pytest tests/test_arc5_total_closed_trades_null_vs_zero.py -q` today → 6 passed. | Pass | None |
| ST-08 | `tests/e2e/settings-heading-order-and-aria-labelledby-regression.spec.js` | New Playwright spec pinning: (a) Settings page renders exactly one `<h1>` and every `SectionCard` heading is `<h2>` (no `<h1>`→`<h3>` skip, `BLG-FE-170`); (b) the 5 named controls (Settings Default Currency + Theme `Select` triggers; TradePlan Market, Status, Setup Type native `select`s) each carry `aria-labelledby` resolving to an existing label element (`BLG-FE-171`/`BLG-FE-166`). No source component change — pins existing behaviour. | CI-blocking test fails if Settings heading order regresses (h1→h3 skip) — met, SC-SET-HDR-01a/b. CI-blocking test fails if any of the 5 controls' `aria-labelledby` association is removed or broken — met, SC-SET-ARIA-01, SC-TP-ARIA-01. | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/e2e/arc5-compliance-section.spec.js` (16 scenarios, all pass — `npx playwright test`), `tests/test_arc5_total_closed_trades_null_vs_zero.py` (6 tests, pass — `backend/.venv/bin/python3 -m pytest`), `tests/e2e/settings-heading-order-and-aria-labelledby-regression.spec.js` (4 scenarios, all pass — `npx playwright test`)
- Regression areas checked: `Arc5ComplianceSection.js` low-trade-volume advisory (boundary + copy), `get_arc5_trade_plan_adherence_rate`/`GET /analytics/arc5-compliance` (all return paths), Settings page heading structure, Settings + TradePlan `aria-labelledby` associations. No production source file was modified by this EPIC (test files only) — no new regression surface introduced.
- Known deviations: None found — all 3 stories' deviation checks completed with nothing to file.

**Frontend testing gate (LL-v3.1-EX-01):** ST-06 and ST-08 introduce Playwright coverage for pre-existing, observable frontend behaviour (advisory visibility/copy; heading levels; `aria-labelledby` association). Each named AC is backed by a passing Playwright scenario listed above — no "code review only" AC in this EPIC, no backlog item required.

**Autonomous class (BLG-GOV-19) — not applicable:** All 3 stories are `autonomous` (Criterion 1 ✓) and no `src/components/**`/`src/pages/**` file was created or modified (Criterion 3's detection rule ✓), but ST-06 and ST-08 have observable, UI-rendering AC verified via Playwright rather than code review alone — Criterion 2 ("no observable UI behaviour") is not met. Per `qa_evidence_template.md`'s Criterion 3 fail-path note, the Standard Sign-Off Block is used instead.

---

## Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] N/A — no frontend component in this EPIC making direct URL construction (test files only; no `src/` change)
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-14
- Comments: All 3 stories autonomous, test-coverage-only (no `src/` changes). ST-06 and ST-08 observable AC each backed by a passing Playwright scenario (see QA test coverage above) — Frontend Testing Gate satisfied via Playwright coverage, no staging run or backlog item required. ST-07 is a pre-met item (LL-v2.4-P4-02) — prior-sprint test file re-verified passing against current `main`. Agent-mediated Director of Quality review confirms: all AC met, all named test scenarios genuinely exercise their AC (not just present), no deviations, no frontend-visible source change in scope.
