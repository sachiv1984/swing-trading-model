**Owner:** QA & Testing Owner
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-04-30
**Cycle:** 2026-04-29__release-v3.1 (ST-09)

---

# Screener Accuracy Test Protocol

## Purpose

This protocol defines the process for validating the accuracy of the Momentum Screener engine. Accuracy testing ensures that the screener's output (signal scores, regime gates, ATR calculations, and sector filters) reflects correct computation rather than data or logic drift.

---

## Frequency

| Phase | Frequency |
|-------|-----------|
| First month post-live | Weekly (every 7 days) |
| Thereafter | Monthly |

Post-live is defined as the date the screener feature was first deployed to production (v3.0, 2026-04-25).

---

## Sample Size

- **Minimum 10 results per run.** If the screener returns fewer than 10 results with default filters, widen the ATR and signal score filters to ensure at least 10 results for comparison.
- Include a mix of UK and US tickers where possible.

---

## Comparison Methodology

For each run, manually compute the following for **3 known tickers** selected from the results:

1. **ATR calculation:** Using the ticker's last 14 trading days' high/low/close, compute ATR manually. Compare against the screener's reported `atr` value.
2. **Signal score:** Review the screener's scoring components (trend alignment, volume, regime). Confirm the reported `signal_score` matches the expected composite score for those inputs.
3. **Regime gate:** Confirm whether the ticker passes or fails the regime gate matches the market regime status reported by `GET /health/detailed`.

---

## Pass/Fail Thresholds

| Metric | Pass Threshold | Fail Condition |
|--------|---------------|----------------|
| ATR accuracy | ≤5% discrepancy from manually computed ATR | >5% discrepancy on any tested ticker |
| Signal score | ≤5% discrepancy from manually computed score | >5% discrepancy on any tested ticker |
| Regime gate | 0% discrepancy — exact match required | Any mismatch between screener and health endpoint |
| UK ticker display | UK tickers display without `.L` suffix | Any `.L` displayed in results table |

---

## Scenario Library Reference

This protocol is used alongside the Screener Scenario Library (`docs/qa/screener_scenarios.md`, BLG-QA-10 / ST-10). Scenario library provides pre-defined test cases for structured regression testing; this protocol covers live-data accuracy comparison runs.

---

## Run Record

For each accuracy run, record the following in a short log entry (can be appended to this file or filed separately):

```
Date: YYYY-MM-DD
Run type: weekly / monthly
Tickers tested: [list of 3 tickers]
ATR comparison: Pass / Fail (discrepancy %: X%)
Signal score comparison: Pass / Fail (discrepancy %: X%)
Regime gate comparison: Pass / Fail
UK display check: Pass / N/A (if no UK results)
Overall: Pass / Fail
Notes: [any anomalies or follow-up actions]
```

---

## Failure Response

If any metric fails the pass threshold:

1. File an incident note in `docs/ops/` describing the discrepancy and affected tickers.
2. Escalate to Backend Engineering Patterns Owner within 24 hours.
3. Do not ship any screener changes until the root cause is identified and resolved.

---

## Acceptance

- Accepted by: Director of Quality
- Date: 2026-04-30
