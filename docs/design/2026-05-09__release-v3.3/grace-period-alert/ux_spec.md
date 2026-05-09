**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Cycle:** 2026-05-09__release-v3.3
**Story:** ST-05 (EPIC-02 — IT-02 Arc 3)
**Approved by:** Product Owner
**Approved date:** 2026-05-09
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# UX Spec — Grace Period Decision Support Alert

## 1. Context

IT-02 surfaces a structured decision prompt when a position enters the final phase of its grace period (day 8 or later, of a 10-day window). The alert displays the original trade plan context alongside current position state, prompting the user to review their thesis and decide whether to stay in, add a stop, or exit.

§13 constraint: The system presents information and prompts review. No automated recommendation is generated. Human decides — system records nothing automatically.

---

## 2. Trigger Condition

Alert is shown when:
- At least one open position has `position_state = 'GRACE'` AND `days_in_state ≥ 8`

Source endpoint: `GET /positions/grace-period-alerts`

Alert is hidden (not rendered) when no qualifying positions exist.

---

## 3. Placement

### 3.1 Positions Page

Alert card(s) appear in a dedicated **Alert Zone** at the top of the Positions page, above the View Switcher. The Alert Zone is a visually distinct region (light amber background, left border in amber/orange, `#FEF3C7` background with `#D97706` left border, 4px width).

One alert card per qualifying position. If multiple positions qualify, cards stack vertically within the Alert Zone.

### 3.2 Other Pages

The alert is scoped to the Positions page only. No global banner on other pages.

---

## 4. Alert Card Layout

```
┌────────────────────────────────────────────────────────┐
│ ⚠  Grace Period Alert — TICKER  [Day 8 of 10]    [✕]  │
│                                                         │
│ Your grace period ends in 2 trading days. Review your  │
│ original thesis before the window closes.               │
│                                                         │
│  Thesis:      "Strong momentum breakout above 50d MA"   │
│  Entry zone:  220p – 225p                               │
│  Stop:        210p                                       │
│  R-target:    240p (1.5R)                               │
│                                                         │
│  [View Trade Plan →]                                    │
└────────────────────────────────────────────────────────┘
```

### 4.1 Card Header

- Icon: ⚠ (amber warning icon)
- Label: "Grace Period Alert — {TICKER}"
- Sub-label: "Day {days_in_state} of 10" — badge or inline text
- Dismiss button: ✕ icon, top-right corner, `aria-label="Dismiss grace period alert for {TICKER}"`

### 4.2 Body Text

One line of contextual guidance (static, not AI-generated):
> "Your grace period ends in {10 - days_in_state} trading day(s). Review your original thesis before the window closes."

When `days_in_state = 10`:
> "Grace period has ended. Your position will transition to LOSING or PROFITABLE on next refresh."

### 4.3 Trade Plan Context Block

Displayed when `trade_plan_id` is present on the alert response. Fields shown:

| Label | Source field | Format |
|-------|-------------|--------|
| Thesis | `trade_plan_summary.thesis_excerpt` | First 120 chars; truncated with "…" if longer |
| Entry zone | `trade_plan_summary.entry_zone` | Native currency |
| Stop | `trade_plan_summary.stop_level` | Native currency; "—" if null |
| R-target | `trade_plan_summary.r_target` | Price + R notation (e.g. "240p (1.5R)"); "—" if null |

When `trade_plan_id` is null: display single line "No trade plan linked. Consider adding a plan for context." No context block shown.

### 4.4 Footer Action

- "View Trade Plan →" — navigates to `/trade-plans/{trade_plan_id}` — only shown when `trade_plan_id` is present
- Styled as a text link (not a button); no destructive implication

---

## 5. Dismiss Behaviour

- Dismiss is per-position per-session (localStorage key: `grace_alert_dismissed_{position_id}`)
- Dismissed alerts do not reappear on page reload within the same browser session
- Alert reappears on next visit (no expiry; user may re-dismiss)
- If a new position enters GRACE ≥ day 8, its alert is shown regardless of other dismissed alerts

---

## 6. States

| State | Display |
|-------|---------|
| No qualifying positions | Alert Zone not rendered (zero height, no visual gap) |
| One qualifying position | Single card in Alert Zone |
| Multiple qualifying positions | Cards stacked vertically; each card independently dismissible |
| All dismissed | Alert Zone collapses (zero height) |
| Trade plan data loading | Skeleton placeholder for context block (200ms delay before skeleton appears) |
| Trade plan load error | Context block replaced with "Trade plan details unavailable." No disruption to dismiss or navigation |

---

## 7. Accessibility

- Alert Zone has `role="alert"` and `aria-live="polite"` so screen readers announce new alerts on page load
- Dismiss button: `aria-label="Dismiss grace period alert for {TICKER}"`
- Card is keyboard-navigable (Tab to card → Tab to "View Trade Plan" → Tab to Dismiss)
- Not modal — does not trap focus

---

## 8. Design Decisions

| Decision | Rationale |
|----------|-----------|
| Amber/warning colour, not red | Alert is advisory — red would imply an error or loss |
| Top of page, above view switcher | Most visible position; user sees it before viewing positions |
| Per-session localStorage dismiss | No backend persistence needed; keeps backend simple; auto-resets on next session naturally |
| Trade plan context inline | Reduces navigation friction — user sees thesis without leaving the page |
| No automated recommendation | §13 compliance — system prompts review, human decides action |
