**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-17
**Cycle:** 2026-07-17__release-v7.4

# Sprint Planning Notes — 2026-07-17__release-v7.4

## Backlog Slice Source

Amended — `claude/cycles/2026-07-17__release-v7.4/amendments/AMD-20260717-01/amended_backlog_slice.md`. `.claude_current_state.json` `amended_backlog_slice_path` is present and non-empty, so per §5 this file supersedes `stage4_backlog_slice.md` for Sprint Planning purposes. The original 5-item `stage4_backlog_slice.md` remains the sealed historical record of the published release plan.

**Root state-pointer drift (advisory, non-blocking):** `.claude_current_state.json`'s own `design_gate_status` field still reads `not_started`, unchanged since Release Planning STEP 7 wrote it. The Design Gate Engine's re-run (commit `3bd5bbd2`) updated `claude/cycles/2026-07-17__release-v7.4/state.json` (`design_gate_status: Passed`) but did not mirror that field back to the root pointer. Per STEP -1 Hard Gate #3, this routine reads `design_gate_status` from the cycle-level `state.json` (authoritative for this check), so the drift does not block Sprint Planning — but it is a hygiene gap worth a backlog item (root pointer sync from Design Gate Engine writes).

## Carry-Forward Items

Reviewed `claude/cycles/2026-07-16__release-v7.3/lessons_learnt_closure.md ## Carry-Forward` (most recently completed cycle, `post_ship_complete = true`, per `.claude_current_state.json`). 3 items:

1. **`BLG-GOV-240` (STEP 8.1 empty-horizon gate gap):** Roadmap engine's own action item, not Sprint Planning's. No action required here.
2. **Capacity check landing near top-of-band for 3 consecutive cycles (v7.1/v7.2/v7.3):** This cycle **breaks** that pattern — 6.0-day midpoint effort against a ~24–28 day band (21–25% utilisation), the widest buffer of any v7.x sprint. Driven by the same-day DL-069 capacity-baseline increase plus `AMD-20260717-01`'s scope reduction. Recorded in `sprint_capacity.md §1.3`.
3. **Cross-EPIC merge conflicts (4th confirmed occurrence when 2+ EPIC branches open concurrently):** Not applicable this sprint — only 1 EPIC in scope.

## Deferred Items

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| ST-02 (`BLG-FE-115`) | Removed from cycle scope by `AMD-20260717-01` (Design Gate BLOCKED — no approved design artefact) | Yes — once a design artefact exists |
| ST-03 (`BLG-FE-116`) | Removed from cycle scope by `AMD-20260717-01` (Design Gate BLOCKED — no design artefact scheduled anywhere in v7.4 plan) | Yes — once a design artefact exists |
| ST-04 (`BLG-FE-117`) | Removed from cycle scope by `AMD-20260717-01` (Design Gate BLOCKED — no UX spec for confirmation/undo-window modal) | Yes — once a design artefact exists |
| ST-05 (`BLG-FE-118`) | Removed from cycle scope by `AMD-20260717-01` (Design Gate BLOCKED — no UX spec for empty state, no calendar-view design review) | Yes — once a design artefact exists |

These were removed from the authoritative backlog slice by a sealed amendment *before* Sprint Planning began — not classified `defer` by this engine's own STEP 3.1 review. They remain in `claude/backlog/backlog.md` (`BLG-FE-115/116/117/118`) unmodified, per §3.3.

The sole item in the authoritative (amended) slice, ST-01 (`BLG-SPEC-95`), is classified `include` — see Dependency Map below.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 (`BLG-SPEC-95`) | None | — | Ready |

No cross-item or cross-EPIC dependencies (single EPIC, single ST item in scope this sprint).

## Execution Sequence

1. EPIC-01 (ST-01) — `autonomous`, ready now, no blockers, no dependents in this sprint's scope.

