**Version:** 1.0
**Date:** 2026-04-29
**Author:** Head of UX & Design
**Approved by:** Product Owner — 2026-04-29
**Story:** ST-06 — Fix screener UK ticker display and watchlist promotion
**Design gate:** 2026-04-29__release-v3.1

---

# UX Decision Record — UK Ticker Display Fix (ST-06)

## Problem

UK tickers sourced from the London Stock Exchange carry a `.L` suffix in their raw symbol (e.g. `BARC.L`, `TSCO.L`). This suffix is a data-source artefact from the Yahoo Finance / yfinance data provider. It has no meaning to the user and must not appear in any displayed context.

## Decision

### Display Rule — Screener Results Table (Ticker Column)

Strip the `.L` suffix from UK ticker symbols before rendering in the Ticker column.

- Condition: `result.market === "UK"`
- Input: `BARC.L`
- Display: `BARC`
- US ticker symbols are unaffected.

### Display Rule — Watchlist Promotion Popover

Strip `.L` from the displayed ticker in the "Add X to Watchlist" confirmation popover header.

- The popover title `"Add BARC.L to Watchlist"` must render as `"Add BARC to Watchlist"`.
- Applies to both the `WatchlistPopover` header label and the "Add X to Watchlist" confirm button label.

### API Call Rule — POST /watchlist

Strip `.L` before posting to `POST /watchlist` for UK tickers. The watchlist must store and operate on the clean symbol, not the suffixed form.

- Rationale: the positions, watchlist, and trade plan systems all operate on clean symbols. Storing `.L`-suffixed symbols would create cross-system inconsistency.
- The strip must happen at the call site (`WatchlistPopover.handleAdd`) before the API call, not after.

### Font Treatment Decision — Ticker Column

Ticker symbols in the screener results table Ticker column use `font-mono` (monospace typeface).

- Rationale: financial identifiers benefit from monospace rendering for visual alignment in a data-dense table, and for visual differentiation from text labels. This aligns with ticker display conventions already present on the Positions and Watchlist pages.
- Applies to: the Ticker column cell content only. Column header remains default sans-serif.

## Spec Update Required

`docs/specs/frontend/pages/screener_results.md` must be updated:
- §4 Column Layout: document UK ticker `.L` stripping rule and `font-mono` treatment
- §8 Watchlist Promotion: document `.L` stripping in popover label and API call

## Constraints

- US ticker display is entirely unaffected.
- The raw `.L`-suffixed symbol is retained in backend data; stripping is display-layer only (except for `POST /watchlist` where the clean symbol must be sent).
- No new visual component or layout change required.
