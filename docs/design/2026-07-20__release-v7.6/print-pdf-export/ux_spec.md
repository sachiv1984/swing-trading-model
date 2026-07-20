**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-20
**Approved by:** Product Owner — 2026-07-20
**Story:** ST-01 — Add print/PDF export action to WeeklyDigest and TradePlan (EPIC-01, BLG-FE-119)
**Cycle:** 2026-07-20__release-v7.6

---

# UX Specification — Print / Export PDF Action

## 1. Context

`BLG-FE-119` asks for a "Print / Export PDF" action on `WeeklyDigest.js` and `TradePlan.js`, legible and correctly formatted without app chrome (nav/sidebar). The backlog scope explicitly permits either a print stylesheet or a server-side PDF-export action.

Reports.md (`docs/specs/frontend/pages/reports.md` §Page Header Controls) already has a **server-side** "Download PDF" pattern (`GET /reports/tax-year?format=pdf&year=YYYY`) for the Tax Year export. That pattern was built for a fixed, pre-formatted financial document with its own backend renderer. It is not reused here.

## 2. Decision

### 2.1 Mechanism: client-side print, not server-side generation

The action is implemented as a **browser print action** (`window.print()`) backed by a print stylesheet (`@media print`), not a new backend PDF-rendering endpoint. Rationale:
- Both target pages are already-rendered on-screen data (a summary table; a read-only plan detail view) — no new data assembly is needed, unlike the Tax Year report's aggregated financial document.
- A print stylesheet works identically for "print to paper" and "print to PDF" (every modern browser's print dialog offers "Save as PDF" as a destination) — it satisfies both the "print-friendly" and "PDF output" halves of the AC with one implementation.
- Avoids two new backend endpoints for an M-effort (~1–2 day) item; no `docs/reference/openapi.yaml` change required.
- Precedent: this pattern is net-new to the codebase (no existing print stylesheet elsewhere) but is the standard low-cost approach for "share this read-only view as a document" requests.

### 2.2 Trigger

Both pages gain a button in the `PageHeader` `actions` slot, styled `variant="outline"` `size="sm"` (consistent with the existing secondary-action buttons on each page — e.g. TradePlan's "Start Trade from Plan" / "Abandon Plan"):

- Label: **"Print / Export PDF"**
- Icon: `Printer` (lucide-react), left of label
- `onClick`: `window.print()`

No loading/generating state is needed — `window.print()` is synchronous from the page's perspective (the browser owns the print dialog).

### 2.3 Placement

| Page | Location | Condition |
|------|----------|-----------|
| `WeeklyDigest.js` | `PageHeader` actions, to the left of the existing "Refresh" button | Always available once digest data has loaded (hidden while `isLoading` or `isError`, matching the existing `DataState` gate on the table) |
| `TradePlan.js` | `PageHeader` actions, alongside "Start Trade from Plan" / "Abandon Plan" / "Back" | Only shown in **detail view** (`editId && existingPlan` — an existing, loaded plan). Not shown on the creation form (`/trade-plans/new`) — printing a half-filled form has no defined use case and is out of scope. |

### 2.4 Print Stylesheet — What Is Hidden

A shared `@media print` rule set (added to the global stylesheet, not per-page) hides:
- The app header/nav bar
- Any sidebar
- The `PageHeader` `actions` slot itself (the print button, Refresh, Start Trade, Abandon, Back — none of these are meaningful on paper)
- Any `DataState` retry affordances, toasts, or loading skeletons

What remains visible:
- `WeeklyDigest.js`: the page title/description text and the full data table (all 8 fields), full width, standard black-on-white print colours (dark theme surface colours are not print-appropriate and are overridden)
- `TradePlan.js`: the page title/description (ticker + market + status badge), and all read-only detail-view content per `trade_plan.md` §7 (core fields, tags, pre-trade checklist read-only state, Setup Quality Score if present) — the Edit/Abandon/Delete/Start Trade action buttons are hidden (§2.3/§2.4 above)

### 2.5 Colour and Legibility on Print

Both pages currently render on a dark theme surface (`bg-slate-900`-family backgrounds, light text). Printing dark backgrounds is both illegible and wastes ink. The print stylesheet forces:
- `background: white` and `color: black` (or near-black, `slate-900`) on the printed root container
- Table borders/dividers switch to a light-grey print-visible border (dark-theme dividers are invisible on white)

This is a global print-stylesheet rule (not scoped to these two pages) so any future page reusing `window.print()` inherits legible output by default.

## 3. §13 Compliance

Display-only, no new automated decision-making, no trade or position-sizing logic. Not applicable.

## 4. States

| State | Behaviour |
|-------|-----------|
| Data not yet loaded / error | Print button hidden (WeeklyDigest) or plan not yet loaded (TradePlan) |
| Data loaded | Print button visible and enabled |
| Clicked | Browser's native print dialog opens (`window.print()`); page behind it is unaffected — no in-app loading/generating state |

## 5. Sign-off

- **Head of UX & Design:** Confirmed — 2026-07-20
- **Product Owner:** Approved — 2026-07-20
