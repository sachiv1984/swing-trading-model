# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-02-20

> ⚠️ Standing Notice
> This backlog records prioritisation and intent only.
> All formulas, schemas, API contracts, and behavioural rules are indicative until
> confirmed in the relevant canonical specifications.
> No item may proceed to implementation without canonical owner sign-off.

---

## Priority Definitions

- **P0 — Critical**: Blocks correctness, trust, or release safety
- **P1 — High**: Enables core workflows or governance
- **P2 — Medium**: High leverage but not blocking
- **P3 — Low**: Nice-to-have or future scale

---

## 1. Platform & Validation Governance Backlog

These items ensure analytical correctness, validation integrity, and operational safety.
They are not user-facing, but they directly affect trust in outputs and release confidence.

---

### BLG-TECH-01 — Fix Sharpe variance method + Capital Efficiency currency basis
**Priority:** P0 (Critical)
**Type:** Metrics Correctness / Validation Integrity

**Problem**
- Sharpe ratio currently uses population variance instead of sample variance.
- Capital efficiency uses `entry_price * shares` instead of actual GBP cost.
- Validation cannot reliably detect non-conformant behaviour.

**Scope**
- Fix `_calculate_sharpe()` to use sample variance (divide by n-1) for:
  - Portfolio Sharpe
  - Trade-level Sharpe
- Fix capital efficiency to use `total_cost (GBP)` from `trade_history`.
- Update `validation_data.py` expected values accordingly.

**Acceptance Criteria**
- Validation passes with updated expected values.
- Metrics Definitions & Analytics Canonical Owner signs off on expected values.
- No regression in existing analytics outputs.

**Owners**
- Engineering (implementation)
- QA (verification)
- Metrics Definitions & Analytics Canonical Owner (sign-off)

---

### BLG-TECH-02 — Implement validation severity model
**Priority:** P1 (High)
**Type:** Governance / Operational Control

**Problem**
- Validation severity is documented but not enforced.
- No reliable mechanism to block deployments on critical failures.

**Scope**
- Add `severity` field to each validation result.
- Add `by_severity` aggregation to validation summary.
- Update API contract in `analytics_endpoints.md` before implementation.
- Implement in validation layer.

**Acceptance Criteria**
- API responses include severity per validation result.
- Aggregated counts by severity are returned.
- Four-tier severity model matches `validation_system.md`.

**Owners**
- Engineering
- QA

---

### BLG-TECH-03 — Consolidate ValidationService into service layer
**Priority:** P1 (High)
**Type:** Architecture / Maintainability

**Problem**
- Validation logic is split between router and service stub.
- Increases risk of duplication and inconsistent behaviour.

**Scope**
- Move all active validation logic into `services/validation_service.py`.
- Delete placeholder stub.
- Keep router thin (request/response only).

**Acceptance Criteria**
- No validation logic remains in router layer.
- Tests pass without behavioural change.
- Code touched once alongside BLG-TECH-02.

**Dependencies**
- Must be delivered alongside BLG-TECH-02.

**Owners**
- Engineering
- QA

---

### BLG-TECH-04 — CI/CD validation workflow (GitHub Actions)
**Priority:** P2 (Medium)
**Type:** Delivery Quality / Automation

**Problem**
- Validation is manual and not enforced at merge time.

**Scope**
- Add `.github/workflows/validate-analytics.yml`.
- Run `POST /validate/calculations` on:
  - Pull requests
  - Pushes to `main` and `develop`
- Block merge if any **critical-severity** validation fails.
- Post validation summary as PR comment.

**Acceptance Criteria**
- Workflow reliably runs on all PRs.
- Merge is blocked only for critical severity failures.
- Clear PR feedback is visible.

**Dependencies**
- BLG-TECH-02 (severity model must exist).

**Owners**
- Engineering
- QA

---

### BLG-TECH-05 — Prometheus metrics endpoint
**Priority:** P3 (Low — v2.0 candidate)
**Type:** Observability

**Scope**
- Add `GET /metrics` Prometheus endpoint exposing:
  - Validation run count
  - Failure count by metric and severity
  - Validation duration
- Optional Grafana dashboard.

**Acceptance Criteria**
- Metrics scrape successfully in Prometheus format.
- Counters and histograms are correct.

**Target**
- v2.0 or when system becomes multi-user.

---

## 2. Product Feature Backlog (User-Facing)

---

### BLG-FEAT-01 — Current Drawdown Widget
**Priority:** P1
**Effort:** ~30 minutes
**Value:** High visibility risk awareness

Display current drawdown from peak and days underwater.
Example: "Drawdown: -8.2%, 12 days underwater"

**Dependency**
- Metrics Definitions owner must confirm drawdown calculation.

---

### BLG-FEAT-02 — R-Multiple Column in Trade History
**Priority:** P2
**Effort:** ~1 hour

Add R-multiple column to trade history table.

**Indicative Formula**

`(Exit Price - Entry Price) / (Entry Price - Stop Price)`

**Notes**
- Formula must be confirmed by Metrics Definitions owner.
- Decide server-side vs frontend-only calculation.

---

### BLG-FEAT-03 — Slippage Tracking
**Priority:** P2
**Effort:** 1-2 hours

Track and display trade slippage and average slippage summary.

**Indicative Formula**

`(Fill Price - Market Price) / Market Price`

Requires data model update.

---

### BLG-FEAT-04 — Best / Worst Trades Widget
**Priority:** P2
**Effort:** ~1 hour

Show top 3 and bottom 3 trades by R-multiple or P&L.

---

### BLG-FEAT-05 — Win Rate by Month Chart
**Priority:** P2
**Effort:** ~1 hour

Bar chart of win rate grouped by calendar month.

