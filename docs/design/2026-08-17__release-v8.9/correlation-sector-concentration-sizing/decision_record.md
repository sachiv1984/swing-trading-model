**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-08-17__release-v8.9
**Story:** ST-04 (EPIC-02, BLG-BE-104)

# Decision Record — Correlation/Sector-Concentration-Aware Position Sizing: Visible Reason Display

## 1. Problem

`BLG-BE-104` extends the existing position-sizing calculation (`POST /portfolio/size`, `backend/services/sizing_service.py`) to reduce or flag a new position's suggested size when it would push sector exposure past a defined concentration threshold, reflecting existing open-position sector concentration rather than just the candidate ticker's own volatility. AC-02 requires the sizing output to "include a visible reason when reduced or flagged for concentration" — this is new user-visible data on an existing surface, so it is Design Required per `design_gate_prompt.md` §6 ("new data displayed").

The sizing calculation's output is currently consumed in exactly one UI surface: the `PositionSizingWidget` (`src/components/trades/PositionSizingWidget.js`), embedded in `TradeEntry.js`. This same endpoint is also the intended backend for the new What-If Sizing/Risk Simulator (ST-05 — see companion decision record `docs/design/2026-08-17__release-v8.9/what-if-sizing-risk-simulator/ux_spec.md`), so the display treatment decided here must work identically in both call sites.

**Baseline spec-debt note:** `PositionSizingWidget` (fields, debounce behaviour, `POST /portfolio/size` contract) has no dedicated frontend spec section prior to this cycle — it is referenced only in passing at `trade_plan.md` §10 (hand-off flow). This decision record documents only the new concentration-reason addition; full baseline documentation of the widget is out of scope here and is filed separately as spec debt (see Notes).

## 2. Decision

Extend the `POST /portfolio/size` response with two new fields:

| Field | Type | Meaning |
|-------|------|---------|
| `concentration_adjusted` | boolean | `true` when the suggested size was reduced from the volatility-only baseline due to sector concentration |
| `concentration_reason` | string \| null | Human-readable reason, e.g. `"Reduced 20% — 3 open positions already in Technology (34% of portfolio heat)."` Null when `concentration_adjusted` is `false`. |

**Note (flagging only, not display):** a position may also be *flagged* without a size reduction (e.g. concentration is elevated but below the reduction threshold). For this case, `concentration_adjusted` remains `false` but `concentration_reason` is non-null — the display rule below keys off `concentration_reason` presence, not `concentration_adjusted`, to cover both cases in one control.

**Display:** when `concentration_reason` is non-null, render an inline note directly beneath the existing "Suggested: {N} shares" result line, in both `PositionSizingWidget` and the ST-05 What-If panel:

- Icon: `AlertTriangle` (Lucide), amber (`text-amber-500`)
- Text: the `concentration_reason` string verbatim, amber (`text-amber-600 dark:text-amber-400`), `text-xs`
- No dismiss affordance — this is not a `StandingAlert`; it re-evaluates on every debounced recalculation and disappears automatically when concentration no longer applies (e.g. stop distance widened, ticker changed) — same convention as the existing invalid-input amber messages already in the widget (`AMBER_MESSAGES`).

When `concentration_reason` is null: no change to current layout — no empty space reserved, consistent with the "hidden entirely when absent" convention used elsewhere on this page (§5a, §10.3 of `trade_plan.md`).

## 3. Constraints Checked

- **§13 compliance:** the concentration adjustment is a deterministic, rule-based calculation over the user's own open positions (sector exposure), not an ML/AI inference. It reduces a suggested value the user may still override (the shares field remains manually editable in both `PositionSizingWidget` and the ST-05 preview) — advisory, not enforced. Compliant with §13.1/§13.2 by the same reasoning already applied to the existing sizing widget.
- Does not contradict `strategy_rules.md §13`.
- No new metric introduced — this is a reason string, not a tracked analytics value; `metrics_definitions.md` unaffected.

## 4. Product Owner Approval

Approved 2026-08-17 (design gate session). No AI-provider call introduced — §13 boundary pre-check (`design_gate_prompt.md` STEP 1) not applicable to this item.

## Notes

- Backend Engineering Patterns Owner must confirm the concentration-reduction threshold and reason-string composition rule at implementation time; this record fixes only the *display* contract (field names, placement, styling), not the underlying threshold logic.
- Baseline `PositionSizingWidget` documentation gap: filed as a follow-up spec-debt backlog item (BLG-SPEC-type) per CLAUDE.md's spec-debt convention — not resolved in this design gate.
