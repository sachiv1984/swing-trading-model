**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.3.0
**Last Updated:** 2026-09-07 (ST-04, EPIC-02, v9.2 — Card 3 Format/Null display row corrected to match shipped `fmtText` behaviour, resolving the Known Deviations entry, BLG-FE-172); prior — 2026-09-07 (ST-01, EPIC-01, v9.2 — added Low-Trade-Volume Advisory subsection, BLG-FEAT-44); prior — 2026-09-04 (v9.1 ST-13 — Known Deviations: Card 3 text-format/null-display divergence documented, BLG-FE-172)
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
| Format | Rule type slug with underscores replaced by spaces (e.g. `"regime gate"`) |
| Null display | `"—"` (consistent with Cards 1, 2, and 4's null-display convention) |

### Card 4 — Trade Plan Adherence

| Property | Value |
|----------|-------|
| Label | `"Trade Plan Adherence"` |
| Source field | `data.trade_plan_adherence_rate` |
| Format | Percentage, 1 decimal place (e.g. `"72.5%"`) |
| Null display | `"—"` |

---

## Low-Trade-Volume Advisory

**Added:** v1.2.0 (ST-01, EPIC-01, v9.2, BLG-FEAT-44)

**Design source:** `docs/design/2026-09-07__release-v9.2/arc5-low-volume-advisory/decision_record.md`

**Assessment outcome:** Advisory warranted. Source data: `docs/design/2026-09-07__release-v9.2/arc5-low-volume-advisory/assessment.md`.

When `data.total_closed_trades` is a non-null number below **20**, render a static advisory banner beneath the four-card stat grid (inside this component's own container, not a page-level `StandingAlertStack` entry). The banner does not render while loading or on error, and does not render when `total_closed_trades` is `null`/absent (a pre-v1.1.0 API response) — absence of the field is treated as "unknown", not "low volume".

| Property | Value |
|----------|-------|
| Container | `bg-blue-50 border-blue-200 text-blue-800 dark:bg-blue-950 dark:border-blue-800 dark:text-blue-200` (StandingAlert Info tone, reused verbatim as a bespoke inline banner — not the `<StandingAlert>` component itself) |
| Icon | `Info` (lucide-react) |
| Copy | `"Based on {N} closed trade(s) — treat these figures as indicative until more trade history accumulates."` where `{N}` is `data.total_closed_trades` |
| Dismissal | None — static while the condition holds, re-evaluated on each data fetch (no `onDismiss`, no dismiss button — distinct from `StandingAlert`'s manual-dismiss pattern) |
| Threshold | `total_closed_trades < 20` |
| Source field | `data.total_closed_trades` (`docs/specs/api_contracts/arc5_compliance_analytics.md` v1.1.0) |

**Why `total_closed_trades` and not a page-level trade count:** `PerformanceAnalytics.js`'s own period-filtered trade count (`filteredTrades.length`, used for its own separate ≥10-trade page gate) is not a valid proxy — it is scoped to the page's selected date-range filter, while `trade_plan_adherence_rate` (the most volume-sensitive of the four stats) is computed all-time. Reusing the page's filtered count would misrepresent the sample size actually backing the displayed statistics.

**Note:** `events_per_week`, `override_rate`, and the period-scoped `top_rule_breach` use narrower windows (fixed 7 days / `period` param) than `total_closed_trades` (all-time). The advisory is anchored to the all-time count as the most recognisable "trade volume" figure and the direct denominator of the adherence-rate card; it is not a precise confidence statement about the other three cards' own (unexposed) per-window sample sizes.

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

**Resolved — v9.2, ST-04 (EPIC-02), BLG-FE-172:** Card 3's Format/Null display row above previously read "Plain text rule type slug (e.g. `"regime_gate"`)" / `"None"`, diverging from the component's actual (already user-visible, tested) `fmtText` behaviour — underscores replaced by spaces, `"—"` on null. Resolved by updating this section's table to document the implementation as-shipped, rather than changing the component: the shipped behaviour already matches Cards 1/2/4's established null-display convention (`"—"`), and both `tests/e2e/arc5-compliance-section.spec.js` scenarios below already assert it, so no functional or test change was needed — only this document's own requirement text was out of date.

- SC-ARC5-07 (`tests/e2e/arc5-compliance-section.spec.js`) — asserts underscore-to-space formatting
- SC-ARC5-08 (`tests/e2e/arc5-compliance-section.spec.js`) — asserts `"—"` on null

No other deviations open against this spec.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.3.0 | 2026-09-07 | Card 3 ("Top Rule Breach") Format/Null display row corrected to document the shipped `fmtText` behaviour (space-separated slug, `"—"` on null) — ST-04, EPIC-02, v9.2, BLG-FE-172. Resolves the Known Deviations entry opened at v9.1 ST-13; no component or test change required. |
| 1.2.0 | 2026-09-07 | Added Low-Trade-Volume Advisory subsection — ST-01, EPIC-01, v9.2, BLG-FEAT-44. New `total_closed_trades` field (contract v1.1.0) drives a static Info-tone banner below the stat grid when below 20. |
| 1.1.0 | 2026-09-04 | Known Deviations: documented Card 3 text-format/null-display divergence from implementation — v9.1 ST-13, BLG-FE-172. No behavioural change to this document's own requirements. |
| 1.0.0 | 2026-05-27 | Initial specification — ST-10 (EPIC-03, v4.1), BLG-FE-48. Formalises Arc5ComplianceSection shipped in v4.0 (ST-01). Component props, rendering conditions, stat card layout, data mapping documented. |
