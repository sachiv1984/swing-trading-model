**Owner:** QA Lead
**Class:** QA Evidence (Class 7)
**Status:** Active
**Cycle:** 2026-03-24__release-v2.3
**Epic:** EPIC-02 — QA Automation Foundation
**Story:** ST-06 — BLG-QA-01: Playwright E2E for Chart Interactivity
**Issued by:** Director of Quality
**Issued:** 2026-03-25

---

# Human Staging Test Script — ST-06 Visual AC

This script covers the visual acceptance criteria for SC-CHART-IX-01 through SC-CHART-IX-06 that Playwright cannot verify: tile selection rings, cursor state, P&L colour coding, tooltip positioning, and scroll-hint animation.

It must be executed against the **staging environment** (or a local dev server with seed data) before EPIC-02 PR sign-off is granted for ST-06.

**Applies to spec:** `docs/testing/chart_interactivity_scenarios.md`

---

## Prerequisites

### 1. Environment

- EPIC-02 branch deployed to staging, or dev server running locally (`npm start`)
- Browser: Chrome or Edge (DevTools required for SC-CHART-IX-06b network check)
- Viewport: **1280×900 minimum** — chart layout is responsive; narrower viewports may alter tooltip flip behaviour

### 2. Seed data state

The Analytics page requires at least **10 closed trades** to render (default `min_trades_for_analytics` setting). The standard seed scripts do not provide enough trades. Before running this script, apply the analytics supplement seed:

```sql
-- Run against staging DB (requires STAGING_DATABASE_URL)
-- Inserts 12 additional closed trades across Jan–Mar 2026 to reach analytics threshold
-- Assumes seed_portfolio_trades.sql has already been run (portfolio row exists)

DO $$
DECLARE v_portfolio_id UUID;
BEGIN
  SELECT id INTO v_portfolio_id FROM portfolios LIMIT 1;

  INSERT INTO trade_history
    (portfolio_id, ticker, market, entry_date, exit_date,
     entry_price, exit_price, stop_price, shares,
     gross_proceeds, net_proceeds, pnl, exit_reason)
  VALUES
    (v_portfolio_id, 'AAAA', 'UK', '2026-01-05', '2026-01-12', 100.00, 115.00,  90.00, 10, 1150.00, 1150.00,  150.00, 'target'),
    (v_portfolio_id, 'BBBB', 'UK', '2026-01-10', '2026-01-20',  50.00,  42.00,  44.00, 10,  420.00,  420.00,  -80.00, 'stop_hit'),
    (v_portfolio_id, 'CCCC', 'UK', '2026-01-15', '2026-01-28',  80.00, 105.00,  72.00,  8,  840.00,  840.00,  200.00, 'target'),
    (v_portfolio_id, 'DDDD', 'UK', '2026-02-02', '2026-02-10',  60.00,  72.00,  54.00, 10,  720.00,  720.00,  120.00, 'target'),
    (v_portfolio_id, 'EEEE', 'US', '2026-02-05', '2026-02-12',  40.00,  35.00,  36.00, 20,  700.00,  700.00, -100.00, 'stop_hit'),
    (v_portfolio_id, 'FFFF', 'UK', '2026-02-08', '2026-02-15',  90.00,  99.00,  81.00, 10,  990.00,  990.00,   90.00, 'manual'),
    (v_portfolio_id, 'GGGG', 'UK', '2026-02-14', '2026-02-20', 120.00, 108.00, 108.00,  5,  540.00,  540.00,  -60.00, 'stop_hit'),
    (v_portfolio_id, 'HHHH', 'US', '2026-02-18', '2026-02-25', 200.00, 230.00, 180.00,  5, 1150.00, 1150.00,  150.00, 'target'),
    (v_portfolio_id, 'IIII', 'UK', '2026-03-01', '2026-03-05',  50.00,  62.00,  45.00, 10,  620.00,  620.00,  120.00, 'target'),
    (v_portfolio_id, 'JJJJ', 'UK', '2026-03-03', '2026-03-07',  75.00,  67.50,  67.50, 10,  675.00,  675.00,  -75.00, 'stop_hit'),
    (v_portfolio_id, 'KKKK', 'US', '2026-03-06', '2026-03-10', 300.00, 336.00, 270.00,  5, 1680.00, 1680.00,  180.00, 'target'),
    (v_portfolio_id, 'LLLL', 'UK', '2026-03-10', '2026-03-14',  40.00,  36.00,  36.00, 15,  540.00,  540.00,  -60.00, 'stop_hit');
END $$;
```

