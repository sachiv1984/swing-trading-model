# Analytics Validation System - Operations Guide

**Version:** 1.0.0  
**Owner:** Platform Team  
**Last Updated:** 2026-02-16  
**Review Cycle:** Quarterly

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
# From validation_data.py
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
      "total": 12,
      "passed": 11,
      "warned": 0,
      "failed": 1,
      "by_severity": {
        "critical": {"passed": 3, "failed": 0},
        "high": {"passed": 3, "failed": 0},
        "medium": {"passed": 4, "failed": 1},
        "low": {"passed": 1, "failed": 0}
      }
    },
    "timestamp": "2026-02-16T10:30:00Z"
  }
}
```

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
Updated 2026-02-16: Added TSLA trade exit on 2026-02-15
Previous max_drawdown: -7.70%
New max_drawdown: -8.50%
Reason: New drawdown occurred after TSLA stop out
"""
```

**Step 3**: Commit and document
```bash
git add test_data/validation_data.py
git commit -m "Update validation: TSLA exit changes max drawdown to -8.50%"
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
    "severity": "medium"  # Set appropriate severity
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

2. **Code Regression**
   - Recent deploy changed calculation
   - Bug introduced in analytics service
   - Frontend/backend mismatch

3. **Expected Values Outdated**
   - Test portfolio changed
   - Forgot to update expected metrics
   - Tolerance too tight

**Step 3**: Fix and Verify
```bash
# Fix identified issue
# Then re-run validation
curl -X POST http://localhost:8000/validate/calculations

# Should pass after fix
```

**Step 4**: Document in Post-Mortem
```markdown
## Validation Failure Post-Mortem

**Date**: 2026-02-16
**Metric**: max_drawdown_percent
**Expected**: -7.70%
**Actual**: -12.50%
**Root Cause**: TSLA position stopped out, creating new max drawdown
**Resolution**: Updated EXPECTED_METRICS to -12.50%
**Prevention**: Add alert when max_drawdown changes >2% in single day
```

---

## CI/CD Integration (Planned v1.5)

### GitHub Actions Workflow

**File**: `.github/workflows/validate-analytics.yml`
```yaml
name: Validate Analytics

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Start test server
        run: |
          python backend/main.py &
          sleep 5
      
      - name: Run validation tests
        id: validation
        run: |
          response=$(curl -X POST http://localhost:8000/validate/calculations)
          echo "::set-output name=result::$response"
          
          # Parse response
          failed=$(echo $response | jq '.data.summary.failed')
          
          # Check critical failures
          critical_failed=$(echo $response | jq '.data.summary.by_severity.critical.failed')
          
          if [ "$critical_failed" -gt 0 ]; then
            echo "❌ CRITICAL validation failures detected"
            exit 1
          fi
      
      - name: Post comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const result = ${{ steps.validation.outputs.result }}
            const comment = `
            ## Analytics Validation Results
            
            ✅ Passed: ${result.data.summary.passed}
            ❌ Failed: ${result.data.summary.failed}
            
            [View full results](${process.env.GITHUB_SERVER_URL}/${process.env.GITHUB_REPOSITORY}/actions/runs/${process.env.GITHUB_RUN_ID})
            `
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            })
```

---

## Production Monitoring (Planned v1.5)

### Prometheus Metrics Endpoint

**File**: `backend/routers/metrics.py`
```python
from prometheus_client import Counter, Histogram, generate_latest

# Metrics
validation_runs = Counter('validation_runs_total', 'Total validation runs')
validation_failures = Counter('validation_failures_total', 'Total validation failures', ['metric', 'severity'])
validation_duration = Histogram('validation_duration_seconds', 'Validation duration')

@router.get("/metrics")
async def prometheus_metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type="text/plain")
```

### Grafana Dashboard

**Panels**:
1. Validation Pass Rate (last 7 days)
2. Critical Failures Over Time
3. Validation Duration Trend
4. Failure Breakdown by Metric

**Alerts**:
```yaml
# alerts.yml
groups:
  - name: analytics_validation
    rules:
      - alert: CriticalValidationFailure
        expr: validation_failures_total{severity="critical"} > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Critical analytics validation failure"
          description: "{{ $labels.metric }} failed validation"
          
      - alert: HighFailureRate
        expr: rate(validation_failures_total[1h]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High validation failure rate"
```

---

## Troubleshooting Guide

### Problem: All metrics failing validation

**Symptoms**:
- All 12 metrics show "fail" status
- Large variances across the board

**Likely Causes**:
1. Test portfolio data corrupted
2. Database connection issue
3. Analytics service bug

**Steps to Resolve**:
```bash
# 1. Check database connection
curl http://localhost:8000/health/detailed

# 2. Verify test portfolio exists
curl http://localhost:8000/trades | jq '.data.total_trades'

# 3. Check analytics endpoint directly
curl http://localhost:8000/analytics/metrics?period=all_time

# 4. Compare to expected
python test_data/validation_data.py  # Should print expected values
```

---

### Problem: Single metric consistently failing

**Symptoms**:
- One metric always fails
- Others pass
- Variance is consistent (e.g., always off by same amount)

**Likely Causes**:
1. Calculation formula changed
2. Expected value outdated
3. Data changed (new trade, withdrawal)

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
    "sharpe_ratio": 0.01,  # ±1% variance acceptable
    "max_drawdown_percent": 0.1,  # ±0.1% acceptable
    # ... etc
}
```

**Guidelines**:
- **Integer metrics** (win_streak, days_underwater): tolerance = 0 (exact match)
- **Percentages** (win_rate, max_drawdown): tolerance = 0.1-0.5% (small variance OK)
- **Ratios** (sharpe, profit_factor): tolerance = 0.01-0.05 (moderate variance OK)
- **Currency** (expectancy): tolerance = 0.10 (pennies OK)

---

## Appendix: Validation Test Cases

### Test Case 1: All Metrics Pass

**Setup**: Fresh test portfolio, all calculations correct

**Expected Result**:
```json
{
  "summary": {
    "total": 12,
    "passed": 12,
    "failed": 0,
    "by_severity": {
      "critical": {"passed": 3, "failed": 0}
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
    "status": "fail"
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
**Severity**: Importance level determining response to validation failure  
**Test Portfolio**: Static set of 5 trades used for validation testing  
**Validation Run**: Single execution of validation endpoint  
**Pass**: Actual value within tolerance of expected value  
**Fail**: Actual value outside tolerance  
**Warn**: Near tolerance limit (within 10% of boundary)
