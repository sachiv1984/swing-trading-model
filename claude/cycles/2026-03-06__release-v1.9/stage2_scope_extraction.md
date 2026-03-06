# Stage 2 — Scope Extraction

**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-03-06__release-v1.9
**Release:** v1.9
**Last Updated:** 2026-03-06

---

## Scope Decision Framework

v1.9 scope is drawn from three authoritative sources (in precedence order):

1. **Roadmap explicit assignment** — items the roadmap directly assigns to v1.9
2. **Backlog explicit target** — items in backlog.md with `Target release: v1.9`
3. **Backlog items promoted** — items in §11 cycle 2026-03-06__item-3.4 flagged for v1.9 slice determination

Items **not** in scope: v2.0 items (3.5 Alerts, 4.1b Tax Statement, 4.1c PDF, 4.3 Signal Exposure), v2.1+ items, deferred items. Scope document does not add, defer, or kill any roadmap initiative.

---

## Items In Scope

| S2-ID | Source | Backlog Ref | Description | Priority | Effort |
|-------|--------|------------|-------------|----------|--------|
| S2-01 | Roadmap 5.1 | — | Structured Trade Reflection Template | P2 | Low–Medium (1–2 days) |
| S2-02 | Roadmap BLG-FEAT-08 | BLG-FEAT-08 | Basic Compliance Metrics (pre-work gate for S2-01) | P2 | ~1 day |
| S2-03 | Roadmap 5.2 | — | Cohort Analysis | P2 | Low–Medium (1–2 days) |
| S2-04 | Roadmap 5.3 | — | Dashboard Homepage / Session Summary | P2 | Low–Medium (1–2 days) |
| S2-05 | Backlog §9 | BLG-RD-01 | Risk Dashboard: entity store fallback masks API errors | P2 | Small |
| S2-06 | Backlog §9 | BLG-RD-02 | Risk Dashboard: GracePeriodPanel empty vs error state | P3 | Small |
| S2-07 | Backlog §9 | BLG-RD-03 | Risk Dashboard: PositionRiskTable sort direction | P2 | Small |
| S2-08 | Backlog §9 | BLG-RD-04 | Risk Dashboard: Stop Price column absent | P2 | Small |
| S2-09 | Backlog §9 | BLG-RD-05 | Risk Dashboard: GRACE badge colour amber not blue | P3 | Small |
| S2-10 | Backlog §9 | BLG-RD-06 | Risk Dashboard: GBP value at risk absent from HeatGauge | P3 | Small |
| S2-11 | Backlog §9 | BLG-RD-07 | Risk Dashboard: Days in Grace column absent | P3 | Small |
| S2-12 | Backlog §9 | BLG-RD-08 | Risk Dashboard: Drawdown data source — spec alignment | P2 | Small |
| S2-13 | Backlog §9 | BLG-RD-09 | Risk Dashboard: ProspectiveHeatPanel threshold label absent | P3 | Small |
| S2-14 | Backlog §9 | BLG-RD-10 | Risk Dashboard: US entry prices in USD not GBP | P2 | Small–Medium |
| S2-15 | Backlog §9 | BLG-RD-11 | Risk Dashboard: current_stop in USD for US positions | P2 | Small–Medium |
| S2-16 | Backlog §10 / §11 | TEST-GAP-EPIC-01 / BLG-NEW-10 | Canonical Test Scenario Library + seeded test infrastructure | P1 | Medium |
| S2-17 | Backlog §11 | BLG-NEW-12 | Service Layer Test Coverage Standard + CI enforcement | P1 | Small–Medium |
| S2-18 | Backlog §11 | BLG-NEW-09 | R-Multiple Distribution Report | P2 | Low–Medium (1–2 days) |
| S2-19 | Backlog §11 | BLG-NEW-11 | Canonical Terms Glossary | P2 | Small |
| S2-20 | Backlog §8 | BLG-NEW-04 | AI-Assisted Workflow Governance Policy | P2 | ~0.5 day |

**Scope Decision (Spec Debt items):** The following P2 spec/documentation debt items are borderline for v1.9 inclusion. Given their age (open since 2026-02-21 per backlog §7) and the backlog's explicit recommendation for "priority upgrade review at v1.9 pre-alignment", the Head of Specs Team includes them in scope as a documentation-only EPIC:

| S2-ID | Backlog Ref | Description | Priority |
|-------|------------|-------------|----------|
| S2-21 | BLG-SPEC-D3 | Document GET /market/status endpoint | P2 |
| S2-22 | BLG-SPEC-G1 | Create settings_model.md | P2 |
| S2-23 | BLG-SPEC-G2 | Define Error Response Standard | P2 |
| S2-24 | BLG-SPEC-D1 | Update API Contracts README to v1.9.0 | P3 |
| S2-25 | BLG-SPEC-D4 | Document GET /positions/search/tags | P3 |
| S2-26 | BLG-SPEC-D8 | Add lifecycle header to System_status_report.md | P3 |
| S2-27 | BLG-SPEC-D9 | Fix broken cross-references to document_lifecycle_guide.md | P3 |
| S2-28 | BLG-SPEC-G3 | Register structured_logging_standards.md in Specs_Index.md | P3 |
| S2-29 | BLG-SPEC-G4 | Move ADR-002 to correct location | P3 |
| S2-30 | BLG-SPEC-G5 | Fix validation_system.md owner field | P3 |

**Rationale for S2-21–S2-30:** These are documentation corrections and spec gaps — not new features. They carry no strategy risk. D3 (P2) and G1+G2 (P2) are overdue. P3 items are small fixes (<30 min each). Grouping into a Documentation Hygiene EPIC makes sequencing clean and does not inflate feature scope.

---

## Items Explicitly Deferred

| Item | Reason | Target |
|------|--------|--------|
| 3.5 Alerts & Notifications | v2.0 gate_3 (QA planning) still pending | v2.0 |
| 4.1b Tax-Year P&L Statement | v2.0 scope | v2.0 |
| 4.1c Server-Side PDF Report | v2.0 scope | v2.0 |
| 4.3 Signal Exposure Enhancement | v2.0 scope (§13 gate cleared; awaiting v2.0 planning) | v2.0 |
| 4.2 Watchlists & Screening | Post v2.0 | v2.1+ |
| Chart Interactivity Enhancements | Post v2.0 | v2.1+ |
| BLG-TECH-05 Prometheus endpoint | v2.1 | v2.1+ |
| 3.1 Performance Analytics (v1.5) | Already shipped | — |
| BLG-FEAT-03 Slippage Tracking | Orphan — no roadmap home confirmed for v1.9 | TBD |

---

## Scope Summary

**Total scope items: 30** (S2-01 through S2-30)

Grouped by theme:
- **User Value features** (S2-01–S2-04): 4 items — trade reflection, compliance metrics, cohort analysis, dashboard homepage
- **Risk Dashboard Defect Resolution** (S2-05–S2-15): 11 items — BLG-RD-01 through BLG-RD-11
- **QA & Test Infrastructure** (S2-16–S2-17): 2 items — canonical test library, service coverage standard
- **Analytics** (S2-18): 1 item — R-multiple distribution
- **Documentation & Governance** (S2-19–S2-30): 12 items — glossary, AI policy, spec/doc debt

---

## Supersession Note

*(To be completed at post-ship closure)*
Superseded by: v1.9 ship — [ship date]
Changelog: docs/product/changelog.md#v1.9
Verification report: claude/cycles/2026-03-06__release-v1.9/verification_report.md
Cycle: 2026-03-06__release-v1.9
