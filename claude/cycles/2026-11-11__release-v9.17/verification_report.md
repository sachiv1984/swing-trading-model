Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active — Signed off
Last Updated: 2026-11-17
Cycle: 2026-11-11__release-v9.17

---

# Delivery Verification Report — 2026-11-11__release-v9.17

## 1. Verification Status

```
Status: Verified_with_deviations
Sprint goal: Ship Site Structure & Usability Phase 3 complete (decision-first Positions page with narrow-screen cards, one warning strip and one grace view; the single Journal area; one Performance page; section indexes on Trade Plan and Strategy Benchmark; the semantic colour token sweep), finish Phase 2's Stops moved group, and fix the four v9.16 Trade Plan found defects.
Cycle: 2026-11-11__release-v9.17
Backlog slice source: claude/cycles/2026-11-11__release-v9.17/stage4_backlog_slice.md (read with its additive stage4_backlog_slice_addendum.md; no amended_backlog_slice_path)
Verification run: 2026-11-17T15:34:25Z
Mode: standard
```

All 20 stories are merged. There is no P0 deviation, no open P1, no `Fail` result and no traceability gap. Two P3 canonical-spec deviations are recorded (`DEV-EPIC01-ST04-01`, `DEV-EPIC04-ST10-01`). One P2 found defect is still open, `BLG-FE-294`, and the Product Owner and Director of Quality accepted it with a rationale before the EPIC-06 merge. Two other P2 found defects, `BLG-FE-300` and `BLG-FE-303`, were fixed on their EPIC branches before merge. Two seal-marked post-merge ACs are still open, as planned (`BLG-OPS-217`, `BLG-GOV-419`). A third, `BLG-BE-211`, is met.

