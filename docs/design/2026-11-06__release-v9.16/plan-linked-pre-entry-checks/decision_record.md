**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-06__release-v9.16
**Stories:** ST-05 (EPIC-02, BLG-FE-271)
**Supersedes:** §2.1, "When the panel shows", of `docs/design/2026-11-03__release-v9.15/trade-entry-pre-entry-checks/decision_record.md`, for the plan-linked rows only

# Decision Record — Pre-Entry Checks on Plan-Linked Trade Entry

## 1. Problem

Trade Entry hides the pre-entry panel when the linked plan has a stored `pre_entry_validation_snapshot`, and shows "Pre-entry checks were run on the linked plan." in its place (`position_form.md` v1.13). The Trade Plan acknowledgement is advisory only. A plan saved over a WARN/FAIL could therefore become a position without the acknowledgement that `strategy_rules.md` §4.2.1 v1.23 requires. `ESC-CLOSE-20261106-01` (Strategy Rules & System Intent Owner, 2026-11-06, option (a)) ruled that the rule applies to this route.

**Gate finding:** `TradePlan.js` never sends `pre_entry_validation_snapshot` on save. The field appears nowhere in `src/` except `TradeEntry.js:166`. Plans saved from the app therefore have no snapshot, so today every plan-linked entry already shows the panel, and the "on-plan line" row can't be reached from the app. ST-05's AC 1 needs both branches, so the plan form must start writing the snapshot (§2.1).

## 2. Decision

### 2.1 The plan stores a dated snapshot

When a plan is saved (create or edit) and the Pre-Entry Validation panel holds a result, `TradePlan.js` sends:

```json
"pre_entry_validation_snapshot": {
  "captured_at": "<ISO-8601 UTC, when the result was received>",
  "advisory_status": "pass | warn | fail",
  "checks": [ { "rule": "...", "status": "...", "detail": "..." } ],
  "inputs": { "quantity": 50, "entry_price": 150.0, "stop_price": 142.0 }
}
```

No result (shares not entered, still loading, or endpoint error) → the field is sent as `null`. On edit, the snapshot is replaced with the current result, or cleared if there is none. The backend stores the value as it does now. No schema change is needed: the column is JSONB, and `data_model.md`'s row already describes it.

### 2.2 When Trade Entry shows the panel (plan linked)

Evaluated when the plan is linked, whether by prefill or by "Link to trade plan". **Stale** means `captured_at` is more than **24 hours** before that moment.

| Linked plan's snapshot | Trade Entry shows |
|------------------------|-------------------|
| None, or no `captured_at` | Panel (unchanged row) |
| Stale | Panel, with reason line "The linked plan's checks are more than a day old, so they have been run again." |
| Fresh, `advisory_status: pass` | On-plan line: "Pre-entry checks were run on the linked plan." (unchanged) |
| Fresh, `warn`/`fail`, plan `pre_entry_override_acknowledged: true` | On-plan line: "Pre-entry checks were run on the linked plan, and their warnings were acknowledged there." |
| Fresh, `warn`/`fail`, plan acknowledgement not `true` | Panel, with reason line "The linked plan's checks had warnings that were not acknowledged." |

**Product Owner decision (the user, in session, 2026-11-06):** the age is 24 hours.

- **Reason line:** above the panel header, `data-testid="pre-entry-rerun-reason"`, `text-xs text-slate-600 dark:text-slate-400`. It shows only when the panel is shown because of the plan.
- **Panel:** when it shows, the checks run against Trade Entry's own inputs, as on the no-plan route. Branch A applies unchanged: the checkbox shows on WARN/FAIL, Submit is disabled until it is ticked, the `pre-entry-ack-required` helper shows, and saving writes one `pre_entry_override` event (`source: trade_entry`). An endpoint failure or a loading check never disables Submit.
- **One panel:** the panel and the on-plan line never show together. Linking or unlinking a plan switches rows without losing form state.

## 3. §13 Compliance

These are the existing deterministic §4.2 rules (SI-01 §13 review; §13.4). The acknowledgement is not a hard gate (`strategy_rules.md` §4.2.6 v1.23). No new §13 review is needed.

## 4. Frontend Spec Impact

- `components/position_form.md` v1.13 → v1.14: §Pre-Entry Checks "When it shows" table, the reason line, and the 24-hour age.
- `pages/trade_plan.md` v1.21 → v1.22: new §5e "Pre-Entry Snapshot on Save".

## 5. Obligations for Sprint Execution

- Add a pointer under §2.1 of the v9.15 record (`trade-entry-pre-entry-checks/decision_record.md`) to this record. This is in ST-05's scope ("update … the design record").
- `data_model.md`'s `pre_entry_validation_snapshot` row may name the four keys. It is optional, because the description is already correct.
- ST-05 AC 3 (the `strategy_rules.md` Known-deviation closure) follows the slice's case (c) route. It is not a design matter.

## 6. Testability (CLAUDE.md §2)

Playwright, with the plan response mocked and the clock fixed:
- Fresh pass snapshot → on-plan line, no panel.
- Fresh fail with no acknowledgement → panel and reason line, Submit disabled until ticked.
- Fresh fail with the plan acknowledged → on-plan line with "acknowledged there".
- Snapshot captured 25 h earlier → panel and stale reason line.
- No snapshot → panel and no reason line.
- Trade Plan save sends a snapshot with `captured_at` when the panel holds a result, and `null` when it doesn't.

Backend test: saving the plan-linked entry with the acknowledgement writes one `pre_entry_override` event with `source: trade_entry`.

## 7. Approval

Head of UX & Design: Approved (agent-mediated, Design Gate Engine, 2026-11-06). Product Owner: Approved (the user, in session, 2026-11-06), 24-hour age.
