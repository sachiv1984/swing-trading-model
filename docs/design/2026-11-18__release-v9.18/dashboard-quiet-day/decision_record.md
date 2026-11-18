**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-18__release-v9.18
**Stories:** ST-09 (BLG-UX-11), ST-10 (BLG-FE-308), ST-11 (BLG-UX-13) — EPIC-02

# Decision Record — Quiet-Day Dashboard, One Grace Definition, "Plan this" on the Today List

## 1. Scope of this record

Three Dashboard stories that edit the same page and the same spec (`dashboard.md`), built in order ST-09 → ST-10 → ST-11 (slice sequencing). Design direction: re-review `docs/ux/site_structure_rereview_2026-11-17.md` §14.3 rows 4 and 6, adopted by DL-089.

Spec impact: `dashboard.md` v4.3 → v4.4 (§1B New signals row, new §3A Quiet-Day Collapse, §1A Cards table, §4 Card 1 and Card 3, new §4B One Grace Definition).

## 2. Quiet day: zero-state elements fold into one line (ST-09)

### 2.1 Which elements fold

An element **folds** when, after its data has loaded, it would render its own empty branch. The test is mechanical: the `empty` prop the element already passes to `DashboardCard` / `DataState`. Nothing new decides emptiness.

| Element | Folds when (existing empty condition) | Name in the line | Line entry goes to |
|---------|---------------------------------------|------------------|--------------------|
| Screener Hits | `newHits === 0` | Screener hits | `/Screener` |
| Positions to Watch | in-grace count = 0 (after ST-10, §4) | Positions to watch | `/Positions?grace=open` |
| Red Flags | `total === 0` | Red flags | `/Journal?section=red-flags` |
| Earnings Alert | `count === 0` | Earnings | `/Positions` |
| Compliance | `score == null` | Compliance | `/Performance?section=compliance` |
| AI Daily Briefing | no briefing for today (`briefing-empty` branch) | AI briefing | Disclosure: reveals the card in place (§2.3) |
| Card 1 Open Positions | `open.length === 0` | Open positions | `/Positions` |
| Card 2 Portfolio Heat | `heat == null` | Portfolio heat | `/RiskDashboard` |
| Card 3 In Grace Today | in-grace count = 0 | In grace | `/Positions?grace=open` |
| Card 5 Recent Activity | `recent.length === 0` | Recent activity | `/TradeHistory` |
| What's New | `changes.length === 0` | What's new | Disclosure: reveals the card in place |

Not in the table, and never folded: the Today list (it has its own quiet line, §1B), Gate Progress (a progress strip, not an empty state; it already hides itself on error).

### 2.2 The line

- **Placement:** directly below the Today list ("Due today"), before anything else. One line, wrapping on narrow screens.
- **Text:** "Nothing to show: " then the names of the folded elements in the table's order, separated by " · ". Each name is a link (or, for the two disclosure entries, a button). `text-sm text-app-muted`, links `text-app-fg underline-offset-2 hover:underline`. `data-testid="dashboard-nothing-to-show"`.
- **Wording choice:** "Nothing to show", not the brief's "All clear". "All clear" reads as a judgement that the portfolio is safe, which the page must not make (§13: the system reports, it does not reassure or advise), and it is wrong for a missing compliance score. "Nothing to show" is true for every row of §2.1. It is the same heading What's New already uses for its empty state.
- **Not shown** when no element folds.
- **Containers:** when every element inside the briefing panel (five Morning Briefing cards and the AI briefing) folds, the panel itself is not rendered. When Cards 1–3 all fold, their row is not rendered. Elements with data keep their v4.0 positions and order; a folded element leaves no gap (the grid re-flows the remaining cards left to right).
- **No icon, no box, no illustration.** It is a text line, not an empty-state component, so the page has at most one empty-state element below "Due today" (the AC).

### 2.3 Disclosure entries

"AI briefing" and "What's new" have no page to link to, and the AI briefing's empty state carries the Regenerate control. Their entries are `<button aria-expanded="false">`. Activating one renders that card in its normal v4.0 position, unfolded, for the rest of the visit (not persisted), with the button showing `aria-expanded="true"`. Focus stays on the button.

### 2.4 States (worked examples)

| Situation | What renders |
|-----------|--------------|
| All 11 elements loaded and empty (quiet-day fixture) | Today list quiet line, then "Nothing to show: Screener hits · Positions to watch · Red flags · Earnings · Compliance · AI briefing · Open positions · Portfolio heat · In grace · Recent activity · What's new", then Gate Progress. No briefing panel, no card rows. |
| 1 open position (healthy, not in grace), everything else empty | Card 1 and Card 2 render in Row 1 (Card 2 heat is non-null), Card 3 folds; line lists the other 8 |
| An element is still loading | It renders its own skeleton in place. It joins the line only once loaded and empty, so the line can grow as sources resolve; it never shrinks except on Refresh |
| An element's fetch fails | It renders its own error state in place. An error is not empty, so it never folds |
| Compliance has a score of 0 | Not empty (`score == null` is the test); the card renders 0% |
| Portfolio heat 0.0% with one open position | Not empty (`heat == null` is the test); 0% is a value (§4A) |

### 2.5 Visual baselines

ST-09 regenerates `dashboard-home-light/dark-chromium.png` with the quiet-day fixture, plus one populated-fixture baseline so a card with data is pinned in its v4.0 position.

