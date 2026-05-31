Owner: Strategy Rules & System Intent Owner
Class: Operational Record (Class 3)
Status: Active — PASS
Last Updated: 2026-05-31
Cycle: 2026-05-30__release-v4.6
Story: ST-18 (EPIC-04)
Backlog ref: BLG-GOV-45
Escalation ref: ESC-EXEC-20260530-03

---

# §13 Pre-Assessment — PS-03: Monte Carlo Simulation (Arc 6)

**Feature:** PS-03 — Monte Carlo Simulation (Arc 6: Performance Science)
**Review type:** §13 System Boundary Pre-Assessment
**Cycle:** 2026-05-30__release-v4.6
**Governance reference:** `claude/strategy/strategy_rules.md §13`
**Roadmap reference:** `claude/roadmap/current_roadmap.md` — Arc 6, PS-03
**Sprint backlog AC reference:** `claude/cycles/2026-05-30__release-v4.6/stage4_backlog_slice.md#ST-18`
**Precedent reviews:**
- `docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md` (SI-01 PASS)
- `docs/product/decisions/decisions--2026-05-30__release-v4.5--SI-02-section13-review.md` (SI-02 PASS)

---

## Review Summary

This document is the formal §13 pre-assessment for PS-03 (Monte Carlo Simulation), required before any PS-03 implementation story may proceed to sprint planning. ST-18 (this assessment) must produce a PASS or CONDITIONAL determination. A PASS or CONDITIONAL unlocks PS-03 for future sprint planning, subject to the binding conditions documented below and the existing 50+ trades gate condition on the roadmap.

This is a pre-assessment — it is written in advance of the implementation sprint, at a time when PS-03 has no committed sprint. Its purpose is to clear the §13 gate proactively so that when the 50+ trades gate is met, implementation may proceed without further §13 delay.

---

## §13 Boundary Criteria (from strategy_rules.md §13)

### §13.1 — This system IS:
- A deterministic decision-support engine
- A risk-managed momentum framework
- A single, explicit, human-designed strategy
- Human-in-the-loop by design

### §13.2 — This system is NOT:
- An automated trading bot
- A broker execution engine
- A discretionary or adaptive rule system
- A multi-strategy or configurable strategy platform
- A machine-learning or AI-driven prediction system
- An options or futures trading system
- A real-time streaming or execution system

---

## PS-03 Feature Description

PS-03 is described in the roadmap as follows:

> "Given your actual trade distribution, what is the realistic range of outcomes over the next 50 and 100 trades? Not prediction — statistical context for drawdown psychology and position sizing decisions. Deterministic simulation, §13 COMPLIANT. Gate: 50+ trades."

The feature asks a single well-scoped question: given the user's observed historical trade outcomes (win rate, average win, average loss, standard deviation of R-multiples), what does a large population of random draws from that distribution produce as outcome envelopes over a fixed future trade count?

**Implementation scope (anticipated):**

