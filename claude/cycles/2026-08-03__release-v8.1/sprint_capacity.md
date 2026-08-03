Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-03
Cycle: 2026-08-03__release-v8.1

# Sprint Capacity — 2026-08-03__release-v8.1

## Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (autonomous execution engine) — per workforce_capacity.md baseline (Effective 2026-07-17)
Available FTE:      1 (solo developer / autonomous execution engine)
Total capacity:     ~24-28 working-day-equivalent units (per sprint)
Skill constraints:  None scarce this cycle — 7 EPICs span 11 distinct owner roles, no concurrent scarce-skill collision identified (unchanged from release_plan.md STEP 4.5 finding)
```

## Item Effort Mapping

| EPIC | Item | Effort Band | Midpoint (days) | Estimate source |
|------|------|-------------|------------------|------------------|
| EPIC-01 | ST-01 (BLG-FE-137) | XS | 0.5 | release_plan.md §Capacity Check |
| EPIC-02 | ST-02 (BLG-OPS-127) | S | 0.5 | release_plan.md §Capacity Check |
| EPIC-03 | ST-03 (BLG-GOV-280) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-03 | ST-04 (BLG-GOV-268) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-03 | ST-05 (BLG-GOV-254) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-03 | ST-06 (BLG-GOV-273) | M | 2.5 | release_plan.md §Capacity Check |
| EPIC-03 | ST-07 (BLG-GOV-246) | M | 2.0 | release_plan.md §Capacity Check |
| EPIC-03 | ST-08 (BLG-GOV-241) | M | 2.5 | release_plan.md §Capacity Check |
| EPIC-03 | ST-09 (BLG-GOV-240) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-04 | ST-10 (BLG-QA-115) | XS | 0.5 | release_plan.md §Capacity Check |
| EPIC-04 | ST-11 (BLG-QA-113) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-04 | ST-12 (BLG-QA-129) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-04 | ST-13 (BLG-QA-131) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-05 | ST-14 (BLG-SPEC-72) | S | 0.5 | release_plan.md §Capacity Check |
| EPIC-05 | ST-15 (BLG-SPEC-82) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-05 | ST-16 (BLG-SPEC-86) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-06 | ST-17 (BLG-BE-47) | M | 2.5 | release_plan.md §Capacity Check |
| EPIC-06 | ST-18 (BLG-BE-55) | S | 1.25 | release_plan.md §Capacity Check |
| EPIC-07 | ST-19 (BLG-GOV-284) | L (~3-5 days) | 4.0 | release_plan.md §Capacity Check |

All 19 items carry an effort estimate (inherited from `release_plan.md ## Execution Plan`/`## Capacity Check`, schema v2). No `[ESTIMATE REQUIRED]` placeholders.

## Total Effort vs Capacity

```
Total estimated effort:  ~25.75 days midpoint
Confirmed capacity:      ~24-28 working-day-equivalent
Utilisation:              ~92-107% (depending on which end of the band is used as denominator)
Outcome:                  pass — confirmed at release planning STEP 4.5 (release_plan.md), re-confirmed here; no over-allocation against the ceiling; sits at top of band per explicit user "full capacity" instruction carried from release planning
```

No over-allocation. No Product Owner acknowledgement of over-capacity risk required (capacity check outcome is `pass`, not `warn`). No `### Phasing Recommendation` exists in `release_plan.md` (only required on `warn` outcome) — nothing to adopt or decline here.

## Conditional (Deferred)

None. `release_plan.md` records `story_items_conditional: 0` — all 19 items in the backlog slice are firm, none are gate-conditionally deferred at planning.
