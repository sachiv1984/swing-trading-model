Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-04
Cycle: 2026-09-03__release-v9.1

# Sprint Capacity — v9.1

## Capacity Inputs

```
Sprint duration:    single sprint (no phasing this cycle)
Available capacity: ~24–28 working-day-equivalent units (claude/roadmap/workforce_capacity.md, unchanged since 2026-07-17)
Total capacity:     confirmed band, single-developer-context (no scarce-skill contention identified this cycle)
Skill constraints:  none flagged in workforce_capacity.md for this scope
```

## Item Effort Mapping

Effort estimates sourced from `release_plan.md ## Capacity Check` (schema v2). All 41 items carry an explicit effort band from `stage4_backlog_slice.md` — no `[ESTIMATE REQUIRED]` placeholders.

| EPIC | Items | Subtotal (days) |
|------|-------|------------------|
| EPIC-01 — Frontend Accessibility & UI Consolidation | ST-01..ST-07 (7) | 3.70 |
| EPIC-02 — Backend Reliability & Technical Debt | ST-08..ST-11 (4) | 6.10 |
| EPIC-03 — QA & Test Coverage | ST-12..ST-18 (7) | 3.30 |
| EPIC-04 — Governance Process Debt & Overdue Dispositions | ST-19..ST-28 (10) | 3.90 |
| EPIC-05 — Spec & Knowledge Debt / AI Governance Register | ST-29..ST-41 (13) | 10.50 |
| **Total** | **41** | **27.50** |

## Total Effort vs Capacity

27.50 days vs confirmed ~24–28 day band. Within band, at its upper bound (~98% of the 28-day ceiling). No over-allocation beyond the confirmed band — matches Product Owner's explicit "use full capacity" instruction recorded at release planning (`release_plan.md`, `cycle_summary.md`, 2026-09-03). **Capacity check outcome: pass, no WARN** (`state.json attributes.capacity_feasible: pass`; WARN applies only when estimated effort exceeds 28 days).

## Conditional (Deferred)

None. No ST item in this cycle carries `status: deferred_at_planning` with a `gate_condition` in `execution_state.json` — all 41 items in the authoritative backlog slice enter the sprint. (Items deferred at release planning — `BLG-FEAT-92`, `BLG-FEAT-73`, `BLG-FEAT-74`, `BLG-GOV-105`, `BLG-GOV-315` — never entered the backlog slice; see `sprint_planning_notes.md` Deferred Items.)

## Minimum Capacity Buffer Floor (Advisory — §1.5)

Scope effort ÷ confirmed capacity ceiling: 27.50 ÷ 28 = **98.2%** — exceeds the 95% buffer-floor recommendation (`sprint_planning_prompt.md` §1.5, ST-05/BLG-GOV-254). This is advisory, not a hard gate; §8's over-allocation rule (unchanged) is not triggered since scope remains within the confirmed band.

**Product Owner acknowledgement:** the "use full capacity" instruction given explicitly at release planning (2026-09-03) is treated as extending to this buffer-floor advisory — the Product Owner has already directed scope to the top of the band with full knowledge of the ~27.5d estimate (`cycle_summary.md`). Recorded here as the acknowledgement of record; see `sprint_planning_notes.md` for the explicit STEP 0 confirmation.

**Gate re-invocation:** If a gate condition on any deferred backlog item (`BLG-FEAT-92`, `BLG-FEAT-73`, `BLG-FEAT-74`) is met during the sprint, do not add it informally. Invoke the amendment cycle (`amend cycle --cycle 2026-09-03__release-v9.1 --reason "<gate met>"`) to add it to the sprint backlog.
