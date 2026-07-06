**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-06
**Cycle:** 2026-07-04__release-v6.6

# Sprint Planning Notes — 2026-07-04__release-v6.6

## Backlog Slice Source

Original — `claude/cycles/2026-07-04__release-v6.6/stage4_backlog_slice.md`. `.claude_current_state.json` and `state.json` both carry `amended_backlog_slice_path: ""` — no amendment in effect.

## Pre-Sprint Required Decisions Resolution

`cycle_summary.md ## Pre-sprint Planning Required Decisions` listed one High-priority decision: **[RISK-04] Design gate not yet cleared for ST-01/ST-02** — required `run design-gate --cycle 2026-07-04__release-v6.6` to reach Passed before `plan sprint`. **Resolved** — `design_gate.md` records Gate Status: PASSED (completed 2026-07-06; PMO Lead, Head of UX & Design, and Product Owner all confirmed); ST-01 cleared Design Not Applicable, ST-02 cleared Design Pre-Approved. No blocker remains.

**Process note (advisory, non-blocking):** `.claude_current_state.json` (root state pointer) still shows `design_gate_status: "not_started"` and `design_gate_record` pointing at the prior cycle (`2026-07-02__release-v6.5/design_gate.md`) — stale, not updated when the design gate commit (`03477fa4`) landed. The cycle-level `claude/cycles/2026-07-04__release-v6.6/state.json` is authoritative and correctly shows `design_gate_status: "Passed"`, which is what this run's STEP -1 hard gate check relied on. Recommend the PMO Lead correct the root pointer's `design_gate_status`, `design_gate_record`, and `design_gate_completed_utc` fields directly — outside this routine's STEP 7 write scope, which only covers the fields listed in `sprint_planning_prompt.md` §STEP 7.

## Deferred Items

None. All 4 ST items from the authoritative backlog slice are classified `include` — within capacity (≈3.5d of ≈12–14d), owned, AC-complete, no unresolved dependency or escalation blocking any item.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| EPIC-01 (ST-01/02) | None | — | N/A — independent of EPIC-02 per `release_plan.md` Execution Plan |
| EPIC-02 (ST-03/04) | None | — | N/A — independent of EPIC-01 per `release_plan.md` Execution Plan ("Sequencing constraint: None") |
| ST-01/ST-02 (Design Gate) | Design Gate | Internal (spec) | Resolved — `design_gate_status = Passed` (2026-07-06), `design_gate.md` confirms both ST-01 (Design Not Applicable) and ST-02 (Design Pre-Approved) cleared without disagreement |

No cross-item dependencies within either EPIC (ST-01/ST-02 independent of each other; ST-03/ST-04 independent of each other). No circular dependencies detected.

## Execution Sequence

1. **EPIC-02 — QA & Test Infrastructure Debt** (ST-03, ST-04) — both `autonomous`, no dependencies; sequenced first per the "autonomous before delegated" grouping rule (STEP 5.2).
2. **EPIC-01 — UX & Accessibility Debt** (ST-01, ST-02) — both `delegated_frontend`; design gate pre-condition already satisfied for both.

### Multi-EPIC Execution Notes

2 EPICs in scope (> 1) — `execution_state.json` ownership rule applies. **`execution_state.json` owner: EPIC-02** (first in execution order). EPIC-01's branch must check for `execution_state.json` existence before creating its own version — if found, read it and append its EPIC's section rather than overwrite.

### Shared File Ownership Advisory

No shared source files identified across EPIC-01/EPIC-02 this sprint:
- EPIC-01 touches: frontend component/style files for secondary/disclaimer text surfaces (ST-01 audit + any follow-up filings), Red Flag Journal component and its localStorage persistence layer (ST-02).
- EPIC-02 touches: `claude/backlog/backlog.md` / `claude/backlog/backlog_archive.md` (ST-03 ID renumbering), `backend/services/position_service.py` and `tests/conftest.py` `_DB_STUB_FUNCTIONS` (ST-04).

