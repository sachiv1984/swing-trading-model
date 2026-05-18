**Owner:** QA & Testing Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.2
**Last Updated:** 2026-05-18
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Derived from:** `docs/specs/frontend/pages/signals.md` v0.1; `docs/specs/api_contracts/signal_endpoints.md` v1.1
**Sprint:** 2026-03-18__release-v2.1 — ST-18 (closes TEST-GAP-SIG-01); 2026-04-17__release-v2.8 — ST-03

---

# Acceptance Test Scenarios — Signals Page

---

## 1. Scope

These scenarios verify Signals page behaviour against the canonical specification. They cover: control defaults and interaction, debounce behaviour, invalid input handling, and empty state rendering. Signal score calculation and backend signal generation logic are out of scope — those are covered by backend unit tests.

---

## 2. Canonical Spec References

| Component | Spec location |
|-----------|--------------|
| Top N control | `docs/specs/frontend/pages/signals.md §Controls/Top N` |
| Lookback (days) control | `docs/specs/frontend/pages/signals.md §Controls/Lookback (days)` |
| Control behaviour on change | `docs/specs/frontend/pages/signals.md §Controls/Control Behaviour on Change` |
| Empty state | `docs/specs/frontend/pages/signals.md §Empty State` |
| API contract | `docs/specs/api_contracts/signal_endpoints.md §GET /signals` |

---

## 3. Scenarios

---

### SC-SIG-01 — Controls render with correct defaults and fire correctly on change

**Component:** Signals page controls (Top N, Lookback)
**API:** `GET /signals?top_n={n}&lookback_days={d}`
**Priority:** P2

#### Preconditions

- User is authenticated and has at least one signal available in the backend.
- Browser dev tools Network tab is open to observe API calls.
- Page is freshly loaded (no prior state).

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Navigate to the Signals page. | Page loads. Top N control shows default value `5`. Lookback control shows default value `252`. A `GET /signals?top_n=5&lookback_days=252` request is visible in the Network tab. Signals table renders with results. |
| 2 | Change the Top N control value to `10`. Do not wait. | No API call fires immediately. A loading indicator appears (or the prior result remains) during the debounce window. |
| 3 | Wait 500ms after the last keystroke. | A `GET /signals?top_n=10&lookback_days=252` request fires. The signals table updates with the new response. |
| 4 | Change the Lookback control value to `126`. Wait 500ms. | A `GET /signals?top_n=10&lookback_days=126` request fires. The signals table updates with the new response. |
| 5 | Rapidly change Top N to `3`, then to `7` within 500ms. | Only one API call fires (`top_n=7`) after the 500ms debounce from the last change. The intermediate value (`3`) does not generate a separate API call. |

#### Pass criteria

- On page load, Top N defaults to `5` and Lookback defaults to `252`.
- On page load, `GET /signals?top_n=5&lookback_days=252` fires exactly once.
- Value changes trigger a new API call with updated parameters after exactly 500ms debounce.
- Rapid successive changes produce only one API call (the final value after the debounce window).
- Both controls remain interactive during an in-flight request.

---

### SC-SIG-02 — Invalid input resets to default; no API call fired

**Component:** Signals page controls (Top N, Lookback)
**API:** `GET /signals` (must NOT fire on invalid input)
**Priority:** P2

#### Preconditions

- Signals page is loaded with default values (top_n=5, lookback_days=252).

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Clear the Top N field and enter `0`. Wait 500ms. | The control resets to the default value `5`. No API call fires for `top_n=0`. |
| 2 | Clear the Top N field and enter `-3`. Wait 500ms. | The control resets to `5`. No API call fires for `top_n=-3`. |
| 3 | Clear the Top N field and enter `abc`. Wait 500ms. | The control resets to `5`. No API call fires for the non-integer value. |
| 4 | Clear the Lookback field and enter `0`. Wait 500ms. | The control resets to `252`. No API call fires for `lookback_days=0`. |
| 5 | Clear the Lookback field and enter `-10`. Wait 500ms. | The control resets to `252`. No API call fires for `lookback_days=-10`. |
| 6 | Enter a valid value in Top N (`8`) after all resets. Wait 500ms. | A `GET /signals?top_n=8&lookback_days=252` fires correctly. |

