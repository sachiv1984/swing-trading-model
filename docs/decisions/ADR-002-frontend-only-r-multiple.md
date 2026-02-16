# ADR-002: Frontend-Only R-Multiple Calculation

**Date**: 2026-02-16  
**Status**: Accepted  
**Deciders**: Analytics Team, Backend Team

---

## Context

R-Multiple is a useful metric for evaluating trade quality relative to risk. However, its calculation requires `stop_price` field, which isn't always available in `trade_history` table (many historical trades lack initial stops).

---

## Decision

R-Multiple will be calculated **frontend-only** in `RMultipleAnalysis.js` component, not in backend analytics endpoint.

---

## Rationale

**Pros of Frontend-Only**:
- ✅ Already implemented and working
- ✅ Can access full position context including stops
- ✅ Avoids data migration to add stops to trade_history
- ✅ Performance not critical (runs client-side on-demand)

**Cons of Frontend-Only**:
- ❌ Not available via API for external tools
- ❌ Can't validate with automated tests
- ❌ No historical trending via API
- ❌ Inconsistent with other metrics (all backend-calculated)

---

## Alternatives Considered

### Alternative 1: Move to Backend
**Pros**: Consistency, validation, API access  
**Cons**: Requires data migration, many trades lack stops  
**Verdict**: Too much migration effort for marginal benefit

### Alternative 2: Hybrid (Backend + Frontend Fallback)
**Pros**: Best of both worlds  
**Cons**: Complexity, two code paths, testing burden  
**Verdict**: Over-engineered for current needs

---

## Consequences

**Positive**:
- R-Multiple feature works today without backend changes
- No data migration required
- Development velocity maintained

**Negative**:
- API consumers can't access R-Multiple
- Can't include in validation suite
- Metric calculation split across frontend/backend

---

## Future Considerations

**Revisit in v2.0 if**:
1. External API consumers request R-Multiple access
2. Need automated validation of R-Multiple
3. Complete data migration of historical stops

---

## Implementation Notes

**File**: `src/components/analytics/RMultipleAnalysis.js`  
**Lines**: 30-50

**Calculation**:
```javascript
const rMultiple = (exit_price - entry_price) / (entry_price - stop_price)
```

**Filtering**:
- Excludes trades without `stop_price`
- Requires `entry_price` and `exit_price`
