# Frontend Specification — Dashboard Homepage

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 3.3
**Last Updated:** 2026-08-14
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Release:** v8.8
**EPIC:** EPIC-03
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

The Dashboard Homepage is the primary entry point for daily use. It provides an at-a-glance session summary across five key data categories, enabling the user to understand their current position, risk, and market status in a single view.

**Route:** `/` (root / home)

Users should immediately see:
- How many positions are open and in what states
- Current portfolio heat level (risk exposure)
- How many positions are in grace period and when the next expires
- Current market regime signals and today’s signal count
- Recent trade activity (closes, opens, stop updates)

---

## 1A. Morning Briefing Section

**Design source:** `docs/design/2026-06-19__release-v6.0/morning-briefing/ux_spec.md`

A new section at the top of `DashboardHome.js`, placed **above** the existing five session-summary cards. It provides start-of-day intelligence across five focused cards. The section is always visible and not collapsible.

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

A composite endpoint (`GET /dashboard/summary`) may be introduced to reduce page-load request count. This is an engineering decision to be confirmed at pre-alignment. If introduced, it must be documented in `docs/specs/api_contracts/` and added to `docs/reference/openapi.yaml`. Composite endpoint must only aggregate — no new server-side computations.

| AI Briefing | Endpoint | Key fields |
|-------------|----------|------------|
| AI Daily Briefing Card | `POST /ai/daily-briefing` | `summary`, `actions[]`, `generated_at`, `advisory: true` |

---

## 3. Layout

### Desktop (>768px)

```
Row 1: [ Open Positions ] [ Portfolio Heat ] [ In Grace Today ]
Row 2: [ Signal Status                    ] [ Recent Activity              ]
```

- Row 1: three equal-width cards
- Row 2: two wider cards (Signal Status slightly wider; layout implementation choice within this constraint)

### Mobile (<768px)

All 5 cards stack vertically in order: Open Positions → Portfolio Heat → In Grace Today → Signal Status → Recent Activity.

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

- **Market regime per market:**
  - SPY: RISK-ON ✓ or RISK-OFF ✗
  - FTSE: RISK-ON ✓ or RISK-OFF ✗
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

If no recent activity: show “No recent trade activity”

---

## 4A. Card Empty States (v7.2 — ST-05)

**Design source:** `docs/design/2026-07-15__release-v7.2/dashboard-empty-states/ux_spec.md`

`DataState` (`src/components/ui/DataState.js`) gains an optional `compact` prop (default `false`, non-breaking) that reduces the `empty` branch's padding/icon/heading size for use inside fixed-height card grids (`py-4`/`w-6 h-6` icon/`text-xs` heading vs the default `py-16`/`w-10 h-10`/`text-sm`). `loading`/`error` branches are unaffected by `compact`.

Applied with `compact` to the following cards' own content (inside `DashboardCard`, below the always-visible title label; `DashboardCard`'s own loading/error short-circuit is untouched):

| Card | Empty condition | Icon | Heading | Body | CTA |
|------|-----------------|------|---------|------|-----|
| Open Positions | 0 open positions | `Inbox` | "No open positions" | "Positions you open will appear here." | None |
| In Grace Today | 0 positions in grace | `ShieldCheck` | "No positions in grace" | "You'll be notified as positions approach review." | None |
| Recent Activity | 0 recent trade events | `Activity` | "No recent activity" | "Trade opens, closes, and stop updates will show up here." | None |

No CTA on any of the three — the existing whole-card click-through (§8 Navigation Targets) already provides the next step; a second CTA would compete with it.

**Explicitly out of scope** (not missing data, so no empty state applies): Portfolio Heat (0% is a meaningful value, not absence of data), Signal Status (0 signals today is a valid count). Morning Briefing's five sub-cards and the AI Daily Briefing Card's existing "No briefing yet" state already have appropriately-scaled empty copy for their contexts and are unchanged by this story.

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

Below header bar, above body:
- Amber badge "AI Advisory" (`#D97706` background, white text)
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
| `MONITOR` | `#D97706` (amber) | "MONITOR" |
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

**Header:** `Sparkles` icon (muted) + **"What's New — v{X.Y}"** (version from the changelog's most recent heading).

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
| Page loading | Skeleton cards for all 5 (loading animation) |
| All loaded | All 5 cards render with live data |
| Individual card error | Card shows error indicator (“Unable to load”); other cards render normally |
| All endpoints failed | Full page error with “Retry” button |

Individual card failure must not break other cards. Each card fetches its data independently (or receives it from a composite endpoint that returns partial results). The §6A What's New Panel fetches independently and its failure does not affect any other section (per its own Error state above).

---

## 8. Navigation Targets

| Card | Click navigates to |
|------|--------------------|
| Open Positions | `/positions` |
| Portfolio Heat | `/risk` |
| In Grace Today | `/risk` |
| Signal Status | `/signals` |
| Recent Activity | `/trades` |

Cards are fully clickable (entire card surface is the click target). Visual affordance: subtle hover state (border highlight or shadow lift). The §6A What's New Panel is not clickable (display-only, no navigation target).

---

## 9. Change Log

| Version | Date | Change |
|---------|------|--------|
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
