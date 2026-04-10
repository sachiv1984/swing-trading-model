**Owner:** QA Lead
**Class:** QA Evidence (Class 7)
**Status:** Active
**Cycle:** 2026-04-05__release-v2.5
**Epic:** EPIC-03 — Frontend & Operations Quick Wins
**Issued by:** Director of Quality
**Issued:** 2026-04-06

---

# Human Staging Test Script — EPIC-03 Visual AC

This script covers the visual acceptance criteria for EPIC-03 that cannot be verified by code review or Playwright alone. It must be executed against the staging environment (or a local dev server with seed data) before EPIC-03 PR sign-off is fully granted.

**Applies to stories:** ST-09 (frontend rendering — fee drag column and StatsCard)
**Note:** ST-07 (workflow YAML) and ST-08 (docs update) have no visual AC. This script covers ST-09 only.

**Prerequisites:**
1. EPIC-03 branch is deployed to staging or dev server is running locally (`npm start` + `uvicorn main:app`)
2. Database has at least 2 closed trades, with:
   - At least one trade where `exit_fees` and `gross_proceeds` are both populated and `gross_proceeds > 0` (produces a non-null `fee_drag_pct`)
   - At least one trade where `gross_proceeds` is null or zero (produces a null `fee_drag_pct` — used to verify the "—" null display; if no such trade exists, skip V-FD-03)
3. Browser: Chrome or Edge (Chromium)
4. Viewport: 1280×900 minimum
5. Navigate to Trade History: `/#/TradeHistory`

**Record results in:** `claude/cycles/2026-04-05__release-v2.5/qa_evidence_EPIC-03.md` — append to the EPIC-03 consolidation sign-off block.

---

## PATH-1: Trade History Table — Fee Drag % Column

Navigate to: **Trade History** (`/#/TradeHistory`). Wait for the table to fully render (trade rows visible).

---

### V-FD-01 — Fee Drag % column header is present after Slippage

**Action:** Observe the column headers in the trade history table.

**Expected:**
- A column header reading **"Fee Drag %"** is present
- It appears to the right of the **"Slippage"** column and to the left of **"R-Multiple"**
- The header does not read "Fee Slippage", "Drag", or any slippage-adjacent label

**Pass:** "Fee Drag %" header visible in correct position between Slippage and R-Multiple.
**Fail:** Column absent, labelled incorrectly, or in wrong position.

**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

### V-FD-02 — Fee drag cell renders amber `+X.XX%` for trades with data

**Action:** Locate a trade row where `fee_drag_pct` is non-null (a trade with exit fees and gross proceeds recorded).

**Expected:**
- The Fee Drag % cell displays a value in `+X.XX%` format (e.g. `+0.38%`, `+1.20%`)
- The `+` prefix is always present (even for very small values)
- The text colour is **amber/orange** — NOT green, NOT red, NOT white/grey
- The amber tone is visually distinct from the emerald/green (profitable P&L) and rose/red (loss P&L) colours used elsewhere in the same row

**Pass:** Value present in `+X.XX%` format in amber/orange colour.
**Fail:** Value missing, wrong format (e.g. `0.38%` without `+`), wrong colour (green/red), or blank.

**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

### V-FD-03 — Null fee drag cell renders "—" in muted colour

**Precondition:** At least one trade exists with null `fee_drag_pct` (gross_proceeds null or zero). If no such trade exists in the dataset, mark as SKIP.

**Action:** Locate a trade row where `fee_drag_pct` is null.

**Expected:**
- The Fee Drag % cell displays exactly `—` (em dash)
- The dash is rendered in a muted/slate grey colour — NOT amber, NOT green, NOT red
- The cell does not display `null`, `0.00%`, `+0.00%`, or blank

**Pass:** `—` displayed in muted grey.
**Fail:** Wrong content or wrong colour treatment.

**Result:** [ ] PASS  [ ] FAIL  [ ] SKIP (no null fee drag trade in dataset)  **Notes:** ___

---

### V-FD-04 — Column header is interactive: sort icon present and changes on click

**Action:**
1. Observe the "Fee Drag %" column header before clicking — a sort icon (two arrows or up/down arrows) should be visible.
2. Click the header once.
3. Observe the icon and row order.
4. Click again.
5. Observe the icon and row order again.

**Expected:**
- Before clicking: a neutral double-arrow icon is visible in the header (muted colour).
- After first click: icon changes to a single upward arrow (ascending sort active); rows reorder by fee drag ascending — lowest `+X.XX%` first.
- After second click: icon changes to a single downward arrow (descending sort active); rows reorder by fee drag descending — highest `+X.XX%` first.
- Trades with null fee drag (`—`) always appear at the end of the sorted list regardless of direction.
- Clicking a third time returns to the unsorted/default order.

