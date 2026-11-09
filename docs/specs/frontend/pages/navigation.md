**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 2.1
**Last Updated:** 2026-11-09 (ST-01/ST-02/ST-03, EPIC-01, v9.16 — BLG-FE-250/251/252 built: §Implementation Status and §Onward Links status updated; Trade History `?ticker=` filter recorded under §Onward Links); prior — 2026-11-04 (ST-08, EPIC-02, v9.15, BLG-SPEC-214 — navigation v2: five job-based areas, placement for all 25 pages, parent links and onward-link rule); prior — 2026-11-03 (v9.15 design gate — ST-12/ST-13/ST-14: §Legacy Dashboard Route, §Browser Tab Title, §Sidebar Footer and Height); prior history retained — see prior entries in version control
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source:** docs/design/2026-03-24__release-v2.3/sidebar-nav-groups/ux_spec.md
**Design Source (v1.3 command palette):** docs/design/2026-07-17__release-v7.5/command-palette/ux_spec.md
**Design Source (v1.4 nav dedup):** docs/design/2026-07-21__release-v7.7/nav-notification-digest-consolidation/ux_spec.md
**Design Source (v1.8 tab title, legacy route, sidebar footer; v2.0 brief):** docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md
**Label source (v2.0):** docs/reference/glossary.md §UI Labels
**Confirmed by:** Head of Specs Team — 2026-03-24
**Release:** v2.3 — ST-13 (BLG-UX-01)

---

# Frontend Specification — Sidebar Navigation

## Purpose

Defines the left sidebar: its areas, which page sits where, how groups expand and collapse, how detail pages link back to their parent, and how every page links onward. It also fixes the browser-tab title, the legacy Dashboard redirect and the sidebar footer. The sidebar appears on every page.

**v2.0 (ST-08, BLG-SPEC-214, v9.15)** regroups the sidebar by the job the user is doing, not by feature type. Page labels come from `docs/reference/glossary.md` §UI Labels, which is the single source for the sidebar, page heading, command palette and browser-tab title.

## Implementation Status

v2.0 was a spec ahead of the code. From v2.1 every part is built. Each part was built by the backlog item named here, not by ST-08.

| Section | Built by | Target |
|---------|----------|--------|
| §Areas, §Page Placement, §Default Expansion | `BLG-FE-250` (ST-01) | v9.16 — built |
| §Parent Links | `BLG-FE-251` (ST-02) | v9.16 — built |
| §Onward Links | `BLG-FE-252` (ST-03) | v9.16 — built |
| Labels from glossary §UI Labels | ST-11 (`BLG-FE-248`) | v9.15 |
| §Browser Tab Title | ST-13 (`BLG-FE-249`) | v9.15 |
| §Legacy Dashboard Route | ST-12 (`BLG-FE-247`) | v9.15 |
| §Sidebar Footer and Height | ST-14 (`BLG-FE-266`) | v9.15 |

`src/Layout.js` `NAV_AREAS` holds the five areas. The v1.x `NAV_GROUPS` (Trading, Analytics, Tools, System) are gone.

## Areas

Five areas, in this order from the top of the sidebar.

| Order | Area | The job it serves | Expanded by default |
|-------|------|-------------------|---------------------|
| 1 | **Today** | See what needs attention now | Yes |
| 2 | **Portfolio** | Manage what I hold and record trades | Yes |
| 3 | **Find trades** | Look for and plan new trades | No |
| 4 | **Review** | Look back at results and discipline | No |
| 5 | **Settings** | Configure the app and check its health | No |

## Page Placement

Every page in `src/pages/` has one row. Labels are the glossary §UI Labels canonical labels. "Sidebar entry: No" pages are reached from their parent or another page; the reason is given.

