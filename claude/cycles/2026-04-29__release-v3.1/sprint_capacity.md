**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-29
**Cycle:** 2026-04-29__release-v3.1

---

# Sprint Capacity — v3.1

## Capacity Inputs

```
Sprint duration:    2-sprint cycle, solo dev, evenings/weekends
Available FTE:      1 (solo developer — all roles collapsed)
Capacity per sprint: ~5 days (mid-point estimate)
Total capacity:     ~10 days (2-sprint cycle mid-point)
Skill constraints:  None — all roles owned by single developer
```

**Source:** `release_plan.md ## Capacity Check` + `workforce_capacity.md`

---

## Item Effort Mapping

### Sprint 1

| Story | Title | Effort Band | Days (mid) |
|-------|-------|-------------|------------|
| ST-06 | Fix screener UK ticker display and watchlist promotion | S | 0.5 |
| ST-07 | Earnings Calendar backend + OpenAPI (DS-04) | M | 2.0 |
| ST-01 | Trade Plan spec authoring: data model schema + API contract | S | 0.75 |
| ST-09 | Screener accuracy test protocol (BLG-QA-11) | S | 0.75 |
| ST-02 | Trade Plan backend: migration, CRUD endpoints, test registration | M | 2.5 |
| ST-11 | Monthly P&L summary report (BLG-FEAT-19) | S | 0.75 |
| ST-12 | External API security policy docs & dependency risk register | S | 0.75 |
| ST-13 | execution_prompt.md §3.1.A reclassification backfill (CF-01) | S | 0.5 |
| ST-14 | execution_prompt.md STEP 8.5 output target fix (CF-02) | S | 0.5 |
| **Sprint 1 Total** | | | **~9.0 days** |

### Sprint 2

| Story | Title | Effort Band | Days (mid) |
|-------|-------|-------------|------------|
| ST-04 | Pre-Trade Research View API contract spec | S | 0.75 |
| ST-03 | Trade Plan frontend: creation flow and detail view | M | 2.5 |
| ST-08 | Earnings Calendar frontend (DS-04) | M | 2.0 |
| ST-05 | Pre-Trade Research View backend: aggregation endpoint | M | 2.5 |
| ST-10 | Screener scenario library (BLG-QA-10) | M | 2.0 |
| **Sprint 2 Total** | | | **~9.75 days** |

---

## Total Effort vs Capacity

| Metric | Sprint 1 | Sprint 2 | Total |
|--------|----------|----------|-------|
| Confirmed capacity | ~5 days | ~5 days | ~10 days |
| Estimated effort | ~9.0 days | ~9.75 days | ~18.75 days |
| Utilisation | ~180% | ~195% | ~188% |
| **Over-allocation** | **+4.0 days** | **+4.75 days** | **+8.75 days** |

**Outcome: WARN (carried from release planning)**

Over-allocation accepted by Product Owner (per release plan capacity_feasible = "warn"; sprint planning initiated with full knowledge of over-allocation. Phasing from release plan followed exactly. Solo dev historically delivers more than conservative capacity estimate suggests — spec authoring overhead estimates tend to compress during execution.).

**Capacity WARN Acknowledgement:** Product Owner acknowledged at sprint planning initiation (2026-04-29). Recorded per IMP-41.

---

## Skill Constraints

No scarce skill conflicts — single-developer model means all skill domains are available on demand. Sequential delivery within each sprint avoids domain-switching overhead.
