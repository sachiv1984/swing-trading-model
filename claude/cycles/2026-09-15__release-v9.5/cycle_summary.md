Owner: Facilitator
Class: Operational Record (Class 3)
Status: Active
Design Gate Required: true
Last Updated: 2026-09-15 (created this run)
Lifecycle Guide: claude/charter/document_lifecycle_guide.md

---

# Cycle Summary — Release Planning 2026-09-15__release-v9.5

**Release:** v9.5 — Full-Capacity Debt Clearance III

**Run type:** Backlog-driven (no formal roadmap section — STEP -1.2 Option (b) equivalence from the `2026-09-14__scheduled` rebalance, extending the v8.5–v9.4 pattern, now 13 consecutive release cycles).

**Anchor scope:** `BLG-BE-117` (CI-blocking test failure on every open/future PR) and `BLG-OPS-160` (possible live risk-management scheduling gap) — the **first cycle on record with genuine ungated P1 scope**; every prior rebalance's own Production Correctness Fast-Track found 0 qualifying P0/P1 items.

**Capacity decision (explicit user instruction, this invocation): "use full capacity".** Applied as: P1-first, then P2-first, then category-balanced round-robin selection across 6 debt themes, reaching 27.99 estimated days — 0.01 days short of the exact 28-day ceiling, the tightest full-capacity fit on record.

**Scope:** 43 stories across 6 EPICs:
- EPIC-01 — Backend & Platform Engineering Debt (4 items: `BLG-BE-117`, `BLG-BE-112`, `BLG-BE-113`, `BLG-BE-114`)
- EPIC-02 — Operations & Security Debt (10 items: `BLG-OPS-160`, `BLG-OPS-153` through `BLG-OPS-159`, `BLG-OPS-161`, `BLG-OPS-162`)
- EPIC-03 — QA & Test Coverage Debt (7 items: `BLG-QA-59`, `BLG-QA-165` through `BLG-QA-170`)
- EPIC-04 — Spec & Documentation Debt (9 items: `BLG-SPEC-D18`, `BLG-SPEC-56`, `BLG-SPEC-57`, `BLG-SPEC-133`, `BLG-SPEC-139` through `BLG-SPEC-143`)
- EPIC-05 — Governance Process Debt (9 items: `BLG-GOV-332`, `BLG-GOV-316`, `BLG-GOV-318` through `BLG-GOV-324`)
- EPIC-06 — Frontend & UX Debt (4 items: `BLG-FE-177`, `BLG-FE-175`, `BLG-FE-176`, `BLG-UX-05`)

**Capacity:** 27.99 estimated days vs confirmed ~24-28 day band — PASS, at the top of the band, matching the explicit "use full capacity" instruction.

**Scope-selection method:** Gate-detection procedure run against the current 195-item active backlog (`scripts/scan_backlog_gate_conditions.py`). 130 gated/conditional items + 3 substantively gate-blocked data-quality-flagged items (`BLG-FEAT-73`/`74`/`76`) leave a 62-item ready pool, ~43.79 estimated days. Selected a 43-item / 27.99-day subset via `release_planning_prompt.md` §1.4c's now-codified method: P1 items first, then P2 items (ascending ID), then category-balanced round-robin oldest-first for the remaining P3/P4 items.

**Deferred:** `BLG-FEAT-73`/`74`/`76` (substantively gate-blocked); 130 formally gated items; 19 further ungated P3/P4 items (~16.80 days) left unselected purely on capacity grounds — available for `plan release v9.6`.

**Ready-pool re-classification (see `run_manifest.md` Friction Item 1):** `BLG-SPEC-56`, `BLG-SPEC-57`, `BLG-QA-59` — excluded at v9.3/v9.4 — re-read this session and found to describe legitimate pre-authoring work, not gate-blocked work; included in scope (`ST-15`, `ST-23`, `ST-24`).

**Escalations:** None raised during this release-planning session.

**Design Gate:** **Required.** All 4 EPIC-06 items carry an observable UI acceptance criterion or UI-shipping Scope text — `BLG-FE-177` (text-formatting change), `BLG-FE-175` (motion-timing fix), `BLG-FE-176` (toast-timing fix), `BLG-UX-05` (compliance-section copy/placement change). **Do not invoke `plan sprint` until `run design-gate --cycle "2026-09-15__release-v9.5"` has passed** — `sprint_planning_pre_condition` blocks the seal otherwise.

**Publish Gate:** All conditions met — `open_escalations` empty, no blocking deferred escalations, `stage4_5_capacity_check` = pass, `stage5_5_cross_stage_integrity` = pass, `stage5_7` = not_applicable (no escalations raised this cycle), `stage1_readiness`/`stage3_5_model_integrity` = pass, `plan_structured`/`plan_executable`/`backlog_committed` = true. `status = Validated`, `publish_eligible = true`.

**Locks:** `backlog_lock` acquired, committed, and released cleanly. `roadmap_lock` acquired, committed, and released cleanly.
