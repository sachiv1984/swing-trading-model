Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-17
Cycle: 2026-11-11__release-v9.17

---

# Sprint Close Record — 2026-11-11__release-v9.17

## Sprint Goal

Ship Site Structure & Usability Phase 3 complete (decision-first Positions page with narrow-screen cards, one warning strip and one grace view; the single Journal area; one Performance page; section indexes on Trade Plan and Strategy Benchmark; the semantic colour token sweep), finish Phase 2's Stops moved group, and fix the four v9.16 Trade Plan found defects.

## Items Done

All 20 in-scope ST items are merged to `main` across 7 EPICs and 7 PRs. No story was returned to the backlog or deferred at planning. The count matches the sealed `sprint_backlog.md` ("Scope confirmed: 20 stories across 7 EPICs"), and every `### ST-xx` in `stage4_backlog_slice.md` has an `execution_state.json` entry. Each Commit SHA below is the story's recorded `commit_sha`. For the one delegated story (ST-15), that is the evidence commit. EPICs are listed in merge order.

### EPIC-01 — Site Structure & Usability Phase 3: Positions Redesign (build-and-ship) (PR #2256, merged 2026-11-12T21:07:56Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-01 | Decision-first Positions table | autonomous | `6b475ae0` | `docs/specs/frontend/pages/positions.md#Decision-First Table`; `docs/design/2026-11-11__release-v9.17/positions-decision-first/decision_record.md`; `tests/e2e/positions-decision-first.spec.js` |
| ST-02 | Card layout for Positions on narrow screens | autonomous | `540887b9` | `docs/specs/frontend/pages/positions.md#Responsive Behavior`; `docs/specs/frontend/pages/positions.md#Decision-First Table`; `docs/design/2026-11-11__release-v9.17/positions-decision-first/decision_record.md`; `tests/e2e/positions-decision-cards.spec.js` |
| ST-03 | Combine the four banners above the Positions table into one strip | autonomous | `360bf177` | `docs/specs/frontend/pages/positions.md#Warning Strip`; `docs/design/2026-11-11__release-v9.17/positions-decision-first/decision_record.md`; `tests/e2e/positions-warning-strip.spec.js` |
| ST-04 | Show grace period in one place, linked from the others | autonomous | `d11ff814` | `docs/specs/frontend/pages/positions.md#Grace Period View`; `docs/specs/frontend/pages/dashboard.md#Card 3 — In Grace Today`; `docs/specs/frontend/pages/risk_dashboard.md#5. Component: Grace Period Status Panel`; `docs/design/2026-11-11__release-v9.17/positions-decision-first/decision_record.md`; `tests/e2e/positions-grace-view.spec.js` |

### EPIC-04 — Site Structure & Usability Phase 2 Completion: Stops Moved Group (PR #2257, merged 2026-11-13T09:55:54Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-09 | Record when the nightly job last moved each position's stop | autonomous | `c50dd966` | `docs/specs/data_model.md`; `docs/specs/data_model_positions_dictionary.md`; `docs/specs/api_contracts/position_endpoints.md#GET /positions`; `docs/specs/api_contracts/position_endpoints.md#POST /positions/nightly-stop-update`; `docs/reference/openapi.yaml`; `tests/test_stop_last_moved.py` |
| ST-10 | Today list "Stops moved" group: TL-09 and TL-10 | autonomous | `2d52ac16` | `docs/specs/frontend/pages/dashboard.md#1B. Today List`; `tests/e2e/dashboard-today-list.spec.js` |

### EPIC-07 — Governance, Strategy Copy & Drift Tooling (PR #2258, merged 2026-11-13T12:49:47Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-18 | Release Planning §1.3a: let a gate clearance also set a gate-worded Provisional-Target to TBD | autonomous | `02587c70` | `claude/system/release_planning_prompt.md#1.3a Gate-Detection Procedure (Mandatory, Scripted)`; `claude/system/changelogs/release_planning_changelog.md` |
| ST-19 | Define or remove the 2R Exit Zone threshold the Positions page states | autonomous | `cad3b87f` | `src/pages/Positions.js`; `docs/specs/frontend/pages/positions.md#Position Lifecycle State Badge`; `docs/design/2026-11-11__release-v9.17/positions-decision-first/decision_record.md`; `tests/e2e/lifecycle-badge-grace-calendar-days.spec.js` |
| ST-20 | Stop check_data_model_drift.py reading index names from rollback blocks | autonomous | `6dc668d8` | `scripts/check_data_model_drift.py`; `tests/test_check_data_model_drift.py`; `docs/ops/data_model_drift_runs/README.md`; `docs/ops/data_model_drift_runs/2026-11-13_staging_triage.md` |

