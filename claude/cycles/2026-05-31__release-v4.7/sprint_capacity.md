**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-31
**Cycle:** 2026-05-31__release-v4.7

---

# Sprint Capacity — 2026-05-31__release-v4.7

## Capacity Baseline

| Field | Value |
|-------|-------|
| Sprint duration | ~24–28 working days per sprint (double capacity, per workforce_capacity.md 2026-05-27 revision) |
| Available FTE | Solo developer (evenings/weekends) |
| Warn threshold | Effort > 14 days per sprint |
| Capacity check outcome | PASS |

Source: `claude/roadmap/workforce_capacity.md` (revised 2026-05-27) and release_plan.md §Capacity Check.

## Sprint 1 — Item Effort Mapping (Firm)

| EPIC | ST | Item | Effort | Delegation |
|------|-----|------|--------|------------|
| EPIC-01 | ST-01 | SI-04 §13 pre-assessment (BLG-GOV-62) | S (~1 day) | delegated_decision |
| EPIC-02 | ST-03 | Arc 5 compliance in monthly P&L (BLG-FEAT-38) | M (~2 days) | autonomous |
| EPIC-03 | ST-04 | Staging deploy live verification (BLG-OPS-28) | XS (~0.5 day) | delegated_decision |
| EPIC-03 | ST-05 | DS-07 migration staging verification (BLG-OPS-44) | XS (~0.5 hr) | delegated_decision |
| EPIC-03 | ST-06 | Severity field staging verification (BLG-OPS-45) | XS (~0.5 hr) | delegated_decision |
| EPIC-03 | ST-07 | Render log retention policy (BLG-OPS-31) | S (~0.5 day) | delegated_decision |
| EPIC-04 | ST-08 | Anthropic API tier cost assessment (BLG-OPS-37) | S (~0.5 day) | delegated_decision |
| EPIC-04 | ST-09 | Pre-entry validation panel UX assessment (BLG-FE-49) | S (~0.5 day) | delegated_decision |
| **Sprint 1 total** | | | **~5–6 days** | |

**Sprint 1 utilisation:** ~20–25% of 24–28 day capacity → **PASS** (well within capacity)

## Sprint 2 — Conditional Items

| EPIC | ST | Item | Effort | Gate |
|------|-----|------|--------|------|
| EPIC-01 | ST-02 | SI-05 Phase 1 implementation (BLG-GOV-67) | M (~2–3 days) | SI-01 + SI-03 live ≥30 days — clears 2026-06-21 |

**Sprint 2 conditional utilisation (if gate met):** ~8–12% of capacity → **PASS**

## Conditional (Deferred)

| EPIC | ST | Effort Band | Gate Condition |
|------|-----|-------------|----------------|
| EPIC-01 | ST-02 | M (~2–3 days) | SI-01 + SI-03 live ≥30 days — clears 2026-06-21 |

> **Gate re-invocation:** If the gate condition above is met during the sprint, do not add deferred items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-05-31__release-v4.7 --reason "SI-05 Phase 1 gate met (2026-06-21)"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 days/sprint |
| Sprint 1 estimated effort (in-scope) | ~5–6 days |
| Sprint 1 utilisation | ~20–25% |
| Sprint 2 conditional effort | ~2–3 days (if gate met) |
| Over-allocation | No |
| Capacity verdict | PASS |
