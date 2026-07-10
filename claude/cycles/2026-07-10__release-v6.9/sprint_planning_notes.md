# Sprint Planning Notes — 2026-07-10__release-v6.9

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-10
**Cycle:** 2026-07-10__release-v6.9

## Backlog Slice Source

Original — `claude/cycles/2026-07-10__release-v6.9/stage4_backlog_slice.md` (`amended_backlog_slice_path` empty — no amendment sealed for this cycle).

## Deferred Items

None. Both ST items from the authoritative backlog slice (ST-01/EPIC-01, ST-02/EPIC-02) are `include` — within capacity, owned, AC-confirmed. See `release_plan.md §Scope → Items explicitly deferred` for backlog items considered and not selected at release planning (out of this routine's scope to revisit).

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 (EPIC-01) | None | — | Resolved (independent) |
| ST-02 (EPIC-02) | None | — | Resolved (independent) |

No cross-item dependencies. `release_plan.md §Execution Plan`: "Both EPICs are independent (different backend surfaces, no shared data model change, no shared endpoint) — may execute in either order or in parallel." No shared source files identified between EPIC-01 and EPIC-02 (ST-01 touches Positions page detail view + a new compliance-recheck endpoint; ST-02 touches the Positions page Alerts column + gap-risk read path) — both touch `docs/specs/frontend/pages/positions.md` (confirmed via design gate: v2.0 → v2.1 added both the Compliance Recheck Panel and the Gap Risk badge in the same design-gate commit, so the spec is already unified going into execution) but no shared backend file. No circular dependency. No multi-EPIC `execution_state.json` ownership conflict beyond the standard first-in-sequence rule below.

## Execution Sequence

1. EPIC-01 — ST-01 (On-demand SI-01 compliance recheck) — designated `execution_state.json` owner (first in execution order; no dependency forces this order, EPIC-01 listed first in both `release_plan.md` and `stage4_backlog_slice.md`).
2. EPIC-02 — ST-02 (Overnight/weekend gap risk flag)

Both `delegated_frontend`; no autonomous items to sequence ahead of them. Independent EPICs — may also execute in parallel per `release_plan.md`.

**Multi-EPIC Execution Notes:** EPIC-01 owns `execution_state.json` (first in execution order). EPIC-02 must check for `execution_state.json` existence before creating its own version — if found, read it and append the EPIC-02 section rather than overwrite.

**Shared file ownership advisory:** `docs/specs/frontend/pages/positions.md` — both EPICs touch this file, but the design gate (`design_gate.md`, `b281a657`) already merged both spec sections (v2.0 → v2.1) into a single locked version before either EPIC starts execution, so no in-sprint rebase-on-merge is anticipated for this file. If either EPIC's execution reopens `positions.md` for further changes, the later-merging EPIC must rebase onto `main` after the earlier EPIC merges before finalising its own edit.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 | Valid — §13 sign-off (Strategy Rules & System Intent Owner) required at AC-04, not yet recorded; expected fast pass given SI-01 precedent per `release_plan.md`. |
| RISK-02 | EPIC-01, EPIC-02 | Resolved — Design Gate required and now **Passed** (`design_gate.md`, cleared 2026-07-10T18:15:00Z, 2 items cleared / 0 blocked). No longer a planning-time blocker. |
| RISK-03 | EPIC-02 | Valid — §13 sign-off (Strategy Rules & System Intent Owner) required at AC-04, not yet recorded; lower likelihood given reuse of existing deterministic calendar/OHLCV data per `release_plan.md`. |

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json`: **clean** — "No known vulnerabilities found."

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| §13 sign-off for ST-01 AC-04 (on-demand SI-01 recheck — no new automation/prediction surface) | Strategy Rules & System Intent Owner | No — same-sprint execution deliverable per `release_plan.md §1.4b`, not a planning-seal blocker |
| §13 sign-off for ST-02 AC-04 (gap risk flag — informational only, no directional prediction) | Strategy Rules & System Intent Owner | No — same-sprint execution deliverable per `release_plan.md §1.4b`, not a planning-seal blocker |

No outstanding action is marked `Blocker? Yes`.

## Hygiene Advisories (non-blocking, STEP -1.7)

Prompt change log gaps detected (current file version exceeds the most recent logged target version):

- ⚠ `roadmap_prompt.md` current v8.6 — last log entry v8.4→v8.5.
- ⚠ `backlog_management_prompt.md` current v1.11 — last log entry v1.8→v1.9.
- ⚠ `release_planning_prompt.md` current v2.42 — last log entry v2.40→v2.41.

Advisory only — does not block sprint planning. Recommend Head of Specs Team backfill the missing `prompt_change_log.md` rows per CLAUDE.md §6.

No `Provisional-Target: Before v6.9 sprint planning` backlog items found in `claude/backlog/backlog.md` — no Pre-Sprint Backlog Advisory section required.

## Carry-Forward Items

Carry-forward items reviewed: 2 items from cycle `2026-07-08__release-v6.8` (`lessons_learnt_closure.md`):

1. Route future "file a follow-up backlog item" lessons-learnt actions to an engine/owner with actual `backlog.md` write scope (Sprint Execution or an explicit PMO Lead `/backlog-add` action), not Delivery Verification or Post-Ship Closure. No action required this cycle — no such action item is pending.
2. SI-02 gate condition 1 should not be expected to clear from the `BLG-BE-46` forward-fix alone. Already reflected in `release_plan.md §1.4` and `cycle_summary.md` (confirmed still NOT MET, 0/20 linked trade-plans, live query this session). No further action.
