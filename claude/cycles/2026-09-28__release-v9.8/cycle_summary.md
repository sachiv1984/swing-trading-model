Owner: Facilitator
Class: Operational Record (Class 3)
Status: Active
Design Gate Required: true
Last Updated: 2026-09-28 (created this run)
Lifecycle Guide: claude/charter/document_lifecycle_guide.md

---

# Cycle Summary — Release Planning 2026-09-28__release-v9.8

**Release:** v9.8 — Full-Capacity Debt Clearance

**Run type:** Backlog-driven (no formal roadmap section — STEP -1.2 Option (b) equivalence from the `2026-09-28__scheduled` rebalance, same-day and postdating the prior release-planning cycle — the first fresh, non-reused citation of this class since `v9.6`).

**Anchor scope:** None. No genuine ready build-and-ship U-item exists this cycle — the ready pool's only `BLG-FEAT-*` items are `73`/`76` (both structurally gate-blocked); `74` already shipped as `v9.7`'s flagship and has been retired from the backlog. The rebalance's PO Modify directive (seat ≥1-2 U-items, PVR 0.089 🔴 Alert) could not be satisfied for lack of candidates — see `run_manifest.md` Friction Item 1.

**Capacity decision (explicit user instruction, this invocation): "full capacity".** Applied as: all 3 ready P2 items seated first, then category-balanced round-robin oldest-first across 6 themes, reaching **28.00 estimated days — exactly the top of the confirmed ~24–28 day band.**

**Scope:** 39 stories across 6 EPICs:
- EPIC-01 — Frontend & UX Debt Clearance (6 items: `BLG-FE-184`, `BLG-FE-185`, `BLG-FE-190`, `BLG-FE-191`, `BLG-SPEC-158`, `BLG-SPEC-159`)
- EPIC-02 — Backend Reliability & Financial Correctness (2 items: `BLG-BE-128`, `BLG-BE-130`)
- EPIC-03 — QA & Test Coverage (8 items: `BLG-AI-07`, `BLG-QA-179`, `BLG-QA-180`, `BLG-QA-181`, `BLG-QA-182`, `BLG-QA-183`, `BLG-QA-184`, `BLG-QA-187`)
- EPIC-04 — Operations & Security Hardening (3 items: `BLG-OPS-169`, `BLG-OPS-170`, `BLG-SEC-39`)
- EPIC-05 — Spec & API Contract Debt (10 items: `BLG-API-04`, `BLG-API-05`, `BLG-SPEC-152`, `BLG-SPEC-153`, `BLG-SPEC-154`, `BLG-SPEC-155`, `BLG-SPEC-161`, `BLG-SPEC-162`, `BLG-SPEC-163`, `BLG-SPEC-172`)
- EPIC-06 — Governance & Process Debt (10 items: `BLG-GOV-338`, `BLG-GOV-339`, `BLG-GOV-340`, `BLG-GOV-341`, `BLG-GOV-342`, `BLG-GOV-346`, `BLG-GOV-348`, `BLG-GOV-349`, `BLG-GOV-351`, `BLG-SPEC-156`)

**Capacity:** 28.00 estimated days vs confirmed ~24–28 day band — PASS, at the top of the band, matching the explicit "full capacity" instruction.

**Scope-selection method:** Gate-detection procedure run against the current 196-item active backlog (`scripts/scan_backlog_gate_conditions.py`): 129 gated, 14 date-lapsed gates, 3 data-quality warnings. All 14 date-lapsed items cross-checked against this morning's `2026-09-28__scheduled` rebalance finding — 8 trace to the still-unconducted 90-day AI-review cluster (`BLG-GOV-351` filed to fix the trigger gap, seated this cycle), the remaining 6 unchanged from `v9.7`'s own verification. `BLG-SPEC-156` retained from the data-quality-warning set (pre-work, not gate-blocked) and subsequently selected; `BLG-FEAT-73`/`76` excluded as substantively gate-blocked. Result: a 65-item / 46.7-day ready pool → 39 items / 28.00 days via `release_planning_prompt.md` §1.4c.

**Deferred:** `BLG-FEAT-73`/`76` (substantively gate-blocked); the 8-item AI-review date-lapsed cluster (`BLG-FEAT-59`/`60`/`63`, `BLG-FE-84`, `BLG-OPS-88`, `BLG-GOV-140`/`141`/`142`, remain gated, review still not conducted); 6 further date-lapsed items unchanged from `v9.7`; 26 further ready items (~18.7 days), including `BLG-QA-185`, `BLG-SPEC-157`, `BLG-GOV-352` (skipped as capacity-overshoot on their category's round-robin turn).

**Escalations:** None raised during this release-planning session. The PO Modify directive shortfall was surfaced as a decision record entry, not routed through the formal escalation subroutine (no missing precondition existed — this was a finding about backlog composition, not a blocker).

**Design Gate:** **Required.** EPIC-01's `BLG-FE-184`, `BLG-FE-185`, `BLG-FE-190`, and `BLG-FE-191` carry an observable UI acceptance criterion. **Do not invoke `plan sprint` until `run design-gate --cycle "2026-09-28__release-v9.8"` has passed** — `sprint_planning_pre_condition` blocks the seal otherwise.

**Publish Gate:** All conditions met — `open_escalations` empty, no blocking deferred escalations, `stage4_5_capacity_check` = pass, `stage5_5_cross_stage_integrity` = pass, `stage5_7` = not_applicable (no escalations raised this cycle), `stage1_readiness`/`stage3_5_model_integrity` = pass, `plan_structured`/`plan_executable`/`backlog_committed` = true. `status = Validated`, `publish_eligible = true`.

**Locks:** `backlog_lock` acquired, committed, and released cleanly. `roadmap_lock` acquired, committed, and released cleanly.
