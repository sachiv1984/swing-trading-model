**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-16__release-v9.13
**Story:** ST-01 (EPIC-01, BLG-FE-226)

# Decision Record — Daily Position Monitor Exits Open the Real Exit Flow

## 1. Problem

Dashboard → Quick Actions → Run Monitor (`MonitorModal.js`) suggests exits for positions with a stop hit or a risk-off market. "Exit Selected" calls `Dashboard.js::handleExitPositions`, which loops `Position.update` → `PATCH /positions/{id}`. That route does not exist, so every confirm returns 405. The handler has no error handling. The modal stays open with the selection cleared, no position closes and no error shows. The payload would also skip fees, the broker fill and exit FX, and would write no `trade_history` row.

## 2. Decision

### 2.1 Flow: one ExitModal per selected position

"Exit Selected" no longer submits anything. It starts an **exit queue** of the selected positions, in the Monitor's display order.

1. The Monitor dialog closes, and `ExitModal` opens for the first queued position. Only one dialog is open at a time. Dialogs are not stacked.
2. `ExitModal` shows its usual fields (shares, exit price, exit FX for US, exit date, reason, note) and submits through `POST /positions/{id}/exit` (`Position.exit`), the same call and payload as the Positions page.
3. On success, the next queued position's `ExitModal` opens. After the last one, the queue ends and a success toast reads "Exited {n} position{s}." The positions, portfolio, `portfolioApi` and trades queries are invalidated, as in the Positions exit mutation.
4. **Cancel, ✕ or Escape** ends the queue. Nothing more is submitted. The Monitor reopens with the positions not yet exited still selected, so the user can resume or deselect. Exits already recorded stay recorded.

The Trade Reflection prompt that follows a Positions-page exit is **not** opened inside the queue, because it would interrupt the sequence. Reflections stay available from Trade Reflections.

### 2.2 Queue indicator

While a queue is running, `ExitModal`'s description reads "Exit {i} of {n} from the Daily Position Monitor. You are about to close your position in {TICKER}." (`data-testid="exit-queue-progress"`). It is omitted when `n` is 1. Outside the queue, the description is unchanged.

### 2.3 Pre-selected reason

The queue passes the reason from the Monitor's suggestion to `ExitModal` as an explicit pre-selection. It overrides `getExitCondition()` for that open:

| Monitor suggestion | Pre-selected Exit Reason | Note under the select (`exit-reason-preselect-note`) |
|--------------------|--------------------------|------------------------------------------------------|
| "Stop price hit" | "Stop Loss Hit" | "Pre-selected from the Daily Position Monitor: the price is at or below the stop." |
| "Market risk off" | "Risk-Off Signal" | "Pre-selected from the Daily Position Monitor: the {US\|UK} market is in a risk-off regime." |

The user can change the reason. The note hides once they do (existing rule). Outside the queue, `ExitModal` keeps using `getExitCondition()` unchanged.

### 2.4 Failure state

If `POST /positions/{id}/exit` fails (network error or any non-2xx):

- `ExitModal` **stays open** with every entered value intact. The queue is kept.
- An inline error appears at the top of the modal body: `AlertTriangle` icon plus "Could not record the exit for {TICKER}. Nothing was changed for this position." If the response carries a `detail` string, it follows on a second line. `role="alert"`, `data-testid="exit-error"`. Light/dark tokens: `text-rose-700 dark:text-rose-400` on `bg-rose-50 dark:bg-rose-500/10`, border `border-rose-200 dark:border-rose-500/30`. Contrast: 5.72:1 light, 6.09:1 dark (over the `slate-900` modal).
- The confirm button re-enables, so the user can retry. A retry that succeeds continues the queue.
- Cancel returns to the Monitor with the failed position and the rest of the queue still selected (§2.1 step 4).

While a submit is in flight, the confirm button is disabled and reads "Exiting…". This prevents double submission.

### 2.5 What does not change

- The Monitor's suggestion list, its "Stop price hit" / "Market risk off" reasons and its footer counts.
- `ExitModal`'s fields, validation and fee display.
- No exit is ever submitted without the user confirming each `ExitModal` (§8.1 "requires manual confirmation"; §13).

## 3. §13 Compliance

Every exit still needs explicit user confirmation, one position at a time. The flow removes a broken bulk write and adds no automated action.

## 4. Frontend Spec Impact

`positions.md` v2.19 → v2.20: new §Daily Position Monitor Exit Queue after §Exit Dialog Pre-Selection and Deep Link. `ExitModal` is specified in `positions.md`. The Monitor has no spec of its own, and its only exit path is this queue.

## 5. Obligations for Sprint Execution

- Delete `Position.update` from `base44Client.js`. No code path may call `PATCH /positions/{id}` (AC 1). `ST-23`'s openapi check depends on it.
- `ExitModal` gains two optional props: an explicit pre-selection with its note, and queue position `{i, n}`. Both default to today's behaviour.
- `ExitModal` must surface the submit error (§2.4). Today it calls `onConfirm` and has no failure path. The Positions page can adopt the same error state. That is not required by this story.

## 6. Testability (CLAUDE.md §2)

- Playwright (AC 4a): a mocked Monitor with one stop suggestion. Select it, confirm, see "Stop Loss Hit" pre-selected, submit, then assert one `POST /positions/{id}/exit` and that the position leaves the open list.
- Playwright (AC 4b): the same with the exit mocked to 500. `exit-error` is visible, the modal stays open with its values, and Cancel reopens the Monitor with the position still selected.
- Beyond the slice ACs (add these or file a backlog item before the PR opens): with two positions queued, `exit-queue-progress` reads "Exit 1 of 2" and then "Exit 2 of 2".

## 7. Observation (not in this story's scope)

The Monitor's own stop predicate (`MonitorModal.js::getPositionStatus`) compares `current_price` with `stop_price` and ignores the grace period. §8.1 says the stop-loss trigger is "active only after the grace period", and the shared predicate `getExitCondition()` uses `current_trailing_stop` and `grace_period`. So the Monitor can suggest "Stop Loss Hit" during grace. Recommend filing with `/backlog-add` at Sprint Planning: switch the Monitor's suggestions to `getExitCondition()`.

## 8. Approval

Head of UX & Design: confirmed, 2026-10-16.
Product Owner: confirmed, 2026-10-16.
