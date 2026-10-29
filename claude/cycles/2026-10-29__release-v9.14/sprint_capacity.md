Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-29
Cycle: 2026-10-29__release-v9.14

# Sprint Capacity — 2026-10-29__release-v9.14

## Capacity Inputs

```
Sprint duration:    One sprint covering the full release scope (Product Owner, 2026-10-29). Cadence is ~1-2 calendar days between sprint starts, per workforce_capacity.md's Effective 2026-07-17 baseline.
Available FTE:      1 (solo developer, agent-delegated execution)
Total capacity:     ~24-28 working-day-equivalent units (workforce_capacity.md)
Skill constraints:  The Strategy Rules & System Intent Owner rules on ST-03 (regime unknown) and ST-09 (FX convention), and confirmed the three case (c) strategy_rules.md writes (ST-03, ST-09, ST-22) at seal. The AI Compliance & Governance Officer rules on ST-15 and ST-17 and reviews ST-23's production sample. The Head of Specs Team chooses ST-45's option. Live-environment Human-Delegation goes to the Infrastructure & Operations Owner (ST-01 Render dashboard, ST-23 production credential, ST-42 run on main, ST-43 Render variable), the FinOps & Resource Architect (ST-39 production cost data) and the Director of Quality or Head of UX & Design (ST-30 staging pass in both themes). No other role is contended.
```

## Item Effort Mapping

An explicit day figure on an item takes precedence over the canonical band-letter midpoint (`workforce_capacity.md` precedence rule, LL-v9.6-P-Closure-01). Range-only items use the range midpoint, and XS items ("<1h", "~1-2h", "<0.5d") are taken at the 0.15d XS midpoint. Calibrated figures come from Release Planning's STEP 4 check (`run_manifest.md`). Every figure reconciles to `release_plan.md ## Capacity Check` (28.00d) before the two planning adjustments below. There are no `[ESTIMATE REQUIRED]` placeholders.

| EPIC | Stories | Slice days | Planning adjustment | Sprint days |
|------|---------|-----------|---------------------|-------------|
| EPIC-01 — Production Deploy & Market-Data Resilience | 8 | 4.15 | ST-03 0.50 → 1.00 (+0.50) | 4.65 |
| EPIC-02 — Sizing, Exit & Position Correctness | 6 | 2.30 | — | 2.30 |
| EPIC-03 — AI Output Safety & Audit Hygiene | 9 | 3.60 | — | 3.60 |
| EPIC-04 — Reports, Dashboard & System Status UI | 5 | 2.60 | — | 2.60 |
| EPIC-05 — Test Coverage & Test Tooling | 9 | 4.50 | — | 4.50 |
| EPIC-06 — Operations, Cost & Security | 6 | 4.05 | — | 4.05 |
| EPIC-07 — Specs & Governance | 11 → 10 | 6.80 | ST-51 deferred at planning (−0.50) | 6.30 |
| **Total** | **54 → 53** | **28.00** | **0.00** | **28.00** |

Per-story figures: ST-01 1.00 (calibrated), ST-02 0.50, ST-03 1.00 (raised), ST-04 0.50, ST-05 0.50, ST-06 0.15, ST-07 0.50, ST-08 0.50; ST-09 0.50, ST-10 0.50, ST-11 0.50, ST-12 0.15, ST-13 0.50, ST-14 0.15; ST-15 0.50, ST-16 0.15, ST-17 0.15, ST-18 0.50, ST-19 0.15, ST-20 0.15, ST-21 1.00 (calibrated), ST-22 0.50, ST-23 0.50; ST-24 2.00, ST-25 0.15, ST-26 0.15, ST-27 0.15, ST-28 0.15; ST-29 0.50, ST-30 0.50, ST-31 0.15, ST-32 1.25, ST-33 0.15, ST-34 0.15, ST-35 0.15, ST-36 1.50, ST-37 0.15; ST-38 1.00, ST-39 1.00, ST-40 1.25, ST-41 0.15, ST-42 0.15, ST-43 0.50; ST-44 0.50, ST-45 0.25, ST-46 1.25, ST-47 0.25, ST-48 0.15, ST-49 0.15, ST-50 0.50, ST-52 1.00, ST-53 1.00, ST-54 1.25.

### Addendum estimate checks (design gate request)

- **ST-03, raised 0.50 → 1.00d.** The addendum extends the unknown state to four surfaces (Dashboard Card 4, the Signals market status bar, the customisable Dashboard regime widgets and the dashboard). It also adds frontend fallbacks defaulting to `"unknown"`, the `GET /market/status` and `GET /market/regime` contract and `openapi.yaml` changes, and an extra Playwright check of the Signals bar, on top of a strategy ruling with three designed branches. Product Owner, 2026-10-29.
- **ST-04/ST-05, held at 0.50d each.** The addendum adds two fields to a third endpoint, which reuse the field set and the Signals FX tile line, and removes one constant. This is absorbed within the shared design.

## Conditional (Deferred)

| EPIC | Story | Effort band | Gate condition |
|------|-------|-------------|----------------|
| EPIC-07 | ST-51 (`BLG-GOV-185`) | S (~0.5 day) | None to re-open. The AC is already met by `metrics_definitions.md` `## Appendix D — Change Log`. Return it only if the Metrics Definitions & Analytics Owner finds that Appendix D does not meet the item's intent. |

> **Gate re-invocation:** If a gate condition above is met during the sprint, do not add deferred items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-10-29__release-v9.14 --reason "<gate met>"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.

## Total Effort vs Capacity

28.00 / 28.00 = **100%** of the band ceiling. There is no over-allocation. The STEP 1.5 buffer floor (95%) is exceeded: the Product Owner acknowledged this and chose to proceed at the ceiling, consistent with the Release Planning instruction "use full capacity", 2026-10-29.
