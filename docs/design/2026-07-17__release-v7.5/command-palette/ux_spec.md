**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-17
**Approved by:** Product Owner — 2026-07-17
**Story:** ST-01 — Global Cmd/Ctrl-K command palette (EPIC-01, BLG-FE-115)
**Depends on:** `docs/specs/blg_fe_115_pre_implementation_readiness_pass.md` — this artefact assumes that readiness pass's index scope, keyboard contract, and `cmdk` dependency-gap findings as its technical baseline
**Cycle:** 2026-07-17__release-v7.5

---

# UX Specification — Global Command Palette

## 1. Context

The app has 20 routes (`src/pages.config.js`) and no cross-page search — a user on Watchlist who wants to jump to a specific trade plan or the Settings page must use the sidebar, which requires knowing (or scanning for) the destination. The readiness pass (`blg_fe_115...md`) confirmed the UI primitives already exist (`src/components/ui/command.js` wraps `cmdk`) but the dependency itself is not installed and no palette is wired up. This spec defines the palette's visible behaviour; the readiness pass remains authoritative for the index-source and keyboard-contract technical detail.

## 2. Decision

### 2.1 Invocation (AC-01)

Two invocation paths, per readiness pass AC-03 (discoverability):

- **Keyboard:** `Cmd+K` (macOS) / `Ctrl+K` (Windows/Linux), global — fires from any page, any time focus is not inside a text input/textarea/select.
- **Mouse fallback:** a search-icon button in the top nav bar header region (`Layout.js`), showing a muted `⌘K` / `Ctrl K` badge hint. Clicking it opens the palette identically to the keyboard shortcut. This satisfies accessibility parity — the feature is not keyboard-only.

### 2.2 Palette Surface

Renders as a centred modal overlay (reuses the project's shared `Dialog` component per `command.js`), consistent with existing modal treatment elsewhere in the app (Add Ticker modal, position entry modal). Contains:

- A single text input at the top, placeholder: `"Search pages, tickers, trade plans…"`, autofocused on open.
- A scrollable results list below, grouped by category (see §2.3).

### 2.3 Result Categories & Ranking

Two groups, rendered in this order when the input is non-empty:

| Group | Label | Source |
|-------|-------|--------|
| Pages | "Pages" | Static index from `pages.config.js` `PAGES` (per readiness pass AC-01) |
| Tickers & Plans | "Your Data" | Dynamic index — tickers/positions/trade plans already loaded client-side (open positions, watchlist, trade plans) |

Within each group, results are ordered by `cmdk`'s built-in fuzzy-match relevance (no custom ranking). A page-name match and a ticker match can both appear simultaneously (e.g. typing "AAPL" surfaces the ticker under "Your Data"; typing "trade" surfaces "Trade Plans" and "Trade History" under "Pages").

**Empty input state:** shows a small set of recent/frequent pages (top-level nav items) with no "Your Data" group — avoids dumping the full ticker list on open.

### 2.4 Selecting a Result (AC-02, AC-03)

- **Page result:** navigates via `useNavigate` to that page's route; palette closes.
- **Ticker/plan result:** navigates to the most relevant surface for that entity — an open position navigates to `/positions` (scrolled/highlighted if the page supports it, otherwise just the page); a watchlist ticker navigates to `/watchlist`; a trade plan navigates to `/trade-plans/{id}` detail view directly (not the list) since the plan ID is already known.
- **Keyboard:** Arrow Up/Down moves the highlighted result; `Enter` selects the highlighted result; `Escape` closes the palette without navigating.
- **Mouse:** clicking any result selects it identically to `Enter`.

### 2.5 No Results

When the typed query matches nothing in either group: `CommandEmpty` renders "No results for '{query}'." — per readiness pass AC-06, this is a new compact-list `DataState` variant (not the existing card-oriented default), since the existing `py-16` default would look oversized inside the palette's compact list. This new variant is added to `design_system.md` in the same commit as the implementation (Frontend Specs owner responsibility, not this artefact).

## 3. §13 Compliance

Pure navigation aid — no trade, position, or data-mutation action is reachable from the palette. All results route to existing read views; nothing here creates, edits, or executes anything. Not a §13-relevant feature.

## 4. States

| State | Behaviour |
|-------|-----------|
| Closed | No DOM overlay present |
| Open, empty input | Recent/frequent pages shown, no "Your Data" group |
| Open, typing | Both groups filtered live, fuzzy match |
| Open, no matches | Compact empty state: "No results for '{query}'." |
| Result highlighted (keyboard) | Highlighted row visually distinct; `Enter` navigates |
| Result selected | Palette closes; app navigates to target route |

## 5. Discoverability (per readiness pass AC-03)

First-session-only dismissible tooltip pointing at the nav-bar search affordance, using the project's existing tooltip/toast primitive. No modal product-tour interrupt.

## 6. Sign-off

- **Head of UX & Design:** Confirmed — 2026-07-17
- **Product Owner:** Approved — 2026-07-17
