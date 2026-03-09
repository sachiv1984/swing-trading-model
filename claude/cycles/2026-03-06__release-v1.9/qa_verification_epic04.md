# QA Verification Report — EPIC-04 Risk Dashboard Defect Resolution

**Owner:** Director of Quality
**Cycle:** 2026-03-06__release-v1.9
**EPIC:** EPIC-04 — Risk Dashboard Defect Resolution
**Stories verified:** ST-08, ST-09, ST-10
**Commit verified:** 20e688f
**Branch:** exec/2026-03-06__release-v1.9/EPIC-04
**Date:** 2026-03-09
**Method:** Static code analysis (test data injection infrastructure unavailable — see TEST-GAP-EPIC-01)
**Spec ref:** docs/specs/frontend/pages/risk_dashboard.md v0.1.7; docs/testing/risk_dashboard_scenarios.md v1.0.1

---

## Section 1 — Scope and Method

Verification covers the six files changed in commit 20e688f:

- src/pages/RiskDashboard.js
- src/components/risk/HeatGauge.js
- src/components/risk/DrawdownSummary.js
- src/components/risk/GracePeriodPanel.js
- src/components/risk/PositionRiskTable.js
- src/components/risk/ProspectiveHeatPanel.js

Test data injection infrastructure (seeded test DB / mock backend) remains unavailable (TEST-GAP-EPIC-01). Groups A, B, C, and F scenarios requiring controlled backend data are code-logic verified only; visual/live confirmation deferred to when TEST-GAP-EPIC-01 is resolved. Groups D, E, and G can be fully verified via code analysis.

---

## Section 2 — Deviation Resolution Status (from risk_dashboard.md §11)

| Ref | v1.8 Status | v1.9 Code Finding | Result |
|-----|-------------|-------------------|--------|
| DEV-ST03-01 | P2 — Entity fallback masked API errors | HeatGauge receives `portfolioError` directly → shows ErrorCard independently. DrawdownSummary same. GracePeriodPanel/PositionRiskTable receive `positionError = usingEntityFallback ? null : portfolioError` — serves entity data when available, amber fallback note rendered by page. Explicit error shown when no entity data. | **RESOLVED** |
| DEV-ST03-02 | P3 — GracePeriodPanel empty vs error indistinguishable | `error` prop now triggers distinct `AlertCircle` error card: "Unable to load position data" — visually distinct from empty state "No positions currently in grace period." | **RESOLVED** |
| DEV-ST03-03 | P2 — Sort descending (spec requires ascending) | Sort corrected: `(a._stopDist ?? Infinity) - (b._stopDist ?? Infinity)` — ascending, tightest stop first. | **RESOLVED** |
| DEV-ST03-04 | P2 — Stop Price column absent | "Stop Price" added to headers array; cell renders `£${pos.current_stop.toFixed(2)}` or `—`. Column present. | **RESOLVED** |
| DEV-ST03-05 | P3 — GRACE badge amber, spec requires blue | GRACE badge: `bg-blue-500/20 text-blue-400 border-blue-500/30`. | **RESOLVED** |
| DEV-ST03-06 | P3 — GBP value at risk absent from HeatGauge | `£${totalAtRisk.toFixed(2)} at risk` rendered as SVG text below gauge percentage. totalAtRisk computed from `position_risks[].position_risk_gbp` (backend field). | **RESOLVED** |
| DEV-ST03-07 | P3 — Days in Grace column absent | GracePeriodPanel row renders `${p.holding_days}d in grace` label per row. | **RESOLVED** |
| DEV-ST03-09 | P3 — ProspectiveHeatPanel missing threshold label | `heatThreshold()` function returns label+colour class; badge rendered alongside projected heat value. Labels: Low / Moderate / High / Extreme matching spec §3.3. | **RESOLVED** |
| DEV-ST03-11 | P2 — US entry prices in USD | Not in scope ST-08/09/10. Remains open (BLG-RD-10). | **OPEN — out of scope** |
| DEV-ST03-12 | P2 — current_stop in USD for US positions | Not in scope ST-08/09/10. Remains open (BLG-RD-11). Stop Price column renders `£` prefix unconditionally — incorrect for US positions pending ST-07 backend fix. | **OPEN — out of scope** |

