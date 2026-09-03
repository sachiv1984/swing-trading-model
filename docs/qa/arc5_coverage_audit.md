**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-08-21 (ST-20, EPIC-04, v9.0, BLG-QA-144 — §3.3 SC-ARC5 subsection refreshed: added the since-landed SC-ARC5-05 row (BLG-QA-58, v5.7), audited value-formatting-level coverage specifically for `Arc5ComplianceSection`, found 3 new gaps (GAP-ARC5-06/07/08) the original 2026-05-29 pass didn't check at this granularity)
**Cycle:** 2026-05-29__release-v4.3 (ST-12 — BLG-QA-33); refreshed 2026-08-21__release-v9.0 (ST-20 — BLG-QA-144)

---

# Arc 5 Strategy Compliance — Playwright Coverage Audit

## 1. Purpose

This document audits the Playwright E2E coverage of all Arc 5 (Strategy Signal Integrity) features delivered across v3.9–v4.3. Arc 5 covers three initiatives: SI-01 (pre-entry validation), SI-03 (red flag events + journal), and the Arc5ComplianceSection analytics dashboard.

---

## 2. Feature Map

| Initiative | Feature | Endpoint(s) | Frontend Component |
|-----------|---------|------------|-------------------|
| SI-01 | Pre-entry validation gate | GET /portfolio/pre-entry-validation | `PreEntryValidationPanel` in TradePlan page |
| SI-01 | Override acknowledgement | PATCH /trade-plans/{id} (pre_entry_override_acknowledged) | Override checkbox in TradePlan page |
| SI-03 | Red Flag Journal read | GET /portfolio/red-flag-journal | `RedFlagJournal` page |
| SI-03 | Arc 5 compliance metrics | GET /analytics/arc5-compliance | `Arc5ComplianceSection` in PerformanceAnalytics |
| Arc 5 | Strategy compliance in P&L report | GET /reports/monthly-pnl (strategy_compliance field) | Strategy Compliance section in Reports page |

---

## 3. Scenario Coverage Audit

### 3.1 SC-SI-01 — Pre-Entry Validation (SI-01)

| Scenario ID | Description | Test File | Status |
|-------------|-------------|-----------|--------|
| SC-SI-01a | Pre-entry validation panel shows with failing checks | `si01-si03-integration.spec.js` | ✅ Covered |
| SC-SI-01b | Override acknowledgement checkbox present when `override_required=true` | `si01-si03-integration.spec.js` | ✅ Covered |
| SC-SI-01c | Override checkbox is interactive (can be checked) | `si01-si03-integration.spec.js` | ✅ Covered |
| SC-TP-20 | Plan saves with `pre_entry_override_acknowledged=true` when override checked | `trade-plan.spec.js` | ✅ Covered |
| SC-TP-21 | `entry_price` and `stop_price` forwarded to pre-entry validation API | `trade-plan.spec.js` | ✅ Covered |

**SI-01 Playwright coverage: 5/5 scenarios (100%)**

### 3.2 SC-RFJ — Red Flag Journal (SI-03 Read Path)

| Scenario ID | Description | Test File | Status |
|-------------|-------------|-----------|--------|
| SC-RFJ-01 | Page renders with mocked events list (type label, ticker, date visible) | `red-flag-journal.spec.js` | ✅ Covered |
| SC-RFJ-02 | Empty state renders when API returns 0 events | `red-flag-journal.spec.js` | ✅ Covered |
| SC-RFJ-03 | Filter by event_type narrows results | `red-flag-journal.spec.js` | ✅ Covered |
| SC-SI-03a | RedFlagJournal renders event list with `pre_entry_override` event | `si01-si03-integration.spec.js` | ✅ Covered |
| SC-SI-03b | Event type filter shows only `pre_entry_override` events | `si01-si03-integration.spec.js` | ✅ Covered |
| SC-SI-03c | Clear filter restores all events | `si01-si03-integration.spec.js` | ✅ Covered |

**SC-RFJ Playwright coverage: 6/6 scenarios (100%)**

### 3.3 SC-ARC5 — Arc5ComplianceSection (SI-03 Analytics)

| Scenario ID | Description | Test File | Status |
|-------------|-------------|-----------|--------|
| SC-ARC5-01 | "Arc 5 Signal Compliance" heading visible | `arc5-compliance-section.spec.js` | ✅ Covered |
| SC-ARC5-02 | All 4 stat card titles visible | `arc5-compliance-section.spec.js` | ✅ Covered |
| SC-ARC5-03 | Loading skeleton shown when API pending | `arc5-compliance-section.spec.js` | ✅ Covered |
| SC-ARC5-04 | Error state shown when API returns 500 | `arc5-compliance-section.spec.js` | ✅ Covered |
| SC-ARC5-05 | `override_rate`/`trade_plan_adherence_rate` render as formatted percentages (`fmtRate`) | `arc5-compliance-section.spec.js` | ✅ Covered (landed BLG-QA-58, v5.7 — not reflected in this doc's original v1.0 table, added in this refresh) |

**SC-ARC5 Playwright coverage: 5/5 scenarios (100%)**

#### 3.3.1 Refresh (2026-08-21, ST-20, BLG-QA-144) — value-formatting-level gaps

The original 2026-05-29 audit (and SC-ARC5-05's later addition) checked card *titles* and *one* of the component's three distinct value-formatting functions (`fmtRate`). `Arc5ComplianceSection.js` has two more formatting functions with no scenario coverage at all, plus a shared null-handling behaviour across all four cards that has never been exercised:

| Gap ID | Description | Function | Severity |
|--------|-------------|----------|----------|
| GAP-ARC5-06 | `events_per_week` (`fmtCount` — 1 decimal place, e.g. `3.0`) has no scenario asserting its rendered value — SC-ARC5-05 only covers the two `fmtRate` fields | `fmtCount` | P3 |
| GAP-ARC5-07 | `top_rule_breach` (`fmtText` — underscore-to-space replacement, e.g. `cash_constraint` → `cash constraint`) has no scenario at all | `fmtText` | P3 |
| GAP-ARC5-08 | No scenario covers any metric field being individually `null` (e.g. `top_rule_breach: null` while the other three fields are populated) — all three formatters (`fmtRate`/`fmtCount`/`fmtText`) render `"—"` for `null`, untested | `fmtRate`/`fmtCount`/`fmtText` | P3 |

Filed as `BLG-QA-154`, `BLG-QA-155`, `BLG-QA-156` respectively (`claude/backlog/backlog.md`).

### 3.4 SC-REP — Arc 5 in Monthly P&L Report (v4.3 ST-18)

| Scenario ID | Description | Test File | Status |
|-------------|-------------|-----------|--------|
| SC-REP-05a | "Strategy Compliance" heading visible in Reports performance tab | `reports-performance-tab.spec.js` | ✅ Covered |
| SC-REP-05b | Arc 5 metric cards visible in P&L compliance section | `reports-performance-tab.spec.js` | ✅ Covered |

**SC-REP Arc 5 coverage: 2/2 scenarios (100%)**

### 3.5 Integration Path

| Scenario ID | Description | Test File | Status |
|-------------|-------------|-----------|--------|
| SC-SI-PATH | Full path: override checkbox checked → PATCH body includes `pre_entry_override_acknowledged=true` | `si01-si03-integration.spec.js` | ✅ Covered |

**Integration path coverage: 1/1 scenario (100%)**

---

## 4. Coverage Summary

| Feature Area | Scenarios | Playwright Covered | Manual (Staging) | Coverage % |
|-------------|----------|-------------------|------------------|-----------|
| SI-01 Pre-entry validation | 5 | 5 | 0 | 100% |
| SI-03 Red Flag Journal | 6 | 6 | 0 | 100% |
| Arc5ComplianceSection | 5 | 5 | 0 | 100% |
| Arc 5 in P&L Report | 2 | 2 | 0 | 100% |
| Integration path | 1 | 1 | 0 | 100% |
| **Total** | **19** | **19** | **0** | **100%** |

All 19 observable Arc 5 acceptance criteria scenarios have Playwright E2E coverage. No observable AC is relying solely on code review or staging. **Caveat (2026-08-21 refresh):** "100% coverage" here means every *identified* scenario has a test — §3.3.1's refresh found 3 real value-formatting-level gaps that existed the whole time without ever being identified as scenarios in the first place (GAP-ARC5-06/07/08). A scenario-based coverage percentage is only as complete as the scenario list underneath it.

---

## 5. Gaps and Recommendations

| Gap ID | Description | Severity | Recommendation |
|--------|-------------|----------|---------------|
| GAP-ARC5-01 | No backend unit test confirms `events_per_week` 7-day rolling window calculation in `get_arc5_compliance_summary()` | P3 | File BLG-QA backlog item for backend unit test of aggregate query |
| GAP-ARC5-02 | `trade_plan_adherence_rate` computation not tested beyond UI render (card title visible) | P3 | **Resolved** by SC-ARC5-05 (BLG-QA-58, v5.7), which added the value-level assertion this gap called for — confirmed in this refresh, §3.3 |
| GAP-ARC5-03 | `GET /analytics/arc5-compliance?period=30d` (non-default period) not tested | P4 | Low priority — UI only passes `7d`; add when period selector is exposed to user |
| GAP-ARC5-04 | No test covers `SC-SI-01` with `advisory_status: pass` (all checks passing) — only failure+override path tested | P3 | Add scenario to `si01-si03-integration.spec.js`: all-pass returns clean panel with no override checkbox |
| GAP-ARC5-05 | `SC-REP-05a/05b` cover heading/card visibility but not the actual metric values in the compliance section | P3 | Add scenario to `reports-performance-tab.spec.js` confirming numeric metric values render from mocked data |
| GAP-ARC5-06 | `events_per_week` (`fmtCount`) rendered value never asserted | P3 | Filed `BLG-QA-154` |
| GAP-ARC5-07 | `top_rule_breach` (`fmtText`, underscore-to-space) rendered value never asserted | P3 | Filed `BLG-QA-155` |
| GAP-ARC5-08 | Per-field `null` → `"—"` handling never asserted for any of the four cards | P3 | Filed `BLG-QA-156` |

---

## 6. Review Sign-Off

```
Director of Quality
Date: 2026-05-29

Arc 5 Playwright coverage audit complete. All 18 observable Arc 5 scenarios have Playwright
E2E coverage (100%). 5 improvement gaps identified — all P3/P4, none blocking current sprint.
Gaps documented for backlog consideration.

Signed: Sprint Execution Engine (autonomous class) — 2026-05-29
```

```
QA Lead
Date: 2026-08-21

ST-20 (BLG-QA-144) refresh: audited Arc5ComplianceSection's Playwright coverage specifically
at the value-formatting level (all three distinct formatter functions — fmtRate, fmtCount,
fmtText — and the shared null-handling path), a finer grain than the 2026-05-29 pass checked.
5/5 identified scenarios remain covered (SC-ARC5-01..05); 3 new gaps found (GAP-ARC5-06/07/08)
and filed as BLG-QA-154/155/156. None blocking -- all P3, consistent with the story's own
priority. GAP-ARC5-02 (original audit) was already resolved by the pre-existing SC-ARC5-05
(BLG-QA-58, v5.7) — corrected from an earlier draft of this sign-off that mischaracterized it
as "superseded" by this refresh's new gaps, which cover distinct fields (fmtCount/null-handling,
not trade_plan_adherence_rate).

Signed: Sprint Execution Engine (agent-mediated, QA Lead role — §5.3) — 2026-08-21
```

---

## 7. Document History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.1 | 2026-08-21 | Sprint Execution Engine | §3.3 SC-ARC5 refresh (ST-20, v9.0 EPIC-04, BLG-QA-144). Added the since-landed SC-ARC5-05 row; audited value-formatting-level coverage specifically for `Arc5ComplianceSection`'s three distinct formatter functions and shared null-handling; found 3 new gaps (GAP-ARC5-06/07/08, filed BLG-QA-154/155/156); total scenario count 18 → 19. |
| 1.0 | 2026-05-29 | Sprint Execution Engine | Initial Arc 5 coverage audit (ST-12, v4.3 EPIC-02, BLG-QA-33). 18 scenarios audited, 100% Playwright coverage. 5 improvement gaps identified. |
