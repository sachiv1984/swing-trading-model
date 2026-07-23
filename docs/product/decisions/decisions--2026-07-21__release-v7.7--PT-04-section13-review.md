**Owner:** Head of Specs Team
**Class:** Operational Record (Class 3)
**Status:** Active — PASS
**Last Updated:** 2026-07-24
**Cycle:** 2026-07-21__release-v7.7
**Story:** ST-07 (EPIC-07)
**Backlog ref:** BLG-GOV-28

---

# §13 Boundary Review — PT-04: Setup Quality Score (Retroactive)

**Feature:** PT-04 — Setup Quality Score (scoring algorithm + `GET /trade-plans/setup-quality-score` endpoint)
**Review type:** §13 System Boundary Compliance Review — **retroactive**, against already-shipped implementation
**Cycle:** 2026-07-21__release-v7.7
**Governance reference:** `claude/strategy/strategy_rules.md §13`
**Shipped:** ST-06 (EPIC-02, v3.7 — frontend display) and ST-08 (EPIC-04, v6.1 — backend endpoint)
**Precedent reviews:** `decisions--2026-05-19__release-v3.8--SI-01-section13-review.md`, `decisions--2026-05-30__release-v4.5--SI-02-section13-review.md`

---

## Review Summary

PT-04 shipped across two cycles (v3.7 frontend display, v6.1 backend endpoint) with inline §13 compliance assertions in its design artefacts (`quality-score-display/ux_spec.md §6`, `trade_plan.md`, `pre_trade_research.md`) but never received a **formal, standalone §13 boundary review document** of the kind produced for SI-01 and SI-02. This is a retroactive gap — the feature has been in production since v6.1 (2026-06-23) — flagged for pickup this cycle (per `cycle_summary.md`). This record closes that gap.

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

## PT-04 Feature Description

PT-04 (Setup Quality Score) surfaces a 0–100 score on the Trade Plan detail view (`/trade-plans/{id}`) and Pre-Trade Research View (`/research/{ticker}`), answering: "how similar is this setup to the user's own historically successful entries?"

**Shipped implementation (`backend/routers/trade_plans.py` `get_setup_quality_score`, `GET /trade-plans/setup-quality-score?ticker={ticker}`):**

```
if closed_trade_count < 20:
    return {gate_not_met: true, min_trades_required: 20, current_trades: N}

win_rate = winning_trades / total_closed_trades * 100
avg_pnl = mean(pnl_pct across all closed trades)
score = clamp(round(win_rate * 0.6 + max(avg_pnl, 0) * 0.4), 0, 100)
```

**Contract:** `docs/specs/api_contracts/trade_plan_endpoints.md` §GET /trade-plans/setup-quality-score v0.5 (shipped ST-08, EPIC-04, v6.1). Note: the original v3.7 design artefact (`quality-score-display/ux_spec.md §2`) referenced a hypothetical `GET /trade-plans/{id}/quality-score` path-param form; the implementation settled on the by-ticker query-param form during ST-08 (v6.1), which is what the canonical contract (`trade_plan_endpoints.md`) and `api_changelog.md` document. This is a resolved design-to-implementation refinement, not an open deviation — the canonical contract already reflects the shipped reality and no other document still claims the path-param form as current.

**Frontend:** `trade_plan.md` §7a (Trade Plan detail view) and `pre_trade_research.md` §5 (Research View) — both display-only, read-only, no action affordance, "N/A — insufficient history" state for <20 closed trades.

**§13 compliance assertion from design artefacts (pre-existing, being formally reviewed here):**
> "Display-only; no automated trade actions triggered. Score is labelled as based on historical data... Explicitly not presented as a prediction, recommendation, or instruction." — `quality-score-display/ux_spec.md §6`

---

## §13 Compliance Assessment

### Criterion 1 — Determinism

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Scoring algorithm is pure computation — no random elements | ✅ COMPLIANT | `score = clamp(round(win_rate*0.6 + max(avg_pnl,0)*0.4), 0, 100)` — a fixed arithmetic formula over aggregated trade history fields. No probabilistic scoring, no ML inference. |
| Formula documented | ✅ COMPLIANT | Formula is documented inline in the endpoint docstring, in `api_changelog.md`, and in `trade_plan_endpoints.md` v0.5. |
| Same inputs → same output | ✅ COMPLIANT | Endpoint reads `trade_history` (closed trades only) and computes a pure function of that data; given the same closed-trade state, the result is identical on every call. |

**Criterion 1 determination: COMPLIANT**

---

### Criterion 2 — Display-Only

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Score display labelled as historical reference, not prediction | ✅ COMPLIANT | `trade_plan.md` line 286: "Display-only score labelled as historical reference ('based on your own trade history'). Not a prediction or recommendation." Mandatory sub-label enforced in both placements per `quality-score-display/ux_spec.md §2/§3`. |
| No backend constraint that uses the score to block any endpoint | ✅ COMPLIANT | `get_setup_quality_score` is a pure `GET` with no side effects; no write path (trade plan creation, position entry) reads or checks this score. Confirmed via code read of `backend/routers/trade_plans.py` and `backend/routers/positions.py` — no cross-reference to `get_setup_quality_score` from any write endpoint. |
| No action affordance adjacent to the score | ✅ COMPLIANT | `quality-score-display/ux_spec.md §4`: "No action button or CTA adjacent to the score." Confirmed in shipped `trade_plan.md` §7a and `pre_trade_research.md` §5 — read-only field only. |

