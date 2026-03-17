**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-17
**Cycle:** 2026-03-17__release-v2.0

---

# Sprint Capacity — v2.0 Reporting & Alerts

---

## Capacity Inputs

```
Sprint duration:    ~2 weeks (standard)
Available FTE:      1 (solo dev, evenings)
Total capacity:     ~40 hrs
Skill constraints:  Full-stack dev; no scarce skill conflicts. EPIC-06 parallel track
                    does not compete with product sprint capacity.
```

Source: `workforce_capacity.md` v2.0 section + `release_plan.md ## Capacity Check`

---

## Capacity WARN — Resolution

The release planning capacity check returned `WARN` when EPIC-03 (3.5 Alerts, ~30 hrs mid) was treated as conditional scope. EPIC-03 has since been deferred to v2.1 (per `qa_notification_planning.md`). ST-03 and ST-11 are pre-completed pre-sprint.

**Effective remaining sprint effort:**

| Story | EPIC | Type | Low hrs | High hrs | Mid hrs |
|-------|------|------|---------|---------|---------|
| ST-01 | EPIC-01 | Spec (design gate pre-work complete) | 0.5 | 1.5 | 1 |
| ST-02 | EPIC-01 | Frontend | 2 | 3 | 2.5 |
| ST-04 | EPIC-02 | Backend | 4 | 8 | 6 |
| ST-05 | EPIC-02 | Frontend | 3 | 5 | 4 |
| ST-12 | EPIC-04 | Backend bug fix (P1) | 2 | 4 | 3 |
| ST-14 | EPIC-05 | Ops documentation | 0.5 | 1 | 0.75 |
| ST-15 | EPIC-05 | Data documentation | 0.5 | 1 | 0.75 |
| ST-16 | EPIC-05 | Engineering governance doc | 0.5 | 1 | 0.75 |
| ST-17 | EPIC-05 | Spec audit | 8 | 16 | 12 |
| **Core subtotal** | | | **21** | **40.5** | **30.75** |
| ST-13 | EPIC-04 | Backend + Spec (stretch P3) | 4 | 8 | 6 |
| ST-20 | EPIC-05 | QA scenario (stretch P3) | 1 | 2 | 1.5 |
| **Core + stretch total** | | | **26** | **50.5** | **38.25** |

*EPIC-06 (ST-18, ST-19) runs as a parallel track — not counted against sprint capacity.*

---

## Capacity Assessment

| Metric | Value |
|--------|-------|
| Confirmed capacity | ~40 hrs |
| Core effort (mid) | ~31 hrs |
| Core + stretch effort (mid) | ~38 hrs |
| Over-allocation | No — core within capacity; stretch borderline feasible |
| Original WARN resolved? | ✅ Yes — EPIC-03 deferred; WARN no longer applies |

**Conclusion:** Single sprint is feasible. Core scope (~31 hrs mid) is comfortably within capacity. Stretch (ST-13, ST-20) adds ~7 hrs and is achievable if execution is efficient, but may slip to a follow-on patch if pace requires. Product Owner has explicitly acknowledged the capacity WARN from release planning and confirms it is resolved by EPIC-03 deferral.

---

## Capacity WARN Acknowledgement

Product Owner acknowledgement: confirmed — original WARN raised with EPIC-03 in scope (~72 hrs mid); EPIC-03 now deferred; effective sprint scope ~31 hrs mid core. Sprint capacity is adequate.
Date: 2026-03-17
