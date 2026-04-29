**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.1
**Last Updated:** 2026-04-29
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source:** docs/design/2026-04-29__release-v3.1/trade-plan/ux_spec.md
**API contract:** docs/specs/api_contracts/trade_plan_endpoints.md

---

# trade_plan.md — Trade Plan Feature

**Purpose:** Specifies the Trade Plan creation form, detail view, and entry points. Trade Plan is not a standalone page — it is a slide-in panel (drawer) accessible from the Positions and Watchlist pages, with a read-only detail view embedded in the Position Detail.

---

## 1. Purpose and User Goals

Users should be able to:

- Document a pre-trade thesis before entering a position (from Watchlist)
- Attach a structured plan to an open position (from Positions Table View)
- Review the trade plan alongside the position while it is live
- Work through a pre-trade checklist to enforce minimum diligence

---

## 2. Entry Points

### From Positions Page (Table View)

A **"Plan"** button is added to the Actions column of the Positions Table View.

- When no trade plan exists for the position: label is **"Plan"**
- When a trade plan already exists: label is **"View Plan"**
- Clicking opens the slide-in drawer with the form pre-populated (existing plan) or blank (new plan)

### From Watchlist Page

A **"Plan"** button is added to the Watchlist Table Actions column (between "Add to Position" and "Remove").

- Clicking opens the slide-in drawer pre-populated with the ticker and market from the watchlist entry
- `position_id` is null for pre-position plans — this is a valid state

---

## 3. Slide-In Drawer (Form Pattern)

### Layout

- **Width:** 480px on desktop; full-width on mobile
- **Position:** right edge of viewport; pushes page content left on desktop; overlays on mobile
- **Close:** "✕" button (top-right); Escape key
- **Unsaved changes:** closing with unsaved changes shows an inline confirmation in the drawer footer:
  > "Discard changes?"
  - **"Discard"** — closes drawer without saving
  - **"Keep editing"** — dismisses the confirmation; drawer stays open

### Drawer Header

- Ticker symbol as a prominent label (stripped of `.L` suffix for UK tickers)
- Sub-label: "Trade Plan" (new) or "Edit Trade Plan" (existing)

---

## 4. Form Fields

### Pre-Populated Read-Only Fields

| Field | Source | Notes |
|-------|--------|-------|
| Ticker | Entry point context | Displayed in drawer header, not an editable field |
| Regime Context | Current regime status API | Read-only text: "Risk-On" or "Risk-Off". Label: "Market Regime (at time of plan)" |

### User-Editable Fields

| Field | Type | Required | Placeholder |
|-------|------|----------|-------------|
| Setup Thesis | Textarea | Yes | "Why does this setup meet your criteria?" |
| Entry Rationale | Textarea | Yes | "What specific signal or pattern is triggering this plan?" |
| R Target | Numeric input | Yes | Positive decimal ≥ 0.1. Label: "R Target (reward/risk ratio)" |
| Early Exit Conditions | Textarea | No | "Under what conditions will you exit early?" |
| Confirmation Criteria | Textarea | No | "What must you see before entering?" |

**Validation:** Setup Thesis, Entry Rationale, and R Target are required. Save button is disabled until all three have valid values.

---

## 5. Pre-Trade Checklist

### Display

Positioned below the editable form fields, above the Save button.

**Label:** "Pre-Trade Checklist"

### Default Checklist Items (pre-populated, all unchecked)

1. Ticker appeared in screener results
2. Sector concentration checked
3. News reviewed (no earnings / surprise risk)
4. R target confirmed (≥ 2.0 recommended)
5. Stop level set

Each item: checkbox + label text. User may check/uncheck any item.

### Custom Items

An **"+ Add item"** link below the default list allows adding custom checklist items:
- Free-text input, max 100 characters
- Maximum 10 total items (5 default + up to 5 custom)
- Custom items are appended to the `checklist_items` JSON array

### `checklist_completed` Flag

The backend sets `checklist_completed = true` when all items in `checklist_items` have `checked: true`. The frontend sends the complete `checklist_items` array with each item's checked state on every save.

---

## 6. Save Behaviour

| Action | API Call | Response |
|--------|----------|----------|
| New plan | `POST /trade-plans` | On success: drawer closes; toast "Trade plan saved." (3s auto-dismiss) |
| Edit existing | `PUT /trade-plans/{id}` | Same as above |
| Error | — | Inline error below Save button: "Could not save trade plan — please try again." Drawer stays open. |

---

## 7. Position Detail — Trade Plan Section

The saved Trade Plan is displayed as a collapsible section within the Position Detail view (the detail modal/panel accessible from the Positions Table View).

### Placement

Below the journal/notes section, above any compliance data.

### Panel Header

- Label: **"Trade Plan"**
- "Edit Plan" button: top-right of panel header (pencil icon). Clicking opens the slide-in drawer with the plan pre-populated.
- Collapse/expand chevron

### Default State

- Expanded if a trade plan exists for this position
- Hidden if no trade plan exists (replaced by empty state)

### Read-Only Display

All trade plan fields are shown in read-only mode:

- Setup Thesis
- Entry Rationale
- Market Regime (at time of plan)
- R Target
- Early Exit Conditions (omitted if empty)
- Confirmation Criteria (omitted if empty)
- Pre-Trade Checklist (checkbox state, read-only — checked items shown as ✓, unchecked as ○)

### Empty State (No Trade Plan)

```
"No trade plan for this position."
[Create Plan]  ← primary button
```

---

## 8. API Reference

| Endpoint | Use |
|----------|-----|
| `POST /trade-plans` | Create new trade plan |
| `GET /trade-plans/by-position/{position_id}` | Load trade plan for a position |
| `PUT /trade-plans/{id}` | Update existing trade plan |
| `GET /trade-plans/{id}` | Load trade plan by ID (direct link) |

- Canonical contract: `docs/specs/api_contracts/trade_plan_endpoints.md`

---

## 9. States

### Loading State (Detail View)

While `GET /trade-plans/by-position/{position_id}` is loading: show a skeleton placeholder inside the Trade Plan section.

### Error State (Detail View)

If the trade plan endpoint fails: show inline error within the section: "Unable to load trade plan." No retry button — user may refresh the page.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-04-29 | Initial spec. ST-03 — EPIC-01 (v3.1 Arc 2: Trade Plan Object). Design source: docs/design/2026-04-29__release-v3.1/trade-plan/ux_spec.md. Approved by Product Owner 2026-04-29. Design gate: 2026-04-29__release-v3.1. |
