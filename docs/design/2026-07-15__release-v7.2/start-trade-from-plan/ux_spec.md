**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-15
**Approved by:** Product Owner — 2026-07-15
**Story:** ST-03 — Trade-plan-to-execution linkage UX ("Start Trade from Plan") (BLG-FE-109)
**Depends on:** ST-02 readiness pass (BLG-SPEC-89) — this artefact assumes ST-02's confirmed `trade_plan_id` auto-link and pre-fill API surface
**Cycle:** 2026-07-15__release-v7.2

---

# UX Specification — "Start Trade from Plan"

## 1. Context

Trade plans (`TradePlan.js`/`TradePlans.js`) and executed trades (`TradeEntry.js`) are currently disconnected flows — a trader must manually remember to associate a plan when entering a trade, and nothing today prompts them to. This is the direct cause of the SI-02 gate's persistent `0/11 linked trade plans` (unchanged 2026-07-12 through 2026-07-15, `.claude_current_state.json`). The fix is behavioural, not just plumbing: make linking the path of least resistance rather than an extra manual step.

The existing `TradeEntry.js` pre-fill pattern (`location.state.watchlist_prefill`, used by the Watchlist "Add to Position" flow) is the established precedent for this kind of cross-page hand-off and is reused here rather than inventing a new mechanism.

## 2. Decision

### 2.1 Entry points (AC-01)

A **"Start Trade"** button is added in two places:

- **`TradePlan.js` detail view:** in the `PageHeader` actions row, to the left of "Abandon Plan"/"Edit"/"Back" — primary button style (filled, not outline), icon `TrendingUp` (Lucide), label "Start Trade".
- **`TradePlans.js` list view, Actions column:** a ghost icon button matching the existing `Edit2`/`Trash2` icon-button pattern (`h-7 w-7`, `text-slate-600 dark:text-slate-400 hover:text-white`), icon `TrendingUp`, positioned first (left of Edit).

**Visibility rule (both surfaces):** shown only when `plan.status` is one of `draft`, `research_pending`, `research_complete`, `entry_conditions_set` — i.e. not yet linked to an open position and not terminal. Hidden when `status` is `active` (a position already exists for this plan — starting another would create an unintended duplicate), `closed`, or `abandoned`. This mirrors the existing `Abandon` button's `status === 'active'` hide rule (`trade_plan.md` §8.1) and extends the same logic to the terminal states.

### 2.2 Hand-off mechanism (AC-02)

Clicking "Start Trade" navigates to `/TradeEntry` passing a new `location.state.trade_plan_prefill` object (sibling pattern to `watchlist_prefill`):

```js
{
  trade_plan_id: plan.id,
  ticker: plan.ticker,
  market: plan.market,
  stop_price: plan.stop_level ?? "",
}
```

`TradeEntry.js` reads this the same way it reads `watchlist_prefill` today, pre-populating `ticker`, `market`, and `stop_price`. `entry_price`, `shares`, `fill_price`, `fx_rate`, `atr_value` are **not** pre-filled from the plan (the plan does not capture live fill terms) — the trader enters these at execution time, unchanged from today's manual flow.

`trade_plan_id` is carried in component state (not a visible/editable form field) and included automatically in the `POST /trades` (or equivalent) payload on submit — no additional user action required, satisfying AC-02. A small non-editable indicator renders directly below the ticker field: a muted pill reading **"Linked to trade plan"** with the ticker, so the trader has visual confirmation the association will be recorded (mirrors the read-only, non-interactive styling of the Signal Context panel badge treatment in `trade_plan.md` §5a). This is additive display only — it does not gate submission.

### 2.3 Manual entry — optional linking (AC-03)

Trades started the normal way (direct navigation to `/TradeEntry`, no `trade_plan_prefill` state) are unaffected: no linked-plan indicator, `trade_plan_id` omitted from the payload, identical to current behaviour.

To satisfy AC-03's "can still optionally select a plan to link": once a ticker is entered manually, an optional **"Link to trade plan (optional)"** select appears below the ticker/market fields, populated from `GET /trade-plans?ticker={ticker}` filtered client-side to non-terminal, non-active statuses (same set as §2.1). Empty when no eligible plans exist for the ticker — the field does not render at all in that case (consistent with the Signal Context panel's "hidden entirely when absent" precedent, not a disabled/empty-state control). Selecting a plan sets the same `trade_plan_id` state as the pre-filled path and renders the same "Linked to trade plan" indicator; it does not overwrite already-entered form values (ticker/market are read-only at that point since they drove the query).

### 2.4 Regression risk (AC-04, cross-referenced from ST-02 AC-07)

No existing `TradeEntry.js` required-field validation (`ticker`, `shares`, `entry_price`) changes. `trade_plan_id` and the optional link selector are additive fields outside the existing `isFormValid` check. The Signal Context panel (§5a, shown only for a linked *signal*, not a linked *plan*) is a separate, unrelated panel and is unaffected — both may render simultaneously if applicable.

## 3. §13 Compliance

Display-only linkage; the trader initiates and confirms every field via the existing manual entry form (or accepts pre-filled values, which remain editable prior to submit). No automated trade execution or recommendation — this only removes a manual data-entry step for an action the trader is already taking. Consistent with ST-02 AC-06 (confirmed not to cross the §13 automated-execution boundary).

## 4. States

| State | Behaviour |
|-------|-----------|
| Plan eligible (non-terminal, non-active) | "Start Trade" button/icon visible on both surfaces |
| Plan active/closed/abandoned | "Start Trade" hidden |
| Arrived via "Start Trade" | Ticker/market/stop pre-filled; "Linked to trade plan" indicator shown; fields remain editable |
| Manual entry, no eligible plan for ticker | Link selector not rendered |
| Manual entry, eligible plan(s) exist | Link selector rendered, unselected by default |
| Link selector: plan selected | "Linked to trade plan" indicator shown; `trade_plan_id` set |

## 5. Sign-off

- **Head of UX & Design:** Confirmed — 2026-07-15
- **Product Owner:** Approved — 2026-07-15
