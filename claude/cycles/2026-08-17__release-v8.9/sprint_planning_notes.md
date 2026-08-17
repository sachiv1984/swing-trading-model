**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-17
**Cycle:** 2026-08-17__release-v8.9

# Sprint Planning Notes — 2026-08-17__release-v8.9

## Backlog Slice Source

Original — `claude/cycles/2026-08-17__release-v8.9/stage4_backlog_slice.md` (`amended_backlog_slice_path` empty in `.claude_current_state.json` and `state.json` — no amendment sealed this cycle).

## Deferred Items

None. All 22 items in the authoritative backlog slice enter the sprint (Sprint 1 or Sprint 2). No item is deferred, blocked, or missing an owner/estimate/AC.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 | ST-01 | Internal (same position-data path) | Resolved — both scheduled Sprint 1, ST-01 sequenced first |
| ST-06 | ST-23 | Internal (§13 gate story, `LL-v3.5-SP-01` pattern) | Resolved — ST-23 sequenced Sprint 1, ST-06 deferred to Sprint 2 pending ST-23 `done` with PASS/CONDITIONAL |
| ST-07 | Head of Engineering reuse-feasibility confirmation (RISK-02, not a story dependency) | External (advisory, not blocking) | Open — to be confirmed early in EPIC-02 execution per Risk Register |
| ST-13 | Product Owner + Frontend Specifications & UX Documentation Owner decision (RISK-04) | Internal (decision precedes implementation, same story) | Open — sequence the decision early within EPIC-04 |

No circular dependencies detected.

## Execution Sequence

**Sprint 1** (EPIC merge order: EPIC-01 → EPIC-02 (Sprint-1 subset) → EPIC-03 → EPIC-04 → EPIC-05 → EPIC-06):

1. EPIC-01: ST-01 → ST-02 → ST-03
2. EPIC-02 (Sprint 1 subset): ST-23 (gate story, sequence early — unblocks Sprint 2's ST-06) → ST-04 → ST-05 → ST-07
3. EPIC-03: ST-08, ST-09, ST-10, ST-11 (no internal sequencing constraint)
4. EPIC-04: ST-13 (decision first, per RISK-04) → ST-12, ST-14, ST-15
5. EPIC-05: ST-16, ST-17, ST-18 (no internal sequencing constraint)
6. EPIC-06: ST-19, ST-20, ST-21, ST-22 (no internal sequencing constraint)

**Sprint 2** (opens once ST-23 reaches `done` with PASS/CONDITIONAL):

7. EPIC-02 (Sprint 2 subset): ST-06

Autonomous items are grouped ahead of delegated items within each EPIC where no other sequencing constraint applies, per §5.2 guidance — reflected in the classification table in `sprint_backlog.md`.

### Multi-EPIC Execution Notes

`execution_state.json` owner: **EPIC-01** (first in execution order; leads capacity allocation per `release_plan.md ## Execution Plan`). EPIC-02 through EPIC-06 branches must check for `execution_state.json` existence before initialising their own — if found, read and append their EPIC's section rather than overwrite.

### Shared File Ownership Advisory

No shared source files identified across EPIC-01 through EPIC-06 this cycle. Per `release_plan.md ## Integrity Validation — 3.5 Local Model Integrity`: each EPIC's data-model and spec touches are scoped to independent files (EPIC-01 → `positions.md`/backend stop-calc path; EPIC-02 → `trade_plan.md`/`strategy_benchmark.md`/`claude_audit_log`; EPIC-03–06 → independent backend/ops/governance files, no data-model impact). No cross-EPIC rebase coordination required beyond the standard merge order above.

### Planning-Deferred Item Traceability

Not applicable — no ST item in the authoritative backlog slice is excluded from the sealed sprint backlog. All 22 items enter (21 in Sprint 1, ST-06 in Sprint 2). No `deferred_at_planning` entries required in `execution_state.json` at initialisation.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-01) | Valid — regression test required before production change; backfill/recompute of existing open positions only after calc-path fix verified correct |
| RISK-02 | EPIC-02 (ST-07) | Valid — Head of Engineering to confirm `production_strategy.py` reuse feasibility early in EPIC-02; if infeasible, scope may narrow (see Multi-vehicle fix-choice check below) |
| RISK-03 | EPIC-03 | Valid — no material risk, standard review |
| RISK-04 | EPIC-04 (ST-13) | Valid — sequence PO/Frontend Specs decision early to avoid mid-sprint stall |
| RISK-05 | EPIC-05 | Valid — no material risk, standard review |
| RISK-06 | EPIC-06 (ST-21) | Valid — full CLAUDE.md §6 checklist must accompany `roadmap_prompt.md` STEP 8 edit in the same commit |

No risk has materialised since release planning (2026-08-17, same day).

**Multi-vehicle fix-choice risk check (LP-14):** RISK-02's mitigation is a single fallback path ("if reuse proves infeasible, scope may need to narrow"), not a multi-vehicle pick-one choice with materially different effort estimates — the check does not apply. No `### Phasing Recommendation` subsection exists in `release_plan.md ## Capacity Check` this cycle, so no cross-reference is applicable.

