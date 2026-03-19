**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-18
**Cycle:** 2026-03-18__release-v2.1
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Sprint Capacity — v2.1 Alerts, Watchlists & Enhancements

## Capacity Inputs

```
Sprint duration:    ~40 hrs/sprint (solo dev, evenings — per workforce_capacity.md v2.0 assessment)
Available FTE:      1 (self-hosted, single developer)
Sprints planned:    3 (capacity WARN — acknowledged by Product Owner 2026-03-18)
Total capacity:     ~120 hrs across 3 sprints
Skill constraints:  None critical — all skills available (Head of Engineering = Backend;
                    Base44 Frontend = Frontend; Head of Specs Team = Specs;
                    Data Model owner and Financial Reporting owner are domain-specific
                    but not scarce in this context)
```

**Capacity WARN Acknowledgement (IMP-41):** The capacity check for this release returned `warn` — total scope mid-estimate (~129 hrs) requires 3 sprints at ~40 hrs/sprint (~120 hrs available). Product Owner has explicitly acknowledged the over-capacity risk (9 hrs mid shortfall at 3-sprint boundary) and accepted the phasing plan. Recorded here. `capacity_warn_acknowledged = true`.

**Sprint 3 stretch risk:** ST-10 (Watchlist frontend, ~10 hrs) may slip to Sprint 4 if Sprint 3 runs long. Product Owner accepts this risk. Sprint 3 core target is ~43 hrs (without ST-10); full Sprint 3 including ST-10 is ~53 hrs — HIGH WARN. ST-10 is flagged as stretch.

---

## Item Effort Mapping

| Item | Sprint | EPIC | Effort Low | Effort High | Effort Mid |
|------|--------|------|-----------|------------|-----------|
| ST-01 | 1 | EPIC-01 | 3 hrs | 6 hrs | 4 hrs |
| ST-11 | 1 | EPIC-04 | 5 hrs | 10 hrs | 7 hrs |
| ST-12 | 1 | EPIC-05 | 8 hrs | 12 hrs | 10 hrs |
| ST-16 | 1 | EPIC-06 | 6 hrs | 10 hrs | 8 hrs |
| ST-17 | 1 | EPIC-06 | 3 hrs | 5 hrs | 4 hrs |
| ST-18 | 1 | EPIC-06 | 3 hrs | 5 hrs | 4 hrs |
| ST-19 | 1 | EPIC-06 | 1 hr | 2 hrs | 2 hrs |
| **Sprint 1 total** | | | **29 hrs** | **50 hrs** | **39 hrs** |
| ST-02 | 2 | EPIC-02 | 6 hrs | 10 hrs | 8 hrs |
| ST-03 | 2 | EPIC-02 | 10 hrs | 18 hrs | 14 hrs |
| ST-13 | 2 | EPIC-05 | 3 hrs | 5 hrs | 4 hrs |
| ST-14 | 2 | EPIC-05 | 6 hrs | 10 hrs | 8 hrs |
| ST-15 | 2 | EPIC-05 | 2 hrs | 4 hrs | 3 hrs |
| **Sprint 2 total** | | | **27 hrs** | **47 hrs** | **37 hrs** |
| ST-04 | 3 | EPIC-02 | 8 hrs | 12 hrs | 10 hrs |
| ST-05 | 3 | EPIC-02 | 4 hrs | 8 hrs | 6 hrs |
| ST-06 | 3 | EPIC-02 | 4 hrs | 8 hrs | 6 hrs |
| ST-07 | 3 | EPIC-02 | 2 hrs | 4 hrs | 3 hrs |
| ST-08 | 3 | EPIC-03 | 4 hrs | 8 hrs | 6 hrs |
| ST-09 | 3 | EPIC-03 | 10 hrs | 16 hrs | 12 hrs |
| ST-10 (stretch) | 3/4 | EPIC-03 | 8 hrs | 14 hrs | 10 hrs |
| **Sprint 3 core (excl. ST-10)** | | | **32 hrs** | **56 hrs** | **43 hrs** |
| **Sprint 3 with ST-10** | | | **40 hrs** | **70 hrs** | **53 hrs** |
| **Release total (all 19 stories)** | | | **88 hrs** | **167 hrs** | **129 hrs** |

---

## Total Effort vs Capacity

| Metric | Sprint 1 | Sprint 2 | Sprint 3 core | Sprint 3 + ST-10 |
|--------|----------|----------|---------------|------------------|
| Estimated effort (mid) | 39 hrs | 37 hrs | 43 hrs | 53 hrs |
| Available capacity | ~40 hrs | ~40 hrs | ~40 hrs | ~40 hrs |
| Status | ✅ Within capacity | ✅ Within capacity | ⚠ WARN (+3 hrs) | ❌ HIGH WARN (+13 hrs) |

**Sprint 3 resolution:** ST-10 (Watchlist frontend) is carried as stretch. If Sprint 3 runs long, ST-10 defers to Sprint 4. Product Owner accepts. No release blocking — ST-09 (backend) is the delivery blocker, not ST-10 (UI layer).