---

### BLG-FEAT-06 — Grace Period Indicator
**Priority:** P2
**Effort:** ~1 hour

Show remaining grace period days in open positions table.
Example: "Day 6 of 10"

---

### BLG-FEAT-07 — CSV Export of Trade History
**Priority:** P2
**Effort:** ~1 hour

One-click CSV export for tax and analysis use.

---

### BLG-FEAT-08 — Basic Compliance Metrics
**Priority:** P2
**Effort:** ~1 day

Lightweight discipline metrics:
- Journal completion rate
- Stop-based exit rate
- Average position size (% of portfolio)

Definitions must be canonicalised first.

---

### BLG-FEAT-09 — Settings page React re-render on keystroke (OBS-005)
**Priority:** P3 (Low)
**Type:** Frontend Performance
**Raised:** 2026-02-20 (observed during 3.2 verification)

**Problem**
The Settings page re-renders the entire form on every keystroke because all fields share a single `formData` state object. Each `setFormData` call triggers a full re-render of all `SectionCard` components, causing a visible flicker.

**Scope**
- Wrap `SectionCard` components in `React.memo`
- Pass individual field values as props rather than the full `formData` object
- Each section only re-renders when its own field values change

**Acceptance Criteria**
- Typing in one settings field does not cause visible re-render of other sections
- Save behaviour is unchanged
- No regression on settings load or save

**Owner**
- Head of Engineering (routine frontend housekeeping)

**Note**
This is a UX polish item. It does not affect correctness. No spec changes required.

---

## 3. Process Improvement Backlog

Items in this section are improvements to the delivery process itself, not to the product. They are raised for Product Owner prioritisation — some may require PMO Lead time, some may be self-contained template updates.

---

### BLG-PROC-01 — PMO Lead proactive next steps communication
**Priority:** P1
**Type:** Process / PMO
**Raised:** 2026-02-20 (identified during 3.2 delivery)

**Problem**
During 3.2, stakeholders had to ask what was happening next at multiple points — after verification passes, after defect resolution, and during shipping closure. The PMO Lead was reactive rather than proactive. This created friction and slowed the pace of the delivery cycle.

**Resolution actioned**
`pre_alignment_run.md` updated to v1.1 with an explicit next steps communication requirement at every phase gate. The Phase Gate Document template has been created (`processes/templates/phase_gate_template.md`) as the primary tool for this.

**What remains for Product Owner**
- Confirm the Phase Gate Document format is fit for purpose
- Confirm whether a Phase Gate Document should be retroactively created for any current in-flight features
- Prioritise adoption for the next feature entering pre-alignment (3.4 Portfolio Heat Gauge)

---

### BLG-PROC-02 — Settings field dependency check in readiness audit
**Priority:** P1
**Type:** Process / PMO
**Raised:** 2026-02-20 (identified during 3.2 lessons learnt)

**Problem**
During 3.2 pre-alignment, the `default_risk_percent` settings field was not identified in the readiness audit. It surfaced in the meeting when widget pre-population was discussed, causing the effort estimate to revise mid-meeting and adding four additional spec document updates to Phase 2.

**Resolution actioned**
`pre_alignment_readiness.md` updated to v1.1 with an explicit settings field dependency check in Section 1.

**What remains for Product Owner**
- No further action required — process improvement is complete
- Confirm awareness so this is not encountered again

---

### BLG-PROC-03 — Cross-navigation state persistence check in QA gate
**Priority:** P1
**Type:** Process / QA
**Raised:** 2026-02-20 (identified during 3.2 lessons learnt)

**Problem**
DEF-006 (Risk % resetting to default after navigation) was not caught before verification. The spec said "retains last-used session value" but no gate explicitly checked that the implementation mechanism was specified and the acceptance criterion covered navigation-away and return.

**Resolution actioned**
`pre_alignment_run.md` Phase 3 updated with an explicit cross-navigation persistence check. Any component with user-editable state must have an acceptance criterion covering navigation behaviour before the QA gate passes.

**What remains for Product Owner**
- No further action required — process improvement is complete
- Confirm awareness so this is not encountered again

---

### BLG-PROC-04 — Test scenario authorship clarity
**Priority:** P1
**Type:** Process / QA
**Raised:** 2026-02-20 (identified during 3.2 delivery)

**Problem**
During 3.2 verification, there was ambiguity about who writes the test scenarios, when they are written, and what format they follow. The QA Lead and wider team were unclear on the process, causing friction at the start of Phase 5.

**Resolution actioned**
`processes/testing_guide.md` created — a new canonical template covering who writes what, when, in what format, and how the QA Lead executes against it.

**What remains for Product Owner**
- Review `testing_guide.md` and confirm it reflects intent
- Confirm whether the QA & Testing Owner should be formally notified to adopt this process from the next feature
- Consider whether existing test scenario documents need to be brought into this format

---

## 4. Deferred / v2.0 Candidates

- Daily email portfolio summary
- FX rate history tracking
- Prometheus validation observability (BLG-TECH-05)
- Position correlation analysis
- Backtesting module
- Multi-portfolio support
- Mobile app
- Full compliance scoring system

---

## 5. Explicitly Out of Scope (Product-Level)

These are deliberate product decisions, not deferrals:

- Broker API integration
- Automated trading execution
- Configurable strategy builder
- ML-based predictions
- Social / community features
- Options and futures trading support

---

## 6. Lifecycle Governance Notes

- This backlog is not canonical and must never override:
  - Strategy rules
  - Metrics definitions
  - API contracts
- Any shipped feature must be backed by:
  - Canonical specification
  - Updated validation where applicable
- Once implemented, backlog items are superseded by canonical documentation.
