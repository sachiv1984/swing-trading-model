Owner: Strategy Rules & System Intent Owner
Class: Operational Record (Class 3)
Status: Active — PASS
Last Updated: 2026-05-31
Cycle: 2026-05-31__release-v4.7
Story: ST-01 (EPIC-01)
Backlog ref: BLG-GOV-62
Escalation ref: ESC-EXEC-20260531-07

---

# §13 Pre-Assessment — SI-04: Strategy Version Comparison (Arc 5)

**Feature:** SI-04 — Strategy Version Comparison
**Review type:** §13 System Boundary Pre-Assessment
**Cycle:** 2026-05-31__release-v4.7
**Governance reference:** `claude/strategy/strategy_rules.md §13`
**Roadmap reference:** `claude/roadmap/current_roadmap.md` — Arc 5, SI-04
**Sprint backlog AC reference:** `claude/cycles/2026-05-31__release-v4.7/stage4_backlog_slice.md#ST-01`
**Precedent reviews:**
- `docs/product/decisions/decisions--2026-05-15__release-v3.5--IT-06-section13-review.md` (IT-06 PASS — Alpaca paper trading)
- `docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md` (SI-01 PASS — pre-entry validation)
- `docs/product/decisions/decisions--2026-05-30__release-v4.5--SI-02-section13-review.md` (SI-02 PASS — behavioural drift detection)
- `docs/product/decisions/arc6_ps03_section13_preassessment.md` (PS-03 PASS — Monte Carlo simulation)

---

## Review Summary

This document is the formal §13 pre-assessment for SI-04 (Strategy Version Comparison), required before any SI-04 implementation story may proceed to sprint planning. ST-01 (this assessment) must produce a PASS or CONDITIONAL determination. A PASS or CONDITIONAL unlocks SI-04 for future sprint planning.

This is a pre-assessment — written at a time when SI-04 has no committed sprint. Its purpose is to clear the §13 gate proactively so that when SI-04 sprint planning is imminent, the governance review is already on record and does not delay execution.

---

## SI-04 Feature Description

SI-04 is described in the roadmap as follows:

> "When `strategy_rules.md` is incremented, the system compares trade history performance before and after the change. Did the parameter update actually improve outcomes? Requires version-tagged trade history."

**Feature scope (anticipated):**

SI-04 answers a specific historical question: after a trader changes their strategy parameters (e.g., adjusts the ATR stop multiplier, changes the regime filter threshold), did their trade outcomes improve or worsen? The system tags trade history entries with the strategy version at execution time and then produces comparative analytics across version transitions.

| Component | Description |
|-----------|-------------|
| Strategy version tagging | Trade history entries tagged with `strategy_version` at execution time — sourced from `strategy_rules.md` version field |
| Version comparison backend | Endpoint computes performance metrics (R-multiple, win rate, expectancy) split by strategy version periods |
| Frontend display | Read-only comparison panel or table — shows side-by-side metrics for each strategy version period |
| Gate condition | Requires version-tagged trade history (at least one version transition on record) |

**Key §13 consideration:** SI-04 compares historical trade performance across version periods. The comparison is retrospective and display-only — it shows what happened, not what to do.

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

## §13 Compliance Assessment

### Criterion 1 — Determinism

| Requirement | Status | Assessment |
|-------------|--------|------------|
| Version comparison algorithm uses no ML model or trained inference | ✅ COMPLIANT | SI-04 computes arithmetic performance metrics (R-multiple averages, win rates, expectancy) split by strategy version period. This is deterministic aggregation over a fixed dataset — no model, no probabilistic inference, no randomness. |
| Same inputs produce same outputs | ✅ COMPLIANT | Given identical trade history and version tags, the comparison output is exactly reproducible. No pseudo-random element. |
| Version tagging is deterministic | ✅ COMPLIANT | Strategy version is read from `strategy_rules.md` version field at trade execution time. The tag applied to each trade record is an exact string value from the canonical spec — no inference involved. |
| Gate condition is deterministic | ✅ COMPLIANT | Gate requires at least one strategy version transition recorded in trade history. This is a query condition (`COUNT DISTINCT strategy_version > 1`) — deterministic and unambiguous. |
| No adaptive parameters updated by comparison | ✅ COMPLIANT | The comparison output is displayed as historical data. It must not write back to `strategy_rules.md`, settings fields, or any parameter that influences future trade decisions. |

**Criterion 1 determination: COMPLIANT**

---

### Criterion 2 — Own-Data Only

