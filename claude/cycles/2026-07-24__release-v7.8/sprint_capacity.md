**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-26
**Cycle:** 2026-07-24__release-v7.8

# Sprint Capacity — 2026-07-24__release-v7.8

## 1.1 Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (autonomous execution engine; effort measured in working-day-equivalent units, not elapsed calendar time) — per workforce_capacity.md "Sprint Capacity & Cadence Baseline (Effective 2026-07-17)"
Available FTE:      1 (solo developer / autonomous execution engine)
Total capacity:     ~24-28 working-day-equivalent units
Skill constraints:  None scarce this cycle — no concurrent scarce-skill collisions identified (workforce_capacity.md §Workforce Economics Gate Assessment N/A this cycle; no Metrics Definitions or similarly scarce role required by any of the 12 EPICs)
```

## 1.2 Item Effort Mapping

Source: `release_plan.md ## Capacity Check` (schema v2).

| EPIC | Item | Effort Band | Midpoint (days) |
|------|------|-------------|------------------|
| EPIC-01 | BLG-FE-128 | M | 2.0 |
| EPIC-02 | BLG-FEAT-84 | S | 1.0 |
| EPIC-03 | BLG-FE-127 | S | 1.0 |
| EPIC-04 | BLG-FE-125 | M | 2.0 |
| EPIC-05 | BLG-FEAT-81 | S | 1.0 |
| EPIC-06 | BLG-FEAT-82 | M | 2.0 |
| EPIC-07 | BLG-SEC-20 | S | 1.0 |
| EPIC-08 | BLG-SEC-21 | M | 2.0 |
| EPIC-09 | BLG-BE-71 | M | 2.0 |
| EPIC-10 | BLG-QA-117 | M | 2.0 |
| EPIC-11 | BLG-QA-119 | M | 2.0 |
| EPIC-12 | BLG-OPS-117 | S | 1.0 |

All 12 items carry an effort estimate from `release_plan.md`. No `[ESTIMATE REQUIRED]` placeholders.

## 1.3 Total Effort vs Capacity

```
Total estimated effort:  ~19.0 days midpoint
Confirmed capacity:      ~24-28 working-day-equivalent
Utilisation:             ~68-79%
Outcome:                 pass (no over-allocation, no capacity WARN)
```

No over-allocation. STEP 3 scope selection may include all 12 EPICs without a capacity-driven deferral.

## 1.4 Gate-Conditional Deferred Items

None. Design Gate (`design_gate.md`, this cycle) cleared all 5 conditionally-gated EPICs (EPIC-01/03/04/05/06) — 0 blocked. No items carry `status: deferred_at_planning` in `execution_state.json`.
