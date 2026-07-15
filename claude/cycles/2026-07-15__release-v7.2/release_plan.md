Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v7.2
Cycle: 2026-07-15__release-v7.2
Last Updated: 2026-07-15

---

# Release Plan — v7.2: Dashboard & Trade-Plan UX Hardening

## Readiness

Release readiness validated against `claude/roadmap/current_roadmap.md §3` (Now horizon, v7.2 section) and `claude/backlog/backlog.md`.

- All 8 scope candidates are ungated, `Provisional-Target: v7.2`, added at roadmap rebalance `2026-07-15__scheduled` (STEP 8.1 Option (a) for the 5 P1 UX items; direct filing for the 3 P2 supporting readiness-pass items).
- Recommended sequencing carried from the roadmap annotation: `BLG-FE-55` (mobile responsiveness baseline) first, as its findings may affect the scope/approach of the four dashboard/trade-plan UX items.
- Advisory scans (§1.1–§1.4b) recorded in full in `run_manifest.md`. Summary:
  - §1.1 Backlog Age: no spec/doc-debt item aged 2+ cycles without story assignment.
  - §1.2 Provisional-Target: 8/8 candidates match `v7.2`.
  - §1.3 Design-Gate Language: `BLG-FE-109`, `BLG-FE-110`, `BLG-FE-111` carry observable UI acceptance criteria — design dependency flagged for the Design Gate (see STEP 4.1 below).
  - §1.4a Perennial-Return: none of the 8 items appeared in the v7.1 backlog slice — no consecutive-return pattern, no PO disposition required.
  - §1.4b Within-Sprint Date Gate: no scope item carries a calendar-dated gate condition — all classifiable as firm capacity, subject to the §4.5 capacity check.
  - §1.4 Gate-Condition Proximity: no gate-conditional candidates in scope. SI-02 context noted — `BLG-FE-109` is itself the UX-side fix for SI-02's stagnant linkage rate, not a candidate awaiting the gate.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

Scope document: `docs/product/scope/scope--2026-07-15__release-v7.2-dashboard-trade-plan-ux-hardening.md`

| S2-ID | Backlog Item | Title | Priority | Effort |
|-------|-------------|-------|----------|--------|
| S2-01 | BLG-FE-55 | Mobile responsiveness baseline assessment | P1 | M (~1–2d) |
| S2-02 | BLG-SPEC-89 | BLG-FE-109 pre-implementation readiness pass | P2 | M (~2–3d) |
| S2-03 | BLG-FE-109 | Trade-plan-to-execution linkage UX ("Start Trade from Plan") | P1 | M (~1–2d) |
| S2-04 | BLG-SPEC-90 | BLG-FE-110/111 pre-implementation spec & instrumentation pass | P2 | S–M (~1–2d) |
| S2-05 | BLG-FE-110 | Dashboard empty/first-run state coverage | P1 | S–M (~0.5–1d) |
| S2-06 | BLG-FE-111 | Dashboard briefing visual hierarchy | P1 | S (~0.5d) |
| S2-07 | BLG-FE-112 | Notification/digest surface consolidation review (audit only) | P1 | M (~1–2d) |
| S2-08 | BLG-QA-111 | Combined design review + shared Playwright suite plan | P2 | S (~0.5–1d) |

