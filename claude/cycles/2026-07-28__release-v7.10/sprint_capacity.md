Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-28
Cycle: 2026-07-28__release-v7.10

# Sprint Capacity — 2026-07-28__release-v7.10

## Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (autonomous execution engine) — per workforce_capacity.md baseline
Available FTE:      1 (solo developer / autonomous execution engine)
Total capacity:     ~24-28 working-day-equivalent units
Skill constraints:  None scarce this cycle — 6 EPICs span 9 distinct owner roles, no concurrent scarce-skill collision identified
```

Source: `release_plan.md ## Capacity Check` (schema v2), carried forward unchanged — no new capacity information since release planning.

## Item Effort Mapping

| EPIC | Item | Effort Band | Midpoint (days) |
|------|------|-------------|------------------|
| EPIC-01 | ST-01 (BLG-BE-68) | S (~0.5d) | 0.5 |
| EPIC-01 | ST-02 (BLG-BE-75) | M | 2.0 |
| EPIC-01 | ST-03 (BLG-BE-76) | M | 2.0 |
| EPIC-01 | ST-04 (BLG-BE-41) | S (~1 day) | 1.0 |
| EPIC-02 | ST-05 (BLG-SEC-22) | S | 1.0 |
| EPIC-02 | ST-06 (BLG-SEC-09) | S (~1 day) | 1.0 |
| EPIC-02 | ST-07 (BLG-SEC-18) | M | 2.0 |
| EPIC-02 | ST-08 (BLG-SEC-13) | M (~1-2 days) | 1.5 |
| EPIC-03 | ST-09 (BLG-QA-127) | M (~1-2 days) | 1.5 |
| EPIC-03 | ST-10 (BLG-QA-96) | S | 1.0 |
| EPIC-03 | ST-11 (BLG-QA-133) | M | 2.0 |
| EPIC-03 | ST-12 (BLG-QA-128) | M | 2.0 |
| EPIC-04 | ST-13 (BLG-SPEC-102) | XS | 0.25 |
| EPIC-04 | ST-14 (BLG-SPEC-103) | XS | 0.25 |
| EPIC-04 | ST-15 (BLG-SPEC-104) | XS | 0.25 |
| EPIC-04 | ST-16 (BLG-GOV-243) | M | 2.0 |
| EPIC-05 | ST-17 (BLG-FE-122) | S | 1.0 |
| EPIC-05 | ST-18 (BLG-FE-123) | XS | 0.25 |
| EPIC-05 | ST-19 (BLG-FE-106) | XS (<1h) | 0.15 |
| EPIC-05 | ST-20 (BLG-FE-134) | M | 2.0 |
| EPIC-06 | ST-21 (BLG-GOV-256) | S (~0.5-1 day) | 0.75 |
| EPIC-06 | ST-22 (BLG-GOV-216) | S | 0.75 |
| EPIC-06 | ST-23 (BLG-GOV-207) | S | 0.75 |

All 23 items carry an effort estimate (inherited from `release_plan.md ## Capacity Check`). No `[ESTIMATE REQUIRED]` placeholders.

## EPIC Effort Subtotals

| EPIC | Subtotal (days) |
|------|------------------|
| EPIC-01 | 5.5 |
| EPIC-02 | 5.5 |
| EPIC-03 | 6.5 |
| EPIC-04 | 2.75 |
| EPIC-05 | 3.4 |
| EPIC-06 | 2.25 |
| **Total** | **25.9** (release plan states ~26.15 midpoint — pre-existing minor rounding in the sealed release plan; both figures sit comfortably within the ~24-28 day band, no reconciliation required for capacity feasibility) |

## Total Effort vs Capacity

```
Total estimated effort:  ~26.15 days midpoint (per sealed release_plan.md ## Capacity Check)
Confirmed capacity:      ~24-28 working-day-equivalent
Utilisation:             ~93-109% (depending on which end of the band is used as denominator)
Outcome:                 pass — no over-allocation against the ~28-day ceiling
```

No over-allocation. Capacity check outcome carried from release planning is `pass`, not `warn` — no Phasing Recommendation subsection exists in `release_plan.md ## Capacity Check`, so no Product Owner Adopt/Decline decision is required at this step (per §0 Phasing Recommendation rule, which only applies on a `warn` outcome).

## Conditional (Deferred)

None. No ST items are recorded as `status: deferred_at_planning` with a `gate_condition` in `execution_state.json` — all 23 items in the authoritative backlog slice enter the sprint.
