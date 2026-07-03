**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-03
**Cycle:** 2026-07-02__release-v6.5

# Sprint Planning Notes — 2026-07-02__release-v6.5

## Backlog Slice Source

Original — `claude/cycles/2026-07-02__release-v6.5/stage4_backlog_slice.md`. `.claude_current_state.json` and `state.json` both carry `amended_backlog_slice_path: ""` — no amendment in effect.

## Deferred Items

None. All 8 ST items from the authoritative backlog slice are classified `include` — within capacity (≈2.8d of ≈12–14d), owned, AC-complete, no unresolved dependency or escalation blocking any item.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| EPIC-01 (ST-01/02/03) | None | — | N/A — independent of EPIC-02/03 per `release_plan.md` Execution Plan |
| EPIC-02 (ST-04/05/06) | None | — | N/A — independent of EPIC-01/03 per `release_plan.md` Execution Plan |
| EPIC-03 (ST-07/08) | Design Gate (ST-07) | Internal (spec) | Resolved — `design_gate_status = Passed` (2026-07-02T23:45:00Z), `design_gate.md` confirms ST-07 cleared with UX spec `docs/design/2026-07-02__release-v6.5/thesis-feedback-mechanism/ux_spec.md` v1.0 and `trade_plan.md` v0.8 |

No cross-item dependencies within any EPIC (ST-01/02/03 independent of each other; ST-04/05/06 independent of each other; ST-07/08 independent of each other). No circular dependencies detected.

## Execution Sequence

1. **EPIC-01 — Audit Remediation Cluster** (ST-01, ST-02, ST-03) — fully autonomous, no dependencies, unblocks earliest.
2. **EPIC-02 — Backlog Debt Clearance** (ST-04, ST-05, ST-06) — fully autonomous, no dependencies.
3. **EPIC-03 — AI Thesis Feedback Loop** (ST-07 delegated_frontend, ST-08 autonomous) — sequenced last per the "autonomous before delegated" grouping rule; ST-07's design gate pre-condition is already satisfied.

### Multi-EPIC Execution Notes

