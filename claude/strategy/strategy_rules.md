# Production Strategy – Momentum Trading System

**Owner:** Strategy Rules & System Intent Owner  
**Status:** Canonical  
**Version:** 1.9
**Last Updated:** 2026-09-08
**Applies to:** Production backtests, live system, and documentation  

---

## Change log

| Version | Date | Summary |
|---|---|---|
| 1.9 | 8 September 2026 | New §12.2 data-volume threshold trigger (100 closed trades since last review), §13.6 SI-02 gate-history-tied periodic boundary review cadence, §15 version cross-reference consistency check (first run: 0 actionable findings), §16 change-justification template (ST-30/ST-39/ST-41/ST-42, EPIC-04, v9.2, BLG-GOV-255/BLG-GOV-262/BLG-GOV-282/BLG-GOV-306) — Documentation/process-only: no change to §4, §12.1, or §13.1/§13.2 canonical behaviour. Rationale: closes 4 independently-scoped governance gaps (calibration-review triggering, event-driven boundary re-check, citation-drift detection, changelog-quality standardisation) surfaced as separate backlog items this cycle. Impact: documentation only — no backtest, live-logic, or comparability impact; §12.3's comparability-acknowledgement requirement does not apply since no listed §12.1/§12.2 parameter value changed. §13 reference: §13.6 extends (does not alter) the existing §13.5 semi-annual cadence; no existing §13 clearance is reopened by this entry itself — SI-02's boundary is only re-reviewed if and when §13.6's own 2-breach trigger condition is later met. This entry is written per the new §16 template itself (first real application). |
| 1.8 | 7 September 2026 | Added §4.1.8 worked numerical example of the low-ATR sizing edge case (ST-34, EPIC-05, v9.1, BLG-SPEC-101) — documents the existing interaction between §4.1's canonical risk-based sizing and §4.1.6's cash-constraint gate for low-volatility instruments. No functional/behavioural change — documentation only. Version chosen as 1.8, not 1.7, to avoid a collision with EPIC-04's independently in-flight (not yet merged) 1.6→1.7 bump (ST-21, §13.5 roster row, commit `5a65aadf`) — same precedent applied earlier this cycle to `OPERATIONAL_GUIDE.md` (v4.174) and `backlog.md` (BLG-QA-159). |
| 1.7 | 7 September 2026 | Added ST-06 — Automated AI Post-Trade Debrief (BLG-FEAT-90) to §13.5's semi-annual re-attestation roster (ST-21, EPIC-04, v9.1, BLG-GOV-311) — `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`, CONDITIONAL determination, v8.9, 9 binding conditions remain in force. Reviewed against the review document's own reasoning before adding, not a mechanical copy: this feature is the highest-condition-count (9) and highest-risk free-text surface reviewed under §13 to date (per-trade, numeric-claim-bearing), making it a genuinely warranted — arguably higher-priority — addition to the re-attestation roster, not just a mechanical registration. No behavioural rules changed. |
| 1.6 | 6 August 2026 | Added §13.5 Semi-Annual Boundary Re-Attestation Cadence (ST-23, EPIC-05, v8.3, BLG-GOV-204) — proposes a rolling 6-month lightweight re-confirmation cadence for every shipped AI/automation-adjacent feature with a recorded §13 clearance (IT-06, SI-01, SI-02, SI-04, BLG-FEAT-50/51, PT-04, on-demand compliance recheck, Gemini thesis generation). First review date set: 2027-02-06. No behavioural rules changed. |
| 1.5 | 3 August 2026 | Added §13.4 continuity note (ST-15, EPIC-05, v8.1, BLG-SPEC-82) — explicit confirmation that the on-demand compliance recheck (BLG-FEAT-64, v6.9) re-applies SI-01's existing deterministic rule set and introduces no new automation/prediction surface beyond it, distinct from and non-duplicative of SI-02's separately-gated drift detection. No behavioural rules changed. |
| 1.4 | 20 May 2026 | Added §4.2 Pre-Entry Advisory Checks — formalises regime gate, sector concentration, earnings proximity, cash constraint, and sizing validity as advisory pre-entry conditions. No change to stop-loss, trailing logic, exit conditions, or position sizing calculation rules. §13 gate: SI-01 PASS recorded in docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md. |
| 1.3 | 19 February 2026 | Revised §4.1.7 — replaced toggle activation model with always-visible widget model per pre-alignment decision record for roadmap item 3.2 (Decision 3). No changes to calculation rules, validity rules, FX handling, or cash constraint behaviour in §4.1.1–§4.1.6. |
| 1.2 | 18 February 2026 | Added canonical rules for the Position Sizing Calculator (Section 4.1). No changes to stop-loss, trailing logic, or exit conditions. |
| 1.1 | 18 February 2026 | Expanded system boundaries and design rationale (Section 13). No behavioural rules changed. |
| 1.0 | February 2026 | Initial canonical version. |

