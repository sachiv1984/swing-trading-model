**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-29__release-v9.14
**Story:** ST-11 (EPIC-02, BLG-FE-231)

# Decision Record — Daily Position Monitor Suggestions Follow the Grace Period

## 1. Problem

`MonitorModal.js::getPositionStatus` suggests "Stop price hit" when `current_price ≤ stop_price`. It ignores the grace period and uses `stop_price`, not the trailing stop. `strategy_rules.md` §8.1 enforces the stop only after grace. The shared predicate `getExitCondition()` (`src/lib/exitCondition.js`) already applies that rule for the Positions exit dialog and the Dashboard "Exit Conditions Met" row. Since v9.13, the Monitor's suggestion also pre-selects the exit reason, so an in-grace position can be queued with "Stop Loss Hit" pre-selected.

## 2. Decision

### 2.1 Predicate and precedence

The Monitor derives each row from `getExitCondition(position)`:

| `getExitCondition` result | Monitor status | Reason line | Queue pre-selection |
|---------------------------|----------------|-------------|---------------------|
| `riskOff` | exit | "Market risk off" | "Risk-Off Signal" |
| `stopBreach` (post-grace, at or below the trailing stop), not `riskOff` | exit | "Stop price hit" | "Stop Loss Hit" |
| Price at or below the trailing stop, but in grace | hold | "In grace: stop not enforced" | — |
| Neither | hold | "Position OK" | — |

- Risk-off takes precedence when both apply, as in `getExitCondition()`. Today the Monitor puts the stop first. The two surfaces would otherwise pre-select different reasons for the same position.
- The reason labels "Market risk off" and "Stop price hit" stay, so the v9.13 queue mapping (`positions.md` §Daily Position Monitor Exit Queue) is unchanged.
- The new hold reason tells the user why a breached in-grace position is not suggested. It uses the existing muted reason line, with no new colour.
- Risk-off now comes from the position's `risk_off_exit` flag, not from the Monitor's own regime lookup. An unknown regime (ST-03) therefore follows the strategy ruling on the backend, and the Monitor applies no separate rule.

### 2.2 Pre-selection note

The "Stop price hit" note in the v9.13 queue table changes from "…the price is at or below the stop." to:

> "Pre-selected from the Daily Position Monitor: the price is at or below the trailing stop and the grace period has ended."

This matches what the predicate now tests. The risk-off note is unchanged.

## 3. §13 Compliance

Suggestions stay suggestions. The user selects each exit and confirms it in `ExitModal`, one position at a time (v9.13 queue). This change removes a suggestion that §8.1 does not support.

## 4. Frontend Spec Impact

`positions.md` v2.20 → v2.21: §Daily Position Monitor Exit Queue gains §Monitor Suggestions (the §2.1 table), and its "Stop price hit" note is updated.

## 5. Obligations for Sprint Execution

- The Monitor's `positions` prop (`Dashboard.js` `openPositions`) must carry `grace_period`, `current_trailing_stop` and `risk_off_exit`, as the Positions page's data does. If any is missing from that source, it is read from `GET /positions`, not recomputed in the browser.
- The Monitor's `marketRegimes` prop is no longer used for suggestions. It is removed if nothing else reads it.

## 6. Testability (CLAUDE.md §2)

- Playwright (AC 2): an in-grace position priced below its trailing stop is not suggested, and its row reads "In grace: stop not enforced".
- Playwright (AC 3): a post-grace breach is suggested with "Stop price hit", and a `risk_off_exit` position with "Market risk off". A position with both reads "Market risk off".

## 7. Approval

Head of UX & Design: confirmed, 2026-10-29.
Product Owner: confirmed, 2026-10-29.
