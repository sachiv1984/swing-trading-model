# Decisions Record — BLG-TECH-01: Fix Sharpe Variance Method + Capital Efficiency Currency Basis

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-02-20
**Backlog Item:** BLG-TECH-01
**Target Release:** v1.6 (Quality Gate)
**Meeting:** Pre-Alignment Meeting
**Attendees:** PMO Lead, Engineering, Metrics Definitions & Analytics Canonical Owner

> **Standing notice:** This document records decisions made during the pre-alignment meeting for
> BLG-TECH-01. It is not a canonical specification. It exists to provide rationale and traceability
> for the implementation work that follows. When this item ships, this document status will be
> updated to Superseded with references to the validation sign-off and changelog entry that
> confirmed delivery.

---

## Context

BLG-TECH-01 corrects two known data integrity defects in the analytics system, both documented as
backlog items in `docs/specs/metrics_definitions.md` Appendix E:

- **Defect A:** `_calculate_sharpe()` uses population variance (÷ n). The canonical spec
  mandates sample variance (÷ n−1, Bessel-corrected).
- **Defect B:** Capital efficiency uses `entry_price × shares` as the cost basis, mixing
  USD and GBP for US-market trades. The canonical spec mandates `trade_history.total_cost (GBP)`.

This item is designated a **v1.6 release gate** in the roadmap. v1.6 must not ship unless this
item is complete and validation passes with signed-off expected values.

---

## Decision 1 — Dataset expansion is in scope for BLG-TECH-01

**Question:** Does expanding the validation dataset form part of this ticket, or is it a
separate prerequisite task?

**Decision:** In scope for BLG-TECH-01.

**Rationale:** The current validation dataset (`test_data/validation_data.py`) has 5 trades and
fewer than 30 portfolio snapshots. The trade-based Sharpe method requires a minimum of 10 trades;
the portfolio-based method requires 30+ snapshots. With the current dataset, `sharpe_ratio`
returns `0.00` with `sharpe_method: "insufficient_data"` — meaning the Sharpe fix, if applied,
would be invisible to the validation suite. Separating the dataset expansion into a prerequisite
task would risk closing BLG-TECH-01 with an untested correction. The fix and the test that
exercises it must ship together.

**Confirmed by:** Engineering, Canonical Owner, PMO Lead

---

## Decision 2 — Both Sharpe methods must be exercised by validation

**Question:** Is it sufficient to validate the portfolio-based Sharpe method only, or must both
the portfolio-based and trade-based fallback methods be independently validated?

**Decision:** Both methods must be validated independently. The expanded dataset must support:
- Portfolio-based Sharpe: 30+ daily portfolio snapshots
- Trade-based Sharpe (fallback): 10+ closed trades

Both methods must have independently calculated expected values in `EXPECTED_METRICS`. They produce
different values from different inputs and must each be tested.

**Rationale:** The two methods are separate code paths. The trade-based fallback is the path that
will be exercised in real usage when a user has fewer than 30 portfolio snapshots. Validating only
the portfolio method would leave the fallback path untested. Both paths carry the same population
variance defect and must both be corrected and confirmed.

**Confirmed by:** Engineering, Canonical Owner

---

## Decision 3 — Expected values must be calculated independently before the code fix is applied

**Question:** In what order should the expected value recalculation and the code fix be applied?

**Decision:** Expected values must be independently derived from the canonical formula — on paper
or in a spreadsheet — before the implementation is changed. The sequence is:

1. Expand `VALIDATION_TRADES` and `VALIDATION_PORTFOLIO_HISTORY`
2. Canonical Owner independently calculates expected Sharpe (both methods) and expected
   `capital_efficiency` from the new dataset using the canonical formulas — without running the code
3. Canonical Owner shares spreadsheet workings with Engineering for arithmetic review
4. Agreed expected values are committed to `EXPECTED_METRICS` in `validation_data.py`
5. Engineering fixes `_calculate_sharpe()` and capital efficiency
6. `POST /validate/calculations` is run — must pass
7. Canonical Owner formally signs off

**Rationale:** If expected values are derived by running the corrected code and copying the output,
the validation system becomes circular — it confirms the code matches itself, not that the code
matches the canonical formula. The expected values are the ground truth. They must be established
independently before the code is written.

**Confirmed by:** Engineering, Canonical Owner, PMO Lead

---

## Decision 4 — `total_cost (GBP)` must be explicitly present in VALIDATION_TRADES

