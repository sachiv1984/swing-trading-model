**Owner:** Head of UX & Design
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-11-17 (created — `BLG-UX-08`)

# Site Structure & Usability — First-Principles Re-Review

**Review date:** 2026-11-17
**Reviewer:** Head of UX & Design (agent-mediated, user-directed: "ask them to complete BLG-UX-08 now", 2026-11-17)
**Backlog item:** `BLG-UX-08`
**Programme:** Site Structure & Usability (DL-088), phases 1–3 shipped in v9.15, v9.16 and v9.17
**Code reviewed:** `main` at `9a34051f`
**Baseline:** the Head of UX & Design website review of 2026-11-03 (`main` at `ab7fbf23`), recorded as `IDEA-head-of-ux-20261103-01` to `-07` and `IDEA-frontend-specs-20261103-01` to `-04` in `claude/cycles/2026-11-03__scheduled/cycle_record.md`

---

## 1. Verdict

**The IA verdict stands: "modify substantially, don't redesign."** The programme made the substantial modifications the 2026-11-03 review asked for, and the structure they produced holds up. Nothing found here calls for a redesign. Nine of the ten baseline metrics reached their target or better. One part of the top 5, the "Today" home page, is only partly done: the list itself works, but on a quiet day the page below it still shows 11 empty-state boxes, the same as before. That gap and three smaller ones are filed as new backlog items (§5).

## 2. Method

The same method as 2026-11-03, against the same first-principles target (a trader opens the app, sees what the strategy says to do today, does it in as few steps as possible, and reviews the week in one journey):

- **Label audit:** sidebar entry vs page heading vs command-palette label vs browser-tab title, from `src/Layout.js` `NAV_AREAS`, `src/lib/pageLabels.js`, each page's `PageHeader`/`<h1>`, and `docs/reference/glossary.md` §UI Labels.
- **Inter-page link scan:** each page's `PageHeader` `parent`/`onward` props and in-page `OnwardLink`s, checked against `navigation.md` §Onward Links.
- **Page-section order:** `DashboardHome.js`, `Positions.js`, `TradePlan.js`, `Performance.js` against their specs.
- **Four journey walkthroughs** (daily review, exit, signal → entry, weekly review), with page and input counts traced through the routes and components.
- **Light and dark screenshots:** the committed Playwright visual baselines (`tests/e2e/__snapshots__/visual-regression-baselines.spec.js/`, regenerated at v9.17 ST-08, `022f62a6`): Dashboard, Positions, Trade Plan, Performance and Settings in both themes. No staging session was used. The sidebar background in the full-page captures stops at the viewport height; the sidebar is `fixed` (`Layout.js`), so this is a capture artefact, not a defect.

## 3. Baseline Metrics — Before and After

| Metric | 2026-11-03 | Target | 2026-11-17 | Result |
|--------|-----------|--------|-----------|--------|
| Unchecked entry routes into Trade Entry | 3 | 0 | 0. The sidebar link, the Positions "New Position" button and the `n` shortcut all reach `TradeEntry.js`, which shows the §4.2 pre-entry checks unless the entry is linked to a plan whose checks passed or were acknowledged (`position_form.md` §Pre-Entry Checks; v9.15 ST-01, v9.16 ST-05) | ✅ Met |
| Sidebar entries / groups | 18 / 4 feature groups, 3 collapsed | ~12 visible, ≤5 groups | 19 entries / 5 job-based areas (Today, Portfolio, Find trades, Review, Settings); 5 visible by default (Today and Portfolio expanded, plus the active area) | ✅ Met. The total rose by 1 (Trade Plans and Research added; Reports, Analytics, Reflections and Red Flag Journal merged into 2) |
| Undiscoverable pages | 2 (Trade Plans, Research) | 0 | 0. Both have sidebar entries; detail pages (Trade Plan, Notification History, Notification Preferences) have parent links | ✅ Met |
| Dead-end pages | 8 | 0 | 0 in the populated state. Every row in `navigation.md` §Onward Links is built, including Journal's "View trade"/"Open position" and Performance → Trade History (v9.17) | ✅ Met |
| Pages from signal to entry | 5 (Signals → Watchlist → Research → Trade Plan → Trade Entry) | 2 after the signal | 3 including Signals (Signals → Trade Plan via "Plan this" → Trade Entry), so 2 after the signal. Ticker, market and price are pre-filled | ✅ Met from Signals and Screener. From the Dashboard's "New signals" group it is 4 (via Research): finding F4 |
| Positions default columns | 14 | ~6 | 6 data columns (Ticker, Price, Stop, To stop, P&L %, Action needed) plus Actions; the rest in an expandable row; urgency order; cards below `md` | ✅ Met |
| Grace surfaces | 4 detail surfaces | 1 (+2 links) | 1 detail view (Positions grace view); the Dashboard "In Grace Today" card and the Risk Dashboard panel link to it (`?grace=open`) | ✅ Met for detail. The Dashboard still shows 4 grace counts with 3 definitions: finding F2 |
| Journal surfaces | 3 | 1 | 1 (Journal: Reflections, Red flags, Position notes). Old routes redirect | ✅ Met |
| Mismatched page names | 7 | 0 | 0. Every sidebar entry, heading, palette label and tab title reads from `PAGE_LABELS`; "trade" vs "position" follows glossary §"Trade" or "position" | ✅ Met |
| Browser-tab titles | 0 of 25 pages | all | 22 of 22 routed pages, plus "Page not found" (`Layout.js` sets `document.title` on every route change) | ✅ Met |

