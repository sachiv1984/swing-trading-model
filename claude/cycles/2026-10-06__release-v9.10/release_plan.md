Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.10
Cycle: 2026-10-06__release-v9.10
Last Updated: 2026-10-06

# Release Plan — v9.10

## Readiness

Preflight (STEP -1) passed in full. The gate-by-gate record is in `run_manifest.md`. Notable items:
- §-1.2: `v9.10` has its own Now-horizon roadmap section (rebalance `2026-10-06__scheduled`, DL-083), so it cleared directly. No Option(b) record was needed.
- §-1.6 SLA-breach check: clear. 1 open root escalation (`ESC-CLOSE-20261006-01`, Head of Specs Team) is due 2026-10-09 and has not breached. It affects this release (RISK-03).
- §-1.5 carry-forward: 3 items from v9.9 closure, all acted on (`BLG-FE-193` seated, `BLG-GOV-368` not re-seated, escalation recorded as RISK-03).

Four items need a ruling as part of their own scope (ST-01, ST-05, ST-11, ST-13). Each ruling is phased as the story's first sub-step (RISK-01, RISK-02).

## Scope

21 S2-items across 4 EPICs, 27.90 estimated days. Full table: `docs/product/scope/scope--2026-10-06__release-v9.10.md`. Ready pool, selection method and every disposition: `run_manifest.md` Scope Construction.

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 — Stop-Parameter Correctness & ATR Integrity | S2-01–S2-05 | Head of Engineering; Strategy Rules & System Intent Owner | RISK-01 | ST-01's ruling is the release's first sub-step; ST-02 and ST-03 follow ST-01 |
| EPIC-02 — Stop & Exit Transparency | S2-06–S2-10 | Frontend Specifications & UX Documentation Owner; Head of UX & Design | RISK-05 | ST-06 and ST-07 after ST-01's ruling (cross-EPIC); ST-09 after ST-08 |
| EPIC-03 — Lifecycle & Gap-Risk Strategy Boundary | S2-11–S2-14 | Strategy Rules & System Intent Owner; Head of Engineering | RISK-02 | ST-13 before ST-14; ST-11 before ST-12's post-grace work |
| EPIC-04 — AI Governance, Ops & QA Hygiene | S2-15–S2-21 | AI Compliance & Governance Officer; Infrastructure & Operations Owner | RISK-03, RISK-04 | ST-20 waits on `ESC-CLOSE-20261006-01`'s ruling for its roadmap AC |