### EPIC-06 — Market-Data Reliability & Sizing Correctness (PR #2259, merged 2026-11-13T15:11:51Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-15 | Find out why most on-demand Yahoo calls fail on production (earnings, positions, gap risk, research) | delegated_backend | `c341eee7` | `docs/ops/data_pipeline_cost_baseline.md#4. Weekly Baseline`; `docs/specs/api_contracts/ops_endpoints.md#GET /ops/api-call-attribution`; `docs/specs/api_contracts/earnings_endpoints.md#GET /earnings/{ticker}`; `docs/specs/data_model.md#DS-36 — Attribute provider calls in api_call_log, and time screener runs (v2.65, 2026-10-27)`; `tests/test_yahoo_on_demand_failures.py` |
| ST-16 | Alert when weekly market-data call volume exceeds 2× the baseline | autonomous | `5578c103` | `docs/ops/data_pipeline_cost_baseline.md#5. Advisory Threshold`; `scripts/check_market_data_volume.py`; `.github/workflows/market-data-volume-check.yml`; `tests/test_market_data_volume_check.py` |
| ST-17 | Batch signal sizing can allocate more than available cash once fees are added | autonomous | `7b3b59e8` | `docs/specs/api_contracts/signal_endpoints.md#Field notes`; `docs/specs/qa/strategy_signal_regression_spec.md#Inverse-Volatility Sizing`; `tests/test_signal_sizing.py` |

### EPIC-05 — Trade Plan Found Defects (v9.16 Carry-Forward) (PR #2260, merged 2026-11-16T09:04:48Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-11 | Move a linked trade plan to `closed` when its position closes | autonomous | `ceda52c5` | `docs/specs/data_model.md#DS-41 — Close active trade plans whose linked position is closed (v2.70, 2026-11-13)`; `docs/specs/data_model.md#Trade Plan Lifecycle (`trade_plans.status`)`; `docs/specs/api_contracts/position_endpoints.md#POST /positions/{position_id}/exit`; `tests/test_trade_plan_close_on_exit.py`; `tests/e2e/trade-plan-lifecycle.spec.js` |
| ST-12 | Reset the Trade Plan pre-entry acknowledgement when the check result changes | autonomous | `94dc3bd8` | `docs/specs/frontend/pages/trade_plan.md#5e. Pre-Entry Snapshot on Save`; `docs/design/2026-11-11__release-v9.17/trade-plan-found-defects/decision_record.md#2. Reset the acknowledgement when the result changes`; `tests/e2e/trade-plan-ack-reset.spec.js` |
| ST-13 | Pass the market from Research View's "Create Trade Plan" so a UK plan is not created as US | autonomous | `3d802d1c` | `docs/specs/frontend/pages/research_view.md#4.7 Trade Plan Panel`; `tests/e2e/research-create-plan-market.spec.js` |
| ST-14 | Pre-fill the Trade Plan stop from the §5 suggested stop and flag a typed stop that differs | autonomous | `f2749a24` | `docs/specs/frontend/pages/trade_plan.md#5a.3 Pre-Population Rules (creation form only)`; `docs/specs/frontend/pages/trade_plan.md#5f. Suggested Size Before Shares`; `docs/specs/frontend/pages/trade_plan.md#Known Deviations`; `tests/e2e/trade-plan-stop-prefill.spec.js` |

### EPIC-02 — Site Structure & Usability Phase 3: Journal & Performance Consolidation (build-and-ship) (PR #2261, merged 2026-11-17T09:09:42Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-05 | Build the single Journal area | autonomous | `45243887` | `docs/specs/frontend/pages/journal.md`; `tests/e2e/journal.spec.js` |
| ST-06 | Merge Reports and Performance Analytics into one Performance page | autonomous | `68b0418b` | `docs/specs/frontend/pages/performance.md`; `docs/design/2026-11-11__release-v9.17/performance-page-brief/decision_record.md`; `tests/e2e/performance.spec.js` |
| ST-07 | Use tabs or sections on the long single-scroll pages | autonomous | `44736ed8` | `docs/specs/frontend/pages/trade_plan.md#5g. Section Index`; `docs/specs/frontend/pages/strategy_benchmark.md#3a. Section Index (v0.10)`; `docs/design/2026-11-11__release-v9.17/long-page-section-index/decision_record.md`; `tests/e2e/section-index.spec.js` |

