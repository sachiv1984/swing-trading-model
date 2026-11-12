**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-12
**Cycle:** 2026-11-11__release-v9.17

# Sprint Capacity — 2026-11-11__release-v9.17

## Capacity Inputs

```
Sprint duration:    One sprint covering the full release scope (Product Owner, 2026-11-12). Cadence ~1-2 calendar days between sprint starts (workforce_capacity.md, Effective 2026-07-17 baseline).
Available FTE:      1 (solo developer, agent-delegated execution)
Total capacity:     ~24-28 working-day-equivalent units (workforce_capacity.md); 28.00 ceiling
Skill constraints:  Head of UX & Design approval of performance.md before ST-06's build (in-story gate, addendum); Metrics Definitions & Analytics Owner KPI confirmation (ST-06 AC 2). Live-environment Human-Delegation: Infrastructure & Operations Owner (ST-15 production api_call_log read and post-fix weekly report; ST-09 production migration and ST-11 production backfill at deploy). RISK-05 decisions were taken at seal by the Strategy Rules & System Intent Owner, so that role is not contended in-sprint. No other role is contended.
```

## Item Effort Mapping

Source: `release_plan.md ## Capacity Check` and the slice's per-story effort (`workforce_capacity.md` precedence rule, LL-v9.6-P-Closure-01): an explicit day figure wins (range midpoint), else the band midpoint XS=0.15, S=0.5, M=2.5, L=3.5. Every figure reconciles to the release plan's 27.95d. No `[ESTIMATE REQUIRED]` placeholders.

| EPIC | Stories | Slice days | Planning adjustment | Sprint days |
|------|---------|-----------|---------------------|-------------|
| EPIC-01 — Phase 3: Positions Redesign | 4 | 7.50 | — | 7.50 |
| EPIC-02 — Phase 3: Journal & Performance Consolidation | 3 | 9.50 | — | 9.50 |
| EPIC-03 — Phase 3: Semantic Colour Token Sweep | 1 | 3.50 | — (boundary set, see below) | 3.50 |
| EPIC-04 — Phase 2 Completion: Stops Moved Group | 2 | 2.00 | — | 2.00 |
| EPIC-05 — Trade Plan Found Defects | 4 | 2.90 | — | 2.90 |
| EPIC-06 — Market-Data Reliability & Sizing Correctness | 3 | 2.00 | — | 2.00 |
| EPIC-07 — Governance, Strategy Copy & Drift Tooling | 3 | 0.55 | — | 0.55 |
| **Total** | **20** | **27.95** | **—** | **27.95** |

Per-story figures: ST-01 2.50, ST-02 2.00, ST-03 1.00, ST-04 2.00; ST-05 3.50, ST-06 3.50, ST-07 2.50; ST-08 3.50; ST-09 1.50, ST-10 0.50; ST-11 1.25, ST-12 0.50, ST-13 0.15, ST-14 1.00; ST-15 1.00, ST-16 0.50, ST-17 0.50; ST-18 0.15, ST-19 0.25, ST-20 0.15.

### Estimate checks at planning

- **ST-08, held at 3.50d (RISK-02).** The boundary is `src/pages/` in full (436 dark-only classes in 21 files, 2026-11-11), plus any component that fails axe `color-contrast` on a routed page in the light theme. The component-only remainder (484 classes in 87 files) is split into **BLG-FE-288** (filed 2026-11-12, PMO Lead and Product Owner). The "no bare `text-white`" AC applies to `src/pages/`.
- **ST-12, held at 0.50d.** The Strategy Rules & System Intent Owner chose option (a), clear on change. Trade Entry's read path is unchanged, so this is the smaller of the two options.
- **ST-19, held at 0.25d.** The Strategy Rules & System Intent Owner chose option (b), reword without a number. There is no `strategy_rules.md`, constants or lint change.
- **ST-06, held at 3.50d.** The spec is sub-step 1, and the build waits on the Head of UX & Design's approval (addendum). The wait is a sequencing risk, not added effort.

## Conditional (Deferred)

None. No story is `deferred_at_planning` and no story has a within-sprint date gate.

> **Gate re-invocation:** If a gate condition is met during the sprint for any item not in scope, do not add it informally. Invoke the amendment cycle (`amend cycle --cycle 2026-11-11__release-v9.17 --reason "<gate met>"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.

## Total Effort vs Capacity

27.95 / 28.00 = **99.8%** of the band ceiling. No over-allocation; capacity check outcome `pass`, so no WARN acknowledgement or Phasing Recommendation applies. The STEP 1.5 buffer floor (95%) is exceeded. The Product Owner acknowledged this and chose to proceed with full scope, consistent with the Release Planning instruction "use full capacity", 2026-11-12.
