# Test Scenarios — Quick Wins Bundle

**Owner:** QA & Testing Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-02-27
**Derived from:**
- `docs/specs/metrics_definitions.md` v1.5.8
- `docs/specs/api_contracts/portfolio_endpoints.md` v1.8.2
- `docs/specs/api_contracts/position_endpoints.md` v1.8.3
- `docs/specs/api_contracts/trade_endpoints.md` v1.8.4
- `docs/specs/api_contracts/analytics_endpoints.md` v1.8.1
- `docs/specs/frontend/pages/dashboard.md` v1.1
- `docs/specs/frontend/pages/trade_history.md` v1.1
- `docs/specs/frontend/pages/analytics.md` v1.2
- `docs/specs/frontend/pages/positions.md` v1.2
- `docs/product/scope/scope--QWB-quick-wins-bundle.md`
**For verification by:** QA Lead

---

## Coverage Map

| Scenario ID | Feature | Acceptance Criterion | Type |
|-------------|---------|----------------------|------|
| B-01 | BLG-FEAT-01 | GET /portfolio returns both new fields | Backend |
| B-02 | BLG-FEAT-01 | Drawdown calculation correct | Backend |
| B-03 | BLG-FEAT-01 | Zero default when no portfolio_history | Backend |
| B-04 | BLG-FEAT-06 | GET /positions returns grace_days_remaining | Backend |
| B-05 | BLG-FEAT-06 | Derivation formula correct (in grace) | Backend |
| B-06 | BLG-FEAT-06 | Null when not in grace period | Backend |
| B-07 | BLG-FEAT-06 | Field always present — never omitted | Backend |
| B-08 | BLG-FEAT-07 | CSV endpoint returns correct status and headers | Backend |
| B-09 | BLG-FEAT-07 | CSV column order and count correct | Backend |
| B-10 | BLG-FEAT-07 | Null fields serialised as empty string | Backend |
| B-11 | BLG-FEAT-07 | Tags serialised as semicolon-separated string | Backend |
| B-12 | BLG-FEAT-07 | Empty trade history returns header row only | Backend |
| B-13 | BLG-FEAT-07 | Error response is JSON not CSV | Backend |
| F-01 | BLG-FEAT-01 | Widget present in Dashboard stats row | Frontend |
| F-02 | BLG-FEAT-01 | Establishing Peak state | Frontend |
| F-03 | BLG-FEAT-01 | At Peak state | Frontend |
| F-04 | BLG-FEAT-01 | In Drawdown state — all fields displayed | Frontend |
| F-05 | BLG-FEAT-01 | Progress bar renders when in drawdown | Frontend |
| F-06 | BLG-FEAT-01 | Progress bar absent when max_drawdown is zero | Frontend |
| F-07 | BLG-FEAT-01 | No fallback data source | Frontend |
| F-08 | BLG-FEAT-02 | R-multiple column present in trade table | Frontend |
| F-09 | BLG-FEAT-02 | R-multiple calculation correct | Frontend |
| F-10 | BLG-FEAT-02 | Em dash for trades without stop_price | Frontend |
| F-11 | BLG-FEAT-02 | Display format: signed, 2dp, R suffix | Frontend |
| F-12 | BLG-FEAT-02 | Column sortable; em-dash values sort to end | Frontend |
| F-13 | BLG-FEAT-06 | Grace column present in open positions table | Frontend |
| F-14 | BLG-FEAT-06 | Correct display format when in grace | Frontend |
| F-15 | BLG-FEAT-06 | Dash/hidden when null | Frontend |
| F-16 | BLG-FEAT-04 | Best/Worst Trades component present | Frontend |
| F-17 | BLG-FEAT-04 | Ranking by R-multiple correct | Frontend |
| F-18 | BLG-FEAT-04 | Trades without stop_price excluded | Frontend |
| F-19 | BLG-FEAT-04 | Card contents complete | Frontend |
| F-20 | BLG-FEAT-04 | Partial panel when fewer than 3 qualifying trades | Frontend |
| F-21 | BLG-FEAT-04 | Empty state when no qualifying trades | Frontend |
| F-22 | BLG-FEAT-05 | Win Rate chart renders on Analytics page | Frontend |
| F-23 | BLG-FEAT-05 | Chart source and axes correct | Frontend |
| F-24 | BLG-FEAT-05 | 50% reference line present | Frontend |
| F-25 | BLG-FEAT-05 | Per-bar colour coding correct | Frontend |
| F-26 | BLG-FEAT-05 | Tooltip content correct (trade_count field) | Frontend |
| F-27 | BLG-FEAT-05 | Component absent when monthly_data empty | Frontend |
| F-28 | BLG-FEAT-07 | CSV export button present on Trade History | Frontend |
| F-29 | BLG-FEAT-07 | Button triggers download | Frontend |
| R-01 | Regression | Existing GET /portfolio fields unaffected | Regression |
| R-02 | Regression | Existing GET /positions fields unaffected | Regression |
| R-03 | Regression | GET /trades unaffected | Regression |
| R-04 | Regression | Dashboard existing stats cards unaffected | Regression |
| R-05 | Regression | Trade History page existing functionality unaffected | Regression |

---

## BACKEND SCENARIOS

---

## B-01 — GET /portfolio returns both new drawdown fields

**Acceptance criterion:** `GET /portfolio` returns `current_drawdown_percent` (float, ≤0.0) and `peak_portfolio_value` (float, GBP) on every response.
**Derived from:** `portfolio_endpoints.md` v1.8.2 §GET /portfolio field notes
**Type:** Backend

**Setup:**
Portfolio with at least one `portfolio_history` snapshot on record.

**Steps:**
1. Call `GET /portfolio`
2. Inspect the response `data` object

**Expected result:**
- HTTP 200
- `data.current_drawdown_percent` is present and is a float ≤ 0.0
- `data.peak_portfolio_value` is present and is a positive float (GBP)
- Both fields are present at the top level of `data`, not nested

