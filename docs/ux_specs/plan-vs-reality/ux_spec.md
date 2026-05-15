**Owner:** Head of UX & Design
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-15
**Cycle:** 2026-05-15__release-v3.5
**Story:** ST-06 — PO-01 Frontend: Plan vs Reality Comparison View
**Sign-off:** Head of UX & Design — 2026-05-15 (design gate v3.5)
**Product Owner approval:** Product Owner — 2026-05-15

---

# UX Spec — Plan vs Reality Comparison View (PO-01)

## 1. Purpose

Surface a structured comparison of trade plan vs actual outcome for closed trades that have a linked trade plan. Rendered as a section within the expandable trade detail row in Trade History. Helps users evaluate how closely their execution matched their pre-trade thesis.

---

## 2. Placement

**Location:** Trade History page — within the Expandable Journal Row, as a 5th section appended after "Strategy Tags".

**Section label:** "Plan vs Reality"

**Visibility rules:**
- Rendered only when the trade is **closed** AND `GET /trades/{id}/plan-vs-reality` returns HTTP 200 with a plan vs reality record.
- Hidden (section not rendered) when `GET /trades/{id}/plan-vs-reality` returns 404 — no trade plan exists for this trade.
- Hidden when `GET /trades/{id}/plan-vs-reality` returns 200 with `{"status": "trade_open"}` — defensive guard.
- When hidden: no placeholder, no "no plan" message, no empty section header visible.

**Lazy loading:** The `GET /trades/{id}/plan-vs-reality` call is made only when the user expands a trade row, not on page load.

---

## 3. Component Layout

The `PlanVsReality` component renders as a card section with a left accent border (blue, `#2563EB`) to distinguish it from Entry Analysis, Exit Reflection, and Strategy Tags sections.

### 3.1 Section Header

- Label: **"Plan vs Reality"**
- No collapse/expand toggle — always visible when section is rendered

### 3.2 Comparison Fields

Four comparison rows, each with a label, planned value (muted), and actual value (bold):

#### Entry Timing Accuracy

| Element | Content |
|---------|---------|
| Label | "Entry Timing" |
| Planned | "Planned zone: {entry_zone_description}" (or "No entry zone recorded" if null) |
| Actual | "Actual entry: {actual_entry_price} ({entry_timing_label})" |
| Entry timing label | `On Time` (green pill) / `Early` (amber pill) / `Late` (amber pill) / `N/A` (grey, no entry zone) |

`entry_timing_label` is backend-calculated and returned by `GET /trades/{id}/plan-vs-reality`.

#### R Achieved vs R Target

| Element | Content |
|---------|---------|
| Label | "R Achieved" |
| Planned | "Target: {r_target}R" (or "No R target set" if null) |
| Actual | "{r_achieved}R" |
| Colour | Green if `r_achieved ≥ r_target`; amber if `r_achieved ≥ r_target × 0.8`; red if `r_achieved < r_target × 0.8` |
| Null handling | If `r_target` is null: display "—" in planned; display actual R without colour coding |

#### Exit Alignment

| Element | Content |
|---------|---------|
| Label | "Exit Alignment" |
| Planned | "Planned: {planned_exit_conditions}" (or "No exit conditions recorded") |
| Actual | "Actual: {actual_exit_reason}" |
| Alignment badge | `Matched` (green) / `Partially Matched` (amber) / `Diverged` (red) |

`alignment_label` is backend-calculated.

#### Lifecycle State at Exit

| Element | Content |
|---------|---------|
| Label | "State at Exit" |
| Value | Lifecycle state badge using the same badge design as the Positions page state badge (`positions.md §Position Lifecycle State Badge`) |
| Source | `lifecycle_state_at_exit` from `GET /trades/{id}/plan-vs-reality` |
| Null handling | Display "UNKNOWN" badge if state is null |

---

## 4. Loading State

When the row is expanding and the API call is in flight:
- Show a single-line skeleton placeholder for the "Plan vs Reality" section
- Section label visible; content area shows skeleton (2 lines, muted)

---

## 5. Error State

If `GET /trades/{id}/plan-vs-reality` returns a network error or 5xx:
- Do not show the section (treat as hidden)
- No error message surfaced in this section
- Other sections (Entry Analysis, Exit Reflection, Strategy Tags) unaffected

---

## 6. Null / Partial Data Handling

- If any individual comparison field is null (e.g. no R target recorded): display "—" in that row's planned value; show actual value without comparative colour coding.
- Component never displays partially blank layout — if the full record is absent (404), the section is hidden entirely.
- Do not display placeholder text like "No comparison data available" — silence is the correct treatment when data is absent.

---

## 7. API Dependency

| Endpoint | Purpose |
|----------|---------|
| `GET /trades/{id}/plan-vs-reality` | Returns plan vs reality comparison record for a closed trade. 404 when no trade plan exists. 200 with `{"status": "trade_open"}` for open trades. |

---

## 8. Design References

- State badge design: reuse from `docs/specs/frontend/pages/positions.md §Position Lifecycle State Badge`
- Colour scale (R colouring): green `#16A34A`, amber `#D97706`, red `#DC2626`
- Card accent border: blue `#2563EB` (4px left border, matches Alert Zone border weight)

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-15 | Initial design — v3.5 design gate. Head of UX & Design approved. Product Owner approved 2026-05-15. |