| Page file | Route | Canonical label | Area | Sidebar entry | Position in area | Reason for no sidebar entry |
|-----------|-------|-----------------|------|---------------|------------------|-----------------------------|
| `DashboardHome.js` | `/` and `/DashboardHome` | Dashboard | Today | Yes | 1 | — |
| `Notifications.js` | `/notifications` | Notifications | Today | Yes | 2 | — |
| `NotificationsHistory.js` | `/notifications/history` | Notification History | Today | No | — | Detail page of Notifications |
| `NotificationPreferences.js` | `/notifications/preferences` and `/NotificationPreferences` | Notification Preferences | Today | No | — | Detail page of Notifications; Settings links to it (§Onward Links) |
| `Positions.js` | `/Positions` | Positions | Portfolio | Yes | 1 | — |
| `TradeEntry.js` | `/TradeEntry` | Trade Entry | Portfolio | Yes | 2 | — |
| `RiskDashboard.js` | `/RiskDashboard` | Risk Dashboard | Portfolio | Yes | 3 | — |
| `Signals.js` | `/Signals` | Signals | Find trades | Yes | 1 | — |
| `Screener.js` | `/Screener` | Screener | Find trades | Yes | 2 | — |
| `Watchlist.js` | `/Watchlist` | Watchlist | Find trades | Yes | 3 | — |
| `Research.js` | `/Research` (new landing) and `/research/:ticker` | Research | Find trades | Yes (new) | 4 | — |
| `TradePlans.js` | `/TradePlans` | Trade Plans | Find trades | Yes (new) | 5 | — |
| `TradePlan.js` | `/TradePlan` | Trade Plan | Find trades | No | — | Create/edit form for one plan; reached from Trade Plans, Trade Entry, Research and notifications |
| `TickerUniverse.js` | `/TickerUniverse` | Ticker Universe | Find trades | Yes | 6 | — |
| `TradeHistory.js` | `/TradeHistory` | Trade History | Review | Yes | 1 | — |
| `PerformanceAnalytics.js` | `/PerformanceAnalytics` | Analytics | Review | Yes | 2 | — |
| `Reports.js` | `/Reports` | Reports | Review | Yes | 3 | — |
| `StrategyBenchmark.js` | `/StrategyBenchmark` | Strategy Benchmark | Review | Yes | 4 | — |
| `Replay.js` | `/Replay` | Replay | Review | Yes | 5 | — |
| `TradeReflection.js` | `/TradeReflection` | Trade Reflections | Review | Yes | 6 | — |
| `RedFlagJournal.js` | `/RedFlagJournal` | Red Flag Journal | Review | Yes | 7 | — |
| `WeeklyDigest.js` | `/WeeklyDigest` | Weekly Digest | Review | Yes | 8 | — |
| `Settings.js` | `/Settings` | Settings | Settings | Yes | 1 | — |
| `SystemStatus.js` | `/SystemStatus` | System Status | Settings | Yes | 2 | — |
| `Dashboard.js` | `/Dashboard` | — | — | No | — | Removed by ST-12; `/Dashboard` redirects to `/` (§Legacy Dashboard Route) |

**Counts:** 25 page files. 21 sidebar entries: the 19 in today's sidebar (18 `NAV_GROUPS` items plus the separate Dashboard link), plus Research and Trade Plans. 3 detail pages without a sidebar entry, each with a parent. 1 page removed.

**`__StandingAlertHarness.js`** is a test-only harness on `/__test/standing-alert` (no Layout). It is not a page and has no placement or label.

**Research landing (new route):** the Research sidebar entry opens `/Research`, which has the page heading "Research" and a single ticker input. Submitting a ticker goes to `/research/:ticker`. Nothing else is on the landing. `BLG-FE-250` builds it.

**Later merges:** `BLG-SPEC-216` (ST-10) may merge Trade Reflections, Red Flag Journal and the Positions journal view into one Journal area in Review, and `BLG-FE-259` may merge Reports into Analytics. Each one revises this table when it ships. Until then the rows above stand.

## Default Expansion and Collapse

- **Expanded by default:** Today and Portfolio, plus the active area if it is a different one.
- **Active area:** the area that contains the current page, or the current page's parent for a page without a sidebar entry (Trade Plan → Find trades; Notification History and Notification Preferences → Today). The active area is always expanded and cannot be collapsed while the user is on one of its pages.
- **Other areas:** the user can expand or collapse them by clicking the area header.
- **Persistence:** collapse state is kept in `sessionStorage` and resets to the default on a full page reload. A user's explicit collapse of Today or Portfolio holds for the session, the same as for any non-active area.
- **Mobile drawer:** same areas, order and default expansion as desktop.

