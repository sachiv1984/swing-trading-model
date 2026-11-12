**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-11__release-v9.17
**Stories:** ST-12 (BLG-FE-278), ST-13 (BLG-FE-281), ST-14 (BLG-FE-282) — EPIC-05

# Decision Record — Trade Plan Found Defects

## 1. Scope of this record

Three P2 defects carried from v9.16 (Carry-Forward #1). Each fixes Trade Plan behaviour against an existing spec, and ST-12 and ST-14 change what the form shows, so both are designed here. ST-13 changes no screen; its spec correction is recorded here so all three stay together. ST-07's section index edits the same file (`TradePlan.js`, RISK-01); nothing here depends on it.

Spec impact: `trade_plan.md` v1.24 → v1.25 (§5a.3, §5e, §5f); `research_view.md` v1.4 → v1.5 (§4.7).

## 2. Reset the acknowledgement when the result changes

### 2.1 What the user sees

The interaction is the same whichever storage option the Strategy Rules & System Intent Owner chooses before the seal (RISK-05: clear on change, or keep the acknowledgement in the dated snapshot).

- **Result key:** the Pre-Entry Validation result is identified by its `advisory_status` and the set of `{rule, status}` pairs in `checks`. `detail` text and `captured_at` are not part of the key, so a refetch with the same outcome does not count as a change.
- **When the key changes** and the new `advisory_status` is `warn` or `fail`, the acknowledgement box is unticked. Under the box, one line reads: "The check results changed. Review them and tick again to acknowledge." (`text-xs text-app-warning`, `data-testid="acknowledgement-reset-note"`). The line stays until the box is ticked or the result returns to `pass`.
- When the new status is `pass`, the box is hidden as today, and its value is saved as `false`.
- **Loading an existing plan** does not count as a change: the stored acknowledgement is shown if the first result received has the same key as the plan's stored snapshot. If the key differs (the market moved since the plan was saved), the box starts unticked with the note.
- Save stays enabled throughout. The acknowledgement is advisory (`trade_plan.md` §5e; `strategy_rules.md` §4.2.6).

### 2.2 Storage options (owner's choice, recorded in `sprint_backlog.md`)

| Option | Saved fields | Trade Entry reads |
|--------|--------------|-------------------|
| (a) Clear on change | `pre_entry_override_acknowledged` set `false` whenever the key changes, as §2.1 | Unchanged (`position_form.md` v1.14 §Pre-Entry Checks) |
| (b) Snapshot-bound | `pre_entry_validation_snapshot.acknowledged: true\|false` written with the snapshot; the top-level flag mirrors it | The snapshot's own flag; a snapshot without the field counts as not acknowledged |

Either option meets both slice ACs. If the shared `PreEntryValidationPanel.js` is changed rather than `TradePlan.js` alone, Trade Entry gets the same reset, and ST-12 records whether that meets `BLG-FE-269` AC 1 (RISK-07).

## 3. Research View carries the market

No visible change other than the correct market. `Research.js`'s "Create Trade Plan" navigates to `/TradePlan?ticker={ticker}&market={market}`, where `market` is the research response's `market` (`US` or `UK`). "View full plan" uses `/TradePlan?edit={id}&ticker={ticker}`; edit mode loads the plan's stored market, so it needs no parameter, and the story confirms that by test.

`research_view.md` §4.7 still names the pre-v8 route `/trade-plans/new?ticker={ticker}`. It is corrected to the live route with `market` at this gate.

## 4. Pre-fill the stop and state the stored stop

### 4.1 Pre-fill

Already specified in `trade_plan.md` §5a.3, not built. Restated precisely:

- **When:** creation form only, when a linked signal exists (§5a.1: a "Plan this" `signal_id`, or the watchlisted lookup) and a suggested stop can be computed.
- **Value:** the same value the Signal Context panel shows as "Suggested stop", from one shared helper (`getSuggestedStop(signal)`, extracted from `SignalContextPanel.js`): the signal's `initial_stop` when present, otherwise `current_price − INITIAL_ATR_MULTIPLIER × atr_value`. Rounded to 2 decimal places in the plan's native currency. The pre-fill and the panel therefore never disagree.
- If the signal has no suggested stop when the form opens, nothing is filled.
- **Never overwrites:** once the user has typed in Planned Stop Price (including clearing it), the field is theirs. Changing the entry afterwards does not move the stop.
- A filled value is plain field content. It gets no special styling; the Signal Context panel already shows "Suggested stop".

### 4.2 Stored-stop line

The **§5 stop** for the plan is Planned Entry Price − `INITIAL_ATR_MULTIPLIER` × the linked signal's `atr_value` (what Trade Entry will compute at that entry). When both are known and the Planned Stop Price differs from it by more than 0.005 in native currency:

- A line appears directly under the suggested size line (§5f), `data-testid="plan-stored-stop-note"`, `text-sm text-app-warning`:
  "Trade Entry will store a stop of {§5 stop} (entry − 5×ATR, §5). The suggested size above uses your stop of {typed stop}."
- Values are currency-formatted in the plan's market currency (`formatCurrency`).
- When the stop matches, or no ATR is known, the line is absent.
- The line is advisory. It changes no field, does not recompute the suggested size against the §5 stop, and does not block Save. (Recomputing would mean a second sizing request; the line tells the user which stop sizing assumed, which is what the gap was.)

### 4.3 Known deviation

`trade_plan.md`'s `DEV-v9.16-ST27-01` Known Deviations row is marked resolved by ST-14 when it merges (slice AC 4), not at this gate.

## 5. §13 Compliance

ST-12 restores the existing advisory acknowledgement flow (`strategy_rules.md` §4.2.1, §4.2.6); it adds no gate. ST-14 pre-fills a value the spec already names and states a deterministic §5 calculation; both are editable and advisory, as `trade_plan.md` §10.6a. ST-13 is a parameter fix. No AI call is added or changed.

## 6. Testability (CLAUDE.md §2)

- **ST-12:** Playwright: acknowledge a WARN, edit shares so a new FAIL appears → box unticked and `acknowledgement-reset-note` visible; save without ticking, open Trade Entry from the plan → panel shown with the unacknowledged reason line. A refetch with the same result keeps the box ticked.
- **ST-13:** Playwright: Research View for `VOD.L` → "Create Trade Plan" → market UK and £; for `AAPL` → US and $.
- **ST-14:** Playwright: "Plan this" and watchlisted-lookup routes pre-fill entry − 5×ATR; a typed stop survives an entry change; a typed stop that differs shows `plan-stored-stop-note` with both values; a matching stop shows no note.

## 7. Approval

Head of UX & Design: confirmed, 2026-11-11 (agent-mediated, Design Gate Engine).
Product Owner: confirmed, 2026-11-11 (the user, in session).
ST-12's storage option (§2.2) is the Strategy Rules & System Intent Owner's, recorded before the sprint seals (RISK-05).
