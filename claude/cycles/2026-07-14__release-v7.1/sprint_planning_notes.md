**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-14
**Cycle:** 2026-07-14__release-v7.1

# Sprint Planning Notes — 2026-07-14__release-v7.1

## Backlog Slice Source

Original — `claude/cycles/2026-07-14__release-v7.1/stage4_backlog_slice.md`. No amendment in effect (`amended_backlog_slice_path` absent/empty in `.claude_current_state.json`).

## Deferred Items

None. Product Owner elected full scope (all 3 EPICs, 7 stories) — see `## Capacity WARN Acknowledgement` below. No item classified `defer`.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 | None | — | Ready |
| ST-02 | None (soft-coordinate with ST-01 — RISK-02, same file `production_strategy.py`) | Internal (advisory) | Ready |
| ST-03 | Design Gate resolution (RISK-03) | Internal | Resolved — `design_gate.md` PASSED, Option (a) selected 2026-07-14 |
| ST-04 | None | — | Ready |
| ST-05 | Design Gate resolution (RISK-04, AC-03 UX consistency review) | Internal | Resolved — `design_gate.md` confirms `docs/design/2026-07-12__release-v7.0/position-review-cadence-nudge/ux_spec.md` still current; AC-03 satisfied via design gate sign-off itself |
| ST-06 | None (design gate confirmed `ux_spec.md` colour convention still current; `reports.md` v0.8→v0.9 closed the spec-text gap this cycle) | — | Ready |
| ST-07 | None | — | Ready |

No circular dependencies detected.

## Execution Sequence

1. **EPIC-01** (ST-01, ST-02) — roadmap-mandatory P1 anchors; sequence or tightly coordinate the two PRs (RISK-02 — both touch `production_strategy.py`'s core signal/simulation path). Recommend ST-01 land first (smaller, isolates the point-in-time eligibility fix), then ST-02 (fix-vehicle selection at kickoff — RISK-01).
2. **EPIC-02** (ST-03) — small, now unblocked post-design-gate; Table View `AlertsCell` fix + `SC-RO-02` update in the same commit.
3. **EPIC-03** (ST-04, ST-05, ST-06, ST-07) — independent of EPIC-01/EPIC-02 and of each other; may run in parallel with, or after, EPIC-01/02. Sequenced last only because EPIC-01/02 are the roadmap-mandatory anchors — no technical dependency forces this order.

**Multi-EPIC Execution Notes (Required — 3 EPICs in scope):**
- `execution_state.json` owner: **EPIC-01** (first in execution order). EPIC-02 and EPIC-03 branches must check for `execution_state.json` existence before creating their own version — if found, read and append rather than overwrite (prevents the v3.3/v3.4 cross-EPIC collision class).
- Merge sequence: EPIC-01 → EPIC-02 → EPIC-03.

**Shared file ownership advisory (Required — 3 EPICs in scope):** Cross-checked `spec_references` across all 7 stories in `stage4_backlog_slice.md`. No file is targeted by more than one EPIC:
- EPIC-01 owns: `backend/services/production_strategy.py`, `import_backtest.py`, `backend/services/ticker_universe_service.py`.
- EPIC-02 owns: `src/pages/Positions.js` (`AlertsCell`), `tests/e2e/epic01-v62-stops-alerts.spec.js` (`SC-RO-02`).
- EPIC-03 owns (internally, across its own 4 stories — no cross-EPIC overlap): `docs/specs/frontend/pages/positions.md` (ST-04 AC-03, ST-05 AC-02), `docs/reference/openapi.yaml` (ST-06 AC-06, ST-07), `claude/system/metrics_definitions.md` (ST-06 AC-05), `backend/backend_engineering_patterns.md` (ST-07 AC-07), `docs/specs/frontend/pages/reports.md` (ST-06 — already at v0.9 post-design-gate).

No cross-EPIC shared-file conflict identified — the STEP 6.1 merge order rebase advisory is precautionary only this sprint.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-02) | Valid — fix vehicle (cache/append-only ledger/drift-alert) not yet selected; Backend Engineering Patterns Owner to select at kickoff/early execution and record the choice |
| RISK-02 | EPIC-01 (ST-01, ST-02) | Valid — mitigation (sequence/coordinate PRs touching `production_strategy.py`) carried into Execution Sequence above |
| RISK-03 | EPIC-02 (ST-03) | Resolved — Design Gate PASSED 2026-07-14, Option (a) selected (spec-compliance fix); `decision_record.md` on file |
| RISK-04 | EPIC-03 (ST-05) | Resolved — Design Gate confirmed existing v7.0 `ux_spec.md` still answers the UX consistency review in substance; AC-03 satisfied via gate sign-off itself |
| RISK-05 | EPIC-03 (ST-04–ST-07) | Valid, Low — 4 items span 4 owning roles but are independent; no single accountable EPIC owner beyond PMO Lead sequencing confirmation (this document) |

