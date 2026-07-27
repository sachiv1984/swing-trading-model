**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-27
**Cycle:** 2026-07-27__release-v7.9

# Sprint Capacity — 2026-07-27__release-v7.9

## 1.1 Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (autonomous execution engine; effort measured in working-day-equivalent units, not elapsed calendar time) — per workforce_capacity.md "Sprint Capacity & Cadence Baseline (Effective 2026-07-17)"
Available FTE:      1 (solo developer / autonomous execution engine)
Total capacity:     ~24-28 working-day-equivalent units
Skill constraints:  None scarce this cycle — 15 EPICs span 11 distinct owner roles, no concurrent scarce-skill collision identified (per `release_plan.md ## Capacity Check`)
```

## 1.2 Item Effort Mapping

Source: `release_plan.md ## Capacity Check` (schema v2).

| EPIC | Item | Effort Band | Midpoint (days) |
|------|------|-------------|------------------|
| EPIC-01 | BLG-FEAT-66 | S (~1 day) | 1.0 |
| EPIC-02 | BLG-FEAT-67 | M (~2 days) | 2.0 |
| EPIC-03 | BLG-SPEC-105 | M (~2-3 days) | 2.5 |
| EPIC-04 | BLG-FEAT-85 | M (~2-3 days) | 2.5 |
| EPIC-05 | BLG-FEAT-87 | S (~1-2 days) | 1.5 |
| EPIC-06 | BLG-BE-73 | M (~2-3 days) | 2.5 |
| EPIC-07 | BLG-BE-74 | M (~2-3 days) | 2.5 |
| EPIC-08 | BLG-OPS-121 | S (~1-2 days) | 1.5 |
| EPIC-09 | BLG-QA-124 | M (~2-3 days) | 2.5 |
| EPIC-10 | BLG-QA-125 | S (~1-2 days) | 1.5 |
| EPIC-11 | BLG-FE-130 | S | 1.0 |
| EPIC-12 | BLG-OPS-120 | M (~2-3 days) | 2.5 |
| EPIC-13 | BLG-FE-129 | S | 1.0 |
| EPIC-14 | BLG-GOV-258 | S | 1.0 |
| EPIC-15 | BLG-QA-123 | S | 1.0 |

All 15 items carry an effort estimate from `release_plan.md`. No `[ESTIMATE REQUIRED]` placeholders.

## 1.3 Total Effort vs Capacity

```
Total estimated effort:  ~26.5 days midpoint
Confirmed capacity:      ~24-28 working-day-equivalent
Utilisation:             ~95-110% (denominator-dependent)
Outcome:                 pass (no over-allocation against the ~28-day ceiling; deliberately at the top of the band per explicit user "use the full capacity" instruction — see `release_plan.md ## Risk Register Summary` RISK-03)
```

No over-allocation against the confirmed ceiling. STEP 3 scope selection includes all 15 EPICs without a capacity-driven deferral. No capacity WARN was raised at release planning (`capacity_check: pass`), so no Phasing Recommendation exists and no capacity WARN acknowledgement is required at this step.

## 1.4 Gate-Conditional Deferred Items

None. Design Gate (`design_gate.md`, this cycle) cleared all 3 Design Required EPICs (EPIC-01, EPIC-02, EPIC-05) and all 12 Design Pre-Approved/Not Applicable EPICs — 15/15 cleared, 0 blocked. No items carry `status: deferred_at_planning` in `execution_state.json`.
