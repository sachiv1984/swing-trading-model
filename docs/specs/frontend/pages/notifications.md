**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.1
**Last Updated:** 2026-03-18
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source:** docs/design/2026-03-18__release-v2.1/notification-feed/ux_spec.md | docs/design/2026-03-18__release-v2.1/notification-preferences/ux_spec.md

---

# notifications.md — Notifications (Feed & Preferences)

## Purpose & User Goals

The Notifications section covers two surfaces:
1. **Notification Feed** — a chronological list of alert events triggered by the system
2. **Notification Preferences** — per-alert-type configuration of email delivery

Users should be able to:
- Review recent alert notifications at a glance
- Mark individual notifications or all notifications as read
- Configure which alert types trigger email delivery
- Navigate between the feed and preferences via sub-navigation

---

## Navigation & Routes

| Route | Page |
|-------|------|
| `/notifications` | Notification Feed (default Notifications view) |
| `/notifications/preferences` | Notification Preferences |

Both routes are accessible from a top-level **"Notifications"** nav item. The default landing is the Feed.

---

## Sub-Navigation

Both pages share a sub-nav tab bar immediately below the page header:

| Tab | Route | Default active? |
|-----|-------|-----------------|
| Feed | `/notifications` | Yes |
| Preferences | `/notifications/preferences` | No |

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

## Page 2: Notification Preferences

### API Reference
- **Endpoint:** `GET /notifications/preferences` (returns current per-type settings)
- **Update:** `PATCH /notifications/preferences` (update one or more preference toggles)
- **Canonical contract:** `docs/specs/api_contracts/alerts_endpoints.md`

### Page Header
- H1: **"Notification Preferences"**
- Subtitle: `"Configure which alerts you receive by email."`

### Preferences Table

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
Email is the only delivery channel for v2.1. SMS is not rendered.

---

## Constraints

- The feed is read-only — users cannot delete individual notifications.
- The feed reflects state at page load. No real-time push updates (refresh to see new notifications).
- Notifications older than 90 days may be excluded by the backend; the frontend accepts whatever the API returns.
- There is a single user; no multi-user or role-based preference scoping.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-18 | Initial spec. ST-05 (notification preferences page) + ST-06 (in-app notification feed). Design gate: 2026-03-18__release-v2.1. Design source: UX specs approved by Product Owner 2026-03-18. |
