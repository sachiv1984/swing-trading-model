# Glossary

**Owner:** Head of Specs Team  
**Scope:** Shared terminology across the specification system  
**Authority:** Language only — canonical definitions live in domain specs  
**Status:** Canonical (terminology)

This glossary defines shared terms used across specs. It does not introduce behavior or override domain specifications.  
In case of conflict, the relevant **domain canonical spec prevails** (Strategy / Data Model / Metrics / API Contracts / Frontend).

---

## A

**Action (HOLD / EXIT)**: Result of position analysis. `HOLD` means no user action required; `EXIT` means exit is recommended and requires user confirmation.

**Analytics Service**: Backend service responsible for calculating all metrics from trade and portfolio data.

**API Contract**: Canonical specification of an endpoint’s purpose, request/response shapes, defaults, validation, errors, and idempotency rules.

**API Envelope (Standard Response Wrapper)**: Standard JSON wrapper for successful and error responses:
- Success: `{ "status": "ok", "data": ... }`
- Error: `{ "status": "error", "message": "..." }`
Health endpoints may explicitly be exceptions.

**ATR (Average True Range)**: Volatility measure used for stop-loss calculations. Typically calculated over a 14-day rolling period.

**ATR Multiplier**: Strategy parameter applied to ATR to set stop distance (e.g., `5 × ATR` for wide stops; `2 × ATR` for tighter trailing stops).

---

## B

**Backtest**: Simulation of strategy rules over historical data to estimate performance. Backtests are not proof of future results.

**Base Currency**: The portfolio’s reporting currency. In this system, portfolio-level values and P&L are tracked in **GBP**.

**Behavioral Contract**: A spec that defines expected system behavior in deterministic terms and is treated as authoritative.

---

## C

**Canonical (Document)**: The authoritative source of truth for a domain. Canonical docs must comply with the documentation lifecycle guide.

**Cash Balance**: Available portfolio cash in base currency (GBP).

**Cash Flow**: Deposits and withdrawals. Used to distinguish portfolio performance from changes due to adding/removing capital.

**Closed Trade**: A position that has been exited and recorded into trade history.

**Contract-Affecting Change**: A change that alters endpoints, request/response shapes, status codes, defaults, validation rules, or user-visible API behavior. Requires OpenAPI alignment review (when applicable).

---

## D

**Data Model**: Canonical definition of stored entities, fields, currency semantics, and lifecycle/state representation.

**Days Underwater**: Number of calendar days since portfolio last reached its peak equity, as defined by the canonical metric method.  
See **Metrics Definitions** for the exact calculation.

**Deprecated (Document Status)**: A document that is still historically accurate but no longer active truth. Must declare what supersedes it and from when.

**Deterministic**: Identical inputs produce identical outputs. Determinism is a core system requirement for rule execution and analytics.

**Drawdown**: Decline from peak to trough in portfolio value. Often expressed as a negative percentage (e.g., `-25%`).

---

## E

**Effective From**: Deprecation metadata indicating the date/version a document was superseded.

**Entry Date**: The date a position was opened.

**Entry Price**: Execution price used to open a position (native currency).

**Exit Date**: The date a position (or portion of a position) was closed.

**Exit Price**: User-provided broker execution price used to close a position (native currency).

**Exit Reason**: User-selected reason for exit (e.g., Manual Exit, Stop Loss Hit, Risk-Off Signal). Used for analytics breakdowns.

---

## F

**Fees Paid**: Total fees associated with a transaction (e.g., stamp duty, FX fee, commission). Fees affect cost basis and P&L.

**Frontend-only Calculation (Exception)**: A calculation performed client-side only for visualization or UX, explicitly documented as an exception (e.g., R-Multiple visualization when necessary).

**FX Fee**: Percentage fee applied when converting currency for USD transactions.

**FX Rate (Entry / Exit)**: Exchange rate used at entry or exit to convert native currency amounts into GBP. FX impacts P&L but must not move native-currency stop levels.

---

## G

**Grace Period**: A fixed number of days after entry during which stop-loss enforcement is disabled, even though stops are calculated and stored.

**Gross Proceeds**: Proceeds from a sale before fees.

---

## H

**Health Endpoint**: API endpoints used for service health/diagnostics. May be exceptions to standard API envelope rules.

**Holding Days**: Number of calendar days a position has been held (entry date to current date or exit date, inclusive as defined by system rules).

---

## I

**Idempotent**: Repeating a request has the same effect as calling it once (e.g., an upsert). `GET` is generally idempotent. Some `DELETE` operations may explicitly be non-idempotent.

