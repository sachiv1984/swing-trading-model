Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-06

# Execution Escalations — 2026-10-06__release-v9.10

> EPIC-03 branch copy. `ESC-EXEC-20261006-01`/`-02` (EPIC-01) live on the EPIC-01 branch; union the files at merge (CLAUDE.md §8).

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
