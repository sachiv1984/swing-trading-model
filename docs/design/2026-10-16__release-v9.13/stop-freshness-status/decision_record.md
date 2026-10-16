**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-16__release-v9.13
**Story:** ST-10 (EPIC-02, BLG-SPEC-188)

# Decision Record — Stop Freshness Panel on System Status

## 1. Problem

v9.9 recorded when each stop was last recalculated (`positions.stop_calculated_at`, DS-22). No view reports how stale open-position stops are, so §7.1's "recalculated daily" is not visible in operation. ST-10 defines the metric in `metrics_definitions.md` and shows it on System Status.

## 2. Decision

### 2.1 Placement

A new **Stop Freshness** panel on System Status, directly after Component Health Checks and before Endpoint Tests. It is a single full-width card. It is not one of the per-component health cards, because it is a data metric and not a service status.

### 2.2 Content

| Element | Display | `data-testid` |
|---------|---------|---------------|
| Heading | "Stop Freshness" | — |
| Median age | "Median stop age" + value | `stop-freshness-median` |
| Maximum age | "Oldest stop" + value + " · {TICKER}" | `stop-freshness-max` |
| Coverage | "{k} of {n} open positions" — `k` counts positions with a `stop_calculated_at` | `stop-freshness-coverage` |
| Never recalculated | "{m} never recalculated", shown only when `m > 0` | `stop-freshness-never` |
| As-of | "As of {local time}" (muted) | — |

- **Age format:** hours with one decimal below 48 h ("18.4 h"). Above that, days and hours ("3 d 6 h"). The `title` attribute holds the exact timestamp of the oldest stop.
- Positions with a NULL `stop_calculated_at` are excluded from the median and the maximum, and counted under "never recalculated". `metrics_definitions.md` (ST-10 AC 1) must state the same exclusion.
- **Neutral display.** No status colour or threshold this release. The metric definition sets no alert threshold, and a weekend gap would otherwise read as a false warning. A threshold, if wanted, is a separate item.

### 2.3 States

| State | Display |
|-------|---------|
| No open positions | "No open positions." (muted) |
| Source unavailable | "Stop freshness unavailable." (muted, `data-testid="stop-freshness-unavailable"`). The rest of the page is unaffected. |
| Loading | Single-line `Skeleton` |

### 2.4 Tokens (light and dark)

The card uses the `design_system.md` §Light-Theme Colour Tokens pairs: `bg-white dark:bg-slate-800/50 border-slate-200 dark:border-slate-700/50`. Values are `text-slate-900 dark:text-white`, and labels are `text-slate-600 dark:text-slate-400`. The rest of System Status keeps its current dark-only classes. Bringing those into line is not in this story.

## 3. §13 Compliance

Display only. Reading the age changes no stop.

## 4. Frontend Spec Impact

`system_status.md` v1.2 → v1.3: new §Stop Freshness Panel.

## 5. Obligations for Sprint Execution

- The figures must come from the backend (median, max, ticker, `k`, `n`, `m`, as-of), not be computed from `GET /positions` in the browser. Then the displayed value and the manual check (AC 2) share one source. A new route triggers RISK-04's chain: `##` contract heading, `openapi.yaml`, `routers/test.py`, the `SystemStatus.js` fallback count and `SC-SS-01b`. An added field on an existing route needs its contract and `openapi.yaml` updated in the same commit.

## 6. Testability (CLAUDE.md §2)

- Playwright: with mocked figures, the four values render as formatted. With the source mocked to fail, `stop-freshness-unavailable` shows and the page still renders.
- AC 2's manual check is recorded in the QA evidence with the SQL used and the displayed value.

## 7. Approval

Head of UX & Design: confirmed, 2026-10-16.
Product Owner: confirmed, 2026-10-16.