No circular dependencies detected. Multi-EPIC ownership/merge-order provisions (§5.2) do not apply — only 1 EPIC in scope.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 | **Changed** — originally flagged as "critical path for all 4 downstream EPICs; any slip delays the whole release." Those 4 downstream EPICs (EPIC-02/03/04/05) are no longer in this sprint's scope (`AMD-20260717-01`), so EPIC-01 no longer gates any in-sprint work. The risk reverts to its ordinary form (readiness-pass document quality/completeness) — no elevated mitigation needed this sprint. |
| RISK-02 | EPIC-01 | Valid — `BLG-SPEC-95`'s AC still explicitly requires both `cmdk` and `react-day-picker` added to `package.json` in this same pass, even though the EPICs that would consume them (EPIC-02/EPIC-05) are deferred. Verify at EPIC-01 close per the original mitigation. |
| RISK-05 | (was EPIC-02, EPIC-05) | **Resolved** — §13 pre-check for `BLG-FE-115`/`BLG-FE-118` completed at the Design Gate re-run (`design_gate.md §Required Decision Resolved`): both PASS. No further action; applies whenever these items re-enter a future release's scope, unless the design deviates from what was assessed. |
| RISK-06 | Release-level | **Not applicable this sprint** — only 1 EPIC in scope, no concurrent-PR merge-conflict surface. |

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json`: **clean** — 61 dependencies scanned, 0 with known vulnerabilities.

## Hygiene Advisories (non-blocking)

**Prompt change log gaps** (per STEP -1 advisory 7 — current version ahead of last logged transition):
- ⚠ `sprint_planning_prompt.md` current v3.13 — last log entry targets v3.12.
- ⚠ `release_planning_prompt.md` current v2.42 — last log entry targets v2.41.
- ⚠ `execution_prompt.md` current v3.57 — last log entry targets v3.55 (2 versions behind).
- ⚠ `roadmap_prompt.md` current v9.2 — last log entry targets v9.0 (2 versions behind — widened since v7.3's 1-version gap).
- ⚠ `backlog_management_prompt.md` current v1.12 — last log entry targets v1.9 (3 versions behind, unchanged since v7.3).

No gap found for `design_gate_prompt.md`, `delivery_verification_prompt.md`, `post_ship_closure.md`, `amendment_cycle_prompt.md`, `roadmap_management_prompt.md`, `ideas_housekeeping_prompt.md`, `idea_intake_prompt.md`. Recorded per CLAUDE.md §6 — Head of Specs Team to add the missing prepended rows to `claude/system/prompt_change_log.md` when convenient; advisory only, does not block this sprint.

**Root state-pointer drift:** See `## Backlog Slice Source` above — `.claude_current_state.json design_gate_status` not mirrored from cycle-level `state.json` by the Design Gate re-run. Advisory only.

**Pre-Sprint Backlog Advisory:** No `claude/backlog/backlog.md` items found with `Provisional-Target: Before v7.4 sprint planning`.

## AC Numbering Note (informational)

Unlike the equivalent v7.3 readiness-pass stories (`BLG-SPEC-91–94`, which carry `AC-01…AC-0N` identifiers in `stage4_backlog_slice.md`), ST-01's acceptance criteria in both `stage4_backlog_slice.md` and the amended slice are an unlabelled bullet list (7 items). The content is complete and was ratified by Product Owner + Head of Specs Team as part of `AMD-20260717-01`; this is a format inconsistency, not a missing-AC gap, so `standard` mode does not require an `[AC REQUIRED]` placeholder. For downstream traceability (Delivery Verification's AC matrix), the 7 bullets map 1:1 to AC-01…AC-07 in list order. Recorded here rather than edited into the sealed backlog slice (write-scope restriction, §6).

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Add 5 missing prompt-change-log rows (see Hygiene Advisories) | Head of Specs Team | No |
| Mirror `design_gate_status` from cycle-level `state.json` to the root `.claude_current_state.json` pointer whenever they diverge (file as backlog item) | Head of Specs Team | No |
| File `BLG-FE-115/116/117/118` re-entry once design artefacts exist (already tracked in `claude/backlog/backlog.md` — no new filing needed, confirm at next `plan release`) | Product Owner | No |

No outstanding action is a Blocker.
