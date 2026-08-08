# reports.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.16
**Last Updated:** 2026-08-08 — v8.5 design gate: Tax Year Trades Table's exact-zero Realised P&L colour converged with the Monthly Financial Table (grey/neutral for both, was red on Tax Year), resolving DEV-REPORTS-ST01-02/BLG-FE-144 (ST-08); prior — 2026-08-07 (sprint execution: Monthly Financial Table's zero-P&L colour rule corrected to match live behaviour, ST-01); prior — 2026-08-07 (v8.4 design gate: Avg P&L/Trade column added to Monthly Financial Table, ST-01); prior history retained — see prior entries in version control
**Design Source (v0.11 monthly CSV export):** docs/design/2026-07-24__release-v7.8/monthly-csv-export/ux_spec.md
**Design Source (v0.7 CSV export + monthly realised/unrealised split):** docs/design/2026-07-12__release-v7.0/tax-year-csv-export/ux_spec.md, docs/design/2026-07-12__release-v7.0/realized-unrealized-split/ux_spec.md
**Design Source (v0.6 SI-02 gate status):** docs/design/2026-07-08__release-v6.8/si02-gate-visibility-indicator/ux_spec.md
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

The page header contains three controls, right-aligned:

1. **Year Selector** (left) — dropdown for selecting the UK tax year (see Year Selector section below)
2. **"Download PDF"** button — secondary button style; triggers server-side PDF generation
3. **"Download CSV"** button (right, v7.0 — ST-13) — secondary button style, same visual weight as PDF; triggers server-side CSV generation

Layout (left to right): `[Year Selector ▼]  [Download PDF]  [Download CSV]`

On narrow screens: stacked vertically in the same order — year selector, then PDF, then CSV (each full width).

#### Download PDF Button States

| State | Label | Behaviour |
|-------|-------|-----------|
| Idle | **"Download PDF"** (with download icon) | Enabled when page loaded successfully |
| Generating | **"Generating…"** (spinner replaces icon) | Button disabled; fires `GET /reports/tax-year?format=pdf&year=YYYY` |
| Success | Returns to Idle | Browser file download begins; no success toast required |
| Error | Returns to Idle | Toast notification: `"PDF generation failed. Please try again."` (auto-dismiss 5s) |

The PDF is valid for empty years (zero closed trades). The button is always enabled once the page loads.

#### Download CSV Button States (v7.0 — ST-13, BLG-FEAT-69)

| State | Label | Behaviour |
|-------|-------|-----------|
| Idle | **"Download CSV"** (with download icon) | Enabled when page loaded successfully |
| Generating | **"Generating…"** (spinner replaces icon) | Button disabled; fires `GET /reports/tax-year?format=csv&year=YYYY` |
| Success | Returns to Idle | Browser file download begins; no success toast required |
| Error | Returns to Idle | Toast notification: `"CSV generation failed. Please try again."` (auto-dismiss 5s) |

Valid for empty years (zero closed trades) — same rule as PDF. Button always enabled once the page loads. Exported figures must match the on-screen summary bar and monthly table exactly — no client-side recalculation. Design source: `docs/design/2026-07-12__release-v7.0/tax-year-csv-export/ux_spec.md`.

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
| Realised P&L | `realised_pnl_gbp` | GBP. Colour-coded: green if positive, red if negative, grey/neutral if exactly zero *(converged v0.16 — see Changelog; previously red-for-zero, see `DEV-REPORTS-ST01-02` resolution)* |
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
- **Colour (v0.9 — ST-06, BLG-SPEC-83):** profit `text-emerald-400`, loss `text-rose-400` — matches the Open Positions Panel P&L convention (`open-positions-panel/ux_spec.md`, v6.4), explicitly aligned rather than distinct, so the same figure reads consistently wherever it appears in the app. Design source: `docs/design/2026-07-12__release-v7.0/realized-unrealized-split/ux_spec.md`.
- **Data freshness (v0.10 — ST-06, BLG-SPEC-83):** `estimated_unrealised_pnl` reads `positions.pnl`, which is written once per night by the automatic trailing-stop ratchet (`run_nightly_trailing_stop_update()`), **not** recomputed live on each request. This is a different data path from the Positions page's Table/Grid View figures, which call `get_positions_with_prices()` and compute `pnl` fresh against the current live price on every request. The two can legitimately show different unrealised totals for the same position at the same moment — see `DEV-REPORTS-ST06-01` below.

---

### Arc 5 Compliance Summary

