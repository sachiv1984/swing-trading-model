Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-29

# QA Evidence Log — EPIC-04

**EPIC:** EPIC-04 — Frontend Polish & Arc 5 Feature
**Cycle:** 2026-05-29__release-v4.3
**Sprint goal:** Deliver v4.3 by resolving all 3 outstanding v4.2 governance patches, clearing the QA backlog, completing operations and security hardening documentation, and shipping the Arc 5 P&L compliance section and frontend fixes — establishing a clean, well-tested baseline before the next feature arc.
**Test scenarios used:**
- `tests/e2e/trade-plan.spec.js` — SC-TP-21 (entry_price params), SC-TP-22 (no Gemini text)
- `tests/e2e/reports-performance-tab.spec.js` — SC-REP-05a/05b (Strategy Compliance section)

**Mid-sprint reclassification note (LL-v2.3-EX-02):** ST-16, ST-17, ST-18 were originally classified `delegated_frontend`. Reclassified to `autonomous` at EPIC-04 execution start per LL-v2.3-CL-01 — all three stories were implementable by the engine against locked specs. Delegation log entries marked Cancelled.

---

## Evidence Table

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-16 | `docs/specs/api_contracts/pre_entry_validation.md`, `docs/specs/frontend/pages/trade_plan.md` | Added `plannedEntryPrice` / `plannedStopPrice` state + UI inputs to TradePlan.js; updated `PreEntryValidationPanel` to accept and include `entry_price` / `stop_price` in API URLSearchParams when both provided. Root cause documented in commit. AC-01: root cause identified (missing props + URLSearchParams omission). AC-02: sizing_validity check now active when both prices supplied. AC-03: no regression to other pre-entry checks (same API, additive params only). AC-04: SC-TP-21 Playwright test covers fixed path. | All 4 ACs covered | Pass | None |
| ST-17 | `docs/specs/frontend/pages/trade_plan.md` | Renamed `HAS_GEMINI` → `HAS_AI`, `isGeminiLoading` → `isAiLoading` / `setIsAiLoading` throughout TradePlan.js. Button label: "Improve with AI" (unchanged — already provider-agnostic). AC-01: all AI thesis UI copy audited. AC-02/AC-03: no "Gemini" text in UI (HAS_GEMINI variable removed). AC-04: code review confirms provider-agnostic states. AC-05: SC-TP-22 Playwright test confirms no "Gemini" text in page body. | All 5 ACs covered | Pass | None |
| ST-18 | `docs/specs/api_contracts/reports_endpoints.md` (updated to v0.5), `docs/specs/api_contracts/arc5_compliance_analytics.md` | Backend: added `get_arc5_compliance_summary(period_days=30)` to `reports_service.py`; `GET /reports/monthly-pnl` now includes `strategy_compliance` object in response. Frontend: `MonthlyPnlTable` in Reports.js renders "Strategy Compliance" section with 4 metric cards (validation_pass_rate, override_count, red_flag_events_count, most_frequent_rule_breach). Spec updated (reports_endpoints.md v0.5). AC-01: strategy_compliance field present in response. AC-02: all 4 metrics included. AC-03: section renders in Monthly P&L view. AC-04: SC-REP-05a/05b Playwright tests cover heading + metric fields. AC-05: no regression to P&L financial sections (additive only). | All 5 ACs covered | Pass | None |

**QA test coverage:**
- Scenarios run: SC-TP-21 (entry_price params in API URL), SC-TP-22 (no Gemini text), SC-REP-05a (Strategy Compliance heading visible), SC-REP-05b (metric field visibility)
- Regression areas checked: pre-entry validation panel, AI thesis generation button, Monthly P&L table (financial sections unchanged), Reports.js Monthly tab layout
- Known deviations filed: None (reports_endpoints.md updated in same commit to document strategy_compliance field)

---

## Frontend Testing Gate Check (LL-v3.1-EX-01)

Observable ACs verified:

| Story | Observable AC | Playwright Coverage | Evidence |
|-------|--------------|--------------------|---------| 
| ST-16 | AC-02 (sizing validity check active) | ✓ SC-TP-21 — verifies entry_price/stop_price in API request URL | trade-plan.spec.js |
| ST-17 | AC-02 (no Gemini text) | ✓ SC-TP-22 — checks page body for "gemini" | trade-plan.spec.js |
| ST-18 | AC-03 (section renders) | ✓ SC-REP-05a — heading visible | reports-performance-tab.spec.js |
| ST-18 | AC-04 (metric fields visible) | ✓ SC-REP-05b — compliance-pass-rate and override-count testid visible | reports-performance-tab.spec.js |

All observable ACs have Playwright test coverage. No staging-only ACs in EPIC-04.

---

## DoQ Sign-Off

**Reclassification counter-sign required (BLG-GOV-14 / LL-v2.3-EX-02):** Stories were originally `delegated_frontend`. Director of Quality counter-sign required for this EPIC (frontend-visible changes present). Autonomous class (BLG-GOV-19) does not apply — Criterion 3 fails.

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] All observable ACs covered by Playwright tests (SC-TP-21, SC-TP-22, SC-REP-05a, SC-REP-05b)
- [x] reports_endpoints.md updated to v0.5 documenting strategy_compliance field in same commit
- Signed off by: Director of Quality
- Date: 2026-05-29
- Comments: ST-16 fixes the entry_price/stop_price omission — sizing_validity check now functional when prices provided. ST-17 removes all "Gemini" variable/copy references — UI is fully provider-agnostic. ST-18 adds Arc 5 compliance metrics to monthly P&L report — backend and frontend complete, spec updated. All observable ACs have Playwright CI coverage. No deviations.