---

## 1. Purpose

This document defines the authoritative production strategy for the Momentum Trading System.

It is a behavioural contract between:
- strategy intent
- system implementation
- backtests and reported performance

If a behaviour can affect trading outcomes, it must be specified here. If there is any conflict between this document and the code, user interface, analytics, or user interpretation, this document prevails.

---

## 2. Strategy intent (non-negotiable)

The strategy is designed to:

1. Capture medium- to long-term momentum trends.  
2. Avoid premature exits caused by early volatility.  
3. Give losing trades time to resolve.  
4. Defend profits aggressively once momentum is confirmed.  
5. Enforce asymmetric risk: losses are tolerated; gains are defended.

These principles define the strategy’s intent and must remain stable over time.

---

## 3. Human-in-the-loop execution model

- Entries and exits are executed manually by the user.  
- Exit signals generated by the system are recommendations, not automatic orders.  
- The system provides decision support only and does not execute trades.

This is a deliberate design constraint.

---

## 4. Position entry rules

Positions are entered manually via the web interface.

**Required at entry:**
- ticker symbol  
- entry date  
- entry price  
- number of shares (fractional shares supported)  
- ATR value (used to calculate the stop at entry)

Fees are applied automatically based on market (UK / US).

---

## 4.1 Position Sizing Calculator (decision support) — canonical rules

This section defines the canonical, deterministic behaviour for the Position Sizing Calculator used during position entry.

- The calculator proposes a share quantity only.  
- It does not change the entry, stop, or exit rules.  
- All sizing calculations are performed on the backend and are authoritative.

### 4.1.1 Definitions

**Entry price**  
The user-entered entry price in the instrument’s native currency.

**Stop price**  
The stop price used for sizing. This is the entry-time initial stop for the prospective position, in the instrument’s native currency.

**Stop distance**  
The difference between Entry price and Stop price, in the instrument’s native currency.

```text
StopDistance = EntryPrice - StopPrice
```

**Portfolio value (GBP)**  
The portfolio value used for sizing. This is the most recent stored snapshot value:

```text
latest portfolio_history.total_value
```

**Available cash (GBP)**  
Cash available to allocate to a new position:

```text
portfolios.cash
```

### 4.1.2 Risk basis (canonical)

Risk is budgeted at the portfolio level.

```text
RiskAmount = PortfolioValue * RiskPercent
```

Available cash is an execution feasibility constraint and must not be used as the risk basis.

### 4.1.3 Share calculation (canonical)

```text
RawShares = RiskAmount / StopDistance
```

**Rounding and precision**
- Shares are returned to 4 decimal places.  
- Rounding is conservative to avoid exceeding the intended risk.

```text
SuggestedShares = floor(RawShares, 4dp)
```

The user interface may display shares to 2 decimal places for readability. The backend value remains 4 decimal places.

### 4.1.4 Validity rules (deterministic constraints)

The sizing result is **invalid** if any of the following are true:

- `RiskPercent <= 0`  
- `PortfolioValue <= 0`  
- `EntryPrice <= 0`  
- `StopPrice <= 0`  
- `StopDistance <= 0` (including `StopPrice >= EntryPrice`)

If invalid:
- the system must not apply `SuggestedShares`, and  
- the backend must return a deterministic invalid reason code.

If the portfolio value snapshot is missing, the backend must return an invalid result with reason code `NO_PORTFOLIO_VALUE_SNAPSHOT`.

### 4.1.5 Currency and FX handling (canonical)

- Entry price and Stop price are in the instrument’s native currency.  
- Portfolio value and Available cash are in GBP.

If conversion is required:
- the system uses an effective FX rate,  
- the default is the system-provided live FX rate, and  
- a user-provided FX rate overrides the live rate.

