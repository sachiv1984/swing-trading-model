Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Published
Release: v7.0
Cycle: 2026-07-12__release-v7.0
Last Updated: 2026-07-12

Design Gate Required: true

---

# Release Plan — v7.0

## Readiness

Preflight (STEP -1): PASS. Release v7.0 not yet formally sectioned on the roadmap; cleared via the `2026-07-12__scheduled` rebalance's STEP 8.1 Option (b) deferral record (see `run_manifest.md`).

### 1.1 Backlog Age Advisory
No spec/documentation debt item in this release's candidate set (or in the wider backlog) was found to have aged 2+ release cycles without a story assignment while remaining otherwise ungated. `BLG-SPEC-80`, `BLG-SPEC-71`, `BLG-SPEC-73` are all receiving story assignment in this cycle. No warning.

### 1.2 Provisional-Target Advisory
0 items carry `Provisional-Target: v7.0` (no roadmap section existed to tag against). 7 items carry `Provisional-Target: v6.9` (missed that cycle's 2-item scope, picked up here): `BLG-FE-97`, `BLG-SPEC-71`, `BLG-BE-50`, `BLG-FE-95`, `BLG-FE-96`, `BLG-SPEC-73`, `BLG-BE-51`. 8 items carry `Unscheduled`/`TBD`/"Next available sprint" (no horizon signal, selected this cycle on readiness + ungated + product-value grounds): `BLG-FE-102`, `BLG-SPEC-80`, `BLG-QA-95`, `BLG-FE-104`, `BLG-BE-38`, `BLG-FEAT-69`, `BLG-FEAT-70`, `BLG-FEAT-68`.

### 1.3 Design-Gate Language Scan
Two items carry explicit design-decision language: `BLG-FE-104` ("design gate review of the combined-badge state") and `BLG-SPEC-73` ("Head of UX & Design confirms... canonical wording"). Both flagged for the Pre-sprint Required Decisions checklist (see `cycle_summary.md`) and the design gate (`run design-gate`).

### 1.4a Perennial-Return Check
N/A — no conditional/gate-blocked candidate in this release's scope; all 15 items are firm, ungated selections. No perennial-return items apply.

### 1.4b Within-Sprint Date Gate Classification
N/A — no item in this release's scope carries a within-sprint date gate (all selected items are gate-free or `Gate criteria: None`).

### 1.4 Gate-Condition Proximity Scan
Arc 4/5 data density sub-check (mandatory): using the `2026-07-12__scheduled` rebalance's same-day live production query (not re-queried here to avoid redundant API calls within one session):
- SI-02 (20+ trades with plans): 0/11 linked trade plans; behavioural-drift endpoint reports `insufficient_data` (9 trades in 90-day window) — gate remains NOT MET, no near-term clearing projection available.
- PO-02 (6+ months AI journal entries) / PO-04 (50+ trades with plans): data not available this cycle — Product Owner to surface at readiness review; neither gate is relevant to any item in this release's scope.

No gate-conditional item is in this release's scope, so this scan does not affect feasibility.

```yaml
# state.json update (STEP 1):
artifacts.stage1_readiness: pass
```

---

## Scope

| S2-ID | Theme | Items |
|-------|-------|-------|
| S2-01 | Positions Grid View Parity | `BLG-SPEC-80`, `BLG-FE-102`, `BLG-FE-97`, `BLG-QA-95`, `BLG-FE-104` |
| S2-02 | v6.9 Carryover Fixes & Reconciliation | `BLG-SPEC-71`, `BLG-BE-50`, `BLG-FE-95`, `BLG-FE-96`, `BLG-SPEC-73`, `BLG-BE-51`, `BLG-BE-38` |
| S2-03 | User-Facing Feature Enhancements | `BLG-FEAT-69`, `BLG-FEAT-70`, `BLG-FEAT-68` |

**Rationale for scope size:** v6.9 shipped only its 2 named-mandatory items against ~12-14 days of capacity (~4-6 days used). PO directed this cycle to fill capacity with ready, ungated backlog items rather than repeat that pattern (see `run_manifest.md` STEP 0 scope-maximization directive). 15 stories selected across 3 themes, estimated ~9.5-10 days total (see Capacity Check) — full use of capacity with buffer, not maximised to the point of infeasibility.

**Items explicitly deferred:**

| Item | Reason | Target |
|------|--------|--------|
| `BLG-FEAT-66` (Watchlist staleness and decay review) | Ungated and ready, but scope already provides coherent capacity utilisation without it; kept for next release rather than added purely to inflate story count | Next release |
| `BLG-FEAT-67` (Historical sector/regime exposure trend) | Same as above | Next release |
| All SI-02/SI-04/PO-02/Arc-4/Arc-6-gated items (e.g. `BLG-FEAT-73`, `BLG-FEAT-74`, `BLG-FEAT-75`, `BLG-SPEC-35`, `BLG-GOV-28`) | Gate-conditional; gates confirmed NOT MET at the `2026-07-12__scheduled` rebalance | Unscheduled — re-check at next rebalance |

```yaml
# state.json update (STEP 2):
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Engineering | RISK-01, RISK-04 | Internal: `BLG-SPEC-80` → `BLG-FE-102` → `BLG-FE-97` → `BLG-QA-95` → `BLG-FE-104` |
| EPIC-02 | S2-02 | Head of Engineering | RISK-02, RISK-04 | No cross-item dependency; items independent within EPIC |
| EPIC-03 | S2-03 | Financial Reporting & Records Owner | RISK-03, RISK-04 | `BLG-FEAT-69`/`BLG-FEAT-70` share `Reports.js`; `BLG-FEAT-68` independent |

**EPIC-01:** `BLG-SPEC-80` lands first (or alongside) so `BLG-FE-102` cites the spec directly, per the item's own text. `BLG-QA-95` (Playwright parity) lands after both badge/indicator stories ship. `BLG-FE-104`'s design review needs both badges rendered together, so it runs last.

**EPIC-02:** All 7 items are independent fixes/instrumentation across different files (`reports.md`, `backend/database.py`-pattern log table, `DashboardHome.js`/`StrategyBenchmark.js`, `Positions.js`, `GateProgressStrip.js`/`dashboard.md`, `backend/routers/ai.py`, `backend/routers/portfolio_risk.py`) — no sequencing constraint.

**EPIC-03:** `BLG-FEAT-69` and `BLG-FEAT-70` both modify the Reports.js P&L view; sequence to avoid rebasing churn but no hard blocker since same EPIC/branch. `BLG-FEAT-68` touches position-review UI, independent.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | `PositionCard.js`/`positions.md` touched by 3 sequential stories (`BLG-SPEC-80`, `BLG-FE-102`, `BLG-FE-97`) plus a review (`BLG-FE-104`) — sequencing must be honoured within the branch to avoid rework | Medium | Sequence per Execution Plan above; single branch/EPIC avoids cross-branch merge risk | null |
| RISK-02 | EPIC-02 | `BLG-SPEC-71` corrects `reports.md` changelog wording that itself caused the drift being fixed (spec-only entries worded identically to shipped-feature entries) — risk of repeating the same ambiguity if the correction isn't precise | Low | Apply `document_lifecycle_guide.md` versioning conventions carefully; explicitly mark corrected sections "Design Only — Implementation Pending" per the item's own suggested convention | null |
| RISK-03 | EPIC-03 | `BLG-FEAT-69` and `BLG-FEAT-70` both modify `Reports.js`'s P&L views concurrently | Low | Sequence within EPIC-03 branch; no cross-branch conflict since same EPIC | null |
| RISK-04 | Release-level | 8 of 15 items carry observable UI acceptance criteria (`BLG-FE-102`, `BLG-FE-97`, `BLG-FE-104`, `BLG-FE-95`, `BLG-FE-96`, `BLG-FEAT-69`, `BLG-FEAT-70`, `BLG-FEAT-68`) — CLAUDE.md hard gate requires Playwright coverage or human staging sign-off per observable AC, and Design Gate must pass before Sprint Planning seals | High | `run design-gate --cycle 2026-07-12__release-v7.0` must complete before `plan sprint` seals — flagged as a Pre-sprint Planning Required Decision (see `cycle_summary.md`) | null |

```yaml
# state.json update (STEP 3):
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All 15 ST items map to exactly one EPIC (S2-01→EPIC-01, S2-02→EPIC-02, S2-03→EPIC-03); all 4 RISK-IDs referenced in the Execution Plan table appear in the Risk Register; no item appears in more than one EPIC; no dangling `Maps to` references. Plan is internally consistent and executable.

```yaml
# state.json update (STEP 3.5):
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Backlog Slice Commitment (STEP 4)

`stage4_backlog_slice.md` written (15 ST items across 3 EPICs). Backlog lock `RP:v7.0:2026-07-12__release-v7.0` acquired, release slice section written to `claude/backlog/backlog.md` with idempotency marker, transaction committed (`BLTX-20260712-01`), lock released. `stage4_issue_manifest.json` written (15 entries; not used for issue creation this cycle — `--issues none`).

### 4.1 Design Gate Classification

8 of 15 items carry at least one observable UI acceptance criterion (visible rendering, element presence/absence, colour, interaction, timing): `BLG-FE-102`, `BLG-FE-97`, `BLG-FE-104`, `BLG-FE-95`, `BLG-FE-96`, `BLG-FEAT-69`, `BLG-FEAT-70`, `BLG-FEAT-68`. `BLG-SPEC-73`'s AC is wording-only (copy alignment, no visual/colour/layout claim) — qualifies for the CLAUDE.md FI-P3-02 code-review exception, but does not remove the release-level classification since other items in scope carry genuine observable-rendering ACs.

**`design_gate_required = true` — N = 8 items classified as UI-facing. Run: `run design-gate --cycle 2026-07-12__release-v7.0`**

```yaml
# state.json update (STEP 4):
artifacts.stage4_backlog_slice: pass
artifacts.stage4_issue_manifest: pass
attributes.backlog_committed: true
attributes.design_gate_required: true
locks.backlog_lock.status: released
status: Committed
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** No matching rows in `scored_initiatives.md` for any of the 15 items (that file tracks larger initiatives, not this grain) — all estimates fall back to inline backlog `**Effort:**` fields; no advisory required.

| EPIC | Stories | Estimated effort (mid-point) |
|------|---------|-------------------------------|
| EPIC-01 | 5 | ~2.35 days |
| EPIC-02 | 7 | ~2.15 days |
| EPIC-03 | 3 | ~5.0 days |
| **Total** | **15** | **~9.5 days** |

Available capacity: ~12-14 days (solo developer, evenings/weekends — `workforce_capacity.md` baseline, unchanged since v6.9).

**Outcome: PASS.** ~9.5 of ~12-14 estimated days used — full, well-justified utilisation of sprint capacity (vs. v6.9's ~4-6 of ~12-14 days) with buffer retained for estimate variance; no phasing recommendation required.

```yaml
# state.json update (STEP 4.5):
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Roadmap Annotation (STEP 5)

No formal `## v7.0` roadmap section exists yet (Option (b) deferred at rebalance), so the `**Next planned release:**` line in `current_roadmap.md` §1 was annotated instead, per the prompt's fallback rule. Roadmap lock `RA:v7.0:2026-07-12__release-v7.0` acquired, annotation written with marker, transaction committed, lock released.

```yaml
# state.json update (STEP 5):
artifacts.roadmap_txn: committed
locks.roadmap_lock.status: released
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity / 5.7 Decision Record Integrity

**5.5 Cross-Stage Integrity:** All 3 S2 IDs (S2-01, S2-02, S2-03) map to exactly one EPIC each; all EPIC IDs (EPIC-01/02/03) in `stage4_backlog_slice.md` match the Execution Plan; all 4 RISK IDs (RISK-01..04) referenced in the EPIC table appear in the Risk Register; no orphaned references found.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` is not `present` (no escalations raised this cycle).

```yaml
# state.json update (STEP 5.5):
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```

---

## Publish Gate Evaluation

- `open_escalations`: empty — PASS
- `deferred_execution_blockers`: empty — PASS
- `stage4_5_capacity_check`: pass — PASS
- `stage5_5_cross_stage_integrity`: pass — PASS
- `stage5_7_decision_record_integrity`: not_applicable — PASS
- `stage1_readiness`, `stage3_5_model_integrity`: pass — PASS
- `plan_structured`, `plan_executable`, `backlog_committed`: true — PASS

**Gate passes. `status = Validated`, `publish_eligible = true`.**

Engine-specific completion: `docs/product/scope/scope--2026-07-12__release-v7.0-grid-view-parity-carryover-fixes.md` exists; `docs/product/decisions/decisions--2026-07-12__release-v7.0.md` exists; `locks.backlog_lock.status = released`; `locks.roadmap_lock.status = released`. All conditions met.
