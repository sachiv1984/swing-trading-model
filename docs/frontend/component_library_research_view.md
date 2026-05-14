**Owner:** Head of Specs Team
**Class:** Reference Document (Class 2)
**Status:** Active
**Last Updated:** 2026-05-14
**Cycle:** 2026-05-14__release-v3.4
**Source:** BLG-FE-31 (ST-11)

---

# Research View Component Library

Catalogue of reusable UI components in the PT-02 research view (`src/pages/Research.js`).
Scope: PT-02 research view components only — not a full application inventory.
Primary use: component reuse reference for Arc 3 frontend stories ST-01/ST-02/ST-03 (EPIC-01).

---

## Components

### SignalBadge

**File:** `src/pages/Research.js:40`
**Type:** Inline component (co-located, not extracted to `/components`)

**Props:**

| Prop | Type | Description |
|------|------|-------------|
| `status` | `string` | Signal status value |

**Variants:**

| Value | Label | Style |
|-------|-------|-------|
| `active` | Active | `bg-emerald-500/20 text-emerald-400 border-emerald-500/30` |
| `watch` | Watch | `bg-amber-500/20 text-amber-400 border-amber-500/30` |
| `no_signal` | No Signal | `bg-slate-700/50 text-slate-400 border-slate-600/30` |
| *(other)* | raw value | slate fallback |

**Reuse candidate for EPIC-01:** Pattern matches the lifecycle state badge requirement (ST-01). Arc 3 GRACE/PROFITABLE/LOSING/EXIT ZONE/UNKNOWN badge should follow the same `inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border` structure with new colour mappings.

---

### HeatValue

**File:** `src/pages/Research.js:54`
**Type:** Inline component (co-located)

**Props:**

| Prop | Type | Description |
|------|------|-------------|
| `value` | `number \| null` | Heat percentage (0–100) |
| `isError` | `bool` | Show N/A if true |

**Colour thresholds:** >25% → red-400, ≥15% → amber-400, <15% → emerald-400.
Displays `—` when value is null, `N/A` when isError is true.

**Reuse candidate for EPIC-01:** Portfolio heat display in concentration limits warning (ST-06 EPIC-02) can adopt this pattern.

---

### PlanStatusBadge

**File:** `src/pages/Research.js:62`
**Type:** Inline component (co-located)

**Props:**

| Prop | Type | Description |
|------|------|-------------|
| `status` | `string` | Trade plan status |

**Variants:**

| Value | Label | Style |
|-------|-------|-------|
| `active` | Active | emerald |
| `draft` | Draft | slate |
| `closed` | Closed | rose |
| *(other)* | raw value | slate fallback |

**Note:** ST-10 (EPIC-03) delivers an extended version of this badge covering all 7 plan states (Draft, Research Pending, Research Complete, Entry Conditions Set, Active, Closed, Abandoned). The extended version will reside in `src/pages/TradePlan.js` or a shared component; consult `docs/frontend/design_system.md` for colour tokens.

---

### Skeleton

**File:** `src/pages/Research.js:76`
**Type:** Inline component (co-located); canonical version available at `src/components/ui/skeleton.js`

**Props:**

| Prop | Type | Description |
|------|------|-------------|
| `className` | `string` | Width/height overrides |

Standard loading placeholder: `h-4 bg-slate-700/50 rounded animate-pulse`. Use the shared `src/components/ui/skeleton.js` in new components rather than the inline version.

---

## Panels

### Price & Signal Panel

**Location:** `src/pages/Research.js:214–275`
**Type:** Inline panel (card section within Research page)

4-column grid:

| Column | Data source | Display |
|--------|-------------|---------|
| Current Price | `r.price` | `$X.XX` or `£X.XX` based on `currencySymbol(ticker)` |
| Price Change | `r.price_change_pct` | `±X.X%` with TrendingUp/TrendingDown icon; emerald if positive, red if negative |
| Momentum Signal | `r.signal.status` | `<SignalBadge>` |
| ATR (14d) | `r.signal.atr` | `$X.XX` or `—` |

