**Owner:** PMO Lead
**Class:** Supporting Document (Class 2) — Living Reference
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-06
**Source:** BLG-GOV-11 (v3.2 ST-17, 3rd consecutive deferral — mandatory)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Cycle Artefact Inventory and Lifecycle Model

**Purpose:** Consolidated inventory of document types across all cycle directories (`claude/cycles/`). Documents are categorised by lifecycle type (point-in-time vs. living), maintenance gaps are identified, and the artefact lifecycle model is stated.

**Cross-Reference:** OPERATIONAL_GUIDE §13 (Artefact Register) lists all canonical artefact types with class and owner. This document provides the lifecycle dimension and a per-type maintenance audit.

---

## 1. Artefact Lifecycle Model

All artefacts fall into one of three lifecycle categories:

| Category | Definition | Examples |
|----------|-----------|---------|
| **Point-in-time (PIT)** | Created for a specific cycle event; never modified after sealing. Accuracy is fixed at creation time. | sprint_backlog.md, run_manifest.md, closure_record.md, verification_report.md, sprint_goal.md |
| **Living Reference** | Maintained continuously. Must be updated when the domain they describe changes. Failure to update creates drift. | backlog.md, current_roadmap.md, System_status_report.md, component_inventory.md (this cycle), credential_policy.md (this cycle) |
| **Operational State** | Machine-readable files used by governance engines. Updated programmatically; not human-maintained manually. | execution_state.json, state.json, closure_state.json, .claude_current_state.json |

---

## 2. Artefact Type Inventory by Lifecycle

### 2.1 Point-in-Time Artefacts

Created once per cycle (or sub-phase); sealed on completion. No maintenance required or expected.

| Document Type | Canonical Path Pattern | Class | Notes |
|---------------|----------------------|-------|-------|
| Cycle Summary | `claude/cycles/<id>/cycle_summary.md` | 3 | Created at rebalance or release planning close |
| Lessons Learnt (cycle/rebalance) | `claude/cycles/<id>/lessons_learnt.md` | 3 | Created at phase end |
| Lessons Learnt (closure) | `claude/cycles/<id>/lessons_learnt_closure.md` | 3 | Created at post-ship closure |
| Lessons Learnt (execution) | `claude/cycles/<id>/lessons_learnt_cycle.md` | 3 | Created at sprint close |
| Sprint Goal | `claude/cycles/<id>/sprint_goal.md` | 4 | Sealed at sprint planning |
| Sprint Backlog | `claude/cycles/<id>/sprint_backlog.md` | 4 | Sealed at sprint planning |
| Sprint Capacity | `claude/cycles/<id>/sprint_capacity.md` | 4 | Sealed at sprint planning |
| Sprint Planning Notes | `claude/cycles/<id>/sprint_planning_notes.md` | 4 | Created at sprint planning |
| Sprint Close Summary | `claude/cycles/<id>/sprint_close.md` | 3 | Created at sprint close |
| Release Plan | `claude/cycles/<id>/release_plan.md` | 4 | Sealed on publish |
| Stage Outputs 1–5 | `claude/cycles/<id>/stage*.md` | 3 | Created at respective phases |
| Stage 4 Backlog Slice | `claude/cycles/<id>/stage4_backlog_slice.md` | 3 | Sealed at release planning |
| Run Manifest | `claude/cycles/<id>/run_manifest.md` | 3 | Created at release planning |
| Design Gate Record | `claude/cycles/<id>/design_gate.md` | 4 | Created at design gate |
| QA Evidence Log | `claude/cycles/<id>/qa_evidence_EPIC-xx.md` | 4 | Created at sprint execution |
| Delegation Log | `claude/cycles/<id>/delegation_log.md` | 4 | Created at sprint execution |
| Verification Report | `claude/cycles/<id>/verification_report.md` | 3 | Created at delivery verification |
| Closure Record | `claude/cycles/<id>/closure_record.md` | 3 | Created at post-ship |
| Audit Report | `claude/cycles/<id>/audit_report_AUD-<date>.md` | 3 | Created at audit |
| Amendment Manifest | `claude/cycles/<id>/amendments/<id>/` | 3 | Created at amendment |
| Meta-Review Record | `claude/cycles/<id>/meta_review.md` | 3 | Created at meta-review |
| Backlog Transaction | `claude/cycles/<id>/backlog_txn.json` | — | Created at release planning |
| Roadmap Transaction | `claude/cycles/<id>/roadmap_txn.json` | — | Created at rebalance |
| Backlog Health Report | `claude/backlog/backlog_health_<date>.md` | 4 | Created at 1M grooming |
| Roadmap Manage Log | `claude/roadmap/manage_roadmap_log_<date>.md` | 4 | Created at 1M |
| Ideas Window Summary | `claude/ideas/window_summary_<IW-id>.md` | 4 | Created per ideas window |

### 2.2 Living Reference Artefacts

Must be maintained when the domain they describe changes.