> **Design Only — Implementation Pending (v0.8, ST-06 reconciliation):** This section is specified but **not currently rendered** in `Reports.js`'s Tax Year P&L view. The v4.1 changelog entry below was worded as a shipped feature but ST-08 (BLG-FEAT-42)'s actual delivered scope was spec-authoring only — confirmed via `git log -S` across all history (commit `5c7d8587` touched only `metrics_definitions.md`/`reports.md`/`execution_state.json`, no `src/` files). See `BLG-SPEC-71` for full root-cause investigation. The field mappings and rendering rules below remain locked and ready to implement if/when the Product Owner schedules this as a new `BLG-FEAT` item — re-implementation effort is low since the design is already fully specified and previously signed off.

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

### SI-02 Gate Status (v0.6 — ST-06, BLG-FEAT-71)

**Design source:** `docs/design/2026-07-08__release-v6.8/si02-gate-visibility-indicator/ux_spec.md`

Displayed below "Arc 5 Compliance Summary" and above "Gross vs Net Comparison". Collapsible, collapsed by default — same pattern as Arc 5 Compliance Summary. Distinct from the Dashboard's "Gate Progress" strip (`dashboard.md` §6, single headline count only) — this section surfaces the fuller breakdown: total vs. trade-plan-linked closed trades, plus per-condition MET/NOT MET status.

**Data sources:** `GET /trades` (total closed trades), `GET /trade-plans` (trade-plan-linked closed trade count), `GET /analytics/arc5-compliance` (`trade_plan_adherence_rate` and other gate-condition inputs)

#### Fields Displayed

| Field | Source | Label | Notes |
|-------|--------|-------|-------|
| Total closed trades | `GET /trades` count | "{N} total closed trades" | |
| Linked closed trades | `GET /trade-plans` closed, `position_id` non-null count | "{N} linked to a trade plan" | Reflects ST-01 (BLG-BE-46) finding as-is, live — not suppressed or approximated if 0 |
| Gate Condition 1 (20-trade threshold) | `total closed trades >= 20` | MET / NOT MET badge | |
| Gate Condition 2 (20-linked-trade threshold) | `linked closed trades >= 20` | MET / NOT MET badge | Product-reviewed 2026-08-03 (ST-14, BLG-SPEC-72) — formalises the value the implementing engine had already used, consistent with the same 20-trade sufficiency bar used by Condition 1 and by the separate SI-02 backend readiness gate (`BLG-GOV-107`) |
| Gate Condition 3 (trade plan adherence) | `trade_plan_adherence_rate >= 0.50` | MET / NOT MET badge | Product-reviewed 2026-08-03 (ST-14, BLG-SPEC-72) — a majority of the user's closed trades must show trade-plan discipline. No prior threshold existed anywhere in the spec (`arc5_compliance_section.md` documents this metric as §13-compliant display-only, no automated threshold); 50% chosen as a meaningful "more disciplined trades than not" bar rather than the previous placeholder (`> 0`, which passed at any non-zero rate including 1%) |

**Badge style:** green "MET" pill / amber "NOT MET" pill — consistent with Dashboard gate colour treatment (`dashboard.md` §6).

#### Rendering Conditions

- Section header: **"SI-02 Gate Status"**
- Collapsed by default; user can expand with a chevron toggle
- Loading state: skeleton placeholder
- Error state: "Unable to load gate status" — does not block rest of Reports page
- Empty state (no closed trades): all counts show 0; all conditions show NOT MET

**§13 Compliance:** Display-only status readout. No automated action or recommendation.

**Playwright coverage required:** section presence/collapse, two-count display, 3-condition MET/NOT MET rendering, loading/error states (ST-06 AC-05).

---

### Gross vs Net Comparison (v6.0 — ST-03)

> **Design Only — Implementation Pending (v0.8, ST-06 reconciliation):** This section is specified but **not currently rendered** in `Reports.js`'s Tax Year P&L Summary Bar. Confirmed via `git log -S` — the v6.0 design gate commit `b8e9df34` touched only spec files, no `src/` files. ST-03 (BLG-FEAT-20, Net-of-costs)'s actual delivered scope was a "Net R column" on the **Trade History** page (`TradeHistoryTable.js`) — a real, shipped, differently-scoped feature — while this Reports-page summary row was written into the spec but never built. See `BLG-SPEC-71` for full root-cause investigation. The field mappings and rendering rules below remain locked and ready to implement if/when the Product Owner schedules this as a new `BLG-FEAT` item.

