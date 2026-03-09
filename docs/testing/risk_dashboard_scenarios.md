**Owner:** QA & Testing Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.1
**Last Updated:** 2026-03-09
**Derived from:** `docs/specs/frontend/pages/risk_dashboard.md` v0.1.1; `docs/specs/metrics_definitions.md` v1.6.0
**Sprint:** 2026-03-04__release-v1.8 — ST-04
**Roadmap item:** §3.4 — Risk Dashboard

---

# Acceptance Test Scenarios — Risk Dashboard Page

---

## 1. Scope

These scenarios verify the Risk Dashboard page (`/risk`) against canonical specifications. All expected values are derived from:

- `docs/specs/metrics_definitions.md §Portfolio Heat Display Thresholds` v1.6.0 (colour thresholds)
- `docs/specs/metrics_definitions.md §Portfolio Heat` v1.6.0 (heat formula)
- `docs/specs/metrics_definitions.md §Position Risk` v1.6.0 (position risk formula)
- `docs/specs/frontend/pages/risk_dashboard.md` v0.1.1 (page behaviour, component states, sort orders)

---

## 2. Known Deviations Affecting Test Execution (v1.8)

The following accepted deviations (documented in `risk_dashboard.md §11`) affect how specific scenarios must be executed or interpreted. Where a scenario is affected, a `[DEV-ST03-xx]` marker is included.

| Ref | Priority | Affect on test execution |
|-----|----------|--------------------------|
| DEV-ST03-01 | P2 | Entity fallback (`base44.entities`) activates on API failure. To test API error states (SC-RD-24 through SC-RD-28), the QA Lead must ensure the entity store contains no matching data, OR test in an environment where the entity store is unavailable. Otherwise the fallback activates and error states do not display. |
| DEV-ST03-02 | P3 | GracePeriodPanel shows "No positions in grace period" on both API failure AND valid empty state. QA Lead must distinguish by checking browser dev tools network tab — on API failure the portfolio request will show an error response. |
| DEV-ST03-03 | P2 | Position Risk Table sort order is **descending** by stop distance (largest first) in v1.8 implementation. Spec §6.4 requires ascending (tightest first). SC-RD-18 documents canonical requirement; v1.8 expected result reflects the known deviation. |
| DEV-ST03-04 | P2 | Stop Price column is absent from Position Risk Table in v1.8. SC-RD-17 notes this absence. |
| DEV-ST03-05 | P3 | GRACE badge renders in Amber in v1.8. Spec §6.3 requires Blue. |

---

## 3. Canonical Formulas (Reference)

### Portfolio Heat
```
Portfolio_Heat_Percent = (Sum of Position_Risk_GBP for all open positions)
                         / Portfolio_Value_GBP × 100
```
Source: `metrics_definitions.md §Portfolio Heat` v1.6.0

### Position Risk (GBP)
```
UK positions (GBP): Position_Risk_GBP = (entry_price_gbp − stop_price_gbp) × shares
                    [Note: UK prices in pence must be ÷ 100 before applying]
US positions (USD): Position_Risk_GBP = (entry_price_usd − stop_price_usd) × shares / fx_rate
```
Source: `metrics_definitions.md §Position Risk` v1.6.0

### Heat Display Thresholds
| Band | Range | Colour hex | Label |
|------|-------|-----------|-------|
| Low | 0% ≤ heat < 10% | `#22c55e` | Low |
| Moderate | 10% ≤ heat < 20% | `#f59e0b` | Moderate |
| High | 20% ≤ heat < 30% | `#f97316` | High |
| Extreme | heat ≥ 30% | `#ef4444` | Extreme |

Boundary values (10%, 20%, 30%) fall into the **higher** band (e.g. 10% = Moderate, not Low).

Source: `metrics_definitions.md §Portfolio Heat Display Thresholds` v1.6.0

---

## 4. Test Data Definitions

The following datasets are referenced by scenario IDs. All monetary values are GBP. Portfolio value = £10,000 in all datasets unless stated.

---

### TD-01 — Zero heat (no open positions)

| Field | Value |
|-------|-------|
| portfolio_heat_percent | 0.0 |
| positions | [] |
| current_drawdown_percent | 0.0 |
| peak_portfolio_value | 10000.00 |

---

### TD-02 — Heat 9.9% (just below 10% boundary)

One open UK position:

| Field | Value | Derivation |
|-------|-------|------------|
| ticker | ALPHA |  |
| market | UK |  |
| entry_price | 9900 (pence) = £99.00 |  |
| current_stop | 8910 (pence) = £89.10 |  |
| shares | 100 |  |
| fx_rate | 1.0 | UK position |
| **Position_Risk_GBP** | **£990.00** | (99.00 − 89.10) × 100 |
| **portfolio_heat_percent** | **9.9** | 990 / 10000 × 100 |
| grace_period | false | |
| status | LOSING | |
| display_status | LOSING | |
| holding_days | 15 | |