**Preflight (STEP -1).**
- Branch `main`, in sync with `origin/main`.
- `execution_state.json` is `sealed: true`. This is a single-file cycle, with no `execution_state/` directory.
- `.claude_current_state.json` status is `Sprint_Complete`. The lifecycle guard passes.
- There is no amended slice, and the slice pointer matches `execution_state.json.backlog_slice_source` (the stage 4 slice, read with its addendum).
- `sprint_close.md` Verification Readiness Statement: all three fields are `Yes`.
- All 7 merged EPICs have a QA evidence log signed `Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)`, which is a compliant format. Each log is dated, has every checkbox ticked, and has a `## Merge Gate Confirmations` section recording the human DoQ/PO confirmation and the merge.
- All 7 EPICs have a non-null `pr_number`. GitHub shows each PR (#2256 to #2262) as `MERGED`, at the times recorded in `sprint_close.md`.
- All required input files in Section 4 are present.

## 2. Traceability Matrix

| ST Item | Title | Outcome | Spec Reference | Backlog Entry |
|---------|-------|---------|----------------|---------------|
| ST-01 | Decision-first Positions table | merged | `positions.md#Decision-First Table`; `positions-decision-first.spec.js` | N/A |
| ST-02 | Card layout for Positions on narrow screens | merged | `positions.md#Responsive Behavior`; `positions-decision-cards.spec.js` | N/A |
| ST-03 | Combine the four banners above the Positions table into one strip | merged | `positions.md#Warning Strip`; `positions-warning-strip.spec.js` | N/A |
| ST-04 | Show grace period in one place, linked from the others | merged | `positions.md#Grace Period View`; `dashboard.md#Card 3`; `risk_dashboard.md#5`; `positions-grace-view.spec.js` | N/A |
| ST-05 | Build the single Journal area | merged | `journal.md`; `journal.spec.js` | N/A |
| ST-06 | Merge Reports and Performance Analytics into one Performance page | merged | `performance.md`; `performance-page-brief/decision_record.md`; `performance.spec.js` | N/A |
| ST-07 | Use tabs or sections on the long single-scroll pages | merged | `trade_plan.md#5g`; `strategy_benchmark.md#3a`; `section-index.spec.js` | N/A |
| ST-08 | Move the remaining pages onto the semantic colour tokens | merged | `design_system.md#Page Colour Token Sweep`, `#Semantic Colour Tokens`; `accessibility-axe-scan.spec.js`; `test_page_colour_tokens.py` | N/A |
| ST-09 | Record when the nightly job last moved each position's stop | merged | `data_model.md` DS-40; `position_endpoints.md#GET /positions`, `#POST /positions/nightly-stop-update`; `openapi.yaml`; `test_stop_last_moved.py` | N/A |
| ST-10 | Today list "Stops moved" group: TL-09 and TL-10 | merged | `dashboard.md#1B. Today List`; `dashboard-today-list.spec.js` | N/A |
| ST-11 | Move a linked trade plan to `closed` when its position closes | merged | `data_model.md` DS-41, §Trade Plan Lifecycle; `position_endpoints.md#POST /positions/{position_id}/exit`; `test_trade_plan_close_on_exit.py` | N/A |
| ST-12 | Reset the Trade Plan pre-entry acknowledgement when the check result changes | merged | `trade_plan.md#5e`; `trade-plan-found-defects/decision_record.md#2`; `trade-plan-ack-reset.spec.js` | N/A |
| ST-13 | Pass the market from Research View's "Create Trade Plan" | merged | `research_view.md#4.7`; `research-create-plan-market.spec.js` | N/A |
| ST-14 | Pre-fill the Trade Plan stop from the §5 suggested stop | merged | `trade_plan.md#5a.3`, `#5f`, `#Known Deviations`; `trade-plan-stop-prefill.spec.js` | N/A |
| ST-15 | Find out why most on-demand Yahoo calls fail on production | merged | `data_pipeline_cost_baseline.md#4`; `ops_endpoints.md#GET /ops/api-call-attribution`; `earnings_endpoints.md#GET /earnings/{ticker}`; `data_model.md` DS-36; `test_yahoo_on_demand_failures.py` | N/A |
| ST-16 | Alert when weekly market-data call volume exceeds 2× the baseline | merged | `data_pipeline_cost_baseline.md#5`; `check_market_data_volume.py`; `market-data-volume-check.yml`; `test_market_data_volume_check.py` | N/A |
| ST-17 | Batch signal sizing can allocate more than available cash once fees are added | merged | `signal_endpoints.md#Field notes`; `strategy_signal_regression_spec.md#Inverse-Volatility Sizing`; `test_signal_sizing.py` | N/A |
| ST-18 | Release Planning §1.3a: gate clearance also sets a gate-worded Provisional-Target to TBD | merged | `release_planning_prompt.md#1.3a`; `release_planning_changelog.md` | N/A |
| ST-19 | Define or remove the 2R Exit Zone threshold the Positions page states | merged | `positions.md#Position Lifecycle State Badge`; `lifecycle-badge-grace-calendar-days.spec.js` | N/A |
| ST-20 | Stop check_data_model_drift.py reading index names from rollback blocks | merged | `check_data_model_drift.py`; `test_check_data_model_drift.py`; `docs/ops/data_model_drift_runs/` | N/A |

`Traceability gaps: 0 | Items returned: 0 | Backlog entries added this run: 0`

Every story is `merged`. Every story's `spec_references` is non-empty, and every story has `deviations_filed = true` and `acceptance_verified = true`. No slice item was returned or deferred at planning.

## 3. QA Evidence Summary

| EPIC | Items | Pass | Fail | Sign-off | Notes |
|------|-------|------|------|----------|-------|
| EPIC-01 | 4 | 4 (ST-04 Pass_with_deviation) | 0 | ✓ DoQ (agent-mediated §5.3) 2026-11-12; human DoQ/PO 2026-11-12T20:58:29Z | `DEV-EPIC01-ST04-01` (P3) |
| EPIC-04 | 2 | 2 (ST-10 Pass_with_deviation) | 0 | ✓ DoQ 2026-11-13; human 2026-11-13T09:34:47Z | `DEV-EPIC04-ST10-01` (P3) |
| EPIC-07 | 3 | 3 | 0 | ✓ DoQ 2026-11-13; human 2026-11-13T11:33:07Z | ST-18 AC 2 post-merge (seal-marked, `BLG-GOV-419`) |
| EPIC-06 | 3 | 3 | 0 | ✓ DoQ 2026-11-13; human 2026-11-13T14:57:46Z | ST-15 AC 2–3 post-merge (seal-marked, `BLG-OPS-217`); found defect `BLG-FE-294` (P2, accepted) |
| EPIC-05 | 4 | 4 | 0 | ✓ DoQ 2026-11-16; human 2026-11-16T08:54:06Z | ST-11 AC 2 post-merge (seal-marked, `BLG-BE-211`, met) |
| EPIC-02 | 3 | 3 | 0 | ✓ DoQ 2026-11-16; human 2026-11-17 on head `282050ea` | Found defect `BLG-FE-300` (P2) fixed before merge |
| EPIC-03 | 1 | 1 | 0 | ✓ DoQ 2026-11-17; human 2026-11-17 on head `ff08a481` | Found defect `BLG-FE-303` (P2) fixed before merge |

**STEP 2.1 / 2.3 checks.**
- Every `Result` is a recognised value: `Pass` or `Pass_with_deviation`.
- Each `Pass_with_deviation` names its AC gap and a confirmed backlog item:
  - ST-04: rows with more than 2 grace days left show no trade plan line / `DEV-EPIC01-ST04-01` / `BLG-BE-215`.
  - ST-10: Stops moved data source and window differ from §1B's wording / `DEV-EPIC04-ST10-01` / `BLG-SPEC-238`.
- All 7 sign-off blocks have every checkbox ticked, and each has a substantive Comments field.

**Found-defect rule (LL-v9.11-P4-01 / LL-v9.13-P4-01).** This was applied at every grade. The `Pass` grades of ST-15, ST-06 and ST-08 name P2 found defects (`BLG-FE-294`, `BLG-FE-300`, `BLG-FE-303`). All three take §7's PO + DoQ acceptance path (§4). The three unfiled P2s fixed on their branches before merge (EPIC-01 grace panel contrast, EPIC-06 UK pence read as pounds, EPIC-05's own-code P2) are in the QA evidence. Nothing about them is open, and the remaining same-kind cases from EPIC-06 are tracked at P3 (`BLG-BE-217`, `BLG-BE-218`).

