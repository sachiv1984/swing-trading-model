**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Active
**Version:** 0.1.8
**Last Updated:** 2026-03-09 (v1.9 Sprint 1 post-ship — §11 deviations resolved)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source:** docs/design/2026-03-04__release-v1.8/risk-dashboard/ux_spec.md
**Confirmed by:** Head of Specs Team — 2026-03-04

---

# Frontend Specification — Risk Dashboard Page

**Route:** `/risk`
**Release:** v1.8
**EPIC:** EPIC-01

---

## 1. Page Identity

| Field | Value |
|-------|-------|
| Route | `/risk` |
| Nav label | Risk |
| Browser title | Risk Dashboard — Momentum Trading Assistant |
| Page heading (h1) | Risk Dashboard |
| Nav position | Between Portfolio and Analytics |
| Access control | Always visible; no gating |

---

## 2. Layout

Two-column top row (Portfolio Heat Gauge + Drawdown Summary, approximately equal width), followed by three full-width rows: Grace Period Status Panel, Position-Level Risk Table, Prospective Heat Indicator.

Single-column layout on narrow viewports (below standard breakpoint).

Data refresh: on page load only. No polling. No auto-refresh.

---

## 3. Component: Portfolio Heat Gauge

### 3.1 Data

- **Source:** `GET /portfolio`
- **Field:** `portfolio_heat_percent` (number, 0–100)
- **Canonical formula:** `docs/specs/metrics_definitions.md §Portfolio Heat` v1.6.0

### 3.2 Display

- Card heading: "Portfolio Heat"
- Gauge style: circular arc or prominent horizontal bar (engineering choice; must be consistent with design source)
- Centre/primary value: current percentage formatted to 1 decimal place (e.g., `14.2%`)
- Secondary: threshold label badge (see §3.3)
- Tertiary: GBP value at risk in smaller text (e.g., `£4,260 at risk`) — derived from portfolio response

### 3.3 Colour Thresholds

Thresholds are canonical and sourced from `metrics_definitions.md §Portfolio Heat Display Thresholds` v1.6.0. Must not be altered without a spec version increment.

| Condition | Label | Colour | Hex |
|-----------|-------|--------|-----|
| 0% ≤ heat < 10% | Low | Green | `#22c55e` |
| 10% ≤ heat < 20% | Moderate | Amber | `#f59e0b` |
| 20% ≤ heat < 30% | High | Orange | `#f97316` |
| heat ≥ 30% | Extreme | Red | `#ef4444` |

Colour applies to: gauge fill, threshold label badge, card left-border accent.

### 3.4 States

| State | Behaviour |
|-------|-----------|
| Loaded | Gauge renders with value, label, and colour |
| Zero positions | 0%, label "Low", sub-text "No open positions" |
| Loading | Skeleton placeholder (animated grey bar) |
| Error | "Unable to load heat data" + retry button |

---

## 4. Component: Current Drawdown Summary

### 4.1 Data

- **`current_drawdown_percent`** — Source: `GET /portfolio` (`PortfolioOverview.current_drawdown_percent`)
  - Value is `<= 0.0`; zero means portfolio is at peak equity
- **`days_underwater`** — Source: `GET /analytics/metrics` (behavioral metrics section)
  - Field: `days_underwater` (integer) — maximum days since peak running equity, computed from trade P&L sequence
  - Documented in `docs/specs/api_contracts/analytics_endpoints.md` §behavioral metrics

> **Note (Head of Specs Team — 2026-03-06):** §4.1 previously listed `GET /analytics/metrics` as the source for both fields. Investigation for ST-06 confirmed that `current_drawdown_percent` is computed by `drawdown_service.py` and returned on `GET /portfolio` (confirmed in `portfolio_service.py` and `openapi.yaml` PortfolioOverview schema). `days_underwater` is computed by `analytics_service.py` and returned on `GET /analytics/metrics`. Split-source data model documented here. `days_underwater` is absent from `openapi.yaml` AnalyticsMetricsResponse (schema is `additionalProperties: true`); a schema addition is deferred to a future spec debt cycle. DEV-ST03-08 resolved.

