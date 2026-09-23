Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.7
Cycle: 2026-09-23__release-v9.7
Last Updated: 2026-09-23

# Release Plan — v9.7 PO-05 Replay Mode & Full-Capacity Debt Clearance

## Readiness

Preflight (STEP -1) passed in full — see `run_manifest.md` for the complete gate-by-gate record. Notable items:
- §-1.2 (release-on-roadmap) cleared via Option(b) equivalence from rebalance `2026-09-19__scheduled` — 15th consecutive cycle relying on this class of equivalence.
- §-1.6 SLA-breach carry-forward check clear — all 6 `v9.6` open escalations Resolved.
- §-1.5 prior-cycle lessons-learnt carry-forward: both items already closed before this session started.

Design dependency detected (§1.3 scan): `BLG-FEAT-74`'s own scope explicitly requires a canonical-spec scope confirmation ("single trade replay vs. full historical window, output format") before implementation — surfaced to the Pre-sprint Planning Required Decisions checklist below.

## Scope

29 S2-items across 7 EPICs. Full table: `docs/product/scope/scope--2026-09-23__release-v9.7-replay-mode-and-capacity-clearance.md`. Selection method, ready pool, and all dispositions: `run_manifest.md` Scope Construction section.

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Head of Engineering; Product Owner | RISK-01 | Scope-confirmation sub-phase must precede backend/frontend build — see note below |
| EPIC-02 | S2-02–S2-07 | Head of UX & Design | RISK-02 | None — independent of EPIC-01 |
| EPIC-03 | S2-08–S2-13 | Head of Engineering | null | None |
| EPIC-04 | S2-14–S2-18 | Director of Quality | null | None |
| EPIC-05 | S2-19–S2-22 | PMO Lead / Head of Specs Team | null | None |
| EPIC-06 | S2-23–S2-26 | Head of Specs Team | null | None |
| EPIC-07 | S2-27–S2-29 | Infrastructure & Operations Owner | RISK-03 | S2-27 requires a real (non-mocked) DB/SQL run — coordinate with Infrastructure & Operations Owner for a staging or delegated execution slot |

**EPIC-01:** `BLG-FEAT-74` alone is sized at 12.0 PO-estimated days (no canonical `VH` midpoint exists) — roughly 43% of this cycle's total capacity. Its own scope note requires "exact scope (single trade replay vs. full historical window, output format)… confirmed by canonical spec before implementation." Recommend Sprint Planning phase this as: (1) scope-confirmation sub-story against `strategy_rules.md` §13 binding conditions, (2) backend replay mechanics, (3) frontend selector + output view — not a single undifferentiated story.

**EPIC-07:** `BLG-OPS-168` (S2-27) is itself a "run this against a live database" verification item — it cannot be satisfied by code review alone; needs either a delegated staging run or explicit Product Owner acceptance of a dry-run/mocked substitute, per the same class of constraint the prior cycle's synthetic-monitor and Playwright-reseed escalations hit (`ESC-EXEC-20260921-02`/`-03`).

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|-----------------|
| RISK-01 | EPIC-01 | `BLG-FEAT-74`'s exact scope (replay granularity, output format) is undefined; sprint planning cannot write concrete ACs for the backend/frontend sub-stories without it | High | Resolve via a scope-confirmation sub-story or Head of Specs Team pre-sprint scoping note, referencing `docs/product/decisions/po05_section13_preassessment.md`'s 6 binding conditions, before sprint planning seals | null |
| RISK-02 | EPIC-02 | `BLG-FE-183` (predictive-language CI lint) may false-positive against legitimate historical/retrospective copy newly introduced by EPIC-01's replay-mode output view, if both land in the same sprint | Low | Sequence `BLG-FE-183`'s lint-rule authoring with awareness of EPIC-01's planned output-view copy; no hard ordering required | null |
| RISK-03 | EPIC-07 | `BLG-OPS-168` needs a real (non-mocked) database run to verify the reflection-reminder migration/SQL — this routine holds no production credential and the sandboxed `DATABASE_URL` targets staging only, requiring the user's prior confirmation before any query per standing session practice | Medium | Route to Infrastructure & Operations Owner for a delegated staging run at sprint execution, same pattern as `ESC-EXEC-20260921-02`/`-03` | null |

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` holds 0 active roadmap initiatives — no pre-assigned Effort Bands for any of this cycle's EPICs. All effort figures are inline STEP-4 estimates per `run_manifest.md`'s effort-to-days rule (`BLG-FEAT-74`'s 12.0d is a Product Owner ad hoc estimate, not derived from the rule — see `run_manifest.md`).

Total estimated effort: **28.00 days.** Confirmed capacity band: **~24–28 working days** (`claude/roadmap/workforce_capacity.md`, reconfirmed unchanged 2026-09-23, `ESC-EXEC-20260921-07`). 28.00 / 28.00 = **100.0% of the band's top edge** — within band, at its ceiling, per explicit "use full capacity" instruction.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

No Phasing Recommendation subsection required — outcome is `pass`, not `warn`.

## Integrity Validation

### 3.5 Local Model Integrity

All 29 selected items map to exactly one EPIC (S2-01 → EPIC-01, S2-02…S2-07 → EPIC-02, S2-08…S2-13 → EPIC-03, S2-14…S2-18 → EPIC-04, S2-19…S2-22 → EPIC-05, S2-23…S2-26 → EPIC-06, S2-27…S2-29 → EPIC-07). No S2-item is unmapped or double-mapped. All 3 RISK-IDs declare a `Relates to` EPIC. Model is internally consistent.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

### 5.5 Cross-Stage Integrity

- All 29 S2-IDs (S2-01–S2-29) map to an EPIC in the Execution Plan table above — confirmed.
- All EPIC-IDs in `stage4_backlog_slice.md` (EPIC-01–EPIC-07) match this document's Execution Plan table — confirmed.
- All 3 RISK-IDs referenced in the EPIC table (RISK-01, RISK-02, RISK-03) appear in the Risk Register Summary — confirmed.
- No orphaned references found.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
attributes.cross_stage_integrity: pass
```

### 5.7 Decision Record Integrity

Not applicable — no escalations were raised this cycle (`artifacts.escalations = not_present`). `decisions--2026-09-23__release-v9.7.md` is present and populated (scope + sequencing decisions; no Accepted Risk records, since none were raised as formal AR/SRB escalations — the `BLG-FEAT-74` seating was a direct Product Owner scope decision, recorded in the Scope decisions table).

```yaml
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.decisions_validated: not_applicable
```
