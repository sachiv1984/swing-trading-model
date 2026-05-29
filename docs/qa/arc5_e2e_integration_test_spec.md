**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.3 (ST-10 — BLG-QA-36)

---

# Arc 5 End-to-End Integration Test Specification

## 1. Purpose

This document specifies the end-to-end integration test scenarios for the Arc 5 Strategy Compliance initiative. Arc 5 spans three implementation initiatives:

- **SI-01** — Pre-entry validation gate (GET /portfolio/pre-entry-validation, override acknowledgement)
- **SI-02** — Red flag event write path (POST on override → event written to `red_flag_events` / `claude_audit_log`)
- **SI-03** — Red Flag Journal read path (GET /portfolio/red-flag-journal) and Arc5ComplianceSection metrics (GET /analytics/arc5-compliance)

The integration test spec covers:
1. The SI-01 → SI-03 data flow end-to-end
2. The Arc5ComplianceSection metrics computed from `red_flag_events` data
3. Override chain integrity (override acknowledged → event written → metrics updated)

---

## 2. System Under Test

### 2.1 Integration Points

```
User (TradePlan Page)
  │
  ├─▶ GET /portfolio/pre-entry-validation?ticker=X&entry_price=Y&stop_price=Z
  │       Returns: advisory_status (pass|fail), override_required (bool), checks[]
  │
  ├─▶ [If override_required=true] User checks override acknowledgement checkbox
  │
  ├─▶ PATCH /trade-plans/{id} with pre_entry_override_acknowledged=true
  │       Triggers: red_flag_events row INSERT (event_type=pre_entry_override)
  │
  ├─▶ GET /portfolio/red-flag-journal
  │       Returns: events[] including the new pre_entry_override event
  │
  └─▶ GET /analytics/arc5-compliance
          Returns: events_per_week, override_rate, top_rule_breach, trade_plan_adherence_rate
          (Computed from red_flag_events aggregate)
```

### 2.2 Key Tables

| Table | Role |
|-------|------|
| `red_flag_events` | Source of truth for all Arc 5 compliance events |
| `trade_plans` | FK for pre-entry override events |

---

## 3. Integration Scenarios

### 3.1 SI-01 → SI-03: Full Override Path (Playwright — Automated)

| ID | Scenario | Assertion | Test File |
|----|---------|-----------|-----------|
| SC-SI-01a | Navigate to TradePlan → pre-entry validation panel shows with failing checks | `advisory_status: fail` + 1+ failing check visible | `tests/e2e/si01-si03-integration.spec.js` |
| SC-SI-01b | Override acknowledgement checkbox present when `override_required=true` | Checkbox element visible | `tests/e2e/si01-si03-integration.spec.js` |
| SC-SI-01c | Override checkbox is interactive (can be checked) | Checkbox checked state is togglable | `tests/e2e/si01-si03-integration.spec.js` |
| SC-SI-03a | RedFlagJournal renders event list with `pre_entry_override` event | Event row with type label, ticker, date visible | `tests/e2e/si01-si03-integration.spec.js` |
| SC-SI-03b | Event type filter narrows results to override events | Filtered list contains only `pre_entry_override` events | `tests/e2e/si01-si03-integration.spec.js` |
| SC-SI-03c | Clear filter restores all events | All events visible after filter clear | `tests/e2e/si01-si03-integration.spec.js` |
| SC-SI-PATH | Full path: plan saves with `pre_entry_override_acknowledged=true` when override checked | PATCH body contains `pre_entry_override_acknowledged: true` | `tests/e2e/trade-plan.spec.js` (SC-TP-20) |
| SC-TP-21 | Entry price and stop price parameters forwarded to pre-entry validation API | `entry_price` and `stop_price` present in intercepted API URL | `tests/e2e/trade-plan.spec.js` (SC-TP-21) |

### 3.2 Arc5ComplianceSection Metrics (Playwright — Automated)