---

### TD-03 — Heat exactly 10.0% (boundary)

One open UK position:

| Field | Value | Derivation |
|-------|-------|------------|
| ticker | BRAVO |  |
| market | UK |  |
| entry_price | 10000 pence = £100.00 |  |
| current_stop | 9000 pence = £90.00 |  |
| shares | 100 |  |
| **Position_Risk_GBP** | **£1,000.00** | (100.00 − 90.00) × 100 |
| **portfolio_heat_percent** | **10.0** | 1000 / 10000 × 100 |

---

### TD-04 — Heat exactly 20.0% (boundary)

One open UK position:

| Field | Value | Derivation |
|-------|-------|------------|
| ticker | CHARLIE |  |
| market | UK |  |
| entry_price | 10000 pence = £100.00 |  |
| current_stop | 8000 pence = £80.00 |  |
| shares | 100 |  |
| **Position_Risk_GBP** | **£2,000.00** | (100.00 − 80.00) × 100 |
| **portfolio_heat_percent** | **20.0** | 2000 / 10000 × 100 |

---

### TD-05 — Heat exactly 30.0% (boundary)

One open UK position:

| Field | Value | Derivation |
|-------|-------|------------|
| ticker | DELTA |  |
| market | UK |  |
| entry_price | 10000 pence = £100.00 |  |
| current_stop | 7000 pence = £70.00 |  |
| shares | 100 |  |
| **Position_Risk_GBP** | **£3,000.00** | (100.00 − 70.00) × 100 |
| **portfolio_heat_percent** | **30.0** | 3000 / 10000 × 100 |

---

### TD-06 — Heat 35.0% (above 30% — deep extreme)

One open UK position:

| Field | Value | Derivation |
|-------|-------|------------|
| ticker | ECHO |  |
| market | UK |  |
| entry_price | 10000 pence = £100.00 |  |
| current_stop | 6500 pence = £65.00 |  |
| shares | 100 |  |
| **Position_Risk_GBP** | **£3,500.00** | (100.00 − 65.00) × 100 |
| **portfolio_heat_percent** | **35.0** | 3500 / 10000 × 100 |

---

### TD-07 — Grace period colour coding (multiple positions)

Three positions in grace period, one not:

| Ticker | grace_period | grace_days_remaining | Expected badge colour | Expected sort position |
|--------|-------------|---------------------|----------------------|------------------------|
| FOXT | true | 1 | Red (≤ 1 day) | 1st (most urgent) |
| GOLF | true | 4 | Amber (2–4 days) | 2nd |
| HOTL | true | 5 | Green (≥ 5 days) | 3rd |
| INDI | false | n/a | Not shown | Not shown |

Source: `risk_dashboard.md §5.3` and `§5.4`

---

### TD-08 — Grace period at day 10 (within grace) and day 11 (expired)

| Ticker | grace_period | grace_days_remaining | holding_days | Expected |
|--------|-------------|---------------------|--------------|----------|
| JULIET | true | 10 | 1 | Green — appears in panel |
| KILO | false | 0 | 12 | Grace expired — NOT in panel |

Note: KILO has `grace_period = false` with `holding_days = 12` indicating grace period has ended. It must not appear in the Grace Period Panel.

---

### TD-09 — All three position states simultaneously

| Ticker | display_status | grace_period | current_price (£) | current_stop (£) | Stop distance % | Sort rank in group |
|--------|---------------|-------------|-------------------|-----------------|----------------|-------------------|
| LIMA | GRACE | true | 5.00 | 4.80 | 4.0% | GRACE group — by stop dist |
| MIKE | LOSING | false | 8.00 | 7.50 | 6.25% | LOSING group — position 1 |
| NOVEM | LOSING | false | 8.00 | 7.00 | 12.5% | LOSING group — position 2 |
| OSCAR | PROFITABLE | false | 15.00 | 12.00 | 20.0% | PROFITABLE group |

Stop distance formula (display-only derivation, spec §6.2):
`stop_distance_pct = (current_price − current_stop) / current_price × 100`
- LIMA: (5.00 − 4.80) / 5.00 × 100 = 4.0%
- MIKE: (8.00 − 7.50) / 8.00 × 100 = 6.25%
- NOVEM: (8.00 − 7.00) / 8.00 × 100 = 12.5%
- OSCAR: (15.00 − 12.00) / 15.00 × 100 = 20.0%

---

### TD-10 — Prospective heat crossing 20% threshold

Current state: portfolio_heat_percent = 15.0% (£1,500 existing risk, portfolio £10,000)