## Area Header

- Label: the area name in uppercase small caps, secondary (muted grey) colour.
- Collapse indicator: chevron on the right (▶ collapsed / ▼ expanded).
- Click target: the whole header row.

## Active Item

The current page's sidebar entry keeps the existing highlight. A page without a sidebar entry highlights its parent's entry (Trade Plan → Trade Plans, Notification History and Notification Preferences → Notifications, `/research/:ticker` → Research).

## Alert Badge Integration

Notifications sits in **Today**, so the alert badge moves with it. Same count source and reset-on-visit rule as before.

- When Today is collapsed and unacknowledged alerts exist, the count shows on the Today header row.
- When Today is expanded, the count shows on the Notifications entry.

Today is expanded by default, so most users see the count on the Notifications entry.

## Parent Links

Every page without a sidebar entry shows a parent link above its page heading: a left chevron and the parent's canonical label, linking to the parent route.

| Page | Parent link text | Goes to |
|------|------------------|---------|
| Trade Plan | Trade Plans | `/TradePlans` |
| Research (`/research/:ticker`) | Research | `/Research` |
| Notification History | Notifications | `/notifications` |
| Notification Preferences | Notifications | `/notifications` |

An existing "Back" button that calls `navigate(-1)` may stay, but it does not replace the parent link: Back depends on how the user arrived.

## Onward Links

**Rule:** every page has at least one in-page link to the next page a user is likely to need, beyond the sidebar. A page with no such link is a dead end. The table names the required onward link per page. A page may have more links than the one listed.

| Page | Required onward link | Status (v2.1) |
|------|----------------------|---------------|
| Dashboard | Each card to its page (Positions, Risk Dashboard, Signals, Screener, Trade History, Red Flag Journal, Analytics); Today items to their action once `BLG-FE-254` ships (`dashboard.md`) | Exists |
| Notifications | Notification Preferences | Exists |
| Notification History | Notifications (parent link) | Built — ST-02 (v9.16) |
| Positions | Trade Entry ("New Position") | Exists |
| Trade Entry | Positions after save; Trade Plan | Exists |
| Risk Dashboard | Positions | Exists |
| Signals | Watchlist | Exists |
| Screener | Research for a result's ticker | Exists |
| Watchlist | Research for a ticker | Exists |
| Research | Trade Plan for this ticker | Exists |
| Trade Plans | Trade Plan (new or edit); Trade Entry from a plan | Exists |
| Trade Plan | Trade Entry from the plan | Exists |
| Ticker Universe | Screener | Built — ST-03 (v9.16) |
| Trade History | Research for a trade's ticker | Built — ST-03 (v9.16): each row has a "Research {TICKER}" icon link to `/research/:ticker` beside the ticker; clicking the ticker text still expands the row |
| Analytics | Trade History | Built — ST-03 (v9.16); shows in the populated state |
| Reports | Analytics | Built — ST-03 (v9.16) |
| Strategy Benchmark | Analytics | Built — ST-03 (v9.16) |
| Replay | Trade History | Built — ST-03 (v9.16) |
| Trade Reflections | Trade History | Built — ST-03 (v9.16) |
| Red Flag Journal | Trade History filtered to the flagged trade's ticker | Built — ST-03 (v9.16): each event links to `/TradeHistory?ticker={TICKER}` |
| Weekly Digest | Notifications | Exists |
| Settings | Notification Preferences | Built — ST-03 (v9.16) |
| Notification Preferences | Notifications (parent link); Weekly Digest | Parent link built — ST-02 (v9.16); Weekly Digest link exists |
| System Status | Settings | Built — ST-03 (v9.16) |

