# UX Decision Record — Cohort Analysis (ST-03)

**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-03-06__release-v1.9
**Last Updated:** 2026-03-06
**Approved by:** Product Owner — 2026-03-06

---

## Feature

Group closed trade performance by entry period (month, quarter, year). Extends the Performance Analytics page with a new Cohort Analysis panel.

## Placement Decision

New panel on the Performance Analytics page, positioned after existing performance metrics and before the new Discipline & Compliance section. The panel is always visible (not behind a tab) with a period selector toggle above it.

## Layout

```
[ Performance Analytics Page ]
  ... existing panels ...
  ─────────────────────────────────────
  Cohort Analysis
  Period:  [ Month ▼ ]  [ Quarter ]  [ Year ]
  ─────────────────────────────────────
  | Period     | Trades | Win Rate | Avg R | Total P&L |
  |------------|--------|----------|-------|-----------|
  | Mar 2026   |   8    |  62.5%   | 1.4R  |  £842     |
  | Feb 2026   |  12    |  58.3%   | 1.1R  |  £634     |
  | Jan 2026   |   9    |  55.6%   | 0.9R  | -£122     |
```

- Period selector: three toggle buttons (Month / Quarter / Year) — active state highlighted
- Table: Period, Trade Count, Win Rate, Avg R-Multiple, Total P&L (GBP)
- Table rows sorted descending by period (most recent first)
- P&L positive: green text; negative: red text
- Minimum 3 columns required for display; if fewer, show "Insufficient history for this period"

## States

| State | Behaviour |
|-------|-----------|
| Loading | Skeleton table rows |
| Loaded | Table rendered |
| Insufficient history | Message: "Not enough closed trades to show [period] cohorts" |
| Error | Section-level error card |

## Interactions

- Period toggle updates table data (new API call or filtered from loaded data — engineering decision)
- Hover state on table rows: highlight row

## Acceptance Criteria for UX

- Panel present on analytics page with period toggle (Month/Quarter/Year)
- Table renders 5 columns per spec above
- P&L colour coding
- Loading, insufficient data, and error states per above
- Period toggle changes displayed data