EPIC-01 note: ST-01 (`BLG-BE-138`, P1) is the Correctness Fast-Track item. A live stop can currently differ from `strategy_rules.md` §7.2.
EPIC-02 note: four build-and-ship items, two of them roadmap-committed (`BLG-FE-193`, `BLG-FE-198`). With EPIC-01's `BLG-BE-138`/`BLG-BE-139` and EPIC-03's `BLG-BE-136`/`BLG-FE-196`, the release puts 8 U-items (19.25d, 69%) first. This is this cycle's execution-heavy rotation slot, per the worsened Skill-Silo reading.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | ST-01's first AC needs a read-only look at the **production** `settings` row, and the governed environment only has a staging `DATABASE_URL`. Its parameter-authority ruling also gates ST-03, ST-06 and ST-07. | High | Sprint Planning phases the ruling as ST-01's first sub-step, and raises a Human-Delegation request (Infrastructure & Operations Owner) for the production read at sprint start. Dependants are sequenced after the ruling. Resolved within the sprint; does not block the sprint seal. | null |
| RISK-02 | EPIC-03 | ST-11 and ST-13 (and ST-01 if option (b)/(c) is ruled) may amend `strategy_rules.md` (§9, §12, §13.3/§4.2.3). That is a governance file outside a normal sprint write scope. | Medium | Each ruling names whether `strategy_rules.md` changes. Any edit needs explicit Strategy Rules & System Intent Owner authority and follows the file's own Change Log / §15 grep rules (v9.9 ST-20 precedent). | null |
| RISK-03 | Release-level | `ESC-CLOSE-20261006-01` (open, SLA 2026-10-09) is the pending ruling on whether sprint stories may write `claude/roadmap/*` files or existing `backlog.md` item fields. ST-20's AC routes a `current_roadmap.md` correction, and Release Planning's own §1.3a gate edits touch the same boundary. | High | **Must resolve before sprint planning seals.** Listed in `cycle_summary.md` Pre-sprint Planning Required Decisions. ST-21's output was moved to `docs/ops/` to keep it clear of the boundary. | ESC-CLOSE-20261006-01 |
| RISK-04 | EPIC-04 | ST-18 needs live Render/GitHub Actions control to create a real stale staging deploy. ST-16 may need a live `claude_audit_log` read. | Low | Expected Human-Delegation at execution time, as with v9.6–v9.9 precedent. ST-16's code-path audit proceeds regardless. | null |
| RISK-05 | EPIC-02 | 7 stories have observable UI ACs (ST-06–ST-10 here, plus ST-12 and ST-14 in EPIC-03). ST-06 is the largest single item (5.0d). | Medium | Design gate is required before `plan sprint`. Each observable AC needs Playwright coverage or a recorded staging run (CLAUDE.md §2). ST-06 may ship its first increment (removing the false "daily" tooltip claim) independently, per its source scope. | null |

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` holds 0 active initiatives, so there are no pre-assigned bands. All figures are inline STEP-4 estimates under `workforce_capacity.md`'s precedence rule. The ST-35 calibration check raised `BLG-OPS-171` one tier (XS→S) for live-environment verification. `BLG-BE-138` and `BLG-OPS-92` were held, with their check and dependency counts named in scope.

| EPIC | Stories | Days |
|------|---------|------|
| EPIC-01 | 5 | 8.50 |
| EPIC-02 | 5 | 9.90 |
| EPIC-03 | 4 | 4.50 |
| EPIC-04 | 7 | 5.00 |
| **Total** | **21** | **27.90** |

Confirmed capacity band: **~24–28 working days** (`claude/roadmap/workforce_capacity.md`, reconfirmed 2026-09-23). 27.90 / 28.00 = **99.6% of the band's top edge**: within band, at the ceiling, per the explicit "full capacity" instruction.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

No Phasing Recommendation subsection: the outcome is `pass`, not `warn`.

## Integrity Validation

### 3.5 Local Model Integrity

Each of the 21 S2-items maps to exactly one EPIC (S2-01…05 → EPIC-01, S2-06…10 → EPIC-02, S2-11…14 → EPIC-03, S2-15…21 → EPIC-04). No item is unmapped or double-mapped. All 5 RISK-IDs declare a `Relates to` EPIC or Release-level. Every cross-EPIC dependency (ST-06/ST-07 on ST-01) points from a later-sequenced story to an earlier one, so there are no cycles.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

### 5.5 Cross-Stage Integrity

- All 21 S2-IDs map to an EPIC in the Execution Plan table: confirmed.
- EPIC-IDs in `stage4_backlog_slice.md` and `stage4_issue_manifest.json` (EPIC-01–EPIC-04) match the Execution Plan: confirmed.
- All RISK-IDs in the EPIC table (RISK-01, -02, -03, -04, -05) appear in the Risk Register: confirmed.
- ST-01–ST-21 in the slice match the issue manifest one to one (21 entries, same S2-ID order): confirmed.
- No orphaned references.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
attributes.cross_stage_integrity: pass
```

### 5.7 Decision Record Integrity

Not applicable. No escalations were raised by this release-planning session (`artifacts.escalations = not_present`). RISK-03 back-links to an *existing* closure escalation owned by another engine and raises no new one. `decisions--2026-10-06__release-v9.10.md` is present and populated (scope and sequencing decisions; no Accepted Risk records).

```yaml
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.decisions_validated: not_applicable
```

## Publish Gate Evaluation

All STEP 6 conditions hold: this cycle's `open_escalations` is empty; no deferred escalations or `deferred_execution_blockers`; `stage4_5_capacity_check` = pass; `stage5_5_cross_stage_integrity` = pass; `stage5_7` = not_applicable; `stage1_readiness` and `stage3_5_model_integrity` = pass; `plan_structured`, `plan_executable` and `backlog_committed` = true; backlog and roadmap locks released. → `status = Validated`, `publish_eligible = true`.

## Pre-sprint Planning Required Decisions

RISK-03 (High, must resolve before the sprint planning seal) is carried into `cycle_summary.md`. RISK-01 is High but is resolved inside the sprint as ST-01's first sub-step, so it does not gate the seal.
