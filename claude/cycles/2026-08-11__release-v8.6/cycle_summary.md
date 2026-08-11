Owner: Facilitator
Class: Operational Record (Class 3)
Status: Active
Design Gate Required: true
Last Updated: 2026-08-11 (created this run)
Lifecycle Guide: claude/charter/document_lifecycle_guide.md

---

# Cycle Summary — Release Planning 2026-08-11__release-v8.6

**Release:** v8.6 — User Features, Data-Integrity Foundation & Correctness Carryover
**Run type:** Backlog-driven (no formal roadmap section — STEP -1.2 Option (b) equivalence, same precedent as `v8.5`).

**User instruction carried into this run:** "use full capacity, user features should be prioritised" — applied as (1) EPIC-01 (user-facing features) leads the EPIC table, (2) scope filled to ~23.75 estimated days against the confirmed ~24-28 day capacity band.

**Scope:** 26 stories across 6 EPICs:
- EPIC-01 — User-Facing Product Features (2 items: `BLG-FEAT-32`, `BLG-FEAT-56`)
- EPIC-02 — Trade-Plan Data Integrity Foundation (1 item: `BLG-BE-91`, P1)
- EPIC-03 — Frontend Design Consistency & Correctness Carryover (7 items)
- EPIC-04 — Backend & Financial Correctness (4 items)
- EPIC-05 — QA Test-Coverage Debt Closure (4 items)
- EPIC-06 — Operations & Governance Debt Closure (8 items)

**Capacity:** ~23.75 estimated days vs confirmed ~24-28 day band — PASS, near top of band per the "use full capacity" instruction.

**Gate-status highlights:** `BLG-FEAT-32`'s gate cleared same-day (2026-08-11 rebalance). `BLG-FEAT-56`'s qualitative usage-pattern gate condition resolved via explicit Product Owner disposition (see `decisions--2026-08-11__release-v8.6.md`). `BLG-BE-91` ungated, named structural response to the Skill-Silo mandatory pull-forward finding.

**Deferred:** `BLG-FEAT-73` (SI-02 frontend — gate not met), `BLG-FEAT-74` (PO-05 Replay Mode — gated, VH effort), `BLG-FEAT-44` (Arc 5 low-volume advisory — gate clears 2026-08-27), `BLG-SPEC-124` (deprioritised behind capacity-filling scope).

**Escalations:** None raised this cycle — all preflight and hard gates passed cleanly.

**Design Gate:** Required — EPIC-03 contains observable UI acceptance criteria (design-token registration, colour drift fixes, dark-class sync timing). Run `run design-gate --cycle 2026-08-11__release-v8.6` before `plan sprint`.

**Publish Gate:** All conditions met — `open_escalations` empty, no blocking deferred escalations, `stage4_5_capacity_check` = pass, `stage5_5_cross_stage_integrity` = pass, `stage5_7` = not_applicable (no escalations raised), `stage1_readiness`/`stage3_5_model_integrity` = pass, `plan_structured`/`plan_executable`/`backlog_committed` = true. `status = Validated`, `publish_eligible = true`.

**Locks:** `backlog_lock` and `roadmap_lock` both acquired, committed, and released cleanly — no contention.
