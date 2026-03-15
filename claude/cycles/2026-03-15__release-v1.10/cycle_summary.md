**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v1.10
**Cycle:** 2026-03-15__release-v1.10
**Last Updated:** 2026-03-15

---

# Cycle Summary — v1.10 Operations & Quality Foundation

**Release:** v1.10 — Operations & Quality Foundation
**Cycle:** 2026-03-15__release-v1.10
**Plan published:** 2026-03-15
**Mode:** standard

---

## Release Theme

v1.10 is the Operations & Quality Foundation release. Its primary mandate is to close the structural governance gap identified in LL-01 (cycle 2026-03-15__item-5.3): no staging/development environment exists, forcing all QA to run against production. BLG-OPS-01 is the P1 prerequisite item. The secondary items (BLG-TECH-06, BLG-API-01, BLG-QA-01) deliver targeted quality improvements that are well-positioned to run alongside or immediately after BLG-OPS-01.

---

## Scope Summary

| S2-ID | Epic | Item | Priority |
|-------|------|------|----------|
| S2-01 | EPIC-01 | BLG-OPS-01 — Staging/dev environment | P1 |
| S2-02 | EPIC-02 | BLG-TECH-06 — Fix CohortAnalysis.js | P2 |
| S2-03 | EPIC-03 | BLG-API-01 — Backend integration tests | P2 |
| S2-04 | EPIC-03 | BLG-QA-01 — v1.7 QA scenario gaps | P2 |

**Stories:** 7 (ST-01 through ST-07)
**Total mid effort:** ~48 hrs / 6 days
**Escalations:** 0 open
**Capacity check:** WARN (no capacity specified; feasible under full-time; phasing recommendation provided)

---

## Key Planning Decisions

1. **BLG-OPS-01 is a Prerequisite, not a peer feature** — LL-01 mandate. If sprint capacity forces phasing, EPIC-01 enters Phase 1. This is non-negotiable.
2. **TEST-GAP-EPIC-06 assigned BLG-QA-01** — Item had been in backlog 3 cycles without story assignment (STEP 1.1 advisory). Promoted to ST-07 in this release. Orphan resolved.
3. **EPIC-02 (CohortAnalysis) is independent** — can be parallelised with EPIC-01 or EPIC-03.
4. **RISK-01 (staging scope):** Infrastructure & Operations Owner must select and document the hosting approach before ST-01 implementation begins. Constrain to simplest viable approach.

---

## Next Steps

1. **`run design-gate --cycle 2026-03-15__release-v1.10`** — Design gate required before sprint planning. Classify all stories (design required / pre-approved / not applicable). Expected: most stories are N/A (infrastructure, refactoring) except possibly ST-01 if UI/UX elements are involved (staging dashboard?).
2. **`plan sprint --cycle 2026-03-15__release-v1.10`** — Sprint planning after design gate passes.
3. **Infrastructure & Operations Owner decision on staging approach** — Required before ST-01. This is the key pre-sprint planning input needed.
4. **BLG-QA-01 backlog update** — Update backlog.md to replace TEST-GAP-EPIC-06 orphan notice with BLG-QA-01 ID at sprint planning.

---

## Phasing Guidance (if sprint planning adopts two sprints)

Per STEP 4.5 phasing recommendation:

- **Sprint 1:** EPIC-01 (ST-01, ST-02, ST-03) — ~20 hrs — deliver staging environment first
- **Sprint 2:** EPIC-02 + EPIC-03 (ST-04, ST-05, ST-06, ST-07) — ~28 hrs — quality improvements on staging foundation

If a single sprint is feasible (full-time availability), all 7 stories may be planned together.

---

## Artefact Paths

| Artefact | Path |
|----------|------|
| Release plan | claude/cycles/2026-03-15__release-v1.10/release_plan.md |
| Backlog slice | claude/cycles/2026-03-15__release-v1.10/stage4_backlog_slice.md |
| Scope document | docs/product/scope/scope--2026-03-15__release-v1.10-operations-quality.md |
| Decisions record | docs/product/decisions/decisions--2026-03-15__release-v1.10.md |
| Issue manifest | claude/cycles/2026-03-15__release-v1.10/stage4_issue_manifest.json |
| State | claude/cycles/2026-03-15__release-v1.10/state.json |
