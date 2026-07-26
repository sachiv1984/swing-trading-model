**Owner:** QA & Testing Owner
**Class:** Class 2
**Status:** Canonical
**Version:** 0.2
**Last Updated:** 2026-07-26
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Sprint Item:** ST-10 — EPIC-04 (v2.3)
**Spec Ref:** docs/specs/frontend/pages/notifications.md §Nav Alert Badge v0.3
**Design Source:** docs/design/2026-03-24__release-v2.3/alert-nav-badge/ux_spec.md

---

# Alert Notification Badge in Nav — Test Scenarios (ANB)

## Purpose

Test scenarios covering the unacknowledged alert count badge on the Alerts nav item in the Tools sidebar group, introduced in ST-10 (BLG-FE-05, v2.3).

**Automated coverage:** SC-ANB-01 through SC-ANB-08 (Playwright) cover non-visual AC — Alerts item presence, badge count accuracy, last-visit filtering, clear on Alerts page visit, 99+ cap, and nav regression. See `tests/e2e/alert-nav-badge.spec.js`.

**Visual scenarios SC-ANB-VIS-01 through SC-ANB-VIS-05** require DoQ manual staging or local-run review. Observable UI behaviour (badge colour, positioning, typography, collapsed group header) cannot be asserted by Playwright alone.

---

## Playwright Scenarios

| Scenario | Description | File |
|----------|-------------|------|
| SC-ANB-01 | Alerts nav item visible in Tools group | alert-nav-badge.spec.js |
| SC-ANB-02 | Badge hidden when history is empty | alert-nav-badge.spec.js |
| SC-ANB-03 | Badge shows full count when no prior Alerts visit | alert-nav-badge.spec.js |
| SC-ANB-04 | Badge counts only evals after last-visit timestamp | alert-nav-badge.spec.js |
| SC-ANB-05 | Badge clears on Alerts page navigation | alert-nav-badge.spec.js |
| SC-ANB-06 | Badge persists across non-Alerts page navigation | alert-nav-badge.spec.js |
| SC-ANB-07 | Badge shows "99+" when count > 99 | alert-nav-badge.spec.js |
| SC-ANB-08 | No regression — existing nav items present | alert-nav-badge.spec.js |

---

## Visual Scenarios — DoQ Manual Review Required

### SC-ANB-VIS-01 — Badge appearance: red circle, white count, top-right of icon

**Precondition:** Unacknowledged alerts exist (mock or real `GET /alerts/history` returns ≥ 1 evaluation; no `alerts-last-visit` in sessionStorage, or last visit predates evaluations).

**Steps:**
1. Navigate to any page that is not the Alerts/Notifications page (e.g., `/watchlist`)
2. Expand the Tools nav group if collapsed
3. Observe the Alerts nav item

**Expected:**
- Red filled circle (`bg-red-600`, updated v0.2 EPIC-03/ST-03 v7.8 — `bg-red-500` gave white-on-red contrast of 3.76:1, below the WCAG AA 4.5:1 normal-text threshold; `bg-red-600` gives 4.83:1) overlaid at the top-right corner of the Bell icon
- White count number centred inside the circle
- Circle is small (~14×14px) and does not obscure the icon or label text
- Count renders correctly (e.g., "3" for 3 unacknowledged alerts)

**Cannot be verified by Playwright:** badge colour, circle sizing, exact positioning.

---

### SC-ANB-VIS-02 — Badge hidden when count = 0

**Precondition:** No unacknowledged alerts (either history is empty, or `alerts-last-visit` is set to a timestamp after all evaluations).

**Steps:**
1. Navigate to Alerts page (`/notifications`) to clear the badge (sets `alerts-last-visit`)
2. Navigate to Watchlist
3. Observe the Alerts nav item in the Tools group

**Expected:**
- No badge visible on the Alerts nav item
- Bell icon appears clean, no overlay circle

**Cannot be verified by Playwright:** absence of rendered badge circle at pixel level.

---

### SC-ANB-VIS-03 — "99+" display for counts exceeding 99

**Precondition:** `GET /alerts/history` returns 100+ evaluations; no `alerts-last-visit` in sessionStorage.

**Steps:**
1. Navigate to Watchlist
2. Observe the Alerts nav item badge

**Expected:**
- Badge shows "99+" (not "100" or a truncated number)
- "99+" text legible in the badge circle — font size may be slightly smaller than numeric-only badges to fit
- Badge circle remains the same visual size as lower-count badges

---

### SC-ANB-VIS-04 — Tools group header badge when group is collapsed

**Precondition:** Unacknowledged alerts exist. Tools group is collapsed (user has manually collapsed it or it is not the active group).

**Steps:**
1. Navigate to a page in a non-Tools group (e.g., Positions, in the Trading group)
2. Ensure Tools group is collapsed
3. Observe the Tools group header row

**Expected:**
- A red badge appears inline after the "Tools" label in the group header
- Badge shows the unacknowledged count (or "99+" if > 99)
- Badge disappears from the header once Tools group is expanded (badge on Alerts item becomes visible instead)
- Collapsing/expanding the group toggles badge between header and item consistently

**Cannot be verified by Playwright:** badge colour in group header, exact inline position.

---

### SC-ANB-VIS-05 — No nav layout regression

**Precondition:** Both alertCount = 0 and alertCount > 0 states tested.

**Steps:**
1. Navigate to each main page (Dashboard, Positions, Watchlist, Analytics, Settings)
2. In both badge-present and badge-absent states, observe the full sidebar nav

**Expected:**
- All existing nav items remain in their original groups and order:
  - Trading: Positions, Trade Entry, Trade History, Reflections
  - Analytics: Analytics, Risk Dashboard, Signals, Reports
  - Tools: Watchlist, **Alerts** (new — ST-10)
  - System: Settings, System Status, Notifications
  - Dashboard (ungrouped, top)
- Adding the Alerts item to Tools does not shift Watchlist or any other item
- Active group auto-expansion still works correctly for all pages
- Adding a badge to the Alerts item does not affect icon alignment or label position on any other nav item

---

## Coverage Gap Note

This scenario file addresses the EPIC-04 test scenario gap flagged at sprint planning seal (2026-03-24). The EPIC-04 gap covers ST-10 (alert badge), ST-11 (empty state CTA — already filed separately in `alert_thresholds_empty_state_scenarios.md`), ST-12 (loading states — filed in loading states test suite), and ST-13 (sidebar nav groups). ST-13 visual scenarios remain pending — a separate scenario file should be authored before the next sprint on this domain.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-27 | Initial version. ST-10 (BLG-FE-05, v2.3): Playwright scenarios SC-ANB-01–08 and visual scenarios SC-ANB-VIS-01–05. Addresses EPIC-04 test scenario gap from sprint planning 2026-03-24. |
| 0.2 | 2026-07-26 | ST-03 (EPIC-03, v7.8, BLG-FE-127) notification accessibility audit: badge colour changed `bg-red-500` → `bg-red-600` (white-on-red contrast 3.76:1 → 4.83:1, WCAG AA 4.5:1 threshold). SC-ANB-VIS-01 updated to the new token. `tests/e2e/alert-nav-badge.spec.js` selectors updated in the same commit (cross-spec selector check). |