The "Status at v2.0" column comes from a scan of in-page links in `src/pages/` and the components they render (2026-11-04). "Exists" means the link shows in the page's normal populated state; a link that shows only in the empty state does not count. Links that depend on data being present (Risk Dashboard → Positions shows when grace-period rows exist; Signals → Watchlist after a ticker is watched) count as existing. The scan agrees with the eight dead-end pages listed in `BLG-FE-252` and finds three more: Settings and Trade History link to no other page, and Analytics links out only from its empty state. `BLG-FE-252`'s AC is that a re-run of the scan finds 0 dead-end pages, so that re-run also covers these three. Its required link is the one in this table.

**v2.1 (ST-03, v9.16):** a header onward link sits under the page description (`PageHeader` `onward`, shared `OnwardLink` component): an arrow after the target's canonical label. The scan is re-run by Playwright `onward-links.spec.js` SC-ONW-12 over every routed page; it finds 0 dead ends. **Trade History ticker filter:** `/TradeHistory?ticker={TICKER}` shows only that ticker's trades (with or without the `.L` suffix), with a "Showing trades for {TICKER}" line and a "Show all trades" button that removes the parameter. It applies on top of the page's other filters and is not stored with them.

## Responsive Behaviour

- Below the breakpoint the sidebar is a slide-in drawer opened by the menu button. The areas, order and default expansion are the same as desktop. Collapse state is kept for the session.
- No other change to mobile navigation.

## Sidebar Footer and Height

*Added v1.8 (ST-14, BLG-FE-266).*

- **Version label:** the footer shows `v{X.Y}`, the latest release from the same source as the Dashboard What's New panel (`api.changelog.latest()`, `dashboard.md` §6A). While loading, or when the source has no version, no version text is shown. No hard-coded version (the former "v1.0.0" is removed).
- **Height:** the desktop sidebar's background spans the full page height at every scroll position and page length.

## Legacy Dashboard Route

*Added v1.8 (ST-12, BLG-FE-247).*

The pre-v7.3 widget dashboard (`src/pages/Dashboard.js`, route `/Dashboard`) is removed with its palette label and the components only it uses. `/#/Dashboard` redirects to `/` (the Dashboard home, `DashboardHome`) as a replace navigation, so Back does not return to the redirect. The command palette lists one "Dashboard" entry.

## Browser Tab Title

*Added v1.8 (ST-13, BLG-FE-249).*

| Page | `document.title` |
|------|------------------|
| Any routed page | `{page label} · Position Manager` |
| Research landing (`/Research`) | `Research · Position Manager` |
| Research page (`/research/:ticker`) | `{TICKER} · Research · Position Manager` |
| Other detail views (trade plan, replayed trade) | `{page label} · Position Manager` |
| Unknown route | `Page not found · Position Manager` |

