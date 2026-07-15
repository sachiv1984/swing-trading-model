Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-15
Cycle: 2026-07-15__release-v7.2

# Sprint Capacity — 2026-07-15__release-v7.2

## 1.1 Capacity Inputs

```
Sprint duration:    ~12-14 working days (solo-dev evenings/weekends baseline, workforce_capacity.md Effective 2026-05-27)
Available FTE:      1 (solo developer — all roles autonomous-executed)
Total capacity:     ~12-14 capacity-days
Skill constraints:  None scarce — all 5 in-scope items classified `autonomous`, single-operator cadence
```

## 1.2 Item Effort Mapping

| EPIC | ST-ID | Item | Effort estimate | Midpoint (days) |
|------|-------|------|------------------|------------------|
| EPIC-01 | ST-01 | `BLG-FE-55` — Mobile responsiveness baseline assessment | M (~1-2 days) | 1.5 |
| EPIC-02 | ST-02 | `BLG-SPEC-89` — BLG-FE-109 pre-implementation readiness pass | M (~2-3 days) | 2.5 |
| EPIC-03 | ST-04 | `BLG-SPEC-90` — BLG-FE-110/111 pre-implementation spec & instrumentation pass | S–M (~1-2 days) | 1.5 |
| EPIC-04 | ST-07 | `BLG-FE-112` — Notification/digest surface consolidation review (audit only) | M (~1-2 days) | 1.5 |
| EPIC-05 | ST-08 | `BLG-QA-111` — Combined design review + shared Playwright suite plan | S (~0.5-1 day) | 0.75 |
| **Total (in-scope)** | | | | **7.75** |

No in-scope item lacks an effort estimate. No `[ESTIMATE REQUIRED]` placeholders.

## 1.3 Total Effort vs Capacity

Total estimated effort for in-scope items (7.75 days midpoint) sits well within the ~12-14 day capacity band, with ~4.25–6.25 days of buffer. Pessimistic reading (top of every in-scope range): 2+3+2+2+1 = 10 days — still within band.

**Outcome: PASS.** No capacity WARN. No Product Owner acknowledgement required.

## 1.4 Gate-Conditional Deferred Items

`ST-03` (`BLG-FE-109`), `ST-05` (`BLG-FE-110`), `ST-06` (`BLG-FE-111`) are deferred out of this sprint — not for capacity reasons, but per the explicit sequencing constraints written into `stage4_backlog_slice.md` (EPIC-02, EPIC-03) and re-confirmed in `design_gate.md`'s Notes: each implementation story may not enter sprint planning until its own readiness/spec pass (`ST-02`, `ST-04` respectively) has *completed* — i.e. been executed, not merely planned. Since `ST-02`/`ST-04` are only entering their first sprint in this run, that condition is not yet met.

| Item | EPIC | Effort band | Gate condition |
|------|------|-------------|-----------------|
| ST-03 | EPIC-02 | M (~1-2 days) | `ST-02` (`BLG-SPEC-89`) must complete execution before `ST-03` enters sprint planning (per `stage4_backlog_slice.md` EPIC-02 sequencing constraint) |
| ST-05 | EPIC-03 | S–M (~0.5-1 day) | `ST-04` (`BLG-SPEC-90`) must complete execution before `ST-05` enters sprint planning (per `stage4_backlog_slice.md` EPIC-03 sequencing constraint) |
| ST-06 | EPIC-03 | S (~0.5 day) | `ST-04` (`BLG-SPEC-90`) must complete execution before `ST-06` enters sprint planning (per `stage4_backlog_slice.md` EPIC-03 sequencing constraint) |

These entries are recorded in `execution_state.json` (initialised this run — see `sprint_planning_notes.md §Planning-deferred item traceability`) as `status: deferred_at_planning`.

**Gate re-invocation:** If a gate condition above is met during the sprint (i.e. `ST-02` or `ST-04` complete execution and merge), do not add the deferred item informally. Re-invoke `plan sprint --cycle 2026-07-15__release-v7.2` to bring `ST-03`/`ST-05`/`ST-06` into sprint planning as a follow-on planning pass within this same cycle, per the resumability model in `sprint_planning_prompt.md §11`.
