**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Planning
**Cycle:** 2026-07-17__release-v7.5
**Release:** v7.5
**Last Updated:** 2026-07-17

---

# Release Plan — v7.5

## Readiness

### 1.1 Backlog Age Advisory
No spec/documentation-debt items appear in this release's scope candidates (`BLG-FE-115/116/117/118` are all Type: Frontend / UX). No advisory triggered.

### 1.2 Provisional-Target Advisory
All 4 scope candidates currently carry `Provisional-Target: v7.4` with a stale-target notice (filed at `groom backlog` 2026-07-17, since v7.4 shipped without them). 0/4 currently match the current release label. These will be updated to `Provisional-Target: v7.5` at STEP 4 backlog-slice commit. Scope-selection authority remains at STEP 2.

### 1.3 Design-Gate Language Scan
All 4 items are UI-facing with observable acceptance criteria (palette opens/closes, alert CRUD UI, bulk-select toolbar, saved-filter/calendar rendering) — design dependency detected for all 4. Surfaced at Pre-sprint Required Decisions checklist (see `cycle_summary.md`) and reflected in STEP 4.1 classification and the Risk Register (RISK-01) below.

### 1.4a Perennial-Return Check
`BLG-FE-115/116/117/118` were removed pre-seal from `2026-07-17__release-v7.4`'s sprint scope by `AMD-20260717-01` (hard-blocker amendment) after `run design-gate` found no approved design artefact for any of the 4 — root cause was structural: each item's plan scheduled artefact production as sprint-execution work sequenced *after* the point Design Gate evaluates, which cannot satisfy a gate that must clear *before* Sprint Planning. This is 1 prior occurrence, below the 2-consecutive-cycle mandatory-disposition threshold — but the identical root cause is unaddressed (no design artefacts produced since the amendment). Product Owner disposition (delegated authority, this session): **(a) Keep as conditional** — updated gate evidence differing from prior cycles: this release plan requires Head of UX & Design to produce design artefacts for all 4 items and `run design-gate` to re-evaluate and PASS **before** Sprint Planning seals, with artefact production explicitly scoped as a precursor step outside sprint-execution work (not repeating the v7.4 structural error). See RISK-01.

