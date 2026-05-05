**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v3.1
**Cycle:** 2026-04-29__release-v3.1
**Last Updated:** 2026-04-29

---

# Cycle Summary — v3.1 Arc 2 Start: Trade Plan Object & Pre-Trade Research Foundation

## Release Overview

| Field | Value |
|-------|-------|
| Release | v3.1 |
| Theme | Arc 2 Start — Trade Plan Object & Pre-Trade Research Foundation |
| Cycle ID | 2026-04-29__release-v3.1 |
| Published | 2026-04-29 |
| EPICs | 4 (EPIC-01 through EPIC-04) |
| Stories | 14 |
| Sprints | 2 |
| Capacity check | WARN (~18.75 days estimated vs ~10 days available) |

## Scope Summary

**Arc 2 delivery (v3.1 scope):**
- PT-01 Trade Plan Object — full (spec + backend + frontend)
- PT-02 Pre-Trade Research View — backend only (frontend deferred to v3.2 pending design gate)

**Arc 1 completion:**
- DS-04 Earnings Calendar Integration (deferred from v3.0)

**Backlog items:**
- BLG-FE-20 (P1 bug: UK ticker display + watchlist promotion) — Sprint 1 priority
- BLG-QA-10/11 (Screener quality documentation)
- BLG-SEC-03/04, BLG-GOV-17 (Security policies + governance docs)
- BLG-FEAT-19 (Monthly P&L summary)
- CF-01/CF-02 (Governance prompt patches — recurring deferred items)

**Deferred to v3.2:** PT-02 frontend, PT-03, PT-05; PT-04 (gate: 20+ trades)

## Key Decisions

1. PT-02 frontend deferred to v3.2 — design gate is a structural requirement; backend foundation delivered now
2. CF-01 and CF-02 converted to sprint stories (EPIC-04) — 2-cycle recurrence demands formal closure
3. BLG-FE-20 first in Sprint 1 (P1 priority) — blocks UK-market users from watchlist promotion

## Design Gate Requirement

Design gate (Phase 1.5) **must run** before sprint planning seals. Scope:
- Trade Plan creation form UI (ST-03) — new data entry surface
- Earnings Calendar display UI (ST-08) — new UI element on 3 existing pages

Bypass authority: Head of UX & Design + Product Owner (per `.claude_current_state.json` design_gate_bypass_authority).

## Capacity Phasing Guidance for Sprint Planning

**Sprint 1 (~9.0 days estimated):** EPIC-01 ST-01/ST-02 + EPIC-03 ST-06/ST-07/ST-09 + EPIC-04 ST-11/ST-12/ST-13/ST-14
**Sprint 2 (~9.75 days estimated):** EPIC-01 ST-03 + EPIC-02 ST-04/ST-05 + EPIC-03 ST-08/ST-10

Sprint Planning Engine should review capacity and consider deferring ST-10 (BLG-QA-10, M) or ST-05 (PT-02 backend, M) to v3.2 if capacity is tight. ST-06 (BLG-FE-20 P1 bug) must not be deferred.

## Risk Summary

| Risk | Priority | Disposition |
|------|----------|-------------|
| RISK-01: No Trade Plan spec exists | High | Resolved by ST-01 as Sprint 1 first story; within-sprint sequencing constraint |
| RISK-02: Design gate for Trade Plan/Earnings Calendar frontend | Medium | Standard Phase 1.5 design gate — must run before sprint planning seals |
| RISK-03: DS-04 Yahoo Finance data quality | Medium | Spec authoring (ST-07) validates data source; graceful null display if data unavailable |
| RISK-04: Governance prompt patches require §6 checklist | Low | commit-check skill enforces compliance |

## Next Steps

1. **Run design gate** (`run design-gate --cycle 2026-04-29__release-v3.1`) — covers Trade Plan frontend (ST-03) and Earnings Calendar frontend (ST-08)
2. **Run sprint planning** (`plan sprint --cycle 2026-04-29__release-v3.1`) — after design gate passes

## Artefact Checklist

| Artefact | Status |
|----------|--------|
| release_plan.md | ✅ Present |
| stage4_backlog_slice.md | ✅ Present |
| stage4_issue_manifest.json | ✅ Present |
| scope document | ✅ Present |
| decisions record | ✅ Present |
| run_manifest.md | ✅ Present |
| state.json | ✅ Present (will be updated to Published) |
| cycle_summary.md | ✅ This document |
| lessons_learnt.md | ✅ Present |
