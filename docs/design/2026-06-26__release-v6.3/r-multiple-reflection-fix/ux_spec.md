**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-06-26
**Cycle:** 2026-06-26__release-v6.3
**Story:** ST-02 (BLG-FE-79)
**Approved by:** Product Owner — 2026-06-26

---

# UX Spec — R-Multiple Display Fix on Reflections Page

## Context

The Reflections page (`/reflections`, `TradeReflection.js`) displays a card grid of closed trades with their structured post-trade reflections. Each card shows P&L, R-Multiple, and hold period. Currently, R-Multiple always shows "—" because `r_multiple` is null in the API response. The fix requires both a data pipeline correction (backend/frontend) and a display behaviour clarification.

## Page: Reflections Card Grid

### R-Multiple Display Rules

| Condition | Display | Format | Colour |
|-----------|---------|--------|--------|
| Value present, profit (≥ 0) | `+X.XXR` | Signed, 2dp, "R" suffix | `text-emerald-400` |
| Value present, loss (< 0) | `-X.XXR` | Signed, 2dp, "R" suffix | `text-rose-400` |
| Value null — no stop loss recorded | `N/A` | Plain text, muted | `text-slate-500` |
| Value null — loading state | `—` | Em dash | `text-slate-500` |

**Distinction between N/A and —:**
- `N/A` is shown when `r_multiple` is null AND it is known that the trade has no stop loss recorded (`stop_price` is null or zero). This is a data completeness state, not a loading state.
- `—` is reserved for loading/unresolved states only and must not be used for settled null data.

### Tooltip Behaviour

When R-Multiple displays `N/A`:
- Tooltip on hover: `"No stop loss recorded for this trade — R cannot be computed"`
- Tooltip on `—` (loading): no tooltip required

### No Other Card Fields Affected

This change applies only to the R-Multiple cell within each reflection card. All other fields (P&L, Hold, Exit Reason badge) retain their existing behaviour.

## UX Decisions

1. **"N/A" over "—" for data-completeness null:** The em dash is a generic placeholder ambiguous to the user. "N/A" communicates that the value is not applicable due to missing data, which is more informative and user-friendly.

2. **Muted styling for N/A:** `text-slate-500` keeps the card visually clean without drawing attention to missing data in a negative way. The value is simply absent, not an error.

3. **No remediation prompt:** The Reflections page is read-only. If a user wants to add a stop loss retroactively, they do so from the Trade History page. No call-to-action is added here.

4. **Profit/loss colour only on real values:** Colouring "N/A" would imply directional meaning that doesn't exist.

## Constraints

- `trade_reflection.md` v0.1 (the reflection modal spec) already specifies `r_multiple` display with "–" for null — that spec covers the modal only and is not affected by this change.
- The Reflections page has no pre-existing frontend spec. A spec (`reflections.md`) must be created as part of this story's delivery.

## Artefact Completeness

This spec is sufficient for implementation without additional wireframes. The card layout and interaction model are unchanged; only the R-Multiple null display rule changes.
