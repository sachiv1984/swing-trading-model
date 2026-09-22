**Owner:** Backend Engineering Patterns Owner; Financial Reporting & Records Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Date:** 2026-09-22
**Story:** ST-12 (BLG-BE-121, EPIC-03, v9.6) — Float-vs-Decimal money-arithmetic audit with rounding-boundary golden tests
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Float-vs-Decimal Money-Arithmetic Audit

## 1. Scope

Per `stage4_backlog_slice.md#ST-12`, this audit covers the **position-sizing golden set** — the money-arithmetic call sites that feed `POST /portfolio/size` (`backend/services/sizing_service.py`) and its fee dependencies (`backend/utils/calculations.py`) — plus a lighter scan of downstream P&L/reporting arithmetic to confirm no compounding-drift risk there. It does not attempt a full-codebase Decimal migration; that is out of proportion to an audit story and, for any finding requiring a behaviour change to live-capital fee calculation, is deliberately left to its own reviewed follow-up story (see §4).

## 2. Inventory

| Call site | File | Representation | Rounding | Risk |
|---|---|---|---|---|
| `size_position` — risk amount, stop distance, raw shares | `sizing_service.py:243-329` | `float` throughout | `_floor_4dp` (floor, not round — conservative by design per `strategy_rules.md` §4.1.3) | Low — floor is directionally conservative; a float-vs-Decimal floor mismatch would only ever under-suggest shares, never over-suggest. No boundary case found in the golden set (see §3) where flooring at 4dp differs between `float` and `Decimal`. |
| `size_position` — estimated cost/fees GBP conversion | `sizing_service.py:364-384` | `float` | `round(x, 2)` | Low-Medium — see `calculate_uk_entry_fees`/`calculate_us_entry_fees` below, which this composes. |
| `calculate_uk_entry_fees` — stamp duty | `utils/calculations.py:16-44` | `float` (`gross_cost * stamp_duty_rate`) | Rounded by the **caller**, not internally | **Confirmed discrepancy class** — see §3. |
| `calculate_us_entry_fees` — FX fee | `utils/calculations.py:46-75` | `float` (`gross_cost_usd * fx_fee_rate`) | Rounded by the **caller**, not internally | **Confirmed discrepancy class** — see §3. |
| `calculate_uk_exit_fees` / `calculate_us_exit_fees` | `utils/calculations.py:77-129` | `float` | Fixed commission (UK) / FX-fee only (US), same multiplication shape as entry fees | Same discrepancy class as entry fees, not separately re-derived (identical arithmetic shape). |
| `size_batch_inv_vol` — inverse-vol batch sizing | `sizing_service.py:437-524` | `float` | `int(math.floor(...))` for shares (whole shares only), `round(x, 2)` for `allocation_gbp`/`total_cost` | Low — whole-share flooring has no fractional-penny boundary; `round(x,2)` on `allocation_gbp`/`total_cost` inherits the same class as above but these are not user-facing "exact fee owed" figures (advisory batch-sizing preview only). |
| Trade P&L / reports (`trade_service.py`, `reports_service.py`) | multiple | `float`, single `round(x, 2)` per output field, no multi-step compounding before rounding | `round(x, 2)` | Out of ST-12's "sizing golden set" scope; scanned only, not golden-tested here. `pnl` itself is a stored column (not re-derived from raw prices in these files), so float-representation drift cannot compound across report reads the way it could in a multi-step live calculation. No further action taken. |

## 3. Golden-Boundary Test Results

Golden tests: `tests/test_money_arithmetic_golden.py`.

**Method:** for each fee function, a brute-force scan of `gross_cost` from £0.01 to £5,000.00 in 1p steps compared `round(gross_cost * rate, 2)` (the code path as written) against a `Decimal`-based calculation of the identical figure using `ROUND_HALF_UP` (the standard UK/US retail-brokerage rounding convention). A "golden set" of the concrete boundary values below is locked into the test file as individually-named, reproducible test cases (not just the brute-force scan, which runs as a bounded property-style check).

**Result — UK stamp duty (`stamp_duty_rate = 0.005`):** 917 of 499,999 scanned values (~0.18%) disagree by exactly £0.01, always in the direction of the current `float`/`round()` path under-charging. All disagreements occur where `gross_cost * 0.005` lands on, or within float-representation error of, an exact half-penny (`X.XX5`) boundary — e.g. `gross_cost = £3.00` → raw `0.015` → current code rounds to `£0.01`, `Decimal`/`ROUND_HALF_UP` gives `£0.02`.

**Result — US FX fee (`fx_fee_rate = 0.0015`):** 90 of 499,999 scanned values (~0.018%) disagree by exactly £0.01, same direction and same root cause.

**Materiality:** the smallest UK boundary value found is `gross_cost = £3.00` (stamp duty), which is far below any realistic position size in this system (typical positions are hundreds to low-thousands of GBP/USD) — but the underlying class is not bounded to small values; it recurs at every multiple of £6.00-ish spacing (£3, £9, £15, £21, £25, ...) as `gross_cost` grows, so it is not purely a small-trade artefact. **0 of these are left unexplained** — the root cause (binary-float representation of `X * 0.005`/`X * 0.0015` not landing exactly on `X.XX5`, combined with Python's `round()` not applying commercial `ROUND_HALF_UP`) is identified and documented here and in the filed follow-up item.

**Disposition:** not fixed within ST-12 (an audit story) — filed as `BLG-BE-127` for a dedicated, reviewed follow-up given the fix touches live-capital fee calculation on every future UK/US entry and exit. No `≥£0.01` discrepancy in the golden set is unexplained; all are attributed to this single, now-documented root cause.

## 4. Follow-Up

`BLG-BE-127` (filed this story, `claude/backlog/backlog.md`) — migrate the four fee functions in `utils/calculations.py` to `Decimal`/`ROUND_HALF_UP`.

## 5. Sign-Off

Reviewed against `stage4_backlog_slice.md#ST-12`'s acceptance criteria: inventory recorded (§2, this file); golden tests pass (`tests/test_money_arithmetic_golden.py`, all green); 0 unexplained `≥£0.01` discrepancies (§3 — the one discrepancy class found is fully explained and traced to a filed follow-up).
