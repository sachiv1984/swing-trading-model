Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-17 (follow-up — §6 row 3 resolved: spec pages registered); prior — 2026-11-17 (created)
Cycle: 2026-11-11__release-v9.17

---

# Post-Ship Closure Record — 2026-11-11__release-v9.17

## §1 — Closure Status

```
Status: Closed_with_actions
Release: v9.17 — Site Structure & Usability, Phase 3
Ship date: 2026-11-17
Cycle: 2026-11-11__release-v9.17
Verification status: Verified_with_deviations
Backlog slice source: claude/cycles/2026-11-11__release-v9.17/stage4_backlog_slice.md, read with the sealed stage4_backlog_slice_addendum.md (original; amended_backlog_slice_path empty; matches execution_state.json.backlog_slice_source)
Closure run: 2026-11-17T15:35:34Z (closure_state.json started_utc)
```

## §2 — Documents Updated

| Step | Document | Action | Status |
|------|----------|--------|--------|
| 1 | docs/product/changelog.md | v9.17 entry written: 7 EPICs, all with `User Impact` populated; 20 tech backlog items tagged U/G/D/P (13 U / 1 G / 6 D / 0 P). Deviations accepted: P2 `BLG-FE-294`. `BLG-FE-300` and `BLG-FE-303` noted as fixed before merge. 2 P3 summarised. Read back through `get_latest_changelog_entry()`: v9.17, 7 rows | ✅ |
| 1.5 | Telegram changelog digest | Attempted with the venv and `PYTHONPATH=backend`: `sent: false` (Telegram credentials not configured in this environment). Non-blocking | ✅ (attempted) |
| 2 | claude/roadmap/current_roadmap.md | §1: Current Version → v9.17 ✅ Complete (2026-11-17); Next planned release → [TBD] (programme plan places the close-out at v9.18); Previous release → v9.16; RA:v9.17 closure status line added. §3 programme plan: Phase 3 marked ✅ v9.17. §8 Release Summary row added. Restored the missing `**Last Updated:**` label on line 4 (Closure FI-2) | ✅ |
| 3 | claude/backlog/backlog.md | 17 shipped source items bannered ✅ COMPLETE with cycle, ST, EPIC, PR and commit; `BLG-BE-211` was already bannered (post-merge backfill met 2026-11-16), so 18 of 20 source items are closed. **Case (i):** `BLG-OPS-217` (ST-15 AC 2–3) and `BLG-GOV-419` (ST-18 AC 2) kept open as their own post-merge trackers (§6 rows 1–2). `BLG-FE-254` bannered, closing v9.16 §6 row 3. 0 Phase 4 additions needed. 1 STEP 8 addition (`BLG-QA-268`). 0 stale parked items (the slice held none). `check_backlog_item_integrity.py` passes | ✅ |
| 4 | Scope document (`scope--2026-11-11__release-v9.17-site-structure-phase-3.md`) | Status Active → Superseded; supersession note added | ✅ |
| 4 | Decisions record (`decisions--2026-11-11__release-v9.17.md`) | Status Active → Superseded; supersession note added. No `AR-*` records this cycle | ✅ |
| 5 | Canonical specs (deviation compliance) | 2 `DEV-*` checked (`DEV-EPIC01-ST04-01` in `positions.md`, `DEV-EPIC04-ST10-01` in `dashboard.md`): all six fields present. 0 fields corrected. `DEV-v9.16-ST27-01` already marked RESOLVED by ST-14 | ✅ |
| 5.1 | Cross-cycle deviation consolidation review | Not due (1 of 3 closures since the 2026-11-11 ninth run) | — |
| 6 | Operational docs | `velocity_metrics.md`: v9.17 row appended (20 planned, 20 completed, 1.00); rolling window → v9.12–v9.17 (1.00; 0.996 exact); header confirmed advanced at the prior append. `System_status_report.md` already accurate (status line set by Delivery Verification). `validation_system.md`: no stale references. Endpoint coverage drift: PASSED (`check_api_performance_baseline_drift.py`); no route added or retired, so no new `categorizeEndpoint()` prefix | ✅ |
| 7 | docs/specs/Specs_Index.md | §6/§7: no items resolved by this delivery. §57 Test Coverage Gaps (v9.17) added with 0 new gaps and 1 spec registry gap (`journal.md`, `performance.md` unregistered; §6 row 3). Changelog row and header updated. **STEP 7.3 full-document sweep: 5 Open TSG entries checked, 0 resolved** (TSG-v9.12-02, TSG-v9.13-01..03, TSG-v9.14-01; their backlog items are all still open) | ✅ |
| 8 | Lessons learnt review | Release Planning `lessons_learnt.md` (3 items); `lessons_learnt_cycle.md` Phase 3 (5 items, 4 Carry-Forward) and Phase 4 (1 item); 2 closure-phase findings. Result: 8 immediate, 4 deferred, 0 escalated | ✅ |
| 8 | claude/system/execution_prompt.md, post_ship_closure.md (+ changelogs, OPERATIONAL_GUIDE.md, prompt_change_log.md, prompt_size_baseline.json) | v3.94→v3.95, v2.47→v2.48; OPERATIONAL_GUIDE.md v4.260→v4.261. CLAUDE.md §6 checklist complete. Governance-drift check: all 29 tracked files in sync; `OPERATIONAL_GUIDE.md` self-consistent at 4.261/2026-11-17. Prompt size budget raised for both prompts with reasons in the change log; `check_prompt_size_budget.py` OK | ✅ |
| 8 | claude/backlog/backlog.md | 1 deferred action filed via `/backlog-add` with target v9.18: `BLG-QA-268` (`LL-v9.17-P3-01` part (b)) | ✅ |
| 8.5 | lessons_learnt_closure.md | Created | ✅ |

