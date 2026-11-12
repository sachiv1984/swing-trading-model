Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.17
Cycle: 2026-11-11__release-v9.17
Last Updated: 2026-11-11

# Release Plan — v9.17

## Readiness

Preflight (STEP -1) passed in full. The gate-by-gate record is in `run_manifest.md`. Notable items:
- **§-1.2:** cleared by the planned-release line in `current_roadmap.md` §1, "Next planned release: v9.17 — Site Structure & Usability, Phase 3", named by the Product Owner on 2026-11-11 (commit `c5e841cc`). The release's provisional content is DL-088's programme plan, Phase 3 row (§3). There is no §3 committed-items section, so the annotation goes on the §1 line, as at v9.14 and v9.16.
- **§-1.6 SLA-breach check:** clear. No root `open_escalations` entry has `disposition: Open`. `ESC-EXEC-20260910-01` remains Deferred, outside this check.
- **v9.16 Carry-Forward:** #1 (five P2 found defects) all seated. #2 applied: §1.4c step 1b (v2.74) seats Phase 3's P3 items, first use, no override. #3 is a `run roadmap` action, not taken before this run (advisory; see `run_manifest.md`). #4 applied: `BLG-BE-205` and `BLG-FE-254`'s TL-09/TL-10 remainder seated together (EPIC-04).
- **§1.3a:** 0 date-lapsed items. 14 gating-item-shipped items, each read, all kept gated (b). No backlog edit this run.
- **Not-ready exclusions:** 8 ungated items, 9.80d (`run_manifest.md`). `BLG-FEAT-73` (P1) is due a re-check (its 2026-11-09 hold has passed), but the check needs a production `trade_plans` count.

Two stories carry a decision as their first sub-step, both the Strategy Rules & System Intent Owner's: ST-12 (how the acknowledgement resets) and ST-19 (add the 2R threshold to `strategy_rules.md` §11, or reword the tooltip) (RISK-05).

ST-15 needs a production `api_call_log` read and a post-fix production weekly report. ST-09's migration and ST-11's backfill run against production at deploy (RISK-03).

## Scope

20 S2-items across 7 EPICs, 27.95 estimated days. Full table: `docs/product/scope/scope--2026-11-11__release-v9.17-site-structure-phase-3.md`. Ready pool, selection method and every disposition: `run_manifest.md` Scope Construction.

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 — Site Structure & Usability Phase 3: Positions Redesign (build-and-ship) | S2-01–S2-04 | Head of Engineering; Head of UX & Design | RISK-01 | ST-01 first; ST-01 → ST-02, ST-03; ST-04 last |
| EPIC-02 — Site Structure & Usability Phase 3: Journal & Performance Consolidation (build-and-ship) | S2-05–S2-07 | Head of Engineering; Head of UX & Design; Metrics Definitions & Analytics Canonical Owner | RISK-01, RISK-04 | ST-05 and ST-06 merge one after the other; ST-06 spec first |
| EPIC-03 — Site Structure & Usability Phase 3: Semantic Colour Token Sweep (build-and-ship) | S2-08 | Frontend Specifications & UX Documentation Owner; Head of Engineering | RISK-02 | Merges last, after every other UI EPIC (baselines) |
| EPIC-04 — Site Structure & Usability Phase 2 Completion: Stops Moved Group | S2-09–S2-10 | Head of Engineering; Backend Engineering Patterns Owner; Data Model & Domain Schema Owner | RISK-03 | ST-09 → ST-10 |
| EPIC-05 — Trade Plan Found Defects (v9.16 Carry-Forward) | S2-11–S2-14 | Head of Engineering; Frontend Specifications & UX Documentation Owner; Strategy Rules & System Intent Owner (consulted) | RISK-01, RISK-03, RISK-05, RISK-07 | ST-12 decision first; ST-12/ST-14 share `TradePlan.js` with ST-07 |
| EPIC-06 — Market-Data Reliability & Sizing Correctness | S2-15–S2-17 | Infrastructure & Operations Owner; Head of Engineering; FinOps & Resource Architect | RISK-03 | ST-15 → ST-16 |
| EPIC-07 — Governance, Strategy Copy & Drift Tooling | S2-18–S2-20 | Head of Specs Team; PMO Lead; Frontend Specifications & UX Documentation Owner; QA & Testing Owner | RISK-05, RISK-06 | ST-18 early; ST-19 decision first, lands on EPIC-01's `Positions.js` |