Prospective position to add:
| Field | Value | Derivation |
|-------|-------|------------|
| ticker | PAPA |  |
| shares | 100 |  |
| entry_price | £10.00 |  |
| stop_price | £9.50 |  |
| Position_Risk_GBP | £50.00 | (10.00 − 9.50) × 100 |
| Projected total risk | £1,550.00 | £1,500 + £50 |
| **Projected heat** | **15.5%** | 1550 / 10000 × 100 |

For a scenario that pushes heat **above** 20%:
| Field | Value | Derivation |
|-------|-------|------------|
| shares | 100 |  |
| entry_price | £20.00 |  |
| stop_price | £14.00 |  |
| Position_Risk_GBP | £600.00 | (20.00 − 14.00) × 100 |
| Projected total risk | £2,100.00 | £1,500 + £600 |
| **Projected heat** | **21.0%** | 2100 / 10000 × 100 |
| **Threshold crossed** | Moderate → High (20% boundary) | |

---

## 5. Test Infrastructure Preconditions

Before attempting to execute scenarios, QA Lead must confirm the following conditions.

---

### 5.1 Environment Requirements

**For automated Playwright execution (recommended — CI):**
- `npm start` dev server running on `http://localhost:3000` (launched automatically by Playwright `webServer` config).
- No live backend required — all API calls are intercepted via `page.route()`.
- Run: `npx playwright test tests/e2e/risk-dashboard.spec.js`

**For manual browser execution:**
- Backend API must be reachable at the configured API base URL (same origin or via `api.*` client).
- Browser developer tools (Network tab, Console tab) must be available for Groups E and G.
- Entity store (`base44.entities`) state must be known and controllable for Group E error-state scenarios.

---

### 5.2 Test Data Injection Approach (v1.1 — Playwright Mock Layer)

**Decision record:** 2026-03-09 — agreed by Facilitator, Head of Engineering, QA & Testing Owner, Infrastructure & Operations Owner, Director of Quality. RISK-07 resolved. See `claude/cycles/2026-03-06__release-v1.9/execution_state.json` for session record.

**Approach:** Playwright `page.route()` network interception. Tests intercept `GET http://localhost:8000/portfolio` and `GET http://localhost:8000/portfolio/prospective-heat` before the React app receives them, returning scenario-controlled mock responses matching the test data definitions in §4.

| Scenario Group | Required infrastructure | Status (v1.1) |
|----------------|------------------------|---------------|
| Group A — Heat Gauge Thresholds (SC-RD-01–SC-RD-06) | `portfolio_heat_percent` values matching TD-01 through TD-06 | **Available** — Playwright mock handler in `tests/e2e/mocks/portfolio-mock-data.js` |
| Group B — Grace Period Panel (SC-RD-07–SC-RD-13) | Positions with specific `grace_period`, `grace_days_remaining` values matching TD-07, TD-08 | **Available** — Playwright mock handler in `tests/e2e/mocks/portfolio-mock-data.js` |
| Group C — Position Risk Table (SC-RD-14–SC-RD-15) | Positions with specific `display_status`, `current_price`, `current_stop` values matching TD-09 | **Available** — mock data defined; SC-RD-14 test pending (canonical sort requires EPIC-04 merged); SC-RD-15 automated |
| Group D — Prospective Heat (SC-RD-16–SC-RD-19) | `/api/portfolio/prospective-heat` mock response + controlled current heat | **Available** — Playwright mock handler covers SC-RD-16–18; SC-RD-19 (collapse state) executable against live |
| Group E — API Error States (SC-RD-20–SC-RD-24) | Portfolio endpoint 500; entity fallback suppressed | **Available** — SC-RD-24 automated; SC-RD-20–23 require entity store suppression (manual or extended Playwright mock) |
| Group F — Empty State (SC-RD-25) | No open positions | **Available** — TD-01 mock delivers zero positions |

---

### 5.3 Automated Coverage Summary (v1.1)

The following 17 scenarios are now automated in `tests/e2e/risk-dashboard.spec.js`:

| Scenario | Group | Automated | Mock Dataset |
|----------|-------|-----------|-------------|
| SC-RD-02 | A | ✓ | TD-02 |
| SC-RD-03 | A | ✓ | TD-03 |
| SC-RD-04 | A | ✓ | TD-04 |
| SC-RD-05 | A | ✓ | TD-05 |
| SC-RD-06 | A | ✓ | TD-06 |
| SC-RD-07 | B | ✓ | TD-07 |
| SC-RD-08 | B | ✓ | TD-07 (FOXT row) |
| SC-RD-09 | B | ✓ | TD-07 variant |
| SC-RD-10 | B | ✓ | TD-07 (GOLF row) |
| SC-RD-11 | B | ✓ | TD-07 (HOTL row) |
| SC-RD-12 | B | ✓ | TD-08 |
| SC-RD-15 | C | ✓ | TD-01 |
| SC-RD-16 | D | ✓ | TD-10 + prospective mock |
| SC-RD-17 | D | ✓ | TD-10 (client validation) |
| SC-RD-18 | D | ✓ | TD-02 variant + prospective mock |
| SC-RD-24 | E | ✓ | TD-10 + error mock |
| SC-RD-25 | F | ✓ | TD-01 |