No items explicitly deferred from this scope pull — all 8 v7.2 Now-horizon roadmap candidates are included. This is a scope extraction only; no reprioritisation of the global backlog performed.

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Sequencing note:** `EPIC-01` (BLG-FE-55) runs first per roadmap recommendation — its findings may inform scope/approach for `EPIC-02` and `EPIC-03`. `EPIC-02`/`EPIC-03` each depend on their respective `BLG-SPEC-*` readiness pass completing before their own `BLG-FE-*` implementation story enters sprint planning (per each spec item's own AC). `EPIC-05` (combined design review + shared Playwright plan) should be scheduled ahead of sprint planning per `BLG-QA-111`'s own AC, covering `EPIC-02`, `EPIC-03`, and `EPIC-04`.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Head of UX & Design | RISK-01 | Runs first |
| EPIC-02 | S2-02, S2-03 | Head of UX & Design; Base44 Frontend Prompt Owner; Head of Specs Team | RISK-02 | S2-02 (readiness pass) before S2-03 (implementation) sprint planning |
| EPIC-03 | S2-04, S2-05, S2-06 | Head of UX & Design; Base44 Frontend Prompt Owner; Frontend Specs & UX Documentation Owner | RISK-03 | S2-04 (spec/instrumentation pass) before S2-05/S2-06 sprint planning |
| EPIC-04 | S2-07 | Head of UX & Design; Frontend Specs & UX Documentation Owner | RISK-04 | Independent; audit findings only, no implementation this release |
| EPIC-05 | S2-08 | Head of UX & Design; Director of Quality | RISK-05 | Scheduled ahead of sprint planning; covers EPIC-02/03/04 |

EPIC-01: Findings feed directly into whether EPIC-02/EPIC-03 items need mobile-specific AC additions before their own sprint planning — Product Owner to review the assessment report before EPIC-02/EPIC-03 seal.

EPIC-02: `BLG-SPEC-89` explicitly scopes the §13 human-in-the-loop boundary confirmation for the new auto-link action before `BLG-FE-109` implementation begins — this is the highest-priority readiness gate in this release.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Mobile assessment findings could require re-scoping EPIC-02/EPIC-03 AC after those EPICs are already planned, if sequencing slips | Medium | Roadmap-recommended sequencing (BLG-FE-55 first) already adopted in this plan; PO reviews assessment report before EPIC-02/EPIC-03 sprint planning seals | null |
| RISK-02 | EPIC-02 | New trade-plan auto-link action (`trade_plan_id` populated with no manual step) could inadvertently cross the §13 human-in-the-loop / automated-execution boundary | High | `BLG-SPEC-89` scope point (6) explicitly confirms the action does not cross §13 before `BLG-FE-109` implementation begins | null |
| RISK-03 | EPIC-03 | `DataState` empty-state pattern and card-hierarchy treatment are not yet formalised in `design_system.md`, risking inconsistent implementation across BLG-FE-110/111 | Medium | `BLG-SPEC-90` formalises both patterns in `design_system.md`/frontend_specs before BLG-FE-110/111 sprint planning | null |
| RISK-04 | EPIC-04 | Audit-only findings could surface a consolidation need larger than this release's remaining capacity | Low | Scope explicitly limited to audit + findings report; any consolidation implementation is filed as a follow-up backlog item, not built this release | null |
| RISK-05 | Release-level | EPIC-05's combined design review + shared Playwright plan creates a soft dependency across EPIC-02/03/04 — if it slips, individual item design reviews could proceed ad hoc, defeating the "combined" intent | Low | `BLG-QA-111`'s own AC requires the combined review to be scheduled ahead of sprint planning; Sprint Planning Engine STEP -1 will check for this per the Pre-sprint Required Decisions checklist if elevated to High (not elevated here) | null |

Decisions record: `docs/product/decisions/decisions--2026-07-15__release-v7.2.md`

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

Checked: all S2-IDs referenced in the Scope table map 1:1 to backlog items that exist in `claude/backlog/backlog.md` (verified by direct read, §STEP 2 above). All EPIC-IDs in the Execution Plan table reference only S2-IDs defined in Scope. No orphaned or undefined identifiers found. Owner/role assignments per EPIC match roles named in `claude/agents/`.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Design Gate Classification (STEP 4.1)

Scan of all 8 ST items for UI-facing scope:

- `ST-03` (`BLG-FE-109`), `ST-05` (`BLG-FE-110`), `ST-06` (`BLG-FE-111`): delegation class `delegated_frontend`, each carrying observable UI acceptance criteria (visible/functional action, empty-state rendering, colour, dual-theme layout hierarchy).
- `ST-01`, `ST-02`, `ST-04`, `ST-07`, `ST-08`: delegation class `autonomous`, no observable UI acceptance criteria (assessment/audit reports, spec/documentation passes, process planning).

**Classification: `design_gate_required = true`** — 3 items (ST-03, ST-05, ST-06) classified as UI-facing.

⚠ DESIGN GATE REQUIRED before plan sprint — 3 items classified as UI-facing. Run: `run design-gate --cycle 2026-07-15__release-v7.2`

```yaml
attributes.design_gate_required: true
```

---

## Capacity Check

**Effort Band Lookup (Tier 3 for all 8 items):** `claude/scoring/scored_initiatives.md` carries no matching initiative row for any of the 8 v7.2 scope items (CPS = N/A this cycle, per the file's own note). Using STEP 4 inline estimates; no advisory required (tier 3 is silent by design).

**Capacity inputs:** Sprint capacity baseline ~12–14 working days (solo developer, evenings/weekends — `claude/roadmap/workforce_capacity.md`, Effective 2026-05-27). Warn threshold: effort > 14 days.

| ST-ID | Item | Effort estimate | Midpoint (days) |
|-------|------|------------------|------------------|
| ST-01 | `BLG-FE-55` | M (~1–2 days) | 1.5 |
| ST-02 | `BLG-SPEC-89` | M (~2–3 days) | 2.5 |
| ST-03 | `BLG-FE-109` | M (~1–2 days) | 1.5 |
| ST-04 | `BLG-SPEC-90` | S–M (~1–2 days) | 1.5 |
| ST-05 | `BLG-FE-110` | S–M (~0.5–1 day) | 0.75 |
| ST-06 | `BLG-FE-111` | S (~0.5 day) | 0.5 |
| ST-07 | `BLG-FE-112` | M (~1–2 days, audit only) | 1.5 |
| ST-08 | `BLG-QA-111` | S (~0.5–1 day) | 0.75 |
| **Total** | | | **10.5** |

At the midpoint, total estimated effort (10.5 days) sits comfortably within the ~12–14 day capacity band, ~1.5–3.5 days of buffer. Pessimistic reading (top of every range): 2+3+2+2+1+0.5+2+1 = 15.5 days — this would exceed the band, but the midpoint (the primary sizing basis per this section's convention) does not, and unlike v7.1's `BLG-BE-60`, no single item here carries a wide (2×+) range driving disproportionate pessimistic-case risk — the widest individual range is `BLG-SPEC-89` at ~2–3 days.

**Outcome: PASS.** No phasing recommendation required — feasible within a single sprint capacity band at the midpoint estimate, with acknowledged pessimistic-case tightness if multiple items trend to their high end simultaneously (Sprint Planning to monitor per the standing v7.1 carry-forward practice of treating the Phasing Recommendation as a live option; no formal phasing proposed here since the outcome is PASS, not WARN).

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity

- All S2 IDs map to an EPIC: S2-01 → EPIC-01; S2-02, S2-03 → EPIC-02; S2-04, S2-05, S2-06 → EPIC-03; S2-07 → EPIC-04; S2-08 → EPIC-05. PASS.
- All EPIC IDs in `stage4_backlog_slice.md` match the Execution Plan (STEP 3): EPIC-01 through EPIC-05 present and consistent in both. PASS.
- All RISK IDs referenced in the Execution Plan EPIC table (RISK-01, RISK-02, RISK-03, RISK-04, RISK-05) appear as rows in the Risk Register Summary. PASS.
- No orphaned S2/EPIC/RISK references found.

**Outcome: PASS.**

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
attributes.cross_stage_integrity: pass
```

## Integrity Validation — 5.7 Decision Record Integrity

Skipped — `artifacts.escalations` is not `present` this cycle (0 escalations raised). Per STEP 5.5 rule, this check runs only when escalations exist.

```yaml
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.decisions_validated: not_applicable
```

---
