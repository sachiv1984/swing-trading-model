**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-08

---

# Delegation Log — 2026-03-06__release-v1.9 (Sprint 1)

---

## DEL-20260308-01

- **ST Item:** ST-07 — Risk Dashboard Backend: US Currency Conversion
- **EPIC:** EPIC-04
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering
- **GitHub Issue:** #39
- **Branch:** exec/2026-03-06__release-v1.9/EPIC-04
- **Target branch:** exec/2026-03-06__release-v1.9/EPIC-04
- **Delegated at:** 2026-03-08T22:00:00Z
- **What is needed:**

  In `backend/services/portfolio_service.py`, the `get_portfolio_summary()` function currently returns `entry_price` in native USD for US positions (line 175: `"entry_price": round(entry_price, 2)` — no FX conversion applied), and `current_stop` without FX conversion for any position (line 181: `"current_stop": round(pos.get("current_stop", 0), 2)`). This causes the Risk Dashboard to display US position entry and stop prices in USD rather than GBP, and makes Stop Distance % incorrect for US positions (mixing currencies).

  **Changes required — service layer only (`backend/services/portfolio_service.py`):**

  1. **Convert `entry_price` to GBP for US positions.** Apply the same pattern already used for `current_price_gbp`: divide by `stored_fx_rate` (or `live_fx_rate` if stored rate is absent). Use `stored_fx_rate = pos.get('fx_rate', 1.27)` — consistent with the existing Position Risk calculation (lines 112, 158). Result should be assigned to `entry_price_gbp`.

  2. **Convert `current_stop` to GBP for US positions.** Same FX conversion: `current_stop_gbp = pos.get("current_stop", 0) / stored_fx_rate` for US positions. For UK positions: `current_stop_gbp = pos.get("current_stop", 0)` (no conversion — already GBP).

  3. **Return GBP values in the positions dict.** Update line 175: `"entry_price": round(entry_price_gbp, 2)`. Update line 181: `"current_stop": round(current_stop_gbp, 2)`.

  4. **Update golden output tests** (`tests/golden_outputs.json`) to include a US position with GBP-converted `entry_price` and `current_stop` — confirm no regression on existing UK positions.

  **Spec references governing this item:**
  - `docs/specs/frontend/pages/risk_dashboard.md §6.2` — Entry Price column: "GBP, 2 decimal places"; Stop Price column: "GBP, 2 decimal places"; Stop Distance derivation: `(current_stop − current_price) / current_price × 100` — requires all values in GBP
  - `docs/specs/frontend/pages/risk_dashboard.md §11` — DEV-ST03-11 (entry_price USD) and DEV-ST03-12 (current_stop USD) — resolution target v1.9

- **Spec reference:** `docs/specs/frontend/pages/risk_dashboard.md#§6.2` and `#§11` (DEV-ST03-11, DEV-ST03-12); `docs/specs/backend_engineering_patterns.md`
- **Base44 prompt draft:** N/A — backend only
- **Unblock criteria:** Commit `[EPIC-04][ST-07] <description>` pushed to `exec/2026-03-06__release-v1.9/EPIC-04`; golden output CI passes with no regression; Director of Quality confirms
- **Commit format required:** `[EPIC-04][ST-07] <description>` pushed to `exec/2026-03-06__release-v1.9/EPIC-04`
- **Status:** Pending

---

## DEL-20260308-02

- **ST Item:** ST-08 — Risk Dashboard Frontend: Error States & Entity Fallback
- **EPIC:** EPIC-04
- **Classification:** delegated_frontend
- **Assigned to:** Base44 Frontend Prompt Owner
- **GitHub Issue:** #40
- **Branch:** exec/2026-03-06__release-v1.9/EPIC-04
- **Target branch:** exec/2026-03-06__release-v1.9/EPIC-04
- **Delegated at:** 2026-03-08T22:00:00Z
- **What is needed:**

  All five Risk Dashboard components (HeatGauge, DrawdownSummary, GracePeriodPanel, PositionRiskTable, ProspectiveHeatPanel) must render their own independent error states when `GET /portfolio` fails. The Base44 entity store fallback (`base44.entities`) must not silently mask API errors. GracePeriodPanel must render a distinct error card (not an empty/no-grace-positions state) when an API error is set.

  **Note on RISK-05 (entity store fallback):** Before submitting the Base44 prompt, confirm with the Base44 Frontend Prompt Owner whether the entity store fallback should be (a) removed from Risk Dashboard components, or (b) retained but shown with an error indicator. The sprint backlog permits either approach. Record the chosen approach in the spec deviation section and flag if it differs from the spec. This pre-alignment must be completed before prompt submission.

