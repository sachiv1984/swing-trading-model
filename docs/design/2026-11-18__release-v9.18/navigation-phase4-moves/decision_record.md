**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-18__release-v9.18
**Stories:** ST-07 (BLG-UX-21), ST-08 (BLG-FE-323); onward-link rows for ST-16 (BLG-UX-12) — EPIC-02, EPIC-03

# Decision Record — Phase 4 Navigation Moves

## 1. Scope of this record

DL-089 adopted the re-review's §14 target state in whole (roadmap rebalance `2026-11-18__scheduled`). ST-07 records it in `navigation.md` (the two §14.2 moves) and `design_system.md` (§14.5 design direction). ST-08 builds the two moves.

**Split of work between this gate and ST-07:** ST-08 is Design Required and may not pass this gate without its spec, so this gate writes the `navigation.md` half now (`navigation.md` v2.4 → v2.5, approved below). ST-07 keeps the `design_system.md` half (outside this gate's write scope) and dates the Head of UX & Design approval of both files in its own commit. Recorded in the addendum.

Spec impact: `navigation.md` v2.4 → v2.5; `performance.md` v1.2 → v1.3 (§3 index, §4 new section, §7 redirect); `strategy_benchmark.md` v0.11 → v0.12 (becomes a section; §2 header, §3a index retired); `ticker_universe.md` v1.2 → v1.3 (route, parent link); `settings.md` v1.10 → v1.11 (onward link).

## 2. Strategy Benchmark becomes "Strategy vs backtest" on Performance

- **Section:** a fifth Performance section, id `strategy-vs-backtest`, `<h2>` "Strategy vs backtest", after Compliance. The section index lists five entries.
- **Content:** the whole Strategy Benchmark page body moves in unchanged: the filter bar, the Benchmark / Version Comparison / Backtest Rule Change tabs and their panels.
- **Inside a section, three things change:**
  - The filter bar is **not sticky** (a sticky bar inside one section of a long page would cover the other sections' headings). It sits at the top of the section.
  - The Benchmark tab's own section index (`strategy_benchmark.md` §3a, v9.17) is **retired**: two section indexes on one page would compete. Its panels become `<h3>` headings ("Open positions", "Performance parity", "Yearly breakdown", "Trade log") under the section's `<h2>`. The page-level index stays the only index.
  - The page header (title, description, actions) is dropped; its description becomes the section's one-line intro under the `<h2>`, and its actions (if any) move to the section's tab row.
- **Loading:** the section fetches its data when the page loads, like the other four. ST-06 records the Performance page's Core Web Vitals baseline before ST-08 merges if the order allows; if not, the baseline notes that it includes this section.
- **Redirect:** `/StrategyBenchmark` → `/Performance?section=strategy-vs-backtest` (replace navigation; other query parameters kept), as `performance.md` §7 does for `/Reports`.
- **Links:** Replay's comment-only mention needs no change. The Strategy Benchmark → Performance onward link is removed (it is now on the page). Command palette entry "Strategy vs backtest" → the redirect target. `pageLabels.js`: the `StrategyBenchmark` label leaves the sidebar list; a section label "Strategy vs backtest" is added for the palette.

## 3. Ticker Universe moves under Settings

- **Route:** `/settings/ticker-universe` (canonical), a detail page of Settings, no sidebar entry. `/TickerUniverse` redirects there (replace navigation, query kept).
- **Parent link:** "Settings" → `/Settings` (`navigation.md` §Parent Links). Active item: Settings; active area: Settings.
- **Entry point:** `PageHeader` takes one onward link, and Settings' is Notification Preferences. So Settings §3 Preferences gains a last row, label "Screener universe", body "The tickers the screener scans each night.", and a link "Ticker Universe" (shared `OnwardLink` style) → `/settings/ticker-universe`, `data-testid="settings-ticker-universe-link"`. The page's own onward link to Screener is unchanged.
- **Command palette:** "Ticker Universe" → `/settings/ticker-universe`.
- **No content change** to the page itself.

## 4. Counts

Sidebar entries 19 → 17 (Strategy Benchmark and Ticker Universe removed). Detail pages without a sidebar entry 3 → 4 (Ticker Universe added). Removed page routes with a redirect: 5 → 6 (Strategy Benchmark; its file may remain as the section's component). Five areas unchanged; Find trades has 5 entries, Review 5, Settings 2.

## 5. Onward links for the Weekly Digest (ST-16)

`navigation.md` §Onward Links, Weekly Digest row: "Performance Summary (realised P&L); Performance Compliance (journal completion); Journal Red flags (red flags, last 7 days); Notifications (alert counts)". Detail in `weekly-review` record §3 and §5.

## 6. Approvals

- Head of UX & Design: approved (agent-mediated, Design Gate Engine), 2026-11-18. ST-07 records the dated approval of `design_system.md` §14.5 in its own commit.
- Product Owner: approved (the user, in session, 2026-11-18). DL-089 adopted §14 in whole.
