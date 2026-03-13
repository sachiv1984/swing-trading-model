**Owner:** QA & Testing Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.3
**Last Updated:** 2026-03-13
**Derived from:** `docs/specs/frontend/pages/risk_dashboard.md` v0.1.1; `docs/specs/metrics_definitions.md` v1.6.0; `docs/specs/frontend/pages/analytics.md` v1.4; `docs/specs/frontend/pages/trade_reflection.md` v0.1; `docs/specs/frontend/pages/dashboard.md` v2.0
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

### 5.5 Playwright Test Maintenance Protocol

**Cross-EPIC microcopy change obligation (Friction 2 — 2026-03-06__release-v1.9 Sprint 1):**

When any frontend delivery (in any EPIC branch) changes a component's UI microcopy — including empty state messages, error text, placeholder text, or any string asserted in a Playwright test — the following obligation applies:

1. **Identify:** The delivering engineer (or governance engine acting as frontend agent) must audit all `SC-RD-*` Playwright tests in `tests/e2e/risk-dashboard.spec.js` for string assertions (`toContainText`, `toHaveText`, `locator('text=...')`) that reference that component's microcopy.
2. **Update:** Any affected locator must be updated to match the new string **in the same PR** as the microcopy change, or in a follow-on commit that is merged before the EPIC branch closes its PR.
3. **Verify:** CI must pass (Playwright suite green) before the EPIC branch merge gate is opened.

**Why this matters:** UI microcopy changes that are not co-ordinated with Playwright test updates silently break adjacent EPIC branches when they rebase against main. The resulting CI failure is easy to fix but requires an unplanned commit and additional CI run, adding session overhead.

**Routing:** If the delivering engineer is not the test author, the obligation must be flagged explicitly in the EPIC's sprint backlog acceptance criteria or delegation record.

*Trigger: Friction Item 2, lessons_learnt_execution.md — cycle 2026-03-06__release-v1.9 Sprint 1. Implemented 2026-03-10.*

---

### 5.6 Backlog Reference

TEST-GAP-EPIC-01 resolved in v1.9 (ST-11). Mock layer infrastructure delivered; all 17 blocked scenarios automated. See `claude/backlog/backlog.md §10`.

---

---

## 6. v1.9 Feature Scenarios (ST-12 Phase 2)

**Added:** 2026-03-13 | **Sprint:** 2026-03-06__release-v1.9 Sprint 2 | **ST:** ST-12

These scenarios cover the v1.9 Sprint 2 feature delivery: EPIC-01 (compliance metrics, trade reflection), EPIC-02 (cohort analysis, R-multiple distribution), and EPIC-03 (dashboard homepage). All scenarios are manual acceptance unless marked `[AUTO]`.

**Known deviations affecting v1.9 test execution:**

| Ref | Priority | Affect on test execution |
|-----|----------|--------------------------|
| DEV-EPIC02-ST03-01 | P2 | CohortAnalysis.js computes cohort values client-side from trade data, not from GET /analytics/cohort. The displayed cohort table values are correct but sourced from client-side aggregation. QA Lead should verify displayed values match expected cohort calculation but cannot verify they came from the backend endpoint via frontend code inspection alone — use network tab to confirm no GET /analytics/cohort call is made (this is the documented deviation). |
| DEV-EPIC03-ST05-01 | P3 | When all 5 dashboard endpoints fail, the page shows 5 individual card errors rather than a full-page overlay with Retry. Scenarios SC-DH-10 reflects this accepted behaviour. |

---

### 6.1 Compliance Metrics Scenarios (ST-01 — analytics.md §17)

**Source spec:** `docs/specs/frontend/pages/analytics.md §17`
**Endpoint:** `GET /analytics/compliance-metrics`
**Component:** `src/components/analytics/DisciplineComplianceSection.js`

---

#### SC-CM-01 — Compliance metrics panel renders on Performance Analytics page