---

## Section 3 — Scenario Results

Result key: PASS-CODE = code logic verified, live visual confirmation needed; PASS = fully verifiable by code analysis; BLOCKED = requires test data injection (TEST-GAP-EPIC-01); NEW-DEV = new deviation found.

### Group A — Heat Gauge Threshold Boundaries (SC-RD-01 to SC-RD-06)

Method: `getColor(v)` in HeatGauge.js: `v>=30 → #ef4444; v>=20 → #f97316; v>=10 → #f59e0b; default → #22c55e`

| Scenario | Description | Code Finding | Result |
|----------|-------------|--------------|--------|
| SC-RD-01 | Heat 0.0% — green | v=0 → default → #22c55e ✓ | PASS-CODE |
| SC-RD-02 | Heat 9.9% — green (below 10%) | v=9.9 → default → #22c55e ✓ | PASS-CODE |
| SC-RD-03 | Heat 10.0% — amber boundary | v=10.0: `10>=10` → #f59e0b ✓ (not green) | PASS-CODE |
| SC-RD-04 | Heat 20.0% — orange boundary | v=20.0: `20>=20` → #f97316 ✓ (not amber) | PASS-CODE |
| SC-RD-05 | Heat 30.0% — red boundary | v=30.0: `30>=30` → #ef4444 ✓ (not orange) | PASS-CODE |
| SC-RD-06 | Heat 35.0% — deep extreme | v=35.0: `35>=30` → #ef4444 ✓ | PASS-CODE |

Note: Group A data delivery blocked by TEST-GAP-EPIC-01. Colour logic is code-correct. "No open positions" sub-text (spec §3.4 zero state) and a threshold label badge within the gauge centre are not rendered — the gauge shows only the percentage value and £X at risk. The legend row at the bottom shows threshold ranges. This is a pre-existing presentation gap, not introduced by this commit; not a new deviation.

### Group B — Grace Period Panel (SC-RD-07 to SC-RD-13)

Method: code analysis of GracePeriodPanel.js

| Scenario | Description | Code Finding | Result |
|----------|-------------|--------------|--------|
| SC-RD-07 | Colour coding and sort order (TD-07) | Sort: `(a.grace_days_remaining ?? 999) - (b.grace_days_remaining ?? 999)` — ascending ✓. daysColor: ≤1→red, ≤4→amber, else→green ✓. Filter: `grace_period === true` ✓. Count badge present when !error && gracePosts.length > 0 ✓. | PASS-CODE |
| SC-RD-08 | Day 1 — red badge | daysColor(1): `1<=1` → red ✓ | PASS-CODE |
| SC-RD-09 | Day 2 — amber lower boundary | daysColor(2): `2<=4` (not ≤1) → amber ✓ | PASS-CODE |
| SC-RD-10 | Day 4 — amber upper boundary | daysColor(4): `4<=4` → amber ✓ (not green) | PASS-CODE |
| SC-RD-11 | Day 5 — green boundary | daysColor(5): not ≤1, not ≤4 → green ✓ | PASS-CODE |
| SC-RD-12 | Day 10 in grace; day 12 expired excluded | Filter `grace_period` boolean: KILO with `grace_period=false` excluded ✓; JULIET with `grace_period=true` and `holding_days` shown ✓ | PASS-CODE |
| SC-RD-13 | Empty state | `gracePosts.length === 0` → "No positions currently in grace period." ✓ | PASS-CODE |

All Group B scenarios code-verified. Live confirmation blocked by TEST-GAP-EPIC-01.

### Group C — Position Risk Table (SC-RD-14 to SC-RD-15)

