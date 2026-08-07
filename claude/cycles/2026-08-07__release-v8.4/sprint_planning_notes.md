# Sprint Planning Notes — 2026-08-07__release-v8.4

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-07
**Cycle:** 2026-08-07__release-v8.4

## Backlog Slice Source

Original — `claude/cycles/2026-08-07__release-v8.4/stage4_backlog_slice.md`. `amended_backlog_slice_path` in `.claude_current_state.json` is empty; no amendment sealed for this cycle.

## Deferred Items

None. All 31 items in the authoritative backlog slice are classified `include` (see STEP 3 review below) — capacity accommodates full scope at the top of the confirmed ~24-28 day band (`sprint_capacity.md`).

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| EPIC-02/ST-02 | — (foundational; no upstream dependency) | Internal | N/A |
| EPIC-02/ST-03–ST-09 | EPIC-02/ST-02 (openapi.yaml structural fix) | Internal (sequencing recommendation, not a hard block — `release_plan.md` states "Sequence ST-02 first within EPIC-02"; ST-03/05/06/08/09 touch other files and could technically proceed in parallel, but ST-02 first avoids rework if OpenAPI Drift Detection gate behaviour shifts) | Resolved — ST-02 has no unmet precondition, sequenced first within EPIC-02 |
| EPIC-05/ST-20 | EPIC-02/ST-02 | Cross-EPIC (explicit — endpoint list must be re-verified against the corrected `openapi.yaml`) | Resolved — EPIC-02 sequenced before EPIC-05 in execution order below |
| EPIC-03/ST-11 | `BLG-BE-80` (`retry_with_backoff` pattern) | External | Resolved — shipped v8.3, no in-cycle dependency |
| EPIC-05/ST-19 | `BLG-OPS-129` | External | Resolved — shipped v8.3, no in-cycle dependency |
| EPIC-04/ST-01, EPIC-04/ST-16 | Design Gate pass | Internal (gate) | Resolved — `design_gate_status = Passed`, `claude/cycles/2026-08-07__release-v8.4/design_gate.md` |
| EPIC-07/ST-30 | Genuinely parallel EPIC branches in the same sprint (structural — depends on branch assignment, not another story's completion) | Internal (structural) | Resolved — see Multi-EPIC Execution Notes below (EPIC-02 / EPIC-03 assigned as the parallel pair) |

No circular dependencies identified.

## Execution Sequence

1. **EPIC-02** — API Contract & Spec Debt Closure (ST-02 first within the EPIC, then ST-03–ST-09 in any order)
2. **EPIC-03** — Backend Engineering Hardening *(runs in parallel with EPIC-02 — see Multi-EPIC Execution Notes)*
3. **EPIC-01** — User-Facing Reporting Enhancement
4. **EPIC-04** — Frontend Code Health, Accessibility & Security
5. **EPIC-05** — Operational Reliability & Cost Monitoring *(starts only after EPIC-02 merges to `main` — ST-20's dependency on ST-02)*
6. **EPIC-06** — QA & Test Infrastructure Hardening
7. **EPIC-07** — Governance Process Integrity *(ST-30's dry-run writeup follows the EPIC-02/EPIC-03 parallel-branch merge; ST-29 has no dependency and may start any time)*

Autonomous items are not otherwise gated ahead of delegated items in this sprint — see Delegation Classes in `sprint_backlog.md`; the only delegation-shaped sequencing consideration is EPIC-05/ST-19, ST-20, ST-21 (`delegated_decision` — staging evidence gathering), which should be scheduled once EPIC-05 opens per the sequence above.

## Multi-EPIC Execution Notes

**`execution_state.json` owner:** EPIC-02 (first in execution order). All other EPIC branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite (per `sprint_planning_prompt.md §5.2`).

**Parallel-branch assignment for EPIC-07/ST-30 (RISK-07 mitigation):** EPIC-02 and EPIC-03 are assigned as the genuinely parallel pair this sprint. Rationale: (a) no sequencing constraint exists between them (only EPIC-02→EPIC-05 is a hard dependency), (b) both touch `data_model.md` (EPIC-02/ST-08, ST-09; EPIC-03/ST-10, ST-13, ST-14), giving the `CLAUDE.md §8` cross-EPIC merge conflict runbook genuine shared-file material to exercise, including the §8.2a "identical-text-masks-differing-semantics" version-bump collision check if both branches independently bump `data_model.md`'s footer version. ST-30's dry-run writeup and any runbook gaps found should be filed as follow-ups once this merge completes.

**Shared file ownership advisory:**

| File | EPICs touching it | Canonical-version owner | Note |
|------|--------------------|--------------------------|------|
| `data_model.md` | EPIC-02 (ST-08, ST-09), EPIC-03 (ST-10, ST-13, ST-14) | EPIC-02 (merges first per execution order) | EPIC-03 must rebase onto `main` after EPIC-02 merges before finalising its `data_model.md` changes. This is also ST-30's exercise case — apply `CLAUDE.md §8` in full, including step 2a, when resolving. |
| `openapi.yaml` | EPIC-02 (ST-02, ST-07) only | EPIC-02 | No cross-EPIC conflict expected — no other EPIC touches this file this cycle. |
| `execution_state.json` | All 7 EPICs (routine multi-EPIC artefact, not a content conflict) | EPIC-02 (see owner designation above) | Standard append-not-overwrite handling per `sprint_planning_prompt.md §5.2`. |

No other cross-EPIC shared-file collisions identified from the backlog slice's stated scope.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-02 | Valid — ST-02's own AC (paths-count cross-check + OpenAPI Drift Detection CI gate) is the objective, automated mitigation; unchanged since release planning |
| RISK-02 | EPIC-04 | Valid — ST-18's own AC requires a full inline-usage audit and functional-regression confirmation before merge; unchanged |
| RISK-03 | EPIC-03 | Valid — ST-13/ST-14 ACs remain narrowly scoped (extend existing pattern; generate-and-triage); unchanged |
| RISK-04 | EPIC-06 | Valid — ST-26's exact-count-match AC remains mechanically verifiable; unchanged |
| RISK-05 | Release-level | Valid — documented and PO-accepted at release planning (`run_manifest.md §STEP 2`); no new information this session |
| RISK-06 | EPIC-05 | Valid — ST-20 flagged `delegated_decision` in `sprint_backlog.md` in direct response to this risk (staging access + ≥5 samples/endpoint is execution-time cost, not a planning blocker) |
| RISK-07 | EPIC-07 | Valid — resolved at planning time via the explicit parallel-branch assignment above (EPIC-02 / EPIC-03), removing the "no natural parallel-branch opportunity" contingency named in the release plan's mitigation |

No risk has materialised since release planning (same-day cycle; no new information).

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json` — **clean**. 58 dependencies scanned, 0 known vulnerabilities, 0 fixes required.

## Endpoint Test Coverage Audit (STEP -1 advisory 8)

`python3 scripts/audit_endpoint_test_coverage.py` — **clean**. 78 route decorators scanned across 23 router files; 8 documented `KNOWN_GAPS` exclusions; 0 undocumented gaps.

## Prompt Change Log Gap Detection (STEP -1 advisory 7, date-scan method)

All 15 Class 6 governance prompts with a `**Version:**` header checked against `claude/system/prompt_change_log.md` using the date-scan method (latest-dated row per filename, not file position). No gaps found — every prompt's current version matches its changelog's latest-dated target version:

`amendment_cycle_prompt.md` v1.9, `backlog_management_prompt.md` v1.13, `delivery_verification_prompt.md` v3.7, `design_gate_prompt.md` v1.9, `execution_prompt.md` v3.65, `idea_intake_prompt.md` v2.8, `ideas_housekeeping_prompt.md` v1.2, `lessons_learnt_prompt.md` v1.10, `OPERATIONAL_GUIDE.md` v4.145, `post_ship_closure.md` v2.24, `release_planning_prompt.md` v2.47, `roadmap_management_prompt.md` v1.4, `roadmap_prompt.md` v9.13, `shared_standards.md` v3.26, `sprint_planning_prompt.md` v3.16 — all current.

## Pre-Sprint Backlog Advisory

No `claude/backlog/backlog.md` items found with `Provisional-Target: Before v8.4 sprint planning`.

## Carry-Forward Items

3 items reviewed from cycle `2026-08-05__release-v8.3` (`lessons_learnt_closure.md ## Carry-Forward`):

1. `BLG-OPS-13`/`BLG-OPS-133` overlap — targeted at Backlog Management (`groom backlog`), not Sprint Planning. No action here; noted for the next grooming run.
2. `execution_prompt.md §7` backlog write-scope escalation, 3 consecutive cycles unresolved — targeted at Sprint Execution/PMO Lead, applies to the next `run sprint` invocation, not this planning routine. Flagged below as a non-blocking Outstanding Action for execution-time awareness.
3. Cross-EPIC merge conflict retrospective (`8a62cfc1`, EPIC-06/ST-27 at v8.3) — targeted at Post-Ship Closure/Head of Specs Team. No action here; relevant precedent already reflected in this cycle's `CLAUDE.md §8` step-2a application to the EPIC-02/EPIC-03 shared-file advisory above.

No item names "Sprint Planning" or "All" as the responsible engine — no direct action required at this routine; all 3 reviewed and carried forward in context above where relevant.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Awareness: `execution_prompt.md §7` backlog write-scope escalation remains unresolved (3 consecutive cycles) — apply heightened attention at `run sprint` invocation for this cycle | PMO Lead | No |
| Staging evidence gathering for ST-19/ST-20/ST-21 (`delegated_decision`, live/staging environment required) — schedule once EPIC-05 opens in execution sequence | Infrastructure & Operations Owner | No |
| HoST design-session check (LL-v2.2-SP-01) for `delegated_decision` items ST-19/ST-20/ST-21: N/A — these are operational staging-verification tasks, not UX/architecture design decisions; no HoST design artefact applies | Head of Specs Team | No |

No outstanding action is marked `Blocker? Yes`.
