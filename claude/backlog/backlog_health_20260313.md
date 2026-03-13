**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-13

# Backlog Health Report — 2026-03-13

Run ID: GROOM-20260313-01
Trigger: Post-ship closure confirmed (2026-03-06__release-v1.9 Sprint 2 — Closed_with_actions)

---

## Summary

```
Backlog Health Summary — 2026-03-13

Total items reviewed:             38
Complete — Archive:               27
Killed — Archive:                  0
Active — Keep:                    10
Orphans flagged (new):             0  (2 pre-existing orphan flags maintained)
Blocked — stale blocker flagged:   0
Spec debt items — resolved:       10 (all BLG-SPEC-* items; 0 remaining)
Spec debt items — still open:      0
Priority misalignments flagged:    0
Promotion candidates:              1 (BLG-OPS-01 — advisory)
Ambiguous items resolved:          0
```

---

## Items Archived (27)

| Item ID | Title | Shipped | Cycle | Story |
|---------|-------|---------|-------|-------|
| BLG-FEAT-08 | Basic Compliance Metrics | v1.9 Sprint 2 | 2026-03-06__release-v1.9 | ST-02 |
| BLG-NEW-09 | R-Multiple Distribution Report | v1.9 Sprint 2 | 2026-03-06__release-v1.9 | ST-05 |
| BLG-NEW-10 | Canonical Test Scenario Library (Phase 1+2) | v1.9 Sprint 1+2 | 2026-03-06__release-v1.9 | ST-11, ST-12 |
| TEST-GAP-EPIC-01 | Risk Dashboard scenario execution infrastructure | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-11 |
| BLG-NEW-11 | Canonical Terms Glossary | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-14 |
| BLG-NEW-12 | Service Layer Test Coverage Standard | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-13 |
| BLG-NEW-04 | AI-Assisted Workflow Governance Policy | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-15 |
| BLG-SPEC-D1 | API Contracts README version frozen | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-D3 | GET /market/status undocumented | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-16 |
| BLG-SPEC-D4 | GET /positions/search/tags undocumented | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-D8 | System_status_report.md missing header | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-D9 | Broken cross-references to lifecycle guide | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-G1 | settings_model.md missing | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-17 |
| BLG-SPEC-G2 | Error Response Standard not defined | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-18 |
| BLG-SPEC-G3 | structured_logging_standards.md not in Specs Index | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-G4 | ADR-002 in wrong location | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-G5 | validation_system.md owner field non-compliant | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-RD-01 | Entity store fallback masks API error states | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-08 |
| BLG-RD-02 | GracePeriodPanel empty vs error state | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-08 |
| BLG-RD-03 | PositionRiskTable sorted descending | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-04 | Stop Price column absent | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-05 | GRACE badge colour amber instead of blue | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-10 |
| BLG-RD-06 | GBP value at risk absent from HeatGauge | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-10 |
| BLG-RD-07 | Days in Grace column absent | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-08 | Drawdown data source (RESOLVED pre-sprint) | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-06 investigation |
| BLG-RD-09 | ProspectiveHeatPanel missing threshold label | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-10 | US entry prices in USD not GBP | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-07 |
| BLG-RD-11 | current_stop in USD for US positions | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-07 |

All archived entries appended to `claude/backlog/backlog_archive.md`.

---

## Active Items (10)

| Item ID | Title | Priority | Target | Notes |
|---------|-------|----------|--------|-------|
| BLG-OPS-01 | Provision development environment | P1 | v1.10 | **Promotion candidate** — see below |
| BLG-TECH-06 | Fix CohortAnalysis client-side computation | P2 | v1.10 | DEV-EPIC02-ST03-01 resolution |
| BLG-TECH-05 | Prometheus metrics endpoint | P3 | v2.1+ | Deferred until multi-user |
| BLG-FEAT-03 | Slippage Tracking | P2 | None | Orphan — existing flag maintained |
| TEST-GAP-EPIC-06 | v1.7 scenario gaps (analytics/portfolio/trades) | — | None | Orphan — existing flag maintained; no BLG-ID |
| BLG-FE-01 | Dashboard full-page error + Retry overlay | P3 | v1.10 | DEV-EPIC03-ST05-01 resolution |
| BLG-API-01 | Backend API integration tests (FastAPI TestClient) | P2 | v1.10 | — |
| TEST-GAP-EPIC-01-v1.9 | Execute v1.9 compliance metrics + trade reflection scenarios | P2 | v1.10 | 11 scenarios; BLG-OPS-01 enables live testing |
| TEST-GAP-EPIC-02-v1.9 | Execute v1.9 cohort + R-multiple distribution scenarios | P2 | v1.10 | 8 scenarios; note DEV-EPIC02-ST03-01 caveat |
| TEST-GAP-EPIC-03-v1.9 | Execute v1.9 dashboard homepage scenarios | P2 | v1.10 | 10 scenarios; SC-DH-07 blocked on BLG-FE-01 |

