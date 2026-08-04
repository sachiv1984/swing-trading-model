Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-04
Cycle: 2026-08-04__release-v8.2

# Sprint Capacity — 2026-08-04__release-v8.2

## Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (autonomous execution engine) — per workforce_capacity.md baseline (Effective 2026-07-17)
Available FTE:      1 (solo developer / autonomous execution engine)
Total capacity:     ~24-28 working-day-equivalent units (per sprint)
Skill constraints:  None scarce this cycle — 5 EPICs span 12 distinct owner roles, no concurrent scarce-skill collision identified (unchanged from release_plan.md STEP 4.5 finding)
```

## Item Effort Mapping

| EPIC | Item | Effort Band | Midpoint (days) | Estimate source |
|------|------|-------------|------------------|------------------|
| EPIC-01 | ST-01 (BLG-FEAT-88) | M | 2.5 | release_plan.md §Capacity Check |
| EPIC-01 | ST-02 (BLG-FE-105) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-01 | ST-03 (BLG-FE-67) | XS | 0.5 | release_plan.md §Capacity Check |
| EPIC-01 | ST-04 (BLG-FE-138) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-01 | ST-05 (BLG-FEAT-86) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-02 | ST-06 (BLG-SEC-27) | S | 0.5 | release_plan.md §Capacity Check |
| EPIC-02 | ST-07 (BLG-OPS-128) | S | 0.75 | release_plan.md §Capacity Check |
| EPIC-03 | ST-08 (BLG-GOV-160) | XS | 0.1 | release_plan.md §Capacity Check |
| EPIC-03 | ST-09 (BLG-GOV-213) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-03 | ST-10 (BLG-GOV-214) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-03 | ST-11 (BLG-GOV-218) | S | 0.5 | release_plan.md §Capacity Check |
| EPIC-03 | ST-12 (BLG-GOV-265) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-03 | ST-13 (BLG-GOV-269) | M | 2.5 | release_plan.md §Capacity Check |
| EPIC-03 | ST-14 (BLG-GOV-278) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-03 | ST-15 (BLG-GOV-279) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-03 | ST-16 (BLG-GOV-281) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-03 | ST-17 (BLG-GOV-283) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-03 | ST-18 (BLG-GOV-285) | S | 0.75 | release_plan.md §Capacity Check |
| EPIC-04 | ST-19 (BLG-OPS-116) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-04 | ST-20 (BLG-OPS-118) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-04 | ST-21 (BLG-OPS-125) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-05 | ST-22 (BLG-QA-126) | S | 1.0 | release_plan.md §Capacity Check |
| EPIC-05 | ST-23 (BLG-SPEC-110) | M | 1.5 | release_plan.md §Capacity Check |
| EPIC-05 | ST-24 (BLG-BE-81) | XS | 0.1 | release_plan.md §Capacity Check |
| EPIC-05 | ST-25 (BLG-FE-131) | S | 1.0 | release_plan.md §Capacity Check |

All 25 items carry an effort estimate (inherited from `release_plan.md ## Execution Plan`/`## Capacity Check`, schema v2). No `[ESTIMATE REQUIRED]` placeholders.

## Total Effort vs Capacity

```
Total estimated effort:  ~24.7 days midpoint
Confirmed capacity:      ~24-28 working-day-equivalent
Utilisation:              ~88-103% (depending on which end of the band is used as denominator)
Outcome:                  pass — confirmed at release planning STEP 4.5 (release_plan.md), re-confirmed here; no over-allocation against the ceiling; sits at top of band per explicit user "full sprint capacity" instruction carried from release planning
```

No over-allocation. No Product Owner acknowledgement of over-capacity risk required under §8 (capacity check outcome is `pass`, not `warn`). No `### Phasing Recommendation` exists in `release_plan.md` (only required on `warn` outcome) — nothing to adopt or decline here.

## Minimum Capacity Buffer Floor (§1.5, advisory — first cycle this recommendation is in force)

`scope_effort ÷ confirmed_capacity`, evaluated across the confirmed band:
- Against the top of band (28 days — the actual target per the user's "full sprint capacity" instruction): 24.7 / 28 ≈ **0.88** — under the 95% floor.
- Against the midpoint (26 days): 24.7 / 26 ≈ **0.95** — at the floor.
- Against the bottom of band (24 days): 24.7 / 24 ≈ **1.03** — exceeds the floor.

**Buffer floor exceeded note:** at the conservative (low) end of the confirmed capacity band, the ratio exceeds the 95% advisory floor. This is distinct from — and less severe than — the hard over-100%-of-capacity WARN threshold in §8, which was not triggered (release planning's own capacity check landed `pass`). Surfaced to the Product Owner per §1.5.

**Product Owner acknowledgement:** Proceed at full scope — deliberately curated (not padded to the ceiling; ~100+ lower-value ungated P3 candidates remained available and were not pulled in), consistent with `release_plan.md` RISK-04's already-accepted rationale and the user's explicit "full sprint capacity" instruction this cycle. — Product Owner, 2026-08-04.

## Conditional (Deferred)

None. `release_plan.md` records `story_items_conditional: 0` — all 25 items in the backlog slice are firm, none are gate-conditionally deferred at planning.
