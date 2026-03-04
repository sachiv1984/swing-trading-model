**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 0.1.0
**Last Updated:** 2026-03-04
**Cycle:** 2026-03-04__release-v1.8
**Approved by:** Product Owner — 2026-03-04

---

# UX Specification — Risk Dashboard Page

## EPIC-01 / v1.8

---

## 1. Purpose

A dedicated Risk Dashboard page that consolidates all risk-awareness features into a single daily view. The user opens this page to understand their current risk exposure at a glance: how much capital is at risk, whether they are in drawdown, which positions are in grace period, and the per-position risk breakdown.

This page is read-only. It displays live data; it does not execute trades or modify positions.

---

## 2. Page Route and Navigation

- **Route:** `/risk` (or `/dashboard/risk` — confirmed in pre-alignment)
- **Nav label:** "Risk" (sidebar navigation item, between Portfolio and Analytics)
- **Access:** Always visible; no gating condition
- **Page title (browser):** "Risk Dashboard — Momentum Trading Assistant"
- **Page heading (h1):** "Risk Dashboard"

---

## 3. Page Layout

```
┌─────────────────────────────────────────────────────────────┐
│  [Sidebar Nav]  │  Risk Dashboard                           │
│                 │                                            │
│                 │  ┌──────────────┐  ┌───────────────────┐  │
│                 │  │ Portfolio    │  │ Current Drawdown  │  │
│                 │  │ Heat Gauge   │  │ Summary           │  │
│                 │  └──────────────┘  └───────────────────┘  │
│                 │                                            │
│                 │  ┌─────────────────────────────────────┐  │
│                 │  │ Grace Period Status Panel            │  │
│                 │  └─────────────────────────────────────┘  │
│                 │                                            │
│                 │  ┌─────────────────────────────────────┐  │
│                 │  │ Position-Level Risk Table            │  │
│                 │  └─────────────────────────────────────┘  │
│                 │                                            │
│                 │  ┌─────────────────────────────────────┐  │
│                 │  │ Prospective Heat Indicator           │  │
│                 │  └─────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Grid:** 2-column top row (Heat Gauge + Drawdown, ~50/50), then full-width rows below.
**Responsive:** Single column on narrow viewport.
**Data refresh:** On page load only. No polling. Manual refresh via browser reload.

---

## 4. Component Specifications

---

### 4.1 Portfolio Heat Gauge

**Data source:** `GET /portfolio` → `portfolio_heat_percent`
**Canonical formula:** `metrics_definitions.md §Portfolio Heat` v1.6.0

**Layout:**
- Card component with heading "Portfolio Heat"
- Large circular gauge (donut/arc style) or prominent horizontal bar
- Centre of gauge: current percentage value (e.g., "14.2%")
- Below gauge: threshold label (Low / Moderate / High / Extreme)
- Below label: sub-text showing portfolio total at-risk value in GBP (e.g., "£4,260 at risk")

**Colour coding — strictly from `metrics_definitions.md` v1.6.0 thresholds:**

| Range | Label | Colour | Hex |
|-------|-------|--------|-----|
| 0% ≤ heat < 10% | Low | Green | `#22c55e` |
| 10% ≤ heat < 20% | Moderate | Amber | `#f59e0b` |
| 20% ≤ heat < 30% | High | Orange | `#f97316` |
| heat ≥ 30% | Extreme | Red | `#ef4444` |

**Colour applies to:** gauge fill, threshold label badge, card border-left accent.

**States:**
- **Loaded:** gauge renders with current value and colour
- **Zero positions:** gauge shows 0%, label "Low", sub-text "No open positions"
- **Loading:** skeleton placeholder (grey animated bar) while API responds
- **Error:** "Unable to load heat data" with retry button

---

### 4.2 Current Drawdown Summary

**Data source:** `GET /analytics/metrics` → drawdown fields
**Fields used:** `max_drawdown_percent`, `current_drawdown_percent`, `days_underwater` (confirm field names match live API before implementation)

**Layout:**
- Card component with heading "Drawdown"
- Two metric rows:
  - **Current drawdown:** percentage from peak equity (e.g., "−3.4%")
  - **Days underwater:** integer count (e.g., "12 days")
- If not in drawdown (current_drawdown_percent = 0 or positive): show "At peak equity" with green indicator
- If in drawdown: show current drawdown % in red, days underwater in amber

**States:**
- **At peak / no drawdown:** "At peak equity ✓" — green
- **In drawdown:** current % in red, days in amber
- **No trade history:** "No closed trades — drawdown not calculable"
- **Loading:** skeleton
- **Error:** "Unable to load drawdown data"

---

### 4.3 Grace Period Status Panel

**Data source:** `GET /portfolio` → positions where `status = "GRACE"`
**Fields used:** `ticker`, `entry_date`, `grace_days_remaining`, `holding_days`

**Layout:**
- Full-width card with heading "Grace Period Positions"
- Badge showing count (e.g., "2 positions in grace period")
- Table:

| Ticker | Entry Date | Days in Grace | Days Remaining |
|--------|------------|---------------|----------------|
| AAPL | 2026-02-20 | 8 | 2 |
| MSFT | 2026-02-24 | 4 | 6 |

- **Days Remaining** column: colour-coded — ≥5 days: green; 2–4 days: amber; ≤1 day: red
- Row sorted by days remaining ascending (most urgent first)

**States:**
- **Empty (no grace positions):** "No positions currently in grace period" — muted text, no table
- **Loaded:** table renders
- **Loading:** skeleton rows
- **Error:** "Unable to load position data"

---

### 4.4 Position-Level Risk Table

**Data source:** `GET /portfolio` → all open positions
**Fields used:** `ticker`, `status`, `display_status`, `entry_price`, `current_price`, `current_stop`, `holding_days`, `pnl_pct`

**Layout:**
- Full-width card with heading "Position Risk"
- Table with columns:

| Ticker | State | Entry Price | Current Price | Stop Price | Stop Distance | Holding Days |
|--------|-------|-------------|---------------|------------|---------------|--------------|
| NVDA | PROFITABLE | 450.00 | 520.00 | 485.00 | −6.7% | 28 |
| TSLA | LOSING | 180.00 | 165.00 | 158.00 | −4.2% | 14 |
| META | GRACE | 340.00 | 328.00 | 320.00 | −2.4% | 9 |

- **Stop Distance:** `(current_stop - current_price) / current_price × 100` — always shown as negative (distance to stop below price)
- **State badge:**
  - GRACE: blue badge
  - LOSING: red badge
  - PROFITABLE: green badge
- **Sort order:** GRACE first, then LOSING, then PROFITABLE; within each group sort by stop distance ascending (tightest stop first = most at risk)
- **Prices:** GBP, 2 decimal places
- **Stop Distance:** 1 decimal place, always prefixed with −

**States:**
- **Empty:** "No open positions"
- **Loaded:** table renders
- **Loading:** skeleton rows
- **Error:** "Unable to load position data"

---

### 4.5 Prospective Heat Indicator

**Purpose:** Show the user what their portfolio heat would be if they added a hypothetical new position. This is purely informational — it does not execute or record anything.

**Layout:**
- Full-width card, collapsible (default: collapsed; heading "Prospective Heat" with expand chevron)
- When expanded:
  - Input row:
    - "Position size (shares)": numeric input, positive integers only
    - "Entry price (GBP)": numeric input, 2 decimal places, positive
    - "Stop price (GBP)": numeric input, 2 decimal places, positive, must be < entry price
  - "Calculate" button
  - Result row (shown after Calculate pressed):
    - "Projected heat: **18.4%**" — colour-coded per heat thresholds
    - "Heat increase: **+4.2%**" from current level
    - Threshold label changes if new heat crosses a boundary (e.g., Low → Moderate)
- Reset button clears inputs and result

**Validation:**
- Stop price must be less than entry price — inline error if not
- All fields required before Calculate is enabled
- Position size must be a positive integer

**Calculation:** Uses the canonical heat formula from `metrics_definitions.md §Portfolio Heat` applied to (existing positions + hypothetical position). All calculation performed backend-side — no client-side formula.

**States:**
- **Collapsed:** heading + expand control only
- **Expanded, no result:** input form only
- **Expanded, result shown:** input form + result row
- **Calculating:** loading spinner on Calculate button

---

## 5. Interactions and Edge Cases

| Scenario | Behaviour |
|----------|-----------|
| 0 open positions | Heat = 0%, "Low"; Grace panel empty; Risk table empty; Prospective Heat still usable |
| All positions profitable, no grace | Grace panel shows "No positions in grace period" |
| Heat exactly at threshold boundary (10.0%) | Classify as Moderate (10% ≤ heat < 20%) |
| Prospective heat > 30% | Result shown in red with "Extreme" label |
| API error on load | Each card shows its own error state independently; others remain functional |
| No trade history (new user) | Drawdown card: "No closed trades — drawdown not calculable" |

---

## 6. Data Dependencies Summary

| Component | Endpoint | Fields |
|-----------|----------|--------|
| Portfolio Heat Gauge | `GET /portfolio` | `portfolio_heat_percent` |
| Drawdown Summary | `GET /analytics/metrics` | `current_drawdown_percent`, `days_underwater` |
| Grace Period Panel | `GET /portfolio` | positions where `status = "GRACE"` |
| Position Risk Table | `GET /portfolio` | all open positions |
| Prospective Heat | `POST` or derived calc endpoint | hypothetical heat calculation |

> **Engineering pre-alignment item (ST-02):** Confirm `portfolio_heat_percent` is available in `GET /portfolio` response, or determine if a separate call is needed. Prospective heat calculation endpoint must be confirmed before ST-03 implementation begins.

---

## 7. Out of Scope for This Page

- Editing positions or stops (read-only page)
- Historical heat trend chart (deferred; no data model for stored heat history)
- Alerts or notifications (v2.0 scope)
- Export / print (v2.0 scope)