### 4.2 Display

- Card heading: "Drawdown"
- Two metric rows:
  - **Current drawdown:** formatted as `−3.4%` (negative sign, 1 decimal place). Colour: red if in drawdown.
  - **Days underwater:** integer (e.g., `12 days`). Colour: amber if > 0.

### 4.3 States

| State | Behaviour |
|-------|-----------|
| At peak equity | "At peak equity ✓" — green indicator; days underwater row not shown |
| In drawdown | Current % in red, days underwater in amber |
| No trade history | "No closed trades — drawdown not calculable" — muted text |
| Loading | Skeleton |
| Error | "Unable to load drawdown data" |

---

## 5. Component: Grace Period Status Panel

### 5.1 Data

- **Source:** `GET /portfolio` → positions where `status = "GRACE"`
- **Fields:** `ticker`, `entry_date`, `grace_days_remaining`, `holding_days`

### 5.2 Display

- Card heading: "Grace Period Positions"
- Count badge: "N positions in grace period" where N is the count
- Table:

| Column | Source field | Format |
|--------|-------------|--------|
| Ticker | `ticker` | Uppercase string |
| Entry Date | `entry_date` | DD MMM YYYY |
| Days in Grace | `holding_days` | Integer |
| Days Remaining | `grace_days_remaining` | Integer, colour-coded |

### 5.3 Days Remaining Colour Coding

| Days remaining | Colour |
|----------------|--------|
| ≥ 5 | Green |
| 2–4 | Amber |
| ≤ 1 | Red |

### 5.4 Sort Order

Ascending by `grace_days_remaining` (most urgent / fewest days remaining first).

### 5.5 States

| State | Behaviour |
|-------|-----------|
| Empty (no grace positions) | "No positions currently in grace period" — muted text, no table |
| Loaded | Table renders |
| Loading | Skeleton rows |
| Error | "Unable to load position data" |

---

## 6. Component: Position-Level Risk Table

### 6.1 Data

- **Source:** `GET /portfolio` → all open positions
- **Fields:** `ticker`, `status`, `display_status`, `entry_price`, `current_price`, `current_stop`, `holding_days`, `pnl_pct`

### 6.2 Display

- Card heading: "Position Risk"
- Full-width table:

| Column | Source | Format |
|--------|--------|--------|
| Ticker | `ticker` | Uppercase string |
| State | `status` | Badge — see §6.3 |
| Entry Price | `entry_price` | GBP, 2 decimal places |
| Current Price | `current_price` | GBP, 2 decimal places |
| Stop Price | `current_stop` | GBP, 2 decimal places |
| Stop Distance | Derived | `(current_stop − current_price) / current_price × 100`, 1 decimal place, prefixed `−` |
| Holding Days | `holding_days` | Integer |

Stop Distance derivation is purely presentational (display arithmetic on backend-provided values — not a new calculation). The underlying stop price is always sourced from the backend.

### 6.3 State Badges

| Status value | Badge label | Badge colour |
|-------------|-------------|--------------|
| GRACE | GRACE | Blue |
| LOSING | LOSING | Red |
| PROFITABLE | PROFITABLE | Green |

### 6.4 Sort Order

Primary: status group order — GRACE first, then LOSING, then PROFITABLE.
Secondary within group: ascending by stop distance (tightest/smallest distance first = most at risk).

### 6.5 States

| State | Behaviour |
|-------|-----------|
| Empty | "No open positions" |
| Loaded | Table renders |
| Loading | Skeleton rows |
| Error | "Unable to load position data" |

---

## 7. Component: Prospective Heat Indicator

### 7.1 Purpose

Allows the user to estimate portfolio heat impact of a hypothetical new position before entry. Read-only and informational — does not create, record, or execute anything.

### 7.2 Layout

