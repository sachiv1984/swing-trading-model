Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-23
Cycle: 2026-07-21__release-v7.7

# Sprint Capacity — 2026-07-21__release-v7.7

## 1.1 Capacity Inputs

```
Sprint duration:    ~1–2 calendar days between sprint starts (back-to-back permitted); no fixed working-day box — effort-bounded per workforce_capacity.md
Available FTE:      1 (solo developer / autonomous execution engine, evenings/weekends pace)
Total capacity:     ~24–28 working-day-equivalent per sprint (effective 2026-07-17, DL-069)
Skill constraints:  None scarce — all 11 EPICs draw on roles already represented in claude/agents/ with no concurrent-use conflict this sprint
```

## 1.2 Item Effort Mapping

| EPIC | ST | Backlog item | Owner | Effort | Midpoint (days) |
|------|----|--------------|-------|--------|------------------|
| EPIC-01 | ST-01 | `BLG-FEAT-75` | Head of Engineering; Head of UX & Design | H (>5d) | 6.5 |
| EPIC-02 | ST-02 | `BLG-FE-114` | Head of UX & Design; Frontend Specs & UX Documentation Owner | M (~1–2d) | 1.5 |
| EPIC-03 | ST-03 | `BLG-FE-113` | Head of UX & Design; Frontend Specs & UX Documentation Owner | XS–S | 0.75 |
| EPIC-04 | ST-04 | `BLG-FE-120` | Base44 Frontend Prompt Owner | M (no range) | 2.0 |
| EPIC-05 | ST-05 | `BLG-FEAT-80` | Product Owner | M | 2.0 |
| EPIC-06 | ST-06 | `BLG-OPS-108` | Infrastructure & Operations Owner | S (~0.5–2d) | 1.25 |
| EPIC-07 | ST-07 | `BLG-GOV-28` | Head of Specs Team | S (~0.5d) | 0.5 |
| EPIC-08 | ST-08 | `BLG-QA-104` | QA & Testing Owner | XS (<1d) | 0.5 |
| EPIC-09 | ST-09 | `BLG-BE-63` | Backend Engineering Patterns Owner | S (~1d) | 1.0 |
| EPIC-10 | ST-10 | `BLG-OPS-110` | Infrastructure & Operations Owner; Head of Engineering | M (~1–2d) | 1.5 |
| EPIC-11 | ST-11 | `BLG-QA-102` | QA & Testing Owner | M (no range) | 2.0 |

All 11 items carry an effort estimate from `release_plan.md ## Execution Plan` / `## Capacity Check` — no `[ESTIMATE REQUIRED]` placeholders.

**Effort Day-Range Advisory (carried from `release_plan.md`):** 2 of 11 items (`BLG-FE-120`, `BLG-QA-102`) carry a bare `M` with no explicit day-range parenthetical (per `shared_standards.md §16.12`). Not backfilled here — flagged for owner judgment at next `groom backlog`. Conservative 2.0-day midpoint used for both in this capacity check, consistent with `release_plan.md`.

## 1.3 Total Effort vs Capacity

**Total estimated effort:** ~19.5 days midpoint (range ~16–24 days depending on where the two unlabelled "M" items and the XS–S/S range items fall).
**Confirmed capacity:** ~24–28 working-day-equivalent per sprint.

~19.5 of ~24–28 days ≈ 70–81% of ceiling. **No over-allocation. No capacity WARN.** This deliberately maximises utilisation per explicit user instruction ("ensure you use full capacity") while retaining ~20–30% buffer against estimate variance (see `release_plan.md` Capacity Check / `run_manifest.md` Full-Capacity Fill Rationale). No Product Owner acknowledgement required; no Phasing Recommendation exists for this cycle (none was produced at release planning — capacity check was `pass`, not `warn`).

## 1.4 Gate-Conditional Deferred Items

None. `stage4_backlog_slice.md` marks EPIC-01 through EPIC-04 "conditional, not firm" pending Design Gate PASS — that condition is now satisfied (`design_gate_status: Passed`, confirmed 2026-07-21T11:20:00Z, `design_gate.md`: 11/11 cleared, 0 blocked). No item in this slice carries a `gate_condition` / `deferred_at_planning` status. All 11 items proceed to Sprint Scope as `include`.
