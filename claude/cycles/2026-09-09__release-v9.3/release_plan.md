Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-09
Cycle: 2026-09-09__release-v9.3
Release: v9.3

# Release Plan — v9.3

Invocation: `plan release --version "v9.3" --capacity "full capacity"`

---

## Readiness

Preflight (STEP -1) passed in full — see `run_manifest.md`. No formal `## v9.3` roadmap section exists; cleared via the STEP -1.2 Option(b)-equivalence rule against the `2026-08-11__scheduled` rebalance's documented "defer again" decision (8th consecutive release cycle relying on this equivalence, v8.5–v9.3). `post_ship_complete`/`next_cycle_unblocked` both `true` for prior cycle `2026-09-07__release-v9.2`. All required agent roles present. Write test passed.

Advisory checks (§1.1–§1.4, full detail in `run_manifest.md`):
- Backlog Age Advisory: no 2+ cycle carried spec/documentation debt items in scope — all 27 selected items are entering `stage4_backlog_slice.md` for the first time.
- Provisional-Target Advisory: no item carries `Provisional-Target: v9.3` (no horizon signal pre-existed); all 27 selected items carry `Unscheduled`/`TBD`.
- Design-Gate Language Scan: no selected item carries an observable UI acceptance criterion → `design_gate_required: false`.
- Gate-Condition Proximity Scan: Arc 4/Arc 5 data-density metrics unchanged since the last rebalance (0/11 linked trade plans; SI-02/PO-02/PO-04 gates NOT MET). No item in this cycle's scope touches that gate family. No ungated P0–P2 item exists this cycle — the entire ready pool (61 items) is P3, except one P4 item.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

Scope document: `docs/product/scope/scope--2026-09-09__release-v9.3-full-capacity-debt-clearance.md`

| S2-ID | Scope theme | Items | Effort (days) |
|-------|-------------|-------|----------------|
| S2-01 | Backend Reliability & Data Correctness Debt | 4 | 8.00 |
| S2-02 | QA & Test Infrastructure Debt | 6 | 5.00 |
| S2-03 | Operations & Cost Monitoring Debt | 5 | 6.50 |
| S2-04 | Spec & Documentation Debt | 5 | 4.50 |
| S2-05 | Governance Process Debt & Security | 7 | 3.50 |
| **Total** | | **27** | **27.50** |

**Items explicitly deferred (not entering v9.3 scope):**
- `BLG-FEAT-92` — reconciled sub-scope of `BLG-FEAT-30`, inherits its gate (screener live ≥60 days AND ≥60 closed trades with attribution); standing Product Owner decision from `2026-09-03__release-v9.1`, reaffirmed each cycle since, unchanged (5th consecutive cycle).
- `BLG-FEAT-73`, `BLG-FEAT-74`, `BLG-FEAT-76` and all remaining Arc 5 pre-entry-gateway / SI-02 / SI-05 / PO-02-family P1 items — gate-conditional, no clearance evidence this cycle.
- `BLG-SPEC-56`, `BLG-SPEC-57`, `BLG-QA-59` (Arc 4 PO-02/03/04 pre-authoring work) — premature while the SI-02/PO-02 data-density gate remains unmet; deliberately excluded to avoid pre-work on a gated horizon.
- 34 further ungated P3 items, ~13.10 estimated days, left unselected purely on capacity grounds — see `run_manifest.md` for the full list; available for the next release cycle.

No scope reprioritisation performed beyond selection from the ungated pool — this routine does not alter strategy boundaries.

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Format note (IMP-08):** full acceptance criteria live in `stage4_backlog_slice.md`; this section is the compact sequencing/risk view.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Backend Engineering Patterns Owner; Data Model & Domain Schema Owner | RISK-01 | No UI ACs; independent of other EPICs |
| EPIC-02 | S2-02 | QA Testing Owner; Director of Quality | RISK-02 | No UI ACs; independent of other EPICs |
| EPIC-03 | S2-03 | Infrastructure & Operations Owner; FinOps & Resource Architect | RISK-03 | No UI ACs; independent of other EPICs |
| EPIC-04 | S2-04 | Head of Specs Team; API Contracts & Documentation Owner | RISK-04 | No UI ACs; independent of other EPICs |
| EPIC-05 | S2-05 | Head of Specs Team; Cybersecurity & Trust Lead | RISK-05 | No UI ACs; sequence governance-tooling-touching stories serially within the sprint to avoid cross-item collisions |