**EPIC-01–03 note:** the three build-and-ship EPICs deliver all of Site Structure & Usability Phase 3 (DL-088, ≈20.5d with `BLG-FE-260`'s 2.5d). After v9.17 only the Close-out phase (`BLG-UX-08`, v9.18) remains.

**EPIC-04 note:** finishes Phase 2. `BLG-FE-254` (v9.16 ST-06) shipped without its Stops moved group because `BLG-BE-205` was not seated; this EPIC seats both.

**Build-and-ship share:** 15 frontend and backend build items, 25.90d (93% of effort), against v9.16's 62%. EPIC-01–03 lead the table (STEP 3 rotation advisory; the last Skill-Silo reading was 68.1%, DL-088).

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01, EPIC-02, EPIC-05, EPIC-07 | Files edited across stories: `Positions.js` (ST-01–ST-04, ST-19), `TradePlan.js` (ST-07, ST-12, ST-14), the nav specs and command palette (ST-05, ST-06). | Medium | The in-EPIC orders are fixed in the slice. ST-19 lands on EPIC-01's version of `Positions.js`. Merges follow CLAUDE.md §8, including step 2a's per-file version check and step 2c's backlog integrity check. | null |
| RISK-02 | EPIC-03 | ST-08 is a sweep: 436 dark-only classes in 21 page files and 484 in 87 component files (grep, 2026-11-11), against 707 counted at filing. Its AC covers every routed page, so the component share may be in scope. It regenerates both themes' visual baselines. | Medium | Held at L with the count named (STEP 4). Sprint Planning confirms the boundary and, if needed, splits the component remainder into a follow-up item before the seal. EPIC-03 merges last. | null |
| RISK-03 | EPIC-04, EPIC-05, EPIC-06 | Production steps: ST-15's `api_call_log` breakdown and a post-fix weekly report (7 days after deploy); ST-09's migration and ST-11's backfill run against production. The governed environment has staging access only. | Medium | Human-Delegation at sprint start (v9.11–v9.16 precedent). Code proceeds regardless. ST-15 AC 2 is post-merge, with a tracking item at Sprint Planning STEP 6.2. The backfill is idempotent and tested on staging first. | null |
| RISK-04 | EPIC-02 | ST-06 writes a new Performance page spec inside the story, and the Metrics Definitions & Analytics Canonical Owner must confirm each KPI's definition. ST-05 and ST-06 both add redirects. | Medium | Spec is sub-step 1 and goes to the design gate if drafted in time, otherwise to the Head of UX & Design before the build. The KPI confirmation is a restated AC. ST-05 and ST-06 merge in sequence. | null |
| RISK-05 | EPIC-05, EPIC-07 | Two Strategy Rules & System Intent Owner decisions: ST-12 (clear the acknowledgement on change, or store it in the snapshot) and ST-19 (add the 2R Exit Zone threshold to `strategy_rules.md` §11, a case (c) write, or reword the tooltip). | High | **Must resolve before sprint planning seals:** the owner records both choices (dated) in `sprint_backlog.md`'s sign-off summary. If ST-19's choice is the §11 write, the owner confirms that AC line there. Listed in `cycle_summary.md`. | null |
| RISK-06 | EPIC-07 | ST-18 changes `release_planning_prompt.md` §1.3a and may extend the `ESC-CLOSE-20261007-01` ruling. | Low | Head of Specs Team confirms the extension in the story. CLAUDE.md §6 checklist applies. | null |
| RISK-07 | EPIC-05 | ST-12 overlaps unseated `BLG-FE-269` (P3), which covers the same reset in the shared panel plus auto-expand. | Low | ST-12 checks whether its change meets `BLG-FE-269`'s first AC and records it for `groom backlog`. | null |

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` holds 0 active initiatives (CPS=N/A), so there are no pre-assigned bands. All figures are inline STEP 4 estimates under `workforce_capacity.md`'s precedence rule.

**STEP 4 calibration check, run on the whole ready pool before selection (v2.63), reading Scope and AC text (v2.71):** 9 raises, +4.35d. Three are new: `BLG-BE-211` (backfill, seated), `BLG-OPS-217` (production diagnosis, seated) and `BLG-BE-210` (production count and migration). Six are carried, one of them seated (`BLG-BE-205`). One seated sweep is held with its count named: `BLG-FE-265` (RISK-02).

| EPIC | Stories | Days |
|------|---------|------|
| EPIC-01 | 4 | 7.50 |
| EPIC-02 | 3 | 9.50 |
| EPIC-03 | 1 | 3.50 |
| EPIC-04 | 2 | 2.00 |
| EPIC-05 | 4 | 2.90 |
| EPIC-06 | 3 | 2.00 |
| EPIC-07 | 3 | 0.55 |
| **Total** | **20** | **27.95** |

Confirmed capacity band: **~24–28 working days** (`claude/roadmap/workforce_capacity.md`). 27.95 / 28.00 = **99.8% of the band's top edge**. That is within band, at the ceiling, per the explicit "use full capacity" instruction. No story is conditional.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

No Phasing Recommendation subsection: the outcome is `pass`, not `warn`. Effort is concentrated in large build stories: ST-05, ST-06 and ST-08 (3.5d each), ST-01 and ST-07 (2.5d each) and ST-02 and ST-04 (2.0d each) carry 19.5d. 8 stories are under one day.

## Integrity Validation

### 3.5 Local Model Integrity

Each of the 20 S2-items maps to exactly one EPIC:
- S2-01…04 → EPIC-01
- S2-05…07 → EPIC-02
- S2-08 → EPIC-03
- S2-09…10 → EPIC-04
- S2-11…14 → EPIC-05
- S2-15…17 → EPIC-06
- S2-18…20 → EPIC-07

No item is unmapped or double-mapped. All 7 RISK-IDs declare a `Relates to` EPIC. The cross-EPIC orders (EPIC-03 last; ST-19 after EPIC-01) run one way, and the in-EPIC orders (ST-01 → ST-02/ST-03 → ST-04, ST-05 → ST-06, ST-09 → ST-10, ST-15 → ST-16) contain no cycles.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

### 5.5 Cross-Stage Integrity

- All 20 S2-IDs map to an EPIC in the Execution Plan table: confirmed.
- The EPIC-IDs in `stage4_backlog_slice.md` and `stage4_issue_manifest.json` (EPIC-01 to EPIC-07) match the Execution Plan: confirmed.
- All RISK-IDs in the EPIC table (RISK-01 to RISK-07) appear in the Risk Register: confirmed.
- ST-01 to ST-20 in the slice match the issue manifest one to one (20 entries, same S2-ID order, same source IDs), and the source set equals the selection output: confirmed by script.
- No orphaned references.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
attributes.cross_stage_integrity: pass
```

### 5.7 Decision Record Integrity

Not applicable. This session raised no escalations (`artifacts.escalations = not_present`). `decisions--2026-11-11__release-v9.17.md` is present and populated.

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

- **No override of the mechanical method this release**, apart from the standing `BLG-TECH-21` deferral. §1.4c step 1b seats Phase 3's P3 items, which v9.16 needed an override for.
- **Judgement calls to confirm:** `BLG-BE-205` seated by step 1b as a Phase 2 item (Phase 2 is unfinished until TL-09/TL-10 pass); `BLG-FE-254` seated as its remainder at 0.5d rather than its whole-item L estimate.
- **Gate edits:** none.
- **For `groom backlog`:** `BLG-FE-269` overlaps ST-12; `BLG-FE-224`/`BLG-FE-242` are superseded when ST-08 ships; 67 unseated pool items still carry stale `v9.16`/`v9.15` tags (closure §6 row 6).
- **For the Product Owner:** `BLG-FEAT-73` (P1) is due a re-check against production `trade_plans`; it stays at 2 of 4 consecutive Option (a) dispositions (§1.4a.1).

## Pre-sprint Planning Required Decisions

RISK-05 (High, must resolve before the sprint planning seal) is carried into `cycle_summary.md`.
