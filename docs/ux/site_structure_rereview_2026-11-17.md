**Owner:** Head of UX & Design
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-11-17 (§9 Accessibility Review added at the user's request; 6 accessibility items filed); prior — 2026-11-17 (§8 Content Review added at the user's request; 5 content findings filed); prior — 2026-11-17 (created — `BLG-UX-08`)

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
