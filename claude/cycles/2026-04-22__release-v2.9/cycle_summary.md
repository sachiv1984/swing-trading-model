Owner: Release Planning Engine
Class: Planning Document (Class 4)
Status: Active
Release: v2.9
Cycle: 2026-04-22__release-v2.9
Last Updated: 2026-04-22

---

# Cycle Summary — v2.9 Arc 1 Foundation

## Release Overview

| Field | Value |
|-------|-------|
| Release | v2.9 |
| Cycle ID | 2026-04-22__release-v2.9 |
| Theme | Arc 1 Foundation — Stock Discovery & Screening Spec & Infrastructure |
| Plan published | 2026-04-22 |
| Sprint count | 2 |
| Story count | 15 |
| EPIC count | 4 |

## Scope Summary

| EPIC | Title | Sprint | Stories | Effort |
|------|-------|--------|---------|--------|
| EPIC-01 | Arc 1 Specification Foundation | 1 | ST-01–04 | 4S |
| EPIC-02 | Arc 1 Implementation Start | 2 | ST-05–07 | 1S + 1M + 1S |
| EPIC-03 | Arc 1 Governance & QA Foundation | 1 | ST-08–10 | 1S + 1M + 1M |
| EPIC-04 | Governance Debt & Quick Wins | 1+2 | ST-11–15 | 3S + 1S + 1S |
| **Total** | | | **15** | **~14.25 days** |

## Capacity Check

- Velocity basis: v2.8 = 1.00; 6-cycle rolling avg = 0.99
- Total estimated effort: 14.25 days (normalised)
- Status: **PASS** — within historical range

## Key Sequencing Constraints

1. **ST-02 before ST-06** — BLG-SPEC-22 (Alpaca API contract) must be complete before DS-05 implementation begins. Hard gate: no ad-hoc endpoint selection permitted.
2. **ST-08 before ST-07** — BLG-GOV-16 (§13 review for DS-06) must be complete and signed off before Alpaca News Panel implementation.
3. **EPIC-01 + EPIC-03 before EPIC-02** — All specification and governance prerequisites in Sprint 1; implementation in Sprint 2.

## Pre-Sprint Planning Required Decisions

| ID | Decision Required | Owner | Due | Risk if Missed |
|----|-------------------|-------|-----|----------------|
| RISK-01 | Confirm BLG-SPEC-22 (ST-02) complete before ST-06 sprint start | Head of Specs Team + Backend Owner | Before Sprint 2 kickoff | DS-05 implementation cannot begin; Sprint 2 EPIC-02 blocked |

## Outstanding Actions

| ID | Description | Owner | Priority |
|----|-------------|-------|----------|
| OA-v29-01 | sprint_planning_prompt.md v2.5: change log shows no entry for v2.3→v2.5 transition — advisory only, does not halt | Head of Specs Team | P3 |
| OA-v29-02 | BLG-GOV-08 retirement review — recommend retire at next `groom backlog` run (5 consecutive deferrals) | Product Owner | P3 |
| OA-v29-03 | CF-1/CF-2 from v2.8 closure (DoQ counter-sign for reclassified frontend EPICs; DoQ EPIC consolidation block) — addressed by ST-11 (BLG-GOV-14) in this cycle | Head of Specs Team | P2 |

## Carry-Forward Items

| ID | Description | Source | Resolution in v2.9 |
|----|-------------|--------|-------------------|
| CF-1 | DoQ counter-sign requirement for reclassified `delegated_frontend` stories with frontend-visible changes | v2.8 closure | ST-11 (BLG-GOV-14) §3.2.A patch |
| CF-2 | DoQ EPIC consolidation block requirement for domain-gated EPICs | v2.8 closure | ST-11 (BLG-GOV-14) §3.2 patch |

## Deferred Items

| ID | Item | Reason | Target |
|----|------|--------|--------|
| DS-01 | Strategy-Rules Screener Engine | BLG-SPEC-21/23 specs must exist first; those specs are v2.9 deliverables | v3.0 |
| DS-02 | Screener Results Page | Depends on DS-01; DS-01 deferred | v3.0 |
| DS-04 | Earnings Calendar Integration | M effort; no blocking dependency on v2.9 items | v3.0 |
| DS-07 | Watchlist Promotion Flow | Depends on DS-02 | v3.0 |
| BLG-GOV-08 | Engine prompt compression | 5 consecutive deferrals; L effort; P3; retirement recommended | Retire |
| BLG-GOV-11 | Cycle artefact inventory | Lower urgency | v2.9+ |
| BLG-FEAT-13 | Correlation Dashboard | Lower urgency | v3.0+ |
| BLG-FEAT-18 | Portfolio Stress Test View | Lower urgency | v3.0+ |
| BLG-FEAT-19 | Entry Zone Proximity Alert | Lower urgency | v3.0+ |
| BLG-FE-16 | Trade History CSV Export | Lower urgency | v2.9+ |
| BLG-OPS-12 | DB backup automation | Lower urgency | v3.0+ |
| BLG-AI-02 | AI model contract | Lower urgency | v2.9+ |
| BLG-SPEC-20 | Data model v2.0 | Lower urgency | v3.0+ |

## Artefacts

| Artefact | Path |
|----------|------|
| Run manifest | claude/cycles/2026-04-22__release-v2.9/run_manifest.md |
| Cycle state | claude/cycles/2026-04-22__release-v2.9/state.json |
| Release plan | claude/cycles/2026-04-22__release-v2.9/release_plan.md |
| Backlog slice | claude/cycles/2026-04-22__release-v2.9/stage4_backlog_slice.md |
| Issue manifest | claude/cycles/2026-04-22__release-v2.9/stage4_issue_manifest.json |
| Scope doc | docs/product/scope/scope--2026-04-22__release-v2.9-arc-1-foundation-stock-discovery-screening-spec.md |
| Decisions record | docs/product/decisions/decisions--2026-04-22__release-v2.9.md |
| Backlog txn | claude/cycles/2026-04-22__release-v2.9/backlog_txn.json |
| Roadmap txn | claude/cycles/2026-04-22__release-v2.9/roadmap_txn.json |