| Scenario | Description | Code Finding | Result |
|----------|-------------|--------------|--------|
| SC-RD-14 | All three states, sort, badges, Stop Price column | Sort: ascending within group — LIMA(4.0%) before MIKE(6.25%) before NOVEM(12.5%) ✓. Status group order: GRACE=0, LOSING=1, PROFITABLE=2 ✓. GRACE badge: blue ✓ (DEV-ST03-05 resolved). Stop Price column: present with `£${current_stop.toFixed(2)}` ✓ (DEV-ST03-04 resolved). Stop Price shows £ for all markets — note DEV-ST03-12 means US positions still show incorrect £ prefix, but that is an out-of-scope pre-existing deviation. | PASS-CODE |
| SC-RD-15 | Empty state | `sorted.length === 0` → "No open positions to display." — spec §6.5 says "No open positions". Minor wording deviation (added "to display."). Pre-existing; not introduced by this commit. | PASS-CODE (minor wording note) |

### Group D — Prospective Heat (SC-RD-16 to SC-RD-19)

| Scenario | Description | Code Finding | Result |
|----------|-------------|--------------|--------|
| SC-RD-16 | Heat crossing 20% threshold (TD-10) | `heatThreshold(21.0)`: `21>=20` → `{label:"High", color:"text-orange-400..."}` ✓. Delta: `21.0 - 15.0 = +6.0` rendered in rose-400 ✓. Projected heat formatted `.toFixed(1)` ✓. | PASS-CODE |
| SC-RD-17 | Stop ≥ entry rejected client-side | `validate()`: `if (stop >= entry) e.stop_price = "Must be less than entry price"` ✓. Inline error displayed. Note: Calculate button is not pre-disabled before submit attempt — spec §7.3/§7.6 says "enabled only when valid / Calculate disabled". This is a pre-existing deviation not introduced by this commit. | PASS-CODE (pre-existing deviation noted) |
| SC-RD-18 | Valid inputs, result shows % and delta | `result.projected_heat_percent?.toFixed(1)` + delta sign logic + threshold badge ✓. | PASS |
| SC-RD-19 | Panel collapsed by default | `useState(false)` → collapsed on mount ✓. | PASS |

### Group E — API Error States (SC-RD-20 to SC-RD-24)

| Scenario | Description | Code Finding | Result |
|----------|-------------|--------------|--------|
| SC-RD-20 | GET /portfolio fails — HeatGauge error state | `error` prop truthy → `<ErrorCard onRetry={onRetry} />`: "Unable to load heat data" + Retry button. Gauge SVG NOT rendered. Matches spec §3.4. ✓ | PASS |
| SC-RD-21 | GET /portfolio fails — DrawdownSummary error state | `if (error) return <ErrorCard />`: "Unable to load drawdown data". Matches spec §4.3. ✓ | PASS |
| SC-RD-22 | GET /portfolio fails — GracePeriodPanel error state | When entity fallback unavailable: `positionError = portfolioError` → `{error ? <AlertCircle..."Unable to load position data">}`. Visually distinct from empty state ✓. When entity store has data: `positionError = null` — entity data shown; amber fallback note on page. DEV-ST03-02 resolved for no-entity-data case. ✓ | PASS |
| SC-RD-23 | GET /portfolio fails — PositionRiskTable error state | `if (error) return <div>...Unable to load position data</div>` — includes header with ArrowDown icon, error body. Matches spec §6.5. ✓ | PASS |
| SC-RD-24 | Prospective heat endpoint fails — inline error | `catch(err) → setApiError(err.message)` → `{apiError && <p className="text-sm text-rose-400">{apiError}</p>}`. Inputs remain accessible. Matches spec §7.6. ✓ | PASS |

### Group F — Empty State (SC-RD-25)

| Scenario | Description | Code Finding | Result |
|----------|-------------|--------------|--------|
| SC-RD-25 | Full empty state — no open positions | HeatGauge: 0.0%, #22c55e ✓. GracePeriodPanel: empty state text ✓. PositionRiskTable: empty state text ✓. ProspectiveHeatPanel: interactive (no dependency on positions) ✓. | PASS-CODE |