CI gate: `.github/workflows/playwright.yml` — triggers on changes to `src/components/risk/`, `src/pages/RiskDashboard.js`, and `tests/e2e/`.

Non-automated scenarios remaining (manual execution or future automation):
- SC-RD-13 (grace empty state — overlaps SC-RD-25), SC-RD-14 (sort order — pending EPIC-04 merge), SC-RD-19 (collapse state — UI interaction, no mock needed), SC-RD-20–23 (portfolio error states — require entity fallback suppression), SC-RD-26–27 (non-functional — console/network inspection).

---

### 5.4 Backend API Coverage Gap

The mock layer tests frontend rendering behavior. Backend-to-API coverage (does the portfolio router return correctly-shaped responses for real database rows?) is a separate concern tracked at:

**BLG-API-01** — `TestClient` integration tests on `GET /portfolio` and `GET /portfolio/prospective-heat` using FastAPI's `TestClient` with injected fixture data. See `claude/backlog/backlog.md §12`.

---

### 5.5 Backlog Reference

TEST-GAP-EPIC-01 resolved in v1.9 (ST-11). Mock layer infrastructure delivered; all 17 blocked scenarios automated. See `claude/backlog/backlog.md §10`.

---

## 6. Scenarios

---

### Group A — Portfolio Heat Gauge: Threshold Boundaries

---

#### SC-RD-01 — Heat gauge at 0% (no positions)

**Spec ref:** `risk_dashboard.md §3.3`, `risk_dashboard.md §3.4 (Zero positions state)`, `metrics_definitions.md §Portfolio Heat Display Thresholds`
**Dataset:** TD-01

**Preconditions:** Backend returns `portfolio_heat_percent = 0.0` and `positions = []`.

**Steps:**
1. Navigate to `/risk`.
2. Wait for page load to complete.
3. Observe the Portfolio Heat Gauge.

**Expected results:**
- Gauge displays value: `0.0%`
- Gauge fill colour: `#22c55e` (green)
- Threshold label: "Low"
- Sub-text: "No open positions" (per `risk_dashboard.md §3.4`)
- No error card displayed

---

#### SC-RD-02 — Heat gauge at 9.9% (just below 10% boundary)

**Spec ref:** `risk_dashboard.md §3.3`, `metrics_definitions.md §Portfolio Heat Display Thresholds`
**Dataset:** TD-02

**Preconditions:** Backend returns `portfolio_heat_percent = 9.9`.

**Steps:**
1. Navigate to `/risk`.
2. Observe the Portfolio Heat Gauge.

**Expected results:**
- Gauge displays: `9.9%`
- Gauge fill colour: `#22c55e` (green — Low band, < 10%)
- Threshold label: "Low"

---

#### SC-RD-03 — Heat gauge at exactly 10.0% (Moderate boundary)

**Spec ref:** `risk_dashboard.md §3.3`, `metrics_definitions.md §Portfolio Heat Display Thresholds`
**Dataset:** TD-03
**Critical boundary:** 10.0% must display Amber (Moderate), NOT green (Low).

**Derivation check:**
- Position_Risk_GBP = (£100.00 − £90.00) × 100 = £1,000.00
- Portfolio_Heat_Percent = £1,000 / £10,000 × 100 = **10.0%**
- Band: 10% ≤ heat < 20% → Moderate → Amber

**Steps:**
1. Navigate to `/risk` with TD-03 data.
2. Observe Portfolio Heat Gauge.

**Expected results:**
- Gauge displays: `10.0%`
- Gauge fill colour: `#f59e0b` (amber — Moderate)
- Threshold label: "Moderate"
- Colour is **NOT** `#22c55e` (green must not appear at exactly 10%)

---

#### SC-RD-04 — Heat gauge at exactly 20.0% (High boundary)

**Spec ref:** `risk_dashboard.md §3.3`, `metrics_definitions.md §Portfolio Heat Display Thresholds`
**Dataset:** TD-04
**Critical boundary:** 20.0% must display Orange (High), NOT amber (Moderate).

**Derivation check:**
- Position_Risk_GBP = (£100.00 − £80.00) × 100 = £2,000.00
- Portfolio_Heat_Percent = £2,000 / £10,000 × 100 = **20.0%**
- Band: 20% ≤ heat < 30% → High → Orange

