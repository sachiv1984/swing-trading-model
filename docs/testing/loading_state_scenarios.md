**Owner:** QA & Testing Owner
**Class:** Class 2
**Status:** Canonical
**Version:** 0.1
**Last Updated:** 2026-03-26
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Sprint Item:** ST-12 — EPIC-04 (v2.3)
**Design Source:** docs/design/2026-03-24__release-v2.3/loading-states/ux_spec.md
**Pattern Spec:** docs/specs/frontend/patterns/loading_states.md v1.0

---

# Loading State Standardisation Test Scenarios — ST-12 (LS)

## Purpose

Test scenarios covering the three-state loading pattern applied to all API-backed components in ST-12:

1. **Loading state** — centred spinner while API call is in flight
2. **Empty state** — neutral icon + heading + body when API returns no data
3. **Error state** — error icon + "Something went wrong" + retry when API fails

**Pages in scope:** Portfolio (Dashboard), Positions, Watchlist, Alerts (Notifications), Analytics.

**Automated coverage:** SC-LS-01 through SC-LS-13 (Playwright) cover non-visual AC — spinner presence, correct text content, retry triggering. See `tests/e2e/loading-states.spec.js`. The scenarios below cover visual AC that requires human review.

**Hard constraints (all scenarios):**
- Spinner must be the only loading indicator — no skeleton loaders anywhere.
- Raw API error details (HTTP status codes, stack traces, error messages) must never appear in the UI.
- Empty state must not use error colouring (red/amber).
- Error state must not be mistakable for empty state (must use red or amber icon).

---

## SC-LS-VIS-01 — Loading State: Spinner Appearance

**Priority:** P1
**Pages:** All five (Portfolio, Positions, Watchlist, Alerts, Analytics)
**Method:** Staging — throttle network to "Slow 3G" in DevTools to hold loading state

### SC-LS-VIS-01a — Spinner is centred and spinner-only

**Precondition:** Network throttled. Navigate to each page in scope.

**Steps:**
1. Open DevTools → Network → throttle to Slow 3G.
2. Navigate to each page: Portfolio (`/#/Dashboard`), Positions (`/#/Positions`), Watchlist (`/#/Watchlist`), Alerts (`/#/notifications`), Analytics (`/#/PerformanceAnalytics`).
3. Observe the component area while the API response is pending.

**Expected (all pages):**
- A single circular spinning animation is visible, centred within the component area.
- No skeleton rows, placeholder boxes, or pulsing grey blocks are shown.
- No "Loading…" text is displayed alongside or instead of the spinner.
- The page header and navigation remain visible and stable (spinner is within the content area only).

### SC-LS-VIS-01b — Spinner disappears on response

**Precondition:** Network throttled. Spinner is visible.

**Steps:**
1. Wait for the API response to arrive.

**Expected:** Spinner is replaced immediately by either the data, empty state, or error state. No transition flash or residual spinner.

---

## SC-LS-VIS-02 — Empty State: Visual Appearance

**Priority:** P1
**Pages:** Positions, Watchlist, Alerts (Notifications)
**Method:** Staging with an account containing no data in the relevant domain

### SC-LS-VIS-02a — Empty state uses neutral styling (not error styling)

**Precondition:** Page loaded with empty dataset (no positions / no watchlist entries / no notifications).

**Steps:**
1. Navigate to each page with no data.
2. Observe the empty state component.

**Expected (all pages):**
- An icon is shown in a neutral colour (grey/slate — not red, not amber).
- A short descriptive heading is shown in white or light text.
- A brief body text is shown in muted grey.
- No red or amber colouring is used anywhere in the component.
- No "Try again" retry button is present.

### SC-LS-VIS-02b — Empty state content is correct per page

**Expected per page:**

| Page | Icon (approximate) | Heading | Body |
|------|-------------------|---------|------|
| Positions | Folder/document | "No open positions" | "Enter a trade to see your positions here." |
| Watchlist | Eye | "Your watchlist is empty" | "Add tickers you're monitoring for entry opportunities." |
| Alerts | Bell | "No notifications yet" | "Alert notifications will appear here when triggered." |

### SC-LS-VIS-02c — CTA button present where applicable

**Expected:**
- Positions empty state: "Enter First Position" button visible, links to Trade Entry page.
- Watchlist empty state: "Add Ticker" button visible, opens the add modal on click.
- Alerts empty state: no CTA button (no direct user action available).

### SC-LS-VIS-02d — Empty state does not appear during loading

**Precondition:** Network throttled.

**Steps:**
1. Navigate to Positions or Watchlist with network throttled.
2. Observe during the loading period.

**Expected:** Empty state is not shown while the spinner is active. The transition goes: spinner → (data or empty or error), never spinner + empty simultaneously.

---

## SC-LS-VIS-03 — Error State: Visual Appearance

**Priority:** P1
**Pages:** Positions, Watchlist, Alerts, Analytics
**Method:** Staging — block the API endpoint using DevTools (Network → block request URL) or use browser DevTools to set the backend offline

### SC-LS-VIS-03a — Error state uses error styling (red or amber icon)