- Collapsible card; default state: **collapsed**
- Card heading: "Prospective Heat" + expand/collapse chevron
- When expanded: input form + result section

### 7.3 Inputs

| Field | Type | Validation |
|-------|------|-----------|
| Position size (shares) | Numeric integer | Required; positive integer; > 0 |
| Entry price (GBP) | Numeric decimal | Required; positive; 2 decimal places |
| Stop price (GBP) | Numeric decimal | Required; positive; must be < entry price |

- "Calculate" button: enabled only when all three fields are valid
- "Reset" button: clears all inputs and result

### 7.4 Calculation

All calculation performed server-side using the canonical heat formula (`metrics_definitions.md §Portfolio Heat`). No client-side formula re-implementation.

- Endpoint: to be confirmed in ST-02 pre-alignment (may be a new query parameter on `GET /portfolio` or a dedicated endpoint)
- Input: current portfolio state + hypothetical position parameters
- Output: projected heat percentage

### 7.5 Result Display

Shown after Calculate is pressed successfully:

- "Projected heat: **X.X%**" — value formatted to 1 decimal place, colour-coded per heat thresholds (§3.3)
- "Heat increase: **+X.X%**" from current level — colour-coded: green if decrease, amber/orange/red per resulting threshold
- Threshold label changes if hypothetical position crosses a boundary

### 7.6 States

| State | Behaviour |
|-------|-----------|
| Collapsed | Heading + expand control only |
| Expanded, no result | Input form only |
| Expanded, calculating | Spinner on Calculate button; inputs disabled |
| Expanded, result shown | Input form + result row |
| Calculation error | "Unable to calculate — please try again" inline error |
| Stop ≥ entry price | Inline validation error on stop price field; Calculate disabled |

---

## 8. Error Handling

Each component handles its own error state independently. A single API failure must not cause the entire page to become blank or non-functional. Components that load successfully should render; failed components display their individual error state with a retry option.

---

## 9. Acceptance Test Reference

Test scenarios for this page: `docs/testing/` (ST-04 output — authored by QA & Testing Owner).

Key boundary conditions to cover:
- Heat exactly at 10%, 20%, 30% threshold values
- Grace period position at day 1, day 10 (boundary), day 11 (expired / not in grace)
- All three position states present simultaneously
- Prospective heat calculation that crosses a threshold boundary
- All API error states

---

## 10. Constraints

- All displayed values are sourced from backend responses. No client-side recalculation of metric values.
- Colour hex values are canonical (§3.3) and must not be altered without a spec version increment referencing `metrics_definitions.md`.
- The page is read-only. No position modification, trade execution, or data entry (except Prospective Heat indicator inputs, which are ephemeral and not persisted).

---

---

## 11. Known Deviations

### v1.8 Delivery Deviations — All Resolved in v1.9 Sprint 1

The following deviations were identified at v1.8 sprint execution and accepted for v1.8 by Product Owner (2026-03-05). All were resolved in v1.9 Sprint 1 (EPIC-04, 2026-03-09) except DEV-ST03-08 and DEV-ST03-10 which were resolved earlier.