3 EPICs in scope (> 1) — `execution_state.json` ownership rule applies. **`execution_state.json` owner: EPIC-01`** (first in execution order). EPIC-02 and EPIC-03 branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite.

### Shared File Ownership Advisory

No shared source files identified across EPIC-01/02/03 this sprint:
- EPIC-01 touches: `OPERATIONAL_GUIDE.md`, `README.md`, `pmo_lead.md`, the governance prompt containing the staging-only AC protocol, the `FRICTION_LOAD` formula's defining prompt/spec, and a state file (per ST-01/ST-03 AC scope).
- EPIC-02 touches: `docs/ops/api_performance_baseline.md`, `tests/e2e/strategy-benchmark.spec.js`, `docs/testing/signals_scenarios.md`.
- EPIC-03 touches: Trade Plan frontend components (Base44), `metrics_definitions.md`, backend query/endpoint work per ST-07/ST-08.

No overlap — no rebase-ordering constraint required at merge time beyond the general EPIC-01→02→03 sequence above.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 | Valid — mitigation is procedural (apply CLAUDE.md §6 checklist in the same commit for any Class 6 prompt/OPERATIONAL_GUIDE touch); to be verified at delivery verification. |
| RISK-02 | EPIC-02 | Valid — mitigation is to follow the existing BLG-QA-37 mock/error-injection strategy for ST-05 AC-03 (API-error state). |
| RISK-03 | EPIC-03 | Resolved — design gate ran (`run design-gate --cycle 2026-07-02__release-v6.5`) and passed for ST-07 before this sprint planning invocation; no longer an open risk to sprint sealing. |

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json`: **clean** — no known vulnerabilities found across all 60 resolved backend dependencies (fastapi 0.135.1, anthropic 0.105.2, sqlalchemy 2.0.23, etc.). Initial invocation failed (`pip-audit: command not found` — not on this shell's `PATH`); the tool is installed via pipx (`/root/.local/bin/pip-audit`, v2.10.1) and was re-run directly at that path. No High/Critical CVEs; no PO/Head of Engineering risk acceptance required.

## Carry-Forward Items

Most recently completed cycle: `2026-07-02__release-v6.4` (`post_ship_complete = true`). Read `lessons_learnt_closure.md` §Carry-Forward — 5 items:

| # | Observation | Implication | Engine | Status re: v6.5 |
|---|-------------|-------------|--------|------------------|
| 1 | BLG-QA-61 / TSG-v60-01 unresolved 3 consecutive cycles. | Head of Specs Team must action a disposition before next release plan opens. | Release Planning | **Resolved** — `release_plan.md` §1.4a records the active disposition; BLG-QA-61 promoted to firm v6.5 scope as ST-06. |
| 2 | Deferred lessons-learnt patches from the immediately-prior cycle were not applied during the following cycle's sprint execution (caught only at closure). | Consider surfacing the prior cycle's still-open Deferred Items table as an explicit STEP 0 read at Release Planning. | Release Planning | Out of Sprint Planning's scope — Release Planning already published for this cycle; no action available here. |
| 3 | STEP 4's merge-gate resume-sync sub-step (execution_prompt.md) has no branch check, risking an orphaned write on a stale `exec/**` branch. | Add an explicit branch check mirroring STEP 5's existing branch-ordering gate. | Sprint Planning (tag as recorded in source; substantively an `execution_prompt.md` STEP 4 patch) | Not actionable within Sprint Planning's write scope (`execution_prompt.md` is not a permitted write path for this engine). Surfaced here for Head of Specs Team visibility; recommend a dedicated backlog item / direct prompt patch outside this routine. |
| 4 | Skill-Silo rolling-3-cycle average was in Alert territory (53.2%) at the rebalance shaping v6.4. | Confirm at next rebalance whether bundling BLG-FEAT-54 corrected the average. | Roadmap | Already actioned — `2026-07-02__scheduled` rebalance recorded the average worsened to 64.8% and pulled BLG-FE-46 forward into v6.5 scope (now ST-07). |
| 5 | AI-adjacent security items derived ad hoc from the same risk assessment for 2 consecutive cycles. | If a 3rd consecutive release repeats this pattern, escalate the standing AI safety checklist proposal from advisory to a scoped backlog item. | Release Planning | Not triggered this cycle — v6.5 scope (ST-07/ST-08) is AI-thesis-feature work, not ad hoc AI/security risk-assessment-derived scope; condition does not recur this release. |

Recorded per `shared_standards.md §16.8` — advisory only, no halt.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| **BLG-ID cross-reference defect:** `stage4_backlog_slice.md` (and `release_plan.md`, `cycle_summary.md`, and `backlog.md`'s own release-slice mapping table) label ST-01 as `BLG-GOV-157` and ST-03 as `BLG-GOV-159`, but the actual `backlog.md` entries have these titles swapped (`BLG-GOV-157` = "OPERATIONAL_GUIDE/prompt version-sync drift" = ST-03's real content; `BLG-GOV-159` = "Lifecycle/prompt/state wording and consistency fixes" = ST-01's real content). ST content/ACs are internally correct and unaffected — only the upstream ID label is wrong. Risk: post-ship closure / `groom backlog` may archive the wrong BLG item against each story. Not fixable within Sprint Planning's write scope (`stage4_backlog_slice.md` sealed; `backlog.md` grooming out of scope). | Head of Specs Team | No |
| **LL-v2.0-P4-2 test scenario gap:** ST-07 (delegated_frontend) introduces a new user-facing control (thesis feedback 👍/👎) with no Playwright AC defined at planning time. Per CLAUDE.md's frontend Playwright hard gate, Sprint Execution must either add Playwright coverage for ST-07 AC-01, or file a backlog item via `/backlog-add` before the PR opens if staging sign-off is deferred. Set EPIC-03 `test_scenarios = "pending — QA & Testing Owner to author before next sprint on this domain"` in `execution_state.json` at Sprint Execution STEP 0. | QA & Testing Owner | No |
No action above is a seal blocker (`Blocker? No` for both) — both are advisory/process-hygiene items for Head of Specs Team and QA & Testing Owner respectively, to be actioned during or after Sprint Execution.

## Capacity WARN Acknowledgement

Not applicable — capacity check outcome is `pass` (≈2.8d vs ~12–14d available). `capacity_warn_acknowledged` will be omitted/`false` at STEP 7.

## Pre-Sprint Backlog Advisory

Scanned `claude/backlog/backlog.md` for `Provisional-Target: Before v6.5 sprint planning` — no matches found. No unconverted "Before Sprint Planning" items.
