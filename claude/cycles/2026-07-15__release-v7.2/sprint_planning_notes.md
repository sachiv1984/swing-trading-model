**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-15
**Cycle:** 2026-07-15__release-v7.2

# Sprint Planning Notes — 2026-07-15__release-v7.2

## Backlog Slice Source

Original — `claude/cycles/2026-07-15__release-v7.2/stage4_backlog_slice.md`. No amendment in effect (`amended_backlog_slice_path` absent/empty in `.claude_current_state.json`).

## Deferred Items

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| ST-03 (`BLG-FE-109`) | Blocked — `stage4_backlog_slice.md` EPIC-02 sequencing constraint requires `ST-02` to *complete* (execute) before `ST-03` enters sprint planning; `ST-02` is only entering its first sprint in this run. Design artefact and frontend spec already exist (`design_gate.md` PASSED) — purely a sequencing gate, not a design gap. | Yes — once `ST-02` executes and merges |
| ST-05 (`BLG-FE-110`) | Blocked — `stage4_backlog_slice.md` EPIC-03 sequencing constraint requires `ST-04` to *complete* (execute) before `ST-05` enters sprint planning. Design artefact already exists (`design_gate.md` PASSED). | Yes — once `ST-04` executes and merges |
| ST-06 (`BLG-FE-111`) | Blocked — same EPIC-03 sequencing constraint as `ST-05`, gated on `ST-04` completion. Design artefact already exists (`design_gate.md` PASSED). | Yes — once `ST-04` executes and merges |

