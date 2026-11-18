Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.18
Cycle: 2026-11-18__release-v9.18
Last Updated: 2026-11-18

# Release Plan — v9.18

## Readiness

Preflight (STEP -1) passed in full. The gate-by-gate record is in `run_manifest.md`. Notable items:
- **§-1.2:** cleared by the formal §3 section "v9.18 — Site Structure & Usability, Phase 4 (stages 1–2) and first-time-right", added by roadmap rebalance `2026-11-18__scheduled` (DL-089, STEP 8.1 Option (a)). 19 items are committed there.
- **§-1.6 SLA-breach check:** clear. No root `open_escalations` entry has `disposition: Open`. `ESC-EXEC-20260910-01` remains Deferred, outside this check.
- **v9.17 Carry-Forward:** #1 applied (`BLG-GOV-422`, `BLG-QA-262` by the P2 tier; `BLG-QA-260` by a dated PO override; `BLG-GOV-422`'s scope extension restated as ACs). #2 applied (`BLG-FE-294`). #3 done (the rebalance ran first). #4 not needed (`BLG-UX-08` done out of sprint, 2026-11-17).
- **§1.3a:** 0 date-lapsed items. 13 gating-item-shipped items, each read, all kept gated (b). No backlog edit this run.
- **Not-ready exclusions:** 9 ungated items, 9.95d (`run_manifest.md`). `BLG-FEAT-73` (P1) is due a re-check; it needs a production `trade_plans` count.

One story carries a `strategy_rules.md` write: ST-27's stock-split rule, approved by the Strategy Rules & System Intent Owner before the build (RISK-05). Two stories are §13 determinations (ST-39, ST-40), with their clauses cited in the slice. ST-32 is conditional on a production report not due before 2026-11-20 (§1.4b).

## Scope

40 S2-items across 7 EPICs, 27.95 estimated days. Full table: `docs/product/scope/scope--2026-11-18__release-v9.18-site-structure-phase-4.md`. Ready pool, selection method and every disposition: `run_manifest.md` Scope Construction.

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 — Site Structure & Usability Phase 4, Stage 1: Correct and Safe (build-and-ship) | S2-01–S2-06 | Head of Engineering; Frontend Specifications & UX Documentation Owner; Cybersecurity & Trust Lead | RISK-01, RISK-06 | ST-01 → ST-02 (same spec file); ST-03 → ST-04; ST-05 early |
| EPIC-02 — Site Structure & Usability Phase 4, Stage 2: Home Page and Navigation (build-and-ship) | S2-07–S2-13 | Head of UX & Design; Frontend Specifications & UX Documentation Owner; Head of Engineering | RISK-01, RISK-02 | ST-07 (specs) first; ST-07 → ST-08, ST-09 → ST-10 → ST-11 |
| EPIC-03 — Site Structure & Usability Phase 4, Stage 2: Weekly Review Loop (build-and-ship) | S2-14–S2-17 | Head of UX & Design; Metrics Definitions & Analytics Owner; Product Owner | RISK-01, RISK-03 | ST-14 → ST-15 + ST-16 → ST-17 |
| EPIC-04 — First-Time-Right Checks (Product Owner direction, 2026-11-12) | S2-18–S2-24 | Head of Specs Team; QA & Testing Owner; Head of Engineering | RISK-04 | ST-18 early in the sprint; ST-20 after EPIC-01's axe changes |
| EPIC-05 — Position Data Correctness | S2-25–S2-31 | Head of Engineering; Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner | RISK-05, RISK-03 | ST-25 → ST-26; ST-27 rule approval first |
| EPIC-06 — Market-Data Reliability and CI | S2-32–S2-38 | Infrastructure & Operations Owner; Head of Engineering; QA & Testing Owner | RISK-03, RISK-07 | ST-32 conditional (≥ 2026-11-20) → ST-33; ST-34 early, → ST-36; ST-29 → ST-38 |
| EPIC-07 — AI Output Boundary | S2-39–S2-40 | AI Compliance & Governance Officer; Product Owner; Backend Engineering Patterns Owner | RISK-03 | ST-39 ruling before code |

**EPIC-01–03 note:** the three build-and-ship EPICs deliver Phase 4 stages 1 and 2 in full (DL-089): the 15 programme items, plus two round-robin items placed beside the stories they touch: `BLG-FE-228` (Alert History values, with ST-03) and `BLG-SPEC-204` (the Digest figure EPIC-03 lays out). Stages 3 and 4 (v9.19) are held by §1.4c step 0. `BLG-SEC-46` (ST-05) decides whether a v9.20 access remedy is needed.