#### Pass criteria

- Non-positive or non-integer values in either control reset the field to its default.
- No API call is fired for invalid values.
- Valid input after a reset fires the API correctly with the current valid values of both controls.

---

### SC-SIG-03 — Empty state renders correctly when API returns no signals

**Component:** Signals page table and empty state
**API:** `GET /signals` returning empty array `[]`
**Priority:** P3

#### Preconditions

- Use a test environment or staging state where `GET /signals` returns `[]` (e.g., set top_n=1 and lookback_days=1 to a period with no signals, or use a portfolio with no generated signals).

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Load the Signals page with parameters that produce an empty signal list. | The signals table area is replaced by the empty state message: **"No signals found for the selected parameters."** No table rows or headers are visible. |
| 2 | Observe the Top N and Lookback controls. | Both controls remain visible, active, and interactive — they are not hidden or disabled in the empty state. |
| 3 | Change Top N to a value likely to return results (e.g., `20`). Wait 500ms. | A new API call fires. If signals are available, the table renders with results and the empty state message is removed. |

#### Pass criteria

- Empty array response renders the message: `"No signals found for the selected parameters."` verbatim per spec.
- No table is rendered in the empty state (no empty rows, no headers without data).
- Controls remain active and functional in the empty state.
- Transitioning from empty state to populated state renders cleanly without requiring a page reload.

---

## 4. Scenarios — Add to Watchlist CTA (v3.7, BLG-FE-33)

*Canonical spec: `docs/specs/frontend/pages/signals.md v0.3 §Signal Card Actions`*
*Playwright file: `tests/e2e/signals-add-to-watchlist.spec.js`*

---

### SC-SIG-WL-01 — Add to Watchlist happy path

**Component:** Signal card — Add to Watchlist CTA
**API:** `POST /watchlist`, `PATCH /signals/{id}`
**Priority:** P1

#### Preconditions

- Signals page loaded with at least one signal in `status = 'new'`.
- `POST /watchlist` returns 201 (new entry created).

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Load Signals page with a new signal card. | Signal card shows **"Add to Watchlist"** as primary CTA and **"Dismiss"** as secondary. No "Add Position" button visible. |
| 2 | Click **"Add to Watchlist"**. | `POST /watchlist` called with `ticker`, `market`, `initial_stop_price` from signal. |
| 3 | POST /watchlist returns 201. | `PATCH /signals/{id} {"status": "watchlisted"}` called. |
| 4 | Observe signal card state after mutation. | Card shows **"Added to Watchlist"** label. **"View in Watchlist"** link visible (→ /Watchlist). No action buttons remain. |

#### Pass criteria

- "Add to Watchlist" button present on new signal cards; "Add Position" absent.
- `POST /watchlist` receives correct ticker, market, initial_stop_price.
- Card transitions to watchlisted state on success.
- "View in Watchlist" link visible and functional.

---

### SC-SIG-WL-02 — Duplicate add handling

**Component:** Signal card — duplicate watchlist entry
**API:** `POST /watchlist` (409), `PATCH /signals/{id}`
**Priority:** P1

#### Preconditions

- Signals page loaded with a new signal whose ticker is already on the watchlist.
- `POST /watchlist` returns 409.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Click **"Add to Watchlist"** on a signal card. | `POST /watchlist` called; returns 409. |
| 2 | Observe toast. | Toast "Already on your watchlist" shown. |
| 3 | Observe signal card state. | `PATCH /signals/{id} {"status": "watchlisted"}` still called. Card transitions to watchlisted state. |

#### Pass criteria

- 409 response shows toast "Already on your watchlist".
- Signal status still transitions to `watchlisted` despite 409.
- "View in Watchlist" link visible after 409.

---

### SC-SIG-WL-03 — No Add Position CTA on signal cards

**Component:** Signal card — CTA non-regression
**Priority:** P2

#### Pass criteria

- No "Add Position" button or text visible on any signal card (including new signal cards).

---

## 5. Scenarios — Supplementary Indicator Fields

*Canonical spec: `docs/specs/api_contracts/signal_endpoints.md v1.1 §POST /signals/generate`*