Not a capacity-driven deferral (in-scope effort is 7.75 days midpoint against a ~12-14 day band — see `sprint_capacity.md §1.3`). This reflects `design_gate.md`'s explicit instruction: "Sprint Planning must still apply the ST-02→ST-03 and ST-04→ST-05/ST-06 sequencing constraints as written in `stage4_backlog_slice.md` regardless of design artefacts already existing."

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 | None | — | Ready |
| ST-02 | None | — | Ready |
| ST-04 | None | — | Ready |
| ST-07 | None | — | Ready |
| ST-08 | None (own AC-04 has a forward-reference to ST-03/ST-05/ST-06's sprint-backlog entries — see Outstanding Actions) | — | Ready |
| ST-03 | ST-02 (must complete execution) | Internal | Deferred — see `## Deferred Items` |
| ST-05 | ST-04 (must complete execution) | Internal | Deferred — see `## Deferred Items` |
| ST-06 | ST-04 (must complete execution) | Internal | Deferred — see `## Deferred Items` |

No circular dependencies detected.

## Execution Sequence

1. **EPIC-01** (ST-01) — mobile responsiveness baseline assessment, sequenced first per roadmap recommendation (RISK-01): findings may inform scope/approach for the readiness passes below, and definitely reach the Product Owner before `ST-03`/`ST-05`/`ST-06` (already deferred out of this sprint) begin.
2. **EPIC-02** (ST-02) — trade-plan-linkage readiness pass; independent of ST-01 in the hard-blocking sense but benefits from running after it per RISK-01's spirit.
3. **EPIC-03** (ST-04) — dashboard spec/instrumentation pass; same independence/ordering rationale as EPIC-02.
4. **EPIC-04** (ST-07) — notification consolidation audit; fully independent, may run in parallel with EPIC-02/EPIC-03.
5. **EPIC-05** (ST-08) — combined design review + shared Playwright suite plan. Note: the combined design review itself (AC-01/AC-03) was substantively satisfied by the `design_gate.md` run already on file (see that document's own Notes). `ST-08`'s remaining execution-time work is naming the shared Playwright spec file (AC-02) — see Outstanding Actions for the AC-04 forward-reference gap.

**RISK-01 handling (EPIC-01 → EPIC-02/EPIC-03):** The release plan's mitigation for RISK-01 ("PO reviews assessment report before EPIC-02/EPIC-03 sprint planning seals") is satisfied without phasing EPIC-02/EPIC-03 out of this sprint entirely: only the *readiness/spec passes* (`ST-02`, `ST-04`) are in scope this sprint, not the UI implementation stories (`ST-03`/`ST-05`/`ST-06`, already deferred per the sequencing-constraint gate above). Readiness/spec passes are documentation/confirmation work — inexpensive to adjust if `ST-01`'s findings suggest a change — and the actual implementation stories will not begin until a future sprint planning run, by which point `ST-01`'s findings will be fully available to the Product Owner. No additional gating needed for `ST-02`/`ST-04` beyond running `ST-01` first in execution sequence.

**Multi-EPIC Execution Notes (Required — 5 EPICs in scope):**
- `execution_state.json` owner: **EPIC-01** (first in execution order). EPIC-02, EPIC-03, EPIC-04, EPIC-05 branches must check for `execution_state.json` existence before creating their own version — if found, read and append rather than overwrite.
- Merge sequence: EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-05.
- `execution_state.json` is initialised this run (did not previously exist for this cycle) with the 3 deferred-at-planning entries for `ST-03`/`ST-05`/`ST-06` per the Planning-deferred item traceability rule below.

**Planning-deferred item traceability (AUD-2026-05-21-002):** `execution_state.json` initialised this run with:
```yaml
epics.EPIC-02.stories.ST-03:
  status: deferred_at_planning
  gate_condition: "ST-02 (BLG-SPEC-89) must complete execution before ST-03 enters sprint planning — stage4_backlog_slice.md EPIC-02 sequencing constraint"
epics.EPIC-03.stories.ST-05:
  status: deferred_at_planning
  gate_condition: "ST-04 (BLG-SPEC-90) must complete execution before ST-05 enters sprint planning — stage4_backlog_slice.md EPIC-03 sequencing constraint"
epics.EPIC-03.stories.ST-06:
  status: deferred_at_planning
  gate_condition: "ST-04 (BLG-SPEC-90) must complete execution before ST-06 enters sprint planning — stage4_backlog_slice.md EPIC-03 sequencing constraint"
```

**Shared file ownership advisory (Required — 5 EPICs in scope):** Cross-checked `spec_references` across all 5 in-scope stories in `stage4_backlog_slice.md`. No file is targeted by more than one EPIC:
- EPIC-01 owns: no code/doc writes — assessment report only (reads `Dashboard.js`, `Positions.js`, `Screener.js`, trade plan form, Red Flag Journal for assessment purposes only).
- EPIC-02 owns: `docs/specs/api_contracts/*` (new entry pre-staged), `data_model.md` (field documented) — documentation only, no code change.
- EPIC-03 owns: `design_system.md`, Base44 prompt template library (documentation), `src/pages/DashboardHome.js` (instrumentation only, AC-03).
- EPIC-04 owns: no code/doc writes — findings report only (reads `Notifications.js`, `NotificationsHistory.js`, `NotificationPreferences.js`, `WeeklyDigest.js` for audit purposes only).
- EPIC-05 owns: no code writes — process/planning item; `tests/e2e/*` referenced for Playwright spec-file naming convention only, not yet writing a spec file (deferred until `ST-03`/`ST-05`/`ST-06` land).

No cross-EPIC shared-file conflict identified.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 | Valid — mitigation satisfied via execution sequencing (EPIC-01 first) plus the fact that EPIC-02/EPIC-03's implementation stories are already deferred out of this sprint; see `## Execution Sequence` RISK-01 handling note above |
| RISK-02 | EPIC-02 (ST-02, in scope) | Valid — `ST-02` scope point (6) explicitly confirms the §13 boundary before `ST-03` implementation begins; `ST-03` itself deferred this sprint, so the boundary confirmation happens with no implementation-timeline pressure |
| RISK-03 | EPIC-03 (ST-04, in scope) | Valid — `ST-04` formalises the `DataState` pattern and card-hierarchy treatment in `design_system.md`/frontend_specs before `ST-05`/`ST-06` (deferred) begin |
| RISK-04 | EPIC-04 (ST-07, in scope) | Valid, Low — scope explicitly limited to audit + findings report this sprint; no capacity risk |
| RISK-05 | EPIC-05 (ST-08, in scope) | Valid, Low — combined design review substantively completed via `design_gate.md`; remaining risk is the AC-04 forward-reference to `ST-03`/`ST-05`/`ST-06` sprint-backlog entries, tracked as an Outstanding Action below |

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json` — **clean**. No known vulnerabilities found across all 60 scanned dependencies.

## Pre-Sprint Backlog Advisory

No backlog items found with `Provisional-Target: Before v7.2 sprint planning` (`grep` against `claude/backlog/backlog.md` returned no match). No advisory required.

## Carry-Forward Items

Reviewed `claude/cycles/2026-07-12__release-v7.0/lessons_learnt_closure.md ## Carry-Forward` (most recent cycle with `post_ship_complete = true`; `.claude_current_state.json.last_post_ship_cycle = "2026-07-12__release-v7.0"`): 1 item present, targeted at the **Release Planning** engine (capacity-filling selection heuristic vs. Product Value Ratio alert state — should inform `release_planning_prompt.md` STEP 2, not this engine). Not actionable within Sprint Planning's scope; noted for traceability only.

Note: `claude/cycles/2026-07-14__release-v7.1/lessons_learnt_closure.md` exists on disk (`Status: Active`) but `post_ship_complete` has not been set for v7.1 in `.claude_current_state.json` (still names v7.0 as `last_post_ship_cycle`) — v7.1's post-ship closure has not been finalised even though v7.2 release planning and design gate have already run. This is a process-sequencing gap outside Sprint Planning's write scope; flagged as an advisory only (see `## Outstanding Actions`).

## Governance Drift Advisory (non-blocking)

`.claude_current_state.json.design_gate_status` still reads `"not_started"` at the time of this run, while the cycle's own `claude/cycles/2026-07-15__release-v7.2/state.json` correctly shows `design_gate_status: "Passed"` (completed 2026-07-15T23:10:00Z, record on file). Per `sprint_planning_prompt.md` STEP -1 check 3, the authoritative field for this gate is the cycle-level `state.json`, so no hard gate fired and this run proceeded correctly. However, the top-level pointer field appears not to have been updated by the design gate engine when it ran — this looks like a missed write in `design_gate_prompt.md`'s own state-update step. Flagged for a future prompt-hygiene pass; does not block this run (STEP 7 of this engine will refresh `.claude_current_state.json` regardless).

Also: prompt change log gap — `claude/system/sprint_planning_prompt.md` current version is `3.13`, but the most recent logged transition in `claude/system/prompt_change_log.md` (via `head -1` on a grep match) targets `v3.12`. Advisory only per STEP -1.7; recommend a prepended changelog row be added in a future governance-hygiene pass.

Also: `claude/cycles/<cycle_id>/execution_state.json` is written by this run (STEP 5.2 Multi-EPIC ownership designation + Planning-deferred item traceability, both explicitly instructed at `sprint_planning_prompt.md` lines 441/445) but `execution_state.json` is not enumerated in `§6 Write Scope Restriction`'s permitted-paths list. Proceeded on the basis that STEP 5.2's explicit, repeated instruction to write this file reflects intended behaviour and §6's list is simply incomplete — but flagging the inconsistency for a future governance-hygiene pass to add `claude/cycles/<cycle_id>/execution_state.json (create/append)` to §6.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Name the shared Playwright spec file (`ST-08` AC-02) and backfill it into `ST-03`/`ST-05`/`ST-06`'s sprint-backlog entries (`ST-08` AC-04) once those stories enter a future sprint planning run | Head of UX & Design / Director of Quality | No — execution/next-sprint-planning-time action, `ST-03`/`ST-05`/`ST-06` are not in this sprint |
| Reconcile `.claude_current_state.json.design_gate_status` write gap (design gate engine did not update the top-level pointer field) | Head of Specs Team | No — advisory, future prompt-hygiene pass |
| Add prepended `prompt_change_log.md` row for `sprint_planning_prompt.md` v3.12→v3.13 | Head of Specs Team | No — advisory, governance hygiene |
| Finalise v7.1 post-ship closure (`lessons_learnt_closure.md` on file but `post_ship_complete` not set; v7.2 release planning/design gate already ran ahead of it) | PMO Lead | No — outside Sprint Planning's write scope; flagged for visibility only |
