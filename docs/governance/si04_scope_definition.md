**Owner:** Product Owner; Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-28
**Cycle:** 2026-05-27__release-v4.2 — ST-12 (BLG-GOV-57)
**Input source:** Product Owner scope input 2026-05-28

---

# SI-04 Strategy Version Comparison — Scope Definition

## Purpose

This document defines the feature scope for SI-04 (Strategy Version Comparison), the Arc 5 analytical closure feature. It serves as the primary input to SI-04 sprint planning and the §13 formal pre-assessment (BLG-GOV-62).

---

## Feature Intent

SI-04 lets a trader compare the aggregate performance of their trading strategy across two self-defined time periods. The goal is to surface whether a strategy change (e.g. tightening stop-loss rules, changing setup type filter) measurably improved outcomes — using only closed-trade history already in the system.

This is retrospective descriptive analytics. No predictions, no adaptive logic, no recommendations. Display-only output, operator-reviewed.

---

## Version Definition

**Strategy versions are defined by date range, not by a formal version object.**

A "version" is a continuous period the trader designates with a start and end date. The user selects two non-overlapping date ranges:

- **Version A** — the baseline period (e.g. 2026-01-01 to 2026-03-31)
- **Version B** — the comparison period (e.g. 2026-04-01 to 2026-06-30)

There is no formal strategy versioning schema, no tagged strategy objects, and no version migration required. Dates are the version boundary. This keeps implementation scope minimal and avoids schema changes to `trade_history`.

---

## Performance Comparison Methodology

Performance is computed as aggregate metrics over closed trades (`exit_date` within the selected range). The delta is Version B minus Version A for each metric.

### Metrics

| Metric | Definition | Source |
|--------|-----------|--------|
| Win rate | % of trades with `pnl > 0` | `trade_history.pnl` |
| Average R-multiple | Mean `(exit_price - entry_price) / (entry_price - stop_loss)` | `trade_history` |
| Average hold time | Mean `(exit_date - entry_date)` in calendar days | `trade_history` |
| Max drawdown per trade | Largest single-trade loss as % of entry value | `trade_history.pnl_pct` |
| Trade count | Number of closed trades in period | `trade_history` |

**Computation rule:** Deterministic aggregates only — sum, mean, count, min/max. No regression, no weighted scoring, no adaptive normalisation.

**Delta display:** Version B minus Version A, shown with sign (+/−). Example: `+0.4R avg R-multiple`, `+8% win rate`, `−2 days avg hold`.

### Minimum trade threshold

A version period with fewer than **5 closed trades** should display a warning: "Insufficient trades for reliable comparison (minimum 5 required)" rather than suppressing the comparison entirely. The metrics are still shown but flagged.

---

## UI View Concept

**Location:** Analytics section, new tab or sub-section labelled "Strategy Versions."

**Layout:** Two-column comparison card.

```
┌─────────────────────────────────────────────────────────────┐
│  Strategy Version Comparison                                │
│                                                             │
│  Version A: [date picker] to [date picker]                  │
│  Version B: [date picker] to [date picker]                  │
│                           [Compare]                         │
├─────────────────┬───────────────────────────────────────────┤
│  Metric         │  Version A    │  Version B    │  Delta    │
├─────────────────┼───────────────┼───────────────┼───────────┤
│  Win Rate       │  52%          │  61%          │  +9%      │
│  Avg R-Multiple │  1.8R         │  2.2R         │  +0.4R    │
│  Avg Hold Time  │  12 days      │  9 days       │  −3 days  │
│  Max Drawdown   │  −4.2%        │  −3.1%        │  +1.1%    │
│  Trade Count    │  24           │  18           │  −6       │
└─────────────────┴───────────────┴───────────────┴───────────┘
```

**Interaction model:**
- User selects two date ranges via date pickers
- Clicks "Compare" button (no auto-refresh)
- Table renders with Version A, Version B, and Delta columns
- Delta cells use green for positive improvement, red for regression (per existing design system conventions)
- No chart required for Phase 1 MVP — tabular is sufficient

**Empty state:** If no closed trades exist in either period, display: "No closed trades found for the selected period."

---

## Data Source

- **Table:** `trade_history`
- **Filter:** `exit_date BETWEEN :start AND :end` (closed trades only; open positions excluded)
- **Scope:** Current portfolio only (no cross-portfolio comparison)
- **No new database tables required** for Phase 1

---

## §13 Compliance Pre-Assessment

SI-04 output is retrospective descriptive analytics:
- No prediction or forward-looking inference
- No automated recommendation ("you should change your strategy")
- No influence on trade entry, position sizing, stop placement, or alert triggering
- Display-only; operator reviews and interprets output

**§13 status (pre-assessment):** CONDITIONALLY COMPLIANT candidate. Formal §13 review (BLG-GOV-62) must be completed before SI-04 sprint planning seals.

---

## Out of Scope (Phase 1)

The following are explicitly deferred to Arc 6 or a later SI-04 phase:

- Regime-conditional comparison (e.g. "Risk On periods only") — Arc 6 scope (PS-02)
- Cohort-split comparisons (by setup type, market, ticker) — future enhancement
- Statistical significance testing — Arc 6 scope
- Export / PDF reporting
- Formal "strategy version" objects with labels/tags

---

## Dependencies Before Sprint Planning

| Item | Status | Gate |
|------|--------|------|
| BLG-SPEC-33: GET /portfolio/red-flag-journal contract | Required | Check before SI-04 sprint planning |
| BLG-GOV-62: §13 formal pre-assessment for SI-04 | Required | Hard gate before sprint planning seals |
| BLG-BE-18: Arc 5 backend query pattern assessment | Advisory | Review before scoping SI-04 API endpoint |
| BLG-FE-48: Arc5ComplianceSection frontend spec | Advisory | Inform UI integration point |

---

## Sign-Off

**Product Owner:** Approved — 2026-05-28
*Scope input provided directly. Version boundary as date range is intentional simplicity for Phase 1. Regime-conditional and cohort comparisons are deliberately deferred.*

**Head of Specs Team:** Approved (agent-mediated) — 2026-05-28
*Scope definition is internally consistent, deterministic methodology confirmed, §13 pre-assessment path identified, dependencies enumerated. Ready for SI-04 sprint planning input.*