**Steps:**
1. Navigate to `/risk` with TD-04 data.
2. Observe Portfolio Heat Gauge.

**Expected results:**
- Gauge displays: `20.0%`
- Gauge fill colour: `#f97316` (orange — High)
- Threshold label: "High"
- Colour is **NOT** `#f59e0b` (amber must not appear at exactly 20%)

---

#### SC-RD-05 — Heat gauge at exactly 30.0% (Extreme boundary)

**Spec ref:** `risk_dashboard.md §3.3`, `metrics_definitions.md §Portfolio Heat Display Thresholds`
**Dataset:** TD-05
**Critical boundary:** 30.0% must display Red (Extreme), NOT orange (High).

**Derivation check:**
- Position_Risk_GBP = (£100.00 − £70.00) × 100 = £3,000.00
- Portfolio_Heat_Percent = £3,000 / £10,000 × 100 = **30.0%**
- Band: heat ≥ 30% → Extreme → Red

**Steps:**
1. Navigate to `/risk` with TD-05 data.
2. Observe Portfolio Heat Gauge.

**Expected results:**
- Gauge displays: `30.0%`
- Gauge fill colour: `#ef4444` (red — Extreme)
- Threshold label: "Extreme"
- Colour is **NOT** `#f97316` (orange must not appear at exactly 30%)

---

#### SC-RD-06 — Heat gauge at 35.0% (above 30%, deep extreme)

**Spec ref:** `metrics_definitions.md §Portfolio Heat Display Thresholds`
**Dataset:** TD-06

**Steps:**
1. Navigate to `/risk` with TD-06 data.
2. Observe Portfolio Heat Gauge.

**Expected results:**
- Gauge displays: `35.0%`
- Gauge fill colour: `#ef4444` (red — Extreme)
- Threshold label: "Extreme"

---

### Group B — Grace Period Panel

---

#### SC-RD-07 — Grace period colour coding and sort order

**Spec ref:** `risk_dashboard.md §5.3`, `risk_dashboard.md §5.4`
**Dataset:** TD-07

**Steps:**
1. Navigate to `/risk` with TD-07 data (FOXT: 1 day, GOLF: 4 days, HOTL: 5 days, INDI: not in grace).
2. Observe the Grace Period Panel.

**Expected results:**
- Panel shows **3 rows** (INDI excluded — `grace_period = false`)
- Row 1 (most urgent): FOXT — `1d remaining` — **Red** badge (≤ 1 day)
- Row 2: GOLF — `4d remaining` — **Amber** badge (2–4 days)
- Row 3: HOTL — `5d remaining` — **Green** badge (≥ 5 days)
- Sort is ascending by `grace_days_remaining` (1 before 4 before 5)
- Count badge: "3 positions"

---

#### SC-RD-08 — Grace period at day 1 (red boundary)

**Spec ref:** `risk_dashboard.md §5.3`

**Preconditions:** One position with `grace_days_remaining = 1`.

**Expected results:**
- Row badge: Red (≤ 1 day threshold)
- Text: "1d remaining"

---

#### SC-RD-09 — Grace period at day 2 (amber lower boundary)

**Spec ref:** `risk_dashboard.md §5.3`

**Preconditions:** One position with `grace_days_remaining = 2`.

**Expected results:**
- Row badge: Amber (2–4 day threshold)
- Text: "2d remaining"

---

#### SC-RD-10 — Grace period at day 4 (amber upper boundary)

**Spec ref:** `risk_dashboard.md §5.3`

**Preconditions:** One position with `grace_days_remaining = 4`.

**Expected results:**
- Row badge: Amber (2–4 day threshold, not green)
- Text: "4d remaining"

---

#### SC-RD-11 — Grace period at day 5 (green boundary)

**Spec ref:** `risk_dashboard.md §5.3`

**Preconditions:** One position with `grace_days_remaining = 5`.

**Expected results:**
- Row badge: Green (≥ 5 days threshold)
- Text: "5d remaining"

---

#### SC-RD-12 — Grace period at day 10 (within grace) and expired position excluded

**Spec ref:** `risk_dashboard.md §5.1`, `risk_dashboard.md §5.5`
**Dataset:** TD-08

**Steps:**
1. Navigate to `/risk` with TD-08 data (JULIET: in grace day 10, KILO: grace_period = false, holding_days = 12).
2. Observe Grace Period Panel.

**Expected results:**
- Panel shows **1 row** (JULIET only)
- JULIET: `grace_period = true`, `grace_days_remaining = 10` → Green badge → "10d remaining"
- KILO does **not** appear (grace_period = false)
- Count badge: "1 position"

---

