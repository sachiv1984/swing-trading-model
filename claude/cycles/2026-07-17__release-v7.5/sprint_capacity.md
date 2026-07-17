Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-17
Cycle: 2026-07-17__release-v7.5

# Sprint Capacity — 2026-07-17__release-v7.5

## 1.1 Capacity Inputs

```
Sprint duration:    ~1–2 calendar days between sprint starts (back-to-back permitted); working-day baseline below
Available FTE:      1 (solo-developer context; all roles operated by the same engine)
Total capacity:     ~24–28 working-day-equivalent capacity units per sprint
Skill constraints:  None — no scarce-skill contention identified (release_plan.md, workforce_capacity.md)
```

**DL-069 capacity baseline verification (BLG-GOV-249, forward flag from `cycle_summary.md`):** `workforce_capacity.md` §"Sprint Capacity & Cadence Baseline (Effective 2026-07-17)" states the baseline as ~24–28 working days/sprint, warn threshold >28 days, effective 2026-07-17. `release_plan.md ## Capacity Check` uses the identical ~24–28 day baseline. **Result: Match — no discrepancy.** No stale cached figure found.

## 1.2 Item Effort Mapping

| EPIC | ST Item | Backlog item | Effort | Midpoint (days) | Source |
|------|---------|--------------|--------|------------------|--------|
| EPIC-01 | ST-01 | BLG-FE-115 | M (~1–2 days) | 1.5 | `release_plan.md ## Execution Plan` / `stage4_backlog_slice.md` |
| EPIC-02 | ST-02 | BLG-FE-116 | L (~3–5 days) | 4.0 | `release_plan.md ## Execution Plan` / `stage4_backlog_slice.md` |
| EPIC-03 | ST-03 | BLG-FE-117 | M (~1–2 days) | 1.5 | `release_plan.md ## Execution Plan` / `stage4_backlog_slice.md` |
| EPIC-04 | ST-04 | BLG-FE-118 | L (~3–5 days) | 4.0 | `release_plan.md ## Execution Plan` / `stage4_backlog_slice.md` |

No matching rows in `scored_initiatives.md` for any of the 4 EPICs (CPS = N/A, 0 active-initiative rows — confirmed at release planning STEP 4.5). Tier 3 resolution per `shared_standards.md §16.7`: using inline backlog estimates, no advisory required. All 4 items have effort estimates present — no `[ESTIMATE REQUIRED]` placeholders.

## 1.3 Total Effort vs Capacity

**Total estimated effort:** ~11–14 days (midpoint 11.0)
**Confirmed capacity:** ~24–28 days/sprint

Total effort is well within capacity even at the high end of each range (14 of 24–28 days, ~50–58% of ceiling). **No over-allocation.** No scope reduction required at STEP 3.

## 1.4 Gate-Conditional Deferred Items

None. All 4 ST items in the authoritative backlog slice were classified `conditional` pending Design Gate PASS (RISK-01); the Design Gate has since passed (4/4 cleared, `design_gate.md`, 2026-07-17) — no item remains gate-conditional at sprint planning. No `execution_state.json` entries required at this step.
