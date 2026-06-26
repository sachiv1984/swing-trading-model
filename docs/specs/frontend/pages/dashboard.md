# Frontend Specification — Dashboard Homepage

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 2.4
**Last Updated:** 2026-06-26
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Release:** v6.3
**EPIC:** EPIC-03
**Design Source (v2.4):** docs/design/2026-06-26__release-v6.3/morning-briefing-progressive-disclosure/ux_spec.md
**Design Source (v2.3):** docs/design/2026-06-24__release-v6.2/ai-daily-briefing-card/ux_spec.md
**Design Source (v2.2):** docs/design/2026-06-22__release-v6.1/gate-proximity-indicator/ux_spec.md
**Design Source (v2.1):** docs/design/2026-06-19__release-v6.0/morning-briefing/ux_spec.md
**Design Source (v2.0):** docs/design/2026-03-06__release-v1.9/dashboard-home/ux_spec.md
**Confirmed by:** Head of Specs Team — 2026-06-26

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

### Section Header

Label: **"Trader's Morning Briefing"** — left-aligned, secondary text weight. Not a prominent heading.

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

## 5. AI Daily Briefing Card (v6.2 — ST-07)

**Design source:** `docs/design/2026-06-24__release-v6.2/ai-daily-briefing-card/ux_spec.md`
**Story:** ST-07 (BLG-FEAT-50)

A full-width card placed below the session-summary cards (§4) and above the Gate Progress Indicator strip (§6). The card synthesises trailing stop alerts, rebalance exits, regime status, and new entries into a plain-English action plan.

### Placement

Full-width card spanning the content area. Does not replace or modify any existing section.

### Card Header

| Element | Position | Spec |
|---------|----------|------|
| Title | Left | "Today's Briefing" |
| Timestamp | Centre-right | "Generated HH:MM" (muted, 12px) |
| Regenerate button | Right | Secondary/outlined style; disabled during load |

### Advisory Label

Below header bar, above body:
- Amber badge "AI Advisory" (`#D97706` background, white text)
- Inline static text: "All actions require your confirmation" (muted italic, 12px)
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
| Gate not met | `{closed_trades}/20 trades` + `(PT-04/SI-02 gate)` muted sub-label + amber progress bar |
| Gate met | `Gate cleared ✓` in green + `(PT-04/SI-02 gate)` muted sub-label + full green progress bar |
| Loading | Single-line skeleton placeholder |
| Error | Strip hidden silently — gate-metrics failure must not affect Dashboard primary content |

**Progress bar:** 4px height, full content width. Fill proportional to `closed_trades / gate_threshold`. Amber while in progress; green when `gate_met = true`.

**Threshold:** sourced from `gate_threshold` field in API response — not hardcoded client-side.

**Interaction:** Display-only. No click, no navigation. Refreshes on page load (no polling).

---

## 7. States

| State | Behaviour |
|-------|-----------|
| Page loading | Skeleton cards for all 5 (loading animation) |
| All loaded | All 5 cards render with live data |
| Individual card error | Card shows error indicator (“Unable to load”); other cards render normally |
| All endpoints failed | Full page error with “Retry” button |

Individual card failure must not break other cards. Each card fetches its data independently (or receives it from a composite endpoint that returns partial results).

---

## 8. Navigation Targets

| Card | Click navigates to |
|------|--------------------|
| Open Positions | `/positions` |
| Portfolio Heat | `/risk` |
| In Grace Today | `/risk` |
| Signal Status | `/signals` |
| Recent Activity | `/trades` |

Cards are fully clickable (entire card surface is the click target). Visual affordance: subtle hover state (border highlight or shadow lift).

---

## 9. Change Log

| Version | Date | Change |
|---------|------|--------|
| 2.4 | 2026-06-26 | v6.3 design gate — §5 progressive disclosure added (ST-12, BLG-FE-80): AI Daily Briefing Card sections (Market Context, Suggested Actions) are individually collapsible; section header rows with ChevronDown/Right toggle; localStorage key ai-briefing-collapse-state-v1 persists state across reloads; default all expanded; §13 advisory label remains non-dismissible and always visible; Playwright test SC-BRIEF-01 required. Design source: morning-briefing-progressive-disclosure/ux_spec.md. Approved: Product Owner 2026-06-26. Head of Specs Team confirmed. |
| 2.3 | 2026-06-24 | v6.2 design gate — §5 AI Daily Briefing Card added (ST-07, BLG-FEAT-50): full-width card below session-summary cards; Regenerate button calls POST /ai/daily-briefing; summary paragraph + ordered action list with type chips (EXIT/ENTER/MONITOR/HOLD); advisory label non-dismissible; §13 compliant display-only; advisory=true verified client-side. Sections renumbered (old §5 Gate Progress→§6, §6 States→§7, §7 Navigation→§8, §8 Change Log→§9). Design source: ai-daily-briefing-card/ux_spec.md. Approved: Product Owner 2026-06-24. Head of Specs Team confirmed. |
| 2.2 | 2026-06-22 | v6.1 design gate — §5 Gate Progress Indicator added (ST-07, BLG-FE-78): compact full-width strip below session-summary cards showing closed-trade count vs 20-trade PT-04/SI-02 gate threshold; uses existing GET /portfolio/gate-metrics endpoint; display-only; error hidden silently. Sections renumbered (old §5→§6, §6→§7, §7→§8). Design source: gate-proximity-indicator/ux_spec.md. Approved: Product Owner 2026-06-22. Head of Specs Team confirmed. |
| 2.1 | 2026-06-19 | v6.0 design gate — §1A Morning Briefing Section added: new section at top of DashboardHome above existing cards; 5 intelligence cards (Screener Hits, Positions to Act On, Red Flags, Earnings Alert, Compliance); horizontal desktop layout, vertical mobile stack; per-card loading/error/empty state behaviour; Compliance card colour-coded by score. Design source: morning-briefing/ux_spec.md. Approved: Product Owner 2026-06-19. Head of Specs Team confirmed. |
| 2.0 | 2026-03-06 | Full rewrite for v1.9 EPIC-03 (ST-05). Dashboard Homepage session summary with 5 data cards. Governance header upgraded to Class 1 compliant format. Design source: docs/design/2026-03-06__release-v1.9/dashboard-home/ux_spec.md. |
| 1.0 | 2026-02-18 | Initial version (pre-governance, general portfolio overview). |
