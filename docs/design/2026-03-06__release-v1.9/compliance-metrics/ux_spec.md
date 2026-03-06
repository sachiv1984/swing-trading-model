# UX Decision Record — Basic Compliance Metrics (ST-01)

**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-03-06__release-v1.9
**Last Updated:** 2026-03-06
**Approved by:** Product Owner — 2026-03-06

---

## Feature

Basic Compliance Metrics — journal completion rate, stop-based exit rate, average position size (% of portfolio).

## Placement Decision

Compliance metrics are **added as a new section on the existing Performance Analytics page**, below the existing analytics panels. They are not a separate page. Rationale: the user visits the analytics page to assess performance; compliance metrics are a natural extension of this review.

Section title: **"Discipline & Compliance"**

## Layout

```
[ Performance Analytics Page ]
  ... existing panels ...
  ─────────────────────────────────────
  Discipline & Compliance
  ─────────────────────────────────────
  [ Journal Completion Rate ]  [ Stop-Based Exit Rate ]  [ Avg Position Size ]
        67%                          83%                        4.2% of portfolio
      (last 30 trades)           (last 30 trades)             (last 30 trades)
```

- Three stat cards in a horizontal row (same visual style as existing metric cards)
- Each card: metric name, value, sub-label showing the denominator/period
- No chart required — scalar values only
- Responsive: stack vertically on narrow viewports

## States

| State | Behaviour |
|-------|-----------|
| Loading | Skeleton cards (same as other analytics loading states) |
| Loaded | Values rendered |
| Insufficient data | Card shows "–" with tooltip "Insufficient trade history" |
| Error | Section-level error card (consistent with §8 error state pattern) |

## Interactions

- No interactions beyond standard page scroll
- Values computed backend-only; no frontend recalculation

## Edge Cases

- Zero trades: all three metrics show "–"
- Journal completion rate: if no trades have a journal entry field, show "–" not 0%

## Acceptance Criteria for UX

- Three metric cards in a new "Discipline & Compliance" section on analytics page
- Values and sub-labels rendered per above
- Responsive stacking on narrow viewports
- Loading and error states match existing analytics page patterns