| Document | Path | Owner | Update Trigger |
|----------|------|-------|---------------|
| Current Roadmap | `claude/roadmap/current_roadmap.md` | Product Owner | Roadmap rebalance |
| Backlog | `claude/backlog/backlog.md` | Product Owner | Each cycle + 1M |
| Backlog Archive | `claude/backlog/backlog_archive.md` | Product Owner | 1M archiving |
| Initiative Register | `claude/roadmap/initiative_register.md` | Product Owner | Roadmap rebalance |
| Decision Log | `claude/roadmap/decision_log.md` | PMO Lead | Each decision event |
| Velocity Metrics | `claude/cycles/velocity_metrics.md` | PMO Lead | Post-ship closure |
| System Status Report | `docs/System_status_report.md` | Director of Quality | Sprint close + post-ship |
| OPERATIONAL_GUIDE | `claude/system/OPERATIONAL_GUIDE.md` | Head of Specs Team | Any prompt/process change |
| Prompt Change Log | `claude/system/prompt_change_log.md` | Head of Specs Team | Any prompt change |
| Team Charter | `claude/charter/team_charter.md` | Head of Specs Team | Governance changes only |
| Document Lifecycle Guide | `claude/charter/document_lifecycle_guide.md` | Head of Specs Team | Governance changes only |
| Strategy Rules | `claude/strategy/strategy_rules.md` | Strategy Rules Owner | Strategy changes only |
| Rejected-but-Strong Register | `claude/ideas/rejected_but_strong.md` | PMO Lead | Per ideas intake |
| **Component Inventory** | `docs/frontend/component_inventory.md` | Frontend Specs Owner | Any Arc 2 component add/change |
| **Design System** | `docs/frontend/design_system.md` | Frontend Specs Owner | Any design token change |
| **Credential Policy** | `docs/operations/credential_policy.md` | Cybersecurity & Trust Lead | Any credential change |
| **External API Risk Register** | `docs/operations/external_api_risk_register.md` | PMO Lead | New/changed API dependency |
| **Cycle Artefact Inventory** | `docs/operations/cycle_artefact_inventory.md` | PMO Lead | New artefact type added |

Items in **bold** are new living references created in v3.2 (ST-13/14/15/16/17).

### 2.3 Operational State Files

Machine-readable; updated programmatically. Do not edit manually unless correcting a governance error.

| File | Path | Owner | Notes |
|------|------|-------|-------|
| Global State Pointer | `.claude_current_state.json` | PMO Lead | Root of all cycle state |
| Cycle State | `claude/cycles/<id>/state.json` | PMO Lead | Release planning output |
| Execution State | `claude/cycles/<id>/execution_state.json` | PMO Lead | Sprint execution tracker |
| Closure State | `claude/cycles/<id>/closure_state.json` | PMO Lead | Post-ship |
| Sprint Backlog Index | `claude/cycles/<id>/sprint_backlog_index.json` | PMO Lead | Sprint planning |
| Ideas Window State | `claude/ideas/ideas_window.json` | PMO Lead | Ideas intake |
| Backlog Lock | `claude/backlog/.lock` | PMO Lead | Do not delete manually |

---

## 3. Closed Cycle Inventory Summary

Closed cycles as at 2026-05-06 (source: `claude/cycles/` directory):

| Cycle | Type | Status |
|-------|------|--------|
| 2026-03-01__item-3.2 | Roadmap item | Closed |
| 2026-03-02__release-v1.7 | Release | Closed |
| 2026-03-04__item-3.4 | Roadmap item | Closed |
| 2026-03-04__release-v1.8 | Release | Closed |
| 2026-03-06__item-3.4 | Roadmap item | Closed |
| 2026-03-06__release-v1.9 | Release | Closed |
| 2026-03-15__item-5.3 | Roadmap item | Closed |
| 2026-03-15__release-v1.10 | Release | Closed |
| 2026-03-17__item-v1.10 | Roadmap item | Closed |
| 2026-03-17__release-v2.0 | Release | Closed |
| 2026-03-18__item-4.3 | Roadmap item | Closed |
| 2026-03-18__release-v2.1 | Release | Closed |
| 2026-03-21__item-3.5 | Roadmap item | Closed |
| 2026-03-21__release-v2.2 | Release | Closed |
| 2026-03-24__release-v2.3 | Release | Closed |
| 2026-03-24__scheduled | Scheduled rebalance | Closed |
| 2026-03-31__release-v2.4 | Release | Closed |
| 2026-03-31__scheduled | Scheduled rebalance | Closed |
| 2026-04-05__release-v2.5 | Release | Closed |
| 2026-04-05__scheduled | Scheduled rebalance | Closed |
| 2026-04-11__release-v2.6 | Release | Closed |
| 2026-04-13__release-v2.7 | Release | Closed |
| 2026-04-17__release-v2.8 | Release | Closed |
| 2026-04-17__scheduled | Scheduled rebalance | Closed |
| 2026-04-21__scheduled | Scheduled rebalance | Closed |
| 2026-04-22__release-v2.9 | Release | Closed |
| 2026-04-24__scheduled | Scheduled rebalance | Closed |
| 2026-04-25__release-v3.0 | Release | Closed |
| 2026-04-29__release-v3.1 | Release | Closed |
| 2026-05-05__scheduled | Scheduled rebalance | Closed |
| 2026-05-05__release-v3.2 | Release | **Active** |

Total closed cycles: 30. Active cycle: 1.

---

## 4. Maintenance Gaps Identified

| Gap | Location | Severity | Resolution |
|-----|----------|----------|-----------|
| No artefact lifecycle model documented | System-wide (pre-v3.2) | Medium | Resolved — this document (ST-17) |
| No component inventory or design system | `docs/frontend/` (pre-v3.2) | Medium | Resolved — ST-13, ST-14 (v3.2) |
| No credential policy | `docs/operations/` (pre-v3.2) | Medium | Resolved — ST-15 (v3.2) |
| No external API risk register | `docs/operations/` (pre-v3.2) | Medium | Resolved — ST-16 (v3.2) |
| Early cycle directories (v1.7–v2.1) may lack document lifecycle headers | `claude/cycles/2026-03-*/` | Low | Not blocking — point-in-time documents; no maintenance required; follow-up filed as BLG-GOV-11b if desired |

**All medium gaps resolved in v3.2. No outstanding maintenance gaps above Low severity.**

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-06 | Initial artefact inventory. v3.2 ST-17 (BLG-GOV-11, 3rd consecutive deferral). 30 closed cycles inventoried; lifecycle model stated; 4 medium gaps resolved in this cycle. |
