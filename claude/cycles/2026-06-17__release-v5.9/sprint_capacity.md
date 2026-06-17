Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-17
Cycle: 2026-06-17__release-v5.9

---

# Sprint Capacity — v5.9

## Capacity Inputs

```
Sprint duration:    1 sprint (~12–14 working days available per workforce_capacity.md 2026-05-27 baseline)
Available FTE:      1 (solo operator, autonomous engine)
Warn threshold:     Effort > 14 working days
Skill constraints:  None identified — all items are governance documentation, QA authoring, or frontend additive change
```

*Source: `claude/roadmap/workforce_capacity.md` (effective 2026-05-27 capacity revision), `release_plan.md ## Capacity Check`.*

## Item Effort Mapping

| EPIC | ST-ID | Source Item | Effort Band | Delegation Class |
|------|-------|-------------|-------------|-----------------|
| EPIC-01 | ST-01 | BLG-GOV-125 | XS (~1 hr) | autonomous |
| EPIC-01 | ST-02 | BLG-GOV-126 | XS (~1 hr) | autonomous |
| EPIC-01 | ST-03 | BLG-GOV-127 | XS (~1 hr) | autonomous |
| EPIC-01 | ST-04 | BLG-GOV-128 | XS (<1 hr) | autonomous |
| EPIC-01 | ST-05 | BLG-GOV-129 | XS (<30 min) | autonomous |
| EPIC-02 | ST-06 | BLG-QA-24 | S (~0.5 day) | autonomous |
| EPIC-02 | ST-07 | BLG-GOV-38 | S (~0.5–1 day) | autonomous |
| EPIC-02 | ST-08 | BLG-QA-34 | S (~0.5 day) | autonomous |
| EPIC-02 | ST-09 | BLG-GOV-53 | S (~0.5 day) | autonomous |
| EPIC-02 | ST-10 | BLG-QA-50 | S (~0.5 day) | autonomous |
| EPIC-02 | ST-11 | BLG-FE-57 | XS (~0.5 day) | autonomous |

## Total Effort vs Capacity

| EPIC | Estimated Effort |
|------|-----------------|
| EPIC-01 (5 × XS) | ~5 hours |
| EPIC-02 (5 × S + 1 × XS) | ~8–12 hours |
| **Total** | **~13–17 hours** |

**Capacity check outcome: PASS** — ~13–17 hours is well within the 12–14 working day sprint baseline. No over-allocation.