**Notes:**
Verify via direct API call, not by reading the frontend display. Check field names match the contract exactly — no aliases.

---

## B-02 — Drawdown calculation correctness

**Acceptance criterion:** `current_drawdown_percent` is correctly calculated as `(total_value − peak) / peak × 100` against the all-time peak from `portfolio_history`.
**Derived from:** `portfolio_endpoints.md` v1.8.2; `metrics_definitions.md` v1.5.8 §Current Drawdown
**Type:** Backend

**Setup:**
Portfolio with known `portfolio_history` snapshots. Identify the maximum `total_value` across all snapshots (the expected peak). Know the current `total_value`.

**Steps:**
1. Query `GET /portfolio/history` to obtain all snapshots and identify `peak_value = MAX(total_value)`
2. Note current `total_value` from `GET /portfolio`
3. Calculate expected drawdown: `(total_value − peak_value) / peak_value × 100`
4. Call `GET /portfolio`
5. Compare `data.current_drawdown_percent` against the calculated expected value

**Expected result:**
- `data.current_drawdown_percent` matches the hand-calculated value within floating-point tolerance (±0.1 percentage points)
- Result is ≤ 0.0 when portfolio is below peak
- Result is 0.0 when portfolio equals peak
- `data.peak_portfolio_value` matches the identified peak value

**Notes:**
The peak must be drawn from ALL portfolio_history snapshots (all-time, not period-scoped). If the current `total_value` equals or exceeds any historical snapshot, `current_drawdown_percent` should be 0.0.

---

## B-03 — Zero defaults when no portfolio_history exists

**Acceptance criterion:** Both new fields are present and return `0.0` when no `portfolio_history` records exist.
**Derived from:** `portfolio_endpoints.md` v1.8.2 field notes; `metrics_definitions.md` v1.5.8 §Failure Behaviour
**Type:** Backend

**Setup:**
Portfolio with no `portfolio_history` records. This may require a clean portfolio or testing environment — do not use production data.

**Steps:**
1. Confirm `GET /portfolio/history` returns `[]` (empty array)
2. Call `GET /portfolio`
3. Inspect `data.current_drawdown_percent` and `data.peak_portfolio_value`

**Expected result:**
- `data.current_drawdown_percent` is `0.0`
- `data.peak_portfolio_value` is `0.0`
- Both fields are present — not omitted, not null

**Notes:**
This is the Establishing Peak condition. The spec defines 0.0 as the sentinel value, not null. If the field is missing or null, this is a defect.

---

## B-04 — GET /positions returns grace_days_remaining on every position object

**Acceptance criterion:** `GET /positions` returns `grace_days_remaining` on every position object; field is always present.
**Derived from:** `position_endpoints.md` v1.8.3 §GET /positions
**Type:** Backend

**Setup:**
Portfolio with at least two open positions — one in grace period (entry within last 10 days) and one post-grace (entry more than 10 days ago).

**Steps:**
1. Call `GET /positions`
2. Inspect every object in the response `data` array

**Expected result:**
- Every position object contains the key `grace_days_remaining`
- The field is never absent — not even for the post-grace position
- The post-grace position has `grace_days_remaining: null`
- The in-grace position has a non-null integer value

**Notes:**
Check all position objects in the response, not just the first. The field must be present (even if null) on every object.

---

## B-05 — grace_days_remaining derivation formula

**Acceptance criterion:** Value is `max(0, 10 − holding_days)` when `grace_period = true`.
**Derived from:** `position_endpoints.md` v1.8.3 §grace_days_remaining field notes
**Type:** Backend

**Setup:**
Open positions with known `holding_days` values while in grace period (day 0–9).

**Steps:**
1. For a position with `holding_days = 0`: call `GET /positions`, verify `grace_days_remaining = 10`
2. For a position with `holding_days = 5`: verify `grace_days_remaining = 5`
3. For a position with `holding_days = 9`: verify `grace_days_remaining = 1`
4. For a position exactly at `holding_days = 10` (first day post-grace): verify `grace_days_remaining = null`

**Expected result:**
- Day 0: `grace_days_remaining = 10`
- Day 5: `grace_days_remaining = 5`
- Day 9: `grace_days_remaining = 1`
- Day 10: `grace_days_remaining = null` (grace period ended)

**Notes:**
The formula `max(0, 10 − holding_days)` means day 10 produces `max(0, 0) = 0`; however the spec states null when `grace_period = false`. Confirm whether day 10 triggers `grace_period = false` in the existing codebase — per `implementation_notes.md`, grace is `holding_days < 10`, so day 10 is post-grace and `grace_days_remaining = null`. If the API returns 0 instead of null for day 10 this is a defect.

---

## B-06 — grace_days_remaining is null when not in grace period

**Acceptance criterion:** `grace_days_remaining` is null when `grace_period = false`.
**Derived from:** `position_endpoints.md` v1.8.3
**Type:** Backend

**Setup:**
Open position with `holding_days ≥ 10` (post-grace).

**Steps:**
1. Identify a position where `display_status` is `PROFITABLE` or `LOSING` (confirming post-grace)
2. Call `GET /positions`
3. Inspect `grace_days_remaining` for that position

**Expected result:**
- `grace_days_remaining` is `null` (JSON null)
- `grace_period` is `false` on the same object

**Notes:**
Null (not 0, not absent). A value of `0` would be a defect.

---

## B-07 — grace_days_remaining field always present — never omitted

**Acceptance criterion:** Field is always present in every position object regardless of grace state.
**Derived from:** `position_endpoints.md` v1.8.3
**Type:** Backend

**Setup:**
Mixed portfolio with positions in both grace and post-grace states.

**Steps:**
1. Call `GET /positions`
2. For every position object, check whether the key `grace_days_remaining` exists in the JSON

**Expected result:**
- Every position object has the key `grace_days_remaining`
- No position object is missing the key