### 1.4b Within-Sprint Date Gate Classification
None of the 4 scope candidates carry a gate condition tied to a specific calendar clearing date — their blocking condition is design-artefact production status, not a date. No item requires mandatory conditional classification under this sub-check (RISK-01's conditional classification is driven by 1.4a instead).

### 1.4 Gate-Condition Proximity Scan

| Item | Gate condition | Current trajectory | Projected clear date |
|---|---|---|---|
| SI-02 (structured field, §5) | 20+ closed trades with linked trade plans | 0/11 trade plans linked (`position_id` set); `insufficient_data` drift, 9 trades in 90-day window | trajectory unknown — 7th consecutive byte-identical reading |

**SI-02 live re-check (direct production API, this session):** `GET /trade-plans` → 11 total, 0 linked (`position_id` set on none). `GET /trades` → 6 returned. `GET /analytics/behavioural-drift` → `insufficient_data`, `trade_count_in_window: 9`. Identical to the `2026-07-17__scheduled` rebalance reading (0/11 linked, insufficient_data, 9 trades) — **7th consecutive byte-identical reading**. Gate remains **NOT MET**. Not directly relevant to this release's scope (no trade/journal-linkage items in v7.5) — recorded for continuity of the tracked series only.

PO-02 (6+ months AI journals) / PO-04 (50+ trades with plans): not directly relevant to this release's scope (no scope items target these gates); not re-queried this session — carried forward from `2026-07-17__scheduled` rebalance reading, consistent with prior release-planning cycles' practice of not re-querying gates unrelated to in-scope items.

```yaml
# state.json update (STEP 1):
artifacts.stage1_readiness: pass
```

---

## Scope

Release v7.5 continues the UI Feature Expansion work named as anchor scope at DL-068 (v7.3) and planned but pre-seal-removed at v7.4 (`AMD-20260717-01`). No fresh idea intake or rebalance ran this session — scope is the 4 already-active, already-named P1 backlog items. All 4 classified **conditional** (not firm) per STEP 1.4a — see RISK-01.

| S2-ID | Backlog ID | Title | Effort |
|-------|-----------|-------|--------|
| S2-01 | BLG-FE-115 | Global command palette / cross-page search | M (~1–2 days) |
| S2-02 | BLG-FE-116 | User-defined custom price alerts | L (~3–5 days) |
| S2-03 | BLG-FE-117 | Bulk actions on list/table views | M (~1–2 days) |
| S2-04 | BLG-FE-118 | Saved filter views and calendar view | L (~3–5 days) |

### Items explicitly deferred
None — all 4 scope candidates carried into this release plan (conditional, per RISK-01).

```yaml
# state.json update (STEP 2):
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

4 EPICs, one per feature item — matches the EPIC-per-item split decision already made and ratified for these same items at v7.4 (`decisions--2026-07-17__release-v7.4.md`, resolving `BLG-GOV-248`: no shared data-model dependency, disjoint files/components, parallel execution preferred over one large cross-surface PR). No readiness-bundle EPIC needed this cycle — `BLG-SPEC-95` (npm deps `cmdk`/`react-day-picker`, shared UX/QA scaffolding) already shipped in v7.4.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Head of UX & Design; Frontend Specs & UX Documentation Owner | RISK-01 | Design Gate must PASS before Sprint Planning seals |
| EPIC-02 | S2-02 | Head of UX & Design; Frontend Specs & UX Documentation Owner; Backend Engineering Patterns Owner | RISK-01 | Design Gate must PASS before Sprint Planning seals |
| EPIC-03 | S2-03 | Head of UX & Design; Frontend Specs & UX Documentation Owner | RISK-01 | Design Gate must PASS before Sprint Planning seals |
| EPIC-04 | S2-04 | Head of UX & Design; Frontend Specs & UX Documentation Owner | RISK-01 | Design Gate must PASS before Sprint Planning seals |

All 4 EPICs may execute in parallel once unblocked — no cross-EPIC data-model dependency (per the v7.4 bundling analysis, unchanged).

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | Release-level | Recurrence of the v7.4 `AMD-20260717-01` blocker: all 4 items require Head of UX & Design artefacts that do not yet exist; the prior cycle's plans scheduled artefact production as sprint-execution work sequenced after Design Gate evaluates, which cannot satisfy a before-Sprint-Planning gate. | High | Head of UX & Design must produce design artefacts for all 4 items as a precursor step **before** `run design-gate --cycle 2026-07-17__release-v7.5` is invoked — not inside any EPIC's sprint-execution scope. Classified conditional (not firm) until Design Gate PASSes. Must-resolve-before-sprint-planning-seal — see Pre-sprint Planning Required Decisions in `cycle_summary.md`. | null |
| RISK-02 | Release-level | Cross-EPIC merge conflicts when 2+ of the 4 parallel EPIC branches are open as PRs simultaneously touching shared files (`execution_state.json`, `openapi.yaml`, `api_changelog.md`, `data_model.md`) — same structural risk flagged (but not exercised, since none of these EPICs reached sprint execution) at v7.4's own run manifest Carry-Forward #3. | Medium | Apply `CLAUDE.md` §8 Cross-EPIC Merge Conflict Resolution procedure if `CONFLICTING/DIRTY` status is reported; merge simplest EPIC first. | null |
| RISK-03 | EPIC-02 | `BLG-FE-116` (price alerts) requires a new backend data model + notification-pipeline integration in addition to frontend UI — largest scope-uncertainty item (L effort, ~3–5 days), no backend design work started. | Medium | Backend Engineering Patterns Owner to scope the data model and pipeline integration as part of EPIC-02's design-artefact precursor work (see RISK-01). | null |

```yaml
# state.json update (STEP 3):
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

Local check of this document's own ID model (full cross-stage check deferred to STEP 5.5):
- 4 S2 IDs (S2-01..04), each maps to exactly one EPIC-ID (EPIC-01..04) — 1:1, no orphans.
- 3 RISK IDs (RISK-01..03), each declares `Relates to:` either `Release-level` or a valid EPIC-ID referenced in the EPIC table — no orphans.
- No EPIC or RISK ID reused or skipped.

Result: PASS.

```yaml
# state.json update (STEP 3.5):
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Backlog Slice Commitment (STEP 4)

`stage4_backlog_slice.md` written — 4 EPICs/STs, all conditional. `claude/backlog/backlog.md` updated: Release Slice v7.5 section added (marker `RP:v7.5:2026-07-17__release-v7.5`), Provisional-Target updated v7.4→v7.5 on all 4 items, prior stale-target notices resolved. `stage4_issue_manifest.json` written (4 entries, `--issues none` this session — no GitHub issues created).

### STEP 4.1 — Design Gate Classification

All 4 ST items have delegation class `delegated_frontend`/observable UI acceptance criteria (palette rendering, alert CRUD UI, bulk-select toolbar, saved-filter/calendar rendering — all visible-rendering and interaction ACs).

**`design_gate_required = true` — 4 items classified as UI-facing.**

⚠ DESIGN GATE REQUIRED before plan sprint — 4 items classified as UI-facing. Run: `run design-gate --cycle 2026-07-17__release-v7.5`

```yaml
# state.json update (STEP 4):
artifacts.stage4_backlog_slice: pass
artifacts.stage4_issue_manifest: pass
attributes.backlog_committed: true
attributes.design_gate_required: true
status: Committed
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** No matching rows in `scored_initiatives.md` for any of the 4 EPICs (0 active-initiative rows, CPS = N/A) — using STEP 4 inline backlog-filed estimates for all 4; no advisory required.

| EPIC | Backlog item | Effort | Midpoint (days) |
|------|-------------|--------|------------------|
| EPIC-01 | BLG-FE-115 | M (~1–2 days) | 1.5 |
| EPIC-02 | BLG-FE-116 | L (~3–5 days) | 4.0 |
| EPIC-03 | BLG-FE-117 | M (~1–2 days) | 1.5 |
| EPIC-04 | BLG-FE-118 | L (~3–5 days) | 4.0 |

**Total estimated effort:** ~11–14 days (midpoint 11.0). **Available capacity:** ~24–28 days/sprint (`workforce_capacity.md`, effective 2026-07-17, DL-069). Excludes RISK-01's design-artefact production, which is precursor work by Head of UX & Design sequenced before Design Gate, not sprint-execution developer capacity.

Total effort is well within the capacity baseline even at the high end of each range (14 of 24–28 days, ~50–58% of ceiling).

**Outcome: PASS** — no phasing recommendation required.

```yaml
# state.json update (STEP 4.5):
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation

### 5.5 Cross-Stage Integrity
- S2 IDs → EPIC mapping: S2-01→EPIC-01, S2-02→EPIC-02, S2-03→EPIC-03, S2-04→EPIC-04 — all 4 map 1:1, no orphans.
- EPIC IDs in `stage4_backlog_slice.md` (EPIC-01..04) match the Execution Plan EPIC table exactly — no drift.
- RISK IDs referenced in the EPIC table (RISK-01, RISK-01, RISK-01, RISK-01) all appear in the Risk Register Summary, plus RISK-02/RISK-03 (Release-level/EPIC-02, correctly not referenced from the EPIC table's per-row Key Risk column since only one risk column exists per row — both still valid Risk Register entries with explicit `Relates to`) — no orphaned RISK IDs.
- Backlog source IDs (`BLG-FE-115/116/117/118`) consistent across `release_plan.md`, `stage4_backlog_slice.md`, `stage4_issue_manifest.json`, and `backlog.md` Release Slice table — no drift.

Result: **PASS**.

### 5.7 Decision Record Integrity
Not applicable — `artifacts.escalations` is `not_started` (no escalations raised this cycle; RISK-01 was mitigated via explicit PO disposition at STEP 1.4a, not escalated). Per STEP 5.5 rule, this sub-check is skipped.

```yaml
# state.json update (STEP 5.5):
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
