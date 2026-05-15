**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.1
**Cycle:** 2026-05-09__release-v3.3
**Story:** ST-07 (EPIC-02 — IT-03 Arc 3)
**Approved by:** Product Owner
**Approved date:** 2026-05-09
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# UX Spec — Stop Management Workflow (ATR Trail Stop)

## 1. Context

IT-03 introduces a guided stop-management interaction for positions in the PROFITABLE or EXIT ZONE state. The system calculates an ATR-based trail stop suggestion and presents it to the user. The user must explicitly confirm before the stop is updated. No automated action occurs.

§13 constraint: System presents the calculation and a confirmation button. Human confirms. System records the updated stop only after explicit user action.

---

## 2. Trigger Condition

"Trail Stop" action button is shown in the Positions Table View Actions column for a position when ALL of the following are true:
- `position_state` is `PROFITABLE` or `EXIT ZONE`
- `current_stop` (from position record) is non-null

When `current_stop` is null: "Trail Stop" button is shown but **disabled**, with tooltip: "No current stop set. Add a stop to use trail management."

When `position_state` is GRACE, LOSING, or UNKNOWN: "Trail Stop" button is **not shown** (hidden, not disabled).

---

## 3. Table View Integration

"Trail Stop" button added to the Actions column, after "Exit" and before "View Journal":

```
Actions: [Exit]  [Trail Stop]  [View Journal]
```

Button style: secondary (outlined), not primary. Label: "Trail Stop".

---

## 4. Trail Stop Modal

Clicking "Trail Stop" (enabled) opens a modal overlay. Modal is non-destructive by default — no change occurs until the user clicks the confirmation button.

### 4.1 Modal Header

- Title: "Trail Stop — {TICKER}"
- Subtitle: "ATR-based stop trail calculation" (static)
- Close (✕) button top-right

### 4.2 Modal Body

Three data rows in a structured layout:

```
  Current Stop       £2.10 / $2.10
  ATR Trail Stop     £2.34 / $2.34    ▲ Raise by £0.24
  Trail Difference   +£0.24  (+0.6R)
```

| Row | Source field | Format |
|-----|-------------|--------|
| Current Stop | `current_stop` from `GET /positions/{id}/stop-trail` | Native currency, 2dp |
| ATR Trail Stop | `atr_trail_stop` | Native currency, 2dp |
| Raise by | `trail_difference` | "+£X.XX" (positive) or "−£X.XX" (negative, amber colour) |
| Trail in R | `trail_r_terms` | "+X.XR" format; e.g. "+0.6R" |

Note on negative trail difference: If the ATR trail stop is below the current stop (unusual but possible in high-volatility conditions), the "Raise by" shows a negative value in amber and the Confirmation Button copy changes to "Lower stop to {atr_trail_stop}" — making the direction explicit. No automated decision about whether to apply is made.

### 4.3 Calculation Footnote

Static text below the data rows:
> "ATR trail stop = current price − (ATR × 2.0). ATR period: 14 days. Multiplier per strategy rules."

This is display-only — no interactive controls. The multiplier is defined by strategy_rules.md.

### 4.4 Confirmation Button

Primary button:
> "Update stop to {atr_trail_stop}"

Example: "Update stop to £2.34"

On click:
1. Button enters loading state (spinner; disabled)
2. `PATCH /positions/{id}` called with new `stop_price = atr_trail_stop`
3. On success: modal closes; position row updates with new stop; success toast: "Stop updated to {atr_trail_stop}"
4. On error: error message inline in modal below button; "Try again" available; modal stays open

### 4.5 Cancel / Dismiss

- "Cancel" text link below the Confirmation Button
- Clicking "Cancel" or ✕ closes the modal; no change is made
- Escape key dismisses the modal

---

## 5. States

| State | Display |
|-------|---------|
| Loading trail data | Modal opens with skeleton rows while `GET /positions/{id}/stop-trail` is in flight |
| Data loaded | Display as described in §4.2 |
| Confirming (in-flight PUT) | Confirmation button: spinner + disabled; Cancel hidden during in-flight |
| Success | Modal closes; toast notification |
| Error (trail fetch) | Modal body: "Unable to load trail calculation. Please try again." + Retry button |
| Error (stop update) | Inline error below confirmation button; modal stays open |
| Null current_stop | Button disabled in table; modal not openable |

---

## 6. Accessibility

- Modal uses `role="dialog"` and `aria-modal="true"`
- Focus is trapped inside modal while open
- Focus returns to "Trail Stop" button on close
- Escape key closes modal
- Data rows: `<dl>` / `<dt>` / `<dd>` semantic structure for screen reader readability
- Confirmation button: descriptive label includes the target stop price

---

## 7. Responsive

- Modal: max-width 480px; full-width on narrow screens
- Data rows: stack vertically on mobile
- Actions: confirmation button full-width on mobile

---

## 8. Design Decisions

| Decision | Rationale |
|----------|-----------|
| Button hidden for GRACE/LOSING/UNKNOWN | Trail stop is only meaningful for profitable positions with an established move |
| Button disabled (not hidden) for null stop | Preserves discoverability; tooltip explains the missing prerequisite |
| Negative trail shown in amber, not blocked | Edge case should be surfaced to user; they confirm or cancel |
| §13 — explicit confirmation button | Human-in-the-loop required for any stop change |
| No multiplier control in UI | Strategy rules govern multiplier; UI does not expose strategy configuration |
| Success toast after close | Confirms action without keeping modal open |

---

## Known Deviations

| ID | Description | Canonical requirement | Priority | Target resolution | Owner | Backlog reference |
|----|-------------|----------------------|----------|-------------------|-------|------------------|
| DEV-v3.4-01 | ✅ RESOLVED v3.5 (ST-08) — §4.4 updated to document `PATCH /positions/{id}`. PATCH is the correct HTTP verb for partial field updates; implementation was correct; spec was corrected to match. | §4.4: `PUT /positions/{id}` called with new `stop_price = atr_trail_stop` | P3 | ✅ Resolved v3.5 | Head of UX & Design | BLG-SPEC-30 |