A gross vs net comparison row is shown in the Summary Bar **only when** the selected tax year's trade set contains at least one trade with cost data (`commission_gbp` or `spread_cost_gbp` non-null and non-zero).

**Placement:** New row below the Win Rate row in the summary bar.

| Metric | Gross | Net (after costs) |
|--------|-------|-------------------|
| Average R-multiple | +0.72R | +0.54R |

- "Net (after costs)" column: computed average across trades that have cost data; trades without cost data excluded from net average
- Footnote below row: _(Net figures based on N trades with brokerage cost data recorded.)_
- When no trades in the year have cost data: row is absent (no "0" placeholder)

All values sourced from API response — frontend does not calculate averages.

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
- **CSV export:** `GET /reports/tax-year?format=csv&year=YYYY` — CSV download, triggered by the "Download CSV" header button (v7.0 — ST-13, BLG-FEAT-69; supersedes the v2.1 "no button, URL-parameter only" note — that variant was never implemented and was inconsistent with the PDF button on the same page)
- **SI-02 Gate Status section (v0.6 — ST-06):** `GET /trades`, `GET /trade-plans`, `GET /analytics/arc5-compliance` — existing endpoints, no new backend work
- **Monthly CSV export (v7.8):** `GET /reports/monthly-pnl?format=csv` — CSV download, triggered by the Monthly P&L Report's "Download CSV" button (ST-05, BLG-FEAT-81)
- **Reconciliation Report (v0.13):** `GET /reports/reconciliation?year=YYYY` — new endpoint, contract specified in §Reconciliation Report below (ST-01, BLG-FEAT-88; implementation and contract filing are sprint-execution scope)
- **Canonical contract:** `docs/specs/api_contracts/reports_endpoints.md`

All values displayed on this page are sourced from the API response. The frontend must not recalculate P&L, FX conversions, or fee adjustments.

---

---

## Monthly P&L Report

Covers the Monthly P&L view (`GET /reports/monthly-pnl`). This view renders a month-by-month breakdown table of realised P&L for the current and prior calendar years.

> **Note:** The monthly financial table (year, month, realised_pnl_gbp, trade_count columns) is the core existing view. This section specifies the **Strategy Compliance** section added by ST-18 (v4.3).

**Design source (Avg P&L/Trade column, v0.14):** `docs/design/2026-08-07__release-v8.4/avg-pnl-per-trade-column/decision_record.md`

---

### Monthly Financial Table

One row per calendar month (descending order). Sourced from `GET /reports/monthly-pnl`.

| Column | Field | Notes |
|--------|-------|-------|
| Year | `year` | Calendar year |
| Month | `month` | 1=January … 12=December; display as full month name |
| Realised P&L | `realised_pnl_gbp` | GBP. Colour-coded: green if positive, red if negative, grey/neutral if exactly zero *(corrected v0.15; converged with the Tax Year Trades Table at v0.16 — both tables now share this rule, see Changelog)* |
| Trades | `trade_count` | Integer count of closed trades |
| Avg P&L/Trade | *derived* (v0.14 — ST-01, BLG-FE-141) | `realised_pnl_gbp / trade_count`, GBP, 2dp. Same colour rule as this table's Realised P&L column (green if positive, red if negative, grey/neutral if exactly zero — breakeven is not a loss). `trade_count = 0`: display **"—"** (no colour), not `£0.00` — avoids implying a computed zero average. Client-side display arithmetic on already-fetched row values, not a P&L recalculation — same basis as the Combined Total Line below. |

Empty state (no closed trades in scope): "No monthly P&L data available yet."

---

### Monthly CSV Export (v7.8 — ST-05, BLG-FEAT-81)

**Design source:** `docs/design/2026-07-24__release-v7.8/monthly-csv-export/ux_spec.md`

A **"Download CSV"** button, right-aligned above the Monthly Financial Table — reuses the Tax Year tab's §Download CSV Button States pattern verbatim (idle/generating/success/error, same visual weight). On narrow screens: drops below the section header, full width.

| State | Label | Behaviour |
|-------|-------|-----------|
| Idle | **"Download CSV"** (with download icon) | Enabled once the Monthly P&L Report has loaded successfully |
| Generating | **"Generating…"** (spinner replaces icon) | Button disabled; fires `GET /reports/monthly-pnl?format=csv` |
| Success | Returns to Idle | Browser file download begins; no success toast required |
| Error | Returns to Idle | Toast notification: `"CSV generation failed. Please try again."` (auto-dismiss 5s) |

