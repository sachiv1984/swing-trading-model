**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.2
**Last Updated:** 2026-03-22
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source:** docs/design/2026-03-18__release-v2.1/notification-feed/ux_spec.md | docs/design/2026-03-18__release-v2.1/notification-preferences/ux_spec.md | docs/design/2026-03-21__release-v2.2/alert-threshold-customisation/ux_spec.md | docs/design/2026-03-21__release-v2.2/alert-history-table/ux_spec.md

---

# notifications.md — Notifications (Feed, Preferences, Alert Rules & History)

## Purpose & User Goals

The Notifications section covers four surfaces:
1. **Notification Feed** — a chronological list of alert events triggered by the system
2. **Notification Preferences** — per-alert-type configuration of email delivery
3. **Alert Rules** — per-rule threshold customisation (v2.2)
4. **Alert History** — evaluation audit log showing every rule evaluation (v2.2)

Users should be able to:
- Review recent alert notifications at a glance
- Mark individual notifications or all notifications as read
- Configure which alert types trigger email delivery
- Set custom thresholds for applicable alert rules
- Review a log of all alert rule evaluations and see which triggered
- Navigate between surfaces via sub-navigation

---

## Navigation & Routes

| Route | Page |
|-------|------|
| `/notifications` | Notification Feed (default Notifications view) |
| `/notifications/preferences` | Notification Preferences & Alert Rules |
| `/notifications/history` | Alert History (new — v2.2) |

All routes are accessible from a top-level **"Notifications"** nav item. The default landing is the Feed.

---

## Sub-Navigation

All pages share a sub-nav tab bar immediately below the page header:

| Tab | Route | Default active? |
|-----|-------|-----------------|
| Feed | `/notifications` | Yes |
| Preferences | `/notifications/preferences` | No |
| History | `/notifications/history` | No (new — v2.2) |

---

## Page 1: Notification Feed

### API Reference
- **Endpoint:** `GET /notifications` (returns list of notifications, newest first)
- **Mark read (one):** `PATCH /notifications/{id}` — sets `read: true`
- **Mark read (all):** `POST /notifications/mark-all-read`
- **Canonical contract:** `docs/specs/api_contracts/alerts_endpoints.md`

### Page Header
- H1: **"Notifications"**
- Right-aligned: **"Mark all as read"** — visible only when ≥1 unread item exists; calls `POST /notifications/mark-all-read`

### Notification List

Ordered newest first. Each item:

| Element | Description |
|---------|-------------|
| Alert type icon | Small icon distinguishing alert category |
| Alert title | e.g. `"Stop Loss Approach — AAPL"`, `"Market Regime Change: Risk-Off"`, `"Daily Portfolio Summary"` |
| Message body | One-line description of the event (sourced from API `message` field) |
| Timestamp | Relative time (e.g. `"2 hours ago"`); absolute datetime (ISO 8601) on hover |
| Unread indicator | Left-border accent (design system accent colour) on unread items; absent on read items |
| Mark as read button | Per-item; calls `PATCH /notifications/{id}`; removes unread indicator on success |

**Unread indicator:** 2px left-border in the design system accent colour. Read items render with neutral background and no border accent.

**Pagination:** 50 items per page. If more exist: **"Load more"** button at bottom of list (not infinite scroll).

### Mark as Read Behaviour
- Per-item: optimistic update (remove indicator immediately); revert on API error + inline message `"Failed to mark as read."` below the item.
- Mark all: optimistic update (remove all indicators); revert all on API error + toast `"Failed to mark all as read. Please try again."`

### States

#### Loading State
Skeleton rows (3–4 rows at standard notification height) while the feed loads.

#### Empty State
Displayed when no notifications exist:
- Bell outline icon (centred)
- Heading: **"No notifications yet."**
- Body: `"Alert notifications will appear here when triggered."`

#### All-Read State
All items render without unread indicators. "Mark all as read" is hidden. Feed remains fully browsable.

#### Error State
Full-width error panel: `"Unable to load notifications. Please refresh."`

---

## Page 2: Notification Preferences & Alert Rules

### API Reference
- **Endpoint:** `GET /notifications/preferences` (returns current per-type settings)
- **Update preferences:** `PATCH /notifications/preferences` (update one or more preference toggles)
- **Get alert rules:** `GET /alerts/rules` (returns configured alert rules including thresholds)
- **Create alert rule:** `POST /alerts/rules`
- **Update alert rule:** `PUT /alerts/rules/{id}`
- **Canonical contract:** `docs/specs/api_contracts/alerts_endpoints.md`