**Question:** Can the capital efficiency fix be validated using derived values, or must
`total_cost (GBP)` be an explicit field in each trade record?

**Decision:** `total_cost (GBP)` must be an explicit field in every record in `VALIDATION_TRADES`.
Derived values are not acceptable.

**Rationale:** If `total_cost` is not present as an explicit field, the capital efficiency fix
will either fail silently or fall back to the old calculation — producing a false pass. The field
must be present and explicitly set to the correct GBP-converted cost for each trade. For US-market
trades, `total_cost` must reflect realistic GBP-converted costs, not USD prices treated as GBP.

**Confirmed by:** Engineering, Canonical Owner

---

## Decision 5 — FX rate assumptions for synthetic test trades must be documented

**Question:** When constructing `total_cost (GBP)` values for US-market trades in the synthetic
validation dataset, must the FX rate assumption be recorded?

**Decision:** Yes. The FX rate used to derive `total_cost (GBP)` for each synthetic US trade must
be documented in a comment block in `validation_data.py` alongside the trade data. The comment must
be sufficient for the values to be independently reproduced.

**Rationale:** Validation data is the ground truth for the system. If the basis for the test
data cannot be reconstructed, the data cannot be audited, corrected, or extended reliably. The FX
assumption is part of the data's provenance and must be recorded.

**Confirmed by:** Canonical Owner, Engineering

---

## Decision 6 — File scope for this ticket

**Question:** If Engineering encounters related issues in `analytics_service.py` during
implementation, may they be fixed in this PR?

**Decision:** No. Only the following files are in scope for the BLG-TECH-01 PR:
- `backend/services/analytics_service.py` — variance method fix and capital efficiency fix
- `backend/test_data/validation_data.py` — dataset expansion and expected value updates
- `backend/routers/validation.py` — second validation pass for trade-method Sharpe
  *(added to scope 2026-02-20 — see Addendum 1)*

Any other issues discovered during implementation must be logged as new backlog items and addressed
separately. They must not be included in the BLG-TECH-01 PR.

**Rationale:** Scope creep in a P0 data-correctness ticket carries high regression risk. Keeping
the change surface minimal ensures the fix is reviewable, the sign-off is meaningful, and no
unintended changes affect other validated metrics.

**Confirmed by:** Engineering, PMO Lead
**Updated:** 2026-02-20 — `validation.py` added to file scope per Addendum 1.

---

## Decision 7 — BLG-TECH-02 and BLG-TECH-03 do not start until BLG-TECH-01 is signed off

**Question:** May BLG-TECH-02 (validation severity model) or BLG-TECH-03 (ValidationService
consolidation) begin in parallel with BLG-TECH-01?

**Decision:** No. BLG-TECH-02 and BLG-TECH-03 must not begin until BLG-TECH-01 is signed off and
the v1.6 quality gate is cleared.

**Rationale:** BLG-TECH-02 and BLG-TECH-03 both touch the validation layer. Starting them before
BLG-TECH-01 is signed off risks the validation suite being modified while the expected values from
BLG-TECH-01 are still being established. The validation baseline must be locked and confirmed
before further changes are made to validation infrastructure.

**Confirmed by:** Engineering, PMO Lead

---

## Out of Scope — Confirmed in This Meeting

| Item | Decision |
|------|----------|
| API response field names or structure | No change. `sharpe_ratio`, `sharpe_method`, `capital_efficiency` field names are unchanged. Decision 6. |
| Validation tolerances | No change to existing tolerances unless recalculation surfaces a specific case requiring review. Decision 6. |
| BLG-TECH-02 (severity model) | Separate ticket. Does not start until BLG-TECH-01 is cleared. Decision 7. |
| BLG-TECH-03 (ValidationService consolidation) | Separate ticket. Does not start until BLG-TECH-01 is cleared. Decision 7. |
| Any other issues found in analytics_service.py | Must be logged as new backlog items. Decision 6. |

---

## Agreed Action Points