- `{page label}` is the glossary §UI Labels canonical label. Until ST-11 applies those labels, the page's current heading label is used.
- The separator is a middle dot with a space on each side.
- Set once by `Layout.js` on route change from the same label source the sidebar, page heading and command palette use (ST-11's single source). No page sets `document.title` itself.
- `public/index.html` keeps "Position Manager" as the pre-render title.
- Playwright checks three pages, one of them a Research page.

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

### Canonical Inventory — All Keyboard-Handling Sites

*Added v1.7 (ST-06, EPIC-01, BLG-SPEC-159).*

The app-wide overlap scan behind this story found keyboard-event handling in `Layout.js`, `CommandPalette.js`, `TradeEntry.js`, `TradePlan.js`, `RedFlagJournal.js` and `TickerUniverse.js`, with no single document listing all of them. This is that inventory.

**Global (document-level `keydown`, active on every applicable page regardless of focus location elsewhere on the page):**

| Key | Source | Action | Guard |
|-----|--------|--------|-------|
| `n` | `Layout.js` | Navigate to Trade Entry | Positions/TradeHistory only; suppressed if focus is in an input/textarea/select or a modifier key is held |
| `w` | `Layout.js` | Dispatch `app:add-to-watchlist` | Screener/Watchlist only; same suppression |
| `r` | `Layout.js` | Dispatch `app:refresh` | All pages; same suppression |
| `Cmd/Ctrl+K` | `CommandPalette.js` | Toggle the command palette | All pages; suppressed if focus is in an input/textarea/select |

**Page-local (scoped to one focused element's own `onKeyDown`, not document-level — cannot fire unless that specific element has focus):**

| Key | Source | Element | Action |
|-----|--------|---------|--------|
| `Enter` | `TradeEntry.js` | Tag input field | Add the typed tag |
| `Enter` | `TradePlan.js` | Tag input field | Add the typed tag (same pattern as TradeEntry) |
| `Enter` | `RedFlagJournal.js` | Ticker filter text input | Apply the ticker filter |
| `Enter` / `Space` | `TickerUniverse.js` | "Clear filters" badge (`role="button"`, not a native `<button>`) | Clear active filters — standard keyboard-activation pattern for a custom interactive element, not a page shortcut |

**Conflict analysis:** no conflicts exist, by construction rather than coincidence —
- Every global shortcut's own handler explicitly returns early when `document.activeElement` is an `<input>`/`<textarea>`/`<select>` (see the suppression rule above and each source file's own guard clause). Every page-local handler in the second table is itself attached to one of those exact element types (or an element that receives focus the same way). The two tables are therefore mutually exclusive by focus state — a page-local handler can only fire in the one state where every global handler has already declined to act.
- The global shortcuts do not collide with each other: `n`, `w`, `r` are distinct bare keys, and `Cmd/Ctrl+K` requires a modifier that `Layout.js`'s handler explicitly excludes (`if (e.metaKey || e.ctrlKey || e.altKey) return;`) before checking `n`/`w`/`r` — so a `Cmd+K`/`Ctrl+K` press cannot also trigger a bare-key binding.
- The page-local handlers do not collide with each other: each is scoped to a distinct element on a distinct page; two of them can never hold focus simultaneously.

No conflicts required filing.

---

## Global Command Palette

*Added v1.3 (v7.5, ST-01, BLG-FE-115).*

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
| Pages | Static index — `pages.config.js` `PAGES`, labelled with the glossary §UI Labels canonical label (v2.0). From v2.0 this includes Notifications, Replay and Research (the `/Research` landing, once `BLG-FE-250` builds it) |
| Your Data | Dynamic index — tickers/positions/trade plans already loaded client-side (open positions, watchlist, trade plans) |

Empty input shows recent/frequent pages only (no "Your Data" group). Typing filters both groups live via fuzzy match.

### Selection & Navigation

- Page result → navigates to that route.
- Ticker/plan result → navigates to the most relevant surface (open position → `/positions`; watchlist ticker → `/watchlist`; trade plan → `/TradePlan?edit={id}` directly).
- Arrow Up/Down highlights; `Enter` selects; `Escape` closes without navigating.

### No Results

`DataState`'s `inline` variant (canonical definition: `docs/specs/frontend/design_system.md` §Data States — a single centered text line, no icon, for contexts where even the `compact` variant's icon+heading+body stack is too tall): `"No results for '{query}'."`

### Discoverability

First-session-only dismissible tooltip on the nav-bar search affordance. No modal product tour.

---

## Known Deviations

### DEV-NAV-ST06-01 — Dark theme not applying inside Radix portaled dialogs app-wide (RESOLVED v8.5)

