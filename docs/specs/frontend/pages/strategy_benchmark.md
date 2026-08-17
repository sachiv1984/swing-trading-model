**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 0.6
**Last Updated:** 2026-08-17 (v8.9 design gate — added §7.6 Backtest Rule Change tab, ST-07 BLG-FEAT-89, EPIC-02); prior — 2026-07-29 (ST-19, EPIC-05, v7.10, BLG-FE-106 — Page Header consolidation); prior history retained — see prior entries in version control.
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Release:** v7.7
**EPIC:** EPIC-01
**Design Source (v0.1):** docs/design/2026-06-26__release-v6.3/strategy-benchmark-page/ux_spec.md
**Design Source (v0.2 additions):** docs/design/2026-07-02__release-v6.4/open-positions-panel/ux_spec.md
**Design Source (v0.3 additions):** docs/design/2026-07-12__release-v7.0/heading-light-theme-contrast/decision_record.md (BLG-FE-95 remediation)
**Design Source (v0.4 additions):** docs/design/2026-07-21__release-v7.7/si04-strategy-version-comparison/ux_spec.md
**Design Source (v0.6 additions):** docs/design/2026-08-17__release-v8.9/in-app-backtesting-engine/ux_spec.md
**Confirmed by:** Head of Specs Team — 2026-07-21

---

# Frontend Specification — Strategy Benchmark Page

## 1. Purpose & User Goals

The Strategy Benchmark page allows the user to compare their live trading performance against the backtest output of `production_strategy.py`. It answers: "Am I trading this strategy, and how does my execution compare?"

**Route:** `/strategy/benchmark`
**Navigation label:** "Strategy Benchmark"
**Navigation icon:** `BarChart3` (Lucide)
**Navigation placement:** Under analytics/reports group in main navigation

Users should be able to:
- See at a glance how live trade performance compares to backtest expectations
- Drill into individual years to identify performance drift
- Browse individual backtest and actual trade records with exit reason context

---

## 2. Page Header

| Element | Spec |
|---------|------|
| Title | "Strategy Benchmark" |
| Description | "Compare live trading vs backtest" |
| Component | `PageHeader` |
| Last updated line | `"Benchmark data as of DD Mon YYYY"` — muted, small; sourced from most recent import; absent when no data |

**Implementation note (v0.3 — ST-08, BLG-FE-95, historical):** at the time of this fix, the shipped implementation (`StrategyBenchmark.js`) used a bare, hand-rolled header (icon + `<h1>` + `<p>`), not the shared `PageHeader` component named above — a pre-existing spec/implementation deviation, out of scope for that contrast-only fix. Title colour fixed that cycle: `text-white` → `text-slate-900 dark:text-white` (light-mode value was missing entirely; ~1.1:1 fail on `bg-slate-100`). Light: `text-slate-900` ≈17.9:1 (AAA). Dark: unchanged, no regression. Sizing/weight (`text-lg font-semibold`) unchanged. Design source: `docs/design/2026-07-12__release-v7.0/heading-light-theme-contrast/decision_record.md`.

**Consolidation (v0.5 — ST-19, EPIC-05, v7.10, BLG-FE-106):** the deviation noted above is resolved — `StrategyBenchmark.js` now renders its title/description via the shared `PageHeader` component, matching this section exactly. The `BarChart2` icon and the "Benchmark data as of" last-updated line (sourced from `summary.last_imported_at`) are preserved as elements adjacent to `PageHeader` (`PageHeader` itself has no icon or subtitle-line prop). This changes the title's visual style to `PageHeader`'s standard gradient-clipped text (`text-2xl font-bold`, `bg-clip-text`) rather than the previous solid-colour `text-lg font-semibold` — an intended consequence of the consolidation, not a regression. `tests/e2e/heading-light-theme-contrast.spec.js`'s SC-HTC-03/04 were updated accordingly (gradient `background-image` stops checked instead of solid `color`, matching the technique already established in `page-header-dark-gradient-contrast.spec.js` for other `PageHeader`-consuming pages).

**Sub-navigation (v0.4 — ST-01, EPIC-01, v7.7; extended v0.6 — ST-07, EPIC-02, v8.9):** a three-tab bar sits immediately below the page header: **"Benchmark"** (default active — existing §3–§7 content, unchanged), **"Version Comparison"** (§7.5), and **"Backtest Rule Change"** (new, §7.6). Client-side tab state via `?tab=version-comparison` / `?tab=backtest-rule-change` query params, no new top-level route.

---

## 3. Sticky Filter Bar

Positioned below the page header. Remains visible while scrolling.