## Pre-Sprint Vulnerability Scan

`pip-audit` module not installed in `backend/.venv` (`No module named pip_audit`) — tool unavailable. Advisory only; does not block sprint planning. Recommend `backend/.venv/bin/pip install pip-audit` before sprint execution begins so the STEP -1.8 scan can run at the next planning cycle.

## Capacity WARN Acknowledgement

Capacity check outcome: **WARN** (14.0 days midpoint / ~15.5 days pessimistic vs ~12-14 day band, zero buffer — see `sprint_capacity.md §1.3`). The release plan's `§Capacity Check` proposed an alternative phasing (Sprint 1: EPIC-01+EPIC-02 ~6.0d; Sprint 2: EPIC-03 ~8.0d) in case the pessimistic case looked likely.

**Product Owner decision (2026-07-14):** Full scope — all 3 EPICs / 7 stories included in this single sprint. The Product Owner explicitly acknowledged the over-capacity risk (zero buffer at midpoint, ~1.5d overrun in the pessimistic case driven primarily by ST-02's fix-vehicle uncertainty, RISK-01) and elected not to phase EPIC-03 out. `capacity_warn_acknowledged = true` set at STEP 7.

## Pre-Sprint Backlog Advisory

No backlog items found with `Provisional-Target: Before v7.1 sprint planning` (`grep` against `claude/backlog/backlog.md` returned no match). No advisory required.

## Carry-Forward Items

Reviewed `claude/cycles/2026-07-12__release-v7.0/lessons_learnt_closure.md ## Carry-Forward`: 1 item present, targeted at the **Release Planning** engine (capacity-filling selection heuristic vs. Product Value Ratio alert state — should inform `release_planning_prompt.md` STEP 2, not this engine). Not actionable within Sprint Planning's scope; noted for traceability only.

## Governance Drift Advisory (non-blocking)

Top-level `.claude_current_state.json.status` reads `"Published"` at time of this run, while `claude/system/lifecycle_schema.json` names the equivalent state `Release_Planning_Complete` (its own description: "state.json status = Published" — referring to the *cycle-level* `state.json`, not the top-level pointer). `sprint_planning_prompt.md` STEP -1 hard gate #1 explicitly accepts `Published` as a valid top-level status for this engine's invocation, and `release_planning_prompt.md` line ~1057 confirms STEP 9 is "the only step that sets `status = Published`" in the top-level file — so this is the actual, current, intended vocabulary; `lifecycle_schema.json`'s table (`last_updated: 2026-03-10`) has not been reconciled with it. No hard gate fired — proceeding was correct per the operative (and more recent) instruction in `sprint_planning_prompt.md` itself. Recommend a future prompt-hygiene pass reconcile `lifecycle_schema.json`'s state names with the literal `status` values the engines actually write, per `CLAUDE.md §6`.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Select `BLG-BE-60` fix vehicle (RISK-01) | Backend Engineering Patterns Owner | No — execution-time decision |
| Install `pip-audit` in `backend/.venv` | Head of Engineering | No — advisory, next-cycle |
| Reconcile `lifecycle_schema.json` state names with actual `status` literals | Head of Specs Team | No — advisory, future prompt-hygiene pass |