**Precondition:** Backend returns valid compliance metrics response
**Steps:**
1. Navigate to the Performance Analytics page (`/PerformanceAnalytics`)
2. Scroll to the Discipline & Compliance section

**Expected result:** Panel renders with three metric cards:
- "Journal Completion Rate" (percentage, 1 decimal place)
- "Stop-Based Exit Rate" (percentage, 1 decimal place)
- "Average Position Size" (percentage, 2 decimal places)
- Each card shows a sub-label "last N trades" where N = trade_count from API response

**Pass criteria:** All three cards visible; values match API response; sub-labels reflect trade_count.

---

#### SC-CM-02 — Compliance metric values match canonical formulas

**Precondition:** Known trade dataset with pre-calculated expected values
**Steps:**
1. Inject or confirm trade data where:
   - 8 of 10 trades have journal notes → journal_completion_rate = 80.0%
   - 6 of 10 trades exited via stop → stop_exit_rate = 60.0%
   - Average total_cost / portfolio_value = 5.25% → avg_position_size_pct = 5.25%
2. Navigate to Performance Analytics, locate Discipline & Compliance section

**Expected result:**
- Journal Completion Rate: 80.0%
- Stop-Based Exit Rate: 60.0%
- Average Position Size: 5.25%

**Pass criteria:** Values exactly match canonical formula output per `metrics_definitions.md §Discipline & Compliance Metrics`.

---

#### SC-CM-03 — Zero trades: all cards show "—"

**Precondition:** Backend returns `{ "trade_count": 0, "journal_completion_rate": 0.0, "stop_exit_rate": 0.0, "avg_position_size_pct": 0.0 }`
**Steps:** Navigate to Performance Analytics, locate Discipline & Compliance section

**Expected result:** All three cards show "—" (em-dash). No sub-label shown (trade_count = 0).

**Pass criteria:** No numeric values displayed when denominator is zero.

---

#### SC-CM-04 — API error: cards show error state

**Precondition:** `GET /analytics/compliance-metrics` returns 500
**Steps:**
1. Mock or block the endpoint to return an error
2. Navigate to Performance Analytics, scroll to Discipline & Compliance

**Expected result:** Each card shows an error icon (AlertCircle) and "Unable to load" message. No numeric values shown. Other analytics sections unaffected.

**Pass criteria:** Error is contained to the compliance section; page does not crash.

---

### 6.2 Trade Reflection Scenarios (ST-02 — trade_reflection.md v0.1)

**Source spec:** `docs/specs/frontend/pages/trade_reflection.md`
**Endpoints:** `GET /trades/{trade_id}/reflection`, `POST /trades/{trade_id}/reflection`
**Component:** `src/components/trades/TradeReflectionModal.js`

---

#### SC-TR-01 — Reflection modal opens on trade exit

**Precondition:** At least one open position visible on Positions page
**Steps:**
1. Navigate to Positions page (`/Positions`)
2. Exit a position (trigger trade close)

**Expected result:** TradeReflectionModal opens automatically after the exit mutation completes. Modal title shows "Trade Reflection — {TICKER}". Trade summary block visible (ticker, entry price, exit price, hold time, exit reason, exit date).

**Pass criteria:** Modal opens post-exit without additional user action.

---

#### SC-TR-02 — Reflection form contains exactly 5 structured prompts

**Precondition:** TradeReflectionModal open
**Steps:** Inspect the modal contents

**Expected result:** Five textarea fields labelled (per spec §3):
1. "Why did you enter this trade? What was the setup?"
2. "What did the trade do well? Was the setup validated?"
3. "What went wrong or was unexpected?"
4. "Did you follow your rules? Any impulse decisions?"
5. "One lesson from this trade."

Each field is optional (placeholder text visible).

**Pass criteria:** Exactly 5 fields present; labels match spec.

---

#### SC-TR-03 — Character counter enforces 500-char limit per field

**Precondition:** TradeReflectionModal open
**Steps:**
1. Type exactly 500 characters into any reflection field
2. Attempt to type a 501st character

