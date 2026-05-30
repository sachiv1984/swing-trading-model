**Owner:** Strategy Rules & System Intent Owner
**Class:** Operational Record (Class 3)
**Status:** Active — PASS
**Last Updated:** 2026-05-30
**Cycle:** 2026-05-30__release-v4.5
**Story:** ST-06 (EPIC-03)
**Backlog ref:** BLG-GOV-39

---

# §13 Boundary Review — SI-02: Behavioural Drift Detection

**Feature:** SI-02 — Behavioural Drift Detection (entry timing, sizing adherence, regime context, consecutive loss context)
**Review type:** §13 System Boundary Compliance Review
**Cycle:** 2026-05-30__release-v4.5
**Governance reference:** `claude/strategy/strategy_rules.md §13`
**Evidence criteria pre-defined in:** `docs/specs/si02/section13_criteria.md` (v4.1, BLG-GOV-44)
**Sprint backlog AC reference:** `claude/cycles/2026-05-30__release-v4.5/stage4_backlog_slice.md#ST-06`
**Precedent review:** `docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md`

---

## Review Summary

This record documents the formal §13 boundary review required before SI-02 implementation stories (backend service, drift query, frontend display) may proceed. ST-06 (this review) must produce a PASS or FAIL determination. ST-07 (metric definition) and ST-08 (data schema) may proceed to execution in parallel with this PASS, but the SI-02 implementation sprint may not seal without this review on record.

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

## SI-02 Feature Description

SI-02 implements behavioural drift detection — an analytics feature that compares a user's actual trading behaviour (entries, sizing, regime choices) against their stated strategy rules over time. It asks: "Are your actual entries drifting from your stated setup criteria?"

**Four drift metrics in scope (from `docs/specs/si02/si02_fe_component_predesign.md §3`):**

| Metric | What it measures | Data source |
|--------|-----------------|-------------|
| Entry timing drift | Days from signal date to actual entry date | `trade_history.entry_date` − `signals.signal_date` (requires DS-07 migration) |
| Sizing adherence | Is `risk_percent_used` staying within stated plan limits per trade? | `trade_plans.risk_percent_used` vs. strategy max |
| Consecutive loss context | Is position sizing adjusted appropriately after a run of losses? | Rolling loss window self-join on `trade_history` |
| Regime context | Are trades being entered in the declared correct market regime? | `trade_plans.regime_context_at_entry` |

**Delivery components (from pre-design artefacts):**
- Backend: `GET /analytics/behavioural-drift` — read-only query endpoint returning drift metrics per portfolio
- Frontend: `DriftDetectionPanel` component (display-only advisory, no action affordances)
- Background job: scheduled recalculation of drift snapshots (read-only writes to analytics table only)

**§13 compliance assertion from sprint pre-design artefacts:**
> "Advisory panel — display-only. Drift score is informational only; no automated remediation action, no submission gate, no position modification." — `docs/specs/si02/si02_fe_component_predesign.md §2`

---

## §13 Compliance Assessment

### Evidence criteria review (per `docs/specs/si02/section13_criteria.md`)

#### Criterion 1 — Determinism

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Drift algorithm is pure computation — no random elements | ✅ COMPLIANT | All four metrics are aggregation functions on stored trade history data (averages, differences, counts). No probabilistic scoring, no ML inference. |
| Formula documentation required before sprint planning seals | ✅ MET — addressed by ST-07 | Metric definition document (`docs/specs/metrics/si02_drift_score.md`) produced as ST-07 deliverable. Formulas are deterministic SQL aggregations + threshold comparisons. |
| Same inputs → same output | ✅ COMPLIANT | Endpoint is read-only against append-only tables; given the same trade_history state, the result is identical on every call. |

**Criterion 1 determination: COMPLIANT**

---