| Ref | Priority | Canonical Requirement | v1.8 Actual | Resolution | Owner | Backlog Ref |
|-----|----------|-----------------------|-------------|------------|-------|-------------|
| DEV-ST03-01 | P2 | §8: Each component renders its own error state independently on `GET /portfolio` failure | Entity store fallback (`base44.entities.Position/Portfolio`) activates on API failure; error states not displayed when entity data is available | RESOLVED 2026-03-09 — v1.9 Sprint 1 (EPIC-04, ST-08): ErrorCard sub-components added to all 5 components; `positionError` suppressed during entity fallback; error states now independent per §8. Commit `20e688f`. | Head of Engineering | BLG-RD-01 |
| DEV-ST03-02 | P3 | §5.5: GracePeriodPanel renders "Unable to load position data" error state | On API failure `positions` is `[]`; "No positions in grace period" shown — indistinguishable from valid empty state | RESOLVED 2026-03-09 — v1.9 Sprint 1 (EPIC-04, ST-08): distinct error card rendered before empty-state check in GracePeriodPanel. | Head of Engineering | BLG-RD-02 |
| DEV-ST03-03 | P2 | §6.4: Sort by stop distance ascending (tightest/smallest first = most at risk) | Sorted descending (largest stop distance first); Base44 prompt incorrectly specified "descending" | RESOLVED 2026-03-09 — v1.9 Sprint 1 (EPIC-04, ST-09): `STATUS_ORDER` primary then `(a._stopDist ?? Infinity) - (b._stopDist ?? Infinity)` ascending sort applied. | Head of Engineering | BLG-RD-03 |
| DEV-ST03-04 | P2 | §6.2: Stop Price column (`current_stop`, GBP, 2 dp) in Position Risk Table | Stop Price column absent; Stop Distance % shown instead (presentational derivation only) | RESOLVED 2026-03-09 — v1.9 Sprint 1 (EPIC-04, ST-09): Stop Price column header and cell (`£${pos.current_stop.toFixed(2)}`) added to PositionRiskTable. | Head of Engineering | BLG-RD-04 |
| DEV-ST03-05 | P3 | §6.3: GRACE badge colour = Blue | GRACE badge rendered in Amber | RESOLVED 2026-03-09 — v1.9 Sprint 1 (EPIC-04, ST-10): `statusBadge.GRACE = "bg-blue-500/20 text-blue-400 border-blue-500/30"`. | Head of Engineering | BLG-RD-05 |
| DEV-ST03-06 | P3 | §3.2: "GBP value at risk" as tertiary metric in Heat Gauge | Absent | RESOLVED 2026-03-09 — v1.9 Sprint 1 (EPIC-04, ST-10): `totalAtRisk` computed from `positionRisks[].position_risk_gbp` sum; rendered as `£${totalAtRisk.toFixed(2)} at risk` in HeatGauge SVG text. | Head of Engineering | BLG-RD-06 |
| DEV-ST03-07 | P3 | §5.2: "Days in Grace" (`holding_days`) column in Grace Period table | `holding_days` column absent from Grace Period table | RESOLVED 2026-03-09 — v1.9 Sprint 1 (EPIC-04, ST-09): `holding_days` column added to GracePeriodPanel rendering `{pos.holding_days}d in grace`. | Head of Engineering | BLG-RD-07 |
| DEV-ST03-08 | — | §4.1: Drawdown data source is `GET /analytics/metrics` | RESOLVED 2026-03-06 — §4.1 updated to split-source model: `current_drawdown_percent` from `GET /portfolio`; `days_underwater` from `GET /analytics/metrics`. See §4.1 note. | Head of Specs Team | BLG-RD-08 (closed) |
| DEV-ST03-09 | P3 | §7.5: Threshold label changes if hypothetical position crosses a boundary | `ProspectiveHeatPanel.js` renders projected heat % and delta only — threshold label absent from result display | RESOLVED 2026-03-09 — v1.9 Sprint 1 (EPIC-04, ST-09): `heatThreshold()` function returns `{label, color}` for 4 bands (Low/Moderate/High/Extreme); threshold label badge rendered alongside projected heat %. | Head of Engineering | BLG-RD-09 |
| DEV-ST03-10 | P2 | §1: Nav label "Risk", nav position between Portfolio and Analytics, always visible | Navigation sidebar entry absent — page is inaccessible via normal UX; route `/risk` IS registered and accessible via direct URL | RESOLVED 2026-03-05 — nav entry added (index.js fix) | Head of Engineering | — |
| DEV-ST03-11 | P2 | §6.2: Entry Price column — "GBP, 2 decimal places" for all positions | US position entry prices display in native USD ($) instead of GBP (£); backend returns `entry_price` in native currency, not GBP-converted | RESOLVED 2026-03-09 — v1.9 Sprint 1 (EPIC-04, ST-07): `portfolio_service.py` converts `entry_price` to GBP using `stored_fx_rate` for US positions. 5 new golden output vectors (FX-01–FX-05). Commit `b31536f`. | Head of Engineering | BLG-RD-10 |
| DEV-ST03-12 | P2 | §6.2: Stop Distance % derived as `(current_price − current_stop) / current_price × 100` — assumes both values in GBP | `current_stop` returned in native USD for US positions; `current_price` is in GBP; display derivation mixes currencies → Stop Distance % incorrect for all US positions | RESOLVED 2026-03-09 — v1.9 Sprint 1 (EPIC-04, ST-07): `portfolio_service.py` converts `current_stop` to GBP using `stored_fx_rate` for US positions. Commit `b31536f`. | Head of Engineering | BLG-RD-11 |

