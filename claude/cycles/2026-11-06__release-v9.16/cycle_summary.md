Owner: Facilitator
Class: Operational Record (Class 3)
Status: Active
Design Gate Required: true
Last Updated: 2026-11-06 (created this run)
Lifecycle Guide: claude/charter/document_lifecycle_guide.md

---

# Cycle Summary — Release Planning 2026-11-06__release-v9.16

**Release:** v9.16 — Site Structure & Usability, Phase 2

**Run type:** Named release with no committed items, as at v9.14. The Product Owner named v9.16 after post-ship closure `2026-11-03__release-v9.15`. Its provisional content is DL-088's programme plan, Phase 2 row. This run sets the full scope.

**Anchor scope:**
- **Site Structure & Usability Phase 2, in full (EPIC-01–03, 16.75d with ST-05 and ST-10):** the job-based sidebar, parent and onward links, the Dashboard "Today" list, "Plan this" from Signals and Screener, suggested size on Trade Plan, and the first semantic colour tokens.
- **`BLG-OPS-214` (ST-11, P1):** rotate the Anthropic key, overdue since 2026-08-25. With `BLG-OPS-213` (ST-12, P2), stop shipping a key copy in the public Pages build.

**Capacity decision (explicit user instruction): "use full capacity".** Selection order:
0. §1.4c step 0 (first use) holds the 8 Phase 3 items for v9.17.
1. The P1 item and the 7 ready P2 items (13.40d).
2. The 3 Phase 2 P3 items, by Product Owner override (3.50d).
3. §1.4c step 1a's deferred lessons-learnt patch, `BLG-GOV-413` (0.15d).

These came to 17.05d. A category-balanced, oldest-first round-robin over P3/P4 filled the rest. Total: **27.95 estimated days, 99.8% of the top of the ~24–28 day band.**

**Scope:** 30 stories across 7 EPICs.

| EPIC | Items | Days | Sources |
|------|-------|------|---------|
| EPIC-01 — Phase 2: Navigation & Wayfinding | 4 | 6.00 | `BLG-FE-250`, `BLG-FE-251`, `BLG-FE-252`, `BLG-FE-253` |
| EPIC-02 — Phase 2: Today List & Signal-to-Entry Flow | 4 | 7.75 | `BLG-FE-271`, `BLG-FE-254`, `BLG-FE-255`, `BLG-FE-256` |
| EPIC-03 — Phase 2: Colour Tokens & Input Contrast | 2 | 3.00 | `BLG-FE-264`, `BLG-FE-223` |
| EPIC-04 — Anthropic Key Security & Operations Baselines | 5 | 1.10 | `BLG-OPS-214`, `BLG-OPS-213`, `BLG-OPS-197`, `BLG-OPS-198`, `BLG-OPS-199` |
| EPIC-05 — Backend Correctness, AI Ticker Check & Spec Debt | 8 | 1.20 | `BLG-BE-175`, `BLG-BE-176`, `BLG-BE-177`, `BLG-AI-27`, `BLG-AI-28`, `BLG-SPEC-195`, `BLG-SPEC-200`, `BLG-SPEC-201` |
| EPIC-06 — Arc 2 Retrospective | 4 | 6.50 | `BLG-QA-21`, `BLG-QA-22`, `BLG-QA-23`, `BLG-FE-39` |
| EPIC-07 — Governance Process | 3 | 2.40 | `BLG-GOV-413`, `BLG-GOV-26`, `BLG-GOV-198` |

**Product mix:** 13 frontend and backend build items carry 17.20d (62% of effort), against v9.15's 34%. Skill-Silo was 68.1% at DL-088.

