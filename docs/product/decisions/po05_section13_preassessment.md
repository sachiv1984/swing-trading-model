Owner: Strategy Rules & System Intent Owner
Class: Operational Record (Class 3)
Status: Active — PASS
Last Updated: 2026-09-23
Cycle: 2026-09-21__release-v9.6
Story: ST-23 (EPIC-06)
Backlog ref: BLG-SPEC-160 (review) / BLG-FEAT-74 (feature this review unblocks)
Escalation ref: ESC-EXEC-20260921-05

---

# §13 Pre-Assessment — PO-05: Lightweight Replay Mode

**Feature:** PO-05 — Lightweight Replay Mode (Arc 4)
**Review type:** §13 System Boundary Pre-Assessment (standalone, extracted per `BLG-SPEC-160` so `BLG-FEAT-74`'s build — >2 weeks — is not blocked on a small review)
**Cycle:** 2026-09-21__release-v9.6
**Governance reference:** `claude/strategy/strategy_rules.md` §13
**Roadmap reference:** `claude/roadmap/current_roadmap.md` — Arc 4, PO-05
**Backlog reference:** `claude/backlog/backlog.md` — `BLG-FEAT-74` (feature), `BLG-SPEC-160` (this review)
**Precedent reviews:**
- `docs/product/decisions/decisions--2026-05-15__release-v3.5--IT-06-section13-review.md` (IT-06 PASS — Alpaca paper trading; PO-05 reuses this infrastructure directly)
- `docs/product/decisions/arc6_ps03_section13_preassessment.md` (PS-03 PASS — Monte Carlo simulation; four-criterion template used here)
- `docs/product/decisions/si04_section13_preassessment.md` (SI-04 PASS — document structure followed here)

---

## Review Summary

This document is the formal §13 pre-assessment for PO-05 (Lightweight Replay Mode), required before `BLG-FEAT-74`'s implementation stories may proceed to sprint planning. ST-23 (this assessment) must produce a PASS or CONDITIONAL determination. A PASS or CONDITIONAL unlocks `BLG-FEAT-74` for future sprint planning — it does not itself schedule the build, which remains subject to normal Release Planning prioritisation and its own `VH (>2 weeks)` effort sizing.

This is a pre-assessment: PO-05/`BLG-FEAT-74` has no committed sprint at the time of this review. Its purpose is to clear the §13 gate proactively, per `BLG-SPEC-160`'s own stated rationale — so that `BLG-FEAT-74` is either genuinely ungated-ready or cleanly rejected, rather than sitting gated indefinitely on an unrun review that itself takes under a day.

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

## PO-05 Feature Description

Per `BLG-FEAT-74`'s Scope:

> "Backend: replay a historical window of the user's own trade/candidate history through the existing paper-trading mechanics under the *current* rule set. Frontend: date range or trade-set selector, and a clearly-labelled retrospective/deterministic output view."

The feature answers a single well-scoped question: "if I had applied the strategy rules I use *today* to a period of my own trading history, what would the paper-trading mechanics have produced?" It reuses IT-06's already-cleared paper-trading infrastructure (read-only, simulation-account mechanics) as its execution surface, and the strategy rule set as already implemented and approved elsewhere in the system — PO-05 introduces no new rule logic of its own.

Exact scope (single trade replay vs. full historical window, output format) is explicitly deferred to a canonical spec before implementation, per the roadmap's Standing Notice and `BLG-FEAT-74`'s own Scope bullet. This review assesses the feature as scoped in the backlog item today; the eventual implementation spec must be checked against the binding conditions below before it is considered pre-cleared by this review (see Binding Condition 6).

---

## Four-Criterion Assessment (template: `arc6_ps03_section13_preassessment.md`)

### Criterion 1 — Determinism

| Requirement | Status | Assessment |
|-------------|--------|------------|
| Replay algorithm uses no ML model or trained inference | ✅ COMPLIANT | The replay applies the system's already-implemented, human-designed strategy rules to already-known historical price/trade data. No model is trained or fitted; no inference step is introduced. |
| Same inputs produce same outputs | ✅ COMPLIANT — unconditionally, no seed needed | Unlike PS-03 (Monte Carlo), PO-05 involves **no random sampling at all**. It replays a fixed historical dataset (the user's own past prices/trades) through a fixed rule set. The same date range or trade set, run twice, must produce byte-identical output. This is a stronger determinism property than PS-03's own (which required a binding condition on seed handling) — PO-05 needs no equivalent condition. |
| No adaptive parameters updated by replay | ✅ COMPLIANT (binding condition) | Replay output must be read-only/display-only — it must not write back to strategy parameters, stop multipliers, risk percentages, or any other configurable value, and it must not modify the real (non-paper) `positions`/`trade_history` tables it reads from. |
| Rule set used is the current, already-approved rule set | ✅ COMPLIANT | Per the backlog item's own scope, the replay explicitly uses "the *current* rule set" — it does not let the user define, tune, or hypothesise an alternative rule set as part of this feature. (A future "what if I used different rules" extension would be a materially different feature requiring its own §13 review — see Critical Question 3 below.) |

**Criterion 1 determination: COMPLIANT — no binding condition needed on reproducibility (stronger than PS-03's own determinism property, since no pseudo-randomness is involved); one binding condition on write isolation carried into §13 Conditions below.**

---

### Criterion 2 — Own-Data Only

| Requirement | Status | Assessment |
|-------------|--------|------------|
| Input data sourced exclusively from the user's own trade/candidate history | ✅ COMPLIANT | Per scope: "the user's own trade/candidate history." No peer, cohort, or third-party trade data is involved. |
| No external market models or factor models | ✅ COMPLIANT | The replay applies the existing strategy rule set to historical price data already used elsewhere in the system (screener/signal generation) — it introduces no new external model. |
| No external benchmark comparison | ✅ COMPLIANT | Nothing in the feature's scope compares replay output against SPY, an index, or any external return series. If a future iteration adds this, it does not change the §13 assessment (a benchmark comparison is itself informational, not predictive or automated) but should be confirmed against this document at that time. |
| Reuses IT-06's already-cleared paper-trading mechanics | ✅ COMPLIANT | PO-05 explicitly depends on and reuses IT-06 (Alpaca paper trading, PASS at v3.5) rather than building new execution infrastructure. IT-06's existing binding conditions (read-only Alpaca access, no automated paper order generation beyond what the replay itself drives, paper data isolation from real signals) apply here unchanged — see Binding Condition 5 below, carrying IT-06's isolation condition forward explicitly for PO-05's use of the same mechanics. |

**Criterion 2 determination: COMPLIANT.**

---

### Criterion 3 — Non-Predictive Output

| Requirement | Status | Assessment |
|-------------|--------|------------|
| Output is framed as retrospective, not prediction | ✅ COMPLIANT (binding condition on framing) | `BLG-FEAT-74`'s own AC already requires: "Output is clearly labelled as retrospective/deterministic, not predictive." This is the single clearest AC of any reviewed feature to date on this exact point — it is already written into the backlog item, not something this review needs to newly impose. |
| No forward-looking claim | ✅ COMPLIANT | The feature replays a *past* window under *current* rules — it produces "what would have happened," never "what will happen." This is categorically different from PS-03's "next 50 trades" framing (which needed a binding condition to avoid reading as forward-looking) — PO-05's entire premise is retrospective, so the same risk does not arise in the same way, but the UI must still avoid phrasing like "this predicts your future performance" anywhere near the output (binding condition, for avoidance of doubt). |
| Output does not claim to model future market conditions | ✅ COMPLIANT | The replay operates entirely on historical, already-realised price data — it makes no claim about any future period. |
| Output is context for user decisions, not a system recommendation | ✅ COMPLIANT | The output informs the user's own judgment about how the current rule set would have performed historically. It issues no buy/sell/hold recommendation and gates no workflow. |

**Criterion 3 determination: COMPLIANT — no new binding condition required beyond what `BLG-FEAT-74`'s own AC already mandates; the "avoid future-facing phrasing" note above is folded into the implementation spec requirement (Binding Condition 6), not treated as a new independent condition.**

---

### Criterion 4 — Decision-Support Only

| Requirement | Status | Assessment |
|-------------|--------|------------|
| Replay output does not gate, block, or auto-trigger any trade action | ✅ COMPLIANT (binding condition) | The replay must remain a standalone retrospective view. Its output must not be wired into the position entry flow, trade plan creation, screener scoring, or any stop/sizing calculation — the same isolation principle already binding on PS-03 and required of IT-06's paper data. |
| Human-in-the-loop preserved | ✅ COMPLIANT | The user selects a date range or trade set and reviews the retrospective output; no system action follows automatically from any replay result. |
| No auto-remediation affordance | ✅ COMPLIANT (binding condition) | The output view must contain no buttons/links/prompts that adjust real strategy parameters, risk percent, or stop multipliers based on replay results. |
| Display-only / no unintended write side-effects | ✅ COMPLIANT (binding condition) | The replay must not persist to the real `positions`/`trade_history` tables it reads from, and any paper-side writes it does make (through IT-06's mechanics) must remain isolated to the existing paper-trading data model, per IT-06's own existing conditions. |

**Criterion 4 determination: COMPLIANT (with binding conditions on isolation and no auto-remediation, both consistent with PS-03/IT-06 precedent — no new condition class introduced).**

---

## Critical §13 Boundary Questions

**1. Does replay output ever block or modify a real trade entry or position?**

No. Per scope, PO-05 is a standalone retrospective view built on IT-06's read/paper-mechanics infrastructure. It has no routing path to `POST /trade-plans`, `POST /portfolio/position`, or any stop-management endpoint against the user's real portfolio.

**Assessment:** NO. Same non-blocking principle already applied to PS-03 and IT-06.

**2. Is "replay under the current rule set" materially different from "predict with the current rule set"?**

Yes, and this is the feature's core §13-relevant distinction. A *predictive* simulation would apply the rule set to *unknown, future* data (prices/candidates that have not yet occurred) to forecast an outcome — that would cross into §13.2's prohibited "machine-learning or AI-driven prediction system" / "discretionary or adaptive rule system" territory if the rules or inputs were themselves speculative. PO-05 applies the rule set to *known, already-realised historical* data — every input the replay touches is a fact already on record (a price that occurred, a candidate the screener already flagged, a rule already shipped and in production use). There is no forecast, no unknown quantity, and no probability distribution anywhere in the computation — it is closer to "re-running a report" than to "simulating the future."

**Assessment:** COMPLIANT. Historical replay under a fixed, already-approved, current rule set is deterministic re-computation of a known past, not prediction — a stronger and simpler case than PS-03's own (which required explicit reasoning about pseudo-random resampling; PO-05 needs none).

**3. Would a future "replay under a *hypothetical* rule set" extension change this assessment?**

Yes — explicitly out of scope for this review and flagged for any future extension. `BLG-FEAT-74`'s scope is unambiguous that replay runs "under the current rule set," not a user-editable or hypothetical one. If a future story lets the user vary strategy parameters (stop multiplier, risk %, entry criteria) and replay history against the *modified* rule set, that is a materially different feature — closer to a "strategy builder" or "what-if tuning" tool, which §13.2 explicitly excludes ("a discretionary or adaptive rule system," "a multi-strategy or configurable strategy platform"). Any such extension requires its own full §13 review before implementation; this PASS does not extend to it.

**Assessment:** Any future rule-parameter-variable extension of PO-05 requires a new §13 review — recorded as a binding condition (Binding Condition 4) so this scope boundary survives into implementation, not just this review.

**4. Does reuse of IT-06's paper-trading mechanics import any of IT-06's own residual risk?**

IT-06 already carries a binding condition (its own §13 Condition 3) that "paper data isolation" — paper P&L/position data must not feed real signals, screener scoring, regime detection, or position-sizing logic. PO-05, by design, computes *retrospective* output from historical data through those same mechanics — it must not create a new pathway by which replay results (paper or otherwise) leak into real-system decision logic.

**Assessment:** COMPLIANT, provided IT-06's existing isolation condition is treated as binding on PO-05 too (Binding Condition 5, explicit carry-forward rather than an implicit assumption).

---

## §13 Conditions for Implementation (Binding on PO-05/`BLG-FEAT-74` Sprint)

The following conditions are mandatory for any PO-05 implementation sprint. They are not optional. Sprint planning for `BLG-FEAT-74` may not seal without confirmation that all conditions are carried forward into the implementation spec required by `BLG-FEAT-74`'s own Scope bullet.

1. **Replay endpoint is read-only against real data.** The replay must not write to the real (non-paper) `positions` or `trade_history` tables it reads from, and must not update strategy parameters, stop multipliers, or risk percentages.
2. **Output is explicitly retrospective-labelled.** Per `BLG-FEAT-74`'s own AC: output must be clearly labelled retrospective/deterministic, not predictive. UI language must avoid any future-facing phrasing ("predicts," "forecasts," "your expected future performance") — consistent framing language: "shows what the current rules would have produced over this past period."
3. **No auto-remediation affordance.** The output view must contain no interactive control that adjusts real strategy parameters, risk percent, or stop multipliers based on replay results.
4. **Rule set is fixed to "current" — no hypothetical/user-editable rule variation.** If a future story wants to let the user vary rule parameters for the replay, that is a new feature requiring its own §13 review; this PASS does not extend to it.
5. **IT-06's paper-data isolation condition applies unchanged.** Replay/paper data must not feed real-system signals, screener scoring, regime detection, or position-sizing logic — the same condition IT-06 already carries, explicitly carried forward here since PO-05 reuses IT-06's mechanics.
6. **Implementation spec must be checked against this document before sprint entry.** Per `BLG-FEAT-74`'s own Scope note ("exact scope... to be confirmed by canonical spec before implementation"), whoever authors that spec must confirm it satisfies conditions 1–5 above — this review clears the feature's §13 boundary in principle, not any specific not-yet-written implementation detail.

---

## Sign-Off

**Signed off by:** Sprint Execution Engine (agent-mediated, Strategy Rules & System Intent Owner role — §5.3)
**Date:** 2026-09-23
**Determination:** PASS
**Comments:** All four criteria (Determinism, Own-Data Only, Non-Predictive Output, Decision-Support Only) assessed COMPLIANT, following the same template already used and PO-approved for PS-03 and IT-06. PO-05's determinism case is materially stronger than PS-03's own — no pseudo-random sampling is involved at all, since the feature replays known historical data through an already-fixed rule set, so no seed-handling condition is needed (contrast PS-03 Condition 3). The 6 binding conditions above are carried forward as mandatory for `BLG-FEAT-74`'s eventual implementation sprint; conditions 4 and 5 explicitly scope this PASS to *replay under the current rule set only*, reusing IT-06's mechanics under IT-06's own existing isolation condition — any future hypothetical-rule-set extension is out of this PASS's scope and requires a fresh review. This clears `BLG-FEAT-74`'s §13 gate per `BLG-SPEC-160`'s own stated purpose; it does not itself schedule `BLG-FEAT-74` into a sprint, which remains a Release Planning / Product Owner prioritisation decision given its `VH (>2 weeks)` effort size.
