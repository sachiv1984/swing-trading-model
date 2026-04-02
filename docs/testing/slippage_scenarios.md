**Owner:** QA & Testing Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.1
**Last Updated:** 2026-04-02
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Derived from:** `docs/specs/frontend/pages/trade_history.md` v1.2; `docs/specs/api_contracts/trade_endpoints.md` v2.1.0; `docs/specs/data_model.md` v1.4+
**Sprint:** 2026-03-31__release-v2.4 — ST-12 (closes TEST-GAP-EPIC-05-SLIP)

---

# Acceptance Test Scenarios — Slippage Tracking

---

## 1. Scope

These scenarios verify slippage tracking behaviour across the trade history page. They cover: fill price capture on trade entry, slippage % column display with colour coding, avg slippage StatsCard update, and null fill price display for pre-v2.1 or no-fill-price trades.

Spec reference: `docs/specs/frontend/pages/trade_history.md` §Slippage Column and §Avg Slippage; `docs/specs/api_contracts/trade_endpoints.md` §fill_price / §slippage_pct.

---

## 2. Canonical Spec References

| Component | Spec location |
|-----------|--------------|
| Fill price field | `docs/specs/data_model.md` — positions.user_fill_price column |
| Slippage column | `docs/specs/frontend/pages/trade_history.md §Slippage Column` |
| Avg Slippage stat | `docs/specs/frontend/pages/trade_history.md §Avg Slippage (Summary Stat)` |
| API fields | `docs/specs/api_contracts/trade_endpoints.md §fill_price`, `§slippage_pct`, `§avg_slippage_pct` |
| Null handling | `docs/specs/frontend/pages/trade_history.md §Slippage Column — Null handling` |

---

## 3. Prerequisites

- Staging environment running with seed data loaded
- At least one trade with `fill_price` recorded (post-v2.1 trade)
- At least one trade without `fill_price` (pre-v2.1 trade or trade entered without fill price)
- Trade history page accessible at `/trade-history` or equivalent route

---

## 4. Test Scenarios

---

### SC-SLIP-01 — Fill price input captured and stored on trade entry

**Scope note (2026-04-02):** The fill price field exists on the **Trade Entry form** (`/TradeEntry`), not the Exit modal. The Exit modal only accepts exit price. SC-SLIP-01 tests entry fill price capture — the "entry deviation" metric (`fill_price − entry_price`). See `docs/testing/slippage_manual_runbook.md` v1.1 for the corrected runbook.

**Precondition:** User is on the Trade Entry form (`/TradeEntry`). The optional Fill Price field is visible below Entry Price.

**Steps:**
1. Navigate to **Trade Entry** page
2. Enter a new position: ticker, market, entry price (e.g. 100.00), shares, stop price, entry date
3. In the **Fill Price (optional)** field: enter a value that differs from entry price (e.g. 100.25 — filled 25p above limit)
4. Submit the trade entry form

**Expected result:**
- Position is saved with `user_fill_price = 100.25` stored against the position
- When the position is subsequently exited, `trade_history.fill_price = 100.25` is written
- Trade appears in Trade History with **Entry Dev.** column showing `+0.25%` (`(100.25 − 100.00) / 100.00 × 100`)
- If fill price is omitted at entry, Trade History shows `—` in the Entry Dev. column for that trade

**Automation:** Manual (staging) — fill price field on TradeEntry form, then exit the position and verify Trade History display

---

### SC-SLIP-02 — Slippage % column displays colour-coded values

**Precondition:** Trade history page loaded with at least one trade having a non-null `slippage_pct`.

**Steps:**
1. Navigate to trade history page
2. Locate the Slippage column in the trade history table
3. Observe colour coding for positive slippage values (filled above market)
4. Observe colour coding for negative slippage values (filled below market)

**Expected result:**
- Slippage column is present after the P&L % column
- Negative slippage (favourable — filled below market) renders in **green** (or emerald/favourable colour)
- Positive slippage (unfavourable — filled above market) renders in **red** (or rose/unfavourable colour)
- Column header shows "Slippage" with ⓘ info icon
- Hovering the ⓘ icon displays tooltip: `"Slippage = (Fill Price − Market Price) / Market Price"` and sign convention explanation

**Automation:** Automated — `tests/e2e/slippage-tracking.spec.js` SC-SLIP-02a (header), SC-SLIP-02b (emerald), SC-SLIP-02c (rose), SC-SLIP-02d (tooltip title)

---

### SC-SLIP-03 — Avg slippage StatsCard updates when trades have fill prices

**Precondition:** At least one closed trade with `fill_price` exists in the dataset.

**Steps:**
1. Navigate to trade history page
2. Locate the Avg Slippage summary stat card in the stats bar
3. Verify the displayed value matches the mean `slippage_pct` across all trades with fill prices

**Expected result:**
- Avg Slippage stat card is visible in the stats bar
- Displays the portfolio-average slippage percentage (non-null)
- Value is consistent with API response `avg_slippage_pct` field
- When no trades have fill price: stat card displays `—` with tooltip: `"No Fill Price data available yet."`

**Automation:** Automated — `tests/e2e/slippage-tracking.spec.js` SC-SLIP-03a (value from API), SC-SLIP-03b (null shows "—")

---

### SC-SLIP-04 — Null fill price shows em dash for trades without fill price

**Precondition:** Trade history contains at least one trade without a fill price (pre-v2.1 or user did not provide fill price).

**Steps:**
1. Navigate to trade history page
2. Identify a trade row for a trade without fill price
3. Observe the Slippage column cell for that row

**Expected result:**
- Slippage column cell displays `—` (em dash)
- Cell is muted/grey with no colour coding (no green/red)
- No error or blank cell — exactly `—` is rendered
- Other trades in the same table that have fill prices continue to show their slippage values correctly

**Automation:** Automated — `tests/e2e/slippage-tracking.spec.js` SC-SLIP-04a (em dash in null row), SC-SLIP-04b (other rows unaffected)

---

## 5. Known Deviations

### DEV-ST14-01 — Avg Slippage StatsCard renders without gradient (cosmetic, P3)

- **Description:** `StatsCard` component receives `color="cyan"` for Avg Slippage but the gradient map has no `"cyan"` key — card renders without gradient background.
- **Priority:** P3 (cosmetic only)
- **Impact on SC-SLIP-03:** SC-SLIP-03 passes functionally; gradient background rendering is a cosmetic failure. Mark as "Pass with notes" for P3 deviation.
- **Backlog reference:** BLG-FE-01
- **Acceptance record:** Director of Quality 2026-03-20

---

## 6. Scenario Index Entry

| Scenario ID | Description | Spec | Automation | Status |
|-------------|-------------|------|-----------|--------|
| SC-SLIP-01 | Fill price input captured on Trade Entry form; entry deviation shown in Trade History | trade_history.md, data_model.md | Manual — `docs/testing/slippage_manual_runbook.md` v1.1 — **Executed Pass 2026-04-02** | Active |
| SC-SLIP-02 | Slippage % column displays colour-coded values | trade_history.md §Slippage Column | Automated — `tests/e2e/slippage-tracking.spec.js` (SC-SLIP-02a–02d) | Active |
| SC-SLIP-03 | Avg slippage StatsCard updates when trades have fill prices | trade_history.md §Avg Slippage | Automated — `tests/e2e/slippage-tracking.spec.js` (SC-SLIP-03a–03b) | Active |
| SC-SLIP-04 | Null fill price shows em dash for trades without fill price | trade_history.md §Null handling | Automated — `tests/e2e/slippage-tracking.spec.js` (SC-SLIP-04a–04b) | Active |