### Page Header
- H1: **"Notification Preferences"**
- Subtitle: `"Configure which alerts you receive by email, and set custom thresholds."`

### Section 1: Email Preferences

A list of alert types with per-type email toggle. No Save button — each toggle persists immediately via `PATCH /notifications/preferences`.

| Alert Type | Description | Email Toggle |
|------------|-------------|--------------|
| Stop Loss Approach | Notify when current stop is within threshold % of price | On / Off |
| Grace Period Warning | Notify on days 8–9 of the grace period | On / Off |
| Market Regime Change | Notify when market regime transitions to risk-off | On / Off |
| Daily Portfolio Summary | Receive a daily digest of portfolio status | On / Off |

**Toggle behaviour:**
- Optimistic update: toggle flips immediately on click.
- API call fires on toggle (150ms debounce).
- On success: brief inline **"Saved"** label adjacent to the toggled switch (fades after 2s).
- On error: revert toggle to prior state + inline error `"Failed to save preference. Please try again."` below the row.

**Loading state:** Skeleton rows (4 rows at preference-row height) while preferences load.

**Error state (load failure):** Inline error panel: `"Unable to load preferences. Please refresh."`

### Channel Scope
Email is the only delivery channel for v2.2. SMS is not rendered.

---

### Section 2: Alert Rule Thresholds (v2.2)

Displayed below the Email Preferences section under a sub-heading: **"Alert Thresholds"**.

#### Supported Threshold Types

| Alert Type | Threshold Label | Unit | Default | Validation |
|------------|----------------|------|---------|------------|
| Stop Loss Approach | "Notify when within ___ % of stop" | % (positive number) | 5 | Min: 0.1, Max: 50, 1 decimal place |
| Grace Period Warning | Fixed (days 8–9) | — | — | Not configurable |
| Market Regime Change | Event-triggered | — | — | Not configurable |
| Daily Portfolio Summary | None | — | — | Not configurable |

Only **Stop Loss Approach** renders a threshold input for v2.2. Threshold fields are rendered only for applicable types.

#### Alert Rule List

For each configured alert rule, display a row with:
- Alert type name (bold)
- Threshold display (muted text below the name):
  - If default: `"Within 5% of stop (default)"`
  - If custom: `"Within N% of stop"`
- Edit button (inline, right-aligned) — opens edit form inline or as an inline expand

For types without a configurable threshold: no threshold display is shown.

**Empty state (no rules configured):**
- Icon: bell with plus
- Heading: **"No alert rules configured."**
- Body: `"Add an alert rule to receive notifications."`
- CTA: **"Add alert rule"** button

#### Alert Rule Create / Edit Form

Appears inline (expanded row or section) when the user clicks "Add alert rule" or "Edit".

**Fields:**

| Field | Type | Notes |
|-------|------|-------|
| Alert type | Select / pre-set | Fixed to the rule being edited; or selectable on create |
| Threshold (if applicable) | Numeric input + "%" suffix | Label: "Notify when within ___ % of stop". Placeholder: current default value. Help: "Leave blank to use the default (5%)." |

**Threshold input validation (inline, on change):**

| Condition | Error message |
|-----------|--------------|
| Non-numeric value | "Please enter a valid number." |
| Value ≤ 0 | "Threshold must be greater than 0." |
| Value > 50 | "Threshold cannot exceed 50%." |
| Blank | Accepted — treated as "use default" |

Errors displayed inline below the threshold input. Form does not submit while errors are present.

**Save behaviour:**
- On success: rule list refreshes; updated threshold displayed in the list.
- On error: inline error above the save button: `"Failed to save alert rule. Please try again."`

**Default value behaviour:**
- Blank / cleared field → system default (5%) is applied.
- Placeholder shows the current default so users know what they are overriding.
- Edit form pre-fills with the existing threshold value from the API.

---

## Page 3: Alert History (v2.2)

### API Reference
- **Endpoint:** `GET /alerts/history` (evaluation log; supports `last_n_days` or `last_n_records` query params)
- **Canonical contract:** `docs/specs/api_contracts/alerts_endpoints.md`

### Page Header
- H1: **"Alert History"**
- Subtitle: `"A log of every alert rule evaluation by the system."`

### Alert History Table

#### Columns

