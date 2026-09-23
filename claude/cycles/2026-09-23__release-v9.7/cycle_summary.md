Owner: Facilitator
Class: Operational Record (Class 3)
Status: Active
Design Gate Required: true
Last Updated: 2026-09-23 (created this run)
Lifecycle Guide: claude/charter/document_lifecycle_guide.md

---

# Cycle Summary — Release Planning 2026-09-23__release-v9.7

**Release:** v9.7 — PO-05 Replay Mode & Full-Capacity Debt Clearance

**Run type:** Backlog-driven (no formal roadmap section — STEP -1.2 Option (b) equivalence from the `2026-09-19__scheduled` rebalance, now 15 consecutive release cycles relying on this class of equivalence; this is the 2nd consecutive release to cite this specific rebalance record — see `run_manifest.md` Friction Item 3).

**Anchor scope:** `BLG-FEAT-74` (PO-05 Lightweight Replay Mode) — Arc 4's flagship long-term validation feature, gate-blocked since 2026-07-10, whose §13 determinism pre-clearance PASSed this week (`ESC-EXEC-20260921-05`, 2026-09-23). This is the first cycle in which this repo's ready pool has ever held a genuinely ready P1 item. Seated as firm scope per explicit Product Owner direction (2026-09-23) — see `docs/product/decisions/decisions--2026-09-23__release-v9.7.md`.

**Capacity decision (explicit user instruction, this invocation): seat `BLG-FEAT-74` as firm P1 scope AND "use full capacity".** Applied as: `BLG-FEAT-74` seated alone at P1 (12.0 PO-estimated days — no canonical `VH` midpoint exists), then all 6 ready P2 items, then category-balanced round-robin oldest-first across 6 remaining themes, reaching **28.00 estimated days — exactly the top of the confirmed ~24–28 day band.**

**Scope:** 29 stories across 7 EPICs:
- EPIC-01 — PO-05 Lightweight Replay Mode (1 item: `BLG-FEAT-74`, 12.0d)
- EPIC-02 — Frontend & UX Correctness (6 items: `BLG-FE-186`, `BLG-FE-187`, `BLG-FE-188`, `BLG-FE-178`, `BLG-FE-179`, `BLG-FE-183`)
- EPIC-03 — Backend Reliability & Financial Correctness (6 items: `BLG-BE-127`, `BLG-BE-123`, `BLG-BE-124`, `BLG-BE-125`, `BLG-BE-126`, `BLG-BE-129`)
- EPIC-04 — QA & Test Coverage (5 items: `BLG-QA-188`, `BLG-QA-174`, `BLG-QA-175`, `BLG-QA-176`, `BLG-QA-177`)
- EPIC-05 — Governance & Process Debt (4 items: `BLG-GOV-327`, `BLG-GOV-330`, `BLG-GOV-331`, `BLG-GOV-333`)
- EPIC-06 — Spec & Data Model Debt (4 items: `BLG-SPEC-147`, `BLG-SPEC-149`, `BLG-SPEC-150`, `BLG-SPEC-151`)
- EPIC-07 — Ops, Security & Verification (3 items: `BLG-OPS-168`, `BLG-OPS-167`, `BLG-SEC-38`)

**Capacity:** 28.00 estimated days vs confirmed ~24–28 day band — PASS, at the top of the band, matching the explicit "use full capacity" instruction. Acknowledgement is due at Sprint Planning.

**Scope-selection method:** Gate-detection procedure run against the current 200-item active backlog (`scripts/scan_backlog_gate_conditions.py`): 129 gated, 4 data-quality warnings. Six date-lapsed gates read individually — all 6 remain gated (none cleared this cycle). One item (`BLG-FE-189`) found already resolved same-session despite no `✅ COMPLETE` banner — excluded, second occurrence of this failure class (see `run_manifest.md` Friction Item 1). Result: a 68-item / 61.35-day ready pool → 29 items / 28.00 days via `release_planning_prompt.md` §1.4c.

**Deferred:** `BLG-FEAT-73`/`76` (substantively gate-blocked); `BLG-FEAT-59`/`60`/`63`, `BLG-FE-84`, `BLG-GOV-140`/`141`/`142`, `BLG-OPS-88` (within-sprint date gate 2026-09-24, classified conditional — re-eligible at v9.8); `BLG-FE-189` (already resolved — archive at next groom); 123 further gated items; 39 further ready items (~21.35 days), including `BLG-FE-184`, `BLG-FE-185`, `BLG-BE-128` (skipped as capacity-overshoot on their category's round-robin turn).

**Escalations:** None raised during this release-planning session. The `BLG-FEAT-74` seating and effort-estimate question was surfaced to the Product Owner directly as a scope-shaping decision, not routed through the formal escalation subroutine (no blocker existed — this was a judgment call about how a cleared-but-ambiguous item should be scoped, not a missing-precondition halt).

**Design Gate:** **Required.** `BLG-FEAT-74` (replay-mode selector + output view) and all 6 EPIC-02 items carry an observable UI acceptance criterion. **Do not invoke `plan sprint` until `run design-gate --cycle "2026-09-23__release-v9.7"` has passed** — `sprint_planning_pre_condition` blocks the seal otherwise.

## Pre-sprint Planning Required Decisions

The following High-priority decisions must be resolved before sprint planning seals (i.e., before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-01] `BLG-FEAT-74`'s exact scope (replay granularity, output format) is undefined — sprint planning cannot write concrete ACs for its backend/frontend sub-stories without it. Required resolution: a scope-confirmation sub-story or Head of Specs Team pre-sprint scoping note, referencing `docs/product/decisions/po05_section13_preassessment.md`'s 6 binding conditions. Owner: Head of Specs Team / Product Owner.

**Publish Gate:** All conditions met — `open_escalations` empty, no blocking deferred escalations, `stage4_5_capacity_check` = pass, `stage5_5_cross_stage_integrity` = pass, `stage5_7` = not_applicable (no escalations raised this cycle), `stage1_readiness`/`stage3_5_model_integrity` = pass, `plan_structured`/`plan_executable`/`backlog_committed` = true. `status = Validated`, `publish_eligible = true`.

**Locks:** `backlog_lock` acquired, committed, and released cleanly. `roadmap_lock` acquired, committed, and released cleanly.
