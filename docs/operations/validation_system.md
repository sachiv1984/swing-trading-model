# Analytics Validation System - Operations Guide

**Version:** 1.0.1
**Owner:** Platform Team
**Last Updated:** 2026-02-21
**Review Cycle:** Quarterly

> ⚠️ **Governance note:** The owner field "Platform Team" is a team name, not a named individual role as required by `docs/governance/document_lifecycle_guide.md`. This is a pre-existing compliance gap flagged by the Head of Specs Team on 2026-02-21. The Infrastructure & Operations Documentation Owner should resolve this at next review.

---

## Purpose

This document defines:
1. How analytics validation works
2. When validation runs
3. Who owns validation maintenance
4. What to do when validation fails

---

## System Architecture
```
┌─────────────────────────────────────────────────┐
│ Validation System Components                    │
├─────────────────────────────────────────────────┤
│                                                  │
│  1. Validation Endpoint                         │
│     POST /validate/calculations                 │
│     - Compares actual vs expected metrics       │
│     - Returns pass/warn/fail per metric         │
│                                                  │
│  2. Expected Values                             │
│     test_data/validation_data.py                │
│     - Ground truth for 5-trade test portfolio   │
│     - Updated manually when portfolio changes   │
│                                                  │
│  3. Tolerance Configuration                     │
│     test_data/validation_data.py:TOLERANCE      │
│     - Acceptable variance per metric            │
│                                                  │
│  4. CI/CD Integration (PLANNED)                 │
│     .github/workflows/validate.yml              │
│     - Runs on every commit                      │
│                                                  │
│  5. Production Monitoring (PLANNED)             │
│     /metrics endpoint for Prometheus            │
│     - Tracks validation status over time        │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## Validation Workflow

### Current State (Manual)

**When to Run**:
1. After changing analytics calculation code
2. Before deploying to production
3. After updating test portfolio data
4. Monthly on first Monday

**How to Run**:
```bash
# Via System Status page
1. Go to https://your-app.com/system-status
2. Click "Run Validation" button
3. Review results

# Via API
curl -X POST https://api.example.com/validate/calculations

# Via Python (local dev)
python -c "
import requests
r = requests.post('http://localhost:8000/validate/calculations')
print(r.json())
"
```

**What Gets Validated**:
```python
# From validation_data.py — 13 metrics (updated 2026-02-21, BLG-TECH-01)
EXPECTED_METRICS = {
    "sharpe_ratio": 0.00,
    "max_drawdown_percent": -7.70,
    "recovery_factor": 0.36,
    "expectancy": 0.39,
    "profit_factor": 1.01,
    "risk_reward_ratio": 1.51,
    "win_streak": 2,
    "loss_streak": 3,
    "avg_hold_winners": 15.5,
    "avg_hold_losers": 10.7,
    "trade_frequency": 1.8,
    "capital_efficiency": 0.22,   # Added BLG-TECH-01: uses Mean(total_cost) GBP
    "days_underwater": 0,
}
```

---

## Severity Levels

### Critical (Block Deployment)

**Metrics**:
- `sharpe_ratio` - Core risk-adjusted return metric
- `max_drawdown_percent` - Risk management fundamental
- `profit_factor` - Strategy viability

**Action on Failure**:
- ❌ Block production deployment
- 🔔 Page on-call engineer
- 📊 Investigate immediately

**Tolerance**: Exact (within defined tolerance)

---

### High (Require Sign-Off)

**Metrics**:
- `recovery_factor` - Portfolio resilience
- `expectancy` - Edge validation
- `risk_reward_ratio` - Risk management

**Action on Failure**:
- ⚠️ Require manual sign-off to deploy
- 📧 Alert analytics team
- 📝 Document reason for variance

**Tolerance**: Moderate (can vary 10-20%)

---

### Medium (Log and Monitor)

**Metrics**:
- `win_streak` / `loss_streak` - Pattern analysis
- `avg_hold_winners` / `avg_hold_losers` - Behavior metrics
- `trade_frequency` - Activity metric
- `capital_efficiency` - Cost basis metric

**Action on Failure**:
- 📝 Log warning
- 📊 Track trend
- 🔍 Investigate if persistent (3+ weeks)

**Tolerance**: Flexible (can vary 20-30%)

---

### Low (Informational Only)

**Metrics**:
- `days_underwater` - Informational metric
- Non-critical metadata

**Action on Failure**:
- 📝 Log only
- No blocking
- Review monthly

**Tolerance**: Wide

---

## Validation Response Format
```json
{
  "status": "ok",
  "data": {
    "validations": [
      {
        "metric": "sharpe_ratio",
        "expected": 0.00,
        "actual": 0.00,
        "diff": 0.00,
        "status": "pass",
        "severity": "critical",
        "tolerance": 0.01,
        "formula": "(Avg Return / Std Dev) × √252",
        "method": "insufficient_data"
      },
      {
        "metric": "max_drawdown_percent",
        "expected": -7.70,
        "actual": -7.71,
        "diff": 0.01,
        "status": "pass",
        "severity": "critical",
        "tolerance": 0.1,
        "formula": "((Peak - Trough) / Peak) × 100"
      }
    ],
    "summary": {
      "total": 13,
      "passed": 13,
      "warned": 0,
      "failed": 0,
      "by_severity": {
        "critical": {"total": 3, "passed": 3, "warned": 0, "failed": 0},
        "high": {"total": 3, "passed": 3, "warned": 0, "failed": 0},
        "medium": {"total": 6, "passed": 6, "warned": 0, "failed": 0},
        "low": {"total": 1, "passed": 1, "warned": 0, "failed": 0}
      }
    },
    "timestamp": "2026-02-21T00:24:41Z"
  }
}
```

> **Note:** The `severity` field per result and `by_severity` summary object are specified in `analytics_endpoints.md` v1.8.1. These are contract additions for BLG-TECH-02 — they will appear in API responses once BLG-TECH-02 is implemented.

---

## Maintenance Procedures

### Updating Expected Values

**When to Update**:
1. Test portfolio changes (new trade, position closed)
2. Calculation formula changes
3. Data model changes affecting metrics
4. Tolerance adjustments

**How to Update**:

**Step 1**: Calculate new expected values manually
```python
# In test_data/validation_data.py

