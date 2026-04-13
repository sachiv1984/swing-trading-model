Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v2.6
Cycle: 2026-04-11__release-v2.6
Last Updated: 2026-04-13
Superseded by: v2.6 ship — 2026-04-13
Changelog: docs/product/changelog.md#v2.6
Verification report: claude/cycles/2026-04-11__release-v2.6/verification_report.md
Cycle: 2026-04-11__release-v2.6

---

## Release Scope — v2.6 Backend Integration Completion, Test Automation & Governance Hardening

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Backend Integration Completion — migrate Reports Performance tab to FastAPI; wire Signals page dismissal/position creation to FastAPI; replace Base44 cash balance on Signals page with GET /cash/summary |
| S2-02 | EPIC-02 | Test Automation & CI Hardening — fix 4 pytest collection errors; add CI test runner workflow; fee drag Playwright spec (SC-FEE-01–04); fee drag backend pytest unit tests (SC-FEE-05/06) |
| S2-03 | EPIC-03 | Frontend UX Polish — StatsCard tooltip prop; Trade History StatsCard bar layout; Trade History column header styling; flexible column sorting across Trade History table |
| S2-04 | EPIC-04 | Governance & Spec Debt — execution_prompt.md STEP 5.1 unpushed-commit check (v2.5 CF-1); §6 edit reminders for design_gate, amendment_cycle, roadmap prompt engines (v2.5 CF-2); decision_log.md structural hard gate (BLG-GOV-15); frontend performance budget spec (BLG-FE-09) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-TECH-05 — Prometheus metrics endpoint | P3 — multi-user prerequisite; no current operational need | v2.7 or when multi-user |
| BLG-QA-11 — System Status Playwright spec | P3 — lower priority vs. active test automation gaps | v2.7 |
| BLG-GOV-08 — Engine prompt compression | P3 — L effort; would dominate sprint capacity | v2.7 |
| BLG-GOV-11 — Cycle artefact inventory | P3 — large scope; deprioritised vs. P1/P2 items | v2.7 |
| BLG-GOV-14 — Governance Health Score | P3 — complex formula definition; deprioritised | v2.7 |
| BLG-SPEC-D17 — Spec Dependency Map | P3 — deprioritised vs. P1/P2 delivery items | v2.7 |
| CF-3 — execution_state.json test_scenarios schema | Low priority carry-forward | v2.7 |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-04-11__release-v2.6
