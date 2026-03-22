**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-22
**Cycle:** 2026-03-21__release-v2.2

---

# Sprint Capacity — v2.2 Security, Alert Maturity & Quality

## Capacity Inputs

```
Sprint structure:    3 sprints (phased delivery per release_plan.md §Capacity Check)
Available FTE:       Solo developer — evenings/part-time
Estimated velocity:  ~3–4 days of work per week
Sprint cadence:      ~3–4 weeks per sprint
Total capacity:      ~9–12 days over the 3-sprint release cycle
Skill constraints:   All skills delivered by same individual; no multi-person
                     resourcing constraint, but governance items (EPIC-05) require
                     careful §6 checklist compliance — do not rush
```

Workforce capacity source: `claude/roadmap/workforce_capacity.md` — v2.1 capacity
released (12–16 days of multi-skill capacity); v2.2 scoped to ~16 days mid-point.

## Item Effort Mapping

| EPIC | Stories | Effort Estimate | Source |
|------|---------|----------------|--------|
| EPIC-01 | ST-01, ST-02 | ~1–1.5 days | release_plan.md §Capacity Check |
| EPIC-02 | ST-03, ST-04, ST-05 | ~5–7 days | release_plan.md §Capacity Check |
| EPIC-03 | ST-06, ST-07, ST-08 | ~0.5–1 day | release_plan.md §Capacity Check |
| EPIC-04 | ST-09, ST-10, ST-11, ST-12 | ~3.5–4 days | release_plan.md §Capacity Check |
| EPIC-05 | ST-13, ST-14, ST-15 | ~3–6 days | release_plan.md §Capacity Check |
| **Total** | **15 stories** | **~13–20 days (mid: ~16 days)** | |

## Total Effort vs Capacity

| Metric | Value |
|--------|-------|
| Total confirmed capacity (3 sprints) | ~9–12 days |
| Total estimated effort (mid-point) | ~16 days |
| Gap | ~4 days over mid-point capacity |
| Outcome | **WARN — over-capacity at mid-point; feasible with phased delivery** |

## Capacity WARN Acknowledgement

**Product Owner acknowledgement (STEP 0 — IMP-41):** Product Owner acknowledges the WARN outcome. The release is feasible with 3-sprint phased delivery per the phasing recommendation in `release_plan.md §Capacity Check`. If Phase 3 (EPIC-05 governance items) proves over-capacity at Sprint 3 planning, EPIC-05 items are the lowest-risk deferral — they affect future cycles only, not current product delivery.

`capacity_warn_acknowledged = true`

## Sprint Phasing

### Sprint 1 — Security + Quick Wins + Alert Design (~3–4 days)

| Item | Effort | Notes |
|------|--------|-------|
| EPIC-01: ST-01 API Key Auth | M (~1d) | P1 — highest priority |
| EPIC-01: ST-02 CSP Headers | XS (<1h) | Bundle with ST-01 |
| EPIC-03: ST-06 CSV Bug Fix | XS (<15min) | Bundle EPIC-03 as single PR |
| EPIC-03: ST-07 Slippage StatsCard | XS (<30min) | Bundle EPIC-03 |
| EPIC-03: ST-08 Health Check Endpoint | XS (<1h) | Bundle EPIC-03 |
| EPIC-02: ST-03 Alert Scheduling Design | S–M (~0.5–1d) | Product Owner decision task |
| Sprint 1 total | ~3–4 days | |

### Sprint 2 — Alert Maturity + QA Coverage (~6–8 days)

| Item | Effort | Notes |
|------|--------|-------|
| EPIC-02: ST-04 Alert Threshold Customisation | M (~2–3d) | Gated on ST-03 complete |
| EPIC-02: ST-05 Alert History Table | M (~2–3d) | Gated on ST-03 complete |
| EPIC-04: ST-09 Execute Notification Scenarios | S (~0.5d QA) | No dev dependency |
| EPIC-04: ST-10 Create Watchlist Scenarios | S–M (~1d) | No dev dependency |
| EPIC-04: ST-11 Test Automation Readiness | XS–S (~0.5d) | Before ST-12 |
| Sprint 2 total | ~6–8 days | |

### Sprint 3 — Governance + QA Traceability (~5–7 days)

| Item | Effort | Notes |
|------|--------|-------|
| EPIC-04: ST-12 Spec-to-Test Traceability Matrix | M (~1.5d) | After ST-11 |
| EPIC-05: ST-13 Provisional-Target Field | M (~1–2d) | §6 checklist required |
| EPIC-05: ST-14 scored_initiatives.md Handoff | M (~1–2d) | §6 checklist required |
| EPIC-05: ST-15 Carry-Forward Block | M (~1–2d) | §6 checklist required |
| Sprint 3 total | ~5–7 days | |

## Skill Constraints

No multi-person skill conflicts (solo developer context). Key constraints:
- EPIC-05 governance items require §6 edit checklist compliance for each of 3+ files per story — do not rush; allow adequate time for checklist verification.
- ST-04/ST-05 (EPIC-02) require backend + frontend coordination — both sides must be in the same EPIC-02 branch.
- ST-01 (EPIC-01) requires backend middleware + frontend env-var wiring in the same PR or back-to-back PRs within EPIC-01 branch.
