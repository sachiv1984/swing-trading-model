Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-06

# Execution Escalations — 2026-10-06__release-v9.10

## ESC-EXEC-20261006-01

- **Raised at:** 2026-10-06T15:08:11Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-06__release-v9.10
- **Step:** STEP 3.1.D (EPIC-01 execution loop, raised at sprint start per `sprint_planning_notes.md` Execution Sequence)
- **ST/EPIC item:** ST-01 / EPIC-01 (BLG-BE-138)
- **Trigger type:** Strategy
- **Blocking statement:** ST-01 AC 2 needs a parameter-authority ruling before the single parameter source can be built, because the source differs by outcome. (a) The §11 values are fixed: one backend constants source, and Settings shows them read-only. (b) A sanctioned personal override recorded in `strategy_rules.md` §12: the `settings` row becomes the one source, and every path must read it, including the nightly job, which hard-codes 5×/2× today. (c) Changeable only through a §12.3 change record: same build as (a), with `strategy_rules.md` §12 wording. Today the paths disagree. `analyze_positions` reads the editable `settings` row. `run_nightly_trailing_stop_update` hard-codes `_INITIAL_ATR_MULT = 5.0` / `_PROFIT_ATR_MULT = 2.0`. `should_exit_position` is called with a literal `grace_period_days=10`. `grace_service` hard-codes `10 - holding_days`. `add_position` hard-codes `multiplier=5.0`. The Settings form seeds `5`/`2`/`3` and Trade Entry seeds `atr_multiplier_initial: 2`. Choosing an outcome is a strategy-boundary decision, so the engine does not make it.
- **Engine recommendation (non-binding):** (a). §11 already says the values "must be consistent across production backtests, live system logic, and reported performance metrics", and §12.3 already governs changing them. An editable per-user override (b) would make the live stop path diverge from the backtest by design. (a) and (c) build the same code; (c) only adds §12 wording.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** A dated ruling (a), (b) or (c), recorded in this escalation's resolution and in ST-01's QA evidence. For (b) or (c), the ruling also authorises the `strategy_rules.md` §12 edit and its Change Log row, which ST-05's registry rule then covers. AC 1 (production read, `DEL-20261006-01`) and AC 6 (Product Owner correction decision for any diverged stop) are tracked separately and do not block the ruling.
- **Dependants:** ST-03 (settings-change text), ST-06 (displayed multiplier), ST-07 (Trade Entry fallback multiplier), ST-05 (registry entry if §12 changes).
- **SLA due-by:** 2026-10-09T15:08:11Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolved at:** 2026-10-06T17:30:09Z
- **Resolved by:** Strategy Rules & System Intent Owner (direct user ruling, 2026-10-06: "Go with (a), start building")
- **Resolution summary:** Outcome (a), fixed parameters. The §11 values (10-day grace, 5× / 2× ATR, 14-day ATR) are held in one backend source, `backend/utils/strategy_parameters.py`, read by every live stop path. They are never read from the editable `settings` row. Settings shows them read-only. No `strategy_rules.md` §12 change is needed, so ST-05's registry rule is not triggered. AC 1 (production read, `DEL-20261006-01`) and AC 6 (Product Owner correction decision, only if production drifted) remain open.

## ESC-EXEC-20261006-02

- **Raised at:** 2026-10-06T15:08:11Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-06__release-v9.10
- **Step:** STEP 3.1.D (EPIC-01 execution loop, raised at sprint start)
- **ST/EPIC item:** ST-05 / EPIC-01 (BLG-BE-137)
- **Trigger type:** Strategy
- **Blocking statement:** ST-05 AC 1 needs a ruling on strategy-version registry coverage. `backend/strategy_version_registry.py` ends at 1.4. `strategy_rules.md` has Change Log rows 1.5–1.14, so `get_current_strategy_version()` stamps every new position and trade plan as 1.4. The registry docstring and `data_model.md` DS-11 both say the registry is updated in the same commit as any new Change Log row. Either that obligation has been breached ten times, or there is an unwritten exemption for documentation-only versions. The two options: (1) register only versions that change behaviour or parameters, and tag each Change Log row as behavioural or documentation-only; (2) register every version, adding 1.5–1.14 with effective dates, which changes `strategy_version_at_entry` stamping and SI-04 comparison attribution from now on.
- **Engine recommendation (non-binding):** (1). The registry's purpose is to group trades by the strategy that produced them (SI-04). A wording-only version produces identical trades, so registering it would split comparable trades into separate cohorts.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** A dated ruling (1) or (2), recorded in this escalation's resolution. The engine then aligns the registry docstring, DS-11 and `strategy_version_comparison_contract.md` Implementation Note 2, and replaces the hard-coded `len == 5` test with one derived from the Change Log.
- **SLA due-by:** 2026-10-09T15:08:11Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolved at:** 2026-10-06T17:40:37Z
- **Resolved by:** Strategy Rules & System Intent Owner (direct user ruling, 2026-10-06: "Go with behaviour-only for ST-05, build it")
- **Resolution summary:** Option (1), behaviour/parameter-changing versions only. The registry stays at 1.0–1.4, and 1.5–1.14 are classified documentation-only in `DOCUMENTATION_ONLY_VERSIONS`. 1.1 is grandfathered (zero-width window). The classification sits beside the registry rather than as a tag on `strategy_rules.md`'s Change Log rows, because that file is outside Sprint Execution's write scope. The test enforces the same rule either way. No `strategy_version_at_entry` stamping or SI-04 attribution changes.

