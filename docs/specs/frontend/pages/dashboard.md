# Frontend Specification — Dashboard Homepage

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 4.1
**Last Updated:** 2026-11-09 (ST-06, EPIC-02, v9.16, BLG-FE-254 — §1B Group headers and TL-21: the Market regime header shows its name only, no count; clarification, edited on user direction); prior — 2026-11-04 (ST-09, EPIC-02, v9.15, BLG-SPEC-215 — new §1B Today list: market regime, exits due, grace ends today, stops moved, new signals, first on the page (Product Owner ruling on "stop changes due"); Card 4 and the Exit Conditions Met row merge into it; testable ACs TL-01..TL-29); prior — 2026-11-03 (v9.15 design gate — ST-14/BLG-FE-266: §6A header has no version suffix when the version is absent); prior history retained — see prior entries in version control
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Release:** v8.8
**EPIC:** EPIC-03
**Design Source (v4.0):** docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md §2.2 (ST-09)
**Design Source (v3.10):** docs/design/2026-10-29__release-v9.14/market-regime-unknown/decision_record.md (ST-03), docs/design/2026-10-29__release-v9.14/fx-rate-source-indicator/decision_record.md (ST-04/ST-05), docs/design/2026-10-29__release-v9.14/stale-price-marker/decision_record.md (ST-08)
**Design Source (v3.8):** docs/design/2026-10-08__release-v9.11/risk-price-integrity/decision_record.md (ST-10 stale-price sub-line); `design_system.md` §Consistency Rules → Number and Currency Formatting (v1.21) for ST-15 — pre-existing canonical rule, no new design artefact
**Design Source (v3.6):** `design_system.md` §Consistency Rules → Number and Currency Formatting (v1.21) — pre-existing canonical rule ("zero renders unsigned in the neutral tone"); no new design artefact authored, applied to a second element (icon badge) within an already-conforming component (the card's own P&L value text already used the same three-way logic)
**Design Source (v3.5):** docs/design/2026-09-14__release-v9.4/ai-advisory-disclosure-badge/decision_record.md (BLG-AI-05)
**Design Source (v3.4):** docs/design/2026-09-03__release-v9.1/dashboardhome-ai-advisory-badge-contrast/decision_record.md (BLG-FE-165)
**Design Source (v3.3):** docs/design/2026-08-14__release-v8.8/whats-new-user-benefit-copy/decision_record.md (BLG-FE-161)
**Design Source (v3.2):** docs/design/2026-07-24__release-v7.8/whats-new-panel/ux_spec.md (BLG-FE-128)
**Design Source (v3.1):** docs/design/2026-07-15__release-v7.2/dashboard-briefing-hierarchy/ux_spec.md (BLG-FE-111)
**Design Source (v3.0):** docs/design/2026-07-15__release-v7.2/dashboard-empty-states/ux_spec.md (BLG-FE-110)
**Design Source (v2.8):** docs/design/2026-07-12__release-v7.0/heading-light-theme-contrast/decision_record.md (BLG-FE-95 remediation)
**Design Source (v2.6):** docs/design/2026-07-06__release-v6.7/secondary-text-contrast/ux_spec.md (BLG-FE-88 remediation)
**Design Source (v2.5):** docs/specs/qa/ai_disclaimer_visibility_assessment.md (BLG-UX-01 remediation)
**Design Source (v2.4):** docs/design/2026-06-26__release-v6.3/morning-briefing-progressive-disclosure/ux_spec.md
**Design Source (v2.3):** docs/design/2026-06-24__release-v6.2/ai-daily-briefing-card/ux_spec.md
**Design Source (v2.2):** docs/design/2026-06-22__release-v6.1/gate-proximity-indicator/ux_spec.md
**Design Source (v2.1):** docs/design/2026-06-19__release-v6.0/morning-briefing/ux_spec.md
**Design Source (v2.0):** docs/design/2026-03-06__release-v1.9/dashboard-home/ux_spec.md
**Confirmed by:** Head of Specs Team — 2026-07-24

---

## 1. Purpose & User Goals

The Dashboard Homepage is the primary entry point for daily use. It provides an at-a-glance session summary across five key data categories (v4.0: led by the Today list, §1B, with Card 4 merged into it), enabling the user to understand their current position, risk, and market status in a single view.

**Route:** `/` (root / home)

**v4.0:** the page leads with the Today list (§1B): the decisions due today, in a fixed order, each linking to where the user acts. The status summary follows below it.

Users should immediately see:
- What needs attention today: the market regime, exits due, grace periods ending, stops moved and new signals (§1B)
- How many positions are open and in what states
- Current portfolio heat level (risk exposure)
- How many positions are in grace period and when the next expires
- Current market regime signals and today’s signal count
- Recent trade activity (closes, opens, stop updates)

---

## 1B. Today List

*Added v4.0 (ST-09, EPIC-02, v9.15, BLG-SPEC-215). Design brief: `docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md` §2.2. Built by `BLG-FE-254` (v9.16); until then `DashboardHome.js` keeps the v3.11 layout, which is planned work, not a deviation.*

The first thing on the page, directly under the page title: what needs the user's attention today, in a fixed order, each item linking to the place where the user acts on it. Nothing on the list executes anything.

### Groups and order

The list has five groups, always in this order. Within a group, the item order is fixed by the rule in the table. The rules are mechanical (strategy reason, alphabet, screener order); none ranks or scores an item.

| Order | Group | Data source | Item | Item order | Link |
|-------|-------|-------------|------|------------|------|
| 1 | **Market regime** | `GET /market/status` (as Card 4 today) | One row per market: "US (SPY)" and "UK (FTSE)", with the regime badge RISK-ON ✓, RISK-OFF ✗ or UNKNOWN ? (the v3.10 unknown state, its accessible description and tooltip unchanged) | US, then UK | Row links to `/Signals` |
| 2 | **Exits due** | `GET /positions`, filtered by the shared `getExitCondition` predicate (`positions.md` §Exit Dialog Pre-Selection and Deep Link): a post-grace stop breach or `risk_off_exit` | Ticker · reason pill ("RISK OFF" `#1E40AF` or "STOP REACHED" `#EA580C`, existing pills) · "Review exit" link | Risk-off first, then stop reached (the predicate's own precedence); A–Z by ticker within each | "Review exit" → `/Positions?exit={position_id}`, `aria-label="Review exit for {TICKER}"` |
| 3 | **Grace ends today** | `GET /positions`: open positions in grace with `grace_days_remaining = 1` (Day 10 of 10, `positions.md` §Grace Period Alert Zone day convention) | Ticker · "Grace ends today — the trailing stop applies from the next session" | A–Z by ticker | Row links to `/Positions?position={position_id}` |
| 4 | **Stops moved** | `GET /positions` field `stop_last_moved_date` and `previous_stop` (new, read-only; see Data dependency) | Ticker · "Stop moved from {previous} to {current}" in the position's native currency | A–Z by ticker | Row links to `/Positions?position={position_id}` |
| 5 | **New signals** | `GET /signals`, today's rows by the same filter Card 4 uses today: `signal_date` equals the user's local date, or `created_date` starts with it (`SignalStatusCard.js`). Every status counts, as in Card 4's count | Ticker · market · "Research" link | The order the screener produced them (`signal_date DESC, rank ASC`, the API's order). The rank number is not shown | "Research" → `/research/{ticker}`, `aria-label="Research {TICKER}"` |

- **Caps:** groups 2–5 show at most 5 items. Overflow shows a "+N more" link: Exits due, Grace ends today and Stops moved → `/Positions`; New signals → `/Signals`.
- **Exits due sub-line:** under the Exits due group header, the v9.10 muted sub-line stays: "These positions meet a strategy exit condition (§8). Nothing is exited automatically."
- **Links are router-relative:** routes in this section omit the HashRouter `/#` prefix (`/Positions?exit={id}` is `/#/Positions?exit={id}` in the address bar), as in §8.
- **Group headers:** the group name and its count, e.g. "Exits due · 2". The Market regime header shows its name only, "Market regime", with no count: its rows are the two markets, not items due. A group with no items is not shown, except Market regime, which always shows.
- **"Stop changes due" in the brief (clarification, Product Owner ruling 2026-11-04):** the app has no manual stop change (`positions.md` §Trail Stop Action, ruling `ESC-EXEC-20261013-06`), so the brief's "stop changes due" is met by two display-only groups: **Grace ends today** (a stop starts being enforced at the next session; existing data) and **Stops moved** (stops the nightly job raised; needs `BLG-BE-205`). Neither offers a stop action.
- **Stops moved, why it is here:** stops are moved only by the nightly trailing-stop job (`strategy_rules.md` §7.1, per the clarification above). The group shows which stops the job moved since the last run; it offers no stop action.
- **Data dependency (Stops moved):** `GET /positions` does not record when a stop last moved (`compliance_service.py` notes the missing column). The group needs a read-only `stop_last_moved_date` and `previous_stop` per open position, written by the nightly job, tracked as `BLG-BE-205`. Until those fields exist, the Stops moved group is not rendered and its ACs (TL-09, TL-10) are not testable; the other groups ship without it.

### Quiet day

When groups 2–5 are all empty, the list collapses to one line under its title:

"Nothing due today · US {RISK-ON ✓ | RISK-OFF ✗ | UNKNOWN ?} · UK {…}"

The regime badges keep their colours and the unknown badge keeps its accessible description. No empty-state box, icon or illustration.

### States

| State | Rendering |
|-------|-----------|
| Loading | Each group shows one single-line skeleton row until its own source resolves; groups whose source has resolved render at once. No spinner. Before any source resolves, that is one skeleton row per group. |
| Ready | Groups per the table above, or the quiet-day line |
| One source fails | That group shows one muted line, "Couldn't load {group name}." with a "Retry" text button that refetches that source only. Other groups render normally. A failed `GET /positions` affects Exits due, Grace ends today and Stops moved; a failed `GET /signals` affects New signals; a failed `GET /market/status` shows the Market regime group's error line. The quiet-day line is never shown while any source has failed. |
| All sources fail | One line, "Today's list is unavailable." with "Retry" (refetches all three) |

### Container and placement

- Full-width `DashboardCard` styling, title "Due today" (`text-sm font-semibold`), `data-testid="today-list"`. The title is not "Today", because that is the name of the navigation area the Dashboard sits in (`glossary.md` §UI Labels). Each group `data-testid="today-group-{regime|exits|grace|stops|signals}"`; each item row `data-testid="today-item-{group}-{ticker or market}"`; the quiet line `data-testid="today-quiet"`.
- Placed directly below the page title and above everything else (§3 Layout).
- On mobile the groups stack in the same order, full width.

### What moves or merges

| Today | v3.11 home | Change |
|-------|------------|--------|
| Market regime | Card 4 Signal Status regime rows | Moves here. Card 4 is removed (its signal count becomes the New signals group count). |
| Exits due | §1A Exit Conditions Met row | Moves here, with the same predicate, pills, link, aria-label and sub-line. The row is removed from the Morning Briefing. **Deliberate change:** rows are ordered risk-off first, then A–Z (the shipped row keeps API order). |
| Grace ends today | Card 3 In Grace Today shows a count and the next expiry date | New group. Card 3 stays as the grace summary. |
| New signals | Card 4 "N new signals today" | Becomes this group. |
| Stops moved | — (Recent Activity's "Stop updated" entry reads a field the API does not send) | New. Recent Activity drops its dead "Stop updated" branch when `BLG-BE-205` ships, so stop moves appear in one place. |

The five Morning Briefing cards, the AI Daily Briefing, Cards 1, 2, 3 and 5, Gate Progress and What's New are unchanged and sit below the list (§3).

### Strategy constraints (§13)

- Display-only: every item is a link to a page; no item executes, confirms or pre-fills an action.
- New signals lists signals the screener already produced, in the screener's order. The list adds no ranking, score, highlight or "do this" wording (brief §2.2 constraint), so no separate §13 confirmation is needed. Changing that needs its own §13 confirmation first.
- Exits due reuses the v9.10 Exit Conditions Met copy, already checked. The Grace ends today and Stops moved copy is new, display-only, and covered by TL-20. All list copy must pass `scripts/check_ui_copy_forbidden_phrases.py`.

### Testable acceptance criteria

*For `BLG-FE-254`. Every observable behaviour in this section has a row.*

| ID | Behaviour | Test |
|----|-----------|------|
| TL-01 | The Today list is the first element after the page title | Playwright: `today-list` precedes every other card in DOM order |
| TL-02 | Groups render in the order regime, exits, grace, stops, signals | Playwright with all five populated (stops after `BLG-BE-205`) |
| TL-03 | Market regime always shows US then UK, with RISK-ON/RISK-OFF/UNKNOWN badges; UNKNOWN keeps its accessible description | Playwright with a mocked unknown SPY |
| TL-04 | A regime row links to `/Signals` | Playwright click |
| TL-05 | Exits due lists exactly the positions the `getExitCondition` predicate selects (in-grace breaches excluded) | Playwright: one post-grace breach, one in-grace breach, one risk-off, one healthy → 2 rows |
| TL-06 | Exits due order: risk-off before stop reached, A–Z within each | Playwright with two of each |
| TL-07 | "Review exit" goes to `/Positions?exit={id}` and opens that position's exit dialog; accessible name "Review exit for {TICKER}" | Playwright |
| TL-08 | More than 5 exits: 5 rows and "+N more" → `/Positions` | Playwright with 7 |
| TL-09 | Stops moved lists positions whose `stop_last_moved_date` is the latest nightly run date, "Stop moved from {previous} to {current}" in native currency | Playwright (after `BLG-BE-205`) |
| TL-10 | A Stops moved row links to `/Positions?position={id}` | Playwright (after `BLG-BE-205`) |
| TL-11 | New signals lists today's signals in API order with no rank or score text | Playwright: three signals in a given order render in that order; no digit-only rank cell |
| TL-12 | "Research" links to `/research/{ticker}` | Playwright |
| TL-13 | An empty group (other than regime) is not rendered | Playwright with no signals → no `today-group-signals` |
| TL-14 | Quiet day: no exits, grace endings, stops or signals → only `today-quiet`, reading exactly "Nothing due today · US {badge} · UK {badge}" with both regime badges | Playwright |
| TL-15 | Loading: each group shows one skeleton row until its source resolves; resolved groups render while others still load; no spinner | Playwright with one delayed response |
| TL-16 | A failed source shows "Couldn't load {group}." with Retry; other groups render; Retry refetches only that source | Playwright: `GET /signals` 500 |
| TL-17 | All sources failing shows "Today's list is unavailable." with Retry | Playwright: all three 500 |
| TL-18 | Card 4 and the Morning Briefing Exit Conditions Met row are gone | Playwright: no `exit-conditions-card`, and no element with the text "Signal Status" |
| TL-19 | Nothing in the list is a button that changes data; every item control is a link | Playwright: no `button` inside `today-list` except Retry |
| TL-20 | List copy passes the forbidden-phrases check | `scripts/check_ui_copy_forbidden_phrases.py` in CI |
| TL-21 | Each group header except Market regime shows the group name and its count, e.g. "Exits due · 2". The Market regime header reads exactly "Market regime" (v4.1) | Playwright |
| TL-22 | Exits due shows the sub-line "These positions meet a strategy exit condition (§8). Nothing is exited automatically." | Playwright |
| TL-23 | Grace ends today lists exactly the open positions in grace with `grace_days_remaining = 1`, A–Z, each linking to `/Positions?position={id}` | Playwright: remaining 1, 2 and null → 1 row |
| TL-24 | More than 5 items in Grace ends today, Stops moved or New signals: 5 rows and "+N more" (→ `/Positions`, `/Positions`, `/Signals`) | Playwright with 7 in each (stops after `BLG-BE-205`) |
| TL-25 | The quiet-day line is not shown while any source has failed | Playwright: `GET /signals` 500, no exits or grace endings → error line, no `today-quiet` |
| TL-26 | A failed `GET /positions` shows error lines for Exits due, Grace ends today and Stops moved; a failed `GET /market/status` shows the regime error line | Playwright |
| TL-27 | Mobile (375px): groups stack full width in the same order | Playwright at 375px |
| TL-28 | With Card 4 removed, Recent Activity spans the full width of its row (§3) | Playwright: Recent Activity card width equals the row width at 1440px |
| TL-29 | New signals uses Card 4's date filter (local `signal_date`, or `created_date` starting with it) and counts every status | Playwright with one signal of each status dated today and one dated yesterday |

---

## 1A. Morning Briefing Section

**Design source:** `docs/design/2026-06-19__release-v6.0/morning-briefing/ux_spec.md`

A new section at the top of `DashboardHome.js`, placed **above** the existing five session-summary cards. (v4.0: it sits below the Today list, §1B and §3.) It provides start-of-day intelligence across five focused cards. The section is always visible and not collapsible.

### Section Container & Header (v7.2 — ST-06)

The section is wrapped in an enclosing panel to visually separate it from the session-summary card grid below: `rounded-2xl border border-slate-300/60 dark:border-slate-800 bg-slate-100/60 dark:bg-slate-900/40 p-4` (explicit light/dark pair — see design source for rationale re: prior bare-dark-token contrast defects).

Label: **"Trader's Morning Briefing"** — preceded by a `Sunrise` icon (`text-amber-500 dark:text-amber-400`), `text-sm font-semibold text-slate-700 dark:text-slate-300` (upgraded from plain caption weight to establish a shared "intelligence section" visual language with the AI Daily Briefing Card, §5).

Design source: `docs/design/2026-07-15__release-v7.2/dashboard-briefing-hierarchy/ux_spec.md`.

### Layout

**Desktop (> 768px):** Five equal-width cards in a single horizontal row.

```
[ Screener Hits ] [ Positions to Act On ] [ Red Flags ] [ Earnings Alert ] [ Compliance ]
```

**Mobile (≤ 768px):** Cards stack vertically in the order listed above.

### Exit Conditions Met Row (v9.10 — ST-09, BLG-FE-199)

**v4.0:** moves into the Today list as its Exits due group (§1B) when `BLG-FE-254` ships; it is then removed from the Morning Briefing. Until then it stays as specified below.

**Design source:** `docs/design/2026-10-06__release-v9.10/exit-condition-surfacing/decision_record.md`

- **Visibility:** rendered only when at least one open position matches the shared `getExitCondition` predicate (`positions.md` §Exit Dialog Pre-Selection and Deep Link): a post-grace stop breach or `risk_off_exit`. Absent while loading, on error, and when nothing qualifies. No empty state, no skeleton.
- **Placement:** full-width row inside the Morning Briefing section, above the five-card grid (first in the mobile stack). The grid layout is unchanged.
- **Container:** `DashboardCard` styling with a 4px left border, orange-600 `#EA580C` (existing breach colour); `data-testid="exit-conditions-card"`.
- **Header:** "Exit Conditions Met" + count. **Sub-line:** "These positions meet a strategy exit condition (§8). Nothing is exited automatically."
- **Rows (max 5):** ticker · reason pill ("RISK OFF" `#1E40AF`, or "STOP REACHED" `#EA580C`, existing pill styles) · "Review exit" link → `/#/Positions?exit={position_id}` (`aria-label="Review exit for {TICKER}"`). Overflow: "+N more" → `/#/Positions`.
- **§13:** display-only. All copy must pass `scripts/check_ui_copy_forbidden_phrases.py`.
- **Observation (not changed here):** the Cards table below names a "Positions to Act On" card. The shipped card is "Positions to Watch" (`ExitZoneCard.js`, grace-period alerts). This pre-existing drift is outside this row's scope.

### Cards

| Card | Primary Metric | Sub-Label / Detail | Empty State | Data Source | Click Target |
|------|----------------|--------------------|-------------|-------------|--------------|
| Screener Hits | Count of new hits since last visit | "since your last visit" | "No new hits" | `GET /screener/results` | `/screener` |
| Positions to Act On | Count in EXIT_ZONE or GRACE_PERIOD state | Up to 3 tickers with state + days-in-state; "+N more" on overflow | "All clear" | `GET /positions` filtered by state | `/positions` |
| Red Flags | Count of new events since last weekly digest | "since last digest" | "No new red flags" | `GET /portfolio/red-flag-journal` | `/red-flag-journal` |
| Earnings Alert | Count of watchlisted/open-position tickers with earnings in next 7 days | Up to 2 tickers with day-of-week; "+N more" on overflow | "No earnings this week" | `GET /earnings/{ticker}` per ticker | Earnings calendar or `/watchlist` |
| Compliance | Current Arc 5 compliance score | Trend arrow ↑↓→ vs prior week; "vs last week" | N/A — score always present when endpoint available | `GET /analytics/arc5-compliance` | `/analytics` |

**Compliance card colour coding:** ≥ 80%: green; 60–79%: amber; < 60%: red.

### Shared Card Behaviour

| Behaviour | Specification |
|-----------|---------------|
| Loading | Skeleton placeholder (same height as loaded card); no section-level spinner |
| Card error | "Unable to load" in muted text; other cards unaffected |
| Click affordance | Entire card surface clickable; hover: subtle border highlight or shadow lift |

---

## 2. Data Sources

| Card | Endpoint | Key field(s) |
|------|----------|-------------|
| Open Positions | `GET /positions` (active filter) | count, state breakdown |
| Portfolio Heat | `GET /portfolio` | `portfolio_heat_percent` |
| In Grace Today | `GET /portfolio` or `GET /positions` | `grace_days_remaining`, earliest expiry |
| Signal Status | `GET /market/status`, `GET /signals` | regime per market, signals today |
| Recent Activity | `GET /trades` or activity endpoint | last 3–5 trade events |
| Today list (v4.0, §1B) | `GET /market/status`, `GET /positions`, `GET /signals` | regime per market; `getExitCondition` inputs; `stop_last_moved_date`/`previous_stop` (`BLG-BE-205`); today's signals in API order; `grace_days_remaining` for Grace ends today |

A composite endpoint (`GET /dashboard/summary`) may be introduced to reduce page-load request count. This is an engineering decision to be confirmed at pre-alignment. If introduced, it must be documented in `docs/specs/api_contracts/` and added to `docs/reference/openapi.yaml`. Composite endpoint must only aggregate — no new server-side computations.

| AI Briefing | Endpoint | Key fields |
|-------------|----------|------------|
| AI Daily Briefing Card | `POST /ai/daily-briefing` | `summary`, `actions[]`, `generated_at`, `advisory: true` |

---

## 3. Layout

### Page order (v4.0)

From the top: page title → **Today list (§1B)** → briefing panel (Morning Briefing §1A, AI Daily Briefing §5) → status cards (§4) → Gate Progress (§6) → What's New (§6A). Until `BLG-FE-254` ships, the v3.11 order (no Today list; Card 4 present) applies.

### Desktop (>768px)

```
Row 1: [ Open Positions ] [ Portfolio Heat ] [ In Grace Today ]
Row 2: [ Signal Status                    ] [ Recent Activity              ]
```

**v4.0:** Card 4 (Signal Status) is removed (§1B What moves or merges), so Row 2 holds Recent Activity alone at full width.

- Row 1: three equal-width cards
- Row 2: two wider cards (Signal Status slightly wider; layout implementation choice within this constraint)

### Mobile (<768px)

All 5 cards stack vertically in order: Open Positions → Portfolio Heat → In Grace Today → Signal Status → Recent Activity. (v4.0: Signal Status is removed, so four cards stack; the Today list stacks above them, §1B.)

### Page Title (v7.0 — ST-08)

`<h1>` "Dashboard" — `text-slate-900 dark:text-white` (was bare `text-white`, invisible on light theme, ~1.1:1 contrast). Reuses the app's existing primary-text pairing (`Layout.js`, dark-mode toggle), no new colour token introduced. Light: `text-slate-900` on `bg-slate-100` ≈17.9:1 (AAA). Dark: `text-white` unchanged, no regression. Sizing/weight unchanged. Design source: `docs/design/2026-07-12__release-v7.0/heading-light-theme-contrast/decision_record.md`.

---

## 4. Card Specifications

### Card 1 — Open Positions

- **Primary:** count of open positions (integer, large)
- **Sub-label:** state breakdown: “N profitable / N losing / N in grace”
- **Source:** `GET /positions` (active filter)
- **Click target:** navigates to `/positions`

---

### Card 2 — Portfolio Heat

- **Primary:** `portfolio_heat_percent` value (percentage, 1dp)
- **Sub-label:** delta vs prior day (from `portfolio_history` if available; omit if unavailable — do not show stale delta)
- **Colour coding:**
  - < 15%: green
  - 15–25%: amber
  - > 25%: red
- **Stale-price sub-line (v3.8 — ST-10, BLG-BE-154; revised v3.10 — ST-08, BLG-FE-214):** when one or more open positions in `GET /portfolio` have `price_is_stale = true`, an extra line appears under the value: "⚠ {N} position price(s) stale", `text-xs text-amber-700 dark:text-amber-400`, `data-testid="dashboard-price-stale-notice"`. The sub-line is not focusable, because the whole card is one link. Instead the card link's accessible description (`aria-describedby`, `sr-only`) is: "Live price unavailable, so the last stored price is shown. Value, P&L and heat use this price until a live price is fetched. Reload the page to try again." The `title` tooltip is removed. It does not change the colour coding or the click target. The per-row markers are on `/risk` (`risk_dashboard.md` §6.6). Design source: `docs/design/2026-10-29__release-v9.14/stale-price-marker/decision_record.md`.
- **FX source sub-line (v3.10 — ST-04/ST-05, BLG-BE-194/BLG-BE-169):** when `GET /portfolio`'s `fx_rate_source` is not `live`, a line appears under the value, after the stale-price sub-line if both show. `text-xs text-amber-700 dark:text-amber-400`, `data-testid="dashboard-fx-source-notice"`. Text: "⚠ FX rate not live: GBP/USD {rate} from {age}" (`last_known`) or "⚠ FX rate unavailable: using fixed GBP/USD {rate}" (`constant`). Its explanation is added to the card link's accessible description. Nothing is shown for `live`. Copy, age format and description: `docs/design/2026-10-29__release-v9.14/fx-rate-source-indicator/decision_record.md` §2.2.
- **Source:** `GET /portfolio`
- **Click target:** navigates to `/risk`

---

### Card 3 — In Grace Today

- **Primary:** count of positions currently in grace period (integer)
- **Sub-label:** “Next expires: {date}” using the earliest `grace_end_date` among grace positions; if none in grace: show “No positions in grace”
- **Source:** `GET /portfolio` or `GET /positions`
- **Click target:** navigates to `/risk` (scrolled to grace panel where supported)

---

### Card 4 — Signal Status

**v4.0:** removed when `BLG-FE-254` ships. Its regime rows become the Today list's Market regime group and its signal count the New signals group count (§1B). The specification below stands until then.

- **Market regime per market:**
  - SPY: RISK-ON ✓, RISK-OFF ✗ or UNKNOWN ?
  - FTSE: RISK-ON ✓, RISK-OFF ✗ or UNKNOWN ?
- **Unknown regime (v3.10 — ST-03, BLG-BE-193):** when `GET /market/status` reports a market's `regime_status` as `unknown` (`is_risk_on: null`), the badge reads "UNKNOWN ?" in neutral slate (`bg-slate-200 text-slate-800 dark:bg-slate-500/20 dark:text-slate-300`), `data-testid="regime-unknown-{SPY|FTSE}"`. It never falls back to RISK-OFF or RISK-ON. The badge's accessible description and hover/focus tooltip: "{US|UK} market regime could not be measured: index data is unavailable." plus the sentence for the Strategy Rules & System Intent Owner's ruling. If the ruling keeps the last known regime, a muted second line reads "last known: {RISK-ON|RISK-OFF}". Branches: `docs/design/2026-10-29__release-v9.14/market-regime-unknown/decision_record.md` §2.3; the unused branches are deleted at implementation.
- **Signals today:** count of signals generated today (“N new signals today”)
- **Source:** `GET /market/status` (regime), `GET /signals` (today filter)
- **Click target:** navigates to `/signals`

---

### Card 5 — Recent Activity

- **Content:** last 3–5 trade events in reverse chronological order
- **Each entry:** ticker + event type + brief value + relative date
  - Closed: “{ticker} closed (+{R}R)” or “{ticker} closed ({P&L})”
  - Opened: “{ticker} opened”
  - Stop updated: “Stop updated on {ticker}”
- **Source:** `GET /trades` (last N, or activity endpoint — engineering to confirm)
- **Click target:** navigates to `/trades`
- **Icon badge colour (v3.6 — ST-35, BLG-FE-192):** the entry icon's background/foreground colour is three-way, matching the adjacent P&L value text — emerald for `pnl > 0`, rose for `pnl < 0`, neutral slate for `pnl === 0` — per `design_system.md` §Consistency Rules → Number and Currency Formatting (zero renders in the neutral tone). Previously used two-way (`>= 0`) logic, which incorrectly rendered zero-P&L entries in the emerald (win) colour.

- **Icon glyph (v3.7 — ST-10, BLG-FE-194):** the glyph is three-way as well: `TrendingUp` for `pnl > 0`, `TrendingDown` for `pnl < 0`, `Minus` for `pnl === 0` (null treated as 0), decorative (`aria-hidden`). Design source: `docs/design/2026-10-06__release-v9.10/recent-trades-neutral-glyph/decision_record.md`.

- **Zero means "displays as £0.00" (v3.8 — ST-15, BLG-FE-204):** the three-way glyph and badge colour test the P&L **as displayed**, rounded to 2 decimal places, not the raw value. A `pnl` of `0.004` displays as "£0.00", so it gets the neutral `Minus` glyph and slate colour. A `pnl` of `0.01` still gets `TrendingUp` and emerald. This is the `design_system.md` v1.21 rule ("zero renders unsigned in the neutral tone") applied to the displayed figure, so the glyph never disagrees with the adjacent "£0.00" text.

If no recent activity: show “No recent trade activity”

---

## 4A. Card Empty States (v7.2 — ST-05)

**Design source:** `docs/design/2026-07-15__release-v7.2/dashboard-empty-states/ux_spec.md`

`DataState`'s `compact` variant (canonical definition: `docs/specs/frontend/design_system.md` §Data States) is used for these cards' `empty` branch, since they live inside fixed-height card grids where the default sizing is oversized. `loading`/`error` branches are unaffected by `compact`.

Applied with `compact` to the following cards' own content (inside `DashboardCard`, below the always-visible title label; `DashboardCard`'s own loading/error short-circuit is untouched):

| Card | Empty condition | Icon | Heading | Body | CTA |
|------|-----------------|------|---------|------|-----|
| Open Positions | 0 open positions | `Inbox` | "No open positions" | "Positions you open will appear here." | None |
| In Grace Today | 0 positions in grace | `ShieldCheck` | "No positions in grace" | "You'll be notified as positions approach review." | None |
| Recent Activity | 0 recent trade events | `Activity` | "No recent activity" | "Trade opens, closes, and stop updates will show up here." | None |

No CTA on any of the three — the existing whole-card click-through (§8 Navigation Targets) already provides the next step; a second CTA would compete with it.

**Explicitly out of scope** (not missing data, so no empty state applies; v4.0: Signal Status leaves with Card 4, §1B): Portfolio Heat (0% is a meaningful value, not absence of data), Signal Status (0 signals today is a valid count). Morning Briefing's five sub-cards and the AI Daily Briefing Card's existing "No briefing yet" state already have appropriately-scaled empty copy for their contexts and are unchanged by this story.

---

## 5. AI Daily Briefing Card (v6.2 — ST-07)

**Design source:** `docs/design/2026-06-24__release-v6.2/ai-daily-briefing-card/ux_spec.md`
**Story:** ST-07 (BLG-FEAT-50)

A full-width card placed below the session-summary cards (§4) and above the Gate Progress Indicator strip (§6). The card synthesises trailing stop alerts, rebalance exits, regime status, and new entries into a plain-English action plan.

### Placement

Full-width card spanning the content area. Does not replace or modify any existing section.

### Card Header

| Element | Position | Spec |
|---------|----------|------|
| Icon (v7.2 — ST-06) | Left, before Title | `Sparkles` (`text-violet-500 dark:text-violet-400`) — same icon used for the "AI draft" badge convention (`trade_plan.md` §5b), establishing a shared "intelligence section" visual language with the Morning Briefing panel (§1A) |
| Title | Left | "Today's Briefing" |
| Timestamp | Centre-right | "Generated HH:MM" (muted, 12px) |
| Regenerate button | Right | Secondary/outlined style; disabled during load |

Design source (icon addition): `docs/design/2026-07-15__release-v7.2/dashboard-briefing-hierarchy/ux_spec.md`. No other change to this card's container, states, or behaviour.

### Advisory Label

Below header bar, above body — this is the first applied instance of the shared `AdvisoryBadge` component (`design_system.md` §Shared UI Components → AdvisoryBadge, v1.14, ST-22/BLG-AI-05, v9.4). No visual change from this citation — the markup below is unchanged, now named/generalised rather than page-local:
- Amber badge "AI Advisory" (`#B45309` background — `bg-amber-700`, white text; darkened from `#D97706`/`bg-amber-600` v9.1 design gate, WCAG AA colour-contrast fix — see §9 v3.4)
- Inline static text: "All actions require your confirmation" (`text-slate-700 dark:text-slate-300` italic, 12px — contrast ≥4.5:1 on both `bg-slate-800` (dark) and `bg-slate-100` (light); dark value unchanged since v2.5/BLG-UX-01, light companion added v2.6/BLG-FE-88; was bare `text-slate-500` prior to v2.5/BLG-UX-01)
- **Non-dismissible**

### Card Body

| Section | Content |
|---------|---------|
| Summary | `response.summary` — plain paragraph, 2–4 sentences |
| Actions | `response.actions[]` — ordered list: type chip + bold ticker + description |

**Action type chips:**

| Type | Chip Colour | Label |
|------|------------|-------|
| `EXIT` | `#DC2626` (red) | "EXIT" |
| `ENTER` | `#16A34A` (green) | "ENTER" |
| `MONITOR` | `#B45309` (amber-700) (v3.9, ST-24, BLG-FE-210: was `#D97706`/`bg-amber-600`, white text 3.19:1, below WCAG AA; `bg-amber-700` is 5.02:1. Same rule as `BLG-FE-165`, v9.1) | "MONITOR" |
| `HOLD` | `#6B7280` (grey) | "HOLD" |

### States

| State | Behaviour |
|-------|-----------|
| No briefing yet | "No briefing for today. Click Regenerate to generate your daily summary." + Regenerate button enabled |
| Loading | Skeleton body (2-line summary, 3-row actions); Regenerate disabled |
| Normal | Summary + action list |
| Empty actions | Summary shown; "No specific actions required today." (muted) |
| Error | "Unable to generate briefing. Try regenerating." (muted red); Regenerate enabled |

### Interactions

**Regenerate button:** Calls `POST /ai/daily-briefing`. Card enters Loading state. On success: updates summary, actions, and timestamp. On error: Error state.

Card content is **display-only** — action items are informational only; no one-click trade execution.

### Constraints

**§13 compliance:** Advisory-only. No action type is executable from this card. Advisory label is non-dismissible. `response.advisory = true` must be verified client-side; if absent or false, show error.

### Progressive Disclosure — Section Collapse (v6.3 — ST-12)

**Design source:** `docs/design/2026-06-26__release-v6.3/morning-briefing-progressive-disclosure/ux_spec.md`

The card body sections are individually collapsible. The advisory label and card header remain always visible (§13 requirement).

#### Collapsible Sections

| Section Key | Section Label | Content |
|------------|--------------|---------|
| `summary` | **Market Context** | `response.summary` paragraph |
| `actions` | **Suggested Actions** | `response.actions[]` ordered list |

#### Section Header Row

Each section is preceded by a header row:

| Element | Spec |
|---------|------|
| Section label | Left-aligned, `text-sm font-semibold text-slate-300` |
| Toggle icon | `ChevronDown` (expanded) / `ChevronRight` (collapsed) — Lucide; right-aligned; `text-slate-400` |
| Separator | `border-t border-slate-700/50` above each section header (except the first) |
| Hover | `hover:bg-slate-700/20`; `cursor-pointer` on full header row width |
| Click target | Full width of section header row |

#### Collapse Behaviour

- Each section collapses and expands independently
- Collapsed state: content hidden; section header visible
- Expanded state: content fully visible below section header
- Transition: instant toggle; smooth 150ms height transition preferred

#### localStorage Persistence

**Key:** `ai-briefing-collapse-state-v1`

**Value:**
```json
{ "summary": false, "actions": false }
```

`false` = expanded (default); `true` = collapsed.

- On mount: read and apply stored state
- On toggle: update localStorage synchronously
- If key absent or parse error: default all expanded; do not throw
- No server-side persistence

#### Default State

All sections expanded — ensures no content is hidden for first-time users.

#### States Integration

| Card State | Section Header Behaviour |
|-----------|------------------------|
| Loading | Section headers shown; toggle disabled; skeleton body |
| No briefing yet | Section headers not shown; placeholder fills card body |
| Error | Section headers not shown; error message fills card body |
| Normal | Section headers shown; localStorage state applied |

#### Playwright Coverage

Test ID `SC-BRIEF-01`: expand all → collapse Market Context → reload → assert Market Context collapsed, Suggested Actions expanded.

---

## 6. Gate Progress Indicator

**Design source:** `docs/design/2026-06-22__release-v6.1/gate-proximity-indicator/ux_spec.md`
**Story:** ST-07 (BLG-FE-78)

A compact full-width strip placed below the 5 session-summary cards. Does not replace or modify any existing section. Lighter visual weight than session-summary cards (no card frame).

**Section label:** “Gate Progress” — left-aligned, muted text (consistent with Morning Briefing label weight)

**Data source:** `GET /portfolio/gate-metrics` (existing endpoint, BLG-BE-34)

### Display

| State | Format |
|-------|--------|
| Gate not met | `{closed_trades}/{threshold} closed trades · {remaining} more to unlock quality insights` muted sub-label + progress percentage + blue progress bar |
| Gate met | `Quality insights unlocked ✓` in green + `{closed_trades} closed trades` muted sub-label |
| Loading | Single-line skeleton placeholder |
| Error | Strip hidden silently — gate-metrics failure must not affect Dashboard primary content |

**Progress bar:** 4px height (`h-1.5`), full content width. Fill proportional to `closed_trades / gate_threshold`. Blue while in progress; strip switches to a green-tinted container once `gate_met = true` (no progress bar shown in the met state).

**Threshold:** sourced from `gate_threshold` field in API response — not hardcoded client-side (client-side `GATE_THRESHOLD = 20` constant used only as a fallback default if the field is absent).

**Interaction:** Display-only. No click, no navigation. Refreshes on page load (no polling).

**Wording rationale (ST-10, BLG-SPEC-73 resolution):** The copy intentionally avoids surfacing internal story/gate code names (`PT-04`/`SI-02`) to end users, using a benefit-oriented "quality insights" framing instead. This table now documents the shipped copy verbatim as canonical — see Change Log v2.9.

---

## 6A. What's New Panel (v7.8 — ST-01, BLG-FE-128)

**Design source:** `docs/design/2026-07-24__release-v7.8/whats-new-panel/ux_spec.md`

A full-width secondary-tier card placed below the §6 Gate Progress Indicator strip. Shows the most recent release's `### Changes shipped` entries, parsed server-side from `docs/product/changelog.md`'s most recent `## vX.Y` block — not a hardcoded copy, so it requires no manual wiring on future releases.

**Header:** `Sparkles` icon (muted) + **"What's New — v{X.Y}"** (version from the changelog's most recent heading). **v3.11 (ST-14, BLG-FE-266):** when the payload has no version, the header is **"What's New"** with no suffix — never "What's New — undefined". The sidebar footer shows the same version (`navigation.md` §Sidebar Footer and Height). Design source: `docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md` §3.4.

**Body (v3.3 — ST-13, BLG-FE-161):** bullet list of the `User Impact` column (not `Description`) from the most recent `### Changes shipped` table, max 8 bullets shown with a non-interactive "+N more" trailer if the table has more rows. `Description` is the engineering record and is never shown here. Rows with an empty/`—` `User Impact` cell are excluded from the parsed feed entirely — an EPIC with no user-facing change does not produce a bullet. `User Impact` copy is curated, present-tense, second-person, one to two sentences, written for what a user can see/click/notice — never raw implementation nouns (endpoint, table, or component names) or ticket IDs. Authoring convention applies at `changelog.md` authoring time (post-ship closure), not at render time — component rendering itself (bullet list, cap, trailer) is unchanged from v3.2. Design source: `docs/design/2026-08-14__release-v8.8/whats-new-user-benefit-copy/decision_record.md`.

**States:** follows `DataState` default (non-`compact`) sizing per `design_system.md` §Shared UI Components → Cards → Data States:

| State | Rendering |
|-------|-----------|
| Loading | `DataState` `loading` branch |
| Error | `DataState` `error` branch — "Unable to load release notes" |
| Empty | `DataState` `empty` branch — "Nothing to show" / "Check back after the next release." |
| Ready | Title + bullet list per above |

**Interaction:** Display-only. No dismiss/collapse, no click-through, no navigation.

**Backend dependency:** requires a new endpoint to parse and serve the changelog's most recent version block (does not exist yet — implementation detail for sprint execution; contract to be added to `docs/specs/api_contracts/` in the same commit per `CLAUDE.md` §2).

---

## 7. States

| State | Behaviour |
|-------|-----------|
| Page loading | Skeleton cards for all 5 (4 from v4.0, Card 4 removed) (loading animation); the Today list has its own states (§1B) |
| All loaded | All 5 cards (4 from v4.0) render with live data |
| Individual card error | Card shows error indicator (“Unable to load”); other cards render normally |
| All endpoints failed | Full page error with “Retry” button |

Individual card failure must not break other cards, and a Today list source failure affects only its own group (§1B). Each card fetches its data independently (or receives it from a composite endpoint that returns partial results). The §6A What's New Panel fetches independently and its failure does not affect any other section (per its own Error state above).

---

## 8. Navigation Targets

| Card | Click navigates to |
|------|--------------------|
| Open Positions | `/positions` |
| Portfolio Heat | `/risk` |
| In Grace Today | `/risk` |
| Signal Status | `/signals` |
| Recent Activity | `/trades` |
| Today list items (v4.0) | Per item: `/Signals`, `/Positions?exit={id}`, `/Positions?position={id}`, `/research/{ticker}`; "+N more" → `/Positions` or `/Signals` (§1B) |

Cards are fully clickable (entire card surface is the click target). Visual affordance: subtle hover state (border highlight or shadow lift). The §6A What's New Panel is not clickable (display-only, no navigation target).

---

## 9. Change Log

| Version | Date | Change |
|---------|------|--------|
| 4.1 | 2026-11-09 | ST-06 (EPIC-02, v9.16, BLG-FE-254). §1B Group headers and TL-21: the Market regime header shows its name only, "Market regime", with no count, because its rows are the two markets, not items due. Clarification, no behaviour change. Recommended by the Frontend Specifications & UX Documentation Owner (agent-mediated, §5.3) after the EPIC-02 DoQ review; edited on user direction, 2026-11-09. |
| 4.0 | 2026-11-04 | ST-09 (EPIC-02, v9.15, BLG-SPEC-215) against the `site-structure-phase1` §2.2 brief. New §1B Today list ("Due today"), first on the page: Market regime (US, UK; unknown state kept), Exits due (the `getExitCondition` predicate, risk-off first, v9.10 sub-line kept), Grace ends today (`grace_days_remaining = 1`), Stops moved (needs `BLG-BE-205`'s read-only `stop_last_moved_date`/`previous_stop`; not rendered until then), New signals (screener order, no rank shown, "Research" link). Fixed group order, caps of 5 with "+N more", a one-line quiet-day state, loading/per-source error/all-failed states, and testable ACs TL-01..TL-29 for `BLG-FE-254`. The brief's "stop changes due" is met by the Grace ends today and Stops moved groups (Product Owner ruling 2026-11-04). Card 4 and the §1A Exit Conditions Met row merge into the list; §3 page order, §7 and §8 updated. §13: display-only, no new ranking, score or "do this" wording. Built by `BLG-FE-254` (v9.16); v3.11 layout stands until then. Head of UX & Design and Head of Specs Team review: see the v9.15 `qa_evidence_EPIC-02.md` ST-09 entry. |
| 3.11 | 2026-11-03 | v9.15 design gate — (ST-14, EPIC-02, BLG-FE-266) §6A What's New header drops the version suffix when the payload has no version; the sidebar footer shows the same version (`navigation.md` v1.8). Design source: `docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md`. Head of UX & Design + Product Owner approved. Head of Specs Team confirmed. |
| 3.10 | 2026-10-29 | v9.14 design gate — (ST-03, EPIC-01, BLG-BE-193) §4 Card 4 gains a neutral UNKNOWN ? regime state with a ruling-dependent description. (ST-04/ST-05, EPIC-01, BLG-BE-194/BLG-BE-169) §4 Card 2 FX source sub-line when the FX rate is last-known or the fixed fallback. (ST-08, EPIC-01, BLG-FE-214) §4 Card 2 stale-price explanation moves from `title` to the card link's accessible description, with new copy and the light-theme amber pair. Design sources: `docs/design/2026-10-29__release-v9.14/market-regime-unknown/decision_record.md`, `.../fx-rate-source-indicator/decision_record.md`, `.../stale-price-marker/decision_record.md`. Head of UX & Design sign-off: 2026-10-29. Product Owner approved: 2026-10-29. Head of Specs Team confirmed. |
| 3.9 | 2026-10-12 | v9.12 design gate — (ST-24, EPIC-03, BLG-FE-210) §5 AI Daily Briefing `MONITOR` action badge `#D97706` → `#B45309` (`bg-amber-700`): white text 3.19:1 → 5.02:1, WCAG AA. Same rule as `BLG-FE-165` (v9.1, §9 v3.4); no new decision record. Head of UX & Design sign-off: 2026-10-12. Product Owner approved: 2026-10-12. Head of Specs Team confirmed. |
| 3.8 | 2026-10-08 | v9.11 design gate — (ST-10, EPIC-02, BLG-BE-154) §4 Card 2 stale-price sub-line from `price_is_stale`; design source `docs/design/2026-10-08__release-v9.11/risk-price-integrity/decision_record.md`. (ST-15, EPIC-02, BLG-FE-204) §4 Card 5 three-way glyph and colour test the P&L rounded to 2 dp, so a value that displays as £0.00 is break-even; pre-existing `design_system.md` v1.21 rule, no new decision record. Head of UX & Design sign-off: 2026-10-08. Product Owner approved: 2026-10-08. Head of Specs Team confirmed. |
| 3.7 | 2026-10-06 | v9.10 design gate — (ST-09, EPIC-02, BLG-FE-199) §1A new conditional "Exit Conditions Met" full-width row above the five-card grid, sharing the `getExitCondition` predicate with the Positions exit dialog; each row links to `/#/Positions?exit={id}`. (ST-10, EPIC-02, BLG-FE-194) §4 Card 5 icon glyph made three-way (`Minus` for break-even). Head of UX & Design sign-off: 2026-10-06. Product Owner approved: 2026-10-06. Head of Specs Team confirmed. |
| 3.6 | 2026-10-01 | v9.9 design gate — Card 5 Recent Activity icon-badge colour fix (ST-35, EPIC-06, BLG-FE-192): icon background/foreground changed from two-way (`>= 0`) to three-way colour logic, giving `pnl === 0` a neutral slate treatment instead of the emerald (win) colour, matching the card's own P&L value text and `design_system.md`'s existing zero-neutral rule (§Consistency Rules → Number and Currency Formatting, v1.21). Design source: pre-existing canonical rule, no new decision record required — see Design Source (v3.6) above. Head of UX & Design sign-off: 2026-10-01. Product Owner approved: 2026-10-01. Head of Specs Team confirmed. |
| 3.5 | 2026-09-14 | v9.4 design gate — (ST-22, EPIC-05, BLG-AI-05): §5 Advisory Label now cites the new shared `AdvisoryBadge` component (`design_system.md` §Shared UI Components) as its first applied instance — no markup/visual change, page-local prose replaced with a component citation. (ST-25, EPIC-06, BLG-FE-174): confirmed this page's card-level loading skeletons already conform to the canonical loading-skeleton pattern (shared `Skeleton` primitive) — no content change. Design sources: `docs/design/2026-09-14__release-v9.4/ai-advisory-disclosure-badge/decision_record.md`, `docs/design/2026-09-14__release-v9.4/loading-skeleton-standardisation/decision_record.md`. Head of UX & Design sign-off: 2026-09-14. Product Owner approved: 2026-09-14. Head of Specs Team confirmed. |
| 3.4 | 2026-09-03 | v9.1 design gate — Advisory Label badge colour fix (ST-01, EPIC-01, BLG-FE-165): background darkened `bg-amber-600` (`#D97706`) → `bg-amber-700` (`#B45309`), white text unchanged — was 3.18:1 (FAIL vs. WCAG AA 4.5:1 for 12px semibold text), now 5.02:1 (PASS). Same amber hue family, one shade darker; no other property changed. Design source: `docs/design/2026-09-03__release-v9.1/dashboardhome-ai-advisory-badge-contrast/decision_record.md`. Head of UX & Design sign-off: 2026-09-03. Product Owner approved: 2026-09-03. Head of Specs Team confirmed. |
| 3.3 | 2026-08-14 | v8.8 design gate — §6A What's New Panel body source changed (ST-13, EPIC-03, BLG-FE-161): now reads a new `User Impact` column from `changelog.md`'s `### Changes shipped` table instead of `Description`; rows with an empty `User Impact` cell are excluded from the feed. `Description` unchanged, retained as the engineering record. No component/layout/rendering change to `WhatsNewCard.js` itself. Design source: `docs/design/2026-08-14__release-v8.8/whats-new-user-benefit-copy/decision_record.md`. Head of UX & Design sign-off: 2026-08-14. Product Owner approved: 2026-08-14. Head of Specs Team confirmed. |
| 3.2 | 2026-07-24 | v7.8 design gate — §6A What's New Panel added (ST-01, EPIC-01, BLG-FE-128): new full-width secondary-tier card below the Gate Progress Indicator strip, showing the most recent release's `### Changes shipped` entries parsed server-side from `docs/product/changelog.md` (no hardcoded copy, no manual re-wiring per release). `DataState` default sizing (loading/error/empty per `design_system.md`). Display-only, no dismiss/collapse, no navigation. Backend endpoint to parse the changelog does not exist yet — flagged as a sprint-execution implementation dependency requiring an API contract entry in the same commit. Design source: `docs/design/2026-07-24__release-v7.8/whats-new-panel/ux_spec.md`. Head of UX & Design sign-off: 2026-07-24. Product Owner approved: 2026-07-24. Head of Specs Team confirmed. |
| 3.1 | 2026-07-15 | v7.2 design gate — §1A Morning Briefing Section (ST-06, BLG-FE-111): enclosing panel added around the section (`bg-slate-100/60 dark:bg-slate-900/40`, explicit light/dark pair) to visually separate it from the session-summary grid; section label upgraded to `Sunrise` icon + `text-sm font-semibold` (from plain caption weight). §5 AI Daily Briefing Card: `Sparkles` icon added to the header, matching the "AI draft" badge convention, to share the same "intelligence section" visual language as the Morning Briefing panel. No change to any card's data, queries, or the `dashboard-retry-root` retry behaviour. Design source: dashboard-briefing-hierarchy/ux_spec.md. Approved: Product Owner 2026-07-15. Head of Specs Team confirmed. |
| 3.0 | 2026-07-15 | v7.2 design gate — §4A Card Empty States added (ST-05, BLG-FE-110): `DataState` gains a `compact` prop (non-breaking); applied to Open Positions, In Grace Today, and Recent Activity cards' zero-count states (icon + heading + body, no CTA), replacing bare muted text/raw-zero rendering. Portfolio Heat and Signal Status explicitly out of scope (0 is a meaningful value for both, not missing data). Morning Briefing sub-cards and AI Daily Briefing's existing empty state unchanged. Loading/error states unaffected. Design source: dashboard-empty-states/ux_spec.md. Approved: Product Owner 2026-07-15. Head of Specs Team confirmed. |
| 2.9 | 2026-07-13 | v7.0 sprint execution (ST-10, BLG-SPEC-73): Resolved the §6 Gate Progress Indicator copy divergence flagged at v2.7 — updated the Display table to document the shipped `GateProgressStrip.js` copy verbatim as canonical (`{closed}/{threshold} closed trades · {remaining} more to unlock quality insights`, `Quality insights unlocked ✓`) instead of the original, never-implemented `PT-04/SI-02`-coded wording. Removed the §6 Known Deviations note (superseded — no longer a deviation now that spec matches shipped code). No code change; `GateProgressStrip.js` and `tests/e2e/gate-progress.spec.js` were already correct. Wording-only change — FI-P3-02 exception applies (CLAUDE.md), code review of static JSX/text substitutes for staging sign-off. |
| 2.8 | 2026-07-12 | v7.0 design gate — Page-title light-theme contrast fix (ST-08, BLG-FE-95): `text-white` → `text-slate-900 dark:text-white` on the "Dashboard" `<h1>` (light-mode value was missing entirely; ~1.1:1 fail). Same defect class as BLG-FE-87/88, now extended to primary heading text (no prior token existed for this class). No layout change. Design source: `docs/design/2026-07-12__release-v7.0/heading-light-theme-contrast/decision_record.md`. Head of UX & Design sign-off: 2026-07-12. Head of Specs Team confirmed. |
| 2.7 | 2026-07-09 | ST-11 (BLG-QA-64, EPIC-03, v6.8) — Known Deviations added to §6 Gate Progress Indicator: shipped `GateProgressStrip.js` copy ("closed trades... quality insights", "Quality insights unlocked ✓") diverges from this section's specified copy ("{N}/20 trades (PT-04/SI-02 gate)", "Gate cleared ✓"). Filed as BLG-SPEC-73. No layout/behaviour change — text-only finding surfaced while fixing dark Playwright spec `gate-progress.spec.js`. |
| 2.6 | 2026-07-06 | v6.7 design gate — Advisory Label disclaimer light-theme fix (ST-02, BLG-FE-88): added `dark:` companion — `text-slate-700 dark:text-slate-300` (light-mode value was missing entirely; dark-theme value unchanged, already passing since v2.5/BLG-UX-01). No layout or badge change. Design source: `docs/design/2026-07-06__release-v6.7/secondary-text-contrast/ux_spec.md` §4. Head of UX & Design sign-off: 2026-07-06. Head of Specs Team confirmed. |
| 2.5 | 2026-07-02 | v6.4 design gate — Advisory Label disclaimer text contrast fix (ST-09, BLG-UX-01): `text-slate-500` → `text-slate-300` (≈2.7:1 → ≥4.5:1 on `bg-slate-800`, WCAG AA). No layout or badge change. Design source: `docs/specs/qa/ai_disclaimer_visibility_assessment.md` (finding C5, approved 2026-06-29). Head of UX & Design sign-off: 2026-07-02. Head of Specs Team confirmed. |
| 2.4 | 2026-06-26 | v6.3 design gate — §5 progressive disclosure added (ST-12, BLG-FE-80): AI Daily Briefing Card sections (Market Context, Suggested Actions) are individually collapsible; section header rows with ChevronDown/Right toggle; localStorage key ai-briefing-collapse-state-v1 persists state across reloads; default all expanded; §13 advisory label remains non-dismissible and always visible; Playwright test SC-BRIEF-01 required. Design source: morning-briefing-progressive-disclosure/ux_spec.md. Approved: Product Owner 2026-06-26. Head of Specs Team confirmed. |
| 2.3 | 2026-06-24 | v6.2 design gate — §5 AI Daily Briefing Card added (ST-07, BLG-FEAT-50): full-width card below session-summary cards; Regenerate button calls POST /ai/daily-briefing; summary paragraph + ordered action list with type chips (EXIT/ENTER/MONITOR/HOLD); advisory label non-dismissible; §13 compliant display-only; advisory=true verified client-side. Sections renumbered (old §5 Gate Progress→§6, §6 States→§7, §7 Navigation→§8, §8 Change Log→§9). Design source: ai-daily-briefing-card/ux_spec.md. Approved: Product Owner 2026-06-24. Head of Specs Team confirmed. |
| 2.2 | 2026-06-22 | v6.1 design gate — §5 Gate Progress Indicator added (ST-07, BLG-FE-78): compact full-width strip below session-summary cards showing closed-trade count vs 20-trade PT-04/SI-02 gate threshold; uses existing GET /portfolio/gate-metrics endpoint; display-only; error hidden silently. Sections renumbered (old §5→§6, §6→§7, §7→§8). Design source: gate-proximity-indicator/ux_spec.md. Approved: Product Owner 2026-06-22. Head of Specs Team confirmed. |
| 2.1 | 2026-06-19 | v6.0 design gate — §1A Morning Briefing Section added: new section at top of DashboardHome above existing cards; 5 intelligence cards (Screener Hits, Positions to Act On, Red Flags, Earnings Alert, Compliance); horizontal desktop layout, vertical mobile stack; per-card loading/error/empty state behaviour; Compliance card colour-coded by score. Design source: morning-briefing/ux_spec.md. Approved: Product Owner 2026-06-19. Head of Specs Team confirmed. |
| 2.0 | 2026-03-06 | Full rewrite for v1.9 EPIC-03 (ST-05). Dashboard Homepage session summary with 5 data cards. Governance header upgraded to Class 1 compliant format. Design source: docs/design/2026-03-06__release-v1.9/dashboard-home/ux_spec.md. |
| 1.0 | 2026-02-18 | Initial version (pre-governance, general portfolio overview). |
