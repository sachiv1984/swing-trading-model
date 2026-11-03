Owner: Facilitator
Class: Operational Record (Class 3)
Status: Active
Design Gate Required: true
Last Updated: 2026-11-03 (created this run)
Lifecycle Guide: claude/charter/document_lifecycle_guide.md

---

# Cycle Summary — Release Planning 2026-11-03__release-v9.15

**Release:** v9.15 — Site Structure & Usability, Phase 1

**Run type:** Roadmap-committed. Roadmap rebalance `2026-11-03__scheduled` (DL-088) added a §3 section for v9.15 that commits 10 items and records a provisional four-phase programme (v9.15–v9.18) from the Head of UX & Design website review. This run sets the rest of the scope.

**Anchor scope:** `BLG-FE-244` (ST-01, P1) and `BLG-FE-245` (ST-02, P1), both STEP 8.0 Correctness Fast-Track promotions:
- Three routes into Trade Entry skip the §4.2 pre-entry checks, including §4.2.1 unknown regime.
- The FX field pre-fills a fixed 1.27, which distorts US sizing because it scales with FX².

**Capacity decision (explicit user instruction): "use full capacity".** Selection order:
1. The 10 DL-088 committed items (12.25d).
2. The other ready P2 items (1.65d).
3. §1.4c step 1a's two deferred lessons-learnt patches (0.65d), the first use of step 1a.

These came to 14.55d. A category-balanced, oldest-first round-robin over P3/P4 filled the rest. Total: **28.00 estimated days, 100% of the top of the ~24–28 day band.**

**Scope:** 45 stories across 7 EPICs.

| EPIC | Items | Days | Sources |
|------|-------|------|---------|
| EPIC-01 — Trade Entry Integrity & Sizing | 7 | 5.05 | `BLG-FE-244`, `BLG-FE-245`, `BLG-FE-246`, `BLG-FE-243`, `BLG-FE-222`, `BLG-BE-173`, `BLG-FE-219` |
| EPIC-02 — Site Structure & Usability Phase 1 | 7 | 8.50 | `BLG-SPEC-214`, `BLG-SPEC-215`, `BLG-SPEC-216`, `BLG-FE-248`, `BLG-FE-247`, `BLG-FE-249`, `BLG-FE-266` |
| EPIC-03 — Metric & Display Correctness | 9 | 2.40 | `BLG-FE-239`, `BLG-FE-240`, `BLG-FE-218`, `BLG-FE-220`, `BLG-BE-170`, `BLG-BE-171`, `BLG-BE-172`, `BLG-BE-174`, `BLG-SPEC-198` |
| EPIC-04 — AI Output Checks & §13 Boundary | 5 | 2.20 | `BLG-AI-23`, `BLG-AI-24`, `BLG-AI-25`, `BLG-AI-26`, `BLG-GOV-194` |
| EPIC-05 — Operations, Security & Market-Data Monitoring | 5 | 2.15 | `BLG-OPS-48`, `BLG-OPS-190`, `BLG-OPS-191`, `BLG-OPS-192`, `BLG-OPS-197` |
| EPIC-06 — Data Model & Spec Debt | 3 | 2.00 | `BLG-SPEC-194`, `BLG-SPEC-196`, `BLG-SPEC-197` |
| EPIC-07 — QA & Governance Tooling | 9 | 5.70 | `BLG-GOV-404`, `BLG-QA-240`, `BLG-QA-220`, `BLG-QA-221`, `BLG-QA-222`, `BLG-QA-224`, `BLG-GOV-193`, `BLG-GOV-195`, `BLG-GOV-196` |

**Product mix:** 19 frontend and backend build items carry 9.45d (34% of effort), against v9.14's 35%. A further 6.00d of design specs (ST-08–ST-10) feeds v9.16/v9.17's build phases. Skill-Silo was 68.1% at DL-088.

