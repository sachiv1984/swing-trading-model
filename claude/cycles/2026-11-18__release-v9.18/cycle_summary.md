Owner: Facilitator
Class: Operational Record (Class 3)
Status: Active
Design Gate Required: true
Last Updated: 2026-11-18 (created this run)
Lifecycle Guide: claude/charter/document_lifecycle_guide.md

---

# Cycle Summary — Release Planning 2026-11-18__release-v9.18

**Release:** v9.18 — Site Structure & Usability, Phase 4 (stages 1–2) and first-time-right

**Run type:** Committed release section. Roadmap rebalance `2026-11-18__scheduled` added a §3 v9.18 section with 19 committed items (≈12–20 days) and the Phase 4 programme plan (DL-089). This run seats all 19 and fills the rest of the band.

**Anchor scope:**
- **Phase 4 stage 1, correct and safe (EPIC-01):** keyboard and label fixes for the Level A failures, truthful alert-delivery copy, the open-access risk re-review, and a Core Web Vitals baseline.
- **Phase 4 stage 2, home page and review loop (EPIC-02, EPIC-03):** navigation and design-system specs, a one-line quiet-day Dashboard, one grace definition, "Plan this" on new signals, automatic checklist status, rules-followed filtering, the two navigation moves, a readable and linked Weekly Digest, and core-loop measurement.
- **First-time-right (EPIC-04):** the Product Owner's 2026-11-12 direction — `BLG-GOV-422` (with its 2026-11-13 extension), `BLG-QA-262`, `BLG-QA-260` — plus the scripted locator check and enforced pre-commit review and prompt budget.
- **Position data correctness (EPIC-05):** native entry, live FX, stock splits, and four older correctness items.

**Capacity decision (explicit user instruction): "use full capacity".** Selection order:
0. §1.4c step 0 holds Phase 4 stages 3–4 (20 items, 16.25d, v9.19).
1. No ready P1. The 12 ready P2 items (9.55d).
2. §1.4c step 1a: `BLG-QA-268` and `BLG-OPS-220` (0.65d).
3. §1.4c step 1b: Phase 4 stages 1–2's 12 P3 items (11.90d).
4. Product Owner override: `BLG-QA-260` (0.15d).

These came to 22.25d. Two passes of the category-balanced, oldest-first round-robin filled the rest (13 items, 5.70d). Total: **27.95 estimated days, 99.8% of the top of the ~24–28 day band.**

**Scope:** 40 stories across 7 EPICs.

| EPIC | Items | Days | Sources |
|------|-------|------|---------|
| EPIC-01 — Phase 4 Stage 1: Correct and Safe | 6 | 3.65 | `BLG-FE-311`, `BLG-FE-312`, `BLG-FE-318`, `BLG-FE-228`, `BLG-SEC-46`, `BLG-QA-271` |
| EPIC-02 — Phase 4 Stage 2: Home Page and Navigation | 7 | 6.15 | `BLG-UX-21`, `BLG-FE-323`, `BLG-UX-11`, `BLG-FE-308`, `BLG-UX-13`, `BLG-UX-19`, `BLG-FE-320` |
| EPIC-03 — Phase 4 Stage 2: Weekly Review Loop | 4 | 4.25 | `BLG-SPEC-204`, `BLG-UX-15`, `BLG-UX-12`, `BLG-FEAT-103` |
| EPIC-04 — First-Time-Right Checks | 7 | 3.70 | `BLG-GOV-422`, `BLG-QA-262`, `BLG-QA-260`, `BLG-QA-268`, `BLG-GOV-420`, `BLG-GOV-421`, `BLG-GOV-388` |
| EPIC-05 — Position Data Correctness | 7 | 6.65 | `BLG-BE-208`, `BLG-BE-213`, `BLG-BE-223`, `BLG-BE-179`, `BLG-BE-181`, `BLG-SPEC-203`, `BLG-FE-225` |
| EPIC-06 — Market-Data Reliability and CI | 7 | 2.55 | `BLG-OPS-217` (remainder, conditional), `BLG-FE-294`, `BLG-OPS-220`, `BLG-OPS-205`, `BLG-OPS-206`, `BLG-QA-225`, `BLG-QA-226` |
| EPIC-07 — AI Output Boundary | 2 | 1.00 | `BLG-AI-29`, `BLG-GOV-378` |

