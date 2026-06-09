**Owner:** Strategy Rules & System Intent Owner; Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-09
**Cycle:** 2026-06-08__release-v5.3 (ST-17, BLG-GOV-104)

---

# Strategy Rules §11 Parameter Validation — v5.3

## 1. Purpose

Annual validation of the production strategy parameters defined in `claude/strategy/strategy_rules.md §11`. Validates whether current parameter values remain appropriate given the current closed trade history.

## 2. Validation Scope

Parameters validated:
1. ATR multiplier — initial stop placement vs ATR (5× ATR)
2. Regime gate — entries blocked count; pass rate for allowed entries
3. Position sizing — documented formula verified against UI implementation
4. Grace period — 10 days

## 3. Trade History Status

**Closed trades at validation date (2026-06-09):** 6 closed trades (11 total trades including open)

**Gate determination: INSUFFICIENT DATA**

Per the acceptance criteria for ST-17 (BLG-GOV-104): "If <20 closed trades: document findings as 'insufficient data' with count recorded." This condition applies — 6 closed trades is below the 20-trade threshold.

## 4. Findings

### 4.1 ATR Multiplier Validation

**Outcome: INSUFFICIENT DATA** (6 closed trades)

With only 6 closed trades, statistical validation of the 5× ATR initial stop multiplier is not meaningful. A minimum of 20 trades with documented stop placements and ATR values is required to assess whether the multiplier is calibrated correctly.

**Observation:** The 5× ATR multiplier was set based on the strategy design intent (wide initial stops to survive noise). No regime-level evidence of over- or under-tightness can be derived from 6 trades.

### 4.2 Regime Gate Pass Rate

**Outcome: INSUFFICIENT DATA** (6 closed trades)

The regime gate (SPY and FTSE above 200-day MA) is implemented correctly in the codebase. With 6 closed trades, a meaningful pass rate analysis is not possible.

**Observation:** The regime gate fires correctly — it is verified by the SI-01 pre-entry validation system (shipped v3.8). No parameter change is indicated.

### 4.3 Position Sizing Formula

**Outcome: VERIFIED — no change needed**

The position sizing formula is documented in `strategy_rules.md §4` and implemented in `backend/routers/portfolio_size.py`:

- Formula: `position_size_pct = risk_per_trade_pct / (stop_distance_pct × 100)`
- UI implementation: `GET /portfolio/size` endpoint
- Verified: formula in `portfolio_size.py` matches the documented formula in `strategy_rules.md`

No parameter change is required.

### 4.4 Grace Period (10 days)

**Outcome: INSUFFICIENT DATA — but no change indicated**

The 10-day grace period is a design choice, not a statistically derived parameter. At 6 trades, no statistical evidence supports changing it. The value remains appropriate given the momentum strategy design.

## 5. Validation Conclusion

| Parameter | Outcome | Recommendation |
|-----------|---------|----------------|
| ATR multiplier (5× initial, 2× profitable) | Insufficient data (<20 trades) | No change. Re-validate when ≥20 closed trades. |
| Regime gate | Insufficient data (<20 trades); mechanically verified | No change. |
| Position sizing formula | Verified correct | No change. |
| Grace period (10 days) | Insufficient data; design rationale intact | No change. |

**Overall recommendation:** No parameter changes. Re-validate when the closed trade count reaches ≥20 (see OA-RP-01 gate condition in v5.3 sprint planning).

## 6. Product Owner Ratification

Per AC for ST-17: Product Owner ratifies any recommended parameter changes.

**PO ratification:** No parameter changes recommended — ratification not required. The "insufficient data" finding is acknowledged. Next validation scheduled when closed trade count ≥20.

Signed: Strategy Rules & System Intent Owner (agent-mediated, 2026-06-09)
Ratified: Product Owner (agent-mediated, 2026-06-09) — no changes; acknowledged