No overlap — no rebase-ordering constraint required at merge time beyond the general EPIC-02→EPIC-01 sequence above.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 | Valid — mitigation is Head of UX & Design sign-off (ST-01 AC-03) plus Playwright visual assertion for ST-02 (AC-03, already specified in the backlog slice); to be verified at delivery verification. |
| RISK-02 | EPIC-02 | Valid — mitigation is to grep all `claude/cycles/*/` and `claude/roadmap/` for any renumbered ID before finalising ST-03, per the item's own AC. |
| RISK-03 | EPIC-02 | Valid — mitigation is a verifying CI run before merge (ST-04 AC-02); if infeasible, resolves as a documented decision with no code change (zero regression risk). |
| RISK-04 | EPIC-01 | **Resolved** — design gate ran (`run design-gate --cycle 2026-07-04__release-v6.6`) and passed for both ST-01 and ST-02 before this sprint planning invocation; no longer an open risk to sprint sealing. |

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json`: **clean** — no known vulnerabilities found across all 59 resolved backend dependencies (fastapi 0.135.1, anthropic 0.105.2, sqlalchemy 2.0.23, etc.). No High/Critical CVEs; no PO/Head of Engineering risk acceptance required.

## Carry-Forward Items

Most recently completed cycle: `2026-07-02__release-v6.5` (`post_ship_complete = true`). Read `lessons_learnt_closure.md ## Carry-Forward` — 3 items:

| # | Observation | Implication | Engine | Status re: v6.6 |
|---|-------------|-------------|--------|------------------|
| 1 | DF-16 (LP-01): STEP 4.1 / STEP 7 state-sync sequencing in `release_planning_prompt.md` remains unresolved — two alternative fixes proposed, needs a design decision. | Head of Specs Team should pick one of the two named approaches at the next `release_planning_prompt.md` revision. | Release Planning | Not actionable within Sprint Planning's scope or write path. Surfaced for Head of Specs Team visibility. |
| 2 | DF-17 (LP-04): v6.5 bundled 2 U-items to test whether that corrects the rolling Skill-Silo Alert more effectively than a single-item pull-forward. | Check at next roadmap rebalance whether the rolling-3-cycle average moved back under threshold. | Roadmap | Already actioned — the `2026-07-03__scheduled` rebalance found the test confounded (only 1 of v6.5's 2 nominal U-items classified U) and named BLG-FE-82 + BLG-FEAT-52 as pull-forward candidates for v6.6, advising ≥2 committed U-items. `release_plan.md` §Readiness records BLG-FE-82 retained and BLG-FE-40 substituted for the gate-blocked BLG-FEAT-52. |
| 3 | DF-18: `/commit-check`'s pathspec-diff reinforcement has now missed its target once (v6.4→v6.5); `.claude/skills/` is outside every governed routine's declared write scope. | If still unapplied at v6.6, this becomes a 2-cycle carry-forward and an automatic recurrence escalation per `lessons_learnt_prompt.md` §3.7 — Head of Specs Team should apply it directly before that threshold is reached. | Release Planning | **Confirmed still unapplied** — `.claude/skills/commit-check/SKILL.md` contains no pathspec-diff reinforcement language, and no backlog item references DF-18. The 2-cycle threshold named in the v6.5 note is now met. Not actionable within Sprint Planning's write scope (`.claude/skills/` is not a permitted write path for this engine) — flagged here for Head of Specs Team to action directly, and for the next lessons-learnt-invoking engine (Sprint Execution / Post-Ship Closure) to raise the automatic recurrence escalation per §3.7. |

Recorded per `shared_standards.md §16.8` — advisory only, no halt.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| DF-18 recurrence threshold met (2-cycle carry-forward, `/commit-check` pathspec-diff patch still unapplied) — recommend filing a backlog item or direct prompt/skill patch outside this routine. | Head of Specs Team | No |
| Root `.claude_current_state.json` design gate fields are stale (see Pre-Sprint Required Decisions Resolution note above) — recommend correcting directly. | PMO Lead | No |

No action above is a seal blocker — both are advisory/process-hygiene items.

## Capacity WARN Acknowledgement

Not applicable — capacity check outcome is `pass` (≈3.5d vs ~12–14d available). `capacity_warn_acknowledged` will be omitted/`false` at STEP 7.

## Pre-Sprint Backlog Advisory

Scanned `claude/backlog/backlog.md` for `Provisional-Target: Before v6.6 sprint planning` — no matches found. No unconverted "Before Sprint Planning" items.
