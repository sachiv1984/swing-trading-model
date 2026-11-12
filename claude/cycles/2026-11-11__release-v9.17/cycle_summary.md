Owner: Facilitator
Class: Operational Record (Class 3)
Status: Active
Design Gate Required: true
Last Updated: 2026-11-11 (created this run)
Lifecycle Guide: claude/charter/document_lifecycle_guide.md

---

# Cycle Summary — Release Planning 2026-11-11__release-v9.17

**Release:** v9.17 — Site Structure & Usability, Phase 3

**Run type:** Named release with no committed items, as at v9.14 and v9.16. The Product Owner named v9.17 after post-ship closure `2026-11-06__release-v9.16`. Its provisional content is DL-088's programme plan, Phase 3 row. This run sets the full scope.

**Anchor scope:**
- **Site Structure & Usability Phase 3, in full (EPIC-01–03, 20.50d):** a decision-first Positions page (urgency table, narrow-screen cards, one warning strip, one grace view), the single Journal area, one Performance page, section tabs on the long pages, and the semantic colour token sweep. After v9.17 only the programme's Close-out (`BLG-UX-08`, v9.18) remains.
- **Phase 2 completion (EPIC-04):** `BLG-BE-205` records stop moves, and the Today list's "Stops moved" group gets its TL-09/TL-10 tests.
- **The five accepted v9.16 P2 found defects (EPIC-05, ST-15).**

**Capacity decision (explicit user instruction): "use full capacity".** Selection order:
0. §1.4c step 0 holds nothing: Phase 3 is this release's phase.
1. No ready P1. The 7 ready P2 items (6.90d).
2. §1.4c step 1a's deferred lessons-learnt patch, `BLG-GOV-419` (0.15d).
3. §1.4c step 1b (first use): Phase 3's 7 P3 items and `BLG-BE-205` (19.50d). No Product Owner override was needed.

These came to 26.55d. One pass of the category-balanced, oldest-first round-robin filled the rest. Total: **27.95 estimated days, 99.8% of the top of the ~24–28 day band.**

**Scope:** 20 stories across 7 EPICs.

| EPIC | Items | Days | Sources |
|------|-------|------|---------|
| EPIC-01 — Phase 3: Positions Redesign | 4 | 7.50 | `BLG-FE-260`, `BLG-FE-261`, `BLG-FE-262`, `BLG-FE-257` |
| EPIC-02 — Phase 3: Journal & Performance Consolidation | 3 | 9.50 | `BLG-FE-258`, `BLG-FE-259`, `BLG-FE-263` |
| EPIC-03 — Phase 3: Semantic Colour Token Sweep | 1 | 3.50 | `BLG-FE-265` |
| EPIC-04 — Phase 2 Completion: Stops Moved Group | 2 | 2.00 | `BLG-BE-205`, `BLG-FE-254` (remainder) |
| EPIC-05 — Trade Plan Found Defects | 4 | 2.90 | `BLG-BE-211`, `BLG-FE-278`, `BLG-FE-281`, `BLG-FE-282` |
| EPIC-06 — Market-Data Reliability & Sizing Correctness | 3 | 2.00 | `BLG-OPS-217`, `BLG-OPS-195`, `BLG-BE-178` |
| EPIC-07 — Governance, Strategy Copy & Drift Tooling | 3 | 0.55 | `BLG-GOV-419`, `BLG-SPEC-202`, `BLG-QA-223` |

**Product mix:** 15 frontend and backend build items carry 25.90d (93% of effort), against v9.16's 62%. Skill-Silo was 68.1% at DL-088.

**Scope-selection method:**
- Gate scan of 282 items: 94 gated, 0 date-lapsed, 14 gating-item-shipped (all kept gated), 3 explicitly ungated, 2 data-quality warnings.
- No §1.3a gate edits; `backlog.md` was not changed.
- The STEP 4 calibration ran on the whole pool, reading Scope and AC text: 9 raises, +4.35d, 3 seated. One seated sweep (`BLG-FE-265`) was held at L with its count named.
- Ready pool: 180 items / 90.75 days. Selected: 20 items / 27.95 days.
- Ready-pool history row appended: gap 62.75d, Δ +6.05, rolling Δ +3.08, pool growing.

**Ungated backlog after this release:** 160 ready items, 62.80 days (≈2.2 releases at 28d), plus 8 ungated items not yet ready (9.80d): 168 items, 72.60 days in all. Of 282 backlog items, 94 are gated.

**Deferred:**
- `BLG-UX-08` (gated, v9.18 Close-out).
- `BLG-TECH-21` (P2): dedicated-release constraint, v10.0.
- `BLG-FEAT-73` (P1, re-check due, needs a production read) and `BLG-FEAT-76`.
- `BLG-GOV-200`/`201` (no ACs), `BLG-GOV-178`, `BLG-GOV-408`, `BLG-OPS-201` (after 2026-12-01).
- 160 further ready items (62.80d) on capacity grounds, including 22 items tagged `v9.17`.

**Escalations:** none raised.

## Product Owner sign-off summary

**Gate edits:** none this run.

**Overrides:** none, apart from the standing `BLG-TECH-21` deferral.

**Judgement calls recorded for confirmation:**
- `BLG-BE-205` seated by step 1b as an item of an earlier, unfinished phase (Phase 2, named in its row; unfinished until TL-09/TL-10 pass).
- `BLG-FE-254` seated as its 0.5d remainder, not its whole-item L estimate.

## Pre-sprint Planning Required Decisions

The following High-priority decision must be resolved before sprint planning seals (before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-05] Strategy Rules & System Intent Owner decisions, dated in `sprint_backlog.md`'s sign-off summary: (1) ST-12 — clear the pre-entry acknowledgement when `advisory_status` or `checks` change, or store it inside the dated snapshot; (2) ST-19 — add the Positions page's 2R Exit Zone threshold to `strategy_rules.md` §11 (a case (c) write, which the owner then confirms as an AC line), or reword the tooltip without a rule number. — Owner: Strategy Rules & System Intent Owner

**Design Gate:** **Required.** 14 stories carry observable UI ACs (ST-01–ST-08, ST-10–ST-14, ST-19). ST-01–ST-04, ST-06 and ST-07 have no page-level design record yet. **Do not invoke `plan sprint` until `run design-gate --cycle "2026-11-11__release-v9.17"` has passed.** `sprint_planning_pre_condition` blocks the seal otherwise.

**Publish Gate:** all conditions met:
- `open_escalations` is empty, with no blocking deferred escalations.
- `stage4_5_capacity_check` = pass; `stage5_5_cross_stage_integrity` = pass; `stage5_7` = not_applicable.
- `stage1_readiness` and `stage3_5_model_integrity` = pass.
- `plan_structured`, `plan_executable` and `backlog_committed` = true.

Result: `status = Validated`, `publish_eligible = true`.

**Locks:** `backlog_lock` was acquired at STEP 3.9, committed and released. `roadmap_lock` was acquired, committed and released. Both released cleanly.
