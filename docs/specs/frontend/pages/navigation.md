**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-04-25
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

## Keyboard Shortcuts

**Design source:** docs/design/2026-04-25__release-v3.0/keyboard-shortcuts/ux_spec.md
**Release:** v3.0 — ST-11 (BLG-FE-19)

Global keyboard shortcuts are available on applicable pages. Shortcuts fire on document-level `keydown` events and are suppressed when focus is inside a `<input>`, `<textarea>`, or `<select>` element (check `document.activeElement.tagName` before acting).

**Available shortcuts:**

| Key | Action | Applicable Pages |
|-----|--------|-----------------|
| `n` | Open new position form/modal | Positions, Trade History |
| `w` | Add-to-watchlist trigger | Watchlist, Screener Results |
| `r` | Refresh / reload page data | All pages with a primary data endpoint |

**Shortcut reference hint — sidebar footer:**

- Location: bottom of the left sidebar panel, below all nav group items
- Section label: "Shortcuts" in uppercase small-caps, secondary muted colour (consistent with nav group headers)
- Each row: monospace key label as a small chip (light background, rounded, border) + action label in secondary typography
- Dynamic filtering: show only shortcuts applicable to the current page; hide the section entirely when no shortcuts apply to the current page
- Responsive: hidden on mobile collapsed sidebar (shortcuts remain active; reference not shown)

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-04-25 | ST-11 (BLG-FE-19, v3.0): §Keyboard Shortcuts added — global shortcuts (n/w/r), suppression rule for text inputs, sidebar footer hint design. Design source: docs/design/2026-04-25__release-v3.0/keyboard-shortcuts/ux_spec.md. Head of UX & Design + Product Owner approved. Design gate: 2026-04-25__release-v3.0. Head of Specs Team confirmed. |
| 1.0 | 2026-03-24 | Initial version. ST-13 (BLG-UX-01, v2.3): collapsible section groups with 4 groups (Trading, Analytics, Tools, System). Product Owner design decision 2026-03-24. Design source: docs/design/2026-03-24__release-v2.3/sidebar-nav-groups/ux_spec.md. Design gate: 2026-03-24__release-v2.3. |