Exports exactly the rows rendered in the Monthly Financial Table above (`Year`, `Month`, `Realised P&L (GBP)`, `Trades`) for whatever range is already loaded — no separate date-range picker, no client-side recalculation. Valid for empty ranges; button always enabled once the section loads. **Does not include Avg P&L/Trade (v0.14)** — that column is a display-only derived figure, not part of the exported column set; unaffected by its addition to the on-screen table.

**Reconciliation rule:** for any calendar year present in both exports, the sum of that year's rows in this CSV must equal the realised P&L total in the Tax Year tab's CSV for the same year — both derive from the same `trade_history.pnl` ledger, grouped differently (month vs. UK tax year). Verified at QA sign-off, not a UI-visible feature.

Does **not** cover the §Unrealised P&L Card or §Strategy Compliance Section figures below — export scope matches the Tax Year export's scope (realised trades table only).

---

### Unrealised P&L Card (v7.0 — ST-14, BLG-FEAT-70)

Displayed directly below the Monthly Financial Table. Reuses the Tax Year tab's approved §Unrealised P&L Card pattern verbatim (same field, same disclaimer, same visual-separation rule) rather than a new one — `realised_pnl_gbp` in the monthly table remains per-row/per-month; unrealised P&L is a current-snapshot figure with no month attribution, so it is shown once, not per row.

- Shows `estimated_unrealised_pnl` (GBP) — same field/computation as the Tax Year tab (sum of `pnl` across all currently open positions)
- Displays the `unrealised_note` disclaimer text verbatim (same API field)
- Card header: **"Indicative Unrealised P&L (current positions)"**
- Colour: profit `text-emerald-400`, loss `text-rose-400` (matches Open Positions Panel convention, `open-positions-panel/ux_spec.md` v6.4)
- Must be visually distinct from the monthly table — users must not mistake this figure for a period-scoped value

#### Combined Total Line (satisfies AC-02 regression check)

Below the Unrealised P&L Card: **"Total (Realised + Unrealised): £X,XXX.XX"**, computed client-side as `sum(displayed monthly rows' realised_pnl_gbp) + estimated_unrealised_pnl` — display-only arithmetic on already-fetched values; no new endpoint, no server-side recalculation of either source figure (consistent with the page's "must not recalculate P&L" rule).

**Colour (v0.9 — ST-06, BLG-SPEC-83):** same convention as the Tax Year tab's Unrealised P&L Card above — profit `text-emerald-400`, loss `text-rose-400`, aligned with the Open Positions Panel P&L convention (`open-positions-panel/ux_spec.md`, v6.4).

Design source: `docs/design/2026-07-12__release-v7.0/realized-unrealized-split/ux_spec.md`.

**Reconciliation rule (v0.10 — ST-06, BLG-SPEC-83, AC-03):** The Combined Total is an **approximate**, not exact, tie-back to `GET /portfolio`'s `total_pnl` field (the portfolio's lifetime "true P&L" — `total_value − net_cash_flow`, a balance-sheet-style calculation independent of the trade-ledger sum used here). The two are expected to differ by a small amount because they are derived through entirely separate computation paths: `total_pnl` uses the portfolio's current live valuation, while realised is a lifetime sum of `trade_history.pnl` (fixed at each trade's own exit-time FX/price) and unrealised is the last nightly-job snapshot (see Data Freshness note above) — not the same live basis `total_pnl` uses. **Verified against production data, 2026-07-14:** realised (lifetime, all 20 closed trades) = £1,100.46; unrealised (`estimated_unrealised_pnl`) = −£126.25; combined = £974.21. `GET /portfolio`'s `total_pnl` at the same moment = £988.19 (diff £13.98, ≈1.4%) — consistent in direction and rough magnitude with one open US position's live-vs-nightly-snapshot valuation gap, not an unexplained divergence. Do not treat the Combined Total as a substitute for `total_pnl`; it is a period-scoped, ledger-based approximation for tax-reference reading, not the authoritative portfolio P&L figure.

---

### Strategy Compliance Section

Displayed below the monthly financial table. Data sourced from a separate call to `GET /analytics/arc5-compliance`.

**Section header:** **"Strategy Compliance"**

#### Fields Displayed

| Field | API Source | Label | Notes |
|-------|-----------|-------|-------|
| Overall validation pass rate | Mean of `data.validation_pass_rate_by_rule[*].pass_rate` | Validation Pass Rate | Percentage; null → "N/A" |
| `override_rate` | `data.override_rate` | Override Rate | Percentage; null → "N/A" |
| `events_per_week` | `data.events_per_week` | Red Flag Events/Week | Float; rounded to 1 dp |
| `top_rule_breach` | `data.top_rule_breach` | Most Frequent Rule Breach | Rule type label; null → "None" |

