Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-02

# QA Evidence — EPIC-05 — Test Coverage & Test Tooling

**EPIC:** EPIC-05 — Test Coverage & Test Tooling
**Cycle:** 2026-10-29__release-v9.14
**Sprint goal:** Restore the production frontend deploy (BLG-OPS-193, P1) so shipped UI reaches GitHub Pages again, and stop a Yahoo Finance outage from silently giving a risk-on regime and a frozen 1.27 FX rate while System Status reports healthy. Also fix US position sizing's FX inversion (BLG-BE-190) and ship v9.14's AI output safety, reporting, test, operations and governance items.
**Branch:** `exec/2026-10-29__release-v9.14/EPIC-05` (cut from `main` at `42bec3ce`, after EPIC-07 merged, so EPIC-05 merges last over the final tree as planned)
**Test scenarios used:** `tests/test_check_local_openapi_contract_completeness.py`, `tests/test_conftest_database_stub_scan.py`, `tests/test_alerts_service.py`, `tests/test_backend_services_sys_path_guard.py`, `tests/e2e/positions-exit-modal.spec.js`, `tests/e2e/stop-cell-provenance.spec.js`, `tests/e2e/accessibility-axe-scan.spec.js`, `tests/e2e/epic02-v62-ai-briefing-chat.spec.js`. Full backend suite at `025c0265`: 3224 passed, 30 skipped (`backend/.venv`, stub `DATABASE_URL`). ST-30 is a human staging pass (DEL-20261102-01).

## Story Evidence

### Positions-page Exit modal submit

- **Story:** ST-29 (BLG-QA-237) · **Commit:** `f32b8c23`
- **Spec references:** `tests/e2e/positions-exit-modal.spec.js`; `docs/testing/state_changing_action_coverage.md` row 2; `position_endpoints.md` §POST /positions/{position_id}/exit
- **What was built:** SC-PEM-01 checks that Confirm Exit posts the expected body (shares, `exit_price` from `current_price_native`, `exit_fx_rate` from `live_fx_rate`, today's `exit_date`, an `exit_reason`), that the modal closes, and that the position leaves the open list. SC-PEM-02 checks that a 400 "Position already closed" (ST-10's documented error) keeps the modal open with Confirm Exit enabled and the position still listed, and that the error is shown. Inventory row 2 now reads Covered and the totals were recomputed (38 covered, 14 not covered).
- **AC 1** (inventory row 2 reads Covered with the scenario IDs): met.
- **AC 2** (both scenarios pass in CI under the API status guard): met. Playwright E2E run 41441543880 succeeded on `f32b8c23`, along with all 8 workflows.
- **Note:** the Positions page reports a failed exit with `window.alert`, not the modal's inline `exit-error` block that the Monitor queue uses, because `handleExit` does not return the mutation promise. SC-PEM-02 asserts the alert text. Filed as BLG-FE-241 (P3). This story is test-only, so the app was not changed.

### Staging visual check of the tailwind-merge layout change