**Seal-marked post-merge ACs (LL-v9.13-P3-03).** ST-11 AC 2 (`BLG-BE-211`), ST-15 AC 2–3 (`BLG-OPS-217`) and ST-18 AC 2 (`BLG-GOV-419`) were marked `post-merge` in the sealed `sprint_backlog.md`, each with its tracker named. They are planned remainders, checked in §5, not deviations.

**STEP 2.2.** No AC was narrowed or omitted without a filed deviation or tracker. Two notes:
- ST-12's evidence records that `BLG-FE-269` AC 1 (a separate P3 item covering both Trade Plan and Trade Entry) is **not** met, because Trade Entry's tick does not reset. That is not one of ST-12's ACs: both of ST-12's ACs are met, and `BLG-FE-269` stays open for `groom backlog`.
- ST-10 AC 2 (banner `BLG-FE-254` at post-ship closure) is a planned post-ship action, not an in-sprint AC.

**Frontend testing gate (CLAUDE.md §2).** EPIC-01, EPIC-02, EPIC-03, EPIC-04 (ST-10), EPIC-05 and EPIC-07 (ST-19) record Playwright coverage, run in real CI, for every observable AC. None records an AC as "code review only". EPIC-06 changes no frontend file.

## 4. Deviation Register

Two canonical-spec `DEV-*` records were filed this sprint. The register also covers each found defect listed in `sprint_close.md` "Deviations Filed This Sprint". Priorities are read from `backlog.md`.

| Deviation Ref | ST Item | Priority | Description | Disposition | Backlog Item |
|---------------|---------|----------|-------------|-------------|--------------|
| `DEV-EPIC01-ST04-01` | ST-04 | P3 | The grace view's trade plan block comes from `GET /positions/grace-period-alerts`, which returns only positions with 2 or fewer grace days left, so rows with more days left show no trade plan line | Recorded. Known Deviations entry present (`positions.md`), target v9.18 | `BLG-BE-215` (P3) |
| `DEV-EPIC04-ST10-01` | ST-10 | P3 | Stops moved is written by both stop recompute paths, and "latest nightly run date" is read as today or the previous weekday (UTC) | Recorded. Known Deviations entry present (`dashboard.md` §1B), Status Open | `BLG-SPEC-238` (P3) |
| FD-ST15 | ST-15 | **P2** | Found pre-existing defect: a failed earnings or gap-risk lookup shows the same as "no upcoming earnings", and the Screener looks up earnings for UK rows | **Accepted** (PO + DoQ, 2026-11-13T14:57:46Z) | `BLG-FE-294` (P2, open) |
| FD-ST06 | ST-06 | **P2** | Found in PR #2261 review: Summary showed £0.00 / 0.0% below the trade minimum | Fixed before merge (`9e807be8`); ✅ COMPLETE. Nothing carried | `BLG-FE-300` (P2, complete) |
| FD-ST08 | ST-08 | **P2** | Found in PR #2262 review: six components dark-only in page states the scans had not reached | Fixed before merge (`7b4e7736`); ✅ COMPLETE. Nothing carried | `BLG-FE-303` (P2, complete) |

### Hard Blocks

