Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-12
Cycle: 2026-08-12__release-v8.7

# Sprint Capacity — 2026-08-12__release-v8.7

## 1.1 Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (workforce_capacity.md cadence declaration, effective 2026-07-17); effort measured in day-equivalent units, not calendar days
Available FTE:      1 (solo developer, generalist — no role-locked skill gaps identified for this scope)
Total capacity:     ~24-28 working-day-equivalent units (workforce_capacity.md, unchanged since 2026-07-17; warn threshold >28)
Skill constraints:  None material — scope spans frontend (EPIC-01/03), backend (EPIC-02/04), security (EPIC-05), infra (EPIC-06), and governance (EPIC-07) but all fall within the single generalist role's established coverage; no specialist-only skill named in release_plan.md's Execution Plan
```

## 1.2 Item Effort Mapping

Effort letters per `stage4_backlog_slice.md` (Effort field); EPIC-level day subtotal per `release_plan.md ## Capacity Check` (schema v2 — no per-item day range published, EPIC subtotal is the authoritative day figure; all 21 items carry `Provisional-Target: TBD` or `v8.7 or later`, so a per-item day range is not mandatory per `shared_standards.md §16.12`).

| EPIC | ST Item | Effort (letter) | Estimate present? |
|------|---------|------------------|--------------------|
| EPIC-01 | ST-01 | M | Yes |
| EPIC-01 | ST-02 | XS | Yes |
| EPIC-01 | ST-03 | S | Yes |
| EPIC-01 | ST-04 | S | Yes |
| EPIC-01 | ST-05 | S | Yes |
| EPIC-01 | ST-06 | S | Yes |
| EPIC-02 | ST-07 | S | Yes |
| EPIC-03 | ST-08 | S | Yes |
| EPIC-03 | ST-09 | XS | Yes |
| EPIC-04 | ST-10 | M | Yes |
| EPIC-04 | ST-11 | M | Yes |
| EPIC-04 | ST-12 | S | Yes |
| EPIC-05 | ST-13 | M | Yes |
| EPIC-05 | ST-14 | M | Yes |
| EPIC-06 | ST-15 | S | Yes |
| EPIC-06 | ST-16 | S | Yes |
| EPIC-06 | ST-17 | S | Yes |
| EPIC-07 | ST-18 | S | Yes |
| EPIC-07 | ST-19 | M | Yes |
| EPIC-07 | ST-20 | S | Yes |
| EPIC-07 | ST-21 | M | Yes |

No `[ESTIMATE REQUIRED]` placeholders — all 21 items carry an effort letter and roll up to a published EPIC-level day subtotal.

| EPIC | Subtotal (days) |
|------|------------------|
| EPIC-01 | 6.25 |
| EPIC-02 | 1.00 |
| EPIC-03 | 1.50 |
| EPIC-04 | 4.50 |
| EPIC-05 | 3.50 |
| EPIC-06 | 3.00 |
| EPIC-07 | 5.50 |
| **Total** | **25.25** |

## 1.3 Total Effort vs Capacity

Total estimated effort: **25.25 days** vs confirmed capacity **~24-28 days**. Within band — no over-allocation. `capacity_check` outcome (per `release_plan.md`): **pass** (not `warn`); no Product Owner WARN acknowledgement required.

## 1.4 Gate-Conditional Deferred Items

None. No ST items in `stage4_backlog_slice.md` are recorded as `status: deferred_at_planning` with a `gate_condition` — all 21 items are confirmed ungated (`release_plan.md` Readiness: `scripts/scan_backlog_gate_conditions.py`, 292 items scanned, 175 gated, all 21 selected items confirmed ungated).

## 1.5 Minimum Capacity Buffer Floor (Advisory)

25.25 ÷ 26 (band midpoint) ≈ 97%; against the top of the band (28) ≈ 90%. Using the band midpoint as the reference, the ratio exceeds the 95% advisory floor. Surfaced to Product Owner: **buffer floor advisory noted** — this is consistent with the cycle's explicit user-directed capacity assumption ("use full capacity, user features to be prioritised," carried from Release Planning into `release_plan.md`'s Readiness section), not an unplanned overrun. Product Owner disposition: **proceed** — no scope trim; the user's own capacity instruction already accounts for running at the top of the band. Advisory only; does not block sealing.