**EPIC-04 note:** the Product Owner's 2026-11-12 direction. ST-18's checks apply from v9.19's design gate onward.

**Build-and-ship share:** 21 frontend and backend build items, 17.70d (63% of effort), against v9.17's 93%. EPIC-01–03 lead the table (STEP 3 rotation advisory; DL-089 read Skill-Silo at 60.2%). All 7 U-items the rebalance named are seated.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01, EPIC-02, EPIC-03, EPIC-04 | Files edited across stories: Dashboard cards and `dashboard.md` (ST-09–ST-11), `navigation.md` and the command palette (ST-07, ST-08, ST-16), `WeeklyDigest.js` (ST-14–ST-17), `accessibility-axe-scan.spec.js` and `runAxeScan` (ST-01, ST-02, ST-20), Notification History (ST-03, ST-04). Several EPICs regenerate visual baselines. | Medium | In-EPIC orders are fixed in the slice. ST-34 (baseline workflow can push) lands early. Merges follow CLAUDE.md §8, including step 2a's per-file version check and step 2c's backlog integrity check. | null |
| RISK-02 | EPIC-02 | ST-07 must revise `navigation.md` and `design_system.md` before ST-08, ST-09 and ST-12's builds; the design gate needs those revisions or their drafts. | Medium | ST-07 is first in EPIC-02 and goes to the design gate as a draft if not merged. Head of UX & Design approval is dated in the story. | null |
| RISK-03 | EPIC-03, EPIC-05, EPIC-06, EPIC-07 | Production steps: ST-32's post-fix weekly report (not before 2026-11-20); ST-40's sample of real debriefs; ST-17's and ST-27's migrations at deploy; ST-35's staging write. The governed environment has staging access only. | Medium | Human-Delegation at sprint start (v9.11–v9.17 precedent). Code proceeds regardless. ST-32 is conditional (§1.4b). Post-merge ACs get tracking items at Sprint Planning STEP 6.2. | null |
| RISK-04 | EPIC-04 | Five governance-prompt edits in one EPIC (ST-18 `design_gate_prompt.md`; ST-21 and ST-22 `execution_prompt.md`; ST-23 `post_ship_closure.md` and `roadmap_prompt.md`), each with a CLAUDE.md §6 bump of `OPERATIONAL_GUIDE.md`. The prompts are near their size budgets (`post_ship_closure.md` is 74,592 bytes). | Medium | Commit in sequence on one branch, re-reading each Change Log's top row before bumping (§9.1). Run the prompt size budget check before each commit; ST-23 makes that check a hook. | null |
| RISK-05 | EPIC-05 | ST-27 adds a stock-split rule to `strategy_rules.md` (§12.3 change control): how a split adjusts entry, quantity, stop, ATR and R, and how a detected split suppresses stop-breach alerts until confirmed. A case (c) write. | High | **Must resolve before sprint planning seals:** the Strategy Rules & System Intent Owner records the rule's direction (dated) in `sprint_backlog.md`'s sign-off summary; the exact text is approved in the story. Listed in `cycle_summary.md`. | null |
| RISK-06 | EPIC-01 | ST-05's re-review may choose a remedy (access control, a narrower front-end key) that becomes a Large v9.20 change. | Low | The remedy is filed as its own item (AC 2) and is out of v9.18 scope; the roadmap already holds a conditional v9.20 row. | null |
| RISK-07 | EPIC-06 | ST-32 is conditional: if the post-fix report is late or still above 10% without a documented cause, the story returns to backlog. | Low | Classified conditional, not firm (§1.4b). 0.25d at risk. | null |

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` holds 0 active initiatives (CPS=N/A), so there are no pre-assigned bands. All figures are inline STEP 4 estimates under `workforce_capacity.md`'s precedence rule.

**STEP 4 calibration check, run on the whole ready pool before selection (v2.63), reading Scope and AC text (v2.71):** 9 raises, +5.35d. Four seated: `BLG-BE-223` (price-consumer sweep, M → L), `BLG-GOV-422` (PO scope extension), `BLG-SPEC-203` (staging verification) and `BLG-OPS-205` (carried). Five carried on unselected items.

| EPIC | Stories | Days |
|------|---------|------|
| EPIC-01 | 6 | 3.65 |
| EPIC-02 | 7 | 6.15 |
| EPIC-03 | 4 | 4.25 |
| EPIC-04 | 7 | 3.70 |
| EPIC-05 | 7 | 6.65 |
| EPIC-06 | 7 | 2.55 |
| EPIC-07 | 2 | 1.00 |
| **Total** | **40** | **27.95** |

Confirmed capacity band: **~24–28 working days** (`claude/roadmap/workforce_capacity.md`). 27.95 / 28.00 = **99.8% of the band's top edge**. That is within band, at the ceiling, per the explicit "use full capacity" instruction. One story (ST-32, 0.25d) is conditional; firm scope is 27.70d.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

No Phasing Recommendation subsection: the outcome is `pass`, not `warn`. Effort is spread wider than v9.17: the largest stories are ST-27 (3.5d) and ST-17 (2.5d); 29 of 40 stories are under one day, so per-story overhead (branch, review, DoQ) is the main schedule risk rather than any single build.

## Integrity Validation

### 3.5 Local Model Integrity

Each of the 40 S2-items maps to exactly one EPIC:
- S2-01…06 → EPIC-01
- S2-07…13 → EPIC-02
- S2-14…17 → EPIC-03
- S2-18…24 → EPIC-04
- S2-25…31 → EPIC-05
- S2-32…38 → EPIC-06
- S2-39…40 → EPIC-07

No item is unmapped or double-mapped. All 7 RISK-IDs declare a `Relates to` EPIC. The cross-EPIC order (ST-20 after EPIC-01's axe changes) runs one way, and the in-EPIC orders (ST-01 → ST-02; ST-03 → ST-04; ST-07 → ST-08/ST-09 → ST-10 → ST-11; ST-14 → ST-15/ST-16 → ST-17; ST-25 → ST-26; ST-32 → ST-33; ST-34 → ST-36; ST-29 → ST-38) contain no cycles.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

### 5.5 Cross-Stage Integrity

- All 40 S2-IDs map to an EPIC in the Execution Plan table: confirmed.
- The EPIC-IDs in `stage4_backlog_slice.md` and `stage4_issue_manifest.json` (EPIC-01 to EPIC-07) match the Execution Plan: confirmed.
- All RISK-IDs in the EPIC table (RISK-01 to RISK-07) appear in the Risk Register: confirmed.
- ST-01 to ST-40 in the slice match the issue manifest one to one (40 entries, same S2-ID order, same source IDs), and the source set equals the selection output: confirmed by script.
- No orphaned references.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
attributes.cross_stage_integrity: pass
```