**Notes:**
Use a JSON inspector or test client. The distinction between `null` value (acceptable) and key absence (defect) must be explicitly checked.

---

## B-08 — CSV endpoint returns correct HTTP status and headers

**Acceptance criterion:** `GET /trades/export/csv` returns HTTP 200 with `Content-Type: text/csv` and `Content-Disposition: attachment; filename="trade_history.csv"`.
**Derived from:** `trade_endpoints.md` v1.8.4 §GET /trades/export/csv
**Type:** Backend

**Setup:**
Portfolio with at least one closed trade.

**Steps:**
1. Call `GET /trades/export/csv` via direct HTTP client (e.g. curl or test harness — not the browser, to inspect raw headers)
2. Inspect response headers

**Expected result:**
- HTTP status: 200
- `Content-Type` header contains `text/csv`
- `Content-Disposition` header is `attachment; filename="trade_history.csv"` (exact value)
- Response body begins with the CSV header row

**Notes:**
Do not rely on the browser's download behaviour to confirm headers — inspect raw HTTP response headers. The `Content-Disposition` value must match exactly.

---

## B-09 — CSV column order and count

**Acceptance criterion:** CSV contains exactly 14 columns in the specified order.
**Derived from:** `trade_endpoints.md` v1.8.4 §CSV columns table
**Type:** Backend

**Setup:**
Portfolio with at least one closed trade.

**Steps:**
1. Call `GET /trades/export/csv`
2. Inspect the first line (header row) of the response body

**Expected result:**
Header row is exactly:
```
ticker,market,entry_date,exit_date,shares,entry_price,exit_price,pnl,pnl_pct,holding_days,exit_reason,tags,entry_note,exit_note
```
- Exactly 14 comma-separated column names
- Column names match the spec exactly (case-sensitive)
- Column order matches the spec exactly
- No additional columns present
- No columns missing

**Notes:**
Count the commas in the header row: should be 13 (14 columns = 13 separators). Any column name deviation or ordering difference is a defect.

---

## B-10 — Null fields serialised as empty string, not "null"

**Acceptance criterion:** Null fields in the CSV are serialised as empty strings.
**Derived from:** `trade_endpoints.md` v1.8.4 §null handling
**Type:** Backend

**Setup:**
At least one closed trade with `entry_note = null` OR `exit_note = null` OR `exit_reason = null`. These fields are nullable in `trade_history`.

**Steps:**
1. Identify a trade with at least one null field (inspect `GET /trades` response)
2. Call `GET /trades/export/csv`
3. Find the data row for that trade
4. Inspect the null field's column value

**Expected result:**
- Null field is represented as empty (nothing between the surrounding commas, or trailing comma)
- The literal string `null` does NOT appear in the CSV
- The literal string `None` does NOT appear in the CSV

**Notes:**
Example: for a trade with `entry_note = null`, the entry_note column in that row should be `,` (empty) not `,null,` or `,None,`.

---

## B-11 — Tags serialised as semicolon-separated string

**Acceptance criterion:** The `tags` column in the CSV uses semicolons to separate multiple tags. Empty array becomes empty string.
**Derived from:** `trade_endpoints.md` v1.8.4 §tags serialisation
**Type:** Backend

**Steps:**
1. Identify a trade with multiple tags (e.g., `["momentum", "breakout"]`) via `GET /trades`
2. Call `GET /trades/export/csv`
3. Find that trade's row, inspect the `tags` column

**Expected result for multi-tag trade:**
- Tags column contains `momentum;breakout` (semicolon-separated, no spaces around semicolon)

**Expected result for trade with empty tags array:**
- Tags column is empty (not `[]` or `null`)

**Notes:**
Check both cases. The semicolon separator must not use commas (which would break CSV parsing) or any other delimiter.

---

## B-12 — Empty trade history returns header row only (HTTP 200)

**Acceptance criterion:** When there are no closed trades, the endpoint returns HTTP 200 with the header row only (not 204, not 404, not an empty body).
**Derived from:** `trade_endpoints.md` v1.8.4 §empty export
**Type:** Backend

**Setup:**
Portfolio with zero closed trades. This requires a clean test environment.

**Steps:**
1. Confirm `GET /trades` returns `total_trades: 0` and `trades: []`
2. Call `GET /trades/export/csv`
3. Inspect response status and body

**Expected result:**
- HTTP 200 (not 204 No Content)
- Response body contains exactly one line: the header row (the 14 column names)
- No data rows follow the header
- Response is not an empty body

**Notes:**
This test requires a portfolio with no exits. Use a separate test portfolio or clean environment. An HTTP 204 response is a defect. An empty body with no header row is a defect.

---

## B-13 — Error response from CSV endpoint is JSON

**Acceptance criterion:** If the endpoint errors, the response body is JSON using the standard error envelope — not a CSV file.
**Derived from:** `trade_endpoints.md` v1.8.4 §errors
**Type:** Backend

**Setup:**
Force an error condition. The most reliable approach: call the endpoint in a state that would trigger an HTTP 500 (e.g., temporarily break the database connection if possible in the test environment, or verify via code inspection that the error handler returns JSON).

**Steps:**
1. If direct error injection is possible: trigger a 500 condition and call `GET /trades/export/csv`
2. Inspect the response body

**Expected result:**
- Response body is valid JSON
- Response body follows standard error envelope: `{"status": "error", "message": "..."}`
- Response body is NOT a CSV-formatted error

**Notes:**
If live error injection is not possible in the verification environment, this scenario may be deferred (mark ⏭). Verify via code review that the router's exception handler returns the standard JSON error envelope rather than a CSV-formatted response. Record evidence of code-level verification in the verification report.

---

## FRONTEND SCENARIOS

---

## F-01 — Current Drawdown widget present in Dashboard stats row

