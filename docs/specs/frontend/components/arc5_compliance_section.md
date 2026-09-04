**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.1.0
**Last Updated:** 2026-09-04 (v9.1 ST-13 — Known Deviations: Card 3 text-format/null-display divergence documented, BLG-FE-172)
**Story:** ST-10 (EPIC-03, v4.1) — BLG-FE-48
**§13 Compliance:** Confirmed — display-only component. No automated recommendation generated.
**API contract:** docs/specs/api_contracts/arc5_compliance_analytics.md
**Component:** src/components/analytics/Arc5ComplianceSection.js
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Arc5ComplianceSection — Component Specification

## Purpose

`Arc5ComplianceSection` is a self-contained display component that renders Arc 5 signal compliance statistics on the Performance Analytics page. It fetches its own data from `GET /analytics/arc5-compliance` and displays four stat cards in a responsive grid.

This component is **display-only** — it presents compliance metrics for human review and makes no automated recommendations or decisions.

---

## Component Interface

```jsx
<Arc5ComplianceSection />
```

**Props:** None. The component fetches its own data via internal API call to `GET /analytics/arc5-compliance`.

**Location:** `src/components/analytics/Arc5ComplianceSection.js`

---

## Data Source

| Endpoint | `GET /analytics/arc5-compliance` |
|----------|----------------------------------|
| Contract | `docs/specs/api_contracts/arc5_compliance_analytics.md` |
| Polling | On mount only (no auto-refresh) |
| Auth | X-API-Key forwarded from app context |

---

## Rendering Conditions

### Loading state

When the API request is pending (`isLoading === true`):

- Render a skeleton placeholder in place of each stat card
- Four skeleton blocks matching the stat card grid dimensions
- No error or empty state displayed while loading

### Error state

When the API request returns an error (`isError === true` or non-2xx response):

- Display: `"Unable to load"` in the section body
- No stack trace or technical detail exposed to user
- Retry is not automatically triggered; user must refresh page

### Data state

When API returns a successful response:

- Render four stat cards in a responsive grid (see layout below)
- All values sourced directly from API response — no client-side calculations

### Empty / zero state

When API returns data but all fields are null or zero, each card displays its null display value (see card definitions below). No "no data" empty state.

---

## Stat Card Layout

Four cards rendered in a responsive CSS grid:

| Breakpoint | Columns |
|------------|---------|
| Mobile (default) | 1 column |
| Small (sm) | 2 columns |
| Large (lg) | 4 columns |

Grid class example: `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4`

---

## Stat Cards

### Card 1 — Red Flag Events/Week

| Property | Value |
|----------|-------|
| Label | `"Red Flag Events/Week"` |
| Source field | `data.events_per_week` |
| Format | Float, 1 decimal place (e.g. `"2.3"`) |
| Null display | `"—"` |

### Card 2 — Override Rate

| Property | Value |
|----------|-------|
| Label | `"Override Rate"` |
| Source field | `data.override_rate` |
| Format | Percentage, 1 decimal place (e.g. `"14.3%"`) |
| Null display | `"—"` |

### Card 3 — Top Rule Breach

| Property | Value |
|----------|-------|
| Label | `"Top Rule Breach"` |
| Source field | `data.top_rule_breach` |
| Format | Plain text rule type slug (e.g. `"regime_gate"`) |
| Null display | `"None"` |

### Card 4 — Trade Plan Adherence

| Property | Value |
|----------|-------|
| Label | `"Trade Plan Adherence"` |
| Source field | `data.trade_plan_adherence_rate` |
| Format | Percentage, 1 decimal place (e.g. `"72.5%"`) |
| Null display | `"—"` |

---

## Section Header

- Heading text: **"Arc 5 Signal Compliance"**
- Style: consistent with other analytics section headers
- No collapsible toggle (this component renders inline; the Reports page has a collapsible wrapper — see `docs/specs/frontend/pages/reports.md`)

---

## §13 Compliance

This component is **§13 compliant — display-only**:

- All four stat cards display raw data from the API response
- No automated recommendation, threshold comparison, or action is generated
- The human reviews the displayed statistics and makes all decisions independently
- There is no colour-coding or severity indicator that could constitute a recommendation

---

## Known Deviations

| Field | Detail |
|-------|--------|
| **Deviation description** | Card 3 ("Top Rule Breach") renders `top_rule_breach` with underscores replaced by spaces (e.g. `"regime gate"`) and renders `"—"` when the value is null. |
| **Canonical requirement** | This section's Card 3 table states: Format = "Plain text rule type slug (e.g. `"regime_gate"`)"; Null display = `"None"`. |
| **Priority** | P3 |
| **Target resolution release** | v9.2 |
| **Owner** | Frontend Specifications & UX Documentation Owner |
| **Backlog reference** | BLG-FE-172 |

Found while authoring Playwright coverage for this card (v9.1 ST-13). No functional/data impact — display-text-only divergence between the spec's originally-stated slug/`"None"` intent and the component's actual (and already user-visible, tested) `fmtText` behaviour, which matches the null-display convention used by the component's other three cards.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.1.0 | 2026-09-04 | Known Deviations: documented Card 3 text-format/null-display divergence from implementation — v9.1 ST-13, BLG-FE-172. No behavioural change to this document's own requirements. |
| 1.0.0 | 2026-05-27 | Initial specification — ST-10 (EPIC-03, v4.1), BLG-FE-48. Formalises Arc5ComplianceSection shipped in v4.0 (ST-01). Component props, rendering conditions, stat card layout, data mapping documented. |
