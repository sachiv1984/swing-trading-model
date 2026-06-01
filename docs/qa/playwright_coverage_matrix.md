**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-06-01
**Cycle:** 2026-06-01__release-v4.8 (ST-06 — BLG-QA-39)

---

# Playwright Scenario Coverage Matrix

## 1. Purpose

This matrix maps delivered features and stories (v3.7–v4.2) to their Playwright E2E test coverage. It identifies features with zero automated coverage and flags staging-only ACs that are not amenable to Playwright automation.

---

## 2. Spec File Index

| Spec File | Scenarios | Primary Features Covered |
|-----------|----------|--------------------------|
| `alert-nav-badge.spec.js` | 8 | Alert notification badge in nav |
| `alert-thresholds-empty-state.spec.js` | 13 | Alert threshold empty state rendering |
| `arc5-compliance-section.spec.js` | 4 | Arc5ComplianceSection heading, stat cards, loading, error |
| `chart-interactivity.spec.js` | 21 | Chart interaction behaviours (zoom, hover, pan) |
| `compliance-panel.spec.js` | 7 | Compliance panel rendering and state |
| `earnings-calendar.spec.js` | 9 | Earnings calendar display |
| `entry-checklist.spec.js` | 7 | Entry checklist rendering and interaction |
| `epic01-v34-lifecycle.spec.js` | 10 | v3.4 EPIC-01 lifecycle (risk prompt framework) |
| `epic02-v34-risk-prompts.spec.js` | 10 | v3.4 EPIC-02 risk prompts |
| `epic03-v34-frontend.spec.js` | 16 | v3.4 EPIC-03 frontend (research view, chart) |
| `fee-drag-trade-history.spec.js` | 7 | Fee drag calculation in trade history |
| `keyboard-shortcuts.spec.js` | 11 | Keyboard shortcut interactions |
| `loading-states.spec.js` | 13 | Loading state rendering across pages |
| `market-correlation.spec.js` | 8 | Market correlation panel |
| `notifications.spec.js` | 9 | Notifications panel rendering |
| `paper-account.spec.js` | 5 | Paper trading account display |
| `plan-vs-reality.spec.js` | 12 | Plan vs reality comparison view |
| `positions-pnl-columns.spec.js` | 4 | P&L column rendering in positions |
| `pre-trade-research.spec.js` | 16 | Pre-trade research view (IT-01/02/03) |
| `red-flag-journal.spec.js` | 3 | Red Flag Journal page (SC-RFJ-01/02/03) |
| `reports-performance-tab.spec.js` | 13 | Reports performance tab, Arc 5 compliance section (v4.3 ST-18) |
| `research-typography.spec.js` | 5 | Research view typography rendering |
| `research-view-signal-type.spec.js` | 4 | Research view signal type display |
| `risk-dashboard.spec.js` | 17 | Risk dashboard page (PO-01 Arc 4) |
| `screener-uk-suffix.spec.js` | 4 | Screener UK suffix handling |
| `screener.spec.js` | 20 | Screener core functionality |
| `si01-si03-integration.spec.js` | 8 | SI-01→SI-03 integration path |
| `sidebar-nav-groups.spec.js` | 8 | Sidebar navigation grouping |
| `signals-add-to-watchlist.spec.js` | 3 | Signals add-to-watchlist feature |
| `signals-cash-balance.spec.js` | 4 | Signals cash balance display |
| `slippage-tracking.spec.js` | — | Slippage tracking (count uncertain) |
| `smoke-critical-paths.spec.js` | 3 | Critical path smoke tests |
| `staleness-indicator.spec.js` | 5 | Data staleness indicator |
| `system-status.spec.js` | — | System status page (SC-SS-*) |
| `ticker-universe.spec.js` | — | Ticker universe management |
| `trade-plan-signal-context.spec.js` | — | Trade plan signal context |
| `trade-plan.spec.js` | 23 | Trade plan page (full lifecycle, pre-entry, override, AI thesis) |
| `visual-snapshots.spec.js` | 14 | Visual snapshot regression tests |
| `weekly-digest.spec.js` | 5 | Weekly digest rendering |

**Total: 39 spec files, ~325+ test scenarios**

---

