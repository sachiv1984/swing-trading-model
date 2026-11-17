**Owner:** Head of UX & Design
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-11-17 (§15 Gap Analysis added at the user's request; no new items); prior — 2026-11-17 (§14 Target State added at the user's request; 1 item filed); prior — 2026-11-17 (§13 Competitors and Best-in-Class Experiences added at the user's request; 5 items filed); prior history retained — see prior entries in version control

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

---

## 8. Content Review (added 2026-11-17, user request)

Added at the user's request after §1–§7 were filed: a review of the words on the site, against 15 criteria, with Keep / Change / Remove / Add for the important pages. Method: the visible copy (headings, page descriptions, labels, helper text, empty states, buttons, tooltips) was extracted from `src/pages/` and the components they render on `main` at `6813c15c`, and read against the light/dark baselines.

**Context for the criteria.** This is a single-user decision-support tool for one trader running one rules-based strategy, not a public site selling a product. Criteria written for marketing pages are applied in their in-app sense below. Where a criterion has no in-app meaning, it says N/A and why, rather than being skipped.

### 8.1 Findings by Criterion

| Criterion | Assessment | Evidence |
|-----------|------------|----------|
| Headline clarity | **Mostly good.** One canonical label per page (§3). Weak spots: the Dashboard subtitle "Session summary — live data" describes the data, not the job; "Due today" (the Today list title) is clear | `DashboardHome.js`; `TodayList.js` |
| Value proposition | **Missing in-app.** Nothing in the app says what it is for (a momentum strategy, ATR stops, a human who decides). The product also has three names: "Position Manager" (sidebar, tab title, PDF export), "Swing Trading Position Manager" (`index.html` meta) and "Momentum Trading Assistant" (changelog, backlog) | `Layout.js:543`, `pageLabels.js:73`, `public/index.html:7` |
| Product/service explanations | **Strong at the point of use, absent overall.** Stop provenance, the FX hint ("How many US dollars £1 buys."), "Initial Stop (set by system)" and the Trail Stop note ("for reference only") explain well. Nothing explains the strategy's core ideas (R, ATR, grace period, regime, heat) in one place | `StopProvenance.js`, `TradeEntry.js`, `Positions.js` |
| Differentiation | **N/A as marketing.** There is no competing product to set the app against. In-app sense: does the app make clear what is *system-set* vs *user-set*? Mostly yes ("set by system", "fixed by the strategy rules"); the Settings page description contradicts it (below) | `Settings.js` |
| Readability | **Good on action pages, poor on Weekly Digest.** The digest renders a `Field / Unit / Value` table with API-style labels ("Unrealised P&L Delta (7d)", "Data Staleness", "As of (UTC)", unit "timestamp") | `WeeklyDigest.js:57-64` |
| Tone of voice | **Consistent, plain, second person.** One outlier: the exported Performance report uses corporate headings ("Executive Summary", "Key Insights") | `AnalyticsSection.js` export HTML |
| Excessive copy | **Low on pages; high on the quiet Dashboard** — 11 empty-state boxes each with a heading and a sentence (finding F1, `BLG-UX-11`). Positions rows carry 4 secondary actions (Mark Reviewed, Recheck Compliance, View Trail, Trade Plan) | Dashboard baselines; `Positions.js` |
| Missing information | (1) The gate strip says "20 more to unlock quality insights" without saying which insights. (2) Signals' "Top N" and "Lookback Days" controls have no explanation. (3) The Trade Plan "Setup Quality Score: Low" gives no reason on the collapsed panel. (4) No help or FAQ (below) | `GateProgressStrip.js:42`; `Signals.js`; `SetupQualityScorePanel.js` |
| Terminology/jargon | (1) **84 strategy-rule references** ("§7.2", "§4.1", "§8.1") in user-visible copy across 15 files, fixed one at a time so far (`BLG-UX-06`, `BLG-UX-09`). (2) Internal IDs: "SI-02 Gate Status" heading on Performance. (3) Raw values: Trade Plan "Regime at Entry" shows `risk_on`. (4) "Live heat unavailable — showing entity data fallback" on Risk Dashboard | `ReportViews.js:502`; `TradePlan.js:976`; `RiskDashboard.js:104` |
| CTA language | **Good and consistent** (glossary §Primary action labels: New Position, Create Position, Plan this, Save Plan, Confirm Exit). "Click Regenerate to generate your daily summary." repeats itself | `AiDailyBriefing.js` |
| Proof points | **Present, in-app sense:** Replay ("your own past trades through today's strategy rules") and Strategy Benchmark ("live vs backtest") are the app's evidence that the rules work. Strategy Benchmark's description "Compare live trading vs backtest" undersells it | `Replay.js`, `StrategyBenchmark.js` |
| Testimonials | **N/A.** Single user, no prospects to persuade | — |
| Case studies | **N/A as marketing.** The in-app equivalent is Replay of the user's own trades (Keep) | — |
| FAQs | **Missing, and the one help affordance is broken:** the sidebar "Docs" link has an external-link icon and `href="#"` — it goes nowhere | `Layout.js:829-835` |
| Trust content | **Strong.** "AI Advisory — All actions require your confirmation"; stop provenance; signal timing ("generated daily at 4 PM UTC weekdays"); data staleness indicator; "Indicative only — not a tax liability"; fees shown as estimates before save | `AiDailyBriefing.js`, `Signals.js`, `TradeEntry.js` |

### 8.2 Keep / Change / Remove / Add — Important Pages

| Page | KEEP | CHANGE | REMOVE | ADD |
|------|------|--------|--------|-----|
| **App shell** | One label per page; "AI Advisory" label; keyboard legend | Pick one product name (§8.1 Value proposition) | The dead "Docs" link (or make it work) | A short "How this works" entry point (help/FAQ) |
| **Dashboard** | "Due today" and its quiet line "Nothing due today · US … · UK …"; regime badges | Subtitle "Session summary — live data" → say the job (for example "What the strategy says to do today"); "Click Regenerate to generate…" → "Regenerate to get today's summary" | The 11 quiet-day empty boxes (`BLG-UX-11`) | — |
| **Positions** | "Sorted by what needs attention first"; "Action needed"; "To stop" with its tooltip; stop provenance | State tooltips citing "§7.2"/"§6.3" → plain words (policy item) | — | — |
| **Trade Entry** | "Initial Stop (set by system)"; FX label and hint; fee preview "(preview — actual fees calculated on submission)"; the no-plan nudge | "Entry − 5× ATR (§5)" → plain words; description "Add a new trade to your portfolio" → match the glossary's trade/position rule ("Record a new position") | — | — |
| **Trade Plan** | Section index; "Planned Shares (for pre-entry checks)"; checklist | "Regime at Entry: `risk_on`" → "Risk-on (US)"; "Suggested size: … (§4.1, …)" (`BLG-UX-09`) | — | A one-line reason on the collapsed Setup Quality Score |
| **Signals** | "Signals are generated daily at 4 PM UTC weekdays"; "Plan this" | — | — | Helper text for "Top N" and "Lookback Days" |
| **Performance** | "Expectancy — Edge per trade"; "Profit Factor — Gross profit / gross loss" helpers; "Not enough trades" states | "SI-02 Gate Status" → plain heading (for example "Trades needed for quality insights"); exit-condition labels "Stop-loss (§8.1)" → plain; export headings "Executive Summary"/"Key Insights" → match in-app tone | — | — |
| **Journal** | Description "Your reflections, rule red flags and position notes in one place." | — | — | — |
| **Risk Dashboard** | "Daily portfolio risk snapshot — review before making trading decisions." | "showing entity data fallback" → "showing the last saved figures"; "See strategy rules §6" → plain | — | — |
| **Weekly Digest** | Alert-count deep links | The `Field / Unit / Value` table → a readable weekly summary (sentences or labelled figures); "7-day trading summary" → a fuller description | "Unit" column; "As of (UTC)" as a row (show as a caption) | Links to Performance/Journal (`BLG-UX-12`); trades closed this week |
| **Settings** | "These parameters are fixed by the strategy rules … shown for reference"; fee defaults shown inline | Description "Configure your strategy parameters and preferences" contradicts the read-only strategy block → "Set fees, risk limits and preferences. Strategy parameters are shown for reference." | — | — |
| **Strategy Benchmark / Replay** | Replay description | "Compare live trading vs backtest" → say what it shows (for example "How your live trades compare with the backtest of the same rules") | — | — |

### 8.3 Content Findings (Filed)

| Ref | Finding | Backlog item |
|-----|---------|--------------|
| C1 | No site-wide rule for strategy-rule references ("§7.2") in user-visible copy: 84 instances in 15 files, fixed piecemeal by `BLG-UX-06` and `BLG-UX-09`. Some (`src/constants/exitReasons.js`) may be stored values, so a copy change needs a data check | `BLG-UX-14` |
| C2 | The sidebar "Docs" link points to `#` | `BLG-FE-309` |
| C3 | Weekly Digest reads as an API table, not a summary | `BLG-UX-15` |
| C4 | Copy fixes: raw `risk_on`, "SI-02 Gate Status", "entity data fallback", the Settings description, the Dashboard subtitle, "unlock quality insights", terse page descriptions, the exported report's headings | `BLG-FE-310` |
| C5 | No in-app statement of what the app is for or of its core terms, and three product names | `BLG-UX-16` |

**Content verdict:** the copy is clear, consistent and trustworthy where the user acts (entry, exit, plan, stops), which is where it matters most. It is weakest where the app explains itself (no value statement, no help, a broken Docs link) and where it reports (Weekly Digest, the quiet Dashboard). None of this changes the IA verdict in §1.

---

## 9. Accessibility Review (added 2026-11-17, user request)

**Standard:** WCAG 2.2 Level AA as the minimum. Two AAA criteria are recommended on top, for reasons given in §9.4.
**Method:** static review of `src/` on `main` at `23f3e676`; the CI axe scan (`tests/e2e/accessibility-axe-scan.spec.js`, `@axe-core/playwright` 4.13) and its baseline exceptions; the light/dark visual baselines. No screen reader, keyboard-only session or zoom test was run. Results are kept in three classes:

- **Observed:** a failure visible in the code, with file and line.
- **Verified by automation:** a check that already runs in CI and passes.
- **Needs testing:** cannot be settled from code, and needs an automated rule not yet enabled or a manual check.

### 9.1 Findings by Area

| Area | WCAG 2.2 criteria | Status | Finding |
|------|-------------------|--------|---------|
| Colour contrast | 1.4.3 (AA), 1.4.11 (AA) | **Verified by automation** for text: axe `color-contrast` passes on every routed page in the light theme, and on the scanned dark states (v9.17 ST-08). **Needs testing:** component remainder `BLG-FE-288`; dialogs and popovers the scan never opens (Exit, Daily Monitor, heatmap detail); non-text contrast of input borders and focus rings (axe does not test 1.4.11) | — |
| Use of colour | 1.4.1 (A) | **Needs testing.** Regime badges carry text ("RISK-ON"); P&L and heatmap tiles rely partly on green/red | — |
| Keyboard navigation | 2.1.1 (A), 2.1.2 (A) | **Observed — 4 failures.** Controls that work by mouse click only (`onClick` on a non-interactive element, no `tabIndex`, `role` or key handler): (1) Daily Position Monitor rows, which select positions to exit (`MonitorModal.js:94`); (2) Notification History row expansion (`NotificationsHistory.js:286`, a `<tr onClick>` with no button or `aria-expanded`); (3) the Trade History AI journal summary toggle (`TradeHistory.js:530`); (4) Performance monthly heatmap tiles, which open the month detail (`MonthlyHeatmap.js:66`). **Needs testing:** tab order through the Positions expandable rows and section indexes; no keyboard traps in the custom dialogs | A1 |
| Focus indicators | 2.4.7 (AA), 2.4.11 Focus Not Obscured (AA, new in 2.2), 2.4.13 (AAA) | **Observed — weak.** shadcn components draw a `focus-visible` ring, but 16 custom inputs and buttons (Ticker Universe, Signals controls and others) use `focus:outline-none` with only a border-colour change (for example `slate-200` → `slate-400`), likely below 3:1 against the unfocused state. **Needs testing:** 2.4.11 with the fixed mobile header, the Strategy Benchmark sticky bar and the "Press ⌘K" tip, which overlays the top-right of the page (visible in the Dashboard baselines). Section links already set a scroll margin (`SectionIndex.js`) | A4 |
| Heading hierarchy | 1.3.1 (A), 2.4.6 (AA) | **Observed.** The Dashboard has one `h1` and one `h2` ("Due today"). Its other visual headings — Morning Briefing, the 5 briefing cards, Today's Briefing, the 3 status cards and Recent Activity — are `<p>`/`<span>` (`DashboardCard.js:27`, `MorningBriefing.js:10`, `AiDailyBriefing.js:121`), so heading navigation skips them. Other pages use `PageHeader`'s `h1` and `h2`/`h3` sections | A3 |
| Labels and forms | 1.3.1 (A), 3.3.2 (A), 4.1.2 (A) | **Observed — Exit dialog.** Shares to Exit, Exit Price, Exit Date and Exit Note have a visible `<Label>` that is not linked to its input (no `htmlFor`/`id`, no `aria-label`; `ExitModal.js` ~327–440). Only the FX field is linked. The CI scan never opens this dialog, so this was not caught. **Known, tracked:** Trade Entry Risk % and entry date inputs (`label`) and the market select (`button-name`), grandfathered in the scan as `BLG-FE-286`. **Needs testing:** 35 of 52 `<Label>` uses have no `htmlFor`; many inputs carry their own `aria-label`, so each needs checking (What-If sizing, alert thresholds, watchlist fields, custom price alerts) | A2 |
| Accessible names | 4.1.2 (A), 2.5.3 Label in Name (A) | **Observed — 1.** The Screener "add to watchlist" popover close button is an `X` icon with no name (`Screener.js:339`). A static scan flagged 17 more, which on inspection carry text inside conditional expressions; axe `button-name` covers those it reaches. The AI chat send button is named ("Send question") | A2 |
| Image alternatives | 1.1.1 (A) | **Verified (static).** No `<img>` without `alt` in `src/`; icons are `lucide-react` SVGs, mostly `aria-hidden` beside text. **Needs testing:** charts (Recharts) expose no text alternative beyond the surrounding figures | — |
| Semantic structure | 1.3.1 (A), 2.4.1 (A), 3.1.1 (A), 4.1.2 (A) | **Verified (static):** `lang="en"`; `nav`, `aside` and `main` landmarks (`Layout.js`), which satisfy 2.4.1 Bypass Blocks. **Observed:** the heatmap month detail is a custom overlay with Escape support but no `role="dialog"`/`aria-modal` (`MonthlyHeatmap.js:131`). **Recommended:** a "Skip to content" link, because about 19 sidebar links precede `main` | A1 |
| Link purpose | 2.4.4 (A) | **Mostly good.** Onward links name their destination (glossary labels); Research icon links are named "Research {TICKER}". **Observed:** the sidebar "Docs" link goes to `#` (filed as `BLG-FE-309`). "View trade" relies on its row for context, which 2.4.4 allows | — |
| Error handling | 3.3.1 (A), 3.3.3 (AA), 4.1.3 Status Messages (AA) | **Good on Trade Entry** (`aria-invalid` plus a described message, for example "FX rate missing for US trades. Enter the rate to save."). Toasts are Radix and announced. **Needs testing:** only 3 fields in the app set `aria-invalid`; other forms (Exit dialog, Trade Plan, Settings, alert thresholds) may rely on a disabled submit or a toast with no field-level message. `BLG-UX-06` already covers one save-time error shown only in a toast | A5 |
| Motion | 2.2.2 (A), 2.3.3 (AAA) | **No AA failure found:** entrance fades are short, and loaders pulse only while loading. **Observed:** `framer-motion` is used in 17 files and only one place reads `prefers-reduced-motion` (`Positions.js:1140`); heatmap tiles scale on hover | A4 |
| Zoom/reflow | 1.4.4 (AA), 1.4.10 (AA), 1.4.12 (AA) | **Verified (static):** the viewport meta allows zoom. Positions switches to cards below `md`; Performance has 375/390 px Playwright checks. **Needs testing:** reflow at 320 CSS px / 400% zoom on every page (wide tables scroll inside their cards, which 1.4.10 allows for data tables), and the text-spacing override | A5 |
| Touch target size | 2.5.8 Target Size (Minimum) (AA, new in 2.2) | **No failure observed:** icon buttons are 36 px (`size="icon"`), and the smallest found is exactly 24 px (Screener close). **Needs testing:** 16 px checkboxes on the Trade Plan checklist (pass if the label is clickable or spacing is ≥24 px), inline pills, and the regime badge tooltip trigger. The CI scan sets no `withTags`, so whether axe's `target-size` rule runs depends on axe-core defaults and is not asserted by the test | A5 |
| Other WCAG 2.2 additions | 2.5.7 Dragging (AA), 3.2.6 Consistent Help (A), 3.3.7 Redundant Entry (A), 3.3.8 Accessible Authentication (AA) | 2.5.7: N/A (no drag interactions). 3.2.6: the one help link is broken (`BLG-FE-309`). 3.3.7: met where checked ("Plan this" pre-fills ticker, market and price into Trade Plan, and Trade Entry from a plan). 3.3.8: sign-in is handled outside the app (`AuthContext.js`) and not reviewable here | — |

### 9.2 CI Coverage Gaps (Why Automation Missed the Observed Failures)

- The scan fails only on `serious`/`critical` impact; `moderate`/`minor` findings are logged and ignored.
- It sets no rule tags (`withTags`), so WCAG 2.2 coverage (for example `target-size`) depends on axe-core defaults and is not asserted.
- It does not open dialogs and transient states — the Exit dialog, Daily Monitor, heatmap detail, Screener popover — where 3 of the observed failures live.
- axe cannot test keyboard operability (2.1.1), focus visibility (2.4.7/2.4.11) or reflow, which need a manual or scripted pass.

### 9.3 Findings (Filed)

| Ref | Finding | Level | Backlog item |
|-----|---------|-------|--------------|
| A1 | 4 mouse-only controls (Daily Monitor exit rows, Notification History rows, Trade History AI summary toggle, heatmap tiles); heatmap detail lacks dialog semantics; Screener close button unnamed | A | `BLG-FE-311` (P2) |
| A2 | Exit dialog fields have no programmatic labels | A | `BLG-FE-312` (P2) |
| A3 | Dashboard section titles are not headings | A (1.3.1) | `BLG-FE-313` |
| A4 | Weak focus indicator on 16 custom controls; no reduced-motion handling | AA (2.4.7) / AAA (2.3.3) | `BLG-FE-314` |
| A5 | CI scan gaps (§9.2) and the manual checks above | — | `BLG-QA-269` (scan), `BLG-QA-270` (manual pass) |

A1 and A2 are Level A failures on core journeys (exiting a position, the daily monitor), so they are filed at P2, above the content and structure findings.

### 9.4 Standard

AA is the right minimum for a single-user app. Two AAA criteria are worth adopting because the app is built for keyboard use (shortcuts, command palette) and uses a lot of animation, and each is cheap: **2.4.13 Focus Appearance** (a clear, consistent focus ring, which A4 delivers) and **2.3.3 Animation from Interactions** (respect `prefers-reduced-motion`, also A4). A full AAA target is not recommended: 1.4.6 Enhanced Contrast (7:1) would mean re-tokenising the colour system v9.17 just finished, for little gain.

**Accessibility verdict:** text contrast, landmarks, image alternatives and most labelling are in good shape, and CI guards them. The observed failures are concentrated in places the automated scan does not reach — dialogs, custom click targets and the Dashboard's heading structure — so the main recommendation, besides fixing A1–A4, is to widen the scan and run one manual keyboard and screen-reader pass (`BLG-QA-269`, `BLG-QA-270`).

---

## 10. Technical Quality and Performance Review (added 2026-11-17, user request)

**Method:** a local production build (`npm run build`, `react-scripts` 5, built from `main` after the last source change), its source map, HTTP headers from the live GitHub Pages site (`curl -I`, 2026-11-17), the data-fetching code, `docs/specs/frontend/performance_budget.md` (v1.0) and `docs/ops/api_performance_baseline.md`.

**No field or lab Web Vitals data exists.** There is no RUM (`web-vitals` is not installed), no Lighthouse run in CI, and the budget's baseline reading has been "TBD" since v2.6. The app has a single user, so CrUX field data will not exist either. So **no LCP, INP or CLS value is reported here.** Where a section says "likely", it is an inference from the code, and it is listed under "needs testing".

### 10.1 Findings by Area

| Area | Observed | Needs testing |
|------|----------|---------------|
| **Core Web Vitals (LCP, INP, CLS)** | No measurement exists (above). The budget targets LCP ≤ 2,500 ms, but only on an unthrottled desktop; it has no INP or CLS target (INP replaced FID in 2024) and still uses TTI, which Lighthouse no longer reports | LCP, INP and CLS on Dashboard, Positions, Trade Plan and Performance, on a mobile profile (Lighthouse "Slow 4G", mid-tier CPU) and on desktop |
| **Rendering approach** | Client-side-rendered SPA (Create React App, `HashRouter`) on GitHub Pages; the HTML is a 1.7 KB shell plus a 1-line GitHub Pages SPA redirect script. Nothing paints until the full JS bundle has downloaded, parsed and run, and then data loads from the Render API. For a single-user authenticated tool, CSR is a reasonable choice; SSR is not recommended | Time from navigation to first paint on mobile |
| **LCP (likely drivers)** | (1) The single 552 KB (gzipped) bundle must load before anything renders. (2) Every `PageHeader` fades in from `opacity: 0` (`PageHeader.js:19`, framer-motion), and Chrome does not count an element for LCP while it is invisible, so the heading — often the LCP element — is held back by the animation. (3) Page content waits on the API: the last measured `GET /positions` was p50 244 ms / p95 547 ms (v2.7); later baselines are estimates, and the Render service can cold-start (RFM-01, "tens of seconds") | Actual LCP element and time per page; effect of removing the fade |
| **INP** | No obvious long tasks found in code review. Candidates: Positions (sorting/expanding many rows), Performance charts (Recharts re-render on period change), Screener filters | INP on those interactions (Chrome DevTools Performance / web-vitals) |
| **CLS** | Loading states use skeletons (`animate-pulse`). But the Today list, the briefing cards and the status cards each swap a skeleton for content of a different height as their queries resolve, so content below can shift. The fixed "Press ⌘K" tip does not shift layout | CLS on the Dashboard as its ~16 queries resolve |
| **Loading behaviour** | **Duplicate requests on the Dashboard:** about 16 queries on load. `GET /positions` is fetched 4 times under 4 different query keys (`home-open-positions`, `home-grace-period`, `today-positions`, `morning-positions`), and `GET /signals` twice (`today-signals`, `morning-screener-hits`). The Morning Briefing earnings card makes one request per open position (`useQueries`, `EarningsAlertCard.js:17`). The query client sets no `staleTime` (`query-client.js`), so every page visit refetches everything | Request count and waterfall on a cold and a warm load |
| **JavaScript weight** | **Over budget.** One bundle, `main.*.js`: 1,992 KB minified, 542 KB gzipped locally, 552 KB served. `performance_budget.md` §3.3 sets ≤ 200 KB for the main bundle and ≤ 500 KB in total. **No code splitting:** no `React.lazy`/dynamic `import()`, so all 22 pages and every chart load on first visit. Approximate composition by source size (source map): app code 23%, Recharts 16%, react-dom 10%, framer-motion/motion-dom 9%, react-router 6%, TanStack Query 4%, moment 3%, Redux Toolkit 3% (pulled in by Recharts), date-fns 3%, lucide-react 3%, react-day-picker 3%. **Duplicates:** two date libraries (`moment` is imported only by `SystemStatus.js`; `date-fns` everywhere else) and two toast systems (`sonner` and the Radix toaster, both mounted in `App.js`) | Parse and compile time on a mid-tier phone |
| **Resource loading** | One deferred script and one stylesheet (121 KB, 20 KB gzipped); no preload/preconnect hints. The API origin (Render) is not preconnected, so the first API call pays DNS, TCP and TLS after the bundle runs | Effect of `<link rel="preconnect">` to the API origin |
| **Caching** | GitHub Pages serves everything, including content-hashed bundles, with `cache-control: max-age=600` and an ETag. Repeat visits after 10 minutes revalidate (a cheap 304), but the hashed assets could be cached as immutable for a year. GitHub Pages does not allow custom headers; this matters little for a single user and is not worth a hosting move on its own | — |
| **Compression** | gzip only, no Brotli (a GitHub Pages limit). Brotli would save roughly 15–20% more on the bundle; same hosting caveat | — |
| **Image optimisation / responsive assets** | **N/A in practice.** No raster images in `src/` (no `<img>`); icons are inline SVG (lucide-react, tree-shaken named imports); no web fonts (system font stack). Charts are SVG | — |
| **Third-party scripts** | **None in the browser.** No analytics, tag managers, fonts or CDN scripts; the only external origin is the app's own API. Market data (Yahoo, Alpaca) and AI calls go through the backend | — |
| **Mobile performance** | Positions has a card layout below `md`; Performance has phone-width checks. The full 552 KB bundle and the same ~16 Dashboard requests apply on a phone, including when the Telegram digest sends the user into the app | Lighthouse mobile run; real-device check on the digest → Dashboard and Positions paths |
| **Build hygiene** | **Public source map:** the live site serves `main.*.js.map` (9.1 MB, HTTP 200), so the full front-end source is downloadable. It does not slow users down (browsers fetch it only with DevTools open), but it exposes code and comments. CRA emits it by default; `GENERATE_SOURCEMAP=false` is not set in `deploy.yml` | — |

### 10.2 Recommendations (Most Value First)

1. **Route-level code splitting** (`React.lazy` + `Suspense` per page in `App.js`/`pages.config.js`). Recharts then loads only on Performance, Strategy Benchmark, Risk Dashboard and Settings (AI spend chart). This is the main way to get back under the budget's 200 KB main-bundle limit. → `BLG-FE-315`
2. **Remove duplicate libraries:** replace `moment` in `SystemStatus.js` with `date-fns`, and keep one toast system. → `BLG-FE-315`
3. **Stop the duplicate Dashboard requests:** share one query key for `GET /positions` and one for `GET /signals`; set a default `staleTime` (for example 30–60 s); batch the per-position earnings lookups into one request. This cuts Dashboard load requests from about 16 + N to about 10, and lowers backend and Yahoo load (relevant to `BLG-OPS-217`). → `BLG-FE-316`
4. **Do not start page headers at `opacity: 0`.** Keep a translate-only or no entrance, and respect reduced motion (with `BLG-FE-314`). → `BLG-FE-317`
5. **Measure, then budget:** add `web-vitals` reporting (to the console or a lightweight endpoint) and a Lighthouse CI job (mobile and desktop) for the four main pages; update `performance_budget.md` to Core Web Vitals (LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1, mobile profile), drop TTI, record the first baseline, and add a bundle-size check to CI. → `BLG-QA-271`
6. **Stop publishing source maps** (`GENERATE_SOURCEMAP=false` in the deploy build, or upload them privately if error tracking needs them). → `BLG-OPS-221`
7. **Preconnect to the API origin** in `public/index.html` (one line; include in `BLG-FE-316`). Immutable caching and Brotli need a host that allows custom headers (for example Cloudflare Pages); not recommended unless measurements show it matters.

**Technical verdict:** for a single-user, authenticated, CSR app with no third-party scripts and no images, the asset side is lean, except JavaScript. The bundle is 2.7× its own budget because nothing is code-split, and the Dashboard repeats its main API call four times. Both are straightforward fixes. No Web Vitals have ever been measured, so the first step is to measure (`BLG-QA-271`), then confirm the gains from items 1–4 against that baseline.

---

## 11. Where AI Could Genuinely Help (added 2026-11-17, user request)

**Test applied:** each candidate must solve a real user problem *better than conventional UX* — a filter, a pre-filled field, a deterministic rule, plain copy — and stay inside `strategy_rules.md` §13. §13.2 says the system "is not … a machine-learning or AI-driven prediction system" and that AI-written text "must not suggest changing stops, position sizing, setups or any other strategy parameter". Every new AI surface needs its own §13 review before it ships (§13.5).

### 11.1 Evidence: How the Existing AI Is Used

Seven AI features ship: daily briefing, chat ("Ask Advisor"), trade plan generation, setup thesis, post-trade debrief and journal summary (the six measured below), plus the monthly P&L narrative added in v9.11, after the measurement window. The only production usage data is `docs/ops/ai_feature_usage_review_2026-09-24.md` (102 days, 2026-06-25 to 2026-10-05):

- **31 AI calls in total, about $0.17.** 23 of them fell in the first week after launch.
- Daily briefing: used on 2 days, last 2026-06-30. Chat: 10 calls, last 2026-08-17. Plan generation: 7 calls.
- Setup thesis, trade debrief and journal summary: **never used.**
- The chat widget appears only on Positions and Signals (`AiChatWidget.js`).

**What this means for the review:** the binding constraint is not a lack of AI capability, it is that the AI already built is rarely used. Adding more AI would add §13 review work, cost and failure modes for features with no evidence of demand. The next usage review is scheduled for 2027-01-03 (`BLG-GOV-382`) and should decide whether to keep, re-place or retire each never-used feature. That is a higher-value AI action than any new capability below.

### 11.2 Candidates Assessed

| Capability | User problem it would solve | Why AI rather than conventional UX? | Data it would need | Risks | When the AI is wrong | Verdict |
|------------|---------------------------|--------------------------------------|--------------------|-------|----------------------|---------|
| **Intelligent search** (natural-language search across trades, plans and journal) | Finding a past trade by situation ("trades I exited early in a risk-off week") | **Weak case.** One user, a few hundred records. Trade History already has filters, saved filters, tags and a calendar; Journal filters by ticker; the command palette finds pages, tickers and plans | Trades, journal, plans, regime history | Misparsed queries silently drop results; the user cannot see why a trade is missing | User acts on an incomplete set (for example a review that misses losing trades) | **Not recommended.** Add a structured filter (for example regime at exit) if this need appears |
| **Natural-language discovery** (of signals or tickers) | "Find me momentum stocks like X" | **Ruled out by §13.2:** signals come from one fixed, deterministic rule set. AI-ranked or AI-described candidates are discretionary selection by another route | Market data, signal history | Strategy drift; the user trusts an AI pick over the rule | A trade outside the strategy | **Not recommended (boundary)** |
| **Guided navigation** | Knowing what to do next | **Already solved deterministically.** The "Due today" list orders regime → exits → grace → stops → signals by the strategy's own rules, each one click from its action (§4) | — | Non-deterministic ordering of safety-critical items | An exit is pushed below the fold | **Not recommended.** Keep the rules-based list |
| **Recommendations** (trades, sizes, stops) | "What should I do?" | **Ruled out by §13.2** (no suggesting changes to stops, sizing, setups or parameters; no prediction) | — | Direct strategy breach | Real financial loss | **Not recommended (boundary)** |
| **Personalised journeys** | Different paths for different users | **No problem to solve:** one user, one fixed daily routine | Behaviour history | Unpredictable UI | User cannot find a page that moved | **Not recommended** |
| **Conversational assistance** | Asking a question about one's own data that no single page answers ("which trades this quarter broke a rule, and in what regime?") | **Plausible.** The answer joins trades, journal, regime and plan data that the UI shows across several pages; the chat already does this with portfolio context | Already passed to chat (positions, regime, trades); would add the selected trade/position | Wrong numbers stated confidently; drift towards advice (§13.2) — already governed by the chat's §13 review and output checks | User draws a wrong lesson from a misstated figure. Mitigation: show the source records with each answer, and keep the existing advisory label and disclaimer | **Conditional — reuse, don't add.** See 11.3 |
| **Content summarisation** (weekly or monthly review in prose) | The Weekly Digest is hard to read (§8, `BLG-UX-15`) | **Weak case.** The problem is presentation, and a deterministic template with exact figures fixes it. The monthly AI narrative (v9.11) and journal summary already exist; the journal summary has never been used | Weekly figures, trades, red flags | AI misstating P&L or compliance; cost per view | User trusts a wrong summary figure over the table | **Not recommended.** Fix the layout (`BLG-UX-15`); revisit only if the monthly narrative shows real use at the 2027-01-03 review |
| **Support automation** | — | **N/A:** a single user, no support function | — | — | — | **Not applicable** |
| **Intelligent forms** (AI-filled trade plans or reflections) | Typing effort on Trade Plan (about 14 fields) | **Mostly solved conventionally:** "Plan this" pre-fills ticker, market, price and signal context; the suggested size fills from §4.1. AI plan generation (7 uses) and thesis/debrief (0 uses) already exist. The thesis is the trader's own reasoning — generating it removes the point of writing it | Signal, research, price data | The trader adopts an AI thesis they did not form; a plan that looks considered but isn't | A trade entered on AI-written reasoning | **Not recommended** beyond what exists. Remove or relocate the unused generators if the 2027-01-03 review confirms no use |
| **Contextual help** ("why is this flagged?", "what is ATR?") | Strategy terms and rule references are unexplained (§8: 84 "§x.y" references; no glossary in the app) | **Weak case.** Explanations must be exact and identical every time; a static glossary plus deterministic "why" text (stop provenance already does this well) is better and cheaper | Glossary, rule text | Paraphrase that subtly misstates a rule | User misunderstands a stop or exit rule | **Not recommended.** Use plain copy and an in-app "How this works" view (`BLG-UX-14`, `BLG-UX-16`) |

### 11.3 The One Recommendation

**Put the existing chat where the questions arise, and only if the 2027-01-03 review keeps it.** A scoped "Ask about this trade" entry on a Trade History row, a Journal entry or Performance, which opens the existing chat with that trade preselected as context. This adds no new model, endpoint or capability. It reuses a §13-reviewed surface, so it needs a §13 re-attestation for the changed context, not a new review.

- **Problem it solves:** questions about past trades come up during review, not on Positions or Signals, the only two pages where the chat appears today.
- **Why AI:** the questions are open-ended and join several data sources; a fixed report would answer only the questions someone anticipated.
- **Data:** the existing chat context plus the selected trade's record, plan and journal entries.
- **Risks:** confident misstatement of figures; the answer reading as advice.
- **When wrong:** each answer names the records it used (so a wrong figure can be checked against the trade row on the same screen), keeps the "AI Advisory" label, and is subject to the existing §13.2 output checks.
- **Measured by:** the shipped chat engagement metric (`BLG-FEAT-60`) — if contextual entry does not raise use, remove it.

Filed, gated on that review's outcome, as `BLG-UX-17`.

**AI verdict:** no new AI capability is recommended. The evidence says the opportunity is in making the existing AI findable at the point of need, or retiring what is unused, not in adding more. Most of the candidate areas are already solved better by deterministic UX, and two (discovery and recommendations) would breach the strategy's own boundary.

---

## 12. Trust, Privacy and Security Messaging (added 2026-11-17, user request)

**Perspective:** what a user sees and is told, not a penetration test. **No technical vulnerability is claimed below unless it was demonstrated.** I made no calls to the production API and did not load the live app with data. The only live checks were header-only and static-file requests to the public GitHub Pages site (`robots.txt` and the source map), and `gh repo view` for repository visibility. Where a point depends on running the live app, it says so.

**Context:** a single-user personal tool. The only user is the owner, who is also the operator. Many consumer-site obligations (cookie consent, privacy notice, data requests) therefore apply differently or not at all — but the user's data is their own **real personal financial data**: manually recorded real trades, fills, cash balance, P&L and journal reflections.

### 12.1 Findings by Area

| Area | Assessment | Evidence |
|------|------------|----------|
| **Cookie consent** | **No cookies set** by the app and no third-party scripts (§10). Browser storage: `localStorage` `theme` and `command-palette-tooltip-seen`; `sessionStorage` `nav-group-collapse` — all functional preferences. Also, legacy placeholder data written to `localStorage` on every load and never read: a fake £10,000 "Main Portfolio" and both market regimes set to `risk_on` (`src/utils/initializeData.js`, called from `index.js`). No consent banner, which is appropriate for an owner-only tool with no tracking | `Layout.js`, `initializeData.js` |
| **Privacy communication** | No privacy notice, and none is needed while the owner is the only user. **Not disclosed in the UI:** portfolio context (positions, cash, P&L, journal text) is sent to an AI provider (Anthropic) when AI features are used; alerts and the weekly digest (P&L and compliance figures) go to Telegram; data is stored with third-party processors (Supabase, Render). The AI disclaimer says only "AI responses are advisory only. All trade decisions require human confirmation." | `AiDisclaimer.js`, `alerts_service.py`, `si05_digest_service.py` |
| **Trust indicators** | **Strong for decision trust:** the "AI Advisory" label, stop provenance, signal timing, data-staleness indicator, "Indicative only — not a tax liability", fee estimates before save (§8). Weak point: the AI chat is titled "**AI Trade Advisor**" / "Ask Advisor", which may read as regulated advice — the strategy's own boundary (§13) is decision support, not advice | `AiChatWidget.js` |
| **Account/security messaging** | **There is no sign-in.** `AuthContext.js` hard-codes a single user and logs "Single-user mode active (no authentication required)"; there is no sign-out, session or account page. The front end is a static site on GitHub Pages; the repository is **public**, the site URL is published in `package.json`, and there is no `robots.txt` (404) or `noindex`. The backend API key the front end uses is embedded in the public bundle with full read and write scope — **already documented and risk-accepted** by the Product Owner (`docs/operations/credential_policy.md` §1.1, ESC-EXEC-20261015-01, 2026-10-15). Nothing in the UI tells the user the app is open to anyone who has the URL | `AuthContext.js`, `credential_policy.md` §1.1 |
| **Data requests** | Owner-only, so subject-access or erasure requests do not arise. Data portability exists: CSV export (Trade History), PDF export (Performance, Weekly Digest) | `DownloadCsvButton.js`, `ExportModal.js` |
| **Forms requesting sensitive information** | No passwords, payment details, broker credentials or ID documents are requested in the UI (broker and AI keys are server-side environment variables). Forms do collect sensitive personal financial data (trade sizes, fills, cash movements, journal notes), which is expected for the product | Trade Entry, Exit, Cash Management |
| **Misleading interaction patterns** | (1) **Notification Preferences say alerts are sent "by email"** (page description and toggles), but delivery is via **Telegram**; there is no email sending in the backend. (2) If Telegram is not configured, a notification is recorded as `delivered = TRUE` with error "email not configured", and the UI never shows delivery status, so the user cannot tell alerts are not arriving. Whether Telegram is configured in production was not checked. (3) Ticker Universe asks "**Permanently** deactivate X? (It can be re-added later.)" — contradictory | `NotificationPreferences.js:116`, `alerts_service.py:1053–1100`, `TickerUniverse.js:279` |
| **Dark patterns** | **None found.** No pre-ticked checkboxes (0 `defaultChecked`/`checked={true}`); no confirm-shaming (the no-plan nudge reads "Consider creating one before entering — or continue without."); destructive actions are confirmed (trade plan delete, exit, deactivate); the pre-entry acknowledgement is opt-in and required only when checks warn | — |
| **Transparency** | Good on how numbers are derived (stop provenance, fee preview, suggested size). Gaps: the third-party data flows above, the email/Telegram mismatch, and the open-access posture | — |

### 12.2 Needs Specialist Review

**Security (Cybersecurity & Trust Lead) — recommended now:**
- **Public readability of the owner's financial data.** The 2026-10-15 accept-risk reasons that this is a "single-user app with no other users' data at risk", and focuses on write scope. It does not explicitly weigh that the owner's *own* real positions, cash, P&L and journal are readable by anyone who loads a publicly discoverable URL (public repo, no `noindex`). That follows from the documented design (no front-end sign-in, full-scope key in the bundle); **I did not demonstrate it** against production. Recommend the Lead re-review the accepted risk with this framing, and choose between keeping it, adding access control in front of the static site, or narrowing the key (the accept-risk's option (a)). → `BLG-SEC-46`
- The public source map (§10, `BLG-OPS-221`) adds to the same exposure.

**Legal — only if circumstances change:** none of the following is needed while the owner is the only user, but each needs legal review before the app is shared, opened to another user or used commercially: a storage/cookie consent assessment (UK PECR); a privacy notice and processor disclosures (UK GDPR: Anthropic, Supabase, Render, Telegram, market-data providers); and the "Advisor" naming and AI output wording against UK FCA rules on investment advice and financial promotions. Whether purely personal use falls under the GDPR household exemption is itself a legal question; it is assumed, not confirmed, here.

### 12.3 Findings (Filed)

| Ref | Finding | Backlog item |
|-----|---------|--------------|
| T1 | Re-review the accepted open-access risk for the owner's own financial data (specialist) | `BLG-SEC-46` (P2) |
| T2 | Notification copy says email, delivery is Telegram; an unconfigured channel is recorded as delivered with no UI signal | `BLG-FE-318` |
| T3 | Disclose third-party data flows (AI provider, Telegram); reconsider "AI Trade Advisor" naming; fix "Permanently … can be re-added later" | `BLG-UX-18` |
| T4 | Legacy placeholder data written to `localStorage` on every load | `BLG-FE-319` |

**Trust verdict:** no dark patterns, and decision-level trust signals are strong. The main concern is posture rather than pattern: an unauthenticated front end on a public URL, over a full-scope key, holding real personal financial data. It is already a recorded, accepted risk, but it deserves a specialist re-review with the owner's own privacy in view. The email/Telegram mismatch is the one place the UI tells the user something untrue.

---

## 13. Competitors and Best-in-Class Experiences (added 2026-11-17, user request)

**Method:** web research on 2026-11-17 (vendor help centres and documentation where found, otherwise third-party reviews, several of them affiliate or competitor-run, so feature claims are indicative). Each example is compared against this app's code on `main`. The aim is the **principle**, not the feature: the app is a single-user tool for one fixed, deterministic strategy (`strategy_rules.md` §13), and several competitor strengths conflict with that on purpose.

### 13.1 Trading and Investing Products

| Example | What they do better | Principle to learn | Applicable here? |
|---------|--------------------|--------------------|------------------|
| **TradeZella — Playbook/Strategies** | Each strategy holds its rules; every trade is checked against them; the journal filters by **rules followed vs rules broken**, which separates execution mistakes from a weak setup | Rule adherence should be a first-class, filterable property of every trade, not only a score | **Yes, and better than theirs:** TradeZella relies on the trader ticking rules by hand, but this app's rules are canonical and mostly computable (pre-entry checks, §8 exit reasons, red flags). Today Trade History cannot filter by adherence (only by ticker, tags, dates). → `BLG-FE-320` |
| **Edgewonk — Tiltmeter** | One glanceable gauge of how often rules are followed, coloured green to red over time | Show discipline as a trend, not only a current value | **Partly.** The compliance score exists (Performance → Compliance, Weekly Digest current vs 7 days ago). The lesson is the trend line. Edgewonk's input is self-rating; this app's deterministic score is stronger, so do not add self-rating |
| **TraderSync — broker import, replay, AI debrief** | Very wide broker import makes journaling near-effortless; replay and AI debrief on top | Journals succeed on **low-friction capture**, not on analysis features | **Mostly not.** This app already has Replay and an AI debrief (the debrief was never used, §11). The real lesson is friction: manual entry is the cost here. A broker import is a product decision outside this review (a broker connection may also meet `credential_policy.md` §1.1's live-broker review trigger) |
| **TradingView — long/short position tool** | Drag the stop or target on the chart and see R:R, quantity and P&L update instantly | Direct manipulation with **immediate consequence feedback** | **The principle, not the chart.** Trade Plan shows the suggested size only after both entry and stop are set (What-If preview). Show the £ risk and R as the stop is typed. A draggable chart is not warranted for a rules-set stop (5× ATR, system-set on Trade Entry) |
| **Sharesight — performance report** | Splits return into capital gain, dividends and **currency movement**; tax-ready exports for an accountant | Separate *what the trade did* from *what the exchange rate did* | **Yes, for US trades.** GBP P&L on a US position mixes price and FX moves; nothing in the app separates them (no FX-effect field in front end or back end). It matters for judging whether the strategy worked. → `BLG-FEAT-102` |
| **Koyfin — customisable dashboards** | Users build their own dashboards and screens from 500+ metrics | Power-user customisation | **No — deliberately.** One fixed strategy; a rules-ordered "Due today" list is the point. Customisation would let the home page drift from what the strategy says matters (§4) |
| **Freetrade / Trading 212 — order review** | One final screen with amount, FX, latest price and shares before confirming; users ask for a price-lock step | Show the full consequence in one place at the commit point | **Already met.** Trade Entry shows an estimated total cost with fees and FX; the Exit dialog previews realised P&L before "Confirm Exit". Price-lock is not applicable: the app records trades, it does not place orders |

### 13.2 Outside the Industry

| Example | What they do better | Principle to learn | Applicable here? |
|---------|--------------------|--------------------|------------------|
| **Aviation checklists** (Boorman's Do-Confirm / Read-Do, via Gawande's *The Checklist Manifesto*) | A checklist sits at a defined **pause point**, holds only the **5–9 items most dangerous to miss**, and each item needs a specific response; machines check what machines can | Ask the human to confirm only what the human must judge; let the system verify the rest | **Yes — strongest lesson in this section.** The Trade Plan "Pre-Entry Checklist" asks the trader to tick "Position size within heat limits" and "Stop level defined" (`EntryChecklist.js`), which the system already knows (the §4.2 pre-entry checks and the stop field). Manual ticks of machine-known facts teach the user to tick without reading. Show those as automatic pass/fail, and keep ticks for judgement items (signal confirmed on the chart, research reviewed). The pause point already exists: the acknowledgement before "Create Position". → `BLG-UX-19` |
| **NHS NEWS2** (early warning score) | Each vital sign scores separately; any single red parameter escalates even if the total is low; **the trend between observations matters**; responses are tiered | A single critical signal must never be hidden by an average; show direction of travel | **Partly.** Positions already puts a single critical signal first (stop reached, exit fired). What is missing is direction: the table shows where a position is, not whether it is getting worse (for example "closer to stop than yesterday"). A composite risk score is **not** recommended — it would hide which rule fired. → `BLG-UX-20` |
| **Things 3 — Today view** | Today holds only what will really be done; quiet when empty; colour is reserved for meaning (about 95% neutral) | Calm by default; colour signals meaning only | **Yes, already partly adopted.** "Due today" follows this. The quiet-day Dashboard (11 empty boxes, `BLG-UX-11`) does not; and decorative gradients (cyan→violet primary buttons) spend colour without meaning, while red/amber/green carry rules. Fold into `BLG-UX-11` and the token work, no new item |
| **Linear — triage and keyboard-first** | An explicit triage inbox; declining asks for a reason; every action has a shortcut; optimistic UI | Dismissal with a reason turns noise into a record; speed builds trust | **Partly.** Shortcuts and a command palette exist. The lesson is the reason: dismissing the drawdown review prompt or an alert records nothing about why. Capturing a one-line reason would feed the Journal's red flags — a product decision; noted, not filed |
| **GOV.UK Design System — error messages** | An error summary at the top linking to each field, plus an inline message saying what went wrong **and how to fix it**; no "invalid", no "please" | One error standard across the product | **Yes.** Trade Entry nearly does this; other forms rely on disabled buttons or toasts (§9, `BLG-UX-06`). Adopt the pattern as the app's written standard. → `BLG-SPEC-240` |
| **Garmin — Training Readiness** | A 0–100 daily score with its **named contributing factors** and a short message | Any score must show its reasons | **The principle only.** A daily "readiness to trade" score would be adaptive guidance outside §13. But the principle applies to existing scores: Trade Plan shows "Setup Quality Score: Low" with no reason on the collapsed panel (§8, `BLG-FE-310`) |
| **Monzo — Trends** | Monthly and yearly views with targets; users asked for periods aligned to their pay cycle, not calendar months | Report periods should match the user's real cycle | **Already met in the main case:** Performance has UK tax-year reports. Keep it in mind for any new period views |

### 13.3 What Not to Copy

- **Customisable dashboards, AI coaches and composite readiness scores** are strengths for discretionary traders with many strategies. For one fixed, rules-based strategy, they would loosen the very structure the app exists to enforce (§13.2).
- **Breadth of analysis** is not the gap: the app already has more analysis than is used (Replay, debrief, narratives — §11). The gaps are adherence visibility, low-friction capture and calm defaults.

### 13.4 Findings (Filed)

| Ref | Lesson | Backlog item |
|-----|--------|--------------|
| B1 | Aviation: system-verifiable checklist items become automatic status | `BLG-UX-19` |
| B2 | TradeZella: filter trades by rules followed vs broken | `BLG-FE-320` |
| B3 | Sharesight: separate price and FX effects in US trade P&L | `BLG-FEAT-102` |
| B4 | NEWS2: show direction of travel on Positions | `BLG-UX-20` |
| B5 | GOV.UK: one written error-message standard | `BLG-SPEC-240` |

**Sources:** [TradeZella — getting started with the Playbook](https://help.tradezella.com/en/articles/7020769-getting-started-with-the-playbook); [TradeZella — groups and rules in the Playbook](https://intercom.help/tradezella-4066d388d93c/en/articles/6986848-what-is-groups-and-rules-in-the-playbook); [Edgewonk — The Tiltmeter](https://edgewonk.zendesk.com/hc/en-us/articles/360010150259); [Edgewonk — Tiltmeter blog](https://edgewonk.com/blog/mastering-trading-discipline-with-edgewonks-tiltmeter); [TraderSync vs Tradervue (Curved Trading)](https://curvedtrading.com/articles/en/reviews/tradersync-vs-tradervue/); [Edgewonk vs TraderSync (TradingTools.review)](https://tradingtools-directory.pages.dev/compare/edgewonk-vs-tradersync/); [TradingView — long and short position tools](https://in.tradingview.com/support/solutions/43000475660-how-to-use-long-and-short-position-drawing-tools/); [Sharesight — portfolio tracker](https://sharesight.com/portfolio-tracker); [Sharesight — tax time](https://sharesight.com/blog/3-ways-sharesight-helps-investors-at-tax-time); [Koyfin review (Bullish Bears)](https://bullishbears.com/koyfin-review/); [Freetrade — new order experience](https://community.freetrade.io/t/new-improved-order-experience/23191); [Freetrade — order confirmation screen request](https://community.freetrade.io/t/feature-request-order-confirmation-screen/17151); [Trading 212 — redesigned CFD order screen](https://community.trading212.com/t/cfds-have-a-new-look-a-redesigned-order-screen-cleaner-interface-and-more/88700); [Shortform — Boeing checklist (Gawande summary)](https://www.shortform.com/blog/boeing-checklist/); [RCP — NEWS2 executive summary](https://www.rcp.ac.uk/media/ctulqqbn/news2-executive-summary_0.pdf); [NHS Scotland — NEWS2 guideline](https://rightdecisions.scot.nhs.uk/media/vhcccgq2/news2-guideline-no-fp.pdf); [MacStories — Things 3 review](https://www.macstories.net/reviews/things-3-beauty-and-delight-in-a-task-manager/); [Cultured Code — Things features](https://culturedcode.com/things/features/); [Linear — triage release](https://linear.app/changelog/2021-06-29-linear-release-and-issue-triage); [GOV.UK — error message](https://design-system.service.gov.uk/components/error-message); [GOV.UK — error summary](https://design-system.service.gov.uk/components/error-summary); [GOV.UK — validation pattern](https://design-system.service.gov.uk/patterns/validation); [Garmin — Training Readiness manual](https://www8.garmin.com/manuals/webhelp/GUID-CF6857C0-CEF9-485F-B3B4-B8DC192FA66A/EN-US/GUID-C21BE0C8-A08E-4DA1-B6C6-2E0E2DDDB372.html); [Monzo — Trends spending and balance](https://monzo.com/help/budgeting-overdrafts-savings/trends-spending-and-balance-web).

---

## 14. Target State: What the App Should Become (added 2026-11-17, user request)

This section turns §1–§13 into one target. It is a **recommendation for Product Owner ratification**, not a committed plan: each part names the backlog items that would deliver it, and anything new is marked *new*. Terms written for a public marketing site are mapped to their in-app equivalents: the "homepage" is the Dashboard, the "hero" is the Due today list, and "proof" means evidence that the system's numbers and rules can be trusted.

### 14.1 Positioning

**What the app is:** *a disciplined co-pilot for one momentum strategy.* It tells the trader what the rules say to do today, makes doing it quick and checked, and shows honestly whether the rules were followed and whether they work.

**What it must communicate immediately, on any page:**

1. **What needs doing now, in rule order:** regime, then exits, then stops, then entries.
2. **That the numbers can be trusted:** where each figure came from and how fresh it is.
3. **That the human decides:** the system computes and checks; it never advises or acts (`strategy_rules.md` §13).

**What it should not communicate:** a terminal, a dashboard builder or an AI adviser. It should feel closer to a pilot's checklist and instrument panel than to a trading terminal.

**Name:** one product name everywhere (`BLG-UX-16`). This is a Product Owner decision. Recommendation: drop "Position Manager", which describes one page, not the job. Pick a name built on the strategy and the decision support, and avoid "Advisor" (§12).

### 14.2 Information Architecture

Keep the five job-based areas (they work, §3). Make three changes: the weekly review becomes the front door of Review, Strategy Benchmark joins Performance, and reference/configuration pages move to Settings.

```
Today
├── Dashboard ("Today")                     home: Due today, then status
└── Notifications                           → Notification History (detail)

Portfolio
├── Positions                               decision-first table/cards; grace view; Daily Monitor
│   └── Exit (dialog), Position notes (→ Journal)
├── Risk Dashboard
└── Record a trade (Trade Entry)            action; also from Positions and Trade Plans

Find trades
├── Signals                                 "Plan this"
├── Screener                                "Plan this"
├── Watchlist
├── Research                                → Research {TICKER}
└── Trade Plans                             → Trade Plan (detail, section index)

Review
├── Weekly review   (was Weekly Digest)     the review journey's start; links onward (BLG-UX-12/15)
├── Performance                             Summary · Reports · Analytics · Compliance · Strategy vs backtest*
├── Trade History                           filters incl. rules followed/broken (BLG-FE-320)
├── Journal                                 Reflections · Red flags · Position notes
└── Replay

Settings
├── Settings                                fees, risk limits, preferences; strategy parameters (read-only)
├── Notification Preferences                (Telegram, BLG-FE-318)
├── Ticker Universe*                        configuration, moved from Find trades
├── System Status
└── How this works*                         purpose, daily routine, core terms, where data goes (BLG-UX-16/18)
```

\* *New or moved.* "Strategy vs backtest" absorbs Strategy Benchmark as a Performance section (one place per review concept, §5). Ticker Universe configures the screener's universe and is not a daily find-trades task. Sidebar entries: 19 → 18, still 5 areas, with Today and Portfolio expanded by default. *New* placement decisions (Strategy Benchmark merge, Ticker Universe move) need a `navigation.md` revision → `BLG-UX-21`.

### 14.3 The Dashboard, Top to Bottom

| # | Section | Contents | Purpose | Delivered by |
|---|---------|----------|---------|--------------|
| 1 | **Header / navigation** | Sidebar (5 areas); page title "Today" with the date; a compact status line: data as of {time}, market data source status | Orient: where am I, how fresh is what I see (trust signal 2) | Existing; title and subtitle copy `BLG-FE-310` |
| 2 | **Hero: Due today** | Regime per market first, then exits due, grace ending, stops moved, new signals (with "Plan this"); each item one click from its action. Quiet day: one line, "Nothing due today · US RISK-ON · UK RISK-ON" | The primary proposition: *what the rules say to do now, in rule order* | Existing; "Plan this" `BLG-UX-13` |
| 3 | **Positions needing attention** | Only when any exist: the top rows of Positions' urgency order, with direction of travel (closer to or further from stop) | Bring in-trade decisions forward without opening Positions | `BLG-UX-20` (direction); otherwise reuses Positions |
| 4 | **Portfolio status strip** | One row: open positions, portfolio heat, in grace (one definition), cash | Context for today's decisions, at a glance, not as cards | Collapses Cards 1–3; `BLG-FE-308`, `BLG-UX-11` |
| 5 | **Review prompts** | Shown only when due: weekly review ready, reflections outstanding, red flags this week | Link today's work to the review loop | *new* (part of `BLG-UX-11`'s quiet-day redesign) |
| 6 | **Briefing (optional)** | The Morning Briefing cards with data, and the AI briefing collapsed by default; zero-state cards fold into one "All clear" line | Supporting context for those who want it, without 11 empty boxes | `BLG-UX-11`; the AI briefing's future depends on the 2027-01-03 usage review (`BLG-GOV-382`) |
| 7 | **Proof / trust** | Rule-adherence trend (rules followed, last 4 weeks); every figure links to how it was computed | Shows the system is honest about discipline and arithmetic | Trend from existing compliance data; links `BLG-UX-14`/`BLG-UX-16` |
| 8 | **Calls to action** | Inline on each item (Exit, Review stop, Plan this, Open review); no global marketing-style CTA. The one persistent action is "Record a trade" | Actions live where the decision is made | Existing pattern |
| 9 | **Supporting content** | What's New (collapsed, one line when there is nothing new); trade-count progress strip | Low-priority information, below the work | Existing, demoted |
| 10 | **Footer** | Version (real), data as-of, "How this works", "Where your data goes"; the Docs link fixed or removed | Help, transparency and version identity in one predictable place (WCAG 3.2.6 consistent help) | `BLG-FE-309`, `BLG-UX-16`, `BLG-UX-18` |

### 14.4 Key Page Templates

| Template | Pages | Structure (top to bottom) |
|----------|-------|---------------------------|
| **Triage list** | Positions, Signals, Screener, Trade Plans, Trade History, Notifications | Page header (title, one-line purpose, primary action) → one warning strip (only if any) → filters, saved views, rule-adherence filter where relevant → list sorted by urgency (the rule that orders it stated in a caption) → rows with leading decision columns, details on expand, and cards below `md` → empty state with one next step |
| **Commit form** | Trade Entry, Exit dialog, Cash, Trade Plan save | Header with the parent link → pre-filled fields (with source shown) → system-verified checks as status (not ticks) → human-judgement confirmations (the pause point) → consequence preview (cost, risk £/R, P&L) → one primary button; errors per the written standard (summary plus inline, `BLG-SPEC-240`) |
| **Record / detail** | Trade Plan, Research {TICKER}, Notification History | Parent link → identity line (ticker, market, status) → section index ("On this page") for long pages → sections in decision order → onward link to the next step |
| **Review report** | Weekly review, Performance, Journal | Period selector (UK tax year, week, month) → headline figures in plain words with links to their records → sections (Summary, Reports, Analytics, Compliance, Strategy vs backtest) → drill-down to Trade History filtered → export |
| **Reference / settings** | Settings, Notification Preferences, Ticker Universe, System Status, How this works | Grouped sections → read-only strategy parameters clearly marked → editable preferences save in place → plain-language help per setting (no "§" references, `BLG-UX-14`) |

### 14.5 Design Direction

| Aspect | Direction | Why (evidence) |
|--------|-----------|----------------|
| **Visual character** | Calm instrument panel: neutral surfaces, high information density where decisions are made, quiet everywhere else | §1–§4 quiet-day finding; Things 3 and aviation lessons (§13) |
| **Typography** | Keep the system font stack (fast, no web fonts, §10). One heading scale, used semantically (`BLG-FE-313`). **Tabular (fixed-width) numerals for every figure** — today only 13 places use `tabular-nums` — so prices, P&L and R line up in tables | Readability of numbers; accessibility headings |
| **Spacing** | The existing Tailwind 4 px grid; tight spacing inside tables and lists, generous spacing between page sections; spacing reflects importance, not decoration | Density only where it earns its place |
| **Colour** | **Colour means something or is absent.** Semantic tokens only (`app-*`, v9.16–v9.17): positive, negative and warning carry rule states; regime badges keep text labels. Retire the 26 decorative cyan-to-violet gradient buttons for one solid primary colour. Both themes pass contrast (AA; focus appearance at AAA, §9.4) | §9, §13 (Things 3); `BLG-FE-288`, `BLG-FE-314` |
| **Imagery** | No photography or illustration. Charts only where a trend matters (Performance, Risk, Strategy vs backtest), each with a text summary as its alternative. Icons always paired with text (lucide, decorative icons hidden from screen readers) | §10 (no image weight); §9 (chart alternatives) |
| **UI components** | One component per job: one toast system, one dialog (with semantics), one table/card pattern, one status pill set, one error pattern; built on the shared `components/ui` primitives with focus rings; no bespoke clickable `div`s | §9 (keyboard failures), §10 (duplicate libraries); `BLG-FE-311`, `BLG-FE-315` |
| **Interaction** | Keyboard-first and direct: shortcuts and the command palette remain; pre-fill everything the system knows; show consequences as values change (risk £/R while typing the stop); confirm only irreversible actions; ask for a one-line reason only where it feeds the journal | §13 (TradingView, Linear, aviation) |
| **Motion** | Almost none. No entrance fades on headings (`BLG-FE-317`); short state transitions only (expand, open dialog); respect reduced motion everywhere (`BLG-FE-314`); never animate numbers that matter | §10 (LCP), §9 (motion) |

### 14.6 Functionality

| Retain | Remove | Redesign | Introduce |
|--------|--------|----------|-----------|
| Due today list, regime first | Legacy placeholder data in browser storage (`BLG-FE-319`) | Dashboard below the hero: quiet day as one line, status as a strip (`BLG-UX-11`, `BLG-FE-308`) | Rules followed/broken filter (`BLG-FE-320`) |
| Pre-entry checks on every route, with acknowledgement | The dead Docs link, unless help ships (`BLG-FE-309`) | Weekly Digest → Weekly review, readable and linked (`BLG-UX-15`, `BLG-UX-12`) | Direction of travel on Positions (`BLG-UX-20`) |
| Decision-first Positions with cards; one grace view; one warning strip | Duplicate libraries (`moment`, second toast system) and the public source map (`BLG-FE-315`, `BLG-OPS-221`) | Trade Plan checklist: machine-known items as automatic status (`BLG-UX-19`) | Price vs FX effect on US trades (`BLG-FEAT-102`) |
| "Plan this" and pre-filled plans; suggested size | Decorative gradients (fold into the colour work) | Notifications: say Telegram and show when an alert was not sent (`BLG-FE-318`) | "How this works" and "Where your data goes" (`BLG-UX-16`, `BLG-UX-18`) |
| Stop provenance, fee and P&L previews, data-freshness indicators | AI features still unused after the 2027-01-03 review (decision via `BLG-GOV-382`) | Rule references ("§7.2") → plain language (`BLG-UX-14`) | Web Vitals measurement and a modern performance budget (`BLG-QA-271`) |
| One Journal, one Performance page, section indexes | | Error handling to one standard (`BLG-SPEC-240`) | Chat opened from a trade, if chat is kept (`BLG-UX-17`) |
| Semantic colour tokens; CI accessibility scan | | Access to the site: re-review the accepted open-access risk (`BLG-SEC-46`) | Wider accessibility scan and one manual pass (`BLG-QA-269`, `BLG-QA-270`) |
| Replay; CSV and PDF exports | | Bundle split by page; Dashboard fetches each dataset once (`BLG-FE-315`, `BLG-FE-316`) | |

### 14.7 Suggested Sequence

1. **Correct and safe first:** the security re-review (`BLG-SEC-46`, P2), the Level A accessibility failures (`BLG-FE-311`, `BLG-FE-312`, P2), the Telegram/email truth fix (`BLG-FE-318`), and measurement before changes (`BLG-QA-271`).
2. **Home and review loop:** `BLG-UX-11`, `BLG-FE-308`, `BLG-UX-12`/`15`, `BLG-UX-19`, `BLG-FE-320`, `BLG-UX-21` (IA changes).
3. **Clarity:** `BLG-UX-14`, `BLG-UX-16`, `BLG-UX-18`, `BLG-FE-310`, `BLG-SPEC-240`, `BLG-FE-313`, `BLG-FE-314`.
4. **Speed and polish:** `BLG-FE-315`, `BLG-FE-316`, `BLG-FE-317`, `BLG-OPS-221`, `BLG-FEAT-102`, `BLG-UX-20`.

This is advice for the next `run roadmap`, which owns sequencing. Ratifying the target state as the brief for a "Site Structure & Usability, Phase 4" programme is the Product Owner's decision → `BLG-UX-21`.

---

## 15. Gap Analysis: Current State vs Recommended Future State (added 2026-11-17, user request)

Direct assessment. **Size** is the gap, not the effort: *Small* = polish, *Medium* = a visible change to how part of the app works, *Large* = a change to what the app is or how it is reached. "Current" is `main` at `80e8bca4` and the findings in §1–§13.

| Area | Current state | Recommended future state | The gap, stated plainly | Size |
|------|---------------|--------------------------|-------------------------|------|
| **Brand** | Three product names ("Position Manager", "Swing Trading Position Manager", "Momentum Trading Assistant"); no statement of purpose anywhere in the app; the AI is branded "AI Trade Advisor"; decorative cyan-to-violet gradients on 26 buttons | One name; the purpose stated in the app ("a disciplined co-pilot for one momentum strategy"); no "Advisor"; colour used only for meaning | **There is no brand.** There is a page label used as a product name. The product does not say what it is or what it is for. Fixing this needs a Product Owner decision before any design work | Medium |
| **UX** | Structure fixed by v9.15–v9.17: job-based navigation, Due today, decision-first Positions, one Journal, one Performance page. But the quiet-day Dashboard is still 11 empty boxes, the weekly review is 3 sidebar hops, the Trade Plan checklist asks for ticks on facts the system knows, and nothing shows direction of travel | Calm home with one quiet line; a weekly review that is one journey; checks the system can verify shown as status; trends visible | **The daily loop is good. The weekly loop and the quiet day are not.** The programme fixed *finding things*; it did not finish *reviewing things*. This is the largest remaining UX gap and it touches the most-used page | Medium |
| **UI** | Semantic colour tokens on every page (v9.17), but 26 decorative gradient buttons, one fixed-width numeral treatment in only 13 places, two toast systems, custom clickable `div`s, entrance fades on every heading | One component per job; one solid primary colour; fixed-width numerals for all figures; no decorative motion | **Consistent in colour, inconsistent in components and emphasis.** Visually it still says "dashboard template", not "instrument" | Medium |
| **Content** | 84 "§x.y" rule references in user copy; raw values (`risk_on`), internal IDs ("SI-02 Gate Status"), API-style Weekly Digest; Settings description contradicts the page; notification copy says "email" when delivery is Telegram; no help; dead Docs link. Strong at the point of action (stops, fees, FX) | Plain language everywhere; a "How this works" page; truthful channel copy; one error standard | **The app explains each number well and explains itself not at all.** One statement on screen (email) is false. Content needs a full pass, not spot fixes | Large |
| **Information architecture** | 5 job-based areas, 19 entries, 0 dead ends, 0 undiscoverable pages | 5 areas, 18 entries: Weekly review leads Review; Strategy Benchmark inside Performance; Ticker Universe in Settings; a help page | **Small.** The IA is the most finished part of the app. What is left is two moves and one new page | Small |
| **Functionality** | Strong core (pre-entry checks on every route, Plan this, stop provenance, one grace view, Replay, exports). Missing: rule-adherence filtering, price vs FX P&L split, direction of travel, delivery status for alerts. Carrying: 3 AI features never used, legacy placeholder storage | Retain the core; introduce adherence filtering, FX split, trend cues, delivery status; remove what is unused | **The app has more features than it uses and lacks the two that would make review honest** (adherence and FX). The gap is depth in review, not breadth | Medium |
| **Mobile** | Positions has cards below `md`; Performance checked at 375/390 px; the full 552 KB bundle and ~16 Dashboard requests load on a phone; the Telegram digest sends the user into the app on mobile; no measured mobile performance; reflow at 320 px untested | Fast first load on a phone (code-split, deduplicated requests), every page reflows at 320 px, measured on a mobile profile | **Layouts are partly mobile-ready; delivery is not.** The heaviest path (Telegram link → Dashboard on a phone) is the least tested | Medium |
| **Accessibility** | Text contrast and landmarks pass in CI. Observed Level A failures: 4 mouse-only controls; unlabelled fields on the Exit dialog — the most safety-critical form; Dashboard has no section headings; weak focus rings; no reduced-motion support; the scan never opens dialogs | WCAG 2.2 AA met and tested (automated plus one manual pass), with AAA focus appearance and reduced motion | **The app does not meet WCAG 2.2 AA today**, and its automated scan would not tell you. The failures are on core journeys. Two are P2 | Medium (fixes small, the testing gap large) |
| **Performance** | One 542 KB gzipped bundle, 2.7× its own 200 KB budget; no code splitting; `GET /positions` fetched 4 times on Dashboard load; no caching between pages; headings start invisible; **no Core Web Vitals have ever been measured**; the budget is outdated (no INP/CLS, desktop only, baseline "TBD" since v2.6) | Measured CWV on mobile and desktop within a modern budget; code-split; each dataset fetched once | **Over budget and unmeasured.** The team cannot currently say whether the app is fast, and its own budget says it is too heavy | Medium |
| **SEO** | Public repository, URL published, no `robots.txt` or `noindex`; a single-page app with no meaningful content for crawlers | **Not indexed** — the right goal for a private financial tool. No SEO investment | **The gap runs the other way: the app is findable when it should not be.** This is a security and privacy item (`BLG-SEC-46`), not a marketing one | Small (to fix), but tied to a Large decision |
| **Conversion** (in-app: do the intended actions happen?) | No funnel data at all. The only evidence is AI usage: 31 calls in 102 days, 3 of 6 features never used. Unknown: how often signals become plans, plans become entries, closed trades get reflections, weekly reviews are opened | The intended loop (Due today → act → record → reflect → weekly review) instrumented, with each step's completion visible, and features that are not used retired | **Nobody knows whether the app's core loop is used.** Every product decision since v6.2 has been made without behavioural data, and the one place data exists says adoption is very low | Large |
| **Technology** | Create React App (`react-scripts` 5, deprecated by the React team in February 2025), client-side SPA on GitHub Pages; Render backend with cold-start risk; no front-end auth; a full-scope API key in the public bundle (accepted risk); public 9.1 MB source map; duplicate libraries | The same architecture, made lean (code-split, one library per job), not publicly exposed, measured. Hosting change only if measurement or the access decision requires it | **Sound shape, exposed and heavy.** The serious gap is access, not framework. A build-tool migration off CRA is advisable in time but not urgent; it is not filed | Medium; Large if the access decision requires authentication |
| **AI capability** | 7 AI features shipped, all advisory and §13-governed; usage very low; the chat appears only on two pages | Fewer, better-placed AI features: unused ones retired at the 2027-01-03 review; chat reachable from a trade if kept; no new AI capability | **Over-built relative to use.** The gap is not missing AI — it is AI nobody uses. The future state has *less* AI, and that is the recommendation | Medium (mostly decisions) |

### 15.1 Scale of Change — Stated Plainly

- **Filed work:** the 31 items from this review estimate at **17–33 days** (7 XS, 16 S, 8 M). One release's capacity ceiling is 28 days. **The filed work alone is roughly one full release, and possibly more.**
- **Not yet estimated, and likely larger than any single filed item:**
  - whatever remedy `BLG-SEC-46` chooses (adding authentication or access control would be a Large change to how the app is reached);
  - the design-direction rollout (one primary colour, typography numerals, component consolidation) beyond the filed items;
  - the shared-component colour sweep already open (`BLG-FE-288`);
  - instrumenting the core loop for conversion data (not filed: it needs a Product Owner decision on what to measure);
  - a build-tool migration off CRA (not filed).
- **Realistic total:** **two releases of focused work, three if the access decision requires authentication.** The programme just finished (Phases 1–3) took three releases. This is a second programme of similar size, not a tidy-up.
- **The hardest gaps are decisions, not code:**
  1. the access/security posture (`BLG-SEC-46`);
  2. the product name and purpose statement (`BLG-UX-16`);
  3. which AI features to retire (`BLG-GOV-382`);
  4. whether to adopt this target state (`BLG-UX-21`);
  5. whether to measure the core loop at all.

  Until those are made, roughly a third of the filed items cannot be finished well.

### 15.2 Overall Verdict

The 2026-11-03 verdict — *modify substantially, don't redesign* — still holds for structure. For the product as a whole, the honest position is stronger: **the app is well organised but unexplained, unmeasured, over-featured where it matters least, and exposed.** It is closer to the target in information architecture than in anything else, and furthest from it in content, conversion evidence and access. Reaching the target is a second programme, not a set of fixes.
