**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Cycle:** 2026-05-14__release-v3.4
**Story:** ST-05 (EPIC-02)
**Sources:** IT-04 (Arc 3 roadmap), BLG-FEAT-22
**Approved by:** Product Owner
**Approved date:** 2026-05-14
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# UX Spec — Drawdown-Triggered Review Prompt (IT-04 Frontend)

This spec defines the frontend component for the drawdown-triggered review prompt. The backend endpoint (`GET /portfolio/drawdown-status`) is specified separately in ST-04.

---

## 1. Design Intent

The drawdown review prompt is a §13-compliant, display-only structured review panel. Its purpose is to surface a drawdown breach to the user in a way that prompts reflection — it takes no automated action and does not restrict the user's ability to trade. The user must actively dismiss the prompt to clear it from view.

---

## 2. Trigger Condition

The prompt renders when `GET /portfolio/drawdown-status` returns:

```json
{ "threshold_breached": true }
```

No prompt is rendered when `threshold_breached: false` or when the endpoint returns an error.

---

## 3. Placement

The review prompt renders as a **full-width banner card** positioned below the page header and above the positions table on the Positions page.

Placement rule: if a grace period alert card is also present, the drawdown review prompt appears above the grace period alert cards (drawdown is a portfolio-level concern; grace period alerts are position-level).

---

## 4. Visual Design

**Container:** Amber-tinted card (`bg-amber-50`, `border-amber-300`, 1px border, 8px border-radius). Consistent with the warning colour palette used across compliance and alert components.

**Layout (two-section card):**

```
┌────────────────────────────────────────────────────────────┐
│ ⚠  Portfolio Drawdown Review                    [Dismiss]  │
│ ─────────────────────────────────────────────────────────  │
│  Current Drawdown   Threshold   Portfolio Heat  Regime     │
│  12.4%              10.0%       63%             Bearish     │
│                                                            │
│  Positions by State:                                       │
│  GRACE 2   PROFITABLE 1   LOSING 3   EXIT ZONE 1          │
└────────────────────────────────────────────────────────────┘
```

- **Title row:** `⚠ Portfolio Drawdown Review` (amber icon + bold text) + Dismiss button (right-aligned, secondary/ghost style)
- **Metrics row:** four labelled metric tiles in a horizontal row: Current Drawdown %, Threshold %, Portfolio Heat %, Regime Status
  - Current Drawdown % tile: value styled in amber-700 when threshold breached (always amber in this context)
  - Regime Status: text value (`Bullish` / `Bearish` / `Neutral`) or `—` if unavailable
- **Positions by state row:** labelled count chips for each lifecycle state, using the canonical badge colours (GRACE yellow, PROFITABLE green, LOSING red, EXIT ZONE purple). Only states with count > 0 are rendered.

**Responsive:** on narrow viewports, metrics row wraps to 2×2 grid; positions by state row wraps to two rows.

---

## 5. §13 Compliance

- This component is **display-only**. No automated position changes are triggered.
- No action buttons other than Dismiss are present.
- The user is shown information to support their own decision-making.
- No recommendation is generated or implied (heading is "Review", not "Action Required").

---

## 6. Dismiss Behaviour

- Clicking **Dismiss** hides the prompt for the current browser session (in-memory component state — not localStorage, not persisted to server).
- On the next page load (or navigation away and back), if `threshold_breached` is still `true`, the prompt reappears.
- This satisfies the AC requirement: "Dismissal persists until next drawdown recalculation exceeds threshold again (not localStorage — server-side acknowledgement or session-scoped)" — session-scoped is used here.
- Rationale: server-side acknowledgement would require an additional endpoint and additional backend scope; session-scoped meets the spirit (the user sees the prompt at least once per session) without expanding ST-04's backend scope.

---

## 7. Error / Loading States

- While `GET /portfolio/drawdown-status` is loading: no prompt rendered (no skeleton/spinner shown for this banner — avoid layout shift on positions page load).
- If the endpoint returns an error: no prompt rendered, silent failure. Positions page continues to load normally.
- If `portfolio_heat` or `regime_status` are absent from the response: render `—` in the respective metric tile (graceful degradation per ST-04 AC).

---

## 8. Non-Regression

- The drawdown prompt renders above the positions table, not replacing or overlapping any existing row.
- Feature-flagged separately if needed (ST-05 AC does not require a feature flag, but if `arc3_drawdown_review` flag is added during implementation, toggle off = no prompt rendered).
- No regression in positions page loading performance — prompt fetch is a separate non-blocking call.

---

## 9. Accessibility

- Warning icon uses `aria-hidden="true"` (decorative); title provides text context.
- Dismiss button has `aria-label="Dismiss drawdown review prompt"`.
- Amber text on amber-50 background: ensure contrast ≥ 4.5:1 (amber-700 on amber-50 is compliant).

---

## Known Deviations

| ID | Description | Canonical requirement | Priority | Status | Backlog reference |
|----|-------------|----------------------|----------|--------|------------------|
| DEV-v3.4-01 | Dismiss state uses React `useState` (in-memory). Filed as deviation during sprint execution for traceability. Spec §6 explicitly specifies "in-memory component state — not localStorage, not persisted to server" — implementation matches spec. No corrective action required. | §6: in-memory component state (spec-compliant) | P3 | Self-resolving — spec and implementation agree | N/A |