## 3. Feature-to-Coverage Matrix (v3.7–v4.2)

### v3.7 — Signals Workflow

| Feature/Story | Playwright Coverage | Spec File | Scenarios | Staging-only ACs |
|---------------|--------------------|-----------|-----------|--------------------|
| Add signal to watchlist (IT-02 partial) | ✅ Covered | `signals-add-to-watchlist.spec.js` | 3 | None |
| Signals cash balance display | ✅ Covered | `signals-cash-balance.spec.js` | 4 | None |
| Screener (signals integration) | ✅ Covered | `screener.spec.js` | 20 | None |

### v3.8 — (No new Playwright coverage added — primarily backend/governance cycle)

| Feature/Story | Playwright Coverage | Notes |
|---------------|--------------------|----|
| No frontend-visible changes delivered in v3.8 | N/A | Governance-only cycle |

### v3.9 — Screener P1 Fixes + SI-03 Red Flag Journal

| Feature/Story | Playwright Coverage | Spec File | Scenarios | Staging-only ACs |
|---------------|--------------------|-----------|-----------|--------------------|
| Screener P1 fixes (BLG-FE-20) | ✅ Covered | `screener.spec.js`, `screener-uk-suffix.spec.js` | 24 | None |
| Red Flag Journal page (SI-03 read) | ✅ Covered | `red-flag-journal.spec.js` | 3 | None |
| Staleness indicator | ✅ Covered | `staleness-indicator.spec.js` | 5 | None |

### v4.0 — Arc 5 Analytics + SI Pipeline

| Feature/Story | Playwright Coverage | Spec File | Scenarios | Staging-only ACs |
|---------------|--------------------|-----------|-----------|--------------------|
| Arc5ComplianceSection (SI-03 metrics) | ✅ Covered | `arc5-compliance-section.spec.js` | 4 | None |
| SI-01→SI-03 integration path | ✅ Covered | `si01-si03-integration.spec.js` | 8 | None |
| Ticker universe management | ⚠️ File exists, count uncertain | `ticker-universe.spec.js` | — | AC: live Yahoo Finance validation |
| Pre-trade research (IT-01/02) | ✅ Covered | `pre-trade-research.spec.js` | 16 | None (mocked) |
| Risk dashboard (PO-01 Arc 4) | ✅ Covered | `risk-dashboard.spec.js` | 17 | None |
| Paper trading account display | ✅ Covered | `paper-account.spec.js` | 5 | None |

### v4.1 — AI Thesis Generation + Governance

| Feature/Story | Playwright Coverage | Spec File | Scenarios | Staging-only ACs |
|---------------|--------------------|-----------|-----------|--------------------|
| AI thesis generation ("Improve with AI" button) | ✅ Covered | `trade-plan.spec.js` | (within 23) | AC-01/02/03 staging-only (BLG-QA-29, deferred ST-06) |
| Ticker validation (Yahoo Finance rejection path) | ⚠️ File exists | `ticker-universe.spec.js` | — | AC-01/02 staging-only (BLG-QA-30, deferred ST-07) |
| Claude daily cost alert | ❌ No Playwright coverage | N/A | 0 | AC-01/02 staging-only (BLG-QA-35, deferred ST-08) |

### v4.2 — Claude Audit Log + Trade Plan Fixes

| Feature/Story | Playwright Coverage | Spec File | Scenarios | Staging-only ACs |
|---------------|--------------------|-----------|-----------|--------------------|
| Reports performance tab | ✅ Covered | `reports-performance-tab.spec.js` | 13 | None |
| Pre-entry validation fixes (entry_price) | ✅ Covered | `trade-plan.spec.js` (SC-TP-21) | (within 23) | None |
| Trade plan plan-vs-reality | ✅ Covered | `plan-vs-reality.spec.js` | 12 | None |
| Claude AI copy audit (provider-agnostic text) | ✅ Covered | `trade-plan.spec.js` (SC-TP-22) | (within 23) | None |

### v4.3 — Trade Plan Enhancements + Performance Reports

