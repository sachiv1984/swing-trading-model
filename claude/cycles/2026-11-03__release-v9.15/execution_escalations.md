Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-04

# Execution Escalations — 2026-11-03__release-v9.15

## ESC-EXEC-20261104-01

- **Raised at:** 2026-11-04T10:56:15Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-03__release-v9.15
- **Step:** STEP 3.1.D (EPIC-01 execution loop, raised at sprint start per `sprint_backlog.md` ST-01 Notes and `stage4_backlog_slice_addendum.md` ST-01, RISK-07)
- **ST/EPIC item:** ST-01 / EPIC-01 (BLG-FE-244)
- **Trigger type:** Strategy
- **Blocking statement:** ST-01 AC 2 says that with a risk-off or unknown regime "save requires the acknowledgement". `strategy_rules.md` §4.2.6 (binding) says the advisory panel "must never prevent, gate, or auto-reject" a submission and that any hard submission gate needs a new §13 review. §4.2.1 (v1.20) says new entries in an unknown-regime market "are blocked". The Trade Plan path's acknowledgement does not disable Save today. A dated ruling is needed: **Branch A (acknowledge to proceed)** — Submit is disabled until a WARN/FAIL is acknowledged; the ruling states that a one-click, user-passable acknowledgement is not a "hard submission gate" under §4.2.6 (and, if needed, clarifies §4.2.1's "are blocked" wording), applied as a case (c) `strategy_rules.md` write confirmed at seal; or **Branch B (advisory only)** — Submit stays enabled as on the plan path, and AC 2 is met by the regime check showing FAIL/unknown with the acknowledgement offered. Both are designed in `docs/design/2026-11-03__release-v9.15/trade-entry-pre-entry-checks/decision_record.md` §2.3.
- **Engine recommendation (non-binding):** see the in-session question; this is a strategy call.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** a dated ruling, Branch A or Branch B, recorded in this escalation's resolution and in ST-01's QA evidence. Under Branch A with a text clarification, the engine applies the case (c) `strategy_rules.md` write with its Change Log row and `STRATEGY_VERSION_REGISTRY` entry in the same commit.
- **SLA due-by:** 2026-11-07T10:56:15Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-04T11:00:36Z):** Strategy Rules & System Intent Owner ruling, given in-session by the user acting in that role, dated 2026-11-04: **Branch A, acknowledge to proceed.** On Trade Entry, when any pre-entry check is WARN or FAIL (including a risk-off or unknown regime), Submit is disabled until the user ticks the acknowledgement. A one-click, user-passable acknowledgement is not a "hard submission gate" under §4.2.6, and §4.2.1's "are blocked" for an unknown regime means the entry cannot be saved until the FAIL is acknowledged (or the regime is measured). The engine recommended Branch A: it carries out v1.20's fail-closed intent while keeping the decision with the user, as §3 requires. Applied by ST-01 as a case (c) `strategy_rules.md` write (§4.2.1, §4.2.6) with a Change Log row and a `STRATEGY_VERSION_REGISTRY` entry. ST-01 reclassified `autonomous`.

## ESC-EXEC-20261104-02

- **Raised at:** 2026-11-04T14:51:24Z (raised and ruled in the same in-session exchange)
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-03__release-v9.15
- **Step:** §5.3 agent-mediated Director of Quality review of EPIC-01, finding 2 (Blocked)
- **ST/EPIC item:** ST-06 / EPIC-01 (BLG-BE-173)
- **Trigger type:** Strategy
- **Blocking statement:** ST-06 AC 1 says `atr_trail_stop` "equals the value `calculate_trailing_stop` would produce from the same inputs". The endpoint passes `current_stop = -inf`, so it reports the §7.2 candidate without ratcheting against the stored stop. Example: entry 100, price 130, ATR 4, stored stop 125 gives 122 and "no action required", where `calculate_trailing_stop` with the stored stop returns 125. A ruling is needed on whether the un-ratcheted candidate is the intended value.
- **Engine recommendation (non-binding):** rule the un-ratcheted candidate as intended. A ratchet would make `trail_difference` always ≥ 0 and the "below current stop — no action required" branch unreachable.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** a dated ruling recorded here and cited in ST-06's QA evidence Deviations cell.
- **SLA due-by:** 2026-11-07T14:51:24Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-04T14:51:24Z):** Strategy Rules & System Intent Owner ruling, given in-session by the user acting in that role, dated 2026-11-04: **the Trail Stop modal's `atr_trail_stop` is the un-ratcheted §7.2 candidate** — `calculate_trailing_stop` with the §11 multipliers and the breakeven floor, but not raised to the stored `current_stop`. `trail_difference` stays signed so the modal can say when the candidate is below the current stop. ST-06 AC 1 is met under this reading; no code change and no backlog remainder. No `strategy_rules.md` text change is needed: §7.2's ratchet governs the stored stop, which this read-only endpoint does not write.

