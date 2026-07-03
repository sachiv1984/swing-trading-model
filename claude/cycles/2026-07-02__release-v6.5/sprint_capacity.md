Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-03
Cycle: 2026-07-02__release-v6.5

---

# Sprint Capacity — 2026-07-02__release-v6.5

## 1.1 Capacity Inputs

```
Sprint duration:    Single sprint (cycle scoped as 1 sprint per cycle_summary.md Plan Overview)
Available FTE:      Solo developer, evenings/weekends (workforce_capacity.md baseline, effective 2026-05-27)
Total capacity:     ~12–14 working days (warn threshold: effort > 14 days)
Skill constraints:  None scarce this sprint — Head of Specs Team, Infrastructure & Operations Owner, QA & Testing Owner, Base44 Frontend, Head of UX & Design, Metrics Definitions & Analytics Owner all have single-item or light load; no concurrent scarce-skill conflict identified.
```

## 1.2 Item Effort Mapping

| EPIC | ST | Effort estimate | Source |
|------|----|-----------------|--------|
| EPIC-01 | ST-01 | XS (<1 hour) | release_plan.md Execution Plan / stage4_backlog_slice.md |
| EPIC-01 | ST-02 | S (~0.5 day) | release_plan.md Execution Plan / stage4_backlog_slice.md |
| EPIC-01 | ST-03 | XS (<1 hour) | release_plan.md Execution Plan / stage4_backlog_slice.md |
| EPIC-02 | ST-04 | XS (<1 hour) | release_plan.md Execution Plan / stage4_backlog_slice.md |
| EPIC-02 | ST-05 | XS (<0.5 day) | release_plan.md Execution Plan / stage4_backlog_slice.md |
| EPIC-02 | ST-06 | XS (<1 hour) | release_plan.md Execution Plan / stage4_backlog_slice.md |
| EPIC-03 | ST-07 | S (~1 day) | release_plan.md Execution Plan / stage4_backlog_slice.md |
| EPIC-03 | ST-08 | S (~0.5 day) | release_plan.md Execution Plan / stage4_backlog_slice.md |

No `[ESTIMATE REQUIRED]` placeholders — all 8 items carry an effort estimate from release planning.

## 1.3 Total Effort vs Capacity

| EPIC | Mid-point effort |
|------|-------------------|
| EPIC-01 | ≈0.7 day |
| EPIC-02 | ≈0.6 day |
| EPIC-03 | ≈1.5 day |
| **Total** | **≈2.8 days** |

Total estimated effort (≈2.8 days) is well within confirmed capacity (~12–14 days). **Outcome: pass.** No over-allocation. No capacity WARN — Product Owner acknowledgement not required.

## 1.4 Conditional (Deferred) Items

None. `release_plan.md` §1.4b confirms no scope candidate carries a within-sprint or gate-conditional deferral — all 8 items are firm. No `execution_state.json` items are marked `deferred_at_planning` at this stage (Sprint Planning STEP 5.2 will record traceability entries for any slice item *not* entering the sealed backlog; all 8 slice items enter scope, so no such entries are required this cycle).
