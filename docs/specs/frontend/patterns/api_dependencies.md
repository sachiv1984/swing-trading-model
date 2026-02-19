# api_dependencies.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Status:** Canonical
**Version:** 1.1
**Last Updated:** 2026-02-19

## Purpose
This document maps every **surface** (page, modal, or component) to the **API endpoints** it directly calls. It exists to make change impact visible — when an endpoint changes, this document tells you which surfaces are affected.

This is a dependency index, not an API contract. For payload shapes, see `docs/specs/api_contracts/`.

---

## Dependency Categories

### 1. Primary Data Dependencies (page loads, critical reads)
Required for the page to render its primary content.
**Behavior expectations:**
- Loading states are shown while data is being fetched.
- Error states are shown if the fetch fails.
- Retry is available where appropriate.

---

### 2. Mutation Dependencies (writes, form submissions)
Triggered by user actions that change state.
**Behavior expectations:**
- Confirmation actions are disabled during submission.
- If submission fails:
  - the UI does not discard user input
  - the user remains in context (modal stays open)
  - a retry path is available

---

### 3. Supporting Data Dependencies (e.g., tags, settings)
Used for autocomplete lists, filters, and configuration-driven UI.
**Behavior expectations:**
- Supporting data must not block primary tasks when unavailable.
- If it fails to load, the primary experience still works with graceful fallback (e.g., manual entry).

---

### 4. Debounced Live Calculation Dependencies
Triggered continuously as the user types. Not form submissions — these calls are read-only and stateless.
**Behavior expectations:**
- The frontend owns debounce timing. The specified debounce delay must be respected to prevent unnecessary API load.
- A loading/shimmer state is shown during the debounce window and response window.
- Failures show a graceful fallback (e.g., `—` values) without blocking the form.
- These calls must not block form submission on failure or invalid result.

---

## API Dependency Map (Surfaces → Endpoints)

> Note: This is a dependency index. For payload shapes, see API contracts.

### Dashboard (Home)
**Reads**
- `GET /portfolio` (portfolio summary)
- `GET /portfolio/history?days=30` (performance series)

**Triggers**
- `GET /positions/analyze` (daily monitor analysis)

---

### Positions Page (Grid / Table / Journal Views)
**Reads**
- `GET /positions` (positions list, includes live pricing and journal fields where applicable)
- `GET /positions/tags` (tag filter options / autocomplete source)

**Opens related flows**
- Exit flow (Exit Modal)
- Journal/detail review (Position Detail Modal)

---

### Position Detail Modal (Journal / Details)

> **Data source note:** This modal does not fetch position data independently. The full position object is passed in as a prop from the parent Positions page, which already holds position data from `GET /positions`. The modal only makes API calls for tag suggestions and journal writes.

**Reads (supporting)**
- `GET /positions/tags` (tag suggestions/autocomplete)

**Writes**
- `PATCH /positions/{id}/note` (update entry_note or exit_note)
- `PATCH /positions/{id}/tags` (update tags)

---

### Trade Entry Page
**Writes**
- `POST /portfolio/position` (create position, optionally includes entry_note and tags)

**Reads (supporting)**
- `GET /positions/tags` (tag suggestions)
- `GET /settings` (fees/strategy parameters; `default_risk_percent` used to pre-populate the sizing calculator Risk % field on form load)

**Debounced live calculations**
- `POST /portfolio/size` (Position Sizing Calculator)
  - **Debounce:** 300ms after the user stops typing in Entry Price, Stop Price, FX Rate, or the Risk % field within the widget
  - **Trigger fields:** `entry_price`, `stop_price`, `fx_rate` (from form fields), `risk_percent` (from widget input)
  - **Called on:** field change (debounced), not on form submission
  - **Read-only:** does not mutate state. Safe to call repeatedly.
  - **On valid result (`valid: true`, `cash_sufficient: true`):** auto-fills Shares if Shares is empty; shows "Use suggested shares" affordance if Shares already has a value
  - **On insufficient cash (`cash_sufficient: false`):** shows `max_affordable_shares` as informational text; does not auto-fill Shares
  - **On invalid result (`valid: false`):** shows plain-language message derived from `reason` code; does not auto-fill Shares
  - **On network failure:** shows `—` in all output fields; retries on next keystroke
  - **Does not block form submission** in any state

---

### Exit Position Modal
**Writes**
- `POST /positions/{position_id}/exit` (exit full/partial, optionally includes exit_note)

**UX note**
- The modal continuously updates preview values as the user edits exit inputs (regardless of where calculations occur).

---

### Trade History Page
**Reads**
- `GET /trades` (closed trades + journal fields for entry/exit notes + tags)
- `GET /positions/tags` (tag filter dropdown values)

---

### Cash Management Modal
**Reads**
- `GET /cash/transactions` (transaction history)
- `GET /cash/summary` (running totals / current cash)

**Writes**
- `POST /cash/transaction` (deposit/withdrawal)

---

### Settings Page
**Reads**
- `GET /settings`

**Writes**
- `PUT /settings`

---

### Performance Analytics Page
**Reads**
- `GET /analytics/metrics?period={period}` (all analytics data — executive metrics, advanced metrics, market comparison, monthly data, exit reasons, day-of-week, holding periods, top performers, consistency metrics, trades for charts)

**UX note**
- This is a single-endpoint page. All charts and metrics on the page are derived from one response. Period filter changes re-fetch the full response.
- The page gates all output behind `summary.has_enough_data`. When `false`, only the period selector and a "not enough data" message are shown.

---

## Do / Don't Guidance

### Do
- Keep endpoint lists in this file, not scattered across specs.
- Link to API contracts for schemas instead of copying them.
- Record read vs write dependencies so impact is clear.
- Call out UX-visible behaviors tied to calls (loading, retry, preservation of input).
- Record debounce timing for live calculation dependencies.
- Update this file whenever a surface adds/removes an endpoint dependency.

### Don't
- Don't paste full request/response shapes here (that belongs to API contracts).
- Don't document implementation mechanisms (React Query, caching, interceptors).
- Don't document endpoints that a surface receives via props — only direct API calls.
