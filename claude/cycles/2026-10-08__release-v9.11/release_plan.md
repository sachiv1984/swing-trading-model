Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.11
Cycle: 2026-10-08__release-v9.11
Last Updated: 2026-10-08

# Release Plan — v9.11

## Readiness

Preflight (STEP -1) passed in full. The gate-by-gate record is in `run_manifest.md`. Notable items:
- **§-1.2:** cleared directly. The first attempt this session halted because `v9.11` had no roadmap section and the only Option (b) record was already used up by v9.10. The user directed "do what is needed", so a scheduled rebalance (`2026-10-08__scheduled`, DL-084) ran first. It added a `v9.11` Now-horizon section with 4 committed items.
- **§-1.6 SLA-breach check:** clear. Every root `open_escalations` entry is Resolved.
- **§1.3a:** all 6 date-lapsed gates were read and re-gated in place on their same conditions, within the `ESC-CLOSE-20261007-01` bounds (`release_planning_prompt.md` v2.60). This was the first run to use the carve-out. The edits are listed in `run_manifest.md` and in the Product Owner sign-off summary in `cycle_summary.md`.

Several items carry a ruling or sign-off as part of their own scope:
- ST-01: Condition 2 sign-off.
- ST-16: in-grace ruling.
- ST-25: §13 confirmation.
- ST-34: `BLG-GOV-339` sign-off.

Each is phased as the story's first sub-step (RISK-01, RISK-05, RISK-06, RISK-07). Four stories expect Human-Delegation for live environments: ST-02, ST-06, ST-20 and ST-42 (RISK-02, RISK-03, RISK-08).

## Scope

43 S2-items across 6 EPICs, 27.975 estimated days. Full table: `docs/product/scope/scope--2026-10-08__release-v9.11.md`. Ready pool, selection method and every disposition: `run_manifest.md` Scope Construction.

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 — Post-Trade Debrief & AI Reliability | S2-01–S2-09 | Backend Engineering Patterns Owner; AI Compliance & Governance Officer | RISK-01, RISK-02, RISK-03 | ST-01's Condition 2 sign-off first; ST-03 before ST-04; ST-07 → ST-08 → ST-09 (same prompt/call sites) |
| EPIC-02 — Risk & Position Display Correctness (build-and-ship) | S2-10–S2-15 | Head of Engineering; Head of UX & Design | RISK-04 | ST-10 first (adds the `GET /portfolio` field ST-13 extends); ST-11 after ST-10; ST-13 after ST-10/ST-11 |
| EPIC-03 — Strategy, Records & Alert Integrity | S2-16–S2-22 | Head of Engineering; Strategy Rules & System Intent Owner | RISK-05, RISK-03 | ST-16's ruling first; ST-17 after ST-16 |
| EPIC-04 — AI Narrative & Engagement Measurement (build-and-ship) | S2-23–S2-28 | Financial Reporting & Records Owner; Metrics Definitions & Analytics Owner | RISK-06 | ST-23 and ST-24 before ST-25; ST-26 after ST-25 |
| EPIC-05 — Spec & Contract Hygiene | S2-29–S2-32 | API Contracts & Documentation Owner; Data Model & Domain Schema Owner | RISK-04 | ST-30 after ST-06/ST-17/ST-20 add columns (cross-EPIC) |
| EPIC-06 — Governance, QA & Ops Hygiene | S2-33–S2-43 | Head of Specs Team; QA & Testing Owner; Infrastructure & Operations Owner | RISK-07, RISK-08 | ST-36 early; ST-41 before ST-39; ST-35 ideally before ST-25's §13 confirmation (cross-EPIC) |

**EPIC-01 note:** ST-01 (`BLG-BE-152`, P1) is the Correctness Fast-Track item. In production, the debrief called a correct profitable trailing-stop exit a contradiction. ST-02 (`BLG-BE-150`, P1) verifies that every AI feature recovered after an escaped defect that broke AI generation from v9.4 to v9.10.

