Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-07
Cycle: 2026-08-07__release-v8.4

# Sprint Capacity — v8.4

## 1.1 Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (Effective 2026-07-17 cadence declaration); working-day-equivalent band below
Available FTE:      Solo developer-equivalent (workforce_capacity.md — no role-scarce constraints flagged this cycle)
Total capacity:     ~24-28 working-day-equivalent units (Effective 2026-07-17, unchanged since; workforce_capacity.md)
Skill constraints:  None flagged. All 7 EPICs draw from roles already represented in claude/agents/ with no concurrent scarce-skill overlap identified (Data Model & Domain Schema Owner spans EPIC-02 and EPIC-03 but not concurrently scarce — sequencing note below covers the shared-file implication, not a skill conflict).
```

## 1.2 Item Effort Mapping

Effort Band Lookup (ST-14/shared_standards §16.7): `scored_initiatives.md` — 0 matching rows for this cycle's 7 EPICs (backlog-driven debt/hardening/single-feature scope, not roadmap-level scored initiatives). Falling back to `release_plan.md ## Execution Plan`/`## Capacity Check` inline estimates per item's own backlog `Effort` band. No advisory required (Tier 3 — no matching row, no advisory per the three-tier rule).

| EPIC | Items | Effort band(s) | Midpoint days |
|------|-------|-----------------|---------------|
| EPIC-01 | ST-01, ST-31 | XS, S | 1.00 |
| EPIC-02 | ST-02–ST-09 | M, XS, S×5, M | 7.50 |
| EPIC-03 | ST-10–ST-14 | S, S, S, M, M | 5.75 |
| EPIC-04 | ST-15–ST-18 | S, S, M, M | 5.00 |
| EPIC-05 | ST-19–ST-24 | XS, S, XS, S, S, S | 3.50 |
| EPIC-06 | ST-25–ST-28 | XS, M, S, S | 3.50 |
| EPIC-07 | ST-29, ST-30 | S, S | 1.50 |
| **Total (31 items)** | | | **27.75** |

All 31 items carry an `Effort` band and an owner in `release_plan.md ## Execution Plan`. No `[ESTIMATE REQUIRED]` placeholders.

## 1.3 Total Effort vs Capacity

Total estimated effort **~27.75 days** against confirmed capacity **~24-28 days** — within band, at the top. No over-allocation gap relative to the band ceiling (28 days); over-allocation relative to the band floor (24 days) is expected and consistent with the explicit user "full capacity" instruction recorded at release planning (`release_plan.md §Readiness`).

**Outcome carried from `release_plan.md ## Capacity Check`: PASS.** No `warn` outcome — `capacity_warn_acknowledged` not required for this cycle.

## 1.4 Gate-Conditional Deferred Items

None. All 31 items in the authoritative backlog slice enter the sprint (see STEP 3 — no `defer` classifications this cycle; capacity accommodates full scope at the top of the confirmed band).

## 1.5 Minimum Capacity Buffer Floor (Advisory)

`scope_effort ÷ confirmed_capacity` = 27.75 ÷ 28 = **99.1%** (against the band ceiling); 27.75 ÷ 24 = **115.6%** (against the band floor). Both exceed the 95% buffer-floor recommendation (`sprint_planning_prompt.md §1.5`).

**Buffer floor exceeded — advisory, not a hard gate.** Distinct from the (not-triggered) over-100%-of-capacity WARN: the release-planning capacity check outcome is `pass`, not `warn`, so this is the softer buffer-floor advisory only.

**Product Owner acknowledgement (agent-mediated, delegated authority):** Proceed at full scope. Basis: the explicit user instruction recorded at this cycle's release planning ("Use full capacity and prioritise user features," `release_plan.md §Readiness`) already directs scope to the top of the confirmed band; the buffer-floor ratio is the expected consequence of that instruction, not a new finding requiring scope trim. No item removed on buffer-floor grounds.

## Sequencing-Driven Capacity Note

EPIC-02/ST-02 (openapi.yaml structural fix) is foundational to EPIC-02's remaining 7 stories and to EPIC-05/ST-20 (endpoint-list re-verification). See `sprint_planning_notes.md ## Dependency Map` and `## Execution Sequence` for the full sequencing rationale — this does not change the effort totals above, only their order.