#### Criterion 2 — Display-Only

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Drift display labelled "Advisory" or equivalent | ✅ COMPLIANT (by spec) | `si02_fe_component_predesign.md §2`: "the drift display must be labelled 'Advisory' or equivalent — the label must be visible without hover or expansion" |
| No backend constraint that uses drift state to block any endpoint | ✅ COMPLIANT | The `GET /analytics/behavioural-drift` endpoint is a pure read. No write path uses drift state. The service layer must not call position service write methods or trade plan service write methods. |
| API contract includes "display-only advisory" declaration | ✅ TO BE CONFIRMED — binding condition | The SI-02 API contract (to be written in SI-02 sprint) must include this declaration. This is a binding condition on ST-03 of the SI-02 implementation sprint. |

**Criterion 2 determination: COMPLIANT (with one forward binding condition on SI-02 sprint)**

---

#### Criterion 3 — No Adaptive Learning

| Requirement | Status | Evidence |
|-------------|--------|----------|
| SI-02 does not modify strategy parameters | ✅ COMPLIANT | Drift detection is read-only analytics. No write path to `settings`, `strategy_rules.md`, or governance artefacts from the drift service. |
| No ML model trained or updated | ✅ COMPLIANT | All drift metrics are deterministic threshold comparisons. No ML inference layer. Statistical aggregation only (rolling means, deviation counts). |
| Drift findings may only be surfaced as read-only display data | ✅ COMPLIANT | Users act on findings manually; the system provides no auto-remediation. |

**Criterion 3 determination: COMPLIANT**

---

#### Criterion 4 — No Automated Action

| Requirement | Status | Evidence |
|-------------|--------|----------|
| SI-02 service must not call Alpaca client | ✅ COMPLIANT (by spec intent) | Drift detection is a portfolio analytics read operation. No market data write, no order execution path. Binding condition: code review at SI-02 EPIC closure must confirm no `alpaca_client` calls from drift service. |
| No automated stop adjustments or position modifications | ✅ COMPLIANT | SI-02 output is a set of displayed metrics. No path from drift score to position modification. |
| Telegram notification must be advisory-only if implemented | ✅ COMPLIANT (advisory) | If drift notifications are included in scope, they must use a new `drift_alert` notification type clearly scoped as advisory. The `alert_rules` table must not include a drift type that triggers automated evaluation. This is a binding condition on SI-02 sprint scoping. |

**Criterion 4 determination: COMPLIANT**

---

### Critical §13 boundary questions

**1. Does drift state ever block or modify a trade plan or position entry?**

Based on all SI-02 pre-design artefacts reviewed:
- The `DriftDetectionPanel` is a standalone read-only panel (not embedded in the trade plan creation form)
- No drift check is wired into `POST /trade-plans` or `POST /portfolio/position`
- The drift endpoint is called independently; its results have no routing path to any entry gate

**Assessment:** NO. Drift state does not block, gate, or modify any trade workflow. This is consistent with §3 (the system provides decision support only) and §4.2.6 (non-blocking principle is binding).

**2. Does the consecutive loss context metric introduce a sizing rule?**

The consecutive loss metric surfaces historical data to the user (e.g. "you entered 3 positions after 5 consecutive losses"). It does not impose any constraint on the current position entry. The user may inspect this information and apply their own judgment.

**Assessment:** NO. This metric is informational display only. It does not enforce or recommend a sizing change. The non-blocking principle (§4.2.6) applies.

**3. Is there a scope creep risk from "making it actionable"?**

The `si02_fe_component_predesign.md §2` explicitly states: "Not present any UI affordance (button, link, or action prompt) that implies automated remediation." This constraint is carried forward as a binding condition.

**Challenger check (from `section13_criteria.md §5`):**
- ✅ No "fix my sizing" button in scope — confirmed by pre-design
- ✅ Notification boundary: any drift alert must be informational only (binding condition)
- ⚠️ Formula transparency: drift thresholds (green/amber/red bands) are defined in ST-07 metric definition — they are hard-coded in the service, not user-configurable. This requires documented rationale in `docs/specs/metrics/si02_drift_score.md`. Addressed as ST-07 deliverable.

