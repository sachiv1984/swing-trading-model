**Owner:** Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active — Assessment Complete
**Last Updated:** 2026-07-24
**Cycle:** 2026-07-21__release-v7.7
**Story:** ST-05 (EPIC-05)
**Backlog ref:** S2-05

---

# SI-02 Gate Acceleration — In-App Nudge Feasibility Assessment

**Feature scope assessed:** A lightweight in-app nudge to accelerate SI-02 gate clearance (currently gated on ≥20 closed trades with ≥1 linked trade plan)
**Assessment type:** Feasibility + recommendation (investigation output only — no shipped UI this cycle, per Design Gate "Design Not Applicable" confirmation)
**Governance reference:** `claude/strategy/strategy_rules.md §13` (advisory-only constraint on any recommendation)

---

## Summary

This assessment evaluates whether a lightweight in-app nudge would meaningfully accelerate SI-02 gate clearance, given `BLG-FE-109` ("Start Trade from Plan") has been in production for a full sprint cycle (shipped v7.3, 2026-07-16) with **zero movement** on the gate's `linked trade plans` metric.

**Assessment outcome: Recommend a nudge — feasible, low-risk, and targets the actual root cause.** The gate is not blocked by a missing feature; it is blocked by a shipped feature nobody is using. A passive capability with no active prompt has a much lower adoption ceiling than the same capability paired with a nudge at the moment of relevant action.

---

## Gate History Context

