**Owner:** QA & Testing Owner; Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.4 (EPIC-03, ST-12, BLG-QA-31)
**Gate inputs:** ST-09 (si02_background_job_adr.md), ST-10 (si02_fe_component_predesign.md), ST-11 (si02_fe_interaction_spec.md)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# SI-02 Playwright Scenario Pre-Design

## 1. Purpose

This document pre-designs the Playwright automated test scenario set for SI-02 (Behavioural Drift Detection). It is produced before the implementation sprint to:

1. Define which test scenarios must be covered by Playwright automation vs human staging
2. Identify staging-only evidence requirements (scenarios that cannot be verified in CI)
3. Give the implementation team a clear testing contract before coding begins
4. Satisfy the DoQ planning gate: observable AC must have designated test coverage before the implementation sprint planning seals (per CLAUDE.md §2 frontend testing gate)

Gate conditions verified:
- ST-09 (ADR-SI02-001 — background job architecture): ✅ done, commit 3fddb77b — cached synchronous pattern confirmed; no background infrastructure required at MVP
- ST-10 (si02_fe_component_predesign.md): ✅ done, commit 070a4663 — Option B (percentage deviation display) selected; 4 component states defined
- ST-11 (si02_fe_interaction_spec.md): ✅ done, commit 7eecefeb — interaction spec with DFT-01–DFT-13 test case specifications

---

## 2. Frontend Surfaces Under Test

SI-02 introduces a single frontend surface: the `DriftAnalysisPanel` component and its `DriftMetricCard` sub-components, rendered in the appropriate analytics or dashboard page.

From `si02_fe_component_predesign.md §4` and `si02_fe_interaction_spec.md §3`:

| Surface | Observable AC | Test approach |
|---------|--------------|---------------|
| Loading state | Four skeleton cards; "Behavioural Drift — Advisory" heading | Playwright (intercepted response delay) |
| Insufficient data state | Muted panel; trade_count in message | Playwright (mocked API response) |
| No drift state | Four metric cards; all green borders; positive message | Playwright (mocked API response) |
| Drift detected — approaching | Amber border on approaching card | Playwright (mocked API response) |
| Drift detected — breached | Red border; advisory note text | Playwright (mocked API response) |
| Error state | Error message; Retry button | Playwright (mocked API error) |
| Collapse/expand | Chevron collapse; compact indicator; expand restores | Playwright (user interaction) |
| Period filter change | Re-fetch triggered; loading re-entered | Playwright (user interaction + response intercept) |
| Tooltip interactions | Metric label, deviation, Advisory badge tooltips | Playwright (hover/focus) |
| Accessibility | ARIA roles, aria-expanded on chevron | Playwright (attribute check) |
| localStorage persistence | Collapse state survives page reload | Playwright (reload + localStorage) |
| Live drift data (real API) | Actual drift metrics from real trade history | Staging-only — see §4 |

---

## 3. Draft Playwright Scenario Set

Scenario IDs from `si02_fe_interaction_spec.md §10` (DFT-01 through DFT-13). Each scenario is expanded here with mock setup and assertion detail.

### Scenario DFT-01 — Loading State

**Observable AC:** Four skeleton cards visible; "Behavioural Drift — Advisory" heading visible while fetch is in-flight.

**Mock setup:** Intercept `GET /analytics/behavioural-drift` and hold the response (delay or never resolve within the test window).

**Assertions:**
- `DriftAnalysisPanel` heading: text matches `/Behavioural Drift.*Advisory/i`
- Four skeleton card elements visible (data-testid or role-based selector)
- No metric values or deviation percentages visible (skeleton only)
- No error message visible

**Coverage type:** Playwright ✅

---

### Scenario DFT-02 — Insufficient Data State

**Observable AC:** Single muted panel; trade_count shown in message matches API response value.

**Mock setup:** Intercept `GET /analytics/behavioural-drift` and return:
```json
{
  "status": "insufficient_data",
  "data_sufficient": false,
  "trade_count": 7,
  "minimum_required": 20,
  "metrics": [],
  "computed_at": "2026-05-29T06:00:00Z"
}
```

