# reports.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.9
**Last Updated:** 2026-07-14
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
- **Colour (v0.9 — ST-06, BLG-SPEC-83):** profit `text-emerald-400`, loss `text-rose-400` — matches the Open Positions Panel P&L convention (`open-positions-panel/ux_spec.md`, v6.4), explicitly aligned rather than distinct, so the same figure reads consistently wherever it appears in the app. Design source: `docs/design/2026-07-12__release-v7.0/realized-unrealized-split/ux_spec.md`.

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
| Gate Condition 1 (20-trade threshold) | derived | MET / NOT MET badge | |
| Gate Condition 2 | derived | MET / NOT MET badge | |
| Gate Condition 3 (trade plan adherence) | `trade_plan_adherence_rate` | MET / NOT MET badge | |

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
- **Canonical contract:** `docs/specs/api_contracts/reports_endpoints.md`

All values displayed on this page are sourced from the API response. The frontend must not recalculate P&L, FX conversions, or fee adjustments.

---

---

## Monthly P&L Report

Covers the Monthly P&L view (`GET /reports/monthly-pnl`). This view renders a month-by-month breakdown table of realised P&L for the current and prior calendar years.

> **Note:** The monthly financial table (year, month, realised_pnl_gbp, trade_count columns) is the core existing view. This section specifies the **Strategy Compliance** section added by ST-18 (v4.3).

---

### Monthly Financial Table

One row per calendar month (descending order). Sourced from `GET /reports/monthly-pnl`.

| Column | Field | Notes |
|--------|-------|-------|
| Year | `year` | Calendar year |
| Month | `month` | 1=January … 12=December; display as full month name |
| Realised P&L | `realised_pnl_gbp` | GBP. Colour-coded: green if positive, red if negative or zero |
| Trades | `trade_count` | Integer count of closed trades |

Empty state (no closed trades in scope): "No monthly P&L data available yet."

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

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.9 | 2026-07-14 | v7.1 design gate (ST-06, BLG-SPEC-83): Explicit colour convention added to both Unrealised P&L Card sections (Tax Year tab and Monthly P&L Report) — profit `text-emerald-400`, loss `text-rose-400`, aligned with the Open Positions Panel P&L convention. Closes ST-06 AC-04 (visual treatment confirmation) — the v7.0 `realized-unrealized-split` design artefact already specified this colour; it had not yet been written into this canonical spec's text. Existing artefact reviewed and confirmed current — no new design work required. Head of UX & Design sign-off: 2026-07-14. Product Owner approved: 2026-07-14. Head of Specs Team confirmed. |
| 0.8 | 2026-07-13 | v7.0 sprint execution (ST-06, BLG-SPEC-71): Reconciled §Arc 5 Compliance Summary and §Gross vs Net Comparison to explicitly state "Design Only — Implementation Pending" — both were specified with changelog entries worded as shipped features, but neither is actually rendered in `Reports.js`'s Tax Year P&L view (confirmed via `git log -S`: both design gate commits touched only spec files, no `src/` files). Root cause: spec-authoring stories' changelog entries were indistinguishable from shipped-feature entries, letting this drift persist undetected for 8+ release cycles (v4.1/v6.0 → v6.8). No code change — documentation reconciliation only. Re-implementation remains available as a Product Owner scheduling decision (new `BLG-FEAT` items), not a default reconciliation path. |
| 0.7 | 2026-07-12 | v7.0 design gate: (ST-13, BLG-FEAT-69) Tax-year CSV export — "Download CSV" header button added alongside "Download PDF" (idle/generating/success/error states, same pattern); supersedes the stale v2.1 "no button, URL-parameter only" API Reference note (never implemented, inconsistent with PDF button). (ST-14, BLG-FEAT-70) Monthly P&L Report — Unrealised P&L Card added below the Monthly Financial Table, reusing the Tax Year tab's approved card pattern (`estimated_unrealised_pnl`, `unrealised_note`); Combined Total line added (client-side sum, no new endpoint). Design sources: v0.7 additions listed above. Head of UX & Design sign-off: 2026-07-12. Product Owner approved: 2026-07-12. Head of Specs Team confirmed. |
| 0.6 | 2026-07-08 | v6.8 design gate — SI-02 Gate Status section added (ST-06, BLG-FEAT-71): collapsible, collapsed by default, below Arc 5 Compliance Summary and above Gross vs Net Comparison. Shows total closed trades vs. trade-plan-linked closed trades as two distinct numbers, plus MET/NOT MET badges for 3 SI-02 gate conditions. Sourced from existing `GET /trades`, `GET /trade-plans`, `GET /analytics/arc5-compliance` — no new backend work. Reflects ST-01 (BLG-BE-46) finding live, as-is. Distinct from Dashboard's single-metric Gate Progress strip (dashboard.md §6). Design source: si02-gate-visibility-indicator/ux_spec.md. Approved: Product Owner 2026-07-08. Head of Specs Team confirmed. |
| 0.5 | 2026-06-19 | v6.0 design gate — Gross vs Net Comparison section added to Summary Bar (ST-03): conditional row showing average gross vs net R-multiple when ≥1 trade in selected year has brokerage cost data; footnote showing trade count with cost data; absent when no cost data. Design source: net-of-costs-tracking/ux_spec.md. Approved: Product Owner 2026-06-19. Head of Specs Team confirmed. |
| 0.4 | 2026-05-29 | v4.3 Monthly P&L Strategy Compliance section (ST-18, BLG-FE-38): Monthly P&L Report section added — financial table spec and Strategy Compliance section (validation pass rate, override rate, red flag events/week, most frequent rule breach from GET /analytics/arc5-compliance). AC field mapping resolved (override_count→override_rate, red_flag_events_count→events_per_week). Design artefact: Arc 5 Compliance Summary v4.1 pattern. Design gate: 2026-05-29__release-v4.3. Head of UX & Design + Product Owner sign-off. |
| 0.3 | 2026-05-27 | v4.1 Arc 5 P&L integration (ST-08, BLG-FEAT-42): Arc 5 Compliance Summary section added — collapsible, collapsed by default, data from GET /analytics/arc5-compliance, composite score or individual metrics per FEAT-40 formula availability. Financial Reporting & Records Owner + Product Owner agent-mediated sign-off cleared. |
| 0.2 | 2026-03-18 | v2.1 PDF export (ST-12, BLG-FR-01): Page Header Controls section added with Download PDF button spec (idle, generating, success, error states). API Reference updated to include PDF and CSV export endpoints. Design source: docs/design/2026-03-18__release-v2.1/pdf-export/ux_spec.md. Design gate: 2026-03-18__release-v2.1. |
| 0.1 | 2026-03-17 | Initial spec. ST-05 — EPIC-02 (4.1b Tax-Year P&L Statement). Design gate: 2026-03-17__release-v2.0. Approved by Head of UX & Design + Product Owner. |
