**Owner:** Director of Quality; QA Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-16
**Source:** ST-10 / BLG-QA-49 — v5.6 sprint execution

---

# Arc 5 Test Scenario Completeness Assessment

## Purpose

Intermediate assessment of Playwright and unit test coverage for the three shipped Arc 5 features: SI-01 (PreEntryValidationPanel), SI-03 (RedFlagJournal.js), and SI-05 Phase 1 (allocation_insufficient badge + digest). Identifies coverage gaps and proposes remediation paths ahead of BLG-QA-26 (Arc 5 E2E QA protocol).

## Feature × AC × Test Scenario Coverage Map

### SI-01 — Pre-Entry Rule Validation Gate

**Sources:** `tests/e2e/si01-si03-integration.spec.js`, `tests/test_pre_entry_validation.py` (20 tests in class methods)

| AC | Description | Test Scenario | File | Status |
|----|-------------|--------------|------|--------|
| SI-01-AC-01 | Panel renders with failing check | SC-SI-01a | si01-si03-integration.spec.js | ✅ Covered |
| SI-01-AC-02 | Override acknowledgement checkbox present | SC-SI-01b | si01-si03-integration.spec.js | ✅ Covered |
| SI-01-AC-03 | Override checkbox is interactive | SC-SI-01c | si01-si03-integration.spec.js | ✅ Covered |
| SI-01-AC-04 | Integration path: TradePlan → validation → navigate to RFJ | SC-SI-PATH-01 | si01-si03-integration.spec.js | ✅ Covered |
| SI-01-AC-05 | All-pass state (no failing checks — panel shows success) | None found | — | ❌ Gap (GAP-ARC5-01) |
| SI-01-AC-06 | Backend unit: 5 validation rules (regime, cash, sector, earnings, sizing) | 20 unit tests including `test_all_pass_gives_pass` | test_pre_entry_validation.py | ✅ Covered |

### SI-03 — Red Flag Journal

**Sources:** `tests/e2e/red-flag-journal.spec.js`, `tests/e2e/si01-si03-integration.spec.js`, `tests/test_red_flag_journal.py` (7 tests in class methods)

| AC | Description | Test Scenario | File | Status |
|----|-------------|--------------|------|--------|
| SI-03-AC-01 | Page renders with events — type, ticker, date visible | SC-RFJ-01 | red-flag-journal.spec.js | ✅ Covered |
| SI-03-AC-02 | Empty state when API returns 0 events | SC-RFJ-02 | red-flag-journal.spec.js | ✅ Covered |
| SI-03-AC-03 | Filter by event_type narrows results | SC-RFJ-03 | red-flag-journal.spec.js | ✅ Covered |
| SI-03-AC-04 | Event from SI-01 override path visible in RFJ | SC-SI-PATH-02 | si01-si03-integration.spec.js | ✅ Covered |
| SI-03-AC-05 | Pagination (>N events — E2E load-more scenario) | None found | — | ❌ Gap (GAP-ARC5-02) |
| SI-03-AC-06 | Backend unit: write path (SI-01 override → red_flag_events insert); filter forwarding | 7 unit tests including `test_create_plan_with_override_writes_event`, `test_pagination_params_forwarded` | test_red_flag_journal.py | ✅ Covered |

**Note:** Backend pagination parameter forwarding (`test_pagination_params_forwarded`) is unit-tested; the gap is specifically at the Playwright/E2E level for full pagination rendering.

### SI-05 Phase 1 — allocation_insufficient Badge + Weekly Digest

#### allocation_insufficient badge (Signals page)

**Source:** `tests/e2e/signals-allocation-insufficient.spec.js`