---

## §13 Conditions for Implementation (Binding on SI-02 Sprint)

The following conditions are mandatory for SI-02 implementation stories. They are not optional.

1. **Display-only is absolute.** The drift panel must never prevent, gate, or auto-reject any trade plan or position entry. All drift information is advisory only. This is consistent with §4.2.6, §4.1.7, and §3.

2. **Only deterministic aggregation.** All drift calculation logic must use pure SQL aggregation against stored data. No ML models, no probabilistic inference, no random elements.

3. **No write operations from drift service.** The SI-02 service layer must not call Alpaca client, position service write methods, trade plan write methods, or settings write methods. Read-only writes to a dedicated `drift_snapshots` analytics table (if caching is implemented) are the only permitted writes.

4. **API contract must include advisory declaration.** The `GET /analytics/behavioural-drift` (or equivalent) contract must include: "display-only advisory; not a submission gate; no side-effects." This is a binding condition on the API Contracts & Documentation Owner at SI-02 sprint contract review.

5. **Frontend component must carry no action affordances.** No buttons, links, or prompts implying automated remediation. The drift panel is observation-only.

6. **Notification type constraint.** If drift notifications are implemented in scope, a new `drift_alert` notification type must be created. It must not re-use enforcement notification types. The `alert_rules` table must not include a drift type that triggers automated evaluation.

7. **§13 compliance note required.** The backend drift service file must include a comment referencing this decision record and affirming: "display-only advisory; no position write; no automated action; §13 PASS — decisions--2026-05-30__release-v4.5--SI-02-section13-review.md."

8. **Threshold rationale documented.** Green/amber/red threshold values must be documented with rationale in `docs/specs/metrics/si02_drift_score.md` before the SI-02 sprint planning seals.

9. **Any future "actionable" extension requires a new §13 review.** If a future sprint proposes adding any auto-remediation, one-click sizing adjustment, or constraint that modifies trade plan behaviour based on drift state, a new §13 review is mandatory before implementation.

---

## FAIL Implications (for reference)

Had this been a FAIL:
- ST-07 and ST-08 would be advisory-only outputs (spec pre-work, no sprint activation)
- SI-02 would be re-parked in the backlog with a blocking §13 objection
- Sprint planning for SI-02 would require §13 re-review before sealing

---

## Sign-Off

**Signed off by:** Strategy Rules & System Intent Owner
**Date:** 2026-05-30
**Determination:** **PASS**
**Comments:** SI-02 Behavioural Drift Detection is clearly within §13 system boundaries. The feature is deterministic read-only analytics, human-in-the-loop by design, and explicitly non-blocking — consistent with the SI-01 precedent (§4.2.6 non-blocking principle). The critical §13 question (does drift state ever block or modify a trade workflow?) is answered unambiguously: it does not.

The consecutive loss context metric requires particular attention to framing — it must surface historical data without implying a sizing mandate. The pre-design constraint ("no action affordance") correctly handles this.

Nine binding conditions above are mandatory for SI-02 implementation. The three forward conditions (API advisory declaration, notification type, threshold rationale) are addressed by ST-07, ST-08, and the SI-02 API contract story. All four §13 criteria confirmed COMPLIANT.

**AC sign-off (AC-01–AC-05):** All acceptance criteria from `stage4_backlog_slice.md#ST-06` met:
- AC-01: ✅ §13 review completed against SI-02 story set; determination: PASS documented above
- AC-02: ✅ Review confirms drift detection output is deterministic, display-only, no automated recommendations (see Criterion 1–4 above)
- AC-03: ✅ Binding conditions documented in §13 Conditions section (nine binding conditions)
- AC-04: ✅ Sign-off recorded in this document; Strategy Rules & System Intent Owner confirmed
- AC-05: N/A — no FAIL escalation required