## §3 — Backlog Additions This Run

- **Phase 4 additions:** none needed. Every verification item already existed (`BLG-BE-215`, `BLG-SPEC-238`, `BLG-FE-294`).
- **STEP 8 deferred action, filed via `/backlog-add` under the STEP 8 rule (LL-v9.12-Release-01):**
  - `BLG-QA-268`: Script the locator-collision check and run it from commit-check (`LL-v9.17-P3-01` (b), v9.18)

## §4 — Deviation Compliance Summary

Two `DEV-*` records were filed this sprint. All compliant: **Yes**.
- `DEV-EPIC01-ST04-01` (`positions.md`, P3, `BLG-BE-215`, target v9.18): all six fields present.
- `DEV-EPIC04-ST10-01` (`dashboard.md` §1B, P3, `BLG-SPEC-238`, target the release that seats it): all six fields present.
- Found defects `BLG-FE-294` (open, accepted), `BLG-FE-300` and `BLG-FE-303` (fixed before merge) are not canonical-spec divergences introduced this sprint; their backlog entries and verification §4 are the record (`ESC-CLOSE-20260923-02` extension).
- No `strategy_rules.md` entry needed routing (ST-19 took option (b), no `strategy_rules.md` write).

Accepted P1/P2 deviations in the changelog: yes (`BLG-FE-294`).

## §5 — Lessons Learnt Action Summary

Records reviewed:
- Release Planning `lessons_learnt.md` (3 friction items)
- `lessons_learnt_cycle.md` Phase 3 (5 friction items, 4 Carry-Forward) and Phase 4 (1 friction item)
- The v9.16 closure's Outstanding deferred patches (2 rows: `BLG-GOV-419` applied in ST-18; stale-gate observation done) and Carry-Forward (4 rows: #1, #2, #4 closed; #3 carried)
- This closure's own findings (2)

**Immediate: 8**
1. Release Planning FI-1 (`LL-v9.17-Release-01`): phase row shipped while a remainder is open. Applied: `post_ship_closure.md` v2.48 STEP 2 item 5a.
2. Release Planning FI-2 (`LL-v9.17-Release-02`): remainder has no effort rule. Applied: `post_ship_closure.md` v2.48 STEP 3.1 case (i).
3. Phase 3 FI-1 (`LL-v9.17-P3-01`) part (a): hidden or moved text breaks locators. Applied: `execution_prompt.md` v3.95 §3.1.A step 13.
4. Phase 3 FI-4 (`LL-v9.17-P3-04`): estimated timestamps. Applied: `execution_prompt.md` v3.95 §9.2.
5. Phase 3 FI-5 (`LL-v9.17-P3-05`): stories left `done` at merge. Applied: `execution_prompt.md` v3.95 STEP 4 step 2.
6. Phase 4 FI-1 (`LL-v9.17-P4-01`): hand-written SSR spec cells. Applied: `execution_prompt.md` v3.95 STEP 5.3A.
7. Closure FI-1 (`LL-v9.17-Closure-01`): new spec files unregistered. Applied: `post_ship_closure.md` v2.48 STEP 7.2.
8. Closure FI-2 (`LL-v9.17-Closure-02`): roadmap header label missing. Applied: data fix in `current_roadmap.md`.

**Deferred: 4**
1. Release Planning FI-3 (`LL-v9.17-Release-03`, observation): no prompt change; carried as Carry-Forward 3 and §6 row 7.
2. Phase 3 FI-1 part (b): scripted locator check. `BLG-QA-268`, Head of Specs Team; QA & Testing Owner, v9.18.
3. Phase 3 FI-2 (`LL-v9.17-P3-02`): design gate premise checks. `BLG-GOV-422` (P2), Head of Specs Team, v9.18.
4. Phase 3 FI-3 (`LL-v9.17-P3-03`): visual baseline push. `BLG-OPS-220` (P3), Infrastructure & Operations Owner, v9.18.