**Assertions:**
- Single panel visible (no metric cards)
- Message text includes "7" (trade_count from API) and "20" (minimum_required)
- Advisory heading still visible
- No metric card grid rendered

**Coverage type:** Playwright ✅

---

### Scenario DFT-03 — No Drift Detected

**Observable AC:** Four metric cards rendered; all green borders; positive summary message visible.

**Mock setup:** Intercept and return all metrics with `status: "ok"`:
```json
{
  "status": "no_drift",
  "data_sufficient": true,
  "trade_count": 25,
  "metrics": [
    {"metric_id": "win_rate_by_setup_type", "label": "Win Rate by Setup Type", "status": "ok", "value": 0.62, "threshold_warn": 0.10, "threshold_breach": 0.20, "deviation_pct": 0.03, "advisory_note": null, "period_days": 90},
    {"metric_id": "win_rate_by_regime", "label": "Win Rate by Regime", "status": "ok", "value": 0.58, "threshold_warn": 0.10, "threshold_breach": 0.20, "deviation_pct": 0.05, "advisory_note": null, "period_days": 90},
    {"metric_id": "entry_timing", "label": "Entry Timing", "status": "ok", "value": 2.1, "threshold_warn": 0.20, "threshold_breach": 0.40, "deviation_pct": 0.08, "advisory_note": null, "period_days": 90},
    {"metric_id": "sizing_adherence", "label": "Sizing Adherence", "status": "ok", "value": 0.021, "threshold_warn": 0.10, "threshold_breach": 0.25, "deviation_pct": 0.04, "advisory_note": null, "period_days": 90}
  ],
  "computed_at": "2026-05-29T06:00:00Z"
}
```

**Assertions:**
- Four `DriftMetricCard` elements rendered
- All cards have green border / "ok" visual treatment
- "All metrics within threshold" summary text visible
- No amber or red accent visible

**Coverage type:** Playwright ✅

---

### Scenario DFT-04 — Drift Detected (Approaching)

**Observable AC:** Amber border on approaching metric card; no advisory note visible for approaching (advisory_note is null).

**Mock setup:** Return with `status: "drift_detected"`, one metric at `approaching`:
```json
{
  "status": "drift_detected",
  "data_sufficient": true,
  "trade_count": 28,
  "metrics": [
    {"metric_id": "win_rate_by_setup_type", "label": "Win Rate by Setup Type", "status": "approaching", "deviation_pct": 0.12, "advisory_note": null, "period_days": 90},
    {"metric_id": "win_rate_by_regime", "label": "Win Rate by Regime", "status": "ok", "deviation_pct": 0.05, "advisory_note": null, "period_days": 90},
    {"metric_id": "entry_timing", "label": "Entry Timing", "status": "ok", "deviation_pct": 0.03, "advisory_note": null, "period_days": 90},
    {"metric_id": "sizing_adherence", "label": "Sizing Adherence", "status": "ok", "deviation_pct": 0.02, "advisory_note": null, "period_days": 90}
  ],
  "computed_at": "2026-05-29T06:00:00Z"
}
```

**Assertions:**
- Win Rate by Setup Type card has amber border / approaching visual treatment
- Other three cards have green border
- No advisory note text rendered (advisory_note is null)
- `! 1 metrics drifting` compact indicator visible if panel is collapsed

**Coverage type:** Playwright ✅

---

### Scenario DFT-05 — Drift Detected (Breached with Advisory Note)

**Observable AC:** Red border on breached metric card; advisory note text visible.

**Mock setup:** Return with one metric at `breached` and `advisory_note` populated:
```json
{
  "status": "drift_detected",
  "metrics": [
    {"metric_id": "sizing_adherence", "label": "Sizing Adherence", "status": "breached", "deviation_pct": 0.32, "advisory_note": "Position size has exceeded plan by >25% in 3 of last 5 trades. Review risk parameters.", "period_days": 90},
    {"metric_id": "win_rate_by_setup_type", "label": "Win Rate by Setup Type", "status": "ok", "deviation_pct": 0.04, "advisory_note": null, "period_days": 90},
    {"metric_id": "win_rate_by_regime", "label": "Win Rate by Regime", "status": "ok", "deviation_pct": 0.03, "advisory_note": null, "period_days": 90},
    {"metric_id": "entry_timing", "label": "Entry Timing", "status": "ok", "deviation_pct": 0.06, "advisory_note": null, "period_days": 90}
  ]
}
```