**Expected result:** Field accepts 500 characters. 501st character is not accepted. Counter shows "500/500" and changes to amber colouring near the limit.

**Pass criteria:** Hard 500-char limit enforced; counter visible.

---

#### SC-TR-04 — Skip button closes modal without saving

**Precondition:** TradeReflectionModal open with content typed in a field
**Steps:**
1. Type text into a reflection field
2. Click "Skip"

**Expected result:** Modal closes. No API call is made to `POST /trades/{id}/reflection`.

**Pass criteria:** Modal closed; no save request sent (verify via network tab).

---

#### SC-TR-05 — Save button persists reflection via POST

**Precondition:** TradeReflectionModal open
**Steps:**
1. Enter text in one or more reflection fields
2. Click "Save Reflection"

**Expected result:** Loading state shown during save. On success, modal shows "Saved!" state and closes after ~1.2 seconds. Network tab shows `POST /trades/{trade_id}/reflection` with the entered field values.

**Pass criteria:** Reflection saved to backend; modal closes on success.

---

#### SC-TR-06 — Existing reflection pre-populates on re-open

**Precondition:** A reflection has been previously saved for a trade
**Steps:**
1. Open the TradeReflection browsing page (`/TradeReflection`)
2. Locate the trade and open its reflection (or re-trigger the modal for a trade with a saved reflection)

**Expected result:** The five reflection fields are pre-populated with the previously saved values. Fields are editable.

**Pass criteria:** `GET /trades/{trade_id}/reflection` is called; previously saved text populates the fields.

---

#### SC-TR-07 — Trade summary values are backend-sourced (no client-side derivation)

**Precondition:** TradeReflectionModal open for a closed trade
**Steps:** Inspect the Trade Summary block in the modal

**Expected result:** All 8 summary fields (ticker, entry price, exit price, hold time, R-multiple, exit reason, exit state, exit date) display values from the GET /trades response. R-multiple: if `null`, shows "—" (spec §4 null rule — GET /trades may not return r_multiple). No client-side R computation performed.

**Pass criteria:** r_multiple shown as backend value or "—". No calculated value appears if backend returns null.

---

### 6.3 Cohort Analysis Scenarios (ST-03 — analytics.md §15)

**Source spec:** `docs/specs/frontend/pages/analytics.md §15`
**Note:** DEV-EPIC02-ST03-01 applies — values are correct but computed client-side from trade data prop, not from GET /analytics/cohort. Verify values match expected cohort calculation; do not expect a GET /analytics/cohort network call.
**Component:** `src/components/analytics/CohortAnalysis.js`

---

#### SC-CA-01 — Cohort analysis panel renders on Performance Analytics page

**Precondition:** Trade history contains at least 3 different entry months
**Steps:** Navigate to Performance Analytics; scroll to Cohort Analysis section (§15)

**Expected result:** Panel renders with period toggle (Month/Quarter/Year) defaulting to "Month". Table shows columns: Period, Trades, Win Rate, Avg R, Net P&L. Rows sorted descending by period (most recent first).

**Pass criteria:** Panel visible; table present; default period = Month.

---

#### SC-CA-02 — Period toggle changes cohort grouping

**Precondition:** Trade history spans multiple quarters and years
**Steps:**
1. Select "Quarter" from the period toggle
2. Verify table updates
3. Select "Year" from the period toggle
4. Verify table updates

**Expected result:** Rows re-group to show quarterly (Q1 2025, Q4 2024 etc.) or yearly (2025, 2024) cohorts. Trade counts change to reflect new grouping. Period labels match format: "Q1 2025" for quarter, "2025" for year.

**Pass criteria:** Toggle changes grouping; labels and counts update correctly.

---

#### SC-CA-03 — Insufficient data state: fewer than 3 periods

**Precondition:** Trade history spans fewer than 3 distinct entry periods for the selected period type
**Steps:** Navigate to Performance Analytics with minimal trade data; view Cohort Analysis

