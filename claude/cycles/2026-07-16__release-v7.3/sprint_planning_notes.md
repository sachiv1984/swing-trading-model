**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-16
**Cycle:** 2026-07-16__release-v7.3

# Sprint Planning Notes — 2026-07-16__release-v7.3

## Backlog Slice Source

Original — `claude/cycles/2026-07-16__release-v7.3/stage4_backlog_slice.md`. `.claude_current_state.json` `amended_backlog_slice_path` is absent/empty — no amendment in effect.

## Carry-Forward Items

Reviewed `claude/cycles/2026-07-15__release-v7.2/lessons_learnt_closure.md ## Carry-Forward` (most recently completed cycle with `post_ship_complete = true` per closure record). 2 items:

1. **Shared Playwright spec file confirmation (actioned this run):** v7.2's EPIC-05 (`BLG-QA-111`) named a shared spec file — `tests/e2e/v7.2-dashboard-tradeplan-ux-hardening.spec.js` (see `docs/specs/frontend/blg_qa_111_combined_design_review_shared_playwright_plan.md` §3) — for the three implementation stories (then v7.2's ST-03/ST-05/ST-06, now this cycle's ST-01/ST-02/ST-03 = `BLG-FE-109/110/111`), rather than three separate page-scoped files. The carry-forward explicitly required this sprint planning run to reference that filename in all three stories' `sprint_backlog.md` entries before sealing, not merely note it as a recommendation. **Closed:** all three ST-01/ST-02/ST-03 entries below carry an explicit `**Shared Playwright Spec:**` field naming this file.
2. **Day-range effort estimate escalation (informational, not this engine's action):** v7.2 supplied a second data point (all 8 v7.2 items voluntarily carried day ranges) for the still-open v7.1 escalation on whether `backlog_management_prompt.md`/`idea_intake_prompt.md` should mandate day ranges. Owner: Head of Specs Team, deadline 2026-07-17. No action required from Sprint Planning; noted for awareness only.

## Deferred Items

None. All 7 items from the authoritative backlog slice are classified `include` (see Dependency Map below) — full scope proceeds within capacity (13.25d midpoint vs. ~12-14d band, PASS).

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 (`BLG-FE-109`) | None | — | Ready |
| ST-02 (`BLG-FE-110`) | None (shares `DashboardHome.js` with ST-03 — same EPIC-01 branch, coordinate to avoid merge conflicts) | Internal (soft) | Ready |
| ST-03 (`BLG-FE-111`) | None (shares `DashboardHome.js` with ST-02 — same EPIC-01 branch, coordinate to avoid merge conflicts) | Internal (soft) | Ready |
| ST-04 (`BLG-SPEC-91`) | None | — | Ready |
| ST-05 (`BLG-SPEC-92`) | None | — | Ready |
| ST-06 (`BLG-SPEC-93`) | None | — | Ready |
| ST-07 (`BLG-SPEC-94`) | None | — | Ready |

No cross-EPIC dependencies. Per `release_plan.md` Execution Plan sequencing note: EPIC-01 has no internal cross-dependency on EPIC-02–05; EPIC-02–05 are independent readiness passes for four different v7.4 candidate features and may run in any order or in parallel.

## Execution Sequence

1. EPIC-01 (ST-01 → ST-02 → ST-03) — `delegated_frontend`, ready now, no blockers. ST-02/ST-03 share `DashboardHome.js`; sequence ST-02 before ST-03 within the branch to minimise merge friction (ST-03 is a layout/hierarchy pass over cards ST-02 also touches for empty states).
2. EPIC-02 (ST-04) — `autonomous`, independent.
3. EPIC-03 (ST-05) — `autonomous`, independent. Highest-priority readiness gate this release (RISK-03, §13 pre-check) — recommend not leaving to last in case the pre-check surfaces a genuine concern requiring PO/Strategy Rules Owner scoping before the sprint closes.
4. EPIC-04 (ST-06) — `autonomous`, independent.
5. EPIC-05 (ST-07) — `autonomous`, independent. Named first candidate to phase into a second sprint if capacity tightens (see `sprint_capacity.md` §1.3) — sequencing last is consistent with that contingency.

No circular dependencies detected.

**Multi-EPIC Execution Notes:** 5 EPICs in scope (> 1). Per `sprint_planning_prompt.md` §5.2:
- `execution_state.json` owner: **EPIC-01** (first in execution order). EPIC-02/03/04/05 branches must check for `execution_state.json` existence before creating their own and append their EPIC's section rather than overwrite.
- **Shared file ownership advisory:** No source file is modified by more than one EPIC. `design_system.md`'s `DataState` empty-state pattern is *referenced/confirmed-unchanged* by EPIC-02 (ST-04 AC-06) and EPIC-05 (ST-07 AC-06) — both are read-only confirmations against the existing v1.1 pattern, not edits, so no rebase-ordering requirement applies. Within EPIC-01, `DashboardHome.js` is modified by both ST-02 and ST-03 (see Dependency Map) — this is a same-branch, same-EPIC concern, not a cross-EPIC shared-file risk.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 | Valid — design gate re-confirmed 2026-07-16 (`design_gate.md`) that `trade_plan.md`/`dashboard.md` are unchanged since the v7.2 design gate commit (`87a02be3`); prior Passed record cited directly, no fresh design review needed. |
| RISK-02 | EPIC-02 | Valid — scope remains explicitly bounded to spec/prompt-template/discoverability-plan/API-contract-stub per `BLG-SPEC-91`'s own AC; no scope-creep signal at planning time. |
| RISK-03 | EPIC-03 | Valid, highest-priority — `BLG-SPEC-92` AC-05 requires the §13 pre-check to be completed and recorded PASS-or-named-follow-up during this pass. Sequenced 3rd (not last) in Execution Sequence above specifically so a genuine §13 finding has runway to reach PO/Strategy Rules Owner before sprint close if it surfaces. |
| RISK-04 | EPIC-04 | Valid — `BLG-SPEC-93` AC-01 requires the batch-mutation pattern to be designed against existing `backend/routers/` conventions, reviewed by Backend Engineering Patterns Owner. |
| RISK-05 | EPIC-05 | Valid — **LP-14 multi-vehicle fix-choice check applied:** `BLG-SPEC-94` AC-01 names a genuine either/or schema choice (JSON-column-on-settings vs. dedicated table) but its own acceptance criteria already require the decision be made and recorded *during this readiness pass*, not deferred to execution kickoff. No live open either/or is being deferred past planning, so no capacity cross-reference against a Phasing Recommendation is needed (none exists this cycle — capacity outcome is PASS, not WARN). |

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json`: **clean** — 61 dependencies scanned, 0 with known vulnerabilities.

## Hygiene Advisories (non-blocking)

**Prompt change log gaps** (per STEP -1 advisory 7 — current version ahead of last logged transition):
- ⚠ `sprint_planning_prompt.md` current v3.13 — last log entry targets v3.12.
- ⚠ `release_planning_prompt.md` current v2.42 — last log entry targets v2.41.
- ⚠ `execution_prompt.md` current v3.57 — last log entry targets v3.55 (2 versions behind).
- ⚠ `roadmap_prompt.md` current v9.1 — last log entry targets v9.0.
- ⚠ `backlog_management_prompt.md` current v1.12 — last log entry targets v1.9 (3 versions behind).

No gap found for `design_gate_prompt.md`, `delivery_verification_prompt.md`, `post_ship_closure.md`, `amendment_cycle_prompt.md`, `roadmap_management_prompt.md`, `ideas_housekeeping_prompt.md`, `idea_intake_prompt.md`. Recorded per CLAUDE.md §6 — Head of Specs Team to add the missing prepended rows to `claude/system/prompt_change_log.md` when convenient; advisory only, does not block this sprint.

**Pre-Sprint Backlog Advisory:** No `claude/backlog/backlog.md` items found with `Provisional-Target: Before v7.3 sprint planning`.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Add 5 missing prompt-change-log rows (see Hygiene Advisories) | Head of Specs Team | No |
| Monitor `BLG-SPEC-92`/`BLG-SPEC-94` effort trend; be prepared to phase `BLG-SPEC-94` into a second sprint via amendment cycle if capacity tightens | PMO Lead | No |

No outstanding action is a Blocker.