| Filter | Control | Options |
|--------|---------|---------|
| Year | Pill/tab selector | All + individual years derived from data (e.g. 2018–2026) |
| Market | Pill/tab selector | All + markets present in data (e.g. UK, US) |

- Both filters apply simultaneously to Panels 1–3
- **Exception:** Panel 0 (Open Positions) respects the Market filter but ignores the Year filter — see §4.5
- Default: Year = All, Market = All
- Active pill: filled background (consistent with existing pill-tab pattern)
- Order: Year filter first, Market filter second

---

## 4. Empty State (No Import Data)

Shown when no benchmark data has been imported yet:

| Element | Spec |
|---------|------|
| Icon | `BarChart3` (Lucide), muted |
| Heading | "No benchmark data imported yet" |
| Body | "Run import_backtest.py to load strategy data." |
| Code display | `python import_backtest.py` — monospace code block |
| Sub-text | "(calls POST /strategy/benchmark/import)" — muted |
| Container | Centred, full-width card; no error styling — this is expected first-run state |

This state replaces all three panels. Filter bar is hidden when no data.

---

## 4.5 Panel 0 — Open Positions

**Design source:** docs/design/2026-07-02__release-v6.4/open-positions-panel/ux_spec.md

**Placement:** Between the Sticky Filter Bar and Panel 1. Panel 1/2/3 numbering is unchanged.

**Conditional rendering:** Rendered only when ≥1 open position exists for the current filter context (see Filter Interaction below). Omitted entirely (no placeholder) when zero open positions match.

### Panel Header

| Element | Spec |
|---------|------|
| Label | "Open Positions" |
| One-line summary | `"<N> open position(s) · <sign>£X,XXX unrealized"` |
| Summary colour | `text-emerald-400` if aggregate unrealized P&L ≥ 0; `text-rose-400` if negative |
| Expand/collapse | None — always expanded when rendered |

### Open Positions Table

| Column | Format |
|--------|--------|
| Ticker | Uppercase |
| Market | Badge (only shown when Market filter = All) |
| Entry Date | DD Mon YYYY |
| Entry Price | `£X.XX` |
| Current Price | `£X.XX` |
| Unrealized P&L (£) | Signed `£X,XXX.XX`; `text-emerald-400` profit / `text-rose-400` loss |
| Unrealized P&L (%) | Signed `X.X%`; `text-emerald-400` profit / `text-rose-400` loss |
| Days Held | Integer, derived from entry date |

**Sorting:** Default sort is Unrealized P&L (%) descending. No user-sortable columns in v0.2.

### Filter Interaction

- Market filter: applies normally — filters rows to the selected market
- Year filter: **does not apply to Panel 0** — panel always shows all currently open positions regardless of the selected year. Open positions are current-state, not historical-per-year data.

### Realized Metric Isolation (Hard Rule)

Unrealized positions must never enter Panel 1 stat cards, Panel 1 PnL bar chart, or Panel 2 yearly breakdown aggregates. No combined figure anywhere on the page mixes realized and unrealized values.

### States

| State | Behaviour |
|-------|-----------|
| ≥1 open position | Panel renders, sorted by P&L% descending |
| 0 open positions (or 0 after Market filter) | Panel omitted entirely |
| Loading | Skeleton row placeholders within panel bounds |
| API error (5xx/timeout) | Panel header renders; muted inline message "Open positions temporarily unavailable." — no icon; rest of page unaffected |

### Data Source

New `backtest_open_positions` table — **fully replaced** (not upserted) on each nightly import, consistent with `backtest_trades`.

---

## 5. Panel 1 — Performance Parity

### 5.1 Stat Card Layout

Two-column layout: **Backtest** (left) | **Actual** (right).

Column headers:
- Left: **"Backtest"** — muted badge
- Right: **"Actual"** — muted badge

Each column contains 4 stat cards:

| Metric | Backtest Label | Actual Label | Actual empty state (no live trades) |
|--------|---------------|--------------|--------------------------------------|
| Win Rate | "Backtest Win Rate" | "Actual Win Rate" | `—` |
| Avg R | "Backtest Avg R" | "Actual Avg R" | `—` |
| Total PnL | "Backtest PnL" | "Actual PnL" | `—` |
| Trade Count | "Backtest Trades" | "Actual Trades" | `0` |

**Hard rule:** Actual stat cards show `—` (not `0`) when no live trades exist for the selected period — except Trade Count which shows `0`. Do not imply zero revenue with a `0` value.

### 5.2 PnL Bar Chart

Grouped bar chart. One group per year; two bars per group (backtest | actual).

