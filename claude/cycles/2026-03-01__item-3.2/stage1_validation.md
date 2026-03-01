# Stage 1 — Roadmap Re-Validation

**Cycle:** 2026-03-01__item-3.2
**Date:** 2026-03-01
**Authorities:** Product Owner + Strategy Rules & System Intent Owner

---

## Active Initiatives Reviewed

---

### v1.7 — Foundation & Governance

#### BLG-TECH-04 — CI/CD GitHub Actions Validation Workflow
**Classification:** 🔥 Must continue

**Justification:**
BLG-TECH-02 is now complete (severity model exists), unblocking this item. The system currently has no automated merge gate for critical validation failures. With v1.6.1 shipped and correctness work done, the next release cycle is exposed without this gate. The risk of regression without automated CI/CD is real and increasing as the spec surface grows.

**What has changed:** BLG-TECH-02 and BLG-TECH-03 are now complete. The dependency is cleared. This item is now unblocked and ready for implementation.

---

#### Strategy Rules §13 Boundary Review
**Classification:** 🔥 Must continue

**Justification:**
Three features are gated behind this review: Signal Exposure Enhancement (4.3), AI Journal Summarisation, and New Technical Indicators. Without a documented §13 decision, none of these features can enter pre-alignment. The review is a prerequisite gate for v2.0 candidates. It is a governance and product-design task, not an engineering task — it is low-effort and high-leverage. Deferring it pushes back v2.0 pre-alignment.

**Strategy Rules & System Intent Owner note:** §13 boundaries remain unchanged as of v1.3. No feature has shipped that altered system boundaries. The review is appropriate and necessary before any gated feature proceeds.

---

#### Metrics Definitions — Portfolio Heat Formula & Thresholds
**Classification:** 🔥 Must continue

**Pre-requisite:** This is the hard gate for v1.8 (Risk Dashboard). Without canonical heat formula and thresholds in `metrics_definitions.md`, the Risk Dashboard may not enter pre-alignment. The formula and thresholds are not complex — the work is definitional, not engineering.

**What has changed:** v1.6.1 shipped Current Drawdown Widget (BLG-FEAT-01). The drawdown data is now live. This validates the appetite for risk-visibility features and increases the case for completing the heat formula to unlock v1.8.

---

#### Structured Logging / Observability Standards
**Classification:** 🔥 Must continue

**Justification:**
v2.0 introduces Alerts & Notifications with async processing. Without observability standards, async failure modes are unobservable and undebuggable. This is a pre-work gate for v2.0. The Head of Engineering owns this. The effort is ~1 day.

---

#### API Versioning Strategy Decision Record
**Classification:** 🔥 Must continue

**Justification:**
v2.0 (Alerts) may introduce webhook or async patterns. The API versioning policy must be decided before these patterns are introduced. This is a decision record task, ~0.5 days.

---

### v1.8 — Risk Dashboard

#### 3.4 Risk Dashboard
**Classification:** 🔥 Must continue

**Justification:**
Risk visibility is a core daily use case. The planned page (heat gauge, drawdown, grace period panel, position-level risk table, prospective heat indicator) builds entirely on existing endpoints except for the heat calculation. v1.6.1 shipped the Current Drawdown Widget and Grace Period Indicator, confirming user value for risk-visibility features. The pre-requisite (metrics definitions for heat formula) is a v1.7 gate that remains on track.

**Note:** Current Drawdown Widget and Grace Period Indicator shipped in v1.6.1. The Risk Dashboard spec must reflect that these may already exist on the dashboard and should not duplicate them — the scope should be reconciled in pre-alignment.

---

### v1.9 — User Value & Insight

#### 5.1 Structured Trade Reflection Template
**Classification:** 🔥 Must continue

**Justification:**
High-value discipline feature. Pre-populated from trade record, no AI, fully deterministic. Pre-requisite is BLG-FEAT-08 (Compliance Metrics definitions). Still strategically sound — the existing journal system (v1.4) provides the foundation. No market or technical change has reduced its value.

---

#### BLG-FEAT-08 — Basic Compliance Metrics
**Classification:** 🔥 Must continue

**Justification:**
Pre-work gate for 5.1. Lightweight (~1 day). Compliance metric definitions must enter `metrics_definitions.md` before implementation. Still warranted.

---

#### 5.2 Cohort Analysis
**Classification:** 🔥 Must continue

**Justification:**
Derivable entirely from existing trade data. Extends the Performance Analytics page. No new backend dependencies beyond a new query. As the system accumulates more trade history, cohort analysis becomes more valuable over time. Still on strategy.

