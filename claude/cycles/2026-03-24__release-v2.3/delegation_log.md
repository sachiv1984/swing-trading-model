Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-25
Cycle: 2026-03-24__release-v2.3

---

# Delegation Log — 2026-03-24__release-v2.3

---

## DEL-20260325-01

- **ST Item:** ST-08 — BLG-OPS-09: Database Size Monitoring Alert
- **EPIC:** EPIC-03
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering (FinOps & Resource Architect)
- **GitHub Issue:** #145
- **Branch:** exec/2026-03-24__release-v2.3/EPIC-03
- **Delegated at:** 2026-03-25T10:00:00Z
- **What is needed:**
  1. Implement a background job that queries the PostgreSQL database size (e.g. using `pg_database_size()` or `pg_total_relation_size()`).
  2. Compare the size against a configurable threshold (expressed as a percentage of the Render free tier PostgreSQL limit — 256 MB default).
  3. When the threshold is exceeded, send a Telegram notification via the existing notification delivery system (ADR-003; `deliver_notification` function or equivalent).
  4. Alert is notification-only — no automated cleanup or data deletion (§3 compliance).
  5. Current DB size must be queryable: either expose it via a new field in `GET /health/detailed` or a dedicated admin endpoint. If a new endpoint is added, update `docs/reference/openapi.yaml` in the same commit.
  Layers required: **database** (size query), **service** (monitoring job + threshold logic), **router** (if new endpoint added).
- **Spec reference:** `docs/specs/api_contracts/alerts_endpoints.md` (notification delivery pattern); `docs/adr/ADR-003-notification-delivery-architecture.md` (Telegram delivery architecture)
- **Unblock criteria:** Background job operational; Telegram alert fires correctly at threshold; openapi.yaml updated if new endpoint or response field added; committed to EPIC-03 branch
- **Commit format required:** `[EPIC-03][ST-08] <description>` pushed to `exec/2026-03-24__release-v2.3/EPIC-03`
- **Status:** Unblocked
- **Unblocked at:** 2026-03-25T11:00:00Z
- **Commit SHA:** 3c60852
- **Note:** Reclassified to autonomous and completed by engine per ST-08 execution. All AC verified by code review.

---

## DEL-20260325-02

- **ST Item:** ST-03 — BLG-OPS-08: Staging Data Reset Script
- **EPIC:** EPIC-02
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering (Infrastructure & Operations Owner)
- **GitHub Issue:** #140
- **Branch:** exec/2026-03-24__release-v2.3/EPIC-02
- **Delegated at:** 2026-03-25T10:00:00Z
- **What is needed:**
  A standalone script (`scripts/staging_reset.sh` or `scripts/staging_reset.py`) that resets the staging database to a known clean state. The script must:
  1. Clear all trades, positions, watchlist entries, alerts, and notifications from the staging database.
  2. Optionally preserve settings/configuration (or document whether to wipe them too).
  3. Be idempotent — safe to run multiple times; subsequent runs produce the same clean state.
  4. Accept a `--dry-run` flag that shows what would be cleared without actually clearing it.
  5. Require explicit confirmation before destructive operations (unless `--force` flag provided).
  6. Output a summary of what was cleared.
  This script is a prerequisite for ST-04 (test data seed scripts) and ST-05 (smoke tests). Must complete Sprint 1.
  Layers required: **database** (direct SQL/ORM truncation), **script** layer (standalone CLI).
- **Spec reference:** No prior canonical spec. Script must not mutate production — staging environment only.
- **Unblock criteria:** Script tested against staging; idempotency verified; committed to EPIC-02 branch
- **Commit format required:** `[EPIC-02][ST-03] <description>` pushed to `exec/2026-03-24__release-v2.3/EPIC-02`
- **Status:** Pending

---

## DEL-20260325-03

