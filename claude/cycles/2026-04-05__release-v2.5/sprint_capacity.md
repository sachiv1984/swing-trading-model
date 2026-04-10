**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-06
**Cycle:** 2026-04-05__release-v2.5

---

# Sprint Capacity — v2.5 Integration Baseline, Quick Wins & Governance Debt

---

## 1.1 Capacity Inputs

```
Sprint duration:    2 sprints × ~3 effective days = ~6 effective days available
Available FTE:      1 (solo-dev, evening cadence)
Total capacity:     ~6–10 effective days (consistent with v2.4: ~8–12 days across 3 sprints / 6 EPICs)
Skill constraints:  All skills available via solo-dev + governance roles; no scarce skill conflicts identified
Workforce source:   workforce_capacity.md (v2.5 candidate pool assessment) + release_plan.md ## Capacity Check
```

## 1.2 Item Effort Mapping

| Sprint | EPIC | ST | Title | Effort Band | Estimated Days |
|--------|------|-----|-------|-------------|----------------|
| Sprint 1 | EPIC-01 | ST-01 | Fix auth forwarding in POST /test/endpoints | XS (<1h) | 0.1 |
| Sprint 1 | EPIC-01 | ST-02 | Sync endpoint test list with openapi.yaml | XS (<1h) | 0.1 |
| Sprint 1 | EPIC-01 | ST-03 | Fix System Status endpoint categorisation | XS (<1h) | 0.1 |
| Sprint 1 | EPIC-04 | ST-10 | Fix governance_sync.yml batch push closure | XS (<1h) | 0.1 |
| Sprint 1 | EPIC-04 | ST-11 | Formalise backlog entry placement standard | XS (<1h) | 0.1 |
| Sprint 1 | EPIC-04 | ST-12 | Apply v2.4 deferred governance prompt patches | S (~0.5d) | 0.5 |
| Sprint 1 | EPIC-04 | ST-13 | Create test scenarios for EPIC-01 correctness | S (~0.5d) | 0.5 |
| **Sprint 1 total** | | | | | **~1.5 days** |
| Sprint 2 | EPIC-02 | ST-04 | Review and document Reports page backend integration | M (~1–2d) | 1.5 |
| Sprint 2 | EPIC-02 | ST-05 | Review and document Signals page backend integration | M (~1–2d) | 1.5 |
| Sprint 2 | EPIC-02 | ST-06 | Investigate high external latency on DB-backed endpoints | M (~1–2d) | 1.5 |
| Sprint 2 | EPIC-03 | ST-07 | Add --max-time to GitHub Actions curl calls | XS (<1h) | 0.1 |
| Sprint 2 | EPIC-03 | ST-08 | Fix Avg Slippage StatsCard gradient rendering | XS (<1h) | 0.1 |
| Sprint 2 | EPIC-03 | ST-09 | Fee drag metric on Trade History | S (~0.5–1d) | 0.75 |
| **Sprint 2 total** | | | | | **~5.5 days** |

**Total estimated effort:** ~7.0 days (mid-point)
**Total estimated range:** ~6.5–10.5 days (from release_plan.md ## Capacity Check)

## 1.3 Total Effort vs Capacity

| Metric | Value |
|--------|-------|
| Total confirmed capacity (2 sprints) | ~6–10 effective days |
| Total estimated effort | ~7.0 days (mid-point) |
| Utilisation | ~87% (mid-point estimate) |
| Over-allocation | No |
| Capacity check outcome | **PASS** (from release_plan.md) |

No over-allocation detected. Sprint 1 is lightweight (~1.5 days), predominantly XS items. Sprint 2 carries the majority of effort (~5.5 days) with the 3×M investigation stories in EPIC-02.

**Skill distribution:**
- Backend engineering: ST-01, ST-02, ST-06 (+ ST-09 backend)
- Frontend: ST-03, ST-08, ST-09 (frontend)
- CI/DevOps: ST-07, ST-10
- Governance/spec: ST-11, ST-12, ST-13
- Review/documentation: ST-04, ST-05

No scarce skill conflicts. All skills available from solo-dev + role governance.
