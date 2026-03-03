**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-02

---

# QA Evidence Log — EPIC-03: Portfolio Heat Definition in Metrics Spec

**EPIC:** EPIC-03 — Portfolio Heat Definition in Metrics Spec
**Cycle:** 2026-03-02__release-v1.7
**Sprint goal:** Establish foundational governance, quality, and specification artefacts to unlock v1.8 and v2.0 pre-alignment, and resolve spec debt.
**Test scenarios used:** Derived from spec + AC (no pre-existing scenario file for EPIC-03)

---

## Evidence Table

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| TASK-06 | docs/specs/metrics_definitions.md#Portfolio Risk Metrics | Canonical Position Risk formula defined: risk_gbp = shares × entry_price × atr_pct / fx_rate; FX handling documented for GBP-denominated portfolio | Formula defined, GBP-adjusted, FX handling explicit | Pass | None |
| TASK-07 | docs/specs/metrics_definitions.md#Portfolio Risk Metrics | Canonical Portfolio Heat formula defined: sum of position_risk_gbp across all open positions, expressed as % of total portfolio value (GBP) | Formula defined canonically; relationship to Position Risk stated | Pass | None |
| TASK-08 | docs/specs/metrics_definitions.md#Portfolio Risk Metrics | Display thresholds defined as explicit numeric bands with colour guidance (Low / Moderate / Elevated / High) | Thresholds are explicit numbers, not indicative ranges | Pass | None |
| TASK-09 | docs/specs/metrics_definitions.md | metrics_definitions.md updated with Portfolio Risk Metrics section; version bumped 1.5.8 → 1.6.0 | Document updated, version incremented per lifecycle guide §5 | Pass | None |
| TASK-10 | docs/specs/metrics_definitions.md | Head of Specs Team sign-off obtained; v1.8 pre-alignment gate cleared | Sign-off obtained; v1.8 gate cleared | Pass | None |

---

## QA Test Coverage

- **Scenarios run:** Manual acceptance review — spec document review
- **Regression areas checked:** metrics_definitions.md version history; Portfolio Risk Metrics formula correctness; FX handling consistency with portfolio_service.py
- **Known deviations filed:** None
- **Note:** Spec-only EPIC. No backend implementation in scope for v1.7 — implementation of Portfolio Heat display is a downstream task. The formula and thresholds are the deliverable.

---

## QA Sign-off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked

Signed off by: Director of Quality
Date: 2026-03-02
Comments: EPIC-03 fully delivered. metrics_definitions.md v1.6.0 contains canonical Position Risk and Portfolio Heat formulas with explicit numeric display thresholds. Head of Specs Team sign-off confirmed. v1.8 pre-alignment gate cleared.
