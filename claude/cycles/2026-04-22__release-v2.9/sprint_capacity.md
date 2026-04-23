Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-04-23
Cycle: 2026-04-22__release-v2.9

---

# Sprint Capacity — v2.9

## Capacity Inputs

Derived from `release_plan.md ## Capacity Check` (schema v2) and `workforce_capacity.md`.

> Note: `stage4_5_capacity_check.md` is not produced for schema v2 cycles — capacity data is embedded in `release_plan.md ## Capacity Check`. This is compliant with sprint_planning_prompt.md v2.5 §5 (schema v2 source rule).

```
Sprint duration:    2 sprints (variable working days — no fixed timebox specified)
Available FTE:      Engine (all roles embodied); velocity-based capacity model
Velocity basis:     v2.8 = 1.00; 6-cycle rolling avg = 0.99
Skill constraints:  Strategy Rules & System Intent Owner required for ST-08 (§13 review);
                    Head of Specs Team for ST-01–03, ST-11–12; Backend for ST-05, ST-06, ST-14
```

## Item Effort Mapping

| Story | EPIC | Sprint | Effort | Delegation |
|-------|------|--------|--------|------------|
| ST-01 BLG-SPEC-21 | EPIC-01 | 1 | S (~0.5 day) | autonomous |
| ST-02 BLG-SPEC-22 | EPIC-01 | 1 | S (~1 day) | autonomous |
| ST-03 BLG-SPEC-23 | EPIC-01 | 1 | S (~0.5 day) | autonomous |
| ST-04 BLG-FE-17 | EPIC-01 | 1 | M (~2 days) | autonomous |
| ST-05 DS-03 | EPIC-02 | 2 | S (~1 day) | autonomous |
| ST-06 DS-05 | EPIC-02 | 2 | M (~2 days) | autonomous |
| ST-07 DS-06 | EPIC-02 | 2 | S (~1 day) | autonomous |
| ST-08 BLG-GOV-16 | EPIC-03 | 1 | S (~0.5 day) | autonomous |
| ST-09 BLG-QA-08 | EPIC-03 | 1 | M (~2 days) | autonomous |
| ST-10 BLG-QA-09 | EPIC-03 | 1 | M (~2 days) | autonomous |
| ST-11 BLG-GOV-14 | EPIC-04 | 1 | S (~0.5 day) | autonomous |
| ST-12 BLG-GOV-15 | EPIC-04 | 1 | S (~0.5 day) | autonomous |
| ST-13 BLG-FE-15 | EPIC-04 | 1 | S (~0.5 day) | autonomous |
| ST-14 BLG-AI-01 | EPIC-04 | 2 | S (~1 day) | autonomous |
| ST-15 TEST-GAP-EPIC-04 | EPIC-04 | 2 | S (~0.5 day) | autonomous |

## Total Effort vs Capacity

| Sprint | Stories | S items | M items | Est. effort |
|--------|---------|---------|---------|-------------|
| Sprint 1 | 10 | 7 | 3 | ~9.75 days |
| Sprint 2 | 5 | 4 | 1 | ~4.5 days |
| **Total** | **15** | **11** | **4** | **~14.25 days** |

**Capacity check outcome:** PASS — within demonstrated delivery range (v2.6: 15 stories @ 1.00, v2.3: 15 stories @ 0.94). No over-allocation.

**Utilisation:** ~100% of velocity baseline (14.25 days vs 14.25 days estimated at 0.99 rolling avg).

**Workforce economics:** No scarce skill conflicts. Strategy Rules owner required for ST-08 (one session). All other items are standard spec, backend, and governance work. No pull-forward or kill required.
