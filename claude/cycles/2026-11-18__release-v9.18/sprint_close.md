Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-27
Cycle: 2026-11-18__release-v9.18

---

# Sprint Close Record — 2026-11-18__release-v9.18

## Sprint Goal

Ship Site Structure & Usability Phase 4 stages 1–2 (Level A keyboard and label fixes, truthful Telegram alert delivery, a one-line quiet-day Dashboard, the two navigation moves, and a readable, linked Weekly Digest with this week's loop), put the first-time-right checks in place before v9.19's design gate, and make position figures correct across native entry, live FX and stock splits.

## Items Done

All 40 in-scope ST items are merged to `main` across 7 EPICs and 7 PRs. No story was returned to the backlog or deferred at planning. The count matches the sealed `sprint_backlog.md` ("Scope confirmed: 40 stories across 7 EPICs in a single sprint; ST-32 conditional (gate 2026-11-20); none deferred"), and every `### ST-xx` in `stage4_backlog_slice.md` has an `execution_state.json` entry (40 of 40). ST-32's conditional gate passed on 2026-11-20. Each Commit SHA below is the story's recorded `commit_sha`. EPICs are listed in merge order.

### EPIC-01 — Site Structure & Usability Phase 4, Stage 1: Correct and Safe (build-and-ship) (PR #2307, merged 2026-11-19T16:36:27Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-01 | Make the four mouse-only controls keyboard-operable | autonomous | `a89a66b2` | `docs/specs/frontend/design_system.md#Accessibility`; `tests/e2e/keyboard-operable-controls.spec.js`; `tests/e2e/accessibility-axe-scan.spec.js` |
| ST-02 | Link the Exit dialog's labels to their inputs | autonomous | `dc803dc1` | `docs/specs/frontend/design_system.md#Accessibility`; `tests/e2e/accessibility-axe-scan.spec.js` |
| ST-03 | Say Telegram, not email, and show when an alert was not sent | autonomous | `74ff6a5e` | `docs/specs/api_contracts/alerts_endpoints.md#GET /notifications`; `docs/specs/frontend/pages/notifications.md#Notification List`; `docs/design/2026-11-18__release-v9.18/alert-delivery-truth/decision_record.md`; `tests/test_notification_delivery_status.py`; `tests/e2e/notification-delivery-truth.spec.js` |
| ST-04 | Fix Alert History compact values | autonomous | `24e7bc76` | `docs/specs/frontend/pages/notifications.md#Alert History Values (v0.12 — ST-04, BLG-FE-228)`; `docs/design/2026-11-18__release-v9.18/alert-delivery-truth/decision_record.md`; `tests/e2e/alert-history-values.spec.js` |
| ST-05 | Re-review the accepted open-access risk | autonomous | `08d73563` | `docs/operations/credential_policy.md#1.1 Frontend API Key: Write Scope and Accepted Risk` |
| ST-06 | Measure Core Web Vitals and update the performance budget | autonomous | `471ef0aa` | `docs/specs/frontend/performance_budget.md`; `scripts/perf/run_lighthouse.mjs`; `scripts/perf/check_bundle_size.py`; `.github/workflows/lighthouse-ci.yml`; `tests/test_check_bundle_size.py` |

### EPIC-07 — AI Output Boundary (PR #2309, merged 2026-11-23T08:59:23Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-39 | Check daily briefing and chat output against §13.2 | autonomous | `5e91c0e8` | `docs/specs/api_contracts/ai_endpoints.md#POST /ai/daily-briefing`; `docs/specs/api_contracts/ai_endpoints.md#POST /ai/chat`; `docs/specs/qa/ai_s13_boundary_test_suite.md`; `claude/strategy/strategy_rules.md#13.2`; `tests/test_briefing_chat_parameter_change_check.py` |
| ST-40 | Decide whether the debrief may say more than one restating sentence | autonomous | `ad42bc87` | `claude/strategy/strategy_rules.md#13.2`; `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` |

### EPIC-04 — First-Time-Right Checks (Product Owner direction, 2026-11-12) (PR #2311, merged 2026-11-24T08:15:39Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-18 | Design gate data-source, writer and worked-example checks | autonomous | `ec1d6eed` | `claude/system/design_gate_prompt.md#2.2 Design work (if needed)`; `docs/ops/design_gate_preapproval_checks_dry_run_2026-11-23.md` |
| ST-19 | Unit-test pure frontend logic in CI | autonomous | `a71ec3f2` | `src/lib/positionUrgency.test.js`; `src/lib/exitCondition.test.js`; `src/test-utils/knownFailing.js`; `.github/workflows/frontend-unit-tests.yml`; `docs/development/frontend_development_guide.md#14. Unit Tests for Pure Modules` |
| ST-20 | Fail the axe scan on incomplete colour-contrast results | autonomous | `95fc6b9a` | `tests/e2e/accessibility-axe-scan.spec.js#runAxeScan`; `tests/e2e/accessibility-axe-scan.spec.js#SC-AXEINC-01`; `tests/e2e/accessibility-axe-scan.spec.js#SC-AXEINC-02` |
| ST-21 | Script the locator-collision check and run it from commit-check | autonomous | `4c42d06a` | `scripts/check_e2e_locator_collisions.py`; `claude/system/execution_prompt.md#3.1.A step 13`; `.claude/skills/commit-check/SKILL.md#Check 13` |
| ST-22 | Require the pre-commit code review in execution_prompt.md | autonomous | `45018750` | `claude/system/execution_prompt.md#3.1.A step 2c` |
| ST-23 | Enforce the prompt size budget on direct commits to main | autonomous | `7d5e02e0` | `.githooks/pre-commit`; `scripts/check_prompt_size_budget.py`; `.github/workflows/prompt-size-budget.yml`; `claude/system/post_ship_closure.md#STEP 8`; `claude/system/roadmap_prompt.md#STEP 11 write scope`; `tests/test_check_prompt_size_budget.py` |
| ST-24 | Count an item as shipped only on a ✅ COMPLETE banner line | autonomous | `f9088b0a` | `scripts/scan_backlog_gate_conditions.py`; `tests/test_scan_backlog_gate_conditions_gating_item_shipped.py` |

### EPIC-05 — Position Data Correctness (PR #2310, merged 2026-11-24T08:39:33Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-25 | Use one native-entry function on every position path | autonomous | `31c4537a` | `docs/specs/data_model_positions_dictionary.md`; `tests/test_fx_market_matrix.py` |
| ST-26 | Use the live FX rate, not a hard-coded 1.27 | autonomous | `eea7511f` | `docs/specs/api_contracts/position_endpoints.md#GET /positions/compliance`; `tests/test_fx_market_matrix.py` |
| ST-27 | Handle a stock split on an open position | autonomous | `bcb13736` | `claude/strategy/strategy_rules.md#9.1 Stock split on an open position`; `docs/specs/data_model.md#DS-42`; `docs/specs/api_contracts/position_endpoints.md#POST /positions/{position_id}/split-adjustment/confirm`; `docs/specs/frontend/pages/positions.md#Split Detected State`; `tests/test_stock_split_adjustment.py`; `tests/e2e/positions-split-detected.spec.js` |
| ST-28 | Tag lifecycle transitions caused by the v9.12 currency correction | autonomous | `05bef324` | `docs/specs/data_model.md#Lifecycle Transition Reasons`; `tests/test_lifecycle_basis_correction.py` |
| ST-29 | Keep GET /settings working when the change-log read fails | autonomous | `21a0df09` | `docs/specs/api_contracts/settings_endpoints.md#GET /settings`; `tests/test_settings_change_log.py` |
| ST-30 | Make the Reports unrealised P&L match the Positions basis | autonomous | `729a9f62` | `docs/specs/frontend/pages/reports.md#Unrealised P&L Card`; `docs/specs/api_contracts/reports_endpoints.md#GET /reports/tax-year`; `tests/e2e/reports-unrealised-live-basis.spec.js`; `tests/test_reports_integration.py` |
| ST-31 | Cache the Trade Entry ATR preview per ticker and market | autonomous | `315887ec` | `docs/specs/frontend/components/position_form.md#ATR (14-day)`; `tests/e2e/trade-entry-atr-preview.spec.js` |

### EPIC-06 — Market-Data Reliability and CI (PR #2312, merged 2026-11-24T14:14:07Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-32 | Finish the on-demand Yahoo failure diagnosis (remainder) | delegated_backend | `229a851b` | `docs/ops/data_pipeline_cost_baseline.md#4. Weekly Baseline` |
| ST-33 | Show "earnings unknown" when an earnings or gap-risk lookup fails | autonomous | `b865cad4` | `docs/specs/api_contracts/earnings_endpoints.md#GET /earnings/{ticker}`; `docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/gap-risk`; `docs/specs/frontend/pages/positions.md#Earnings Unknown (v2.30 — ST-33, BLG-FE-294)`; `docs/specs/frontend/pages/screener_results.md`; `docs/specs/frontend/pages/watchlist.md#Earnings Cell (v0.11 — ST-33, BLG-FE-294)`; `tests/e2e/earnings-unknown.spec.js` |
| ST-34 | Let the visual-baseline workflow push regenerated snapshots | autonomous | `b6f03ef4` | `.github/workflows/update-visual-snapshots.yml` |
| ST-35 | Seed staging's UK positions with the .L suffix | delegated_backend | `e0879873` | `tests/test_seed_uk_ticker_suffix.py`; `scripts/seeds/seed_portfolio_trades.sql` |
| ST-36 | Build the E2E bundle once per Playwright run | autonomous | `bb821fe2` | `.github/workflows/playwright.yml`; `playwright.config.js`; `scripts/build_e2e_bundle.js` |
| ST-37 | Keep a bare root pytest out of the mutmut pilot tests | autonomous | `400a4395` | `conftest.py`; `backend/setup.cfg` |
| ST-38 | Run the settings change-log SQL against real Postgres in CI | autonomous | `1781aa29` | `tests/test_settings_change_log_postgres.py`; `docs/specs/data_model.md#DS-33 — Add settings_change_log (v2.62, 2026-10-15)` |

### EPIC-02 — Site Structure & Usability Phase 4, Stage 2: Home Page and Navigation (build-and-ship) (PR #2313, merged 2026-11-27T09:12:41Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-07 | Revise navigation.md and design_system.md for the Phase 4 target state | autonomous | `4460bf5f` | `docs/specs/frontend/design_system.md#Design Direction`; `docs/specs/frontend/pages/navigation.md` |
| ST-08 | Move Strategy Benchmark into Performance and Ticker Universe into Settings | autonomous | `874ffedf` | `docs/specs/frontend/pages/navigation.md#Page Placement`; `docs/specs/frontend/pages/performance.md#4.1 Strategy vs Backtest Section (v1.3 — ST-08, BLG-FE-323)`; `docs/specs/frontend/pages/strategy_benchmark.md`; `docs/specs/frontend/pages/ticker_universe.md`; `docs/specs/frontend/pages/settings.md#3. Preferences` |
| ST-09 | Make the quiet-day Dashboard a single line | autonomous | `0125538c` | `docs/specs/frontend/pages/dashboard.md#Quiet-Day Collapse (v4.4 — ST-09, BLG-UX-11)` |
| ST-10 | Use one grace-period definition across the Dashboard | autonomous | `8ff17e93` | `docs/specs/frontend/pages/dashboard.md#4B. One Grace Definition (v4.4 — ST-10, BLG-FE-308)`; `docs/specs/frontend/pages/risk_dashboard.md` |
| ST-11 | Offer "Plan this" on the Today list's New signals rows | autonomous | `d758184d` | `docs/specs/frontend/pages/dashboard.md#1B. Today List`; `docs/specs/frontend/pages/signals.md` |
| ST-12 | Show machine-checkable checklist items as automatic status | autonomous | `d5b2acc3` | `docs/specs/frontend/pages/trade_plan.md#6. Pre-Trade Entry Checklist (v3.2 — PT-05; split v1.30 — ST-12, BLG-UX-19)`; `docs/specs/api_contracts/red_flag_journal.md` |
| ST-13 | Filter Trade History and Journal by rules followed or broken | autonomous | `518b1214` | `docs/specs/metrics_definitions.md#Rules Followed (per closed trade)`; `docs/specs/api_contracts/trade_endpoints.md#GET /trades`; `docs/specs/frontend/pages/trade_history.md#Rules Filter (v1.18 — ST-13, BLG-FE-320)` |

### EPIC-03 — Site Structure & Usability Phase 4, Stage 2: Weekly Review Loop (build-and-ship) (PR #2314, merged 2026-11-27T17:05:08Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-14 | Rename the Weekly Digest's journal completion figure | autonomous | `a5438839` | `docs/specs/api_contracts/digest_endpoints.md#GET /digest/weekly`; `docs/specs/metrics_definitions.md#Journal Completion Rate`; `docs/specs/frontend/pages/weekly_digest.md`; `tests/test_weekly_digest_data.py`; `tests/test_weekly_digest_postgres.py`; `tests/e2e/weekly-digest.spec.js` |
| ST-15 | Rewrite the Weekly Digest as a readable weekly summary | autonomous | `d64cc465` | `docs/specs/frontend/pages/weekly_digest.md`; `src/lib/weeklyDigest.js`; `src/lib/weeklyDigest.test.js`; `tests/e2e/weekly-digest.spec.js` |
| ST-16 | Link the Weekly Digest figures to their pages | autonomous | `d64cc465` | `docs/specs/frontend/pages/weekly_digest.md`; `docs/specs/frontend/pages/navigation.md#Onward Links`; `docs/specs/api_contracts/digest_endpoints.md#GET /digest/weekly`; `tests/e2e/weekly-digest.spec.js`; `tests/test_weekly_digest_data.py`; `tests/test_weekly_digest_postgres.py` |
| ST-17 | Measure the core loop and show this week's loop on the Weekly Digest | autonomous | `544ebe49` | `docs/specs/metrics_definitions.md#Core Loop Metrics`; `docs/specs/api_contracts/digest_endpoints.md#POST /digest/events`; `docs/specs/data_model.md#DS-43`; `docs/specs/frontend/pages/weekly_digest.md`; `docs/specs/frontend/pages/dashboard.md`; `tests/e2e/weekly-digest.spec.js`; `tests/e2e/dashboard-today-list.spec.js`; `tests/test_digest_events_router.py`; `tests/test_weekly_digest_postgres.py` |
## Items Returned to Backlog

None. No story was returned during the sprint or at close.

## Items Delegated and Outstanding

No story is outstanding. `delegated_items` and `blocked_items` are empty. All three delegation log entries have a terminal outcome:

| Record | Story | Outcome |
|--------|-------|---------|
| `DEL-20261120-01` | ST-40 (EPIC-07) | Unblocked 2026-11-20T14:14:19Z, in session. The AI Compliance & Governance Officer generated and supplied 10 production v1.1 debriefs. |
| `DEL-20261124-01` | ST-32 (EPIC-06) | Unblocked 2026-11-24, in session. The Infrastructure & Operations Owner supplied the production weekly attribution report and the `GET /positions` Yahoo call read. |
| `DEL-20261124-02` | ST-35 (EPIC-06) | Unblocked 2026-11-24, in session. The production read found no UK row without `.L` (no UPDATE run), and the user supplied the staging `GET /positions` UK rows (`price_is_stale: false`). |

**Post-merge ACs.** The sealed plan named three trackers (`sprint_planning_prompt.md` STEP 6.2), and one more was set during execution:
- **`BLG-OPS-217`** tracks ST-32 AC 2 and AC 3. It is **met**: conditional story ST-32 recorded the post-fix production weekly report (Yahoo failures 665 → 21 a week) and re-recorded `data_pipeline_cost_baseline.md` §4 v1.4 (`qa_evidence_EPIC-06.md`, 2026-11-24). Bannered ✅ COMPLETE at this close (LL-v9.16-P3-06).
- **`BLG-GOV-378`** tracks ST-40 AC 1 if the production sample was not available in-sprint. The sample was supplied in-sprint, so AC 1 was met (`qa_evidence_EPIC-07.md`, 2026-11-20). Bannered ✅ COMPLETE at this close.
- **`BLG-GOV-421`** tracks ST-23 AC 3: the next post-ship closure raises no prompt size baseline in a later PR. It is **still open, as planned**. Post-ship closure `2026-11-18__release-v9.18` is the first run that can meet it.
- **`BLG-QA-276`** tracks ST-30 AC 1, the staging check that the Reports and Positions unrealised P&L match at the same moment. The Product Owner moved it post-merge on 2026-11-23, and it was filed before PR #2310 opened. It is **still open** (Provisional-Target v9.18 post-merge). ST-30 is graded `Pass_with_deviation` for it (below).

## QA Evidence Logs Produced

Every log has a completed DoQ sign-off block with a non-blank date and a `## Merge Gate Confirmations` section that records the merge. Each DoQ sign-off block is agent-mediated (`Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)`). In every EPIC, the human who holds both the Director of Quality and Product Owner roles gave QA sign-off and PO acceptance in session, and then merged the PR (also confirmation by merge, `ESC-CLOSE-20261103-01`). For EPIC-01, the in-session confirmation arrived 67 seconds after the merge; the merge itself counts as confirmation.

| EPIC | Log | Sign-off date | Human confirmation and merge |
|------|-----|---------------|------------------------------|
| EPIC-01 | `qa_evidence_EPIC-01.md` | 2026-11-19 | Merged `3a07684e` 2026-11-19T16:36:27Z; in session 2026-11-19T16:37:34Z |
| EPIC-07 | `qa_evidence_EPIC-07.md` | 2026-11-20 | In session 2026-11-20T16:38:02Z; merged `a83f8595` |
| EPIC-04 | `qa_evidence_EPIC-04.md` | 2026-11-23 | In session 2026-11-24T07:59:51Z; merged `7f07c18e` |
| EPIC-05 | `qa_evidence_EPIC-05.md` | 2026-11-23 | In session 2026-11-23T15:05:40Z; merged `97cdd2de` |
| EPIC-06 | `qa_evidence_EPIC-06.md` | 2026-11-24 | In session 2026-11-24; merged `7c7bea76` |
| EPIC-02 | `qa_evidence_EPIC-02.md` | 2026-11-27 | In session 2026-11-27T09:04:29Z; merged `81d7155b` |
| EPIC-03 | `qa_evidence_EPIC-03.md` | 2026-11-27 | In session 2026-11-27T16:43:07Z; merged `43d01fc4` |

## Process Notes

Rolled up from `execution_state.json.process_notes` (32 entries, 2026-11-19 to 2026-11-27):

- **Sprint start left `main` without the state file (EPIC-01).** `main` carried `Executing` while `execution_state.json` existed only on the EPIC-01 branch, failing `test_execution_state_path_file_exists` on PR #2306. Fixed at the user's direction (`f4b642d3`) and filed as `BLG-GOV-430` (P2, v9.19). Since PR #2308 the pre-commit hook blocks the failing commit.
- **Out-of-sprint fix (EPIC-01).** `BLG-FE-325` (CSP redirect script, found in ST-06) was fixed in PR #2306 at the Product Owner's direction and bannered after EPIC-01 merged.
- **Early staging data correction (EPIC-01 / EPIC-06).** The user renamed the two staging UK positions to `BARC.L`/`LGEN.L` on 2026-11-19 so ST-04's staging check could run; ST-35's seed fix and AC 2 followed in EPIC-06.
- **Nine escalations, all resolved in session.** Every `ESC-EXEC-*` raised this cycle was a Lifecycle owner ruling (ST-05, ST-39, ST-40, ST-07, ST-12, ST-13 ×3, ST-17), resolved by the user in the owning role, most within minutes. None blocked execution past its SLA.
- **Review rounds.** EPIC-07 reached the §5.3 retry limit after three DoQ review rounds; the user directed sign-off on the round-3 fix (`0c442abe`). EPIC-04's head commit `a82923c8` fixed DoQ finding 1 (locator-collision script noise, P2).
- **Backlog ID collision between open branches (EPIC-04 / EPIC-05).** Four IDs filed on EPIC-04 were already used on the open EPIC-05 branch and were renumbered before acceptance: `BLG-SPEC-243→244`, `BLG-QA-276→280`, `BLG-QA-277→281`, `BLG-FE-329→332`. `BLG-QA-279` now covers this case.
- **Merge order and the one cross-EPIC merge.** The sealed Merge Order was kept. EPIC-05's PR waited for EPIC-04, then `main` was merged into it (`dd27391c`, CLAUDE.md §8: `backlog.md` rebuilt from both parents, `execution_state.json` merged as data). Every other branch was cut from `main` after the previous merge.
- **Issue auto-close skipped (EPIC-03).** `governance_sync` did not close #2279 because ST-14's own commit recorded it `in_progress`; the engine closed it after CI passed, and later stories got a state commit carrying their tag.
- **Flaky scenario found in another EPIC's code (EPIC-03).** SC-RF-08 (`rules-filter.spec.js`, EPIC-02) failed once in EPIC-03's CI and reproduces about 1 run in 4 on `main`; filed as `BLG-FE-339` (P2), accepted for v9.19.
- **Orphaned post-merge commit checks (LL-v6.8-P3-01).** Run at each merge and again at this close for EPIC-03: `git log origin/main..origin/exec/2026-11-18__release-v9.18/EPIC-0{1..7}` returned no commits.
- **Sibling-branch sync (STEP 4 step 3c).** Not needed at any merge: no later EPIC branch existed when each merge happened, except EPIC-05, which was synced by the merge above.
- **Sprint close (2026-11-27).**
  - The resume-sync found PR #2314 merged and recorded it on `main` in `d30c49a3`, with EPIC-03's Merge Gate Confirmations (confirmed by merge).
  - That note was first written with an estimated time (17:20:00Z, after the clock time); it was corrected at this close to the commit's git time, 2026-11-27T17:07:06Z (§9.2, LL-v9.17-P3-04; Phase 3 friction item).
  - STEP 5.0A confirmed all 7 PRs `MERGED`. Every `spec_references` path resolves on disk, so no correction was needed. No unpushed commits on any EPIC branch.

**System Status Report corrections (STEP 5.1.B):** None needed. The report has no SC-* scenario count cells and no current `execution_prompt.md` version reference to update. Only the new v9.18 section was added (STEP 5.3A).

## Deviations Filed This Sprint

Two canonical-spec `DEV-*` records were filed, both P3 and both accepted as-is by Product Owner ruling. Every merged story's deviation check finished with `deviations_filed = true`.

| Spec file | Deviation ref | Priority | Tracking item |
|-----------|---------------|----------|---------------|
| `docs/specs/frontend/pages/positions.md` (also `screener_results.md`, `watchlist.md`) | `DEV-EPIC06-ST33-01` (ST-33: a failed earnings lookup is held 60 seconds, then retried, not retried on every render) | P3 | None — accepted as-is (Product Owner ruling, 2026-11-24); fold the wording into §Earnings Unknown at the next design gate touching it |
| `docs/specs/frontend/pages/positions.md` | `DEV-EPIC06-ST33-02` (ST-33: the expanded row shows "Unknown" under its "Earnings" label, not "Earnings: unknown") | P3 | None — accepted as-is (Product Owner ruling, 2026-11-24) |

Two stories are graded `Pass_with_deviation`. None is P0. The deviation severity matches the DoQ assessments. Each tracking item's own `**Priority:**` was read from `backlog.md` (LL-v9.12-P4-01). Found defects filed at P1 or P2 are also listed (LL-v9.13-P4-01), each with its PO and DoQ acceptance record (LL-v9.15-P4-02). No P1 was filed this cycle.

| Story | Grade | Gap or found defect | Deviation severity | Tracking item | Tracking item priority | PO + DoQ acceptance |
|-------|-------|---------------------|--------------------|---------------|------------------------|---------------------|
| ST-30 | Pass_with_deviation | AC 1 staging match moved post-merge by the Product Owner (2026-11-23) | P3 | `BLG-QA-276` | P3 | n/a (P3) |
| ST-33 | Pass_with_deviation | `DEV-EPIC06-ST33-01`, `DEV-EPIC06-ST33-02` | P3 | — (accepted as-is) | — | n/a (P3) |
| ST-05 | Pass | ST-05's own remedies (AC 2): access control in front of the site and API; `noindex` and robots.txt | P2 | `BLG-SEC-48`, `BLG-SEC-49` | P2, P2 | PO and DoQ, 2026-11-19T16:37:34Z (`qa_evidence_EPIC-01.md` Merge Gate Confirmations). `BLG-SEC-48` v9.20 (M-sized infrastructure); `BLG-SEC-49` earliest v9.19 slot (under 1 h, cuts discoverability meanwhile). **Open.** |
| — (EPIC-01 process, PR #2306 CI) | — | Process finding: sprint start sets `Executing` on `main` without the state file | P2 | `BLG-GOV-430` | P2 | PO and DoQ, 2026-11-19T16:37:34Z. Accepted v9.19, before the next sprint start; the pre-commit hook blocks the failure meanwhile. **Open.** |
| ST-39 | Pass with notes | Found defect (PR #2309 review): Dashboard briefing "Ask the AI" sends a string `context` and is rejected | P2 | `BLG-FE-328` | P2 | PO and DoQ, 2026-11-20T16:38:02Z (`qa_evidence_EPIC-07.md`). Pre-existing since ST-12; the floating chat works. Accepted v9.19. **Open.** |
| ST-40 | Pass | Found defects from the debrief sample: R basis mismatch; focus sentence dropped on went-to-plan trades; duplicate INTC `trade_history` row | P2 | `BLG-BE-226`, `BLG-AI-35`, `BLG-BE-228` | P2, P2, P2 | PO and DoQ, 2026-11-20T16:38:02Z (`qa_evidence_EPIC-07.md`). All pre-existing; each needs a ruling, logging or the user's go-ahead first. Accepted v9.19; `BLG-BE-228` kept at P2 (P1 recommendation not taken up). **Open.** |
| ST-20 | Pass | Follow-up (PR #2311 review): triage non-strict axe scans' page-content incomplete contrast | P2 | `BLG-QA-281` | P2 | PO and DoQ, 2026-11-24T07:59:51Z (`qa_evidence_EPIC-04.md`). Not an ST-20 AC gap; widens the strict set. Accepted v9.19. **Open.** |
| ST-27 | Pass with notes | Found defect: View Trail compared a US position's GBP entry with its USD price | P2 | `BLG-BE-229` | P2 | PO and DoQ, 2026-11-23T15:05:40Z (`qa_evidence_EPIC-05.md`). Fixed on the branch in `bcb13736` and bannered ✅ COMPLETE. Nothing is carried. |
| ST-27 | Pass with notes | Product gap (PR #2310 review): no notification when a split is detected | P2 | `BLG-BE-231` | P2 | PO and DoQ, 2026-11-23T15:05:40Z. Accepted as a follow-up, target TBD; a detected split pauses that stop until Positions is opened. **Open.** |
| ST-32 | Pass with notes | Found defect: the weekly market-data volume check times out on the production report | P2 | `BLG-OPS-223` | P2 | PO and DoQ, 2026-11-24 (`qa_evidence_EPIC-06.md`). It fails loudly with a Telegram message, and the report was obtained by hand. **Open.** |
| ST-15 / ST-16 | Pass | Found defect (EPIC-03 CI): Trade History does not always restore the stored rules option (EPIC-02 code; SC-RF-08 flaky on `main`) | P2 | `BLG-FE-339` | P2 | PO and DoQ, 2026-11-27 (`qa_evidence_EPIC-03.md` Decisions item 4 and Merge Gate Confirmations). Pre-existing, about 1 run in 4, no data loss. Accepted v9.19. **Open.** |

One more P2 was found in review and fixed on the branch before merge without being filed: EPIC-04's DoQ finding 1, locator-collision script noise (`a82923c8`, 249 → 18 hits). `BLG-GOV-431` (P2, v9.19) is a process item from the EPIC-07 retrospective, not a found defect.

**Carried-forward P2s.** This sprint ships the first-time-right items the Product Owner directed on 2026-11-12 (`BLG-GOV-422` ST-18, `BLG-QA-262` ST-19, `BLG-QA-260` ST-20) and the P2 position-correctness items `BLG-BE-208`, `BLG-BE-213` and `BLG-BE-223` (EPIC-05). These are each story's source item and are left for their ✅ COMPLETE banners at post-ship closure STEP 3.1.

**Backlog follow-ups filed during execution.** 59 items carry a `2026-11-18__release-v9.18` source. These are out-of-scope findings, not spec deviations; four (`BLG-SPEC-241`, `BLG-BE-224`, `BLG-UX-22`, `BLG-QA-274`) are design gate observations filed at Sprint Planning. Six are already bannered ✅ COMPLETE: `BLG-FE-325`, `BLG-BE-229`, `BLG-BE-234`, `BLG-FE-335`, `BLG-BE-235` and `BLG-BE-236`. Open P2s: `BLG-SEC-48`, `BLG-SEC-49`, `BLG-GOV-430`, `BLG-GOV-431`, `BLG-FE-328`, `BLG-BE-226`, `BLG-AI-35`, `BLG-BE-228`, `BLG-BE-231`, `BLG-QA-281`, `BLG-OPS-223` and `BLG-FE-339`.

| Backlog IDs | Filed by | Subject |
|-------------|----------|---------|
| `BLG-SPEC-241`, `BLG-BE-224`, `BLG-UX-22`, `BLG-QA-274` | Design gate, filed at Sprint Planning | Design gate observations for filing |
| `BLG-SEC-48`, `BLG-SEC-49`, `BLG-FE-325`–`327`, `BLG-GOV-430`, `BLG-SPEC-242`, `BLG-BE-225` | EPIC-01 (ST-03 to ST-06, PRs #2306/#2307) | Access control, CSP, Telegram wording, state file at sprint start, notification statuses |
| `BLG-AI-34`–`40`, `BLG-BE-226`–`228`, `BLG-FE-328`, `BLG-GOV-431`, `BLG-QA-275` | EPIC-07 (ST-39, ST-40, PR #2309) | §13.2 detector coverage, debrief R basis and focus sentence, duplicate trade row, in-card chat, sampling real AI output |
| `BLG-SPEC-244`, `BLG-QA-278`–`281`, `BLG-FE-332` | EPIC-04 (ST-18 to ST-23, PR #2311) | Design-gate strip states, ID checks across branches, the ESLint Jest override, axe contrast triage, shell contrast |
| `BLG-QA-276`, `BLG-QA-277`, `BLG-BE-229`–`232`, `BLG-FE-329`–`331`, `BLG-SPEC-243` | EPIC-05 (ST-27, ST-30, PR #2310) | Staging P&L match, View Trail currency, split notification and display, split follow-ups |
| `BLG-OPS-223`, `BLG-QA-282`–`284`, `BLG-FE-333`–`335`, `BLG-BE-233`–`236` | EPIC-06 (ST-32 to ST-37, PR #2312) | Volume check timeout, mutmut pilot, seed sweep, Phase B database guard, earnings callers, UK watchlist signals, DoQ review findings |
| `BLG-FE-336`–`338`, `BLG-BE-237` | EPIC-02 (ST-08, ST-13, PR #2313) | Navigation follow-ups, rules-filter data |
| `BLG-BE-238`, `BLG-BE-239`, `BLG-FE-339` | EPIC-03 (ST-14 to ST-16, PR #2314) | Realised P&L window, UTC analytics cutoffs, Trade History rules restore |

## Open Escalations

None for this cycle. All nine `ESC-EXEC-*` records raised this cycle (`ESC-EXEC-20261119-01`, `-20261120-01`, `-20261120-02`, `-20261124-01` to `-03`, `-20261126-01` to `-03`, `-20261127-01`) are `Resolved` in `execution_escalations.md`, `execution_state.json` and `.claude_current_state.json`. The only unresolved escalation in `.claude_current_state.json` is `ESC-EXEC-20260910-01` (cycle `2026-09-09__release-v9.3`, Deferred, non-blocking), which is not from this cycle.

## Net Outcome vs Sprint Goal

**Met.**
- **Site Structure & Usability Phase 4, stage 1 (EPIC-01, EPIC-02).** The following shipped:
  - Level A keyboard and label fixes on the Daily Monitor exit rows, Exit dialog and Alert History (ST-01, ST-02);
  - truthful Telegram alert delivery and correct Alert History values (ST-03, ST-04);
  - the dated open-access re-review (ST-05) and Core Web Vitals budgets in CI (ST-06);
  - the design direction, the two navigation moves, the one-line quiet-day Dashboard, one grace definition, "Plan this" from New signals, the split entry checklist and the rules filter (ST-07 to ST-13).
- **Stage 2 (EPIC-03).** The Weekly Digest is a readable, linked weekly summary with this week's core loop (ST-14 to ST-17).
- **First-time-right checks before v9.19's design gate (EPIC-04).** Design gate pre-approval checks, frontend unit tests in CI, stricter axe contrast, the locator-collision check, commit-check before every commit, the prompt size budget on direct-to-main commits and the gate-scan banner fix (ST-18 to ST-24).
- **Position figures correct (EPIC-05).** Native entry, live FX for NULL rates and stock-split adjustment, with basis corrections, settings resilience, live unrealised P&L on Reports and the ATR preview (ST-25 to ST-31).
- **Alongside.** Market-data reliability and CI (EPIC-06, ST-32 to ST-38) and the AI output boundary check on the briefing and chat with the debrief length decision (EPIC-07, ST-39, ST-40).

Every commitment in the goal is delivered. What remains open is two post-merge ACs (`BLG-GOV-421`, `BLG-QA-276`), two P3 deviations accepted as-is, and twelve P2 follow-ups that the PO and DoQ accepted with a rationale (two of them, `BLG-SEC-48`/`BLG-SEC-49`, are ST-05's own planned remedies).

## Verification Readiness Statement
| Field | Status |
|-------|--------|
| All spec references populated in execution_state.json | Yes |
| All P1–P3 deviations filed and backlog references updated | Yes |
| QA evidence logs complete and DoQ sign-off non-blank for all EPICs | Yes |
