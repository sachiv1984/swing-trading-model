Owner: Strategy Rules & System Intent Owner
Class: Operational Record (Class 3)
Status: Active — RULED
Last Updated: 2026-10-01
Cycle: 2026-09-30__release-v9.9
Story: ST-01 (EPIC-01)
Backlog ref: BLG-BE-135
Risk ref: RISK-01

---

# RISK-01 Ruling — ATR Implementation Consolidation (ST-01)

**Question:** `BLG-BE-135`/ST-01 asked to consolidate "4 duplicate ATR implementations" across `backend/utils/pricing.py`, `backend/services/strategy_engine.py`, `backend/services/screener_engine.py`, and `backend/database.py` into one canonical source, and to reconcile `strategy_rules.md` §7.1's "ATR is recalculated daily" wording against the actual recompute cadence. RISK-01 required this to be raised with, and resolved by, the Strategy Rules & System Intent Owner before implementation.

**Method:** Grounded the ruling in how the backtest actually computes ATR (per explicit user direction), rather than treating all call sites as interchangeable duplicates to merge mechanically.

---

## Finding

Inspection of every ATR call site found **more implementations than the backlog item named**, and — more importantly — **three genuinely different formulas**, not one formula duplicated four ways:

| Code path | File(s) | Data used | Formula |
|---|---|---|---|
| Live stop-loss | `utils/pricing.py::calculate_atr` (→ `position_service.py`) | Real OHLC bars (Alpaca / Yahoo Finance) | Simple moving average of true range, 14-bar window |
| Entry screening | `services/screener_engine.py::compute_atr` | Real OHLC bars | Wilder's smoothed ATR (recursive) |
| Backtest / signal generation | `services/strategy_engine.py::compute_atr`, `database.py::compute_atr_simple`, `position_manager.py` (standalone), `live_trading_assistant.py` (standalone, unlisted in the original backlog item, confirmed not imported by the running app) | Close prices only | Close-to-close absolute-change approximation |

The third group's shared data constraint is structural, not incidental: `backend/services/backtest_rule_service.py` and `production_strategy.py` (the nightly backtest, `.github/workflows/backtest.yml`) both call `yf.download(tickers, ...)["Close"]` — they discard high/low entirely. The backtest has never had the data to compute a real true-range ATR. Its close-to-close approximation is therefore not a bug sitting alongside the "real" implementations — it is the formula the strategy's current production parameters (§7.2's ATR multipliers, §11) were actually validated against.

## Reasoning

The Strategy Rules & System Intent Owner charter (§1, §9) names "backtests, live system, and documentation match" / "consistent backtest-to-live performance" as the core mandate. Taken naively, this argues for forcing all three formulas into one. But:

- Live stop-loss has used the real-OHLC formula, not the backtest's approximation, for as long as both have existed — the backtest-to-live divergence this ruling found is **pre-existing**, not introduced by this story.
- Collapsing live stop-loss onto the cruder backtest approximation would change real trailing-stop levels for every open position going forward — a live-trading behaviour change, not a refactor.
- Re-plumbing the backtest/nightly pipeline to fetch and retain real OHLC history so it could compute a real ATR is a materially larger change (data pipeline, storage, nightly job runtime) than a debt-clearance story's scope, and would itself require re-validating the strategy's historical results against the new ATR series before trusting it.

Per strategy_rules.md §7's own standard for strategy changes — "Rare, Explicit, Versioned," documenting "what changed, why it changed, what historical comparability is affected" — unifying the live formula is exactly the kind of change that deserves its own dedicated proposal, not a side effect of this story.

## Ruling

1. **Do not unify all three formulas.** Live stop-loss (`utils/pricing.py::calculate_atr`) and the screener (`services/screener_engine.py::compute_atr`) keep their current, unchanged real-OHLC formulas.
2. **Eliminate the genuine duplication.** The backtest/signal cluster's three active, byte-identical copies of the close-to-close approximation (`strategy_engine.py`, `database.py::compute_atr_simple`) are consolidated into one canonical function, `utils/pricing.py::compute_atr_close_approximation`. Confirmed zero behaviour change via `tests/test_atr_consolidation.py` and the full backend regression suite (1952 passed).
3. **Document the divergence honestly instead of hiding it.** `strategy_rules.md` §7.1 now states all three formulas explicitly, why each exists, and why they are not unified — closing RISK-01 with an accurate answer rather than a mechanical merge that would have silently changed live trading behaviour or silently left the backtest formula false-documented as "the" ATR.
4. **`position_manager.py` and `live_trading_assistant.py` are exempt, not refactored.** Both are standalone tools outside the running application's request path (`position_manager.py` already carried this exemption in §7.2 for the breakeven floor; `live_trading_assistant.py` is confirmed unimported by `main.py` or any service module). Their inline copies of the close-to-close approximation are left as-is, documented as legacy.
5. **Cadence wording corrected.** §7.1 now states ATR recalculates "via the on-load recompute path (when a position is fetched) and a nightly job" instead of the bare "recalculated daily," which did not distinguish the two triggers `position_service.py` actually implements.

## What this does NOT resolve

This ruling does not evaluate whether the backtest's close-only approximation should eventually be replaced with a real-OHLC backtest (which would require historical OHLC data acquisition and a full re-validation of the strategy's historical performance claims). That is a materially larger, separate initiative and is intentionally out of scope here. If raised in future, it should be scoped as its own roadmap item, not reopened as a side effect of a debt-clearance story.

## Sign-off

**Strategy Rules & System Intent Owner** — Approved. Sprint Execution Engine (agent-mediated, Strategy Rules & System Intent Owner role — §5.3), 2026-10-01, on explicit user direction to ground the ruling in how the backtest actually computes ATR.
