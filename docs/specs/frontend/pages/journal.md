**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Approved — not yet built (`BLG-FE-258`)
**Version:** 1.0
**Last Updated:** 2026-11-04 (ST-10, EPIC-02, v9.15, BLG-SPEC-216 — initial version: one Journal area combining reflections, red flags and position notes)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source:** docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md §2.3
**Builds on:** `reflections.md` v0.3, `red_flag_journal.md` v1.4, `positions.md` §View Switcher and §Journal View, `journal_components.md` v1.1
**Built by:** `BLG-FE-258` (Provisional-Target v9.17)

---

# Frontend Specification — Journal

## 1. Purpose

Journaling is split across three places today, and none links to the others:

- **Trade Reflections** (`TradeReflection.js`, route `/TradeReflection`): structured post-trade reflections, one card per closed trade.
- **Red Flag Journal** (`RedFlagJournal.js`, route `/RedFlagJournal`): rule-deviation events from `GET /portfolio/red-flag-journal`.
- **The Journal view inside Positions** (`JournalView.js`): entry/exit notes and tags on positions, which retitles the Positions page "Trade Journal".

This spec merges them into one **Journal** page with three sections. It changes where the content lives and how the user moves between it. It does not change what any section shows or the data behind it: each section keeps its existing spec for content, data source and states, and that spec stays canonical for those parts.

## 2. Route, Label and Placement

- **Route:** `/Journal`. The section is chosen by `?section=reflections | red-flags | notes`. With no or an unknown `section`, the page opens on **Reflections**.
- **Canonical label:** "Journal" (page heading, sidebar entry, palette entry and tab title `Journal · Position Manager`).
- **Placement:** Review area, replacing the separate Trade Reflections and Red Flag Journal entries at their position (`navigation.md` §Page Placement).
- When `BLG-FE-258` ships, the same commit updates:
  - `navigation.md`: §Page Placement (one Journal row; the "Later merges" note), §Onward Links (Journal rows replace Trade Reflections and Red Flag Journal), and the keyboard inventory row for the Red Flag Journal ticker input (now the shared filter, §3);
  - `glossary.md` §UI Labels: one "Journal" row in place of "Trade Reflections" and "Red Flag Journal"; the Positions "Trade Journal" deliberate difference is removed;
  - `src/lib/pageLabels.js`: `PAGE_LABELS` and `PALETTE_PAGE_KEYS` (Journal in, the two old keys out);
  - `positions.md`: §View Switcher (no Journal View), §Journal View (moved here, marked superseded by `journal.md` §4), the keyboard-navigation tab order and the "Hidden in Journal View" notes;
  - `reflections.md` §2–§3 and §10 (card structure, §4 below) and `red_flag_journal.md` §2 (route) and §4 (ticker control): a "superseded by `journal.md`" note on each;
  - the SI-05 digest link (`backend/services/si05_digest_service.py`, `rfj_url = .../#/RedFlagJournal`), which changes to `/#/Journal?section=red-flags`.

## 3. Layout

```
Journal                                             (h1)
Your reflections, rule red flags and position notes in one place.
[ Reflections (N) ]  [ Red flags (N) ]  [ Position notes (N) ]     ← tabs
[ Ticker filter ________ ]                                          ← shared
<section content>
```

