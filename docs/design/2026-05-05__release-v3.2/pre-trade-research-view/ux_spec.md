**Owner:** Head of UX & Design
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-05
**Cycle:** 2026-05-05__release-v3.2
**Approved by:** Product Owner — 2026-05-05
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# UX Spec — Pre-Trade Research View (EPIC-01: ST-01, ST-02, ST-03)

## Purpose

This document defines the layout, component regions, interaction model, and design decisions for the Pre-Trade Research View introduced in v3.2 (PT-02 + PT-03). It is the authoritative design source for `docs/specs/frontend/pages/pre_trade_research.md`.

---

## Route and Entry Points

- **Route:** `/research/{ticker}`
- **Entry points:** screener results "Research" button; watchlist "Research" button (see screener-to-research-navigation UX spec)
- **URL structure:** ticker in path (not query param) — shareable and bookmarkable

---

## Page Layout

```
┌──────────────────────────────────────────────────────────┐
│  [← Back]    AAPL — Apple Inc.                          │
│  Technology · Market Cap: $3.2T · Last updated: 2m ago  │
├──────────────────────────────────────────────────────────┤
│  PRICE & SIGNAL                                          │
│  $182.50  ▲ +1.2%  │  Signal: Active (green)            │
│  ATR: $4.20                                              │
├──────────────────────────────────────────────────────────┤
│  PROSPECTIVE HEAT AT ENTRY                               │
│  Current portfolio heat: 12%                             │
│  Heat if entered (est. qty): 16%  ← colour-coded band   │
├──────────────────────────────────────────────────────────┤
│  TRADE PLAN                                              │
│  [if exists] Status · Stop · Notes summary               │
│  [if absent] "Create Trade Plan" CTA                     │
├──────────────────────────────────────────────────────────┤
│  RECENT NEWS                                             │
│  • Headline 1 — Source · 2h ago                         │
│  • Headline 2 — Source · 4h ago                         │
└──────────────────────────────────────────────────────────┘
```

---

## Region Specifications

### 1. Page Header

- Back navigation link: `← Back` — returns to the referring page (screener or watchlist). Browser back is the mechanism — no custom scroll-position state required.
- Ticker symbol: large, uppercase, bold
- Company name: subtitle level, plain weight
- Sector, market cap: metadata row below ticker/name (render `—` for null values)
- "Last updated" timestamp: derived from API response timestamp

### 2. Price & Signal Region

| Element | Source | Display |
|---------|--------|---------|
| Current price | `GET /research/{ticker}` | Formatted in native currency |
| Price change | `GET /research/{ticker}` | `▲ +X.X%` in green or `▼ -X.X%` in red |
| Momentum signal | `GET /research/{ticker}` | Badge: `Active` (green) / `Watch` (amber) / `No Signal` (grey) — matches watchlist signal badge conventions |
| ATR (14d) | `GET /research/{ticker}` | Formatted with currency symbol |

### 3. Prospective Heat at Entry Region (ST-03)

Displayed below Price & Signal. Calls `GET /portfolio/prospective-heat` with the researched ticker and a default quantity parameter.

| Element | Display |
|---------|---------|
| Current portfolio heat | Shows the user's existing portfolio heat percentage |
| Prospective heat if entered | Shows estimated heat with the new position; colour-coded: green (<15%), amber (15–25%), red (>25%) |
| Heat label | "Prospective heat at entry" — explicit label required |
| Unavailable state | Show "N/A" for prospective heat value if endpoint returns error; do not block the rest of the view |

**Colour bands:** Align with existing portfolio heat display conventions on the dashboard/positions pages. Same green/amber/red thresholds.

**Default quantity:** Use the minimum standard position size (1 unit / 1 share) if no quantity context is available from the entry point. The intent is to show relative heat, not a precise projection.

### 4. Trade Plan Context Panel (ST-02)

Conditional display based on whether an active or draft trade plan exists for the ticker.

**If a plan exists:**
- Panel heading: "Trade Plan"
- Show: plan status badge, stop level (formatted), risk/reward notes summary (first 100 chars if long), "View full plan" link
- Panel is read-only in this view — no inline editing
- Data source: `GET /trade-plans?ticker={ticker}` filtered to the most recent active/draft plan

**If no plan exists:**
- Panel heading: "Trade Plan"
- Body: "No trade plan for {TICKER}."
- CTA: "Create Trade Plan" button — links to `/trade-plans/new?ticker={ticker}`

### 5. Recent News Region

- Show up to 5 recent news headlines from the `GET /research/{ticker}` response
- Per headline: headline text + source name + relative timestamp ("2 hours ago")
- No sentiment labels or scores (per BLG-GOV-16 §13 precedent)
- Empty state: "No recent news available."

---

## States

| State | Behaviour |
|-------|-----------|
| Loading | Show skeleton placeholders for all four regions; page header visible immediately |
| Error (research endpoint) | Full-page error: "Unable to load research data. Please try again." with Retry button |
| Partial error (prospective heat) | Show "N/A" for heat region only; rest of page renders normally |
| Partial error (trade plan) | Treat as "no plan" — show "Create Trade Plan" CTA; do not block page |

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Ticker in URL path (not query param) | Bookmarkable and shareable; consistent with v3.1 screener and watchlist routing patterns |
| Prospective heat uses default quantity | Users at the research stage have not decided on quantity; a relative heat indicator is more useful than a blank |
| Trade plan panel is read-only | The research view is a discovery context — editing belongs in the Trade Plan form |
| Back navigation via browser back | No custom scroll-state management; back from research returns to previous page naturally |
| News capped at 5 headlines | Sufficient for morning routine; keeps the page focused on research signals not news browsing |

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-05 | Initial design gate artefact for v3.2 EPIC-01 (ST-01, ST-02, ST-03). Approved by Product Owner 2026-05-05. |