**Expected result:** Panel shows message: "Not enough closed trades to show [month/quarter/year] cohorts" (per spec §15).

**Pass criteria:** Insufficient-data message shown; no table rendered.

---

#### SC-CA-04 — Win rate and P&L values are numerically correct

**Precondition:** Known trade dataset:
- March 2025: 4 trades, 3 winning → win_rate = 75.0%; total P&L = £800
- February 2025: 2 trades, 1 winning → win_rate = 50.0%; total P&L = −£100
**Steps:** Navigate to Performance Analytics; locate March 2025 and February 2025 cohort rows

**Expected result:** March 2025 row: Trades=4, Win Rate=75.0%, Net P&L=£800. February 2025 row: Trades=2, Win Rate=50.0%, Net P&L=−£100.

**Pass criteria:** Values match expected calculation.

---

### 6.4 R-Multiple Distribution Scenarios (ST-04 — analytics.md §16)

**Source spec:** `docs/specs/frontend/pages/analytics.md §16`
**Endpoint:** `GET /analytics/r-multiple-distribution`
**Component:** `src/components/analytics/RMultipleDistributionBackend.js`

---

#### SC-RM-01 — R-multiple distribution panel renders on Performance Analytics page

**Precondition:** At least 5 closed trades with stop prices available
**Steps:** Navigate to Performance Analytics; scroll to R-Multiple Distribution section (§16)

**Expected result:** Panel renders with a bar chart showing frequency distribution across 7 R-multiple buckets. Positive buckets (>0R): green bars. Negative buckets (<0R): red bars. Summary row below chart shows 4 stats: Median R, % > 1R, Avg Winner, Avg Loser.

**Pass criteria:** Chart visible; colour coding correct; 4 stat cards below chart.

---

#### SC-RM-02 — Values are backend-sourced (no client-side R computation)

**Precondition:** Developer tools available
**Steps:**
1. Navigate to Performance Analytics with at least 5 qualifying trades
2. Open Network tab in developer tools
3. Inspect the GET /analytics/r-multiple-distribution response
4. Compare the displayed chart and stat values with the response payload

**Expected result:** The displayed bucket distribution, median_r, pct_above_1r, avg_winner_r, avg_loser_r exactly match the API response. No R-multiple is computed in the frontend code.

**Pass criteria:** Displayed values match API response 1:1. Hard rule: no client-side R derivation in §16 component.

---

#### SC-RM-03 — Insufficient data state: fewer than 5 qualifying trades

**Precondition:** Fewer than 5 closed trades with stop price data
**Steps:** Navigate to Performance Analytics; view R-Multiple Distribution section

**Expected result:** Panel shows message: "Close at least 5 trades to see R-multiple distribution." (per spec §16). No chart rendered.

**Pass criteria:** Threshold message shown; chart absent.

---

#### SC-RM-04 — R-multiple formula matches canonical spec

**Precondition:** Known trade: entry_price=£10.00, exit_price=£13.00, initial_stop_price=£8.00 → expected R = (13-10)/(10-8) = 1.5R
**Steps:**
1. Ensure the above trade exists in trade history with stop data
2. View R-Multiple Distribution; check which bucket the trade falls in (expected: "+1R to +2R")
3. Verify summary stats reflect this trade's R value

**Expected result:** Trade falls in the "+1R to +2R" bucket. Median R and avg_winner_r reflect 1.5 if this is the only qualifying trade. Backend formula used (no client-side computation).

**Pass criteria:** Trade lands in correct bucket; R value = 1.5.

---

### 6.5 Dashboard Homepage Scenarios (ST-05 — dashboard.md v2.0)

**Source spec:** `docs/specs/frontend/pages/dashboard.md` v2.0
**Component:** `src/pages/DashboardHome.js`; `src/components/dashboard/home/`

---

#### SC-DH-01 — Dashboard is the landing page (route `/`)

**Precondition:** Application loaded fresh
**Steps:** Navigate to application root (`/` or app entry URL)

