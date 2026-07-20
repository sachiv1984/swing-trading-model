Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-20
Cycle: 2026-07-20__release-v7.6

# Sprint Capacity — 2026-07-20__release-v7.6

## 1.1 Capacity Inputs

```
Sprint duration:    ~1–2 calendar days between sprint starts (back-to-back permitted); no fixed working-day box — effort-bounded per workforce_capacity.md
Available FTE:      1 (solo developer / autonomous execution engine, evenings/weekends pace)
Total capacity:     ~24–28 working-day-equivalent per sprint (effective 2026-07-17, DL-069)
Skill constraints:  None scarce — all 8 EPICs draw on roles already represented in claude/agents/ with no concurrent-use conflict this sprint
```

## 1.2 Item Effort Mapping

| EPIC | ST | Backlog item | Owner | Effort | Midpoint (days) |
|------|----|--------------|-------|--------|------------------|
| EPIC-01 | ST-01 | `BLG-FE-119` | Head of UX & Design; Frontend Specs & UX Documentation Owner | M (~1–2 days) | 1.5 |
| EPIC-02 | ST-02 | `BLG-QA-112` | QA Lead | S (~1 day) | 1.0 |
| EPIC-03 | ST-03 | `BLG-FEAT-79` | Financial Reporting & Records Owner | M (no range) | 2.0 |
| EPIC-04 | ST-04 | `BLG-BE-65` | Backend Engineering Patterns Owner | M (no range) | 2.0 |
| EPIC-05 | ST-05 | `BLG-QA-114` | QA & Testing Owner | M (no range) | 2.0 |
| EPIC-06 | ST-06 | `BLG-BE-62` | Backend Engineering Patterns Owner | M (no range) | 2.0 |
| EPIC-07 | ST-07 | `BLG-FEAT-77` | FinOps & Resource Architect | M (no range) | 2.0 |
| EPIC-08 | ST-08 | `BLG-QA-69` | Director of Quality; Backend Engineering Patterns Owner | M (~1–2 days) | 1.5 |

All 8 items carry an effort estimate from `release_plan.md ## Execution Plan` / `## Capacity Check` — no `[ESTIMATE REQUIRED]` placeholders.

**Effort Day-Range Advisory (carried from `release_plan.md`):** 5 of 8 items (`BLG-FEAT-79`, `BLG-BE-65`, `BLG-QA-114`, `BLG-BE-62`, `BLG-FEAT-77`) carry a bare `M` with no explicit day-range parenthetical (per `shared_standards.md §16.12`). Not backfilled here — flagged for owner judgment at next `groom backlog`. Conservative 2.0-day midpoint used for all 5 in this capacity check, consistent with `release_plan.md`.

## 1.3 Total Effort vs Capacity

**Total estimated effort:** ~14.0 days midpoint (range ~11–17 days depending on where each unlabelled "M" falls within a typical 1.5–3 day band).
**Confirmed capacity:** ~24–28 working-day-equivalent per sprint.

~14 of ~24–28 days ≈ 50–58% of ceiling. **No over-allocation. No capacity WARN.** Consistent with the v7.5 baseline (11–14 days, also ~50–58%). No Product Owner acknowledgement required; no Phasing Recommendation exists for this cycle (none was produced at release planning — capacity check was `pass`, not `warn`).

## 1.4 Gate-Conditional Deferred Items

None. `stage4_backlog_slice.md` marks ST-01 and ST-07 "conditional, not firm" pending Design Gate PASS — that condition is now satisfied (`design_gate_status: Passed`, confirmed 2026-07-20T18:10:00Z, `design_gate.md`: 8/8 cleared, 0 blocked). No item in this slice carries a `gate_condition` / `deferred_at_planning` status. All 8 items proceed to Sprint Scope as `include`.
