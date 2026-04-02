---
**Owner:** QA & Testing Owner
**Class:** Working Document (Class 3)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-04-02
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Scenario covered:** SC-SLIP-01 (docs/testing/slippage_scenarios.md)
**Sprint:** 2026-03-31__release-v2.4 — ST-12
**Change:** v1.0 → v1.1: Corrected form reference from Exit modal to Trade Entry form.
  Prior version (v1.0) incorrectly instructed testers to enter fill price in the Exit modal.
  The fill price field exists only on Trade Entry. Exit modal accepts exit price only.
  Decision authority: PO/Challenger debate 2026-04-02.
---

# Human Test Runbook — SC-SLIP-01: Fill Price Captured on Trade Entry

---

## Why this is manual

SC-SLIP-01 requires entering a new trade via the live Trade Entry form with a fill price, then exiting
that position, and confirming the entry deviation value appears correctly in Trade History.
This involves a live staging backend — `page.route()` interception cannot test DB persistence
of `user_fill_price` through to `trade_history.fill_price`.

---

## Prerequisites

| # | Requirement | Check |
|---|-------------|-------|
| 1 | Staging environment running (frontend + backend accessible) | [ ] |
| 2 | At least one watchlist entry or known ticker to use for the test trade | [ ] |
| 3 | Trade Entry page accessible at `/#/TradeEntry` | [ ] |
| 4 | Trade History page accessible at `/#/TradeHistory` | [ ] |

---

## Test Steps

### Step 1 — Enter a new position with fill price

1. Navigate to **Trade Entry** (`/#/TradeEntry`)
2. Complete required fields:
   - Ticker: e.g. `TSCO`
   - Market: `UK`
   - Entry Price: `200.00`
   - Shares: `10`
   - Stop Price: `185.00`
   - Entry Date: today
3. In the **Fill Price (optional)** field enter `200.50`
   - This is 50p above the limit — unfavourable fill, positive deviation
   - Expected entry deviation: `(200.50 − 200.00) / 200.00 × 100 = +0.25%`
4. Submit the form

### Step 2 — Exit the position

1. Navigate to **Positions** (`/#/Positions`)
2. Find the TSCO position just entered
3. Click the Exit (LogOut) button
4. In the Exit modal:
   - Exit Price: `210.00`
   - Exit Date: today
   - Reason: Manual Exit
5. Confirm exit

### Step 3 — Verify in Trade History

1. Navigate to **Trade History** (`/#/TradeHistory`)
2. Find the TSCO trade (most recent row)
3. Check the **Slippage** column (displays entry deviation):

| Check | Expected | Result |
|-------|----------|--------|
| SC-SLIP-01-A | Fill Price field is present and accepts input on Trade Entry form | Visible, numeric | [ ] Pass / [ ] Fail |
| SC-SLIP-01-B | Trade History shows `+0.25%` in Slippage column for this trade | `+0.25%` rendered | [ ] Pass / [ ] Fail |
| SC-SLIP-01-C | Cell colour is rose/red (positive = unfavourable fill above limit) | `text-rose-400` | [ ] Pass / [ ] Fail |
| SC-SLIP-01-D | Avg Entry Dev. StatsCard updates to reflect this trade's deviation | Non-null, ~`+0.25%` if only trade | [ ] Pass / [ ] Fail |

### Step 4 — Verify null case (fill price omitted)

1. Enter another test trade **without** entering a fill price
2. Exit that position
3. Confirm Trade History shows `—` in Slippage column for that trade
4. Confirm the Avg Entry Dev. StatsCard still shows a value (excludes null trades from average)

| Check | Expected | Result |
|-------|----------|--------|
| SC-SLIP-01-E | Trade without fill price shows `—` in Slippage column | `—` (em dash) | [ ] Pass / [ ] Fail |
| SC-SLIP-01-F | StatsCard average excludes the null-slippage trade | Average unchanged | [ ] Pass / [ ] Fail |

---

## Failure recording

```
Date: ___________
Tester: ___________
Check failed: ___________
Expected: ___________
Actual: ___________
Screenshot path: ___________
Backlog item raised: ___________
```

---

## Sign-off

```
Tester: _______________________   Date: ___________
Result: [ ] Pass  [ ] Pass with notes  [ ] Fail
Notes: _________________________________________________
```