**Escalated: 0**

Full detail: `claude/cycles/2026-11-11__release-v9.17/lessons_learnt_closure.md`.

## §6 — Outstanding Actions

| # | Description | Owner | Deadline | Escalation path | Resolution |
|---|-------------|-------|----------|-----------------|------------|
| 1 | **Split-achievability case (i):** `BLG-OPS-217` not marked COMPLETE. Outstanding: ST-15 AC 2 (post-fix production weekly report, failure rate < 10% or documented) and AC 3 (`data_pipeline_cost_baseline.md` §4 updated). Needs 7 days of post-fix production data (EPIC-06 merged 2026-11-13). Its Provisional-Target is `TBD`. | Infrastructure & Operations Owner | On or after 2026-11-20 | `BLG-OPS-217` | *(open)* |
| 2 | **Split-achievability case (i):** `BLG-GOV-419` not marked COMPLETE. Outstanding: ST-18 AC 2 (the next Release Planning gate scan after a clearance shows no data-quality warning for the cleared item's `Provisional-Target`). Its `Provisional-Target` still reads v9.17; retarget to the next release. | Head of Specs Team; PMO Lead | Next Release Planning run that clears a gate | `BLG-GOV-419` | *(open)* |
| 3 | Register `docs/specs/frontend/pages/journal.md` and `docs/specs/frontend/pages/performance.md` in `docs/specs/Specs_Index.md` §8b (and review whether the Reports and Performance Analytics specs they replaced are marked superseded) | Head of Specs Team | Next spec edit | `Specs_Index.md` §57 | ✅ Resolved 2026-11-17 (Head of Specs Team, user-directed): both registered in §8b; `reports.md` and `analytics.md` already carry their own "Superseded by `performance.md`" headers; `BLG-SPEC-221` met and archived |
| 4 | Mark `docs/specs/metrics_definitions.md` Appendix E Item 4 (`BLG-FE-240`) Resolved (carried from v9.16 §6 row 2; still reads Open). | Metrics Definitions & Analytics Canonical Owner | Next spec edit | `deviation_consolidation_review_2026-11-11.md` | *(open)* |
| 5 | Confirm the ninth deviation consolidation review (carried from v9.16 §6 row 7; agent-mediated DoQ sign-off still pending human confirmation). | Director of Quality | Next session | `docs/governance/deviation_consolidation_review_2026-11-11.md` | *(open)* |
| 6 | Add ACs to, or kill, `BLG-GOV-200` and `BLG-GOV-201` (carried from v9.16 §6 row 5). | PMO Lead; item owners | Before either is seated | `backlog_health_20261111.md` | *(open)* |
| 7 | Link `docs/governance/governance_overhead_audit_2026-11-02.md` and the ST-45 sunset review (`BLG-GOV-408`) as inputs at the next `run roadmap` (carried from v9.16 §6 row 8). | PMO Lead | Next `run roadmap` | `lessons_learnt_closure.md` Carry-Forward 3 | *(open)* |
| 8 | Retarget stale tags: `BLG-GOV-419` (v9.17), and the open v9.15/v9.16/v9.17-tagged items listed in this run's `backlog_health` report (carried from v9.16 §6 row 6). `BLG-BE-215` reads `TBD` while its Known Deviation targets v9.18. | PMO Lead; item owners | Next Release Planning run | `backlog_health_20261117.md` | *(open)* |
| 9 | `BLG-UX-08` gate met (all of `BLG-FE-244`–`266` and `BLG-SPEC-214`–`216` closed). Seat the programme close-out re-review and clear its gate in place. | Product Owner; Head of UX & Design | Next Release Planning run | `lessons_learnt_closure.md` Carry-Forward 4 | *(open)* |
| 10 | Telegram changelog digest not delivered (credentials absent in this environment). Send the v9.17 digest from an environment with `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` if wanted. | Infrastructure & Operations Owner | Optional | — | *(open, non-blocking)* |

The v9.16 closure's §6 row 1 (owner notice for `DEV-v9.16-ST27-01`) is superseded: ST-14 resolved that deviation. Rows 3 (`BLG-FE-254`) and 4 (`ESC-CLOSE-20261111-01`) are closed.

## §7 — Closure Confirmation

```
Post-ship closure complete — 2026-11-11__release-v9.17 — 2026-11-17
Release: v9.17 — Site Structure & Usability, Phase 3
Verification status: Verified_with_deviations
Lessons learnt applied: 8 immediate | 4 deferred | 0 escalated
Outstanding actions carried forward: 10 in §6
Next cycle may now open.
```
