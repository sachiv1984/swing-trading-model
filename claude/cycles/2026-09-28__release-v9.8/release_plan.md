Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.8
Cycle: 2026-09-28__release-v9.8
Last Updated: 2026-09-28

# Release Plan — v9.8 Full-Capacity Debt Clearance

## Readiness

Preflight (STEP -1) passed in full — see `run_manifest.md` for the complete gate-by-gate record. Notable items:
- §-1.2 (release-on-roadmap) cleared via Option(b) equivalence from rebalance `2026-09-28__scheduled` — the first cycle since `v9.6` where the cited rebalance record is same-day/fresh rather than reused a second time from a stale record.
- §-1.6 SLA-breach carry-forward check clear — `ESC-CLOSE-20260928-02` open but not yet due (SLA 2026-10-01).
- §-1.5 prior-cycle lessons-learnt carry-forward: 3 items reviewed, none require action within this engine's write scope.

No design-dependency scope note comparable to `v9.7`'s `BLG-FEAT-74` §13 pre-clearance requirement exists this cycle — all 39 selected items are independently scoped debt/hygiene items with no cross-item sequencing prerequisite.

## Scope

39 S2-items across 6 EPICs. Full table: `docs/product/scope/scope--2026-09-28__release-v9.8-full-capacity-debt-clearance.md`. Selection method, ready pool, and all dispositions: `run_manifest.md` Scope Construction section.

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01–S2-06 | Head of UX & Design; Frontend Specifications & UX Documentation Owner | null | None |
| EPIC-02 | S2-07–S2-08 | Head of Engineering; Financial Reporting & Records Owner | null | None |
| EPIC-03 | S2-09–S2-16 | Director of Quality | null | None |
| EPIC-04 | S2-17–S2-19 | Infrastructure & Operations Owner; Cybersecurity & Trust Lead | RISK-01 | S2-17 (`BLG-OPS-169`) needs a design decision on where the post-deploy check lives before implementation |
| EPIC-05 | S2-20–S2-29 | Head of Specs Team; Data Model & Domain Schema Owner | null | None |
| EPIC-06 | S2-30–S2-39 | PMO Lead; Head of Specs Team | RISK-02 | S2-39 (`BLG-GOV-351`) needs a design decision on which governed routine owns firing the review before the mechanism can be built |

**EPIC-01 leads the table** as the closest available honouring of the Skill-Silo rotation guideline's intent this cycle (no ready build-and-ship U-item exists — see `run_manifest.md`'s PO Modify directive re-check) — it is the most execution-heavy category with genuine ready scope, including this cycle's two largest single items (`BLG-FE-184`, `BLG-FE-185`).

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|-----------------|
| RISK-01 | EPIC-04 | `BLG-OPS-169`'s scope explicitly requires deciding *where* the post-deploy staging-redeploy check runs (existing `staging-smoke-test.yml`, a new post-merge workflow, or a cycle-close verification step) before implementation can begin | Low | Sprint Planning to phase this as a short design-decision sub-step ahead of the implementation story, per its own Scope text | null |
| RISK-02 | EPIC-06 | `BLG-GOV-351`'s scope explicitly requires deciding which governed routine (post-ship closure is the most natural fit per its own Problem statement) owns firing the 90-day AI feature usage review before the mechanism itself can be built | Low | Sprint Planning to phase this as a design-decision sub-step (routine ownership) ahead of implementation, consistent with the item's own stated scope | null |

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` holds 0 active roadmap initiatives — no pre-assigned Effort Bands for any of this cycle's EPICs. All effort figures are inline STEP-4 estimates, applying `workforce_capacity.md`'s effort-to-days precedence rule (item's own explicit day figure first, canonical band-letter midpoint otherwise) — see `run_manifest.md`.

Total estimated effort: **28.00 days.** Confirmed capacity band: **~24–28 working days** (`claude/roadmap/workforce_capacity.md`, reconfirmed unchanged 2026-09-23, `ESC-EXEC-20260921-07`). 28.00 / 28.00 = **100.0% of the band's top edge** — within band, at its ceiling, per explicit "full capacity" instruction.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

No Phasing Recommendation subsection required — outcome is `pass`, not `warn`.

## Integrity Validation

### 3.5 Local Model Integrity

All 39 selected items map to exactly one EPIC (S2-01…S2-06 → EPIC-01, S2-07…S2-08 → EPIC-02, S2-09…S2-16 → EPIC-03, S2-17…S2-19 → EPIC-04, S2-20…S2-29 → EPIC-05, S2-30…S2-39 → EPIC-06). No S2-item is unmapped or double-mapped. Both RISK-IDs declare a `Relates to` EPIC. Model is internally consistent.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

### 5.5 Cross-Stage Integrity

- All 39 S2-IDs (S2-01–S2-39) map to an EPIC in the Execution Plan table above — confirmed.
- All EPIC-IDs in `stage4_backlog_slice.md` (EPIC-01–EPIC-06) match this document's Execution Plan table — confirmed.
- Both RISK-IDs referenced in the EPIC table (RISK-01, RISK-02) appear in the Risk Register Summary — confirmed.
- No orphaned references found.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
attributes.cross_stage_integrity: pass
```

### 5.7 Decision Record Integrity

Not applicable — no escalations were raised this cycle (`artifacts.escalations = not_present`). `decisions--2026-09-28__release-v9.8.md` is present and populated (scope + sequencing decisions; no Accepted Risk records).

```yaml
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.decisions_validated: not_applicable
```