#### SC-RD-13 — Grace period empty state

**Spec ref:** `risk_dashboard.md §5.5`
**Dataset:** TD-01 (no positions)

**Steps:**
1. Navigate to `/risk` with no open positions.
2. Observe Grace Period Panel.

**Expected results:**
- Panel displays: "No positions in grace period" (muted text)
- No table rows rendered
- No count badge

---

### Group C — Position Risk Table

---

#### SC-RD-14 — All three position states simultaneously with correct sort

**Spec ref:** `risk_dashboard.md §6.2`, `risk_dashboard.md §6.3`, `risk_dashboard.md §6.4`
**Dataset:** TD-09

**Canonical sort order (spec §6.4):**
- Primary: GRACE → LOSING → PROFITABLE
- Secondary within group: ascending by stop distance % (tightest / smallest first = most at risk)

**[DEV-ST03-03]** v1.8 implementation sorts **descending** within group (largest stop distance first). The v1.8 expected sort result below reflects the known deviation. The canonical expected result is noted separately.

**Steps:**
1. Navigate to `/risk` with TD-09 data.
2. Observe Position Risk Table.

**Expected results — canonical (spec):**
| Row | Ticker | Status | Stop Distance % |
|-----|--------|--------|----------------|
| 1 | LIMA | GRACE | 4.0% |
| 2 | MIKE | LOSING | 6.25% (tightest — most at risk) |
| 3 | NOVEM | LOSING | 12.5% |
| 4 | OSCAR | PROFITABLE | 20.0% |

**Expected results — v1.8 actual (DEV-ST03-03 known deviation):**
| Row | Ticker | Status | Stop Distance % |
|-----|--------|--------|----------------|
| 1 | LIMA | GRACE | 4.0% |
| 2 | NOVEM | LOSING | 12.5% (largest — appears first in v1.8) |
| 3 | MIKE | LOSING | 6.25% |
| 4 | OSCAR | PROFITABLE | 20.0% |

**Status badge colours [DEV-ST03-05 note]:**
- GRACE: Amber in v1.8 (spec requires Blue)
- LOSING: Red
- PROFITABLE: Green

**Missing column [DEV-ST03-04 note]:**
- Stop Price column is absent in v1.8. Columns present: Ticker, Status, Entry Price, Current (GBP), Stop Dist %, Held.

**Stop distance % values to verify:**
- LIMA: (5.00 − 4.80) / 5.00 × 100 = **4.0%** ✓
- MIKE: (8.00 − 7.50) / 8.00 × 100 = **6.25%** ✓
- NOVEM: (8.00 − 7.00) / 8.00 × 100 = **12.5%** ✓
- OSCAR: (15.00 − 12.00) / 15.00 × 100 = **20.0%** ✓

---

#### SC-RD-15 — Position Risk Table empty state

**Spec ref:** `risk_dashboard.md §6.5`
**Dataset:** TD-01 (no open positions)

**Steps:**
1. Navigate to `/risk` with no open positions.
2. Observe Position Risk Table.

**Expected results:**
- Message: "No open positions to display" (or equivalent per spec §6.5)
- No table rows

---

### Group D — Prospective Heat Indicator

---

#### SC-RD-16 — Prospective heat crossing 20% threshold

**Spec ref:** `risk_dashboard.md §7.4`, `risk_dashboard.md §7.5`
**Dataset:** TD-10 (current heat 15.0%; prospective position PAPA with entry £20.00, stop £14.00, 100 shares)

**Derivation:**
- Added risk = (£20.00 − £14.00) × 100 = £600
- Projected total risk = £1,500 + £600 = £2,100
- Projected heat = £2,100 / £10,000 × 100 = **21.0%**
- Delta = 21.0% − 15.0% = **+6.0%**
- Threshold crossed: Moderate (15%) → High (21%) — boundary at 20%

**Preconditions:**
- Current `portfolio_heat_percent = 15.0`
- Prospective heat endpoint available at `/api/portfolio/prospective-heat`
- Panel expanded

**Steps:**
1. Navigate to `/risk`.
2. Click "Prospective Heat Calculator" to expand the panel.
3. Enter: Ticker = "PAPA", Shares = 100, Entry Price = 20.00, Stop Price = 14.00.
4. Click "Calculate".

**Expected results:**
- API call made to `/api/portfolio/prospective-heat?ticker=PAPA&shares=100&entry_price=20.00&stop_price=14.00`
- "Projected Heat" displayed: **21.0%**
- "Delta" displayed: **+6.0%** (in red — positive delta)
- Threshold label for 21.0%: "High" / orange (20% ≤ heat < 30%)

---

#### SC-RD-17 — Prospective heat: stop price ≥ entry price rejected client-side

