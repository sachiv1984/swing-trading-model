**Owner:** QA & Testing Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.1
**Last Updated:** 2026-05-18
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Derived from:** `docs/specs/frontend/pages/watchlist.md` v0.1; `docs/specs/api_contracts/watchlist_endpoints.md`; `docs/design/2026-05-18__release-v3.7/signal-context-panel/ux_spec.md`
**Sprint:** 2026-03-21__release-v2.2 — ST-10; 2026-05-18__release-v3.7 — ST-03

---

# Acceptance Test Scenarios — Watchlist

---

## 1. Scope

These scenarios verify the Watchlist feature against its canonical specification. They cover: adding a watchlist entry, editing an entry, removing an entry, the "Add to Position" flow (watchlist entry removed on successful position entry), duplicate ticker validation, and sort order behaviour with mixed signal statuses. SC-WATCH-06 satisfies the deferred AC-6 from ST-10 (v2.1) DoQ sign-off. §4 (v3.7) adds Signal Context panel presence/absence scenarios for the trade plan form (SC-TP-SIG-01 through SC-TP-SIG-04).

Out of scope: signal status computation (backend responsibility), price data accuracy, position entry form validation beyond the watchlist pre-population.

---

## 2. Canonical Spec References

| Component | Spec location |
|-----------|--------------|
| Watchlist page | `docs/specs/frontend/pages/watchlist.md §Watchlist Table` |
| Add ticker modal | `docs/specs/frontend/pages/watchlist.md §Add Ticker Modal` |
| Edit modal | `docs/specs/frontend/pages/watchlist.md §Edit Modal` |
| Add to Position | `docs/specs/frontend/pages/watchlist.md §Add to Position` |
| Sort order | `docs/specs/frontend/pages/watchlist.md §Watchlist Table` |
| API — list | `docs/specs/api_contracts/watchlist_endpoints.md §GET /watchlist` |
| API — create | `docs/specs/api_contracts/watchlist_endpoints.md §POST /watchlist` |
| API — update | `docs/specs/api_contracts/watchlist_endpoints.md §PATCH /watchlist/{id}` |
| API — delete | `docs/specs/api_contracts/watchlist_endpoints.md §DELETE /watchlist/{id}` |

---

## 3. Scenarios

---

### SC-WATCH-01 — Add a new watchlist entry

**Component:** Frontend — Add Ticker modal
**API:** `POST /watchlist`
**Priority:** P1

#### Preconditions

- User is on the Watchlist page (`/#/watchlist`).
- Watchlist is empty or contains at least one existing entry with a different ticker.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Click the **"+ Add Ticker"** button in the page header. | The Add Ticker modal opens. Ticker, Market (UK/US radio), Target Entry Price, Initial Stop Price, and Current Stop Price fields are visible. |
| 2 | Enter ticker symbol `MSFT`. Market radio defaults to or is set to `US`. | Ticker field shows `MSFT` (uppercase enforced on input). |
| 3 | Enter Target Entry Price `420.00`, Initial Stop Price `390.00`. Leave Current Stop blank. | Numeric fields accept the values. |
| 4 | Click **"Add to Watchlist"**. | `POST /watchlist` fires with body `{ticker: "MSFT", market: "US", target_entry_price: 420.00, initial_stop_price: 390.00}`. Modal closes. |
| 5 | Observe the watchlist table. | A new row appears for `MSFT` with Target Entry `$420.00`, Initial Stop `$390.00`, Current Stop `—`. |

#### Pass criteria

- Modal fields accept all required and optional values.
- `POST /watchlist` fires with correct field mapping.
- New row appears in the table after successful submission.

---

### SC-WATCH-02 — Edit an existing watchlist entry

**Component:** Frontend — Edit modal
**API:** `PATCH /watchlist/{id}`
**Priority:** P1

#### Preconditions

- At least one watchlist entry exists (e.g. `MSFT` from SC-WATCH-01 or pre-seeded).

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Click the ticker name `MSFT` in the watchlist table. | The Edit modal opens. Ticker field shows `MSFT` and is **read-only**. Price fields are pre-populated with current values. |
| 2 | Change Target Entry Price from `420.00` to `425.00`. | Field accepts the new value. |
| 3 | Click **"Save Changes"**. | `PATCH /watchlist/{id}` fires with body `{target_entry_price: 425.00}`. Modal closes. |
| 4 | Observe the row in the watchlist table. | `MSFT` row shows updated Target Entry `$425.00`. |

