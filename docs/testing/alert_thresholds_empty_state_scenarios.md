**Owner:** QA & Testing Owner
**Class:** Class 2
**Status:** Canonical
**Version:** 0.1
**Last Updated:** 2026-03-26
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Sprint Item:** ST-11 — EPIC-04 (v2.3)
**Spec Ref:** docs/specs/frontend/pages/notifications.md §Section 2 v0.3
**Deviation Closed:** DEV-EPIC02-ST04-01

---

# Alert Thresholds Empty State Test Scenarios — ST-11 (ATS)

## Purpose

Test scenarios covering the "Add alert rule" CTA button added to `AlertThresholdsSection` in ST-11, and the inline create form it opens.

**Automated coverage:** SC-ATS-01 through SC-ATS-11 (Playwright) cover non-visual AC — button presence, form opening, selector options, threshold validation (numeric), POST request body, refresh after save, error handling, cancel behaviour, and populated-state regression. See `tests/e2e/alert-thresholds-empty-state.spec.js`.

**SC-ATS-05** (non-numeric threshold validation) is DoQ manual only — the browser coerces `input[type=number]` non-numeric values to `""` at the DOM level, preventing Playwright UI simulation. Code review confirms `validateThreshold('abc')` returns the correct error message.

---

## Visual Scenarios — DoQ Manual Review Required

### SC-ATS-VIS-01 — CTA button styling in empty state

**Precondition:** Navigate to `/notifications/preferences` with no alert rules configured (or mock `/alerts/rules` to return empty array).

**Steps:**
1. Observe the Alert Thresholds section

**Expected:**
- BellPlus icon visible, centred, in muted (slate-600) colour
- "No alert rules configured." heading in white, bold
- "Add an alert rule to receive notifications." body in muted text (slate-400)
- "Add alert rule" button rendered below body text, centred
- Button has cyan-to-violet gradient fill (matches design system primary action style)
- Button text is white and legible

**Evidence method:** Local run or staging.

---

### SC-ATS-VIS-02 — Create form layout

**Precondition:** Empty state visible; click "Add alert rule".

**Steps:**
1. Click "Add alert rule" button
2. Observe the create form that appears below the empty state content

**Expected:**
- Form appears inline below the icon/heading/body block, separated by a top border
- "Alert Type" label and dropdown selector visible
- Threshold label and input visible (default: Stop Loss Approach selected)
- "Leave blank to use the default (5%)." helper text in muted colour
- Save button with cyan-to-violet gradient; Cancel button as ghost style
- Layout is not clipped or overflowing the card boundary

**Evidence method:** Local run or staging.

---

### SC-ATS-VIS-03 — Threshold input hides for non-threshold types

**Precondition:** Create form open.

**Steps:**
1. Change alert type selector to "Grace Period Warning"
2. Observe threshold field
3. Repeat for "Market Regime Change" and "Daily Portfolio Summary"

**Expected:**
- Threshold input and its label are hidden for all three non-configurable types
- Layout remains clean (no empty whitespace gap where the field was)

**Evidence method:** Local run or staging.

---

### SC-ATS-VIS-04 — Threshold validation error styling

**Precondition:** Create form open with "Stop Loss Approach" selected.

**Steps:**
1. Type `0` in the threshold input
2. Observe the input border and error message

**Expected:**
- Input border changes to rose/red accent (`border-rose-500/60`)
- Error message "Threshold must be greater than 0." appears in rose/red text below the input
- Save button is disabled (visually dimmed)
3. Clear the value (leave blank)
4. Helper text "Leave blank to use the default (5%)." reappears in muted colour
5. Save button re-enables

**Evidence method:** Local run or staging.

---

### SC-ATS-VIS-05 — Non-numeric validation (manual only)

**Note:** This scenario cannot be exercised via Playwright because `input[type=number]` coerces non-numeric values at the browser level.

**Precondition:** Create form open with "Stop Loss Approach" selected.

**Steps:**
1. Using browser DevTools console, set the input value to a non-numeric string and dispatch an `input` event, OR manually inspect that `validateThreshold('abc')` returns `"Please enter a valid number."` via code review.

**Expected (code review):**
- `validateThreshold('abc')` → `"Please enter a valid number."`
- If somehow triggered in UI: error message appears below input; Save button disabled

**Evidence method:** Code review (function confirmed correct); DoQ sign-off may record as code-review-verified.

---

### SC-ATS-VIS-06 — Populated state: no regression

**Precondition:** Navigate to `/notifications/preferences` with rules present (default seeded state).

**Steps:**
1. Observe the Alert Thresholds section

**Expected:**
- Rule list renders (Stop Loss Approach with threshold, other types without)
- No "Add alert rule" button visible anywhere in the section
- Edit pencil icon present on Stop Loss Approach row
- No visual regression to spacing, typography, or card border

**Evidence method:** Local run or staging.

---

## Playwright Coverage Summary

| Scenario | Playwright | DoQ Manual |
|----------|-----------|-----------|
| SC-ATS-01 — CTA button present in empty state | Pass | — |
| SC-ATS-02 — CTA opens create form | Pass | — |
| SC-ATS-03 — All 4 types in selector | Pass | — |
| SC-ATS-04a — Threshold input shown for stop_loss | Pass | — |
| SC-ATS-04b — Threshold input hidden for others | Pass | — |
| SC-ATS-05 — Non-numeric validation | Skipped | Required |
| SC-ATS-06 — Value ≤ 0 validation | Pass | — |
| SC-ATS-07 — Value > 50 validation | Pass | — |
| SC-ATS-08 — POST fires with correct body + refresh | Pass | — |
| SC-ATS-09 — API error shows inline message | Pass | — |
| SC-ATS-10 — Cancel closes form, CTA re-appears | Pass | — |
| SC-ATS-11 — Populated state regression | Pass | — |
| SC-ATS-VIS-01 — CTA button styling | — | Required |
| SC-ATS-VIS-02 — Create form layout | — | Required |
| SC-ATS-VIS-03 — Threshold hides for non-threshold types | — | Required |
| SC-ATS-VIS-04 — Validation error styling | — | Required |
| SC-ATS-VIS-05 — Non-numeric validation (manual) | Skipped | Required |
| SC-ATS-VIS-06 — Populated state no regression | — | Required |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-26 | Initial document. ST-11 (BLG-FE-04, v2.3) — Alert Thresholds empty state CTA button + create form scenarios. 11 Playwright + 6 visual manual scenarios. Closes DEV-EPIC02-ST04-01. |