## ESC-EXEC-20261104-03

- **Raised at:** 2026-11-04T19:29:15Z (raised and ruled in the same in-session exchange)
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-03__release-v9.15
- **Step:** STEP 3.1.D (EPIC-03 execution loop, raised at EPIC start per `sprint_backlog.md` ST-20 Notes)
- **ST/EPIC item:** ST-20 / EPIC-03 (BLG-BE-171)
- **Trigger type:** Strategy
- **Blocking statement:** ST-20's first sub-step needs a ruling: is a behavioural strategy version's effective date the ruling date or the date its code reaches production? `strategy_version_at_entry` is stamped by `get_current_strategy_version()` from the registry in the live code. v1.15 was ruled 9 October 2026, but PR #1970 merged to `main` (and deployed) on 12 October 2026 (`e07d2a04`, 12:58Z), so positions entered 9–11 October were stamped "1.4" while their `entry_date` falls in the v1.15 window. The same one-day lag exists for v1.17 (Change Log 16 October, PR #2071 merged 17 October) and v1.20 (29 October, PR #2131 merged 30 October); v1.21 and v1.23 reached `main` on their Change Log dates.
- **Engine recommendation (non-binding):** the deploy date. The stamp switches when the code deploys, so a deploy-date window agrees with the stamps by construction.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** a dated ruling recorded here; under the deploy date, ST-20 applies the case (c) `strategy_rules.md` Change Log row 1.15 Date write (confirmed at seal) with the matching registry `effective_date`.
- **SLA due-by:** 2026-11-07T19:29:15Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-04T19:29:15Z):** Strategy Rules & System Intent Owner ruling, given in-session by the user acting in that role, dated 2026-11-04: **a behavioural version's effective date is the date its code reaches production (merges to `main`, which deploys).** ST-20 records the rule in the `strategy_version_registry.py` docstring and moves v1.15's registry `effective_date` and Change Log row 1.15 Date to 12 October 2026 (case (c), confirmed at seal). The v1.17 and v1.20 one-day lags fall outside the seal's authorisation (row 1.15 only) and are filed as a follow-up backlog item. ST-20 reclassified `autonomous`.

## ESC-EXEC-20261104-04

- **Raised at:** 2026-11-04T19:29:15Z (raised and ruled in the same in-session exchange)
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-03__release-v9.15
- **Step:** STEP 3.1.D (EPIC-03 execution loop, raised at EPIC start per `sprint_backlog.md` ST-23 Notes, RISK-07)
- **ST/EPIC item:** ST-23 / EPIC-03 (BLG-SPEC-198)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-23's first sub-step needs a ruling on the canonical open-position `pnl` basis. The live computation (`calculate_position_pnl()`, used by `get_positions_with_prices()` and `portfolio_service.py`) is `(current_price − native_entry) × shares ÷ live_fx_rate` for US positions, with no `fees_paid` deduction. `data_model_positions_dictionary.md` v0.6 §5.2 and the `pnl` row say entry-time `fx_rate` and `− fees_paid`. Closed-trade realised P&L is `exit_proceeds_gbp − total_cost_gbp` (fees deducted, currency movement included), so neither matches it exactly.
- **Engine recommendation (non-binding):** the spec follows the code. This is a doc-only change, no displayed figure changes, and it fits the 0.5d estimate. The basis difference from realised P&L gets its own follow-up item.
- **Owning authority:** Data Model & Domain Schema Owner
- **Unblock criteria:** a dated ruling recorded here and in `data_model_positions_dictionary.md`'s decision record.
- **SLA due-by:** 2026-11-05T19:29:15Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-04T19:29:15Z):** Data Model & Domain Schema Owner ruling, given in-session by the user acting in that role, dated 2026-11-04: **the spec follows the code.** Open-position `pnl` is native P&L converted at the live GBP/USD rate (US) and is not net of `fees_paid`. Rationale: it is the figure every surface displays today, and changing it would change displayed P&L on several pages, which needs a design pass and more than the 0.5d budget. The difference from the realised (closed-trade) basis, which is fee-netted and includes currency movement on the principal, is recorded in the dictionary and filed as a follow-up backlog item. ST-23 reclassified `autonomous`.
