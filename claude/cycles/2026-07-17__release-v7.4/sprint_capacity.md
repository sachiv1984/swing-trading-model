Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-17
Cycle: 2026-07-17__release-v7.4

---

# Sprint Capacity — 2026-07-17__release-v7.4

## 1.1 Capacity Inputs

```
Sprint duration:    ~24-28 working days (solo developer, evenings/weekends)
Available FTE:      1 (solo developer — no role-locked skill contention)
Total capacity:     ~24-28 capacity-day units
Skill constraints:  None — sole in-scope item is single-developer-context (spec/UX-documentation/design-review authoring); no scarce or role-locked skills identified
```

Source: `claude/roadmap/workforce_capacity.md` §Sprint Capacity & Cadence Baseline (Effective 2026-07-17) — warn threshold: effort > 28 days.

**Forward-flag verification (`BLG-GOV-249`):** Confirmed this capacity read matches the DL-069 baseline value directly from `workforce_capacity.md`'s most recent entry (raised same-day as this cycle's release plan, 2026-07-17, from the prior ~12–14 day baseline) — not a stale cached figure. Match confirmed: ~24–28 days.

## 1.2 Item Effort Mapping

**Backlog slice in effect:** Amended (`AMD-20260717-01`) — 1 EPIC / 1 ST item in scope (down from the original 5 EPICs / 5 ST items; ST-02/03/04/05 removed, see `sprint_planning_notes.md`).

| EPIC | ST-ID | Item | Effort estimate | Midpoint (days) |
|------|-------|------|------------------|------------------|
| EPIC-01 | ST-01 | `BLG-SPEC-95` | L (~5–7 days) | 6.0 |
| **Total** | | | | **6.0** |

The single in-scope item carries an explicit effort estimate from `release_plan.md ## Execution Plan` (Capacity Check table). No `[ESTIMATE REQUIRED]` placeholder.

## 1.3 Total Effort vs Capacity

Total estimated effort: **6.0 days** (midpoint) against a confirmed ~24–28 day capacity band.

**Outcome: PASS** — 21–25% utilisation of the band, the largest buffer of any v7.x sprint to date. This breaks the 3-consecutive-cycle top-of-band pattern flagged in `2026-07-16__release-v7.3`'s lessons-learnt carry-forward #2 — driven by two compounding factors this cycle: (a) the DL-069 capacity baseline more than doubled (~12–14d → ~24–28d) the same day this release plan was published, and (b) `AMD-20260717-01` cut scope from 5 items (17-day original estimate) to 1 item (6-day estimate) after the Design Gate blocked ST-02/03/04/05. No Phasing Recommendation subsection exists or is needed — effort is comfortably within a single sprint with substantial headroom remaining.

Pessimistic reading (top of range): 7 days — still only ~25–29% of the band. No monitoring note required.

## 1.4 Gate-Conditional Deferred Items

None. ST-02/03/04/05 are not gate-conditional deferrals at planning — they were removed from this cycle's authoritative (amended) backlog slice entirely by `AMD-20260717-01` before Sprint Planning began, per a ratified amendment, not a planning-time capacity/dependency decision. They remain valid backlog scope (`BLG-FE-115/116/117/118`) for a future release once design artefacts exist (see `design_gate.md` and `amended_backlog_slice.md`). No `execution_state.json` `deferred_at_planning` entries apply, since the authoritative slice for this sprint (the amended slice) contains only ST-01, and ST-01 is fully in scope.

---
