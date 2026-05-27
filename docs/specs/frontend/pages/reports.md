# reports.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.3
**Last Updated:** 2026-05-27
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source (v2.1 PDF export):** docs/design/2026-03-18__release-v2.1/pdf-export/ux_spec.md

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

### Page Header Controls

The page header contains two controls, right-aligned:

1. **Year Selector** (left) — dropdown for selecting the UK tax year (see Year Selector section below)
2. **"Download PDF"** button (right) — secondary button style; triggers server-side PDF generation

Layout (left to right): `[Year Selector ▼]  [Download PDF]`

On narrow screens: stacked vertically — year selector above, Download PDF button below (full width).

#### Download PDF Button States

| State | Label | Behaviour |
|-------|-------|-----------|
| Idle | **"Download PDF"** (with download icon) | Enabled when page loaded successfully |
| Generating | **"Generating…"** (spinner replaces icon) | Button disabled; fires `GET /reports/tax-year?format=pdf&year=YYYY` |
| Success | Returns to Idle | Browser file download begins; no success toast required |
| Error | Returns to Idle | Toast notification: `"PDF generation failed. Please try again."` (auto-dismiss 5s) |

The PDF is valid for empty years (zero closed trades). The button is always enabled once the page loads.

---

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

### Arc 5 Compliance Summary

Displayed below the Unrealised P&L Card. This section is collapsible and **collapsed by default**.

**Data source:** `GET /analytics/arc5-compliance`

When the composite score formula is available (per `docs/specs/metrics_definitions.md` §Arc 5 Compliance Composite Score), the computed `composite_score` is displayed as the headline metric.

When the composite score is unavailable (null API inputs), individual metric components are displayed instead.

#### Fields Displayed

| Field | Source | Label | Notes |
|-------|--------|-------|-------|
| `composite_score` | Computed (formula) | **Compliance Score** | Displayed as percentage if formula inputs available; "N/A" otherwise |
| `events_per_week` | `data.events_per_week` | Red Flag Events/Week | Float |
| `override_rate` | `data.override_rate` | Override Rate | Percentage |
| `validation_pass_rate_by_rule` (top 3) | `data.validation_pass_rate_by_rule` | Top Rule Pass Rates | Top 3 rules by fail rate; displayed as list |
| `top_rule_breach` | `data.top_rule_breach` | Top Rule Breach | Rule type label; null → "None" |

#### Rendering Conditions

- Section header: **"Arc 5 Signal Compliance"**
- Collapsed by default; user can expand with a chevron toggle
- Loading state: skeleton placeholder while `GET /analytics/arc5-compliance` is pending
- Error state: "Unable to load compliance data" if API returns error
- Empty state (no data): display "No compliance data recorded yet"

#### Sign-off

- **Financial Reporting & Records Owner:** agent-mediated sign-off cleared 2026-05-27 (ST-08, EPIC-03, v4.1)
- **Product Owner:** agent-mediated sign-off cleared 2026-05-27 (ST-08, EPIC-03, v4.1)

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

- **Endpoint:** `GET /reports/tax-year?year=YYYY` — page data
- **PDF export:** `GET /reports/tax-year?format=pdf&year=YYYY` — server-side PDF download (`Content-Disposition: attachment`)
- **CSV export:** `GET /reports/tax-year?format=csv&year=YYYY` — CSV download (ST-13; no UI control beyond API — URL parameter only; no button on this page)
- **Canonical contract:** `docs/specs/api_contracts/reports_endpoints.md`

All values displayed on this page are sourced from the API response. The frontend must not recalculate P&L, FX conversions, or fee adjustments.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.3 | 2026-05-27 | v4.1 Arc 5 P&L integration (ST-08, BLG-FEAT-42): Arc 5 Compliance Summary section added — collapsible, collapsed by default, data from GET /analytics/arc5-compliance, composite score or individual metrics per FEAT-40 formula availability. Financial Reporting & Records Owner + Product Owner agent-mediated sign-off cleared. |
| 0.2 | 2026-03-18 | v2.1 PDF export (ST-12, BLG-FR-01): Page Header Controls section added with Download PDF button spec (idle, generating, success, error states). API Reference updated to include PDF and CSV export endpoints. Design source: docs/design/2026-03-18__release-v2.1/pdf-export/ux_spec.md. Design gate: 2026-03-18__release-v2.1. |
| 0.1 | 2026-03-17 | Initial spec. ST-05 — EPIC-02 (4.1b Tax-Year P&L Statement). Design gate: 2026-03-17__release-v2.0. Approved by Head of UX & Design + Product Owner. |
