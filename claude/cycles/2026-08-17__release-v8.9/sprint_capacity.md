Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-17
Cycle: 2026-08-17__release-v8.9

# Sprint Capacity — 2026-08-17__release-v8.9

## Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (workforce_capacity.md, effective 2026-07-17); this cycle runs 2 sequential sprints (Sprint 1, Sprint 2 — see Multi-Sprint Structure below), gated by the ST-06 §13 review rather than a calendar boundary.
Available capacity: ~24-28 working-day-equivalent units (solo-developer/agent-mediated context; no per-role FTE split — unchanged since 2026-07-17, confirmed current at 2026-07-28 rebalance)
Total capacity:     ~24-28 working-day-equivalent units
Skill constraints:  None material. Metrics Definitions/Strategy Rules & System Intent Owner concurrency not required this cycle (ST-03 spec entry and ST-07 backtesting are sequenced independently). Strategy Rules & System Intent Owner is the sole owner of the ST-23 §13 gate story — no concurrent demand on that role elsewhere in scope.
```

## Item Effort Mapping

Effort labels below are as carried from `stage4_backlog_slice.md`; EPIC day-subtotals are as computed and validated at `release_plan.md ## Capacity Check` (authoritative for the days total — individual XS/S/M/L labels are relative-sizing indicators, not a strict per-item day breakdown).

| EPIC | Story | Effort label | Notes |
|------|-------|--------------|-------|
| EPIC-01 | ST-01 | M | |
| EPIC-01 | ST-02 | S | Depends on ST-01 |
| EPIC-01 | ST-03 | S | |
| **EPIC-01 subtotal** | | **3.25d** | Per `release_plan.md` |
| EPIC-02 | ST-04 | M | |
| EPIC-02 | ST-05 | M | |
| EPIC-02 | ST-06 | M | Sprint 2 — gated on ST-23 |
| EPIC-02 | ST-07 | L | RISK-02: Head of Engineering reuse-feasibility check early in EPIC |
| EPIC-02 | ST-23 (new) | S | §13 gate story — see Multi-Sprint Structure below; not present in `stage4_backlog_slice.md`, scoped directly into this sprint per `design_gate.md` STEP 1 / `execution_prompt.md` §5.1 (`LL-v3.5-SP-01` pattern) |
| **EPIC-02 subtotal** | | **11.00d + ~1d (ST-23)** | 11.00d per `release_plan.md`; ST-23 is an addition beyond the release-planning capacity check baseline — see Capacity Note below |
| EPIC-03 | ST-08 | S | |
| EPIC-03 | ST-09 | XS | Staging-only evidence (real invocation log) |
| EPIC-03 | ST-10 | S | |
| EPIC-03 | ST-11 | S | |
| **EPIC-03 subtotal** | | **3.375d** | Per `release_plan.md` |
| EPIC-04 | ST-12 | XS | |
| EPIC-04 | ST-13 | S | Decision-gated (Product Owner + Frontend Specs) |
| EPIC-04 | ST-14 | S | |
| EPIC-04 | ST-15 | S | |
| **EPIC-04 subtotal** | | **3.375d** | Per `release_plan.md` |
| EPIC-05 | ST-16 | S | |
| EPIC-05 | ST-17 | S | |
| EPIC-05 | ST-18 | XS | |
| **EPIC-05 subtotal** | | **2.375d** | Per `release_plan.md` |
| EPIC-06 | ST-19 | XS | |
| EPIC-06 | ST-20 | S | |
| EPIC-06 | ST-21 | XS | |
| EPIC-06 | ST-22 | S | |
| **EPIC-06 subtotal** | | **2.75d** | Per `release_plan.md` |

## Total Effort vs Capacity

| Metric | Value |
|--------|-------|
| Total estimated effort (release-planning baseline, 22 items) | 26.125d |
| ST-23 addition (§13 gate story, new this routine) | ~1d |
| **Total estimated effort (this sprint, 23 items)** | **~27.125d** |
| Confirmed capacity band | 24-28d |
| Result | **PASS** — within band, does not exceed 28d upper bound. No `warn` outcome. |

No over-allocation requiring Product Owner scope removal. `capacity_warn_acknowledged`: not applicable — capacity check outcome is `pass`, not `warn` (§9 field note).

### Minimum Capacity Buffer Floor Advisory (STEP 1.5)

`scope_effort ÷ confirmed_capacity` (lower bound) = 27.125 ÷ 24 ≈ **113%**; against the upper bound = 27.125 ÷ 28 ≈ **97%**. Both exceed the recommended 95% buffer-floor guideline (advisory only — does not block sealing per §8/STEP 1.5).

**Product Owner acknowledgement (2026-08-17):** Proceed at full ~27.125d scope. Confirmed consistent with the 2026-08-17 widen-to-full-capacity decision already recorded in `release_plan.md` (Product Owner presented with tight/widen/moderate options at release planning, chose widen). No items trimmed.

## Conditional (Deferred)

None. No ST items in the authoritative backlog slice are recorded as `status: deferred_at_planning` with a `gate_condition` in `execution_state.json` — this is a fresh cycle with no prior execution_state.json.

## Multi-Sprint Structure (Design Gate-Mandated)

Per `design_gate.md` (Gate Status: PASSED, ST-06 Conditionally Cleared) and `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-gate-story-scoping.md`: ST-06 (BLG-FEAT-90, Automated AI post-trade debrief) requires a §13 System Boundary Review before implementation may begin, per the `LL-v3.5-SP-01` gate-story pattern (`execution_prompt.md` §5.1).

- **Sprint 1:** all items except ST-06, plus a new gate story **ST-23 — §13 System Boundary Review: Automated AI Post-Trade Debrief** (`delegated_decision`, Strategy Rules & System Intent Owner), scoped directly per the decision record above (not sourced from `stage4_backlog_slice.md` — see `sprint_backlog.md` for its full acceptance criteria, taken verbatim from the decision record).
- **Sprint 2:** ST-06 only, gated on ST-23 reaching `status: done` with a PASS or CONDITIONAL determination. If ST-23 is not resolved by end of Sprint 1: escalate and defer ST-06 to the next cycle (per the decision record's own fallback clause).

This is not a calendar-scheduled Sprint 2 (no fixed gate date) — it is a completion-gated sequencing within the same cycle, re-evaluated at Sprint 2 planning once ST-23 reaches `done`.
