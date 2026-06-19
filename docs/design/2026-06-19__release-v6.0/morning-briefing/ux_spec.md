**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Date:** 2026-06-19
**Approved by:** Product Owner — 2026-06-19
**Cycle:** 2026-06-19__release-v6.0
**Story:** ST-02 (EPIC-02)

---

# UX Spec — Trader's Morning Briefing Dashboard Section (ST-02)

## Purpose

Provide a single at-a-glance "start of day" intelligence summary at the top of the Dashboard Homepage. Five tightly scoped cards surface the most action-relevant signals a trader needs before the market opens: new screener hits, positions requiring attention, recent red flags, upcoming earnings, and current compliance standing.

## Placement

- Position: above the existing five session-summary cards in `DashboardHome.js`
- Full-width section with a labelled section header
- Section header: **"Trader's Morning Briefing"** (left-aligned, subtle secondary text weight — not a heading-level call-out)
- Section is always visible; not collapsible

## Layout

### Desktop (> 768px)

Five cards in a single horizontal row:

```
[ Screener Hits ] [ Positions to Act On ] [ Red Flags ] [ Earnings Alert ] [ Compliance ]
```

Equal-width cards, consistent card height. Same card shell as the existing dashboard cards (border, padding, hover affordance).

### Mobile (≤ 768px)

Cards stack vertically in order:
1. Screener Hits
2. Positions to Act On
3. Red Flags
4. Earnings Alert
5. Compliance

---

## Card Specifications

### Card 1 — Screener Hits

| Attribute | Specification |
|-----------|---------------|
| Label | "Screener Hits" |
| Primary metric | Count of new screener hits since last page visit (integer) |
| Sub-label | "since your last visit" |
| Empty state | "No new hits" |
| Data source | `GET /screener/results` — count of results newer than `last_visit_utc` (backend tracks per user) |
| Click target | `/screener` |

### Card 2 — Positions to Act On

| Attribute | Specification |
|-----------|---------------|
| Label | "Positions to Act On" |
| Primary metric | Count of positions in `EXIT_ZONE` or `GRACE_PERIOD` state (integer) |
| Sub-label | List of up to 3 tickers with their state + days-in-state: e.g. "AAPL EXIT_ZONE (2d) · MSFT GRACE (1d)"; overflow: "+N more" link |
| Empty state | "All clear" |
| Data source | `GET /positions` filtered by state in [EXIT_ZONE, GRACE_PERIOD] |
| Click target | `/positions` |

### Card 3 — Red Flags

| Attribute | Specification |
|-----------|---------------|
| Label | "Red Flags" |
| Primary metric | Count of new red flag events since last weekly digest (integer) |
| Sub-label | "since last digest" |
| Empty state | "No new red flags" |
| Data source | `GET /portfolio/red-flag-journal` — count of events with `event_date` after last digest date |
| Click target | `/red-flag-journal` |

### Card 4 — Earnings Alert

| Attribute | Specification |
|-----------|---------------|
| Label | "Earnings Alert" |
| Primary metric | Count of watchlisted or open-position tickers with earnings in the next 7 calendar days (integer) |
| Sub-label | Up to 2 ticker symbols: "AAPL (Mon) · NVDA (Wed)"; overflow: "+N more" |
| Empty state | "No earnings this week" |
| Data source | `GET /earnings/{ticker}` for each watchlisted/open-position ticker — engine filters to next 7 days |
| Click target | Earnings calendar page or `/watchlist` (engineering to confirm; document in spec update if endpoint confirmed) |

### Card 5 — Compliance

| Attribute | Specification |
|-----------|---------------|
| Label | "Compliance" |
| Primary metric | Current Arc 5 compliance score (integer or percentage) |
| Sub-label | Trend arrow: ↑ (up vs prior week), ↓ (down vs prior week), → (flat ±0); trend label: "vs last week" |
| Data source | `GET /analytics/arc5-compliance` |
| Click target | `/analytics` (PerformanceAnalytics) |
| Colour coding | Score ≥ 80%: green; 60–79%: amber; < 60%: red |

---

## Shared Card Behaviour

| Behaviour | Specification |
|-----------|---------------|
| Loading state | Skeleton placeholder (same height as loaded card); no spinner overlay on section |
| Error state | Card shows "Unable to load" in muted text; other cards render normally |
| Click affordance | Entire card surface is clickable; hover: subtle border highlight or shadow lift (consistent with existing cards) |
| Empty state | Each card has a defined empty-state message (see above); empty is valid — never show "0" as an error state |

---

## §13 Compliance

All cards are display-only aggregations of existing live data. No automated recommendations or decisions. No AI-generated content. Fully compliant with strategy_rules.md §13.

## Playwright Test Scenarios

- **SC-MB-01a**: Morning Briefing section renders above existing dashboard cards on page load
- **SC-MB-01b**: Screener Hits card renders with count and sub-label; click navigates to /screener
- **SC-MB-01c**: Positions to Act On card shows empty state ("All clear") when no EXIT_ZONE or GRACE_PERIOD positions exist
- **SC-MB-01d**: Positions to Act On card shows ticker list when positions exist
- **SC-MB-01e**: Red Flags card renders with count; click navigates to /red-flag-journal
- **SC-MB-01f**: Earnings Alert card renders with count; empty state when no earnings in 7 days
- **SC-MB-01g**: Compliance card renders score and trend arrow
- **SC-MB-01h**: Mobile (≤ 768px): cards stack vertically in specified order
- **SC-MB-01i**: Individual card error (mocked 500) does not break other cards
