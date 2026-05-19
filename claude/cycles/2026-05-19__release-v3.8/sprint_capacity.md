**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-19
**Cycle:** 2026-05-19__release-v3.8

---

# Sprint Capacity — v3.8

---

## 1.1 Capacity Inputs

```
Sprint duration:    ~10 working days (2 sprints × ~5 working days each)
Available FTE:      1.0 (solo developer — autonomous + delegated delivery)
Total capacity:     ~10 capacity units (1 unit = 1 working day)
Skill constraints:  delegated_decision item (ST-01 §13 review) requires Strategy Rules &
                    System Intent Owner; must complete in Sprint 1 before ST-02/ST-03 begin.
```

Source: `release_plan.md §Capacity Check` + `claude/roadmap/workforce_capacity.md`

---

## 1.2 Item Effort Mapping

| EPIC | ST Item | Effort | Delegation Class | Sprint |
|------|---------|--------|-----------------|--------|
| EPIC-04 | ST-09 Ticker Universe Management Page | M (~1–2 days) | delegated_frontend | 1 |
| EPIC-04 | ST-10 Governance Debt Clearance | XS (<0.5 day) | autonomous | 1 |
| EPIC-03 | ST-06 Setup Type Classification Field | S (~0.5 days) | delegated_frontend | 1 |
| EPIC-03 | ST-07 News Context Panel | S (~0.5 days) | delegated_frontend | 1 |
| EPIC-03 | ST-08 AI-Assisted Thesis Generation | M (~1–2 days) | delegated_frontend | 1 |
| EPIC-01 | ST-01 §13 Review Gate | XS (~0.5 days) | delegated_decision | 1 |
| EPIC-01 | ST-02 SI-01 Backend Validation Service | M (~1–2 days) | autonomous | 2 |
| EPIC-01 | ST-03 SI-01 Frontend Validation Panel | M (~1–2 days) | delegated_frontend | 2 |

**EPIC-02 REMOVED:** ST-04 and ST-05 (PT-04 Setup Quality Score) removed from sprint scope. Product Owner decision 2026-05-19: gate not met (< 20 closed trades). PT-04 formally parked in backlog.

---

## 1.3 Total Effort vs Capacity

### Sprint 1

| EPIC | Stories | Effort Low | Effort High |
|------|---------|-----------|-------------|
| EPIC-04 | ST-09, ST-10 | 1.0d | 2.5d |
| EPIC-03 | ST-06, ST-07, ST-08 | 1.5d | 3.0d |
| EPIC-01 | ST-01 | 0.5d | 0.5d |
| **Sprint 1 Total** | **6 stories** | **3.0d** | **6.0d** |

### Sprint 2

| EPIC | Stories | Effort Low | Effort High |
|------|---------|-----------|-------------|
| EPIC-01 | ST-02, ST-03 | 2.0d | 4.0d |
| **Sprint 2 Total** | **2 stories** | **2.0d** | **4.0d** |

### Overall

| Metric | Low | Mid | High |
|--------|-----|-----|------|
| Total effort (8 stories) | 5.0d | ~8.0d | 10.0d |
| Available capacity | — | 10d | — |
| Utilisation | — | ~80% | — |
| Over-allocation | **No** | — | — |

**Capacity check: WITHIN RANGE.** The release planning WARN was triggered by PT-04 inclusion (mid ~12d). With EPIC-02 removed, effective scope mid-point is ~8 days — within comfortable range for a 2-sprint solo-developer cycle at 0.97 velocity. Capacity WARN acknowledged by Product Owner virtue of PT-04 parking decision (2026-05-19).

---

## 1.4 Skill Constraints

| Constraint | Scope | Mitigation |
|-----------|-------|-----------|
| §13 review (ST-01) requires Strategy Rules & System Intent Owner | Sprint 1 gate story | delegated_decision; ST-02/ST-03 blocked until ST-01 done |
| delegated_frontend items (ST-09, ST-06, ST-07, ST-08, ST-03) require Base44 Frontend coordination | Across both sprints | EPIC merge order ensures sequential delivery; ST-08 implements template-engine only (no external API) |
