**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-09
**Cycle:** 2026-11-06__release-v9.16

# Sprint Capacity — 2026-11-06__release-v9.16

## Capacity Inputs

```
Sprint duration:    One sprint covering the full release scope (Product Owner, 2026-11-09). Cadence ~1-2 calendar days between sprint starts (workforce_capacity.md, Effective 2026-07-17 baseline).
Available FTE:      1 (solo developer, agent-delegated execution)
Total capacity:     ~24-28 working-day-equivalent units (workforce_capacity.md); 28.00 ceiling
Skill constraints:  Rulings: AI Compliance & Governance Officer (ST-20 collisions); Base44 Frontend Prompt Owner (ST-30 convention). Strategy Rules & System Intent Owner confirmed ST-05's case (c) strategy_rules.md line at seal (RISK-02). Live-environment Human-Delegation: Cybersecurity & Trust Lead and Infrastructure & Operations Owner (ST-11 Anthropic console and Render; ST-12 GitHub secret and console), FinOps & Resource Architect (ST-13 production read, from 2026-11-09), Infrastructure & Operations Owner (ST-14 production benchmark, from ~2026-11-12), AI Compliance & Governance Officer (ST-19 production log tokens). No other role is contended.
```

## Item Effort Mapping

Source: `release_plan.md ## Capacity Check` and `run_manifest.md` §Effort-to-days rule (`workforce_capacity.md` precedence rule, LL-v9.6-P-Closure-01): an explicit day figure wins (range midpoint), else the band midpoint XS=0.15, S=0.5, M=2.5, L=3.5. Every figure reconciles to the release plan's 27.95d. No `[ESTIMATE REQUIRED]` placeholders.

| EPIC | Stories | Slice days | Planning adjustment | Sprint days |
|------|---------|-----------|---------------------|-------------|
| EPIC-01 — Navigation & Wayfinding | 4 | 6.00 | — | 6.00 |
| EPIC-02 — Today List & Signal-to-Entry Flow | 4 | 7.75 | — | 7.75 |
| EPIC-03 — Colour Tokens & Input Contrast | 2 | 3.00 | — | 3.00 |
| EPIC-04 — Anthropic Key Security & Operations Baselines | 5 | 1.10 | — (ST-13, ST-14 0.30 conditional) | 1.10 |
| EPIC-05 — Backend Correctness, AI Ticker Check & Spec Debt | 8 | 1.20 | — | 1.20 |
| EPIC-06 — Arc 2 Retrospective | 4 | 6.50 | — | 6.50 |
| EPIC-07 — Governance Process | 3 | 2.40 | — | 2.40 |
| **Total** | **30** | **27.95** | **—** | **27.95** |

Per-story figures: ST-01 2.50, ST-02 1.00, ST-03 2.00, ST-04 0.50; ST-05 0.75, ST-06 3.50, ST-07 2.50, ST-08 1.00; ST-09 2.50, ST-10 0.50; ST-11 0.15, ST-12 0.50, ST-13 0.15 (conditional), ST-14 0.15 (conditional), ST-15 0.15; ST-16 to ST-23 0.15 each; ST-24 2.00, ST-25 1.00, ST-26 2.00, ST-27 1.50; ST-28 0.15, ST-29 1.00, ST-30 1.25.

### Addendum estimate checks

- **ST-03, held at 2.00d.** 11 dead-end pages, not 8; the three extra links are one line each (addendum).
- **ST-04, held at 0.50d.** Anchor moves to Analytics §19 with a third digest link; same size.
- **ST-05, held at 0.75d.** Adds the plan form's dated snapshot write (JSONB, no migration). Within the S range's upper half; no adjustment.
- **ST-07, held at 2.50d.** `signal_id` route parameter and §5a.1 acceptance are inside the M band.
- **ST-12, held at 0.50d.** Playwright specs asserting AI controls absent in CI are updated, not new.

## Conditional (Deferred)

None. No story is `deferred_at_planning`. ST-13 (`BLG-OPS-197`, gate 2026-11-09) and ST-14 (`BLG-OPS-198`, gate ~2026-11-12) stay in scope as conditional stories (§1.4b), marked `Status at sprint open: conditional` in `sprint_backlog.md`. A return of either at sprint close is expected-path, not a deviation (RISK-05).

> **Gate re-invocation:** If a gate condition is met during the sprint for any item not in scope, do not add it informally. Invoke the amendment cycle (`amend cycle --cycle 2026-11-06__release-v9.16 --reason "<gate met>"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.

## Total Effort vs Capacity

27.95 / 28.00 = **99.8%** of the band ceiling. No over-allocation; capacity check outcome `pass`. The STEP 1.5 buffer floor (95%) is exceeded: the Product Owner acknowledged this and chose to proceed with full scope, consistent with the Release Planning instruction "use full capacity", 2026-11-09.