#### Pass criteria

- Ticker field is read-only in edit mode.
- Pre-populated values displayed correctly.
- PATCH fires with only changed fields.
- Table reflects updated values after save.

---

### SC-WATCH-03 — Delete a watchlist entry via the Remove flow

**Component:** Frontend — Edit modal remove confirmation
**API:** `DELETE /watchlist/{id}`
**Priority:** P1

#### Preconditions

- At least one watchlist entry exists.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Click the ticker name to open the Edit modal. | Edit modal opens. |
| 2 | Click **"Remove from Watchlist"** (destructive button, bottom of modal). | An inline confirmation prompt appears within the modal: `"Remove [TICKER] from your watchlist?"` with **"Remove"** and **"Cancel"** buttons. |
| 3 | Click **"Cancel"** on the confirmation. | Confirmation dismisses. Edit modal remains open. The watchlist entry is unchanged. |
| 4 | Click **"Remove from Watchlist"** again. | Confirmation prompt reappears. |
| 5 | Click **"Remove"** (destructive). | `DELETE /watchlist/{id}` fires. Modal closes. Row is removed from the table (with slide/fade animation ≤200ms). |

#### Pass criteria

- Confirmation prompt shown before destructive action.
- "Cancel" dismisses the prompt without deleting.
- Second confirmation → DELETE fires → row removed from table.

---

### SC-WATCH-04 — "Add to Position" removes entry from watchlist

**Component:** Frontend — Add to Position button; position entry integration
**API:** `DELETE /watchlist/{id}` (triggered on successful position entry)
**Priority:** P1

#### Preconditions

- At least one watchlist entry exists with Target Entry Price and Initial Stop Price populated.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Click the **"Add to Position"** button on a watchlist row (e.g. `MSFT`). | The position entry modal opens, pre-populated with: ticker `MSFT`, market `US`, entry price `425.00` (from target), initial stop `390.00`. |
| 2 | Complete and submit the position entry form. | `POST /positions` fires. Position entry modal closes. |
| 3 | Observe the watchlist table. | The `MSFT` row is removed from the watchlist (backend calls `DELETE /watchlist/{id}` as part of position creation). |

#### Pass criteria

- Position entry modal pre-populated from watchlist values.
- On successful position entry: watchlist entry removed automatically.
- Row disappears from the watchlist table without a manual refresh.

#### Partial execution note

- This scenario requires submitting a full position entry form. If position creation is blocked by missing fields (e.g. no FX rate), document the blocker in QA evidence and mark as **Conditional Pass** with a path to resolution.

---

### SC-WATCH-05 — Duplicate ticker shows inline error; 409 conflict handled

**Component:** Frontend — Add Ticker modal, duplicate validation
**API:** `POST /watchlist` (returns 409)
**Priority:** P2

#### Preconditions

- A watchlist entry for ticker `MSFT` already exists.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Click **"+ Add Ticker"**. | Add Ticker modal opens. |
| 2 | Enter ticker `MSFT` (matching an existing entry). Market: `US`. | Ticker field shows `MSFT`. |
| 3 | Click **"Add to Watchlist"**. | `POST /watchlist` fires and returns 409. |
| 4 | Observe the modal. | An inline error message appears below the ticker field: `"This ticker is already on your watchlist."` The modal remains open. |

#### Pass criteria

- 409 response is handled gracefully — no crash, no modal close.
- Inline error message matches the spec exactly: `"This ticker is already on your watchlist."`

---

### SC-WATCH-06 — Sort order: Active first, then Watch, then No Signal; alphabetical within group

**Component:** Frontend — Watchlist table default sort
**Priority:** P2
**Source requirement:** Deferred AC-6 from ST-10 (v2.1) DoQ sign-off — sort order with mixed `signal_status` values was not exercised in v2.1 due to test data limitations (all entries had `no_signal`).

#### Preconditions

- Watchlist contains at least one entry per signal status:
  - `active` (e.g. `AAPL`)
  - `watch` (e.g. `TSLA`)
  - `no_signal` (e.g. `GOOGL`)