The FX rate used must be returned in the sizing response for auditability.

### 4.1.6 Cash constraint (execution feasibility gate)

The calculator must not apply a share count that exceeds Available cash.

```text
EstimatedCost = (SuggestedShares * EntryPrice) + EstimatedFees
```

If:

```text
EstimatedCost > AvailableCash
```

then:

```text
Result = INSUFFICIENT_CASH
```

In this case:
- shares must not be auto-filled, and  
- the result may include `MaxAffordableShares` for user interface messaging.

### 4.1.7 User interface interaction requirement

- The Position Sizing Calculator is always visible within the Position Entry form. It does not require activation via a toggle or any other user action.

**Calculation behaviour**

- The calculator recalculates automatically as the user enters or modifies entry_price, stop_price, or risk_percent.
- Recalculation is debounced: the backend call is made 300ms after the user stops typing.
- A loading state is shown during the window between the debounce firing and the response returning.
- All sizing calculations are performed on the backend and are authoritative.

**Auto-fill behaviour**

- When a valid result is returned and the shares field is empty: the shares field is auto-filled with SuggestedShares.
- When a valid result is returned and the user has already manually entered a share count: the shares field is not overwritten. The suggested value is displayed alongside the field with an explicit "use this" affordance, allowing the user to apply it deliberately.
- When the result is INSUFFICIENT_CASH: the shares field is not auto-filled. MaxAffordableShares is shown as informational context only.
- When the result is invalid: the shares field is not auto-filled. An inline plain-language message is shown beneath the widget.

**Form submission**

- An invalid or cash-constrained sizing result does not block form submission.
- The user may enter shares manually and proceed regardless of widget state.
- The sizing calculator is decision support; it is not a submission gate.

**Rationale for change from v1.2**

The toggle model specified in v1.2 was written before the pre-alignment meeting for roadmap item 3.2. During that meeting, the Head of UX & Design and Product Owner agreed that the calculator should be always visible in the entry form — requiring users to discover and activate a toggle would reduce the daily workflow value that justifies the feature. The auto-fill protection rule (do not overwrite a manually entered value) is a financial safety constraint: silently replacing a user-entered share count could cause an unintended position size to be submitted. Full decision rationale: docs/product/decisions/3.2-position-sizing-calculator.md Decision 3.

### 4.1.8 Worked example — low-ATR sizing edge case

This is a worked numerical example only. It documents an existing interaction between §4.1's canonical rules and does not introduce, change, or reinterpret any calculation, validity, or gating rule defined above.

At entry-time sizing, the Stop price used in §4.1.1–§4.1.3 is the prospective position's initial stop (§5): `InitialStop = EntryPrice - (InitialATRMultiplier * ATR)`, so `StopDistance = InitialATRMultiplier * ATR` (§11: `InitialATRMultiplier = 5`). A ticker with an unusually small ATR relative to its price — a low-volatility instrument — therefore produces a small `StopDistance`, which the §4.1.3 division (`RawShares = RiskAmount / StopDistance`) can turn into a large `SuggestedShares`, without ever failing the §4.1.4 validity check (`StopDistance` is still `> 0`). The result is a mathematically valid but capital-heavy suggestion, which then meets the separate §4.1.6 cash-constraint gate rather than any sizing-validity rule.

**Example**
- `PortfolioValue` = £50,000
- `RiskPercent` = 1% → `RiskAmount` = £500
- `EntryPrice` = £20.00
- `ATR` = £0.10 (low-volatility instrument)
- `StopDistance` = `InitialATRMultiplier * ATR` = 5 × £0.10 = £0.50
- `StopPrice` = £20.00 − £0.50 = £19.50
- `RawShares` = £500 / £0.50 = 1,000 shares → `SuggestedShares` = 1,000.0000 (§4.1.3; passes §4.1.4 — `StopDistance > 0`)
- `EstimatedCost` = 1,000 × £20.00 = £20,000 (+ fees) (§4.1.6)
- If `AvailableCash` = £5,000: `EstimatedCost` (£20,000) `> AvailableCash` (£5,000) → `Result = INSUFFICIENT_CASH`; `MaxAffordableShares` ≈ 250 (informational only, per §4.1.7's cash-constrained auto-fill suppression)

**Why this is worth documenting:** the same mechanism that produces a valid, well-behaved `SuggestedShares` for an ordinary-volatility instrument can, for a low-ATR instrument, propose a share count whose cost is disproportionate to the portfolio's cash — not because the risk math is wrong (§4.1.2's `RiskAmount` is still respected per share of stop distance), but because a tight ATR-derived stop concentrates the same risk budget into far more shares. The `INSUFFICIENT_CASH` path (§4.1.6) is the existing, correct handling for this case — it already suppresses auto-fill and surfaces `MaxAffordableShares` as informational context. No new rule is required; this section exists so the interaction is discoverable at the canonical source rather than inferred informally, as it had been referenced across other backlog items prior to this addition.