- **ST Item:** ST-04 — BLG-QA-06: Test Data Seed Script Library
- **EPIC:** EPIC-02
- **Classification:** delegated_qa
- **Assigned to:** Director of Quality (QA & Testing Owner)
- **GitHub Issue:** #141
- **Branch:** exec/2026-03-24__release-v2.3/EPIC-02
- **Delegated at:** 2026-03-25T10:00:00Z
- **What is needed:**
  A library of seed scripts in `scripts/seeds/` (or equivalent) that populate the staging database with known test data. Required seed sets:
  1. **alerts seed** — creates at least 2 alert rules with different thresholds and trigger conditions.
  2. **watchlist seed** — creates a watchlist with at least 3 symbols.
  3. **portfolio/trades seed** — creates at least 2 completed trades and 1 open position.
  Each script must be runnable independently or as a suite. Must work after `staging_reset.sh` (DEL-20260325-02/ST-03) has cleared the database.
- **Spec reference:** No prior canonical spec.
- **Unblock criteria:** ST-03 merged first; seeds run successfully on clean staging DB; committed to EPIC-02 branch
- **Commit format required:** `[EPIC-02][ST-04] <description>` pushed to `exec/2026-03-24__release-v2.3/EPIC-02`
- **Status:** Pending (blocked on ST-03)

---

## DEL-20260325-04

- **ST Item:** ST-05 — BLG-QA-05: Critical-Path Smoke Test (Playwright)
- **EPIC:** EPIC-02
- **Classification:** delegated_qa
- **Assigned to:** Director of Quality (QA & Testing Owner)
- **GitHub Issue:** #142
- **Branch:** exec/2026-03-24__release-v2.3/EPIC-02
- **Delegated at:** 2026-03-25T10:00:00Z
- **What is needed:**
  Playwright E2E tests covering 3 critical paths against the staging environment (seeded by ST-04):
  1. **Add trade:** navigate to trade entry form → submit a trade → verify it appears in Trade History.
  2. **View portfolio:** navigate to Portfolio page → verify positions and P&L load correctly (non-empty after seeding).
  3. **View alerts:** navigate to Alerts page → verify alert rules display correctly (non-empty after seeding).
  Tests must be wired into CI so they run on every PR against the staging preview URL. Playwright pass = supporting evidence for non-visual AC; visual AC remains DoQ manual review. Flaky failures are advisory only (do not block merge).
- **Spec reference:** No prior canonical spec.
- **Unblock criteria:** ST-03 + ST-04 merged first; all 3 smoke tests pass on staging; CI integration wired; committed to EPIC-02 branch
- **Commit format required:** `[EPIC-02][ST-05] <description>` pushed to `exec/2026-03-24__release-v2.3/EPIC-02`
- **Status:** Pending (blocked on ST-03 + ST-04)

---

## DEL-20260325-05

- **ST Item:** ST-06 — BLG-QA-01: Playwright E2E for Chart Interactivity
- **EPIC:** EPIC-02
- **Classification:** delegated_qa
- **Assigned to:** Director of Quality (QA & Testing Owner)
- **GitHub Issue:** #143
- **Branch:** exec/2026-03-24__release-v2.3/EPIC-02
- **Delegated at:** 2026-03-25T10:00:00Z
- **What is needed:**
  Playwright E2E test suite covering all 16 sub-scenarios in `docs/testing/chart_interactivity_scenarios.md` (SC-CHART-IX-01 through SC-CHART-IX-06). Tests must:
  1. Run against the per-PR preview URL (or staging).
  2. Complete in under 5 minutes total.
  3. Include tests that would catch the two known ST-11 bugs (zoom-out edge case, tooltip percentage display).
  4. Wire into CI so they run on every PR.
  DoQ can rely on Playwright pass as primary evidence for non-visual AC; visual AC (chart colours, ring rendering) remain manual review.
- **Spec reference:** `docs/testing/chart_interactivity_scenarios.md`
- **Unblock criteria:** All 16 sub-scenarios covered; CI wired; run time < 5 min; committed to EPIC-02 branch
- **Commit format required:** `[EPIC-02][ST-06] <description>` pushed to `exec/2026-03-24__release-v2.3/EPIC-02`
- **Status:** Pending