**Scope-selection method:**
- Gate scan of 271 items: 99 gated, 0 date-lapsed, 19 gating-item-shipped, 5 explicitly ungated, 3 data-quality warnings.
- §1.3a gate edits: 5 PT-04/Arc 2 gates cleared (a) in place, under the backlog lock. This is the first run where the scan reads roadmap feature IDs. The other 14 gating-item-shipped items keep an unmet limb.
- The STEP 4 calibration ran on the whole pool, reading Scope and AC text: 6 raises, +2.85d, none seated. One AC-level sweep was held, with its count named.
- **§1.4c step 0:** 8 Phase 3 items held (20.50d), including P2 `BLG-FE-260`.
- **Product Owner override:** the 3 Phase 2 P3 items were seated (3.50d), displacing 7 round-robin items (3.55d).
- Ready pool: 159 items / 84.70 days. Selected: 30 items / 27.95 days.
- Ready-pool history row appended: gap 56.70d, Δ +9.20, rolling Δ +6.70, pool growing.

**Deferred:**
- Phase 3 (step 0 hold) and `BLG-UX-08` (gated).
- `BLG-BE-205`: Today list "Stops moved" data. ST-06 ships without that group.
- `BLG-OPS-195` (needs `BLG-OPS-197`'s baseline) and `BLG-OPS-201` (after 2026-12-01).
- `BLG-TECH-21` (P2): dedicated-release constraint, v10.0.
- `BLG-FEAT-73`/`76`: data-quality warnings; not re-checked before 2026-11-09.
- `BLG-OPS-48`, `BLG-AI-23` (split-achievability), `BLG-GOV-178`, `BLG-GOV-192` and `BLG-GOV-408`. See `run_manifest.md`.
- 129 further ready items (56.75d) on capacity grounds, including `BLG-GOV-399` and 27 items tagged `v9.16`.

**Escalations:** none raised.

## Product Owner sign-off summary

**Gate edits (informational, per §1.3a bound 6):**

| Item | Disposition | Evidence |
|------|-------------|----------|
| `BLG-FE-39` | Cleared (a) | PT-04 ✅ Shipped v6.1 (2026-06-23) |
| `BLG-QA-21` | Cleared (a) | PT-04 ✅ Shipped v6.1; Arc 2 ✅ Fully Complete (v3.1–v6.1) |
| `BLG-QA-22` | Cleared (a) | Same as `BLG-QA-21` |
| `BLG-QA-23` | Cleared (a) | PT-04 ✅ Shipped v6.1 |
| `BLG-GOV-26` | Cleared (a) | PT-04 ✅ Shipped v6.1; Arc 2 ✅ Fully Complete |

**Product Owner override (user decision in session, 2026-11-06):** `BLG-FE-251`, `252` and `253` are seated with the Phase 2 P2s so that Phase 2 ships complete in the release named for it.

## Pre-sprint Planning Required Decisions

The following High-priority decision must be resolved before sprint planning seals (before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-02] Strategy Rules & System Intent Owner confirmation, dated in `sprint_backlog.md`'s sign-off summary, of ST-05 AC 4: close the `strategy_rules.md` §4.2.1 Known deviation (v1.26, `BLG-FE-271`) as a documentation-only version under `execution_prompt.md` §7 case (c), once the fix ships. Alternatively, the owner rules that the closure goes to Post-Ship Closure STEP 5, and the AC is met by that routing note. A line without confirmation is void. — Owner: Strategy Rules & System Intent Owner

**Design Gate:** **Required.** 11 stories carry observable UI ACs (ST-01–ST-10, ST-12). ST-05 also changes the locked `trade-entry-pre-entry-checks` design record. **Do not invoke `plan sprint` until `run design-gate --cycle "2026-11-06__release-v9.16"` has passed.** `sprint_planning_pre_condition` blocks the seal otherwise.

**Publish Gate:** all conditions met:
- `open_escalations` is empty, with no blocking deferred escalations.
- `stage4_5_capacity_check` = pass; `stage5_5_cross_stage_integrity` = pass; `stage5_7` = not_applicable.
- `stage1_readiness` and `stage3_5_model_integrity` = pass.
- `plan_structured`, `plan_executable` and `backlog_committed` = true.

Result: `status = Validated`, `publish_eligible = true`.

**Locks:** `backlog_lock` was acquired before the §1.3a gate edits (v2.64), re-entered at STEP 3.9, committed and released. `roadmap_lock` was acquired, committed and released. Both released cleanly.
