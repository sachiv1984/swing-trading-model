Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-09
Cycle: 2026-08-08__release-v8.5

# Sprint Capacity — 2026-08-08__release-v8.5

## 1.1 Capacity Inputs

```
Sprint duration:    ~24-28 working-day-equivalent band (Effective 2026-07-17, unchanged since; workforce_capacity.md)
Available FTE:      1 (solo developer, evenings/weekends — all governance roles are agent-embodied personas over this single contributor)
Total capacity:     ~24-28 capacity-day units
Skill constraints:  None named this cycle — no scarce/role-locked skill flagged in workforce_capacity.md or release_plan.md
```

Source: `release_plan.md ## Capacity Check` (schema v2) — no standalone `stage4_5_capacity_check.md` this cycle (pre-v2.11 artefact superseded). `workforce_capacity.md` confirms the ~24-28 day band unchanged since the 2026-07-17 out-of-band raise (DL-069), last re-affirmed at the `2026-07-28__scheduled` rebalance (hold-unchanged decision, 1 data point since raise).

## 1.2 Item Effort Mapping

Per-item effort estimates below apportion `release_plan.md`'s own per-band subtotals (XS ~4.1d / S ~13.75d / M ~9.3d) across each band's member items; all items carry a defined `Effort` band and source estimate — no `[ESTIMATE REQUIRED]` placeholders.

| EPIC | Item | Effort Band | Est. Days |
|------|------|-------------|-----------|
| EPIC-01 | ST-01 | XS | 0.5 |
| EPIC-01 | ST-02 | XS | 0.5 |
| EPIC-02 | ST-03 | S | 1.0 |
| EPIC-02 | ST-04 | S | 1.0 |
| EPIC-02 | ST-05 | S | 0.75 |
| EPIC-03 | ST-06 | S | 1.25 |
| EPIC-03 | ST-07 | XS | 0.3 |
| EPIC-03 | ST-08 | XS | 0.7 |
| EPIC-04 | ST-09 | S | 1.0 |
| EPIC-04 | ST-10 | M | 2.0 |
| EPIC-04 | ST-11 | S | 0.75 |
| EPIC-04 | ST-12 | M | 1.5 |
| EPIC-04 | ST-13 | S | 1.25 |
| EPIC-04 | ST-14 | M | 2.0 |
| EPIC-05 | ST-15 | M | 2.0 |
| EPIC-05 | ST-16 | S | 1.25 |
| EPIC-05 | ST-17 | S | 0.75 |
| EPIC-05 | ST-18 | S | 1.25 |
| EPIC-05 | ST-19 | M | 1.8 |
| EPIC-05 | ST-20 | XS | 0.3 |
| EPIC-06 | ST-21 | S | 1.25 |
| EPIC-06 | ST-22 | S | 1.0 |
| EPIC-06 | ST-23 | XS | 0.9 |
| EPIC-06 | ST-24 | XS | 0.9 |
| EPIC-06 | ST-25 | S | 1.25 |
| **Total** | **25 items** | | **27.15** |

Per-item estimates are indicative midpoints (per `shared_standards.md` standing notice), not committed hours — they reconcile to `release_plan.md`'s own band subtotals exactly.

## 1.3 Total Effort vs Capacity

Total estimated effort: **~27.15 days** against confirmed capacity **~24-28 days**.

**Within capacity band, at the top** — consistent with `release_plan.md`'s own STEP 4.5 Capacity Feasibility outcome (`pass`) and the explicit user "full capacity" instruction carried from release planning. No over-allocation; STEP 3 scope selection admits all 25 items as `include` (see `sprint_planning_notes.md`).

## 1.4 Conditional (Deferred) Items

None. No item in `execution_state.json` is recorded `status: deferred_at_planning` — this is a fresh cycle with no prior `execution_state.json` initialised. All 25 backlog-slice items enter the sprint (see STEP 3 scope selection); none are gate-conditionally deferred.

*(ST-19's conditional in-story scope — "if/when a consumer adopts `ChartContainer`" — is a within-story execution condition documented in the item's own AC/Note, not a planning-time deferral. It is not recorded in this section.)*

## 1.5 Minimum Capacity Buffer Floor (Advisory)

`scope_effort ÷ confirmed_capacity` = 27.15 ÷ 26 (band midpoint) ≈ **104%**; against the band ceiling (28d) = **97%**.

**Buffer floor (95%) exceeded** — consistent with `release_plan.md`'s explicit "top of band" sizing under the user's "full capacity" instruction. This is the same sizing posture as `v8.4` (31 items at the prior top-of-band level). Surfaced to Product Owner per §1.5; recorded as an explicit accept in `sprint_planning_notes.md` (Capacity WARN / buffer-floor acknowledgement), consistent with the standing user capacity instruction already on record this session at release planning — not a fresh over-allocation requiring new scope trimming, since `release_plan.md`'s own capacity outcome is `pass`, not `warn`.
