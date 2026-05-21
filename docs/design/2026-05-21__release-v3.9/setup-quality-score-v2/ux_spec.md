**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Date:** 2026-05-21
**Approved by:** Product Owner — 2026-05-21
**Cycle:** 2026-05-21__release-v3.9
**Story:** ST-14 (EPIC-05, conditional — 20+ closed trades gate)
**Extends:** docs/design/2026-05-18__release-v3.7/quality-score-display/ux_spec.md

---

# UX Spec — Setup Quality Score v2 (ST-14, v3.9)

## Changes from v3.7

The v3.7 design established the basic score display on the Trade Plan detail view. v3.9 adds:

1. **Qualitative label** alongside numeric score (Excellent / Good / Fair / Low)
2. **Tooltip / expandable detail panel** with underlying stats
3. **Ticker-based endpoint**: `GET /trade-plans/setup-quality-score?ticker={ticker}` (not per-plan-ID)
4. **Score updates on ticker change** (React Query refetch on ticker param change)
5. **Shown in Trade Plan creation form** (new placement — not just detail view)

---

## Score Display

### Score Badge

| Condition | Display |
|-----------|---------|
| `gate_not_met: true` | "Insufficient trade history (< 20 trades)" — no score badge |
| Score 0–39 | `{N}/100` + label **"Low"** (red pill) |
| Score 40–59 | `{N}/100` + label **"Fair"** (amber pill) |
| Score 60–79 | `{N}/100` + label **"Good"** (blue pill) |
| Score 80–100 | `{N}/100` + label **"Excellent"** (green pill) |

Qualitative label: pill badge to the right of the score value. Colour matches label tier.

Sub-label below badge: "Based on your own trade history" (muted, small). §13 compliance note.

### Tooltip / Expandable Detail

Clicking the score badge (or an info icon adjacent to it) opens a detail panel:

| Field | Source | Display |
|-------|--------|---------|
| Matching trades | `matching_trades` | "{N} matching trades found" |
| Win rate | `win_rate` | "{X}% win rate" |
| Average R | `average_R` | "{X.X}R average profit" |

Panel closes on click-outside or Escape key.

### States

| State | Display |
|-------|---------|
| Loading | Inline skeleton placeholder (matching badge height) |
| Error | Section hidden silently — does not block page |
| Gate not met | "Insufficient trade history (< 20 trades)" message instead of badge |

---

## API

Endpoint: `GET /trade-plans/setup-quality-score?ticker={ticker}`

Gate not met response:
```json
{ "gate_not_met": true, "min_trades_required": 20 }
```

Gate met response:
```json
{ "score": 74, "matching_trades": 31, "win_rate": 0.68, "average_R": 1.4, "score_explanation": "..." }
```

---

## Placement

### Pre-Trade Research View (`/research/{ticker}`)

Replace the v3.7 §5 quality score row. Now ticker-based (not plan-based).
- Shown for all tickers regardless of whether a trade plan exists
- Ticker from URL path param
- Score refetches when ticker in URL changes

### Trade Plan Detail View (`/trade-plans/{id}`)

Update §7a. Displayed below status badge, above pre-trade checklist.
- Ticker derived from `trade_plan.ticker`

### Trade Plan Creation Form (`/trade-plans/new`) — New in v3.9

Read-only panel shown when ticker field is populated.
- Hidden on initial empty form (no ticker entered)
- Refetches on ticker input change (debounced 500ms)

---

## §13 Compliance

Display-only in all three placements. Sub-label "Based on your own trade history" visible in all contexts. No automated actions.

---

## Playwright Tests

- **SC-SQS-01**: Score badge renders with numeric value and qualitative label
- **SC-SQS-02**: Gate-not-met message renders when `gate_not_met: true`
- **SC-SQS-03**: Score updates on ticker change (refetch triggered)
