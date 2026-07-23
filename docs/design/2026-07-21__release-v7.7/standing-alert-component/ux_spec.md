**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Approved
**Last Updated:** 2026-07-21
**Cycle:** 2026-07-21__release-v7.7
**Story:** ST-04 (EPIC-04, BLG-FE-120)

---

# UX Decision Record — Shared Standing Alert Component

## 1. Problem

The app currently has one alert-style primitive: transient toasts (`sonner`, `src/components/ui/sonner.js` / `use-toast.js`), used for short-lived system feedback (e.g. "Failed to mark all as read. Please try again."). There is no primitive for a condition that needs to remain visible until the user acknowledges it — a toast that auto-dismisses after ~4s is unsuitable for something like a triggered custom price alert, which the user may miss if not looking at the screen at that moment.

`BLG-FE-116` (custom price alerts, shipped v7.5) is the near-term consumer: today, a triggered custom alert only appears as a row in the Notification Feed (`notifications.md` §"Custom Price Alerts (v7.5)") — there is no in-the-moment surface. ST-04 builds the primitive; wiring it into live alert evaluation is `BLG-FE-116`'s own future scope (RISK-03, out of this release).

## 2. Component: `StandingAlert`

### Distinction from Toast

| | Toast (`sonner`) | `StandingAlert` |
|---|---|---|
| Dismissal | Auto-dismiss (~4s) | Manual only (explicit ✕), or programmatic clear when the underlying condition resolves |
| Position | Floating, corner-anchored, overlays content | Inline banner, in document flow (does not overlay content) |
| Use case | Transient system feedback (success/error confirmations for an action just taken) | A condition requiring sustained user awareness until acknowledged |
| Stacking | Library-managed stack | Parent-owned array; component renders what it's given |

### Layout

Full-width banner, rendered at the top of the page content area, below `PageHeader` and above the page's primary content. Left-to-right: severity icon, message text, optional action link, dismiss `✕` (right-aligned).

### Severity variants

Reuses existing design-system semantic colours (no new palette):

| Severity | Icon | Background/border (light + dark pair) |
|----------|------|-----------------------------------------|
| Info | `Info` | `bg-blue-50 border-blue-200 text-blue-800` / `dark:bg-blue-950 dark:border-blue-800 dark:text-blue-200` |
| Warning | `AlertTriangle` | `bg-amber-50 border-amber-200 text-amber-800` / `dark:bg-amber-950 dark:border-amber-800 dark:text-amber-200` |
| Critical | `AlertOctagon` | `bg-red-50 border-red-200 text-red-800` / `dark:bg-red-950 dark:border-red-800 dark:text-red-200` |

Per Card Hierarchy precedent (`design_system.md`), any new background/border token ships as an explicit light+dark pair from the start — no dark-only class.

### Stacking

Parent component owns the active-alerts array (not a global store, unlike toasts) and passes it to a `StandingAlertStack` wrapper. Stack renders newest-first, vertically. Cap at 3 visible; beyond that, a trailing summary row: **"+N more"** (click expands the rest inline — no modal).

### Dismissal

- Manual: `✕` calls `onDismiss(id)`. Optimistic removal, no undo.
- Programmatic: parent may clear an alert when its underlying condition resolves (e.g. a price alert's threshold is no longer crossed) — same `onDismiss(id)` path.
- Not persisted across page reload — this is an in-session surface, distinct from the persisted Notification Feed row, which remains the durable record.

### Accessibility

`role="alert"`, `aria-live="polite"` for Info/Warning, `aria-live="assertive"` for Critical. Dismiss button has `aria-label="Dismiss alert"`.

## 3. Integration Point (AC requirement)

**Identified integration point:** the Notification Feed page (`/notifications`, top of content area, above the notification list) is the landing zone for `BLG-FE-116`'s future live-evaluation work — when a custom price alert triggers while the user is already in-app, it renders as a `StandingAlert` here in addition to (not instead of) the persisted Feed row. This gives `BLG-FE-116` a concrete, already-specified slot rather than needing its own layout decision when it picks the primitive up.

No other page wires `StandingAlert` in this cycle — EPIC-04's own scope is the component and its documentation, not this integration (RISK-03).

## 4. Constraints

- No new backend endpoint or schema — purely a frontend presentational primitive; the array of active alerts is supplied by whatever future feature consumes it (client-side state).
- Must not visually collide with existing page-level error banners (`DataState` error branch) — `StandingAlert` sits above the page's main content region; `DataState` errors remain scoped to their own content area.

## 5. Approval

Product Owner: approved 2026-07-21.
Head of UX & Design: approved 2026-07-21.
