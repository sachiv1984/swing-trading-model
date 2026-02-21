# Product Backlog — Momentum Trading Assistant

Owner: Product Owner
Status: Active
Class: Planning Document (Class 4)
Last Updated: 2026-02-21

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

### ✅ BLG-TECH-01 — Fix Sharpe variance method + Capital Efficiency currency basis
**Status: COMPLETE — 2026-02-21**
**Priority:** P0 (Critical)
**Type:** Metrics Correctness / Validation Integrity

**Problem**
- Sharpe ratio used population variance instead of sample variance.
- Capital efficiency used `entry_price * shares` instead of actual GBP cost.
- Validation could not reliably detect non-conformant behaviour (`capital_efficiency` block was absent from `routers/validation.py`).

**Scope delivered**
- `_calculate_sharpe()` updated to sample variance (÷ n−1) for both portfolio and trade methods (AP-06).
- `_calculate_advanced_metrics()` updated to use `Mean(trade.total_cost)` GBP cost basis (AP-07).
- `total_cost` field added to all 5 entries in `test_data/validation_data.py`.
- `capital_efficiency` expected value updated `0.17 → 0.22` to reflect corrected basis.
- `capital_efficiency` validation block added to `routers/validation.py` (was previously absent).
- `metrics_definitions.md` updated to v1.5.7: Appendix E Backlog Items 1 and 2 marked resolved; inline conformance notes updated; changelog entry added.

**Closure evidence**
- `POST /validate/calculations` 13/13 pass, zero warnings, zero failures.
- Timestamp: 2026-02-21T00:24:41Z.
- Metrics Definitions & Analytics Canonical Owner sign-off granted: 2026-02-21.

**Release gate cleared:** v1.6 quality gate for this item is satisfied.

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

## 3. Deferred / v2.0 Candidates

- Daily email portfolio summary
- FX rate history tracking
- Prometheus validation observability (BLG-TECH-05)
- Position correlation analysis
- Backtesting module
- Multi-portfolio support
- Mobile app
- Full compliance scoring system

---

## 4. Explicitly Out of Scope (Product-Level)

These are deliberate product decisions, not deferrals:

- Broker API integration
- Automated trading execution
- Configurable strategy builder
- ML-based predictions
- Social / community features
- Options and futures trading support

---

## 5. Lifecycle Governance Notes

- This backlog is not canonical and must never override:
  - Strategy rules
  - Metrics definitions
  - API contracts
- Any shipped feature must be backed by:
  - Canonical specification
  - Updated validation where applicable
- Once implemented, backlog items are superseded by canonical documentation.

---