---

## 4.2 Pre-Entry Advisory Checks (decision support)

This section defines advisory pre-entry conditions surfaced to the user during trade plan creation. All checks are non-blocking — they do not prevent plan submission. The user retains full discretion to proceed regardless of advisory status.

These checks are implemented via `GET /portfolio/pre-entry-validation` (SI-01). §13 compliance: the panel is display-only advisory; it is not a submission gate.

### 4.2.1 Regime gate

Do not enter a new position in a market that is in a risk-off regime (§8.2). The pre-entry check surfaces the current regime state for the target market (US: SPY 200-day MA; UK: FTSE 100 200-day MA).

- **Advisory status:** FAIL if the target market is currently risk-off.
- **Rationale:** Entering a new position during a risk-off regime is inconsistent with the momentum strategy's intent (§2) to capture medium- to long-term trends. Risk-off regimes are an exit condition (§8.2); they also serve as an advisory caution at entry.

### 4.2.2 Sector concentration

A portfolio sector allocation projected to exceed 30% of total portfolio value is an advisory concentration warning. This threshold is shared with `GET /portfolio/concentration-status`.

- **Advisory status:** WARN if projected sector allocation ≥ 30%.
- **Threshold:** 30% of total portfolio value (cash + positions).
- **Calculation:** Current sector value (at live prices) + estimated new position value, divided by total portfolio value.
- **Rationale:** Concentrated sector exposure increases correlation risk and portfolio sensitivity to sector-specific events. 30% is the established operational limit.

### 4.2.3 Earnings proximity

A position opened within 5 calendar days of an earnings announcement carries elevated gap risk. This check applies to US tickers only (earnings data sourced from Yahoo Finance via `GET /earnings/{ticker}`).

- **Advisory status:** WARN if next earnings date is within 5 calendar days (0–5 inclusive).
- **Rationale:** Earnings announcements can cause large overnight gaps that bypass the trailing stop entirely. Entering immediately before earnings is inconsistent with the strategy's risk management principles (§7, §8).

### 4.2.4 Cash constraint

A proposed position whose estimated cost exceeds available portfolio cash is a feasibility advisory. This mirrors the §4.1.6 cash constraint in the Position Sizing Calculator.

- **Advisory status:** FAIL if estimated cost (quantity × live price, in GBP) exceeds available cash.
- **Calculation:** Same basis as §4.1.6: `EstimatedCost = quantity × live_price_gbp`.
- **Rationale:** The portfolio cash balance is the execution feasibility ceiling for new positions.

### 4.2.5 Sizing validity

When entry price and stop price are provided, the proposed stop configuration is checked against §4.1.4 validity constraints.

- **Advisory status:** FAIL if stop distance ≤ 0 (i.e. stop price ≥ entry price), or if either price ≤ 0.
- **Applies when:** Both `entry_price` and `stop_price` are supplied as query parameters.
- **Rationale:** A non-positive stop distance produces an invalid position sizing result (§4.1.4) and must be corrected before position entry.

### 4.2.6 Non-blocking principle (binding)

All pre-entry advisory checks are informational. The advisory panel must never prevent, gate, or auto-reject a trade plan submission. This principle is consistent with §4.1.7 (sizing calculator does not block form submission) and §3 (the system provides decision support only). Any future extension that introduces a hard submission gate requires a new §13 review.

---

## 5. Initial stop calculation

At entry, an initial protective stop is calculated:

```text
InitialStop = EntryPrice - (InitialATRMultiplier * ATR)
```

**Rules**
- The stop exists immediately.  
- The stop is stored and tracked from day one.  
- The stop is not enforced during the grace period.

