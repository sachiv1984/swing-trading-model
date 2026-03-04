**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-04
**Cycle:** 2026-03-04__release-v1.8

---

# Cycle Summary — Release Planning v1.8

## Release: v1.8 — Risk Dashboard

**Cycle ID:** 2026-03-04__release-v1.8
**Status:** Validated (Publish Gate passed)
**Planned date:** 2026-03-04
**Engine:** Release Planning Engine v2.7

---

## What Was Planned

v1.8 is the Risk Dashboard release. The primary roadmap item (§3.4) is a dedicated risk dashboard page consolidating portfolio heat, drawdown, grace period status, and per-position risk visibility. This cycle also incorporates high-priority backlog items from the IW-20260304-01 pool (DL-005) spanning CI quality gates, critical spec debt, and governance documentation.

---

## Sprint Structure

| EPIC | Title | Tasks | Effort | Priority |
|------|-------|-------|--------|----------|
| EPIC-01 | Risk Dashboard Page | ST-01–ST-04 | 3–4 days | P0 |
| EPIC-02 | CI Quality Gates | ST-05–ST-08 | ~2.5 days | P1 |
| EPIC-03 | API & Spec Debt | ST-09 (gated), ST-10 | ~1.5 days | P1/P2 |
| EPIC-04 | Governance Docs | ST-11, ST-12 | ~1 day | P1 |

**Total:** 12 tasks, ~8–9 effort-days

---

## Key Decisions

- **Scope selection:** 9 of 11 eligible backlog items included; 2 (BLG-NEW-04, BLG-SPEC-D3) deferred to v1.9 on capacity grounds. 9 P3 spec debt items deferred.
- **Capacity mode:** No explicit timebox/capacity specified; standard assumption applied (2 weeks, solo-dev evenings). Capacity check returned WARN — accepted in standard mode per project norms (milestone-based delivery, no hard deadline).
- **EPIC-01 is the release gate:** v1.8 is considered shipped when EPIC-01 delivers.

---

## Escalations

| ID | Type | Disposition | Blocks Execution |
|----|------|-------------|-----------------|
| ESC-20260304-01 | Execution pre-condition | Deferred | No (ST-09 only) |

**No execution blockers.** ESC-20260304-01 gates ST-09 only; all other 11 tasks are unblocked.

---

## Pre-Conditions for Next Phase

| Gate | Condition | Status |
|------|-----------|--------|
| Design Gate (Phase 1.5) | Must run before `plan sprint` | Pending — use `run design-gate --cycle 2026-03-04__release-v1.8` |
| ESC-20260304-01 | Product Owner decision on settings endpoint | Open — resolve before ST-09 execution |

---

## Artefacts Produced

| Artefact | Path |
|----------|------|
| Run Manifest | `claude/cycles/2026-03-04__release-v1.8/run_manifest.md` |
| Stage 1 Readiness | `claude/cycles/2026-03-04__release-v1.8/stage1_readiness.md` |
| Stage 2 Scope Extraction | `claude/cycles/2026-03-04__release-v1.8/stage2_scope_extraction.md` |
| Stage 3 Execution Plan | `claude/cycles/2026-03-04__release-v1.8/stage3_execution_plan.md` |
| Stage 3.5 Model Integrity | `claude/cycles/2026-03-04__release-v1.8/stage3_5_model_integrity.md` |
| Stage 4 Backlog Slice | `claude/cycles/2026-03-04__release-v1.8/stage4_backlog_slice.md` |
| Stage 4.5 Capacity Check | `claude/cycles/2026-03-04__release-v1.8/stage4_5_capacity_check.md` |
| Stage 5.5 Cross-Stage Integrity | `claude/cycles/2026-03-04__release-v1.8/stage5_5_cross_stage_integrity.md` |
| Stage 5.7 Decision Record Integrity | `claude/cycles/2026-03-04__release-v1.8/stage5_7_decision_record_integrity.md` |
| Escalations | `claude/cycles/2026-03-04__release-v1.8/escalations.md` |
| Cycle Summary | `claude/cycles/2026-03-04__release-v1.8/cycle_summary.md` |
| Lessons Learnt | `claude/cycles/2026-03-04__release-v1.8/lessons_learnt.md` |
| Backlog Transaction | `claude/cycles/2026-03-04__release-v1.8/backlog_txn.json` |
| State | `claude/cycles/2026-03-04__release-v1.8/state.json` |
