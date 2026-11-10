**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-11-10 (created — v9.16 ST-29/BLG-GOV-26)

---

# Arc 2 Velocity Report

## Purpose

This report gives arc-level delivery velocity for Arc 2 (Pre-Trade Research & Planning). It covers stories per cycle, the EPIC completion rate and rolling velocity. Arc 2 is used as the baseline for later arcs.

Arc 2 was planned for v3.1–v3.3. It was declared complete at v6.1, when PT-04 (Setup Quality Score) shipped (`current_roadmap.md`: "Arc 2 ✅ Fully Complete (v3.1–v6.1)"). The report therefore covers every release cycle from v3.1 to v6.1.

## Sources and method

- **Story counts** come from the Velocity History table in `claude/cycles/velocity_metrics.md`. That file is the canonical per-cycle record, and its Planned, Completed and Velocity definitions apply here unchanged.
- **EPIC counts** come from each cycle's `claude/cycles/<date>__release-vX.Y/execution_state.json`.
- **Generator:** `scripts/arc_velocity_report.py`. The data section below is its output and should not be edited by hand. To regenerate it:
  `python3 scripts/arc_velocity_report.py --arc "Arc 2" --from v3.1 --to v6.1 --out docs/governance/arc_velocity_report_arc2.md`

**Measures**

| Measure | Definition |
|---------|------------|
| Stories per cycle | Completed stories per cycle (mean, median, range) |
| Velocity | Completed / Planned per cycle, as defined in `velocity_metrics.md` |
| Arc velocity | Total Completed / total Planned across the arc, weighted by story count |
| EPIC completion rate | EPICs ending `merged` or `done`, divided by EPICs in sprint scope. EPICs `deferred_at_planning` were never in scope and are left out of the denominator. |
| Rolling velocity | Mean per-cycle velocity over the trailing 6 cycles (the `velocity_metrics.md` window) |

## Data

<!-- arc-velocity:begin -->
### Arc 2 summary (v3.1–v6.1)

| Measure | Value |
|---------|-------|
| Cycles | 31 |
| Stories planned / completed | 365 / 347 |
| Arc velocity (story-weighted) | 0.951 |
| Mean per-cycle velocity | 0.942 |
| Stories completed per cycle | mean 11.2, median 11, range 2–24 |
| EPIC completion rate | 104 / 108 = 0.963 |
| EPICs deferred at planning (excluded) | 2 |
| Cycles below velocity 1.00 | 6 of 31 |
| Lowest 6-cycle rolling velocity | 0.743 (window ending v5.8) |
| Rolling velocity at arc close | 0.833 (window ending v6.1) |

### Arc 2 per-cycle detail

| Cycle | Planned | Completed | Velocity | 6-cycle rolling | EPICs completed / in scope | Not completed |
|-------|---------|-----------|----------|-------------|-----------------|---------------|
| v3.1 | 14 | 14 | 1.00 | — | 4 / 4 | — |
| v3.2 | 17 | 17 | 1.00 | — | 4 / 4 | — |
| v3.3 | 17 | 14 | 0.82 | — | 4 / 4 | — |
| v3.4 | 14 | 14 | 1.00 | — | 4 / 4 | — |
| v3.5 | 13 | 13 | 1.00 | — | 4 / 4 | — |
| v3.6 | 7 | 7 | 1.00 | 0.970 | 3 / 3 | — |
| v3.7 | 8 | 8 | 1.00 | 0.970 | 3 / 3 | — |
| v3.8 | 8 | 8 | 1.00 | 0.970 | 3 / 3 | — |
| v3.9 | 12 | 12 | 1.00 | 1.000 | 4 / 4 | 1 deferred at planning |
| v4.0 | 11 | 11 | 1.00 | 1.000 | 3 / 3 | 1 deferred at planning |
| v4.1 | 15 | 14 | 0.93 | 0.988 | 4 / 4 | — |
| v4.2 | 13 | 13 | 1.00 | 0.988 | 4 / 4 | — |
| v4.3 | 18 | 18 | 1.00 | 0.988 | 4 / 4 | — |
| v4.4 | 13 | 13 | 1.00 | 0.988 | 4 / 4 | — |
| v4.5 | 8 | 8 | 1.00 | 0.988 | 3 / 3 | — |
| v4.6 | 18 | 18 | 1.00 | 0.988 | 3 / 4 | EPIC-02: returned_to_backlog |
| v4.7 | 8 | 8 | 1.00 | 1.000 | 4 / 4 | — |
| v4.8 | 7 | 7 | 1.00 | 1.000 | 2 / 2 | — |
| v4.9 | 5 | 5 | 1.00 | 1.000 | 3 / 3 | — |
| v5.0 | 13 | 13 | 1.00 | 1.000 | 4 / 4 | — |
| v5.1 | 6 | 6 | 1.00 | 1.000 | 3 / 3 | — |
| v5.2 | 16 | 16 | 1.00 | 1.000 | 4 / 4 | — |
| v5.3 | 24 | 24 | 1.00 | 1.000 | 4 / 4 | — |
| v5.4 | 4 | 3 | 0.75 | 0.958 | 3 / 3 | — |
| v5.5 | 14 | 10 | 0.71 | 0.910 | 3 / 4 | EPIC-04: returned_to_backlog |
| v5.6 | 10 | 10 | 1.00 | 0.910 | 3 / 3 | — |
| v5.7 | 14 | 10 | 0.71 | 0.862 | 2 / 3 | EPIC-03: returned_to_backlog |
| v5.8 | 7 | 2 | 0.29 | 0.743 | 1 / 2 | EPIC-02: gate_deferred |
| v5.9 | 11 | 11 | 1.00 | 0.743 | 2 / 2 | — |
| v6.0 | 11 | 11 | 1.00 | 0.785 | 4 / 4 | — |
| v6.1 | 9 | 9 | 1.00 | 0.833 | 4 / 4 | — |
<!-- arc-velocity:end -->

