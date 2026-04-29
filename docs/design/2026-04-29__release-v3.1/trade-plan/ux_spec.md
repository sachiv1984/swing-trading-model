**Version:** 1.0
**Date:** 2026-04-29
**Author:** Head of UX & Design
**Approved by:** Product Owner — 2026-04-29
**Story:** ST-03 — Trade Plan frontend: creation flow and detail view
**Design gate:** 2026-04-29__release-v3.1

---

# UX Decision Record — Trade Plan Creation Flow & Detail View (ST-03)

## Purpose

The Trade Plan is a structured pre-entry document the user fills out before entering a trade. It captures setup thesis, entry rationale, regime context, R target, early exit conditions, and confirmation criteria. A checklist enforces minimum diligence before the plan is considered complete.

This artefact defines: entry points, form pattern, detail view placement, and checklist behaviour.

---

## Entry Points

**Decision:** Two entry points — from the Positions page (Table View) and from the Watchlist page.

### Entry Point 1 — Positions Table View

- A **"Plan"** button is added to the Table View Actions column for each open position.
- The button label is **"Plan"** (short form, space-constrained).
- If a Trade Plan already exists for this position: button label changes to **"View Plan"** (indicates an existing plan).
- Entry point rationale: trade plan may be created after position entry (e.g., for documentation of a plan that existed mentally).

### Entry Point 2 — Watchlist Table

- A **"Plan"** button is added to the Watchlist Table Actions column (alongside the existing "Add to Position" and "Remove" controls).
- Behaviour: opens the trade plan creation form pre-populated with the ticker symbol and market from the watchlist entry.
- Since `position_id` is nullable in the Trade Plan schema, a pre-position plan is valid.
- Entry point rationale: users planning a trade before entry should document their thesis before committing capital.

---

## Form Pattern — Slide-In Drawer (Right Panel)

**Decision:** Trade Plan creation and editing uses a right-side slide-in drawer, not a full modal or page navigation.

- Rationale: the user may want to see the positions/watchlist context while writing their plan. A drawer keeps the underlying page visible (partially) rather than hiding it behind a modal overlay.
- Drawer width: 480px on desktop; full-width on mobile.
- The drawer pushes the underlying page content left on desktop (push pattern); on mobile it overlays.
- The drawer closes via an **"✕"** button in the top-right corner, or by pressing Escape.
- Unsaved changes: if the user attempts to close with unsaved changes, a confirmation prompt appears inline within the drawer footer: `"Discard changes?"` with "Discard" and "Keep editing" buttons.

---

## Form Layout

The form is contained within the slide-in drawer. Fields are displayed as a single vertical stack.

### Pre-Populated Fields (read-only, top of form)

| Field | Source | Display |
|-------|--------|---------|
| Ticker | URL param / watchlist entry | Displayed as a header label above the form |
| Regime Context | Current regime status (from existing signal/regime API) | Read-only text field: "Risk-On" or "Risk-Off". Label: "Market Regime (at time of plan)" |

### User-Editable Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Setup Thesis | Textarea | Yes | Placeholder: "Why does this setup meet your criteria?" Min 1 char. |
| Entry Rationale | Textarea | Yes | Placeholder: "What specific signal or pattern is triggering this plan?" |
| R Target | Numeric input | Yes | Positive decimal. Label: "R Target (reward/risk ratio)". Min value: 0.1. |
| Early Exit Conditions | Textarea | No | Placeholder: "Under what conditions will you exit early?" |
| Confirmation Criteria | Textarea | No | Placeholder: "What must you see before entering?" |

### Pre-Trade Checklist

Displayed below the form fields, above the Save button.

**Label:** "Pre-Trade Checklist"

**Default checklist items (pre-populated, all unchecked):**

1. Ticker appeared in screener results
2. Sector concentration checked
3. News reviewed (no earnings / surprise risk)
4. R target confirmed (≥ 2.0 recommended)
5. Stop level set

Each item: checkbox + label. The user may check/uncheck any item.

**Custom items:** An **"+ Add item"** link below the list allows the user to append a custom checklist item (free-text input, max 100 characters). The custom item is added to `checklist_items` JSON. Up to 10 total items (default 5 + up to 5 custom).

**`checklist_completed` flag:** Set to `true` by the backend when all items in `checklist_items` are checked. The frontend sends the full `checklist_items` array with each item's checked state.

---

## Save Behaviour

- **"Save Plan"** button: primary action, bottom of drawer.
- On save: calls `POST /trade-plans` (new plan) or `PUT /trade-plans/{id}` (edit existing).
- On success: drawer closes; a brief toast notification appears: `"Trade plan saved."` (auto-dismiss 3s).
- On error: inline error message below the Save button: `"Could not save trade plan — please try again."` Drawer stays open.
- Validation: Setup Thesis, Entry Rationale, and R Target are required. Save button is disabled until these three fields are non-empty/non-zero.

---

## Detail View — Position Detail (Trade Plan Section)

**Decision:** The saved Trade Plan is displayed as a collapsible panel on the Position Detail (the modal that opens when clicking "View Journal" or equivalent in the positions table).

### Placement

- Below the journal/notes section, above any compliance data.
- Panel label: **"Trade Plan"**
- Default state: expanded if a trade plan exists; hidden if none.

### Display

- Read-only view of all trade plan fields (no inline editing — user opens the drawer via "Edit Plan" button within the panel).
- **"Edit Plan"** button: top-right of the panel header (pencil icon).
- Fields displayed:
  - Setup Thesis
  - Entry Rationale
  - Regime Context (at time of plan)
  - R Target
  - Early Exit Conditions (if set)
  - Confirmation Criteria (if set)
  - Pre-Trade Checklist (checkbox state, read-only)
- Empty state (no trade plan): a prompt within the panel: `"No trade plan for this position."` + **"Create Plan"** button.

---

## Spec Update Required

New file: `docs/specs/frontend/pages/trade_plan.md` — full spec covering entry points, form, checklist, detail view, and states.