### EPIC-03 — Site Structure & Usability Phase 3: Semantic Colour Token Sweep (build-and-ship) (PR #2262, merged 2026-11-17T14:38:11Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-08 | Move the remaining pages onto the semantic colour tokens | autonomous | `7b4e7736` | `docs/specs/frontend/design_system.md#Page Colour Token Sweep`; `docs/specs/frontend/design_system.md#Semantic Colour Tokens`; `docs/specs/frontend/pages/trade_plan.md`; `docs/specs/frontend/pages/analytics.md`; `tests/e2e/accessibility-axe-scan.spec.js`; `tests/test_page_colour_tokens.py` |

## Items Returned to Backlog

None. No story was returned during the sprint or at close.

## Items Delegated and Outstanding

No story is outstanding. `delegated_items` and `blocked_items` are empty. The one delegation log entry has a terminal outcome:

| Record | Story | Outcome |
|--------|-------|---------|
| `DEL-20261113-01` | ST-15 (EPIC-06) | Unblocked 2026-11-13T13:41:30Z, in session. The Infrastructure & Operations Owner supplied the production `api_call_log` Q1–Q3 output. |

**Post-merge ACs.** All three were marked `post-merge` at the seal, and each has a named tracker (`sprint_planning_prompt.md` STEP 6.2):
- **`BLG-BE-211`** tracks ST-11 AC 2, the production backfill. It is **met**: the backfill ran after PR #2260 merged and closed 3 plans, leaving 0 active plans on closed positions. The item was bannered ✅ COMPLETE on 2026-11-16.
- **`BLG-OPS-217`** tracks ST-15 AC 2 and AC 3: the post-fix production weekly report, and `data_pipeline_cost_baseline.md` §4 updated to match. It is **still open, as planned**, because it needs 7 days of post-fix production data. No banner yet.
- **`BLG-GOV-419`** tracks ST-18 AC 2: the next Release Planning gate scan after a clearance. It is **still open, as planned**. The next Release Planning run that clears a gate will meet it. No banner yet.

## QA Evidence Logs Produced

Every log has a completed DoQ sign-off block with a non-blank date and a `## Merge Gate Confirmations` section that records the merge. Each DoQ sign-off block is agent-mediated (`Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)`). In every EPIC, the human who holds both the Director of Quality and Product Owner roles also gave QA sign-off and PO acceptance explicitly in session before the merge, and then merged the PR (also confirmation by merge, `ESC-CLOSE-20261103-01`).

| EPIC | Log | Sign-off date | Human confirmation and merge |
|------|-----|---------------|------------------------------|
| EPIC-01 | `qa_evidence_EPIC-01.md` | 2026-11-12 | In session 2026-11-12T20:58:29Z; merged `61154853` |
| EPIC-04 | `qa_evidence_EPIC-04.md` | 2026-11-13 | In session 2026-11-13T09:34:47Z; merged `71e86455` |
| EPIC-07 | `qa_evidence_EPIC-07.md` | 2026-11-13 | In session 2026-11-13T11:33:07Z; merged `c7153fba` |
| EPIC-06 | `qa_evidence_EPIC-06.md` | 2026-11-13 | In session 2026-11-13T14:57:46Z; merged `aaeb2957` |
| EPIC-05 | `qa_evidence_EPIC-05.md` | 2026-11-16 | In session 2026-11-16T08:54:06Z; merged `cb65bb12` |
| EPIC-02 | `qa_evidence_EPIC-02.md` | 2026-11-16 | In session 2026-11-17, on head `282050ea`; merged `28fb7239` |
| EPIC-03 | `qa_evidence_EPIC-03.md` | 2026-11-17 | In session 2026-11-17, on head `ff08a481`; merged `3400cba4` |

## Process Notes

Rolled up from `execution_state.json.process_notes` (33 entries, 2026-11-12 to 2026-11-17):

