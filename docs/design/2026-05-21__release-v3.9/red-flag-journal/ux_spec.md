**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Date:** 2026-05-21
**Approved by:** Product Owner — 2026-05-21
**Cycle:** 2026-05-21__release-v3.9
**Story:** ST-08 (EPIC-03)

---

# UX Spec — Red Flag Journal (ST-08)

## Purpose

The Red Flag Journal is a display-only audit log of instances where the operator deviated from their stated trading strategy — pre-entry rule validation overrides, checklist skips, and stop/drawdown prompt dismissals. Separate from the Trade Journal. Introduces the SI-03 frontend surface.

**§13 Compliance:** Display-only audit log. No automated decisions or recommendations.

---

## Route and Navigation

- Route: `/red-flag-journal`
- Page title: **"Red Flag Journal"**
- Nav group: **Trading** (added after Trade Reflection)
- Nav item label: **"Red Flag Journal"**
- `createPageUrl` key: `"RedFlagJournal"` — must be added to the `createPageUrl` map in `App.js`

---

## Page Layout

### Filter Controls (above event list)

| Control | Type | Options |
|---------|------|---------|
| Event Type | Dropdown | "All types" (default); "Pre-Entry Override"; "Checklist Skipped"; "Stop Prompt Dismissed"; "Drawdown Prompt Dismissed" |
| Ticker | Text input | Free-text; passed as `ticker` query param |
| Date Range | From / To date inputs | ISO date; From → `since` query param |

Filters applied additively (AND). Changing any filter re-fetches from API.

### Event List

Paginated, 20 events per page, most recent first.

Each event row:

| Element | Source | Display |
|---------|--------|---------|
| Icon | `event_type` | ⚠ pre_entry_override; ☑ checklist_skipped; ⏭ stop_prompt_dismissed; ⬇ drawdown_prompt_dismissed |
| Type label | `event_type` | "Pre-Entry Override" / "Checklist Skipped" / "Stop Prompt Dismissed" / "Drawdown Prompt Dismissed" |
| Ticker | `ticker` | Uppercase; `.L` suffix stripped for display (LSE tickers) |
| Context summary | `context` JSON | Short human-readable summary extracted from context (fallback: raw JSON string) |
| Date | `created_at` | Relative time ("2 hours ago"); absolute date shown on hover |

### Pagination Controls

- Previous / Next page buttons
- "Page {N} of {M}" indicator
- "{total} events recorded" count displayed above or below the list

### Empty States

| Condition | Display |
|-----------|---------|
| No events, no active filters | "No strategy deviations recorded yet" + sub-text: "Override events will appear here when you proceed past a strategy gate warning." |
| No events, active filters | "No events match your current filters." + "Clear filters" link |

### Loading State

Skeleton rows (matching event row height) while API request is in flight.

### Error State

"Unable to load Red Flag Journal. Please try again." + Retry button.

---

## API Reference

`GET /portfolio/red-flag-journal?page={n}&page_size=20&event_type={type}&ticker={ticker}&since={date}`

Response: `{ total: int, page: int, page_size: int, items: [...] }`

---

## Playwright Tests

- **SC-RFJ-01**: Page renders with mocked events list (event type label, ticker, date visible)
- **SC-RFJ-02**: Empty state renders when API returns 0 events
- **SC-RFJ-03**: Filter by event_type narrows results in mocked response