---

## Promotion Candidates

| Item ID | Title | Priority | Why Promote | Target Release | Pre-work Status |
|---------|-------|----------|-------------|----------------|-----------------|
| BLG-OPS-01 | Provision development environment | P1 | Prerequisite for live-app QA before v1.10 sprint 1 begins. Without it, the three post-merge hotfix PRs from v1.9 Sprint 2 will recur. Governance gap: DoQ sign-off rule requires testing a live app, but no non-production environment exists. | v1.10 | None — infrastructure decision only; Product Owner must approve environment provisioning |

Note: This list is advisory only. No items are added to the roadmap by this engine. The Product Owner decides which (if any) candidates to advance, and the Roadmap Rebalance Engine executes any additions.

---

## Priority Alignment Notes

No misalignments found. All active items are either:
- Targeted at v1.10 (consistent with next planned release)
- Targeted at v2.1+ (consistent with roadmap deferral)
- Orphaned with no target release (flagged separately)

---

## Orphans Flagged

| Item ID | Title | Last activity | Flag status |
|---------|-------|--------------|-------------|
| BLG-FEAT-03 | Slippage Tracking | None recorded — pre-governance era item | Existing flag maintained; no new flag added |
| TEST-GAP-EPIC-06 | v1.7 scenario coverage gaps | 2026-03-02__release-v1.7 | Existing orphan notice maintained; no BLG-ID assigned; v1.9 delivered analytics domain items without executing this gap — stale but not actionable without Product Owner decision |

**Product Owner action required:** Both orphans should be explicitly retained, reprioritised, or killed at next Roadmap Rebalance. TEST-GAP-EPIC-06 is now 2 cycles stale (v1.7 → v1.9 passed without action).

---

## Blocked Items — Stale Blockers

None identified.

---

## Spec Debt Status

| Item ID | Spec | Status | Action taken |
|---------|------|--------|-------------|
| BLG-SPEC-D1 | api_contracts/README.md | ✅ Resolved (v1.9 ST-19) | Archived |
| BLG-SPEC-D3 | market_endpoints.md | ✅ Resolved (v1.9 ST-16) | Archived |
| BLG-SPEC-D4 | position_endpoints.md | ✅ Resolved (v1.9 ST-19) | Archived |
| BLG-SPEC-D8 | System_status_report.md | ✅ Resolved (v1.9 ST-19) | Archived |
| BLG-SPEC-D9 | process_index.md + Specs_Index.md | ✅ Resolved (v1.9 ST-19) | Archived |
| BLG-SPEC-G1 | settings_model.md | ✅ Resolved (v1.9 ST-17) | Archived |
| BLG-SPEC-G2 | conventions.md §13 | ✅ Resolved (v1.9 ST-18) | Archived |
| BLG-SPEC-G3 | Specs_Index.md §3.5b | ✅ Resolved (v1.9 ST-19) | Archived |
| BLG-SPEC-G4 | docs/product/decisions/ | ✅ Resolved (v1.9 ST-19) | Archived |
| BLG-SPEC-G5 | validation_system.md | ✅ Resolved (v1.9 ST-19) | Archived |

No open spec debt items remaining.

---

## Items Requiring Product Owner Decision

1. **TEST-GAP-EPIC-06** — 2 cycles stale (v1.7 era). v1.9 shipped analytics/portfolio/trades domain features without executing these scenarios. Product Owner should decide: retain (assign BLG-ID and target release) or kill (scenario window has passed). Recommend kill if v1.9 features did not regress the relevant endpoints.

2. **BLG-FEAT-03** (Slippage Tracking) — orphaned with no roadmap home. Product Owner should decide: retain (assign to a release) or kill.

3. **BLG-OPS-01 promotion** — advisory: consider pulling this to active v1.10 planning as a pre-sprint prerequisite (see Promotion Candidates above).