**Acceptance criterion:** Widget appears in the Dashboard Portfolio Summary Cards stats row.
**Derived from:** `dashboard.md` v1.1 §Current Drawdown Widget — Placement
**Type:** Frontend

**Setup:**
Standard portfolio with portfolio_history snapshots and current drawdown present.

**Steps:**
1. Navigate to the Dashboard page
2. Locate the Portfolio Summary Cards stats row
3. Count the cards in the row

**Expected result:**
- A "Current Drawdown" widget (or equivalent label) is visible in the stats row
- It is positioned within the stats row alongside the existing four summary cards
- It is visible on page load without requiring any user interaction

**Notes:**
Confirm the widget is the fifth card in the row, not in a separate section below. Do not infer from page title alone — the widget must be visible in the stats card row.

---

## F-02 — Current Drawdown: Establishing Peak state

**Acceptance criterion:** When `peak_portfolio_value === 0.0`, the widget renders the "Establishing Peak" state and does not show a percentage.
**Derived from:** `dashboard.md` v1.1 §Current Drawdown Widget — Display states; `metrics_definitions.md` v1.5.8 §Failure Behaviour
**Type:** Frontend

**Setup:**
Portfolio with no `portfolio_history` records, so `GET /portfolio` returns `peak_portfolio_value: 0.0`.

**Steps:**
1. Navigate to the Dashboard page
2. Inspect the Current Drawdown widget

**Expected result:**
- Widget displays an "Establishing Peak" message (or equivalent)
- No drawdown percentage is shown
- No progress bar is shown
- Widget does not display an error state — it renders a defined state

**Notes:**
This requires a clean portfolio or test environment with no history snapshots. If the test environment cannot replicate this state, defer and record.

---

## F-03 — Current Drawdown: At Peak state

**Acceptance criterion:** When `current_drawdown_percent === 0`, the widget renders the at-peak state ("🎉 New Peak!").
**Derived from:** `dashboard.md` v1.1 §Display states
**Type:** Frontend

**Setup:**
Portfolio where current `total_value` equals `peak_portfolio_value` — i.e., today is an all-time high.

**Steps:**
1. Navigate to the Dashboard page
2. Confirm via `GET /portfolio` that `current_drawdown_percent` is `0.0`
3. Inspect the Current Drawdown widget

**Expected result:**
- Widget displays "🎉 New Peak!" (or equivalent at-peak message)
- No negative percentage is shown
- No progress bar is shown

**Notes:**
May require portfolio state manipulation. Alternatively verify by directly inspecting the widget component's rendering logic for the `current_drawdown_percent === 0` branch if live environment cannot replicate the state — record evidence.

---

## F-04 — Current Drawdown: In Drawdown state — all fields displayed

**Acceptance criterion:** When in drawdown, widget shows drawdown percentage, days underwater, and progress bar.
**Derived from:** `dashboard.md` v1.1 §Display states
**Type:** Frontend

**Setup:**
Portfolio in drawdown (current value below historical peak). `GET /analytics/metrics` returns a non-zero `advanced_metrics.days_underwater`.

**Steps:**
1. Navigate to the Dashboard page
2. Confirm via `GET /portfolio` that `current_drawdown_percent < 0`
3. Inspect the Current Drawdown widget

**Expected result:**
- A negative drawdown percentage is displayed (e.g., "-3.2%"), formatted to 1 decimal place
- Days underwater count is visible (sourced from `advanced_metrics.days_underwater`)
- Progress bar is visible

**Notes:**
The days underwater value must match `advanced_metrics.days_underwater` from `GET /analytics/metrics` — not a client-side calculation. Verify by cross-referencing the displayed value against the raw API response.

---

## F-05 — Progress bar renders when in drawdown with non-zero max_drawdown

**Acceptance criterion:** Progress bar renders when `current_drawdown_percent < 0` and `advanced_metrics.max_drawdown.percent` is non-zero.
**Derived from:** `dashboard.md` v1.1 §Progress bar
**Type:** Frontend

**Setup:**
Portfolio in drawdown with a non-zero historical max drawdown.

**Steps:**
1. Confirm `GET /analytics/metrics` returns `advanced_metrics.max_drawdown.percent` as a non-zero negative value
2. Navigate to the Dashboard page
3. Inspect the Current Drawdown widget

**Expected result:**
- A progress bar is visible within the widget
- The bar visually represents the current drawdown as a proportion of the max drawdown
- The bar has non-zero fill (since current drawdown > 0% of max drawdown)

---

## F-06 — Progress bar absent when max_drawdown.percent is zero

**Acceptance criterion:** Progress bar does not render when `max_drawdown.percent === 0`.
**Derived from:** `dashboard.md` v1.1 §Progress bar
**Type:** Frontend

**Setup:**
Portfolio in drawdown (negative `current_drawdown_percent`) but `advanced_metrics.max_drawdown.percent` is zero (no completed drawdown cycle yet). This is an edge case that may require environment manipulation.

**Steps:**
1. Confirm `GET /analytics/metrics` returns `advanced_metrics.max_drawdown.percent` as `0` or `0.0`
2. Navigate to the Dashboard page
3. Inspect the Current Drawdown widget

**Expected result:**
- No progress bar is rendered within the widget
- The widget still shows the drawdown percentage and days underwater
- No JavaScript error occurs

**Notes:**
If this exact state cannot be replicated in the verification environment, verify via code inspection of the progress bar rendering guard condition. Record evidence.

---

## F-07 — No fallback data source

**Acceptance criterion:** Widget reads from `GET /portfolio` (drawdown %) and `GET /analytics/metrics` (days_underwater, max_drawdown) only. No fallback path.
**Derived from:** `dashboard.md` v1.1; decisions record D10
**Type:** Frontend

**Setup:**
Standard portfolio.

**Steps:**
1. Open browser developer tools, Network tab
2. Navigate to or refresh the Dashboard page
3. Inspect network requests made on load