## ESC-EXEC-20261006-03

- **Raised at:** 2026-10-06T15:37:51Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-06__release-v9.10
- **Step:** STEP 3.1.D (EPIC-03 execution loop, raised at sprint start)
- **ST/EPIC item:** ST-11 / EPIC-03 (BLG-SPEC-185)
- **Trigger type:** Strategy
- **Blocking statement:** ST-11 AC 1 needs a ruling: is the Positions lifecycle badge a `strategy_rules.md` §9 state machine, or a display overlay that defers to §9? §9 defines GRACE (days 0–9), LOSING (post-grace, P&L ≤ 0), PROFITABLE (post-grace, P&L > 0) and EXITED. The badge adds EXIT ZONE (price ≥ entry + 2R), and after grace it uses ±0.5 ATR bands, so a position within 0.5 ATR of entry shows UNKNOWN (`flat_after_grace`) where §9 would say LOSING or PROFITABLE. ST-12 (`0e8a431b`, this branch) has already aligned the grace part with §6.2 (calendar days, grace first), so only the post-grace semantics remain open. §1 says §9 prevails.
- **Engine recommendation (non-binding):** overlay that defers to §9, with no §9 amendment. After grace, LOSING/PROFITABLE follow §9's P&L sign, so the ±0.5 ATR neutral zone and `flat_after_grace` are removed. EXIT ZONE stays as a display sub-state of PROFITABLE. The registry states this. (Making the overlay canonical would mean amending §9 under §16's change-justification template, a heavier change for a display element.)
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** A dated ruling recorded here and in ST-11's QA evidence. If the overlay becomes canonical, the ruling also authorises the §9 amendment and its Change Log row (ST-05's registry rule then applies). The engine then updates `position_lifecycle_states_registry.md`, plus the code and `flat_after_grace` contract value if §9 governs.
- **Dependants:** ST-12 post-grace copy (`flat_after_grace` is dropped from the contract if §9 governs); ST-05 (registry entry if §9 changes).
- **SLA due-by:** 2026-10-09T15:37:51Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Open

## ESC-EXEC-20261006-04

- **Raised at:** 2026-10-06T15:37:51Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-06__release-v9.10
- **Step:** STEP 3.1.D (EPIC-03 execution loop, raised at sprint start)
- **ST/EPIC item:** ST-13 / EPIC-03 (BLG-GOV-365); gates ST-14 (BLG-BE-136)
- **Trigger type:** Strategy
- **Blocking statement:** ST-13 needs a dated ruling, recorded as an addendum to `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`, on two shipped behaviours that `strategy_rules.md` §13.3 does not cover. (1) **UK tickers:** §13.3 recognises only a scheduled earnings date "per §4.2.3", and §4.2.3 is US-only. `gap_risk_service.get_gap_risk` applies the earnings trigger to every market. (2) **Day 0:** the trigger fires at `days_until_earnings == 0`. For a before-open release the gap has already happened, which §13.3 excludes, and the code cannot tell before-open from after-close releases.
- **Engine recommendation (non-binding):** (1) restrict the earnings trigger to US positions, which matches §4.2.3 as written and needs no `strategy_rules.md` change; (2) drop day 0, so the flag covers earnings due from the next trading session up to the next trading day. A Friday position with Monday earnings still flags, which ST-14 AC 2 requires. Neither choice needs a §13.3/§4.2.3 wording change.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** A dated addendum to the v9.9 §13 review record with both rulings. If either ruling changes `strategy_rules.md` §13.3/§4.2.3 wording, the ruling authorises that edit, its Change Log row and the §15 grep. ST-14 then implements the ruled behaviour, its weekend-hold disposition and the label alignment. ST-14 AC 6 also needs this owner's sign-off that Binding Conditions 1–8 still hold.
- **SLA due-by:** 2026-10-09T15:37:51Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Open
