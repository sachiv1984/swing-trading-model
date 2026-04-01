---
**Owner:** QA & Testing Owner
**Class:** Working Document (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-04-01
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Scenario covered:** SC-SLIP-01 (docs/testing/slippage_scenarios.md)
**Sprint:** 2026-03-31__release-v2.4 — ST-12
---

# Human Test Runbook — SC-SLIP-01: Fill Price Captured on Trade Entry

---

## Why this is manual

SC-SLIP-01 requires entering a trade with a fill price through the live UI and confirming the value persists in the database. This involves:
- Live staging environment with a working backend
- A real (or test) trade entry form interaction
- Database confirmation that `fill_price` and `slippage_pct` were written

Playwright cannot automate the fill price field interaction because trade entry in the current UI delegates to the Base44 entity store, which cannot be fully intercepted with `page.route()` in a way that also tests persistence.

---

## Prerequisites

| # | Requirement | Check |
|---|-------------|-------|
| 1 | Staging environment running (backend accessible at `$STAGING_URL`) | [ ] |
| 2 | Seed data loaded — at least one open position exists to exit | [ ] |
| 3 | Trade history page accessible | [ ] |
| 4 | Tester has login access (if auth required) | [ ] |

---

## Test Steps

### Step 1 — Open an existing position

1. Navigate to **Positions** page
2. Identify any open position (note the ticker and current market price)
3. Click the **Exit** (LogOut icon) button for that position

### Step 2 — Enter fill price that differs from market price

In the Exit modal:

1. Confirm the **Shares** field is pre-filled
2. In the **Exit Price** field: enter the current market price (e.g. `£200.00`)
3. In the **Fill Price** field: enter a value that is **different** from exit price
   - Example: exit price = `200.00`, fill price = `200.50` (50p above market)
   - This should produce **positive slippage** = `(200.50 − 200.00) / 200.00 × 100` = **+0.25%**
4. Set exit date to today
5. Click **Confirm Exit**

### Step 3 — Confirm in Trade History

1. Navigate to **Trade History**
2. Find the trade just closed (most recent row)
3. Check the **Slippage** column for that row:

| Expected result | Pass condition |
|----------------|----------------|
| Slippage cell shows `+0.25%` (or the computed value) | Matches formula: `(fill − entry) / entry × 100` |
| Cell renders in **rose / red** colour (unfavourable, filled above market) | `text-rose-400` class applied |
| All other rows in the table remain unchanged | No side-effects on other rows |

4. Check the **Avg Slippage** StatsCard at the top of Trade History:
   - If this is the **first** trade with a fill price: value should be `+0.25%`
   - If other fill-price trades exist: value should be the updated mean

### Step 4 — Repeat with favourable slippage (optional but recommended)

Exit another position with fill price **below** market:
- Exit price `200.00`, fill price `199.50`
- Expected slippage: `−0.25%`
- Expected colour: **emerald / green** (`text-emerald-400`)

---

## Pass/Fail Criteria

| # | Check | Expected | Result |
|---|-------|----------|--------|
| SC-SLIP-01-A | Fill price field is present in Exit modal | Visible and accepts numeric input | [ ] Pass / [ ] Fail |
| SC-SLIP-01-B | Trade saved with fill_price captured | Slippage column shows computed value (not "—") | [ ] Pass / [ ] Fail |
| SC-SLIP-01-C | slippage_pct formula correct | Value matches `(fill − entry) / entry × 100` | [ ] Pass / [ ] Fail |
| SC-SLIP-01-D | Trade appears in Trade History with slippage populated | Non-null value visible in Slippage column | [ ] Pass / [ ] Fail |

---

## Failure recording

If any check fails, record:
```
Date: ___________
Tester: ___________
Step failed: ___________
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
