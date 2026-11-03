**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-03__release-v9.15
**Stories:** ST-08 (BLG-SPEC-214), ST-09 (BLG-SPEC-215), ST-10 (BLG-SPEC-216), ST-11 (BLG-FE-248), ST-12 (BLG-FE-247), ST-13 (BLG-FE-249), ST-14 (BLG-FE-266) — all EPIC-02

# Decision Record — Site Structure & Usability Phase 1

## 1. Scope of this record

EPIC-02 is Phase 1 of the Site Structure & Usability programme (DL-088). It has two kinds of story:

- **Three spec stories (ST-08, ST-09, ST-10).** Their deliverable *is* the design: navigation v2 and the glossary's UI-label section, the Dashboard "Today" list, and the single Journal area. That work is sized at 2 days each and approved inside the sprint by the Head of UX & Design, as the release plan sets out (RISK-02). This gate does not pre-empt it. §2 records the brief each spec must meet, so the in-sprint review has fixed criteria.
- **Four build stories (ST-11 to ST-14).** §3 designs ST-12, ST-13 and ST-14 now. ST-11 applies the labels ST-08 produces, so §3.1 fixes the rule it applies and its dependency.

## 2. Brief for the in-sprint specs

### 2.1 Navigation v2 and UI labels (ST-08)

`navigation.md` v2.0 and a new UI-label section in `docs/reference/glossary.md` must:

- Group all routed pages into about five job-based areas (Today · Portfolio · Find trades · Review · Settings), giving every page in `src/pages/` one placement, or recording why a page has no sidebar entry (detail pages, Replay).
- Replace the current §Group Structure table. It has drifted again: it omits Replay and lists "Trade Reflection" where the sidebar shows "Reflections".
- Keep the collapsible-group pattern, active-group-always-expanded and session persistence (§Collapse Behaviour). Name the groups that are expanded by default.
- Surface Trade Plans and Research, which have no sidebar entry today.
- Give every detail page a parent link and every page an onward link (the "where next" rule).
- Absorb §3.2 and §3.3 of this record as the browser-tab title rule and the legacy-route redirect.
- In the glossary: one canonical label per page and per primary action, the "trade" vs "position" usage rule, and a column for any deliberate difference between sidebar, heading and palette (ST-11 AC 1).
- Keep the alert-badge rule (§Alert Badge Integration) on whichever area holds Notifications.

**Approval:** the Head of UX & Design reviews both documents (ST-08 AC 1). Phase 2 (v9.16) builds the sidebar from this spec, so ST-08 changes no sidebar code.

### 2.2 Dashboard "Today" list (ST-09)

`dashboard.md` (Class 1, Head of Specs Team approval) must specify:

- The Today list first: regime per market (including the v9.14 unknown state), then exits and stop changes due, then qualifying entries. Each item links to its action through the existing deep links (`/Positions?exit=<id>`, `/Positions?position=<id>`).
- A single-line quiet-day state, and the ordering, empty, loading and error states. Each card that moves or merges is named.
- Status cards, What's New and gate progress below the list.
- A testable AC for every observable behaviour, ready for `BLG-FE-254` (ST-09 AC 1).
- **§13 constraint:** "qualifying entries" lists signals the screener already produced, in the order it produced them. The list must not add a new ranking, score or "do this" wording. If it does, it needs its own §13 confirmation before approval.

### 2.3 Journal area (ST-10)

The Journal area spec must cover the sections or filters for reflections, red flags and position notes, the routes and redirects for the old pages, and what happens to the Positions journal view. Its §13 confirmation is part of the story (ST-10 AC 2, with the §13 clause citations restated in the slice). This gate adds nothing to it.

## 3. Build stories

### 3.1 One name per page and action (ST-11)

- **Rule:** for every page, sidebar label = page heading = command-palette label = browser-tab title label, from one source in code (for example one exported label map that `NAV_GROUPS`, `PageHeader` callers, `CommandPalette.js` `PAGE_LABELS` and §3.2 read). The glossary records any deliberate difference.
- **Dependency:** the labels are ST-08's glossary section. ST-11 starts only after ST-08 is approved (slice Sequencing). If ST-08 is not approved by sprint close, ST-11 returns to backlog with it (RISK-02). This is a dependency inside the sprint, not a missing design.
- Replay and Notifications gain palette labels (slice Scope).

### 3.2 Browser-tab title (ST-13)

- **Format:** `{page label} · Position Manager`. The separator is a middle dot with a space on each side.
- **Research pages:** `{TICKER} · Research · Position Manager`.
- **Other detail views** (a trade plan, a replayed trade): the page label alone, so ST-13 needs no per-record data fetch.
- **Unknown route:** `Page not found · Position Manager`.
- **Source:** set once in `Layout.js` on route change, from the §3.1 label source. Until ST-11 lands, that is the current page heading label. No page sets `document.title` itself.
- `public/index.html` keeps "Position Manager" as the pre-render title.

### 3.3 Legacy Dashboard route (ST-12)

- `/Dashboard` (the pre-v7.3 widget page, `src/pages/Dashboard.js`) is removed. `/#/Dashboard` redirects to `/`, the Dashboard home, with a replace navigation so Back does not loop.
- The palette shows one "Dashboard" entry (`DashboardHome`).
- Components used only by the legacy page are removed (slice Scope). That includes the widget library and the two win-rate widgets. See the gate record's Notes on ST-16.

### 3.4 Sidebar chrome (ST-14)

- **Footer version:** the sidebar footer shows `v{X.Y}`, the latest release from the same source as the What's New panel (`api.changelog.latest()`, `dashboard.md` §6A). While loading, or if the source has no version, the footer shows no version text. The hard-coded "v1.0.0" is removed.
- **What's New heading:** "What's New — v{X.Y}" when the entry has a version, and "What's New" otherwise (`dashboard.md` §6A). Never "undefined".
- **Sidebar background:** the desktop sidebar's background runs the full height of the page at every scroll position and page length.

## 4. §13 Compliance

Navigation, labels, titles and chrome only. ST-09's list carries the §2.2 constraint. ST-10's §13 confirmation is in its own ACs.

## 5. Frontend Spec Impact (this gate)

- `pages/navigation.md` v1.7 → v1.8: new §Browser Tab Title (ST-13), §Legacy Dashboard Route (ST-12), §Sidebar Footer and Height (ST-14). ST-08 then revises the file to v2.0 in the sprint.
- `pages/dashboard.md` v3.10 → v3.11: §6A header drops the version suffix when there is no version (ST-14).

ST-08, ST-09 and ST-10 write their own specs in the sprint.

## 6. Testability (CLAUDE.md §2)

- ST-13: Playwright reads `document.title` on three pages, one of them a Research page with a ticker.
- ST-12: Playwright opens `/#/Dashboard` and lands on the Dashboard home. A palette search for "Dashboard" returns one result.
- ST-14: Playwright with `api.changelog.latest()` mocked to `version: "9.15"` (footer shows "v9.15") and to no version (no footer version, heading "What's New"). The full-height sidebar is a visual AC: Playwright compares the sidebar's bounding box with the document height on a long page.
- ST-11: the existing nav and palette Playwright specs are updated (slice AC 2).

## 7. Approval

Head of UX & Design: confirmed, 2026-11-03 (agent-mediated, Design Gate Engine). The ST-08, ST-09 and ST-10 specs need their own Head of UX & Design approval in the sprint (§2).
Product Owner: confirmed, 2026-11-03 (the user, in session).