- P0: none.
- P1: none.
- P2 open: `BLG-FE-294` only. It is accepted with a rationale (below) and has a confirmed backlog item. `BLG-FE-300` and `BLG-FE-303` are fixed and closed.
- Carried-forward v9.16 P2s: `BLG-BE-211` is met (production backfill closed 3 plans; bannered 2026-11-16). `BLG-FE-278`, `BLG-FE-281` and `BLG-FE-282` are fixed by ST-12, ST-13 and ST-14, with banners due at post-ship closure STEP 3.1. `BLG-OPS-217` has its causes fixed and stays open only for its post-merge weekly report (§5).

### Acceptance Records

| Item | Priority | Accepted by | When | Rationale | Source |
|------|----------|-------------|------|-----------|--------|
| `BLG-FE-294` | P2 | Product Owner and Director of Quality (the user, holding both roles) | 2026-11-13T14:57:46Z, before the merge | A display gap that existed before this EPIC, not a regression. ST-15's cache and cap make failed lookups much rarer. Tracked for a later release. | `qa_evidence_EPIC-06.md` Merge Gate Confirmations |
| `BLG-FE-300` | P2 | Product Owner and Director of Quality (the user) | 2026-11-17, before the merge | Fixed on the branch at the PO's direction. | `qa_evidence_EPIC-02.md` Merge Gate Confirmations |
| `BLG-FE-303` | P2 | Product Owner and Director of Quality (the user) | 2026-11-17, before the merge | Fixed on the branch (user direction, option (a)). | `qa_evidence_EPIC-03.md` Merge Gate Confirmations |

### Known Deviations Sync (LL-v2.3-CL-03)

- Both `DEV-*` records have a Known Deviations entry in their canonical spec. Each entry carries priority, description, canonical requirement, target, owner and the matching backlog reference: `positions.md` `DEV-EPIC01-ST04-01` → `BLG-BE-215`, and `dashboard.md` `DEV-EPIC04-ST10-01` → `BLG-SPEC-238`. Nothing needs to go to Post-Ship Closure STEP 5.
- `DEV-v9.16-ST27-01` (`trade_plan.md`, pre-existing) is marked RESOLVED by ST-14 in that spec's Known Deviations table.
- `BLG-FE-294` is a pre-existing gap, not a divergence introduced by this sprint's stories. Its backlog entry, together with this register, is the tracking record (`ESC-CLOSE-20260923-02` extension).

## 5. Outstanding Items and Deferred Execution Blockers

### (a) Outstanding items carried to backlog

| Item | Type | Outcome | Backlog ref |
|------|------|---------|-------------|
| ST-15 AC 2 and AC 3 | Seal-marked post-merge AC | Open, as planned. Needs 7 days of post-fix production data, then `data_pipeline_cost_baseline.md` §4 updated | `BLG-OPS-217` ✓ |
| ST-18 AC 2 | Seal-marked post-merge AC | Open, as planned. Met by the next Release Planning run that clears a gate | `BLG-GOV-419` ✓ |
| ST-11 AC 2 | Seal-marked post-merge AC | Met 2026-11-16 (production backfill closed 3 plans; 0 active plans on closed positions). Bannered ✅ COMPLETE | `BLG-BE-211` ✓ |
| ST-10 AC 2 | Planned post-ship action | `BLG-FE-254` banner due at post-ship closure | `BLG-FE-254` ✓ |
| ST-12 / ST-13 / ST-14 source items | Met by this sprint's stories | ✅ banners due at post-ship closure STEP 3.1 | `BLG-FE-278` ✓, `BLG-FE-281` ✓, `BLG-FE-282` ✓ |
| ST-06 `BLG-FE-237` | Covered item | AC met by ST-06 (`performance.md` §9); for `groom backlog` to close | `BLG-FE-237` ✓ |
| ST-08 remaining shared components | Excluded at seal (RISK-02) | Open | `BLG-FE-288` ✓ |
| ST-12 note: Trade Entry acknowledgement reset | Separate open item | Open, for `groom backlog` | `BLG-FE-269` ✓ |
| Delegation `DEL-20261113-01` | Human-Delegation | Unblocked in session 2026-11-13T13:41:30Z; terminal | N/A |
| `ESC-EXEC-20261116-01` | This cycle's escalation | `Resolved` in session 2026-11-16 | N/A |
| `ESC-EXEC-20260910-01` (cycle v9.3) | Prior-cycle Deferred escalation, non-blocking | Not from this cycle. Its trigger (`DEL-20261030-04`) is still unmet | `BLG-GOV-399` ✓ |

No new `backlog.md` entries were needed: every outstanding item already has a traceable entry. `delegated_items` and `blocked_items` are empty. The 49 follow-ups filed during execution are listed in `sprint_close.md` and are not repeated here.

### (b) Deferred execution blocker dispositions

