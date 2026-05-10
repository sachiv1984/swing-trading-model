**Owner:** Frontend UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-10
**Story:** ST-09 (EPIC-03, v3.3) — BLG-FE-28
**Canonical spec:** docs/specs/frontend/pages/research_view.md
**Provenance spec:** docs/specs/data_provenance/research_view_provenance.md
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# UX Specification — Research View (PT-02)

Formalises the UX design for the Research View shipped in v3.1 (PT-02). All layout and interaction patterns described here reflect the current shipped state.

---

## 1. Layout — Panel Arrangement

The page uses a responsive single-column layout on mobile and a two-column grid on tablet/desktop.

```
┌──────────────────────────────────────────────────────┐
│  PageHeader: "{TICKER} — Research"         [← Back]  │
├──────────────────────────────────────────────────────┤
│  Price Panel (left, wider)  │  Regime Panel (right)  │
├──────────────────────────────────────────────────────┤
│  Signal Panel               │  Screener Panel        │
├──────────────────────────────────────────────────────┤
│  Trade Plan Panel (full width)                       │
├──────────────────────────────────────────────────────┤
│  Earnings Panel             │  Sector/Industry       │
├──────────────────────────────────────────────────────┤
│  Prospective Heat Panel (full width)                 │
├──────────────────────────────────────────────────────┤
│  News Feed (full width)                              │
└──────────────────────────────────────────────────────┘
```

---

## 2. Data Field Hierarchy and Visual Treatment

### 2.1 Price Panel

- **Primary:** Current price — large font (text-2xl or text-3xl), bold
- **Secondary:** Daily change % — medium font with directional colour:
  - Positive: text-green-400
  - Negative: text-red-400
  - Zero/null: text-slate-400
- **Tertiary:** Market cap — small font (text-sm), muted
- **Attribution:** `text-xs text-slate-400` — "Source: Yahoo Finance · Updated {HH:MM}"

### 2.2 Signal Panel

- Panel header: "Signal" (text-sm text-slate-400 uppercase)
- Signal status badge: `rounded-full px-2 py-0.5 text-xs font-semibold`
  - Active: `bg-green-900 text-green-300`
  - Watch: `bg-amber-900 text-amber-300`
  - Others: `bg-slate-700 text-slate-300`
- Grid layout: 2 columns — entry/stop/ATR/R-target displayed as labelled key-value pairs
- Signal date shown beneath badge in muted text

### 2.3 Market Regime Panel

- Regime label badge — centre-aligned, large:
  - Risk On: `bg-green-900 text-green-200`
  - Risk Off: `bg-red-900 text-red-200`
  - Mixed: `bg-amber-900 text-amber-200`
- SPY and FTSE status shown below regime badge as small inline indicators:
  - `SPY ✓` (green) / `SPY ✗` (red)
  - `FTSE ✓` (green) / `FTSE ✗` (red)
- Attribution tooltip: hover over panel → "Source: Live market data"

### 2.4 Trade Plan Panel

- If active plan exists: card with plan status badge, stop level, R/R notes, read-only checklist
- Checklist items: rendered as static indicators (not interactive checkboxes) — checked state shown with checkmark icon
- If no plan: CTA card with button "Create Trade Plan" (primary, links to `/trade-plans/new?ticker={ticker}`)

### 2.5 Earnings Panel

- Days-until count shown as prominent number if ≤ 30 days (amber treatment)
- If > 30 days: standard display
- If null: "No upcoming earnings data" in muted text

### 2.6 News Feed

- List of up to 5 headlines
- Each item:
  - Headline text: truncated to 2 lines with `line-clamp-2`
  - Source + relative time: `text-xs text-slate-400`
  - Entire item is clickable (links to article URL, `target="_blank" rel="noopener"`)
- Empty state: "No recent news" centred in a muted card

---

## 3. Source Attribution Display Format

Per `docs/specs/data_provenance/research_view_provenance.md §2`:

- Attribution line beneath each section header
- Format: `Source: {name} · Updated {HH:MM}` (when timestamp available)
- Without timestamp: `Source: {name}`
- CSS: `text-xs text-slate-400`
- No icon required; icon (e.g. info circle) is optional enhancement

---

## 4. Freshness Indicator

- Trigger: 5 minutes after page load without a re-fetch
- Display: Amber pill at the top of the page or sticky notice: "Data may be stale — click to refresh"
- Click/tap: re-fetches `GET /research/{ticker}` and updates all panels
- Placement: below the page header, above all panels

---

## 5. Empty and Error States

### 5.1 Full-Page Error (GET /research fails with 5xx)

- Full-page error card centred
- Heading: "Unable to load research data"
- Body: "There was a problem fetching data for {TICKER}. Please try again."
- CTA: "Retry" button (triggers re-fetch)
- Back link: "← Back" visible in all error states

### 5.2 Individual Field Null State

- Per §4 of canonical spec — each panel shows its specific null display
- No spinner; null state renders immediately

### 5.3 Loading State

- Skeleton loading: 4 skeleton cards rendered while `GET /research/{ticker}` is in flight
- Skeleton size matches the expected panel sizes
- No spinner component — skeleton only

---

## 6. Interaction Model

| Action | Behaviour |
|--------|-----------|
| Click headline | Opens URL in new tab |
| Click "Create Trade Plan" | Navigate to `/trade-plans/new?ticker={ticker}` |
| Click "← Back" | Navigate to previous page (`history.back()`) |
| Click "Retry" (error state) | Re-fetches research endpoint |
| Click "Refresh" (stale) | Re-fetches research endpoint |
| Click trade plan "Edit" | Navigate to `/trade-plans/{id}/edit` |

---

## Sign-off

- Frontend UX Documentation Owner: Accepted — 2026-05-10 (agent-mediated, v3.3 design gate)

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-10 | Initial creation — ST-09 (EPIC-03, v3.3). Formalises v3.1 PT-02 shipped UX. Panel layout, field hierarchy, attribution format, freshness indicator, error states. |