Loading state: 4-col Skeleton grid.

---

### Prospective Heat Panel

**Location:** `src/pages/Research.js:277–304`
**Type:** Inline panel

2-column grid using `HeatValue`:

| Column | Data source |
|--------|-------------|
| Current Portfolio Heat | `heatData.current_heat_percent` |
| Prospective Heat (if entered) | `heatData.prospective_heat_percent` |

Data from `GET /portfolio/prospective-heat?ticker=&shares=1&entry_price=&stop_price=`. Enabled only when both `signal.entry_price` and `signal.stop_price` are present and `entry > stop`.

---

### Trade Plan Context Panel

**Location:** `src/pages/Research.js:306–369`
**Type:** Inline panel

Displays the active or draft trade plan for the ticker. Shows: `PlanStatusBadge`, stop level, risk/reward notes (truncated at 100 chars), R target, and `EntryChecklist` (read-only).

**Reuse candidate for EPIC-01:** The trade plan link from the grace-period alert card (ST-02) can navigate to the plan using the same `navigate('/TradePlan?edit=${plan.id}&ticker=${ticker}')` pattern.

---

### News Feed

**Location:** `src/pages/Research.js:371–401`
**Type:** Inline panel

Displays up to 5 news headlines from `r.news_headlines`. Structure per item:

```
<p className="text-sm text-slate-200">{h.headline || h.title}</p>
<p className="text-xs text-slate-500 mt-0.5">{h.source} · {relativeTime(h.published_at)}</p>
```

#### Source Attribution Row

Inline within each news item: `{h.source ? '${h.source} · ' : ''}` + relative time.

#### Freshness Indicator

**Location:** `src/pages/Research.js:201–212` (header meta area)

Displays `Updated {relativeTime(r.updated_at)}` as a `text-xs text-slate-500` span when `r.updated_at` is present. Used as a lightweight data freshness signal for the whole research record.

---

## Utility Functions

### stripUkSuffix

**File:** `src/pages/Research.js:32`

```js
function stripUkSuffix(t) {
  return t?.endsWith(".L") ? t.slice(0, -2) : (t ?? "");
}
```

Strips `.L` suffix from UK ticker symbols for display purposes. Also defined identically in `src/pages/Screener.js` and `src/pages/Watchlist.js` — a shared utility extract is a candidate for a future cleanup sprint.

**Reuse candidate for ST-07 (EPIC-03):** ST-07 uses this utility to strip `.L` from Research page header. The existing definition in Research.js is already in scope.

---

### relativeTime

**File:** `src/pages/Research.js:12`

Converts ISO timestamp to human-readable relative string (e.g. `3h ago`, `2d ago`).

---

### formatMarketCap

**File:** `src/pages/Research.js:24`

Formats large numbers to T/B/M suffix strings (e.g. `$1.2B`). Prepends `$` unconditionally.

---

### currencySymbol

**File:** `src/pages/Research.js:36`

Returns `£` for `.L` tickers, `$` otherwise.

---

## Shared UI Primitives Used

| Component | File | Usage in Research view |
|-----------|------|----------------------|
| `PageHeader` | `src/components/ui/PageHeader.js` | Page title + back button |
| `Button` | `src/components/ui/button.js` | Back button, Retry, Create Trade Plan |
| `EntryChecklist` | `src/components/trades/EntryChecklist.js` | Read-only pre-entry checklist in Trade Plan panel |

---

## Arc 3 EPIC-01 Reuse Summary

| EPIC-01 Story | Recommended reuse |
|---------------|------------------|
| ST-01 — Lifecycle badge | Use `SignalBadge` pattern (same structure, new colour map); add `days_in_state` alongside GRACE state |
| ST-02 — Grace period alert card | Adopt `relativeTime` for `days_in_state` display; use plan navigation pattern from Trade Plan panel |
| ST-03 — Stop management panel | Use `currencySymbol` for stop price display; follow `HeatValue` colour-coding pattern for R-terms |