---

### SC-SIG-IND-01 — POST /signals/generate response includes all four supplementary fields per signal object

**Component:** Signals endpoint — supplementary indicator fields
**API:** `POST /signals/generate`
**Priority:** P1
**Canonical spec:** `signal_endpoints.md v1.1 §POST /signals/generate` — supplementary fields

#### Preconditions

- At least one trade position exists to generate a signal for.
- External data (Yahoo Finance / benchmark) is available for the relevant tickers.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Issue `POST /signals/generate` with valid parameters. | HTTP 200 response. |
| 2 | Inspect each signal object in the `signals` array. | Each signal object contains all four supplementary fields: `relative_strength_pct`, `week52_high_proximity_pct`, `avg_daily_volume_20d`, `price_vs_50d_ma`. |
| 3 | Verify `relative_strength_pct`. | Numeric value (or `null`). Represents stock momentum % minus benchmark momentum % over `lookback_days`. |
| 4 | Verify `week52_high_proximity_pct`. | Numeric value (or `null`). `(current_native_price − 52w_high) / 52w_high × 100`. Negative = below 52-week high. |
| 5 | Verify `avg_daily_volume_20d`. | Integer (or `null`). Average daily trading volume over last 20 trading days. |
| 6 | Verify `price_vs_50d_ma`. | Numeric value (or `null`). `(current_native_price − 50d_MA) / 50d_MA × 100`. |
| 7 | Verify supplementary fields do not affect `rank`. | Signal ordering/ranking is unchanged compared to a response without supplementary data — these fields are display-only. |

#### Pass criteria

- All four supplementary fields present on every signal object.
- All values are either a number or `null` — no missing keys, no errors.
- `rank` ordering is unaffected by supplementary field values.
- No 500 or error response raised.

---

### SC-SIG-IND-02 — relative_strength_pct is None (not an error) when benchmark data unavailable

**Component:** Signals endpoint — supplementary field null handling
**API:** `POST /signals/generate`
**Priority:** P1
**Canonical spec:** `signal_endpoints.md v1.1 §POST /signals/generate` — `relative_strength_pct` null behaviour

#### Preconditions

- At least one position exists for a ticker.
- Benchmark data (SPY or ^FTSE) is unavailable (simulate via test fixture or staging override, or use a test environment where benchmark data is disabled).

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Issue `POST /signals/generate` in an environment where benchmark data is unavailable. | HTTP 200 response (not 500 or 400). |
| 2 | Inspect `relative_strength_pct` on the affected signal. | `relative_strength_pct: null` — not an error, not omitted. |
| 3 | Verify other supplementary fields. | `week52_high_proximity_pct`, `avg_daily_volume_20d`, `price_vs_50d_ma` still present (may also be `null` if their data sources are unavailable). |
| 4 | Verify the `rank` field. | `rank` is still present and valid — benchmark data absence does not affect signal ranking. |

#### Pass criteria

- HTTP 200 returned when benchmark data unavailable.
- `relative_strength_pct` is `null` (not omitted, not an error object).
- Other fields and `rank` remain valid.
- No 500 raised for missing benchmark data.

---

## 6. Out of Scope

- Signal score calculation correctness — covered by backend unit tests.
- `PATCH /signals/{signal_id}` and `DELETE /signals/{signal_id}` — covered by backend integration tests.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.2 | 2026-05-18 | ST-02 (BLG-FE-33, v3.7): Added §4 Add to Watchlist CTA scenarios — SC-SIG-WL-01 (happy path), SC-SIG-WL-02 (duplicate 409), SC-SIG-WL-03 (no Add Position regression). Playwright: tests/e2e/signals-add-to-watchlist.spec.js. QA & Testing Owner. |
| 1.1 | 2026-04-18 | ST-03 (EPIC-02, v2.8): Added §4 Supplementary Indicator Field scenarios — SC-SIG-IND-01, SC-SIG-IND-02. Updated spec reference to signal_endpoints.md v1.1. Existing scenarios not modified. QA & Testing Owner. |
| 1.0 | 2026-03-18 | Initial version — SC-SIG-01 through SC-SIG-03 authored for ST-18. QA & Testing Owner. |
