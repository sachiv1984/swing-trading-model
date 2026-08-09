# Sprint Planning Notes — 2026-08-08__release-v8.5

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-09
**Cycle:** 2026-08-08__release-v8.5

## Backlog Slice Source

Original — `claude/cycles/2026-08-08__release-v8.5/stage4_backlog_slice.md`. `amended_backlog_slice_path` in `.claude_current_state.json` is empty; no amendment sealed for this cycle.

## Deferred Items

None. All 25 items in the authoritative backlog slice are classified `include` (see Scope Selection below) — capacity accommodates full scope at the top of the confirmed ~24-28 day band (`sprint_capacity.md`).

## Scope Selection & Delegation Class

Every item is within capacity, owned per `release_plan.md ## Execution Plan`, and AC-confirmed directly from `stage4_backlog_slice.md` (no drafting needed this cycle — all 25 items already carry structured ACs from Release Planning). Delegation class assigned per §3.1 heuristics (BLG-GOV-72 fast-path, LL-v1.10-P3-3):

| EPIC | Item | Classification | Delegation Class | Rationale |
|------|------|----------------|-------------------|-----------|
| EPIC-01 | ST-01 | include | autonomous | Backend bug fix (DB column ensure), no UX change |
| EPIC-01 | ST-02 | include | delegated_backend | CI/CD log verification + a hardening decision to record |
| EPIC-02 | ST-03 | include | autonomous | Metrics/analysis task against existing logs |
| EPIC-02 | ST-04 | include | autonomous | Scheduled-job engineering task |
| EPIC-02 | ST-05 | include | autonomous | Documentation-only runbook |
| EPIC-03 | ST-06 | include | autonomous | Config fix restoring an already-canonical token (BLG-GOV-72(a)); Design Pre-Approved |
| EPIC-03 | ST-07 | include | autonomous | Prop/state threading fix, no UX change (BLG-GOV-72(a)) |
| EPIC-03 | ST-08 | include | autonomous | Colour-convention decision already resolved at Design Gate (`decision_record.md`); this story implements it |
| EPIC-04 | ST-09 | include | autonomous | Audit-only, no code decision |
| EPIC-04 | ST-10 | include | autonomous | Microcopy pattern already resolved at Design Gate (`decision_record.md`); applies to ≥3 pages |
| EPIC-04 | ST-11 | include | autonomous | Verification of existing behaviour |
| EPIC-04 | ST-12 | include | autonomous | Corrective fixes against already-approved layout spec (Design Pre-Approved) |
| EPIC-04 | ST-13 | include | autonomous | Targeted audit, no new UI change |
| EPIC-04 | ST-14 | include | delegated_decision | AC explicitly requires Head of UX & Design sign-off on the inventory/ranking output |
| EPIC-05 | ST-15 | include | delegated_decision | Design recommendation deliverable — directional UX judgment call |
| EPIC-05 | ST-16 | include | delegated_decision | AC explicitly requires Head of UX & Design sign-off |
| EPIC-05 | ST-17 | include | autonomous | Spec-writing deliverable against an already-decided pattern (ST-10) |
| EPIC-05 | ST-18 | include | delegated_decision | AC explicitly requires Head of UX & Design review |
| EPIC-05 | ST-19 | include | delegated_frontend | Conditional scope (BLG-GOV-72 exception — genuinely cannot pre-classify autonomous while the triggering consumer is unknown); most likely closes as "still unused, no action" per its own Note |
| EPIC-05 | ST-20 | include | autonomous | Deferred-trigger verification story; no design decision |
| EPIC-06 | ST-21 | include | autonomous | Placement/colour decision already resolved at Design Gate (`decision_record.md`) |
| EPIC-06 | ST-22 | include | autonomous | Internal governance-tooling chart, no product UX surface |
| EPIC-06 | ST-23 | include | delegated_decision | AC explicitly requires Head of Specs Team sign-off (governance-file patch) |
| EPIC-06 | ST-24 | include | delegated_decision | AC explicitly requires Head of Specs Team sign-off (governance-file patch) |
| EPIC-06 | ST-25 | include | autonomous | Test-infrastructure fix, matches existing guarded pattern |