**Expected result:** DashboardHome page renders. URL is `/` or the app root. Page title shows "Dashboard" heading.

**Pass criteria:** DashboardHome renders at app entry; no redirect to another page.

---

#### SC-DH-02 — All 5 data cards render with live data

**Precondition:** All backend endpoints reachable; at least one open position and recent signal
**Steps:** Navigate to Dashboard; wait for data to load

**Expected result:** Five cards visible:
1. Open Positions — shows open position count with profitable/losing/grace breakdown
2. Portfolio Heat — shows heat percentage with colour coding (green <15%, amber 15–25%, red >25%)
3. In Grace Today — shows count of positions in grace period
4. Signal Status — shows today's signal status
5. Recent Activity — shows recent trade activity

**Pass criteria:** All 5 cards loaded with data; loading spinners resolved.

---

#### SC-DH-03 — Cards fetch independently (no shared endpoint)

**Precondition:** Developer tools available
**Steps:**
1. Navigate to Dashboard
2. Open Network tab; observe API calls made on load

**Expected result:** At minimum, the following endpoints are called independently:
- `GET /positions` (Open Positions card)
- `GET /portfolio` (Portfolio Heat card)
- One endpoint for signals
- No composite `GET /dashboard/summary` endpoint called (engineering decision: individual calls only per PR notes)

**Pass criteria:** Individual endpoint calls observed; no composite endpoint.

---

#### SC-DH-04 — Individual card error does not break other cards

**Precondition:** One endpoint (e.g. `GET /positions`) blocked to return 500
**Steps:**
1. Mock or block `GET /positions` to return an error
2. Navigate to Dashboard
3. Observe all 5 cards

**Expected result:** Open Positions card shows an error state ("Unable to load" or equivalent from DashboardCard). All other 4 cards load normally with data.

**Pass criteria:** Error is isolated to the affected card; remaining cards unaffected.

---

#### SC-DH-05 — Portfolio Heat card colour coding

**Precondition:** Backend returns known heat values
**Steps:**
1. Set portfolio_heat_percent = 8% (expected: green, "Heat within safe range")
2. Set portfolio_heat_percent = 20% (expected: amber, "Heat elevated — monitor closely")
3. Set portfolio_heat_percent = 30% (expected: red, "Heat critical — review positions")

**Expected result per step:** Correct colour applied (emerald-400 / amber-400 / rose-400) and correct descriptive text.

**Pass criteria:** Three heat bands displayed correctly per spec.

---

#### SC-DH-06 — Click navigation: Open Positions card links to Positions page

**Precondition:** Dashboard loaded with data
**Steps:** Click the Open Positions card

**Expected result:** Browser navigates to the Positions page (`/Positions`).

**Pass criteria:** Navigation occurs; Positions page renders.

---

#### SC-DH-07 — Click navigation: Portfolio Heat card links to Risk Dashboard

**Precondition:** Dashboard loaded with data
**Steps:** Click the Portfolio Heat card

**Expected result:** Browser navigates to the Risk Dashboard page (`/RiskDashboard`).

**Pass criteria:** Navigation occurs; Risk Dashboard page renders.

---

#### SC-DH-08 — Responsive layout: 3-card row + 2-card row

**Precondition:** Browser at desktop width (≥768px)
**Steps:** Navigate to Dashboard; observe card layout

**Expected result:** Top row: 3 cards (Open Positions, Portfolio Heat, In Grace Today). Bottom row: 2 cards (Signal Status, Recent Activity). Cards fill available width.

**Pass criteria:** 3+2 card grid layout at desktop width.

---

#### SC-DH-09 — All API calls go through api.* (no direct fetch)