**Expected result:**
- The page makes a request to `GET /portfolio` — response includes `current_drawdown_percent` and `peak_portfolio_value`
- The page makes a request to `GET /analytics/metrics` — response includes `advanced_metrics.days_underwater` and `advanced_metrics.max_drawdown.percent`
- No request is made to `GET /portfolio/history` for the purpose of drawdown calculation (the old prototype fallback path)
- The widget does not perform its own drawdown calculation from raw portfolio history

**Notes:**
This test guards against the prototype-era fallback logic (`estimated` / `default` data source modes) being carried forward. The out-of-scope `dataSource` prop and `estimated` calculation path must not be present in the shipped component.

---

## F-08 — R-Multiple column present in Trade History table

**Acceptance criterion:** An R-multiple column is present in the Trade History table.
**Derived from:** `trade_history.md` v1.1 §R-Multiple Column
**Type:** Frontend

**Setup:**
Portfolio with at least one closed trade.

**Steps:**
1. Navigate to the Trade History page
2. Inspect the trade table headers

**Expected result:**
- A column labelled "R" or "R-Multiple" (per spec) is visible in the trade table
- The column is visible without requiring any filter or toggle

---

## F-09 — R-Multiple calculation correct

**Acceptance criterion:** R-multiple is calculated frontend-only using `(exit_price − entry_price) / (entry_price − stop_price)`, sourced from `trades_for_charts` joined by trade `id`.
**Derived from:** `trade_history.md` v1.1; `metrics_definitions.md` v1.5.8 §R-Multiple; `analytics_endpoints.md` v1.8.1 §trades_for_charts
**Type:** Frontend

**Setup:**
At least one closed trade with known `entry_price`, `exit_price`, and `stop_price` values (verify via `GET /analytics/metrics` → `trades_for_charts`).

**Steps:**
1. Call `GET /analytics/metrics` and identify a trade in `trades_for_charts` with all three price fields present: e.g., `entry_price: 55.20`, `exit_price: 70.40`, `stop_price: 48.50`
2. Calculate expected R: `(70.40 − 55.20) / (55.20 − 48.50) = 15.20 / 6.70 = 2.27`
3. Navigate to the Trade History page
4. Find the corresponding row (match by ticker/date)
5. Read the R-multiple value displayed

**Expected result:**
- Displayed R-multiple is `+2.27R` (matching the hand-calculated value)
- Sign is positive for winners, negative for losers

**Notes:**
Tolerance: ±0.01R (rounding to 2dp). Use a trade with a large stop distance to make rounding errors obvious.

---

## F-10 — Em dash for trades without stop_price

**Acceptance criterion:** Trades where `stop_price` is null or zero in `trades_for_charts` display `—` (em dash), not `0`, not blank.
**Derived from:** `trade_history.md` v1.1 §null handling
**Type:** Frontend

**Setup:**
At least one closed trade with `stop_price: null` or `stop_price: 0` in `trades_for_charts` (confirm via `GET /analytics/metrics`).

**Steps:**
1. Call `GET /analytics/metrics` and identify a trade in `trades_for_charts` where `stop_price` is null or 0
2. Navigate to Trade History page
3. Find the corresponding row

**Expected result:**
- R-multiple column for that trade shows `—` (em dash character)
- Does not show `0`, `0.00R`, `NaN`, `undefined`, or empty cell

**Notes:**
The em dash is U+2014. Verify it is not a hyphen-minus (-) or en dash (–).

---

## F-11 — R-Multiple display format

**Acceptance criterion:** R-multiple displays as signed, 2 decimal places, with "R" suffix (e.g., `+2.31R`, `-0.87R`). Positive values use profit colour; negative values use loss colour.
**Derived from:** `trade_history.md` v1.1 §display format
**Type:** Frontend

**Setup:**
Portfolio with at least one winning trade and one losing trade with `stop_price` present.

**Steps:**
1. Navigate to Trade History page
2. Identify a winning trade (positive R) and a losing trade (negative R)
3. Inspect the R-multiple column values and styling

**Expected result:**
- Positive R: formatted as `+X.XXR` with leading plus sign and profit colour (green)
- Negative R: formatted as `-X.XXR` with loss colour (red)
- Both values show exactly 2 decimal places
- "R" suffix is present (uppercase, immediately after the number with no space)

---

## F-12 — R-Multiple column sortable; em-dash values sort to end

**Acceptance criterion:** The R-multiple column is sortable. Trades with `—` sort to the end.
**Derived from:** `trade_history.md` v1.1 §sort behaviour
**Type:** Frontend

**Setup:**
Portfolio with a mix of trades: some with calculable R-multiple and at least one with `—`.

**Steps:**
1. Navigate to Trade History page
2. Click the R-multiple column header to sort ascending
3. Observe sort order

**Expected result:**
- Table sorts by R-multiple value ascending (most negative first)
- Trades displaying `—` appear at the end of the sorted list, after all calculable values
- Click again (descending): sorted most positive first, `—` trades still at end

**Notes:**
Verify that `—` rows are at the end in both ascending and descending sort. They must not sort by the dash character's ASCII value.

---

## F-13 — Grace period indicator column present in Open Positions table

**Acceptance criterion:** A `grace_days_remaining` column (or equivalent) is present in the Open Positions table.
**Derived from:** `positions.md` v1.2 §grace_days_remaining column
**Type:** Frontend

**Setup:**
Portfolio with at least one open position.

**Steps:**
1. Navigate to the Positions page
2. Inspect the open positions table columns

**Expected result:**
- A column for grace days / grace period indicator is visible in the table
- Column is visible without requiring any filter or toggle

---

## F-14 — Grace period indicator: correct display format when in grace

**Acceptance criterion:** When `grace_days_remaining` is an integer, displays "Day {holding_days + 1} of 10".
**Derived from:** `positions.md` v1.2; `position_endpoints.md` v1.8.3
**Type:** Frontend

**Setup:**
Open position in grace period. Know its `holding_days` value.