Per `run_manifest.md` (this cycle's audit): SI-02's live re-check has returned **9 consecutive byte-identical readings** since 2026-07-12 — `total_trades: 20`, `trade-plans: 11 total, 0 linked` (`position_id` null on all 11). The gate condition is "≥20 closed trades **with linked trade_plans**" — the 20-trade threshold has been met for at least 9 cycles; the blocker is exclusively the "0 linked" half of the condition.

`BLG-FE-109` ("Start Trade from Plan", `docs/design/2026-07-15__release-v7.2/start-trade-from-plan/ux_spec.md`) shipped specifically to address this: a "Start Trade" button on both the Trade Plan detail view and the Trade Plans list view that pre-fills `TradeEntry.js` and auto-attaches `trade_plan_id` to the resulting trade — removing the manual linking step entirely for any trade started this way.

**Verified still correctly shipped and wired** (code read, this assessment): `src/pages/TradePlans.js` and `src/pages/TradePlan.js` both render the "Start Trade" button per spec (`grep` confirms both entry points and the `trade_plan_prefill` hand-off object); `src/pages/TradeEntry.js` reads `location.state.trade_plan_prefill` and carries `trade_plan_id` through to submission. This is not a bug — the feature works as designed. The problem is that traders are not discovering or choosing to use it; they continue navigating directly to `/TradeEntry` from muscle memory, the sidebar, or the command palette, none of which pass through a trade plan at all.

---

## Root Cause Analysis

A shipped, functioning capability with **zero adoption movement across 9 gate readings** (i.e., since the feature went live) points to a discoverability/habit problem, not a technical one:

1. **No prompt at the moment of action.** The "Start Trade" button only appears on `TradePlan.js`/`TradePlans.js` — pages the trader must already be on. A trader who goes straight to `/TradeEntry` (their pre-existing habit from before this feature existed) never sees it.
2. **No connection back from the entry point traders actually use.** `TradeEntry.js`'s manual-entry path does surface an optional "Link to trade plan" selector (§2.3 of the ux_spec) once a ticker is typed and an eligible plan exists for it — but this is passive (renders silently, no visual emphasis) and requires the trader to already know a plan exists for that ticker.
3. **No feedback loop telling the trader the gate exists or that their behaviour affects it.** SI-02 gate state is currently only visible via `GateProgressStrip.js` (dashboard) showing closed-trade count — it does not surface the "linked" half of the condition at all, so a trader has no visibility into *why* the gate isn't clearing even after crossing 20 trades.

---

## Feasibility Analysis

### Technical Feasibility

All the data needed for a nudge already exists and is already computed:
- `GET /trade-plans?status=...` already returns non-terminal plans (used by the existing optional-link selector).
- The manual `/TradeEntry` flow already has a code path (§2.3 of the ux_spec) that queries eligible plans for a given ticker — a nudge would surface this existing query result more prominently rather than adding new backend work.
- `GET /portfolio/gate-metrics` (backing `GateProgressStrip.js`) already computes the closed-trade count; extending it to also surface the linked-count would be a small, additive backend change, not new infrastructure.

**Technical feasibility: Yes.** No new backend surface is required for the minimum nudge; a gate-progress extension is a small additive change if the richer version (below) is chosen.

### UX Feasibility — Nudge Design Options

Two candidate nudge shapes, in increasing order of intrusiveness:

| Option | Description | §13 risk |
|--------|-------------|----------|
| **(a) Passive — emphasise the existing link selector** | When a trader manually enters `/TradeEntry` and an eligible trade plan exists for the ticker they've typed, visually promote the existing (currently easy-to-miss) "Link to trade plan" selector — e.g. reuse the new `StandingAlert` component (`src/components/ui/StandingAlert.js`, shipped this same cycle by EPIC-04) as an `info`-severity banner: *"A trade plan exists for {TICKER} — link it?"* with a one-click action that selects the plan, dismissible without linking. | None — purely informational, no gating, dismissible, does not block submission. |
| **(b) Active — dashboard/portfolio-level reminder** | A dismissible `StandingAlert` on the Dashboard or Positions page when non-terminal trade plans exist and the trader is about to enter a position for a ticker with a matching plan (or periodically, e.g. "You have 3 trade plans ready to execute"). | Slightly higher risk of feeling like a push toward action — must remain purely informational (no "you should trade this" framing), consistent with §13's non-blocking principle. |

**Recommendation: Option (a).** It targets the exact moment the gap occurs (a trader is already at `/TradeEntry` with a ticker typed, and a plan exists they didn't notice), requires no new backend surface, and carries the lowest §13 framing risk since it never initiates contact — it only responds to an action the trader has already taken. Option (b) is a reasonable follow-on if (a) alone doesn't move the metric, but should not be built pre-emptively.

### §13 Compliance

Both options are within the same §13 envelope already established for `BLG-FE-109` itself (`ux_spec.md §3`: "Display-only linkage; the trader initiates and confirms every field... No automated trade execution or recommendation"). A nudge that surfaces an existing, already-approved linking action more visibly does not change that determination — it is still the trader who clicks, still fully editable, still non-blocking. No new §13 review is required for Option (a); Option (b), if pursued later, should be re-assessed at design time given its slightly broader surface (proactive rather than purely reactive prompting).

---

## Recommendation

**Propose Option (a)** for a future sprint: reuse the newly-shipped `StandingAlert` component to promote the existing (already-built, currently under-visible) "Link to trade plan" selector on `TradeEntry.js`'s manual-entry path, when an eligible plan exists for the typed ticker. This is a small, low-risk frontend-only change (no new backend endpoint, reuses this cycle's own `StandingAlertStack`) that directly targets the demonstrated root cause — a working feature nobody notices — rather than adding gate-acceleration logic that changes the gate's own criteria (out of scope; the 20-trade-with-linkage condition itself is not being questioned here).

**Scope sketch for a future ST:**
1. On `TradeEntry.js`, when a ticker is typed and `GET /trade-plans?ticker={ticker}` (already called for the existing optional-link selector) returns ≥1 eligible plan, render a `StandingAlert` (`severity="info"`) above the existing link selector: *"A trade plan exists for {TICKER}."* with an action link that scrolls to/focuses the existing selector (no new selection UI — reuses what's already built).
2. No backend change required for this minimum version — the existing `GET /trade-plans?ticker=` query already backs the current (passive) selector.
3. Playwright coverage: confirm the banner appears only when an eligible plan exists, is dismissible, and does not affect existing form submission.

**Not recommended this cycle:** No action is proposed as an alternative was also considered — "do nothing and wait" was rejected given 9 consecutive zero-movement readings already demonstrate the passive approach has plateaued; further waiting has no evidence behind it that adoption will spontaneously improve.

---

## Sign-Off

**Reviewed by:** Product Owner (this assessment)
**Date:** 2026-07-24
**Determination:** Nudge (Option a) proposed as a scope sketch for a future sprint; no implementation in this cycle (investigation output only, per Design Gate "Design Not Applicable" — no shipped UI this cycle).

**AC sign-off:**
- ✅ Review completed assessing whether a lightweight in-app nudge would meaningfully accelerate SI-02 gate clearance, referencing the SI-02 gate's live re-check history (9 consecutive byte-identical NOT MET readings since 2026-07-12, per `run_manifest.md`)
- ✅ Recommendation recorded — nudge feature proposed (Option a) with scope sketch, supporting rationale (root-cause analysis of the shipped-but-unused `BLG-FE-109` feature)
