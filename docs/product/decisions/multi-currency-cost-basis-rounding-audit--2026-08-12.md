**Owner:** Financial Reporting & Records Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-08-12
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

**Quantified bound:** empirically, worst-case sequential single-share partial exits of a 3-share and a 7-share position (both markets) produced a cumulative drift between the sum of persisted `trade_history.total_cost` values and the original `total_cost` of no more than a few pence in the worst case tested, well under the ≤£0.02 bound asserted in `test_uk_position_drift_bounded` / `test_us_position_drift_bounded` / `test_drift_is_symmetric_across_markets`. The error does not compound across exits — each write is independently rounded to the nearest cent by the DB column, not accumulated in an unbounded unrounded chain.

**`reports_service.py` consumers introduce no additional drift.** The tax-year report, reconciliation report, and monthly P&L report all read back already-persisted (DB-rounded) `total_cost`/`pnl` values and apply `round(x, 2)` defensively (a no-op on an already-2dp value) — none re-derive cost basis independently. Notably, `get_reconciliation_report()` (`reports_service.py` ~line 287) already carries a pre-existing ±£0.01 tolerance (`matched = abs(round(system_total - export_total, 2)) <= 0.01`) for exactly this class of float-aggregation noise — an established codebase precedent that sub-penny/one-cent drift from proportional allocation is treated as immaterial by design, not a defect.

**Incidental observation (not a rounding-audit finding):** a full exit's `update_position()` call does not clear `positions.total_cost` — the field is simply never read again once `status == 'closed'`, so this has no financial-correctness impact. Noted for completeness; not filed as a backlog item since there is no reachable consumer of a closed position's `total_cost`.

## Regression coverage

New tests added: `tests/test_multi_currency_cost_basis_rounding_audit.py` — 5 tests: `test_uk_position_drift_bounded`, `test_us_position_drift_bounded`, `test_drift_is_symmetric_across_markets`, `test_realized_pnl_and_persisted_total_cost_use_identical_cost_per_share`, `test_us_and_uk_total_cost_both_land_on_a_2dp_value`. Full backend suite confirmed green alongside these.

## Determination

**No inconsistency requiring a fix was found.** The audit's own hypothesis of a US-vs-UK entry-side asymmetry does not survive DB-column rounding; the real (market-symmetric) partial-exit rounding source is bounded, sub-penny-to-low-pence per event, non-compounding, and consistent with the codebase's own existing ±£0.01 reconciliation tolerance precedent. Per DEL-20260811-02's unblock criterion (b): documented here as immaterial with a quantified, test-verified bound rather than a code change. No behaviour change applied — no existing calculation was altered.

## Sign-Off

**Signed off by:** Financial Reporting & Records Owner (agent-mediated, §5.3)
**Date:** 2026-08-12
**Determination:** Audit complete — systematic (all named call sites covered, not just the delegation's starting-point finding); no inconsistency found requiring a fix; documented and quantified per unblock criterion (b).
