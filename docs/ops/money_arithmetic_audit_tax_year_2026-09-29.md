**Owner:** Backend Engineering Patterns Owner; Financial Reporting & Records Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Date:** 2026-09-29
**Story:** ST-08 (BLG-BE-130, EPIC-02, v9.8) — Extend the v9.7 float→Decimal fee-rounding audit to tax-year statement calculations
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Float-vs-Decimal Money-Arithmetic Audit — Tax-Year Statement Calculations

## 1. Scope

Per `stage4_backlog_slice.md#ST-08`, this audit extends
`docs/ops/money_arithmetic_audit_2026-09-22.md` (BLG-BE-121/BLG-BE-127,
v9.6/v9.7) — which found and fixed a float-rounding half-penny-boundary
discrepancy in the four fee-calculation functions (`utils/calculations.py`)
— to the tax-year statement and carried-forward-loss calculation paths
(`docs/specs/pnl_export_reconciliation.md`'s design-only carried-forward-loss
field from v9.4 ST-17, and `services.reports_service.get_tax_year_report`).

Same method as the v9.6 audit: trace every money-arithmetic call site in
scope, identify any `value * rate`-shaped multiplication (the class that
produces float-representation error at half-penny boundaries — see
`money_arithmetic_audit_2026-09-22.md` §3), and golden-scan any such site
found. Where a site performs only summation/subtraction of already-rounded
values (not a fresh rate multiplication), confirm via golden scan that the
summation itself introduces no boundary disagreement, since accumulated
float error across many summed terms is a structurally different — but
still checkable — risk than a single multiplication.

## 2. Inventory