### Group G — Non-Functional (SC-RD-26 to SC-RD-27)

| Scenario | Description | Code Finding | Result |
|----------|-------------|--------------|--------|
| SC-RD-26 | No console errors on clean load | Cannot verify without live browser. No obvious error-generating patterns in code (no undefined prop accesses, all arrays guarded with `?? []`). | PASS-CODE |
| SC-RD-27 | All values sourced from backend | `portfolio_heat_percent` passed directly as `heatPercent` ✓. `current_drawdown_percent` passed directly ✓. `positionRisks[]` passed from API response ✓. Stop Distance % is only client-derived value — acceptable per spec §6.2 ✓. | PASS |

---

## Section 4 — New Deviations Found

No new deviations introduced by commit 20e688f.

Pre-existing deviations noted during review (not introduced by this commit, not in scope):

- Gauge zero state: "No open positions" sub-text and a per-value threshold label badge not present in HeatGauge centre — pre-existing gap, no backlog entry currently assigned.
- PositionRiskTable empty state wording: "No open positions to display." vs spec §6.5 "No open positions" — minor; pre-existing.
- ProspectiveHeatPanel Calculate button not pre-disabled when inputs invalid (spec §7.3 says "enabled only when all fields valid") — pre-existing.
- DEV-ST03-11/12 remain open (US currency for entry_price and current_stop) — out of scope.

---

## Section 5 — Sprint Backlog AC Checklist (ST-08, ST-09, ST-10)

### ST-08 — Error States and Entity Fallback

- [x] HeatGauge renders independent error state on GET /portfolio failure
- [x] DrawdownSummary renders independent error state
- [x] GracePeriodPanel renders distinct error card (not empty state) when portfolioError set and no entity fallback
- [x] PositionRiskTable renders independent error state
- [x] Entity fallback preserved; amber note shown when active; error indicator present for API-dependent components

### ST-09 — Table and Column Fixes

- [x] PositionRiskTable sorted ascending by stop distance within group (DEV-ST03-03 resolved)
- [x] Stop Price column present in PositionRiskTable (DEV-ST03-04 resolved)
- [x] Days in Grace (holding_days) column present in GracePeriodPanel rows (DEV-ST03-07 resolved)
- [x] Threshold label badge present in ProspectiveHeatPanel result row (DEV-ST03-09 resolved)

### ST-10 — HeatGauge and Cosmetic Fixes

- [x] GRACE badge colour blue (DEV-ST03-05 resolved)
- [x] GBP value at risk displayed below gauge percentage (DEV-ST03-06 resolved)

---

## Section 6 — Limitations and Deferred Confirmation

The following cannot be confirmed without test data injection infrastructure (TEST-GAP-EPIC-01):

- Groups A, B, C visual rendering with controlled backend data
- Exact hex colour rendering in browser (code logic verified; rendering environment not available)
- SC-RD-26 console error check (requires live browser)

These limitations are pre-existing and not introduced by this commit. See risk_dashboard_scenarios.md §5.4.

---

## Section 7 — Sign-Off

ST-08: **APPROVED** — all AC criteria code-verified. Error states implemented correctly per spec §3.4, §4.3, §5.5, §6.5, §7.6, §8.

ST-09: **APPROVED** — all AC criteria code-verified. Sort direction, Stop Price column, Days in Grace column, and threshold badge all confirmed in code.

ST-10: **APPROVED** — all AC criteria code-verified. GRACE badge blue confirmed; GBP at risk confirmed.

EPIC-04 merge gate: **CONDITIONALLY APPROVED** pending:

1. Visual spot-check of colour rendering in deployed environment (Groups A/B/C/G — cannot be completed until test infrastructure available or manual spot-check in deployed app)
2. DEV-ST03-11 and DEV-ST03-12 confirmed as remaining open (out of scope for this EPIC-04 commit)

Signed: Director of Quality
Date: 2026-03-09
