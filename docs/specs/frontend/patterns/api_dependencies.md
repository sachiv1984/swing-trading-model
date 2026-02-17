# api_dependencies.md

## Purpose
The API Dependencies pattern defines how the frontend documentation records **which UX surfaces depend on which backend APIs**, without duplicating API contract detail.

Its goal is to ensure API usage is:
- Discoverable (easy to find which surfaces call what)
- Non-duplicative (no scattered endpoint lists across files)
- UX-aligned (focus on user-visible loading, error, and state outcomes)
- Maintainable (easy to update when contracts or flows change)

This pattern applies to all pages, modals, and components that read or write backend data.

---

## When This Pattern Is Used
Use the API Dependencies pattern whenever:
- A page or modal fetches data (initial load or refresh)
- A UI action writes data (create/update/exit)
- A reusable component depends on remote data (e.g., tag suggestions)
- A change to an endpoint could affect multiple UX surfaces
- A reviewer needs to assess blast-radius for a backend or data model change

---

## UX Rationale
- Designers and QA need to know **what data a surface relies on** to validate states and edge cases without reading code.
- Engineers need a single place to see **read vs write dependencies** to evaluate change impact quickly.
- Documentation should not repeat schemas; schemas drift unless they remain owned by a single source.
- A dependency view helps prevent silent regressions by making shared data contracts visible across the product.

---

## Source of Truth (Contracts)
Canonical request/response shapes, error payloads, and field-level schemas live in the API contracts (`specs/api_contracts/`).

This pattern intentionally documents only:
- which surfaces depend on which endpoints
- whether they read or write
- UX-visible loading/error expectations tied to those calls

---

## Dependency Types & Expected Behavior

### 1. Read Dependencies (GET)
Used when the UI must retrieve data to render.
**Behavior expectations:**
- A loading state is visible while data is being fetched.
- If the request fails:
  - show a global error banner (page) or modal error banner (modal)
  - preserve user context (do not navigate away)
  - allow retry where feasible

---

### 2. Write Dependencies (POST / PATCH / PUT)
Used when the user commits a change.
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
- `GET /settings` (fees/strategy parameters where needed for UI)

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
- Update this file whenever a surface adds/removes an endpoint dependency.

### Don't
- Don't paste full request/response shapes here (that belongs to API contracts).
- Don't document implementation mechanisms (React Query, caching, interceptors).
- Don't document endpoints that a surface receives via props — only direct API calls.
