**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-08-14__release-v8.8
**Story:** ST-14 (EPIC-03, BLG-FE-162)

# Decision Record — Research Page Trade Plan Status Badge

## 1. Problem

`Research.js`'s local `PlanStatusBadge` maps only 3 of the 6 `trade_plans.status` values (`active`, `draft`, `closed`) and falls back to the raw status string for the other 3 (`research_pending`, `research_complete`, `entry_conditions_set`) — a user sees literal snake_case on the Research page. A second, complete map already exists and is already shipping correctly: `TradePlans.js`'s `STATUS_CONFIG`/`TradePlanStatusBadge` (all 6 statuses plus `abandoned`, already-approved colours: grey/amber/blue/violet/green/slate/red). `TradePlan.js` additionally keeps its own third, label-only map (`STATUS_LABELS`) for its edit-form dropdown. Three divergent sources of truth for the same 6 labels is the root cause, not just Research.js's incompleteness.

## 2. Decision

No new visual design is required — `TradePlans.js`'s `STATUS_CONFIG` is already the most complete, already-shipped, already-approved source. Promote it to the single canonical source:

- Export `STATUS_CONFIG` (or an equivalent named export) from `TradePlans.js` alongside the already-exported `TradePlanStatusBadge`.
- `Research.js` deletes its local `PlanStatusBadge` function entirely and renders `<TradePlanStatusBadge status={activePlan.status} />` (already imported pattern elsewhere in the codebase — `TradePlan.js` already imports `TradePlanStatusBadge` from `./TradePlans`, so this is not a new cross-file dependency, just extending an existing one to a second consumer).
- `TradePlan.js`'s `STATUS_LABELS` (label-only, used for its status-select dropdown `<option>` text) may remain as-is — it is a different UI surface (plain-text dropdown option, not a coloured badge) and carries no incorrect/divergent values today. Not in scope for this fix; the AC targets badge rendering specifically.

This keeps exactly one coloured-badge implementation (`TradePlans.js`'s `STATUS_CONFIG`/`TradePlanStatusBadge`) consumed by every page that renders a trade-plan status badge.

## 3. Constraints Checked

- No new colours, no new component — reuse of an already-approved, already-shipped visual pattern. No light/dark theming risk (colours unchanged from what's already live on the Trade Plans list page).
- Motion/timing clause (`design_gate_prompt.md` §6): not applicable — no animation or timing parameter involved.