| Element | Spec |
|---------|------|
| Backtest bar | `#6B7280` (slate grey) |
| Actual bar — profit | `#22C55E` (green) |
| Actual bar — loss | `#EF4444` (red) |
| X-axis | Year labels; 45° rotation on mobile |
| Y-axis | GBP, auto-scaled |
| Legend | Below chart: ▪ Backtest ▪ Actual |
| Hover tooltip | "Year: [Y] / Backtest: £X / Actual: £X or N/A" |
| No data | "No data for selected period" — centred placeholder |
| Single-year filter | Chart collapses to 2-bar comparison (Backtest vs Actual only) |

---

## 6. Panel 2 — Yearly Breakdown Table

Scrollable table. All years in data appear as rows. Columns:

| Column | Format | Empty (no live trades for year) |
|--------|--------|----------------------------------|
| Year | 4-digit integer | — |
| BT Trades | Integer | — |
| Actual Trades | Integer | `—` |
| BT Win Rate | `X.X%` | — |
| Actual Win Rate | `X.X%` | `—` |
| BT Avg R | `±X.XXR` (signed, 2dp) | — |
| Actual Avg R | `±X.XXR` | `—` |
| BT PnL | `£X,XXX` | — |
| Actual PnL | `£X,XXX` | `—` |

**Total row:** Bottom row labelled "All years". Backtest aggregates over all years. Actual aggregates only over years with live data.

**Sorting:** Default sort is ascending by Year. No user-sortable columns in v0.1.

---

## 7. Panel 3 — Trade Log

### 7.1 Toggle Mode Selector

Three-way segmented control above table:

```
[ Backtest only ]  [ Actual only ]  [ Side-by-side ]
```

Default: **Backtest only**.

### 7.2 Trade Table Columns

| Column | Modes present | Format |
|--------|--------------|--------|
| Source | Side-by-side only | "BT" badge (muted) / "Live" badge (cyan) |
| Ticker | All | String |
| Entry Date | All | DD Mon YYYY |
| Exit Date | All | DD Mon YYYY |
| Exit Reason | All | Badge — see §7.3 |
| Entry Price | All | `£X.XX` |
| Exit Price | All | `£X.XX` |
| PnL | All | `±£X.XX`; profit: `text-emerald-400`, loss: `text-rose-400` |
| R-Multiple | All | `±X.XXR` signed 2dp; `N/A` if no stop loss |

### 7.3 Exit Reason Badges

Consistent with existing badge language on Positions/Signals pages:

| Reason | Label | Style |
|--------|-------|-------|
| Stop | **Stop** | Red — `bg-rose-500/20 text-rose-400 border-rose-500/30` |
| Risk-Off | **Risk-Off** | Amber — `bg-amber-500/20 text-amber-400 border-amber-500/30` |
| Rebalance | **Rebalance** | Teal — `bg-teal-500/20 text-teal-400 border-teal-500/30` |
| Other | Uppercased | Slate default |

### 7.4 Side-by-Side Mode Layout

Rows interleaved per trade pair:
- Backtest trade row — subtle background tint (`bg-slate-800/30`)
- Matching actual trade row (if any) — no background tint
- If no actual trade match: actual row shows placeholder `"No matching live trade"` with `—` across all metric columns

---

## 7.5 Version Comparison Tab (v0.4 — ST-01, EPIC-01, BLG-FEAT-75, v7.7)

**Design source:** docs/design/2026-07-21__release-v7.7/si04-strategy-version-comparison/ux_spec.md
**API contract:** docs/specs/api_contracts/strategy_version_comparison_contract.md (`GET /analytics/strategy-version-comparison`, v0.1.0)