---

#### 5.3 Dashboard Homepage / Session Summary
**Classification:** 🔥 Must continue

**Justification:**
All data already available from existing endpoints. Makes the product feel complete for daily use. With v1.6.1 shipping 6 user-facing features, the product now has richer data to surface on a homepage. This item's value has increased, not decreased.

---

### v2.0 — Reporting & Alerts

#### 3.5 Alerts & Notifications
**Classification:** ⚠ Re-evaluate

**Justification:**
Pre-requisites (observability standards, API versioning) remain incomplete (v1.7). QA planning session has not yet occurred. The testing surface for email/SMS delivery is significantly larger than the effort estimate implies. While the feature is still strategically sound, the pre-requisite chain is long and the QA complexity deserves re-examination before this moves to active planning. Will be reviewed at the v2.0 pre-alignment gate — not removing from roadmap.

**Required resolution by STEP 8:** Must be re-committed (🔥) with explicit justification or deferred with conditions.

---

#### 4.1a — CSV Export of Trade History
**Classification:** ❌ Consider stopping

**Justification:**
BLG-FEAT-07 shipped in v1.6.1. This item is explicitly superseded. The roadmap already notes "(may already ship via BLG-FEAT-07 in v1.6.1)" and "If BLG-FEAT-07 ships in v1.6.1, this item is superseded." It has shipped. This item should be killed (closed as superseded).

---

#### 4.1b — Tax-Year P&L Statement
**Classification:** 🔥 Must continue

**Justification:**
High-value financial record for tax purposes. Requires its own canonical spec and dedicated report endpoint — separate from analytics. No change to strategic fit. Still a v2.0 candidate.

---

#### 4.1c — Server-Side PDF Report
**Classification:** 🔥 Must continue

**Justification:**
Replaces brittle browser-print approach. Consistent with existing analytics capability. Still medium-value and technically clean.

---

#### 4.3 — Signal Exposure Enhancement
**Classification:** ⚠ Re-evaluate

**Justification:**
This item is gated behind a `strategy_rules.md` update confirming `top_n` and `lookback_days` are formally user-configurable. That gate is part of the §13 boundary review (v1.7 item). If the §13 review confirms these parameters are user-configurable, this item advances to active planning. If the review finds that exposing them would constitute a configurable strategy builder (§13 violation), this item is killed. Must not be treated as active until the gate is cleared.

**Required resolution:** Dependent on §13 boundary review outcome (v1.7). Re-evaluate classification post-review.

---

### Priority 2 — Next Phase

#### 4.2 Watchlists & Screening
**Classification:** 🔥 Must continue

**Justification:**
Marked "do not pull forward" — this remains appropriate. No change to strategic fit. Confirmed at current priority.

---

#### Chart Interactivity Enhancements
**Classification:** 🔥 Must continue

**Justification:**
Low-Medium effort. Adds value to existing analytics page without new data dependencies. Scope boundary (no new technical indicators) is clear. Confirmed at current priority.

---

## Summary Table

| Initiative | Classification | Action required |
|-----------|----------------|-----------------|
| BLG-TECH-04 CI/CD | 🔥 Must continue | None |
| §13 Boundary Review | 🔥 Must continue | None |
| Metrics Defs — Heat Formula | 🔥 Must continue | None |
| Structured Logging | 🔥 Must continue | None |
| API Versioning Decision | 🔥 Must continue | None |
| 3.4 Risk Dashboard | 🔥 Must continue | Reconcile scope re: v1.6.1 features in pre-alignment |
| 5.1 Trade Reflection | 🔥 Must continue | None |
| BLG-FEAT-08 Compliance Metrics | 🔥 Must continue | None |
| 5.2 Cohort Analysis | 🔥 Must continue | None |
| 5.3 Dashboard Homepage | 🔥 Must continue | None |
| 3.5 Alerts & Notifications | ⚠ Re-evaluate | Resolve by STEP 8 |
| 4.1a CSV Export | ❌ Consider stopping | Kill — superseded by BLG-FEAT-07 |
| 4.1b Tax-Year P&L | 🔥 Must continue | None |
| 4.1c Server-Side PDF | 🔥 Must continue | None |
| 4.3 Signal Exposure | ⚠ Re-evaluate | Resolve post §13 review (v1.7 gate) |
| 4.2 Watchlists | 🔥 Must continue | Confirm hold at Priority 2 |
| Chart Interactivity | 🔥 Must continue | Confirm hold at Priority 2 |