> **AC field mapping:** ST-18 AC-02 uses names `validation_pass_rate`, `override_count`, `red_flag_events_count`, `most_frequent_rule_breach`. These map to the above API fields; no endpoint extension required. Resolved at design gate 2026-05-29.

#### Rendering Conditions

- Always visible below the monthly financial table (not collapsible)
- Loading state: skeleton placeholder while `GET /analytics/arc5-compliance` is pending
- Error state: "Unable to load compliance data" if API returns error
- Empty state (no data): "No compliance data recorded yet"

#### Design Basis

Follows the Arc 5 Compliance Summary design language from the tax-year report (§Arc 5 Compliance Summary, added v4.1). Stat-card or list layout with metric labels and values. Same `GET /analytics/arc5-compliance` data source.

#### Sign-off

- **Head of UX & Design:** Design artefact confirmed (existing Arc 5 Compliance Summary pattern, reports.md v0.3). Design gate: 2026-05-29__release-v4.3.
- **Product Owner:** Confirmed no new design decisions required; rate-based field mapping accepted. Design gate: 2026-05-29__release-v4.3.

---

## Reconciliation Report (v0.13 — ST-01, BLG-FEAT-88)

**Design source:** `docs/design/2026-08-04__release-v8.2/pnl-reconciliation-report/decision_record.md`

