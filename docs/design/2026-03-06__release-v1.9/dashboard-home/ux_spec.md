# UX Decision Record — Dashboard Homepage / Session Summary (ST-05)

**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-03-06__release-v1.9
**Last Updated:** 2026-03-06
**Approved by:** Product Owner — 2026-03-06

---

## Feature

A proper home page for the product. Replaces/upgrades the existing dashboard (dashboard.md v1.0) with a daily session summary view combining the most important at-a-glance data.

## Design Decision

The existing `dashboard.md` (v1.0) will be updated to v2.0 to incorporate this design. The route remains `/` (root).

## Layout — Five Data Categories

```
[ Home ]
─────────────────────────────────────────────────────────
  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
  │  OPEN POSITIONS  │  │  PORTFOLIO HEAT  │  │  IN GRACE TODAY  │
  │       12         │  │     18.3%        │  │       3          │
  │  (3 profitable)  │  │  (↑ from 16.1%)  │  │  (exit: 8 Mar)  │
  └──────────────────┘  └──────────────────┘  └──────────────────┘

  ┌──────────────────────────────┐  ┌──────────────────────────────┐
  │        SIGNAL STATUS         │  │       RECENT ACTIVITY        │
  │  SPY: RISK-ON ✓              │  │  Closed NVDA (+2.1R) 2 days  │
  │  FTSE: RISK-ON ✓             │  │  Opened TSLA yesterday       │
  │  2 new signals today         │  │  Stop updated on META        │
  └──────────────────────────────┘  └──────────────────────────────┘
```

## Card Definitions

### Card 1 — Open Positions
- Primary: count of open positions
- Sub-label: count in each state (profitable / losing / grace)
- Source: `GET /positions` (active filter)

### Card 2 — Portfolio Heat
- Primary: `portfolio_heat_percent` from `GET /portfolio`
- Sub-label: delta vs prior day (if `portfolio_history` available) or omit if unavailable
- Colour: green < 15%, amber 15–25%, red > 25% (consistent with Risk Dashboard heat thresholds)

### Card 3 — In Grace Today
- Primary: count of positions currently in grace period
- Sub-label: next grace expiry date (earliest `grace_end_date` among grace positions)
- Source: `GET /portfolio` or `GET /positions`

### Card 4 — Signal Status
- Market regime per market (SPY: RISK-ON/RISK-OFF, FTSE: RISK-ON/RISK-OFF)
- Count of new signals today (from `GET /signals` — signals generated today)
- Source: `GET /market/status`, `GET /signals`

### Card 5 — Recent Activity
- Last 3–5 trade events (closed, opened, stop updated)
- Each entry: ticker + event type + brief value (e.g., R-multiple for closes) + relative date
- Source: `GET /trades` or `GET /positions` activity log (engineering to confirm at pre-alignment)

## States

| State | Behaviour |
|-------|-----------|
| Loading | Skeleton cards for all 5 |
| Loaded | All cards render with live data |
| Partial failure | Individual card shows error indicator; others render normally |
| Error (all) | Full page error with retry |

## Interactions

- Each card is clickable and navigates to the relevant detail page:
  - Open Positions → `/positions`
  - Portfolio Heat → `/risk`
  - In Grace Today → `/risk` (scrolled to grace panel)
  - Signal Status → `/signals`
  - Recent Activity → `/trades`
- No inline editing or actions on the home page

## Responsive Layout

- Desktop (>768px): 3 cards top row + 2 cards bottom row (as above)
- Mobile (<768px): all 5 cards stack vertically

## Acceptance Criteria for UX

- 5 data cards rendered on home page load
- Each card with correct source endpoint
- Colour coding on Portfolio Heat card (green/amber/red)
- All 5 cards clickable with correct navigation targets
- Partial failure: individual card error without breaking others
- Responsive layout per above
