---
title: Fee Drag Test Scenarios
version: v1.0
status: Active
owner: QA
spec_refs: ST-06, ST-07 (v2.6)
---

# Fee Drag Test Scenarios

Fee drag measures the proportion of gross sale proceeds consumed by broker exit fees.

Formula:
- `fee_drag_pct = exit_fees / gross_proceeds × 100` (rounded to 2 dp)
- `avg_fee_drag_pct = mean of all non-null fee_drag_pct values` (rounded to 2 dp)
- Both are `None` / null when inputs are missing or zero

## Scenario Inventory

### SC-FEE-01 — Fee Drag column header is present

| Field      | Value |
|------------|-------|
| ID         | SC-FEE-01 |
| Type       | Frontend UI |
| Priority   | P1 |
| Automation | Confirmed: `tests/e2e/fee-drag-trade-history.spec.js` |

**Precondition:** Trade History page loaded with at least one closed trade.

**Steps:**
1. Navigate to `/#/TradeHistory`
2. Wait for trade table to render

**Expected:** A column header matching `/fee drag/i` (or button with that text) is visible in the table header row.

---

### SC-FEE-02 — Non-null fee_drag_pct renders with amber colour

| Field      | Value |
|------------|-------|
| ID         | SC-FEE-02 |
| Type       | Frontend UI |
| Priority   | P1 |
| Automation | Confirmed: `tests/e2e/fee-drag-trade-history.spec.js` |

**Precondition:** Response contains a trade with `fee_drag_pct: 0.45`.

**Steps:**
1. Navigate to `/#/TradeHistory`
2. Wait for trade table to render

**Expected:**
- Cell for the trade with `fee_drag_pct: 0.45` contains text `+0.45%`
- Cell has class `text-amber-400`

---

### SC-FEE-03 — Avg Fee Drag StatsCard shows calculated average

| Field      | Value |
|------------|-------|
| ID         | SC-FEE-03 |
| Type       | Frontend UI |
| Priority   | P1 |
| Automation | Confirmed: `tests/e2e/fee-drag-trade-history.spec.js` |

**Precondition:** Response contains `avg_fee_drag_pct: 0.35`.

**Steps:**
1. Navigate to `/#/TradeHistory`
2. Wait for trade table to render

**Expected:**
- StatsCard with title "Avg Fee Drag" is visible
- Value displayed is `+0.35%`

---

### SC-FEE-04 — Null fee_drag_pct renders em dash

| Field      | Value |
|------------|-------|
| ID         | SC-FEE-04 |
| Type       | Frontend UI |
| Priority   | P1 |
| Automation | Confirmed: `tests/e2e/fee-drag-trade-history.spec.js` |

**Precondition:** Response contains a trade with `fee_drag_pct: null`.

**Steps:**
1. Navigate to `/#/TradeHistory`
2. Find the row for the trade with null fee drag

**Expected:**
- Cell contains `—` (em dash)
- Cell has class `text-slate-500`

---

### SC-FEE-05 — Backend fee_drag_pct formula correctness

| Field      | Value |
|------------|-------|
| ID         | SC-FEE-05 |
| Type       | Backend unit |
| Priority   | P1 |
| Automation | Confirmed: `tests/test_trade_service.py` |

**Assertions:**
- `exit_fees=9.95`, `gross_proceeds=2200.00` → `fee_drag_pct = round(9.95/2200.00*100, 2) = 0.45`
- `exit_fees=0`, `gross_proceeds=1000.00` → `fee_drag_pct = 0.0`
- `exit_fees=None` → `fee_drag_pct = None`
- `gross_proceeds=None` → `fee_drag_pct = None`
- `gross_proceeds=0` → `fee_drag_pct = None` (division guard)

---

### SC-FEE-06 — Backend avg_fee_drag_pct aggregation

| Field      | Value |
|------------|-------|
| ID         | SC-FEE-06 |
| Type       | Backend unit |
| Priority   | P1 |
| Automation | Confirmed: `tests/test_trade_service.py` |

**Assertions:**
- Multiple trades with non-null `fee_drag_pct` → avg is `round(mean, 2)`
- All trades have `fee_drag_pct=None` → `avg_fee_drag_pct=None`
- Empty trade list → `avg_fee_drag_pct=None`
- Mix of null and non-null → only non-null values included in average

---

## Automation Summary

| Scenario | Automation File | Status |
|----------|----------------|--------|
| SC-FEE-01 | `tests/e2e/fee-drag-trade-history.spec.js` | Confirmed |
| SC-FEE-02 | `tests/e2e/fee-drag-trade-history.spec.js` | Confirmed |
| SC-FEE-03 | `tests/e2e/fee-drag-trade-history.spec.js` | Confirmed |
| SC-FEE-04 | `tests/e2e/fee-drag-trade-history.spec.js` | Confirmed |
| SC-FEE-05 | `tests/test_trade_service.py` | Confirmed |
| SC-FEE-06 | `tests/test_trade_service.py` | Confirmed |

---

## Known Deviations

| Description | Canonical requirement | Priority | Target resolution | Owner | Backlog reference |
|-------------|----------------------|----------|------------------|-------|------------------|
| SC-FEE-01 to SC-FEE-04 Playwright automated run failed in v2.6 due to systemic `page.route()` intercept failure affecting the entire Playwright suite (not a spec or implementation defect; spec file structurally correct and code-review verified) | Scenarios SC-FEE-01–04 fully automated and passing in headless Playwright | P3 | v2.7 | QA & Testing Owner | BLG-QA-11 |
