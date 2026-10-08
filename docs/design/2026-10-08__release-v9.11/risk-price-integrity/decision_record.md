**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-08__release-v9.11
**Stories:** ST-10 (EPIC-02, BLG-BE-154), ST-11 (EPIC-02, BLG-FE-206), ST-13 (EPIC-02, BLG-BE-155)

# Decision Record — Price Integrity on the Risk Dashboard Position Table and Dashboard

## 1. Problem

The Position Risk table (`PositionRiskTable.js`, `risk_dashboard.md` §6) shows several things the system does not actually do:

- **Fabricated prices (ST-10).** When the live price fetch fails, `GET /portfolio` falls back to `stored × 1.38` for US positions. The user sees an invented GBP price with nothing to say it is not live.
- **Mixed currencies (ST-11).** Entry Price is formatted in the market's native currency ("$"), while Current is GBP. The column header says nothing, so a US row compares dollars with pounds.
- **Grace stops look enforced (ST-11).** A GRACE position's stop is not enforced (`strategy_rules.md` §6), but the table shows its Stop Price and colours Stop Dist % rose or amber as if it were live risk.
- **Wrong stop distance for US positions (ST-13).** Stop Dist % is computed in the browser from GBP figures. Those figures mix entry and live FX, so the percentage drifts with FX rather than with price.

## 2. Decision

### 2.1 Stale price marker (ST-10)

**Risk Dashboard, Position Risk table:** when `price_is_stale = true`, the Current Price cell shows the price followed by a small amber marker:

- Icon `Clock` (lucide, `w-3.5 h-3.5`, `text-amber-400`), then the word "stale" in `text-xs text-amber-400`.
- `data-testid="price-stale-marker"`.
- Tooltip and `aria-label`: **"Live price unavailable. Showing the last stored price converted at today's FX rate."**
- When `price_is_stale` is false, missing or null, nothing is shown, so older responses still render.

**Dashboard (Card 2 — Portfolio Heat, which already reads `GET /portfolio`):** when one or more open positions have `price_is_stale = true`, an extra amber sub-line appears under the heat value:

- **"⚠ {N} position price(s) stale"** in `text-xs text-amber-400`, with `data-testid="dashboard-price-stale-notice"`.
- Same tooltip text as above.
- It does not change the heat colour coding or the click target (`/risk`, where the per-row markers are).

Amber is the established "may be outdated" tone (Analytics Staleness Indicator, Screener stale advisory). No new colour.

### 2.2 GBP entry prices (ST-11)

- Entry Price renders in GBP: `formatCurrency(entry_price)` with the GBP value `GET /portfolio` returns, the same as Current and Stop. It no longer passes `currencyForMarket`.
- Column headers become **"Entry (GBP)"**, **"Current (GBP)"** (already shipped) and **"Stop (GBP)"**, so every money column states its currency.

### 2.3 Grace stops shown as not enforced (ST-11)

For a row whose `display_status = "GRACE"`:

- **Stop column:** the text **"Not enforced (grace)"** in `text-xs text-slate-600 dark:text-slate-400`, instead of the price.
- **Stop Dist % column:** the same text, in the same neutral tone. No rose or amber distance colour.
- Tooltip on both cells: **"Stops are not enforced during the 10-day grace period. See strategy rules §6."**
- `data-testid="stop-not-enforced"` on each cell.
- **Sort:** GRACE rows keep the first status group (§6.4). Within that group, the "smallest distance first" rule does not apply, so they sort by `grace_days_remaining` ascending, the same as the Grace Period panel.

### 2.4 Stop distance from the API (ST-13)

- Stop Dist % shows `stop_distance_pct` from `GET /portfolio`, which the backend computes in native currency. The browser no longer derives it.
- Format: 1 decimal place followed by "%". Colour thresholds unchanged: ≤ 5% rose, ≤ 15% amber, otherwise default text.
- If `stop_distance_pct` is null, the cell shows "—".
- Grace rows follow §2.3, not this rule.

## 3. §13 Compliance

Display-only and deterministic. No AI. Removing the ×1.38 fallback removes a fabricated value. Showing grace stops as not enforced makes the display match `strategy_rules.md` §6.

## 4. Frontend Spec Impact

- `risk_dashboard.md` v0.1.11 → v0.1.12: §6.1 Data, §6.2 Display, §6.4 Sort Order, and a new §6.6 Stale Price Marker.
- `dashboard.md` v3.7 → v3.8: §4 Card 2 — Portfolio Heat, stale-price sub-line.

## 5. Obligations for Sprint Execution

- **ST-10** adds `price_is_stale` (boolean) per position to `GET /portfolio`. ST-13 adds `stop_distance_pct` (number, nullable). Both are documented in `portfolio_endpoints.md` and `docs/reference/openapi.yaml` in the same commit (CLAUDE.md §2). Neither adds a route.
- **ST-11 and ST-13** each update `risk_dashboard.md` §6 as their ACs require. This gate has already written the target text, so the stories confirm it against what ships and fix any difference.

## 6. Testability (CLAUDE.md §2)

Playwright, mocked `GET /portfolio`:

1. ST-10: a position with `price_is_stale: true` shows `price-stale-marker` on the Risk Dashboard and `dashboard-price-stale-notice` on the Dashboard. A position with `false` shows neither.
2. ST-11: a US row's Entry cell starts with "£" and shows the GBP value from the mock.
3. ST-11: a GRACE row shows "Not enforced (grace)" in the Stop and Stop Dist % cells, with no `text-rose-400` or `text-amber-400` class.
4. ST-13: the Stop Dist % cell shows the mock's `stop_distance_pct`, for example `8.0%`, not a value derived in the browser.

## 7. Approval

Head of UX & Design: confirmed, 2026-10-08.
Product Owner: confirmed, 2026-10-08.