There are no deferred execution blockers: `state.json.deferred_execution_blockers` is `[]`.

### Stale parked items (STEP 4.3)

Skipped. The authoritative slice contains no `parked` items.

## 6. Test Coverage Assessment

Every EPIC has a populated `test_scenarios` list. All 24 listed files exist on disk, and each is cited in its EPIC's QA evidence log, either under "Scenarios run" or in the per-story CI evidence. EPIC-05's `test_lifecycle_transitions.py` is covered by the full local suite (3645 passed) and CI Pytest on each story SHA.

No story replaced a core algorithm, model or scoring function, so the AUD-2026-06-22-007 advisory does not apply. ST-17 changes batch sizing to trim whole shares until each signal's fee-inclusive cost fits its allocation. That extends the existing inverse-volatility sizing and is covered by `test_signal_sizing.py` and `strategy_signal_regression_spec.md`.

| EPIC | Scenario files | Cited as run | Status |
|------|----------------|--------------|--------|
| EPIC-01 | 4 | 4 | Covered |
| EPIC-02 | 3 | 3 | Covered |
| EPIC-03 | 3 | 3 | Covered |
| EPIC-04 | 2 | 2 | Covered |
| EPIC-05 | 6 | 6 | Covered |
| EPIC-06 | 4 | 4 | Covered |
| EPIC-07 | 2 | 2 | Covered |

### Test Scenario Gaps — Structured Register

No test scenario gaps identified. Table N/A.

These known coverage remainders already have their own backlog items, so they are not new gaps: `BLG-QA-263` (weekend clock tests for Stops moved), `BLG-QA-264` (staging index check), `BLG-QA-266` (debounce test), `BLG-QA-267` (token check parser) and `BLG-TECH-35` (frontend unit tests in CI).

## 7. System Status Confirmation

**Corrected.** `docs/System_status_report.md` § Sprint 2026-11-11__release-v9.17 lists all 7 merged EPICs, records "None" under "Capabilities deferred or returned" (correct), and shows both P3 deviations and the accepted P2 against their capability rows.

Corrections made this run:
1. `**Status:**` line updated from `Sprint_Complete — pending verification` to `Verified_with_deviations — 2026-11-17` (routine, BLG-GOV-170).
2. EPIC-05 "Spec sections implemented": `trade_plan_endpoints.md` replaced with ST-11's actual references, `data_model.md#DS-41` and `position_endpoints.md#POST /positions/{position_id}/exit`. Added `trade_plan.md#5f` (ST-14) and `research_view.md#4.7` (ST-13). The Deviations cell now notes that ST-11's post-merge backfill was met (`BLG-BE-211`).
3. EPIC-02: `performance.md` v1.0 corrected to v1.2, the version signed off in `qa_evidence_EPIC-02.md`.
4. EPIC-03: added `design_system.md#Page Colour Token Sweep`, ST-08's primary spec reference.
5. `**Last Updated:**` header updated (current entry plus 2 prior, per `shared_standards.md` §16.14).

## 9. Sign-off Block

## Director of Quality Sign-off

- [x] Traceability complete (or gaps documented with rationale)
- [x] QA evidence reviewed and accepted
- [x] Deviation register reviewed; all P0/P1/P2 dispositions confirmed
- [x] Test coverage gaps actioned (backlog items created)
- [x] System status report confirmed accurate
- [x] Deferred execution blockers dispositioned

Signed off by: Director of Quality (the user, in session)
Date: 2026-11-17
Comments: Signed off as Verified_with_deviations. The two P3 deviations are recorded, with Known Deviations entries and backlog items (`BLG-BE-215`, `BLG-SPEC-238`). The P2 acceptance for `BLG-FE-294` is re-confirmed. `BLG-FE-300` and `BLG-FE-303` were fixed before merge. ST-11's post-merge backfill is met (`BLG-BE-211`). The System Status Report corrections are confirmed.

## Product Owner Acceptance

- [x] Outstanding items confirmed in backlog
- [x] P1/P2 deviation acceptances confirmed (if any)
- [x] Deferred execution blocker outcomes acknowledged
- [x] Next cycle cleared to open

Accepted by: Product Owner (the user, in session)
Date: 2026-11-17
Comments: Accepted. Outstanding items are confirmed in the backlog (`BLG-OPS-217`, `BLG-GOV-419` open as planned; `BLG-FE-254`, `BLG-FE-278`, `BLG-FE-281`, `BLG-FE-282` awaiting banners). The `BLG-FE-294` P2 acceptance is re-confirmed. There are no deferred execution blockers. The next cycle is cleared to open.
