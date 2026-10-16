**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-16__release-v9.13
**Story:** ST-05 (EPIC-01, BLG-GOV-391)

# Decision Record — Interim "Outside §8 — Informational" Label on Rebalance Exit Signals

## 1. Problem

Since v6.2, `generate_rebalance_exit_signals` recommends exiting open positions outside the top-5 momentum ranking on the last trading day of each month. The Signals page shows these as `exit_rebalance` cards with a "Month-End Exit" status badge. `strategy_rules.md` §8 allows exactly three exit conditions, and rebalancing is not one of them. Until the Strategy Rules & System Intent Owner rules, the user sees a strategy-looking exit recommendation that the strategy does not define.

## 2. Decision

### 2.1 Interim label (until the determination is applied)

On every Signal card whose status is `exit_rebalance`, directly under the status badge row:

- `Info` icon (lucide, 12 px, `aria-hidden`) + "Outside §8 — informational" (`text-xs font-medium`).
- A second muted line: "Not one of the strategy's three exit conditions. No action is required."
- Colour: `text-slate-600 dark:text-slate-400` (secondary token, 7.58:1 light / 5.71:1 dark). It is informational, not a warning.
- `data-testid="rebalance-outside-s8-label"`. The badge's `title` attribute holds the full sentence.

The "Month-End Exit" badge and the card layout are otherwise unchanged. Wherever the Signals table renders the `exit_rebalance` type badge ("Rebalance Exit", `signals.md` §Signal Type Badge Styling), the same label follows it.

### 2.2 After the determination

- **§8 amended to include rebalance exit:** the interim label is removed in the same change as the §8 edit. The badge stays.
- **Signal withdrawn:** no `exit_rebalance` signals are generated, so the card state and the label are retired with `rebalance-exit.yml` (AC 3).

Either outcome deletes the label. It is not a permanent state.

## 3. §13 Compliance

Display only. The label reduces the signal's apparent authority, and adds no action.

## 4. Frontend Spec Impact

`signals.md` v0.4 → v0.5: new §Rebalance Exit Interim Label after §Signal Type Badge Styling.

## 5. Obligations for Sprint Execution

- Any non-UI surface that delivers the rebalance signal (for example a notification from `rebalance-exit.yml`) is outside this AC. If one exists, apply the same wording or file a backlog item.

## 6. Testability (CLAUDE.md §2)

- Playwright (AC 2): mocked `GET /signals` with one `exit_rebalance` signal, where `rebalance-outside-s8-label` is visible with "Outside §8 — informational". A `new` signal shows no label.

## 7. Approval

Head of UX & Design: confirmed, 2026-10-16.
Product Owner: confirmed, 2026-10-16.
