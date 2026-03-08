**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-08

---

# Delegation Log — 2026-03-06__release-v1.9 Sprint 1

---

## DEL-20260308-01

- **ST Item:** ST-07 — Risk Dashboard Backend: US Currency Conversion
- **EPIC:** EPIC-04
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering
- **GitHub Issue:** #39
- **Branch:** exec/2026-03-06__release-v1.9/EPIC-04
- **Delegated at:** 2026-03-08T22:00:00Z
- **What is needed:** In `backend/services/portfolio_service.py`, convert `entry_price` to GBP for US positions using the stored `fx_rate` field (same pattern as existing `current_price` conversion). Also convert `current_stop` to GBP for US positions using the same `fx_rate`. All position prices returned in GBP for both US and UK positions. Stop Distance % calculation must use matching currencies. Update golden output tests to include a US position with GBP-converted `entry_price` and `current_stop`; confirm golden output CI passes with no UK position regression. Canonical spec: `docs/specs/frontend/pages/risk_dashboard.md §6.2, §6.4` and `docs/specs/api_contracts/portfolio_endpoints.md`.
- **Spec reference:** `docs/specs/frontend/pages/risk_dashboard.md` §6.2, §6.4; `docs/specs/api_contracts/portfolio_endpoints.md`
- **Unblock criteria:** Commit `[EPIC-04][ST-07]` pushed to `exec/2026-03-06__release-v1.9/EPIC-04`; golden output CI passes; SC-RD scenarios for US position currency display pass.
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
- **Delegated at:** 2026-03-08T22:00:00Z
- **What is needed:** Update the Risk Dashboard React components so each renders its own independent error state when `GET /portfolio` fails, without silently falling back to the Base44 entity store. See Base44 prompt draft below.
- **Spec reference:** `docs/specs/frontend/pages/risk_dashboard.md` (all component sections)
- **Base44 prompt draft:**

  **Context:** The Risk Dashboard at `src/pages/RiskDashboard.js` fetches portfolio data via `GET /portfolio` using `api.*` or `doFetch` from `src/api/base44Client.js`. Currently when the API fails, some components fall back to the Base44 entity store (`base44.entities`) and display no visible error to the user. Scenarios SC-RD-02 and SC-RD-03 are currently failing.

  **The change:** For each of the following components — HeatGauge, DrawdownSummary, GracePeriodPanel, PositionRiskTable, ProspectiveHeatPanel — add an explicit error state that renders when `portfolioError` is set or the API call fails. The error state must be visually distinct from the "no data / loading" state (e.g. a red or amber card with an error message). For GracePeriodPanel specifically: when `portfolioError` is set, render a distinct error card (not an empty card). Remove or visually flag any silent entity store fallback so the user always knows the API failed.

  **API contract:** `GET /portfolio` is the primary data source. Error response follows `docs/specs/api_contracts/conventions.md §13`. Error codes: 500 for server error, network error for connection failure. No new endpoints required.

  **Behaviour rules:** (1) Each component must handle its own error independently — one component failing must not suppress errors in others. (2) Error state must render even if Base44 entity store has cached data. (3) Error messages must be user-readable (e.g. "Unable to load portfolio data. Please try again."). (4) No raw error objects or stack traces exposed to UI.

  **Non-functional rules:** Use existing component file structure in `src/components/risk/`. Do not introduce new API calls. Do not change the data contract with `GET /portfolio`. Use existing styling conventions.

  **Expected outcome:** Simulate a 500 response from `GET /portfolio` (or block the network call). Each of the 5 components shows a visible error state. GracePeriodPanel shows an error card — not an empty card. SC-RD-02 (portfolio API error → error state shown) and SC-RD-03 (GracePeriodPanel error vs empty state) both pass.

- **Unblock criteria:** Commit `[EPIC-04][ST-08]` pushed to branch; SC-RD-02 and SC-RD-03 confirmed passing by Director of Quality.
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
- **Delegated at:** 2026-03-08T22:00:00Z
- **What is needed:** Four independent column and sort fixes to the Risk Dashboard. See Base44 prompt draft below.
- **Spec reference:** `docs/specs/frontend/pages/risk_dashboard.md` §5.2, §6.2, §6.4, §7.5
- **Base44 prompt draft:**

  **Context:** The Risk Dashboard at `src/pages/RiskDashboard.js` with components in `src/components/risk/`. Four spec-defined display properties are currently incorrect or absent.

  **The change — 4 items:**
  1. **PositionRiskTable sort order:** Sort rows by stop distance ascending (tightest stop distance first = most at risk) within each state group. Spec: `risk_dashboard.md §6.4`.
  2. **Stop Price column:** Add a "Stop Price" column to PositionRiskTable showing `current_stop` in GBP, formatted to 2 decimal places. Spec: `risk_dashboard.md §6.2`.
  3. **Days in Grace column:** Add a "Days in Grace" column to the Grace Period table showing `holding_days`. Spec: `risk_dashboard.md §5.2`.
  4. **ProspectiveHeatPanel threshold label:** In the ProspectiveHeatPanel result row, add a badge showing the current threshold label (e.g. "Low", "Medium", "High"). The badge must update when a boundary is crossed. Spec: `risk_dashboard.md §7.5`.

  **API contract:** Data source is `GET /portfolio` (existing). `current_stop` and `holding_days` are already returned in the portfolio response. `GET /portfolio/prospective-heat` returns threshold label data for ProspectiveHeatPanel.

  **Behaviour rules:** (1) Sort ascending within state group — do not mix state groups. (2) Stop Price formatted as GBP with £ prefix, 2 dp. (3) Days in Grace is an integer count. (4) Threshold badge updates reactively when prospective heat recalculates.

  **Non-functional rules:** Minimal changes to existing component files. Use existing styling for columns and badges. Do not alter other columns or row data.

  **Expected outcome:** SC-RD-04 (sort ascending with 3+ positions), SC-RD-05 (Stop Price column present), SC-RD-07 (Days in Grace column present), SC-RD-08 (threshold label badge updates on boundary cross) — all pass.

