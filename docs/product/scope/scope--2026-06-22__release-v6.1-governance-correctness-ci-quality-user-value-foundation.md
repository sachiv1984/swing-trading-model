Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Superseded by: claude/cycles/2026-06-22__release-v6.1/closure_record.md — post-ship closure 2026-06-23
Release: v6.1
Cycle: 2026-06-22__release-v6.1
Last Updated: 2026-06-23

---

# Scope Document — v6.1 Governance Correctness, CI Quality & User Value Foundation

---

## Items in Scope

| S2-ID | EPIC | BLG ID | Description | Classification |
|-------|------|--------|-------------|----------------|
| S2-01 | EPIC-01 | BLG-GOV-132 | Release planning: Design Gate Required flag — patch release_planning_prompt.md to detect UI-facing scope and set design_gate_required=true | Firm |
| S2-02 | EPIC-01 | BLG-GOV-133 | Sprint planning: Design Gate hard gate at preflight — patch sprint_planning_prompt.md to halt and require design gate sign-off before sprint seals | Firm |
| S2-03 | EPIC-02 | BLG-QA-60 | Register morning-briefing.spec.js and screener-quality.spec.js in playwright.yml to ensure CI runs all Playwright tests | Firm |
| S2-04 | EPIC-03 | BLG-FE-76 | Portfolio sector heat-map visualization — SectorHeatMap.js component showing sector weight breakdown with concentration alerts | Firm |
| S2-05 | EPIC-01 | BLG-GOV-131 | Governance overhead ceiling metric and accountability mechanism — proposal document + sprint planning reporting | Firm |
| S2-06 | EPIC-03 | BLG-FE-78 | Trade gate proximity indicator on dashboard — badge/counter reading GET /portfolio/gate-metrics, indicating progress toward next trade gate | Firm |
| S2-07 | EPIC-02 | BLG-OPS-73 | Add PATCH /trades/{id}/costs to api_performance_baseline.md — register endpoint baseline after v6.0 patch shipping | Firm |
| S2-08 | EPIC-04 | BLG-FEAT-25 | Setup Quality Score — backend scoring engine + frontend display (PT-04): conditional on ≥20 closed trades | **Conditional** |

---

## Items Explicitly Deferred

| BLG ID | Description | Reason | Target |
|--------|-------------|--------|--------|
| BLG-GOV-134 | CI OpenAPI/baseline drift detection | Provisional-Target v6.1 but not in rebalance Now section; scope-lock rule prevents inclusion | v6.2 candidate |
| BLG-QA-62 | Playwright glob auto-registration | Provisional-Target v6.1 but not in rebalance Now table; follow-on to BLG-QA-60 | v6.2 candidate |
| BLG-FE-77 | Watchlist.js ESLint compliance | Provisional-Target v6.1 but not in rebalance Now table | v6.2 candidate |
| BLG-OPS-74 | Log morning briefing API cost | Provisional-Target v6.1 but not in rebalance Now table | Unscheduled |
| BLG-QA-61 | signals_scenarios.md review | v6.1 provisional but not in rebalance Now table | Before next signal sprint |
| SI-02 frontend | Setup Quality Score frontend integration | Gate condition identical to PT-04; assess if gate clears at sprint planning | v6.2+ |

---

## Supersession Note

*Blank at planning time. To be completed by Amendment Cycle Engine or subsequent release plan if scope changes.*
