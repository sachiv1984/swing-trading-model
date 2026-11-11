**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-11__release-v9.17
**Stories:** ST-01 (BLG-FE-260), ST-02 (BLG-FE-261), ST-03 (BLG-FE-262), ST-04 (BLG-FE-257) — EPIC-01; ST-19 (BLG-SPEC-202) — EPIC-07

# Decision Record — Decision-First Positions Page

## 1. Scope of this record

EPIC-01 rebuilds the Positions page around the question "what needs me now?". The four stories edit the same page in the slice order ST-01 → ST-02 → ST-03 → ST-04. ST-19 changes one tooltip on the same page and lands on EPIC-01's version of `Positions.js` (RISK-01), so its wording is fixed here too.

The Product Owner made three choices at this gate (the user, in session, 2026-11-11):

- **Near stop** reuses the Risk Dashboard's existing ≤ 5% band. No new threshold is introduced (§2.2).
- **The single grace view** is one `GracePeriodView` component, shown as the grace entry of the warning strip. Other pages show a count and link to it (§5).
- The Grid and Journal views are not redesigned here. The Journal view is removed by ST-05 (`journal.md` v1.0 §5).

Spec impact: `positions.md` v2.24 → v2.25, `dashboard.md` v4.1 → v4.2, `risk_dashboard.md` v0.1.15 → v0.1.16 (§8).

## 2. Urgency order

### 2.1 Tiers

Every open position falls into exactly one tier. The first match wins.

| Tier | Name | Test | Source |
|------|------|------|--------|
| 1 | Exit condition met | `getExitCondition(position).riskOff === true` | `src/lib/exitCondition.js`, `strategy_rules.md` §8 |
| 2 | Stop reached | `isPostGraceStopBreach(position) === true` | same module, §7 |
| 3 | Near stop | Post-grace (`grace_period === false`), not tier 1–2, and stop distance ≤ 5% (§2.2) | `risk_dashboard.md` §6 colour band |
| 4 | Other | Everything else, including every in-grace position | — |

Within a tier: stop distance % ascending (closest to its stop first), then ticker A–Z. Positions with no computable distance (null stop or price) sort last in their tier, then A–Z.

The predicate lives in one new module, `src/lib/positionUrgency.js` (`getUrgencyTier`, `compareByUrgency`), next to `exitCondition.js`. The table, the narrow-screen cards (ST-02) and the Grid view all sort with it. A query-string deep link (`?position=`, `?exit=`) does not change the order.

### 2.2 Stop distance

- **Percent:** `(price − trailing stop) ÷ price × 100`, on the GBP basis the breach test already uses (`current_price`, `current_trailing_stop`). One decimal place. Negative when the price is below the stop.
- **R:** `(price − trailing stop) ÷ (entry − initial stop)` in native currency (`current_price_native`, `current_trailing_stop_native`, `entry_price`, `initial_stop`). One decimal place, suffix "R". "—" when `entry − initial stop ≤ 0` or any input is null.
- **Near stop band:** ≤ 5.0%. This is the band `risk_dashboard.md` §6 already colours rose on its Stop Dist % column. Reusing it keeps one definition across both pages. It is a display band, not a strategy rule, and the UI never states it as a rule.
- **In grace:** the cell reads "Not enforced (grace)" (`text-xs text-app-muted`, no colour band), as `risk_dashboard.md` §6.2a does. In-grace positions never enter tiers 2 or 3.
- Colour: ≤ 5% `text-app-negative`; ≤ 15% `text-app-warning`; otherwise `text-app-fg` (the Risk Dashboard bands).

## 3. Decision-first table

### 3.1 Default columns