- If staging data does not provide mixed signal statuses, use mock-layer interception (Playwright `page.route()`) to return a pre-seeded watchlist with all three status values.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Navigate to `/#/watchlist`. | Watchlist table loads. |
| 2 | Observe the row order. | Active entries appear first (green badge), then Watch (amber badge), then No Signal (grey badge). Within each group, rows are ordered alphabetically by ticker. |
| 3 | If multiple Active entries exist (e.g. `AAPL` and `AMZN`): | `AAPL` appears before `AMZN` within the Active group. |
| 4 | Observe the Entry Signal column badges. | `active` → green "Active" badge; `watch` → amber "Watch" badge; `no_signal` → grey "No Signal" badge. |

#### Pass criteria

- Sort order: Active → Watch → No Signal groups.
- Alphabetical within each group.
- Correct badge colour and label per signal_status value.

#### Resolution of deferred AC-6 (v2.1)

This scenario was deferred from v2.1 because all test watchlist entries had `no_signal` status (signal integration not yet live). The Playwright mock-layer approach enables this scenario to be exercised deterministically regardless of live signal data. SC-WATCH-06 closes the deferred AC-6 from v2.1 ST-10 DoQ sign-off.

---

## 4. Scenarios — Signal Context Panel in Trade Plan Form (v3.7, BLG-FE-34)

*Canonical spec: `docs/design/2026-05-18__release-v3.7/signal-context-panel/ux_spec.md`*
*Playwright file: `tests/e2e/trade-plan-signal-context.spec.js`*

---

### SC-TP-SIG-01 — Panel present when watchlisted signal exists for ticker

**Component:** Trade Plan form — Signal Context panel
**API:** `GET /signals?status=watchlisted`
**Priority:** P1

#### Preconditions

- Trade plan creation form loaded with `ticker=AAPL&market=US`.
- `GET /signals?status=watchlisted` returns a signal with `ticker=AAPL` and `status=watchlisted`.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Navigate to `/#/TradePlan?ticker=AAPL&market=US`. | Trade plan form loads. |
| 2 | Observe the form area between Early Exit Conditions and Pre-Entry Checklist. | **"Signal Context"** panel visible (`data-testid="signal-context-panel"`). Panel shows Rank `#N`, Momentum %, ATR, and Suggested stop. |

#### Pass criteria

- `data-testid="signal-context-panel"` element is visible.
- Panel header "Signal Context" is present.
- Signal rank, momentum, and ATR values rendered.

---

### SC-TP-SIG-02 — Panel absent when no watchlisted signal exists

**Component:** Trade Plan form — Signal Context panel absence
**API:** `GET /signals?status=watchlisted` returning `[]`
**Priority:** P1

#### Preconditions

- Trade plan creation form loaded with `ticker=AAPL&market=US`.
- `GET /signals?status=watchlisted` returns `[]`.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Navigate to `/#/TradePlan?ticker=AAPL&market=US`. | Trade plan form loads. |
| 2 | Observe the form area between Early Exit Conditions and Pre-Entry Checklist. | No Signal Context panel visible. Form fields unchanged from baseline. |

#### Pass criteria

- `data-testid="signal-context-panel"` is not visible.
- No placeholder or empty state shown in the panel location.
- Form fields (entry rationale, confirmation criteria) are empty by default.

---

### SC-TP-SIG-03 — Pre-population from linked signal

**Component:** Trade Plan form — pre-population
**API:** `GET /signals?status=watchlisted`
**Priority:** P2

#### Pass criteria

- When a linked signal exists, `entry_rationale` textarea is pre-populated with the signal rank momentum text (e.g. `"Rank 2 momentum signal…"`).
- User can edit the pre-populated text.
- Fields are not pre-populated in edit mode.

---

### SC-TP-SIG-04 — Panel absent in edit mode

**Component:** Trade Plan form — edit mode non-regression
**Priority:** P1

#### Pass criteria

- `data-testid="signal-context-panel"` is not visible when `?edit=<id>` is present in the URL, even if a watchlisted signal exists for the ticker.
- Existing saved form values are not overwritten by pre-population.

---

## 5. Director of Quality Sign-Off

*(To be completed after scenario execution)*

- [ ] SC-WATCH-01 through SC-WATCH-06 executed (or partial execution documented)
- [ ] SC-TP-SIG-01 through SC-TP-SIG-04 executed (or partial execution documented)
- [ ] Results recorded in `qa_evidence_EPIC-01.md`
- [ ] SC-WATCH-06 explicitly closes deferred AC-6 from v2.1
- [ ] No unresolved P0 or P1 deviations

**Signed off by:** *(pending)*
**Date:** *(pending)*
