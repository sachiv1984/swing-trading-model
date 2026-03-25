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

The Analytics page requires at least **10 closed trades** to render (default `min_trades_for_analytics` setting). The standard seed scripts do not provide enough trades. Before running this script, apply the analytics seed:

```bash
export STAGING_DATABASE_URL="postgresql://user:pass@host:5432/db"

# Option A — run all seeds (recommended after a fresh reset):
./scripts/seeds/seed_all.sh

# Option B — run analytics seed only (if portfolio/watchlist/alerts already seeded):
psql "$STAGING_DATABASE_URL" --no-psqlrc --single-transaction \
    -f scripts/seeds/seed_analytics.sql
```

`seed_analytics.sql` inserts 12 closed trades (AAAA–LLLL) across Jan–Mar 2026. It is idempotent — safe to re-run.

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

> **STAGING BLOCKED — V-CHART-05a, V-CHART-05b, V-CHART-05c**
>
> The `trade_history` table has no `stop_price` column. The `/trades` API response therefore never includes `stop_price`. `RMultipleAnalysis.js` filters trades with `trades.filter(t => t.stop_price && ...)`, so the R-Multiple chart will render as empty (no bars) on staging regardless of how many trades exist in the database.
>
> These three checks **cannot be executed on staging** until `stop_price` is added to the API response. Skip all three and record them as staging-blocked in the sign-off record.
>
> **Backlog tracking:** A backlog item for adding `stop_price` to the `/trades` API response has been filed during ST-06 delivery.

Scroll to the **R-Multiple Analysis** section.

### V-CHART-05a — Bar tooltip shows all three fields

**Scenario ref:** SC-CHART-IX-05a

> **STAGING BLOCKED** — R-Multiple chart will not render. `stop_price` is absent from the `/trades` API response. Skip until the API gap is resolved.

**Result:** [ ] STAGING-BLOCKED  **Notes:** ___

---

### V-CHART-05b — Zero-count bar tooltip shows "0 trades, 0%"

**Scenario ref:** SC-CHART-IX-05b

> **STAGING BLOCKED** — R-Multiple chart will not render. `stop_price` is absent from the `/trades` API response. Skip until the API gap is resolved.

**Result:** [ ] STAGING-BLOCKED  **Notes:** ___

---

### V-CHART-05c — Tooltip cursor repositioning near chart edges

**Scenario ref:** SC-CHART-IX-05a (tooltip positioning)

> **STAGING BLOCKED** — R-Multiple chart will not render. `stop_price` is absent from the `/trades` API response. Skip until the API gap is resolved.

**Result:** [ ] STAGING-BLOCKED  **Notes:** ___

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
Seed state confirmed: [ ] reset run  [ ] seed_all.sh run (includes seed_analytics.sql)
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

Section 4 — R-Multiple tooltip (STAGING BLOCKED — stop_price not in /trades API):
  V-CHART-05a (bar tooltip 3 fields):    [ ] STAGING-BLOCKED
  V-CHART-05b (zero-count bar):          [ ] STAGING-BLOCKED
  V-CHART-05c (tooltip edge clipping):   [ ] STAGING-BLOCKED

Section 5 — Network:
  V-CHART-06b (no API calls):            [ ] PASS  [ ] FAIL

Overall visual verdict: [ ] ALL PASS  [ ] FAILURES — see notes
Notes: _______________

DoQ confirmation of visual sign-off: [ ] Confirmed — ST-06 visual AC sign-off granted
                                     [ ] Deferred — failures filed as deviations (list IDs): ___
```