Other values the 2026-11-03 ideas set targets for:

| Metric | 2026-11-03 | 2026-11-17 | Result |
|--------|-----------|-----------|--------|
| Regime position on the Dashboard | Row 4, inside Signal Status | Row 1, first line of "Due today" | ✅ |
| Empty-state boxes on a quiet day | 11 | 11 below a one-line "Nothing due today" (5 Morning Briefing cards, the AI briefing, 3 status cards, Recent Activity, What's New; both themes) | ❌ Not met: finding F1 |
| Banners above the Positions table | 4 | 1 warning strip | ✅ |
| Duplicated KPI sets (Reports vs Analytics) | 2 | 1 (`performance.md` §5 one home per KPI) | ✅ |
| Long single-scroll pages without sections | 3 | 0 (Performance has a section index; Trade Plan and Strategy Benchmark have "On this page") | ✅ |
| Inverted FX label | 1 | 0 ("FX rate — USD per £1 (GBP/USD)" on entry and exit) | ✅ |
| Hard-coded 1.27 FX default on Trade Entry | Yes | No (live rate from `GET /market/status`) | ✅ |
| Light-theme contrast on routed pages | Piecemeal failures | Every routed page scanned by axe in the light theme in CI (v9.17 ST-08); component remainder in `BLG-FE-288` | ✅ |

## 4. Journey Walkthroughs

**Daily review.** Dashboard → "Due today" lists market regime (US, UK), exits due, grace ending today, stops moved and new signals, in that order, each one click from its action. Before: scan 13 equal blocks, with the regime in row 4. This is the journey the programme improved most. On a quiet day, the list collapses to one line, but the 11 empty boxes below it remain (F1).

**Exit.** Dashboard "Exits due" item → Positions with the exit dialog already open (`?exit=<id>`): 2 pages, 1 click. The dialog asks for shares, exit price, date, FX (US only), reason and an optional note. Shares and FX are pre-filled. No change needed.

**Signal → entry.** Signals or Screener "Plan this" → Trade Plan (ticker, market, price and signal context pre-filled; the §4.1 suggested size shows before the shares field once entry and stop are set) → "Start trade" → Trade Entry with the plan linked: 3 pages, down from 5. From the Dashboard "New signals" group, each signal links to Research, not to "Plan this", which adds a page (F4).

**Weekly review.** Sidebar Review → Weekly Digest. The digest's alert counts link to Notifications, but its P&L, compliance and red-flag figures link nowhere, so the user goes back to the sidebar for Performance, then Journal, then Trade History: 4 pages, 3 of them by sidebar, and the Review area is collapsed by default. Before the programme this journey crossed Reports, Analytics, Reflections and Red Flag Journal (6 pages), so it is shorter, but it is still not one journey (F3).

## 5. Top 5 From 2026-11-03 — Status

| # | 2026-11-03 top 5 | Status |
|---|------------------|--------|
| 1 | Checked entry on every route | **Stands, done.** 0 unchecked routes |
| 2 | "Today" home page | **Stands, partly done.** The list works and the regime is first. The quiet-day page is not yet a single line (F1) |
| 3 | Job-based navigation | **Stands, done** |
| 4 | One vocabulary | **Stands, done** |
| 5 | One place per concept | **Stands, done for detail views.** The Dashboard's grace counts still disagree in definition (F2) |

**Revised top 5 for what is left** (all P3, all modifications, none structural): (1) quiet-day Dashboard (F1); (2) one grace definition on the Dashboard (F2); (3) weekly review as one journey from the digest (F3); (4) "Plan this" from the Today list (F4); (5) finish the component colour sweep (`BLG-FE-288`, already filed).

## 6. New Findings (Filed)

| Ref | Finding | Backlog item |
|-----|---------|--------------|
| F1 | On a quiet day the Dashboard shows "Nothing due today" and then 11 empty-state boxes (both themes, `dashboard-home-*-chromium.png`). The 2026-11-03 target was 1. `dashboard.md` §3 v4.0 kept the briefing panel and status cards below the list unchanged, so this is a spec revision, not a defect | `BLG-UX-11` |
| F2 | The Dashboard shows grace in 4 places with 3 definitions: "Positions to Watch" (`grace_period === true`, links to `/Positions`, not the grace view), "Open Positions" ("N in grace", `grace_days_remaining > 0` or status `GRACE`), "In Grace Today" (links to the grace view), and the Today list "Grace ends today" (`grace_days_remaining === 1`). Surfaces that count the same thing differently can disagree, the risk `BLG-BE-183` showed | `BLG-FE-308` |
| F3 | Weekly Digest figures other than alert counts have no onward link, so the weekly review needs 3 sidebar hops (Performance, Journal, Trade History) | `BLG-UX-12` |
| F4 | The Today list's "New signals" rows link to Research, so signal → entry from the Dashboard is 4 pages, against 3 from Signals or Screener | `BLG-UX-13` |

No finding needs a P1 or P2. Nothing found contradicts `strategy_rules.md` or moves a §13 boundary.

## 7. Sign-off

- Reviewed by: Head of UX & Design (agent-mediated, §5.3; user-directed 2026-11-17)
- Date: 2026-11-17
- Confirm-or-revise statement: **Confirmed** — the IA verdict "modify substantially, don't redesign" stands. Top 5 items 1, 3 and 4 are done; items 2 and 5 are partly done, with the remainder filed as `BLG-UX-11` and `BLG-FE-308`.