**Purpose**
- to make downside risk visible  
- to anchor trailing stop logic  
- to reduce reactive decision-making

---

## 6. Grace period

### 6.1 Definition
A fixed grace period applies to all new positions.

### 6.2 Current production configuration
Grace period length: **10 calendar days** (days 0–9 inclusive)

### 6.3 Behaviour during the grace period
- Stop-loss enforcement is disabled.  
- The stop price is calculated and stored.  
- No stop-based exit recommendation may be generated.  
- Manual exit is always permitted.

### 6.4 Rationale
The grace period reduces the likelihood of exits caused by normal post-entry volatility rather than a breakdown of the trade thesis.

---

## 7. Trailing stop-loss framework (post-grace)

After the grace period, the position enters active risk management.

### 7.1 ATR framework
- ATR period: 14 days (rolling)  
- ATR is recalculated daily.

### 7.2 Profit-aware stop logic

**Losing or breakeven positions**
```text
Stop = CurrentPrice - (InitialATRMultiplier * ATR)
```
- Wide stop intended to allow recovery.  
- Reduces noise-driven exits.

**Profitable positions**
```text
Stop = CurrentPrice - (ProfitATRMultiplier * ATR)
```
- Tight trailing stop intended to lock in gains.  
- Reduces drawdowns on winning positions.

### 7.3 Stop movement rule (hard constraint)

```text
UpdatedStop = max(CurrentStop, NewlyCalculatedStop)
```

Stops must never move downwards. Once tightened, a stop must not be loosened. This rule is absolute.

---

## 8. Exit conditions

A position may exit under exactly three conditions.

### 8.1 Stop-loss trigger
- Active only after the grace period.  
- Triggered when the market price breaches the trailing stop.  
- Exit is recommended and requires manual confirmation.

### 8.2 Market risk-off override
- Positions are exited when the relevant market enters a risk-off regime.  
- The regime is defined by the 200-day moving average of the relevant index.  
- This applies regardless of stop position.

### 8.3 Manual exit
- User-initiated.  
- Available at any time.

---

## 9. Position states

Each position exists in exactly one state at any time.

| State | Definition |
|---|---|
| GRACE | Days 0–9, stop inactive |
| LOSING | Post-grace, P&L ≤ 0, wide stop |
| PROFITABLE | Post-grace, P&L > 0, tight stop |
| EXITED | Position closed |

States are mutually exclusive and deterministic.

---

## 10. Risk management summary

**Position-level**
- Fixed grace period.  
- Wide stops while losing.  
- Tight stops once profitable.  
- Stops only tighten.

**Portfolio-level**
- Market regime override.  
- Currency-aware P&L.  
- Cash-flow-adjusted performance tracking.

---

## 11. Current production parameters

- Grace period: 10 days  
- Initial / losing stop multiplier: 5 × ATR  
- Profitable stop multiplier: 2 × ATR  
- ATR period: 14 days  

These parameters must be consistent across production backtests, live system logic, and reported performance metrics.

---

## 12. Parameter governance

The values above are parameters, not immutable rules. They describe how the strategy currently expresses its intent.

### 12.1 Stable elements
- A grace period exists.  
- Losses and profits are treated asymmetrically.  
- Profits are defended once momentum is confirmed.  
- Stops do not loosen.

### 12.2 Elements that may change
- Grace period length.  
- ATR multipliers.  
- ATR lookback period.

**Data-volume threshold trigger (ST-39, EPIC-04, v9.2, BLG-GOV-262):** the elements above were calibrated against the trade history available at the time each was set — with a small closed-trade sample, any recalibration proposal is itself low-confidence. A review of these elements' calibration is triggered once **100 closed trades** have accumulated since the last time any element in this list was reviewed (whether or not it was changed) — tracked via a running count in `docs/specs/metrics_definitions.md`'s trade-count-dependent metrics infrastructure, not a new separate counter. Below 100 closed trades since the last review, a recalibration proposal may still be raised (nothing here prevents it) but must explicitly disclose the small-sample caveat per §12.3's "state the rationale and expected impact" requirement. This does not lower the bar §12.3 already sets for an actual change — it only defines when a *review* (not necessarily a change) is warranted on data-volume grounds specifically, distinct from a review prompted by a specific observed problem.

### 12.3 Change control requirements