**Scope-selection method:**
- Gate scan of 287 items: 101 gated, 1 date-lapsed, 20 gating-item-shipped, 10 explicitly ungated, 2 data-quality warnings, 5 already-resolved.
- §1.3a gate edit: `BLG-OPS-48` cleared (a), under the backlog lock.
- 18 gating-item-shipped items keep an unmet limb, and `BLG-FE-195` is already ✅ COMPLETE. `BLG-GOV-400`'s check is met by this reading.
- The STEP 4 calibration ran on the whole pool before selection: 6 raises, +2.70d, 2 of them on seated items. Two AC-level sweeps were held, with counts named.
- **Product Owner override:** the Phase 2/3 programme items are held to v9.16/v9.17 (10 items, 20.00d).
- Ready pool: 148 items / 75.55 days. Selected: 45 items / 28.00 days.
- Ready-pool history row appended: gap 47.55d, Δ −6.00 (mostly the held items), rolling Δ +6.93, pool growing.

**Deferred:**
- The Phase 2/3 programme items (PO override); `BLG-FE-250`–`252`, `254`, `258`, `265` (depend on unshipped specs or items).
- `BLG-OPS-195` (needs `BLG-OPS-197`'s baseline) and `BLG-OPS-201` (needs a month of data, after 2026-12-01).
- `BLG-TECH-21` (P2): dedicated-release constraint, v10.0.
- `BLG-FEAT-73`/`76`: data-quality warnings; not re-checked before 2026-11-09.
- `BLG-GOV-185`, `BLG-GOV-192`, `BLG-GOV-400`, `BLG-OPS-203`, `BLG-FE-195`: already met, resolved or delivered. Archive at the next `groom backlog`.
- 103 further ready items (47.55d) on capacity grounds, including `BLG-GOV-399` and 43 items tagged `v9.15`.

**Escalations:** none raised.

## Product Owner sign-off summary

**Gate edit (informational, per §1.3a bound 6):**

| Item | Disposition | Evidence |
|------|-------------|----------|
| `BLG-OPS-48` | Cleared (a) | `BLG-OPS-36` shipped at v4.2 (2026-05-28); the gate's "no earlier than 2026-11-01" limb has passed. |

**Product Owner override (user decision in session, 2026-11-03):** the Site Structure & Usability Phase 2/3 items are held to their DL-088 provisional releases rather than seated by §1.4c's P2-first step. These are `BLG-FE-255`, `256`, `260`, `264` (P2) and `BLG-FE-253`, `257`, `259`, `261`, `262`, `263` (P3), 20.00d.

## Pre-sprint Planning Required Decisions

The following High-priority decision must be resolved before sprint planning seals (before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-03] Strategy Rules & System Intent Owner confirmation, dated in `sprint_backlog.md`'s sign-off summary, of ST-28 AC 3: a §13 clarification written under `execution_prompt.md` §7 case (c) if the re-read finds the boundary language ambiguous. Alternatively, the owner rules that no §13 write is authorised this sprint, and any clarification is then filed as a backlog item. A line without confirmation is void, and the story raises a `delegated_decision` instead. — Owner: Strategy Rules & System Intent Owner

**Design Gate:** **Required.** 14 stories carry observable UI ACs (ST-01–ST-04, ST-06, ST-07, ST-11–ST-18), and ST-08–ST-10 are design specs for review. **Do not invoke `plan sprint` until `run design-gate --cycle "2026-11-03__release-v9.15"` has passed.** `sprint_planning_pre_condition` blocks the seal otherwise.

**Publish Gate:** all conditions met:
- `open_escalations` is empty, with no blocking deferred escalations.
- `stage4_5_capacity_check` = pass; `stage5_5_cross_stage_integrity` = pass; `stage5_7` = not_applicable.
- `stage1_readiness` and `stage3_5_model_integrity` = pass.
- `plan_structured`, `plan_executable` and `backlog_committed` = true.

Result: `status = Validated`, `publish_eligible = true`.

**Locks:** `backlog_lock` was acquired before the §1.3a gate edit (v2.64), re-entered at STEP 3.9, committed and released. `roadmap_lock` was acquired, committed and released. Both released cleanly.
