**Owner:** Head of UX & Design
**Status:** Approved
**Approved by:** Product Owner
**Approved date:** 2026-03-18
**Cycle:** 2026-03-18__release-v2.1
**Items:** ST-06
**Frontend spec target:** docs/specs/frontend/pages/notifications.md (new — shared with ST-05 spec)

---

# UX Spec — In-App Notification Feed (ST-06)

## 1. Purpose & User Goal

The user needs visibility of alert events that occurred while they were away from the application. The in-app feed is a secondary record — email is the primary delivery channel — but provides a quick glance at what has triggered.

**User goal:** Review recent alerts at a glance and dismiss those that have been actioned.

---

## 2. Navigation & Placement

- Accessible from the main navigation as **"Notifications"** → default sub-item **"Feed"** (or the top-level "Notifications" link lands on the feed directly).
- Route: `/notifications` (feed is the default notifications view; preferences are at `/notifications/preferences`).
- Page title: **"Notifications"**

---

## 3. Layout

### 3.1 Page Header
- H1: **"Notifications"**
- Right-aligned action: **"Mark all as read"** link/button (visible only when one or more unread items exist).
- Sub-nav tabs: **"Feed"** (active) | **"Preferences"** (links to `/notifications/preferences`).

### 3.2 Notification List

An ordered list of notification items, newest first.

**Each notification item contains:**
- **Alert type icon** — small icon distinguishing alert category (stop loss, grace period, regime, daily summary)
- **Alert title** — e.g. `"Stop Loss Approach — AAPL"`, `"Regime Change: Risk-Off"`, `"Daily Summary"`
- **Message body** — one-line description of the event (e.g. `"Current stop ($148.20) is within 3.1% of price ($152.80)"`)
- **Timestamp** — relative time (e.g. `"2 hours ago"`) with absolute datetime on hover
- **Read/unread indicator** — unread items have a left-border accent (blue stripe or equivalent design system colour); read items are visually neutral
- **Mark as read button** — small secondary action on each item; clicking marks that item read and removes the unread indicator

### 3.3 Read/Unread State
- Unread items render with a distinct left-border accent.
- On click of "Mark as read" (per-item): item transitions to read state (accent removed); API call to update read status.
- "Mark all as read": transitions all visible items to read state in one API call.
- If API call fails: revert visual state and show inline error.

### 3.4 Pagination / Scroll
- Show the 50 most recent notifications on initial load.
- If more than 50 exist: "Load more" button at bottom of list (not infinite scroll — the list is not high-volume for a single-user system).

---

## 4. States

### 4.1 Loading State
- Skeleton notification rows (3–4 rows at standard height) while the feed loads.

### 4.2 Empty State
- Displayed when no notifications exist:
> **"No notifications yet."**
> "Alert notifications will appear here when triggered."
- A muted icon (bell outline) centred above the message.

### 4.3 All-Read State
- All items render without unread indicators. "Mark all as read" button is hidden.
- Feed is still fully visible — read items remain browsable.

### 4.4 Error State
- If feed cannot be loaded: full-width error panel: "Unable to load notifications. Please refresh."

---

## 5. Constraints

- The feed is read-only — users cannot delete individual notifications (deletion is out of scope for v2.1).
- Notifications older than 90 days may be excluded by the backend; the frontend does not need to handle this explicitly (the API returns what it returns).
- Real-time updates (WebSocket push) are out of scope; the feed reflects the state at page load. Users refresh to see new notifications.

---

## 6. UX Decisions Recorded

| Decision | Rationale |
|----------|-----------|
| Feed as default Notifications view | Most common intent when visiting /notifications is to see recent events, not adjust preferences |
| No real-time push | System operates on daily decision cadence (strategy_rules.md §13); real-time streaming is out of scope |
| Read indicator via left-border accent | Non-intrusive; border colour distinguishes state without requiring a separate badge count column |
| No notification deletion | Single-user context; the list will not grow large enough to warrant management; simplicity preferred |
| "Load more" not infinite scroll | Prevents accidental infinite load; volume is predictable and low |