Any parameter change must:
- be explicitly documented  
- be versioned at the strategy level  
- state the rationale and expected impact  
- acknowledge loss of direct comparability with prior results  
- be applied consistently across backtests, live logic, and documentation  

Until a change is made, the listed parameters define canonical production behaviour.

---

## 13. System boundaries

### 13.1 This system is
- a deterministic decision-support engine  
- a risk-managed momentum framework  
- a single, explicit, human-designed strategy  
- human-in-the-loop by design

### 13.2 This system is not
- an automated trading bot  
- a broker execution engine  
- a discretionary or adaptive rule system  
- a multi-strategy or configurable strategy platform  
- a machine-learning or AI-driven prediction system  
- an options or futures trading system  
- a real-time streaming or execution system

### 13.3 Design boundary rationale

Human-in-the-loop execution is a design principle, not a limitation.

Gap risk monitoring is excluded by design because the system operates on a daily decision cadence and cannot act on gaps at the moment they occur. Exposing a gap risk metric would increase noise without enabling a decision.

The strategy is fixed and explicit. A strategy builder, adaptive rules engine, or machine learning-based signal generation would change the nature of the system and is outside the design intent.

### 13.4 §13 continuity note — On-demand compliance recheck (BLG-FEAT-64, v6.9)

The on-demand "Recheck Compliance" action added in `2026-07-10__release-v6.9` (ST-01, `docs/design/2026-07-10__release-v6.9/on-demand-compliance-recheck/ux_spec.md`) re-applies SI-01's existing, already-approved deterministic rule set against current position/market state, on user request, for a single open position. It introduces no new automation or prediction surface beyond SI-01's existing gate: no new rule logic, no scheduling/background execution, no persisted recommendation or flag (the result is point-in-time and dismissed on modal close, per the design spec §3 step 5), and no interaction with SI-02's drift-detection gate (which remains separately gated per §13.2/§14 and the `BLG-GOV-107` conditions). This is confirmed consistent with §13.1 (deterministic, human-in-the-loop) and §13.2 (not adaptive, not ML-driven) — the feature is a manual re-run of an existing check, not a new decision surface.

### 13.5 Semi-Annual Boundary Re-Attestation Cadence (ST-23, BLG-GOV-204, EPIC-05, v8.3)

Every shipped AI/automation-adjacent feature that previously cleared a §13 boundary review is re-attested on a rolling **semi-annual (6-month)** cadence — a lightweight re-confirmation that the feature still operates within the boundaries in §13.1/§13.2, not a full re-review from first principles. This closes a gap: `strategy_rules.md`'s Change Log shows individual §13 reviews accumulating one feature at a time (below), with no standing mechanism ever proposed for re-checking a previously-cleared feature after later, unrelated system changes.