**Criterion 2 determination: COMPLIANT**

---

### Criterion 3 — No Adaptive Learning

| Requirement | Status | Evidence |
|-------------|--------|----------|
| PT-04 does not modify strategy parameters | ✅ COMPLIANT | Read-only endpoint; no write path to `settings`, `strategy_rules.md`, or any governance artefact. |
| No ML model trained or updated | ✅ COMPLIANT | Fixed-weight linear formula (0.6/0.4 split), hard-coded, not learned or updated from data. |
| Score is surfaced as read-only display data only | ✅ COMPLIANT | Confirmed — no write-back of the score anywhere; it is computed fresh on each request. |

**Criterion 3 determination: COMPLIANT**

---

### Criterion 4 — No Automated Action

| Requirement | Status | Evidence |
|-------------|--------|----------|
| PT-04 service must not call the Alpaca client | ✅ COMPLIANT | `get_setup_quality_score` reads only `get_portfolio()` and `get_trade_history()` — both local DB reads. No `alpaca_client` import or call in `trade_plans.py`'s scoring function. |
| No automated stop adjustments or position modifications | ✅ COMPLIANT | No path from the score to any position/trade-plan write. |
| No notification tied to the score | ✅ COMPLIANT | No `alert_rules`/`notifications` entry references `setup_quality_score`; this feature has no notification surface at all. |

**Criterion 4 determination: COMPLIANT**

---

### Critical §13 boundary questions

**1. Does the score ever block or modify a trade plan or position entry?**

Confirmed via code read: no write endpoint (`POST /trade-plans`, `POST /portfolio/position`, or their update/exit equivalents) calls or checks `get_setup_quality_score`. The score is fetched independently by the frontend for display only.

**Assessment:** NO. Consistent with §3 (decision support only) and the non-blocking principle established at SI-01/SI-02.

**2. Could the "insufficient history" gate be mistaken for a system judgement (e.g. "this setup is not good enough")?**

The gate (<20 closed trades) is a data-completeness threshold, not a quality judgement — it exists because the formula is statistically meaningless on a small sample, not because the system is withholding approval. The shipped copy ("N/A — insufficient history") and design intent (`quality-score-display/ux_spec.md §6`: "a data completeness indicator, not a system judgement") both frame this correctly.

**Assessment:** Acceptable framing, no §13 concern. No wording change required.

**3. Is there a scope-creep risk from "making the score actionable"?**

No CTA, button, or link exists adjacent to the score in either shipped placement. The formula's fixed 0.6/0.4 weighting is not user-configurable, consistent with the "single, explicit, human-designed strategy" principle (§13.1).

**Assessment:** NO. No scope-creep observed in the shipped implementation.

---

## Determination

**PASS.** All four §13 criteria are COMPLIANT against the shipped implementation. PT-04 is a deterministic, read-only, display-only historical-reference feature with no automated action, no adaptive learning, and no gating power over any trade or position workflow. This retroactive review confirms in a formal governance record what the design artefacts already asserted inline.

---

## Binding Conditions (Forward-Looking)

1. **Display-only is absolute — unchanged going forward.** Any future extension that makes the score gate trade-plan submission, recommend a specific action, or feed an automated remediation would require a new §13 review before implementation (consistent with SI-01/SI-02 precedent condition 9).
2. **Formula changes require documentation.** If the 0.6/0.4 weighting or the 20-trade threshold changes, the change must be documented in `trade_plan_endpoints.md`'s changelog and `api_changelog.md`, with rationale, before shipping.
3. **No binding conditions apply retroactively to the already-shipped code** — the implementation as it exists today requires no changes as a result of this review.

---

## Sign-Off

**Signed off by:** Head of Specs Team
**Date:** 2026-07-24
**Determination:** **PASS**
**Comments:** PT-04 is unambiguously within §13 system boundaries — a deterministic, read-only, advisory-only historical-reference score with no write path, no automated action, and no gating power. The retroactive nature of this review (feature shipped v3.7/v6.1, reviewed v7.7) reflects a formal-documentation gap, not a compliance gap — the design artefacts' inline §13 assertions were correct at the time and remain accurate against the current shipped code. No binding conditions apply to the existing implementation; the three forward-looking conditions above govern any future extension.

**AC sign-off:**
- ✅ §13 checklist run against PT-04's shipped implementation (Setup Quality Score scoring algorithm + API endpoint) — see Compliance Assessment above
- ✅ PASS/FAIL determination documented, with binding conditions recorded (forward-looking only; none apply retroactively)
- ✅ Sign-off recorded by Head of Specs Team (this document)
