**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 5)
**Status:** Active
**Last Updated:** 2026-09-28
**Cycle:** 2026-09-28__release-v9.8
**Story:** ST-01 (BLG-FE-184)

# ST-01 — Formatting Helper Migration: Scope & Allow-List

## Scope rule applied

`src/lib/format.js` (`formatCurrency`, `formatPercent`, `formatR`) governs display of **trading-domain money, percentage, and R-multiple figures** per `design_system.md` v1.21 §Number and Currency Formatting. This migration pass covers every `toFixed(`/`toLocaleString(` call site outside `src/lib/format.js` and applies one of three dispositions:

1. **Migrated** — call site renders a trading-domain money/%/R value directly as user-facing text (JSX text node, print/export HTML template, CSV export). Replaced with the shared helper.
2. **Allow-listed (this document)** — call site is a trading-domain money/%/R value, but migrating it would break something else. Reasoned exceptions below.
3. **Out of scope, no listing required** — call site is not a money/percentage/R-multiple value at all (dates, ratios without a defined convention such as Sharpe ratio/profit factor/risk-reward-ratio/FX rate, durations in days/weeks/ms, trade/streak counts, fractional share quantities, system-health operational percentages such as API success rate or response time). These are not "money/percentage/R formatting call sites" under the AC and are left unchanged.

## Allow-listed call sites (trading-domain money/%/R, deliberately not migrated)

| File:Line | Value | Reason |
|---|---|---|
| `src/pages/PerformanceAnalytics.js:399` | `winRate` (monthly heatmap data prep) | Feeds `MonthlyHeatmap` as a numeric-shaped chart data field; the helper returns a string with a trailing `%`, which would corrupt chart consumption. The heatmap's own display cell (`MonthlyHeatmap.js`) is migrated separately at its own render call site. |
| `src/pages/PerformanceAnalytics.js:421` | `winRate` (market comparison data prep) | Same reason — feeds `MarketComparison` as data; display migrated at that component's own render site. |
| `src/pages/PerformanceAnalytics.js:499` | `winRate` (cohort/monthly data prep) | Same reason. |
| `src/pages/Screener.js:270` | `WatchlistPopover` default price input value | Feeds an editable numeric text input's initial value, not display text — the helper's formatted string (currency symbol, grouping) is not valid input-field content. |
| `src/components/reports/PortfolioGrowthChart.js:105` | Y-axis tick formatter (portfolio value) | Abbreviated `£1.2k` notation for compact axis space; the shared helper has no abbreviation mode (same treatment as the abbreviated market-cap convention). |
| `src/components/dashboard/widgets/CurrentDrawdownWidget.js:102-105` (`formatPeak`) | Peak portfolio value, abbreviated | Abbreviated `£X.XXM` / `£X.XK` notation for a compact stat-card readout; the shared helper has no abbreviation mode. |
| `src/components/charts/PortfolioChart.js:84` | Y-axis tick formatter (portfolio value) | Abbreviated `£Xk` notation; same reasoning as the two rows above. |

*(Additional rows are appended below as the migration pass covers each file — see individual story commits and this file's own edit history for the running list.)*

## Out-of-scope categories (representative, not exhaustive)

- Ratios with no defined design-system convention: Sharpe ratio, recovery factor, profit factor (raw, unprefixed), risk/reward ratio (`X:1`), FX conversion rate.
- Durations: avg hold time (days), trade frequency (per week), API response time (ms).
- Dates/timestamps: `toLocaleString()` on `Date` objects.
- Counts: win/loss streak (trades).
- Fractional share quantities (`toFixed(4)` shares).
- System-health/operational percentages not tied to trading P&L (e.g. `SystemStatus.js` test success rate).
- **Operational/infrastructure cost amounts not tied to trading P&L, position value, or price** — e.g. AI/Claude API spend (`src/components/charts/AiSpendTrendChart.js:33`, `src/pages/Settings.js:453`, both USD). Ruling (engine-classified, ST-01, applying the existing system-health/operational carve-out above — that carve-out already exempts *percentages* describing system/infra health rather than trading outcomes; this extends the same non-trading-domain reasoning to a *cost amount* describing infra spend rather than trading outcomes): these are not "trading-domain money" under the AC's scope rule (§ above — money/%/R governed by `design_system.md` v1.21 is scoped to trading P&L, positions, and prices) and are left unmigrated, consistent with how `SystemStatus.js` response-time/success-rate figures are already treated. Not escalated as a `delegated_decision` — this is a direct application of the scope rule already stated at the top of this document, not a new precedent.
