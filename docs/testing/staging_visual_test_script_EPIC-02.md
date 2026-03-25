**Owner:** QA Lead
**Class:** QA Evidence (Class 7)
**Status:** Active
**Cycle:** 2026-03-24__release-v2.3
**Epic:** EPIC-02 — QA Automation Foundation
**Issued by:** Director of Quality
**Issued:** 2026-03-25

---

# Human Staging Test Script — EPIC-02 Visual AC

This script covers the visual acceptance criteria that Playwright cannot verify.
It must be executed against the **staging environment** before EPIC-02 PR sign-off is granted.

**Applies to stories:** ST-05 (smoke paths exercise these visual elements)

**Prerequisites:**
1. EPIC-02 branch is deployed to staging (or dev server running locally)
2. Staging DB has been reset and seeded:
   ```
   export STAGING_DATABASE_URL="postgresql://..."
   ./scripts/reset_staging_db.sh
   ./scripts/seeds/seed_all.sh
   ```
3. Browser: Chrome or Edge (tests written for Chromium)
4. Viewport: 1280×900 minimum

**Record results in:** `claude/cycles/2026-03-24__release-v2.3/qa_evidence_EPIC-02.md` — append to the ST-05 DoQ Sign-Off block.

---

## PATH-1: Add Trade — Visual Checks

Navigate to the staging frontend. Go to: **Trade Entry** (Menu → Trade Entry or `/#/TradeEntry`)

### V-PATH1-01 — Submit button gradient renders
**Action:** Observe the "Create Position" button before filling the form (button is disabled).
**Expected:** Button is rendered with a gradient colour (cyan to violet / blue-purple range) even in disabled state.
**Pass:** Gradient visible — button does not appear plain grey or unstyled.
**Fail:** Button renders as flat grey or with no colour treatment.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

### V-PATH1-02 — Form fields render with dark styling
**Action:** Observe the form panel containing Ticker Symbol, Market, Entry Date, Fill Price, Stop Price fields.
**Expected:** Input fields have a dark background (slate/charcoal), light text, and coloured focus border when clicked.
**Pass:** Fields visually distinct against page background; focused field shows coloured border (cyan/blue).
**Fail:** Fields are white-background, invisible, or misaligned.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

### V-PATH1-03 — "Creating..." spinner appears during submission
**Action:**
  1. Fill Ticker = `LGEN`, Entry Date = today, Fill Price (£) = `2.45`, Stop Price = `2.15`
  2. Wait for the position sizing widget to show a suggested shares value
  3. Click **Create Position** immediately
**Expected:** Button briefly shows a spinner icon and "Creating..." text before the page navigates away.
**Pass:** Spinner visible for at least one frame before navigation completes.
**Fail:** Button stays as "Create Position" with no loading indicator, or page freezes.
**Note:** This may be fast — use slow network throttle (DevTools → Network → Slow 3G) if needed.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

### V-PATH1-04 — Navigation to Positions page on success
**Action:** After clicking Create Position (continuing from V-PATH1-03).
**Expected:** Page navigates to the Positions page showing open positions.
**Pass:** URL changes to `/#/Positions` and at least one position is listed.
**Fail:** Page stays on TradeEntry, shows error, or navigates to wrong page.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

## PATH-2: View Portfolio — Visual Checks

Navigate to: **Positions** (Menu → Positions or `/#/Positions`)

*Prerequisites: seed_portfolio_trades.sql must have been run — LGEN and BARC positions should be present.*

### V-PATH2-01 — Positive P&L renders in green
**Action:** Observe the P&L column for LGEN (seeded with pnl=+£70.05) and BARC (+£96.05).
**Expected:** Positive P&L values display in a green colour (emerald/green range).
**Pass:** £70.05 and £96.05 values appear in green text.
**Fail:** Values appear in white, grey, or red.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

### V-PATH2-02 — Position cards render without overflow (default grid view)
**Action:** Observe the positions page in grid/card view (default view).
**Expected:** Each position card is fully contained within its bounds. Ticker, market badge, entry price, P&L, and stop price are all visible without truncation or overflow.
**Pass:** Cards render cleanly at 1280px wide with no text cut off.
**Fail:** Cards overlap, text is clipped, or layout breaks.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