**LL-v2.0-P4-2 (test scenario gap) applicability check:** Only one item (`ST-19`, `delegated_frontend`) carries a scope that *could* introduce new user-facing controls — but only if a `ChartContainer` consumer is adopted this cycle, which is unconfirmed at planning time (`chart.js` has zero live consumers today, per Design Gate). Per-item `test_scenarios` is not pre-set to "pending" here since the triggering condition is unknown; if a consumer is adopted during execution, the EPIC-05 owner must apply the LL-v2.0-P4-2 backstop at that point (recorded as an Outstanding Action below).

**LL-v2.2-SP-01 (blocked-decision design artefact) check:** For the 6 `delegated_decision` items (ST-02, ST-14, ST-15, ST-16, ST-18, ST-23, ST-24 — 7 total): none require a *pre-execution* design/decision artefact to unblock start — each story's own AC produces the review/decision/sign-off as its deliverable, not as a precondition. `ST-08`/`ST-10`/`ST-21` (the 3 genuine Design Required items this cycle) already have their decision records produced at Design Gate (`design_gate.md` Notes) and are classified `autonomous` accordingly. No gap to surface.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| EPIC-04/ST-09, ST-13 | EPIC-03/ST-06 | Internal (sequencing, per `release_plan.md §Execution Plan` note and RISK-01) | Resolved — ST-06 sequenced first within the sprint (see Execution Sequence below) |
| EPIC-04/ST-08, ST-10, ST-21 | Design Gate decision records (`design_gate.md`) | Internal (gate) | Resolved — `design_gate_status = Passed`, all 3 decision records present (`exact-zero-pnl-colour-convention`, `empty-state-microcopy-pattern`, `regime-distribution-panel`) |
| EPIC-05/ST-17 | EPIC-04/ST-10 (empty-state pattern decision) | Internal | Resolved — ST-10's decision record exists at Design Gate; ST-17 draws on it as reference material only, not a blocking precondition |
| EPIC-05/ST-19 | Unknown future `ChartContainer` consumer adoption | External (conditional, in-story) | N/A — condition may or may not occur this sprint; not a cross-item blocker |
| EPIC-05/ST-20 | Unknown future `ui/calendar.js` consumer | External (conditional, in-story) | N/A — deferred-trigger item; closes with "no consumer yet" if condition doesn't occur |

No circular dependencies identified.

## Execution Sequence

1. **EPIC-01** — Production Correctness Fixes (ST-01, ST-02) — standalone, P1, no sequencing constraint; leads per standing correctness precedence
2. **EPIC-03** — Frontend Correctness Fixes (ST-06 first — RISK-01 mitigation — then ST-07, ST-08)
3. **EPIC-04** — Design System & Contrast Consistency Audit (ST-09/ST-13 after ST-06 lands; remaining items any order)
4. **EPIC-02** — Security Hardening (ST-03–ST-05) — standalone, no sequencing constraint
5. **EPIC-05** — Frontend UX Review & Documentation (ST-15–ST-20) — standalone; ST-17 may reference ST-10's decision record once EPIC-04 lands
6. **EPIC-06** — Analytics & Governance Process Fixes (ST-21–ST-25) — standalone

Autonomous items are not otherwise gated ahead of delegated items in this sprint; the only delegation-shaped sequencing consideration is EPIC-04/ST-14 and EPIC-05/ST-15/16/18 (`delegated_decision` — Head of UX & Design review/sign-off), which should be scheduled once their respective EPICs open per the sequence above, and EPIC-06/ST-23/ST-24 (`delegated_decision` — Head of Specs Team sign-off on governance-file patches).

## Multi-EPIC Execution Notes

**`execution_state.json` owner:** EPIC-01 (first in execution order). All other EPIC branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite (per `sprint_planning_prompt.md §5.2`).

**Shared file ownership advisory:**

