**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-30
**Cycle:** 2026-05-30__release-v4.6

---

# Sprint Capacity — 2026-05-30__release-v4.6

---

## 1. Capacity Inputs

Source: `claude/roadmap/workforce_capacity.md` (2026-05-27 revision) + release plan capacity check.

```
Sprint duration:    Double (~24–28 working days per sprint; 2× solo-dev baseline)
Available FTE:      1 solo developer (evenings/weekends), doubled throughput
Total capacity:     ~24–28 capacity units per sprint (~48–56 across both sprints)
Skill constraints:  None identified — all stories are within solo-dev skill profile
Warn threshold:     Effort > 14 days per sprint
Capacity verdict:   PASS — well within doubled capacity
```

---

## 2. Item Effort Mapping

### Sprint 1

| EPIC | ST | Title | Effort Band | Effort Est. | Delegation class |
|------|-----|-------|-------------|-------------|-----------------|
| EPIC-04 | ST-14 | System_status_report stale status correction | XS | ~15 min | autonomous |
| EPIC-04 | ST-15 | release_planning_prompt gate scan + data density checkpoint | S | ~2–3 hrs | autonomous |
| EPIC-04 | ST-16 | Closed trade count audit (PT-04 + SI-02 data density gate) | XS | ~30 min | delegated_decision |
| EPIC-04 | ST-17 | Arc 4 data density risk trajectory assessment | S | ~2–3 hrs | delegated_decision |
| EPIC-04 | ST-18 | Arc 6 Monte Carlo §13 pre-assessment | S | ~2–3 hrs | delegated_decision |
| EPIC-04 | ST-19 | Trade plan schema field count gate check | S | ~1–2 hrs | delegated_decision |
| EPIC-04 | ST-20 | Sprint close automation failure investigation | S | ~1–2 hrs | autonomous |
| EPIC-04 | ST-21 | External API integration spec template | S | ~2–3 hrs | autonomous |
| EPIC-04 | ST-22 | roadmap_prompt.md advisory — set next_release after DL decision | XS | ~1 hr | autonomous |
| **EPIC-04 total** | | | | **~1.5–2 days** | |
| EPIC-01 | ST-01 | DS-07 data migration: add SI-02 columns to trade_plans | M | ~3–4 hrs | autonomous |
| EPIC-01 | ST-02 | POST /trade-plans: capture 5 new SI-02 fields | M | ~3–4 hrs | autonomous |
| EPIC-01 | ST-03 | SI-02 behavioural drift detection service (4 metrics) | H | ~1–1.5 days | autonomous |
| EPIC-01 | ST-04 | GET /analytics/behavioural-drift endpoint, openapi.yaml, API contract | M | ~3–4 hrs | autonomous |
| EPIC-01 | ST-05 | SI-02 unit test suite | M | ~4 hrs | autonomous |
| **EPIC-01 total** | | | | **~1.5–2 days** | |
| **Sprint 1 total** | | | | **~3–4 days** | |

**Sprint 1 utilisation:** ~12–15% of 24–28 day capacity → well within.

### Sprint 2 (Firm)

| EPIC | ST | Title | Effort Band | Effort Est. | Delegation class |
|------|-----|-------|-------------|-------------|-----------------|
| EPIC-03 | ST-09 | BLG-BE-16: red_flag_events severity field | M | ~3–4 hrs | autonomous |
| EPIC-03 | ST-10 | BLG-OPS-40: Arc 5 hosting cost projection assessment | S | ~1–2 hrs | delegated_decision |
| EPIC-03 | ST-11 | BLG-FE-42: Arc 5 nav cohesion review | M | ~3–4 hrs | delegated_decision |
| EPIC-03 | ST-12 | BLG-FE-47: Red Flag Journal design review scope document | S | ~1 hr | autonomous |
| **EPIC-03 firm total** | | | | **~0.75–1 day** | |
| **Sprint 2 firm total** | | | | **~0.75–1 day** | |

**Sprint 2 firm utilisation:** ~3–4% of 24–28 day capacity → well within.

---

## 3. Total Effort vs Capacity

| Sprint | Estimated effort (firm) | Capacity | Utilisation |
|--------|------------------------|----------|-------------|
| Sprint 1 | ~3–4 days | ~24–28 days | ~12–15% |
| Sprint 2 (firm) | ~0.75–1 day | ~24–28 days | ~3–4% |
| **Total (firm)** | **~3.75–5 days** | **~48–56 days** | **~7–10%** |

No over-allocation. Scope is constrained by available actionable items, not capacity.

---

## 4. Conditional (Deferred at Planning)

The following items are in the authoritative backlog slice but deferred at planning pending gate confirmation. They are **not** part of the sealed sprint backlog.

| EPIC | ST | Title | Effort | Gate Condition |
|------|----|-------|--------|---------------|
| EPIC-02 | ST-06 | BehaviouralDriftPanel component | H (~4–6 hrs) | ST-16 audit (Sprint 1) confirms ≥20 closed trades with linked trade_plans; Product Owner confirms EPIC-02 gate met before Sprint 2 planning seals |
| EPIC-02 | ST-07 | BehaviouralDriftPanel integration into PerformanceAnalytics | S (~2 hrs) | Same as ST-06 |
| EPIC-02 | ST-08 | SI-02 Playwright test coverage | S (~2–3 hrs) | Same as ST-06 |
| EPIC-03 | ST-13 | BLG-GOV-67: SI-05 Phase 1 implementation | M (~1.5–2 days) | SI-01 + SI-03 live ≥30 days (gate clears 2026-06-21); Product Owner must confirm gate met before Sprint 2 planning seals with ST-13 |

**Conditional sprint 2 effort (if all gates met):** +~1.5–2 days (EPIC-02) + ~1.5–2 days (ST-13) = +~3–4 days additional. Total Sprint 2 with all conditionals: ~3.75–5 days — still well within 24–28 day capacity.

> **Gate re-invocation:** If a gate condition above is met during the sprint, do not add deferred items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-05-30__release-v4.6 --reason "<gate met>"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.