- **CI caught locator collisions on new visible text (EPIC-01).**
  - ST-01: the STEP 3.1.A step 13 grep for new visible text (LL-v9.16-P3-01) was not run before `b2d93f6d`. The new caption and the row chevrons broke SC-COMP-03/07, which was fixed in `6b475ae0`.
  - ST-03: SC-LBG-03 asserted banner body copy that was now inside a collapsed strip entry. The pre-commit grep searched headings, labels and dismiss text but not body copy. Fixed in `360bf177`.
- **Rulings in session on spec premises the code contradicted (EPIC-04).**
  - ST-09: `GET /positions/analyze` also raises stops, so moves are recorded on both paths. The Head of Specs Team and the Data Model owner ruled on this.
  - ST-10: the Stops moved group uses a today-or-previous-weekday window. The Frontend Spec owner and the Head of UX & Design ruled on this. It is recorded as `DEV-EPIC04-ST10-01`.
  - Both were found by the pre-commit `/code-review`.
- **One escalation, resolved in session.** `ESC-EXEC-20261116-01` (ST-06): `performance.md` v1.0 needed Head of UX & Design approval and confirmation of the KPIs by the Metrics owner. Both were given 2026-11-16, about 3 minutes after the escalation was raised.
- **Review rounds.** Every EPIC had an agent-mediated DoQ review, with PO or Head of UX & Design reviews where the user asked for them. Four reviews returned Blocked or Changes Requested at least once, and each finding was fixed on the branch before the human confirmations:
  - EPIC-01: Risk Dashboard grace panel contrast (P2).
  - EPIC-04: spec drift for the `bf6ac67b` rules (P2).
  - EPIC-06: UK pence read as pounds (P2), then stored-data risk.
  - EPIC-03: `BLG-FE-303`.

  At PR review, EPIC-02 found the P2 `BLG-FE-300` and EPIC-05 found a P2 in its own new code. Both were fixed before merge.
- **Visual snapshot baselines (EPIC-03).** The Update Visual Snapshot Baselines workflow cannot push to `exec/**` branches (403, `GITHUB_TOKEN` lacks write access), so the baselines were committed from the run artifact. Filed as `BLG-OPS-220`.
- **Some note timestamps are estimates.** Three EPIC-03 notes are stamped 2026-11-17T15:00Z, 18:00Z and 18:30Z, but PR #2262 merged at 14:38:11Z after all three events. Those timestamps were estimates written at the time, not wall-clock reads. One EPIC-05 note was corrected the same way on 2026-11-16. The events are in the right order: the head commits they cite (`ff08a481`, `bbd0f38d`) come before the merge (Phase 3 friction item).
- **Product Owner direction for v9.18 Release Planning.** Seat `BLG-GOV-422` and `BLG-QA-262` next release, with `BLG-QA-260` (P3, needs a recorded override). Extend `BLG-GOV-422`'s design gate STEP 2.2 checks with the writer check, the competing-value check and the failure-state check from the EPIC-04, EPIC-06 and EPIC-07 retrospectives.
- **Orphaned post-merge commit checks (LL-v6.8-P3-01).** These ran at each merge, and again at this close for EPIC-03: `git log origin/main..origin/exec/2026-11-11__release-v9.17/EPIC-0{1..7}` returned no commits.
- **Sibling-branch sync (STEP 4 step 3c).** Not needed at any merge. Each later EPIC branch was cut from `main` after the previous merge, in the sealed Merge Order.
- **Sprint close (2026-11-17).**
  - The resume-sync found PR #2262 merged and recorded it on `main` in `8626e6fc`.
  - STEP 5.0A confirmed all 7 PRs are `MERGED`.
  - EPIC-02's three stories were normalised from `done` to `merged` to match their merged EPIC.
  - Every `spec_references` path resolves on disk, so no correction was needed.

**System Status Report corrections (STEP 5.1.B):** None needed. The report has no SC-* scenario count cells and no current `execution_prompt.md` version reference to update. Only the new v9.17 section was added (STEP 5.3A).

## Deviations Filed This Sprint

Two canonical-spec `DEV-*` records were filed, both P3. Every merged story's deviation check finished with `deviations_filed = true`.

