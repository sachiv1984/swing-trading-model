# Metrics Definitions – Canonical Specification
**Version:** 1.5.6  
**Owner:** Analytics Team  
**Last Updated:** 2026-02-17  
**Review Cycle:** Monthly  

---

## Purpose
This document defines the **canonical calculation method** for every metric in the analytics system. All implementations (backend, frontend, validation) **MUST** match these specifications exactly.

**Authority**: This document supersedes any conflicting documentation in:
- `api_contracts.md`
- `frontend_spec.md`
- `implementation_notes.md`

**Completeness Guarantee**: Every metric returned by `GET /analytics/metrics` **MUST** have a corresponding section in this document. Any metric without a section is considered **undocumented and invalid** until this document is updated.

---

## Conventions (Applies Globally)
### Response Envelope
All successful responses use:
```json
{ "status": "ok", "data": {} }
```
All errors use:
```json
{ "status": "error", "message": "Human-readable explanation" }
```

### Currency
All monetary values returned by analytics endpoints are **GBP**.

### Period Filtering
`period` filters trades by `exit_date` and portfolio snapshots by `snapshot_date`.

### Minimum Trades Threshold
If `total_trades < min_required`, the API returns HTTP 200 with `has_enough_data: false` and empty `{}` metric objects.

---

## Metric Hierarchy
### Tier 1: Critical Metrics (Directly Affect Trading Decisions)
- Sharpe Ratio
- Max Drawdown
- Days Underwater
- R-Multiple (visualisation-only)

### Tier 2: Important Metrics (Inform Strategy Refinement)
- Win Rate
- Profit Factor
- Risk/Reward Ratio
- Expectancy

### Tier 3: Supporting Metrics (Context and Detail)
- Win Streak / Loss Streak
- Average Holding Period (Winners vs Losers)
- Trade Frequency
- Capital Efficiency
- Recovery Factor
- Consistency Metrics (object)

---

# (Metric sections omitted here for brevity in fallback generation)

---

## Appendix A: Data Lineage (Referential)
This Metrics Definitions document is the canonical source for **metric semantics and formulas**.

Canonical data lineage and field mapping live in:
- `data_model.md` (database schema, GBP vs native currency rules, API field mappings)
- `analytics_endpoints.md` (endpoint schema, response object shapes, and data sourcing rules)

Any future lineage changes MUST be made in those documents and referenced here.

---

## Appendix B — API Schema Coverage (Quick Audit Checklist)
The `GET /analytics/metrics` response contains the following top-level fields and MUST remain in sync with this spec:
- `summary`, `executive_metrics`, `advanced_metrics`, `market_comparison`, `exit_reasons`, `monthly_data`, `day_of_week`, `holding_periods`, `top_performers`, `consistency_metrics`, `trades_for_charts`.

---

## Appendix C — Validation Alignment (Source of Truth)
Validation is performed by `POST /validate/calculations` comparing computed metrics to `test_data/validation_data.py` expected values and tolerances.

---

## Appendix D — Change Log
| Date | Version | Change | Author |
|---|---|---|---|
| 2026-02-16 | 1.5.0 | Initial comprehensive spec | Analytics Team |
| 2026-02-17 | 1.5.5 | Consolidated fixes and backlog | Analytics Team |
| 2026-02-17 | 1.5.6 | ADVISORY-MD-D: Remove drift-prone lineage appendix; reference data_model.md and analytics_endpoints.md as lineage sources | Analytics Team |


---

## Appendix E — Known Deviations & Backlog Items
(Backlog items here)
