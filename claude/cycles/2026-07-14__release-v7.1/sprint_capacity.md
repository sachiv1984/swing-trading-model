Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-14
Cycle: 2026-07-14__release-v7.1

# Sprint Capacity — 2026-07-14__release-v7.1

## 1.1 Capacity Inputs

```
Sprint duration:    ~12-14 working days (solo-dev evenings/weekends baseline, workforce_capacity.md Effective 2026-05-27)
Available FTE:      1 (solo developer — all roles autonomous-executed)
Total capacity:     ~12-14 capacity-days
Skill constraints:  None scarce — all 7 items classified `autonomous`, single-operator cadence
```

## 1.2 Item Effort Mapping

| EPIC | ST-ID | Item | Effort estimate | Midpoint (days) |
|------|-------|------|------------------|------------------|
| EPIC-01 | ST-01 | `BLG-BE-59` — Gate nightly backtest ticker eligibility on `ticker_universe.created_at` | M (~1-2 days) | 1.5 |
| EPIC-01 | ST-02 | `BLG-BE-60` — Fix nightly backtest `total_pnl_gbp` non-reproducibility | L (~3-5 days) | 4.0 |
| EPIC-02 | ST-03 | `BLG-FE-107` — Table View RISK OFF badge colour/label spec compliance | S (~0.5 day) | 0.5 |
| EPIC-03 | ST-04 | `BLG-BE-61` — Position review-cadence nudge: backend/data-integrity hardening | M | 2.0 |
| EPIC-03 | ST-05 | `BLG-QA-106` — Position review-cadence nudge: frontend/QA polish | M | 2.0 |
| EPIC-03 | ST-06 | `BLG-SPEC-83` — Realized/unrealized P&L split: spec & metrics hardening | M | 2.0 |
| EPIC-03 | ST-07 | `BLG-SPEC-84` — Tax-year P&L CSV export: spec & test hardening | M | 2.0 |
| **Total** | | | | **14.0** |

No item lacks an effort estimate. No `[ESTIMATE REQUIRED]` placeholders.

## 1.3 Total Effort vs Capacity

Total estimated effort (14.0 days midpoint) sits at the top of the ~12-14 day capacity band with zero buffer; pessimistic case (top of ST-01/ST-02 ranges, +1.5d) reaches ~15.5 days, past the 14-day warn threshold.

**Outcome: WARN** (carried from `release_plan.md §Capacity Check`). Product Owner explicitly acknowledged the over-capacity risk and elected full scope (all 3 EPICs, 7 stories) in this single sprint rather than the phased Sprint 1 / Sprint 2 split the release plan proposed as an alternative. See `sprint_planning_notes.md §Capacity WARN Acknowledgement`.

## 1.4 Gate-Conditional Deferred Items

None. All 7 items in the authoritative backlog slice are included in this sprint's scope — no item is `status: deferred_at_planning`. (`BLG-BE-62` and `BLG-SPEC-85` were already excluded at release planning — see `stage4_backlog_slice.md ## Deferred Items` — and are not part of this engine's scope selection.)