| File | EPICs touching it | Canonical-version owner | Note |
|------|--------------------|--------------------------|------|
| `docs/specs/frontend/design_system.md` | EPIC-03 (ST-06), EPIC-04 (ST-09, ST-10, ST-13) | EPIC-03 (merges first per execution order) | EPIC-04 must rebase onto `main` after EPIC-03 merges before finalising its own `design_system.md` changes (if any beyond the already-landed v1.8 decision record). |
| `docs/specs/frontend/pages/reports.md` | EPIC-03 (ST-08) only | EPIC-03 | No cross-EPIC conflict expected — already at v0.16 per Design Gate; no other EPIC touches this file this cycle. |
| `docs/specs/frontend/pages/screener_results.md` | EPIC-06 (ST-21) only | EPIC-06 | No cross-EPIC conflict expected — already at v1.4 per Design Gate. |
| `release_planning_prompt.md` / `CLAUDE.md` | EPIC-06 (ST-23, ST-24) | EPIC-06 | Both are governance-file patches within the same EPIC — no cross-EPIC collision, but RISK-04's Governance File Edit Checklist applies independently to each story's own commit. |
| `execution_state.json` | All 6 EPICs (routine multi-EPIC artefact, not a content conflict) | EPIC-01 (see owner designation above) | Standard append-not-overwrite handling per `sprint_planning_prompt.md §5.2`. |

No other cross-EPIC shared-file collisions identified from the backlog slice's stated scope. EPIC-04 and EPIC-03 are not assigned as a genuinely parallel pair this sprint — ST-06's sequencing dependency (RISK-01) makes true parallelism unsafe; run EPIC-03 to merge before EPIC-04's ST-09/ST-13 land.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-04 | Valid — ST-06 sequenced first within the sprint (Execution Sequence above); mitigation unchanged since release planning |
| RISK-02 | EPIC-04, EPIC-05 | Valid — ACs are explicit that audit-only/review-only completion is a valid, complete outcome for the 10 audit/review/documentation items; DoQ sign-off should reference this note per the release plan's own mitigation |
| RISK-03 | EPIC-01 | Valid — ST-01's AC requires an explicit no-regression confirmation against existing `trade_plans.py` endpoints regardless of which candidate fix (narrow vs broad) is taken; unchanged |
| RISK-04 | EPIC-06 | Valid — ST-23/ST-24 both carry an explicit `Governance-file note` in `stage4_backlog_slice.md` naming the CLAUDE.md §6 checklist; unchanged |
| RISK-05 | Release-level | Valid — documented and PO-accepted at release planning (`run_manifest.md §STEP 2`); no new information this session; reflected in `sprint_goal.md` Release Context |
| RISK-06 | EPIC-02 | Valid — no urgency-driven mitigation needed; ST-04/ST-05 sequencing remains flexible within the sprint |