### 5.7 Decision Record Integrity

Not applicable. This session raised no escalations (`artifacts.escalations = not_present`). `decisions--2026-11-18__release-v9.18.md` is present and populated.

```yaml
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.decisions_validated: not_applicable
```

## Publish Gate Evaluation

All STEP 6 conditions hold:
- This cycle's `open_escalations` is empty.
- There are no deferred escalations or `deferred_execution_blockers` for this cycle.
- `stage4_5_capacity_check` = pass; `stage5_5_cross_stage_integrity` = pass; `stage5_7` = not_applicable.
- `stage1_readiness` and `stage3_5_model_integrity` = pass.
- `plan_structured`, `plan_executable` and `backlog_committed` = true.
- The backlog and roadmap locks are released.

→ `status = Validated`, `publish_eligible = true`.

## Product Owner Sign-off Summary

- **Override:** `BLG-QA-260` seated by your 2026-11-12 direction (dated in `run_manifest.md`). The standing `BLG-TECH-21` deferral continues.
- **Judgement calls to confirm:** `BLG-OPS-220` seated under step 1a by reading v9.17's closure (its fields do not match the step's literal test); `BLG-OPS-217` seated as its remainder at 0.25d; `BLG-GOV-422`'s scope extension restated as three ACs (+0.25d).
- **Gate edits:** none.
- **For `groom backlog`:** stale `Provisional-Target` tags (21 × v9.17, 25 × v9.16, 40 × v9.15 in the pool); `BLG-OPS-220` and `BLG-GOV-419` need their tags set.
- **For the Product Owner:** `BLG-FEAT-73` (P1) is due a re-check against production `trade_plans` (third run raising it); it stays at 2 of 4 consecutive Option (a) dispositions (§1.4a.1).

## Pre-sprint Planning Required Decisions

RISK-05 (High, must resolve before the sprint planning seal) is carried into `cycle_summary.md`.
