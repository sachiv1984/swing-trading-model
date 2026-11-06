**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-06__release-v9.16
**Stories:** ST-07 (EPIC-02, BLG-FE-255), ST-08 (EPIC-02, BLG-FE-256)

# Decision Record — "Plan this" and Suggested Size on Trade Plan

## 1. Problem

Getting from a signal to a checked entry takes five pages: Signals → Watchlist → Research → Trade Plan → Trade Entry. Signals cards offer only "Add to Watchlist", and Screener rows offer Watchlist and Research. On Trade Plan, "Planned Shares (for pre-entry checks)" (`TradePlan.js:867`) comes before Planned Entry and Stop, and before the §4.1 suggestion (`WhatIfSizingPreview`). The user types a share count the system could have suggested. Both stories change how a plan is started and sized, so this record covers both.

## 2. Decision

### 2.1 "Plan this"

| Surface | Where | Shown when |
|---------|-------|------------|
| Signals card (`SignalCard.js`) | Action row, after the primary CTA: secondary button "Plan this" | `status` is `new` or `watchlisted`. Hidden for `dismissed`, `entered`, `already_held` and `allocation_insufficient`. |
| Screener row (`Screener.js`) | News column action cell, after "Research": same small bordered style as "Research" | Every result row |

- **Target:** `/TradePlan?ticker={ticker}&market={market}&entry_price={price}` and, from Signals only, `&signal_id={id}`. `{ticker}` is the row's stored ticker. `TradePlan.js` already matches the `.L` suffix. `{price}` is `signal.current_price` or the screener row's `price`. Omit `entry_price` if the price is null.
- **One click, no write:** the button only navigates. It does not change the signal's status and does not create a plan. The plan exists only after "Save Trade Plan".
- **Pre-fill on the new-plan form:** Ticker, Market and **Planned Entry Price** (`planned_entry_price`, from `entry_price`). Pre-fill does not apply in edit mode and never overwrites a value the user has typed.
- **Signal context:** with `signal_id`, the form fetches that signal (any status except `dismissed`) and shows the §5a Signal Context panel with its pre-population rules. Without `signal_id`, §5a's existing watchlisted-signal lookup applies unchanged. A Screener row gets the panel only if a watchlisted signal exists for the ticker.
- **Accessible name:** `aria-label="Plan this: {TICKER}"`. Test ids: `signal-plan-this-{ticker}` and `screener-plan-this-{ticker}`.

### 2.2 Suggested size before shares

New field order in the pre-entry block of the creation and edit forms:

1. Planned Entry Price | Planned Stop Price (the existing two-column row, moved up)
2. **Suggested size** line (new)
3. Planned Shares (for pre-entry checks)
4. Pre-Entry Validation panel (unchanged)

- **Suggested size line** (`data-testid="plan-suggested-size"`), shown once entry and stop are both valid positive numbers. It calls `POST /portfolio/size`, the endpoint `WhatIfSizingPreview` and `PositionSizingWidget` already use, debounced 300 ms with the default risk %, and the live FX rate for US plans.
  - Valid: "Suggested size: {N} shares (§4.1, {risk}% risk)", `text-sm text-slate-800 dark:text-slate-200`.
  - Invalid or cash-insufficient: reuse the `AMBER_MESSAGES`/`SYSTEM_MESSAGES` text and colours of `trade_plan.md` §10.6a.
  - Loading: a one-line skeleton.
  - Before both inputs are valid: no line and no placeholder.
- **Pre-fill:** on a valid, cash-sufficient result, Planned Shares is set to `suggested_shares` (whole shares, floored) **while the user has not typed in Planned Shares**. After the user edits the field, the suggestion stays on screen but no longer writes to it. In edit mode a stored `planned_quantity` counts as user-typed.
- **"Use suggested size" button:** shown under the line when the user's value differs from the suggestion. It copies the suggestion in.
- The What-If Sizing Preview (§5d) is unchanged. It keeps its own entry and risk inputs for exploring scenarios.

## 3. §13 Compliance

"Plan this" is a user-started navigation to an unsaved form. No position, plan or status is created or changed. The suggested size is the deterministic §4.1 calculation, shown as advice and always editable. This matches the existing §10.6a statement. No new §13 review is needed.

## 4. Frontend Spec Impact

- `pages/signals.md` v0.8 → v0.9: §Signal Card Actions gains "Plan this".
- `pages/screener_results.md` v1.10 → v1.11: §11 gains "Plan this".
- `pages/trade_plan.md` v1.21 → v1.22 (one bump, shared with ST-05's §5e): §2 route parameters, §5a.1 `signal_id` presence, and new §5f "Suggested Size Before Shares".

## 5. Obligations for Sprint Execution

- ST-07 merges before ST-08 (slice sequencing). Both edit `TradePlan.js`.
- `navigation.md` v2.0 §Onward Links: Signals and Screener gain an onward link to Trade Plan. Add it there under ST-03, in the same sprint.
- Observation, not filed by this gate: `trade_plan.md` §5d.4 says `trade_plans` has no entry-price column, but `planned_entry_price` and `planned_quantity` are persisted (`TradePlan.js:578–579`). Sprint Planning should file a spec-debt item.

## 6. Testability (CLAUDE.md §2)

Playwright:
- From a Signals card, "Plan this" opens `/TradePlan` with ticker, market and entry pre-filled, and with the Signal Context panel shown.
- From a Screener row, the same check, without the panel unless a watchlisted signal exists.
- With entry and stop entered, Planned Shares pre-fills with the mocked `suggested_shares`.
- A typed shares value is not overwritten, and "Use suggested size" restores the suggestion.
- Run in light and dark themes for the new line.

## 7. Approval

Head of UX & Design: Approved (agent-mediated, Design Gate Engine, 2026-11-06). Product Owner: Approved (the user, in session, 2026-11-06).