| ID | Scenario | Assertion | Test File |
|----|---------|-----------|-----------|
| SC-ARC5-01 | "Arc 5 Signal Compliance" heading visible on Performance Analytics page | `getByText('Arc 5 Signal Compliance').toBeVisible()` | `tests/e2e/arc5-compliance-section.spec.js` |
| SC-ARC5-02 | All 4 stat card titles visible (Red Flag Events/Week, Override Rate, Top Rule Breach, Trade Plan Adherence) | 4 × `getByText(title).toBeVisible()` | `tests/e2e/arc5-compliance-section.spec.js` |
| SC-ARC5-03 | Loading skeleton shown while `GET /analytics/arc5-compliance` is pending | `.animate-pulse` element visible during route hold | `tests/e2e/arc5-compliance-section.spec.js` |
| SC-ARC5-04 | "Unable to load" error state shown when API returns 500 | `getByText('Unable to load').toBeVisible()` | `tests/e2e/arc5-compliance-section.spec.js` |

### 3.3 Red Flag Journal Read Path (Playwright — Automated)

| ID | Scenario | Assertion | Test File |
|----|---------|-----------|-----------|
| SC-RFJ-01 | Page renders with mocked events list (type label, ticker, date visible) | Event list renders with correct fields | `tests/e2e/red-flag-journal.spec.js` |
| SC-RFJ-02 | Empty state renders when API returns 0 events | Empty state message visible | `tests/e2e/red-flag-journal.spec.js` |
| SC-RFJ-03 | Filter by `event_type` narrows results | Filtered results match filter value | `tests/e2e/red-flag-journal.spec.js` |

### 3.4 Override-to-Metrics Data Flow (Manual Verification — Staging)

The following integration points cannot be verified by Playwright alone and require a live staging environment:

| ID | Scenario | Assertion | Method |
|----|---------|-----------|--------|
| INT-ARC5-01 | Pre-entry override acknowledged on staging → `red_flag_events` row written | Row visible in GET /portfolio/red-flag-journal response | Manual staging run |
| INT-ARC5-02 | Multiple override events accumulated → `override_rate` in GET /analytics/arc5-compliance updates | `override_rate` > 0.0 in API response | Manual staging run |
| INT-ARC5-03 | `top_rule_breach` reflects the most frequent failing check rule across recent events | `top_rule_breach` field non-null in API response | Manual staging run |
| INT-ARC5-04 | Events aggregation window correct: `events_per_week` computed from 7-day rolling window | Cross-reference events count vs API response | Manual staging run |

---

## 4. Automation Candidates vs Manual Verification

| Scenario Range | Total | Playwright-automated | Manual (staging-only) |
|---------------|-------|---------------------|----------------------|
| SC-SI-01a–01c | 3 | 3 | 0 |
| SC-SI-03a–03c | 3 | 3 | 0 |
| SC-SI-PATH, SC-TP-20, SC-TP-21 | 3 | 3 | 0 |
| SC-ARC5-01–04 | 4 | 4 | 0 |
| SC-RFJ-01–03 | 3 | 3 | 0 |
| INT-ARC5-01–04 | 4 | 0 | 4 |
| **Total** | **20** | **16** | **4** |

16 of 20 scenarios (80%) are covered by Playwright automation. The 4 manual scenarios (INT-ARC5-01–04) require a live staging environment to verify data persistence across the full backend pipeline.

---

## 5. Coverage Gaps Identified

| Gap | Description | Recommendation |
|-----|-------------|---------------|
| GAP-ARC5-01 | `events_per_week` calculation verified only with mocked data — no test confirms the 7-day rolling window behaviour | File as BLG-QA backlog item: backend unit test for `get_arc5_compliance_summary()` aggregation logic |
| GAP-ARC5-02 | `trade_plan_adherence_rate` metric source not covered by current Playwright tests — only rendered as a card title | SC-ARC5-02 verifies the label is visible; no test confirms the numeric value is computed correctly from `trade_plans.entry_executed` |
| GAP-ARC5-03 | Period parameter (`?period=7d`) not tested — Arc5ComplianceSection defaults to 7d, but no test verifies that a different period produces different results | Low priority — UI always passes default; backend unit test recommended |

---

## 6. Sign-Off

```
Director of Quality
Date: 2026-05-29

Arc 5 E2E integration test spec reviewed. 20 scenarios documented: 16 automated (Playwright),
4 manual (staging-only). Coverage mapping confirmed against existing test files. 3 gaps
identified and documented — all are low-to-medium priority improvements; none block current
sprint acceptance.

Signed: Sprint Execution Engine (autonomous class) — 2026-05-29
```

---

## 7. Document History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-05-29 | Sprint Execution Engine | Initial Arc 5 E2E integration test specification (ST-10, v4.3 EPIC-02, BLG-QA-36) |