| AC | Description | Test Scenario | File | Status |
|----|-------------|--------------|------|--------|
| Badge visible on signal card | Orange "Cannot Size" badge | SC-SIG-AI-01a | signals-allocation-insufficient.spec.js | ✅ Covered |
| Panel rendered below card | "Allocation insufficient" panel | SC-SIG-AI-01b | signals-allocation-insufficient.spec.js | ✅ Covered |
| Reason string rendered | Reason text in card | SC-SIG-AI-02a | signals-allocation-insufficient.spec.js | ✅ Covered |
| Null reason no error | No crash when reason is null | SC-SIG-AI-02b | signals-allocation-insufficient.spec.js | ✅ Covered |
| Active signal badge correct | "New Signal" not "Cannot Size" | SC-SIG-AI-03a | signals-allocation-insufficient.spec.js | ✅ Covered |

#### Arc 5 Compliance Section (PerformanceAnalytics page)

**Source:** `tests/e2e/arc5-compliance-section.spec.js`

| AC | Description | Test Scenario | File | Status |
|----|-------------|--------------|------|--------|
| Section heading visible | "Arc 5 Signal Compliance" heading | SC-ARC5-01 | arc5-compliance-section.spec.js | ✅ Covered |
| All stat card titles visible | 4 metric cards present | SC-ARC5-02 | arc5-compliance-section.spec.js | ✅ Covered |
| Loading skeleton shown | Skeleton while pending | SC-ARC5-03 | arc5-compliance-section.spec.js | ✅ Covered |
| Error state | "Unable to load" shown | SC-ARC5-04 | arc5-compliance-section.spec.js | ✅ Covered |
| Compliance score trend value verified | Value rendered correctly from API | None found | — | ❌ Gap (GAP-ARC5-03) |

#### SI-05 Digest Delivery (API level)

**Source:** `tests/e2e/si05-digest-delivery.spec.js`, `tests/test_si05_digest_service.py`

| AC | Description | Test Scenario | File | Status |
|----|-------------|--------------|------|--------|
| Successful delivery returns sent=true | POST /digest/si05/send | si05-digest-delivery.spec.js | ✅ Covered |
| Zero red flags handled | Graceful empty state | si05-digest-delivery.spec.js | ✅ Covered |
| Message length > 0 | Content present | si05-digest-delivery.spec.js | ✅ Covered |
| Response shape consistent | All scenarios | si05-digest-delivery.spec.js | ✅ Covered |
| N/A pass rate includes reason | "N/A (no events this week)" distinct from "N/A (data unavailable)" | ST-02 (in progress this sprint) | si05_digest_service.py | 🔄 In progress — AC met when ST-02 commits |

**Note on N/A row:** ST-02 (BLG-FE-74) in this sprint directly addresses this AC. No gap ID assigned — this AC will be covered by ST-02's unit tests and/or E2E addition. Treated as in-sprint remediation, not a gap.

#### SI-05 Weekly Digest (frontend display)

**Source:** `tests/e2e/weekly-digest.spec.js`

| AC | Description | Test Scenario | File | Status |
|----|-------------|--------------|------|--------|
| Heading renders | "Weekly Digest" heading | SC-DIG-01 | weekly-digest.spec.js | ✅ Covered |
| All 8 digest fields displayed | Field presence | SC-DIG-02 | weekly-digest.spec.js | ✅ Covered |
| Numeric formatting | Formatted values | SC-DIG-03 | weekly-digest.spec.js | ✅ Covered |
| Null value renders em-dash | Null unrealised_pnl_delta_7d | SC-DIG-04 | weekly-digest.spec.js | ✅ Covered |
| Error state | API failure | SC-DIG-05 | weekly-digest.spec.js | ✅ Covered |

#### SI-02 Backend (Behavioural Drift Service — included per BLG-QA-45)

**Source:** `tests/test_behavioural_drift_service.py` — **35 unit tests**

| Coverage Area | Test Count | Status |
|--------------|-----------|--------|
| Drift computation (sufficient/insufficient data, zero trades) | 3 | ✅ Covered |
| Entry timing drift (4 scenarios) | 4 | ✅ Covered |
| Sizing adherence (4 variants) | 4 | ✅ Covered |
| Consecutive loss sizing | 2 | ✅ Covered |
| Regime context (4 variants) | 4 | ✅ Covered |
| Security/error safety | 2 | ✅ Covered |
| Additional edge cases | 16 | ✅ Covered |
| Frontend Playwright coverage | — | ❌ Expected gap (frontend gated on 20+ trades) |

