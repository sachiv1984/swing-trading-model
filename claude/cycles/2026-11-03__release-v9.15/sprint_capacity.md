Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-03
Cycle: 2026-11-03__release-v9.15

# Sprint Capacity — 2026-11-03__release-v9.15

## Capacity Inputs

```
Sprint duration:    One sprint covering the full release scope (Product Owner, 2026-11-03). Cadence is ~1-2 calendar days between sprint starts, per workforce_capacity.md's Effective 2026-07-17 baseline.
Available FTE:      1 (solo developer, agent-delegated execution)
Total capacity:     ~24-28 working-day-equivalent units (workforce_capacity.md)
Skill constraints:  The Strategy Rules & System Intent Owner rules on ST-01 (acknowledgement vs §4.2.6), ST-20 (effective dates), ST-28 (§13 re-read) and ST-44 (exclusions), confirms ST-10's §13 line, and confirmed the three case (c) strategy_rules.md lines at seal. The Head of UX & Design approves ST-08, ST-09 and ST-10 (Head of Specs Team also for ST-09, Class 1). The Data Model & Domain Schema Owner rules on ST-23; the AI Compliance & Governance Officer on ST-25; the Product Owner on ST-45. Live-environment Human-Delegation goes to the AI Compliance & Governance Officer (ST-24 production log read), the Cybersecurity & Trust Lead (ST-29 Anthropic console), the Data Model & Domain Schema Owner (ST-35, ST-36 staging and production) and the FinOps & Resource Architect (ST-33 production read, from 2026-11-09). No other role is contended.
```

## Item Effort Mapping

An explicit day figure on an item takes precedence over the canonical band-letter midpoint (`workforce_capacity.md` precedence rule, LL-v9.6-P-Closure-01). Range-only items use the range midpoint (ST-01 "~2-3 days" 2.50; ST-02 "~0.5-1 day" 0.75; ST-28, ST-43, ST-44, ST-45 "~0.5-2 days" 1.25), and XS items are taken at the 0.15d XS midpoint. Calibrated figures come from Release Planning's STEP 4 check (`run_manifest.md`: ST-35 1.00, ST-36 0.50). Every figure reconciles to `release_plan.md ## Capacity Check` (28.00d) before the planning adjustment below. There are no `[ESTIMATE REQUIRED]` placeholders.

| EPIC | Stories | Slice days | Planning adjustment | Sprint days |
|------|---------|-----------|---------------------|-------------|
| EPIC-01 — Trade Entry Integrity & Sizing | 7 | 5.05 | — | 5.05 |
| EPIC-02 — Site Structure & Usability Phase 1 | 7 | 8.50 | — | 8.50 |
| EPIC-03 — Metric & Display Correctness | 9 → 8 | 2.40 | ST-16 deferred as superseded (−0.50) | 1.90 |
| EPIC-04 — AI Output Checks & §13 Boundary | 5 | 2.20 | — | 2.20 |
| EPIC-05 — Operations, Security & Market-Data Monitoring | 5 | 2.15 | — (ST-33's 0.15 conditional) | 2.15 |
| EPIC-06 — Data Model & Spec Debt | 3 | 2.00 | — | 2.00 |
| EPIC-07 — QA & Governance Tooling | 9 | 5.70 | — | 5.70 |
| **Total** | **45 → 44** | **28.00** | **−0.50** | **27.50** |

Per-story figures: ST-01 2.50, ST-02 0.75, ST-03 0.50, ST-04 0.50, ST-05 0.15, ST-06 0.50, ST-07 0.15; ST-08 2.00, ST-09 2.00, ST-10 2.00, ST-11 1.00, ST-12 0.50, ST-13 0.50, ST-14 0.50; ST-15 0.15, ST-17 0.15, ST-18 0.15, ST-19 0.15, ST-20 0.15, ST-21 0.15, ST-22 0.50, ST-23 0.50; ST-24 0.15, ST-25 0.50, ST-26 0.15, ST-27 0.15, ST-28 1.25; ST-29 0.50, ST-30 0.50, ST-31 0.50, ST-32 0.50, ST-33 0.15 (conditional); ST-34 0.50, ST-35 1.00 (calibrated), ST-36 0.50 (calibrated); ST-37 0.50, ST-38 0.15, ST-39 0.15, ST-40 0.50, ST-41 0.50, ST-42 0.15, ST-43 1.25, ST-44 1.25, ST-45 1.25.

### Addendum estimate checks

- **ST-01, held at 2.50d.** The addendum adds a ruling first sub-step with both branches already designed, and an optional `pre_entry_override_acknowledged` field on `POST /portfolio/position` (contract and `openapi.yaml`). The M band's midpoint covers it; the released ST-16 0.50d is not reassigned.
- **ST-16, deferred (−0.50d).** See Conditional (Deferred).

## Conditional (Deferred)

| EPIC | Story | Effort band | Gate condition |
|------|-------|-------------|----------------|
| EPIC-03 | ST-16 (`BLG-FE-240`) | S (~0.5 day) | None to re-open in v9.15. Superseded by ST-12, which deletes the only page carrying both widgets. A home-page win rate, if wanted, is new UI for ST-09's spec and a later release. Product Owner, 2026-11-03. |

ST-33 (`BLG-OPS-197`) stays in scope as a conditional story (gate 2026-11-09, §1.4b), not deferred.

> **Gate re-invocation:** If a gate condition above is met during the sprint, do not add deferred items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-11-03__release-v9.15 --reason "<gate met>"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.

## Total Effort vs Capacity

27.50 / 28.00 = **98.2%** of the band ceiling. There is no over-allocation. The STEP 1.5 buffer floor (95%) is exceeded: the Product Owner acknowledged this and chose to proceed, consistent with the Release Planning instruction "use full capacity", 2026-11-03.
