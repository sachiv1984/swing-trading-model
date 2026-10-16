Owner: Facilitator
Class: Operational Record (Class 3)
Status: Active
Design Gate Required: true
Last Updated: 2026-10-16 (created this run)
Lifecycle Guide: claude/charter/document_lifecycle_guide.md

---

# Cycle Summary — Release Planning 2026-10-16__release-v9.13

**Release:** v9.13

**Run type:** Roadmap-committed. Rebalance `2026-10-16__scheduled` (STEP 8.1 Option (a), DL-086) added the `v9.13` section, committing `BLG-FE-226` (P1), `BLG-FE-227` and `BLG-BE-182` (P2). All three are seated.

**Anchor scope:** `BLG-FE-226` (ST-01, P1). Since 2026-01-24, the Daily Position Monitor's "confirm exits" has called `PATCH /positions/{id}`, a route that does not exist. Every confirmation fails with a 405 and no message, so the home page's exit shortcut does nothing when §8.1/§8.2 say to exit.

**Capacity decision (explicit user instruction): "use full capacity".** The 1 ready P1 item and the 11 seatable P2 items came first (11.40d), then a category-balanced, oldest-first round-robin over P3/P4. Total: **28.00 estimated days, 100% of the top of the ~24–28 day band.**

**Scope:** 40 stories across 6 EPICs.

| EPIC | Items | Days | Sources |
|------|-------|------|---------|
| EPIC-01 — Exit Flow, Exit Reasons & Red Flag Journal | 5 | 5.50 | `BLG-FE-226`, `BLG-SPEC-186`, `BLG-FE-227`, `BLG-BE-182`, `BLG-GOV-391` |
| EPIC-02 — Stop, Sizing & Position Data Correctness | 9 | 2.75 | `BLG-BE-180`, `BLG-BE-161`, `BLG-API-07`, `BLG-BE-156`, `BLG-SPEC-188`, `BLG-SPEC-180`, `BLG-QA-204`, `BLG-QA-208`, `BLG-QA-210` |
| EPIC-03 — AI Output Safety, Debrief & Chat | 8 | 3.10 | `BLG-AI-17`, `BLG-AI-18`, `BLG-AI-16`, `BLG-AI-15`, `BLG-AI-14`, `BLG-FE-211`, `BLG-FE-212`, `BLG-FE-208` |
| EPIC-04 — API Call Integrity & UI Rendering | 5 | 6.25 | `BLG-QA-228`, `BLG-QA-227`, `BLG-FE-221`, `BLG-FE-209`, `BLG-QA-211` |
| EPIC-05 — Operations, Cost & Platform | 7 | 8.50 | `BLG-OPS-187`, `BLG-OPS-189`, `BLG-OPS-18`, `BLG-OPS-19`, `BLG-OPS-23`, `BLG-OPS-77`, `BLG-TECH-23` |
| EPIC-06 — Governance & Spec Tooling | 6 | 1.90 | `BLG-GOV-390`, `BLG-GOV-373`, `BLG-SPEC-184`, `BLG-GOV-376`, `BLG-GOV-377`, `BLG-GOV-387` |

**Product mix:** 15 build-and-ship items carry 8.60d (31% of effort), down from v9.12's 42%. The three Product-Owner-committed U-items from the §7.1 sustained-failure clause are seated. The last rebalance read Skill-Silo at 69.6% (above ceiling, improving) and PVR 0.204 (8th consecutive Alert, improving).

**Scope-selection method:**
- Gate scan of 252 items: 124 gated, 0 date-lapsed, 25 gating-item-shipped, 2 data-quality warnings, 3 already-resolved.
- First run of the gating-item-shipped check: 5 Ops items treated as ungated (their gating items shipped v6.8–v9.3), 1 delivered, 19 kept gated.
- No §1.3a gate edits were needed, so `backlog.md` was not changed.
- The STEP 4 calibration ran on the whole pool before selection: 8 raises, +4.35d, 4 of them on seated items.
- Ready pool: 124 items / 64.65 days. Selected: 40 items / 28.00 days (§1.4c). Ready-pool history row appended.

**Deferred:**
- `BLG-TECH-21` (P2; dedicated-release constraint, v10.0).
- `BLG-GOV-142`, `BLG-GOV-360`, `BLG-SPEC-199`, `BLG-GOV-361`, `BLG-GOV-368`, `BLG-GOV-374`: done or resolved. Archive at the next `groom backlog`.
- `BLG-FEAT-73`/`76`: gate-blocked.
- 84 further ready items (36.65d) on capacity grounds, including 6 tagged `v9.13` and 20 stale `v9.12` tags.

**Escalations:** none raised.

## Product Owner sign-off summary — gate edits (informational, per §1.3a bound 6)

None. The scripted date-lapsed list was empty, so no existing `backlog.md` item was edited. Five items were treated as ungated under the gating-item-shipped check without editing their gate text (see `run_manifest.md`).

## Pre-sprint Planning Required Decisions

The following High-priority decision must be resolved before sprint planning seals (before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-02] Write route for `claude/strategy/strategy_rules.md`. ST-38 and ST-39 edit it, and ST-05 (§8 determination), ST-06 (stop floor, §5) and ST-07 (§6.3 exception) may. Sprint Execution may not write the file under `execution_prompt.md` §7; the v9.9 ST-20 edit was made on the user's explicit instruction. Decide one: (a) the user and the Strategy Rules & System Intent Owner authorise named `strategy_rules.md` writes for these stories, with one EPIC sequencing the version bumps; or (b) Sprint Planning reclassifies the edits as decision records with exact proposed text, applied by the owner outside the sprint. — Owner: Strategy Rules & System Intent Owner, with the Product Owner and the user

**Design Gate:** **Required.** 12 stories carry observable UI ACs (ST-01, ST-03–ST-06, ST-09, ST-10, ST-20–ST-22, ST-25, ST-26). **Do not invoke `plan sprint` until `run design-gate --cycle "2026-10-16__release-v9.13"` has passed.** `sprint_planning_pre_condition` blocks the seal otherwise.

**Publish Gate:** all conditions met:
- `open_escalations` is empty, with no blocking deferred escalations.
- `stage4_5_capacity_check` = pass; `stage5_5_cross_stage_integrity` = pass; `stage5_7` = not_applicable.
- `stage1_readiness` and `stage3_5_model_integrity` = pass.
- `plan_structured`, `plan_executable` and `backlog_committed` = true.

Result: `status = Validated`, `publish_eligible = true`.

**Locks:** `backlog_lock` and `roadmap_lock` were each acquired, committed and released cleanly.
