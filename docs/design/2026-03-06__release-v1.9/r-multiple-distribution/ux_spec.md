# UX Decision Record — R-Multiple Distribution Report (ST-04)

**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-03-06__release-v1.9
**Last Updated:** 2026-03-06
**Approved by:** Product Owner — 2026-03-06

---

## Feature

Distribution chart of R-multiple values across all closed trades. Extends the Performance Analytics page.

## Placement Decision

New panel on the Performance Analytics page. Positioned within the existing analytics content area, near the existing R-multiple summary metric (if present). The analytics.md spec already references "R-multiple distributions" as a user goal — this delivers it.

## Layout

```
[ R-Multiple Distribution ]
─────────────────────────────────────
Bar chart: X-axis = R-multiple buckets, Y-axis = trade count

   ▇
   ▇ ▇
   ▇ ▇ ▇
   ▇ ▇ ▇ ▇
   ▇ ▇ ▇ ▇ ▇ ▇
  -2R -1R 0R 1R 2R 3R+

Summary stats below chart:
  Median R: 0.9R    |   % trades > 1R: 47%   |   Avg winner: 2.1R   |   Avg loser: -0.8R
```

- Bar chart: R-multiple range bucketed (e.g., <-2R, -2 to -1R, -1 to 0R, 0 to 1R, 1 to 2R, 2 to 3R, >3R — bucket boundaries to be defined by Metrics Definitions owner)
- X-axis: R-multiple range labels; Y-axis: trade count
- Positive R bars: green; negative R bars: red
- Summary stats row below chart: 4 scalar values
- Minimum 5 closed trades required for display

## States

| State | Behaviour |
|-------|-----------|
| Loading | Skeleton chart area |
| Loaded | Chart and stats rendered |
| Insufficient data (<5 trades) | Message: "Close at least 5 trades to see R-multiple distribution" |
| Error | Section-level error card |

## Interactions

- Hover on bar: tooltip showing exact trade count and R-multiple range
- No other interactions required at v1.9

## Acceptance Criteria for UX

- Bar chart present on analytics page with R-multiple distribution
- Colour coding (green/red) per above
- Summary stats row with 4 values
- Hover tooltip on bars
- Insufficient data and error states per above
- All values sourced from backend; no client-side computation of R-multiple
