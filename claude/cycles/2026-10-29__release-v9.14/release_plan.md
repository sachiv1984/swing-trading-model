Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.14
Cycle: 2026-10-29__release-v9.14
Last Updated: 2026-10-29

# Release Plan — v9.14

## Readiness

Preflight (STEP -1) passed in full. The gate-by-gate record is in `run_manifest.md`. Notable items:
- **§-1.2:** cleared by `current_roadmap.md` §1's planned-release line, "Next planned release: v9.14 — Named" (Product Owner direction DL-087). No items are committed. No scheduled rebalance ran before this run, although the even cycle count (90) advised one. DL-087 allows skipping it (Friction Item 3).
- **§-1.6 SLA-breach check:** clear. Every root `open_escalations` entry is Resolved.
- **v9.13 closure outstanding actions:** rows 1–5 were resolved on 2026-10-29, including the human confirmation of the v9.13 DoQ and PO sign-offs. Row 6 is actioned here: the three deferred lessons-learnt patches are seated by Product Owner override.
- **§1.3a:** 2 date-lapsed gates (`BLG-FEAT-58`, `BLG-BE-43`) were re-gated on the same PO-02 condition. The lapse was a false positive. The edits were made under the backlog lock.
- **§1.3a gating-item-shipped list:** 23 items, each read:
  - 3 are treated as ungated: `BLG-OPS-85`, `BLG-OPS-21`, `BLG-FEAT-99`.
  - 1 is delivered: `BLG-FE-195`.
  - 19 keep an unmet limb.
- **Explicitly-ungated items:** 17 items with `Gate criteria: None` are counted in the ready pool for the first time (`BLG-GOV-390`, v9.13).

Several stories carry a ruling or choice as their first sub-step:
- ST-03: what "regime unknown" means (Strategy Rules & System Intent Owner).
- ST-09: the FX convention confirmation.
- ST-15 and ST-17: AI Compliance & Governance Officer ruling changes.
- ST-45: option (a) or (b) (Head of Specs Team).

Three stories name `strategy_rules.md` sections under the standing case (c) rule: ST-03 (conditional), ST-09 and ST-22. Each needs the Strategy Rules & System Intent Owner's confirmation recorded at the sprint planning seal (RISK-02).

Six stories expect Human-Delegation for production data, live dashboards or human staging checks: ST-01, ST-23, ST-30, ST-39, ST-43, and ST-42 if a branch rule blocks the workflow (RISK-01).

## Scope

54 S2-items across 7 EPICs, 28.00 estimated days. Full table: `docs/product/scope/scope--2026-10-29__release-v9.14.md`. Ready pool, selection method and every disposition: `run_manifest.md` Scope Construction.

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 — Production Deploy & Market-Data Resilience (build-and-ship) | S2-01–S2-08 | Infrastructure & Operations Owner; Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner | RISK-01, RISK-02, RISK-03, RISK-06 | ST-01 first in the sprint (P1); ST-02 → ST-03 → ST-06; ST-04 → ST-05 → ST-06; ST-07 → ST-08 |
| EPIC-02 — Sizing, Exit & Position Correctness | S2-09–S2-14 | Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner | RISK-02, RISK-05 | ST-09 ruling first; ST-09 → ST-13; ST-10 before ST-29 (cross-EPIC) |
| EPIC-03 — AI Output Safety & Audit Hygiene | S2-15–S2-23 | AI Compliance & Governance Officer; Backend Engineering Patterns Owner | RISK-01, RISK-02, RISK-04, RISK-05 | ST-15 → ST-18; ST-16 → ST-17; ST-19 → ST-21; ST-23 last; ST-22 coordinates with ST-28 (cross-EPIC) |
| EPIC-04 — Reports, Dashboard & System Status UI (build-and-ship) | S2-24–S2-28 | Financial Reporting & Records Owner; Frontend Specifications & UX Documentation Owner | RISK-04 | ST-24 first; ST-26 → ST-27 |
| EPIC-05 — Test Coverage & Test Tooling | S2-29–S2-37 | Director of Quality; QA & Testing Owner | RISK-01, RISK-04 | ST-31 early; ST-29 after ST-10; ST-30 after ST-01; ST-36 late |
| EPIC-06 — Operations, Cost & Security | S2-38–S2-43 | Infrastructure & Operations Owner; FinOps & Resource Architect; Cybersecurity & Trust Lead | RISK-01 | ST-38 → ST-39 |
| EPIC-07 — Specs & Governance | S2-44–S2-54 | Head of Specs Team; PMO Lead; Metrics Definitions & Analytics Owner | RISK-04, RISK-05 | ST-44 → ST-45; ST-51 → ST-48 |