**Product mix:** 21 frontend and backend build items carry 17.70d (63% of effort), against v9.17's 93%. Skill-Silo was 60.2% at DL-089; all 7 U-items the rebalance named are seated.

**Scope-selection method:**
- Gate scan of 356 items: 94 gated, 0 date-lapsed, 13 gating-item-shipped (all kept gated), 3 explicitly ungated, 2 data-quality warnings.
- No §1.3a gate edits; `backlog.md` was not changed.
- The STEP 4 calibration ran on the whole pool, reading Scope and AC text: 9 raises, +5.35d, 4 seated.
- Ready pool: 233 items / 110.35 days. Selected: 40 items / 27.95 days.
- Ready-pool history row appended: gap 82.35d, Δ +19.60, rolling Δ +11.62, pool growing.

**Ungated backlog after this release:** 193 ready items, 82.40 days (≈2.9 releases at 28d), plus 20 held Phase 4 items (16.25d, v9.19) and 9 ungated items not yet ready (9.95d). Of 356 backlog items, 94 are gated.

**Deferred:**
- Phase 4 stages 3–4 (v9.19), held by §1.4c step 0.
- `BLG-TECH-21` (P2): dedicated-release constraint, v10.0.
- `BLG-FEAT-73` (P1, re-check due, needs a production read) and `BLG-FEAT-76`.
- `BLG-GOV-200`/`201` (no ACs), `BLG-GOV-178`, `BLG-GOV-408` (complete), `BLG-GOV-419` (remainder), `BLG-OPS-201` (after 2026-12-01).
- 193 further ready items (82.40d) on capacity grounds.

**Escalations:** none raised.

## Product Owner sign-off summary

**Gate edits:** none this run.

**Overrides:** `BLG-QA-260`, by your dated direction of 2026-11-12. The standing `BLG-TECH-21` deferral continues.

**Judgement calls recorded for confirmation:**
- `BLG-OPS-220` seated under step 1a by reading v9.17's closure, though its fields do not meet the step's literal test.
- `BLG-OPS-217` seated as its 0.25d remainder, classified conditional (report due on or after 2026-11-20).
- `BLG-GOV-422`'s 2026-11-13 extension restated as three ACs (+0.25d).

## Pre-sprint Planning Required Decisions

The following High-priority decision must be resolved before sprint planning seals (before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-05] ST-27 stock-split rule — the Strategy Rules & System Intent Owner records the direction of the `strategy_rules.md` rule (how a split adjusts entry, quantity, stop, ATR and R, and that a detected split suppresses stop-breach alerts until confirmed), dated, in `sprint_backlog.md`'s sign-off summary — Owner: Strategy Rules & System Intent Owner

**Design Gate:** **Required.** 17 stories carry observable UI ACs (ST-01–ST-04, ST-08–ST-17, ST-27, ST-30, ST-33). The Weekly Digest rewrite, the "Split detected" state and the rules-followed filter have no page-level design record yet; ST-07's `navigation.md`/`design_system.md` revisions go to the gate as drafts if not merged. **Do not invoke `plan sprint` until `run design-gate --cycle 2026-11-18__release-v9.18` has passed.**

**Publish Gate:** all conditions met:
- `open_escalations` is empty, with no blocking deferred escalations.
- `stage4_5_capacity_check` = pass; `stage5_5_cross_stage_integrity` = pass; `stage5_7` = not_applicable.
- `stage1_readiness` and `stage3_5_model_integrity` = pass.
- `plan_structured`, `plan_executable` and `backlog_committed` = true.

Result: `status = Validated`, `publish_eligible = true`.

**Locks:** `backlog_lock` was acquired at STEP 3.9, committed and released. `roadmap_lock` was acquired, committed and released. Both released cleanly.