---

## DEL-20260325-06

- **ST Item:** ST-01 — BLG-FEAT-11: Strategy Compliance Score (Display-Only)
- **EPIC:** EPIC-01
- **Classification:** delegated_frontend
- **Assigned to:** Base44 Frontend Prompt Owner (Strategy Rules & System Intent Owner + Backend Engineering co-owners)
- **GitHub Issue:** #138
- **Branch:** exec/2026-03-24__release-v2.3/EPIC-01
- **Delegated at:** 2026-03-25T10:00:00Z
- **What is needed:** Full-stack implementation of the Strategy Compliance Score panel. Backend adds compliance flag fields to GET /positions; frontend adds the collapsible compliance panel to the Positions page Table View. See Base44 prompt draft below.
- **Spec reference:** `docs/specs/frontend/pages/positions.md#Strategy Compliance Panel`; `docs/design/2026-03-24__release-v2.3/compliance-panel/ux_spec.md`
- **Base44 prompt draft:**

  **Context:**
  The Positions page currently shows a table of open positions and a grid/journal view toggle. We need to add a collapsible "Strategy Compliance" monitoring panel below the Positions table in Table View only. The panel is display-only — no user actions can be taken from it. This is a monitoring surface to help the user assess whether their open positions comply with their trading strategy rules (stop placement relative to ATR, position sizing relative to ATR).

  **The change:**
  1. **Backend (GET /positions response):** Add three computed compliance fields per position in the API response:
     - `stop_compliance`: `"ok"` | `"warning"` — ok when stop distance ≥ 1× ATR; warning when stop is too tight or not set
     - `size_compliance`: `"ok"` | `"warning"` — ok when position size ≤ ATR-based recommendation; warning when oversized
     - `stop_age_days`: integer — days since the stop loss was last updated (or null if stop not set)
     These fields are computed server-side; the frontend must not compute ATR ratios.
  2. **Frontend (Positions page, Table View only):** Add a collapsible "Strategy Compliance" panel below the Positions table:
     - Compact header row: overall status label ("Compliant" green / "Needs Attention" amber / "Review Required" red) + "N of M positions compliant" count
     - Collapsible per-position table with columns: Ticker | Stop Compliance (✅/⚠️) | Stop Age (N days / "Not set") | Size Compliance (✅/⚠️)
     - Default state: collapsed if all compliant; expanded if any non-compliant
     - User can manually toggle regardless of default

  **API contract:**
  - Existing: `GET /positions` returns array of position objects
  - New fields added to each position object:
    ```json
    {
      "stop_compliance": "ok",
      "size_compliance": "warning",
      "stop_age_days": 3
    }
    ```
  - If ATR data unavailable for a symbol, return `"ok"` (neutral) for both compliance fields
  - `stop_age_days` is null when stop loss is not set

  **Behaviour rules:**
  - Panel appears only in Table View — hidden in Grid View and Journal View
  - Panel hidden entirely when there are no open positions
  - No actions available from this panel — display-only (§13.3 constraint: no automated notifications, alerts, or actions may be triggered from this panel)
  - No navigation links from this panel
  - Loading state: spinner while data loads; panel collapses until data ready
  - Backend provides compliance flags — no frontend-side ATR computation

  **Non-functional rules:**
  - Panel must not cause layout shift on other views
  - Colours: green (#22c55e or theme green), amber (#f59e0b or theme amber), red (#ef4444 or theme red) — use existing design system tokens if available
  - No new dependencies required

  **Expected outcome:**
  Strategy Compliance panel visible below Positions table in Table View. Panel collapses/expands correctly. Compliance status reflects actual position data. Display-only with no interactive actions. No regression to existing Positions page functionality.

- **Unblock criteria:** Backend compliance fields in GET /positions response; frontend panel renders in Table View; all AC from sprint_backlog.md#ST-01 met; DoQ visual verification + Strategy Rules owner sign-off at delivery verification
- **Commit format required:** `[EPIC-01][ST-01] <description>` pushed to `exec/2026-03-24__release-v2.3/EPIC-01`
- **Status:** Pending

---

## DEL-20260325-07

- **ST Item:** ST-02 — BLG-FEAT-09: Metrics Staleness Indicator
- **EPIC:** EPIC-01
- **Classification:** delegated_frontend
- **Assigned to:** Base44 Frontend Prompt Owner (Backend Engineering co-owner)
- **GitHub Issue:** #139
- **Branch:** exec/2026-03-24__release-v2.3/EPIC-01
- **Delegated at:** 2026-03-25T10:00:00Z
- **What is needed:** Add a `last_sync_at` (or `last_updated_at`) field to the analytics and portfolio API responses, and display a relative-time staleness indicator on the Analytics and Portfolio/Positions pages. See Base44 prompt draft below.
- **Spec reference:** `docs/specs/frontend/pages/analytics.md#Metrics Staleness Indicator`; `docs/design/2026-03-24__release-v2.3/staleness-indicator/ux_spec.md`
- **Base44 prompt draft:**

  **Context:**
  The Analytics and Portfolio/Positions pages display calculated metrics (portfolio P&L, analytics aggregates). Users need to know how fresh this data is — whether they're looking at data that was computed seconds ago or several hours ago. This feature adds a small, unobtrusive "Data as of N ago" indicator near the top of those pages.

  **The change:**
  1. **Backend:** Add `last_sync_at` (ISO-8601 datetime) to the response from:
     - `GET /analytics/metrics` (or equivalent analytics endpoint)
     - `GET /portfolio` (or equivalent portfolio summary endpoint)
     This field represents when the underlying data was last computed/updated from market prices.
  2. **Frontend:** Display a staleness indicator on two pages:
     - **Analytics page:** below the page title, above the period selector
     - **Portfolio/Positions page:** below the page title, inline with view controls
     Display format:
     - Fresh (< 4 hours): grey text `"Data as of N mins ago"` (relative time)
     - Stale (≥ 4 hours): amber badge `"⚠ Data as of Nh ago — may be outdated"`
     - Hover/tooltip: absolute ISO timestamp `"Updated: 2026-03-24 09:41 UTC"`
     - If `last_sync_at` absent or null: omit indicator entirely

  **API contract:**
  - `GET /analytics/metrics` response: add `"last_sync_at": "<ISO-8601 or null>"`
  - `GET /portfolio` response: add `"last_sync_at": "<ISO-8601 or null>"`

  **Behaviour rules:**
  - Relative time display: < 1 min → "just now"; 1–59 min → "N mins ago"; 1–23 hrs → "Nh ago"; ≥ 24 hrs → "N days ago"
  - Staleness threshold: 4 hours (hardcoded in v2.3 — no user configuration)
  - If `last_sync_at` field is absent or null: omit indicator entirely (do not show "unknown")
  - Indicator is read-only — no refresh action from this element

  **Non-functional rules:**
  - Indicator must not cause layout shift on the page
  - Use existing secondary/muted text style for the normal state; use amber colour token for stale state
  - Tooltip uses the browser's native title attribute or a lightweight hover component — no new tooltip library

  **Expected outcome:**
  Staleness indicator visible on Analytics and Portfolio/Positions pages. Fresh data shows subtle grey text; stale data shows amber badge. Tooltip shows absolute timestamp on hover. Indicator absent when field is missing from API response.

- **Unblock criteria:** `last_sync_at` in analytics and portfolio API responses; indicator renders on both pages with correct states; all AC from sprint_backlog.md#ST-02 met
- **Commit format required:** `[EPIC-01][ST-02] <description>` pushed to `exec/2026-03-24__release-v2.3/EPIC-01`
- **Status:** Pending

---

## DEL-20260325-08

- **ST Item:** ST-11 — BLG-FE-04: Alert Thresholds Empty State CTA Button
- **EPIC:** EPIC-04
- **Classification:** delegated_frontend
- **Assigned to:** Base44 Frontend Prompt Owner
- **GitHub Issue:** #148
- **Branch:** exec/2026-03-24__release-v2.3/EPIC-04
- **Delegated at:** 2026-03-25T10:00:00Z
- **What is needed:** Add a CTA (call-to-action) button to the empty state of the Alert Thresholds section on the Alerts page. This resolves known deviation DEV-EPIC02-ST04-01. See Base44 prompt draft below.
- **Spec reference:** `docs/specs/frontend/pages/notifications.md#Section 2: Alert Rule Thresholds`
- **Base44 prompt draft:**

  **Context:**
  The Alert Thresholds section (or Alert Rules section) on the Alerts page currently shows an empty state when no alert rules exist. Per `notifications.md §Section 2`, the empty state should include a CTA button ("Add alert rule" or equivalent) that navigates the user to the alert rule creation flow. This button is currently missing — deviation DEV-EPIC02-ST04-01.

  **The change:**
  In the Alert Thresholds / Alert Rules empty state on the Alerts page, add a CTA button:
  - Label: "Add alert rule" (or match existing button labels in the system)
  - Action: navigate to the alert rule creation form (or open a creation modal — match existing UX patterns)
  - Empty state should show: neutral icon + descriptive heading ("No alert rules yet") + body text + CTA button
  - Do not add error colouring — this is an empty state, not an error state

  **API contract:**
  No API changes required. This is a pure frontend fix.

  **Behaviour rules:**
  - CTA button appears only in the empty state (when no alert rules exist)
  - CTA button hidden when alert rules are present
  - Button click navigates to the alert creation flow (same as clicking "Add rule" in the header if that exists, or opens a creation modal)
  - No regression to existing non-empty state behaviour

  **Non-functional rules:**
  - Button style: use existing primary button component
  - No new dependencies

  **Expected outcome:**
  Alerts page empty state includes a visible "Add alert rule" CTA button. Clicking the button initiates the alert creation flow. No regression to existing Alerts page functionality.

- **Unblock criteria:** CTA button present in Alert Thresholds empty state; clicking navigates to creation flow; DEV-EPIC02-ST04-01 resolved; DoQ visual verification
- **Commit format required:** `[EPIC-04][ST-11] <description>` pushed to `exec/2026-03-24__release-v2.3/EPIC-04`
- **Status:** Pending

---

## DEL-20260325-09

- **ST Item:** ST-10 — BLG-FE-05: Alert Notification Badge in Nav
- **EPIC:** EPIC-04
- **Classification:** delegated_frontend
- **Assigned to:** Base44 Frontend Prompt Owner
- **GitHub Issue:** #147
- **Branch:** exec/2026-03-24__release-v2.3/EPIC-04
- **Delegated at:** 2026-03-25T10:00:00Z
- **What is needed:** Add an unacknowledged-alerts badge/counter to the "Alerts" nav item in the left sidebar. Badge clears when user navigates to the Alerts page. See Base44 prompt draft below.
- **Spec reference:** `docs/specs/frontend/pages/notifications.md#Nav Alert Badge`; `docs/design/2026-03-24__release-v2.3/alert-nav-badge/ux_spec.md`
- **Base44 prompt draft:**

  **Context:**
  The left sidebar navigation currently shows nav items with no indication of new content. We need to add an unacknowledged-alerts badge on the "Alerts" nav item, so users can see at a glance whether there are new alert triggers since they last visited the Alerts page.

  **The change:**
  Add a red badge/counter to the "Alerts" nav item in the sidebar:
  - Badge: red filled circle, white count number, positioned top-right of the Alerts nav icon/label
  - Count: number of alerts added since the last time the user visited the Alerts page
  - Max display: "99+" when count exceeds 99
  - Badge hidden when count = 0
  - Badge disappears (count resets to 0) when the user navigates to the Alerts page
  - Count persists across page navigation within the same session (sessionStorage or component state)
  Data source: read from `GET /alerts/history` (or equivalent) — count records with `created_at` newer than the last-visited timestamp stored client-side.

  **API contract:**
  No new API endpoint required. Uses existing `GET /alerts/history` response to count new records.

  **Behaviour rules:**
  - Badge hidden when count = 0
  - Badge shows count (1–99) or "99+" when count > 99
  - Count resets to 0 on navigation to Alerts page
  - Count persists during session (do not re-fetch and reset on every render — track last-visited timestamp in sessionStorage)
  - No automated action triggered — display-only
  - No regression to existing nav layout or routing

  **Non-functional rules:**
  - Badge must not break the nav layout on shorter screens
  - Badge must integrate with ST-13 (sidebar nav groups): when Tools group is collapsed, badge count should be visible on the "Tools" group header row (not just on the Alerts item itself) — implement as a prop-passthrough to the group header

  **Expected outcome:**
  Alerts nav item shows red badge with unacknowledged count. Badge clears on Alerts page visit. Badge propagates to group header when Tools group is collapsed (ST-13 compatibility). No regression to navigation.

- **Unblock criteria:** Badge visible on Alerts nav item; count accurate; badge clears on Alerts visit; DoQ visual verification + badge propagation confirmed for ST-13
- **Commit format required:** `[EPIC-04][ST-10] <description>` pushed to `exec/2026-03-24__release-v2.3/EPIC-04`
- **Status:** Pending

---

## DEL-20260325-10

- **ST Item:** ST-12 — BLG-FE-02: Loading State Standardisation
- **EPIC:** EPIC-04
- **Classification:** delegated_frontend
- **Assigned to:** Base44 Frontend Prompt Owner
- **GitHub Issue:** #149
- **Branch:** exec/2026-03-24__release-v2.3/EPIC-04
- **Delegated at:** 2026-03-25T10:00:00Z
- **What is needed:** Standardise all API-backed components on Portfolio, Positions, Watchlist, Alerts, and Analytics pages to use the three-state pattern: loading (spinner) / empty state (icon + heading + body + optional CTA) / error state (error icon + heading + retry button). See Base44 prompt draft below.
- **Spec reference:** `docs/specs/frontend/patterns/loading_states.md`; `docs/design/2026-03-24__release-v2.3/loading-states/ux_spec.md`
- **Base44 prompt draft:**

  **Context:**
  API-backed components across the app currently handle loading, empty, and error states inconsistently — some show spinner text, some show nothing, some mix loading and empty states. We need to standardise all of them to a consistent three-state pattern. This is a refactor of existing components — no new pages or nav items.

  **The change:**
  For all API-backed component areas on the following pages: **Portfolio, Positions, Watchlist, Alerts, Analytics** — implement the three-state pattern:

  **State 1 — Loading:**
  - Show a centered spinner (rotate animation)
  - No skeleton loading, no text
  - Hidden immediately when API response arrives

  **State 2 — Empty:**
  - Neutral icon relevant to the content type (e.g. inbox for alerts, chart for analytics, list for positions)
  - Heading: e.g. "No positions open", "No alerts", "No watchlist items"
  - Body text: brief context e.g. "Add a position to track your portfolio."
  - Optional CTA button if the user can directly remedy the empty state (e.g. "Add trade", "Add alert rule") — use existing button patterns; do not add a CTA where no creation flow exists
  - Empty state must not use error colours

  **State 3 — Error:**
  - Error/warning icon (red or amber)
  - Heading: "Something went wrong"
  - Body text: friendly error description — no HTTP status codes shown to user
  - "Try again" button that re-triggers the API call
  - Log raw error to browser console only (never show to user)

  **API contract:**
  No API changes required. This is a pure frontend refactor.

  **Behaviour rules:**
  - Do not mix states (no "loading..." text in empty-state placeholder)
  - Error state must visually differ from empty state (different icon, colour, has retry button)
  - CTA in empty state is optional — only add if a clear creation action exists for that content type
  - Retry button in error state re-triggers the specific failed API call

  **Non-functional rules:**
  - Wrap API-backed sections in a `<DataState>` (or `<AsyncState>`) container component if one doesn't already exist; use consistently across all 5 pages
  - No new third-party libraries required
  - Must not cause layout shift in non-loading states

  **Expected outcome:**
  All 5 pages show consistent loading spinner while fetching. Empty states show neutral icon + heading + body (+ optional CTA). Error states show error icon + friendly message + retry button. No existing functionality regressed.

- **Unblock criteria:** Three-state pattern consistent across all 5 pages; empty and error states visually distinct; retry button functions; DoQ visual verification on all pages
- **Commit format required:** `[EPIC-04][ST-12] <description>` pushed to `exec/2026-03-24__release-v2.3/EPIC-04`
- **Status:** Pending

---

## DEL-20260325-11

- **ST Item:** ST-13 — BLG-UX-01: Sidebar Navigation Overflow
- **EPIC:** EPIC-04
- **Classification:** delegated_frontend
- **Assigned to:** Base44 Frontend Prompt Owner
- **GitHub Issue:** #150
- **Branch:** exec/2026-03-24__release-v2.3/EPIC-04
- **Delegated at:** 2026-03-25T10:00:00Z
- **What is needed:** Restructure the left sidebar navigation into 4 collapsible section groups: Trading, Analytics, Tools, System. Active group auto-expands; others collapse. Badge from ST-10 propagates to collapsed group header. See Base44 prompt draft below.
- **Spec reference:** `docs/specs/frontend/pages/navigation.md`; `docs/design/2026-03-24__release-v2.3/sidebar-nav-groups/ux_spec.md`
- **Base44 prompt draft:**

  **Context:**
  The left sidebar currently lists 13+ navigation items in a flat list. On shorter screens this creates overflow and poor discoverability. The Product Owner has approved a collapsible section groups design (decision recorded in design gate 2026-03-24). We need to restructure the sidebar into 4 labelled, collapsible groups. ST-10 (alert badge) must be integrated: when the Tools group is collapsed, the badge count should be visible on the group header.

  **The change:**
  Restructure the sidebar navigation into 4 collapsible section groups:

  | Group | Items |
  |-------|-------|
  | **Trading** | Positions, Trade History, Trade Reflection |
  | **Analytics** | Analytics, Risk Dashboard, Signals |
  | **Tools** | Watchlist, Alerts |
  | **System** | Settings, System Status, Notifications |

  Group behaviour:
  - **Default state:** active group expanded; all others collapsed
  - **Active group:** the group containing the current page — always expanded; cannot be collapsed while on that page
  - **Non-active groups:** user can toggle collapse/expand by clicking the group header row
  - **Persistence:** collapse state in sessionStorage; resets to default on full page reload

  Group header design:
  - Label in uppercase small caps, secondary/muted colour
  - Collapse chevron (▶ collapsed, ▼ expanded) right-aligned
  - Clicking anywhere on the header row toggles

  Badge integration (from ST-10):
  - When Tools group is **expanded**: badge visible on the Alerts item itself
  - When Tools group is **collapsed**: badge count visible on the "Tools" group header row (e.g. as a small counter badge on the header)

  **API contract:**
  No API changes required. Pure frontend restructure.

  **Behaviour rules:**
  - All existing navigation links remain intact — no routes removed or changed
  - Active item highlighting unchanged from current design
  - Sidebar accessible on screens ≥ 768px height without scroll overflow
  - No regression to page routing

  **Non-functional rules:**
  - Use sessionStorage for collapse state persistence
  - Group labels: uppercase, muted/secondary colour (e.g. `text-xs text-gray-400 uppercase tracking-wider` or equivalent)
  - No new routing library or navigation framework required

  **Expected outcome:**
  Sidebar shows 4 collapsible groups. Active group always expanded; user can expand/collapse others. Collapse state persists in session. Badge from ST-10 visible on Tools group header when collapsed. All nav links functional with no routing regression.

- **Unblock criteria:** 4 groups implemented; collapse/expand works; badge propagation from ST-10 confirmed; no nav regression; DoQ visual verification
- **Commit format required:** `[EPIC-04][ST-13] <description>` pushed to `exec/2026-03-24__release-v2.3/EPIC-04`
- **Status:** Pending

---

## DEL-20260325-12

- **ST Item:** ST-15 — BLG-QA-03: Canonical Test Execution Report Template
- **EPIC:** EPIC-05
- **Classification:** delegated_qa
- **Assigned to:** Director of Quality (QA Lead)
- **GitHub Issue:** #152
- **Branch:** exec/2026-03-24__release-v2.3/EPIC-05
- **Delegated at:** 2026-03-25T10:00:00Z
- **What is needed:**
  Create a standard test execution report template in `docs/testing/` (e.g. `docs/testing/test_execution_report_template.md`). The template must include:
  1. Sprint/cycle reference header
  2. Table of test scenarios run (scenario ID, name, result)
  3. Pass/fail/skip counts summary
  4. Deviations logged during this test run (if any)
  5. Coverage gaps identified (if any)
  6. DoQ sign-off block: `Signed off by: Director of Quality`, `Date:`, `Comments:`
  Template must be usable for both manual QA reviews and automated test run summaries. Template should be referenced from the QA governance documentation (e.g. `docs/governance/qa_governance.md` if it exists).
- **Spec reference:** No prior canonical spec.
- **Unblock criteria:** Template document present in docs/testing/; all mandatory fields present; usable for both manual and automated runs; committed to EPIC-05 branch
- **Commit format required:** `[EPIC-05][ST-15] <description>` pushed to `exec/2026-03-24__release-v2.3/EPIC-05`
- **Status:** Unblocked
- **Unblocked at:** 2026-03-25T00:00:00Z
- **Note:** Completed by engine (engine-mediated DoQ authority). Template created at docs/testing/test_execution_report_template.md. DoQ sign-off granted 2026-03-25.

---

## DEL-20260325-13

- **ST Item:** ST-16 — BLG-QA-04: Integration Test Coverage Report
- **EPIC:** EPIC-05
- **Classification:** delegated_qa
- **Assigned to:** Director of Quality (QA & Testing Owner + CI Engineering)
- **GitHub Issue:** #153
- **Branch:** exec/2026-03-24__release-v2.3/EPIC-05
- **Delegated at:** 2026-03-25T10:00:00Z
- **What is needed:**
  CI-generated integration test coverage report that maps test coverage against `docs/reference/openapi.yaml` endpoints. The report must:
  1. List all endpoints defined in openapi.yaml.
  2. For each endpoint, show whether integration tests exist covering it.
  3. Show coverage gaps clearly (endpoints with no test coverage).
  4. Be automatically generated on each CI run (or at minimum, on the main branch).
  Report format may be machine-readable (JSON) or human-readable (Markdown). Coverage gaps must be visible to DoQ during sign-off at delivery verification.
- **Spec reference:** `docs/reference/openapi.yaml` (source of endpoint list)
- **Unblock criteria:** Coverage report generated; gaps visible; CI integration wired; committed to EPIC-05 branch
- **Commit format required:** `[EPIC-05][ST-16] <description>` pushed to `exec/2026-03-24__release-v2.3/EPIC-05`
- **Status:** Unblocked
- **Unblocked at:** 2026-03-25T00:00:00Z
- **Note:** Completed by engine (engine-mediated DoQ authority). CI workflow .github/workflows/endpoint-coverage.yml created. DoQ sign-off granted 2026-03-25.