**Assertions:**
- Sizing Adherence card has red border / breached visual treatment
- Advisory note text "Position size has exceeded plan…" is visible in the card
- Other cards have green treatment
- Heading accent matches highest severity (red)

**Coverage type:** Playwright ✅

---

### Scenario DFT-06 — Error State

**Observable AC:** Error message visible; Retry button present and focusable.

**Mock setup:** Intercept and return HTTP 500 or network error for `GET /analytics/behavioural-drift`.

**Assertions:**
- Error message text visible (e.g. "Unable to load drift analysis")
- Retry button present and focusable (tab-reachable)
- Retry button click triggers a new fetch (response intercepted again)
- No metric cards rendered

**Coverage type:** Playwright ✅

---

### Scenario DFT-07 — Collapse and Expand

**Observable AC:** Chevron click collapses panel; compact heading indicator visible; expand restores cards.

**Mock setup:** Use the DFT-03 (no drift) or DFT-05 (breached) mock. Allow response to resolve so the panel is in its rendered state.

**Assertions (collapse):**
- Click chevron element
- Metric cards are hidden (not in DOM or `display: none`)
- Compact indicator visible with appropriate text
- Chevron `aria-expanded` is `"false"`

**Assertions (expand):**
- Click chevron again
- Metric cards are visible
- Chevron `aria-expanded` is `"true"`

**Coverage type:** Playwright ✅

---

### Scenario DFT-08 — Period Filter Change

**Observable AC:** Re-fetch triggered on period prop change; loading state re-entered.

**Mock setup:** First response is DFT-03 mock. After period selector interaction, intercept the second request and hold it briefly to observe loading state.

**Assertions:**
- Initial state: no drift (DFT-03 cards visible)
- Change period selector to "last 30 days"
- Loading state re-entered (skeleton cards visible or loading indicator)
- New API request made with `?period=last_30_days` (or equivalent param)
- Second response resolves with updated data

**Coverage type:** Playwright ✅

---

### Scenario DFT-09 — Tooltip: Metric Label

**Observable AC:** Hover/focus on metric label shows description tooltip.

**Assertions:**
- Hover (or focus via keyboard Tab) on metric label element
- Tooltip element becomes visible with descriptive text
- Tooltip text matches the metric definition (e.g. "Win rate for trades entered under stated setup type")
- Tooltip hidden on mouseout/blur

**Coverage type:** Playwright ✅

---

### Scenario DFT-10 — Tooltip: Deviation Display

**Observable AC:** Hover/focus on deviation percentage line shows formula tooltip.

**Assertions:**
- Hover/focus on deviation percentage element
- Tooltip shows formula explanation (e.g. "|actual - expected| / expected")
- Tooltip hidden on mouseout/blur

**Coverage type:** Playwright ✅

---

### Scenario DFT-11 — Tooltip: Advisory Badge

**Observable AC:** Hover/focus on "Advisory" badge shows advisory-only disclaimer tooltip.

**Assertions:**
- Hover/focus on the "Advisory" badge in the panel heading
- Tooltip text confirms display-only nature (e.g. "This analysis is for review only. No automated action is triggered.")
- Tooltip hidden on mouseout/blur

**Coverage type:** Playwright ✅

---

### Scenario DFT-12 — Accessibility

**Observable AC:** Panel has `role="region"` with correct `aria-label`; chevron has `aria-expanded`.

**Assertions:**
- Panel container has `role="region"`
- `aria-label` on panel contains "Behavioural Drift" or equivalent
- Chevron button has `aria-expanded` attribute
- `aria-expanded` is `"true"` when panel is expanded, `"false"` when collapsed
- All interactive elements reachable via Tab key

**Coverage type:** Playwright ✅

---

### Scenario DFT-13 — localStorage Collapse Persistence

**Observable AC:** Collapse state persists across page reload.

**Mock setup:** DFT-03 or DFT-05 mock active. Collapse the panel (DFT-07 first assertion). Then reload the page.