**Spec ref:** `risk_dashboard.md §7.6 (Stop ≥ entry price state)`

**Steps:**
1. Expand Prospective Heat panel.
2. Enter: Shares = 100, Entry Price = 10.00, Stop Price = 10.00 (equal to entry).
3. Attempt to click Calculate.

**Expected results:**
- Inline validation error displayed on Stop Price field
- Calculate button does not submit the form / is disabled
- No API call made

**Repeat with Stop Price = 10.01 (above entry price):**
- Same outcome: inline validation error; no API call

---

#### SC-RD-18 — Prospective heat: valid inputs, result shows projected % and delta

**Spec ref:** `risk_dashboard.md §7.5`

**Preconditions:** Current `portfolio_heat_percent = 9.0` (within Low band).

**Steps:**
1. Expand Prospective Heat panel.
2. Enter valid inputs (all fields positive, stop < entry).
3. Click Calculate.

**Expected results:**
- `projected_heat_percent` displayed to 1 decimal place
- Delta shown as `+X.X%` if projected > current, `-X.X%` if projected < current

---

#### SC-RD-19 — Prospective heat: panel collapsed by default

**Spec ref:** `risk_dashboard.md §7.2`

**Steps:**
1. Navigate to `/risk`.
2. Observe Prospective Heat panel on initial load.

**Expected results:**
- Panel is collapsed (input form not visible)
- Heading and expand chevron visible
- Click chevron → panel expands and form is visible

---

### Group E — API Error States

**Important precondition for all SC-RD-20 through SC-RD-24:** To force the error states in the v1.8 implementation, the entity store must not contain matching data, OR testing must occur in an environment where entity store data is unavailable. **[DEV-ST03-01]** — If entity data is present, the fallback activates and error states may not display.

---

#### SC-RD-20 — GET /portfolio fails: Heat Gauge error state

**Spec ref:** `risk_dashboard.md §3.4 (Error state)`, `risk_dashboard.md §8`

**Preconditions:** Backend `/api/portfolio` returns HTTP 5xx (simulated). No entity store data available.

**Steps:**
1. Navigate to `/risk` with portfolio endpoint returning an error.
2. Wait for page load.
3. Observe Heat Gauge section.

**Expected results:**
- Heat Gauge renders an error card: "Could not load portfolio heat. Check API connection." (or equivalent per spec §3.4)
- Heat gauge itself does NOT render
- Other components (Drawdown, Grace Period, Position Risk Table) render their own independent error or empty states
- Page is NOT entirely blank

---

#### SC-RD-21 — GET /portfolio fails: Drawdown Summary error state

**Spec ref:** `risk_dashboard.md §4.3 (Error state)`, `risk_dashboard.md §8`

**Preconditions:** Same as SC-RD-20.

**Expected results:**
- Drawdown Summary renders error: "Could not load drawdown data. Check API connection." (or equivalent per spec §4.3)
- Does NOT render drawdown values

---

#### SC-RD-22 — GET /portfolio fails: Grace Period Panel error state

**Spec ref:** `risk_dashboard.md §5.5 (Error state)`, `risk_dashboard.md §8`
**[DEV-ST03-02]** In v1.8, `GET /portfolio` failure causes `positions` to be `[]`, and GracePeriodPanel displays "No positions in grace period" — identical to valid empty state. To distinguish: check network tab confirms portfolio request returned an error.

**Preconditions:** Same as SC-RD-20.

**Expected results (canonical — spec §5.5):**
- Grace Period Panel renders: "Unable to load position data" error state

**Expected results (v1.8 actual — DEV-ST03-02):**
- Grace Period Panel renders: "No positions in grace period" — **indistinguishable from empty state**
- Confirm this is the error path via browser dev tools (network tab shows failed portfolio request)

---

#### SC-RD-23 — GET /portfolio fails: Position Risk Table error state

**Spec ref:** `risk_dashboard.md §6.5 (Error state)`, `risk_dashboard.md §8`
**[DEV-ST03-02]** Same concern as SC-RD-22 — empty state renders instead of explicit error state in v1.8.

**Preconditions:** Same as SC-RD-20.

**Expected results (canonical — spec §6.5):**
- Position Risk Table renders: "Unable to load position data" error state

**Expected results (v1.8 actual):**
- Position Risk Table renders: "No open positions to display" — confirms via network tab

---

#### SC-RD-24 — Prospective Heat endpoint fails: inline error

**Spec ref:** `risk_dashboard.md §7.6 (Calculation error state)`

**Preconditions:** Prospective heat endpoint `/api/portfolio/prospective-heat` returns HTTP 5xx.

**Steps:**
1. Navigate to `/risk`.
2. Expand Prospective Heat panel.
3. Enter valid inputs.
4. Click Calculate.