- **Story:** ST-30 (BLG-QA-235) · **Delegation:** DEL-20261102-01 (Director of Quality or Head of UX & Design)
- **Spec references:** `src/lib/utils.js` (`cn()`); `stage4_backlog_slice.md#ST-30`
- **What is needed:** a human staging pass in light and dark themes of Positions (grid and table), Trade History with a row expanded, Dashboard, Trade Plans, Screener, Settings, and at least one dialog and one sheet. Compare each page with the pre-change build (`2f5cc56a~1`). Production now serves the post-change build, because deploys resumed from `main` on 2026-11-02.
- **Staging run date:** 2026-11-02. The Product Owner reviewed staging in a browser and accepted the findings below; they did not record which pages or themes they viewed. The both-theme, page-by-page coverage below is the engine comparison. The human part of DEL-20261102-01's "staging pass in both themes" is therefore met as a browser review plus acceptance of that comparison, not as a recorded page-by-page human pass in both themes. AC 1 (date and pages recorded) is met. The before/after comparison (DEL-20261102-01 step 3) used engine screenshots from local builds of `2f5cc56a~1` (`388e31d9`) and `d11e6446`, whose app code is `main` `42bec3ce`: same mocked API data, Chromium 1280×900, both themes.
- **Staging commit check (DEL step 1):** the staging bundle (`static/js/main.2f34524f.js`, fetched 2026-11-02) contains `3a3b9868`'s change (EPIC-04 ST-28, `/reports` → Analytics) and the ST-25 emerald fills. `3a3b9868` is the last commit touching `src/` before `42bec3ce`, and `git diff 3a3b9868 42bec3ce -- src/ public/ package.json tailwind.config.js` is empty, so staging serves the same frontend as the "after" build.
- **Pages and themes checked:** Dashboard, Positions (grid and table), Exit Position dialog, Trade History (row expanded), Trade Plans, Screener, Settings, and the mobile slide-in menu at 390px as the sheet. The app renders no `Sheet` component (`ui/sheet.js` is never imported). All pages were checked in light and dark: 18 pairs, each pixel-diffed, style-diffed per element, and run through axe `color-contrast` in both builds.
- **Differences found and dispositions** (Head of UX & Design, agent-mediated at the Product Owner's instruction, 2026-11-02; finding 1 decided by the Product Owner):
  1. Light theme, Trade History "No saved filters" text contrast 4.32:1 → 1.45:1 (dark-only `bg-slate-800/50` fill now applied). **Unintended → BLG-FE-242** (Product Owner decision: backlog, not an in-sprint fix).
  2. Positions table trailing stop value slate-300 → rose-400, both themes. **Intended.** The cell always authored `text-rose-400`; `design_system` §1.3 assigns rose-400 to stop values, and the grid card already shows it. Table and grid now agree. The orange BREACH pill stays distinct (v6.2 trailing-stop ux_spec §3).
  3. Form fields take their `bg-slate-800/50` fill (Exit dialog, Trade History filters). **Intended in dark**, which matches `design_system` §1.1 (input field `bg-slate-800`). The light-theme rendering is the dark-only-token class and is covered by BLG-FE-242. It is not a blocker, because it removes 4 existing light-theme contrast failures and adds only finding 1.
  4. Trade Plans icon buttons 36 → 28px, Clone/Start Trade 32 → 28px tall, rows ~8px shorter, Start Trade emerald border; Positions table icon buttons 36 → 32px. **Intended.** These are the sizes and border the callers authored. 28px exceeds the WCAG 2.2 SC 2.5.8 24px minimum target size. Tables collapse to cards on mobile (`design_system` §Responsive Behavior), so touch use doesn't land on these buttons.
  5. Trade History cell side padding 24 → 8px; the table fits at 1280px (1362 → 986px) with no horizontal scroll; light-theme headers slate-600 → slate-300 on the dark table. **Intended / acceptable.** Already disclosed in `2f5cc56a` (RISK-05). All 14 `trade_history.md` columns are visible without scrolling. 8px is tighter than the living reference's compact `px-3`, which is noted, not filed. The Post-Trade Debrief Generate/Regenerate buttons, which the delegation named as a known unplanned change, now sit on screen at 1280px (x=1145, was x=1520 off-screen). Their light-theme text colour was already fixed in `2f5cc56a` (`text-slate-800 dark:text-slate-300`, SC-DBF-06a), and the after screenshot shows Regenerate readable on the white debrief card. **Intended.**
  - Unchanged: Dashboard, Screener, Settings, mobile menu (pixel-identical in both themes); Positions grid (only the view toggle's 12px unused padding, visible in hover state).
  - Pre-existing, equal in both builds, not caused by this change: light-theme dark tables and dialogs, and about 39 axe contrast failures each on light Dashboard and Screener.
- **QA findings (Director of Quality):** see the Sign-Off Block.
- **Disposition:** Pass. AC 1 is met: the date and the pages checked are recorded above. AC 2 is met: the one unintended change is backlogged as BLG-FE-242 (Product Owner decision).

### Pre-commit OpenAPI contract check reads staged content

- **Story:** ST-31 (BLG-QA-238) · **Commit:** `f1474aa4`
- **Spec references:** `scripts/check_local_openapi_contract_completeness.py`, `.githooks/pre-commit`, `tests/test_check_local_openapi_contract_completeness.py`
- **What was built:** a `--staged` mode that exports the index version of the check scripts and their inputs with `git checkout-index` and runs the checks there. The hook passes `--staged`; a manual run still checks the working tree.
- **AC 1–3:** met. Tests run against a throwaway git repo with the real check scripts: an unstaged undocumented route does not fail; a staged undocumented route fails, even after the working tree is reverted; manual mode still fails on the working tree. 13/13 tests pass. Every EPIC-05 commit after `f1474aa4` ran the hook in `--staged` mode. All 7 CI workflows succeeded on `f1474aa4`.

### conftest.py AST scan coverage

- **Story:** ST-32 (BLG-QA-93) · **Commit:** `b1d36bb5`
- **Spec references:** `tests/conftest.py` (`_discover_database_stub_functions`), `tests/test_conftest_database_stub_scan.py`
- **What was built:** `rglob` already reached every subpackage. The gap was the `import database` / `database.<fn>` form: `routers/strategy_benchmark.py`'s 6 names were missing from the stub. The scan now covers that form. The new test compares the scan with an independent regex scan of the git-tracked backend files, per subpackage, and with a synthetic tree (nested packages, aliases, vendored-path exclusion).
- **AC 1–3:** met. All 4 new tests fail on the previous scan. The confirmation and date are in the scan's docstring. All 7 CI workflows succeeded on `b1d36bb5` (CI Pytest 41439987293).

### Grace warning ignores settings.min_hold_days

- **Story:** ST-33 (BLG-QA-214) · **Commit:** `2b1fee78`
- **Spec references:** `tests/test_alerts_service.py` (`TestGraceWarningIgnoresSettingsMinHoldDays`); `strategy_rules.md` §11
- **What was built:** `evaluate_alerts` runs with a settings row of `min_hold_days = 5`, offered both through `get_settings()` and through the cursor. Positions held 3, 4, 7, 8, 9 and 10 days warn on days 8 and 9 only, and the message names the 10-day period.
- **AC:** met. Mutation-checked: putting back the pre-v9.10 settings read fails both tests (`[3, 4] != [8, 9]`). All 7 CI workflows succeeded on `2b1fee78`.

### Stop-details tooltip time under a non-UTC browser timezone

- **Story:** ST-34 (BLG-QA-215) · **Commit:** `458362fa`
- **Spec references:** `tests/e2e/stop-cell-provenance.spec.js`; `positions.md` §Stop Provenance Line and Per-Row Stop Details
- **What was built:** SC-SCP-11, with `timezoneId: 'Europe/London'`.
- **AC:** met. The tooltip reads "Last recalculated 5 Oct 2026, 22:15 — nightly update" for input `2026-10-05T21:15:00+00:00`. Playwright E2E run 41440281517 succeeded, along with all 8 workflows.

### Applied theme asserted in every Reports/Notifications axe scan

- **Story:** ST-35 (BLG-QA-216) · **Commit:** `9314f01c`
- **Spec references:** `tests/e2e/accessibility-axe-scan.spec.js`
- **What was built:** a shared `expectThemeApplied` helper, called before `runAxeScan` in all 8 Reports/Notifications tests. The Replay block reuses it.
- **AC:** met. Playwright E2E run 41440528040 succeeded (14/14 locally).

### No test file adds backend/services/ to sys.path

- **Story:** ST-36 (BLG-QA-218) · **Commit:** `025c0265`
- **Spec references:** `tests/conftest.py` (backend/services sys.path guard), `tests/test_plan_vs_reality.py`, `tests/test_backend_services_sys_path_guard.py`
- **What was built:** `test_plan_vs_reality.py`, the last offender, now loads the service by file path. The conftest guard fails collection of any file that leaves `backend/services/` on `sys.path`, and fails any test that adds it at run time. Subprocess probe tests exercise both paths, and a static AST backstop covers `tests/`.
- **AC 1:** met. The old `test_plan_vs_reality.py` fails collection under the guard.
- **AC 2:** met. Full suite: 3224 passed, 30 skipped. All 7 CI workflows succeeded on `025c0265` (CI Pytest 41442365106).
- **Issue closure:** #2113 was closed by hand at 2026-11-02T12:13:01Z. Governance Sync on `025c0265` logged "Skipping close for ST-36 — execution_state status is not done/merged", because ST-36's `done` status landed in the later governance commit `d11e6446`. #2107 (ST-30) was closed by hand for the same reason (`done` landed in `c1e8eeb2`).

### ⌘K hint toast in SC-AC-03

- **Story:** ST-37 (BLG-QA-219) · **Commit:** `f982225a`
- **Spec references:** `tests/e2e/epic02-v62-ai-briefing-chat.spec.js`
- **What was built:** a `beforeEach` sets `command-palette-tooltip-seen` with `addInitScript` for all 6 chat scenarios, and SC-AC-03 asserts the hint never shows. The app is unchanged.
- **AC:** met. SC-AC-03 passed 10/10 with `--repeat-each=10` locally, and no `test.fixme` is needed. A pre-fix run also passed 10/10 in this sandbox, so the flake did not reproduce here; the fix removes the timing exposure the item describes. Playwright E2E run 41440862985 succeeded.

## Consolidation Block

**EPIC:** EPIC-05 — Test Coverage & Test Tooling
**Cycle:** 2026-10-29__release-v9.14
**Sprint goal:** as above.
**Test scenarios used:** as above.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-29 | `positions-exit-modal.spec.js`; inventory row 2 | SC-PEM-01..02 Exit modal submit and failure | Covers AC 1, AC 2 | Pass | None (BLG-FE-241 incidental finding) |
| ST-30 | `src/lib/utils.js` `cn()` | Staging visual check, both themes, 9 screens; Product Owner browser review 2026-11-02 (DEL-20261102-01) | Covers AC 1, AC 2 | Pass | None (BLG-FE-242: unintended light-theme contrast change, backlogged per AC 2) |
| ST-31 | `check_local_openapi_contract_completeness.py` | `--staged` hook mode | Covers AC 1, AC 2, AC 3 | Pass | None |
| ST-32 | `tests/conftest.py` AST scan | `import database` form covered; coverage test | Covers AC 1, AC 2, AC 3 | Pass | None |
| ST-33 | `test_alerts_service.py`; §11 | Grace-warning behaviour test, mutation-checked | Covers AC 1 | Pass | None |
| ST-34 | `stop-cell-provenance.spec.js` | SC-SCP-11 Europe/London | Covers AC 1 | Pass | None |
| ST-35 | `accessibility-axe-scan.spec.js` | Theme asserted before all 8 scans | Covers AC 1 | Pass | None |
| ST-36 | `tests/conftest.py` sys.path guard | File-path load; collection and run-time guard | Covers AC 1, AC 2 | Pass | None |
| ST-37 | `epic02-v62-ai-briefing-chat.spec.js` | ⌘K hint suppressed in chat scenarios | Covers AC 1, AC 2 | Pass | None |

**QA test coverage:**
- Scenarios run: the files listed under "Test scenarios used"; CI run IDs per story above.
- Regression areas checked: Positions page (Exit modal, stop tooltip), Reports/Notifications/Replay accessibility, AI chat widget, alerts evaluation, backend test-harness isolation (conftest database stub, sys.path), pre-commit hook.
- Known deviations: None found. All stories' deviation checks completed with nothing to file. BLG-FE-241 is an incidental finding (no spec requirement on the Positions page), not a deviation. BLG-FE-242 (P3) tracks the one unintended light-theme contrast change found by ST-30, backlogged per its AC 2.

## Sign-Off Block

EPIC-05 includes a human staging check (ST-30), so the autonomous-class block (BLG-GOV-19) does not apply: Criterion 1 is not met.

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object. N/A: no EPIC-05 commit touches `src/`.
- [x] **Strategy values checked:** ST-33: §6 grace length and §11 `GRACE_PERIOD_DAYS` (10; warning on days 8–9). ST-29: exit body only, no exit-rule values asserted. ST-34: display of `stop_calculated_at` only, no stop values. Other stories touch no stop/grace/ATR/exit/sizing logic.
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-11-02
- Comments: All 9 ST ACs verified against the diffs and the sealed slice. CI is green on every story SHA, and the Playwright shard logs of run 41441543880 show SC-PEM-01/02, SC-SCP-11 and SC-AC-03 passing. Stub-DB pytest on the EPIC's backend test files passed 79/79 in the review; the full suite at `025c0265` is 3224 passed, 30 skipped. ST-30 staging run 2026-11-02 (Product Owner browser review, with engine before/after diffs of 9 screens in both themes) found one unintended light-theme contrast change, backlogged as BLG-FE-242 (P3). There are no P0/P1 deviations. Disclosed limits: SC-PEM-02 asserts the window.alert path (BLG-FE-241), ST-37's flake didn't reproduce before the fix, the Product Owner's staging review didn't record pages or themes, and #2113 and #2107 were closed by hand.

## Merge Gate Confirmations

- **Merged:** PR #2139 by the human developer, 2026-11-02T15:06:08Z, merge commit `0fd6a669`. At merge time, the only review on the PR was the agent-mediated Director of Quality + Product Owner comment (6580448267). That comment does not satisfy the always-human rows, and no written human confirmation existed.
- **Director of Quality QA sign-off (given after the merge):** given by the human repository owner, acting as Director of Quality, in session on 2026-11-02, after the merge, and recorded on PR #2139 (comment 6581095942; head `92933853`, all 44 check runs succeeded). It accepts this evidence (ST-29 to ST-37 Pass), including ST-30's staging visual check as recorded, and the review's comments as non-blocking. Follow-ups: BLG-FE-241 (P3), BLG-FE-242 (P3) and BLG-FE-243 (P2, a found pre-existing defect still routed to the delivery verification §7 path).
- **Product Owner acceptance (given after the merge):** given by the human repository owner, acting as Product Owner, in session on 2026-11-02, and recorded on PR #2139 (same comment). It accepts ST-29 to ST-37 against `stage4_backlog_slice.md`, including the ST-30 unintended change backlogged as BLG-FE-242. There are no post-merge items.
