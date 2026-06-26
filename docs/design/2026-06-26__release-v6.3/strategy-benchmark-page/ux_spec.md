**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-06-26
**Cycle:** 2026-06-26__release-v6.3
**Story:** ST-11 (BLG-FEAT-53)
**Approved by:** Product Owner — 2026-06-26

---

# UX Spec — Strategy Benchmark Page

## Purpose

A single page allowing the user to compare their live trading performance against the production strategy's backtest output. Answers the question: "Am I trading this strategy, and how does my execution compare to the backtest?"

---

## Navigation

- Route: `/strategy/benchmark`
- Navigation label: **"Strategy Benchmark"** — added to main navigation under or alongside Reports/Analytics
- Navigation icon: `BarChart3` (Lucide) — consistent with analytics-adjacent pages

---

## Page Layout

```
┌─────────────────────────────────────────────────────┐
│  Page Header: "Strategy Benchmark"                  │
│  Sub-label: "Compare live trading vs backtest"      │
│  Last updated: "Benchmark data as of DD Mon YYYY"   │
├─────────────────────────────────────────────────────┤
│  [Sticky Filter Bar]                                │
│  Year: [All ▾] [2018] [2019] ... [2026]             │
│  Market: [All ▾] [UK] [US]                          │
├─────────────────────────────────────────────────────┤
│  Panel 1: Performance Parity                        │
│  ┌─────────────┐ ┌─────────────┐                   │
│  │  Backtest   │ │   Actual    │                    │
│  │  stat cards │ │  stat cards │                    │
│  └─────────────┘ └─────────────┘                   │
│  PnL Bar Chart (grouped by year)                    │
├─────────────────────────────────────────────────────┤
│  Panel 2: Yearly Breakdown Table                    │
├─────────────────────────────────────────────────────┤
│  Panel 3: Trade Log                                 │
│  Toggle: [Backtest only] [Actual only] [Side-by-side]│
│  Trade table with exit reason badges                │
└─────────────────────────────────────────────────────┘
```

---

## Sticky Filter Bar

Positioned below the page header. Remains visible while scrolling.

| Filter | Control | Options |
|--------|---------|---------|
| Year | Pill/tab selector | All \| 2018 \| 2019 \| 2020 \| 2021 \| 2022 \| 2023 \| 2024 \| 2025 \| 2026 (dynamically derived from data) |
| Market | Pill/tab selector | All \| UK \| US (or markets present in data) |

- Both filters apply simultaneously to all three panels
- Default: Year = All, Market = All
- Active filter pill: filled background (consistent with existing pill-tab pattern in the app)

---

## Panel 1 — Performance Parity

### Stat Cards (Side-by-Side)

Two column layout: Backtest column (left) | Actual column (right).

Each column shows 4 stat cards:

| Metric | Backtest Label | Actual Label | Actual Empty State |
|--------|---------------|--------------|-------------------|
| Win Rate | "Backtest Win Rate" | "Actual Win Rate" | "—" |
| Average R | "Backtest Avg R" | "Actual Avg R" | "—" |
| Total PnL | "Backtest PnL" | "Actual PnL" | "—" |
| Trade Count | "Backtest Trades" | "Actual Trades" | "0" |

**Empty state rule:** When no live trades exist for the selected period, Actual stats show "—" (not "0", except Trade Count which shows "0"). Do not show a zero that implies the user made zero profit — show absence.

Column header labels:
- Left: **"Backtest"** — muted badge
- Right: **"Actual"** — muted badge

### PnL Bar Chart

Grouped bar chart — one group per year, two bars per group (backtest PnL | actual PnL).

| Element | Spec |
|---------|------|
| Backtest bar colour | `#6B7280` (slate) |
| Actual bar colour | `#22C55E` (green) for profit / `#EF4444` (red) for loss |
| Year axis | X-axis labels, rotated 45° on mobile |
| PnL axis | Y-axis, GBP, auto-scaled |
| Legend | Inline below chart: ▪ Backtest ▪ Actual |
| Empty/no data | "No data for selected period" placeholder |
| Tooltip on hover | "Year: [year] / Backtest: £X / Actual: £X (or N/A)" |

