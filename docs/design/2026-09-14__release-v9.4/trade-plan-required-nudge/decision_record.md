**Owner:** Head of UX & Design
**Cycle:** 2026-09-14__release-v9.4
**Story:** ST-28 (BLG-FEAT-95, EPIC-06)
**Status:** Approved

# Decision Record — "Trade Plan Required Before Entry" Soft Nudge

## Context

`position_form.md` (Class 1, the position-entry form component) has no concept of `trade_plan_id` linkage today — a position can be created with no trade plan attached, and the form gives no signal either way. `strategy_rules.md` §4.2 already establishes the precedent that pre-entry checks are advisory and non-blocking ("the user retains full discretion to proceed regardless of advisory status") — this story extends that same non-blocking-advisory pattern to trade-plan linkage specifically, rather than introducing a new interaction category.

## Decision

1. **Placement:** an inline advisory banner inside `PositionForm`, above the submit button, visible only when no `trade_plan_id` is associated with the in-progress entry.
2. **Copy:** "No trade plan linked to this position. Consider creating one before entering — or continue without." Non-alarming tone (this is guidance, not an error) — amber/advisory colour treatment (`bg-amber-50 dark:bg-amber-950/30` + amber icon, matching the existing pre-entry advisory panel's tone in `strategy_rules.md` §4.2 rather than a destructive/red warning treatment).
3. **Actions:** two affordances, neither blocking:
   - **"Create Trade Plan"** — secondary-button link, navigates to the Trade Plan creation flow (opens in the existing trade-plan creation surface; does not lose the in-progress position-entry form state — implementation detail for the executing story to confirm against current routing/state patterns).
   - **Submit button remains enabled throughout** — the form's existing submission behaviour (`position_form.md` §Form submission behaviour: "does not block form submission") is unchanged. No confirmation dialog interrupts submission; this is a persistent inline nudge, not a modal gate.
4. **§13 compliance:** this does not automate or influence the entry decision itself (no computed recommendation, no default action forced) — it surfaces an existing fact (plan-linkage absence) exactly as `strategy_rules.md` §4.2's advisory checks already do. No new §13 review is required; this generalises an existing cleared pattern rather than introducing a new automation surface.
5. **Dismissal:** the banner has no explicit dismiss control — it simply stops rendering once a `trade_plan_id` becomes associated with the entry (e.g. user follows the Create Trade Plan link and returns with one attached), consistent with `strategy_rules.md` §4.2's advisory checks being condition-driven, not manually dismissed.

## Evidence-method note

This is a new, visible, interactive banner — Playwright coverage is required per the CLAUDE.md frontend-visible-change standard and is already named directly in the story's own AC ("Playwright coverage confirms the nudge does not block entry"). Minimum coverage: banner renders when `trade_plan_id` is absent, does not render when present, and submission succeeds with the banner visible (non-blocking assertion).

## Frontend spec update

`position_form.md` gains a new subsection documenting this banner (placement, copy, states, the two actions) under a new "Trade Plan Linkage Advisory" heading, cross-referencing `strategy_rules.md` §4.2 as the precedent this generalises.

## Sign-off

Head of UX & Design: Approved, 2026-09-14.
Product Owner: Approved, 2026-09-14 (confirms §13 non-gate consistent with §4.2 precedent).
