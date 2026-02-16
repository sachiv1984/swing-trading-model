# Glossary

## A

**Analytics Service**: Backend service responsible for calculating all metrics from trade and portfolio data.

**ATR (Average True Range)**: Volatility measure used for stop loss calculations. Calculated over 14-day period.

---

## D

**Days Underwater**: Number of calendar days since portfolio last reached its all-time peak equity. See [Metrics Definitions](../specs/metrics_definitions.md#days-underwater).

---

## R

**R-Multiple**: Ratio of actual profit/loss to initial risk. Formula: `(Exit Price - Entry Price) / (Entry Price - Stop Price)`. Currently calculated frontend-only. See [ADR-002](../decisions/ADR-002-frontend-only-r-multiple.md) for rationale.

---

## S

**Sharpe Ratio**: Risk-adjusted return metric. Portfolio-based method preferred; trade-based fallback. See [Metrics Definitions](../specs/metrics_definitions.md#sharpe-ratio).

**Stop Price**: Price level at which position should be exited to limit loss. Stored in native currency (USD for US stocks, GBP for UK stocks).

---

## V

**Validation**: Automated testing of analytics calculations against known expected values. See [Validation System](../operations/validation_system.md).