To run:
```bash
export STAGING_DATABASE_URL="postgresql://..."
psql "$STAGING_DATABASE_URL" -c "<paste SQL above>"
```

After seeding, navigate to Analytics page → switch time period to **"All Time"** → confirm charts render (not the "Not Enough Data" empty state).

### 3. Expected data state for assertions

| Month tile | Trades | Total P&L |
|------------|--------|-----------|
| 2026-01    | 3      | +£270.00  |
| 2026-02    | 5      | +£200.00  |
| 2026-03    | 4      | +£165.00  |

(Plus the 2 trades from `seed_portfolio_trades.sql` if run — ULVR and VOD exit dates determine which month they fall in.)

---

## Section 1 — Monthly Heatmap: Visual AC

Navigate to: **Performance Analytics** (`/#/PerformanceAnalytics`)
Switch time period to **All Time**.
Scroll down to the **Monthly Performance** heatmap section.

### V-CHART-01a — Tile selection ring appears on click

**Scenario ref:** SC-CHART-IX-01a
**Action:**
1. Identify the 2026-01 tile (it should show "+£270" or similar).
2. Click the tile.
3. Observe the tile while the modal is open.

**Expected:** The clicked tile shows a **2px inset ring in the accent/focus colour** (violet/purple range — `ring-violet-400` per component code). The ring is visibly distinct from other tiles.

**Pass:** Ring visible around the originating tile while modal is open.
**Fail:** No ring, tile looks identical to unselected tiles, or ring appears on wrong tile.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

### V-CHART-01b — Tile ring removed on modal close

**Scenario ref:** SC-CHART-IX-01b
**Action:**
1. With the modal still open from V-CHART-01a, close it (press Escape, click X, or click backdrop).
2. Observe the tile that was previously selected.

**Expected:** The 2px inset ring is **removed** from the tile after the modal closes. The tile returns to its normal unselected appearance.

**Pass:** Ring gone after close. Tile looks identical to other non-selected tiles.
**Fail:** Ring remains visible after modal is dismissed.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

### V-CHART-01c — Cursor default on zero-trade tile

**Scenario ref:** SC-CHART-IX-01c

**Implementation note:** `MonthlyHeatmap` only renders tiles for months that have trades. There are no zero-trade tiles in the rendered output for this dataset. This visual check is therefore **not applicable** for the current implementation — the component is spec-compliant by not rendering such tiles at all.

**What to verify instead:** Hover over a **clickable tile** (e.g. 2026-01) and confirm the cursor is a **pointer** (hand icon). This confirms the cursor state logic is wired correctly — the inverse (default cursor on zero-trade tiles) cannot be visually tested without a dataset containing zero-trade months.

**Action:** Hover over the 2026-01 tile without clicking.
**Expected:** Cursor changes to a hand/pointer icon.
**Pass:** Pointer cursor visible on hover.
**Fail:** Default arrow cursor — tile is not recognisably clickable.
**Result:** [ ] PASS  [ ] FAIL  [ ] N/A (no zero-trade tiles in dataset)  **Notes:** ___

---

### V-CHART-01d — P&L colour coding in modal trade table

**Scenario ref:** SC-CHART-IX-01d
**Action:**
1. Click the 2026-01 tile to open the modal.
2. Observe the P&L column in the trade table.

**Expected:**
- AAAA (+£150.00): P&L cell renders in **green** (emerald/green range).
- BBBB (-£80.00): P&L cell renders in **red** (rose/red range).
- CCCC (+£200.00): P&L cell renders in **green**.

**Pass:** Green for positive, red for negative — consistent with colour coding across the application.
**Fail:** All values the same colour, or colours reversed, or values appear in default white/grey.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

## Section 2 — Underwater Equity Curve: Visual AC

Scroll to the **Underwater Equity Curve** section.

### V-CHART-02a — "Scroll to zoom" hint appears on first hover

**Scenario ref:** SC-CHART-IX-02a (optional behaviour)
**Action:**
1. Ensure chart is at full range (no Reset button visible).
2. Hover the mouse over the chart area for the first time.

**Expected:** A muted hint text **"Scroll to zoom"** briefly appears (centred, above the chart area) and **fades within 3 seconds**. This is optional per spec — it only appears on the first hover and only when there are more than 4 data points.