- **Description:** `tailwind.config.js`'s `darkMode: ["class"]` requires an ancestor element carrying the literal `dark` class for any `dark:` variant to apply. `src/Layout.js` only ever applied that class to its own wrapper `<div>` — never to `document.documentElement`. Radix's `DialogPortal` (`src/components/ui/dialog.js`) renders its content into `document.body`, **outside** that wrapper's DOM subtree, so every `dark:` variant and every CSS custom property that differs between `:root` and `.dark` (`src/index.css`) had always resolved to its **light** value inside every Dialog-based component app-wide (14+ consumers: `CommandPalette`, `ExportModal`, `WatchlistModal`, `WidgetLibrary`, `PositionEntryModal`, etc.), regardless of the user's actual theme setting — a pre-existing, systemic production bug, not introduced by the story that found it.
- **Canonical requirement:** Every Dialog-based/Radix-portaled component must render using the user's actual active theme (light or dark), matching the rest of the app — an implicit requirement of this document's own theming conventions and `design_system.md`'s dark-mode support, not a single named spec line (the bug predates any spec text calling this out explicitly).
- **Discovery:** v8.5 EPIC-03/ST-06 (`BLG-FE-145`)'s own new Playwright tests (`command-palette.spec.js` SC-CP-13/SC-CP-14) failed on the first real GitHub Actions CI run with `Received: "rgb(115, 115, 115)"` (the *light*-theme `--muted-foreground` value) instead of the expected dark-theme value — the `-muted` token registration that story shipped made the wrong-theme value distinguishable from an empty CSS rule for the first time, surfacing a defect that had been silently invisible until then.
- **Resolution:** `Layout.js` now also syncs the `dark` class onto `document.documentElement`, which covers every portal (portals still mount under `<html>`/`<body>`), fixing this at the root cause for all consumers, not just the discovering story's own call sites. Shipped in the same commit as the discovery, `41619410` ("[EPIC-03][ST-06] Fix dark theme not applying inside portaled dialogs"), 2026-08-10, cycle `2026-08-08__release-v8.5`.
- **Priority:** P1 (app-wide visual defect across every Dialog-based component, silently present since Radix portals were first adopted; not a figure-correctness issue but genuinely observable to every user in dark theme)
- **Target resolution release:** v8.5 — already shipped (see Resolution); this record is a retroactive backfill, not an open target.
- **Owner:** Frontend Specifications & UX Documentation Owner
- **Backlog reference:** Filed retroactively this story (`ST-22`, `BLG-GOV-294`, `EPIC-06`, v8.6) — no distinct backlog item existed for this specific finding at discovery time; it was fixed directly within `BLG-FE-145`'s own commit as an emergent, same-session finding rather than tracked separately.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 2.1 | 2026-11-09 | ST-01/ST-02/ST-03 (EPIC-01, v9.16, BLG-FE-250/251/252). §Implementation Status: areas, parent links and onward links built. §Onward Links status column updated to built; records the header onward-link placement, the SC-ONW-12 automated scan and the Trade History `?ticker=` filter that the Red Flag Journal link uses. No rule changes. |
| 2.0 | 2026-11-04 | ST-08 (EPIC-02, v9.15, BLG-SPEC-214). Navigation v2 against the `site-structure-phase1` §2.1 brief. Replaces the drifted §Group Structure table with five job-based areas (Today · Portfolio · Find trades · Review · Settings) and §Page Placement for all 25 files in `src/pages/` (21 sidebar entries, 3 detail pages with parents, `Dashboard.js` removed). Today and Portfolio expanded by default, plus the active area; collapsible pattern, active-area-always-expanded and session persistence kept. Trade Plans and Research gain sidebar entries (new `/Research` landing). New §Parent Links and §Onward Links (dead-end rule). Alert badge moves with Notifications to Today. §Browser Tab Title, §Legacy Dashboard Route and §Sidebar Footer and Height kept. New §Implementation Status maps each part to its build item (`BLG-FE-250/251/252`, v9.16; ST-11 to ST-14, v9.15). Labels come from `glossary.md` §UI Labels (v1.3). Head of UX & Design review: see the v9.15 `qa_evidence_EPIC-02.md` ST-08 entry. |
| 1.8 | 2026-11-03 | `2026-11-03__release-v9.15` design gate. New §Sidebar Footer and Height (ST-14, BLG-FE-266: real release version, none when absent; full-height background), §Legacy Dashboard Route (ST-12, BLG-FE-247: `/Dashboard` removed, redirects to `/`, one palette entry) and §Browser Tab Title (ST-13, BLG-FE-249: `{page label} · Position Manager`, Research adds the ticker). Notes the §Group Structure drift that ST-08's v2.0 replaces. Design source: `docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md`. Head of UX & Design + Product Owner approved. Head of Specs Team confirmed. |
| 1.7 | 2026-09-28 | ST-06 (EPIC-01, v9.8, BLG-SPEC-159): §Keyboard Shortcuts gains "Canonical Inventory — All Keyboard-Handling Sites", listing the global shortcuts (already documented) alongside the page-local `onKeyDown` handlers in `TradeEntry.js`, `TradePlan.js`, `RedFlagJournal.js` and `TickerUniverse.js` that had no single documented home. Conflict analysis performed: none found (global handlers are input-focus-suppressed by construction; page-local handlers are scoped to one element each). Documentation-only; no implementation change. |
| 1.6 | 2026-08-12 | ST-22 (EPIC-06, v8.6, BLG-GOV-294): added §Known Deviations, filed retroactive `DEV-NAV-ST06-01` for the v8.5 EPIC-03/ST-06 dark-mode/Radix-portal `Layout.js` fix (commit `41619410`) — documentation only, no behavioural change. **Renumbered 1.5→1.6 at cross-EPIC merge-conflict resolution** (this row originally landed on this branch as v1.5, as flagged pre-emptively in this row's own text at authoring time — see prior row): EPIC-03's ST-09 independently bumped this file to v1.5 for a different change (§Group Structure count correction) and merged to `main` first (PR #1359), so per `CLAUDE.md` §8.2a this branch's bump renumbers to the next free version rather than conflating the two changes under one version number. |
| 1.5 | 2026-08-11 | ST-09 (EPIC-03, v8.6, BLG-FE-154): corrected §Group Structure table against live `NAV_GROUPS` (`src/Layout.js`) — Trading gained Trade Entry; Analytics gained Strategy Benchmark and Reports; Tools gained Screener and Ticker Universe. Documentation-only correction, no behavioural change. Head of Specs Team confirmed (Sprint Execution Engine, agent-mediated). |
| 1.4 | 2026-07-21 | v7.7 design gate — ST-02 (EPIC-02, BLG-FE-114): removed duplicate "Alerts" nav item (Tools group; routed to the same page as "Notifications" with no visual indication of the duplication). "Notifications" (System group) retained as sole nav path, inherits the alert-count badge. "Weekly Digest" moved from Analytics to System group, adjacent to Notifications. §Alert Badge Integration updated (Tools → System propagation). Design source: nav-notification-digest-consolidation/ux_spec.md. Approved: Product Owner 2026-07-21. Design gate: 2026-07-21__release-v7.7. Head of Specs Team confirmed. |
| 1.3 | 2026-07-17 | v7.5 design gate — added §Global Command Palette (ST-01, BLG-FE-115): Cmd/Ctrl-K invocation, nav-bar mouse fallback, Pages/Your Data result groups, selection/navigation rules, new compact-list `DataState` empty-state variant, discoverability tooltip. Design source: command-palette/ux_spec.md. Approved: Product Owner 2026-07-17. Design gate: 2026-07-17__release-v7.5. Head of Specs Team confirmed. |
| 1.2 | 2026-05-21 | v3.9 design gate — added Red Flag Journal to Trading group (ST-08, EPIC-03: new page at `/red-flag-journal`, nav item after Trade Reflection). Design source: docs/design/2026-05-21__release-v3.9/red-flag-journal/ux_spec.md. Approved: Product Owner 2026-05-21. Head of Specs Team confirmed. |
| 1.1 | 2026-04-25 | ST-11 (BLG-FE-19, v3.0): §Keyboard Shortcuts added — global shortcuts (n/w/r), suppression rule for text inputs, sidebar footer hint design. Design source: docs/design/2026-04-25__release-v3.0/keyboard-shortcuts/ux_spec.md. Head of UX & Design + Product Owner approved. Design gate: 2026-04-25__release-v3.0. Head of Specs Team confirmed. |
| 1.0 | 2026-03-24 | Initial version. ST-13 (BLG-UX-01, v2.3): collapsible section groups with 4 groups (Trading, Analytics, Tools, System). Product Owner design decision 2026-03-24. Design source: docs/design/2026-03-24__release-v2.3/sidebar-nav-groups/ux_spec.md. Design gate: 2026-03-24__release-v2.3. |
