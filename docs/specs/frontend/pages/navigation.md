**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-03-24
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source:** docs/design/2026-03-24__release-v2.3/sidebar-nav-groups/ux_spec.md
**Confirmed by:** Head of Specs Team — 2026-03-24
**Release:** v2.3 — ST-13 (BLG-UX-01)

---

# Frontend Specification — Sidebar Navigation

## Purpose

Defines the left sidebar navigation structure, including the collapsible group model introduced in v2.3 (BLG-UX-01). The sidebar appears on all pages.

## Group Structure

| Group Label | Nav Items |
|-------------|-----------|
| **Trading** | Positions, Trade History, Trade Reflection |
| **Analytics** | Analytics, Risk Dashboard, Signals |
| **Tools** | Watchlist, Alerts |
| **System** | Settings, System Status, Notifications |

All existing routes are preserved. No items removed.

## Collapse Behaviour

- **Default:** Active group expanded; all others collapsed
- **Active group:** the group containing the current page's nav item — always expanded; user cannot collapse it while on that page
- **Non-active groups:** user can toggle expand/collapse by clicking the group header
- **Persistence:** collapse state in `sessionStorage`; resets to default on full page reload

## Group Header

- Label: uppercase small caps, secondary colour (muted grey)
- Collapse indicator: chevron right-aligned (▶ collapsed / ▼ expanded)
- Click target: entire group header row

## Active Item

Active nav item retains existing highlight styling (no change from pre-v2.3 behaviour).

## Alert Badge Integration (ST-10 BLG-FE-05)

When the **Tools** group is collapsed and unacknowledged alerts exist:
- The badge count propagates to the Tools group header row (e.g. "Tools [2]" or badge overlay on the group chevron)
- When Tools is expanded, badge appears on the Alerts item directly

## Responsive Behaviour

- On narrow screens (< breakpoint): sidebar remains collapsible (hamburger or slide-in); group collapse state preserved within the session
- No change to existing mobile nav behaviour beyond the group structure

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-24 | Initial version. ST-13 (BLG-UX-01, v2.3): collapsible section groups with 4 groups (Trading, Analytics, Tools, System). Product Owner design decision 2026-03-24. Design source: docs/design/2026-03-24__release-v2.3/sidebar-nav-groups/ux_spec.md. Design gate: 2026-03-24__release-v2.3. |
