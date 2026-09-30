Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.9
Cycle: 2026-09-30__release-v9.9
Last Updated: 2026-09-30

# Release Plan — v9.9

## Readiness

Preflight (STEP -1) passed in full — see `run_manifest.md` for the complete gate-by-gate record. Notable items:
- §-1.2 (release-on-roadmap) cleared via Option(b) equivalence from rebalance `2026-09-30__scheduled` — same-day, fresh record, first citation of it.
- §-1.6 SLA-breach carry-forward check clear — 4 open escalations (`ESC-CLOSE-20260928-02`, `-20260930-01/-02/-03`) none yet due.
- §-1.5 prior-cycle lessons-learnt carry-forward: 3 items reviewed, none require action within this engine's write scope.

No design-dependency scope note comparable to `v9.7`'s `BLG-FEAT-74` §13 pre-clearance requirement exists this cycle — all 35 selected items are independently scoped debt/hygiene items, except `BLG-BE-135` (mid-implementation spec query, see RISK-01) and two governance items needing a routing/authority decision (RISK-02) and live production data (RISK-03).

## Scope

35 S2-items across 6 EPICs. Full table: `docs/product/scope/scope--2026-09-30__release-v9.9.md`. Selection method, ready pool, and all dispositions: `run_manifest.md` Scope Construction section.

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01–S2-05 | Head of Engineering; Backend Engineering Patterns Owner | RISK-01 | None |
| EPIC-02 | S2-06–S2-09 | Infrastructure & Operations Owner; Cybersecurity & Trust Lead | null | None |
| EPIC-03 | S2-10–S2-18 | Director of Quality; QA & Testing Owner | null | None |
| EPIC-04 | S2-19–S2-27 | Head of Specs Team; PMO Lead | RISK-02, RISK-03 | S2-26 (`BLG-GOV-353`) needs a routing/authority decision before implementation; S2-19 (`BLG-GOV-356`) may need Human-Delegation for live production data |
| EPIC-05 | S2-28–S2-34 | Data Model & Domain Schema Owner; Head of Specs Team | null | None |
| EPIC-06 | S2-35 | Head of UX & Design; Frontend Specifications & UX Documentation Owner | null | None |

**EPIC-01 leads the table** — `BLG-BE-135` is the PO Modify directive's recommended build-and-ship candidate (the backend half of this cycle's `BLG-BE-135`/`BLG-FE-193` pair, see `run_manifest.md`) and this cycle's single largest item (8.00d).

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|-----------------|
| RISK-01 | EPIC-01 | `BLG-BE-135`'s scope explicitly requires raising a mid-implementation spec query to the Strategy Rules & System Intent Owner (whether `strategy_rules.md` §7.1's "daily" cadence text should be updated to the actual on-load + nightly cadence, or implementation constrained to match it) before the item can be considered complete | Low | Sprint Planning to phase this as a design-decision sub-step ahead of/alongside implementation, per the item's own stated scope | null |
| RISK-02 | EPIC-04 | `BLG-GOV-353`'s scope explicitly requires a Roadmap Engine/Head of Specs Team routing decision (formal authorisation to create a new `claude/roadmap/*` file) before implementation can proceed, per `execution_prompt.md` §7's write-scope restriction | Low | Sprint Planning to phase the authorisation step ahead of the file-creation work | null |
| RISK-03 | EPIC-04 | `BLG-GOV-356` requires real production AI-feature adoption/cost data (Anthropic API usage, session counts) that this sandboxed environment has no production credential for — the same structural gap recorded at `ESC-EXEC-20260921-02/03/04` and `ESC-EXEC-20260910-01` | Low | Likely to require a Human-Delegation escalation at execution time (direct user action against production), consistent with existing precedent | null |

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` holds 0 active roadmap initiatives — no pre-assigned Effort Bands for any of this cycle's EPICs. All effort figures are inline STEP-4 estimates, applying `workforce_capacity.md`'s effort-to-days precedence rule (item's own explicit day figure first, canonical band-letter midpoint otherwise) — see `run_manifest.md`.

Total estimated effort: **27.85 days.** Confirmed capacity band: **~24–28 working days** (`claude/roadmap/workforce_capacity.md`, reconfirmed unchanged 2026-09-23, `ESC-EXEC-20260921-07`). 27.85 / 28.00 = **99.5% of the band's top edge** — within band, at its ceiling, per explicit "full capacity" instruction.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

No Phasing Recommendation subsection required — outcome is `pass`, not `warn`.

## Integrity Validation

### 3.5 Local Model Integrity

All 35 selected items map to exactly one EPIC (S2-01…S2-05 → EPIC-01, S2-06…S2-09 → EPIC-02, S2-10…S2-18 → EPIC-03, S2-19…S2-27 → EPIC-04, S2-28…S2-34 → EPIC-05, S2-35 → EPIC-06). No S2-item is unmapped or double-mapped. All 3 RISK-IDs declare a `Relates to` EPIC. Model is internally consistent.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

### 5.5 Cross-Stage Integrity

- All 35 S2-IDs (S2-01–S2-35) map to an EPIC in the Execution Plan table above — confirmed.
- All EPIC-IDs in `stage4_backlog_slice.md` (EPIC-01–EPIC-06) match this document's Execution Plan table — confirmed.
- All 3 RISK-IDs referenced in the EPIC table (RISK-01, RISK-02, RISK-03) appear in the Risk Register Summary — confirmed.
- No orphaned references found.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
attributes.cross_stage_integrity: pass
```

### 5.7 Decision Record Integrity

Not applicable — no escalations were raised this cycle (`artifacts.escalations = not_present`). `decisions--2026-09-30__release-v9.9.md` is present and populated (scope + sequencing decisions; no Accepted Risk records).

```yaml
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.decisions_validated: not_applicable
```

## Pre-sprint Planning Required Decisions

No High-priority risk carries a "must resolve before sprint planning seal" disposition — all 3 risks above are Low priority, phaseable as design-decision sub-steps within their own stories. Section omitted from `cycle_summary.md` per STEP 7.