**Pass:** Hint text appears and fades automatically within ~3 seconds.
**Fail:** Hint never appears, or appears and never fades, or appears on every hover (not just first).
**Result:** [ ] PASS  [ ] FAIL  [ ] N/A (hint did not appear — acceptable if data ≤ 4 points)  **Notes:** ___

---

### V-CHART-02b — Grab cursor while zoomed

**Scenario ref:** SC-CHART-IX-03a (cursor visual)
**Action:**
1. Click the `+` zoom button to zoom in.
2. Hover over the chart area without clicking.

**Expected:** Cursor changes to a **grab** hand icon (open hand) — indicating the chart is pannable.

**Pass:** Grab cursor visible on hover when zoomed.
**Fail:** Default arrow cursor, or no visual indication of panning capability.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

### V-CHART-02c — Grabbing cursor during drag

**Scenario ref:** SC-CHART-IX-03a (cursor visual, mid-drag)
**Action:**
1. With chart zoomed in, click and hold the mouse on the chart area.
2. While holding the mouse button, observe the cursor.

**Expected:** Cursor changes to a **grabbing** (closed fist) icon during the drag.

**Pass:** Grabbing cursor while mouse button is held down.
**Fail:** Cursor stays as grab hand or arrow during drag.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

## Section 3 — Underwater Equity Curve: Tooltip Visual AC

### V-CHART-04a — Tooltip appears and shows all four fields

**Scenario ref:** SC-CHART-IX-04a
**Action:**
1. Hover slowly over different data points on the Underwater Equity Curve.
2. When a tooltip appears, observe its content.

**Expected:** Tooltip panel shows all four fields:
- **Date** — formatted as a readable date (e.g. "12/03/2026" in en-GB)
- **Drawdown %** — a signed percentage (e.g. "–8.30%" in rose/red colour)
- **Current:** — cumulative equity in GBP (e.g. "Current: £450")
- **Peak:** — peak equity in GBP (e.g. "Peak: £600")

**Pass:** All four fields visible with correct labelling and formatting.
**Fail:** Tooltip missing one or more fields, or fields show incorrect labels (e.g. raw key names like `drawdown`, `equity`).
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

### V-CHART-04b — Tooltip flips left in right 30% of chart

**Scenario ref:** SC-CHART-IX-04a (tooltip repositioning)
**Action:**
1. Hover over a data point in the **leftmost 30%** of the chart — note the tooltip position relative to the cursor (it should appear to the right of or near the cursor).
2. Hover over a data point in the **rightmost 30%** of the chart — observe tooltip position.

**Expected:** When cursor is in the right 30% of the chart area, the tooltip appears to the **left** of the cursor rather than overlapping or clipping at the chart edge.

**Note:** Recharts handles tooltip positioning via its built-in offset logic. This check verifies the default Recharts tooltip repositioning behaviour is intact — it is not explicitly coded in the component but is a Recharts default.

**Pass:** Tooltip does not overflow or clip at chart edges in either position.
**Fail:** Tooltip clips off the right edge of the chart when hovering near the right side.
**Result:** [ ] PASS  [ ] FAIL  [ ] UNABLE — insufficient data points to reach right 30% of chart  **Notes:** ___

---

## Section 4 — R-Multiple Analysis: Tooltip Visual AC

Scroll to the **R-Multiple Analysis** section.

### V-CHART-05a — Bar tooltip shows all three fields

**Scenario ref:** SC-CHART-IX-05a
**Action:**
1. Hover over any bar in the R-Multiple Distribution histogram (left panel, "Distribution" subheading).
2. When a tooltip appears, observe its content.

**Expected:** Tooltip shows:
- **Bucket label** — e.g. `"1R to 2R"` or `"-1R to 0R"` (bold text at top of tooltip)
- **Trade count** — e.g. `"3 trades"` or `"1 trade"` (singular/plural correct)
- **% of closed trades** — e.g. `"20% of closed trades"` (rounded integer %)

**Pass:** All three fields visible with correct labels and formatting.
**Fail:** Any field missing, or labels show raw keys (e.g. `"count"`, `"value"`), or percentage is absent.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

### V-CHART-05b — Zero-count bar tooltip shows "0 trades, 0%"

**Scenario ref:** SC-CHART-IX-05b
**Action:**
1. Identify a bar with height = 0 in the distribution chart. With 12 trades, the `-3R+`, `2R to 3R`, and `3R+` buckets are likely to be empty (0 count) depending on the actual trade data.
2. Hover over a zero-height bar (click the chart area at the appropriate bucket position on the X-axis — look for bars that appear flat at the baseline).