**Steps:**
1. Call `GET /positions` and identify a position with non-null `grace_days_remaining`
2. Note its `holding_days` value (e.g., `holding_days: 3`)
3. Navigate to Positions page
4. Find that position's row in the table
5. Read the grace column value

**Expected result:**
- Display shows "Day 4 of 10" (when `holding_days = 3`: `holding_days + 1 = 4`)
- Format matches exactly: "Day {N} of 10"

**Notes:**
Examples:
- `holding_days: 0` → "Day 1 of 10"
- `holding_days: 5` → "Day 6 of 10"
- `holding_days: 9` → "Day 10 of 10"

---

## F-15 — Grace period indicator: dash or hidden when null

**Acceptance criterion:** When `grace_days_remaining` is null (position not in grace), the cell shows a dash or is hidden.
**Derived from:** `positions.md` v1.2
**Type:** Frontend

**Setup:**
Open position post-grace period (`holding_days ≥ 10`).

**Steps:**
1. Confirm a position has `grace_days_remaining: null` via `GET /positions`
2. Navigate to Positions page
3. Find that position's row
4. Inspect the grace column cell

**Expected result:**
- Cell displays a dash (`—` or `-`) or is visually empty/hidden
- Does not display "Day 0 of 10" or "null" or "0"

---

## F-16 — Best/Worst Trades component present on Analytics page

**Acceptance criterion:** Best/Worst Trades component is visible on the Performance Analytics page, positioned below the Top Performers component.
**Derived from:** `analytics.md` v1.2 §Best/Worst Trades placement
**Type:** Frontend

**Setup:**
Portfolio with at least one qualifying trade (has `stop_price` in `trades_for_charts`).

**Steps:**
1. Navigate to the Performance Analytics page
2. Scroll to find the Top Performers component (existing)
3. Inspect what comes immediately below

**Expected result:**
- A Best/Worst Trades component is present below Top Performers
- It has two panels: one for best trades (positive R), one for worst trades (negative R)
- Component renders on page load without user interaction

---

## F-17 — Best/Worst Trades: ranking by R-multiple correct

**Acceptance criterion:** Top panel shows the 3 highest R-multiple trades; bottom panel shows the 3 lowest R-multiple trades.
**Derived from:** `analytics.md` v1.2 §Best/Worst Trades ranking
**Type:** Frontend

**Setup:**
Portfolio with at least 6 qualifying closed trades (all with `stop_price` in `trades_for_charts`). Know each trade's expected R-multiple.

**Steps:**
1. Call `GET /analytics/metrics` and extract `trades_for_charts`
2. Calculate R-multiple for every trade with a non-null/non-zero `stop_price`
3. Sort by R-multiple: identify top 3 and bottom 3
4. Navigate to Performance Analytics page
5. Inspect Best/Worst Trades component

**Expected result:**
- Top panel: displays exactly the 3 trades with highest R-multiple
- Bottom panel: displays exactly the 3 trades with lowest R-multiple
- Ordering within each panel: by R-multiple (highest to lowest / lowest to highest)

---

## F-18 — Trades without stop_price excluded from Best/Worst ranking

**Acceptance criterion:** Trades where `stop_price` is null or zero are excluded from the ranking entirely.
**Derived from:** `analytics.md` v1.2 §Best/Worst Trades exclusion rule
**Type:** Frontend

**Setup:**
Portfolio mix: some trades with `stop_price` and some without.

**Steps:**
1. Call `GET /analytics/metrics` → `trades_for_charts`
2. Identify trades with `stop_price: null` or `stop_price: 0`
3. Note their tickers/dates
4. Navigate to Performance Analytics page
5. Inspect Best/Worst Trades panels

**Expected result:**
- Trades without a valid `stop_price` do not appear in either panel, even if their P&L would rank them in the top/bottom 3
- Ranking is computed only from qualifying trades

---

## F-19 — Best/Worst Trades: card contents complete

**Acceptance criterion:** Each trade card shows ticker, R-multiple (signed, 2dp, R suffix), P&L (GBP, signed), exit date, exit reason.
**Derived from:** `analytics.md` v1.2 §Best/Worst Trades card contents
**Type:** Frontend

**Setup:**
Best/Worst Trades component rendering with data.

**Steps:**
1. Navigate to Performance Analytics page
2. Inspect a card in the Best panel and a card in the Worst panel

**Expected result:**
Each card shows:
- Ticker symbol (e.g., "NVDA")
- R-multiple: signed, 2dp, R suffix (e.g., "+2.31R" or "-0.87R")
- P&L: signed GBP value (e.g., "+£450.00" or "-£82.50")
- Exit date (formatted date)
- Exit reason (e.g., "Trailing Stop")

**Notes:**
Verify all five fields are present. If any field is missing this is a defect.

---

## F-20 — Best/Worst Trades: partial panel when fewer than 3 qualifying trades

**Acceptance criterion:** When fewer than 3 qualifying trades exist, the panel renders available trades (up to available count) rather than erroring or hiding entirely.
**Derived from:** `analytics.md` v1.2 §Best/Worst Trades — partial data
**Type:** Frontend

**Setup:**
Portfolio with exactly 1 or 2 qualifying trades (with `stop_price`).

**Steps:**
1. Navigate to Performance Analytics page with a portfolio having only 2 qualifying trades
2. Inspect both panels

**Expected result:**
- Best panel shows 2 cards (not 3)
- Worst panel shows 2 cards (the same trades, if only 2 exist — both will be "best" and "worst")
- No error message or blank panel
- No crash / unhandled exception

**Notes:**
If the test environment cannot replicate this exact state, defer. Record evidence.

---

## F-21 — Best/Worst Trades: empty state when no qualifying trades

**Acceptance criterion:** If no qualifying trades exist, both panels render an empty state message rather than crashing.
**Derived from:** `analytics.md` v1.2 §Best/Worst Trades empty state
**Type:** Frontend

