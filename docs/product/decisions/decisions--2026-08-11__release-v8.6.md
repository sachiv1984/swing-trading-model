Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v8.6
Cycle: 2026-08-11__release-v8.6
Last Updated: 2026-08-11

## Planning Decisions — v8.6 User Features, Data-Integrity Foundation & Correctness Carryover

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Lead the EPIC table with user-facing feature scope (EPIC-01) ahead of debt/governance scope | Explicit user instruction this cycle ("user features should be prioritised"); also satisfies the Skill-Silo rotation guideline (§3, `release_planning_prompt.md`) given the 2026-08-11 rebalance's 3rd-consecutive-worsening Skill-Silo Alert reading (89.8%) | Product Owner | 2026-08-11 |
| `BLG-FEAT-56`'s qualitative usage-pattern gate condition ("existing AI touchpoints show established, validated usage patterns") is confirmed met | v6.2 (daily briefing + chat AI touchpoints) has been live in production 47 days (shipped 2026-06-25) with no adoption-abandonment signal recorded in any intervening rebalance (`2026-06-30__scheduled` through `2026-08-11__scheduled`); the AI-adoption-window date half of the gate (~2026-07-25) is independently cleared | Product Owner | 2026-08-11 |
| Fill capacity to the top of the confirmed ~24-28 day band rather than leaving slack | Explicit user instruction this cycle ("use full capacity"); added `BLG-BE-92`/`BLG-BE-93` (ungated P2 financial-correctness items) to reach ~23.75 estimated days | Product Owner | 2026-08-11 |
| Include all 20 backlog items already carrying `Provisional-Target: v8.6` | These were horizon-planned for this release at filing time (mostly v8.5 PR-review findings); no item with that signal was excluded | Product Owner | 2026-08-11 |
| Defer `BLG-FEAT-73` (SI-02 frontend) | Gate not met — 0/20 closed trades currently have linked trade plans; `BLG-BE-91` (this cycle) only enforces linkage going forward, does not backfill | Product Owner | 2026-08-11 |
| Defer `BLG-FEAT-74` (PO-05 Replay Mode) | VH effort (>2 weeks) exceeds single-cycle sizing; §13 pre-clearance not yet run | Product Owner | 2026-08-11 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| `BLG-FE-147` (remaining shadcn token registration) should land before/alongside `BLG-FE-148` (Playwright coverage for those tokens) | Coverage needs the tokens registered first to assert real, non-empty computed styles | PMO Lead | 2026-08-11 |
| No forced cross-EPIC sequencing beyond the above | All other EPICs are independent of one another; Sprint Planning has full freedom to interleave | PMO Lead | 2026-08-11 |

### Accepted risks

| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|--------------|-----------|
| None | — | No escalations were raised this cycle (all preflight/hard gates passed cleanly) | — | — |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-08-11__release-v8.6
