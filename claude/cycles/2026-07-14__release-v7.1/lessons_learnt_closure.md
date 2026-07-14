Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Cycle: 2026-07-14__release-v7.1
Release: v7.1
Last Updated: 2026-07-14
Authority: Post-Ship Closure Engine v2.17

---

# Lessons Learnt — Closure Summary: v7.1

Reviewed by: PMO Lead
Date filed: 2026-07-14
Prior cycle checked: claude/cycles/2026-07-12__release-v7.0/lessons_learnt_closure.md

## Classification Summary

| Count | Category |
|-------|----------|
| 0 | Immediate |
| 1 | Deferred (carried forward as Outstanding Action) |
| 1 | Escalated |

---

## Action Classification Detail

### Immediate (0)

None this cycle — no lessons learnt action item was both unambiguous and fully resolvable within this run's write scope.

### Deferred (1 — carried to next cycle or next relevant engine invocation)

| ID | Source | Summary | Owner | Target |
|----|--------|---------|-------|--------|
| Release Planning Carry-Forward #2 | Release Planning lessons_learnt.md | This cycle's capacity check landed at exactly the top of the ~12–14 day capacity band (14.0d midpoint, ~15.5d pessimistic) after combining 3 mandatory anchors with 4 capacity-filling items — a WARN outcome with zero buffer. `BLG-BE-60`'s fix-vehicle choice (RISK-01) was a genuine either/or engineering decision deferred to execution kickoff rather than resolved at planning time. | Sprint Planning Engine / PMO Lead | Next `plan sprint` invocation — treat `release_plan.md §Capacity Check` Phasing Recommendation as a live option and confirm early whether any RISK-tagged fix-vehicle choice is trending toward the pessimistic estimate before committing to single-sprint delivery of all items |

### Escalated (1)

| ID | Source | Question | Owner | Deadline |
|----|--------|----------|-------|----------|
| Release Planning Friction Item 1 | Release Planning lessons_learnt.md | Should `backlog_management_prompt.md` (`groom backlog`) or `idea_intake_prompt.md` require an explicit day-range estimate alongside the letter effort band (S/M/L/XS) for any backlog item carrying a `Provisional-Target` value, so Release Planning STEP 4.5's capacity check does not have to infer ranges by analogy to unrelated prior items? First occurrence this cycle (not yet confirmed recurring); the item's own suggested-fix language explicitly deferred this judgment call rather than proposing an unambiguous patch. | Head of Specs Team | 2026-07-17 (72 hours from filing) |

---

## Closure-Phase Observations

- Both `docs/product/scope/scope--2026-07-14__release-v7.1-nightly-backtest-data-integrity.md` and `docs/product/decisions/decisions--2026-07-14__release-v7.1.md` were cleanly located and marked Superseded — no "not found" flag needed this cycle.
- Specs Index (`docs/specs/Specs_Index.md`) required no §6/§7 resolutions this run — no shipped ST item closed an open Pending Spec Work or Open Compliance Issue entry. §6.6 (`BLG-SPEC-72`) remains open, unchanged, out of scope. The one open TSG entry (`TSG-v6.8-01`/`BLG-QA-86`) remains open and unchanged. No new spec gaps surfaced (`verification_report.md §6` confirmed zero test scenario gaps this cycle) — no new numbered TSG section added, consistent with the v6.9/v7.0 precedent of noting "no gaps" in the Last Updated line rather than appending an empty section.
- The new P3 deviation (`DEV-REPORTS-ST06-01`, `BLG-SPEC-87`) arrived at closure fully pre-dispositioned by sprint execution and verification — description, canonical requirement, priority, target resolution ("TBD — not yet scheduled"), owner, and backlog reference all present in `reports.md §Known Deviations`; STEP 5 (deviation compliance check) required zero corrections. Following the precedent question of whether a per-deviation entry should also be duplicated into Specs Index §6/§7: confirmed this is not the established pattern (`DEV-EPIC01-ST05-01` was not duplicated there either at v7.0 closure) — Specs Index tracks document-level/structural gaps, not the general deviation registry, which lives in each canonical spec's own Known Deviations section.
- Endpoint coverage drift check (STEP 6): no new endpoints were added this cycle (confirmed via `git log --diff-filter=A -- backend/routers/` across both EPIC-01 and EPIC-03 commits — zero new router files or endpoints; ST-04's `PATCH /positions/{id}/mark-reviewed` fix reused the existing endpoint). No new drift introduced by v7.1; the long-standing accumulated openapi.yaml/`api_performance_baseline.md` gap remains tracked by its own pre-existing `BLG-OPS-13`-lineage backlog items, not restated here.
- STEP 3 (backlog reconciliation) and STEP 5 (deviation compliance) traced cleanly: all 7 shipped ST items marked ✅ COMPLETE in `backlog.md` against their `execution_state.json` `done` records (`BLG-BE-59`, `BLG-BE-60`, `BLG-FE-107`, `BLG-BE-61`, `BLG-QA-106`, `BLG-SPEC-83`, `BLG-SPEC-84`); both deviations (the new P3 and the closed P2) carried all required fields in their respective canonical specs with no correction needed.
- No stale parked items found (IMP-15 check) — zero items in `backlog.md` are marked `parked`, matching `verification_report.md §5`'s own finding that the authoritative backlog slice contained zero `parked`-status items.
- v7.0's carried-forward item (capacity-filling heuristic should check the live Product Value Ratio explicitly, rather than applying it ad hoc) was substantively resolved this cycle: Release Planning's own `lessons_learnt.md` "What worked well #1" confirms the PVR (0.33, Advisory) was checked explicitly before selecting the 4 capacity-filling items and the reasoning recorded in `run_manifest.md`. This closes the practice gap even though the underlying suggestion to codify the check as an explicit `release_planning_prompt.md` STEP 2 instruction was not itself applied as a prompt patch this cycle — since the target was "next `plan release` invocation" (this cycle) and that invocation demonstrably followed the practice, this is treated as resolved-in-practice rather than a 2-cycle unresolved-patch recurrence escalation per `lessons_learnt_prompt.md §3.7`.

---

## Recurrence Escalations

None. No friction item from this cycle matched a prior-cycle friction item with an unresolved outstanding action; no deferred patch has carried 2+ cycles without a `prompt_change_log.md` entry (see the v7.0 carry-forward note above, treated as resolved-in-practice rather than a recurrence).

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Backlog items carrying a `Provisional-Target` value sometimes have only a bare letter effort band (S/M/L/XS) with no explicit day range, forcing Release Planning's capacity check to infer ranges by analogy rather than reading them directly — right when the total can land close to a WARN threshold. | Head of Specs Team to decide (escalated, deadline 2026-07-17) whether `backlog_management_prompt.md` or `idea_intake_prompt.md` should require an explicit day range alongside the letter band for any item carrying `Provisional-Target`. | Roadmap |
| 2 | v7.1's capacity check landed at exactly the top of the capacity band (14.0d midpoint, ~15.5d pessimistic) with zero buffer, and one item's fix-vehicle choice (RISK-01) was a genuine either/or engineering decision deferred to execution kickoff rather than resolved at planning time. | Sprint Planning should treat the capacity check's Phasing Recommendation as a live option and confirm early in Sprint 1 whether any RISK-tagged fix-vehicle choice is trending toward the pessimistic estimate before committing to single-sprint delivery of all items. | Sprint Planning |

// ARTEFACT_STATUS
```json
{
  "cycle_id": "2026-07-14__release-v7.1",
  "phase": "Post-Ship Closure",
  "status": "present",
  "generated_utc": "2026-07-14T22:00:00Z"
}
```
