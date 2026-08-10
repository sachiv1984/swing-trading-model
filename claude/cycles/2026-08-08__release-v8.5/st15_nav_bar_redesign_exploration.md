**Owner:** Head of UX & Design
**Class:** Design Exploration (Class 4)
**Status:** Complete
**Last Updated:** 2026-08-10

# Nav Bar Redesign Exploration (ST-15)

## Problem

The current nav bar occupies a fixed portion of the visible screen area. As the application grows in Arc 2 and beyond, the navigation structure may benefit from a redesign to reclaim vertical space. Three patterns were named for evaluation: **Sticky/Fixed Header** (current pattern, optimised), **mega menu** (grouped sections), **breadcrumb navigation** (context-sensitive, minimal footprint).

## Current State (evaluated directly against the live implementation)

- **Structure:** left sidebar, 4 collapsible groups (Trading — 4 items, Analytics — 3, Tools — 1, System — 4) + a top-level `DashboardHome` link outside any group. `docs/specs/frontend/pages/navigation.md` §Group Structure is the canonical spec.
- **Collapse behaviour:** only the active group is expanded by default; all others start collapsed and persist their state per-session (`sessionStorage`) — the sidebar does not show all 13 nav items' full label+icon rows simultaneously except when a user deliberately expands every group.
- **Screen real-estate impact:**
  - Desktop (`lg:` breakpoint+): fixed `w-64` (256px) sidebar, permanently visible (`src/Layout.js:570`).
  - Mobile/tablet (below `lg:`): **zero persistent footprint** — the nav is an off-canvas slide-in drawer (`w-72`, `fixed`, toggled by a hamburger button), not a fixed on-screen element (`src/Layout.js:486-527`). The real-estate concern named in the problem statement does not apply below the `lg:` breakpoint at all in the current implementation.
- **Escape valve already in place:** the global command palette (`Cmd+K`/`Ctrl+K`, `docs/specs/frontend/pages/navigation.md` §Global Command Palette, shipped v7.5) gives one-keystroke access to any page or in-app record (open position, watchlist ticker, trade plan) without touching the sidebar at all — this substantially reduces the practical cost of a fixed sidebar, since power users are not required to visually scan or click through it.
- **Page inventory (Arc 2+ page count):** `src/pages.config.js` registers 20 total pages. Of those, 13 have a persistent nav entry (`DashboardHome` + 12 grouped items); the remaining 7 (`Dashboard` legacy alias, `Reports`, `TradeEntry`, `Screener`, `TradePlan`, `TradePlans` detail, `TickerUniverse`, `StrategyBenchmark`) are reached via contextual links from other pages or the command palette, not the sidebar — the sidebar was already curated down to the pages that benefit from always-on discoverability, not a flat list of every route.

## Evaluation

| Pattern | Screen real-estate impact | Mobile responsiveness | Arc 2+ page count fit |
|---------|---------------------------|------------------------|-------------------------|
| **Sticky/Fixed Header (current)** | 256px fixed on desktop only; 0px on mobile (off-canvas). Collapsible groups already keep the visible list short (avg. ~4 rows expanded, not 13). | Already optimal — off-canvas drawer, no persistent footprint. | 13 curated nav items across 4 groups scales comfortably; command palette absorbs the long tail (7 pages) without adding sidebar rows. A pattern already designed to scale past today's 20-page inventory. |
| **Mega menu** | Would trade the persistent 256px sidebar for a dropdown/flyout that only occupies space while open — real desktop-space win. But mega menus earn their complexity at page counts well beyond today's 20 (typically 50+ with deep category trees); at 13 curated items in 4 groups, a mega menu adds interaction cost (hover/click-to-reveal every navigation) without a proportionate space payoff, and would require rebuilding a component with no existing equivalent in the design system. | Mega menus commonly degrade on mobile to... an off-canvas drawer — i.e., converging back to what already exists today. | Would be justified only if page count materially grows past the current curated set; not yet, and the command palette already absorbs long-tail growth without sidebar changes. |
| **Breadcrumb navigation** | Smallest footprint (a single header row), but breadcrumbs are a *complement* to primary navigation, not a *replacement* — they show "where am I" within a hierarchy, not "where can I go". This app's page set is largely flat (not deeply nested), so breadcrumbs would add a thin header row without removing the need for a way to actually navigate between top-level sections. | No inherent mobile benefit — would still need a separate mechanism (which converges back to a sidebar/drawer or the command palette) for actual cross-page navigation. | Doesn't address the stated problem (reclaiming space from the *navigation* mechanism) since it isn't a substitute for one. |

## Recommendation

**Maintain current pattern (Sticky/Fixed Header, i.e. the collapsible-group left sidebar).** It already reclaims the real-estate cost that motivated this exploration on the one surface where it matters most (mobile, via the off-canvas drawer), keeps the visible desktop footprint modest through per-session collapse state, and pairs with a command palette that absorbs navigational scale independent of sidebar structure. Neither alternative pattern offers a real-estate or scalability win large enough to justify a redesign and its migration cost at the current 20-page inventory. Revisit if/when the page inventory grows substantially past today's curated 13-item sidebar (e.g. a new Arc adds 10+ pages warranting their own top-level group), at which point a mega-menu re-evaluation would have a stronger real-estate case.

No implementation follow-on filed — per this story's own AC, a UX spec and implementation backlog item are only required if redesign is recommended.

**Design gate note:** Design Not Applicable for this cycle (no live UI change) — this document is the deliverable in full; confirmed in `design_gate.md` Notes for this sprint.

## Sign-off

- Reviewed by: Head of UX & Design (agent-mediated, per `execution_prompt.md` §5.3)
- Date: 2026-08-10
