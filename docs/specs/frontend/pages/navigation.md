**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.3
**Last Updated:** 2026-07-17
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source:** docs/design/2026-03-24__release-v2.3/sidebar-nav-groups/ux_spec.md
**Design Source (v1.3 command palette):** docs/design/2026-07-17__release-v7.5/command-palette/ux_spec.md
**Confirmed by:** Head of Specs Team — 2026-03-24
**Release:** v2.3 — ST-13 (BLG-UX-01)

---

# Frontend Specification — Sidebar Navigation

## Purpose

Defines the left sidebar navigation structure, including the collapsible group model introduced in v2.3 (BLG-UX-01). The sidebar appears on all pages.

## Group Structure

| Group Label | Nav Items |
|-------------|-----------|
| **Trading** | Positions, Trade History, Trade Reflection, Red Flag Journal |
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

## Global Command Palette (v7.5 — ST-01 BLG-FE-115)

**Design source:** docs/design/2026-07-17__release-v7.5/command-palette/ux_spec.md
**Depends on:** docs/specs/blg_fe_115_pre_implementation_readiness_pass.md (index scope, keyboard contract, `cmdk` dependency gap)

A global cross-page search palette, invoked from any page.

### Invocation

- **Keyboard:** `Cmd+K` (macOS) / `Ctrl+K` (Windows/Linux) — global, suppressed while focus is inside a text input/textarea/select.
- **Mouse fallback:** a search-icon button in the top nav header region, showing a muted `⌘K` / `Ctrl K` badge hint.

### Content

Centred modal overlay (shared `Dialog` component) with a single search input and a results list grouped into:

| Group | Source |
|-------|--------|
| Pages | Static index — `pages.config.js` `PAGES` |
| Your Data | Dynamic index — tickers/positions/trade plans already loaded client-side (open positions, watchlist, trade plans) |

Empty input shows recent/frequent pages only (no "Your Data" group). Typing filters both groups live via fuzzy match.

### Selection & Navigation

- Page result → navigates to that route.
- Ticker/plan result → navigates to the most relevant surface (open position → `/positions`; watchlist ticker → `/watchlist`; trade plan → `/trade-plans/{id}` detail view directly).
- Arrow Up/Down highlights; `Enter` selects; `Escape` closes without navigating.

### No Results

Compact `DataState` empty-state variant (new — not the existing `py-16` default card variant, which is oversized for the palette's compact list): `"No results for '{query}'."`

### Discoverability

First-session-only dismissible tooltip on the nav-bar search affordance. No modal product tour.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.3 | 2026-07-17 | v7.5 design gate — added §Global Command Palette (ST-01, BLG-FE-115): Cmd/Ctrl-K invocation, nav-bar mouse fallback, Pages/Your Data result groups, selection/navigation rules, new compact-list `DataState` empty-state variant, discoverability tooltip. Design source: command-palette/ux_spec.md. Approved: Product Owner 2026-07-17. Design gate: 2026-07-17__release-v7.5. Head of Specs Team confirmed. |
| 1.2 | 2026-05-21 | v3.9 design gate — added Red Flag Journal to Trading group (ST-08, EPIC-03: new page at `/red-flag-journal`, nav item after Trade Reflection). Design source: docs/design/2026-05-21__release-v3.9/red-flag-journal/ux_spec.md. Approved: Product Owner 2026-05-21. Head of Specs Team confirmed. |
| 1.1 | 2026-04-25 | ST-11 (BLG-FE-19, v3.0): §Keyboard Shortcuts added — global shortcuts (n/w/r), suppression rule for text inputs, sidebar footer hint design. Design source: docs/design/2026-04-25__release-v3.0/keyboard-shortcuts/ux_spec.md. Head of UX & Design + Product Owner approved. Design gate: 2026-04-25__release-v3.0. Head of Specs Team confirmed. |
| 1.0 | 2026-03-24 | Initial version. ST-13 (BLG-UX-01, v2.3): collapsible section groups with 4 groups (Trading, Analytics, Tools, System). Product Owner design decision 2026-03-24. Design source: docs/design/2026-03-24__release-v2.3/sidebar-nav-groups/ux_spec.md. Design gate: 2026-03-24__release-v2.3. |
