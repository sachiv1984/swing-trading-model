**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-18
**Cycle:** 2026-11-18__release-v9.18

# Sprint Capacity — 2026-11-18__release-v9.18

## Capacity Inputs

```
Sprint duration:    One sprint covering the full release scope (Product Owner, 2026-11-18). Cadence ~1-2 calendar days between sprint starts (workforce_capacity.md, Effective 2026-07-17 baseline).
Available FTE:      1 (solo developer, agent-delegated execution)
Total capacity:     ~24-28 working-day-equivalent units (workforce_capacity.md); 28.00 ceiling
Skill constraints:  In-story sign-offs before build: Strategy Rules & System Intent Owner (ST-27 exact rule text; ST-12 trade_plan.md §6 §13-note amendment), Metrics Definitions & Analytics Owner (ST-13 rules-followed definition; ST-17 five step definitions), Head of UX & Design (ST-07 dated approval of navigation.md and design_system.md), Cybersecurity & Trust Lead + Product Owner (ST-05 decision), AI Compliance & Governance Officer (ST-39 ruling; ST-40 decision with the Product Owner). Live-environment Human-Delegation: Infrastructure & Operations Owner (ST-32 production weekly report, not before 2026-11-20; ST-17 and ST-27 production migrations at deploy); user permission for staging writes/reads (ST-35 staging correction; ST-04 one real UK row; ST-30 staging check); production debrief sample for ST-40. RISK-05's rule direction was decided at seal, so the Strategy Rules & System Intent Owner is needed in-sprint only to approve the exact text.
```

## Item Effort Mapping

Source: `release_plan.md ## Capacity Check` and the slice's per-story **Planning estimate** (`workforce_capacity.md` precedence rule: an explicit day figure wins). Every figure reconciles to the release plan's 27.95d. No `[ESTIMATE REQUIRED]` placeholders.

| EPIC | Stories | Slice days | Planning adjustment | Sprint days |
|------|---------|-----------|---------------------|-------------|
| EPIC-01 — Phase 4 Stage 1: Correct and Safe | 6 | 3.65 | — | 3.65 |
| EPIC-02 — Phase 4 Stage 2: Home Page and Navigation | 7 | 6.15 | — | 6.15 |
| EPIC-03 — Phase 4 Stage 2: Weekly Review Loop | 4 | 4.25 | — | 4.25 |
| EPIC-04 — First-Time-Right Checks | 7 | 3.70 | — | 3.70 |
| EPIC-05 — Position Data Correctness | 7 | 6.65 | — | 6.65 |
| EPIC-06 — Market-Data Reliability and CI | 7 | 2.55 | — (ST-32 0.25d conditional) | 2.55 |
| EPIC-07 — AI Output Boundary | 2 | 1.00 | — | 1.00 |
| **Total** | **40** | **27.95** | **—** | **27.95** |

Per-story figures: ST-01 0.75, ST-02 0.15, ST-03 0.50, ST-04 0.25, ST-05 0.50, ST-06 1.50; ST-07 0.50, ST-08 1.25, ST-09 1.50, ST-10 0.50, ST-11 0.15, ST-12 0.75, ST-13 1.50; ST-14 0.50, ST-15 0.75, ST-16 0.50, ST-17 2.50; ST-18 0.75, ST-19 1.50, ST-20 0.15, ST-21 0.50, ST-22 0.15, ST-23 0.50, ST-24 0.15; ST-25 0.50, ST-26 0.50, ST-27 3.50, ST-28 0.50, ST-29 0.15, ST-30 1.00, ST-31 0.50; ST-32 0.25, ST-33 0.50, ST-34 0.15, ST-35 0.50, ST-36 0.50, ST-37 0.15, ST-38 0.50; ST-39 0.50, ST-40 0.50.

Firm scope: 27.70d (39 stories). Conditional: 0.25d (ST-32).

### Estimate checks at planning

- **ST-27, held at 3.50d (RISK-05).** The direction was decided at seal (see `sprint_backlog.md` sign-off): a new `strategy_rules.md` §9.1, with a ratio that leaves a non-whole quantity handled manually. Manual entry of the post-split share count is part of the confirmation dialog `positions.md` v2.30 already specifies, so the choice adds no effort. Design gate addendum tier 0 ("Split to confirm") in `positionUrgency.js` is inside the 3.50d.
- **ST-07, held at 0.50d.** The design gate wrote the `navigation.md` half (addendum); the `design_system.md` §14.5 half is most of the work.
- **ST-13, ST-14, ST-16, ST-03, ST-33: addendum API fields.** Each design gate addendum field (`rules_followed`/`rules_broken`, `closed_trades_total`, `red_flags_7d`, `delivery_status`, `data_status`) falls within the story's existing scope bullet for a contract and `openapi.yaml` change. No estimate change.
- **ST-10, held at 0.50d.** The addendum adds Card 3 (`GracePeriodCard.js`) and moves `nextEndsText` into `positionUrgency.js`. This is at the top of the estimate; it is flagged as a slippage watch item, not re-estimated.

## Capacity Buffer Floor (§1.5)

27.95 ÷ 28.00 = **0.998**, above the 0.95 advisory floor. Product Owner chose to proceed at 99.8% in a single sprint, 2026-11-18. Not an over-allocation: scope is within the confirmed band.

## Conditional (Deferred)

| EPIC | Story | Effort | Gate condition |
|------|-------|--------|----------------|
| EPIC-06 | ST-32 (`BLG-OPS-217` remainder) | 0.25d | Conditional, not deferred: within-sprint date gate 2026-11-20 (7 days of production data after PR #2259 merged 2026-11-13T15:11:51Z). Promoted to firm only when the Infrastructure & Operations Owner confirms the post-fix weekly report (dated). If the report is late, or still above 10% without a documented cause, the story returns to backlog. |

> **Gate re-invocation:** If a gate condition above is met during the sprint, do not add deferred items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-11-18__release-v9.18 --reason "<gate met>"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.

ST-32 is in the sealed scope as a conditional story (§1.4b), not `deferred_at_planning`, so meeting its gate needs no amendment. Only if it is dropped does it return to the backlog.
