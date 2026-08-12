**Owner:** Financial Reporting & Records Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-08-12 (revised same day — see Revision History; original conclusion was corrected, not just annotated)
**Cycle:** 2026-08-11__release-v8.6
**Story:** ST-12 (EPIC-04)
**Delegation record:** DEL-20260811-02
**Backlog source:** BLG-BE-91's parent triage identified this as a follow-on correctness check

---

# Multi-Currency Cost-Basis Rounding Consistency Audit

## Scope

Systematically audit cost-basis rounding across every UK (`.L`) and US market call site: `position_service.add_position()` (entry), `position_service.exit_position()` (exit/partial exit), and `reports_service.py`'s P&L consumers (tax-year report, reconciliation report, monthly P&L), against `docs/specs/data_model.md`'s `positions`/`trade_history` schema — `entry_price NUMERIC(10,4)` vs `total_cost NUMERIC(12,2)` (two different precisions on the same row).

## Method

Traced every arithmetic step between a raw entry/exit price and a persisted `total_cost` value, for both markets, then wrote `tests/test_multi_currency_cost_basis_rounding_audit.py` to exercise the real `add_position()`/`exit_position()`/`calculate_realized_pnl()` functions (DB layer mocked with a round-trip that mimics `NUMERIC(12,2)` column rounding — Postgres rounds, not truncates, on every write) and empirically measure the drift.

## Findings

**Delegation's starting-point hypothesis (an entry-side US-vs-UK asymmetry) does not survive DB persistence.** `add_position()` computes `total_cost_gbp` unrounded in Python, and US positions pass through an extra FX-division step that UK positions don't. But `total_cost` is `NUMERIC(12,2)` on both `positions` and `trade_history` (`docs/specs/data_model.md` lines 70, 156) — every write is rounded to 2dp by Postgres regardless of how many unrounded arithmetic steps preceded it. The "3 rounding steps for US vs 1 for UK" claim is true of the *computation path* but produces no extra *persisted* imprecision — both land on the same single ±0.005 rounding tolerance. `test_us_and_uk_total_cost_both_land_on_a_2dp_value` confirms both markets' entry-side `total_cost` land on an exact 2dp value.

**The real rounding source is market-symmetric, not asymmetric: partial-exit cost allocation.** `exit_position()`'s `cost_per_share = total_cost / total_shares` then `exit_total_cost = cost_per_share * exit_shares` divides a GBP total by a fractional share count — this produces a repeating decimal for UK positions exactly as readily as for US ones (division by 3, 7, etc. is currency-agnostic). `calculate_realized_pnl()` independently re-derives the identical formula from the identical inputs — confirmed bit-for-bit consistent with `exit_position()`'s own computation (`test_realized_pnl_and_persisted_total_cost_use_identical_cost_per_share`), so this is not a second, additional source of drift.

**CORRECTED FINDING (this is the material change in this revision): the drift compounds, and is NOT reliably bounded to ≤£0.02.** The original version of this audit asserted the per-exit rounding error "does not compound across exits ... bounded to a per-exit tolerance, not accumulated," checked only against two small fixtures (a 3-share and a 7-share split of a £100 position). An agent-mediated Financial Reporting & Records Owner review of PR #1363 disproved this with a concrete counter-example: **37 sequential single-share exits of a £12,345.67 position drifted £0.12 — 6x the originally-asserted bound.** The mechanism: the pre-fix code computed `remaining_cost = total_cost - exit_total_cost` from the *unrounded* `exit_total_cost`, then independently rounded that remainder on write. The next exit then read the already-slightly-wrong `remaining_cost` as its new starting `total_cost` — small per-step errors can accumulate in one direction across many exits rather than cancelling out, growing roughly with exit count and position size rather than staying capped near a fixed penny-level bound.