## 3. One grace definition (ST-10)

### 3.1 Data-source check

- `GET /positions` returns `grace_period` (boolean) and `grace_days_remaining` for every open position (`position_service.py` ~231 and ~265: `grace_period = holding_days < 10`; `grace_days_remaining = max(0, 10 − holding_days)` when in grace, else `null`, per `grace_service.py`). So for this endpoint `grace_period === true` ⇔ `grace_days_remaining ≥ 1`.
- **Gap found:** Card 3 (`GracePeriodCard.js`) also counts `grace_end_date` and `status === "GRACE"`, and builds "Next expires" from `grace_end_date`. No backend file writes `grace_end_date`, and no contract lists it (grep, 2026-11-18), so the sub-label always reads "No expiry date set" when anyone is in grace. `status === "GRACE"` is the stored lifecycle status, which can lag the computed flag.
- `OpenPositionsCard.js` counts `grace_days_remaining > 0 || status === "GRACE"`; `ExitZoneCard.js` counts `grace_period === true` and labels the ≤ 2-days-left subset (from `GET /positions/grace-period-alerts`) "exit zone", a name the strategy uses for something else.

### 3.2 Decision

- **One predicate:** `isInGrace(position)` from `src/lib/positionUrgency.js` (`grace_period === true`), the predicate `positions.md` §Grace Period View, the Positions warning strip and the Risk Dashboard grace panel already use. Every Dashboard grace count uses it: Positions to Watch, Card 1's "N in grace", Card 3. The Today list's Grace ends today group stays a subset: `isInGrace` and `grace_days_remaining = 1`.
- **Card 3 sub-label:** the Risk Dashboard grace panel's text (`risk_dashboard.md` §5.2, `GracePeriodPanel.js` `nextEndsText`), from the minimum `grace_days_remaining` of in-grace positions: 1 → "Ends today"; n ≥ 2 → "Next ends in {n − 1} day(s)". Move `nextEndsText` into `src/lib/positionUrgency.js` and use it in both places (ST-19's unit-test convention applies).
- **Positions to Watch:** count = in-grace positions; sub-text "{n} in grace" plus, when any has `grace_days_remaining ≤ 2`, " · {m} ending within 2 days". "exit zone" wording is removed. The card links to `/Positions?grace=open` whenever the count is above 0, else `/Positions`. The second query (`grace-period-alerts`) is no longer needed by this card.

### 3.3 Worked examples (fixture rows for the ST-10 Playwright test)

| Position | `grace_period` | `grace_days_remaining` | stored `status` | In grace? | Grace ends today? |
|----------|----------------|------------------------|-----------------|-----------|-------------------|
| A, held 0 days | true | 10 | GRACE | Yes | No |
| B, held 9 days | true | 1 | GRACE | Yes | Yes |
| C, held 10 days | false | null | GRACE (stale) | **No** (Card 1 and Card 3 count it today) | No |
| D, held 8 days | true | 2 | OPEN (lagging) | Yes | No |
| E, held 30 days | false | null | PROFITABLE | No | No |

Every count is 3 (A, B, D). Card 3 reads "Ends today" (min remaining 1). Positions to Watch reads "3 in grace · 2 ending within 2 days". Today list Grace ends today: B only. The AC's disagreeing fixture is row C (or a hand-built row with `grace_period: true, grace_days_remaining: null`, which counts as in grace, and is excluded from "Ends today"/"ending within 2 days" because it has no day count).

## 4. "Plan this" on the Today list's New signals rows (ST-11)

**Product Owner decision (the user, in session, 2026-11-18): add it.**

- Each New signals row: Ticker · market · "Research" link · "Plan this" link. "Plan this" goes to `/TradePlan?ticker={ticker}&market={market}&entry_price={current_price}&signal_id={id}` (`entry_price` omitted when the price is null), the same route and parameters as `signals.md` §"Plan this" Action (BLG-UX-09), so the Trade Plan pre-fills exactly as from Signals. `aria-label="Plan this: {TICKER}"`. `data-testid="today-plan-{ticker}"`.
- **Shown on the same statuses as Signals:** `new` and `watchlisted`. The group lists every status today (TL-29), so a row for a `dismissed`, `entered`, `already_held` or `allocation_insufficient` signal keeps only "Research". Worked example: three signals today, statuses `new`, `entered`, `watchlisted` → three rows; "Plan this" on the first and third.
- It is a link, not a button: TL-19 (no data-changing control in the list) still holds. It pre-fills nothing on the Dashboard; the Trade Plan form pre-fills on arrival, as it does from Signals.
- **§13:** §1B's constraint ("no item … pre-fills an action") is amended to: no item executes or confirms an action; "Plan this" opens a form the user completes, the same as on Signals and Screener (covered by `signals.md` §"Plan this" Action's §13 note). The list still adds no ranking, score or "do this" wording; "Plan this" is a navigation label, identical on every row.
- Data-source check: `GET /signals` returns `id`, `ticker` and `market` for every row the group lists (`signals_endpoints.md`); no gap.

## 5. Approvals

- Head of UX & Design: approved (agent-mediated, Design Gate Engine), 2026-11-18.
- Product Owner: approved (the user, in session, 2026-11-18); ST-11 "Plan this" chosen by the Product Owner.
