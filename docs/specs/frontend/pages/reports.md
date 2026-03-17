# reports.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.1
**Last Updated:** 2026-03-17
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

## Purpose & User Goals

The Reports page provides a structured, tax-year-scoped view of a user's realised trading P&L. It is a financial reference record — not an analytics view. Users access it to understand their gains and losses within a specific UK tax year for personal record-keeping and tax reference purposes.

Users should be able to:
- Select a UK tax year and see all closed trades attributed to that year
- See a summary of total realised P&L, gross profit, gross loss, and win rate for the year
- Review each individual trade's contribution to the year's P&L
- See an indicative unrealised P&L for currently open positions (clearly distinguished from realised figures)
- Understand the limitations of the data before using it for tax purposes

> **Disclaimer (displayed on page):** This report is provided for user reference only. It is not a substitute for qualified tax advice. Users are responsible for verifying figures against their broker records and obtaining appropriate professional advice before submitting any tax return.

---

## Page Layout

### Disclaimer Banner

A prominent banner at the top of the page displays the disclaimer above verbatim. The banner must be visible without scrolling.

---

### Year Selector

- A dropdown control for selecting the UK tax year
- Label format: `"2025/26"`, `"2024/25"`, etc. — matching `tax_year_label` from the API response
- Default: the current UK tax year (the tax year whose `tax_year_start` is on or before today's date)
- Future years are disabled (the backend returns 400 for future years; the frontend must not allow their selection)
- On year change: triggers a new `GET /reports/tax-year?year=YYYY` request and re-renders the page
- The selected `year` value is the start year of the UK tax year (e.g. `2025` for "2025/26")

---

### Summary Bar

Displayed below the year selector. Sourced from the `summary` object in the API response.

| Field | Label | Notes |
|-------|-------|-------|
| `total_realised_pnl` | Total Realised P&L | GBP. Green if positive, red if negative. |
| `total_gross_profit` | Gross Profit | GBP. Always ≥ 0. |
| `total_gross_loss` | Gross Loss | GBP. Always ≤ 0. |
| `win_rate` | Win Rate | Percentage. |
| `total_closed_trades` | Trades | Integer count. |

All values are sourced directly from the API response. The frontend must not calculate or derive these figures.

---

### Trades Table

Displays the `trades[]` array from the API response. One row per trade.

| Column | Field | Notes |
|--------|-------|-------|
| Ticker | `ticker` | |
| Market | `market` | "UK" or "US" badge |
| Entry Date | `entry_date` | YYYY-MM-DD |
| Exit Date | `exit_date` | YYYY-MM-DD |
| Holding Days | `holding_days` | Integer |
| Entry Price | `entry_price_native` | Native currency |
| Exit Price | `exit_price_native` | Native currency |
| Shares | `shares` | Decimal |
| Total Cost | `total_cost_gbp` | GBP |
| Exit Proceeds | `exit_proceeds_gbp` | GBP |
| Realised P&L | `realised_pnl_gbp` | GBP. Colour-coded: green if positive, red if negative or zero. |
| P&L % | `pnl_pct` | Percentage |
| Tags | `tags` | Displayed as tag pills; empty if none |

**FX rates:** `entry_fx_rate` and `exit_fx_rate` are available for US trades (`null` for UK trades). These may be shown as a tooltip or in an expandable column — not required as primary columns.

**Sorting:** Default sort by `exit_date` ascending. User may sort by any column.

**Currency indicator:** The native currency (`currency` field) is shown alongside entry/exit prices to disambiguate GBP vs USD values.

---

### Unrealised P&L Card

Displayed below the trades table, clearly separated from the realised section.

- Shows `estimated_unrealised_pnl` (GBP) — the sum of `pnl` across all currently open positions
- Displays the full `unrealised_note` text from the API response verbatim
- Card header: **"Indicative Unrealised P&L (current positions)"**
- Must be visually distinct from the realised summary bar — users must not mistake this figure for a tax-year-scoped value

---

### Empty State

When `trades[]` is empty (no closed trades in the selected tax year):

> "No closed trades recorded for the [tax_year_label] tax year."

The summary bar still renders with zero values. The unrealised P&L card still renders if `estimated_unrealised_pnl` is non-zero.

---

### Scope Note

A note at the bottom of the page:

> "UK tax year only (6 April to 5 April). Verify all figures against your broker records and seek qualified tax advice before filing."

---

## API Reference

- **Endpoint:** `GET /reports/tax-year?year=YYYY`
- **Canonical contract:** `docs/specs/api_contracts/reports_endpoints.md`

All values displayed on this page are sourced from the API response. The frontend must not recalculate P&L, FX conversions, or fee adjustments.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-17 | Initial spec. ST-05 — EPIC-02 (4.1b Tax-Year P&L Statement). Design gate: 2026-03-17__release-v2.0. Approved by Head of UX & Design + Product Owner. |