**FIX APPLIED** (not just documented — this satisfies unblock criterion (a), "any inconsistency found is fixed," for this finding): `backend/services/position_service.py`'s `exit_position()` now rounds `exit_total_cost`/`exit_entry_fees` to 2dp immediately (matching the `NUMERIC(12,2)`/`NUMERIC(10,2)` columns they persist to), and derives `remaining_cost`/`remaining_fees` by **exact subtraction from the already-rounded starting total_cost/fees_paid** — not by independently rounding a second, separately-computed unrounded remainder. This "round once, derive the rest by exact subtraction" ordering makes the allocation telescope exactly: the sum of every `exit_total_cost` across a position's full partial-exit lifecycle reconstructs the original `total_cost` to the cent, for any share count, position size, or exit count. Verified against the exact counter-example (`TestExactTelescopingAllocation::test_regression_reviewer_counter_example_37_exits_of_large_position`) — post-fix drift is exactly £0.00, not just "under a bound." The same fix was applied to `fees_paid`, which goes through the identical proportional-split pattern and was equally exposed (`test_fees_paid_telescopes_exactly_too`).

**`reports_service.py` consumers introduce no additional drift.** The tax-year report, reconciliation report, and monthly P&L report all read back already-persisted (DB-rounded) `total_cost`/`pnl` values and apply `round(x, 2)` defensively (a no-op on an already-2dp value) — none re-derive cost basis independently. Notably, `get_reconciliation_report()` (`reports_service.py` ~line 287) already carries a pre-existing ±£0.01 tolerance (`matched = abs(round(system_total - export_total, 2)) <= 0.01`) for exactly this class of float-aggregation noise — an established codebase precedent that sub-penny/one-cent drift from proportional allocation is treated as immaterial by design, not a defect.

**Incidental observation (not a rounding-audit finding):** a full exit's `update_position()` call does not clear `positions.total_cost` — the field is simply never read again once `status == 'closed'`, so this has no financial-correctness impact. Noted for completeness; not filed as a backlog item since there is no reachable consumer of a closed position's `total_cost`.

## Regression coverage

`tests/test_multi_currency_cost_basis_rounding_audit.py` — 8 tests: `TestExactTelescopingAllocation` (`test_uk_position_drift_is_exactly_zero`, `test_us_position_drift_is_exactly_zero`, `test_drift_is_zero_and_symmetric_across_markets`, `test_regression_reviewer_counter_example_37_exits_of_large_position`, `test_regression_large_us_position_many_exits`, `test_realized_pnl_and_persisted_total_cost_use_identical_cost_per_share`, `test_fees_paid_telescopes_exactly_too`) and `TestEntrySideRoundingSymmetryAfterDbPersist::test_us_and_uk_total_cost_both_land_on_a_2dp_value`. Full backend suite confirmed green alongside these (1071 passed, 5 skipped).

## Determination

**Two findings, two different resolutions.** (1) The entry-side US-vs-UK asymmetry hypothesis does not survive DB-column rounding — documented as immaterial with a quantified bound, no fix needed, satisfying unblock criterion (b). (2) The partial-exit proportional-allocation drift **does compound and is not reliably bounded** — this was a real inconsistency, now **fixed** (exact-remainder derivation in `exit_position()`, covering both `total_cost` and `fees_paid`), satisfying unblock criterion (a). The original version of this determination incorrectly applied criterion (b) to finding (2) as well, based on an insufficiently adversarial test (only two small fixtures) — corrected after an agent-mediated review produced a disproving counter-example.

## Sign-Off

**Signed off by:** Financial Reporting & Records Owner (agent-mediated, §5.3)
**Date:** 2026-08-12 (original determination); revised 2026-08-12 same day after an independent agent-mediated review of PR #1363 disproved the original "bounded, non-compounding" claim for finding (2) with a concrete counter-example.
**Determination:** Audit complete — systematic (all named call sites covered). Finding (1): no fix needed, documented per criterion (b). Finding (2): real inconsistency, fixed per criterion (a), verified against the exact counter-example that disproved the original conclusion.

## Revision History

- **2026-08-12 (original):** Audit concluded no code fix was needed for either finding; finding (2)'s "bounded ≤£0.02, non-compounding" claim was checked only against two small fixtures.
- **2026-08-12 (revised, same day):** Agent-mediated Financial Reporting & Records Owner review of PR #1363 produced a counter-example (37 exits of a £12,345.67 position, £0.12 drift) disproving finding (2)'s original claim. Fix applied (exact-remainder derivation); this document, the test file, and the delegation log were all revised to reflect the corrected finding and the applied fix. Prior history retained — see prior entries in version control.
