**Owner:** QA & Testing Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-03-17
**Derived from:** `docs/specs/frontend/pages/analytics.md` v1.4; `docs/specs/api_contracts/analytics_endpoints.md` v1.9.0
**Sprint:** 2026-03-17__release-v2.0 — ST-20

---

# Acceptance Test Scenarios — Analytics Page

---

## 1. Scope

These scenarios verify Analytics page components against their canonical specifications. Scenarios are grouped by component. Each scenario references the canonical spec section that defines the expected behaviour.

---

## 2. Canonical Spec References

| Component | Spec location |
|-----------|--------------|
| CohortAnalysis panel | `docs/specs/frontend/pages/analytics.md §15` |
| `GET /analytics/cohort` API | `docs/specs/api_contracts/analytics_endpoints.md#GET /analytics/cohort` |
| `has_enough_data` gate | `docs/specs/frontend/pages/analytics.md §4 (Not Enough Data State)` |

---

## 3. Scenarios — CohortAnalysis Backend Integration Regression

### SC-CA-BACKEND-01 — Period toggle triggers API refetch and table updates

**Component:** CohortAnalysis panel (`analytics.md §15`)
**API:** `GET /analytics/cohort?period={month|quarter|year}`
**Priority:** P2

#### Preconditions

- Analytics page is loaded and in the Main Render State (`has_enough_data: true` on the primary `GET /analytics/metrics` call).
- The backend has ≥3 distinct cohort periods of closed trades available for at least two of the three period granularities (month, quarter, year) so that `has_enough_data: true` is returned for multiple period choices.
- QA tooling (browser dev tools Network tab) is open to observe API calls.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Navigate to the Analytics page. Observe the CohortAnalysis panel. | Panel loads with the default period (`month`). A `GET /analytics/cohort?period=month` request is visible in the Network tab. The cohort table renders with rows sorted descending by `period_label` (most recent first). |
| 2 | Click the **Quarter** toggle button. | A new `GET /analytics/cohort?period=quarter` request fires immediately. The previous `month` table clears (or shows a loading skeleton) while the request is in flight. |
| 3 | Observe the table once the `quarter` response loads. | Table re-renders with quarter cohort rows (`period_label` format: "Q1 2026"). Rows are sorted descending by period. Column values (`Trade Count`, `Win Rate`, `Avg R-Multiple`, `Total P&L`) match the fields in the `cohorts[]` array of the API response exactly — no client-side recalculation. |
| 4 | Click the **Year** toggle button. | A new `GET /analytics/cohort?period=year` request fires. Table re-renders with annual rows (`period_label` format: "2026"). Column values match the API response. |
| 5 | Click **Month** again. | A new `GET /analytics/cohort?period=month` request fires. Table returns to monthly view. |

#### Pass criteria

- Each period toggle fires exactly one new API call with the updated `period` parameter.
- No period toggle reuses a stale cached response without a network call (each toggle must produce a new request).
- Column values displayed in the table match the corresponding fields in the API response verbatim:

| Column header | API field | Format |
|---------------|-----------|--------|
| Period | `period_label` | string |
| Trade Count | `trade_count` | integer |
| Win Rate | `win_rate` | percentage, 1dp (e.g. "60.0%") |
| Avg R-Multiple | `avg_r_multiple` | 1dp with "R" suffix (e.g. "0.8R"); "—" or equivalent if `null` |
| Total P&L | `total_pnl` | signed GBP, 2dp; green if positive, red if negative (e.g. "+£320.50") |

#### Fail criteria

- Toggle does not fire a new API call.
- Table retains stale data after toggle (no re-render).
- Column value does not match the API response field (client-side derivation suspected).

---

### SC-CA-BACKEND-02 — `has_enough_data: false` shows insufficient history message

**Component:** CohortAnalysis panel (`analytics.md §15`)
**API:** `GET /analytics/cohort?period={period}`
**Priority:** P2

#### Preconditions