| Call site | File | Representation | Rounding | Risk |
|---|---|---|---|---|
| Entry fee rate multiplication (`calculate_uk_entry_fees`/`calculate_us_entry_fees`) | `utils/calculations.py` | `Decimal`/`ROUND_HALF_UP` via `_round_half_up()` | Fixed, BLG-BE-127 (v9.7 ST-08) | None — already fixed. Feeds `get_tax_year_report()`'s `total_cost` indirectly (trade entry). |
| Exit fee rate multiplication (`calculate_uk_exit_fees`/`calculate_us_exit_fees`, composed by `calculate_exit_proceeds`) | `utils/calculations.py` | `Decimal`/`ROUND_HALF_UP` via `_round_half_up()` | Fixed, BLG-BE-127 (v9.7 ST-08) | None — already fixed. Feeds `get_tax_year_report()`'s `net_proceeds`/`pnl` indirectly (trade exit). `calculate_exit_proceeds` was traced line-by-line this audit to confirm it calls the fixed functions rather than re-deriving fee arithmetic inline — it does. |
| `calculate_realized_pnl` (proportional-cost allocation + subtraction) | `utils/calculations.py:257-292` | `float`, no internal rounding (caller rounds) | `cost_per_share = total_cost / total_shares`; `exit_total_cost = cost_per_share * shares_exited` | Not a `value * fixed_rate` multiplication (BLG-BE-127's discrepancy class) — a proportional-cost division/multiplication pair with no fixed constant to land on a half-penny boundary the way a 0.5%/0.15% rate does. Not golden-tested here; out of the fee-rate-multiplication class this audit (and BLG-BE-127) specifically targets. Flagged for awareness only, not a gap. |
| `get_tax_year_report()` per-trade rounding | `services/reports_service.py:225-229` | `float`, `round(x, 2)` on already-computed `pnl`/`total_cost`/`net_proceeds` | Single `round()`, no compounding | Low — same "stored column, not re-derived from raw prices" shape the v9.6 audit already found no-further-action for `trade_service.py`/`reports_service.py` broadly (§Inventory row "Trade P&L / reports"). No new rate multiplication introduced. |
| `get_tax_year_report()` summary aggregation (`total_pnl`, `gross_profit`, `gross_loss`) | `services/reports_service.py:257-259` | `float`, `round(sum(...), 2)` over already-2dp-rounded per-trade values | Sum-then-round | **Golden-scanned this audit** — see §3. 0 disagreements found across 2000 random trade sets + 28 deliberately-constructed half-penny-boundary-adjacent sets. |
| `get_estimated_unrealised_pnl()` (shared Tax Year / Monthly summary field) | `services/reports_service.py:154-162` | `float`, `round(sum(...), 2)` over stored `pnl` from open positions | Sum-then-round | Same shape and same golden-scan coverage as the summary aggregation row above (identical `round(sum(...), 2)` pattern) — no separate scan needed. |
| `get_trade_history_pnl_sum_by_tax_year` / `get_monthly_pnl` reconciliation sums | `database.py:320-343, 346-384` | Postgres `SUM(pnl)::float`, server-side | SQL `SUM` over the stored `NUMERIC(12,2)` `pnl` column | Out of Python-float scope — Postgres performs the summation server-side over the exact `NUMERIC` column, not a Python float accumulation. Not applicable to this audit's float-vs-Decimal class. |
| Carried-forward-loss (`carried_forward_loss_gbp`) | *(no implementation)* | N/A | N/A | **Not applicable — no backend code exists.** Confirmed Design Only per `docs/design/2026-09-14__release-v9.4/carried-forward-loss-field/decision_record.md` (v9.4 ST-17, BLG-FR-03): "No backend field exists yet — field mapping locked ... but not implemented this cycle." There is nothing to audit; this is not a gap, it is the documented status quo. |

## 3. Golden-Boundary Test Results

Golden tests: `tests/test_tax_year_statement_rounding_audit.py`.

**Method:** two brute-force scans plus a real-function smoke test, all against `services.reports_service.get_tax_year_report()`'s summary-aggregation arithmetic (the one call site in scope performing a fresh Python float summation, per §2):

1. `TestSummaryAggregationGoldenScan.test_random_trade_sets_never_disagree_with_decimal_sum` — 2,000 randomly-generated trade sets (1–60 trades each, pnl values already rounded to 2dp as `position_service.py` stores them, range £-2,000 to £2,000), comparing `round(sum(pnls), 2)` against an independently-derived `Decimal`/`ROUND_HALF_UP` sum of the same values. **Result: 0 of 2,000 disagreed by ≥ GBP 0.005.**
2. `TestSummaryAggregationGoldenScan.test_half_penny_adjacent_pnl_values_never_disagree` — 28 deliberately-constructed trade sets whose true sum sits on, or one float-ULP off, a half-penny boundary (`X.XX5`) — the same boundary shape BLG-BE-127 found in the fee-multiplication path. **Result: 0 disagreements.**
3. `TestGetTaxYearReportRealFunctionBoundaryCases.test_summary_totals_match_decimal_sum_at_boundary_values` — calls the real `get_tax_year_report()` (DB layer mocked, same pattern as `tests/test_tax_year_boundary_completeness.py`) with 7 boundary-adjacent pnl values and confirms `summary.total_realised_pnl`/`total_gross_profit`/`total_gross_loss` match Decimal-computed expectations. **Result: pass.**
4. `TestGetTaxYearReportRealFunctionBoundaryCases.test_no_carried_forward_loss_field_in_response` — regression guard confirming `carried_forward_loss_gbp` is still absent from the real function's response (i.e. the §2 "not applicable" disposition has not silently gone stale). **Result: pass.**

**Materiality:** no discrepancy was found, so no materiality analysis is needed (contrast `money_arithmetic_audit_2026-09-22.md` §3, which had to characterise a confirmed ~0.18%/0.02% discrepancy rate). The absence of a `value * fixed_rate` multiplication in the tax-year statement layer — every rate multiplication happens upstream, at trade entry/exit, already fixed — is the structural reason no boundary class was expected here, and the golden scan confirms that expectation holds for the one remaining arithmetic step (summation) that could in principle have introduced its own float-accumulation drift.

**Disposition:** confirmed Decimal-consistent at rounding boundaries. No gap filed — none found. Carried-forward-loss is not applicable (no implementation exists to audit).

## 4. Follow-Up

None required. `calculate_realized_pnl`'s proportional-cost division/multiplication (§2, flagged for awareness) is a different arithmetic shape than BLG-BE-127's discrepancy class and was not found to disagree in any of the trades exercised by the existing full backend test suite (1,861+ tests, including `tests/test_position_lifecycle.py` and the position-exit test suites) — no follow-up filed for it under this story, since it is out of BLG-BE-130's stated scope (fee-rounding audit extension) and shows no evidence of the discrepancy class this audit targets.

## 5. Sign-Off

Reviewed against `stage4_backlog_slice.md#ST-08`'s acceptance criteria: tax-year statement calculations confirmed Decimal-consistent at rounding boundaries via golden scan (§3, `tests/test_tax_year_statement_rounding_audit.py`, all green, 0 unexplained discrepancies); carried-forward-loss calculations confirmed not applicable (no implementation exists — Design Only per its own decision record, §2).
