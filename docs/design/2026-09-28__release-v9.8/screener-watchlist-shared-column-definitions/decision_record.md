**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-28__release-v9.8
**Story:** ST-02 (EPIC-01, BLG-FE-185)

# Decision Record — Screener/Watchlist Table Body Cells Driven from the Shared Column Definitions

## 1. Problem

`SCREENER_COLUMNS` (`src/pages/Screener.js`) and `WATCHLIST_COLUMNS` (`src/components/watchlist/WatchlistTable.js`) already act as the single source of truth for table headers and CSV export (established at the v9.6 CSV export story, `docs/design/2026-09-21__release-v9.6/screener-watchlist-csv-export/decision_record.md`), but table body cells are still rendered by separate, hand-written JSX per column — a third, independently-maintained path that can drift from the header/CSV definitions.

## 2. Decision

No new visual design. Body cells are re-pointed to read their render logic from the same `SCREENER_COLUMNS`/`WATCHLIST_COLUMNS` definitions already governing header and CSV, so there is exactly one definition per column instead of three. Rendered output (text, formatting, colour, layout) must be pixel-identical to today's — this is an internal single-source-of-truth refactor, not a redesign. The existing Screener/Watchlist Playwright specs passing unchanged is itself evidence the visual contract held.

## 3. §13 Compliance

Not applicable — no AI call.

## 4. Frontend Spec Impact

`screener_results.md` gains a short §Column Definition Architecture note (precedent: v1.5's §10 loading-skeleton pattern note) recording that header, body cell and CSV value for every column derive from one definition (`SCREENER_COLUMNS`), so a future change to one path doesn't silently diverge from the others. `watchlist.md` gains the equivalent note for `WATCHLIST_COLUMNS`. No rendering behaviour documented elsewhere in either spec changes.

## 5. Testability (CLAUDE.md §2)

Existing Screener/Watchlist Playwright specs re-run unchanged (slice AC) plus the standard frontend-visible-change Playwright requirement — both satisfied by the "no visual change" nature of this refactor; a spec failure here is itself the regression signal.

## 6. Approval

Head of UX & Design: confirmed, 2026-09-28.
Product Owner: confirmed, 2026-09-28.