## Summary Table

| Feature | ACs Covered | Playwright Scenarios | Backend Unit Tests | Status |
|---------|-------------|---------------------|-------------------|--------|
| SI-01 (Pre-entry validation) | 5/6 ACs | 4 (SC-SI-01a/b/c + SC-SI-PATH-01) | 20 tests | ⚠️ 1 gap (GAP-ARC5-01) |
| SI-03 (Red Flag Journal) | 5/6 ACs | 4 (SC-RFJ-01/02/03 + SC-SI-PATH-02) | 7 tests | ⚠️ 1 gap (GAP-ARC5-02) |
| SI-05 allocation badge | 5/5 ACs | 5 (SC-SIG-AI-01a/b/02a/02b/03a) | N/A (frontend) | ✅ Complete |
| SI-05 compliance section | 4/5 ACs | 4 (SC-ARC5-01/02/03/04) | N/A (frontend) | ⚠️ 1 gap (GAP-ARC5-03) |
| SI-05 digest API | 4/4 ACs | 4 (si05-digest-delivery.spec.js) | 26 unit tests | ✅ Complete |
| SI-05 digest frontend | 5/5 ACs | 5 (SC-DIG-01/02/03/04/05) | N/A (frontend) | ✅ Complete |
| SI-02 drift backend | Full backend coverage | 0 (frontend gated) | 35 unit tests | ✅ Complete |

## Top-3 Coverage Gaps

### GAP-ARC5-01 (P3): SI-01 all-pass state not covered by Playwright

**Gap:** No Playwright scenario exercises the case where all 5 validation checks pass and the panel shows a success/green state. SC-SI-01a/b/c only test the failure + override path. The backend `test_all_pass_gives_pass` unit test confirms the logic works, but the frontend rendering of the all-pass state is not verified.

**Risk:** Regression in the pass-state rendering branch (e.g., conditional CSS or component logic) would not be caught by CI.

**Proposed remediation:** Add `SC-SI-01d: All validation checks pass — panel shows success state` to `si01-si03-integration.spec.js`. Mock all checks as passing in the API response; assert no override checkbox visible and a success indicator present.

**Effort:** XS (<1 hour)

### GAP-ARC5-02 (P3): SI-03 pagination not covered by Playwright

**Gap:** `red-flag-journal.spec.js` covers single-page event list (SC-RFJ-01) and empty state (SC-RFJ-02), but not pagination rendering. The backend pagination parameter forwarding is unit-tested; the gap is the E2E scenario confirming the frontend requests page 2+ and renders additional events.

**Proposed remediation:** Add `SC-RFJ-04: Pagination — load-more renders additional events` to `red-flag-journal.spec.js`. Requires mock payload with events > page size and a load-more trigger.

**Effort:** XS (<1 hour)

### GAP-ARC5-03 (P3): Compliance score trend value not verified by Playwright

**Gap:** `arc5-compliance-section.spec.js` covers heading, card titles, loading skeleton, and error state (SC-ARC5-01/02/03/04) but does not verify that compliance score trend values are rendered correctly from the API response (e.g., pass rate % formatted correctly, trend direction indicator present).

**Proposed remediation:** Add `SC-ARC5-05: Compliance score trend value rendered from API` to `arc5-compliance-section.spec.js`. Use mock payload with known values; assert formatted value visible.

**Effort:** XS (<1 hour)

## Relationship to BLG-QA-26

Per `docs/qa/arc5_qa_completion_criteria.md` (ST-09 v5.6), this assessment (C-05) is the final remaining criterion before BLG-QA-26 may enter sprint planning. All three gaps above are P3 Playwright scenario gaps against shipped and unit-tested features. None block BLG-QA-26 sprint planning — they should be filed as backlog items and addressed within BLG-QA-26 scope or in a parallel sprint.

## Sign-Off

| Role | Decision | Date |
|------|----------|------|
| Director of Quality | Approved | 2026-06-16 |
