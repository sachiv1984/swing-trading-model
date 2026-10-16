Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.13
Cycle: 2026-10-16__release-v9.13
Last Updated: 2026-10-16

# Release Plan — v9.13

## Readiness

Preflight (STEP -1) passed in full. The gate-by-gate record is in `run_manifest.md`. Notable items:
- **§-1.2:** cleared directly. `v9.13` has a roadmap section, added by rebalance `2026-10-16__scheduled` (STEP 8.1 Option (a), DL-086). It commits `BLG-FE-226` (P1), `BLG-FE-227` and `BLG-BE-182` (P2), and all three are seated.
- **§-1.6 SLA-breach check:** clear. All 24 root `open_escalations` entries are Resolved.
- **v9.12 closure outstanding actions:** all 7 rows in `closure_record.md` §6 were resolved on 2026-10-15, including the human confirmation of the v9.12 DoQ and PO sign-offs (Carry-Forward #3).
- **§1.3a:** 0 date-lapsed gates, so no gate edit was made and `backlog.md` was not changed by this run.
- **§1.3a gating-item-shipped list (first run under ST-40):** 25 items, each read. 5 Ops items whose only gate was a shipped item are treated as ungated this run (`BLG-OPS-18`, `-19`, `-23`, `-77`, `-85`); 1 is delivered (`BLG-FE-195`); 19 keep an unmet limb.

Several stories carry a ruling or decision as their first sub-step:
- ST-05: whether month-end rebalance exits enter §8.
- ST-06: reject or floor a stop at or below zero.
- ST-07: align `position_manager.py` with §6.3 or record an exception.
- ST-08: reject or flag the fixed Settings fields.
- ST-16, ST-17, ST-18: AI Compliance & Governance Officer sign-offs.
- ST-27: test-isolation decision.

Five stories may write `claude/strategy/strategy_rules.md` (ST-38 and ST-39 certainly; ST-05, ST-06 and ST-07 depending on their rulings). Sprint Execution may not write that file without explicit authorisation, so RISK-02 must resolve before the sprint planning seal.

Seven stories expect Human-Delegation for live environments, dashboards or live data: ST-02, ST-22, ST-28, ST-29, ST-30, ST-31 and ST-32 (RISK-01).

## Scope

40 S2-items across 6 EPICs, 28.00 estimated days. Full table: `docs/product/scope/scope--2026-10-16__release-v9.13.md`. Ready pool, selection method and every disposition: `run_manifest.md` Scope Construction.

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 — Exit Flow, Exit Reasons & Red Flag Journal (build-and-ship) | S2-01–S2-05 | Head of Engineering; Head of UX & Design; Strategy Rules & System Intent Owner | RISK-01, RISK-02, RISK-04 | ST-01 first (P1); ST-01 → ST-02 → ST-03; ST-01 before ST-23/ST-24 (cross-EPIC) |
| EPIC-02 — Stop, Sizing & Position Data Correctness | S2-06–S2-14 | Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner | RISK-02, RISK-03, RISK-04 | ST-06 and ST-07 rulings first; otherwise independent |
| EPIC-03 — AI Output Safety, Debrief & Chat | S2-15–S2-22 | AI Compliance & Governance Officer; Backend Engineering Patterns Owner | RISK-01, RISK-03, RISK-04 | ST-15 → ST-16 → ST-17 (shared ticker matching in `ai_service.py`); ST-20 → ST-21 (same file) |
| EPIC-04 — API Call Integrity & UI Rendering | S2-23–S2-27 | Director of Quality; API Contracts & Documentation Owner | RISK-04, RISK-05 | ST-23 and ST-24 after ST-01 (cross-EPIC); ST-23 → ST-24 |
| EPIC-05 — Operations, Cost & Platform | S2-28–S2-34 | Infrastructure & Operations Owner; FinOps & Resource Architect | RISK-01, RISK-04 | ST-30 → ST-31; ST-29 early (it restores staging deploys other stories verify against) |
| EPIC-06 — Governance & Spec Tooling | S2-35–S2-40 | Head of Specs Team; PMO Lead; Strategy Rules & System Intent Owner | RISK-02, RISK-04 | ST-35 → ST-36 (same script); ST-38 → ST-39 (one `strategy_rules.md` bump) |

**EPIC-01 note:** ST-01 (`BLG-FE-226`, P1) is the release's anchor. Since 2026-01-24 the home page's exit shortcut has called a route that does not exist, so no Monitor exit has ever been recorded. All three roadmap-committed items (DL-086) are in this EPIC.

**EPIC-04 note:** ST-23 and ST-24 are the follow-through on ST-01's defect class: they make CI fail on a frontend call to a missing route, statically and in Playwright.

**Build-and-ship share:** 15 U-shaped items, 8.60d (31% of effort), down from v9.12's 42%. The three Product-Owner-committed U-items from the §7.1 sustained-failure clause are seated. The share fell because §1.4c's P2-first step seats `BLG-QA-227` (3.5d, test infrastructure) and the round-robin seated 4.5d of Ops items that the gating-item-shipped check made ready. Recorded as Friction Item 2.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01, EPIC-03, EPIC-05 | Seven stories need access the governed environment lacks: a CHECK constraint and backfill on staging and production (ST-02), a live migration (ST-22), a real failed-run Telegram receipt (ST-28), Render dashboard deploy hooks and GitHub secrets (ST-29), live usage data (ST-30, ST-31) and a full-universe screener run (ST-32). | Medium | Human-Delegation at sprint start to the Infrastructure & Operations Owner or the Data Model & Domain Schema Owner, following the v9.11/v9.12 precedent. Code and docs proceed regardless. | null |
| RISK-02 | EPIC-01, EPIC-02, EPIC-06 | ST-38 and ST-39 edit `claude/strategy/strategy_rules.md`, and ST-05, ST-06 and ST-07 may. `execution_prompt.md` §7 forbids Sprint Execution writing that file. The v9.9 ST-20 edit was made on the user's explicit instruction. Several bumps to one file across three EPICs also risk a version collision. | High | **Must resolve before sprint planning seals.** The user and the Strategy Rules & System Intent Owner either authorise named `strategy_rules.md` writes for these stories, with one EPIC owning the bumps in order, or Sprint Planning reclassifies the edits as decision records with the text left for the owner to apply. Listed in `cycle_summary.md`. | null |
| RISK-03 | EPIC-02, EPIC-03 | Rulings are first sub-steps: ST-05 (§8 determination), ST-06 (stop floor), ST-07 (§6.3 alignment), ST-08 (reject or flag), ST-16/ST-17/ST-18 (AI compliance sign-offs) and ST-27 (test isolation). | Medium | Each ruling is a `delegated_decision` first sub-step. Defaults that need no strategy change exist for ST-07 (align the code) and ST-08 (400). | null |
| RISK-04 | EPIC-01, EPIC-02, EPIC-03, EPIC-04, EPIC-05, EPIC-06 | Shared files edited across EPICs: `openapi.yaml` (ST-08, ST-22, ST-28, possibly ST-10), the `routers/test.py` registry, `SystemStatus.js` fallback count and `SC-SS-01b` (ST-22, possibly ST-10), `data_model.md` (ST-02, ST-22), `metrics_definitions.md` (ST-02, ST-10, ST-11, ST-22) and `strategy_rules.md` (RISK-02). | Medium | Contract changes update `openapi.yaml` in the same commit (CLAUDE.md §2). Merges follow CLAUDE.md §8, including step 2a's per-file version check for `metrics_definitions.md` and `strategy_rules.md`, and step 2c's backlog integrity check. | null |
| RISK-05 | EPIC-04 | ST-24 is the largest story (3.5d after calibration): a suite-wide 404/405 fixture plus a sweep of 59 state-changing calls in 22 files. The fixture may expose further broken routes mid-sprint. | Medium | ST-24 runs after ST-01 and ST-23. Its AC (restated) files exposed defects as backlog items rather than fixing them inside the story. Sprint Planning may split it into the fixture and the sweep. | null |

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` holds 0 active initiatives (CPS=N/A, 18th consecutive rebalance), so there are no pre-assigned bands. All figures are inline STEP-4 estimates under `workforce_capacity.md`'s precedence rule.

**STEP 4 calibration check, run on the whole ready pool before selection (v2.63):** 8 raises (+4.35d):
- Seated: `BLG-SPEC-186` (CHECK constraint + live backfill, 1.0→1.5), `BLG-FE-208` (live migration, 0.5→1.0), `BLG-QA-227` (sweep of 59 calls in 22 files, 2.5→3.5) and `BLG-OPS-189` (Render dashboard + live staging run, 0.5→1.0).
- Unseated: `BLG-SPEC-196` (0.5→1.0), `BLG-SPEC-197` (0.15→0.5), `BLG-BE-166` (0.5→1.0) and `BLG-BE-186` (1.0→1.5).
- The raises changed the final pick: `BLG-GOV-387` seated in place of `BLG-BE-164`.

| EPIC | Stories | Days |
|------|---------|------|
| EPIC-01 | 5 | 5.50 |
| EPIC-02 | 9 | 2.75 |
| EPIC-03 | 8 | 3.10 |
| EPIC-04 | 5 | 6.25 |
| EPIC-05 | 7 | 8.50 |
| EPIC-06 | 6 | 1.90 |
| **Total** | **40** | **28.00** |

Confirmed capacity band: **~24–28 working days** (`claude/roadmap/workforce_capacity.md`). 28.00 / 28.00 = **100% of the band's top edge**: within band, at the ceiling, per the explicit "use full capacity" instruction.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

No Phasing Recommendation subsection: the outcome is `pass`, not `warn`.

## Integrity Validation

### 3.5 Local Model Integrity

Each of the 40 S2-items maps to exactly one EPIC:
- S2-01…05 → EPIC-01
- S2-06…14 → EPIC-02
- S2-15…22 → EPIC-03
- S2-23…27 → EPIC-04
- S2-28…34 → EPIC-05
- S2-35…40 → EPIC-06

No item is unmapped or double-mapped. All 5 RISK-IDs declare a `Relates to` EPIC. Every cross-EPIC dependency runs one way (ST-01 before ST-23/ST-24), so there are no cycles.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

### 5.5 Cross-Stage Integrity

- All 40 S2-IDs map to an EPIC in the Execution Plan table: confirmed.
- EPIC-IDs in `stage4_backlog_slice.md` and `stage4_issue_manifest.json` (EPIC-01–EPIC-06) match the Execution Plan: confirmed.
- All RISK-IDs in the EPIC table (RISK-01 to RISK-05) appear in the Risk Register: confirmed.
- ST-01–ST-40 in the slice match the issue manifest one to one (40 entries, same S2-ID order): confirmed by script.
- No orphaned references.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
attributes.cross_stage_integrity: pass
```

### 5.7 Decision Record Integrity

Not applicable. This session raised no escalations (`artifacts.escalations = not_present`). `decisions--2026-10-16__release-v9.13.md` is present and populated.

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

RISK-02 (High, must resolve before the sprint planning seal) is carried into `cycle_summary.md`. RISK-03's rulings are resolved inside the sprint as first sub-steps, so they do not gate the seal.