**EPIC-02 / EPIC-04 note:** build-and-ship scope comes first. The roadmap-committed `BLG-BE-154`/`BLG-FE-206` plus `BLG-BE-153`/`BLG-BE-155`/`BLG-BE-147`/`BLG-FE-204` (EPIC-02), `BLG-FEAT-59` (EPIC-04), and EPIC-01's `BLG-BE-152`/`BLG-FE-205` make 9 U-items worth 8.275d (30% of effort). This answers the Skill-Silo reading (87.4%, above ceiling) and the 7th consecutive PVR Alert.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | ST-01 passes code-derived figures (R achieved, stop at exit) to the model. Whether that still meets Condition 2 of the debrief §13 review (`decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`) is the AI Compliance & Governance Officer's call. | High | The sign-off is ST-01's first sub-step, before the prompt change. Resolved within the sprint; does not block the seal. | null |
| RISK-02 | EPIC-01 | ST-02 needs all six AI features exercised on a staging deploy with a working Anthropic key. The governed environment cannot do this alone. | Medium | Human-Delegation to the Infrastructure & Operations Owner at sprint start. The debrief's 2026-10-07 production verification is already recorded. | null |
| RISK-03 | EPIC-01, EPIC-03 | ST-06, ST-20 and possibly ST-17 need live schema migrations on staging and production. | Medium | Human-Delegation to the Data Model & Domain Schema Owner with the Infrastructure & Operations Owner, following the DS-17 precedent (`ESC-EXEC-20260921-04`). Code and `data_model.md` proceed regardless. | null |
| RISK-04 | EPIC-02, EPIC-05 | ST-10 and ST-13 both extend the `GET /portfolio` contract. ST-19 adds an endpoint, and ST-31 edits `openapi.yaml`. These are shared-file edits across three EPICs. | Medium | ST-10 lands first within EPIC-02. Every contract change updates `openapi.yaml` in the same commit (CLAUDE.md §2). Cross-EPIC merges follow CLAUDE.md §8 (union of paths, highest version). | null |
| RISK-05 | EPIC-03 | ST-16 needs a Strategy Rules & System Intent Owner ruling (`delegated_decision`) that may touch `strategy_rules.md` §6.3. ST-19 adds a new endpoint with the CLAUDE.md §2 registration chain. | Medium | Ruling first, and any `strategy_rules.md` edit is under that owner's explicit authority. ST-19's AC lists every registration step. | null |
| RISK-06 | EPIC-04 | ST-25 adds AI-generated narrative to a financial report. Its §13 standing must be confirmed before build, not discovered at sign-off (the `BLG-GOV-359` gap-risk lesson). | High | **Must resolve before sprint planning seals.** The Strategy Rules & System Intent Owner confirms whether ST-25 sits within SRB-v1.7's advisory classification or needs its own §13 review. If a review is needed, ST-25 is re-scoped to a pre-assessment at sprint planning. Listed in `cycle_summary.md`. | null |
| RISK-07 | EPIC-06 | ST-33, ST-35 and ST-36 edit governance prompts or templates. ST-34 writes `claude/roadmap/product_value_ratio_history.md` and changes `roadmap_prompt.md` STEP 2.4. | Medium | ST-34 is classified `delegated_decision` under the named-file rule (`ESC-CLOSE-20261006-01`). Its prompt change waits for `BLG-GOV-339`'s Head of Specs Team + Product Owner sign-off. Every prompt edit runs the CLAUDE.md §6 checklist and the §8 step 2a per-file version-collision check. | null |
| RISK-08 | EPIC-06 | ST-42 needs repository admin access to change branch protection. | Low | Human-Delegation to the Infrastructure & Operations Owner. | null |
| RISK-09 | Release-level | 43 stories is the joint-highest count since v9.5. Per-story overhead (commits, QA evidence, DoQ blocks) is higher than the day estimate suggests. | Medium | 20 stories are XS/≤0.5d and grouped by file. Sprint Planning may split the release into 2 sprints along EPIC lines (EPIC-01/02/03, then EPIC-04/05/06). | null |

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` holds 0 active initiatives, so there are no pre-assigned bands. All figures are inline STEP-4 estimates under `workforce_capacity.md`'s precedence rule.

**ST-35 calibration check:**
- Raised `BLG-AI-08` (live migration, +0.5d) and `BLG-OPS-175` (live migration, XS→S).
- Held `BLG-BE-150` (6 features named), `BLG-BE-142` (4 files named), `BLG-BE-153` (3 readers named) and `BLG-QA-217` (an automated all-module import, so the count is not material).

| EPIC | Stories | Days |
|------|---------|------|
| EPIC-01 | 9 | 6.75 |
| EPIC-02 | 6 | 4.775 |
| EPIC-03 | 7 | 4.55 |
| EPIC-04 | 6 | 4.90 |
| EPIC-05 | 4 | 1.80 |
| EPIC-06 | 11 | 5.20 |
| **Total** | **43** | **27.975** |

Confirmed capacity band: **~24–28 working days** (`claude/roadmap/workforce_capacity.md`, held at `2026-10-08__scheduled`). 27.975 / 28.00 = **99.9% of the band's top edge**: within band, at the ceiling, per the explicit "full capacity" instruction.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

No Phasing Recommendation subsection: the outcome is `pass`, not `warn`. RISK-09's optional two-sprint split is advisory.

## Integrity Validation

### 3.5 Local Model Integrity

Each of the 43 S2-items maps to exactly one EPIC:
- S2-01…09 → EPIC-01
- S2-10…15 → EPIC-02
- S2-16…22 → EPIC-03
- S2-23…28 → EPIC-04
- S2-29…32 → EPIC-05
- S2-33…43 → EPIC-06

No item is unmapped or double-mapped. All 9 RISK-IDs declare a `Relates to` EPIC or Release-level. Every cross-EPIC dependency points from a later-sequenced story to an earlier one (ST-30 after ST-06/17/20; ST-25 after ST-35, advisory), so there are no cycles.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

### 5.5 Cross-Stage Integrity

- All 43 S2-IDs map to an EPIC in the Execution Plan table: confirmed.
- EPIC-IDs in `stage4_backlog_slice.md` and `stage4_issue_manifest.json` (EPIC-01–EPIC-06) match the Execution Plan: confirmed.
- All RISK-IDs in the EPIC table (RISK-01 to RISK-08) appear in the Risk Register; RISK-09 is Release-level: confirmed.
- ST-01–ST-43 in the slice match the issue manifest one to one (43 entries, same S2-ID order): confirmed by script.
- No orphaned references.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
attributes.cross_stage_integrity: pass
```

### 5.7 Decision Record Integrity

Not applicable. This release-planning session raised no escalations (`artifacts.escalations = not_present`). The rebalance's `ESC-RB-20261008-01` belongs to that cycle and is Resolved. `decisions--2026-10-08__release-v9.11.md` is present and populated.

```yaml
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.decisions_validated: not_applicable
```

## Publish Gate Evaluation

All STEP 6 conditions hold:
- This cycle's `open_escalations` is empty.
- There are no deferred escalations or `deferred_execution_blockers`.
- `stage4_5_capacity_check` = pass; `stage5_5_cross_stage_integrity` = pass; `stage5_7` = not_applicable.
- `stage1_readiness` and `stage3_5_model_integrity` = pass.
- `plan_structured`, `plan_executable` and `backlog_committed` = true.
- Backlog and roadmap locks are released.

→ `status = Validated`, `publish_eligible = true`.

## Pre-sprint Planning Required Decisions

RISK-06 (High, must resolve before the sprint planning seal) is carried into `cycle_summary.md`. RISK-01 is High but is resolved inside the sprint as ST-01's first sub-step, so it does not gate the seal.