| Spec file | Deviation ref | Priority | Tracking item |
|-----------|---------------|----------|---------------|
| `docs/specs/frontend/pages/positions.md` | `DEV-EPIC01-ST04-01` (ST-04: the grace view's trade plan block comes from `GET /positions/grace-period-alerts`, which returns only positions with 2 or fewer grace days left) | P3 | `BLG-BE-215` |
| `docs/specs/frontend/pages/dashboard.md` | `DEV-EPIC04-ST10-01` (ST-10: Stops moved is written by both stop recompute paths, and the "latest nightly run date" is read as today or the previous weekday) | P3 | `BLG-SPEC-238` |

Two stories are graded `Pass_with_deviation`. None is P0. The deviation severity matches the DoQ assessments. The tracking item's own `**Priority:**` was read from `backlog.md` (LL-v9.12-P4-01). Found defects filed at P1 or P2 are also listed (LL-v9.13-P4-01), each with its PO and DoQ acceptance record (LL-v9.15-P4-02). Post-merge ACs that were marked at the seal are not deviations (LL-v9.13-P3-03). They are covered under Items Delegated and Outstanding.

| Story | Grade | Gap or found defect | Deviation severity | Tracking item | Tracking item priority | PO + DoQ acceptance |
|-------|-------|---------------------|--------------------|---------------|------------------------|---------------------|
| ST-04 | Pass_with_deviation | The grace view has no trade plan link for in-grace positions with more than 2 grace days left (`DEV-EPIC01-ST04-01`) | P3 | `BLG-BE-215` | P3 | n/a (P3) |
| ST-10 | Pass_with_deviation | The Stops moved data source and window differ from §1B's wording (`DEV-EPIC04-ST10-01`) | P3 | `BLG-SPEC-238` | P3 | n/a (P3) |
| ST-15 | Pass | Found defect: a failed earnings or gap-risk lookup is shown the same as "no upcoming earnings", and the Screener looks up earnings for UK rows | P2 | `BLG-FE-294` | P2 | PO and DoQ, 2026-11-13T14:57:46Z, before the merge (`qa_evidence_EPIC-06.md` Merge Gate Confirmations). Rationale: the display gap existed before this EPIC and is not a regression. ST-15's cache and cap make failed lookups much rarer, and the item is tracked for a later release. **Open.** |
| ST-06 | Pass | Found defect (PR #2261 review): Summary showed £0.00 / 0.0% below the trade minimum | P2 | `BLG-FE-300` | P2 | PO and DoQ, 2026-11-17, before the merge (`qa_evidence_EPIC-02.md` Merge Gate Confirmations). Fixed on the branch in `9e807be8` at the PO's direction and bannered ✅ COMPLETE. Nothing is carried. |
| ST-08 | Pass | Found defect (PR #2262 review): six components were dark-only in page states the scans had not reached | P2 | `BLG-FE-303` | P2 | PO and DoQ, 2026-11-17, before the merge (`qa_evidence_EPIC-03.md` Merge Gate Confirmations). Fixed on the branch in `7b4e7736` (user direction, option (a)) and bannered ✅ COMPLETE. Nothing is carried. |

Three more P2 defects were found in review and fixed on the branch before merge without being filed: EPIC-01's grace panel contrast (`d11ff814`), EPIC-06's UK pence read as pounds (`c341eee7`, with the remaining cases of the same kind in `BLG-BE-217` and `BLG-BE-218`, both P3) and EPIC-05's own-code P2 (`d485d9ca`/`084bdaac`). Each one's QA evidence records it.

**Carried-forward P2s.** This sprint fixes four of the five v9.16 found defects named in the goal: `BLG-BE-211` (ST-11, already bannered after its post-merge backfill), `BLG-FE-278` (ST-12), `BLG-FE-281` (ST-13) and `BLG-FE-282` (ST-14). The last three are each story's own source item and are left for their ✅ COMPLETE banners at post-ship closure STEP 3.1. The fifth, `BLG-OPS-217` (ST-15), has its causes found and fixed in-sprint and stays open for its post-merge report.

**Backlog follow-ups filed during execution.** 49 items carry a `2026-11-11__release-v9.17` source, including the design gate and Sprint Planning filings (`BLG-SPEC-230`, `BLG-SPEC-231`, `BLG-FE-288`). These are out-of-scope findings, not spec deviations. Five are already bannered ✅ COMPLETE on their branches: `BLG-FE-295`, `BLG-FE-296`, `BLG-FE-298`, `BLG-FE-300` and `BLG-FE-303`. Open P2s: `BLG-GOV-422`, `BLG-QA-262` and `BLG-FE-294`.

| Backlog IDs | Filed by | Subject |
|-------------|----------|---------|
| `BLG-SPEC-232`–`236`, `BLG-FE-289`–`293`, `BLG-BE-215`, `BLG-TECH-34`, `BLG-GOV-422`, `BLG-QA-262`, `BLG-TECH-35` | EPIC-01 pre-commit reviews, DoQ and PR #2256 reviews, retrospective | Positions "To stop" basis, shared breach pills, grace display rules, the Compliance panel on narrow screens, splitting `Positions.js`, design gate data-source checks, frontend unit tests in CI |
| `BLG-SPEC-237`, `BLG-SPEC-238`, `BLG-BE-216`, `BLG-QA-263` | EPIC-04 (ST-09, ST-10, PR #2257) | Migration headings, the Stops moved wording, Stop Age, weekend clock tests |
| `BLG-SPEC-239`, `BLG-QA-264`, `BLG-QA-265`, `BLG-GOV-423` | EPIC-07 (ST-19, ST-20, PR #2258) | Exit Zone vs plan R target, the staging index check, drift-check wording, clearing known false positives |
| `BLG-FE-294`, `BLG-BE-217`, `BLG-BE-218` | EPIC-06 (ST-15, DoQ rounds) | "Earnings unknown", UK pence guesses, UK quote currency |
| `BLG-BE-219`–`221`, `BLG-FE-295`–`298` | EPIC-05 (ST-11, PR #2260, post-merge deploy check) | P&L reconciliation, the stored-stop line, a US ATR shown in GBP, false errors from the ensure functions |
| `BLG-FE-299`–`302`, `BLG-QA-266`, `BLG-BE-222` | EPIC-02 (ST-06, PR #2261) | Discipline window, the Performance Summary, section index links, the debounce test, digest link names |
| `BLG-FE-303`–`307`, `BLG-OPS-220`, `BLG-QA-267` | EPIC-03 (ST-08, PR #2262) | Dark-only components, a shared card surface, calendar days, Signal card de-emphasis, the dark heatmap, the baseline workflow push, the token check parser |

## Open Escalations

None for this cycle. `ESC-EXEC-20261116-01`, the only `ESC-EXEC-*` record raised this cycle, is `Resolved` in `execution_escalations.md`, `execution_state.json` and `.claude_current_state.json`. The only unresolved escalation in `.claude_current_state.json` is `ESC-EXEC-20260910-01` (cycle `2026-09-09__release-v9.3`, Deferred, non-blocking), which is not from this cycle.

## Net Outcome vs Sprint Goal

**Met.**
- **Site Structure & Usability Phase 3.** The following shipped:
  - the decision-first Positions page with narrow-screen cards, one warning strip and one grace view (ST-01 to ST-04);
  - the single Journal area (ST-05);
  - one Performance page (ST-06);
  - section indexes on Trade Plan and Strategy Benchmark (ST-07);
  - the semantic colour token sweep across every page (ST-08), with the remaining shared components in `BLG-FE-288` under the RISK-02 boundary.
- **Phase 2's Stops moved group.** Stop moves are recorded, and the group shows on the Today list (ST-09, ST-10).
- **The four v9.16 Trade Plan found defects.** All four are fixed: plans close on exit (ST-11), the acknowledgement resets (ST-12), Research keeps the market (ST-13), and the stop is pre-filled (ST-14).
- **Alongside.** These also shipped:
  - market-data reliability and sizing correctness (EPIC-06, ST-15 to ST-17);
  - governance, strategy copy and drift tooling (EPIC-07, ST-18 to ST-20).

Every commitment in the goal is delivered. What remains open is two post-merge ACs (`BLG-OPS-217`, `BLG-GOV-419`), two P3 deviations, and one pre-existing P2 found defect (`BLG-FE-294`) that the PO and DoQ accepted with a rationale.

## Verification Readiness Statement
| Field | Status |
|-------|--------|
| All spec references populated in execution_state.json | Yes |
| All P1–P3 deviations filed and backlog references updated | Yes |
| QA evidence logs complete and DoQ sign-off non-blank for all EPICs | Yes |
