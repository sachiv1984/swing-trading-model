**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v3.5
**Cycle:** 2026-05-15__release-v3.5
**Last Updated:** 2026-05-15

---

# Cycle Summary — v3.5 Arc 3 Completion + Arc 4 Foundation

## Release Overview

| Field | Value |
|-------|-------|
| Release | v3.5 |
| Cycle | 2026-05-15__release-v3.5 |
| Theme | Arc 3: Alpaca Paper Trading (IT-06) + Arc 4 Foundation: Plan vs Reality (PO-01) |
| Stories | 13 |
| EPICs | 4 |
| Sprints | 2 |
| Status | Validated — publish eligible |
| Capacity check | WARN — see phasing recommendation |

## Sprint Allocation

| Sprint | EPICs | Stories | Estimated effort | Notes |
|--------|-------|---------|------------------|-------|
| Sprint 1 | EPIC-04 (governance), EPIC-03 (spec/QA debt), EPIC-01 (ST-01 §13 review only) | ST-07–13, ST-01 | ~4–6 days | Front-load governance; §13 review gates Sprint 2 EPIC-01 implementation |
| Sprint 2 | EPIC-01 (ST-02/03, conditional), EPIC-02 (ST-04–06) | ST-04–06, ST-02–03 (conditional) | ~8–11 days | Arc 4 foundation; IT-06 implementation if §13 PASS; PO-01 front to back |

## Story Count by EPIC

| EPIC | Theme | Stories | Sprint |
|------|-------|---------|--------|
| EPIC-01 | Arc 3 Completion — IT-06 Alpaca Paper Trading | ST-01, ST-02, ST-03 | Sprint 1 (ST-01) + Sprint 2 (ST-02/03, conditional) |
| EPIC-02 | Arc 4 Foundation — PO-01 Plan vs Reality | ST-04, ST-05, ST-06 | Sprint 2 |
| EPIC-03 | Spec & QA Debt | ST-07, ST-08, ST-09, ST-10 | Sprint 1 |
| EPIC-04 | Governance Patches | ST-11, ST-12, ST-13 | Sprint 1 |

## Key Risks

| RISK-ID | Priority | Status | Resolution path |
|---------|----------|--------|-----------------|
| RISK-01 | High | Open | ST-01 §13 review Sprint 1 — gates IT-06 implementation |
| RISK-02 | Medium | Open | PO-01 frontend (ST-06) phaseable to v3.6 if capacity exceeded |
| RISK-03 | Low | Open | PO-01 graceful degradation when no trade plan data exists |

## Deferred Items

| Item | Target |
|------|--------|
| IT-06 implementation (if §13 FAIL) | Post-§13 decision — future release |
| PT-04 Setup Quality Score | Arc 4 later cycle (gate: 20+ closed trades) |
| PO-01 frontend (if capacity exceeded) | v3.6 |
| BLG-FE-26 Research page UX review | Arc 4/5 design gate |
| PO-02 through PO-05 | Arc 4 later cycles |

## Recommended Merge Order

Suggested EPIC merge order: **EPIC-04 → EPIC-03 → EPIC-01 → EPIC-02**

- EPIC-04 first: governance patches ship before any execution EPIC — ensures improved prompts are in place before sprint execution begins
- EPIC-03 second: spec corrections are documentation-only, no conflicts
- EPIC-01 third: IT-06 (if §13 PASS) — backend then frontend; US-market position paths
- EPIC-02 last: PO-01 introduces new data model (plan_vs_reality field) — higher conflict risk; merge last

## Design Gate Required

**Design Gate (Phase 1.5) must be run before sprint planning seals.** Required outputs:

1. **IT-06 UX spec** (if ST-01 §13 PASS) — `docs/ux_specs/paper-trading/ux_spec.md` — Owner: Head of UX & Design
2. **PO-01 Plan vs Reality UX spec** — `docs/ux_specs/plan-vs-reality/ux_spec.md` — Owner: Head of UX & Design

Sprint planning must not seal until both UX specs are available (or IT-06 is descoped via §13 FAIL).

---

## Pre-sprint Planning Required Decisions

The following High-priority decisions must be resolved before sprint planning seals (i.e., before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-01] §13 compliance review for IT-06 Alpaca Paper Trading — ST-01 must complete and produce a written PASS or FAIL determination before EPIC-01 ST-02/03 can be scheduled. Required: written §13 determination document at `docs/product/decisions/decisions--2026-05-15__release-v3.5--IT-06-section13-review.md`. Owner: Strategy Rules & System Intent Owner. If FAIL: EPIC-01 reduces to ST-01 only; backup capacity absorbed by EPIC-02.

---

## Planning Artefacts

| Artefact | Path | Status |
|----------|------|--------|
| Release Plan | claude/cycles/2026-05-15__release-v3.5/release_plan.md | ✅ Present |
| Backlog Slice | claude/cycles/2026-05-15__release-v3.5/stage4_backlog_slice.md | ✅ Present |
| Issue Manifest | claude/cycles/2026-05-15__release-v3.5/stage4_issue_manifest.json | ✅ Present |
| Scope Document | docs/product/scope/scope--2026-05-15__release-v3.5-arc-3-completion-arc-4-foundation.md | ✅ Present |
| Decisions Record | docs/product/decisions/decisions--2026-05-15__release-v3.5.md | ✅ Present |
| State | claude/cycles/2026-05-15__release-v3.5/state.json | ✅ Present |
