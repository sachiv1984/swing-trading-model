Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-14
Cycle: 2026-08-14__release-v8.8

# Sprint Capacity — 2026-08-14__release-v8.8

## 1.1 Capacity Inputs

```
Sprint duration:    Not calendar-fixed — capacity expressed in working-day-equivalent effort units.
                     Cadence: ~1–2 calendar days between sprint starts (workforce_capacity.md, effective 2026-07-17);
                     back-to-back sprints permitted.
Available FTE:      1 (solo developer, evenings/weekends) — workforce_capacity.md
Total capacity:     ~24–28 working-day-equivalent units (unchanged since 2026-07-17)
Skill constraints:  None scarce/role-locked this cycle. Scope spans Backend, Frontend, QA, Security, Spec,
                     Governance domains — all deliverable by the single-developer execution engine +
                     delegated review roles named in the release plan's Execution Plan table.
```

Source: `claude/roadmap/workforce_capacity.md` (Sprint Capacity & Cadence Baseline, effective 2026-07-17) and `release_plan.md ## Capacity Check` (schema v2, embedded — no separate `stage4_5_capacity_check.md` this cycle).

## 1.2 Item Effort Mapping

Effort estimates sourced from `release_plan.md ## Capacity Check` (EPIC-level subtotals) and `stage4_backlog_slice.md` (per-story size band: XS/S/M/L). All 29 items carry an estimate — no `[ESTIMATE REQUIRED]` placeholders.

| EPIC | Stories | Subtotal (days) | Story effort bands |
|------|---------|------------------|---------------------|
| EPIC-01 | ST-01–ST-06 | 2.75 | S, S, S, XS, XS, S |
| EPIC-02 | ST-07–ST-12 | 7.25 | M, M, M (advisory), XS, XS, S |
| EPIC-03 | ST-13–ST-17 | 3.00 | M, XS, S, XS, XS |
| EPIC-04 | ST-18–ST-21 | 3.00 | S, S, S, S |
| EPIC-05 | ST-22–ST-25 | 2.50 | S, S, S, XS |
| EPIC-06 | ST-26–ST-27 | 1.00 | S, XS |
| EPIC-07 | ST-28–ST-29 | 1.00 | XS, XS |
| **Total** | **29 stories** | **20.50** | |

Note (ST-09, RISK-02): effort is explicitly advisory/not fully scoped at release planning. Product Owner confirmed at this sprint planning session (2026-08-14) that the **full linkage scope (schema + backend + frontend)** proceeds — see `sprint_planning_notes.md` Outstanding Actions and Risk Flags. The M estimate above reflects this full-scope decision; if actual effort materially exceeds M during execution, this is a risk to monitor, not a re-plan trigger on its own.

## 1.3 Total Effort vs Capacity

Total estimated effort: **20.50 days** vs confirmed capacity **~24–28 days**.

20.50 / 24 (conservative lower bound) = **~85.4% of capacity**. No over-allocation — comfortably within capacity with headroom. No items require deferral on capacity grounds.

## 1.4 Gate-Conditional Deferred Items

None. `release_plan.md` confirms "Items explicitly deferred: None" — all 29 items in the authoritative backlog slice are ungated and included in this sprint. No `Conditional (Deferred)` section required.

## 1.5 Minimum Capacity Buffer Floor (Advisory)

20.50 / 24 = 85.4%, well below the 95% buffer-floor recommendation (`sprint_planning_prompt.md` §1.5). No buffer-floor advisory triggered — no Product Owner acknowledgement required on this point.

## Capacity WARN

Not triggered. `release_plan.md ## Capacity Check` records `outcome: pass` (WARN only applies when estimated effort exceeds the band's upper bound — 20.50 is well under even the lower bound). `capacity_warn_acknowledged` remains unset/false in the STEP 7 state write.

## Phasing Recommendation

None present in `release_plan.md ## Capacity Check` — not applicable this cycle (no WARN, no phasing subsection).
