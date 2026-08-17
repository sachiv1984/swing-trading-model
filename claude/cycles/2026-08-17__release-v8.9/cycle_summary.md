Owner: Facilitator
Class: Operational Record (Class 3)
Status: Active
Design Gate Required: true
Last Updated: 2026-08-17 (created this run)
Lifecycle Guide: claude/charter/document_lifecycle_guide.md

---

# Cycle Summary — Release Planning 2026-08-17__release-v8.9

**Release:** v8.9 — Live Risk-Management Correctness & Trade Intelligence Expansion

**Run type:** Backlog-driven (no formal roadmap section — STEP -1.2 Option (b) equivalence, same precedent as `v8.5`–`v8.8`).

**Anchor scope:** Two brand-new P0 items filed today (`BLG-BE-102`, `BLG-BE-103`), both `Provisional-Target: TBD (next release)` — named for v8.9 — found during a real production investigation of a live position's stop-loss discrepancy.

**Product Owner sizing decision carried into this run:** Presented with 3 options (tight P0-only ~2.25 days / widen to full ~24–28 day capacity band / moderate P0+P2-only ~10–15 days), the Product Owner chose to widen. Applied as (1) EPIC-01 (live risk-management correctness) leads the EPIC table, (2) scope filled to ~26.1 estimated days against the confirmed ~24-28 day capacity band, (3) scope selection ran `scripts/scan_backlog_gate_conditions.py` first to confirm the full candidate pool was ungated before filling remaining capacity, weighted toward execution-heavy items (EPIC-02) per the Skill-Silo mitigation rotation guidance.

**Scope:** 22 stories across 6 EPICs:
- EPIC-01 — Live Risk-Management Correctness (3 items: `BLG-BE-102`, `BLG-BE-103`, `BLG-SPEC-85`)
- EPIC-02 — Trade Sizing & Post-Trade Intelligence (4 items: `BLG-BE-104`, `BLG-FEAT-91`, `BLG-FEAT-90`, `BLG-FEAT-89`)
- EPIC-03 — Backend Reliability & Performance (4 items: `BLG-BE-98`, `BLG-BE-99`, `BLG-BE-100`, `BLG-BE-101`)
- EPIC-04 — Test Coverage & QA Hardening (4 items: `BLG-QA-149`, `BLG-QA-150`, `BLG-QA-151`, `BLG-QA-152`)
- EPIC-05 — Operations & Spec Currency (3 items: `BLG-OPS-146`, `BLG-OPS-113`, `BLG-SPEC-130`)
- EPIC-06 — Governance Process Debt Closure (4 items: `BLG-GOV-308`, `BLG-GOV-309`, `BLG-GOV-264`, `BLG-GOV-260`)

**Capacity:** ~26.125 estimated days vs confirmed ~24-28 day band — PASS, within the band near its midpoint, matching the Product Owner's widen-to-full-capacity decision.

**Scope-selection highlights:** All 22 items confirmed ungated via `scripts/scan_backlog_gate_conditions.py` (268 items scanned, 170 gated + 6 data-quality warnings). 2 items carry `Provisional-Target: TBD (next release)` explicitly naming v8.9 (`BLG-BE-102`, `BLG-BE-103`), both P0 live production correctness bugs. `BLG-GOV-105` was shortlisted then dropped — already ✅ CLOSED (confirmed duplicate). `BLG-FEAT-92` was shortlisted then dropped — its own item text names an unresolved scope-overlap dependency on gated `BLG-FEAT-30` requiring PO/Head of Specs Team reconciliation, not resolvable unilaterally by this routine — see `run_manifest.md`.

**Deferred:** `BLG-FEAT-92` (dependency reconciliation needed) and `BLG-GOV-105` (already closed, pending archival) — see Scope Document. 60 further ungated P3 items remain unselected and available for future release cycles.

**Escalations:** None raised this cycle — all preflight and hard gates passed cleanly.

**Design Gate:** Required — `BLG-BE-103` (ST-02) and 3 of 4 EPIC-02 items (`BLG-BE-104`/`BLG-FEAT-91`/`BLG-FEAT-90`/`BLG-FEAT-89`, ST-04 through ST-07) carry observable UI acceptance criteria (position-card currency display, live sizing preview, closed-trade debrief surface, backtest results/candidate-comparison surface). Run `run design-gate --cycle 2026-08-17__release-v8.9` before `plan sprint`.

**Publish Gate:** All conditions met — `open_escalations` empty, no blocking deferred escalations, `stage4_5_capacity_check` = pass, `stage5_5_cross_stage_integrity` = pass, `stage5_7` = not_applicable (no escalations raised), `stage1_readiness`/`stage3_5_model_integrity` = pass, `plan_structured`/`plan_executable`/`backlog_committed` = true. `status = Validated`, `publish_eligible = true`.

**Locks:** `backlog_lock` acquired, committed, and released cleanly. `roadmap_lock` acquired, committed, and released cleanly.