- **Unblock criteria:** Commit `[EPIC-04][ST-09]` pushed to branch; SC-RD-04/05/07/08 confirmed passing by Director of Quality.
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
- **Delegated at:** 2026-03-08T22:00:00Z
- **What is needed:** Two cosmetic fixes to the HeatGauge component. See Base44 prompt draft below.
- **Spec reference:** `docs/specs/frontend/pages/risk_dashboard.md` §3.2, §6.3
- **Base44 prompt draft:**

  **Context:** The Risk Dashboard HeatGauge component (`src/components/risk/HeatGauge.js` or equivalent) has two cosmetic deviations from spec.

  **The change — 2 items:**
  1. **GRACE badge colour:** The state badge for the GRACE state must be blue (not amber). Spec: `risk_dashboard.md §6.3`. Change the badge colour class/style for GRACE state to blue.
  2. **GBP value at risk:** Display the GBP value at risk below the gauge percentage value in the HeatGauge component. The value should be formatted as £X,XXX (rounded to nearest pound or 2 dp). Spec: `risk_dashboard.md §3.2`.

  **API contract:** Both values are available from `GET /portfolio`. The GBP value at risk can be computed from `portfolio_heat_percent` and total portfolio value — or may be directly available in the portfolio response.

  **Behaviour rules:** (1) Badge colour change must apply only to GRACE state — do not alter other state badge colours. (2) GBP value at risk must be visible below the percentage value, not replacing it.

  **Non-functional rules:** Minimal changes. Existing styling conventions apply.

  **Expected outcome:** SC-RD-05 (GRACE badge is blue) and SC-RD-06 (GBP value at risk visible below gauge) both pass.

- **Unblock criteria:** Commit `[EPIC-04][ST-10]` pushed to branch; SC-RD-05/06 confirmed passing by Director of Quality.
- **Commit format required:** `[EPIC-04][ST-10] <description>` pushed to `exec/2026-03-06__release-v1.9/EPIC-04`
- **Status:** Pending

---

## DEL-20260308-05

- **ST Item:** ST-11 — Canonical Test Scenario Library Phase 1 (Risk Dashboard)
- **EPIC:** EPIC-05
- **Classification:** delegated_qa
- **Assigned to:** Director of Quality
- **GitHub Issue:** #43
- **Branch:** exec/2026-03-06__release-v1.9/EPIC-05
- **Delegated at:** 2026-03-08T22:00:00Z
- **What is needed:** First, agree with Head of Engineering on the test infrastructure approach (seeded SQLite DB, mock/stub API layer, or test fixture API). Then: (1) Create the agreed seeded test infrastructure. (2) Add a "Test Infrastructure Preconditions" section to `docs/testing/risk_dashboard_scenarios.md` describing how to set up the environment for independent replication. (3) Re-run all 17 NOT EXECUTED Risk Dashboard scenarios (SC-RD-02–06, SC-RD-07–12, SC-RD-15, SC-RD-16–18, SC-RD-24–25) against the seeded environment. (4) Record results (PASS/FAIL/BLOCKED) in `risk_dashboard_scenarios.md`. Infrastructure must be reproducible — no live external data.
- **Spec reference:** `docs/testing/risk_dashboard_scenarios.md`
- **Unblock criteria:** All 17 NOT EXECUTED scenarios have a recorded result in `risk_dashboard_scenarios.md`; "Test Infrastructure Preconditions" section present and sufficient for independent replication; commit `[EPIC-05][ST-11]` pushed to `exec/2026-03-06__release-v1.9/EPIC-05`.
- **Commit format required:** `[EPIC-05][ST-11] <description>` pushed to `exec/2026-03-06__release-v1.9/EPIC-05`
- **Status:** Pending

---

## DEL-20260308-06

- **ST Item:** ST-13 — Service Layer Test Coverage Standard
- **EPIC:** EPIC-05
- **Classification:** delegated_backend
- **Assigned to:** Backend Engineering Patterns Owner (document standard + CI step); Head of Engineering (agree threshold %)
- **GitHub Issue:** #45
- **Branch:** exec/2026-03-06__release-v1.9/EPIC-05
- **Delegated at:** 2026-03-08T22:00:00Z
- **What is needed:** (1) Agree a named coverage threshold % with Head of Engineering. (2) Author a Service Layer Test Coverage Standard in `docs/specs/backend_engineering_patterns.md` (version incremented) covering: threshold %, scope (`backend/services/`), tool (pytest-cov or equivalent). (3) Add a CI workflow step that runs pytest-cov on `backend/services/` and fails the build if coverage falls below the threshold. (4) Confirm CI passes with current test suite at or above threshold. Layer required: CI workflow YAML (`.github/workflows/`) + documentation (`backend_engineering_patterns.md`). Canonical spec: `docs/specs/backend_engineering_patterns.md`.
- **Spec reference:** `docs/specs/backend_engineering_patterns.md`
- **Unblock criteria:** Commit `[EPIC-05][ST-13]` pushed to `exec/2026-03-06__release-v1.9/EPIC-05`; `backend_engineering_patterns.md` version incremented; CI workflow YAML contains coverage step with named threshold; Director of Quality confirms.
- **Commit format required:** `[EPIC-05][ST-13] <description>` pushed to `exec/2026-03-06__release-v1.9/EPIC-05`
- **Status:** Pending