**Precondition:** API call fails (network blocked or backend offline).

**Steps:**
1. Block the API endpoint for the page under test.
2. Navigate to each page in scope.
3. Observe the error state.

**Expected (all pages):**
- An error icon (exclamation circle or similar) is shown in **red or amber** — not grey, not green.
- The heading reads exactly: **"Something went wrong"**.
- A brief body text is shown (e.g. "Unable to load data. Please try again.").
- A **"Try again"** button is visible below the body text.
- No raw error details, HTTP status codes (e.g. "500"), or stack traces are shown in the UI.

### SC-LS-VIS-03b — Error state is visually distinct from empty state

**Steps:**
1. Compare the error state (SC-LS-VIS-03a) side-by-side with the empty state (SC-LS-VIS-02a) for the same page.

**Expected:**
- The error icon colour (red/amber) is clearly different from the neutral empty state icon (grey/slate).
- The "Something went wrong" heading text is different from the empty state heading.
- The "Try again" button is only present in the error state, never in the empty state.

### SC-LS-VIS-03c — Raw errors logged to console only

**Precondition:** Error state is visible. DevTools Console tab is open.

**Steps:**
1. Open DevTools → Console.
2. Observe both the UI and the console.

**Expected:**
- The browser console contains an error entry with the raw API error details.
- The UI shows only the friendly "Something went wrong" message — no raw error text visible on screen.

---

## SC-LS-VIS-04 — Retry Button Behaviour

**Priority:** P1
**Pages:** Positions, Watchlist, Alerts, Analytics
**Method:** Staging — temporarily block API, then unblock

### SC-LS-VIS-04a — Retry re-enters loading state

**Precondition:** Error state is visible.

**Steps:**
1. Without unblocking the API, click "Try again".

**Expected:** The spinner appears again (loading state re-entered). The error state disappears while the retry is in flight.

### SC-LS-VIS-04b — Retry resolves to data on success

**Precondition:** Error state is visible. API is then unblocked.

**Steps:**
1. Unblock the API endpoint.
2. Click "Try again".

**Expected:** Spinner appears, then is replaced by data (or empty state if no data). Error state does not reappear.

---

## SC-LS-VIS-05 — No Regression to Existing Layouts

**Priority:** P1
**Pages:** All five
**Method:** Staging — normal load with data present

### SC-LS-VIS-05a — Populated pages render correctly

**Precondition:** Account has data in each domain (positions, watchlist entries, notifications, trades).

**Steps:**
1. Navigate to each page in scope with data present.
2. Verify data renders as expected.

**Expected:**
- Portfolio (Dashboard): widgets load and display correctly; drag-and-drop functions.
- Positions: position cards or table rows render; grid/table/journal view toggle works.
- Watchlist: ticker rows render with signal badges; Add Ticker, Edit, Delete actions work.
- Alerts: notification rows render; Mark as read, Mark all as read work.
- Analytics: charts and metric cards render; time period selector works.
- No layout shift, overflow, or missing content on any page.

### SC-LS-VIS-05b — No skeleton loaders visible anywhere

**Precondition:** Pages loaded as in SC-LS-VIS-05a (or throttled as in SC-LS-VIS-01a).

**Steps:**
1. Check each page during loading and after load.

**Expected:** No pulsing grey skeleton rows, placeholder boxes, or skeleton shimmer effects are visible at any point on any of the five pages.

---

## Automated Coverage Reference

The following Playwright scenarios run in CI and cover non-visual AC. A passing Playwright run is required as supporting evidence before DoQ sign-off.

| Scenario | Description | File |
|----------|-------------|------|
| SC-LS-01 | Positions — spinner present during load | loading-states.spec.js |
| SC-LS-02 | Positions — error state on 500 | loading-states.spec.js |
| SC-LS-03 | Positions — empty state heading | loading-states.spec.js |
| SC-LS-04 | Watchlist — spinner present during load | loading-states.spec.js |
| SC-LS-05 | Watchlist — error state on 500 | loading-states.spec.js |
| SC-LS-06 | Watchlist — empty state heading | loading-states.spec.js |
| SC-LS-07 | Notifications — spinner present during load | loading-states.spec.js |
| SC-LS-08 | Notifications — error state on 500 | loading-states.spec.js |
| SC-LS-09 | Notifications — empty state heading | loading-states.spec.js |
| SC-LS-10 | Analytics — spinner present during load | loading-states.spec.js |
| SC-LS-11 | Analytics — error state on 500 | loading-states.spec.js |
| SC-LS-12 | Dashboard — spinner present during load | loading-states.spec.js |
| SC-LS-13 | Positions — retry triggers new API call | loading-states.spec.js |

---

## Sign-Off

| Role | Sign-Off | Date | Evidence Method |
|------|----------|------|-----------------|
| QA & Testing Owner | Pending | — | Authoring review |
| Director of Quality | Pending | — | Staging run required |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-26 | Initial scenarios. ST-12 / EPIC-04 (v2.3). 5 scenario groups, 13 visual sub-scenarios. Automated reference: SC-LS-01–13 (Playwright). |