- **Tabs:** an ARIA tablist (`role="tablist"`), one tab per section. A tab shows its count in brackets once that section has loaded: the number of items the section lists under the current filters (Reflections: closed trades listed; Red flags: the response `total` under the current filters; Position notes: positions listed). Sections load when their tab is first opened (§4), so an unopened tab shows no count; there is no count while loading or on error. The selected tab sets `?section=` with a replace navigation, so switching tabs does not add history entries. Arrow keys move between tabs; the selected tab's panel has `role="tabpanel"`.
- **Shared ticker filter:** one text input above the panel, "Filter by ticker…". It filters every section and is kept when the user switches tab. Matching differs by section, because the red-flag endpoint is unchanged (§6):
  - **Reflections and Position notes** (filtered in the browser): case-insensitive partial match, ignoring a UK ".L" suffix on both sides ("AA" matches "AAPL"; "LGEN" matches "LGEN.L").
  - **Red flags** (filtered by the server, `UPPER(ticker) = ?` in `GET /portfolio/red-flag-journal`): the exact ticker, case-insensitive. The input is sent as typed, upper-cased; a UK ticker must include ".L" ("LGEN.L"). When the Red flags panel shows no events for a ticker without ".L", its empty state reads: "No events for {TICKER}. UK tickers need the .L suffix here, e.g. LGEN.L."
  - **URL:** mirrored as `?ticker=` (replace navigation). The URL is the single source: opening `/Journal?ticker=AAPL` pre-fills the input.
  - **When it applies:** Reflections and Position notes filter client-side as the user types. Red flags filters server-side (`?ticker=` on `GET /portfolio/red-flag-journal`, as today); it refetches 300 ms after typing stops, or at once on Enter.
  - **Saved red-flag filters:** the Red Flag Journal's saved filters (`localStorage["redFlagJournal.filters"]`) no longer store the ticker; its other saved filters stay. An old saved ticker is ignored, and `?ticker=` wins.
- **Section filters:** each section's other filters stay inside its panel (Red flags: `red_flag_journal.md` §4 rule and date filters; Position notes: §4 below).
- **Mobile:** the tabs scroll horizontally if they do not fit; the filter goes full width.

## 4. Sections

| Section | `section=` | Content and states | Data source | Item link (onward link) |
|---------|------------|--------------------|-------------|-------------------------|
| **Reflections** | `reflections` | As `reflections.md` §4–§7 and §9 (card grid, field specs, empty and loading states, reflection modal). Its page header (§2) and search bar (§3) are replaced by this page's heading and the shared ticker filter. **Card structure changes:** today each card is one `<button>` (`reflections.md` §10); it becomes a card whose body is the button that opens the modal, with a sibling "View trade" link in the card footer, so no interactive element is nested in another (supersedes `reflections.md` §10 on this point). | `GET /trades`, every closed trade with or without a saved reflection (as today, `base44.entities.TradeReflection.list`) | Card body → reflection modal (as today); footer "View trade" → `/TradeHistory?ticker={ticker}` |
| **Red flags** | `red-flags` | As `red_flag_journal.md` §4–§9 (filters, event list, pagination, empty, loading and error states, keyboard). Its own ticker input (§4) is replaced by the shared filter; its other filters stay. | `GET /portfolio/red-flag-journal` (as today) | Each event links "View trade" → `/TradeHistory?ticker={ticker}` |
| **Position notes** | `notes` | The Positions Journal View as specified in `positions.md` §Journal View (scope: all positions the page holds, open and closed; timeline cards; exit-details expander), moved unchanged, with card components from `journal_components.md`. Its four filters stay inside the panel: note-text Search (entry and exit notes), Tag, Win/Loss and Date range; the shared ticker filter applies on top (AND). Empty states as `positions.md` §Journal View: "no positions at all" keeps its path to enter a position (→ `/TradeEntry`); "no results match" offers clearing the filters (shared ticker included). | `GET /positions` (as today) | An open position's card links "Open position" → `/Positions?position={position_id}`; a closed position's card has no item link (it is no longer on Positions) |

**Trade History `?ticker=` (new, part of `BLG-FE-258`):** Trade History does not read a `ticker` query parameter today. The "View trade" links need it: Trade History reads `?ticker=` on load into its existing ticker filter. This is the same behaviour `navigation.md` §Onward Links asks of the Red Flag Journal → Trade History link (`BLG-FE-252`); whichever item ships first builds it, and the other reuses it.

Each section fetches only when its tab is first opened, and keeps its data for the session after that. Red flags still refetches when its filters (including the shared ticker) change, as today. A section's error or empty state affects only its panel; the tabs and the other sections keep working.

## 5. Redirects and Removed Views