When Year filter is set to a single year: chart collapses to a simple two-bar comparison (Backtest vs Actual) — not grouped by year.

---

## Panel 2 — Yearly Breakdown Table

Scrollable table. Columns:

| Column | Format | Notes |
|--------|--------|-------|
| Year | 4-digit integer | Row per year in data |
| BT Trades | Integer | Backtest trade count |
| Actual Trades | Integer | Live trade count; "—" if none |
| BT Win Rate | X% (1dp) | — |
| Actual Win Rate | X% (1dp) | "—" if no live trades |
| BT Avg R | ±X.XX R | Signed, 2dp |
| Actual Avg R | ±X.XX R | "—" if no live trades |
| BT PnL | £X,XXX | GBP, no dp needed |
| Actual PnL | £X,XXX | "—" if no live trades |

**"—" rule:** All actual columns show "—" (not 0) when no live trades exist for that year.

**Total row:** Bottom row labelled "All years" — aggregated values for each column. Actual aggregates only over years with live data.

---

## Panel 3 — Trade Log

### Toggle Mode Selector

Three-way toggle above the table:

```
[ Backtest only ]  [ Actual only ]  [ Side-by-side ]
```

- Default: **Backtest only**
- Toggle style: segmented control (consistent with existing multi-option toggles in the app)

### Trade Table Columns

| Column | Present in | Format |
|--------|-----------|--------|
| Source | Side-by-side only | "BT" / "Live" badge |
| Ticker | All | String |
| Entry Date | All | DD Mon YYYY |
| Exit Date | All | DD Mon YYYY |
| Exit Reason | All | Badge — see badge spec below |
| Entry Price | All | £X.XX |
| Exit Price | All | £X.XX |
| PnL | All | ±£X.XX, profit/loss colour |
| R-Multiple | All | ±X.XXR; "N/A" if no stop |

### Exit Reason Badges

Consistent with existing badge language (Positions/Signals pages):

| Exit Reason | Badge Label | Colour |
|-------------|------------|--------|
| Stop | **Stop** | Red (`#DC2626` bg, white text) |
| Risk-Off | **Risk-Off** | Amber (`#D97706` bg, white text) |
| Rebalance | **Rebalance** | Teal (`#0D9488` bg, white text) |
| Other / unknown | Text uppercased | Slate default |

### Side-by-Side Mode Layout

When Side-by-side is selected, the table interleaves rows:
- Backtest trade for a given period shown first (shaded subtle)
- Matching actual trade (if any) shown immediately below (unshaded)
- If no actual trade matches: actual row shows "No matching live trade" with "—" for all metrics

---

## Empty State (No Import Data)

When no benchmark data has been imported yet:

```
┌─────────────────────────────────────────────────────┐
│  📊                                                 │
│  No benchmark data imported yet                     │
│  Run import_backtest.py to load strategy data.      │
│                                                     │
│  python import_backtest.py                          │
│  (calls POST /strategy/benchmark/import)            │
└─────────────────────────────────────────────────────┘
```

- Centred in the content area
- Code block showing the CLI command
- No error styling — this is an expected first-run state

---

## "Last Updated" Timestamp

Below the page header, above the filter bar:

- Label: `"Benchmark data as of DD Mon YYYY"` — muted, small
- Source: most recent `import_date` from the benchmark data
- Absent when no data imported

---

## States Summary

| State | Behaviour |
|-------|-----------|
| No data | Empty state with import instructions |
| Loading | Skeleton placeholders per panel |
| Data present, no live trades | Panels render; Actual columns show "—" throughout |
| Data present with live trades | Full render |
| Filter returns no data | "No data for selected period" per panel |
| Import API error | Toast error "Import failed — check CSV paths"; page stays |

---

## Constraints

- No automated import on page load — data is populated via the CLI script only
- All data is read-only; no trade entry or editing from this page
- Badge colours must match exactly the values used on Positions/Signals pages to ensure visual consistency
- §13 does not apply — this page displays historical trade and strategy data, not AI advisory content
