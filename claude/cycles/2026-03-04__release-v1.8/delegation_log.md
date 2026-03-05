Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-05

# Delegation Log — 2026-03-04__release-v1.8

---

## DEL-20260305-01

- **ST Item:** ST-02 — Backend: Confirm Heat Calculation Availability
- **EPIC:** EPIC-01
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering
- **GitHub Issue:** #18
- **Branch:** exec/2026-03-04__release-v1.8/EPIC-01
- **Delegated at:** 2026-03-05T01:00:00Z
- **What is needed:** Confirm that `portfolio_heat_percent` is available in the `GET /portfolio` response (or document the dedicated endpoint approach). Verify the implementation formula matches `metrics_definitions.md §Portfolio Heat` exactly for a known set of open positions. Also confirm the approach for prospective heat calculation (query param extension to `GET /portfolio` vs dedicated endpoint). API Contracts & Documentation Owner must confirm contract alignment. No new external dependencies permitted.
- **Spec reference:** `docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio`, `docs/specs/metrics_definitions.md#Portfolio Heat`
- **Unblock criteria:** Manual test confirms `GET /portfolio` returns `portfolio_heat_percent` matching the canonical formula; API Contracts owner confirms; commit pushed to `exec/2026-03-04__release-v1.8/EPIC-01` in format `[EPIC-01][ST-02] <description>`
- **Commit format required:** `[EPIC-01][ST-02] <description>` pushed to `exec/2026-03-04__release-v1.8/EPIC-01`
- **Status:** Pending

---

## DEL-20260305-02