| # | Action | Owner | Status |
|---|--------|-------|--------|
| AP-01 | Expand `VALIDATION_TRADES` to 10+ trades; add `total_cost (GBP)` field to all records with FX rate assumption documented | Engineering | ✅ Complete |
| AP-02 | Expand `VALIDATION_PORTFOLIO_HISTORY` to 30+ daily snapshots with a realistic equity curve and drawdown | Engineering | ✅ Complete |
| AP-03 | Independently calculate expected Sharpe (both methods) and `capital_efficiency`; confirm FRES.L `total_cost = £1,116.70` (£40.98 × 27.25); update `capital_efficiency` expected value to 16.18%; provide written sign-off | Canonical Owner | ✅ Complete — signed off 2026-02-20 |
| AP-04 | Share workings with Engineering for arithmetic review | Canonical Owner | ✅ Complete — 2026-02-20 |
| AP-05 | Commit corrected `validation_data.py` to `backend/test_data/` with Canonical Owner sign-off reference in commit message | Engineering | In progress |
| AP-06 | Fix `_calculate_sharpe()` to use sample variance (n−1) for both portfolio and trade methods; **and** add second validation pass in `validation.py` to exercise trade-method Sharpe independently (see Addendum 1) | Engineering | Pending AP-05 |
| AP-07 | Fix capital efficiency to use `Mean(total_cost)` from `VALIDATION_TRADES` | Engineering | Pending AP-05 |
| AP-08 | Run `POST /validate/calculations` — all metrics must pass including both Sharpe method checks | Engineering | Pending AP-06/07 |
| AP-09 | Review validation output and formally sign off in writing | Canonical Owner | Pending AP-08 |
| AP-10 | On receipt of Canonical Owner sign-off, clear the BLG-TECH-01 v1.6 quality gate | PMO Lead | Pending AP-09 |

---

## Specs Requiring Updates

| Document | Change Required | Owner | Status |
|----------|----------------|-------|--------|
| `docs/specs/metrics_definitions.md` | Close Appendix E items 1 & 2; remove non-conformance notes from Sharpe and Capital Efficiency sections; update Appendix C to reflect two-pass validation; add Appendix D entry; bump to v1.5.7 | Canonical Owner | ✅ Complete — 2026-02-20 |
| `docs/operations/validation_system.md` | Update to reflect two-pass validation model | Engineering | Pending — alongside AP-06 |
| `docs/specs/api_contracts/analytics_endpoints.md` | Remove two Known Limitations bullet points (Sharpe variance + capital efficiency) | API Contracts Owner | Pending — on ship confirmation |
| `docs/product/changelog.md` | Add v1.6 entry for BLG-TECH-01 | Product Owner | Pending — on ship |

The files that change as a result of this work are:
- `backend/services/analytics_service.py`
- `backend/test_data/validation_data.py`
- `backend/routers/validation.py` *(added — Addendum 1)*

---

## Addendum 1 — Post-Sign-Off Scope Addition: `sharpe_ratio_trade` Validation Check
**Added:** 2026-02-20
**Raised by:** Canonical Owner (sign-off response, 2026-02-20)
**Resolved by:** PMO Lead scope decision, 2026-02-20

### Observation
The `sharpe_ratio_trade` key added to `EXPECTED_METRICS` in `validation_data.py` has no
corresponding check in `validation.py`. If left as a passive reference value it will never be
tested, creating false confidence that the trade-based Sharpe code path is validated.

### Engineering Proposed Resolution
Add a second validation pass in `validation.py` using a trade-only dataset (no portfolio
snapshots) to force the trade-based Sharpe fallback. Approximately 15 lines of additive code.
No restructuring of existing validation logic.

```python
# Second pass — trade-only data to exercise trade-based Sharpe fallback
result_trade_only = service.calculate_metrics_from_data(
    trades=VALIDATION_TRADES,
    portfolio_history=[],   # no snapshots → forces trade method
    period="all_time",
    min_trades=2
)

validations.append({
    "metric": "sharpe_ratio_trade_method",
    "expected": EXPECTED_METRICS["sharpe_ratio_trade"],
    "actual": result_trade_only.get("executive_metrics", {}).get("sharpe_ratio", 0.0),
    "diff": abs(...),
    "status": "pass" if ... else "fail",
    "tolerance": TOLERANCE["sharpe_ratio"],
    "formula": "(Avg Ann Return / Sample StdDev) — trade method",
    "method": "trade"
})
```

### PMO Scope Decision
Included in BLG-TECH-01 PR. Directly required to fulfil Decision 2 — both Sharpe methods must
be exercised by validation. The change is additive and low risk. Decision 6 updated to include
`routers/validation.py` in the file scope for this PR.

**Confirmed by:** PMO Lead, Head of Engineering, Canonical Owner

---

*When BLG-TECH-01 ships, update this document status to Superseded and reference the
`docs/product/changelog.md` entry for v1.6.*
