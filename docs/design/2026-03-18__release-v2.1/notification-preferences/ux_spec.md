**Owner:** Head of UX & Design
**Status:** Approved
**Approved by:** Product Owner
**Approved date:** 2026-03-18
**Cycle:** 2026-03-18__release-v2.1
**Items:** ST-05
**Frontend spec target:** docs/specs/frontend/pages/notifications.md (new)

---

# UX Spec — Notification Preferences Page (ST-05)

## 1. Purpose & User Goal

The user needs to control which alerts they receive and how, without wading through general application settings. This is a focused configuration surface.

**User goal:** Turn specific alert types on or off, and choose delivery channels (email; SMS is out of scope for v2.1 per single-user, self-hosted deployment context per strategy_rules.md §13).

---

## 2. Navigation & Placement

- Accessible from the main navigation as **"Notifications"** → sub-item **"Preferences"**, or from a direct link in the notification feed header.
- Route: `/notifications/preferences` (or `/settings/notifications` if the engineering team prefers co-location with Settings — either is acceptable; consistency with the nav structure is the constraint).
- Page title: **"Notification Preferences"**

---

## 3. Layout

### 3.1 Page Header
- H1: **"Notification Preferences"**
- Subtitle: **"Configure which alerts you receive by email."**
- No period selector (preferences are global, not period-scoped).

### 3.2 Alert Type Table

A list of alert types, each with:
- **Alert name** (left)
- **Description** (below name, muted text, 1 line)
- **Email toggle** (right — on/off switch)

| Alert Type | Description |
|------------|-------------|
| Stop Loss Approach | Notify when current stop is within threshold % of price |
| Grace Period Warning | Notify on days 8–9 of the grace period |
| Market Regime Change | Notify when market regime transitions to risk-off |
| Daily Portfolio Summary | Receive a daily digest of portfolio status |

### 3.3 Toggle Behaviour
- Toggles are independent per alert type.
- Toggling immediately calls the API (PATCH preference endpoint) — no "Save" button required; optimistic UI update.
- On API error: revert the toggle to its prior state and show an inline error message below the row: `"Failed to save preference. Please try again."`
- Loading state: the toggled switch shows a brief spinner overlay (150ms debounce before API call).

### 3.4 Save Confirmation
- On successful save: brief inline confirmation ("Saved" in muted text, fades after 2s) adjacent to the toggled control.
- No page-level toast — keep feedback local to the changed control.

---

## 4. States

### 4.1 Loading State
- Skeleton rows (same width as the alert type list) while preferences fetch from the API.

### 4.2 Empty / Error State
- If preferences cannot be loaded: inline error panel with "Unable to load preferences. Please refresh."

### 4.3 All Off State
- No special warning — users are allowed to disable all alerts.

---

## 5. Constraints

- Email is the only delivery channel for v2.1. SMS toggle is not rendered.
- Preference state is per-user. There is a single user in this deployment — no multi-user considerations.
- The frontend must not cache stale preference state between sessions; always load fresh on page mount.

---

## 6. UX Decisions Recorded

| Decision | Rationale |
|----------|-----------|
| No global Save button | Optimistic per-toggle saves reduce friction; the preference list is short enough that accidental saves are recoverable by re-toggling |
| Email only (no SMS) | Single-user, self-hosted context — SMS infrastructure out of scope per strategy_rules.md §13 and ADR-003 decision scope |
| Inline error (not toast) | Error feedback must be co-located with the failed action so the user knows which preference failed |
| Notification Preferences as standalone route | Separation from Settings page keeps the UX intent clear; preferences are notification-scoped, not general settings |
