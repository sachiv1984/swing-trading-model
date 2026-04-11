**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-11
**Cycle:** 2026-04-11__release-v2.6

# Sprint Capacity — 2026-04-11__release-v2.6

---

## Capacity Inputs

```
Sprint structure:    2 sprints
Developer model:     Solo developer with AI engine assistance
Velocity baseline:   1.00 (v2.4: 1.00, v2.5: 1.00 — two consecutive cycles)
Available capacity:  ~100–120h total across 2 sprints (engine-assisted)
  Sprint 1:          ~60–70h
  Sprint 2:          ~40–50h
Skill constraints:   None — all required skills available (Backend, Frontend, QA, Governance)
```

---

## Item Effort Mapping

Source: `release_plan.md ## Capacity Check`

| EPIC | Stories | Effort Low | Effort High | Effort Mid |
|------|---------|-----------|------------|-----------|
| EPIC-01 | ST-01, ST-02, ST-03 | 32h | 56h | 44h |
| EPIC-02 | ST-04, ST-05, ST-06, ST-07 | 15h | 27h | 21h |
| EPIC-03 | ST-08, ST-09, ST-10, ST-11 | 13h | 20h | 17h |
| EPIC-04 | ST-12, ST-13, ST-14, ST-15 | 12h | 20h | 16h |
| **Total** | **15** | **72h** | **123h** | **98h** |

### Per-Sprint Breakdown

| Sprint | EPICs | Effort Mid | Capacity Mid | Notes |
|--------|-------|-----------|-------------|-------|
| Sprint 1 | EPIC-01, EPIC-02 | 65h | ~65h | P1 backend migration and CI infra |
| Sprint 2 | EPIC-03, EPIC-04 | 33h | ~45h | UX polish and governance patches |

---

## Capacity Assessment

| Metric | Value |
|--------|-------|
| Total confirmed capacity (mid) | ~110h |
| Total estimated effort (mid) | 98h |
| Utilisation | ~89% |
| Over-allocation | No |
| High-end risk | 123h vs ~110h — +13h (acceptable given AI velocity and 1.00 track record) |

**Verdict:** PASS. Mid-point total (98h) is comfortably within the 2-sprint capacity envelope. High-end scenario is marginally above but acceptable given demonstrated velocity = 1.00 across two prior consecutive cycles.