- **Spec reference:** `docs/specs/frontend/pages/risk_dashboard.md#§3.4`, `#§4.3`, `#§5.5`, `#§6.5`, `#§7.6`
- **Base44 prompt draft:**

  ---

  **SECTION 1 — Context**

  The Risk Dashboard page (`src/pages/RiskDashboard.js` and its child components in `src/components/risk/`) displays portfolio heat, drawdown, grace period positions, position risk table, and prospective heat. The page fetches data from `GET /portfolio` and (for drawdown days) `GET /analytics/metrics`.

  Currently, when `GET /portfolio` fails, some or all components may fall back to the Base44 entity store (`base44.entities`) rather than showing an error state. This means API failures are silently masked — the user sees stale data instead of an error message. This is DEV-ST03-01 and DEV-ST03-02 in `docs/specs/frontend/pages/risk_dashboard.md §11`.

  **SECTION 2 — The Change**

  Make every Risk Dashboard component render an independent, visible error state when the portfolio API call fails. Per `docs/specs/frontend/pages/risk_dashboard.md §3.4, §4.3, §5.5, §6.5, §7.6`:

  - **HeatGauge** error state: card shows "Unable to load heat data" + retry button. No gauge rendered.
  - **DrawdownSummary** error state: card shows "Unable to load drawdown data". No metrics shown.
  - **GracePeriodPanel** error state: card shows "Unable to load position data". This must be visually distinct from the empty state ("No positions currently in grace period") — the error state indicates an API failure, not zero grace positions.
  - **PositionRiskTable** error state: card shows "Unable to load position data". No table rendered.
  - **ProspectiveHeatPanel** error state (if triggered): does not block input, but shows error on calculate failure.

  Additionally, the Base44 entity store fallback (`base44.entities`) must not silently provide stale data while an API error is active. Either: (a) remove the entity store fallback from Risk Dashboard components entirely, or (b) if retained, show a visible indicator ("Showing cached data — live data unavailable") alongside stale content. Approach to be confirmed with Base44 Frontend Prompt Owner before prompt submission (RISK-05).

  **SECTION 3 — API Contract**

  Primary endpoint: `GET /portfolio` (no request body)

  Success response shape:
  ```json
  {
    "cash": 12500.00,
    "total_value": 28340.00,
    "portfolio_heat_percent": 14.2,
    "positions": [
      {
        "ticker": "AAPL",
        "market": "US",
        "status": "open",
        "display_status": "GRACE",
        "entry_price": 142.50,
        "current_price": 148.30,
        "current_stop": 138.00,
        "holding_days": 4,
        "grace_days_remaining": 6,
        "pnl_pct": 4.07
      }
    ],
    "position_risks": [{"ticker": "AAPL", "position_risk_gbp": 450.00}],
    "current_drawdown_percent": -2.4
  }
  ```

  Error response (HTTP 4xx/5xx or network failure): component must detect `portfolioError` (however the current implementation exposes the error state from the API hook) and render the error card.

  Secondary endpoint (drawdown days only): `GET /analytics/metrics` — separate call; failure must show "Unable to load drawdown data" in DrawdownSummary independently.

  **SECTION 4 — Behaviour Rules**

  - Error state is triggered by any API failure: network timeout, HTTP 500, HTTP 404, or any non-2xx response.
  - Error state must be visible and distinct. It must not be hidden behind a loading spinner, empty state, or stale cached data.
  - GracePeriodPanel has two non-loaded states that must be clearly different:
    - *Empty state* (API success, zero grace positions): "No positions currently in grace period" — muted text, no table.
    - *Error state* (API failure): "Unable to load position data" — error card styling (e.g., red/amber border or icon).
  - Each component's error state is independent. If only `GET /portfolio` fails, components that depend on `GET /analytics/metrics` independently may still show data (and vice versa).
  - Retry button (where spec'd — HeatGauge §3.4): triggers re-fetch of the failed API call.
  - Error state must not persist after a successful re-fetch. If the user retries and the API responds successfully, the component renders normally.
  - Do not show both an error state and data simultaneously (unless entity store fallback with indicator is chosen per RISK-05 approach (b)).

  **SECTION 5 — Non-Functional Rules**

  - Do not change any component that is not in error-state scope. Loading states, successful data display, and the Prospective Heat input form must remain unchanged.
  - Do not alter the API call pattern — the same endpoints must be called in the same sequence.
  - Do not add new API calls or new dependencies.
  - Do not change any styling that is not directly related to the error state card (e.g., do not alter column widths, colour themes, or layout).
  - Existing passing scenarios (SC-RD-01 — successful load) must not regress.

  **SECTION 6 — Expected Outcome**

  Return the complete modified files:
  - `src/pages/RiskDashboard.js` (if the error state logic is managed at page level)
  - `src/components/risk/HeatGauge.js`
  - `src/components/risk/DrawdownSummary.js`
  - `src/components/risk/GracePeriodPanel.js`
  - `src/components/risk/PositionRiskTable.js`
  - `src/components/risk/ProspectiveHeatPanel.js`

  Return only files that are changed. Each file must include the complete modified content (not a diff). File naming: PascalCase matching the existing filenames exactly.

  ---

- **Unblock criteria:** Commit `[EPIC-04][ST-08]` pushed to `exec/2026-03-06__release-v1.9/EPIC-04`; SC-RD-02 (portfolio API error → error state shown) and SC-RD-03 (GracePeriodPanel error vs empty state) verified by Director of Quality; entity store fallback decision documented
- **Commit format required:** `[EPIC-04][ST-08] <description>` pushed to `exec/2026-03-06__release-v1.9/EPIC-04`
- **Status:** Pending

---

## DEL-20260308-03

- **ST Item:** ST-09 — Risk Dashboard Frontend: Table and Column Fixes
- **EPIC:** EPIC-04
- **Classification:** delegated_frontend
- **Assigned to:** Base44 Frontend Prompt Owner
- **GitHub Issue:** #41
- **Branch:** exec/2026-03-06__release-v1.9/EPIC-04
- **Target branch:** exec/2026-03-06__release-v1.9/EPIC-04
- **Delegated at:** 2026-03-08T22:00:00Z
- **What is needed:**

  Four independent fixes to the Risk Dashboard table and column structure. Can be batched into a single Base44 prompt session alongside ST-08 if convenient, but each fix is independent.

- **Spec reference:** `docs/specs/frontend/pages/risk_dashboard.md#§5.2` (Days in Grace column), `#§6.2` (Stop Price column), `#§6.4` (sort order), `#§7.5` (threshold label)
- **Base44 prompt draft:**

  ---

  **SECTION 1 — Context**

  The Risk Dashboard (`src/pages/RiskDashboard.js`, `src/components/risk/`) has four known spec deviations that need correcting. All four fixes are purely presentational — no new backend calls, no new data fields, no new API endpoints. The backend already returns all required fields.

  **SECTION 2 — The Change**

  Four fixes, all based on `docs/specs/frontend/pages/risk_dashboard.md`:

  **Fix 1: PositionRiskTable — Sort order (§6.4)**
  Within each status group (GRACE, LOSING, PROFITABLE), positions must be sorted by stop distance ascending (smallest absolute stop distance first = most at risk). Primary sort: status group order (GRACE → LOSING → PROFITABLE). Secondary sort within group: ascending by `|(current_stop − current_price) / current_price × 100|`. Currently, the table is sorted descending (DEV-ST03-03).

  **Fix 2: PositionRiskTable — Add Stop Price column (§6.2)**
  The `current_stop` field is already returned by `GET /portfolio` but is not displayed. Add a "Stop Price" column to PositionRiskTable showing `current_stop` formatted as GBP, 2 decimal places (e.g., `£138.00`). Column position: after "Current Price", before "Stop Distance" (per §6.2 column order). DEV-ST03-04 resolution.

  **Fix 3: GracePeriodPanel — Add Days in Grace column (§5.2)**
  The Grace Period table must include a "Days in Grace" column sourced from `holding_days` (integer). Column position: between "Entry Date" and "Days Remaining" per §5.2 table definition. DEV-ST03-07 resolution.

  **Fix 4: ProspectiveHeatPanel — Threshold label badge updates on boundary cross (§7.5)**
  After the Calculate call returns, the result section must show a threshold label (Low / Moderate / High / Extreme) that updates dynamically when the calculated heat crosses a threshold boundary. The label follows the same colour scheme as HeatGauge §3.3: Green/Low (<10%), Amber/Moderate (10–19.9%), Orange/High (20–29.9%), Red/Extreme (≥30%). DEV-ST03-09 resolution.

  **SECTION 3 — API Contract**

  `GET /portfolio` response — position fields in use:
  ```json
  {
    "ticker": "AAPL",
    "display_status": "GRACE",
    "entry_price": 142.50,
    "current_price": 148.30,
    "current_stop": 138.00,
    "holding_days": 4,
    "grace_days_remaining": 6,
    "pnl_pct": 4.07
  }
  ```

  Prospective heat endpoint: `GET /portfolio/prospective-heat?ticker=&shares=<int>&entry_price=<decimal>&stop_price=<decimal>`
  Success response: `{ "projected_heat_percent": 18.6, "heat_increase_percent": 4.4 }` (fields may vary — use what the component currently receives).

  **SECTION 4 — Behaviour Rules**

  **Fix 1 — Sort:**
  - Stop distance = `|(current_stop − current_price) / current_price × 100|` (absolute value, or the signed value with sign stripped for sort purposes)
  - Ascending = smallest distance first = position most at risk of being stopped out
  - Sort is stable within each status group
  - No user-controlled sort toggle (spec does not define one)

  **Fix 2 — Stop Price column:**
  - Display `current_stop` with £ prefix, 2 decimal places: `£138.00`
  - Column header: "Stop Price"
  - If `current_stop` is 0 or missing: display `—` (em dash)

  **Fix 3 — Days in Grace column:**
  - Display `holding_days` as integer: `4`
  - Column header: "Days in Grace"
  - No colour coding (colour coding applies to "Days Remaining" only per §5.3)

  **Fix 4 — Threshold label in ProspectiveHeatPanel:**
  - After Calculate: show threshold label badge alongside the "Projected heat" value
  - Label + colour: Low (green, <10%), Moderate (amber, 10–19.9%), High (orange, 20–29.9%), Extreme (red, ≥30%)
  - Label updates reactively if a new calculate result arrives with a different heat value
  - On reset: label clears with the rest of the result section

  **SECTION 5 — Non-Functional Rules**

  - Do not change any columns not mentioned above (Ticker, State, Entry Price, Current Price, Holding Days, P&L % in PositionRiskTable remain unchanged)
  - Do not alter the error states or loading states of any component
  - Do not change the GracePeriodPanel "Days Remaining" column or its colour coding
  - Do not add new API calls
  - Existing SC-RD-01 (successful load) must not regress

  **SECTION 6 — Expected Outcome**

  Return the complete modified files:
  - `src/components/risk/PositionRiskTable.js` (fixes 1 and 2)
  - `src/components/risk/GracePeriodPanel.js` (fix 3)
  - `src/components/risk/ProspectiveHeatPanel.js` (fix 4)

  Return only files that are changed. Complete file content, not a diff.

  ---

- **Unblock criteria:** Commit `[EPIC-04][ST-09]` pushed to `exec/2026-03-06__release-v1.9/EPIC-04`; SC-RD-04 (sort ascending), SC-RD-05 (Stop Price column), SC-RD-07 (Days in Grace column), SC-RD-08 (threshold label) verified by Director of Quality
- **Commit format required:** `[EPIC-04][ST-09] <description>` pushed to `exec/2026-03-06__release-v1.9/EPIC-04`
- **Status:** Pending

---

## DEL-20260308-04

- **ST Item:** ST-10 — Risk Dashboard Frontend: HeatGauge and Cosmetic Fixes
- **EPIC:** EPIC-04
- **Classification:** delegated_frontend
- **Assigned to:** Base44 Frontend Prompt Owner
- **GitHub Issue:** #42
- **Branch:** exec/2026-03-06__release-v1.9/EPIC-04
- **Target branch:** exec/2026-03-06__release-v1.9/EPIC-04
- **Delegated at:** 2026-03-08T22:00:00Z
- **What is needed:**

  Two cosmetic fixes to HeatGauge component: (1) GRACE badge colour changed from amber to blue; (2) GBP value at risk displayed below the gauge percentage value.

- **Spec reference:** `docs/specs/frontend/pages/risk_dashboard.md#§3.2` (GBP value at risk), `#§6.3` (GRACE badge blue)
- **Base44 prompt draft:**

  ---

  **SECTION 1 — Context**

  The Risk Dashboard HeatGauge (`src/components/risk/HeatGauge.js`) and PositionRiskTable (`src/components/risk/PositionRiskTable.js`) have two cosmetic spec deviations (DEV-ST03-05 and DEV-ST03-06).

  **SECTION 2 — The Change**

  **Fix 1: GRACE badge colour — PositionRiskTable (§6.3)**
  The GRACE status badge currently renders in amber. Per §6.3, GRACE badge colour must be blue (no specific hex given — use a standard blue, e.g., `#3b82f6` or tailwind `blue-500`). LOSING remains red. PROFITABLE remains green. DEV-ST03-05 resolution.

  **Fix 2: GBP value at risk — HeatGauge (§3.2)**
  The HeatGauge currently shows: primary value (heat %) and threshold label badge. §3.2 requires a tertiary display: "GBP value at risk in smaller text (e.g., £4,260 at risk)". This value is derived from the portfolio response.

  The GBP value at risk is the total of all `position_risk_gbp` values from `position_risks[]` in the `GET /portfolio` response:
  ```json
  "position_risks": [
    {"ticker": "AAPL", "position_risk_gbp": 450.00},
    {"ticker": "SHEL", "position_risk_gbp": 320.00}
  ]
  ```
  Sum = £770.00 at risk. Display format: `£770.00 at risk` — smaller font, below the heat percentage. If `position_risks` is empty or sum is zero: display `£0.00 at risk` (do not hide the row).

  **SECTION 3 — API Contract**

  `GET /portfolio` response fields in use:
  ```json
  {
    "portfolio_heat_percent": 14.2,
    "position_risks": [
      {"ticker": "AAPL", "position_risk_gbp": 450.00},
      {"ticker": "SHEL", "position_risk_gbp": 320.00}
    ]
  }
  ```
  `position_risks` is an array of `{ticker: string, position_risk_gbp: number}` objects.

  **SECTION 4 — Behaviour Rules**

  **Fix 1 — GRACE badge:**
  - GRACE badge background: blue (e.g., `#3b82f6`)
  - GRACE badge text: white (maintain readability)
  - No other badge colour changes

  **Fix 2 — GBP value at risk:**
  - Sum all `position_risk_gbp` values from `position_risks` array
  - Format as `£{total.toFixed(2)} at risk`
  - Display below the heat percentage value, above or below the threshold badge (implementation choice; must not obscure primary value)
  - Font size: smaller than primary heat percentage (e.g., `text-sm` or similar)
  - Colour: muted text (grey), not colour-coded to the heat threshold
  - States: if `position_risks` is missing or null, treat as empty array (sum = 0); display `£0.00 at risk`
  - In error state (API failed): do not show the GBP value row — the error card replaces the gauge entirely (per §3.4)

  **SECTION 5 — Non-Functional Rules**

  - Do not change HeatGauge loading state, gauge arc/bar rendering, primary percentage display, or threshold colour logic
  - Do not change any PositionRiskTable column other than the GRACE badge colour
  - Do not add new API calls
  - Existing SC-RD-01 must not regress

  **SECTION 6 — Expected Outcome**

  Return the complete modified files:
  - `src/components/risk/HeatGauge.js` (fix 2)
  - `src/components/risk/PositionRiskTable.js` (fix 1)

  Return complete file content, not a diff. PascalCase filenames matching existing disk names exactly.

  ---

- **Unblock criteria:** Commit `[EPIC-04][ST-10]` pushed to `exec/2026-03-06__release-v1.9/EPIC-04`; Director of Quality visually confirms GRACE badge is blue and GBP value at risk displayed beneath gauge percentage; SC-RD-05 and SC-RD-06 pass
- **Commit format required:** `[EPIC-04][ST-10] <description>` pushed to `exec/2026-03-06__release-v1.9/EPIC-04`
- **Status:** Pending

---

## DEL-20260308-05

- **ST Item:** ST-11 — Canonical Test Scenario Library Phase 1 (Risk Dashboard)
- **EPIC:** EPIC-05
- **Classification:** delegated_qa
- **Assigned to:** Director of Quality (QA & Testing Owner)
- **GitHub Issue:** #43
- **Branch:** exec/2026-03-06__release-v1.9/EPIC-05
- **Target branch:** exec/2026-03-06__release-v1.9/EPIC-05
- **Delegated at:** 2026-03-08T22:00:00Z
- **What is needed:**

  1. **Agree test infrastructure approach** with Head of Engineering at sprint start: seeded SQLite database, mock/stub API layer, or test fixture API. Record the chosen approach in a new "Test Infrastructure Preconditions" section of `docs/testing/risk_dashboard_scenarios.md` (this is also an outstanding action from the v1.8 closure record).

  2. **Set up the infrastructure** so the following states can be reproduced reliably:
     - Specific `portfolio_heat_percent` values (e.g., 0%, 8%, 18%, 32%)
     - Positions with specific `grace_days_remaining` values (e.g., 0, 1, 3, 9)
     - Empty position state (no open positions)
     - Controlled `GET /portfolio/prospective-heat` responses

  3. **Re-run all 17 NOT EXECUTED scenarios** from `docs/testing/risk_dashboard_scenarios.md`: SC-RD-02, SC-RD-03, SC-RD-04, SC-RD-05, SC-RD-06, SC-RD-07, SC-RD-08, SC-RD-09, SC-RD-10, SC-RD-11, SC-RD-12, SC-RD-15, SC-RD-16, SC-RD-17, SC-RD-18, SC-RD-24, SC-RD-25 — against the seeded environment. Record result (PASS / FAIL / BLOCKED) for each.

  4. **Commit** the updated `risk_dashboard_scenarios.md` (with results and preconditions section) to `exec/2026-03-06__release-v1.9/EPIC-05` with commit format `[EPIC-05][ST-11] <description>`.

  Note: ST-11 should be run **after** ST-07, ST-08, ST-09, ST-10 are delivered — so that the error state and column fix scenarios (SC-RD-02–SC-RD-09) can be tested against the corrected frontend.

- **Spec reference:** `docs/testing/risk_dashboard_scenarios.md`
- **Base44 prompt draft:** N/A — QA work
- **Unblock criteria:** All 17 scenarios have recorded results in `risk_dashboard_scenarios.md`; "Test Infrastructure Preconditions" section present and sufficient for independent replication; Director of Quality confirms completeness; commit pushed
- **Commit format required:** `[EPIC-05][ST-11] <description>` pushed to `exec/2026-03-06__release-v1.9/EPIC-05`
- **Status:** Pending

---

## DEL-20260308-06

- **ST Item:** ST-13 — Service Layer Test Coverage Standard
- **EPIC:** EPIC-05
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering (implementation); Backend Engineering Patterns Owner (standard document)
- **GitHub Issue:** #45
- **Branch:** exec/2026-03-06__release-v1.9/EPIC-05
- **Target branch:** exec/2026-03-06__release-v1.9/EPIC-05
- **Delegated at:** 2026-03-08T22:00:00Z
- **What is needed:**

  1. **Agree coverage threshold %** between Backend Engineering Patterns Owner and Head of Engineering at sprint start. Record this threshold in the standard document.

  2. **Author the Service Layer Test Coverage Standard** as a new section in `docs/specs/backend_engineering_patterns.md` (or a referenced child document). The standard must include:
     - Named coverage threshold (the agreed %)
     - Scope: `backend/services/` directory
     - Tool: `pytest-cov` (or agreed equivalent)
     - Enforcement: CI build fails if coverage falls below threshold

  3. **Add a CI workflow step** in `.github/workflows/` that:
     - Runs `pytest-cov` (or equivalent) on `backend/services/`
     - Fails the build if coverage is below the agreed threshold
     - Produces a coverage report (stdout or artifact)

  4. **Demonstrate enforcement** with a controlled test: show that a coverage-reducing change causes the CI step to fail.

  5. **Increment the version** of `docs/specs/backend_engineering_patterns.md`.

  6. **Commit** all changes to `exec/2026-03-06__release-v1.9/EPIC-05` with format `[EPIC-05][ST-13] <description>`.

- **Spec reference:** `docs/specs/backend_engineering_patterns.md`
- **Base44 prompt draft:** N/A — backend/CI work
- **Unblock criteria:** Commit `[EPIC-05][ST-13]` pushed to `exec/2026-03-06__release-v1.9/EPIC-05`; CI coverage step visible in workflow YAML; threshold named in standard document; `backend_engineering_patterns.md` version incremented; Director of Quality confirms CI step present
- **Commit format required:** `[EPIC-05][ST-13] <description>` pushed to `exec/2026-03-06__release-v1.9/EPIC-05`
- **Status:** Pending
