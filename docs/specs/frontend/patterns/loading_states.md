**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-03-24
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source:** docs/design/2026-03-24__release-v2.3/loading-states/ux_spec.md
**Confirmed by:** Head of Specs Team — 2026-03-24
**Release:** v2.3 — ST-12 (BLG-FE-02)

---

# Frontend Pattern — Loading State Standardisation

## Purpose

Defines the canonical three-state pattern for all API-backed components. Ensures consistent user experience across Portfolio, Positions, Watchlist, Alerts, and Analytics pages.

## The Three-State Pattern

### 1. Loading State

**When:** API call in progress (request sent; response not yet received).

**Component:**
- Centered spinner in the component area
- No skeleton loading or placeholder layout
- No text (spinner only)

**Behaviour:** Shown immediately when the API call is triggered; removed as soon as a response arrives (success or error).

### 2. Empty State

**When:** API call succeeded but returned empty data (zero records).

**Component:**
- Relevant neutral icon (e.g. inbox, list, chart — contextual)
- Heading: descriptive e.g. "No positions open", "No alerts configured", "No trades recorded"
- Body text: brief, friendly context e.g. "Open a position to see it here."
- CTA button (optional): included only when the user can directly remedy the empty state (e.g. "Add trade", "Add alert rule"); omit if no direct action is available

**Constraints:**
- Empty state must NOT look like an error (no error colouring, no retry button)
- Empty state is distinct from loading — never show empty state while data is loading

### 3. Error State

**When:** API call failed (network error, server error, timeout).

**Component:**
- Error icon (red or amber)
- Heading: "Something went wrong"
- Body text: friendly description; do NOT show HTTP status codes or raw error messages to users
- Retry button: "Try again" — re-triggers the API call

**Constraints:**
- Raw API error details MUST be logged to browser console (for debugging)
- Raw error details MUST NOT be shown in the UI

## Implementation Guidance

- Wrap API-backed sections in a shared `<DataState>` container component (or equivalent pattern)
- The container accepts: `loading`, `error`, `empty`, `children` props
- All three states must be visually distinct — loading (spinner), empty (neutral icon + text), error (red icon + text + retry)

## Pages in scope for v2.3

- Portfolio
- Positions
- Watchlist
- Alerts
- Analytics

## Out of scope for v2.3

- Global page-level loading indicators (e.g. top progress bar)
- Real-time / streaming state transitions
- Pagination loading states

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-24 | Initial version. ST-12 (BLG-FE-02, v2.3): three-state loading pattern for all API-backed components. Design source: docs/design/2026-03-24__release-v2.3/loading-states/ux_spec.md. Approved: Product Owner 2026-03-24. Design gate: 2026-03-24__release-v2.3. |