| Old route or view | New behaviour |
|-------------------|---------------|
| `/TradeReflection` | Redirects to `/Journal?section=reflections` (replace navigation) |
| `/RedFlagJournal` | Redirects to `/Journal?section=red-flags` (replace navigation) |
| Positions journal view (the BookOpen view-switcher button; heading "Trade Journal") | Removed. The Positions view switcher keeps Grid and Table. In its place, a "Position notes" text link in the Positions header goes to `/Journal?section=notes` |
| Dashboard Morning Briefing Red Flags card link (`/RedFlagJournal`) | Points to `/Journal?section=red-flags` |

Any other in-app link to the old routes is updated in the same commit, so the redirects only serve bookmarks, old notification links and old digests. Redirects keep any query string except `section` (e.g. `/RedFlagJournal?ticker=AAPL` → `/Journal?section=red-flags&ticker=AAPL`).

**Positions "Position notes" link:** a text link in the Positions page header actions, before the Daily Monitor button, "Position notes", → `/Journal?section=notes`.

## 6. What Does Not Change

- The data, endpoints, fields and AI-free content of all three sections.
- The reflection modal (`trade_reflection.md`) and the Trade History `?reflect=` re-entry path.
- The Trade History AI journal summary (`POST /ai/journal-summary`) and the AI post-trade debrief stay on Trade History. The Journal page shows no AI-generated text (§8).

## 7. Testable Acceptance Criteria

*For `BLG-FE-258`.*

| ID | Behaviour | Test |
|----|-----------|------|
| JA-01 | `/Journal` shows the heading "Journal", three tabs in the order Reflections, Red flags, Position notes, and opens on Reflections | Playwright |
| JA-02 | `?section=red-flags` and `?section=notes` open those tabs; an unknown value opens Reflections | Playwright |
| JA-03 | Selecting a tab updates `?section=` without adding a history entry (Back leaves the Journal) | Playwright |
| JA-04 | Tabs are an ARIA tablist; Left/Right arrow keys move between tabs | Playwright + axe scan |
| JA-05 | A tab shows its count only once its section has loaded (Reflections: closed trades listed; Red flags: response `total`; Position notes: positions listed); unopened tabs, loading and error show no count | Playwright with mocked lists |
| JA-06 | The shared ticker filter filters each section and is kept across tab switches; it is mirrored in `?ticker=` | Playwright: filter "AAPL", switch tabs, each panel shows only AAPL items |
| JA-07 | Reflections section renders the `reflections.md` card grid, empty and loading states, and opens the reflection modal | Playwright (retargeted reflections scenarios) |
| JA-08 | Red flags section renders the `red_flag_journal.md` event list, its own non-ticker filters, pagination, empty and error states | Playwright (retargeted red-flag scenarios) |
| JA-09 | Position notes renders the `positions.md` §Journal View timeline (open and closed), its note-text Search, Tag, Win/Loss and Date filters, and both empty states | Playwright (retargeted journal-view scenarios) |
| JA-10 | Item links: reflection footer and red-flag "View trade" → `/TradeHistory?ticker={ticker}`, which opens Trade History filtered to that ticker; an open position's "Open position" → `/Positions?position={id}`; a closed position's card has no item link | Playwright; axe scan finds no nested-interactive violation on Reflections |
| JA-11 | A section's fetch failure shows its error state in its panel only; the other tabs still load | Playwright: red-flag endpoint 500 |
| JA-12 | `/TradeReflection` → `/Journal?section=reflections` and `/RedFlagJournal` → `/Journal?section=red-flags`, both replace navigations | Playwright |
| JA-13 | Positions has no Journal view button, its heading is always "Positions", and its "Position notes" link opens `/Journal?section=notes` | Playwright |
| JA-14 | The sidebar and palette show one "Journal" entry and no "Trade Reflections" or "Red Flag Journal" entry; the tab title is `Journal · Position Manager` | Playwright |
| JA-15 | The Journal page contains no AI-generated text and calls no `/ai/*` endpoint | Playwright: request log has no `/ai/` call |
| JA-16 | Opening `/Journal?ticker=AAPL` pre-fills the filter and every section shows only AAPL items. In Reflections and Position notes, "AA" and "LGEN" match AAPL and LGEN.L (partial, ".L" ignored); in Red flags the request carries `ticker=LGEN.L` exactly as typed (upper-cased), and "LGEN" with no UK events shows the ".L" hint | Playwright with mocked lists and request capture |
| JA-17 | Red flags refetches 300 ms after typing stops, or at once on Enter; a saved red-flag ticker in `localStorage` is ignored and `?ticker=` wins | Playwright with a seeded `redFlagJournal.filters` |
| JA-18 | Redirects keep the query string: `/RedFlagJournal?ticker=AAPL` → `/Journal?section=red-flags&ticker=AAPL` | Playwright |
| JA-19 | A section's data is requested only when its tab is first opened | Playwright: request log before and after opening Red flags |
| JA-20 | At 375px the tabs scroll horizontally and the filter is full width; no page-level horizontal scroll | Playwright at 375px |
| JA-21 | The Positions header shows a "Position notes" link before the Daily Monitor button, going to `/Journal?section=notes` | Playwright |