| Column | Source field | Format |
|--------|-------------|--------|
| Date / Time | `evaluation_timestamp` | `YYYY-MM-DD HH:mm` (local time); full ISO on hover |
| Alert Type | `rule_type` | Human-readable label (see mapping below) |
| Symbol | `symbol` | Uppercase ticker, or `—` if not symbol-specific |
| Triggered | `triggered` | `true` → "Yes" (amber badge); `false` → "No" (grey badge) |
| Notified | `notification_sent` | `true` → "Yes" (green badge); `false` → "No" (grey badge) |
| Values | `values_compared` | Compact key-value summary; truncated to fit; full detail on row expand |

**Rule type display labels:**

| API value | Display label |
|-----------|--------------|
| `stop_loss_approach` | Stop Loss Approach |
| `grace_period_warning` | Grace Period Warning |
| `market_regime_change` | Market Regime Change |
| `daily_portfolio_summary` | Daily Portfolio Summary |
| Unknown | Raw value (fallback) |

#### Sort

- **Default:** newest first (descending `evaluation_timestamp`)
- **User-controllable:** Date / Time column header toggle (ascending / descending)
- Active sort direction indicated by up/down arrow on column header

#### Filter

Rule type filter above the table (right-aligned):

```
Label: "Filter by type:"
Control: Dropdown / select
Options: All types (default) | Stop Loss Approach | Grace Period Warning | Market Regime Change | Daily Portfolio Summary
```

Selecting a type filters rows. "All types" clears the filter. Active filter reflected in the dropdown selection.

#### Pagination

- Default window: last 30 days or last 200 records (whichever is smaller)
- **"Load more"** button at bottom of table fetches next window
- No infinite scroll

#### Row Expand — Values Detail

Clicking any row expands it inline to show full `values_compared` map as key: value list (no modal). Example:

```
▼ Stop Loss Approach — AAPL — 2026-03-21 16:30
  stop_price:        $42.10
  current_price:     $43.50
  gap_pct:           3.3%
  threshold_pct:     5.0%
  triggered:         Yes
  notification_sent: Yes
```

Click again to collapse.

#### States

**Loading state:** Skeleton rows (5 rows at standard table-row height).

**Empty state — no records:**
- Heading: **"No alert history yet."**
- Body: `"Alert evaluations will appear here once the system has run."`

**Empty state — filter applied, no matches:**
- Body: `"No evaluations found for the selected alert type."`
- Link: "Clear filter" (resets to All types)

**Error state:** Full-width error panel: `"Unable to load alert history. Please refresh."`

---

## Constraints

- The notification feed is read-only — users cannot delete individual notifications.
- The notification feed reflects state at page load. No real-time push updates.
- Notifications older than 90 days may be excluded by the backend; the frontend accepts whatever the API returns.
- Alert history is an audit log — users cannot delete evaluation records.
- Alert history reflects state at page load. No real-time push updates.
- There is a single user; no multi-user or role-based preference scoping.

---

## Known Deviations

### DEV-EPIC02-ST04-01 — Alert Thresholds empty state: missing "Add alert rule" CTA button

- **Description:** The v2.2 implementation of `AlertThresholdsSection` renders the empty state icon, heading ("No alert rules configured."), and body text but omits the "Add alert rule" CTA button specified in §Section 2. In practice this state is effectively unreachable — `GET /alerts/rules` auto-seeds rules on first use, so the empty state is only reachable if all rules have been manually deleted.
- **Canonical requirement:** §Section 2 Empty state must include a CTA button labelled "Add alert rule".
- **Priority:** P3
- **Target resolution release:** v2.3
- **Owner:** Base44 Frontend Prompt Owner
- **Backlog reference:** To be filed as BLG-FE item at next roadmap rebalance.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.2 | 2026-03-22 | v2.2 additions: Section 2 (Alert Rule Thresholds — ST-04) and Page 3 (Alert History — ST-05). Sub-nav extended with "History" tab. Purpose & Goals, routes, and constraints updated. Design sources: `docs/design/2026-03-21__release-v2.2/alert-threshold-customisation/ux_spec.md` and `docs/design/2026-03-21__release-v2.2/alert-history-table/ux_spec.md`. Approved by Product Owner 2026-03-22. Confirmed compliant by Head of Specs Team. |
| 0.1 | 2026-03-18 | Initial spec. ST-05 (notification preferences page) + ST-06 (in-app notification feed). Design gate: 2026-03-18__release-v2.1. Design source: UX specs approved by Product Owner 2026-03-18. |
