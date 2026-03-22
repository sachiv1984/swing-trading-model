**Owner:** Head of UX & Design
**Status:** Approved
**Approved by:** Product Owner
**Approved date:** 2026-03-22
**Cycle:** 2026-03-21__release-v2.2
**Items:** ST-04
**Frontend spec target:** docs/specs/frontend/pages/notifications.md (update to v0.2)

---

# UX Spec — Alert Threshold Customisation (ST-04)

## 1. Purpose & User Goal

Users need to set per-rule numeric thresholds so that alerts fire at personally meaningful levels rather than a fixed system default. For example, a user may want to be notified when their stop loss is within 3% of price rather than the default 5%.

**User goal:** Configure a custom threshold value on any alert rule that supports it, and see that threshold reflected in the alert list.

---

## 2. Scope

This spec covers:
- Threshold input on the alert rule creation form
- Threshold input on the alert rule edit form
- Threshold display on the alert rule list view

It does not cover:
- Alert scheduling (ST-03 — gating story; must complete before ST-04 is implemented)
- Alert history (ST-05 — separate spec)
- Notification preferences toggles (covered in notifications.md v0.1)

---

## 3. Alert Rules Surface

### 3.1 Placement

Alert threshold customisation is part of the **Alert Rules** management UI. This may be co-located under `/notifications/preferences` as a second section (below the email toggles), or surfaced as a separate `/alerts/rules` route — the engineering team may determine final route placement based on ST-03 outcomes. Both layouts must satisfy these UX requirements.

For the purposes of this spec: the Alert Rules section presents a list of configurable alert rules (one per alert type), each editable inline or via a modal form.

### 3.2 Alert Types Supporting Thresholds

| Alert Type | Threshold Label | Unit | Default | Validation |
|------------|----------------|------|---------|------------|
| Stop Loss Approach | "Notify when within ___ % of stop" | % (positive number) | 5 | Min: 0.1, Max: 50, 1 decimal place |
| Grace Period Warning | No threshold (fixed: days 8–9) | N/A | — | Not editable in this story |
| Market Regime Change | No threshold (event-triggered) | N/A | — | Not editable in this story |
| Daily Portfolio Summary | No threshold | N/A | — | Not editable in this story |

Only **Stop Loss Approach** supports a user-configurable threshold for v2.2. The threshold field is rendered only for applicable types.

---

## 4. Alert Rule Creation / Edit Form

### 4.1 Threshold Input Field

For alert types supporting a threshold (currently: Stop Loss Approach):

```
Label:       "Notify when within"
Input:       Numeric input field (text input, number type)
Unit label:  "%" (suffix, inline with input)
Placeholder: e.g. "5" (the system default)
Help text:   "Leave blank to use the default (5%)."
```

Layout: Threshold input appears directly below the alert type selector / rule type label. It is part of the same card or form row as the other rule fields.

### 4.2 Validation (inline, on submit)

| Condition | Error message |
|-----------|--------------|
| Non-numeric value | "Please enter a valid number." |
| Value ≤ 0 | "Threshold must be greater than 0." |
| Value > 50 | "Threshold cannot exceed 50%." |
| Empty (blank) | Accepted — treated as "use default" |

Errors are displayed inline below the threshold input field. Form does not submit while errors are present.

### 4.3 Default Value Behaviour

- If the user leaves the field blank or clears it: the system default (5% for stop_loss_approach) is applied.
- The placeholder shows the current default value so users know what they are overriding.
- On load of the edit form: pre-fill the input with the existing threshold value (from API), or show the placeholder if the rule uses the default.

### 4.4 Save Behaviour

- Save is part of the alert rule form submission (same button as the rest of the form).
- On success: the rule list view refreshes; the updated threshold is shown in the list.
- On error: display inline error above the save button: "Failed to save alert rule. Please try again."

---

## 5. Alert Rule List View

### 5.1 Threshold Display

For each alert rule in the list, display the threshold value alongside the rule summary:

| Element | Behaviour |
|---------|-----------|
| Threshold badge / label | "Within 5% of stop" (or custom value if set) |
| Placement | Below the alert type name, in muted/secondary text |
| Default indicator | If using the default, label reads "Within 5% of stop (default)" |
| Custom indicator | If custom, label reads "Within N% of stop" (no "(default)" suffix) |

For alert types without a configurable threshold (grace period warning, market regime change, daily portfolio summary): no threshold field or badge is shown.

---

## 6. States

### 6.1 Loading State
Skeleton rows while alert rules load from the API.

### 6.2 Empty State
No alert rules configured:
- Icon (bell with plus)
- Heading: **"No alert rules configured."**
- Body: "Add an alert rule to receive notifications."
- CTA: **"Add alert rule"** button

### 6.3 Error State (list load failure)
Inline error panel: "Unable to load alert rules. Please refresh."

---

## 7. UX Decisions Recorded

| Decision | Rationale |
|----------|-----------|
| Only Stop Loss Approach supports threshold for v2.2 | Grace period (days 8–9) and market regime change (event-based) have no meaningful numeric threshold; daily summary has none. Extensible for future types. |
| Blank = use default | Reduces friction; users who don't need customisation don't need to know or set a default value |
| Inline validation (not submit-time only) | Numeric threshold errors are simple and immediately correctable; inline validation improves usability |
| Threshold shown in list view | Users need to confirm their configuration at a glance without opening the edit form |
| Default indicated with "(default)" suffix | Distinguishes a system default from a user choice; helps users know whether customisation is active |