## Pre-Sprint Vulnerability Scan

Clean. `pip-audit -r backend/requirements.txt --format=json` (via `backend/.venv`): 58 dependencies scanned, 0 with known vulnerabilities.

## Pre-Sprint Endpoint Coverage Audit

Clean. `scripts/audit_endpoint_test_coverage.py`: 80 route decorators scanned across 23 router files; 8 documented `KNOWN_GAPS` exclusions; no undocumented gaps.

## Prompt Change Log Gap Scan

No gaps found. Date-scan method applied per shared_standards.md §STEP -1.7-Class Prompt Change Log Gap Detection across all 15 Class 6 governance prompts (`amendment_cycle_prompt.md`, `backlog_management_prompt.md`, `delivery_verification_prompt.md`, `design_gate_prompt.md`, `execution_prompt.md`, `idea_intake_prompt.md`, `ideas_housekeeping_prompt.md`, `lessons_learnt_prompt.md`, `OPERATIONAL_GUIDE.md`, `post_ship_closure.md`, `release_planning_prompt.md`, `roadmap_management_prompt.md`, `roadmap_prompt.md`, `shared_standards.md`, `sprint_planning_prompt.md`) — each file's current header `**Version:**` matches or trails the latest-dated `prompt_change_log.md` row naming it in its own filename column (not merely mentioning it in body text — an initial naive substring scan produced 3 false-positive gaps, corrected by restricting the match to the row's filename column).

## Carry-Forward Items

Reviewed: 2 items from cycle `2026-08-14__release-v8.8` (`lessons_learnt_closure.md ## Carry-Forward`). Note: `.claude_current_state.json`'s `last_post_ship_cycle` pointer is stale (reads `2026-08-11__release-v8.6`, a known bug — see `BLG-GOV-309`/ST-20 in this very sprint's scope, and `stage4_backlog_slice.md#ST-19` which fixes the writer). The actual most-recently-completed cycle was identified directly by filesystem evidence (`claude/cycles/2026-08-14__release-v8.8/closure_record.md` + `lessons_learnt_closure.md` both present, dated after v8.6) rather than trusting the stale pointer field.

| # | Observation | Implication | Engine | This-cycle disposition |
|---|-------------|-------------|--------|------------------------|
| 1 | Ungated P1/P2 backlog pool was nearly exhausted at v8.8 scoping time. | Treat as a scoping-input signal at the next scheduled rebalance; do not assume a ready P1/P2 pool exists without checking. | Roadmap | Not directly actionable by Sprint Planning — flagged for the next roadmap rebalance. |
| 2 | Two Phase 4 deferred patches (CI-green per-fix restatement clarification; canonical Sandbox Access Constraint block) carried v8.7 → v8.8 without a `prompt_change_log.md` entry. If still unapplied after the v8.8 → v8.9 transition, the §6.4 2-cycle-without-application threshold is crossed and both must escalate to Head of Specs Team rather than re-deferred a 3rd time. | The v8.8 → v8.9 transition has now occurred (this session). | All | **Threshold now crossed by the note's own wording** — out of Sprint Planning's write scope to resolve (not one of §6's permitted paths). Surfaced here as an Outstanding Action for Head of Specs Team; not a Sprint Planning hard gate. |

## Pre-Sprint Backlog Advisory

None found. No `claude/backlog/backlog.md` item carries `Provisional-Target: Before v8.9 sprint planning`.

## Design Gate Follow-Up (Non-Backlog-Slice Action)

`design_gate.md` notes a spec-debt gap found while documenting ST-04 (`PositionSizingWidget` baseline undocumented in `trade_plan.md`), with an explicit instruction: "Action for PMO Lead / Head of Specs Team: file a P3 Spec Debt backlog item (`/backlog-add`) for 'Document PositionSizingWidget baseline in trade_plan.md' after this routine completes." Sprint Planning's own write scope (§6) excludes `claude/backlog/backlog.md` — filed as a separate governance action immediately after this routine's STEP 8 commit, not as part of the sealed sprint artefacts.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Confirm `production_strategy.py` reuse feasibility for ST-07 (RISK-02) | Head of Engineering | No — early-EPIC-02 action, not a seal blocker |
| Sequence PO/Frontend Specs decision for ST-13 early in EPIC-04 (RISK-04) | Product Owner; Frontend Specifications & UX Documentation Owner | No |
| Full CLAUDE.md §6 checklist accompanying ST-21's `roadmap_prompt.md` STEP 8 edit (RISK-06) | Head of Specs Team | No — execution-time requirement |
| File P3 Spec Debt backlog item for `PositionSizingWidget` baseline documentation (design gate follow-up) | PMO Lead / Head of Specs Team | No — outside sprint scope, filed as a separate governance action post-commit |
| Escalate the 2 carried-forward Phase 4 deferred patches (now crossing the §6.4 2-cycle threshold) | Head of Specs Team | No — outside Sprint Planning's write scope; advisory only |

No outstanding action is marked `Blocker? Yes`.
