Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-27
Cycle: 2026-07-27__release-v7.9
Release: v7.9

# Release Plan — v7.9

## Readiness

Preflight (STEP -1) passed all hard gates. Prior cycle `2026-07-24__release-v7.8` is `Closed` with `post_ship_complete = true` and `next_cycle_unblocked = true`. No `## v7.9` roadmap section exists; this release is scoped via the STEP -1.2 Option (b) equivalence rule, citing the `2026-07-27__scheduled` rebalance's documented STEP 8.1 Option (b) decision (Now horizon fully empty, deferred to next `plan release`). See `run_manifest.md` for full STEP -1 detail, the STEP 1.1/1.2/1.3/1.4/1.4a/1.4b advisory outputs, and a flagged data-consistency note (a stale `BLG-FE-128` reference in the prior rebalance's own outcome text — already shipped/archived, not usable as a scope input).

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

No scope changes to strategy or roadmap boundaries. This section extracts a backlog-driven scope slice (no formal roadmap release section exists yet for v7.9 — see Readiness above).

### Items in scope

| S2-ID | Epic | Item | Description |
|-------|------|------|-------------|
| S2-01 | EPIC-01 | BLG-FEAT-66 | Watchlist staleness and decay review |
| S2-02 | EPIC-02 | BLG-FEAT-67 | Historical sector/regime exposure trend |
| S2-03 | EPIC-03 | BLG-SPEC-105 | Formalise trade_plan-to-position FK linkage schema |
| S2-04 | EPIC-04 | BLG-FEAT-85 | Monthly P&L CSV export: tax-lot cost-basis reconciliation |
| S2-05 | EPIC-05 | BLG-FEAT-87 | "Why is my stop moving" explainer tooltip |
| S2-06 | EPIC-06 | BLG-BE-73 | Audit trail for manual position overrides |
| S2-07 | EPIC-07 | BLG-BE-74 | Nightly backtest data-integrity smoke test as a standing CI gate |
| S2-08 | EPIC-08 | BLG-OPS-121 | Provision staging credential for SI-02 live gate re-checks |
| S2-09 | EPIC-09 | BLG-QA-124 | Shared cross-EPIC smoke-test tagging for parallel-branch merges |
| S2-10 | EPIC-10 | BLG-QA-125 | Pre-commit hook automating `backend/routers/test.py` registration check |
| S2-11 | EPIC-11 | BLG-FE-130 | WCAG contrast checklist addendum for chart colour palettes |
| S2-12 | EPIC-12 | BLG-OPS-120 | Cost-tag cloud infrastructure spend by EPIC |
| S2-13 | EPIC-13 | BLG-FE-129 | Dark-mode AC checklist addendum for Base44 prompt drafts |
| S2-14 | EPIC-14 | BLG-GOV-258 | Displacement debt register |
| S2-15 | EPIC-15 | BLG-QA-123 | Defined visual-regression baseline refresh cadence for Grid View |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-56 | Gate ("AI adoption window ~2026-07-25 AND validated AI-touchpoint usage") — date sub-condition elapsed but usage-validation sub-condition unconfirmable this session | Unscheduled — PO to confirm before next release |
| BLG-FEAT-73 | SI-02 gate NOT MET (9th+ consecutive reading); PO perennial-return disposition already parked it (Option (b), `manage roadmap` 2026-07-27) | Unscheduled, pending gate clearance |
| BLG-FEAT-74 | §13 determinism pre-clearance not run; VH effort exceeds single-cycle sizing; same PO disposition as above | Unscheduled, pending gate clearance + phasing review |
| BLG-FE-43 | Gate ("SI-05 sprint planning imminent") not met this cycle | Unscheduled |
| BLG-SPEC-35 | Gate ("PO-02 sprint planning imminent") not met this cycle | Unscheduled |
| 4 remaining P3 candidates from `IW-20260727-01` (BLG-FE-131, BLG-GOV-259, BLG-GOV-260, BLG-GOV-261, BLG-GOV-262, BLG-FEAT-86, BLG-OPS-122, BLG-QA-126) | Capacity — full band reached by the 15 items above; these are ungated and available for the next release without further review | v7.10 candidate pool |

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Format note:** compact table per IMP-08; full acceptance criteria live in `stage4_backlog_slice.md`.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Head of UX & Design; Product Owner | RISK-01 | None |
| EPIC-02 | S2-02 | Metrics Definitions & Analytics Owner; Head of UX & Design | RISK-01 | None |
| EPIC-03 | S2-03 | Data Model & Domain Schema Owner | — | None |
| EPIC-04 | S2-04 | Financial Reporting & Records Owner | — | After EPIC-06 (shared audit-trail/reporting domain, sequencing preference not a hard dependency) |
| EPIC-05 | S2-05 | Head of Engineering; Head of UX & Design | RISK-01 | None |
| EPIC-06 | S2-06 | Financial Reporting & Records Owner | — | None |
| EPIC-07 | S2-07 | Head of Engineering | RISK-02 | None |
| EPIC-08 | S2-08 | Infrastructure & Operations Owner | — | None |
| EPIC-09 | S2-09 | QA Lead | — | None |
| EPIC-10 | S2-10 | QA & Testing Owner | — | None |
| EPIC-11 | S2-11 | Frontend Specifications & UX Documentation Owner | — | None |
| EPIC-12 | S2-12 | FinOps & Resource Architect | — | None |
| EPIC-13 | S2-13 | Base44 Frontend Prompt Owner | — | None |
| EPIC-14 | S2-14 | Challenger; Head of Specs Team | — | None |
| EPIC-15 | S2-15 | Head of UX & Design | — | None |