SI-04 strategy-version performance comparison. Placed as a tab on this page rather than embedded in `Arc5ComplianceSection` — see design source §2 for the placement rationale (avoids an unscheduled dependency on `BLG-FE-59`'s extension-point spec).

### Controls Row
Two version-select dropdowns, **"From"** and **"To"**, populated from the strategy version registry. A **"Compare"** button triggers the fetch — dropdown changes alone do not fire a request.

### Comparison Table

| Metric | Source field |
|--------|-------------|
| Trades Compared | `trade_count` |
| Win Rate | `win_rate` — formatted `XX.X%` |
| Average R | `avg_R` — formatted `X.XXR` |
| Compliance Rate | **pending** — `strategy_version_comparison_contract.md` v0.1.0 has no `compliance_rate` field yet (flagged gap, design source §3); renders `—` with tooltip `"Not yet available"` until the contract adds it |

Three columns: Metric | `{version_from}` | `{version_to}`.

### Comparison Summary Strip

Below the table: `win_rate_delta`, `avg_R_delta`, `trade_count_delta` as signed values (e.g. `+0.05`, `-0.12R`) with directional colour (green = improvement, red = degradation, matching `performance_delta`'s sign convention), plus the `assessment` value (`Improved` / `Degraded` / `Insufficient data`) as a badge.

### States

| State | Trigger | Behaviour |
|-------|---------|-----------|
| Idle | Initial load | Controls row only; `"Select two strategy versions to compare."` |
| Loading | Compare clicked | Skeleton rows; Compare button disabled |
| Loaded | 200 | Table + summary strip populated |
| Insufficient data | 422 `insufficient_data` | Table replaced with `"Not enough trades to compare — {version} has {trade_count} trades (minimum 10 required)."` |
| Version not found | 404 `version_not_found` | Inline error under the offending dropdown: `"Version not found."` |
| Invalid order | 400 `version_order_error` | Inline error under "To" dropdown: `"Must be chronologically after the 'From' version."` |
| Error | Network/5xx | `"Unable to load comparison. Please try again."` + Retry |

### Constraints

Read-only — no strategy-modification or live-position-modification action available from this tab (contract §13 binding conditions 2, 4, 5). No trade-volume gate on the feature itself (PO decision, `decisions--2026-07-21__release-v7.7.md`); the 10-trade minimum is the contract's own `insufficient_data` threshold.

---

## 7.6 Backtest Rule Change Tab (v0.6 — ST-07, EPIC-02, BLG-FEAT-89, v8.9)

**Design source:** docs/design/2026-08-17__release-v8.9/in-app-backtesting-engine/ux_spec.md

> **§13 Compliance:** Deterministic simulation (same backtest logic class already used by §3–§7's Benchmark tab, applied to a candidate rule set) over historical data — no ML model, no adaptive inference. Output is comparative statistical context for a human decision; nothing here writes to `strategy_rules.md` or any live rule configuration.

Runs a candidate `strategy_rules.md` change against historical data from inside the app — no external script step — and compares the result against the current live rule set.

### Left Panel — Candidate Rule Input

Text input for the candidate rule change (raw diff vs. structured parameter form deferred to implementation — see design source §2.1). **"Run Backtest"** button (primary), disabled while a run is in progress; inline spinner + `"Running backtest…"` label during execution.

### Right Panel — Results (shown after a run completes)

| Element | Content |
|---------|---------|
| Win rate | Candidate vs. live rule set, side-by-side percentages |
| R-multiple distribution | Histogram, candidate overlaid against live (reuse existing distribution chart styling used elsewhere on this page) |
| Max drawdown | Candidate vs. live, side-by-side |
| Run metadata | Timestamp, rule diff summary, run initiator |

### Run History

Collapsible list below the results panel, most-recent-first, each entry expandable to re-view its stored output without re-running. Satisfies the audit requirement (what was tested, when, by what rule diff) without a separate page.

### States

| State | Trigger | Behaviour |
|-------|---------|-----------|
| Empty | Initial load, no run yet | `"Paste a candidate rule change and run a backtest to compare it against your live strategy."` — no chart/table shown |
| Running | Run Backtest clicked | Button disabled, spinner + `"Running backtest…"` |
| Loaded | Run complete | Results panel populated; run appended to Run History |
| Error | Backend failure | `"Backtest failed to complete. Please try again."` + Retry |

### Constraints

Read-only comparative output — adopting a rule change remains a separate, manual, human-authored edit to `strategy_rules.md` outside this feature's scope. No new metric definitions introduced (win rate / R-multiple / drawdown are existing canonical metrics already computed by the Benchmark tab).

---

## 8. States

| State | Behaviour |
|-------|-----------|
| No data imported | Empty state (§4); filter bar hidden |
| Loading | Skeleton placeholders per panel |
| Data, no live trades | Panels render; actual columns show `—` |
| Data with live trades | Full render |
| Filter — no results | "No data for selected period" per panel |
| Import error (toast) | Error toast "Import failed — check CSV paths"; page data unchanged |

---

## 9. API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /strategy/benchmark/import` | Import backtest CSV data |
| `GET /strategy/benchmark/summary` | Fetch stat cards + chart data |
| `GET /strategy/benchmark/trades` | Fetch trade log records |
| `GET /strategy/benchmark/open-positions` | Fetch open positions with unrealized P&L (Panel 0 — v0.2/ST-08) |
| `GET /analytics/strategy-version-comparison` | Fetch version comparison data (§7.5 — v0.4/ST-01); pre-authored contract, see `strategy_version_comparison_contract.md` |

All endpoints must be documented in `docs/reference/openapi.yaml` and `docs/specs/api_contracts/` in the same commit as implementation (per CLAUDE.md §2), with `backend/routers/test.py` registration for `GET /strategy/benchmark/open-positions` and `GET /analytics/strategy-version-comparison`.

---

## 10. Accessibility

- Toggle segmented control: each option is a `<button>` or `role="radio"` within a `role="radiogroup"`
- Table: standard `<table>` with `<th>` headers; `scope="col"` on column headers
- Empty state: announced by screen reader on page load

---

## 11. Change Log

| Version | Date | Change |
|---------|------|--------|
| 0.6 | 2026-08-17 | v8.9 design gate — ST-07 (EPIC-02, BLG-FEAT-89): added §7.6 Backtest Rule Change tab — third sub-nav tab alongside Benchmark/Version Comparison; candidate rule input, results panel (win rate/R-multiple distribution/drawdown vs. live rule set), persisted Run History for audit. §2 Sub-navigation updated to three-tab bar. Design source: in-app-backtesting-engine/ux_spec.md. Approved: Product Owner 2026-08-17. Design gate: 2026-08-17__release-v8.9. Head of Specs Team confirmed. |
| 0.5 | 2026-07-29 | ST-19 (EPIC-05, v7.10, BLG-FE-106): §2 Page Header consolidation resolved — `StrategyBenchmark.js` now renders via the shared `PageHeader` component (was a hand-rolled header, noted as a deviation since v0.3). `BarChart2` icon and last-updated line preserved as adjacent elements. `tests/e2e/heading-light-theme-contrast.spec.js` SC-HTC-03/04 rewritten for the new gradient-clipped title (technique already established for other `PageHeader` pages). New Playwright coverage: `tests/e2e/strategy-benchmark.spec.js` SC-SB-08a–e. |
| 0.4 | 2026-07-21 | v7.7 design gate — ST-01 (EPIC-01, BLG-FEAT-75): added §7.5 Version Comparison tab (SI-04) — two-tab sub-nav ("Benchmark" / "Version Comparison"), version-select controls, comparison table + summary strip against `GET /analytics/strategy-version-comparison`, all states. §9 API Endpoints updated. Placement chosen over `Arc5ComplianceSection` embed to avoid an unscheduled dependency on `BLG-FE-59` (see design source §2). Flagged (not blocking): pre-authored contract v0.1.0 lacks a `compliance_rate` field required by the AC — Sprint Execution follow-up. Design source: si04-strategy-version-comparison/ux_spec.md. Approved: Product Owner 2026-07-21. Design gate: 2026-07-21__release-v7.7. Head of Specs Team confirmed. |
| 0.3 | 2026-07-12 | v7.0 design gate — Page-title light-theme contrast fix (ST-08, BLG-FE-95): `text-white` → `text-slate-900 dark:text-white` on the "Strategy Benchmark" `<h1>` (light-mode value was missing entirely; ~1.1:1 fail). Same defect class as BLG-FE-87/88, extended to primary heading text. Noted (not resolved, out of scope): shipped header is a hand-rolled `<h1>`, not the `PageHeader` component named in §2 — pre-existing spec/implementation deviation, candidate follow-up. No layout change. Design source: `docs/design/2026-07-12__release-v7.0/heading-light-theme-contrast/decision_record.md`. Head of UX & Design sign-off: 2026-07-12. Head of Specs Team confirmed. |
| 0.2 | 2026-07-02 | v6.4 EPIC-03 ST-08 (BLG-FEAT-54). Added §4.5 Panel 0 — Open Positions (header/summary, table columns, Market-only filter interaction, realized-metric isolation hard rule, states, `backtest_open_positions` replace-on-import data source). §3 filter bar note updated with Panel 0 Year-filter exception. §9 API Endpoints: added `GET /strategy/benchmark/open-positions`. Design source: open-positions-panel/ux_spec.md. Design Gate cleared: Head of UX & Design, Product Owner — 2026-07-02. Head of Specs Team confirmed. |
| 0.1 | 2026-06-26 | Initial spec — v6.3 EPIC-03 ST-11. Covers full page layout: sticky filter bar, empty state, Panel 1 (stat cards + PnL bar chart), Panel 2 (yearly breakdown table), Panel 3 (trade log with 3 toggle modes and exit reason badges). Design source: strategy-benchmark-page/ux_spec.md. Approved: Product Owner 2026-06-26. Head of Specs Team confirmed. |