- **ST Item:** ST-03 — Frontend: Risk Dashboard Page Implementation
- **EPIC:** EPIC-01
- **Classification:** delegated_frontend
- **Assigned to:** Base44 Frontend Prompt Owner
- **GitHub Issue:** #19
- **Branch:** exec/2026-03-04__release-v1.8/EPIC-01
- **Delegated at:** 2026-03-05T01:00:00Z
- **What is needed:** Implement the Risk Dashboard page using Base44 code generation from the Base44 prompt draft below. ST-02 must be confirmed done before frontend wiring begins (heat endpoint must be confirmed available).
- **Spec reference:** `docs/specs/frontend/pages/risk_dashboard.md` v0.1.0
- **Base44 prompt draft:**

  **Context:**
  Swing-trading decision-support tool (FastAPI backend, Base44 React frontend). The backend is the single source of truth for all calculations. The frontend must never derive or recalculate metric values — every displayed number comes from a backend response.

  **The change:**
  Add a new Risk Dashboard page. This is a monitoring page the trader views each day to assess overall portfolio risk before making decisions. It is accessible via a route in the main nav (e.g. `/risk`).

  **API contract:**
  - `GET /portfolio` — returns portfolio overview including `portfolio_heat_percent` (confirmed by ST-02), `current_drawdown_percent`, `peak_portfolio_value`, and the `positions` array with fields: `id, ticker, market, entry_date, entry_price, shares, current_price (GBP), current_value, pnl, pnl_pct, current_stop, holding_days, status, display_status, fx_rate, grace_period, grace_days_remaining, live_fx_rate`
  - Heat formula (from `metrics_definitions.md §Portfolio Heat`): `portfolio_heat_percent = (sum of stop distances in GBP across all open positions) / total_portfolio_value × 100`. This is computed server-side; frontend reads `portfolio_heat_percent` directly.
  - Prospective heat: to be confirmed by ST-02 whether query param extension or dedicated endpoint is used.

  **Behaviour rules:**
  1. Portfolio Heat Gauge: circular or arc gauge showing `portfolio_heat_percent`. Colour-coded: `#22c55e` (green) for < 10%, `#f59e0b` (amber) for 10–20%, `#f97316` (orange) for 20–30%, `#ef4444` (red) for ≥ 30%. Boundary values (exactly 10%, 20%, 30%) use the higher colour (10% = amber, 20% = orange, 30% = red). Show current value as text in the centre.
  2. Drawdown Summary: show `current_drawdown_percent` (e.g. "−8.2%") and the number of days since the portfolio was last at peak (derive from portfolio history if available, or show "N/A"). Show `peak_portfolio_value` as reference.
  3. Grace Period Panel: list all positions where `grace_period == true`, sorted by `grace_days_remaining` ascending (most urgent first). Per row: ticker, entry_date, `grace_days_remaining` days remaining (colour-coded: ≥ 5 days = green, 2–4 days = amber, ≤ 1 day = red). If empty: show "No positions in grace period."
  4. Position Risk Table: list all open positions. Per row: ticker, `display_status` badge (GRACE/LOSING/PROFITABLE), entry_price (native), current_price (GBP), stop distance % (derive from `(current_price - current_stop) / current_price * 100`... wait, actually this needs to come from the backend — check whether stop_distance_percent is returned. If not, this is a display calculation from `current_price` and `current_stop` — acceptable per spec since it's a display aid), holding_days. Sort: GRACE first, then LOSING, then PROFITABLE; within each group sort by stop distance descending (most at risk first).
  5. Prospective Heat Indicator: collapsible panel. Input fields: ticker (text), shares (positive number), entry_price (positive number), stop_price (positive number, must be < entry_price — enforce client-side). On submit: call backend prospective heat endpoint (confirmed by ST-02). Show projected heat % and delta from current. All validation also enforced server-side.
  6. Each component renders its own error state independently on API failure. If `GET /portfolio` fails, each panel shows its own error message, not a full-page error.
  7. Empty state: if no open positions, show appropriate empty states in each panel.
  8. No console errors on clean load.

  **Non-functional rules:**
  - All metric values read from backend response — zero client-side recalculation of portfolio metrics (stop distance % as a display-only derived field is the only exception, and only if not returned by backend).
  - Prospective heat inputs validated positive integers/decimals; stop_price < entry_price enforced client-side before submission.
  - No new authentication surface.
  - XSS risk: numeric inputs only in prospective heat form.

  **Expected outcome:**
  Risk Dashboard page renders at designated route. All five sections display correctly. Heat gauge colour matches thresholds at boundary values. ST-04 acceptance scenarios all pass. Director of Quality sign-off.

- **Unblock criteria:** ST-02 confirmed done; Base44 prompt submitted and page implemented; commit pushed to `exec/2026-03-04__release-v1.8/EPIC-01` in format `[EPIC-01][ST-03] <description>`; ST-04 acceptance scenarios pass
- **Commit format required:** `[EPIC-01][ST-03] <description>` pushed to `exec/2026-03-04__release-v1.8/EPIC-01`
- **Status:** Pending

---

## DEL-20260305-03

- **ST Item:** ST-04 — QA: Risk Dashboard Acceptance Test Scenarios
- **EPIC:** EPIC-01
- **Classification:** delegated_qa
- **Assigned to:** QA & Testing Owner (scenario authoring); Director of Quality (review and sign-off)
- **GitHub Issue:** #20
- **Branch:** exec/2026-03-04__release-v1.8/EPIC-01
- **Delegated at:** 2026-03-05T01:00:00Z
- **What is needed:** Author `docs/testing/risk_dashboard_scenarios.md` with acceptance test scenarios covering all five Risk Dashboard page sections. Scenarios may be drafted before ST-03 completes; execution and Director of Quality sign-off requires ST-03 built.
  Scenario requirements:
  - Heat gauge threshold boundaries: exactly 0%, 10%, 20%, 30%
  - Grace period at day 1, day 10 (within grace), day 11 (grace expired)
  - All three position states simultaneously: at least one GRACE, one LOSING, one PROFITABLE
  - Prospective heat: a new position that would push heat above 20% threshold
  - All API error states per component (5 independent error scenarios)
  - Empty state (no open positions)
  - All expected values derived from `metrics_definitions.md` v1.6.0 — no independent interpretation
  Document must be lifecycle-compliant (Owner, Class, Status, Version, Last Updated).
- **Spec reference:** `docs/specs/metrics_definitions.md#Portfolio Heat`, `docs/specs/frontend/pages/risk_dashboard.md`
- **Unblock criteria:** `docs/testing/risk_dashboard_scenarios.md` created and lifecycle-compliant; Director of Quality reviews and explicitly approves the scenario document; commit pushed to `exec/2026-03-04__release-v1.8/EPIC-01` in format `[EPIC-01][ST-04] <description>`; Director of Quality signs off on PR
- **Commit format required:** `[EPIC-01][ST-04] <description>` pushed to `exec/2026-03-04__release-v1.8/EPIC-01`
- **Status:** Pending

---

## DEL-20260305-04

- **ST Item:** ST-05 — Golden Output Regression Baseline
- **EPIC:** EPIC-02
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering (implementation); QA & Testing Owner (coverage review)
- **GitHub Issue:** #21
- **Branch:** exec/2026-03-04__release-v1.8/EPIC-02
- **Delegated at:** 2026-03-05T01:00:00Z
- **What is needed:** Create `tests/golden_outputs.json` with golden test cases for stop-loss calculation and position sizing calculation. Golden values must be independently derived from `strategy_rules.md` canonical spec — not reverse-engineered from the current implementation. Precision tolerance: ≥ 4 decimal places for share counts, 2 for prices; document in the JSON file. Add a CI step to the workflow (new workflow or extension of `validate-analytics.yml`) that asserts all golden outputs match on every PR; build must fail on any numeric deviation. Director of Quality must confirm the golden set covers all stop and sizing calculation paths, and that the CI step fails correctly on a known-bad input.
- **Spec reference:** `claude/strategy/strategy_rules.md` (canonical stop-loss and position sizing formulas)
- **Unblock criteria:** `tests/golden_outputs.json` exists with spec-derived values; CI step added and confirmed to fail on known-bad input; Director of Quality confirms coverage; commit pushed to `exec/2026-03-04__release-v1.8/EPIC-02` in format `[EPIC-02][ST-05] <description>`
- **Commit format required:** `[EPIC-02][ST-05] <description>` pushed to `exec/2026-03-04__release-v1.8/EPIC-02`
- **Status:** Pending

---

## DEL-20260305-05

- **ST Item:** ST-06 — Backtest vs Live Stop Reconciliation
- **EPIC:** EPIC-02
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering
- **GitHub Issue:** #22
- **Branch:** exec/2026-03-04__release-v1.8/EPIC-02
- **Delegated at:** 2026-03-05T01:00:00Z
- **What is needed:** After ST-05 is complete, add an automated CI check comparing backtest stop calculations vs live system stop calculations for all golden inputs from `tests/golden_outputs.json`. Any divergence between backtest and live logic must fail the check. Integrate into CI pipeline (same run as or adjacent to the golden output check from ST-05). Confirm the check catches a synthetically introduced divergence. Director of Quality must confirm CI integration.
  **Note:** This item is blocked on ST-05 being complete first.
- **Spec reference:** `tests/golden_outputs.json` (from ST-05); backtest calculation code and live calculation code in backend
- **Unblock criteria:** ST-05 complete; CI reconciliation check exists; confirmed to fail on synthetic divergence; Director of Quality confirms; commit in format `[EPIC-02][ST-06] <description>`
- **Commit format required:** `[EPIC-02][ST-06] <description>` pushed to `exec/2026-03-04__release-v1.8/EPIC-02`
- **Status:** Pending (blocked on ST-05)

---

## DEL-20260305-06

- **ST Item:** ST-07 — Dependency Vulnerability Scanning
- **EPIC:** EPIC-02
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering
- **GitHub Issue:** #23
- **Branch:** exec/2026-03-04__release-v1.8/EPIC-02
- **Delegated at:** 2026-03-05T01:00:00Z
- **What is needed:** Add a CI step scanning Python dependencies for known CVEs on every PR. Select and document the tool (e.g. `pip-audit` or `safety`) in the workflow file. Document the severity threshold: high/critical CVEs block merge (or produce a mandatory review comment — document which). Cybersecurity & Trust Lead must acknowledge the approach and severity threshold. Director of Quality must confirm CI integration. If safe to do so in the CI environment, test with a known-vulnerable dependency version to confirm the scan output format is correct.
- **Spec reference:** (no canonical spec for CI tooling — approach to be documented in workflow file)
- **Unblock criteria:** CI step exists in workflow; tool documented; severity threshold documented; Cybersecurity & Trust Lead acknowledges; Director of Quality confirms; commit in format `[EPIC-02][ST-07] <description>`
- **Commit format required:** `[EPIC-02][ST-07] <description>` pushed to `exec/2026-03-04__release-v1.8/EPIC-02`
- **Status:** Pending

---

## DEL-20260305-07

- **ST Item:** ST-08 — Automated OpenAPI Drift Detection
- **EPIC:** EPIC-02
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering
- **GitHub Issue:** #24
- **Branch:** exec/2026-03-04__release-v1.8/EPIC-02
- **Delegated at:** 2026-03-05T01:00:00Z
- **What is needed:** Add a CI step that detects drift between `docs/reference/openapi.yaml` and the canonical markdown API contract files in `docs/specs/api_contracts/`. Document the approach in the workflow file (generation vs diff — choice to be made and documented during implementation). Merge must be blocked if drift is detected. This item should ship alongside or after ST-10 (openapi.yaml update) so that the check passes on a clean post-ST-10 state. Confirm the check fails when a synthetic drift is introduced. Director of Quality must confirm CI integration.
  **Note:** ST-10 (openapi.yaml update to v1.9.0) is complete on EPIC-03 branch. Once EPIC-03 is merged to main, this ST-08 check must pass on the updated state.
- **Spec reference:** `docs/reference/openapi.yaml` (updated to v1.9.0 by ST-10)
- **Unblock criteria:** ST-10 merged to main; CI drift check exists and passes on post-ST-10 openapi.yaml; confirmed to fail on synthetic drift; Director of Quality confirms; commit in format `[EPIC-02][ST-08] <description>`
- **Commit format required:** `[EPIC-02][ST-08] <description>` pushed to `exec/2026-03-04__release-v1.8/EPIC-02`
- **Status:** Pending (coordinate with ST-10 merge)

---

## DEL-20260305-01 UPDATE — 2026-03-05T02:00:00Z

Status correction (append-only): DEL-20260305-01 (ST-02) is now **Unblocked/Complete**. Head of Engineering pushed commit `6b1bee9` to `exec/2026-03-04__release-v1.8/EPIC-01` adding `portfolio_heat_percent` and `position_risks[]` to `GET /portfolio`. Formula verified against `metrics_definitions.md §Portfolio Heat`. Issue #18 closed. ST-02 marked `done` in execution_state.json. **Updated status: Complete.**

---

## DEL-20260305-02 UPDATE — 2026-03-05T02:15:00Z

**GOVERNANCE BREACH FINDING (append-only):** ST-03 implementation was committed directly to `main` (commits `0d319b4`–`7b08fa7`, 2026-03-05 10:10–11:05 UTC) bypassing the EPIC-01 branch and `[EPIC-01][ST-03]` commit format. All five Risk Dashboard components are present and largely spec-compliant. Two deviations identified: DEV-ST03-01 (P2 entity fallback masks error states) and DEV-ST03-02 (P3 GracePeriodPanel error vs empty state indistinguishable). ESC-EXEC-20260305-02 raised for Product Owner acknowledgement. ST-03 set to `blocked_decision` pending PO acceptance. **Updated status: Blocked (decision) — ESC-EXEC-20260305-02.**

---

## DEL-20260305-02 UPDATE — 2026-03-05T02:00:00Z

Status update (append-only): ST-02 (EPIC-01/EPIC-01 dependency for ST-03) is now complete. **The first unblock criterion for ST-03 is met.** The Base44 prompt draft is already recorded in DEL-20260305-02 above. The Base44 Frontend Prompt Owner may now proceed with code generation using that prompt. Note: the prospective heat endpoint approach should be confirmed with Head of Engineering before wiring the Prospective Heat Indicator section (ST-02 confirms `portfolio_heat_percent` exists; the prospective endpoint approach for new-position simulation was not explicitly resolved in the ST-02 commit — confirm before building that panel). **Updated status: In Progress — ST-02 unblocked; awaiting Base44 implementation and commit.**