**Assertions:**
- Before reload: collapse state in `localStorage` under `si02.driftPanel.collapsed = true`
- After page reload: panel loads in collapsed state (metric cards not visible, compact indicator visible)
- API fetch still occurs in background (drift data is loaded; only the display is collapsed)

**Coverage type:** Playwright ✅

---

## 4. Staging-Only Scenarios

The following scenarios require live drift data from real trade history and **cannot** be verified in CI with mocked responses. They are designated `[staging-only evidence]` per CLAUDE.md §2 and sprint_planning_prompt.md §7.

| Scenario | Surface | Why staging-only | Evidence required |
|----------|---------|-----------------|------------------|
| S-STG-01 | Live drift metrics with real trades | CI has no trade history; mocks cannot simulate real drift calculation correctness | Human staging sign-off: confirm API returns `status: "drift_detected"` with correct metric values for a real portfolio that has drift |
| S-STG-02 | Drift metric accuracy vs actual trades | Whether the backend correctly identifies win-rate drift requires real trade data matching the strategy baseline | Human staging: compare displayed percentages against manual calculation from trade export |
| S-STG-03 | Cache TTL behaviour (8h stale data) | Cannot test 8h cache expiry in CI | Human staging: verify that data refreshes after TTL or deploy-triggered cache reset |
| S-STG-04 | Insufficient data gate at PT-04 boundary | Requires a real portfolio at exactly 19 and then 20 trades | Human staging: verify `insufficient_data` → `drift_detected`/`no_drift` transition at 20 trades |

**Backlog items required:** Per CLAUDE.md §2, each staging-only AC without Playwright coverage must have a backlog item filed before the SI-02 implementation sprint PR opens. These items must be filed at SI-02 sprint planning seal:

| Staging scenario | Backlog item to file |
|-----------------|---------------------|
| S-STG-01 | BLG-QA-xx — Human staging sign-off for SI-02 live drift metrics (post-merge) |
| S-STG-02 | BLG-QA-xx — Human staging: drift metric accuracy vs manual trade calculation |
| S-STG-03 | BLG-QA-xx — Human staging: verify 8h cache TTL and deploy reset behaviour |
| S-STG-04 | BLG-QA-xx — Human staging: insufficient_data → active transition at PT-04 boundary |

---

## 5. Implementation Notes for SI-02 Sprint

1. **Mock response shape:** The `DriftMetricCard` tests (DFT-03 through DFT-08) use mocked API responses. Mocks must match the canonical API response shape from `si02_fe_component_predesign.md §6.1` exactly — nested fields must not be flattened (per CLAUDE.md §2 mock payload advisory).

2. **Test file location:** All DFT-xx scenarios should be implemented in a single spec file: `tests/e2e/si02-drift.spec.js` (or `.ts`).

3. **Selector approach:** All selectors must use `data-testid` attributes or ARIA roles — no CSS class selectors. The implementation team must add `data-testid="drift-panel"`, `data-testid="drift-metric-card"`, `data-testid="drift-chevron"` etc. in the same commit as the component.

4. **waitFor pattern:** Per CLAUDE.md §2 (execution_prompt.md §14), all page navigations must be followed by element-specific waits, not `waitForLoadState('networkidle')`. Use `await expect(page.locator('[data-testid="drift-panel"]')).toBeVisible()` after navigation.

5. **CI exclusion for staging-only scenarios:** S-STG-01 through S-STG-04 must not be included in the CI test suite. If they are authored, they must be tagged `@staging-only` and excluded via `--ignore-snapshots` or `testIgnore` in `playwright.config.js`.

---

## 6. Sign-Off

**Director of Quality confirmation:** Draft scenario set reviewed. All 13 DFT test cases are appropriate for the observable AC from `si02_fe_interaction_spec.md`. The 4 staging-only scenarios (S-STG-01 through S-STG-04) correctly identify scenarios that cannot be covered by CI mocks. Backlog items must be filed at SI-02 sprint planning seal before PR can open.

| Role | Status | Date |
|------|--------|------|
| QA & Testing Owner | Approved | 2026-05-29 |
| Director of Quality | Confirmed | 2026-05-29 |