**All v1.8 deviations resolved.** No active deviations as of v1.9 Sprint 1 (2026-03-09).

**v1.8 acceptance:** Product Owner, 2026-03-05 (DEV-ST03-01 through DEV-ST03-12)

**QA observation filed:** QA-OBS-ST07-01 (non-blocking) — `current_price` uses `live_fx_rate` while `entry_price_gbp` and `current_stop_gbp` use `stored_fx_rate`. Minor basis discrepancy in Stop Distance % for US positions (second-order, typically < 1% of the percentage). Pre-existing design pattern. No action required. Logged as future refinement consideration.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 0.1.8 | 2026-03-09 | v1.9 Sprint 1 post-ship closure: §11 deviations DEV-ST03-01 through DEV-ST03-07, DEV-ST03-09, DEV-ST03-11, DEV-ST03-12 all marked RESOLVED with resolution detail (EPIC-04 commits b31536f, 20e688f). QA-OBS-ST07-01 noted. Table header updated from "Resolution Target" to "Resolution". |
| 0.1.7 | 2026-03-06 | ST-06 / DEV-ST03-08 resolution: §4.1 updated to split-source data model — `current_drawdown_percent` from `GET /portfolio`, `days_underwater` from `GET /analytics/metrics`. DEV-ST03-08 marked resolved in §11. Head of Specs Team decision 2026-03-06. |
| 0.1.6 | 2026-03-06 | §11 deviation compliance update: backlog references assigned for all active deviations (BLG-RD-01 through BLG-RD-11). Updated by Delivery Verification Engine 2026-03-06 per standard mode deviation compliance. |
| 0.1.5 | 2026-03-05 | Added DEV-ST03-12 (P2): `current_stop` returned in USD for US positions; Stop Distance % display derivation mixes currencies per §6.2. Found SC-RD-27 network tab inspection. Acceptance pending PO. |
| 0.1.4 | 2026-03-05 | Added DEV-ST03-11 (P2): US position entry prices display in USD instead of GBP per §6.2. Found SC-RD-14 live execution. DEV-ST03-10 marked RESOLVED (nav fix applied). |
| 0.1.3 | 2026-03-05 | Added DEV-ST03-10 (P2) to §11: Navigation sidebar entry absent for /risk page per §1. Identified during live scenario execution of SC-RD-01. Subsequently resolved by fix 2026-03-05. |
| 0.1.2 | 2026-03-05 | Added DEV-ST03-09 (P3) to §11: ProspectiveHeatPanel missing threshold label per §7.5. Identified by Director of Quality during ST-04 QA review. Accepted for v1.8; v1.9 resolution target. |
| 0.1.1 | 2026-03-05 | Added §11 Known Deviations. 8 deviations (3×P2, 4×P3, 1×P2 awaiting spec owner) identified from v1.8 delivery and accepted for v1.8 by Product Owner. All carry v1.9 resolution target. |
| 0.1.0 | 2026-03-04 | Initial specification. Design source: docs/design/2026-03-04__release-v1.8/risk-dashboard/ux_spec.md. Approved for EPIC-01 Sprint Planning. |
