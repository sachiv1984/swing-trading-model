**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-15
**Cycle:** 2026-03-15__release-v1.10

---

# Sprint Capacity — 2026-03-15__release-v1.10

## Capacity Inputs

**Source:** `release_plan.md ## Capacity Check`; `claude/roadmap/workforce_capacity.md`

```
Sprint duration:    Not specified (--capacity not passed at invocation)
Available FTE:      Solo developer
Intensity model:    Full-time: ~35–40 hrs/week; Evenings/weekends: ~15–20 hrs/week
Total capacity:     Full-time sprint (1.5 wks): ~52–60 hrs
                    Evenings sprint (3 wks): ~45–60 hrs
Skill constraints:  Infrastructure provisioning (EPIC-01) requires DevOps / cloud or same-host
                    skills. Frontend JS refactoring (EPIC-02). Backend FastAPI + CI (EPIC-03).
                    No scarce skill conflicts identified — solo developer has all required skills.
```

**Capacity check outcome: WARN** — No capacity parameter specified. Estimates are feasible under full-time assumption. Could stretch under evenings-only mode. Product Owner acknowledgement required before scope seals.

---

## Item Effort Mapping

**Source:** `release_plan.md ## Capacity Check`; `stage4_backlog_slice.md`

| ST-ID | EPIC | Title | Effort Lo | Effort Hi | Effort Mid |
|-------|------|-------|-----------|-----------|------------|
| ST-01 | EPIC-01 | Provision staging environment infrastructure | 1 day (8 hrs) | 2 days (16 hrs) | 1.5 days (12 hrs) |
| ST-02 | EPIC-01 | Configure CI/CD auto-deploy to staging | 0.5 days (4 hrs) | 1 day (8 hrs) | 0.75 days (6 hrs) |
| ST-03 | EPIC-01 | Update QA sign-off governance process | 0.25 days (2 hrs) | 0.25 days (2 hrs) | 0.25 days (2 hrs) |
| ST-04 | EPIC-02 | Refactor CohortAnalysis.js to use backend endpoint | 0.5 days (4 hrs) | 1 day (8 hrs) | 0.75 days (6 hrs) |
| ST-05 | EPIC-03 | FastAPI TestClient integration tests for portfolio endpoints | 1 day (8 hrs) | 2 days (16 hrs) | 1.5 days (12 hrs) |
| ST-06 | EPIC-03 | Add integration test CI step | 0.5 days (4 hrs) | 0.5 days (4 hrs) | 0.5 days (4 hrs) |
| ST-07 | EPIC-03 | Author v1.7 missing QA test scenarios (BLG-QA-01) | 0.5 days (4 hrs) | 1 day (8 hrs) | 0.75 days (6 hrs) |

**EPIC totals:**
- EPIC-01: 2.5 days mid (20 hrs)
- EPIC-02: 0.75 days mid (6 hrs)
- EPIC-03: 2.75 days mid (22 hrs)

---

## Total Effort vs Capacity

| Metric | Lo estimate | Mid estimate | Hi estimate |
|--------|-------------|--------------|-------------|
| Total effort | 4.25 days (34 hrs) | 6.0 days (48 hrs) | 9.25 days (74 hrs) |
| Capacity (full-time, 1.5 wks) | — | 52–60 hrs | — |
| Capacity (evenings, 3 wks) | — | 45–60 hrs | — |

**Assessment:**
- At full-time (1.5-week sprint): mid estimate 48 hrs fits within ~52–60 hrs available. **PASS** at mid, headroom at low. Hi estimate (74 hrs) would over-run — risk if stories encounter complexity.
- At evenings-only (3-week sprint): mid estimate 48 hrs fits within ~45–60 hrs. Borderline — low headroom if stories run long.
- **Overall: WARN** — feasible at full-time; constrained at evenings. Product Owner must acknowledge before sprint seals.

### Phasing Option (if needed)

Per `release_plan.md ## Capacity Check` phasing recommendation:

| Phase | EPICs | Stories | Mid Effort |
|-------|-------|---------|------------|
| Sprint 1 (if phased) | EPIC-01 | ST-01, ST-02, ST-03 | 20 hrs |
| Sprint 2 (if phased) | EPIC-02 + EPIC-03 | ST-04, ST-05, ST-06, ST-07 | 28 hrs |

EPIC-01 (BLG-OPS-01) is the P1 LL-01 prerequisite and must ship in Sprint 1 if phasing is adopted. This is non-negotiable per `cycle_summary.md` Key Planning Decision #1.
