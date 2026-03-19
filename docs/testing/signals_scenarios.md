**Owner:** QA & Testing Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-03-18
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Derived from:** `docs/specs/frontend/pages/signals.md` v0.1; `docs/specs/api_contracts/signal_endpoints.md`
**Sprint:** 2026-03-18__release-v2.1 — ST-18 (closes TEST-GAP-SIG-01)

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

## 4. Out of Scope

- Signal score calculation correctness — covered by backend unit tests.
- `POST /signals/generate` — covered separately as part of EPIC-02/03 implementation testing.
- `PATCH /signals/{signal_id}` and `DELETE /signals/{signal_id}` — covered by backend integration tests.