# Update trade data
VALIDATION_TRADES = [
    {
        "id": "...",
        "ticker": "NVDA",
        # ... updated trade data
    }
]

# Recalculate expected metrics
# Use calculator or Excel to verify
EXPECTED_METRICS = {
    "sharpe_ratio": NEW_VALUE,
    # ... update others
}
```

**Step 2**: Document why values changed
```python
# Add comment in validation_data.py
"""
Updated 2026-02-21 (BLG-TECH-01):
capital_efficiency: 0.17 → 0.22
  Reason: Cost basis corrected to Mean(total_cost) GBP from trade_history.
  Previous method used entry_price × shares (mixed USD/GBP).
"""
```

**Step 3**: Commit and document
```bash
git add test_data/validation_data.py
git commit -m "Update validation: BLG-TECH-01 capital_efficiency 0.17→0.22, total_cost fields added"
```

**Step 4**: Run validation to confirm
```bash
curl -X POST http://localhost:8000/validate/calculations
# Should all pass after update
```

---

### Adding New Metrics

**When**: New metric added to analytics endpoint

**Procedure**:

**Step 1**: Add to validation_data.py
```python
EXPECTED_METRICS = {
    # Existing metrics...
    "new_metric_name": CALCULATED_VALUE,
}

TOLERANCE = {
    # Existing tolerances...
    "new_metric_name": ACCEPTABLE_VARIANCE,
}
```

**Step 2**: Update validation.py endpoint
```python
# In backend/routers/validation.py

validations.append({
    "metric": "new_metric_name",
    "expected": EXPECTED_METRICS["new_metric_name"],
    "actual": result.get("new_metric_name", 0.0),
    "diff": abs(...),
    "status": "pass" if ... else "fail",
    "tolerance": TOLERANCE["new_metric_name"],
    "formula": "NEW_METRIC_FORMULA_HERE",
    "severity": "medium"  # Set appropriate severity per validation_system.md
})
```

**Step 3**: Add to metrics_definitions.md
```markdown
## New Metric Name

### Definition
...

### Formula
...
```

**Step 4**: Test thoroughly
```bash
# Run validation
curl -X POST http://localhost:8000/validate/calculations

# Verify new metric appears in response
```

---

## Incident Response

### Validation Failure in Production

**Scenario**: Daily validation cron job fails

**Step 1**: Assess Severity
```
IF severity == "critical":
    → Page on-call engineer immediately
    → Block new deployments
    → Start incident response

ELSE IF severity == "high":
    → Alert analytics team
    → Require manual review before next deploy
    → Investigate within 4 hours