| Component | Description |
|-----------|-------------|
| Backend simulation endpoint | `GET /analytics/monte-carlo` (or equivalent) — takes user's closed trade history, resamples with replacement, returns percentile outcome bands |
| Simulation inputs | Closed trade R-multiples drawn from `trade_history` (user's own data only) |
| Simulation outputs | Percentile ranges (e.g. 5th, 25th, 50th, 75th, 95th) of equity curve outcomes over N=50 and N=100 forward simulated trades |
| Frontend display | Read-only chart/table showing percentile envelope — no action affordances |

**Gate condition:** 50+ closed trades. Below this threshold, the trade sample is insufficient for the distribution to be stable; the gate is deterministic (count of `trade_history` rows where `pnl IS NOT NULL`).

---

## §13 Compliance Assessment

### Criterion 1 — Determinism

| Requirement | Status | Assessment |
|-------------|--------|------------|
| Simulation algorithm uses no ML model or trained inference | ✅ COMPLIANT | Monte Carlo resampling is a bootstrapping operation: random draws from a fixed empirical distribution. No ML training, no neural network, no probabilistic model fitted to external data. The distribution is the user's own trade history. |
| Same inputs produce same outputs (given identical seed) | ✅ COMPLIANT (with binding condition) | Monte Carlo simulation inherently uses pseudo-random number generation. With a fixed seed, the output is exactly reproducible. Implementation must use a fixed seed per request, or expose the seed in the API response for reproducibility. Output distributions (percentile bands) are stable with sufficient iterations (N ≥ 10,000 simulations recommended). |
| Gate condition is deterministic | ✅ COMPLIANT | The 50+ trades gate is a count query against `trade_history`. No probabilistic element — the gate either passes or fails based on an integer count. |
| No adaptive parameters updated by simulation results | ✅ COMPLIANT | Simulation results are computed on demand and displayed. They must not write back to strategy parameters, stop multipliers, risk percentages, or any other configurable value. |

**Criterion 1 determination: COMPLIANT (with one binding condition on seed handling)**

---

### Criterion 2 — Own-Data Only

| Requirement | Status | Assessment |
|-------------|--------|------------|
| Input data sourced exclusively from user's own trade history | ✅ COMPLIANT | The simulation resamples from the user's closed trade R-multiples (`trade_history.pnl` / position sizing data). No external benchmark, index, peer data, or market return distribution is used. |
| No external market models or factor models | ✅ COMPLIANT | The simulation makes no claims about market conditions, volatility regimes, or macro factors. It uses only what actually happened in the user's own trades. |
| No external benchmark comparison | ✅ COMPLIANT | PS-03 outputs outcome ranges for the user's own strategy distribution. It does not compare against SPY, a benchmark index, or any external return series. |
| Simulation does not import or depend on external data feeds at runtime | ✅ COMPLIANT | Inputs are sourced from the local database (`trade_history` table). No Alpaca, Yahoo Finance, or other external call is required to execute the simulation. |

**Criterion 2 determination: COMPLIANT**

---

### Criterion 3 — Non-Predictive Output

| Requirement | Status | Assessment |
|-------------|--------|------------|
| Output is framed as statistical context, not prediction | ✅ COMPLIANT (with binding condition on framing) | The roadmap explicitly states: "Not prediction — statistical context for drawdown psychology and position sizing decisions." The feature is designed to show the range of outcomes that would have occurred historically under resampling — not what will happen. The frontend display must use language consistent with this (e.g. "based on your historical trade distribution" — not "expected outcome" or "forecast"). |
| No point prediction displayed | ✅ COMPLIANT (with binding condition) | Output must display percentile ranges (envelope), not a single "expected" line presented as a prediction. The 50th percentile median line may be shown as a reference within an explicitly labelled envelope. A solitary point estimate labelled as "expected outcome" is prohibited. |
| Output does not claim to model future market conditions | ✅ COMPLIANT | The simulation assumes the user's historical trade distribution is stable — it does not model future market regimes, volatility, or macro conditions. This assumption must be surfaced explicitly in the UI (see binding conditions). |
| Output is statistical context for user decisions, not a system recommendation | ✅ COMPLIANT | The simulation informs two user decisions: (a) drawdown psychology (understanding realistic worst-case sequences), and (b) position sizing calibration (understanding outcome sensitivity). Neither of these involves the system issuing a recommendation. |

**Criterion 3 determination: COMPLIANT (with two binding conditions on output framing)**

---

### Criterion 4 — Decision-Support Only

| Requirement | Status | Assessment |
|-------------|--------|------------|
| Simulation output does not gate, block, or auto-trigger any trade action | ✅ COMPLIANT | PS-03 is a standalone analytics view. Its output must not be wired into the position entry flow, trade plan creation, or any stop or sizing calculation. |
| Human-in-the-loop preserved | ✅ COMPLIANT | The user observes the simulation output and applies their own judgment. No system action is triggered by any percentile outcome. |
| No auto-remediation affordance | ✅ COMPLIANT (with binding condition) | The frontend display must contain no buttons, links, or prompts that auto-adjust risk percent, stop multipliers, or any other configurable parameter based on simulation output. If a "recalculate with adjusted sizing" interactive mode is added in a future extension, a new §13 review is required. |
| Display-only endpoint — no write side-effects from simulation | ✅ COMPLIANT | The Monte Carlo endpoint must be a pure read-compute-return operation. It must not persist simulation results to any table other than a dedicated cache/snapshots table (if caching is implemented for performance). It must not write to `settings`, `trade_history`, `positions`, `trade_plans`, or any governance artefact. |

**Criterion 4 determination: COMPLIANT (with one binding condition on write isolation)**

---

## Critical §13 Boundary Questions

**1. Does the Monte Carlo output ever block or modify a trade entry or position?**

PS-03 is a standalone analytics feature with no integration into the trade plan creation form or position entry workflow. It is not a pre-entry check (that is SI-01's role). Simulation output must have no routing path to `POST /trade-plans`, `POST /portfolio/position`, or any stop-management endpoint.

**Assessment:** NO. Simulation output does not block, gate, or modify any trade workflow. The non-blocking principle (§4.2.6, §3) applies.

**2. Is pseudo-random resampling compatible with §13.1 "deterministic"?**

The §13.1 framing refers to determinism in the sense that the system's rules and logic are explicit and human-designed — not that every output is a fixed scalar. A Monte Carlo simulation with a fixed seed is reproducible: the same trade history input and the same seed produce the same percentile envelope. What matters for §13.1 compliance is that no trained model or adaptive inference layer mediates the output. Bootstrapping from an empirical distribution is a well-established deterministic algorithm; the pseudo-randomness is a computational tool for exploring the distribution, not a probabilistic model generating forecasts.

**Assessment:** COMPLIANT. Pseudo-random resampling with a fixed seed is consistent with §13.1 "deterministic decision-support engine" — provided implementation uses a fixed seed per request (binding condition).

**3. Does expressing outcomes over "the next 50 trades" constitute a prediction?**

The phrase "next 50 trades" is a framing convenience — it means "if you executed 50 more trades drawn from your historical distribution." It is not a claim that any particular sequence of 50 real trades will follow this distribution. The UI must make this clear. An appropriate framing: "If your next 50 trades were drawn from your historical trade distribution, the range of cumulative outcomes would look like this." An inappropriate framing: "Your expected equity curve over the next 50 trades is..."

**Assessment:** COMPLIANT — provided the output framing binding conditions below are observed.

**4. Is there scope creep risk in interactive "what if" sizing modes?**

A natural product extension of PS-03 is an interactive mode where the user can adjust their risk percent or win rate assumption and see how the envelope changes. This extension is valuable — but it introduces a new §13 question: does the system now advise the user to change their risk percent? If the interface shows "adjust your risk to X% to achieve Y outcome," that crosses from statistical context into system recommendation.

**Assessment:** Any interactive simulation mode that proposes parameter adjustments (rather than simply recomputing the envelope for user-provided inputs) requires a new §13 review before implementation.

---

## §13 Conditions for Implementation (Binding on PS-03 Sprint)

The following conditions are mandatory for any PS-03 implementation sprint. They are not optional. Sprint planning for PS-03 may not seal without confirmation that all conditions are carried forward.

1. **Output displays percentile ranges, not point predictions.** The simulation output must show a percentile envelope (at minimum: median and one pair of outer percentiles, e.g. 25th/75th or 5th/95th). A single "expected outcome" line presented in isolation, without an accompanying envelope, is not compliant.

2. **Simulation uses actual trade distribution only.** All input data must be drawn from `trade_history` rows where `pnl IS NOT NULL`. No external benchmark, peer cohort, market return series, or ML-generated distribution may be blended in. The simulation resamples only from the user's own closed trades.

3. **Fixed seed per request for reproducibility.** The implementation must use a deterministic pseudo-random seed per API request (e.g. derived from the request timestamp or a configurable parameter). The seed must be included in the API response so the result is auditable and reproducible.

4. **50+ trades gate is deterministic.** The gate is `COUNT(*) FROM trade_history WHERE pnl IS NOT NULL >= 50`. The gate check must be performed server-side. Below threshold: endpoint must return a structured gate-not-met response (not an empty envelope). Below-threshold output must not be displayed as if it were a stable distribution.

5. **Output framing must be historically-grounded, not predictive.** Frontend display must use language such as "based on your historical trade distribution" or "simulated from your actual trade outcomes." Language implying prediction or forecast ("your expected equity curve", "predicted performance", "forecast range") is prohibited.

6. **No write operations from simulation endpoint.** The Monte Carlo endpoint must not write to `settings`, `trade_history`, `positions`, `trade_plans`, or any governance artefact. A dedicated `monte_carlo_snapshots` table (for caching, if implemented) is the only permitted write destination.

7. **No action affordances in the frontend display.** The simulation output panel must contain no buttons, links, or prompts that auto-adjust risk percent, stop multipliers, or any other configurable parameter. If a future extension adds interactive sizing adjustment, a new §13 review is required before implementation.

8. **Distribution assumption disclosed in UI.** The interface must surface — either inline or via a tooltip/info affordance — that the simulation assumes the historical trade distribution is representative of future trades. It does not model market regimes, volatility changes, or macro conditions.

9. **§13 compliance note required in backend simulation service file.** The backend simulation service must include a comment referencing this pre-assessment and affirming: "statistical context only; display-only advisory; no position write; no automated action; §13 PASS — docs/product/decisions/arc6_ps03_section13_preassessment.md."

10. **Any actionable extension requires a new §13 review.** If a future sprint proposes adding automated parameter suggestions, one-click sizing adjustment from simulation output, or any gate based on simulation results, a new §13 review is mandatory before implementation.

---

## Determination

**Determination: PASS**

All four §13 criteria are confirmed COMPLIANT for PS-03 as described in the roadmap. The feature is a deterministic bootstrapping simulation operating on the user's own trade history, producing statistical context (percentile envelopes) for human decision support. It does not predict future market outcomes, does not use external data or ML models, and does not gate or modify any trade action.

The ten binding conditions above are mandatory and carry forward to the PS-03 implementation sprint. The most critical conditions — output as percentile envelope (not point prediction), own-data only, fixed seed for reproducibility, and no action affordances — directly address the §13 boundary risk areas identified in this review.

The 50+ trades gate on the roadmap is a separate eligibility condition (not a §13 requirement) and remains binding. This §13 pre-assessment clears the governance gate; the data density gate must be cleared separately at sprint planning time.

---

## FAIL Implications (for reference)

Had this been a FAIL:
- PS-03 would be re-parked in the backlog with a blocking §13 objection
- Arc 6 Monte Carlo would require redesign before a new §13 review could be submitted
- Sprint planning for PS-03 could not proceed

---

## Sign-Off

**Signed off by:** Strategy Rules & System Intent Owner
**Date:** 2026-05-31
**Determination:** **PASS**
**Comments:** PS-03 Monte Carlo Simulation is clearly within §13 system boundaries. The feature is a bootstrapping simulation operating on the user's own closed trade data — it is deterministic (given a fixed seed), uses no external data, produces statistical context rather than predictions, and has no automated action path. The critical §13 distinction — statistical context versus prediction — is well-grounded in the roadmap description ("not prediction — statistical context for drawdown psychology and position sizing decisions") and carries forward as a binding output-framing condition.

The pseudo-random element of Monte Carlo resampling is consistent with §13.1 "deterministic" because the algorithm itself is explicit, human-designed, and reproducible with a fixed seed. This is not ML inference — it is bootstrapping from an empirical distribution.

Ten binding conditions are documented above. The three most sensitive are: (1) output must display percentile envelopes, not point predictions; (2) simulation must use only the user's own trade distribution; (3) any future interactive mode that proposes parameter adjustments requires a new §13 review. All four §13 criteria confirmed COMPLIANT.

**AC sign-off (AC-01–AC-05):**
- AC-01: ✅ §13 pre-assessment document produced at `docs/product/decisions/arc6_ps03_section13_preassessment.md`
- AC-02: ✅ Assessment confirms: (a) deterministic — no ML/probability model, bootstrapping from empirical distribution with fixed seed; (b) own trade distribution data only — no external benchmarks; (c) output is statistical context (percentile envelopes), not a recommendation; (d) gate condition ≥50 trades is deterministic count query — see Criterion 1 and gate condition binding condition
- AC-03: ✅ Binding conditions documented: "simulation uses actual trade distribution only" (condition 2), "output displays percentile ranges, not point predictions" (condition 1), plus eight additional binding conditions
- AC-04: ✅ Determination: **PASS** — rationale in Determination section and Criterion 1–4 assessments
- AC-05: ✅ Strategy Rules & System Intent Owner sign-off recorded in this document (above)
