**Owner:** Head of UX & Design
**Status:** Approved
**Approved by:** Product Owner — 2026-03-24
**Cycle:** 2026-03-24__release-v2.3
**Story:** ST-12 (BLG-FE-02)

---

# UX Spec — Loading State Standardisation

## Standard Three-State Pattern

All API-backed components must implement exactly three states:

### 1. Loading State
- A spinner (centered in the component area)
- No skeleton loading — spinner only to avoid layout shift
- Shown immediately when the API call begins; hidden when response arrives

### 2. Empty State
- **Icon:** relevant neutral icon (e.g. inbox, chart, list)
- **Heading:** descriptive ("No positions open", "No alerts", "No trades")
- **Body text:** brief context ("Open a position to see it here.")
- **CTA (optional):** action button if the user can directly remedy the empty state (e.g. "Add trade", "Add alert rule")
- Empty state is distinct from error state — no error colouring; no retry button

### 3. Error State
- **Icon:** error or warning icon (red or amber)
- **Heading:** "Something went wrong"
- **Body text:** brief description (use friendly language — no HTTP status codes shown to user)
- **Retry button:** "Try again" — re-triggers the API call
- Raw API error details logged to browser console only (never shown in UI)

## Pages in scope

Apply pattern to all API-backed components on: Portfolio, Positions, Watchlist, Alerts, Analytics.

## Implementation notes

- Wrap API-backed sections in a `<DataState>` or equivalent container component
- Do not mix loading and empty states (e.g. no "loading..." text in an empty-state placeholder)
- Error state must not look like empty state (colour and icon must differ)

## Out of scope for v2.3

- Global page-level loading indicators (e.g. topbar progress bar)
- Real-time / streaming states
