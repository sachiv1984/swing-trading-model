**Owner:** Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active — Assessment Complete
**Last Updated:** 2026-06-03
**Cycle:** 2026-06-03__release-v5.0
**Story:** ST-13 (EPIC-04, v5.0)
**Backlog ref:** BLG-BE-26

---

# SI-02 Drift Summary — Feasibility Assessment

**Feature scope assessed:** Read-only drift summary display on System Status or Reports page
**Assessment type:** Feasibility + UX risk evaluation
**Governance reference:** `claude/strategy/strategy_rules.md §13` (§13 advisory context)

---

## Summary

This assessment evaluates whether a lightweight, read-only drift summary (showing aggregated SI-02 behavioural drift metrics) could be added to the System Status or Reports page. The purpose is to surface SI-02 drift data in a low-friction location before the full SI-02 frontend component (gated by BLG-GOV-87 re-entry criteria) is ready.

**Assessment outcome:** **Feasible with conditions** — a read-only drift summary is technically feasible and within scope, but requires UX risk mitigations (framing, threshold calibration advisory, and §13 disclosure) before implementation is sprint-ready.

---

## Feasibility Analysis

### Technical Feasibility

The SI-02 backend service (`/analytics/behavioural-drift`) is implemented and live (v4.6). It returns the following metrics:
- `drift_score`: aggregate drift score (0–100 scale)
- `override_count`: number of strategy overrides
- `validation_pass_rate`: % of trades passing pre-entry validation
- `red_flag_frequency_trend`: trend direction of red flag events

All four metrics are available from a single API call. No new backend work is required for a read-only display. The data is already being computed and stored.

**Technical feasibility: Yes.** The backend data is ready.

### Display Location

**Option A — System Status page** (`/system-status`): Low-traffic, developer-oriented page. Risk: drift metrics would appear alongside server health indicators, potentially creating a false equivalence between "system health" and "strategy behavioural health."

**Option B — Reports page** (`/reports`): Better semantic fit. Drift summary would sit alongside P&L and performance metrics — appropriate context for a behavioural self-assessment. Users visiting Reports expect analytical context.

**Recommended location:** Reports page (Option B). System Status is not the right semantic home for behavioural analytics.

### Minimal Display Scope

If implemented, the minimal display scope recommended for sprint planning:

| Field | Display label | Framing note |
|-------|--------------|--------------|
| `drift_score` | "Drift Score (last 30 days)" | Must include "advisory only — interpret with context" caveat |
| `validation_pass_rate` | "Pre-entry adherence" | Display as % with trend arrow |
| `override_count` | "Overrides this period" | Count only, no judgment framing |

`red_flag_frequency_trend` is appropriate to include in the full SI-02 frontend component but is lower priority for a summary view.

---

## UX Risk Evaluation

### Risk 1 — Drift score without sufficient context (HIGH if unmitigated)

A drift score of, say, 42 is meaningless without:
- Reference range (what's expected vs concerning?)
- Trend context (improving or worsening?)
- Sample size context (how many closed trades is this based on?)

**Mitigation:** Display the drift score with:
- A calibration advisory: "Score is informational — calibration improves as closed-trade history accumulates"
- The number of closed trades in the calculation window
- A simple trend indicator (↑ / ↓ / → vs prior 30 days)

### Risk 2 — §13 compliance framing (MEDIUM)

Drift scores that appear to "rate" the user's trading behaviour could be interpreted as automated performance judgements, which risks the §13 boundary ("not an automated trading bot" / "not a discretionary or adaptive rule system").

**Mitigation:** Apply the §13 advisory framing from the SI-02 §13 review (`decisions--2026-05-30__release-v4.5--SI-02-section13-review.md`):
- Label the section "Behavioural Self-Review" (not "Performance Score" or "Strategy Rating")
- Include a brief §13 compliance note visible in the UI: "Advisory context only — this data does not modify your strategy or trading decisions"
- Past-tense framing: "trades reviewed in this period," "adherence to date"

### Risk 3 — Threshold calibration not established (MEDIUM)

Without a formally calibrated threshold (e.g., "score < 30 = concerning"), any colour-coding or visual emphasis would be arbitrary. Arbitrary thresholds create user confusion.

**Mitigation:** For the initial implementation, display the score without colour-coded status indicators. Use trend arrows only (↑ / ↓ / →). Document that formal thresholds are a future gate condition for the full SI-02 frontend (BLG-GOV-87).

---

## Assessment Outcome

| Dimension | Assessment |
|-----------|-----------|
| Technical feasibility | ✅ Feasible — backend data ready, no new backend work |
| Display location | Reports page (not System Status) |
| UX risk: context/framing | Manageable with mitigations (calibration advisory, sample count, trend only) |
| UX risk: §13 compliance | Manageable with advisory framing and correct section labelling |
| UX risk: threshold calibration | Defer colour-coded status — trend arrows only for initial display |
| Sprint-ready? | **Yes, with conditions** — mitigations above must be included in acceptance criteria |

**Outcome: Feasible and recommended for sprint planning** with the mitigations documented above as acceptance criteria.

---

## Sprint Planning Scope (when promoted)

When SI-02 drift summary is promoted to a sprint, the sprint story should include:

1. Read-only drift summary component on the Reports page
2. Fields: drift score + calibration advisory, pre-entry adherence %, override count, trend indicators
3. §13 framing: "Behavioural Self-Review" label + advisory disclosure note
4. No colour-coded status — trend arrows only until formal thresholds established
5. Sample count displayed alongside drift score
6. Backlog item to be filed for formal threshold calibration (prerequisite for full SI-02 frontend)

---

## Product Owner Sign-Off

**Assessment reviewed by:** Product Owner
**Date:** 2026-06-03
**Disposition:** Feasible — proceed with sprint planning inclusion when capacity allows
**Comments:** The mitigations are appropriate. The key guard is the Reports page location (not System Status) and the advisory-only framing. No colour-coded status until calibrated thresholds are established — this prevents the drift score from being misread as a pass/fail system judgement. BLG-BE-26 scope updated: feasibility confirmed; implementation ready for sprint planning with acceptance criteria as documented above.
