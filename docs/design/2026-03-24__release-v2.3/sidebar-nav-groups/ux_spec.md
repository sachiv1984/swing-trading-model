**Owner:** Head of UX & Design
**Status:** Approved
**Approved by:** Product Owner — 2026-03-24 (design decision made this session)
**Cycle:** 2026-03-24__release-v2.3
**Story:** ST-13 (BLG-UX-01)

---

# UX Spec — Sidebar Navigation Collapsible Groups

## Product Owner Design Decision

Selected approach: **Collapsible section groups**. Items grouped into labelled sections; each section collapses/expands independently. Active section auto-expands; others default to collapsed.

## Group Structure

| Group | Items |
|-------|-------|
| **Trading** | Positions, Trade History, Trade Reflection |
| **Analytics** | Analytics, Risk Dashboard, Signals |
| **Tools** | Watchlist, Alerts |
| **System** | Settings, System Status, Notifications |

## Collapse Behaviour

- **Default state:** active group expanded; all others collapsed
- **Active group:** the group containing the current page's nav item — always expanded; cannot be collapsed while on that page
- **User can expand/collapse:** any non-active group by clicking the group heading
- **Persistence:** collapse state stored in sessionStorage; resets to default on full page reload

## Group Header Design

- Group label in uppercase small caps, secondary colour (e.g. muted grey)
- Collapse chevron (▶ / ▼) right-aligned in group header row
- Clicking anywhere on the group header row toggles collapse

## Active Item Styling

Unchanged from current design — active nav item highlighted as before.

## Badge Compatibility

The Alerts nav item (ST-10 BLG-FE-05) badge must remain visible whether the Tools group is collapsed or expanded.
- When collapsed: badge visible on the collapsed group header row ("Tools" header shows the Alerts badge count)
- When expanded: badge visible on the Alerts item itself

## Constraints

- All navigation links remain intact (no links removed or rerouted)
- No regression to page routing
- Sidebar must remain accessible on shorter screens after grouping