**Setup:**
Portfolio with no qualifying trades (all trades have `stop_price: null` or no closed trades at all).

**Steps:**
1. Navigate to Performance Analytics page
2. Inspect Best/Worst Trades component

**Expected result:**
- Component renders
- Both panels show an empty state message (not blank, not an error)
- No JavaScript error

**Notes:**
If the test environment cannot replicate no-qualifying-trades state, defer.

---

## F-22 — Win Rate by Month chart renders on Analytics page

**Acceptance criterion:** Win Rate by Month bar chart is visible on the Performance Analytics page, positioned below Best/Worst Trades.
**Derived from:** `analytics.md` v1.2 §Win Rate by Month placement
**Type:** Frontend

**Setup:**
Portfolio with non-empty `monthly_data` in `GET /analytics/metrics` response.

**Steps:**
1. Navigate to Performance Analytics page
2. Scroll below the Best/Worst Trades component

**Expected result:**
- A bar chart is present
- It is labelled "Win Rate by Month" (or equivalent)
- Bars are visible, corresponding to monthly data

---

## F-23 — Win Rate by Month: source and axes correct

**Acceptance criterion:** X-axis labels come from `monthly_data[].month`; Y-axis is 0–100 fixed scale.
**Derived from:** `analytics.md` v1.2; `analytics_endpoints.md` v1.8.1 §monthly_data
**Type:** Frontend

**Steps:**
1. Call `GET /analytics/metrics` and note `monthly_data` entries (e.g., `"month": "2026-01"`, `"win_rate": 66.7`)
2. Navigate to Performance Analytics page
3. Inspect Win Rate by Month chart

**Expected result:**
- X-axis labels correspond to months in `monthly_data` (formatted as readable month labels)
- Y-axis scale is fixed 0–100 (does not auto-scale beyond 100)
- Bar heights correspond to `win_rate` values (e.g., a month with 66.7% win rate has a bar reaching ~67% of the chart height)

---

## F-24 — Win Rate by Month: 50% reference line present

**Acceptance criterion:** A horizontal dashed reference line at 50% is visible.
**Derived from:** `analytics.md` v1.2 §Win Rate by Month — 50% reference
**Type:** Frontend

**Steps:**
1. Navigate to Performance Analytics page
2. Inspect the Win Rate by Month chart

**Expected result:**
- A horizontal reference line is visible at the 50% mark on the Y-axis
- The line is visually distinct (dashed style and muted/subdued colour)

---

## F-25 — Win Rate by Month: per-bar colour coding

**Acceptance criterion:** Bars above 50% win rate are profit-coloured (green); bars at or below 50% are loss-coloured (red).
**Derived from:** `analytics.md` v1.2 §Win Rate by Month — colours
**Type:** Frontend

**Setup:**
Portfolio with months having win rates both above and at/below 50%.

**Steps:**
1. Call `GET /analytics/metrics` and identify at least one month with `win_rate > 50` and one with `win_rate ≤ 50`
2. Navigate to Performance Analytics page
3. Inspect bar colours for those specific months

**Expected result:**
- Month with `win_rate = 66.7%`: bar is green (profit colour)
- Month with `win_rate = 40.0%`: bar is red (loss colour)
- Month with `win_rate = 50.0%` exactly: bar is red (the rule is "at or below 50%")

**Notes:**
Boundary condition: exactly 50% must use red (loss colour). Verify this explicitly if a 50% month exists.

---

## F-26 — Win Rate by Month: tooltip shows trade_count field

**Acceptance criterion:** Tooltip on hover/touch shows month, win rate (%), and trade count sourced from `monthly_data[].trade_count`.
**Derived from:** `analytics.md` v1.2 §tooltip; `analytics_endpoints.md` v1.8.1 §monthly_data schema
**Type:** Frontend

**Steps:**
1. Call `GET /analytics/metrics` and note a specific month's `month`, `win_rate`, and `trade_count` values (e.g., `"month": "2026-01"`, `"win_rate": 66.7`, `"trade_count": 3`)
2. Navigate to Performance Analytics page
3. Hover over (or touch) the bar for that month
4. Inspect the tooltip

**Expected result:**
- Tooltip displays the month label (formatted, e.g., "Jan 2026")
- Tooltip displays win rate: "66.7%" (or similar formatting)
- Tooltip displays trade count: "3 trades" (or similar formatting)
- Trade count value matches `trade_count` from the API (not `total_trades` — the field was renamed in the spec correction F-02, confirmed at v1.2)

**Notes:**
This scenario specifically validates the F-02 spec fix from QA review. The field must be `trade_count` not `total_trades`. Verify the tooltip value matches `monthly_data[].trade_count` from the raw API response.

---

## F-27 — Win Rate by Month component absent when monthly_data is empty

**Acceptance criterion:** Component does not render when `monthly_data` is empty.
**Derived from:** `analytics.md` v1.2 §empty state
**Type:** Frontend

**Setup:**
Portfolio where `GET /analytics/metrics` returns `monthly_data: []` (no monthly data — possible when `has_enough_data: false` or no recent trades).

**Steps:**
1. Confirm `GET /analytics/metrics` returns `monthly_data: []`
2. Navigate to Performance Analytics page
3. Inspect the area where Win Rate by Month would appear

**Expected result:**
- No Win Rate by Month chart is rendered
- No empty chart frame or skeleton is visible in its place
- No JavaScript error

**Notes:**
Component must not render at all — not render with an empty state message. If this environment state cannot be replicated, verify via code inspection of the `monthly_data.length === 0` rendering guard.

---

## F-28 — CSV export button present on Trade History page

**Acceptance criterion:** A CSV export button is visible on the Trade History page.
**Derived from:** `trade_history.md` v1.1 §CSV export button
**Type:** Frontend

**Setup:**
Portfolio with at least one closed trade.

**Steps:**
1. Navigate to the Trade History page
2. Look for an export or download button