**Implementation (Non-Canonical)**: Code or artifacts that implement behavior. Implementation must conform to canonical specs.

---

## L

**Lifecycle (Document)**: The state of a document: Draft, Canonical, Deprecated, Archived. Governed by the documentation lifecycle guide.

**Live FX Rate**: The current FX rate fetched at query time for display or conversion.

---

## M

**Market (US/UK)**: Market classification used for pricing, fees, and regime indicators.

**Market Regime**: Risk-on/risk-off classification based on index vs its moving average (e.g., SPY vs 200-day MA for US).

**MA200 (200-day Moving Average)**: Long-term moving average used as the regime threshold.

**Manual Exit**: User-initiated exit outside automated stop or regime recommendations.

**Metrics Definitions**: Canonical source of truth for metric formulas, thresholds, and failure behaviors.

---

## N

**Native Currency**: The currency in which an asset trades (USD for US stocks, GBP for UK stocks). Stops are stored and enforced in native currency.

**Net Cash Flow**: `Total Deposits − Total Withdrawals`. Used as the portfolio cost basis for performance calculations.

**Net Proceeds**: Proceeds after fees.

---

## O

**Open Position**: A position currently held (not yet exited).

**Owner (Document Owner)**: The role accountable for the accuracy, maintenance, and governance of a document or domain.

---

## P

**P&L (Profit and Loss)**: Profit/loss expressed in base currency (GBP) unless explicitly stated.  
- **Unrealized P&L**: P&L on open positions  
- **Realized P&L**: P&L on closed trades

**P&L %**: Percentage gain/loss relative to entry cost basis.

**Parameter (Strategy Parameter)**: A tunable value (e.g., grace period length, ATR multipliers) that expresses strategy intent. Parameters may change via versioned strategy updates.

**Portfolio History (Snapshot)**: Daily time-series record of portfolio totals used for charting and portfolio-based metrics.

**Position**: A holding created by entering a trade. Can be open or closed depending on lifecycle state.

**Position State / Display Status**: User-visible classification derived from holding days and profitability (e.g., GRACE / LOSING / PROFITABLE).

**Profit Factor**: Metric defined as gross profits divided by gross losses. Canonical definition lives in Metrics Definitions.

---

## R

**R-Multiple**: Ratio of actual profit/loss to initial risk.  
Formula: `(Exit Price - Entry Price) / (Entry Price - Stop Price)`.  
May be calculated frontend-only for visualization when explicitly documented. See ADRs where applicable.

**Rebalance Frequency**: How often positions are reviewed/selected in a systematic portfolio strategy (primarily relevant to backtest logic if used).

**Reference Artifact**: A supporting representation of canonical specs (e.g., OpenAPI YAML). Must not contradict canonical documents and must be reviewed inline when contract-affecting changes occur.

**Risk-Off Signal**: Regime condition indicating defensive posture (e.g., index below MA200). Often triggers exit recommendation.

**Risk-On Signal**: Regime condition indicating favorable market environment (e.g., index above MA200).

---

## S

**Sharpe Ratio**: Risk-adjusted return metric. Portfolio-based method preferred; trade-based fallback.  
See **Metrics Definitions** for exact calculation and variance conventions.

**Stop Price**: Price level at which position should be exited to limit loss. Stored and enforced in **native currency**.

**Stop Tightening Rule**: Stop prices must not move downwards. Stops may only stay the same or rise (tighten).

**Supporting Spec**: Non-canonical document that aids understanding or provides reference, without overriding canonical definitions.

**Superseded By**: Deprecation metadata indicating the document that replaces a deprecated document.

---

## T

**Tag**: User-defined label used to categorize positions/trades (e.g., `momentum`, `breakout`). Tag format and limits are governed by API and frontend rules.

**Trade**: A completed lifecycle from entry to exit (or partial exit portion). Trades are immutable records in trade history.

**Trade History**: Immutable record of closed trades used for analytics and review.

---

## U

**Unrealized P&L**: P&L on currently open positions.

---

## V

**Validation**: Automated testing of analytics calculations against known expected values and tolerances.  
See the Validation System documentation where applicable.

**Version (Document Version)**: A MAJOR.MINOR identifier used when changes alter interpretation or meaning (per lifecycle guide).

**Volatility**: Degree of price variation. In this system, ATR is the primary volatility measure used for stops.

---

## W

**Win Rate**: Percentage of closed trades with positive P&L. Canonical definition lives in Metrics Definitions.