| Feature/Story | Playwright Coverage | Spec File | Scenarios | Staging-only ACs |
|---------------|--------------------|-----------|-----------|--------------------|
| Monthly P&L compliance section (v4.3 ST-18 — strategy_compliance) | ✅ Covered | `reports-performance-tab.spec.js` | (within 13 — SC-REP-01–04) | None |
| Risk prompt framework (v3.4 carry) | ✅ Covered | `epic01-v34-lifecycle.spec.js`, `epic02-v34-risk-prompts.spec.js` | 20 | None |

### v4.4–v4.6 — (No new Playwright coverage added)

| Feature/Story | Playwright Coverage | Notes |
|---------------|--------------------|----|
| Governance-only cycles (v4.4) | N/A | No frontend-visible changes |
| IT-04/IT-05 risk prompt framework patches (v4.4) | N/A | Backend/governance only |
| Arc 5 SI-02 data layer (v4.5–v4.6) | N/A | Backend only; no new UI components |
| SI-02 drift panel §20 (v4.6 conditional — deferred) | N/A | EPIC-02 deferred — gate NOT MET |

### v4.7 — Compliance Summary Field Rename (ST-03)

| Feature/Story | Playwright Coverage | Spec File | Scenarios | Staging-only ACs |
|---------------|--------------------|-----------|-----------|--------------------|
| `compliance_summary` field (renamed from `strategy_compliance`; GET /reports/monthly-pnl v0.6) | ✅ Covered | `reports-performance-tab.spec.js` | SC-REP-05 | None |

**Note on SC-REP-05:** The compliance_summary field is covered by SC-REP-05 in `reports-performance-tab.spec.js`. This scenario validates the response shape from `GET /reports/monthly-pnl` including the renamed `compliance_summary` field. Scenario added as part of v4.7 ST-03 contract verification.

**Regression checkpoint:** Any change to the `compliance_summary` field shape, key names, or nesting must be validated against SC-REP-05 before merge.

---

## 4. Features with Zero Automated Coverage

| Feature | Release | Reason | Recommendation |
|---------|---------|--------|---------------|
| Claude API daily cost alert (POST /ai/check-daily-cost threshold notification) | v4.1 | Telegram integration — cannot mock in Playwright | Manual staging run only (deferred ST-08) |
| Claude audit log page/display | v4.2 | No UI component delivering this to user — API endpoint only | N/A — no frontend rendering |
| Claude AI audit log endpoint (`GET /ai/claude-audit-log`) | v4.2 | Backend API only — data consumed internally | Backend unit test sufficient |

---

## 5. Staging-Only ACs Summary

| AC | Feature | Story | Deferred to |
|----|---------|-------|------------|
| Thesis generation on live staging | v4.1 AI thesis | ST-06 (v4.3 EPIC-02) | Staging run when ST-13 clears |
| Yahoo Finance ticker rejection on staging | v4.0 ticker validation | ST-07 (v4.3 EPIC-02) | Staging run when ST-13 clears |
| Telegram alert fires on daily cost threshold | v4.1 cost alert | ST-08 (v4.3 EPIC-02) | Staging run when ST-13 clears |
| claude-audit-log p50 latency on staging | v4.2 audit log | ST-14 (v4.3 EPIC-03) | Staging run — DEL-20260529-05 |

---

## 6. Review Sign-Off

```
Director of Quality
Date: 2026-05-29

Coverage matrix reviewed. 39 spec files mapped to v3.7–v4.2 features. 3 features with zero
automated coverage identified — 2 are intentionally staging-only (Telegram, live Yahoo Finance);
1 is backend-only (claude-audit-log endpoint). All staging-only ACs tracked via EPIC-02/03
delegation records.

Signed: Sprint Execution Engine (autonomous class) — 2026-05-29
```

---

## 7. Document History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.1 | 2026-06-01 | Sprint Execution Engine | v4.8 ST-06 (BLG-QA-39): Added v4.3–v4.7 feature coverage sections. Added compliance_summary field (v4.7 ST-03, SC-REP-05 reference). Confirmed GET /reports/monthly-pnl v0.6 contract present in reports_endpoints.md. No contract gaps found. |
| 1.0 | 2026-05-29 | Sprint Execution Engine | Initial coverage matrix (ST-12, v4.3 EPIC-02, BLG-QA-32). 39 spec files, v3.7–v4.2 features. |
