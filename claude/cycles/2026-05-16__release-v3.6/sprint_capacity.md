**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-16
**Cycle:** 2026-05-16__release-v3.6

---

# Sprint Capacity — 2026-05-16__release-v3.6

## Capacity Inputs

| Field | Value |
|-------|-------|
| Sprint duration | 2 sprints (~10 working days theoretical) |
| Available FTE | solo-dev (evening hours + occasional full days; ~1.5–2 hrs/day effective) |
| Total usable capacity | ~3–4 days (6–8 effective working sessions) |
| Skill constraints | All 7 active stories: autonomous (no delegated items in scope); openapi.yaml shared by EPIC-01 and EPIC-03 — EPIC-03 merges first |
| Capacity check outcome | WARN (standard mode; acknowledged by Product Owner at release planning: `capacity_warn_acknowledged = true` in state.json) |

Source: `claude/cycles/2026-05-16__release-v3.6/release_plan.md ## Capacity Check`

---

## Item Effort Mapping

| Sprint | EPIC | ST | Title | Effort |
|--------|------|----|-------|--------|
| 1 | EPIC-04 | ST-09 | execution_prompt.md §13 gate story pattern | XS (~0.25 day) |
| 1 | EPIC-04 | ST-10 | execution_prompt.md metadata + sprint_close patches | XS (~0.25 day) |
| 1 | EPIC-03 | ST-06 | SC-RV-18 and SC-RV-19 Playwright coverage | S (~0.5 day) |
| 1 | EPIC-03 | ST-07 | Research endpoint HTTP error code differentiation | S (~0.5 day) |
| 1 | EPIC-03 | ST-08 | Research page UX fix: regime lozenge + font | XS (~0.25 day) |
| 1 | EPIC-01 | ST-01 | Capture planned_entry_price at trade entry | S–M (~1 day) |
| 2 | EPIC-01 | ST-02 | Update PlanVsReality component for entry_delta_pct | XS–S (~0.5 day) |

**Sprint 1 total:** ~2.75–3 days
**Sprint 2 total:** ~0.5 day
**Grand total (active scope):** ~3.25–3.5 days

---

## Total Effort vs Capacity

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~3–4 days |
| Total estimated effort (in-scope, 7 stories) | ~3.25–3.5 days |
| Utilisation | ~85–100% |
| Over-allocation | No (within WARN-acknowledged range; Sprint 2 has buffer) |

**Outcome:** WARN acknowledged. Phasing distributes workload — Sprint 1 is fuller (~2.75–3 days); Sprint 2 is light (~0.5 day). Solo-dev capacity is sufficient across 2 sprints.

---

## Deferred Items

| Item | EPIC | Reason |
|------|------|--------|
| ST-03 | EPIC-02 | Design gate: PO confirmed <20 closed trades (2026-05-16) — PT-04 gate not met; defers to v3.7 |
| ST-04 | EPIC-02 | Depends on ST-03 (spec); deferred with EPIC-02 to v3.7 |
| ST-05 | EPIC-02 | Depends on ST-03 (spec) + ST-04 (API); deferred with EPIC-02 to v3.7 |
