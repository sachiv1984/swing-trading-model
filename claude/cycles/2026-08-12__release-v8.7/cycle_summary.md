Owner: Facilitator
Class: Operational Record (Class 3)
Status: Active
Design Gate Required: true
Last Updated: 2026-08-12 (created this run)
Lifecycle Guide: claude/charter/document_lifecycle_guide.md

---

# Cycle Summary — Release Planning 2026-08-12__release-v8.7

**Release:** v8.7 — User Features, Data-Integrity Closure & Cross-Domain Hardening

**Run type:** Backlog-driven (no formal roadmap section — STEP -1.2 Option (b) equivalence, same precedent as `v8.5`/`v8.6`).

**User instruction carried into this run:** "use full capacity, user features to be prioritised" — applied as (1) EPIC-01 (user-facing features) leads the EPIC table, (2) scope filled to ~25.25 estimated days against the confirmed ~24-28 day capacity band, (3) scope selection ran `scripts/scan_backlog_gate_conditions.py` first to identify the full ungated `BLG-FEAT-*`/`BLG-FE-*` candidate pool before filling remaining capacity from other categories.

**Scope:** 21 stories across 7 EPICs:
- EPIC-01 — User-Facing Product Features & UX Completion (6 items: `BLG-FEAT-84`, `BLG-FE-158`, `BLG-BE-95`, `BLG-FE-151`, `BLG-FE-152`, `BLG-FE-156`)
- EPIC-02 — Trade-Plan Data Integrity Closure (1 item: `BLG-BE-96`, P1, mandatory carryover)
- EPIC-03 — Test Coverage for Shipped UI & Financial Correctness (2 items: `BLG-FE-157`, `BLG-QA-148`)
- EPIC-04 — Backend Reliability & Performance Hardening (3 items: `BLG-BE-89`, `BLG-BE-90`, `BLG-BE-30`)
- EPIC-05 — Security Hardening (2 items: `BLG-SEC-30`, `BLG-SEC-31`)
- EPIC-06 — Operations & Infrastructure Debt (3 items: `BLG-OPS-139`, `BLG-OPS-140`, `BLG-OPS-142`)
- EPIC-07 — Governance & Spec Debt (4 items: `BLG-GOV-290`, `BLG-GOV-303`, `BLG-GOV-305`, `BLG-SPEC-124`)

**Capacity:** ~25.25 estimated days vs confirmed ~24-28 day band — PASS, mid-band, consistent with the "use full capacity" instruction without requiring scope trim or a WARN outcome.

**Scope-selection highlights:** All 21 items confirmed ungated via `scripts/scan_backlog_gate_conditions.py` (292 items scanned, 175 gated). `BLG-BE-96` carries an explicit v8.6 Product Owner risk-acceptance condition ("do not defer further") and is treated as mandatory regardless of the user-features-first ordering. `BLG-OPS-142` closes the `check_api_performance_baseline_drift.py` fix carried across 3 consecutive Post-Ship Closures (v8.4→v8.5→v8.6) — see Carry-Forward Advisory in `run_manifest.md`.

**Deferred:** None formally — this cycle draws directly from the ungated backlog pool with no committed prior scope to defer from. Remaining ungated items (further P1/P2 gated items such as `BLG-FEAT-73`/`BLG-FEAT-74`, still gate-blocked, and additional P2/P3 governance/ops items not selected) remain available for the next release cycle.

**Escalations:** None raised this cycle — all preflight and hard gates passed cleanly.

**Pre-sprint Planning Required Decisions**

The following High-priority decision must be resolved before sprint planning seals (i.e., before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-02] `BLG-BE-96` staging/live-Postgres access — confirm a reachable staging (or production read-only) environment exists for the linkage verification, orphaned-row query, and DS-12 constraint check before sprint execution begins; if still unavailable, Product Owner must explicitly re-confirm the item proceeds via best-available proxy rather than silently repeating the v8.6 mocked-DB substitution — Owner: Head of Engineering

**Design Gate:** Required — EPIC-01 contains observable UI acceptance criteria (theme-consistency fixes, modal token conversion, new trade-plan-entry field, position-entry confirmation banner) and EPIC-03 adds Playwright coverage for those surfaces. Run `run design-gate --cycle 2026-08-12__release-v8.7` before `plan sprint`.

**Publish Gate:** All conditions met — `open_escalations` empty, no blocking deferred escalations, `stage4_5_capacity_check` = pass, `stage5_5_cross_stage_integrity` = pass, `stage5_7` = not_applicable (no escalations raised), `stage1_readiness`/`stage3_5_model_integrity` = pass, `plan_structured`/`plan_executable`/`backlog_committed` = true. `status = Validated`, `publish_eligible = true`.

**Locks:** `backlog_lock` acquired, committed, and released cleanly. `roadmap_lock` was not required to be formally acquired (no `claude/roadmap/.lock` file existed at any point during this run — annotation written directly and confirmed idempotent via marker check); `roadmap_txn.json` recorded committed for audit completeness.
