**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Cycle:** 2026-05-14__release-v3.4
**Story:** ST-06 (EPIC-02)
**Sources:** IT-05 (Arc 3 roadmap), DS-03 (sector data, v2.9)
**Approved by:** Product Owner
**Approved date:** 2026-05-14
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# UX Spec — Position Concentration Limits Warning (IT-05 Frontend)

This spec defines the frontend warning component for portfolio position and sector concentration limit breaches. The backend endpoint (`GET /portfolio/concentration-status`) is specified in ST-06 backend AC.

---

## 1. Design Intent

The concentration limits warning is a §13-compliant, display-only indicator. It informs the user when any single position or sector exceeds configurable concentration thresholds. It lists the breaching items to enable informed review — no automated rebalancing or restriction is applied.

---

## 2. Trigger Condition

The warning renders when `GET /portfolio/concentration-status` returns one or more breaching items (positions or sectors exceeding their respective thresholds).

No warning is rendered when all positions and sectors are within thresholds, or when the endpoint returns an error.

---

## 3. Placement

The concentration limits warning renders as a **full-width summary card** below the page header on the Positions page.

Stacking order when multiple warnings are present:
1. Drawdown Review Prompt (portfolio-level, highest severity)
2. Concentration Limits Warning (portfolio-level, structural)
3. Grace Period Alert cards (position-level)

---

## 4. Visual Design

**Container:** Amber-tinted card (`bg-amber-50`, `border-amber-300`, 1px border, 8px border-radius). Consistent with the drawdown review prompt and existing warning components.

**Layout:**

```
┌──────────────────────────────────────────────────────────┐
│ ⚠  Concentration Limits                                  │
│ ────────────────────────────────────────────────────────  │
│  Positions exceeding limit (15% of portfolio heat):      │
│  • NVDA  — 22.1% of heat  (limit: 15%)                  │
│  • TSLA  — 18.4% of heat  (limit: 15%)                  │
│                                                          │
│  Sectors exceeding limit (30% concentration):            │
│  • Technology  — 41.2%   (limit: 30%)                   │
└──────────────────────────────────────────────────────────┘
```

- **Title:** `⚠ Concentration Limits` (amber icon + bold text)
- **Positions section:** shown only when one or more positions breach the single-position threshold. Lists: ticker, heat % of portfolio, limit in parentheses.
- **Sectors section:** shown only when one or more sectors breach the sector concentration threshold AND sector data (DS-03) is available. Lists: sector name, concentration %, limit in parentheses.
- Limit values shown inline with each breaching item (not in a separate section header) so the user can immediately assess magnitude.

**No dismiss button** — the warning persists as long as the breach exists. This is a persistent informational indicator, not a one-time prompt. The user's recourse is to adjust positions or thresholds in Settings.

---

## 5. §13 Compliance

- Display-only. No automated rebalancing or forced position changes.
- No action button other than an optional "Review Settings" link (navigates to Settings → Portfolio Limits — passive navigation).
- The user may choose to take action (reduce a position, adjust a threshold) or proceed with full awareness of the breach.

---

## 6. Graceful Degradation

**Positions without sector data:**
- Included in the single-position heat % calculation normally.
- Excluded from sector concentration calculation — they are not attributed to any sector bucket.
- No warning displayed for these positions in the sector section (cannot calculate sector concentration without sector assignment).
- No error state shown; the sector section simply omits positions without sector data silently.

**Sector section absent:**
- If no positions have DS-03 sector data, the sector section is not rendered (not "no sectors breaching" — entire section omitted).
- If sector data exists but no sector exceeds threshold, sector section is still omitted (only breaching items shown).

**Single-position section absent:**
- If no positions exceed the position threshold, the positions section is not rendered.

**Both absent:**
- If neither section has breaching items, the entire warning card is not rendered (trigger condition returns no breaches).

---

## 7. Error / Loading States

- While `GET /portfolio/concentration-status` is loading: no warning card rendered (no skeleton/spinner — avoid layout shift).
- If the endpoint returns an error: no warning rendered, silent failure. Positions page loads normally.
- If `portfolio_heat_pct` is unavailable for a position: omit that position from both calculations; do not render a partial or `—` value in the warning.

---

## 8. Configurable Thresholds Display

The warning card shows the breaching threshold values inline (e.g. `limit: 15%`). These values come from the `GET /portfolio/concentration-status` response (which reads from settings). This ensures the displayed threshold is always consistent with the user's configured value, not a hardcoded UI default.

---

## 9. Non-Regression

- No regression in positions page layout or existing columns.
- Warning card is appended above the table, not modifying existing components.
- No regression in watchlist or screener views (this component is positions-page-only).

---

## 10. Accessibility

- Warning icon uses `aria-hidden="true"` (decorative); title provides text context.
- Breaching items list uses `<ul>/<li>` semantic markup.
- Amber text on amber-50 background: amber-700 on amber-50 meets WCAG AA contrast ≥ 4.5:1.
- Optional "Review Settings" link has a descriptive `aria-label`: "Review portfolio concentration limit settings".