### V-PATH2-03 — "New Position" button is visible and styled
**Action:** Observe the page header area.
**Expected:** A "New Position" button or link is visible, styled (not plain text link).
**Pass:** Button present with visible styling.
**Fail:** Button absent or renders as an unstyled plain link.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

---

## PATH-3: View Alerts — Visual Checks

Navigate to: **Notifications** (Menu → Notifications or `/#/notifications`)

*Prerequisites: seed_alerts.sql must have been run — 2 unread notifications should be present.*

### V-PATH3-01 — Unread notification has cyan left border
**Action:** Observe the notification rows. The "Stop Loss Approaching: LGEN" notification is seeded as unread.
**Expected:** Unread notifications have a visible cyan/teal left border stripe along the left edge of the row.
**Pass:** Cyan left border visible on unread row(s). Read rows have no such border.
**Fail:** No border visible, or all rows look the same regardless of read status.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

### V-PATH3-02 — Notification type icons render
**Action:** Observe the icon area of each notification row.
**Expected:** Each notification type has a distinct icon (e.g. stop_loss_approach shows a relevant icon, daily_portfolio_summary shows a different icon). Icons are not broken/missing.
**Pass:** Icons visible and distinct per notification type.
**Fail:** Icons missing, show broken image, or are identical across all types.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

### V-PATH3-03 — "Mark all as read" button is visually distinct
**Action:** Observe the "Mark all as read" button in the page header area.
**Expected:** Button is styled and clearly actionable — not plain text, not greyed out.
**Pass:** Button has visible styling (border, background, or colour treatment).
**Fail:** Button appears as plain unstyled text or is greyed-out/disabled.
**Result:** [ ] PASS  [ ] FAIL  **Notes:** ___

### V-PATH3-04 — Read vs unread visual distinction persists after page reload
**Action:**
  1. Click "Mark as read" on the "Stop Loss Approaching: LGEN" notification.
  2. Reload the page.
**Expected:** After reload, the previously-unread notification no longer shows the cyan left border.
**Pass:** Border absent after reload.
**Fail:** Border reappears after reload (optimistic update not persisted).
**Note:** This test requires a live staging backend. If running against mock-only Playwright, skip and note as staging-only.
**Result:** [ ] PASS  [ ] FAIL  [ ] SKIP (no live backend)  **Notes:** ___

---

## Sign-Off Record

Complete this block and paste into `qa_evidence_EPIC-02.md` → ST-05 DoQ Sign-Off section.

```
Visual staging test completed by: _______________
Date: _______________
Environment: [ ] Local dev  [ ] Staging (Render)
Seed state confirmed: [ ] reset run  [ ] seed_all.sh run

PATH-1 visual results:
  V-PATH1-01 (button gradient):       [ ] PASS  [ ] FAIL
  V-PATH1-02 (form field styling):    [ ] PASS  [ ] FAIL
  V-PATH1-03 ("Creating..." spinner): [ ] PASS  [ ] FAIL
  V-PATH1-04 (navigation on success): [ ] PASS  [ ] FAIL

PATH-2 visual results:
  V-PATH2-01 (green P&L):             [ ] PASS  [ ] FAIL
  V-PATH2-02 (card no overflow):      [ ] PASS  [ ] FAIL
  V-PATH2-03 (New Position button):   [ ] PASS  [ ] FAIL

PATH-3 visual results:
  V-PATH3-01 (cyan unread border):    [ ] PASS  [ ] FAIL
  V-PATH3-02 (notification icons):    [ ] PASS  [ ] FAIL
  V-PATH3-03 (Mark all button style): [ ] PASS  [ ] FAIL
  V-PATH3-04 (read state persists):   [ ] PASS  [ ] FAIL  [ ] SKIP

Overall visual verdict: [ ] ALL PASS  [ ] FAILURES — see notes
Notes: _______________________________________________

DoQ confirmation of visual sign-off: [ ] Confirmed — full ST-05 and EPIC-02 sign-off now granted
```