**EPIC-01 note:** ST-01 (`BLG-OPS-193`, P1) is the release's anchor. Production has not received a frontend build since 2026-10-15: v9.13's shipped UI is not live on GitHub Pages. ST-02–ST-06 close the data-provider assessment's fail-open paths, where a Yahoo outage silently gives a risk-on regime and FX frozen at 1.27, while System Status reports healthy.

**EPIC-03 note:** ST-23 draws the first live AI output sample. `BLG-AI-06`'s sampling hook has shipped, which is `ESC-EXEC-20260910-01`'s deferred trigger, so that escalation can be resolved or re-deferred with a reason.

**Build-and-ship share:** 21 U-shaped items, 9.70d (35% of effort), up from v9.13's 31%. EPIC-01 and EPIC-04 are build-and-ship and lead the table (STEP 3 rotation advisory; Skill-Silo was 69.6% at the last rebalance).

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01, EPIC-03, EPIC-05, EPIC-06 | Six stories need access the governed environment lacks: Render dashboard (ST-01, ST-43), production AI samples and cost data (ST-23, ST-39), a human staging pass in both themes (ST-30), and possibly a branch-rule bypass for a workflow commit (ST-42). | Medium | Human-Delegation at sprint start to the Infrastructure & Operations Owner, AI Compliance & Governance Officer or Director of Quality, following the v9.11–v9.13 precedent. Code and docs proceed regardless. | null |
| RISK-02 | EPIC-01, EPIC-02, EPIC-03 | ST-03 (§4.2.1/§8.2, if the ruling changes behaviour), ST-09 (§4.1.5 Known Deviations entry; §4.1.3 if ambiguous) and ST-22 (§13.5 roster row) write `strategy_rules.md` under case (c). Each write is void without the Strategy Rules & System Intent Owner's confirmation in the sealed sign-off summary. Three bumps in three EPICs also risk a version collision. | High | **Must resolve before sprint planning seals:** the Strategy Rules & System Intent Owner confirms each of the three AC lines (dated) in `sprint_backlog.md`'s sign-off summary. Bumps are taken in merge order, under CLAUDE.md §8 step 2a. Listed in `cycle_summary.md`. | null |
| RISK-03 | EPIC-01 | ST-02–ST-07 change overlapping code: `check_market_regime()`, `get_live_fx_rate()`, `health_service.py`, `position_service.py`. ST-05 (`BLG-BE-169`) and ST-04 (`BLG-BE-194`) both address the 1.27 fallback. | Medium | One EPIC, one branch, with the order fixed in the slice. ST-05's AC is restated to reuse ST-04's stored rate and age. | null |
| RISK-04 | EPIC-01, EPIC-02, EPIC-03, EPIC-04, EPIC-05, EPIC-07 | Files edited across EPICs: `openapi.yaml` (ST-05, ST-07, ST-10, ST-22), `SystemStatus.js` and `system-status.spec.js` (ST-22, ST-28), `ai_s13_boundary_test_suite.md` (ST-15, ST-18), `metrics_definitions.md` (ST-24, ST-48, ST-51) and `OPERATIONAL_GUIDE.md` (ST-44, ST-45). | Medium | Contract changes update `openapi.yaml` in the same commit (CLAUDE.md §2). Merges follow CLAUDE.md §8, including step 2a's per-file version check and step 2c's backlog integrity check. | null |
| RISK-05 | EPIC-01, EPIC-02, EPIC-03, EPIC-07 | Rulings or choices are first sub-steps: ST-03, ST-09, ST-15, ST-17 and ST-45. | Medium | Each is a `delegated_decision` first sub-step. ST-09's fix is needed whatever the ruling (the inversion is arithmetic), and ST-45's two options are both pre-specified. | null |
| RISK-06 | EPIC-01 | ST-01's root cause is inferred for production: the failed `deploy.yml` logs have expired. The production build may fail for a second reason once the ESLint config is restored. | Medium | ST-01 runs first. Its CI step runs the real production build on every PR, so a second cause surfaces before merge. The production AC is post-merge, with a tracking item. | null |

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` holds 0 active initiatives (CPS=N/A), so there are no pre-assigned bands. All figures are inline STEP-4 estimates under `workforce_capacity.md`'s precedence rule.

**STEP 4 calibration check, run on the whole ready pool before selection (v2.63):** 8 raises, +3.85d. Two are seated:
- `BLG-OPS-193`: production deploy plus Render dashboard, 0.5→1.0.
- `BLG-BE-166`: `ensure_*` sweep, 0.5→1.0.

Six are unseated: `BLG-TECH-25`, `BLG-SPEC-196`, `BLG-SPEC-197`, `BLG-BE-186`, `BLG-SPEC-206` and `BLG-SPEC-208`. The raises did not change the final pick.

| EPIC | Stories | Days |
|------|---------|------|
| EPIC-01 | 8 | 4.15 |
| EPIC-02 | 6 | 2.30 |
| EPIC-03 | 9 | 3.60 |
| EPIC-04 | 5 | 2.60 |
| EPIC-05 | 9 | 4.50 |
| EPIC-06 | 6 | 4.05 |
| EPIC-07 | 11 | 6.80 |
| **Total** | **54** | **28.00** |

Confirmed capacity band: **~24–28 working days** (`claude/roadmap/workforce_capacity.md`). 28.00 / 28.00 = **100% of the band's top edge**. That is within band, at the ceiling, per the explicit "use full capacity" instruction.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

No Phasing Recommendation subsection: the outcome is `pass`, not `warn`. 54 stories is the most of any release so far (v9.12: 48). 22 are under half a day and 42 are half a day or less, so the count reflects small items, not extra days.

## Integrity Validation

### 3.5 Local Model Integrity

Each of the 54 S2-items maps to exactly one EPIC:
- S2-01…08 → EPIC-01
- S2-09…14 → EPIC-02
- S2-15…23 → EPIC-03
- S2-24…28 → EPIC-04
- S2-29…37 → EPIC-05
- S2-38…43 → EPIC-06
- S2-44…54 → EPIC-07

No item is unmapped or double-mapped. All 6 RISK-IDs declare a `Relates to` EPIC. The cross-EPIC dependencies (ST-10 before ST-29, ST-01 before ST-30) run one way. ST-22 and ST-28 are a coordination point, not a dependency. There are no cycles.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

### 5.5 Cross-Stage Integrity

- All 54 S2-IDs map to an EPIC in the Execution Plan table: confirmed.
- The EPIC-IDs in `stage4_backlog_slice.md` and `stage4_issue_manifest.json` (EPIC-01 to EPIC-07) match the Execution Plan: confirmed.
- All RISK-IDs in the EPIC table (RISK-01 to RISK-06) appear in the Risk Register: confirmed.
- ST-01 to ST-54 in the slice match the issue manifest one to one (54 entries, same S2-ID order): confirmed by script.
- No orphaned references.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
attributes.cross_stage_integrity: pass
```

### 5.7 Decision Record Integrity

Not applicable. This session raised no escalations (`artifacts.escalations = not_present`). `decisions--2026-10-29__release-v9.14.md` is present and populated.

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
- The backlog and roadmap locks are released.

→ `status = Validated`, `publish_eligible = true`.

## Pre-sprint Planning Required Decisions

RISK-02 (High, must resolve before the sprint planning seal) is carried into `cycle_summary.md`. RISK-05's rulings are resolved inside the sprint as first sub-steps, so they do not gate the seal.
