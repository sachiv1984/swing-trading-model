**Owner:** Financial Reporting & Records Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-07-30
**Cycle:** 2026-07-30__release-v8.0
**Story:** ST-03 (EPIC-01)
**Backlog source:** BLG-SPEC-107

---

# FX Conversion Audit Trail Completeness Check (§4.1.5)

## Scope

`strategy_rules.md` §4.1.5 (Currency and FX handling, canonical) states: "The FX rate used must be returned in the sizing response for auditability." Audit every backend code path that performs a live-rate FX conversion (native currency → GBP, or vice versa) to confirm the rate actually used is surfaced back to the caller wherever the conversion feeds a monetary figure a user relies on. Fix any gap found.

## Method

Enumerated every call site of `get_live_fx_rate()` and every function accepting an explicit `fx_rate` parameter (`grep -rn "fx_rate" backend/`), then classified each by what it produces:

- **Monetary amount returned to the caller** (in scope — the rate used must accompany the figure)
- **Internal boolean/derived compliance signal** (out of scope — no currency amount is returned to audit; the entry-time rate that fed the signal is already independently visible via the position object's own `fx_rate` field)

## Findings

### In scope — audited and already compliant

| Path | Endpoint | Status |
|------|----------|--------|
| `sizing_service.size_position()` | `POST /portfolio/size` | ✅ Already returns `fx_rate_used` |
| `position_service.exit_position()` | `POST /positions/{id}/exit` | ✅ Already returns `exit_fx_rate`; persisted to `trade_history.exit_fx_rate` |

### In scope — gaps found and fixed

| Path | Endpoint | Gap | Fix |
|------|----------|-----|-----|
| `position_service.add_position()` | `POST /portfolio/position` | `fx_rate_to_use` computed and persisted to `positions.fx_rate`, but never returned in the response — the actual trade-entry endpoint (highest-stakes path: real cash movement, not an advisory calculation) had *weaker* auditability than the advisory sizing endpoint. | Added `fx_rate_used` to the response dict. Contract updated: `docs/specs/api_contracts/portfolio_endpoints.md` §POST /portfolio/position (v2.6.0). |
| `prospective_heat.prospective_heat_endpoint()` | `GET /portfolio/prospective-heat` | `fx_rate_used` computed to derive `prospective_risk_gbp`, never returned. | Added `fx_rate_used` to the response. Contract updated: same file, §GET /portfolio/prospective-heat (v2.6.0). |
| `pre_entry_validation._check_cash_constraint()` | `GET /portfolio/pre-entry-validation` (`cash_constraint` check) | `estimated_cost_gbp` is FX-derived for US tickers; the rate used was computed but not included in the check's result object. | Added `fx_rate_used` to the `cash_constraint` check result (`1.0` for UK — no conversion applied). Contract updated: same file, §GET /portfolio/pre-entry-validation `checks[]` field table (v2.6.0). |

### Out of scope — reviewed, no monetary amount returned

| Path | Reason not flagged as a gap |
|------|------------------------------|
| `compliance_service._compute_size_compliance()` (`GET /positions/compliance`) | Returns only a boolean `size_compliant` flag, not a currency amount. The entry-time `fx_rate` it reads is already independently visible via the position object's own `fx_rate` field (`GET /positions`), so an auditor is not blocked from reconstructing the calculation. |
| `pre_entry_validation._check_sector_concentration()` / `compliance_recheck_service._check_sector_concentration_recheck()` | Returns a percentage (`projected_sector_pct`), not a GBP monetary amount. FX only feeds an intermediate ratio term, not a returned currency figure. |
| `portfolio_service.py`, `portfolio_risk.py`, `services/position_service.py` display/summary functions (`GET /portfolio`, `GET /positions`, `GET /portfolio/risk`, etc.) | All already return both `fx_rate` (entry-time, persisted) and `live_fx_rate` (current) alongside every GBP-converted figure — confirmed already compliant, no change needed. |
| `signal_service.py` (screener signal generation) | Returns `fx_rate` at the top level of the signals response alongside GBP-converted prices — already compliant. |
| `portfolio_setup.py` | Interactive one-off CLI setup script, not a served API response — out of scope for a "response" auditability requirement. |

## Regression coverage

New tests added: `tests/test_fx_audit_trail_completeness.py` — covers the 3 fixed response shapes (`add_position` returns `fx_rate_used`; `prospective_heat_endpoint` returns `fx_rate_used`; `_check_cash_constraint` returns `fx_rate_used` for both US and UK).

## Determination

**3 gaps found and fixed** (all additive response-field changes — no existing field removed, renamed, or reinterpreted; no behaviour change to any calculation). No P0/P1 defect — all three were silent omissions of an already-computed value, not a miscalculation. No backlog item required; fixed directly in this story per its own acceptance criteria ("any gap found is fixed").

## Sign-Off

**Signed off by:** Financial Reporting & Records Owner (agent-mediated, §5.3)
**Date:** 2026-07-30
**Determination:** Audit complete — 3 gaps found and fixed (see table above); all other FX conversion paths confirmed already compliant or out of scope.