## 8. §13 Confirmation

**Requirement:** the Strategy Rules & System Intent Owner confirms the merge moves no §13 boundary, naming the §13 clauses it answers (story ST-10 AC 2, §13 clause-citation rule).

**Clauses answered:**

- **No §13 clause names the journal.** None of §13.1–§13.6 mentions reflections, red flags or position notes, so the confirmation is made against the general clauses.
- **§13.1 (deterministic, human-in-the-loop decision support).** The Journal holds records the user writes (reflections, position notes) and records the deterministic red-flag rules already produce. The merge changes their layout and navigation only. It adds no automation, no scheduling and no new decision surface.
- **§13.2 (not automated, not adaptive, not ML/AI-driven).** The merge adds no model call, no prediction and no new rule. Nothing in the Journal feeds signals, sizing, scoring or any recommendation, as before.
- **§13.5 roster (AI journal surfaces).** The merged area surfaces **no AI journal summaries**: the AI journal summary (`POST /ai/journal-summary`) and the AI post-trade debrief (`GET`/`POST /trades/{trade_id}/debrief`, roster row "ST-06 — Automated AI Post-Trade Debrief (BLG-FEAT-90)") stay on Trade History, unchanged (§6, JA-15). Roster check result: no roster row is affected by this merge. Observation for the re-attestation roster: `POST /ai/journal-summary` is cleared by its contract note (SRB-v1.7, `ai_endpoints.md`) and has no row in the §13.5 table; this spec does not change that, and it is in scope of ST-28's §13 language pass on AI journal summarisation.
- **Moving any AI journal output into the Journal later** needs its own §13 confirmation, with the §13.5 roster checked and updated, before it ships.

**Confirmation:** recorded in the v9.15 `qa_evidence_EPIC-02.md` ST-10 entry (Strategy Rules & System Intent Owner, with date).

## 9. Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-11-04 | Initial version. ST-10 (EPIC-02, v9.15, BLG-SPEC-216) against the `site-structure-phase1` §2.3 brief: one `/Journal` page with Reflections, Red flags and Position notes tabs, a shared ticker filter, per-section content and states taken unchanged from `reflections.md`, `red_flag_journal.md` and `positions.md` §Journal View (Reflections card restructured so "View trade" is not nested in the card button); redirects from `/TradeReflection` and `/RedFlagJournal`; the Positions journal view removed in favour of a "Position notes" link; onward links from every item; testable ACs JA-01..JA-21 for `BLG-FE-258`; §13 confirmation section citing §13.1, §13.2 and the §13.5 roster. Head of UX & Design approval and the Strategy Rules & System Intent Owner's §13 confirmation: see the v9.15 `qa_evidence_EPIC-02.md` ST-10 entry. |