ELSE IF severity == "medium":
    → Log warning
    → Investigate within 24 hours
    → Add to backlog if recurring

ELSE:
    → Log only
    → Review at next weekly sync
```

**Step 2**: Investigate Root Cause

**Common Causes**:
1. **Data Issue**
   - New trade entered incorrectly
   - Price data stale/incorrect
   - Database corruption

2. **Calculation Change**
   - Calculation formula changed
   - Expected value outdated
   - Data changed (new trade, withdrawal)

**Steps to Resolve**:
```bash
# 1. Manually calculate expected value
# Use Excel/calculator with VALIDATION_TRADES data

# 2. Compare to actual
curl http://localhost:8000/validate/calculations | \
  jq '.data.validations[] | select(.metric=="METRIC_NAME")'

# 3. If expected value is wrong, update it
# Edit test_data/validation_data.py

# 4. If calculation is wrong, fix analytics_service.py
```

---

### Problem: Tolerance too tight/loose

**Symptoms**:
- Metric fails validation despite "correct" calculation
- Small floating point differences causing failures
- Or: metric passes despite being obviously wrong

**Solution**:

Adjust tolerance in `validation_data.py`:
```python
TOLERANCE = {
    "sharpe_ratio": 0.01,           # ±0.01 variance acceptable
    "max_drawdown_percent": 0.1,    # ±0.1% acceptable
    "capital_efficiency": 0.05,     # ±0.05 acceptable
    # ... etc
}
```

**Guidelines**:
- **Integer metrics** (win_streak, days_underwater): tolerance = 0 (exact match)
- **Percentages** (win_rate, max_drawdown): tolerance = 0.1-0.5% (small variance OK)
- **Ratios** (sharpe, profit_factor): tolerance = 0.01-0.05 (moderate variance OK)
- **Currency** (expectancy): tolerance = 0.10 (pennies OK)
- **Efficiency ratios** (capital_efficiency): tolerance = 0.05

---

## Appendix: Validation Test Cases

### Test Case 1: All Metrics Pass

**Setup**: Fresh test portfolio, all calculations correct

**Expected Result**:
```json
{
  "summary": {
    "total": 13,
    "passed": 13,
    "failed": 0,
    "by_severity": {
      "critical": {"total": 3, "passed": 3, "warned": 0, "failed": 0},
      "high": {"total": 3, "passed": 3, "warned": 0, "failed": 0},
      "medium": {"total": 6, "passed": 6, "warned": 0, "failed": 0},
      "low": {"total": 1, "passed": 1, "warned": 0, "failed": 0}
    }
  }
}
```

**If Fails**: Something is fundamentally broken, investigate immediately

---

### Test Case 2: Expected Max Drawdown Outdated

**Setup**: New trade creates deeper drawdown than expected

**Expected Result**:
```json
{
  "validations": [{
    "metric": "max_drawdown_percent",
    "expected": -7.70,
    "actual": -12.50,
    "diff": 4.80,
    "status": "fail",
    "severity": "critical"
  }]
}
```

**Resolution**: Update EXPECTED_METRICS["max_drawdown_percent"] to -12.50

---

### Test Case 3: Insufficient Data for Sharpe

**Setup**: Test portfolio has < 10 trades and < 30 snapshots

**Expected Result**:
```json
{
  "validations": [{
    "metric": "sharpe_ratio",
    "expected": 0.00,
    "actual": 0.00,
    "diff": 0.00,
    "status": "pass",
    "severity": "critical",
    "method": "insufficient_data"
  }]
}
```

**Note**: This is expected behavior, not a failure

---

## Glossary

**Critical Metric**: Metric that directly affects trading decisions; failures block deployment
**Expected Value**: Ground truth metric calculated manually from test portfolio
**Tolerance**: Acceptable variance between expected and actual values
**Severity**: Importance level determining response to validation failure (critical/high/medium/low)
**Test Portfolio**: Static set of 5 trades used for validation testing
**Validation Run**: Single execution of validation endpoint
**Pass**: Actual value within tolerance of expected value
**Fail**: Actual value outside tolerance
**Warn**: Near tolerance limit (within 10% of boundary)

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0.1 | 2026-02-21 | BLG-TECH-01 closure: added `capital_efficiency` to EXPECTED_METRICS list; corrected metric count 12→13 throughout; updated by_severity totals in examples; added governance note on owner field; added `capital_efficiency` to Medium severity tier |
| 1.0.0 | 2026-02-16 | Initial version |