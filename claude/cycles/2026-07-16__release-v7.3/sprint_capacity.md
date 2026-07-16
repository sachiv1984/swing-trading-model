Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-16
Cycle: 2026-07-16__release-v7.3

---

# Sprint Capacity — 2026-07-16__release-v7.3

## 1.1 Capacity Inputs

```
Sprint duration:    ~12-14 working days (solo developer, evenings/weekends)
Available FTE:      1 (solo developer — no role-locked skill contention)
Total capacity:     ~12-14 capacity-day units
Skill constraints:  None — all 7 items are single-developer-context (frontend UX implementation + spec/readiness authoring); no scarce or role-locked skills identified (workforce_capacity.md, 2026-07-16__scheduled rebalance)
```

Source: `claude/roadmap/workforce_capacity.md` §Sprint Capacity Baseline (Effective 2026-05-27) — warn threshold: effort > 14 days.

## 1.2 Item Effort Mapping

| EPIC | ST-ID | Item | Effort estimate | Midpoint (days) |
|------|-------|------|------------------|------------------|
| EPIC-01 | ST-01 | `BLG-FE-109` | M (~1–2 days) | 1.5 |
| EPIC-01 | ST-02 | `BLG-FE-110` | S–M (~0.5–1 day) | 0.75 |
| EPIC-01 | ST-03 | `BLG-FE-111` | S (~0.5 day) | 0.5 |
| EPIC-02 | ST-04 | `BLG-SPEC-91` | M (~2–3 days) | 2.5 |
| EPIC-03 | ST-05 | `BLG-SPEC-92` | L (~3–4 days) | 3.5 |
| EPIC-04 | ST-06 | `BLG-SPEC-93` | M (~2 days) | 2.0 |
| EPIC-05 | ST-07 | `BLG-SPEC-94` | M (~2–3 days) | 2.5 |
| **Total** | | | | **13.25** |

All 7 items carry explicit effort estimates from `release_plan.md ## Execution Plan` — no `[ESTIMATE REQUIRED]` placeholders.

## 1.3 Total Effort vs Capacity

Total estimated effort: **13.25 days** (midpoint) against a confirmed ~12–14 day capacity band.

**Outcome: PASS** — within band, but with a materially thinner buffer than v7.2 (0.75 days to the 14-day warn threshold, vs. v7.2's 3.5 days). This did not reach the `warn` outcome (`attributes.capacity_feasible: pass` in `release_plan.md`), so the STEP 0 Capacity WARN acknowledgement (IMP-41) is not triggered as a hard gate. No formal `### Phasing Recommendation` subsection was produced by Release Planning (not required by rule at a `pass` outcome).

Pessimistic reading (top of every range): 15.5 days — would exceed the 14-day threshold by 1.5 days. Given this, and per `release_plan.md`'s own advisory (Capacity Check §, and `cycle_summary.md` Next Steps #2): if `BLG-SPEC-92` (ST-05, widest single range) or `BLG-SPEC-94` (ST-07, schema-decision item) trend toward their pessimistic estimates during the sprint, `BLG-SPEC-94` (ST-07 — least urgent of the four readiness passes, no other in-scope item depends on it) is the named first candidate to phase into a second sprint via the amendment cycle. This is recorded as a monitoring note, not a scope change at planning time — full 7-item scope proceeds since the formal outcome is PASS.

## 1.4 Gate-Conditional Deferred Items

None. All 7 backlog-slice items enter the sprint backlog as `include` (see `sprint_planning_notes.md`). No items are conditionally deferred at planning.

---