EPIC-01/02/05: all three carry at least one observable UI acceptance criterion (visible rendering, visual flagging, tooltip display) — classified `design_gate_required = true` at STEP 4.1 below.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01, EPIC-02, EPIC-05 | Three EPICs carry observable UI acceptance criteria and require Design Gate PASS before Sprint Planning may seal | Medium | Run `run design-gate --cycle 2026-07-27__release-v7.9` promptly after this plan publishes; per CLAUDE.md, Playwright coverage or recorded staging sign-off required for each observable AC | null |
| RISK-02 | EPIC-07 | The nightly-backtest smoke test has a documented history (BLG-BE-59/60, BLG-BE-63) of surfacing real pre-existing data-integrity defects once implemented — a new finding during EPIC-07's own build could expand scope beyond the story's own AC | Low | Treat any newly-surfaced data-integrity defect as its own backlog item (BLG-BE-*), not a blocker to EPIC-07's own "smoke test added, passes on current data" AC | null |
| RISK-03 | Release-level | Scope is deliberately sized to the top of the confirmed ~24-28 day capacity band (~26.5 days midpoint, ~95-110% utilisation) per explicit user "use the full capacity" instruction, leaving limited slack for in-sprint surprises | Medium | Accepted per explicit user instruction (see `decisions--2026-07-27__release-v7.9.md`); STEP 4.5 Capacity Check below confirms no over-allocation against the ceiling | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All EPIC-ID / S2-ID / RISK-ID cross-references above resolve internally (15 S2-IDs ↔ 15 EPIC-IDs, 1:1; 3 RISK-IDs all reference EPIC-IDs present in the Scope table or "Release-level"). No orphaned references found.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** 0 of the 15 EPICs have a matching row in `claude/scoring/scored_initiatives.md` (all are backlog-driven items, not roadmap initiatives) — Tier 3 applies uniformly: STEP 4 inline estimate used for all 15, no advisory required.

### Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (autonomous execution engine) — per workforce_capacity.md baseline
Available FTE:      1 (solo developer / autonomous execution engine)
Total capacity:     ~24-28 working-day-equivalent units
Skill constraints:  None scarce this cycle — 15 EPICs span 11 distinct owner roles, no concurrent scarce-skill collision identified
```

### Item Effort Mapping

| EPIC | Item | Effort Band | Midpoint (days) |
|------|------|-------------|------------------|
| EPIC-01 | BLG-FEAT-66 | S (~1 day) | 1.0 |
| EPIC-02 | BLG-FEAT-67 | M (~2 days) | 2.0 |
| EPIC-03 | BLG-SPEC-105 | M (~2-3 days) | 2.5 |
| EPIC-04 | BLG-FEAT-85 | M (~2-3 days) | 2.5 |
| EPIC-05 | BLG-FEAT-87 | S (~1-2 days) | 1.5 |
| EPIC-06 | BLG-BE-73 | M (~2-3 days) | 2.5 |
| EPIC-07 | BLG-BE-74 | M (~2-3 days) | 2.5 |
| EPIC-08 | BLG-OPS-121 | S (~1-2 days) | 1.5 |
| EPIC-09 | BLG-QA-124 | M (~2-3 days) | 2.5 |
| EPIC-10 | BLG-QA-125 | S (~1-2 days) | 1.5 |
| EPIC-11 | BLG-FE-130 | S | 1.0 |
| EPIC-12 | BLG-OPS-120 | M (~2-3 days) | 2.5 |
| EPIC-13 | BLG-FE-129 | S | 1.0 |
| EPIC-14 | BLG-GOV-258 | S | 1.0 |
| EPIC-15 | BLG-QA-123 | S | 1.0 |

All 15 items carry an effort estimate. No `[ESTIMATE REQUIRED]` placeholders.

### Total Effort vs Capacity

```
Total estimated effort:  ~26.5 days midpoint
Confirmed capacity:      ~24-28 working-day-equivalent
Utilisation:             ~95-110% (depending on which end of the band is used as denominator)
Outcome:                 pass (does not exceed the ~28-day ceiling; intentionally at the top of the band per explicit user "use the full capacity" instruction)
```

No over-allocation against the confirmed ceiling. STEP 3/STEP 4 scope selection includes all 15 EPICs — this is a deliberate full-capacity fill, not a phasing scenario, so no `### Phasing Recommendation` subsection is required (that subsection is required only on a `warn` outcome; this is `pass`).

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity

Verified: all 15 S2-IDs map 1:1 to EPIC-IDs in both `## Scope` and `## Execution Plan`; all 15 EPIC-IDs in `stage4_backlog_slice.md` match the Execution Plan table exactly; all 3 RISK-IDs referenced in the Execution Plan table appear in the Risk Register Summary; no orphaned S2/EPIC/RISK references found. `stage4_issue_manifest.json` contains exactly 15 entries (ST-01 through ST-15), one per EPIC, labels consistent with `cycle:2026-07-27__release-v7.9`.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` is not `present` (no escalations were raised this cycle; capacity outcome was `pass`, not `warn`/`fail`, so the escalation subroutine never triggered).

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