**Expected results:**
- Inline error displayed: "Unable to calculate — please try again" (or equivalent per spec §7.6)
- No projected heat value rendered
- Input fields remain accessible (user can try again)
- No full-page error or crash

---

### Group F — Empty State (No Open Positions)

---

#### SC-RD-25 — Full empty state: no open positions

**Spec ref:** `risk_dashboard.md §3.4`, `§5.5`, `§6.5`
**Dataset:** TD-01

**Steps:**
1. Navigate to `/risk` with no open positions and `portfolio_heat_percent = 0.0`.

**Expected results:**
- Heat Gauge: 0.0%, Green (#22c55e), sub-text "No open positions"
- Drawdown Summary: renders (may show N/A for days underwater if no history)
- Grace Period Panel: "No positions in grace period"
- Position Risk Table: "No open positions to display"
- Prospective Heat: still interactive (allows prospective calculation even with zero existing positions)
- No console errors

---

### Group G — Non-Functional

---

#### SC-RD-26 — No console errors on clean load

**Spec ref:** `risk_dashboard.md §10` (implicit — no error conditions on clean load)

**Preconditions:** Valid `GET /portfolio` response; at least one open position.

**Steps:**
1. Open browser developer tools → Console tab.
2. Navigate to `/risk`.
3. Wait for all components to render.
4. Inspect console.

**Expected results:**
- Zero console errors
- Zero unhandled promise rejections
- Warnings reviewed: any unexpected warnings noted to Director of Quality

---

#### SC-RD-27 — All metric values sourced from backend (no client-side recalculation)

**Spec ref:** `risk_dashboard.md §10`

**Steps:**
1. Navigate to `/risk`.
2. Open browser developer tools → Network tab.
3. Inspect the `GET /portfolio` response payload.
4. Compare `portfolio_heat_percent` from the API response to the value displayed in the gauge.
5. Compare `current_drawdown_percent` from API response to the Drawdown Summary display.

**Expected results:**
- `portfolio_heat_percent` displayed = `portfolio_heat_percent` in API response (no recalculation)
- `current_drawdown_percent` displayed = value in API response
- Stop Distance % in Position Risk Table is the only client-side derived value (display arithmetic from `current_price` and `current_stop` — acceptable per spec §6.2)
- No other values are computed client-side from raw fields

---

## 7. Sign-Off Checklist (Director of Quality)

The following must be confirmed before marking ST-04 done and opening EPIC-01 merge gate:

- [ ] All SC-RD-01 through SC-RD-07 (heat gauge thresholds) executed and passed
- [ ] All boundary values (10%, 20%, 30%) verified with exact hex colour match
- [ ] SC-RD-07 through SC-RD-13 (grace period) executed and passed
- [ ] SC-RD-14 through SC-RD-15 (position risk table) executed — v1.8 deviations noted
- [ ] SC-RD-16 through SC-RD-19 (prospective heat) executed and passed
- [ ] SC-RD-20 through SC-RD-24 (error states) executed with DEV-ST03-01 precondition met
- [ ] SC-RD-25 (empty state) executed and passed
- [ ] SC-RD-26 (no console errors) executed and passed
- [ ] SC-RD-27 (no client-side recalculation) verified
- [ ] All known deviations (DEV-ST03-01 through DEV-ST03-05) observed and matches recorded here
- [ ] No new deviations from canonical spec observed beyond those listed in §2
- Signed off by: Director of Quality
- Date:
- Notes:

---

## 8. Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-03-09 | ST-11 delivery: §5 Test Infrastructure Preconditions updated to reflect Playwright mock layer approach (RISK-07 resolved). §5.1 updated for automated + manual execution paths. §5.2 table updated: all 17 previously-blocked scenario groups now "Available". §5.3 Automated Coverage Summary table added (17 scenarios). §5.4 Backend API gap noted (BLG-API-01 raised). §5.5 replaces prior §5.4 backlog reference. TEST-GAP-EPIC-01 resolved. |
| 1.0.1 | 2026-03-06 | Added §5 Test Infrastructure Preconditions: documents which scenario groups require test data injection (Groups A–C and most of F — 17/27 scenarios), which are executable without injection (Groups D, E, G — 10/27 scenarios), environment requirements, and backlog reference TEST-GAP-EPIC-01. Renumbered prior §5–§7 to §6–§8. Applied from EX-LL Friction Item 3 deferred patch. |
| 1.0.0 | 2026-03-05 | Initial version. 27 scenarios covering heat thresholds, grace period, position risk table, prospective heat, API error states, empty states, and non-functional requirements. Derived from risk_dashboard.md v0.1.1 and metrics_definitions.md v1.6.0. Known deviations DEV-ST03-01 through DEV-ST03-05 documented in §2. |