| # | Column | Content |
|---|--------|---------|
| — | Expand | Chevron button, `aria-expanded`, `aria-controls="position-detail-{id}"`, `aria-label="Show details for {TICKER}"` |
| 1 | Ticker | Ticker and market pill (unchanged cell) |
| 2 | Price | Current price, native currency, with the stale marker (unchanged cell) |
| 3 | Stop | Trailing stop, native currency, with the breach badge and frozen indicator (current two-line cell's second line). In grace: "Not enforced (grace)" |
| 4 | To stop | "{x.x}R · {y.y}%" (§2.2), `data-testid="stop-distance"` |
| 5 | P&L % | Unchanged cell |
| 6 | Action needed | Tier 1: existing "RISK OFF" pill; tier 2: existing "STOP REACHED" pill; tier 3: "Near stop" text (`text-app-negative text-xs font-medium`); in grace with `grace_days_remaining = 1`: "Grace ends today" (`text-app-warning text-xs`); otherwise "—". `data-testid="action-needed"` |
| — | Actions | Unchanged icon buttons (exit, edit, trail stop, recheck) |

That is six data columns. The Actions column stays because it holds the only exit control.

"Action needed" reuses copy already on the page or the Dashboard Today list. It adds no "do this" wording and no new ranking (§9).

### 3.2 Expanded row

Clicking the chevron, or pressing Enter or Space on it, opens one full-width row below (`id="position-detail-{id}"`, `data-testid="position-detail"`). It holds every field the table loses, in this order, as a label/value grid (2 columns below `lg`, 4 at `lg`):

Entry price · Initial stop (first line of today's stop cell) · Shares · P&L (GBP) · Days held · State (lifecycle badge) · Grace (days remaining pill) · Earnings · Alerts (risk-off and gap risk badges) · Last reviewed · Stop provenance line (`positions.md` §Stop Provenance Line).

- Rows are collapsed by default. More than one row may be open at once.
- A `?position={id}` deep link opens that row as well as highlighting it.
- Open/closed state is not persisted.
- No animation: the row appears and disappears in one frame. This keeps it out of the §6 motion rule and needs no reduced-motion branch.

### 3.3 Header

The column headers are not sortable. The order is the urgency order, stated in a muted caption above the table: "Sorted by what needs attention first" (`text-xs text-app-muted`, `data-testid="urgency-caption"`).

## 4. Narrow screens

Below `md` (< 768 px), the Table view renders a card list instead of the table (`data-testid="position-decision-card"` per card) in the §2 order:

```
┌──────────────────────────────────────┐
│ AAPL [US]              STOP REACHED  │  ticker, market pill, Action needed
│ $182.40   Stop $185.10   −1.5% · −0.3R│  Price · Stop · To stop
│ P&L +4.2%                 [⋯ Details]│  P&L % · disclosure button
├──────────────────────────────────────┤
│ (details: the §3.2 grid, 2 columns)  │  open only when expanded
│ [Exit] [Edit] [Trail] [Recheck]      │  the row's action buttons
└──────────────────────────────────────┘
```

- Same fields, tier order and Action needed rule as §3. The details grid is §3.2's, 2 columns.
- The action buttons sit in the card footer and are always visible, at least 44 × 44 px each.
- At 390 px width the page has no horizontal scroll (`document.documentElement.scrollWidth ≤ 390`).
- The Grid view below `md` is unchanged (it is already one card per row), but it follows the §2 order.

## 5. Single grace view

### 5.1 The one component

`GracePeriodAlertZone` is replaced by **`GracePeriodView`**, the only component that renders per-position grace detail. It lists **every** open position in grace (not only those within 2 days of the end), so the Risk Dashboard's list can go.

- **Source:** `GET /positions` (in-grace: `grace_period === true`), joined to `GET /positions/grace-period-alerts` for the trade plan summary where present.
- **Order:** `grace_days_remaining` ascending, then ticker A–Z.
- **Row:** ticker (links to `/Positions?position={id}`) · "Day {n} of 10" (existing day convention) · days-left sentence (existing copy, including the `grace_days_remaining = 0` sentence) · the existing trade-plan block (thesis, stop, R-target) or "No trade plan linked." · "View Trade Plan" link when a plan is linked.
- Rows with `grace_days_remaining ≤ 2` keep today's amber accent (left border, `text-app-warning` day label). Others use the neutral strip style.
- **Dismiss is removed.** A dismissed alert hid detail that is now the page's only grace view. The `grace_alert_dismissed_*` session keys are no longer read.
- `data-testid="grace-period-view"`, rows `data-testid="grace-row-{ticker}"`.

### 5.2 Where it renders

`GracePeriodView` is the expanded content of the warning strip's grace entry (§6). The entry exists whenever at least one position is in grace.

- `/Positions?grace=open` opens the strip's grace entry and scrolls it into view (instant scroll; `scrollIntoView({ block: "start" })` with no smooth behaviour).
- The table's Grace column moves to the expanded row (§3.2). A days-remaining pill and the Today list's "Grace ends today" rows are a status and a count, not grace detail, and stay.

### 5.3 The other surfaces

| Surface | Today | After ST-04 |
|---------|-------|-------------|
| Dashboard Card 3 "In Grace Today" (`GracePeriodCard.js`) | Count, next expiry; click → `/risk` | Same count and "Next expires" line; click → `/Positions?grace=open` |
| Dashboard Morning Briefing "Positions to Watch" (`ExitZoneCard.js`) | Count of exit zone and in-grace, click → `/Positions` | Unchanged. Already a count and a link. |
| Risk Dashboard §5 Grace Period Status Panel (`GracePeriodPanel.js`) | Table of in-grace positions | Heading, count badge ("N positions in grace period") and "Next ends in {n} day(s)" (lowest `grace_days_remaining`, a field the panel already reads) only, with a "View grace periods on Positions" link → `/Positions?grace=open`. The row table is removed. Empty state unchanged. |
| Risk Dashboard §6 table | "Not enforced (grace)" cells | Unchanged (a status, not grace detail) |

## 6. Warning strip

One `PositionsWarningStrip` (`data-testid="positions-warning-strip"`) replaces the four stacked components between the page header and the view content. It renders only when at least one warning is active, so a quiet portfolio shows no strip and no gap.

**Entries,** in fixed order (most severe first), one per active warning:

| Order | Entry | Active when | Summary line (collapsed) | Expanded content |
|-------|-------|-------------|--------------------------|------------------|
| 1 | Drawdown | `DrawdownReviewPrompt` would render | "Drawdown review: {current}% against a {threshold}% threshold" | The current prompt content, unchanged |
| 2 | Concentration | `ConcentrationLimitsWarning` would render | "Concentration limit exceeded: {n} breach(es)" | The current warning content, unchanged |
| 3 | Grace period | One or more positions in grace | "{n} position(s) in grace · next ends {dd MMM}" | `GracePeriodView` (§5). Before ST-04 merges: today's `GracePeriodAlertZone` content |
| 4 | Metrics staleness | `MetricsStalenessIndicator` would render | Its current one-line text | The indicator's current detail, unchanged |

- Each entry is a row: an icon in the warning's existing accent colour, the summary line, and a "Show details" / "Hide details" text button (`aria-expanded`, `aria-controls`). `data-testid="warning-entry-{drawdown|concentration|grace|staleness}"`.
- All entries start collapsed, except that `?grace=open` opens the grace entry.
- Strip surface: `bg-app-raised border border-app-line rounded-xl`, entries divided by `border-app-line`. Text in `app-fg` / `app-muted` tokens.
- `role="region"`, `aria-label="Warnings"`. The old per-warning `role="alert"` live regions are removed, because they announced on every page load.
- No animation (as §3.2).
- The summary text reads from each component's existing query, so no new API call is added.

## 7. Exit Zone tooltip

The PROFITABLE lifecycle badge tooltip reads "Advances to Exit Zone when P&L reaches 2R target". The 2R test exists only in `backend/services/position_lifecycle_service.py` (price ≥ entry + 2 × (entry − initial stop)). `strategy_rules.md` defines no R-multiple rule. The Strategy Rules & System Intent Owner chooses before the sprint seals (RISK-05). The UI wording for each choice is fixed here:

| Owner's choice | PROFITABLE tooltip | EXIT ZONE tooltip |
|----------------|--------------------|-------------------|
| (a) Add the threshold to `strategy_rules.md` §11 | "Advances to Exit Zone when the price reaches {EXIT_ZONE_R_MULTIPLE}R above entry (§11)." The number is imported from `src/constants/strategy.js` and checked by `scripts/check_strategy_copy.py`. | "The price is {EXIT_ZONE_R_MULTIPLE}R or more above entry (§11). Review the stop or exit." |
| (b) Reword without a number | "Advances to Exit Zone when the price is well above the initial risk taken. The app's lifecycle labels mark this; it is not a strategy rule." | "The price is well above the initial risk taken. Review the stop or exit." |

Either way the wording describes the shipped behaviour and states no number that `strategy_rules.md` lacks. "R" is defined in the glossary (`docs/reference/glossary.md`).

## 8. Frontend spec impact (this gate)

- `pages/positions.md` v2.24 → v2.25: new §Decision-First Table (§2–§3), §Warning Strip (§6), §Grace Period View replacing §Grace Period Alert Zone (§5), Responsive Behavior Table row (§4), lifecycle tooltip note (§7).
- `pages/dashboard.md` v4.1 → v4.2: Card 3 click target (§5.3).
- `pages/risk_dashboard.md` v0.1.15 → v0.1.16: §5 reduced to a count and a link (§5.3).

## 9. §13 compliance

Display-only. The urgency tiers apply existing deterministic §7/§8 tests and the Risk Dashboard's existing distance band; no new score, ranking signal or recommendation is introduced. "Action needed" reuses existing pill and Today-list copy, which already passes `scripts/check_ui_copy_forbidden_phrases.py`. Nothing submits an exit; the exit stays the user's click on the existing button. No AI call is added.

## 10. Testability (CLAUDE.md §2)

Every AC below is observable, so each needs Playwright coverage (light and dark where colour is asserted):

- **ST-01:** with four mocked positions (one per tier, plus an in-grace breach), rows render in tier order; the header row has 6 data columns plus expand and Actions; expanding a row shows `position-detail` with every §3.2 field; the in-grace breach is tier 4 with "Not enforced (grace)".
- **ST-02:** at 390 × 844, `position-decision-card` elements render in the same order, `scrollWidth ≤ 390`, and Details opens the grid.
- **ST-03:** with all four warnings mocked active, `positions-warning-strip` has four entries in §6 order; each "Show details" reveals its content; with none active, no strip renders.
- **ST-04:** `grace-period-view` is the only element on any page with per-position "Day n of 10" text (Dashboard, Risk Dashboard and Positions visited); Card 3 and the Risk Dashboard link go to `/Positions?grace=open`, which opens the grace entry.
- **ST-19:** the PROFITABLE tooltip text matches the chosen row of §7; `scripts/check_strategy_copy.py` passes.

## 11. Approval

Head of UX & Design: confirmed, 2026-11-11 (agent-mediated, Design Gate Engine).
Product Owner: confirmed, 2026-11-11 (the user, in session; near-stop band and single grace view chosen at this gate).
ST-19's §7 row is chosen by the Strategy Rules & System Intent Owner before the sprint seals (RISK-05).
