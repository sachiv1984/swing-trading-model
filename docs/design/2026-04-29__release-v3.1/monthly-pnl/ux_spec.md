**Version:** 1.0
**Date:** 2026-04-29
**Author:** Head of UX & Design
**Approved by:** Product Owner — 2026-04-29
**Story:** ST-11 — Monthly P&L summary report (BLG-FEAT-19)
**Design gate:** 2026-04-29__release-v3.1

---

# UX Decision Record — Monthly P&L Summary Report (ST-11)

## Purpose

The existing Reports page is tax-year-scoped and trade-level. The Monthly P&L breakdown gives the user a higher-level summary: how each calendar month performed, enabling trend identification and planning.

---

## Placement Decision

**Decision:** The Monthly Breakdown is a new section appended **below the Unrealised P&L Card** on the existing Reports page.

- It is always visible (not collapsible), positioned as the last section on the page.
- It is not filtered by the tax year selector — it shows a rolling 12-month window of data (current month + prior 11 months) regardless of which tax year is selected.
- Rationale: monthly breakdown is a different lens from tax-year (calendar months vs. tax years do not align). Tying it to the year selector would produce confusing partial-month data at tax-year boundaries.

---

## Section Layout

### Section Header

**Label:** "Monthly Breakdown"

Sub-label (smaller, muted): "Last 12 months — realised trades only"

---

### Monthly Breakdown Table

| Column | Source | Notes |
|--------|--------|-------|
| Month | `year`+`month` from response | Formatted as "Apr 2026", "Mar 2026", etc. (abbreviated month name + year). Sorted descending (most recent first). |
| Realised P&L | `realised_pnl_gbp` | GBP. Colour-coded: green if positive, red if negative, muted if zero. |
| Trades | `trade_count` | Integer. "0" shown as muted `—`. |

- Column count: 3. No additional columns.
- No sorting controls — rows are always descending by date.
- No pagination — all 12 rows displayed.

### Empty State

When `realised_pnl_gbp` is 0 and `trade_count` is 0 for a given month: the row is still shown (with `—` for trades and `£0.00` muted for P&L). The table always shows all 12 months, even if some months have zero activity.

If the feature is loaded and `GET /reports/monthly-pnl` returns an empty array: show the section header with the message: `"No closed trades in the last 12 months."` (no table rendered).

---

## API

- **Endpoint:** `GET /reports/monthly-pnl`
- **Response:** `[{ year, month, realised_pnl_gbp, trade_count }]` sorted descending
- The frontend renders exactly what the API returns; it must not filter, aggregate, or re-sort.

---

## Loading State

While `GET /reports/monthly-pnl` is loading: show a skeleton table (12 skeleton rows, same column layout).

---

## Error State

If the endpoint fails: show inline error within the section: `"Unable to load monthly breakdown. Please refresh."` No retry button required (page-level refresh suffices).

---

## Scope Constraints

- Monthly data covers **realised P&L only** (closed trades). Open position P&L is excluded.
- The section is display-only. No PDF or CSV export for the monthly breakdown in v3.1.
- Currency: GBP only. No native currency breakdown.

---

## Spec Update Required

`docs/specs/frontend/pages/reports.md`: add Monthly Breakdown section documenting placement, table columns, empty/loading/error states, and API reference.
