Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-27

# QA Evidence — Home Page and Navigation

**EPIC:** EPIC-02 — Site Structure & Usability Phase 4, Stage 2: Home Page and Navigation (build-and-ship)
**Cycle:** 2026-11-18__release-v9.18
**Sprint goal:** Ship Site Structure & Usability Phase 4 stages 1–2 (… a one-line quiet-day Dashboard, the two navigation moves …), put the first-time-right checks in place before v9.19's design gate, and make position figures correct (`sprint_goal.md`). EPIC-02 delivers the home page and navigation share: the design direction, the two navigation moves, the quiet-day Dashboard, one grace definition, "Plan this" on the Today list, the automatic checklist items and the rules filter.
**Branch:** `exec/2026-11-18__release-v9.18/EPIC-02`
**Test scenarios used:** `tests/e2e/strategy-benchmark.spec.js`, `tests/e2e/section-index.spec.js`, `tests/e2e/performance.spec.js`, `tests/e2e/ticker-universe.spec.js`, `tests/e2e/page-labels-single-source.spec.js`, `tests/e2e/onward-links.spec.js`, `tests/e2e/sidebar-nav-groups.spec.js`, `tests/e2e/accessibility-axe-scan.spec.js`, `tests/e2e/dashboard-quiet-day.spec.js`, `tests/e2e/morning-briefing.spec.js`, `tests/e2e/empty-state-next-action.spec.js`, `tests/e2e/v7.2-dashboard-tradeplan-ux-hardening.spec.js`, `tests/e2e/dashboard-grace-definition.spec.js`, `tests/e2e/dashboard-today-list.spec.js`, `tests/e2e/entry-checklist.spec.js`, `tests/e2e/rules-filter.spec.js`, `tests/test_red_flag_checklist_skipped.py`, `tests/test_rules_followed.py`, `tests/test_rules_followed_db.py`, plus frontend unit tests `src/lib/quietDay.test.js`, `src/lib/positionUrgency.grace.test.js`, `src/lib/checklistStatus.test.js`, `src/lib/rulesFilter.test.js` (CI `frontend-unit-tests.yml`)

