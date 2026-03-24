**Owner:** Head of UX & Design
**Status:** Approved
**Approved by:** Product Owner — 2026-03-24
**Cycle:** 2026-03-24__release-v2.3
**Story:** ST-10 (BLG-FE-05)

---

# UX Spec — Alert Notification Badge in Nav

## Placement

Small badge/pill overlaid on the "Alerts" nav item in the left sidebar.

## Badge Design

- Red filled circle with white count number
- Count: unacknowledged alert count (alerts since last visit to Alerts page)
- Max display: 99+ if count > 99
- Position: top-right corner of the Alerts nav icon/label

## Clear behaviour

- Badge disappears (count resets to 0) when user navigates to the Alerts page
- Persistence: count persists across page navigation until Alerts is visited
- Storage: frontend-managed (local state or sessionStorage); does not require a backend acknowledged/unacknowledged endpoint

## States

- **Count = 0:** badge hidden entirely
- **Count 1–99:** badge shown with count
- **Count > 99:** badge shows "99+"

## Data source

Reads from alert history data (`GET /alerts/history` or equivalent) — counts records added since last visit. Backend BLG-FEAT-12 (v2.2) provides the history table; this badge reads from it.

## Constraints

- Display-only. No automated action triggered.
- No regression to existing nav layout or item order.
