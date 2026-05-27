**Owner:** Strategy Rules & System Intent Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-27
**Cycle:** 2026-05-26__release-v4.1 (ST-13, BLG-GOV-44)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# SI-02 §13 Evidence Criteria

## 1. Purpose

This document defines the evidence criteria that SI-02 (Behavioural Drift Detection) must satisfy to pass the §13 governance review. The §13 review in `claude/strategy/strategy_rules.md` requires that any system feature be assessed against four determinism and autonomy criteria before it can be implemented.

By defining these criteria in advance, the SI-02 sprint planning team has a clear pass/fail framework rather than conducting the §13 review ad hoc during planning.

---

## 2. §13 Review Framework

The §13 governance review evaluates any feature against:

| Criterion | Description | SI-02 Assertion |
|-----------|-------------|-----------------|
| **Determinism** | Does the feature produce consistent, reproducible outputs from the same inputs? | Must be YES |
| **Display-only** | Is the feature display-only (no automated trading decisions, no adaptive rule changes)? | Must be YES |
| **No adaptive learning** | Does the feature alter trading rules, parameters, or strategy logic based on detected drift? | Must be NO |
| **No automated action** | Does the feature trigger any automated action (order placement, position modification, alert escalation to non-advisory) based on detected drift? | Must be NO |

---

## 3. SI-02 Assertion Evidence

### 3.1 Determinism

**Assertion:** SI-02 drift analysis is deterministic given the same trade history and strategy rules as inputs.

**Evidence required:**
- The drift detection algorithm must be pure computation (no random elements, no machine-learning inference, no probabilistic scoring without documented formula)
- For each drift metric (entry timing, sizing adherence, regime context), the calculation must be documented as a formula or decision tree in `docs/specs/metrics_definitions.md` before sprint planning seals
- The API response for `GET /analytics/behavioural-drift` (or equivalent endpoint) must return identical results when called twice with unchanged data

**Binding condition:** All drift formulas documented in `metrics_definitions.md` before SI-02 sprint planning seals.

### 3.2 Display-Only

**Assertion:** SI-02 outputs are advisory displays only. No detection result gates, blocks, or modifies a trade plan, position entry, or exit.

**Evidence required:**
- The drift display (frontend component) must be labelled "Advisory" or equivalent
- No constraint exists in the backend that uses drift state to block `POST /trade-plans`, `POST /portfolio/position`, or any exit endpoint
- The spec for `GET /analytics/behavioural-drift` explicitly states: "display advisory only; not a submission gate"

**Binding condition:** The API contract for the SI-02 endpoint must include an explicit "display-only advisory" declaration, consistent with `strategy_rules.md §4.2` (pre-entry advisory checks precedent).

### 3.3 No Adaptive Learning

**Assertion:** SI-02 does not modify strategy parameters, update `strategy_rules.md`, or alter user settings based on detected drift.

**Evidence required:**
- The SI-02 implementation may not write to `settings` table, `strategy_rules.md`, or any governance artefact
- Drift findings may only be surfaced as read-only display data; the user acts on findings manually
- No ML model is trained or updated based on trade history for this feature (statistical aggregation only)

**Binding condition:** Code review at EPIC closure must confirm: no write operations to `settings` or governance files from SI-02 service layer.

### 3.4 No Automated Action

**Assertion:** SI-02 drift detection triggers no automated orders, stop adjustments, or position modifications.

**Evidence required:**
- The SI-02 service must not call `alpaca_client`, position service write methods, or notification escalation paths beyond standard informational notifications
- Any Telegram notification for drift (if implemented) must be advisory only and scoped to a new `drift_alert` type — not re-using existing enforcement notification types
- The `alert_rules` table must not include a `behavioural_drift` type that triggers automated evaluation

**Binding condition:** SI-02 API contract must not list any write side-effects. Code review must confirm no calls to write services from the drift analysis path.

---

## 4. Binding Conditions Summary

Before the SI-02 §13 review gate can be cleared, all of the following must be true:

| Condition | Owner | Evidence Path |
|-----------|-------|---------------|
| All drift formulas documented in `metrics_definitions.md` | Metrics Definitions & Analytics Owner | `docs/specs/metrics_definitions.md` SI-02 section |
| API contract for SI-02 endpoint includes "display-only advisory" declaration | API Contracts & Documentation Owner | `docs/specs/api_contracts/` SI-02 contract |
| No write operations to settings/governance from SI-02 service | Head of Backend Engineering | Code review at EPIC closure |
| No automated action pathway | Head of Backend Engineering + Cybersecurity & Trust Lead | Code review + API contract review |

---

## 5. Challenger Review Points

The Challenger role must verify the following during the §13 review:

1. **Scope creep risk:** Is there pressure to make the drift panel "actionable" (e.g. one-click "fix my sizing")? Any such feature requires a separate §13 review.
2. **Notification boundary:** Does any drift notification escalate beyond advisory? Advisory = informational; non-advisory = gates or modifies behaviour.
3. **Formula transparency:** Are all drift thresholds user-configurable or hard-coded? Hard-coded thresholds require documented rationale; configurable thresholds require a `settings` field (which is a separate schema change).

---

## 6. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Strategy Rules & System Intent Owner | Pending | — |
