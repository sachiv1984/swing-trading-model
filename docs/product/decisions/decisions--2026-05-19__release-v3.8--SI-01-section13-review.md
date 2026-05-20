**Owner:** Strategy Rules & System Intent Owner
**Class:** Operational Record (Class 3)
**Status:** Active — PASS
**Last Updated:** 2026-05-20
**Cycle:** 2026-05-19__release-v3.8
**Story:** ST-01 (EPIC-01, v3.8)

---

# §13 Boundary Review — SI-01: Pre-Entry Rule Validation

**Feature:** SI-01 — Pre-Entry Validation Service + Advisory Panel
**Review type:** §13 System Boundary Compliance Review
**Cycle:** 2026-05-19__release-v3.8
**Governance reference:** `claude/strategy/strategy_rules.md §13`
**Sprint backlog AC reference:** `claude/cycles/2026-05-19__release-v3.8/stage4_backlog_slice.md#ST-01`

---

## Review Summary

This record documents the formal §13 boundary review required before SI-01 implementation stories (ST-02 — backend validation service, ST-03 — frontend panel) may proceed. ST-01 (this review) must produce a PASS or FAIL determination before any SI-01 implementation begins.

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

## SI-01 Feature Description

SI-01 implements two components:

**ST-02 — Backend Validation Service:**
- New endpoint: `GET /portfolio/pre-entry-validation?ticker={ticker}&quantity={n}`
- Checks a proposed position against strategy pre-entry conditions
- Returns per-rule advisory results (pass/warn/fail) and an aggregate advisory status
- Non-blocking: all check results are advisory; no hard enforcement occurs in the backend

**ST-03 — Frontend Advisory Panel:**
- Read-only advisory panel within the Trade Plan creation form
- Displays per-rule check results with pass/warn/fail visual indicators
- Override capability: user may acknowledge and proceed; acknowledgement is recorded on the trade plan object
- Panel hidden when no ticker or quantity is set
- No submission gate — the panel is informational only; plan creation is never blocked

**§13 compliance assertion from sprint backlog ST-03 notes:**
> "Advisory panel — non-blocking. Override flow with override acknowledgement recorded on trade plan object. §13 compliant — decision support, not a hard gate."

---

## §13 Compliance Assessment

### Compliance criteria

| Criterion | Status | Notes |
|-----------|--------|-------|
| Feature provides information only — no automated decision | ✅ COMPLIANT | Panel is display-only advisory; no automated action triggered by validation result |
| Non-blocking — submission never prevented | ✅ COMPLIANT | Consistent with §4.1.7 precedent: "An invalid or cash-constrained sizing result does not block form submission" |
| No automated order execution | ✅ COMPLIANT | Advisory output only; user retains full control of trade plan creation and position entry |
| Human-in-the-loop preserved | ✅ COMPLIANT | Override is user-initiated; no rule result blocks or bypasses user decision |
| Deterministic rules only — no ML or inference | ✅ COMPLIANT | Sprint backlog: "No ML — purely deterministic aggregation / rule checks" |
| Override acknowledgement is metadata, not a gate bypass | ✅ COMPLIANT | Override is recorded on the trade plan object for auditability; it does not modify any calculation |
| Not a real-time streaming system | ✅ COMPLIANT | Validation is request-driven on ticker/quantity input; no persistent connection |
| Not a discretionary or adaptive rule system | ✅ COMPLIANT | Rules are drawn from strategy_rules.md; no runtime rule modification |

### Critical §13 boundary — non-blocking enforcement

The most sensitive §13 question for SI-01 is: **does the advisory panel ever block or prevent plan submission?**

Based on the SI-01 spec:
- ST-02 backend returns advisory results only — no hard enforcement in the API response
- ST-03 frontend is explicitly non-blocking: the plan can be submitted regardless of panel state
- The override acknowledgement records the user's informed decision; it does not unlock a submission gate

**Assessment:** The system does NOT block plan submission based on validation results. This is consistent with §4.1.7 (Position Sizing Calculator) and §3 (the system provides decision support only). The override record is an informational audit trail, not a circumvention mechanism.

### Critical §13 boundary — rule grounding

The sprint backlog specifies five rule types to validate: regime gate, position sizing, sector concentration, earnings proximity, cash constraint. This review distinguishes two categories:

**Category A — Directly grounded in strategy_rules.md:**
- Regime gate: §8.2 (market risk-off regime is a defined exit/avoidance condition)
- Position sizing validity: §4.1.4 (deterministic validity constraints — stop distance, portfolio value)
- Cash constraint: §4.1.6 (explicit execution feasibility gate)

These three checks may be implemented directly. The rules, parameters, and validity conditions are explicit in the strategy document.

**Category B — Not currently in strategy_rules.md:**
- Sector concentration threshold: no canonical concentration limit is defined in the strategy document
- Earnings proximity warning: no strategy rule currently governs position entry relative to earnings events

**Binding condition (see §Conditions below):** Category B checks may only be implemented in ST-02 if the corresponding rules are formally added to strategy_rules.md v1.4 in the same commit as the ST-02 backend implementation. If the ST-02 author chooses not to define those rules, Category B checks must be deferred to a future sprint (a backlog item must be filed via /backlog-add before the PR opens). The three Category A checks are sufficient to satisfy the ST-02 AC on their own.

---

## §13 Conditions for Implementation

The following conditions are binding on ST-02 and ST-03 implementation. They are not optional.

1. **Non-blocking is absolute.** The pre-entry validation endpoint and the advisory panel must never prevent, gate, or auto-reject a trade plan submission. Any fail-severity result is advisory only. This is consistent with §4.1.7 and §3 of strategy_rules.md and must not be deviated from.

2. **Only deterministic rule checks.** All validation logic must be derivable from explicit rules in strategy_rules.md or formally added to strategy_rules.md before ST-02 merges. No heuristics, ML models, or inferred conditions.

3. **Category A checks are immediately authorised.** Regime gate (§8.2), position sizing validity (§4.1.4), and cash constraint (§4.1.6) may be implemented directly. No further review required for these three.

4. **Category B checks require rule formalisation first.** Sector concentration and earnings proximity may only be implemented in ST-02 if the rules — including specific thresholds, severity classification (warn vs. fail-advisory), and rationale — are added to strategy_rules.md in the same commit. The strategy document version must be bumped, and the prompt_change_log.md must be updated. If formalised, this is not a change to trading behaviour — it is making existing judgment explicit.

5. **Override acknowledgement is trade plan metadata only.** The recorded override must not affect stop calculation, position sizing, signal scoring, screener results, regime detection, or any other calculated output. It is informational only.

6. **No cross-contamination.** Validation results must not be fed into signals, screener scoring, or any other automated pipeline. Results are computed on demand, returned to the frontend, and discarded server-side.

7. **§13 compliance note required in backend service file.** A comment referencing this decision record and affirming the non-blocking, advisory-only constraint must appear in the backend pre-entry validation service file.

8. **Panel is display-only.** The frontend panel must contain no action buttons other than the override acknowledgement. No fields are modified by validation results.

---

## FAIL Implications (for reference)

Had this been a FAIL:
- ST-02 and ST-03 would be removed from Sprint 2 scope
- EPIC-01 would be closed as gate-failed for this cycle
- SI-01 would be re-parked in the backlog for a future sprint

---

## Sign-Off

**Signed off by:** Strategy Rules & System Intent Owner
**Date:** 2026-05-20
**Determination:** PASS
**Comments:** SI-01 Pre-Entry Rule Validation is clearly within §13 system boundaries. The feature is deterministic decision-support, human-in-the-loop by design, and explicitly non-blocking — consistent with §4.1.7 and §3 precedent. The critical §13 question (does the panel block submission?) is answered unambiguously: it does not. The override acknowledgement is metadata only.

The only constraint requiring attention is Category B rule grounding (sector concentration, earnings proximity). These checks are valid momentum-strategy concerns but are not currently in strategy_rules.md. The binding conditions above govern how ST-02 must handle this. ST-02 may implement three Category A checks immediately; Category B implementation is conditional on same-commit rule formalisation in strategy_rules.md.

All eight compliance criteria confirmed COMPLIANT. Eight binding conditions above are mandatory for ST-02 and ST-03. Any future extension to SI-01 that introduces automated enforcement (i.e. preventing submission based on validation results) requires a new §13 review before implementation.