**In scope — shipped features with a recorded §13 clearance (as of this cadence's proposal, 2026-08-06):**

| Feature | §13 Review Record | Cleared |
|---------|-------------------|---------|
| IT-06 (Arc 3 integration) | `docs/product/decisions/decisions--2026-05-15__release-v3.5--IT-06-section13-review.md` | v3.5 |
| SI-01 (pre-entry advisory checks) | `docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md` | v3.8 |
| SI-02 (drift detection) | `docs/product/decisions/decisions--2026-05-30__release-v4.5--SI-02-section13-review.md` | v4.5 |
| SI-04 (strategy history / binding conditions) | `docs/product/decisions/decisions--2026-06-03__release-v5.0--SI-04-binding-conditions.md` | v5.0 |
| BLG-FEAT-50/51 (AI Advisory Layer — daily briefing + chat) | `docs/product/decisions/decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md` | v6.2 |
| PT-04 (Setup Quality Score) | `docs/product/decisions/decisions--2026-07-21__release-v7.7--PT-04-section13-review.md` | v7.7 |
| On-demand compliance recheck (BLG-FEAT-64) | §13.4 above | v6.9 |
| Gemini thesis generation | `docs/specs/api_contracts/gemini_thesis_generation.md` §13 compliance note | (contract-documented, no standalone review record — added to the cadence for its first formal re-attestation) |
| ST-06 — Automated AI Post-Trade Debrief (BLG-FEAT-90) | `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` | v8.9 (**CONDITIONAL** — 9 binding conditions remain in force; one Known Deviation already recorded against Condition 1's literal example text, superseded by BLG-TECH-17/ST-04, v9.0) |

This list is the **starting roster**, not a closed set — any future feature that clears its own §13 review (or pre-assessment, e.g. `arc6_ps03_section13_preassessment.md`, `si04_section13_preassessment.md`) is added to it at that time, per the Maintenance rule below.

**Re-attestation procedure:** For each in-scope feature, confirm:
1. No behavioural change has been made to the feature since its last clearance (or last re-attestation) that would alter its standing against §13.1/§13.2.
2. If a change *has* been made: determine whether it is covered by the existing clearance's stated scope, or requires a fresh full §13 review (per each review record's own "re-confirm only if..." language, where present — e.g. §13.4's own note above).
3. Record the outcome (unchanged / re-reviewed / escalated) in a dated re-attestation log entry — see Maintenance below for where.

**First review date:** 2027-02-06 (6 months from this cadence's proposal date).

**Maintenance:** A future re-attestation pass appends its findings to a new `docs/product/decisions/section13_reattestation_log.md` (create at the first actual re-attestation run, not by this story — no re-attestation has occurred yet as of this proposal). New features entering the roster do so by adding a row to the table above in the same commit that records their own initial §13 clearance.

**Sign-off:** Strategy Rules & System Intent Owner.

### 13.6 Periodic §13 Boundary Review Cadence Tied to SI-02's Gate History (ST-30, EPIC-04, v9.2, BLG-GOV-255)

§13.5's semi-annual cadence re-attests every in-scope feature on a fixed calendar schedule, regardless of how any individual feature is actually behaving. This subsection adds a second, **event-driven** trigger specifically for SI-02 (drift detection) — the one §13.5 roster feature whose gate has its own live, recurring status history (per `roadmap_prompt.md`-adjacent tracking and the SI-02 threshold calibration reviews already on record: `BLG-SPEC-72`, `BLG-SPEC-86`, `BLG-GOV-237`).

**Trigger:** if SI-02's gate status crosses from PASS to a non-PASS state (condition 2 or condition 3 breach, per `BLG-SPEC-72`/`BLG-SPEC-86`'s formalised thresholds) **twice within a rolling 6-month window**, this is treated as a signal that the boundary itself — not just the gate's calibration — may need re-examination, and a full §13 boundary review (not merely a semi-annual re-attestation) is triggered for SI-02 ahead of its next scheduled §13.5 date.

**Rationale:** a single gate breach is expected behaviour (that's what the gate is for — catching drift as it happens) and does not by itself imply the boundary is wrong. Two breaches within 6 months is a different signal: either the gate's thresholds are miscalibrated (a `BLG-SPEC-*` fix, already has a governed path) or the underlying assumption behind SI-02's boundary (that drift is an occasional, correctable deviation rather than a persistent characteristic of current market conditions) may no longer hold — which is a §13 boundary question, not a threshold-tuning question, and belongs to the Strategy Rules & System Intent Owner, not to a routine calibration fix.

**Procedure when triggered:** record the trigger event and its 2 qualifying breach dates in a new dated entry under `docs/product/decisions/section13_reattestation_log.md` (same file §13.5 uses, distinguished by an `Trigger: SI-02 gate-history (§13.6)` tag rather than `Trigger: semi-annual (§13.5)`), and open a full §13 review scoped specifically to whether SI-02's boundary (not just its threshold) remains correct.

**Sign-off:** Strategy Rules & System Intent Owner — Approved. Tying this specifically to SI-02 (rather than generalising to every §13.5 roster feature) is correct — SI-02 is the only roster feature whose gate produces a recurring, dated pass/fail history to trigger from; the other features are point-in-time clearances with no equivalent live signal. The 2-breaches-in-6-months threshold is a reasonable first calibration, consistent with the other 2-cycle/2-instance automatic-escalation thresholds already used elsewhere in this governance system (e.g. `shared_standards.md` §6.4). Sprint Execution Engine (agent-mediated, Strategy Rules & System Intent Owner role — §5.3), 2026-09-08.

---

## 14. Authority statement

This document is the single source of truth for production strategy behaviour.

If a discrepancy exists between code, user interface behaviour, analytics, or user interpretation, this document prevails.

**Guiding principle**  
If a rule can change outcomes, it must be explicit, intentional, and owned.

---

## 15. Version Cross-Reference Consistency Check (ST-41, EPIC-04, v9.2, BLG-GOV-282)

Other documents across the repository cite a specific `strategy_rules.md vX.Y` when recording what was canonical at that point (e.g. a §13 review's binding conditions, a decision record's "Governing Document" field, a changelog entry). These citations are **intentionally historical** — they document what version governed at the time, not a live pointer that must track the current version. This check exists to catch the *different* failure mode: a document that cites a `strategy_rules.md` version **without any dating context**, implying (misleadingly) that it is describing the current/canonical version when it is not being kept in sync.

**Method:** grep the repository for `strategy_rules.md` followed by a version string (`v[0-9]`), outside `strategy_rules.md` itself. For each hit, confirm the citation sits inside a dated, point-in-time artefact (a decision record, changelog entry, governance evidence file, or scope document tied to a specific past cycle) — these are compliant by construction, since their entire purpose is a historical record. Flag any citation that is **not** inside such a dated artefact — e.g. a live spec or currently-active reference document asserting a version number with no date qualifying it as historical.

**First run's findings (2026-09-08):** 7 real citations found outside this file: `docs/System_status_report.md` (dated EPIC-01 delivery-log row, v1.4 — compliant), `docs/product/changelog.md` ×2 (dated changelog rows, v1.3/v1.4 — compliant), `docs/product/scope/scope--2026-03-17__release-v2.0-reporting-alerts.md` (dated scope doc row, v1.3 — compliant), `docs/product/decisions/SRB-v1.7-2026-03-02__release-v1.7.md` (dated decision record's own "Governing Document" field, v1.3 — compliant, correctly records what governed at that decision's time), `docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md` (dated §13 review's binding condition, v1.4 — compliant), `claude/charter/document_lifecycle_guide.md` (a template *example string* — `"strategy_rules.md v2.3 as of 2026-03-04"` — illustrating the checksum-note format, not an actual citation; not a real instance, excluded from the count).

**Triage outcome: 0 actionable findings.** All 6 real citations are correctly scoped as dated, historical point-in-time records; none asserts current-version status without dating context. No corrective action required this run.

**Re-run cadence:** re-run this grep at each future `strategy_rules.md` version bump (the moment new citations are most likely to appear), as part of applying §16's Strategy Rules Change-Justification Template below.

**Sign-off:** Strategy Rules & System Intent Owner — Approved. The check correctly distinguishes "cites an old version because it's a dated historical record" (fine, by design) from "cites a version as if current, undated" (the actual risk) — a naive version-match grep without this distinction would have produced 6 false-positive findings against perfectly correct historical records. Sprint Execution Engine (agent-mediated, Strategy Rules & System Intent Owner role — §5.3), 2026-09-08.

---

## 16. Strategy Rules Change-Justification Template (ST-42, EPIC-04, v9.2, BLG-GOV-306)

Every future `strategy_rules.md` version bump's Change Log entry (table below) should follow this template, so a reader can assess a change's weight without opening a linked decision record:

```markdown
| <version> | <date> | <One-line summary of what changed> (<ST-xx>, <EPIC-xx>, <cycle version>, <BLG-xx>) — <Behavioural/documentation-only classification>. <Rationale: why this change, in one sentence.> <Impact: what it affects — backtests / live logic / documentation only, per §12.3's comparability-acknowledgement requirement.> <§13 gate reference if the change touches an AI/automation boundary, else omit.> |
```

Required elements, in order: (1) what changed, (2) provenance (story/epic/cycle/backlog IDs), (3) behavioural-vs-documentation-only classification (per §12.3's own requirement to "state the rationale and expected impact" and "acknowledge loss of direct comparability with prior results" for behavioural changes), (4) rationale, (5) impact scope, (6) §13 cross-reference where applicable.

**Applied to the next version bump:** this cycle's own §12.2/§13.6/§15/§16 additions (this commit) are the template's first real application — see the Change Log table entry for this version below, written in the format above rather than free prose.

**Sign-off:** Strategy Rules & System Intent Owner — Approved. Self-applying the template to the same commit that introduces it is the right validation — it proves the format is usable in practice rather than only in the abstract. Sprint Execution Engine (agent-mediated, Strategy Rules & System Intent Owner role — §5.3), 2026-09-08.