**No design-gate-triggering EPIC this cycle** — the first release since v9.0 with zero observable UI acceptance criteria in scope; the entire selection is backend/QA/ops/spec/governance debt, consistent with the ready pool containing no ungated P0–P2 item.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | `BLG-BE-44` (signal write-path consolidation) touches code stabilised by `BLG-SEC-02`'s v6.4 sanitisation fix — a premature refactor could compound an unproven change, even though the 30-day stability gate has since cleared | Medium | Story author confirms current production stability (no incidents since 2026-07-02) before starting the refactor; QA sign-off requires regression coverage on all 3 consolidated write paths | null |
| RISK-02 | EPIC-02 | `BLG-QA-85` (contract test suite) may surface pre-existing `openapi.yaml` vs. route-behaviour drift beyond its own scope, generating follow-on spec-debt items mid-sprint | Low | Any drift found beyond the 5-endpoint sample is filed as a new `BLG-SPEC-*` item rather than expanding this story's scope inline | null |
| RISK-03 | EPIC-03 | 3 of 5 EPIC-03 items (`BLG-OPS-17`, `BLG-OPS-20`, `BLG-OPS-96`) depend on external API call-volume visibility (Alpaca, research endpoint, Anthropic) that may require new logging infrastructure shared across all three, risking duplicated instrumentation if built independently | Medium | Sequence `BLG-OPS-17` first as the reference instrumentation pattern; `BLG-OPS-20`/`BLG-OPS-96` reuse its logging approach rather than inventing separate mechanisms | null |
| RISK-04 | EPIC-04 | `BLG-SPEC-70` (cross-reference linter) may find orphaned specs spanning multiple documentation owners, requiring cross-owner triage before the item can close within the sprint | Low | Head of Specs Team triages any findings within the sprint window; unresolved individual specs are filed as follow-on `BLG-SPEC-*` items rather than blocking this story's closure | null |
| RISK-05 | EPIC-05 | 7 EPIC-05 items span 4 different owners (Head of Specs Team, Base44 Frontend Prompt Owner ×3, Director of HR, Cybersecurity & Trust Lead) with no single reviewer across all of them | Low | Head of Specs Team runs one consolidated review pass across all EPIC-05 items before DoQ sign-off, matching the v9.2 EPIC-05 precedent | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All 27 ST items in `stage4_backlog_slice.md` carry a `**Source:** BLG-xxx` reference resolving to an existing, currently-open backlog entry in `claude/backlog/backlog.md` (confirmed via the same script-driven extraction used to build the slice — no fabricated or stale IDs). All 5 EPIC IDs are internally consistent between `release_plan.md` and `stage4_backlog_slice.md`. No `[ESTIMATE REQUIRED]` or `[AC REQUIRED]` placeholders present in any of the 27 stories.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` has 0 active initiatives — no pre-assigned Effort Bands. All 5 EPICs sized via inline STEP 4 estimate from each item's own `**Effort:**` field in `claude/backlog/backlog.md`, using the canonical Effort Band → Days table added to `workforce_capacity.md` at v9.2 closure (XS=0.15d, S=0.5d, M=2.5d, L=3.5d).

| EPIC | Items | Subtotal (days) |
|------|-------|-------------------|
| EPIC-01 — Backend Reliability & Data Correctness Debt | 4 | 8.00 |
| EPIC-02 — QA & Test Infrastructure Debt | 6 | 5.00 |
| EPIC-03 — Operations & Cost Monitoring Debt | 5 | 6.50 |
| EPIC-04 — Spec & Documentation Debt | 5 | 4.50 |
| EPIC-05 — Governance Process Debt & Security | 7 | 3.50 |
| **Total** | **27** | **27.50** |

27.50 days vs the confirmed ~24–28 day band (`claude/roadmap/workforce_capacity.md`, unchanged since 2026-07-17) — within band, at its upper bound (98% of the 28-day ceiling), matching the explicit "use full capacity" instruction. **Capacity check outcome: pass, no WARN.**

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity / 5.7 Decision Record Integrity

**5.5 Cross-Stage Integrity:** All 5 S2 IDs (S2-01..S2-05) map 1:1 to EPIC-01..EPIC-05. All 5 EPIC IDs in `stage4_backlog_slice.md` match the Execution Plan table. All 5 RISK IDs in the EPIC table appear in the Risk Register Summary. No orphaned references found.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` is not `present` (no escalations raised this cycle; all preflight/gate checks passed cleanly). `decisions--2026-09-09__release-v9.3.md` is still produced per STEP 3's standing requirement (scope/sequencing decisions, not escalation-driven).

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```

---

## Change Log

| Date | Version | Change | Authority |
|------|---------|--------|-----------|
| 2026-09-09 | 1.0 | Initial publication — v9.3 release plan, 27 items / 5 EPICs / 27.50 days, full capacity | Head of Specs Team (Release Planning Engine) |