**Expected result:**
- A button with a CSV/export label is visible on the page
- The button is visible without requiring any filter interaction or scrolling (or is reasonably discoverable within the page header area)

---

## F-29 — CSV export button triggers file download

**Acceptance criterion:** Clicking the button triggers `GET /trades/export/csv` and the browser handles the file download.
**Derived from:** `trade_history.md` v1.1 §CSV export button behaviour
**Type:** Frontend

**Setup:**
Portfolio with at least one closed trade. Browser developer tools open, Network tab active.

**Steps:**
1. Navigate to Trade History page
2. Open Network tab in browser developer tools
3. Click the CSV export button
4. Observe network activity and browser behaviour

**Expected result:**
- Browser makes a request to `GET /trades/export/csv`
- Browser initiates a file download (file save dialog appears or file appears in Downloads)
- Downloaded file is named `trade_history.csv`
- Downloaded file opens as valid CSV with trade data

**Notes:**
Verify the network request goes to `GET /trades/export/csv` — not a client-side CSV generation. The old `ExportModal.js` prototype built CSV client-side; that must NOT be the implementation. A client-side Blob download with no network request is a defect.

---

## REGRESSION SCENARIOS

---

## R-01 — Existing GET /portfolio fields unaffected

**Acceptance criterion:** All pre-existing fields on `GET /portfolio` are unchanged after the new fields are added.
**Derived from:** `portfolio_endpoints.md` v1.8.2; regression risk from additive schema change
**Type:** Regression

**Steps:**
1. Call `GET /portfolio`
2. Verify all pre-existing fields are present: `cash`, `cash_balance`, `total_value`, `open_positions_value`, `total_pnl`, `initial_value`, `net_deposits`, `live_fx_rate`, `last_updated`, `positions` array
3. Verify the `positions` summary objects contain their pre-existing fields: `id`, `ticker`, `market`, `entry_date`, `entry_price`, `shares`, `current_price`, `current_price_native`, `stop_price`, `stop_price_native`, `pnl`, `pnl_percent`, `holding_days`, `status`, `grace_period`, `display_status`

**Expected result:**
- All pre-existing fields present with correct types and values
- No existing field renamed, removed, or relocated
- No breaking change to the existing response shape

---

## R-02 — Existing GET /positions fields unaffected

**Acceptance criterion:** All pre-existing fields on `GET /positions` are unchanged after `grace_days_remaining` is added.
**Derived from:** `position_endpoints.md` v1.8.3; regression risk from additive schema change
**Type:** Regression

**Steps:**
1. Call `GET /positions`
2. Verify all pre-existing fields are present on each position object: `id`, `ticker`, `market`, `entry_date`, `entry_price`, `shares`, `current_price`, `current_price_native`, `stop_price`, `stop_price_native`, `initial_stop`, `pnl`, `pnl_percent`, `holding_days`, `status`, `grace_period`, `display_status`, `atr_value`, `fx_rate`, `live_fx_rate`, `entry_note`, `exit_note`, `tags`

**Expected result:**
- All pre-existing fields present with correct types
- `grace_days_remaining` present as an additional field, not replacing anything

---

## R-03 — GET /trades unaffected

**Acceptance criterion:** The existing `GET /trades` endpoint is unchanged. No new fields added, no fields removed.
**Derived from:** `trade_endpoints.md` v1.8.4; regression risk from adding new endpoint in same domain
**Type:** Regression

**Steps:**
1. Call `GET /trades`
2. Verify the response shape: `total_trades`, `win_rate`, `total_pnl`, `trades` array
3. Verify each trade object contains: `id`, `ticker`, `market`, `entry_date`, `exit_date`, `shares`, `entry_price`, `exit_price`, `pnl`, `pnl_pct`, `pnl_percent`, `holding_days`, `exit_reason`, `entry_note`, `exit_note`, `tags`

**Expected result:**
- All existing fields present with correct types
- No changes to the existing endpoint

---

## R-04 — Dashboard existing summary cards unaffected

**Acceptance criterion:** The four existing Portfolio Summary Cards (Cash, Portfolio Value, Total P&L, Open Positions) are present and displaying correct values after the Current Drawdown widget is added.
**Derived from:** Regression risk from adding a fifth card to the stats row
**Type:** Regression

**Steps:**
1. Note current values via `GET /portfolio` (cash balance, total value, total P&L, position count)
2. Navigate to Dashboard page
3. Confirm all four existing summary cards are present and display the correct values

**Expected result:**
- All four existing cards are visible in the stats row
- Values match the API response
- No card has been displaced, hidden, or replaced by the new drawdown widget

---

## R-05 — Trade History page existing functionality unaffected

**Acceptance criterion:** All existing Trade History functionality works correctly after R-multiple column and CSV button are added.
**Derived from:** Regression risk from adding new column and button
**Type:** Regression

**Steps:**
1. Navigate to Trade History page
2. Verify the existing summary stats row is present (total trades, win rate, total P&L, etc.)
3. Verify existing table columns are present: Ticker, Market, Entry Date, Exit Date, Shares, Entry Price, Exit Price, P&L, P&L %, Days Held, Exit Reason
4. Click a trade row to expand the journal
5. Apply a filter (e.g., by market)
6. Verify filtered results are correct

**Expected result:**
- All existing table columns present
- Expandable journal rows still function
- Filters still work correctly
- No existing column has been removed or displaced
- Page does not error when `GET /analytics/metrics` fails or is slow (R-multiple column degrades to `—` but page still loads)

**Notes:**
The final point is important: the Trade History page now makes two API calls. If `GET /analytics/metrics` fails, the trade table must still render (with `—` in the R-multiple column). Verify this degraded behaviour is handled gracefully.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-02-27 | Initial version. Covers all 6 bundle items. 42 scenarios total: 13 backend, 22 frontend, 5 regression. Authored by QA & Testing Owner for A-TS-01. |