## Consolidation Block

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-07 | `design_system.md` v1.28 §Design Direction; `navigation.md` v2.5 | §Design Direction from re-review §14.5 (adopted by DL-089), each gap naming its backlog item. Commit `4460bf5f`. | AC 1 (dated PO decision): met by DL-089, carried as context. AC 2: both files reflect the decision, with dated Head of UX & Design approval (the user, 2026-11-24, `ESC-EXEC-20261124-01`). | Pass — documentation-only story; verified by document review. | None |
| ST-08 | `navigation.md` v2.5/v2.6; `performance.md` v1.3 §4.1; `strategy_benchmark.md` v0.12; `ticker_universe.md` v1.3; `settings.md` v1.11 | Strategy Benchmark is Performance's "Strategy vs backtest" section (no sticky bar, no inner index, panels h3); Ticker Universe at `/settings/ticker-universe` with parent Settings and the Settings "Screener universe" row; both old routes redirect; sidebar 17; palette entries. Commit `874ffedf`. | AC 1 (no sidebar entry; both old URLs land on the new location): SC-SB-01b, SC-TU-10a/b, sidebar-nav-groups (17). AC 2 (Playwright covers both redirects and the new entry points): SC-SB-01a/b, SC-SIX-06/06b/06c, SC-PERF-01/02, SC-PL-02b, SC-ONW-05, SC-TU-10a/b. | Pass | None |
| ST-09 | `dashboard.md` v4.4 §3A (v4.5 notes) | Zero-state elements fold into one "Nothing to show: …" line under the Today list; disclosure entries for AI briefing and What's new; errors stay in place; containers hide; rows re-flow. Commit `0125538c`; baselines `e8b975cb`. | AC 1 (quiet-day fixture: at most 1 empty-state element below "Due today", light and dark): SC-QD-01a/b. AC 2 (a card with data keeps its v4.0 position): SC-QD-02 and the populated Dashboard baseline. | Pass | None (QD-04's request corrected to `GET /signals` in v4.5, a spec text fix) |
| ST-10 | `dashboard.md` v4.4 §4B (v4.6 notes); `risk_dashboard.md` §5.2 | One predicate `isInGrace` for Card 1, Card 3, Positions to Watch and the Today list's Grace ends today; Card 3 "next ends" text shared with the Risk Dashboard (`nextEndsText` moved to `positionUrgency.js`); Positions to Watch loses "exit zone" and links to the grace view. Commits `8ff17e93`, CI fix `6b193c24`. | AC 1 (disagreeing fixture: every grace count the same): SC-GD-01, SC-GD-01b. AC 2 (Positions to Watch opens the grace view): SC-GD-02. | Pass | None |
| ST-11 | `dashboard.md` v4.4 §1B, TL-30 (v4.7 note); `signals.md` §"Plan this" Action | "Plan this" link on `new`/`watchlisted` New signals rows with the shared `planThisUrl`. Commit `d758184d`. | AC 1 (§1B records the decision; "Plan this" opens Trade Plan pre-filled with ticker and market): SC-TL-30 (light, dark; US with price, UK without). | Pass | None |
| ST-12 | `trade_plan.md` v1.30 §6 (v1.31 notes); `red_flag_journal.md` contract v1.2.0 | Checklist split into "Checked by the system" (Position size checks, Stop level defined) and "Your judgement"; saved with `auto: true`; Research read-only status from the stored snapshot; backend `checklist_skipped` counts judgement items only. Commit `d5b2acc3`. | AC 1 (the two system items show automatic status that follows the inputs and cannot be ticked; "Position size within heat limits" renamed "Position size checks" per the addendum §ST-12, Product Owner decision 2026-11-18): SC-CL-12. AC 2 (judgement items tickable; existing plans load without losing saved ticks): SC-CL-13, SC-CL-13b, unit `checklistStatus.test.js`. Pre-build Strategy Rules & System Intent Owner confirmation: 2026-11-24 (`ESC-EXEC-20261124-02`). | Pass | None |
| ST-13 | `metrics_definitions.md` v1.36.0 §Rules Followed; `trade_endpoints.md` v2.7.0; `trade_history.md` v1.18 §Rules Filter (v1.19 notes) | `GET /trades` gains `rules_followed`/`rules_broken`; Trade History "Rules" filter with counts, `?rules=`, presets and stored filters; expanded-row line; filtered empty state. Commit `47b79ca0`; pre-PR review fixes and the `ESC-EXEC-20261126-03` revision in the follow-up commit (see CI record). | AC 1 (definition recorded in `metrics_definitions.md`): §Rules Followed, approved `ESC-EXEC-20261124-03`, revised `ESC-EXEC-20261126-02` and `-03`. AC 2 (compliant and non-compliant fixture: each filter shows only its trades): SC-RF-01, SC-RF-02. | Pass | None |

**AC coverage:** every slice AC for ST-07 to ST-13 (read with the addendum) is named in its row above.

**Frontend testing gate:** every observable AC has Playwright coverage (scenario IDs in the rows above); none relies on code review alone. ST-07 is documentation only.