- A test environment or mock where `GET /analytics/cohort?period=year` returns `has_enough_data: false` (fewer than 3 distinct year cohorts) and `GET /analytics/cohort?period=month` returns `has_enough_data: true` (normal data).

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Load the Analytics page with `month` as the active period. | CohortAnalysis panel renders the cohort table normally. |
| 2 | Click the **Year** toggle button. | `GET /analytics/cohort?period=year` fires. Response contains `has_enough_data: false`. |
| 3 | Observe the CohortAnalysis panel. | The cohort table is replaced by the insufficient history message: **"Not enough closed trades to show year cohorts"**. No table rows render. |
| 4 | Click the **Month** toggle button. | `GET /analytics/cohort?period=month` fires. Response contains `has_enough_data: true`. Panel returns to normal table view. |

#### Pass criteria

- When `has_enough_data: false`, the panel shows the canonical message "Not enough closed trades to show [period] cohorts" (where `[period]` is replaced with the selected period word, e.g. "year cohorts").
- No table rows render when `has_enough_data: false`.
- The period toggle buttons remain active and usable when `has_enough_data: false`.
- Switching back to a period with `has_enough_data: true` restores the table.

#### Fail criteria

- Message text does not match the canonical string.
- Table rows render despite `has_enough_data: false`.
- Period toggle buttons are disabled or unresponsive when `has_enough_data: false`.

---

### SC-CA-BACKEND-03 — Column values match `GET /analytics/cohort` response fields

**Component:** CohortAnalysis panel (`analytics.md §15`)
**API:** `GET /analytics/cohort?period=month`
**Priority:** P1

**Purpose:** Regression guard — ensures the frontend renders API values verbatim and does not re-derive, round, or transform them independently.

#### Preconditions

- A controlled dataset with known cohort values (see TD-CA-01 below).
- Browser dev tools Network tab open. QA Lead captures the raw API response JSON.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Load the Analytics page with period = `month`. | `GET /analytics/cohort?period=month` fires. |
| 2 | Capture the raw `cohorts[]` array from the API response in the Network tab. | Response recorded. |
| 3 | For each row in the CohortAnalysis table, compare every column value against the corresponding `cohorts[]` entry field. | All values match exactly per the format rules in SC-CA-BACKEND-01 Pass criteria. |
| 4 | Pay specific attention to `avg_r_multiple: null` rows (no stop data). | The panel renders "—" (or equivalent null display) rather than "0.0R" or an error. |

#### Pass criteria

- Every displayed value traces directly to a field in the API response.
- `avg_r_multiple: null` renders as a null-safe placeholder (not "0.0R").
- `total_pnl` sign (positive/negative) and colour (green/red) are correct for all rows.
- Row order is descending by period (most recent first), matching `cohorts[]` array order.

#### Fail criteria

- Any displayed value differs from the API response field value (indicating client-side recalculation).
- `null` `avg_r_multiple` crashes the component or renders as a numeric value.

---

## 4. Test Data Definitions

### TD-CA-01 — Known cohort dataset (controlled regression)

Use this dataset for SC-CA-BACKEND-03. All values are definitive — the table must display them exactly.

`GET /analytics/cohort?period=month` response (`data.cohorts`):

| period_label | trade_count | win_rate | avg_r_multiple | total_pnl |
|--------------|-------------|----------|----------------|-----------|
| Mar 2026 | 5 | 60.0 | 0.8 | 320.50 |
| Feb 2026 | 3 | 33.3 | null | -85.00 |
| Jan 2026 | 8 | 75.0 | 1.2 | 940.00 |

Expected table display:

| Period | Trade Count | Win Rate | Avg R-Multiple | Total P&L |
|--------|-------------|----------|----------------|-----------|
| Mar 2026 | 5 | 60.0% | 0.8R | +£320.50 |
| Feb 2026 | 3 | 33.3% | — | −£85.00 |
| Jan 2026 | 8 | 75.0% | 1.2R | +£940.00 |

Notes:
- "Feb 2026" row has `avg_r_multiple: null` (no `initial_stop` data for those trades). Must render as "—" or equivalent, not "0.0R".
- "Feb 2026" `total_pnl` is negative — must render in red.
- Row order: most recent first (Mar → Feb → Jan).

---

## 5. Known Deviations Affecting Test Execution

None recorded at v1.0. Update this section if accepted deviations are identified during testing.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-17 | Initial version — SC-CA-BACKEND-01, SC-CA-BACKEND-02, SC-CA-BACKEND-03 authored for ST-20. QA & Testing Owner. |