A new **"Reconciliation"** tab (4th tab in the page's tab navigation, alongside Performance / Tax Year / Monthly). Gives the user a single confirming view that the system-computed realised P&L total for a tax year and an independently re-derived sum of that year's individual trade export rows agree — surfacing user-visibly what the Monthly CSV export's and Combined Total's existing reconciliation rules (§Monthly CSV Export, §Unrealised P&L Card) only state in prose.

**Scope:** realised P&L vs. trade export only — does not cover unrealised P&L (already caveated by the Combined Total note) or portfolio `total_pnl` (already covered by the existing approximate-tie-back rule).

### Layout

| Element | Content |
|---------|---------|
| Year selector | Reuses the page's existing shared §Year Selector |
| System Total card | Label "System-Computed Total", value `system_total_pnl_gbp`, page's standard profit/loss colour convention (`text-emerald-400` / `text-rose-400`) |
| Export Total card | Label "Trade Export Total", value `export_total_pnl_gbp`, same colour convention |
| Match indicator | Badge — "✓ Reconciled" (reuses the SI-02 Gate Status `MET` badge style verbatim) when `matched: true`; "⚠ Discrepancy — £X.XX difference" (reuses the `NOT MET` badge style) when `matched: false` |
| Sign-off note | Static text: "Reviewed and confirmed matching by the Financial Reporting & Records Owner on \<date\>" |

### States

| State | Content |
|-------|---------|
| Loading | Skeleton placeholder, matches existing page loading pattern |
| Error | "Unable to load reconciliation data" |
| Empty (no trades in selected year) | "No trade data available for {year} — reconciliation not applicable" |

### API Contract (shape only)

`GET /reports/reconciliation?year=YYYY` →

```
{
  "system_total_pnl_gbp": number,
  "export_total_pnl_gbp": number,
  "matched": boolean
}
```

`export_total_pnl_gbp` must be computed via a query path independent of the one powering the existing CSV export, so a divergence is meaningful rather than definitionally impossible. Endpoint implementation, the `## GET /reports/reconciliation` entry in `docs/specs/api_contracts/reports_endpoints.md`, and the `docs/reference/openapi.yaml` entry (same-commit, per `CLAUDE.md` §2) are sprint-execution scope — this design gate specifies the contract shape only.

### Sign-off

- **Head of UX & Design:** Approved — 2026-08-04 (reuses existing badge/card visual language verbatim; no new visual pattern introduced)
- **Financial Reporting & Records Owner:** Scope confirmed as matching BLG-FEAT-88's acceptance criteria — 2026-08-04
- **Product Owner:** Approved — 2026-08-04

---

## Known Deviations

### DEV-REPORTS-ST06-01 — Unrealised P&L differs between Reports and Positions page (data freshness)

- **Description:** `GET /reports/monthly-pnl` and `GET /reports/tax-year`'s `estimated_unrealised_pnl` field (`get_estimated_unrealised_pnl()`, `backend/services/reports_service.py`) sums `positions.pnl` via a raw `database.get_positions()` read — a column written once per night by `run_nightly_trailing_stop_update()` (`backend/services/position_service.py`), not recomputed live. The Positions page (`GET /positions` → `get_positions_with_prices()`) computes `pnl` fresh against the current live price on every request. The two pages can therefore show different unrealised P&L figures for the same position at the same moment, with no in-app indication that one is a snapshot. Discovered during ST-06's AC-03 reconciliation verification (2026-07-14): production showed Reports' `estimated_unrealised_pnl` = −£126.25 vs the Positions page's live figure = −£115.06 for the same single open position at the same time (£11.19 gap).
- **Canonical requirement:** §Unrealised P&L Card states the figure is "the sum of `pnl` across all currently open positions" with no staleness caveat — a user could reasonably read this as reflecting current market price, matching the Positions page.
- **Priority:** P3 (informational figure only, clearly labelled "Indicative" with an existing not-a-tax-liability disclaimer; not a financial-record-integrity issue — no money moves based on this number)
- **Target resolution release:** TBD — not yet scheduled
- **Owner:** Frontend Specifications & UX Documentation Owner
- **Backlog reference:** BLG-SPEC-87 (filed sprint execution 2026-07-14, cycle 2026-07-14__release-v7.1, ST-06) — candidate fix directions: (a) switch `get_estimated_unrealised_pnl()` to live-compute via `get_positions_with_prices()` instead of the raw nightly-snapshot read, or (b) keep the snapshot for performance/cost reasons but add an explicit "as of last nightly update" caveat to `unrealised_note`. Not decided here — ST-06's scope is documentation/verification, not a fix.

### DEV-REPORTS-ST01-02 — Monthly Financial Table's zero-P&L colour rule differs from the Tax Year Trades Table's (RESOLVED v0.16)

- **Description:** Both tables display `realised_pnl_gbp` and both were documented with identical wording ("green if positive, red if negative or zero"), but the two live components actually disagreed at the exact-zero case: the Tax Year tab's Trades Table (`TaxYearReport`, `src/pages/Reports.js`) rendered exact-zero as **red** (binary `pnl > 0 ? emerald : rose`, no neutral branch); the Monthly P&L Report's table (`MonthlyPnlTable`) renders exact-zero as **grey/neutral** (three-way ternary with a dedicated zero case). Discovered during ST-01's Avg P&L/Trade column work (2026-08-07) when the new column's colour rule was checked against its cited spec text and found to match the Monthly table's actual code, not the words on this page — which had been silently describing the Tax Year table's behaviour for both all along.
- **Resolution (v0.16, ST-08, BLG-FE-144, v8.5 design gate):** both tables converge on grey/neutral-for-zero. `TaxYearReport`'s `Realised P&L` column changed to match `MonthlyPnlTable`'s existing three-way rule. Design source: `docs/design/2026-08-08__release-v8.5/exact-zero-pnl-colour-convention/decision_record.md`.
- **Priority:** P3 (colour-only, no figure is wrong or missing; exact-zero months/trades are visually rare and the underlying number is always correct regardless of colour)
- **Owner:** Frontend Specifications & UX Documentation Owner
- **Backlog reference:** BLG-FE-144 (filed sprint execution 2026-08-07, cycle 2026-08-07__release-v8.4, ST-01; resolved 2026-08-08, cycle 2026-08-08__release-v8.5, ST-08).

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.16 | 2026-08-08 | v8.5 design gate — ST-08 (EPIC-03, BLG-FE-144): resolved `DEV-REPORTS-ST01-02` — Tax Year Trades Table's `Realised P&L` column colour rule converged with the Monthly Financial Table's (green if positive, red if negative, grey/neutral if exactly zero; was binary red-for-zero on the Tax Year table). No change to non-zero colouring in either table. Design source: `docs/design/2026-08-08__release-v8.5/exact-zero-pnl-colour-convention/decision_record.md`. Head of UX & Design sign-off: 2026-08-08. Product Owner approved: 2026-08-08. Head of Specs Team confirmed. |
| 0.15 | 2026-08-07 | Sprint execution — ST-01 (EPIC-01, BLG-FE-141) follow-up correction, agent-mediated on behalf of Frontend Specifications & UX Documentation Owner (Product Owner directed): Monthly Financial Table's Realised P&L and Avg P&L/Trade rows corrected from "red if negative or zero" to "red if negative, grey/neutral if exactly zero" — the prior wording never matched `MonthlyPnlTable`'s actual code (only the separate Tax Year Trades Table implements literal red-for-zero). Filed as `DEV-REPORTS-ST01-02`/`BLG-FE-144` rather than silently rewritten, since the two tables' now-documented behaviours still disagree with each other — that convergence decision is not made here. |
| 0.14 | 2026-08-07 | v8.4 design gate — ST-01 (EPIC-01, BLG-FE-141): Avg P&L/Trade column added to the Monthly Financial Table — client-side derived (`realised_pnl_gbp / trade_count`), same colour rule as Realised P&L, zero-trade months show "—" rather than a fabricated `£0.00`. Explicitly excluded from the Monthly CSV export's column set (display-only figure). Design source: `docs/design/2026-08-07__release-v8.4/avg-pnl-per-trade-column/decision_record.md`. Head of UX & Design sign-off: 2026-08-07. Product Owner approved: 2026-08-07. Head of Specs Team confirmed. |
| 0.13 | 2026-08-04 | v8.2 design gate — ST-01 (EPIC-01, BLG-FEAT-88): §Reconciliation Report added — new "Reconciliation" tab comparing the system-computed realised P&L total against an independently re-derived sum of the individual trade export, for a selected year, with a match/discrepancy badge (reuses SI-02 Gate Status's MET/NOT MET badge style verbatim). New endpoint `GET /reports/reconciliation?year=YYYY` contract specified (shape only — implementation, `reports_endpoints.md` entry, and `openapi.yaml` entry are sprint-execution scope, same-commit per CLAUDE.md §2). Design source: `docs/design/2026-08-04__release-v8.2/pnl-reconciliation-report/decision_record.md`. Head of UX & Design sign-off: 2026-08-04. Financial Reporting & Records Owner scope confirmation: 2026-08-04. Product Owner approved: 2026-08-04. Head of Specs Team confirmed. |
| 0.12 | 2026-08-03 | ST-14 (EPIC-05, v8.1, BLG-SPEC-72): §SI-02 Gate Status Condition 2 and Condition 3 thresholds product-reviewed and formally documented, closing the `Specs_Index.md`-tracked "engine-filled gap" (never previously product-reviewed). Condition 2 confirmed at the existing `linked closed trades >= 20` (consistent with Condition 1's own 20-trade bar and the separate `BLG-GOV-107` backend gate). Condition 3 changed from the placeholder `trade_plan_adherence_rate > 0` to `>= 0.50` — a majority-discipline bar; no prior threshold existed for this metric anywhere in the spec. `src/pages/Reports.js`'s `SI02GateStatusSection` updated to match, with new Playwright coverage for the changed threshold. Product Owner decision (agent-mediated, §5.3, explicit user direction). |
| 0.11 | 2026-07-24 | v7.8 design gate — ST-05 (EPIC-05, BLG-FEAT-81): Monthly CSV Export added to the Monthly P&L Report view — "Download CSV" button reusing the Tax Year tab's export pattern verbatim (idle/generating/success/error states), new `GET /reports/monthly-pnl?format=csv` endpoint, reconciliation rule against the Tax Year CSV documented. Scope excludes Unrealised P&L Card and Strategy Compliance Section figures (matches Tax Year export's scope). Design source: `docs/design/2026-07-24__release-v7.8/monthly-csv-export/ux_spec.md`. Head of UX & Design sign-off: 2026-07-24. Product Owner approved: 2026-07-24. Head of Specs Team confirmed. |
| 0.10 | 2026-07-14 | v7.1 sprint execution (ST-06, BLG-SPEC-83): §Unrealised P&L Card (both tabs) — added Data Freshness note (nightly-snapshot vs live-computed distinction) and Reconciliation Rule (AC-03, verified against production data: realised £1,100.46 + unrealised −£126.25 = £974.21 vs `GET /portfolio.total_pnl` £988.19, diff £13.98/≈1.4%, explained by the snapshot-vs-live valuation gap — approximate tie-back, not exact). Added §Known Deviations, filed `DEV-REPORTS-ST06-01` (P3, BLG-SPEC-87) for the underlying Reports-vs-Positions unrealised P&L data-freshness gap discovered during this verification. |
| 0.9 | 2026-07-14 | v7.1 design gate (ST-06, BLG-SPEC-83): Explicit colour convention added to both Unrealised P&L Card sections (Tax Year tab and Monthly P&L Report) — profit `text-emerald-400`, loss `text-rose-400`, aligned with the Open Positions Panel P&L convention. Closes ST-06 AC-04 (visual treatment confirmation) — the v7.0 `realized-unrealized-split` design artefact already specified this colour; it had not yet been written into this canonical spec's text. Existing artefact reviewed and confirmed current — no new design work required. Head of UX & Design sign-off: 2026-07-14. Product Owner approved: 2026-07-14. Head of Specs Team confirmed. |
| 0.8 | 2026-07-13 | v7.0 sprint execution (ST-06, BLG-SPEC-71): Reconciled §Arc 5 Compliance Summary and §Gross vs Net Comparison to explicitly state "Design Only — Implementation Pending" — both were specified with changelog entries worded as shipped features, but neither is actually rendered in `Reports.js`'s Tax Year P&L view (confirmed via `git log -S`: both design gate commits touched only spec files, no `src/` files). Root cause: spec-authoring stories' changelog entries were indistinguishable from shipped-feature entries, letting this drift persist undetected for 8+ release cycles (v4.1/v6.0 → v6.8). No code change — documentation reconciliation only. Re-implementation remains available as a Product Owner scheduling decision (new `BLG-FEAT` items), not a default reconciliation path. |
| 0.7 | 2026-07-12 | v7.0 design gate: (ST-13, BLG-FEAT-69) Tax-year CSV export — "Download CSV" header button added alongside "Download PDF" (idle/generating/success/error states, same pattern); supersedes the stale v2.1 "no button, URL-parameter only" API Reference note (never implemented, inconsistent with PDF button). (ST-14, BLG-FEAT-70) Monthly P&L Report — Unrealised P&L Card added below the Monthly Financial Table, reusing the Tax Year tab's approved card pattern (`estimated_unrealised_pnl`, `unrealised_note`); Combined Total line added (client-side sum, no new endpoint). Design sources: v0.7 additions listed above. Head of UX & Design sign-off: 2026-07-12. Product Owner approved: 2026-07-12. Head of Specs Team confirmed. |
| 0.6 | 2026-07-08 | v6.8 design gate — SI-02 Gate Status section added (ST-06, BLG-FEAT-71): collapsible, collapsed by default, below Arc 5 Compliance Summary and above Gross vs Net Comparison. Shows total closed trades vs. trade-plan-linked closed trades as two distinct numbers, plus MET/NOT MET badges for 3 SI-02 gate conditions. Sourced from existing `GET /trades`, `GET /trade-plans`, `GET /analytics/arc5-compliance` — no new backend work. Reflects ST-01 (BLG-BE-46) finding live, as-is. Distinct from Dashboard's single-metric Gate Progress strip (dashboard.md §6). Design source: si02-gate-visibility-indicator/ux_spec.md. Approved: Product Owner 2026-07-08. Head of Specs Team confirmed. |
| 0.5 | 2026-06-19 | v6.0 design gate — Gross vs Net Comparison section added to Summary Bar (ST-03): conditional row showing average gross vs net R-multiple when ≥1 trade in selected year has brokerage cost data; footnote showing trade count with cost data; absent when no cost data. Design source: net-of-costs-tracking/ux_spec.md. Approved: Product Owner 2026-06-19. Head of Specs Team confirmed. |
| 0.4 | 2026-05-29 | v4.3 Monthly P&L Strategy Compliance section (ST-18, BLG-FE-38): Monthly P&L Report section added — financial table spec and Strategy Compliance section (validation pass rate, override rate, red flag events/week, most frequent rule breach from GET /analytics/arc5-compliance). AC field mapping resolved (override_count→override_rate, red_flag_events_count→events_per_week). Design artefact: Arc 5 Compliance Summary v4.1 pattern. Design gate: 2026-05-29__release-v4.3. Head of UX & Design + Product Owner sign-off. |
| 0.3 | 2026-05-27 | v4.1 Arc 5 P&L integration (ST-08, BLG-FEAT-42): Arc 5 Compliance Summary section added — collapsible, collapsed by default, data from GET /analytics/arc5-compliance, composite score or individual metrics per FEAT-40 formula availability. Financial Reporting & Records Owner + Product Owner agent-mediated sign-off cleared. |
| 0.2 | 2026-03-18 | v2.1 PDF export (ST-12, BLG-FR-01): Page Header Controls section added with Download PDF button spec (idle, generating, success, error states). API Reference updated to include PDF and CSV export endpoints. Design source: docs/design/2026-03-18__release-v2.1/pdf-export/ux_spec.md. Design gate: 2026-03-18__release-v2.1. |
| 0.1 | 2026-03-17 | Initial spec. ST-05 — EPIC-02 (4.1b Tax-Year P&L Statement). Design gate: 2026-03-17__release-v2.0. Approved by Head of UX & Design + Product Owner. |