**QA test coverage:**
- Scenarios run: Playwright, locally against the E2E bundle — ST-08 81 + 70 + 10 + 5 + 69; ST-09 8 + 166 + 45 + 78; ST-10 95 + 79; ST-11 52; ST-12 73; ST-13: `rules-filter.spec.js` 9 test instances (8 tests, SC-RF-07 in both themes) run with `saved-filters-calendar-view.spec.js` and `trade-history-win-rate.spec.js` = 23, then the six Trade History regression specs (`fee-drag-trade-history`, `net-r-trade-history`, `saved-filters-calendar-view`, `trade-history-ai-journal-summary`, `trade-history-win-rate`, `onward-links`) = 41 (all passed). Unit (Jest): quietDay 35, positionUrgency 176, checklistStatus 47, rulesFilter 26. Pytest: affected suites 191 passed; full suite 4016 passed, with 2 local-only failures traced to `database.py` being edited during the run and the ignored `backend/mutants/` folder (both pass on rerun). `tests/test_rules_followed_db.py` needs real Postgres and runs only in CI Phase B (skipped locally). CI per story commit: see "CI record" below.
- Regression areas checked: Performance page (sections, index, exports, axe); Strategy Benchmark tabs (Version Comparison, Backtest Rule Change); Settings; Ticker Universe; sidebar, palette and labels; onward links; Dashboard (Today list, Morning Briefing, AI briefing, What's New, cards, visual baselines); Risk Dashboard grace panel; Trade Plan form, clone and Research read-only plan; red-flag journal writer; Trade History filters, presets, Calendar; staleness indicator; Replay axe scans.
- Known deviations: none found — every story's deviation check completed with nothing to file.

**CI record:** ST-08 `874ffedf` all 11 workflows success (Playwright 45424461843). ST-09 `0125538c` all 11 success (Playwright 45433956563); baselines regenerated on the CI runner (update-visual-snapshots 45453182629, commit `e8b975cb`). ST-10 `8ff17e93`: CI Pytest 45456088579 failed (strategy-copy lint matched a unit-test title) and Playwright 45456088330 failed (ReplayTradeSet:dark, the ⌘K hint toast during the scan); both fixed in `6b193c24`, cleared on `d758184d` (contains it): all 9 workflows success (Playwright 45859218434, CI Pytest 45859218389). ST-11 `d758184d` as above. ST-12 `d5b2acc3`: 9 of 9 reported workflows success; its Playwright and Pytest runs were superseded by `47b79ca0`, which contains it. ST-13 `47b79ca0`: Playwright 45867564450 failed SC-RF-08 (the test left through Positions, which crashes on the catch-all mock) and CI Pytest 45867564435 failed `test_missing_trade_plans_table_keeps_the_event_evidence` (the scratch schema's `search_path` included `public`, so a dropped scratch table fell through to another test's `public.trade_plans`); both test faults, fixed in the follow-up commit with the review fixes and the `ESC-EXEC-20261126-03` revision. Follow-up commit `86130e54`: 8 of 9 workflows success, incl. Playwright E2E 45872238856 (all shards and both visual jobs); CI Pytest 45872238877 failed two Phase B tests because the fixture's in-transaction `SET search_path` was undone by the code's rollback — fixed in `518b1214` (connection-option search path). Baselines regenerated on the CI runner for the Trade Plan checklist (update-visual-snapshots 45872268887, commit `774650db`), checked by eye. Final head `518b1214`: all 7 triggered workflows success (CI Pytest 45897742478; Phase B ran all 7 `test_rules_followed_db.py` tests, all passed); Playwright and the frontend jobs are path-filtered and did not trigger for this test-only commit, and the frontend code is unchanged since `86130e54`, whose Playwright run passed.

## Pre-PR Agent-Mediated Reviews (2026-11-26)

**[Agent-mediated review — on behalf of Director of Quality, pending human confirmation]** ❌ Blocked, then cleared. Blockers: SC-RF-08 and the Phase B DB test failed in CI (both test faults, fixed), and ST-13's grading and run counts did not yet reflect them (corrected above). Also fixed: ST-12's AC cell cites the addendum rename; the OpenAPI 3.53.0 header comment; `trade_history.md`'s SC-RF range. Checks it ran: 10 commits all `[EPIC-02][ST-xx]`, no foreign EPIC commits; execution-state consistency OK; OpenAPI drift 154/154; backlog integrity OK; 16 `spec_references` resolve; Jest 284 passed; pytest 47 passed, 5 skipped (Phase B).

**[Agent-mediated review — on behalf of Product Owner, pending human confirmation]** ⚠️ Approved with Comments. Decisions taken to the user and ruled (`ESC-EXEC-20261126-03`): a draft plan's skipped checklist no longer marks the trade broken permanently, and pre-v9.18 events no longer count. Fixed: the behaviour-change list above now covers the Stop pre-tick, the remembered Rules option, "Not known" for older trades, and the navigation changes. Filed: BLG-FE-338. To reconfirm at acceptance: the AI briefing folding on every Dashboard arrival.

### Product Owner and Director of Quality acceptance (the user, in session, 2026-11-27T09:04:29Z)

The user, who holds the Product Owner and Director of Quality roles, gave both in session: Director of Quality "Sign off"; Product Owner "Accept all". Recorded as given:

1. **Accepted:** the AI Daily Briefing card folds into the "Nothing to show" line on every Dashboard arrival (it loads no briefing on mount); the "AI briefing" entry reveals it with Regenerate.
2. **Accepted until v9.19:** BLG-BE-237 — editing a linked plan's checklist after entry changes that trade's rules-followed result, and the edit is not audit-logged.
3. **Accepted:** the other behaviour changes listed above.
4. No P1 or P2 defect was filed during this EPIC; follow-ups BLG-FE-336, BLG-FE-337, BLG-FE-338 and BLG-BE-237 are P3.

## Rulings and decisions recorded during execution

All given by the user in session, holding the named role:

- `ESC-EXEC-20261124-01` (2026-11-24) — Head of UX & Design approval of `design_system.md` v1.28 and `navigation.md` v2.5 (ST-07).
- `ESC-EXEC-20261124-02` (2026-11-24) — Strategy Rules & System Intent Owner confirmation of the `trade_plan.md` v1.30 §6 §13-note amendment (ST-12).
- `ESC-EXEC-20261124-03` (2026-11-24) — Metrics Definitions & Analytics Owner approval of the rules-followed definition (ST-13).
- `ESC-EXEC-20261126-01` (2026-11-26) — Product Owner and Head of UX & Design: `checklist_skipped` counts judgement items only (ST-12, found by first-time-right check 17 before the build).
- `ESC-EXEC-20261126-02` (2026-11-26) — Metrics Definitions & Analytics Owner: plan-time events join through the plan; the evidence date is `positions.created_at` (ST-13, found by the pre-commit review).
- `ESC-EXEC-20261126-03` (2026-11-26) — Product Owner and Metrics Definitions & Analytics Owner: `checklist_skipped` is judged by the linked plan's last saved checklist (judgement items), not by past events, so a draft completed later does not count and pre-v9.18 events no longer matter (ST-13, found by the pre-PR Product Owner review).

## Behaviour changes to note for acceptance

- The AI Daily Briefing card folds on every Dashboard arrival, because it loads no briefing on mount; the "AI briefing" line entry reveals it with Regenerate. This is the approved design (`dashboard-quiet-day` record §2.1, §2.3).
- Card 3 "In Grace Today" showed "No expiry date set" whenever anyone was in grace (it read `grace_end_date`, which no endpoint returns); it now reads "Ends today" / "Next ends in N days" or nothing.
- Positions to Watch counts in-grace positions and drops the "exit zone" wording.
- The Earnings card shows its error, not "No earnings in 7 days", when no dated earnings exist and a lookup failed (the mixed case stays with BLG-FE-333).
- Fewer `checklist_skipped` red flags from now on: the two system items no longer count, including the old heat and stop ticks on pre-v9.18 plans re-saved.
- Trade History and the Journal can differ for one trade: the Journal still lists a past "Checklist Skipped" event, while the trade reads "Followed" when its plan was later saved complete (`ESC-EXEC-20261126-03`). Editing a linked plan's checklist after entry changes the result (BLG-BE-237).
- Trade Plan: "Stop level defined" is no longer pre-ticked from Early Exit Conditions; a plan with exit conditions and no Stop Level shows "✗ Not set".
- Trade History: the Rules option is remembered on the device and re-applied when arriving from the sidebar; "Clear filters" also clears an incoming `?ticker=` filter.
- Trade History: most trades from positions created before 2026-11-04 with no plan snapshot show "Not known"; positions created after that date outside Trade Entry show "Followed" (stated in the definition); today only `pre_entry_override` and `checklist_skipped` can occur as reasons (`stop_prompt_dismissed` and `drawdown_prompt_dismissed` have no writer).
- Navigation: Ticker Universe's URL is `/settings/ticker-universe`; inside Performance, Strategy Benchmark has no sticky filter bar and no section index of its own.

## Follow-ups filed during this EPIC

- BLG-FE-336 (P3) — the palette entry for a Performance section drops `?period=` and does not re-jump to the same section (ST-08 review).
- BLG-FE-337 (P3) — Settings has no unsaved-edit guard; decide in `settings.md` (ST-08 review).
- BLG-FE-338 (P3) — word "Not known" by its reason (no position link, failed evidence) (pre-PR Product Owner review).
- BLG-BE-237 (P3) — record or block checklist edits on a plan linked to a position: under the `ESC-EXEC-20261126-03` rule, re-saving a linked plan's checklist after entry changes the trade's rules result, and the edit is not audit-logged (ST-13 review of the revision).

No P1 or P2 defect was filed during this EPIC.

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object (none added: the new fetches go through `api.*` and `database`/service paths)
- [x] **Strategy values checked:** ST-10 — §6 grace period (grace length 10 days via `grace_service.compute_grace_days_remaining`; the Dashboard reads the server's `grace_period`/`grace_days_remaining`, and 1 day left is "Ends today", Day 10 of 10, as §6.1/§11); ST-12 — §4.2.2 sector concentration, §4.2.4 cash constraint, §4.2.5 sizing validity, §4.2.6 advisory (no new rule, statuses from the existing checks). Other stories touch no stop, grace, ATR, exit or sizing logic.
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-11-27
- Comments: Entered at the explicit direction of the user, who holds the Director of Quality role, in session at 2026-11-27T09:04:29Z, after the pre-PR agent-mediated reviews (Director of Quality ❌ Blocked then cleared; Product Owner ⚠️ Approved with Comments, decisions ruled in `ESC-EXEC-20261126-03`). Results per the Consolidation Block: ST-07 to ST-13 Pass. Frontend-visible changes: every observable AC has Playwright coverage, observed passing in real CI — Playwright E2E 45872238856 on `86130e54` (all shards and both visual jobs; frontend unchanged after it); post-open CI fixes restated: ST-10's two failures (CI Pytest 45456088579, Playwright 45456088330) cleared on `d758184d` (Playwright 45859218434, CI Pytest 45859218389); ST-13's (Playwright 45867564450, CI Pytest 45867564435, 45872238877) cleared on `86130e54`/`518b1214` (Playwright 45872238856; CI Pytest 45897742478, Phase B 7 of 7). Autonomous class unavailable (src/pages and src/components changed). Story-level authority sign-offs, all cleared: Head of UX & Design (ST-07, `ESC-EXEC-20261124-01`), Strategy Rules & System Intent Owner (ST-12, `ESC-EXEC-20261124-02`), Metrics Definitions & Analytics Owner (ST-13, `ESC-EXEC-20261124-03`, `ESC-EXEC-20261126-02`, `-03`), Product Owner and Head of UX & Design (ST-12, `ESC-EXEC-20261126-01`). Follow-ups filed: BLG-FE-336, BLG-FE-337, BLG-FE-338, BLG-BE-237 (all P3).

## Merge Gate Confirmations

To be written when the PR merges (STEP 4).