**Precondition:** Source code inspection
**Steps:** Review src/pages/DashboardHome.js and src/components/dashboard/home/*.js

**Expected result:** All API calls use `api.*` methods from base44Client.js (which routes through `doFetch`). No direct `fetch()` or `axios` calls in dashboard components.

**Pass criteria:** api.* pattern confirmed in all 5 card components.

---

#### SC-DH-10 — All endpoints failed: 5 individual card errors shown (DEV-EPIC03-ST05-01)

**Precondition:** All 5 dashboard endpoints blocked to return errors
**Steps:**
1. Mock all dashboard endpoints to return 500
2. Navigate to Dashboard

**Expected result:** Each of the 5 cards shows its individual error state. A "Retry" button is present in the page (per implementation: hidden in `<div className="hidden">`; not a full-page overlay). This is the accepted P3 behaviour per DEV-EPIC03-ST05-01.

**Note:** Spec §5 canonical requirement is a full-page error overlay with prominent Retry button. The hidden retry implementation is an accepted P3 deviation for v1.9. Scenario passes against implemented (not canonical) behaviour.

**Pass criteria:** 5 individual card errors visible; no full-page overlay (expected per deviation). Retry handler present in DOM.

---

### 5.7 v1.9 Automated Coverage Plan

The following v1.9 scenarios are candidates for Playwright automation in a future sprint (extending `tests/e2e/`):

| Scenario | Automation status | Notes |
|----------|------------------|-------|
| SC-CM-01 | Candidate | Requires analytics page mock for compliance-metrics endpoint |
| SC-CM-03 | Candidate | Mock empty response |
| SC-CM-04 | Candidate | Mock 500 error |
| SC-TR-01 | Candidate | Requires Positions page + exitMutation trigger |
| SC-TR-04 | Candidate | Simple: open modal, click Skip, verify no POST |
| SC-DH-01 | Candidate | Simple: navigate to `/`, assert heading |
| SC-DH-04 | Candidate | Mock one endpoint error, assert others load |
| SC-DH-10 | Candidate | Mock all errors, assert 5 card errors |

Manual-only (business logic verification):
- SC-CM-02, SC-TR-02, SC-TR-03, SC-TR-05, SC-TR-06, SC-TR-07 (require real trade data or complex form interaction)
- SC-CA-01 through SC-CA-04 (client-side cohort calculation — values depend on trade data)
- SC-RM-01 through SC-RM-04 (R-multiple values — backend numeric verification)
- SC-DH-02, SC-DH-05, SC-DH-06, SC-DH-07, SC-DH-08, SC-DH-09

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
| 1.2 | 2026-03-10 | Friction 2 deferred patch: added §5.5 Playwright Test Maintenance Protocol — cross-EPIC microcopy change obligation documented. When a component's UI microcopy is changed in a frontend delivery, Playwright tests for that component must be audited and updated in the same PR or a follow-on commit before the EPIC merges. §5.6 (backlog reference) renumbered from §5.5. |
| 1.1 | 2026-03-09 | ST-11 delivery: §5 Test Infrastructure Preconditions updated to reflect Playwright mock layer approach (RISK-07 resolved). §5.1 updated for automated + manual execution paths. §5.2 table updated: all 17 previously-blocked scenario groups now "Available". §5.3 Automated Coverage Summary table added (17 scenarios). §5.4 Backend API gap noted (BLG-API-01 raised). §5.5 replaces prior §5.4 backlog reference. TEST-GAP-EPIC-01 resolved. |
| 1.0.1 | 2026-03-06 | Added §5 Test Infrastructure Preconditions: documents which scenario groups require test data injection (Groups A–C and most of F — 17/27 scenarios), which are executable without injection (Groups D, E, G — 10/27 scenarios), environment requirements, and backlog reference TEST-GAP-EPIC-01. Renumbered prior §5–§7 to §6–§8. Applied from EX-LL Friction Item 3 deferred patch. |
| 1.0.0 | 2026-03-05 | Initial version. 27 scenarios covering heat thresholds, grace period, position risk table, prospective heat, API error states, empty states, and non-functional requirements. Derived from risk_dashboard.md v0.1.1 and metrics_definitions.md v1.6.0. Known deviations DEV-ST03-01 through DEV-ST03-05 documented in §2. |