| Requirement | Status | Assessment |
|-------------|--------|------------|
| Input data sourced exclusively from user's own trade history | ✅ COMPLIANT | SI-04 queries `trade_history` rows, filtered by `strategy_version` tags. All data is from the user's own closed trades — no external benchmark, peer cohort, or market return series. |
| No external market models or factor models | ✅ COMPLIANT | The comparison makes no reference to external market conditions, volatility regimes, or sector performance. It measures what the user's own strategy produced under each version. |
| No external benchmark comparison | ✅ COMPLIANT | SI-04 compares the user's strategy versions against each other — not against SPY, a benchmark index, or any external return series. The reference point is the user's own prior strategy performance. |
| Version tags derived from user's own strategy record | ✅ COMPLIANT | Strategy version is read from `strategy_rules.md`, which is the user's own canonical strategy definition. The version tag is a user-owned artefact. |

**Criterion 2 determination: COMPLIANT**

---

### Criterion 3 — Non-Predictive Output

| Requirement | Status | Assessment |
|-------------|--------|------------|
| Output is framed as historical analysis, not prediction | ✅ COMPLIANT (with binding condition on framing) | SI-04 is explicitly retrospective — "did the parameter update actually improve outcomes?" is a past-tense question answered with historical data. The frontend display must use past-tense framing ("before the change," "after the change," "outcomes during v1.3 period"). Forward-looking language ("expected improvement," "projected performance") is prohibited. |
| No point prediction displayed | ✅ COMPLIANT | Output is aggregated historical metrics by version period. There is no forecast, no expected future outcome, no projection. The display shows what happened, not what will happen. |
| Output does not claim to model future performance | ✅ COMPLIANT | SI-04 makes no claim about future outcomes from the current strategy version. It is a look-back review. The implicit assumption ("if version X outperformed version Y in the past, it may continue to") is a user judgment — the system must not make this inference explicit or present it as a system recommendation. |
| Output is statistical context for user decisions, not a system recommendation | ✅ COMPLIANT | The comparison informs one user decision: whether a recent strategy change appears to have been beneficial based on historical data. The system presents the data; the human interprets it and decides. |

**Criterion 3 determination: COMPLIANT (with one binding condition on output framing)**

---

### Criterion 4 — Decision-Support Only

| Requirement | Status | Assessment |
|-------------|--------|------------|
| Comparison output does not gate, block, or auto-trigger any trade action | ✅ COMPLIANT | SI-04 is a standalone analytics view. Its output must not be wired into the position entry flow, trade plan creation, pre-entry validation, or any stop or sizing calculation. |
| Human-in-the-loop preserved | ✅ COMPLIANT | The user observes the version comparison and applies their own judgment about whether their strategy change was beneficial. No system action is triggered by the comparison result. |
| No auto-reversion affordance | ✅ COMPLIANT (with binding condition) | The display must not include buttons or links that automatically revert `strategy_rules.md` to a prior version based on comparison output. If a strategy rollback feature is ever added, a new §13 review is required. |
| Display-only endpoint — no write side-effects | ✅ COMPLIANT | The version comparison endpoint must be a pure read-compute-return operation. It must not write to `strategy_rules.md`, `settings`, `trade_history`, or any other table. |

**Criterion 4 determination: COMPLIANT (with one binding condition on auto-reversion)**

---

## Critical §13 Boundary Questions

**1. Does the comparison output constitute a recommendation to change the current strategy?**

SI-04 shows historical outcome distributions by strategy version period. If version v1.3 shows a higher win rate than v1.2, the system is presenting a fact — not recommending the user revert to v1.3 or adopt its parameters. The critical safeguard: the frontend must not include any affordance that converts this observation into a system recommendation or an automated action. The user interprets and decides; the system displays.

**Assessment:** NO recommendation or automated action. Binding condition 3 (no auto-reversion affordance) governs this.

**2. Is version-tagging trade history compatible with §13.1 "single, explicit, human-designed strategy"?**

Version tagging does not introduce multiple strategies — it records the history of a single strategy's evolution. The system remains a single-strategy platform; version comparison enables the user to evaluate whether their own edits to that single strategy improved outcomes. This is analogous to a trader reviewing their journal before and after changing a rule. No multi-strategy capability is introduced.

**Assessment:** COMPLIANT. Version tagging preserves the single-strategy model.

**3. What happens if version periods have very few trades (statistically thin)?**

A version period with 2–3 trades produces unreliable performance statistics. The frontend display must surface this caveat — either by warning when a version period has fewer than N trades (e.g., N = 10) or by visually muting thin-period statistics. Presenting metrics from a 2-trade period alongside metrics from a 50-trade period without context could mislead the user.

**Assessment:** Implementation must include a minimum-sample caveat. See binding condition 2.

**4. Could SI-04 be extended to automatically optimise strategy parameters?**

