Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-21

# Execution Escalations — 2026-08-21__release-v9.0

Append-only. Do not edit previous entries.

---

## ESC-EXEC-20260821-01

- **Raised at:** 2026-08-21T14:26:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-08-21__release-v9.0
- **Step:** STEP 3 (Execution Loop) — EPIC-01
- **ST/EPIC item:** ST-03 / EPIC-01
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-03 ("Decide 'linked journal entries' data source for the AI Post-Trade Debrief") requires an explicit Product Owner decision before any implementation can proceed: should the debrief's "linked journal entries" continue to source from `red_flag_events` only (current implementation, `backend/services/debrief_service.py::_journal_context_for_trade`), be changed to also/instead draw on `trade_history.entry_note`/`exit_note` (the fields the UI already labels "Trade Journal" one section above the Debrief panel in `TradeHistoryTable.js`), or both. This is BLG-BE-108, raised by an agent-mediated Product Owner review during ST-06/PR #1460 (v8.9) as a plausible-but-debatable reading of that story's own AC, not yet resolved.
- **Owning authority:** Product Owner
- **Unblock criteria:** Product Owner decision recorded (keep `red_flag_events`-only, add entry/exit notes, or both). If implementation changes: `tests/test_debrief_service.py` covers the new data source; full backend suite re-verified passing; spec updated to reflect the confirmed interpretation.
- **SLA due-by:** 2026-08-24T14:26:00Z (72h — scope/product decision, not a lifecycle/strategy/quality violation)
- **Blocks execution:** No — other EPIC-01/EPIC-02+ items continue; only ST-03 itself is parked.
- **Disposition:** Open
- **Resolution summary:** (complete when closing)

---

## ESC-EXEC-20260821-02

- **Raised at:** 2026-08-21T15:04:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-08-21__release-v9.0
- **Step:** STEP 3 (Execution Loop) — EPIC-02
- **ST/EPIC item:** ST-07 / EPIC-02
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-07 ("Decide and apply treatment for trade_plans.setup_type='Other' conflating user-chosen-Other with never-classified", BLG-FEAT-93) requires an explicit Product Owner decision: either implement a way to distinguish "explicitly Other" from "never classified" (e.g. a `setup_type_source` field, a distinct enum value, or a null-preserving default used only in reporting) — and if so, whether to also extend the default to `PUT /trade-plans/{id}`, not just `POST` — or make an explicit, documented decision to accept the conflation with rationale. This is a design tradeoff affecting future `win_rate_by_setup_type` (SI-02) analytics precision, not something the engine should decide unilaterally.
- **Owning authority:** Product Owner
- **Unblock criteria:** Decision recorded (implement a distinguishing mechanism, or accept-as-is with documented rationale). If implemented: `win_rate_by_setup_type`'s future query logic (or its predesign doc) updated to reflect the distinction; Product Owner sign-off.
- **SLA due-by:** 2026-08-24T15:04:00Z (72h — scope/product decision, not a lifecycle/strategy/quality violation)
- **Blocks execution:** No — other EPIC-02+ items continue; only ST-07 itself is parked.
- **Disposition:** Open
- **Resolution summary:** (complete when closing)

---

## ESC-EXEC-20260821-01 — Resolution (Addendum)

- **Refers to:** ESC-EXEC-20260821-01 above. This file is append-only — recording the resolution as a new entry rather than editing the original.
- **Resolved at:** 2026-08-21T22:00:00Z (well within the 72h SLA due 2026-08-24T14:26:00Z)
- **Disposition:** Resolved
- **Resolution summary:** Product Owner decision: "linked journal entries" (BLG-BE-108) draws on **both** sources, not one or the other — `backend/services/debrief_service.py::_journal_context_for_trade()` now includes the trade's own `entry_note`/`exit_note` (the fields the UI itself labels "Trade Journal", directly adjacent to the Debrief panel in `TradeHistoryTable.js` — the more literal reading of "journal entries") FIRST, followed by Red Flag Journal events for the ticker (the pre-existing implementation, retained rather than dropped). Both are free text/labels, not numbers — no impact on `numeric_cross_check` (§13 Condition 2 sourcing discipline applies only to quantitative claims). Evidence: `tests/test_debrief_service.py` (6 new tests, `TestJournalContextForTrade`, all passing); `docs/specs/api_contracts/trade_endpoints.md` v2.5.0→v2.5.1 documents the sourcing clarification. Full backend suite: 1282 passed, 5 skipped, zero regressions. Commit `94b759cb` (EPIC-01). See `execution_state.json` ST-03 for the full record.

---

## ESC-EXEC-20260821-02 — Resolution (Addendum)

- **Refers to:** ESC-EXEC-20260821-02 above. This file is append-only — recording the resolution as a new entry rather than editing the original.
- **Resolved at:** 2026-08-21T22:00:00Z (well within the 72h SLA due 2026-08-24T15:04:00Z)
- **Disposition:** Resolved
- **Resolution summary:** Product Owner decision: accept the `setup_type="Other"` conflation between user-chosen-Other and never-classified (`BLG-FEAT-93`) — no new distinguishing field, enum value, or schema change. `win_rate_by_setup_type` is a future, unbuilt SI-02 predesign query, itself still far from its own ≥20-linked-trades trigger gate — a distinguishing mechanism now would be speculative complexity ahead of the feature that would consume it; re-open when that feature is actually scheduled. `PUT /trade-plans/{id}` is explicitly NOT extended with `POST`'s null→"Other" default (a client that wants to reset it sends `"Other"` directly — matches every other field's null-means-don't-touch semantics rather than special-casing this one field). Evidence: `docs/product/decisions/setup-type-other-conflation-decision--2026-08-21.md` (full rationale); `docs/specs/api_contracts/trade_plan_endpoints.md` v0.13→v0.14; 2 new regression tests (`TestSetupTypePutDoesNotDefault`) lock in the accepted behaviour. Full backend suite: 1263 passed, 10 skipped, zero regressions. Commit `6bc1add4` (EPIC-02). See `execution_state.json` ST-07 for the full record.
