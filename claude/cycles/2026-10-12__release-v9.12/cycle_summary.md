Owner: Facilitator
Class: Operational Record (Class 3)
Status: Active
Design Gate Required: true
Last Updated: 2026-10-12 (created this run)
Lifecycle Guide: claude/charter/document_lifecycle_guide.md

---

# Cycle Summary — Release Planning 2026-10-12__release-v9.12

**Release:** v9.12

**Run type:** Roadmap-named by Product Owner direction at the v9.11 closure (DL-085), in place of a scheduled rebalance. The `v9.12` section commits `BLG-BE-162` (P1), which is seated.

**Anchor scope:** `BLG-BE-162` (ST-01, P1). Since 2026-04-18, every journal summary requested from Trade History has failed with HTTP 422, because the endpoint types trade IDs as integers but they are UUIDs. Seating it at P1 was the condition of v9.11's verification acceptance.

**Capacity decision (explicit user instruction): "use full capacity".** The 1 ready P1 item and the 8 seatable P2 items came first (5.15d), then a category-balanced, oldest-first round-robin over P3/P4. Total: **27.95 estimated days, 99.8% of the top of the ~24–28 day band.**

**Scope:** 48 stories across 6 EPICs.

| EPIC | Items | Days | Sources |
|------|-------|------|---------|
| EPIC-01 — AI Feature Correctness & Cost Visibility | 6 | 2.80 | `BLG-BE-162`, `BLG-AI-11`, `BLG-AI-12`, `BLG-AI-10`, `BLG-AI-13`, `BLG-OPS-183` |
| EPIC-02 — Stop, Sizing & Position Correctness | 10 | 5.55 | `BLG-BE-157`, `BLG-BE-158`, `BLG-QA-205`, `BLG-BE-159`, `BLG-BE-160`, `BLG-BE-145`, `BLG-BE-149`, `BLG-BE-148`, `BLG-FE-202`, `BLG-BE-144` |
| EPIC-03 — Trade Entry, Settings & Accessibility | 8 | 7.05 | `BLG-BE-146`, `BLG-FE-203`, `BLG-QA-206`, `BLG-FE-201`, `BLG-GOV-369`, `BLG-FE-207`, `BLG-FE-200`, `BLG-FE-210` |
| EPIC-04 — Security, Operations & Platform | 8 | 5.05 | `BLG-OPS-184`, `BLG-SEC-41`, `BLG-SEC-42`, `BLG-TECH-22`, `BLG-OPS-181`, `BLG-OPS-182`, `BLG-OPS-185`, `BLG-GOV-371` |
| EPIC-05 — Spec & Data Model Hygiene | 6 | 2.10 | `BLG-SPEC-176`, `BLG-SPEC-178`, `BLG-SPEC-179`, `BLG-SPEC-181`, `BLG-SPEC-182`, `BLG-SPEC-183` |
| EPIC-06 — Governance Tooling & Test Integrity | 10 | 5.40 | `BLG-GOV-385`, `BLG-GOV-386`, `BLG-GOV-363`, `BLG-GOV-367`, `BLG-GOV-364`, `BLG-GOV-372`, `BLG-QA-212`, `BLG-QA-209`, `BLG-QA-213`, `BLG-QA-202` |

**Product mix:** 16 build-and-ship items carry 11.85d (42% of effort), up from v9.11's 30%. This responds to the last rebalance's Skill-Silo reading (87.4%, above ceiling) and the 7th consecutive PVR Alert (0.161).

**Scope-selection method:**
- Gate scan of 232 items: 124 gated, 0 date-lapsed, 2 data-quality warnings, 2 already-resolved.
- No §1.3a gate edits were needed, so `backlog.md` was not changed.
- The STEP 4 calibration raised 3 selected items (`BLG-BE-162`, `BLG-SEC-41`, `BLG-OPS-182`).
- Ready pool: 101 items / 54.70 days. Selected: 48 items / 27.95 days (§1.4c).

**Deferred:**
- `BLG-TECH-21` (P2; dedicated-release constraint, v10.0).
- `BLG-GOV-142`, `BLG-GOV-360`, `BLG-GOV-361`, `BLG-GOV-368`: done or resolved. Archive or narrow at the next `groom backlog`.
- `BLG-FEAT-73`/`76`: gate-blocked.
- 53 further ready items (26.75d) on capacity grounds, including 22 tagged `Provisional-Target: v9.12` and 4 aged spec items (`BLG-SPEC-180`/`184`/`186`/`188`, §1.1 advisory, recommended for v9.13).

**Escalations:** none raised.

## Product Owner sign-off summary — gate edits (informational, per §1.3a bound 6)

None. The scripted date-lapsed list was empty, so no existing `backlog.md` item was edited.

## Pre-sprint Planning Required Decisions

The following High-priority decision must be resolved before sprint planning seals (before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-03] Whether light mode is a supported theme (ST-23, `BLG-FE-200`). If yes, ST-23 adds light-mode tokens and fixes Reports and Notifications at its 2.5d estimate. If no, ST-23 records the decision and handles the toggle and the axe baseline, and Sprint Planning re-estimates it. Expected at the design gate. — Owner: Head of UX & Design, with the Product Owner

**Design Gate:** **Required.** 11 stories carry observable UI ACs (ST-10, ST-13, ST-15, ST-17, ST-18, ST-20–ST-24, ST-26). **Do not invoke `plan sprint` until `run design-gate --cycle "2026-10-12__release-v9.12"` has passed.** `sprint_planning_pre_condition` blocks the seal otherwise.

**Publish Gate:** all conditions met:
- `open_escalations` is empty, with no blocking deferred escalations.
- `stage4_5_capacity_check` = pass; `stage5_5_cross_stage_integrity` = pass; `stage5_7` = not_applicable.
- `stage1_readiness` and `stage3_5_model_integrity` = pass.
- `plan_structured`, `plan_executable` and `backlog_committed` = true.

Result: `status = Validated`, `publish_eligible = true`.

**Locks:** `backlog_lock` and `roadmap_lock` were each acquired, committed and released cleanly.

**Open item for the user:** v9.11 closure action #8(b) (extend `release_planning_prompt.md` §1.3a bound 5 to gates removed by a Product Owner decision outside Release Planning) was due before this run and is still open. It needs a Head of Specs Team prompt change, outside this routine's write scope. ST-40 edits the same section, so Sprint Planning may bundle it there.