**Pass:** Sort icon changes with each click; rows reorder correctly; nulls at end.
**Fail:** Icon doesn't change, rows don't reorder, or nulls appear at top.

**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

## PATH-2: Trade History Summary Bar — Avg Fee Drag StatsCard

Remain on the Trade History page (`/#/TradeHistory`). Observe the row of StatsCards at the top of the page (above the filters panel).

---

### V-FD-05 — Avg Fee Drag StatsCard is present and positioned rightmost

**Action:** Observe all StatsCards in the summary bar.

**Expected:**
- A card labelled **"Avg Fee Drag"** is present
- It is the **rightmost card** in the summary bar (after "Avg Entry Dev.")
- The label text is "Avg Fee Drag" — NOT "Avg Slippage", "Fee Slippage", or any slippage-adjacent label
- On screens narrower than the full 6-card grid width, the card wraps to a second row — this is acceptable

**Pass:** "Avg Fee Drag" card present as rightmost stat.
**Fail:** Card absent, labelled incorrectly, or positioned before Avg Entry Dev.

**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

### V-FD-06 — Avg Fee Drag StatsCard renders with amber gradient background

**Action:** Observe the background styling of the "Avg Fee Drag" card compared to the other StatsCards.

**Expected:**
- The Avg Fee Drag card has a visible **amber/orange gradient** background (amber-tinted, not cyan/violet/emerald/rose)
- The card icon (TrendingDown) is rendered in amber/orange colour
- The gradient is visually consistent with how other cards use their respective gradient colours (e.g. Win Rate uses emerald when ≥50%, Total P&L uses emerald when positive)

**Pass:** Amber gradient background and icon colour visible; card is styled, not plain/flat.
**Fail:** Card renders with no gradient (plain dark background), wrong gradient colour, or icon is unstyled.

**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

### V-FD-07 — Avg Fee Drag StatsCard value format: `+X.XX%`

**Action:** Observe the value displayed on the Avg Fee Drag card.

**Expected:**
- The card displays a value in `+X.XX%` format (e.g. `+0.42%`) — always-positive with `+` prefix, 2 decimal places
- The value matches the portfolio mean of the `fee_drag_pct` values visible in the table (approximate check — exact match not required)
- If no trades have fee drag data (all null), the card displays `—`; otherwise `+X.XX%` is shown

**Pass:** `+X.XX%` format displayed; value is plausible given trades visible in the table.
**Fail:** Value shows without `+` prefix, shows negative (impossible for fee drag), or shows raw decimal instead of percentage.

**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

### V-FD-08 — Avg Fee Drag subtitle is visible and correct

**Action:** Observe the subtitle text below the value on the Avg Fee Drag card.

**Expected:**
- A subtitle reading **"Exit fees / gross proceeds"** is visible below the value in smaller, muted text
- The subtitle is clearly readable (not clipped or overflowing the card boundary at 1280px)

**Pass:** Subtitle text present and legible.
**Fail:** Subtitle absent, truncated, or overflowing card bounds.

**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

## Sign-Off Record

Complete this block and paste into `claude/cycles/2026-04-05__release-v2.5/qa_evidence_EPIC-03.md` — append to the EPIC-03 consolidation sign-off block under a "Visual staging test results" heading.

```
Visual staging test completed by: _______________
Date: _______________
Environment: [ ] Local dev  [ ] Staging (Render)
Seed state confirmed: [ ] Trades with fee drag data present  [ ] Null fee drag trade present (or SKIP noted)

PATH-1 — Fee Drag % Column:
  V-FD-01 (column present, correct position):       [ ] PASS  [ ] FAIL
  V-FD-02 (amber +X.XX% cell format):               [ ] PASS  [ ] FAIL
  V-FD-03 (null cell shows "—", muted colour):      [ ] PASS  [ ] FAIL  [ ] SKIP
  V-FD-04 (sort icon + sort behaviour):             [ ] PASS  [ ] FAIL

PATH-2 — Avg Fee Drag StatsCard:
  V-FD-05 (card present, rightmost, label correct): [ ] PASS  [ ] FAIL
  V-FD-06 (amber gradient background):              [ ] PASS  [ ] FAIL
  V-FD-07 (value format +X.XX%):                    [ ] PASS  [ ] FAIL
  V-FD-08 (subtitle text visible):                  [ ] PASS  [ ] FAIL

Overall visual verdict: [ ] ALL PASS  [ ] FAILURES — see notes
Notes: _______________

DoQ confirmation of visual sign-off: [ ] Confirmed — full EPIC-03 visual AC sign-off granted
```