## Findings

1. **Delivery was steady except during one gate-blocked stretch.** 25 of 31 cycles completed every planned story. Four of the six shortfalls fell between v5.4 and v5.8 (v5.4, v5.5, v5.7, v5.8), when the 2026-06-21 and 2026-07-04 date gates had not cleared. Stories and EPICs that depended on them were returned (v5.4, v5.5, v5.7) or deferred (v5.8). The rolling velocity fell to 0.743 at v5.8 and had recovered to 0.833 by arc close. The other two were v3.3 (0.82), where three `delegated_frontend` stories were returned to backlog, and v4.1 (0.93), where ST-11's staging ACs were returned at the Product Owner's discretion. After v3.0 retired Base44 delegation, and v3.1 moved frontend work to autonomous delivery, that cause did not recur.
2. **No story was missed for lack of capacity.** All 18 stories not completed in the arc are recorded in `velocity_metrics.md` as gate-deferred or returned to backlog. Gates account for 14 of them (v5.4 1, v5.5 4, v5.7 4, v5.8 5). Three were `delegated_frontend` returns (v3.3), and one was a Product Owner discretionary deferral (v4.1). None is recorded as unfinished because the sprint ran out of capacity.
3. **Arc 2 velocity was not exclusive to Arc 2.** Arcs 3, 4, 5 and 6 work, and governance work, ran in the same cycles. Read the figures as the delivery system's velocity across the Arc 2 window, not as Arc 2 feature throughput. Arc 2's own gating cost was the repeated PT-04 deferral, from v3.6 onward (`velocity_metrics.md` counts the 4th at v4.0 and the 6th at v4.6). It appears as `deferred_at_planning` EPICs at v3.9 and v4.0, and at v3.6 as an EPIC deferred before execution started. One source conflict: `velocity_metrics.md` calls v4.6's EPIC-02 "deferred at planning", but its `execution_state.json` records `returned_to_backlog`. This report follows `execution_state.json`, so v4.6 shows 3 / 4 EPICs.
4. **Baseline for Arc 3+ planning.** Planners can expect about 11 stories and 3–4 EPICs per cycle, with an arc velocity of about 0.95. A gate-dependent run of cycles can pull the rolling figure down to about 0.75. Cycles from v6.2 onward use larger, full-capacity sprints (often 20–50 stories), so later arcs should be compared on velocity and EPIC completion rate, not on raw stories per cycle.

## Reusing this format for Arc 3+

1. Copy this file to `docs/governance/arc_velocity_report_arc<N>.md`. Update the header, Purpose (the arc's release range and the record that closes it) and Findings. Keep the two `arc-velocity` markers.
2. Run `python3 scripts/arc_velocity_report.py --arc "Arc <N>" --from v<first> --to v<last> --out docs/governance/arc_velocity_report_arc<N>.md`.
3. Any cycle missing a `velocity_metrics.md` row or an `execution_state.json` is listed under "Cycles in range with missing inputs". Backfill `velocity_metrics.md` before using the figures.

Producing this report automatically at arc close, and feeding it into Release Planning for arc-boundary cycles, needs a governance prompt change. That change is not made here. It is tracked by `BLG-GOV-415`.