No risk has materialised since release planning (same-day-adjacent cycle; no new information).

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json` — **unavailable** (`pip-audit` not installed in this environment). Per STEP -1 advisory 6: flagged, not blocking. Recommend installing `pip-audit` before sprint execution begins so the scan can run with real results; if unavailable at execution time too, Sprint Execution should note the same gap in its own evidence trail.

## Endpoint Test Coverage Audit (STEP -1 advisory 8)

`python3 scripts/audit_endpoint_test_coverage.py` — **clean**. 78 route decorators scanned across 23 router files; 8 documented `KNOWN_GAPS` exclusions; 0 undocumented gaps.

## Prompt Change Log Gap Detection (STEP -1 advisory 7, date-scan method)

All 16 Class 6 governance prompts with a `**Version:**` header checked against `claude/system/prompt_change_log.md` using the date-scan method (latest-dated row per filename; same-date ties broken by highest target version, not file position):

`amendment_cycle_prompt.md` v1.9, `backlog_management_prompt.md` v1.13, `delivery_verification_prompt.md` v3.7, `design_gate_prompt.md` v1.9, `execution_prompt.md` v3.66, `gh_issue_template.md` v1.0, `idea_intake_prompt.md` v2.8, `ideas_housekeeping_prompt.md` v1.2, `lessons_learnt_prompt.md` v1.10, `post_ship_closure.md` v2.25, `release_planning_prompt.md` v2.48, `roadmap_management_prompt.md` v1.4, `roadmap_prompt.md` v9.13, `shared_standards.md` v3.26, `sprint_planning_prompt.md` v3.16 — all current, no gap.

**⚠ One genuine gap found — `OPERATIONAL_GUIDE.md`:** document header currently reads `**Version:** 4.147` (confirmed by direct read), but `prompt_change_log.md`'s own latest-dated row (`2026-08-08`, target `v4.148→v4.149`) and the document's own `§14` Change Log table top row (`4.149`, `2026-08-08`) both record `4.149` as current. The header is **2 versions behind its own internally-logged state** — a live recurrence of the exact "header-drift" pattern the document has self-corrected at least 5 times before (see its own standing v4.85 note and the `4.146→4.148` self-correction entry, itself dated the same day as this newly-found drift). This is outside Sprint Planning's write scope (`OPERATIONAL_GUIDE.md` is not a permitted write path per §6) — surfaced here as advisory only, not actioned. **Recommend filing a backlog item** (e.g. `BLG-GOV-*`, Head of Specs Team) to correct the header to `4.149` and to consider whether the recurring nature of this exact failure mode (now observed live a 6th+ time) warrants a structural fix (e.g. deriving the header field mechanically from the §14 table's top row) rather than another manual correction.

## Pre-Sprint Backlog Advisory

No `claude/backlog/backlog.md` items found with `Provisional-Target: Before v8.5 sprint planning`.

## Carry-Forward Items

4 items reviewed from cycle `2026-08-07__release-v8.4` (`lessons_learnt_closure.md ## Carry-Forward`):

1. `scripts/check_api_performance_baseline_drift.py` substring-matching false negative (`GET /trade-plans/tags`) — targeted at Post-Ship Closure / Infrastructure & Operations Owner script hardening. No action here; no story in this cycle's scope touches that script.
2. `post_ship_closure.md` STEP 7.3's stale "§27" reference — targeted at Post-Ship Closure / Head of Specs Team, next revision touching STEP 7. No action here.
3. `DEV-EPIC02-ST03-01` stale-target deviation re-triage — targeted at Head of Specs Team, "before next `plan release`." Next release planning has already run (this cycle, `v8.5`) without a recorded re-triage; flagged below as an Outstanding Action (not a Sprint Planning blocker — deviation re-triage is Head of Specs Team's action, not scoped to this sprint's backlog slice).
4. `reports.md` 2-of-10 deviation concentration watch — targeted at the next cadence-triggered Post-Ship Closure deviation consolidation review. No action here; `ST-08` (this cycle) touches `reports.md` for a colour-convention reconciliation, not a new deviation.

No item names "Sprint Planning" or "All" as the responsible engine — no direct action required at this routine.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Install `pip-audit` before sprint execution so the pre-sprint vulnerability scan can run with real results (currently unavailable in this environment) | Infrastructure & Operations Owner | No |
| `OPERATIONAL_GUIDE.md` header (`4.147`) is 2 versions behind its own §14 table / `prompt_change_log.md` (`4.149`) — file a backlog item to correct and consider a structural fix for this recurring drift pattern | Head of Specs Team | No |
| `DEV-EPIC02-ST03-01` re-triage (carried from `v8.4` closure, targeted "before next `plan release`") remains unresolved as of this sprint planning run — surface again at this cycle's Post-Ship Closure if still open | Head of Specs Team | No |
| If a `ChartContainer` consumer is adopted during execution of ST-19, apply LL-v2.0-P4-2's `test_scenarios` roll-up backstop and treat the rendering/colour question as needing a fresh design pass (per `design_gate.md` Notes), not the pre-cleared Design Not Applicable outcome | EPIC-05 owner (Head of UX & Design; Frontend Specifications & UX Documentation Owner) | No |

No outstanding action is marked `Blocker? Yes`.