This is the critical scope creep risk. An extension that uses the version comparison to recommend parameter values (e.g., "your v1.3 stop multiplier of 1.5× outperformed v1.2's 2.0× — recommended stop multiplier: 1.5×") would cross from historical display into adaptive recommendation. This extension would require a new §13 review and would likely result in CONDITIONAL or FAIL.

**Assessment:** Any extension beyond display-only comparison requires a new §13 review. Binding condition 4 governs this.

---

## §13 Conditions for Implementation (Binding on SI-04 Sprint)

The following conditions are mandatory for any SI-04 implementation sprint. Sprint planning for SI-04 may not seal without confirmation that these conditions carry forward.

1. **Comparison output is display-only.** The version comparison endpoint must be a pure read-compute-return operation. No write operations to `strategy_rules.md`, `settings`, `trade_history`, or any table except a dedicated analytics cache (if caching is implemented). No side effects.

2. **Thin-period statistical caveat required.** When a strategy version period contains fewer than 10 closed trades, the frontend must display a caveat (e.g., "Insufficient sample — interpret with caution" or a visual indicator). Metrics from thin periods must not be presented equivalently to well-sampled periods.

3. **No auto-reversion affordance.** The frontend display must not include any button, link, or prompt that automatically reverts `strategy_rules.md` to a prior version based on comparison output. If strategy rollback functionality is added in any future sprint, a new §13 review is required before implementation.

4. **No parameter optimisation extension.** Any extension that uses the version comparison to recommend, suggest, or calculate optimal strategy parameter values requires a new §13 review before implementation. This pre-assessment covers display-only comparison only.

5. **Past-tense framing throughout.** Frontend display must use past-tense historical framing: "trades before the change," "outcomes during v1.x period," "win rate after update." Forward-looking language ("expected improvement," "projected performance," "recommended parameters") is prohibited.

6. **§13 compliance note in backend service.** The backend version comparison service must include a comment referencing this pre-assessment and affirming: "display-only historical analysis; no adaptive output; no write operations to strategy or settings tables; §13 PASS — docs/product/decisions/si04_section13_preassessment.md."

---

## Determination

**Determination: PASS**

All four §13 criteria are confirmed COMPLIANT for SI-04 as described in the roadmap. SI-04 is a retrospective, deterministic historical analysis operating on the user's own trade history, split by strategy version tags. It answers a backward-looking question ("did the change help?") with factual aggregations. It does not predict future performance, does not use external data or ML models, and does not gate, block, or automatically modify any trade action or strategy parameter.

The six binding conditions above are mandatory. The most critical are: display-only with no auto-reversion affordance (condition 3), no parameter optimisation extension without new §13 review (condition 4), and past-tense historical framing throughout (condition 5).

---

## FAIL Implications (for reference)

Had this been a FAIL:
- SI-04 would be re-parked in the backlog with a blocking §13 objection
- Arc 5 Strategy Version Comparison would require redesign before a new §13 review could be submitted
- Sprint planning for SI-04 could not proceed

---

## Sign-Off

**Signed off by:** Strategy Rules & System Intent Owner
**Date:** 2026-05-31
**Determination:** **PASS**
**Comments:** SI-04 Strategy Version Comparison is clearly within §13 system boundaries. The feature is a retrospective, display-only historical analysis — it answers the question "did my strategy change improve outcomes?" using deterministic arithmetic aggregations over the user's own trade history, split by strategy version tags written at trade execution time. This is structurally analogous to a trader manually reviewing their journal before and after a parameter change, and the system automates that review without any adaptive or predictive element.

The critical §13 risk area for SI-04 is scope creep: the comparison display is naturally suggestive of parameter optimisation ("use the version that performed best"). Binding conditions 3 and 4 — no auto-reversion affordance and no parameter optimisation extension without new §13 review — address this risk directly. As long as SI-04 remains a read-and-display feature with no action affordances derived from the comparison output, it is fully §13 compliant.

The version tagging mechanism is a prerequisite for SI-04 and is itself §13-neutral: it records a version label on trade history rows, analogous to a journal timestamp. It does not introduce multi-strategy capability or adaptive behaviour.

Six binding conditions are documented. All four §13 criteria confirmed COMPLIANT.

**AC sign-off (AC-01–AC-06):**
- AC-01: ✅ §13 review checklist applied against SI-04 feature description (roadmap Arc 5 and backlog slice ST-01)
- AC-02: ✅ Determination: **PASS**
- AC-03: ✅ Binding conditions documented (6 conditions; most critical: display-only, no auto-reversion, no optimisation extension)
- AC-04: ✅ Assessment document produced at `docs/product/decisions/si04_section13_preassessment.md` (Class 3 Operational Record)
- AC-05: ✅ Strategy Rules & System Intent Owner sign-off recorded in this document
- AC-06: ✅ BLG-GOV-62 marked COMPLETE in backlog with date and cycle reference
