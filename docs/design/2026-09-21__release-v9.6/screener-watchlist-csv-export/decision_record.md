**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-21__release-v9.6
**Story:** ST-03 (EPIC-01, BLG-FEAT-97)

# Decision Record — CSV Export for Screener Results and Watchlist

## 1. Problem

Reports and Trade History export CSV; Screener and Watchlist do not, so ranked candidates cannot leave the app. The Reports page already has an approved CSV button pattern (`reports.md` §Download CSV Button States) that should be reused, not reinvented.

## 2. Decision

### 2.1 Control

A secondary (outline) button labelled **"Download CSV"** with the download icon — the **same label and weight as Reports' button** for consistency (the backlog's working title "Export CSV" is superseded by the established wording).

| Page | Placement |
|------|-----------|
| Screener Results | Right end of the filter bar (`screener_results.md` §5.2), after the Sector filter |
| Watchlist | Page header action group, immediately left of the primary **"+ Add Ticker"** button |

Narrow screens: the button drops below the toolbar row, full width (same rule as Reports).

### 2.2 What is exported

- **Rows:** exactly the rows currently displayed — i.e. **after** the active filters and sort (Screener: Market/Regime/Sector filters and current sort; Watchlist: its current default ordering). Watchlist row selection (bulk actions) has **no effect** on the export.
- **Columns:** the table's full column set at desktop width, in display order, **excluding the non-data columns** (the Watchlist selection checkbox and the Actions column on both pages). Responsive hiding on mobile (`screener_results.md` §4: Sector/Entry Zone hidden <768px) does **not** shrink the export — the export is viewport-independent.
- **Single source of truth:** each table's column list must be defined once (an array of `{ header, value }`) and consumed by *both* the table renderer and the CSV builder, so the two cannot drift. This is the mechanism that makes "columns equal the visible columns" hold by construction.
- **Header row:** the displayed header labels verbatim.
- **Cell values are machine-readable, not presentation-formatted:** plain numbers (no currency symbols, no thousands separators, no % signs), ISO dates (`YYYY-MM-DD`), and the label text for chip/badge columns (e.g. `Risk On`, `Active`). Screener `Signal` exports the raw 0.0–1.0 score.

Screener columns: Ticker, Market, Price, ATR, Regime, Signal, Sector, Entry Zone, News. Watchlist columns: the `TABLE_HEADERS` set minus checkbox and Actions.

### 2.3 File format

UTF-8, header row, RFC 4180 quoting (fields containing comma, quote or newline are quoted, quotes doubled), `\r\n` row terminators, no BOM. Filename carries the local date: `screener-results-YYYY-MM-DD.csv`, `watchlist-YYYY-MM-DD.csv`. Generated **client-side** from already-loaded data; nothing persisted, no network call.

### 2.4 Spreadsheet-formula-injection guard

Watchlist notes and tickers are user-entered. Any **string-typed** cell beginning with `=`, `+`, `-` or `@` is prefixed with a single quote (`'`) in the file. Numeric cells (including negatives) are written as numbers and are not affected.

### 2.5 States

| State | Behaviour |
|-------|-----------|
| ≥1 displayed row | Enabled |
| 0 displayed rows (empty, loading, or everything filtered out) | **Disabled** with tooltip `"Nothing to export"` — an empty file has no value (deliberately differs from Reports, whose empty tax year is a valid document) |
| Success | Browser download begins; no success toast (matches Reports) |
| Failure (Blob/download error) | Toast `"CSV download failed. Please try again."` — Error severity, 8s (Toast Notification Timing standard) |

Generation is synchronous, so there is no "Generating…" state.

### 2.6 Motion / timing

None.

## 3. §13 Compliance

Exports data already shown on screen. No computation, ranking change or AI call. §13 pre-check does not apply.

## 4. Frontend Spec Impact

- `screener_results.md` v1.6 → v1.7: new §5.3 CSV Export.
- `watchlist.md` v0.7 → v0.8: Page Header action group gains the button; new §CSV Export.

## 5. Testability (CLAUDE.md §2)

Playwright on both pages: download fires; header row equals the rendered table headers (minus checkbox/Actions); filtered Screener view exports only filtered rows; button disabled at zero rows; a string cell starting with `=` is written with the guard prefix.

## 6. Approval

Head of UX & Design: confirmed, 2026-09-21.
Product Owner: confirmed, 2026-09-21.