**Expected:** Tooltip shows: bucket label, `"0 trades"`, `"0% of closed trades"`.

**Note:** Zero-height Recharts bars may be difficult to hover. If the bar is not hoverable, note this and skip — this is a known Recharts constraint with zero-height bars.

**Pass:** Tooltip shows "0 trades" and "0% of closed trades" when hovering a zero-count bucket.
**Fail:** Tooltip shows non-zero values for an empty bucket, or shows nothing (which is acceptable — see note).
**Result:** [ ] PASS  [ ] FAIL  [ ] SKIP — zero-height bars not hoverable in Recharts  **Notes:** ___

---

### V-CHART-05c — Tooltip cursor repositioning near chart edges

**Scenario ref:** SC-CHART-IX-05a (tooltip positioning)
**Action:**
1. Hover over the **leftmost bar** (`-3R+`) in the distribution chart.
2. Hover over the **rightmost bar** (`3R+`).
3. Observe whether the tooltip flips or adjusts to avoid clipping.

**Expected:** Tooltip does not overflow the visible chart boundary at either edge.

**Pass:** Tooltip fully visible and within the chart/page bounds at both edges.
**Fail:** Tooltip clips or overflows the chart boundary at either edge.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

## Section 5 — Cross-Chart: No Network Requests

### V-CHART-06b — Network tab confirms no API calls during interactions

**Scenario ref:** SC-CHART-IX-06b
**Action:**
1. Open Chrome DevTools → **Network** tab.
2. Clear the network log (click the 🚫 clear button).
3. Perform each of the following interactive actions:
   - Click a heatmap tile (open and close the modal)
   - Click `+` zoom button twice on the Underwater Equity Curve
   - Click Reset
   - Hover over the Underwater Equity Curve chart
   - Hover over bars in the R-Multiple Distribution chart
4. Observe the Network tab throughout.

**Expected:** **No new network requests** appear in the Network tab during any of the above interactions. All interaction operates over already-loaded data.

**Pass:** Network tab shows 0 new requests after clearing, through all interactions.
**Fail:** Any API request appears (e.g. `GET /trades`, `GET /analytics/*`, or similar) triggered by hovering or clicking chart elements.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

## Sign-Off Record

Complete this block and append to `claude/cycles/2026-03-24__release-v2.3/qa_evidence_EPIC-02.md` → ST-06 DoQ Sign-Off section.

```
Visual staging test completed by: _______________
Date: _______________
Environment: [ ] Local dev  [ ] Staging
Seed state confirmed: [ ] reset run  [ ] seed_all.sh run  [ ] analytics supplement SQL run
Analytics threshold check: [ ] confirmed — "All Time" shows charts (not empty state)

Section 1 — Monthly Heatmap:
  V-CHART-01a (tile selection ring):      [ ] PASS  [ ] FAIL
  V-CHART-01b (ring removed on close):   [ ] PASS  [ ] FAIL
  V-CHART-01c (cursor on tile):          [ ] PASS  [ ] FAIL  [ ] N/A
  V-CHART-01d (P&L colour coding):       [ ] PASS  [ ] FAIL

Section 2 — Underwater Equity Curve:
  V-CHART-02a (scroll-to-zoom hint):     [ ] PASS  [ ] FAIL  [ ] N/A
  V-CHART-02b (grab cursor while zoomed):[ ] PASS  [ ] FAIL
  V-CHART-02c (grabbing cursor on drag): [ ] PASS  [ ] FAIL

Section 3 — Tooltip visual:
  V-CHART-04a (tooltip 4 fields):        [ ] PASS  [ ] FAIL
  V-CHART-04b (tooltip flip at right):   [ ] PASS  [ ] FAIL  [ ] UNABLE

Section 4 — R-Multiple tooltip:
  V-CHART-05a (bar tooltip 3 fields):    [ ] PASS  [ ] FAIL
  V-CHART-05b (zero-count bar):          [ ] PASS  [ ] FAIL  [ ] SKIP
  V-CHART-05c (tooltip edge clipping):   [ ] PASS  [ ] FAIL

Section 5 — Network:
  V-CHART-06b (no API calls):            [ ] PASS  [ ] FAIL

Overall visual verdict: [ ] ALL PASS  [ ] FAILURES — see notes
Notes: _______________

DoQ confirmation of visual sign-off: [ ] Confirmed — ST-06 visual AC sign-off granted
                                     [ ] Deferred — failures filed as deviations (list IDs): ___
```
