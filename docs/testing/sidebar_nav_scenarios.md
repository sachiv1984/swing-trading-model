**Owner:** QA & Testing Owner
**Class:** Class 2
**Status:** Canonical
**Version:** 0.1
**Last Updated:** 2026-03-29
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Sprint Item:** ST-13 — EPIC-04 (v2.3)
**Spec Ref:** docs/specs/frontend/pages/navigation.md v1.0
**Design Source:** docs/design/2026-03-24__release-v2.3/sidebar-nav-groups/ux_spec.md

---

# Sidebar Navigation Groups — Test Scenarios (SNV)

## Purpose

Test scenarios covering the collapsible group sidebar navigation introduced in ST-13 (BLG-UX-01, v2.3). Groups organise nav items into labelled, collapsible sections with active-group auto-expansion and sessionStorage persistence.

**Visual scenarios SC-SNV-VIS-01 through SC-SNV-VIS-08** require DoQ manual staging or local-run review. Group collapse animation, chevron rendering, typography, sessionStorage persistence, and badge propagation to collapsed group headers cannot be asserted by automated tests alone.

---

## Group Structure Under Test

| Group | Items |
|-------|-------|
| **Trading** | Positions, Trade History, Trade Reflection |
| **Analytics** | Analytics, Risk Dashboard, Signals |
| **Tools** | Watchlist, Alerts |
| **System** | Settings, System Status, Notifications |

Dashboard sits ungrouped at the top.

---

## Visual Scenarios — DoQ Manual Review Required

### SC-SNV-VIS-01 — Default state: active group expanded, all others collapsed

**Precondition:** Fresh page load (sessionStorage cleared, or first visit).

**Steps:**
1. Navigate to `/positions` (a Trading group item)
2. Observe the full sidebar

**Expected:**
- Dashboard link visible at the top, ungrouped
- **Trading** group expanded — Positions, Trade History, Trade Reflection all visible
- **Analytics**, **Tools**, **System** groups collapsed — only their group header rows visible
- No nav item links from non-active groups are visible
- Positions item highlighted as active

---

### SC-SNV-VIS-02 — Group header design: label, chevron, styling

**Precondition:** At least one group is collapsed and one is expanded.

**Steps:**
1. Navigate to `/positions`
2. Observe the collapsed group headers (Analytics, Tools, System) and the expanded group header (Trading)

**Expected:**
- Group labels rendered in uppercase, muted/secondary colour (e.g. muted grey)
- Chevron visible right-aligned in each group header row
- Collapsed groups: chevron points right (▶)
- Expanded group: chevron points down (▼)
- Clicking anywhere on a collapsed group header row expands that group (not just the chevron)

---

### SC-SNV-VIS-03 — User can expand and collapse non-active groups

**Precondition:** On a Trading page (e.g. Positions). Analytics group is collapsed.

**Steps:**
1. Click the Analytics group header
2. Observe Analytics group expands — Analytics, Risk Dashboard, Signals visible
3. Click the Analytics group header again
4. Observe Analytics group collapses

**Expected:**
- Expand: items animate open, chevron rotates to ▼
- Collapse: items animate closed, chevron rotates to ▶
- Active group (Trading) remains expanded throughout; its chevron does not change

---

### SC-SNV-VIS-04 — Active group cannot be collapsed while on that page

**Precondition:** On the Positions page (Trading group).

**Steps:**
1. Click the Trading group header
2. Observe

**Expected:**
- Trading group does not collapse
- Items remain visible
- Chevron remains ▼

---

### SC-SNV-VIS-05 — Active group auto-expands on page navigation

**Precondition:** Analytics group is collapsed. Currently on Positions (Trading).

**Steps:**
1. Expand Analytics group manually
2. Navigate to Risk Dashboard (Analytics group item)
3. Observe sidebar

**Expected:**
- Analytics group is expanded and Risk Dashboard is highlighted as active
- Trading group collapses (was previously active)
- Chevrons update accordingly

---

### SC-SNV-VIS-06 — sessionStorage persistence across in-session navigation

**Precondition:** On Positions. Tools group manually expanded by user.

**Steps:**
1. Expand Tools group (click header)
2. Navigate to Trade History (still in Trading group)
3. Navigate back to Positions
4. Observe Tools group state

**Expected:**
- Tools group remains expanded — user's manual expansion persisted in sessionStorage
- Active group (Trading) remains expanded as always

---

### SC-SNV-VIS-07 — sessionStorage resets on full page reload

**Precondition:** On Positions. Tools group manually expanded. Analytics group manually expanded.

**Steps:**
1. Expand Tools and Analytics groups
2. Hard-reload the page (Cmd/Ctrl + Shift + R)
3. Observe sidebar

**Expected:**
- Only Trading group (active) is expanded
- Tools and Analytics return to collapsed (default state)
- Manual expansions do not survive a full reload

---

### SC-SNV-VIS-08 — No nav layout regression: all items present and routable

**Precondition:** None.

**Steps:**
1. Expand each group in turn and confirm all items are visible:
   - Trading: Positions, Trade History, Trade Reflection
   - Analytics: Analytics, Risk Dashboard, Signals
   - Tools: Watchlist, Alerts
   - System: Settings, System Status, Notifications
2. Click each item and confirm navigation to the correct page (no broken routes)
3. Confirm Dashboard link at top navigates to dashboard

**Expected:**
- All 12 items present and in correct groups
- Dashboard ungrouped at top
- No items duplicated or missing
- All routes resolve without errors

---

## Coverage Gap Addressed

This document addresses the ST-13 test scenario gap flagged at sprint planning seal (2026-03-24) and noted in the ST-13 `execution_state.json` entry. The visual test scenarios cover the primary AC in `docs/specs/frontend/pages/navigation.md` (collapse behaviour, group header design, active group enforcement, sessionStorage persistence, regression).

Badge propagation to a collapsed Tools group header (spec §Alert Badge Integration) is covered visually by **SC-ANB-VIS-04** in `docs/testing/alert_nav_badge_scenarios.md` — not duplicated here.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-29 | Initial version. ST-13 (BLG-UX-01, v2.3): visual scenarios SC-SNV-VIS-01–08 covering group structure, collapse behaviour, header design, sessionStorage persistence, and nav regression. Addresses EPIC-04 test scenario gap. |
